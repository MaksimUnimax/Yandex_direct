import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import vm from 'node:vm';import crypto from 'node:crypto';
import * as fake from './idb_artifact_fixture.mjs';
const source=fs.readFileSync(new URL('../inputs/file_artifact_store.js',import.meta.url));
assert.equal(crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+source.length+'\0'),source])).digest('hex'),'7d021387406cd8c9e222537c745cc697e009c928','unchanged Patch A bytes');
const ctx=vm.createContext({...fake,crypto:crypto.webcrypto,TextEncoder,Uint8Array,ArrayBuffer,console});ctx.globalThis=ctx;vm.runInContext(source.toString(),ctx);vm.runInContext(fs.readFileSync(new URL('../candidate/b8/search_async_export.js',import.meta.url),'utf8'),ctx);
const A=ctx.YMBFileArtifactStore;let serial=0;
const req=r=>new Promise((res,rej)=>{r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error);});
async function countChunks(key){const db=await req(fake.indexedDB.open(A.DB_NAME,A.DB_VERSION));const rows=await req(db.transaction('chunks','readonly').objectStore('chunks').getAll());db.close();return rows.filter(x=>x.artifact_key===key).length;}
async function textOf(d){const decoder=new TextDecoder('utf8',{fatal:true});let text='';for(let i=0;i<d.chunk_count;i++){const c=await A.getChunk(d.artifact_key,i);assert.equal(c.sha256,crypto.createHash('sha256').update(c.bytes).digest('hex'));assert.ok(c.bytes.byteLength<=256*1024);text+=decoder.decode(c.bytes,{stream:true});}return text+decoder.decode();}
function setup(rawSize=1024){const id='artifact'+(++serial);const s={job_id:id,total:2,revision:3,counts:{SUCCEEDED:1,UNKNOWN:1},busy:false};
 const store={async peekNext(){return {folder_id:'folder',parameters:{region:'225'},progress:{...s}};},async getSummary(){return{...s};},
  async readItem(j,o,i){return{job_id:id,index:i,query:'браслет\n💎',state:i?'UNKNOWN':'SUCCEEDED',operation_id:i?undefined:'op-1'};},
  async readResult(j,o,i){return i?null:{job_id:id,index:i,operation_id:'op-1',raw_text:'Ж💎'.repeat(Math.ceil(rawSize/6)),normalized:{results:[{rank:1,url:null,title:'Сохраняем даже без URL'}]}};}};
 const api=ctx.YMBSearchAsyncExport.create({store,artifacts:A,authorize:async()=>true,now:()=>1});
 return {id,s,store,api,args:{jobId:id,owner:'owner',folderId:'folder',deliveryId:id}};}
test('actual Patch A binary stage / read / per-chunk SHA / cleanup preserves export JSON and Unicode',async()=>{
 const f=setup(1024*1024);const r=await f.api.stagePage(f.args);const text=await textOf(r.descriptor);const json=JSON.parse(text);
 assert.equal(json.items[0].result.raw_text,(await f.store.readResult()).raw_text);assert.equal(json.items[0].result.normalized.results[0].url,null);assert.equal(json.items[1].result,null);
 assert.equal(Buffer.byteLength(text),r.report.bytes);assert.ok(r.descriptor.chunk_count>1);assert.equal(await countChunks(r.descriptor.artifact_key),r.descriptor.chunk_count);
 await f.api.discard(r.descriptor);assert.equal(await A.getMeta(r.descriptor.artifact_key),undefined);assert.equal(await countChunks(r.descriptor.artifact_key),0);
});
test('unchanged Patch A handles plain legacy text and several deliveries independently',async()=>{
 const d1=await A.stageTextArtifact({artifactKey:'legacy-1',deliveryId:'d1',filename:'old.txt',text:'старый результат'});
 const f=setup(20000),d2=(await f.api.stagePage(f.args)).descriptor;
 assert.equal(await textOf(d1),'старый результат');await f.api.discard(d2);assert.equal(await textOf(d1),'старый результат');await A.deleteArtifact(d1.artifact_key);
});
test('each requested chunk reads a single record, not the whole chunk store',async()=>{
 const f=setup(1024*1024);const d=(await f.api.stagePage(f.args)).descriptor;
 const oldGet=fake.IDBObjectStore.prototype.get,all=fake.IDBObjectStore.prototype.getAll;let reads=0;
 fake.IDBObjectStore.prototype.get=function(...a){if(this.name==='chunks')reads++;return oldGet.apply(this,a);};
 fake.IDBObjectStore.prototype.getAll=function(){throw new Error('no whole store read');};
 try{await A.getChunk(d.artifact_key,0);assert.equal(reads,1);await A.getChunk(d.artifact_key,d.chunk_count-1);assert.equal(reads,2);}finally{fake.IDBObjectStore.prototype.get=oldGet;fake.IDBObjectStore.prototype.getAll=all;}
 await f.api.discard(d);
});
test('actual binary staging transaction failure does not leave a partial export',async()=>{
 const f=setup();const put=fake.IDBObjectStore.prototype.put;
 fake.IDBObjectStore.prototype.put=function(v,...rest){if(this.name==='chunks')throw new Error('disk unavailable');return put.call(this,v,...rest);};
 try{await assert.rejects(()=>f.api.stagePage(f.args));}finally{fake.IDBObjectStore.prototype.put=put;}
 assert.equal(await A.getMeta('async-export:'+f.id),undefined);assert.equal(await countChunks('async-export:'+f.id),0);
});
test('export source revision changes after real stage: chunks and meta removed but source remains readable',async()=>{
 const f=setup(1024*1024);const artifactProxy={...A,async stageTextArtifact(a){const d=await A.stageTextArtifact(a);f.s.revision++;return d;}};
 const api=ctx.YMBSearchAsyncExport.create({store:f.store,artifacts:artifactProxy,authorize:async()=>true});
 await assert.rejects(()=>api.stagePage(f.args),e=>e.code==='EXPORT_REVISION_CHANGED');assert.equal(await countChunks('async-export:'+f.id),0);assert.equal(await A.getMeta('async-export:'+f.id),undefined);assert.ok((await f.store.readResult()).raw_text);
});
