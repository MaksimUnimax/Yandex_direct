// Deterministic transactional test double, NOT a browser/IndexedDB conformance proof.
// Only APIs used by search_async_store are supported. Never packaged with extension.
const copy=x=>x===undefined?undefined:structuredClone(x);
const keyOf=k=>JSON.stringify(k);
function cmp(a,b){if(Array.isArray(a)&&Array.isArray(b)){for(let i=0;i<Math.min(a.length,b.length);i++){const c=cmp(a[i],b[i]);if(c)return c;}return Math.sign(a.length-b.length);}return a===b?0:a<b?-1:1;}
function at(v,p){return Array.isArray(p)?p.map(k=>v[k]):v[p];}
const failure=(name)=>Object.assign(new Error(name),{name});
export class IDBKeyRange {
  constructor(lower,upper,lowerOpen=false,upperOpen=false){Object.assign(this,{lower,upper,lowerOpen,upperOpen});}
  static only(k){return new IDBKeyRange(k,k);}
  static bound(a,b,lo=false,uo=false){return new IDBKeyRange(a,b,lo,uo);}
  includes(k){return k!==undefined&&cmp(k,this.lower)>=(this.lowerOpen?1:0)&&cmp(k,this.upper)<=(this.upperOpen?-1:0);}
}
class Request{constructor(){this.result=undefined;this.error=null;}}
class Tx {
  constructor(db,names,mode){this.db=db;this.names=Array.isArray(names)?names:[names];this.mode=mode;this.tasks=[];this.overlay=new Map();this.active=true;this.running=false;this.timer=null;this.error=null;db.queue.push(this);db.start();}
  objectStore(name){if(!this.names.includes(name))throw failure('NotFoundError');return new IDBObjectStore(this,name);}
  enqueue(fn,request=new Request()) {if(!this.active)throw failure('TransactionInactiveError');this.tasks.push({fn,request});this.schedule();return request;}
  schedule(){if(!this.running||this.timer||!this.active)return;this.timer=setImmediate(()=>{this.timer=null;this.step();});}
  step(){if(!this.active)return;const task=this.tasks.shift();if(!task){this.complete();return;}try{task.request.result=task.fn();task.request.onsuccess?.({target:task.request});}catch(e){task.request.error=e;task.request.onerror?.({target:task.request});this.abort(e);}this.schedule();}
  record(name,k){const changes=this.overlay.get(name);if(changes?.has(keyOf(k)))return copy(changes.get(keyOf(k)));return copy(this.db.stores.get(name).data.get(keyOf(k)));}
  rows(name){const all=new Map(this.db.stores.get(name).data);for(const[k,v]of this.overlay.get(name)||[])v===undefined?all.delete(k):all.set(k,v);return [...all.values()];}
  write(name,k,v){if(this.mode!=='readwrite'&&this.mode!=='versionchange')throw failure('ReadOnlyError');if(!this.overlay.has(name))this.overlay.set(name,new Map());this.overlay.get(name).set(keyOf(k),copy(v));}
  complete(){if(!this.active)return;for(const[name,rows]of this.overlay){const data=this.db.stores.get(name).data;for(const[k,v]of rows)v===undefined?data.delete(k):data.set(k,v);}this.active=false;this.oncomplete?.();this.db.queue.shift();this.db.start();}
  abort(e=failure('AbortError')){if(!this.active)throw failure('InvalidStateError');this.active=false;this.error=e;clearImmediate(this.timer);this.timer=null;setImmediate(()=>{this.onabort?.();if(this.db.queue[0]===this)this.db.queue.shift();else this.db.queue=this.db.queue.filter(t=>t!==this);this.db.start();});}
}
export class IDBObjectStore{
  constructor(tx,name){this.transaction=tx;this.name=name;this.definition=tx.db.stores.get(name);this.indexNames={contains:n=>this.definition.indexes.has(n)};}
  createIndex(n,p,options){this.definition.indexes.set(n,{path:p,unique:!!options?.unique});}
  index(n){return new IDBIndex(this,n);}
  get(k){return this.transaction.enqueue(()=>{if(k instanceof IDBKeyRange)return copy(this.transaction.rows(this.name).filter(v=>k.includes(at(v,this.definition.keyPath))).sort((a,b)=>cmp(at(a,this.definition.keyPath),at(b,this.definition.keyPath)))[0]);return this.transaction.record(this.name,k);});}
  put(value){return this._put(value,false);}
  add(value){return this._put(value,true);}
  _put(value,add){return this.transaction.enqueue(()=>{const k=at(value,this.definition.keyPath);if(add&&this.transaction.record(this.name,k)!==undefined)throw failure('ConstraintError');for(const idx of this.definition.indexes.values()){if(!idx.unique)continue;const ik=at(value,idx.path);if(ik===undefined)continue;if(this.transaction.rows(this.name).some(r=>cmp(at(r,this.definition.keyPath),k)!==0&&at(r,idx.path)!==undefined&&cmp(at(r,idx.path),ik)===0))throw failure('ConstraintError');}this.transaction.write(this.name,k,value);return k;});}
  delete(k){return this.transaction.enqueue(()=>this.transaction.write(this.name,k,undefined));}
  getAll(){return this.transaction.enqueue(()=>copy(this.transaction.rows(this.name)));}
  openCursor(range){return cursor(this,range,null);}
}
export class IDBIndex{
  constructor(store,name){this.store=store;this.definition=store.definition.indexes.get(name);if(!this.definition)throw failure('NotFoundError');}
  get(k){const s=this.store;return s.transaction.enqueue(()=>copy(s.transaction.rows(s.name).filter(v=>{const a=at(v,this.definition.path);return k instanceof IDBKeyRange?k.includes(a):a!==undefined&&cmp(a,k)===0;}).sort((a,b)=>cmp(at(a,this.definition.path),at(b,this.definition.path)))[0]));}
  openCursor(range){return cursor(this.store,range,this.definition.path);}
}
function cursor(store,range,indexPath){const tx=store.transaction;const path=indexPath||store.definition.keyPath;const request=new Request();let last=null;
  const advance=()=>{const row=tx.rows(store.name).filter(v=>range.includes(at(v,path))&&(last===null||cmp(at(v,path),last)>0)).sort((a,b)=>cmp(at(a,path),at(b,path)))[0];if(!row)return null;last=at(row,path);return {value:copy(row),primaryKey:at(row,store.definition.keyPath),update(v){return store.put(v);},continue(){tx.enqueue(advance,request);}};};tx.enqueue(advance,request);return request;
}
class Database{
  constructor(name){this.name=name;this.stores=new Map();this.queue=[];this.objectStoreNames={contains:n=>this.stores.has(n)};}
  start(){const t=this.queue[0];if(t&&!t.running){t.running=true;t.schedule();}}
  createObjectStore(name,opt){this.stores.set(name,{keyPath:opt.keyPath,data:new Map(),indexes:new Map()});return new IDBObjectStore({db:this,mode:'versionchange'},name);}
  transaction(names,mode){return new Tx(this,names,mode);}
  close(){}
}
const dbs=new Map();
export const indexedDB={open(name,version){const r=new Request();setImmediate(()=>{let db=dbs.get(name);const upgrade=!db;if(!db){db=new Database(name);dbs.set(name,db);}r.result=db;if(upgrade)r.onupgradeneeded?.();r.onsuccess?.();});return r;}};
