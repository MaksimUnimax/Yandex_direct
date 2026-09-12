// QA ONLY: preserved deterministic double lacks openKeyCursor. Extend only that
// API with a primary-key tiebreak for equal index keys, needed by Patch A cleanup.
// This is NOT real IndexedDB/resource evidence. Never included in installable code.
import * as fake from '../inputs/idb_test_double.mjs';
export * from '../inputs/idb_test_double.mjs';
fake.IDBIndex.prototype.openKeyCursor=function(range){
 const s=this.store,tx=s.transaction,field=this.definition.path;
 const request={};let last=null;
 const next=()=>{
  const rows=tx.rows(s.name).filter(v=>range.includes(v[field])&&(last===null||v[s.definition.keyPath]>last))
   .sort((a,b)=>a[s.definition.keyPath]<b[s.definition.keyPath]?-1:1);
  if(!rows.length)return null;
  const row=rows[0];last=row[s.definition.keyPath];
  return{key:row[field],primaryKey:last,continue(){tx.enqueue(next,request);}};
 };
 tx.enqueue(next,request);return request;
};
