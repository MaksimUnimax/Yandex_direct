import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const source=fs.readFileSync(new URL('../candidate/b8/search_async_export.js',import.meta.url),'utf8');
const ctx=vm.createContext({TextEncoder,console,URL});ctx.globalThis=ctx;vm.runInContext(source,ctx);
const E=ctx.YMBSearchAsyncExport, owner='https://chatgpt.com|owner', folderId='folder', jobId='job',deliveryId='delivery';
const parse=x=>JSON.parse(JSON.stringify(x));
function fixture(n=4,options={}){
 const items=Array.from({length:n},(_,index)=>({job_id:jobId,index,query:`💎 тест ${index}`,state:'SUCCEEDED',operation_id:`op-${index}`,poll_count:1}));
 const results=items.map(i=>({job_id:jobId,index:i.index,operation_id:i.operation_id,raw_text:JSON.stringify({id:i.operation_id,done:true,response:{rawData:'cmF3'}}),normalized:{results:[{rank:1,url:`https://example.test/${i.index}`,title:'текст\n" 💎',domain:'example.test',snippet:'\\t'}]}}));
 let summary={job_id:jobId,total:n,revision:10,counts:{SUCCEEDED:n},busy:false,all_successful:true};
 const files=new Map(),stats={reads:0,stage:0,deleted:0,peeks:0,summary:0};
 const store={
  async peekNext(a){if(a.owner!==owner)throw Object.assign(new Error(),{code:'WRONG_OWNER'});stats.peeks++;return{folder_id:folderId,parameters:{region:'225',page:0,groupsOnPage:10},progress:{...summary,counts:{...summary.counts}}};},
  async readItem(j,o,i){assert.equal(j,jobId);assert.equal(o,owner);stats.reads++;return items[i];},
  async readResult(j,o,i){assert.equal(o,owner);return results[i];},
  async getSummary(j,o){assert.equal(o,owner);stats.summary++;return{...summary,counts:{...summary.counts}};}
 };
 const artifacts={
  async getMeta(k){return files.get(k)?.descriptor;},
  async stageTextArtifact(a){stats.stage++;const descriptor={artifact_key:a.artifactKey,delivery_id:a.deliveryId,filename:a.filename,status:'ready',byte_length:Buffer.byteLength(a.text)};files.set(a.artifactKey,{text:a.text,descriptor});return descriptor;},
  async deleteArtifact(k){stats.deleted++;files.delete(k);}
 };
 let authorized=true;
 const api=E.create({store,artifacts,authorize:async()=>authorized,now:()=>1000,...options});
 return {api,store,artifacts,items,results,files,stats,get summary(){return summary;},set summary(v){summary=v;},set authorized(v){authorized=v;},args:{jobId,owner,deliveryId,folderId},run(a={}){return api.stagePage({...this.args,...a});}};
}
function rejects(fn,code){return assert.rejects(fn,e=>e.code===code);}
const samples=['','ASCII','Кириллица','中文','💎','\ud800','\udc00','\ud800x','\n\r\t\b\f\u0001','"\\','\u2028\u2029',null,true,false,0,-0,1.234,1e30,[1,'💎'],{a:undefined,b:'é',nested:{x:[false,null]}}];
for(let i=0;i<samples.length;i++)test(`exact UTF8 JSON budget ${i}`,()=>{
 const expected=Buffer.byteLength(JSON.stringify(samples[i]));assert.equal(E.jsonBytes(samples[i],expected),expected);
 assert.throws(()=>E.jsonBytes(samples[i],expected-1),e=>e.code==='EXPORT_BYTE_LIMIT');
});
test('budget rejects cyclic, custom, accessor, sparse, non-JSON and deeply nested data without executing it',()=>{
 const cyc={};cyc.x=cyc;let calls=0;
 const getter={get x(){calls++;return 1;}};
 for(const value of [cyc,getter,new Date(),new Uint8Array(2),{toJSON(){calls++;}},NaN,Infinity,1n,()=>1,[undefined],Array(3)])assert.throws(()=>E.jsonBytes(value,1000));
 assert.equal(calls,0);let deep={};for(let i=0;i<35;i++)deep={x:deep};assert.throws(()=>E.jsonBytes(deep,10000),e=>e.code==='EXPORT_COMPLEXITY_LIMIT');
});
test('plain JSON exact counters, provenance, original raw and normalized rows, no payload in report',async()=>{
 const f=fixture();const r=await f.run();const content=JSON.parse(f.files.get(r.descriptor.artifact_key).text);
 assert.equal(r.report.bytes,Buffer.byteLength(JSON.stringify(content)+'\n'));assert.equal(content.items.length,4);assert.equal(content.parameters.region,'225');
 assert.deepEqual(content.items[0],{item:f.items[0],result:f.results[0]});assert.equal(content.page.result_row_count,4);
 assert.equal(r.report.has_more,false);assert.equal(r.report.all_job_items_in_this_file,true);assert.equal(r.report.next_after,3);
 for(const word of ['raw_text','normalized','query','cmF3'])assert.equal(JSON.stringify(r.report).includes('"'+word+'"'),false);
 assert.equal(f.stats.stage,1);assert.equal(f.stats.reads,4);
});
test('every record including failed, cancelled and UNKNOWN preserved; never fabricate empty raw',async()=>{
 const f=fixture();for(const [index,state]of ['FAILED','CANCELLED','UNKNOWN','PARSE_FAILED'].entries()){f.items[index].state=state;if(index<3)f.results[index]=undefined;}
 f.summary={...f.summary,counts:{FAILED:1,CANCELLED:1,UNKNOWN:1,PARSE_FAILED:1},all_successful:false};
 const r=await f.run(),content=JSON.parse(f.files.get(r.descriptor.artifact_key).text);
 assert.equal(content.items.length,4);assert.equal(content.items[0].result,null);assert.equal(content.items[3].result.raw_text,f.results[3].raw_text);
 assert.equal(r.report.items_with_raw,1);assert.equal(content.job_summary.all_successful,false);
});
test('multiple explicit pages preserve exact 1500 ids without full-dataset fetch',async()=>{
 const f=fixture(1500);let after=-1,revision=null;const ids=[];
 for(let i=0;i<60;i++){
  const r=await f.run({after,revision,deliveryId:'page-'+i});assert.equal(r.report.item_count,25);
  const page=JSON.parse(f.files.get(r.descriptor.artifact_key).text);ids.push(...page.items.map(r=>r.item.index));
  after=r.report.next_after;revision=r.report.revision;assert.equal(r.report.has_more,i<59);await f.api.discard(r.descriptor);
 }
 assert.deepEqual(ids,Array.from({length:1500},(_,i)=>i));assert.equal(f.stats.reads,1500);assert.equal(f.files.size,0);
});
test('byte cap yields exact next record, no truncation or skipped oversized record',async()=>{
 const f=fixture(5,{maxPageBytes:4096});for(const r of f.results)r.raw_text='x'.repeat(500);
 const a=await f.run();assert.ok(a.report.item_count>0&&a.report.item_count<5);assert.equal(a.report.next_after,a.report.item_count-1);assert.equal(a.report.has_more,true);
 const b=await f.run({after:a.report.next_after,revision:a.report.revision,deliveryId:'page-next'});
 const p=JSON.parse(f.files.get(b.descriptor.artifact_key).text);assert.equal(p.items[0].item.index,a.report.next_after+1);
});
test('single oversized record fails BEFORE staging and without mutating source',async()=>{
 const f=fixture(1,{maxPageBytes:4096});f.results[0].raw_text='x'.repeat(1e6);
 await rejects(()=>f.run(),'EXPORT_SINGLE_RECORD_TOO_LARGE');assert.equal(f.stats.stage,0);assert.equal(f.results[0].raw_text.length,1e6);assert.equal(f.summary.revision,10);
});
test('missing item or result provenance fails closed',async()=>{
 for(const mutate of [f=>f.items[0]=null,f=>f.items[0].index=99,f=>f.results[0].operation_id='other',f=>f.results[0].job_id='other']){
  const f=fixture();mutate(f);await assert.rejects(()=>f.run());assert.equal(f.stats.stage,0);
 }
});
test('missing stored raw/normalized cannot be called a complete result',async()=>{
 const f=fixture();delete f.results[0].raw_text;await rejects(()=>f.run(),'EXPORT_RAW_RESULT_MISSING');
 const g=fixture();delete g.results[0].normalized;await rejects(()=>g.run(),'EXPORT_NORMALIZED_RESULT_MISSING');
});
test('revision required for continuation and mismatches refused',async()=>{
 const f=fixture();await rejects(()=>f.run({after:0}),'EXPORT_REVISION_REQUIRED');await rejects(()=>f.run({revision:9}),'EXPORT_REVISION_CHANGED');assert.equal(f.stats.stage,0);
});
test('source mutation during reading rejects whole page BEFORE staging',async()=>{
 const f=fixture();const read=f.store.readResult;f.store.readResult=async(...a)=>{const r=await read(...a);f.summary.revision++;return r;};
 await rejects(()=>f.run(),'EXPORT_REVISION_CHANGED');assert.equal(f.stats.stage,0);
});
test('mutation during staging deletes only staged export, never source',async()=>{
 const f=fixture();const stage=f.artifacts.stageTextArtifact;f.artifacts.stageTextArtifact=async a=>{const d=await stage(a);f.summary.revision++;return d;};
 await rejects(()=>f.run(),'EXPORT_REVISION_CHANGED');assert.equal(f.files.size,0);assert.equal(f.stats.deleted,1);assert.equal(f.results.length,4);
});
test('authorization revocation before or during stage stops and cleans up',async()=>{
 const f=fixture();f.authorized=false;await rejects(()=>f.run(),'EXPORT_NOT_AUTHORIZED');assert.equal(f.stats.peeks,0);
 const g=fixture();const stage=g.artifacts.stageTextArtifact;g.artifacts.stageTextArtifact=async a=>{const d=await stage(a);g.authorized=false;return d;};
 await rejects(()=>g.run(),'EXPORT_NOT_AUTHORIZED');assert.equal(g.files.size,0);
});
test('wrong owner/folder and active jobs are refused',async()=>{
 const f=fixture();await rejects(()=>f.run({owner:'wrong'}),'WRONG_OWNER');await rejects(()=>f.run({folderId:'wrong'}),'EXPORT_FOLDER_MISMATCH');
 f.summary.busy=true;await rejects(()=>f.run(),'EXPORT_JOB_BUSY');f.summary.busy=false;f.summary.counts.SUBMITTING=1;await rejects(()=>f.run(),'EXPORT_JOB_BUSY');assert.equal(f.stats.stage,0);
});
test('abort before staging and after stage produces no orphan ready file',async()=>{
 const f=fixture();const c=new AbortController();c.abort();await rejects(()=>f.run({signal:c.signal}),'EXPORT_ABORTED');assert.equal(f.stats.stage,0);
 const g=fixture();const d=new AbortController();const stage=g.artifacts.stageTextArtifact;g.artifacts.stageTextArtifact=async a=>{const v=await stage(a);d.abort();return v;};
 await rejects(()=>g.run({signal:d.signal}),'EXPORT_ABORTED');assert.equal(g.files.size,0);
});
test('staging response checksum/length contract mismatch cleans up',async()=>{
 const f=fixture();const stage=f.artifacts.stageTextArtifact;f.artifacts.stageTextArtifact=async a=>({...await stage(a),byte_length:1});
 await rejects(()=>f.run(),'EXPORT_ARTIFACT_MISMATCH');assert.equal(f.files.size,0);
});
test('ambiguous write failure cleans export, cleanup failure never masked',async()=>{
 const f=fixture();const stage=f.artifacts.stageTextArtifact;f.artifacts.stageTextArtifact=async a=>{await stage(a);throw Object.assign(new Error(),{code:'WRITE_FAIL'});};
 await rejects(()=>f.run(),'WRITE_FAIL');assert.equal(f.files.size,0);
 const g=fixture();g.artifacts.stageTextArtifact=async()=>{throw new Error('write');};g.artifacts.deleteArtifact=async()=>{throw new Error('delete');};await rejects(()=>g.run(),'EXPORT_CLEANUP_REQUIRED');
});
test('busy exporter cannot stage two same-delivery operations and existing artifact is not overwritten',async()=>{
 const f=fixture();let release;const original=f.store.peekNext;f.store.peekNext=async a=>{await new Promise(r=>release=r);return original(a);};
 const p=f.run();await new Promise(r=>setImmediate(r));await rejects(()=>f.run(),'EXPORT_BUSY');release();const r=await p;
 f.store.peekNext=original;await rejects(()=>f.run(),'EXPORT_DELIVERY_ALREADY_STAGED');assert.equal(f.files.size,1);assert.equal(f.stats.stage,1);await f.api.discard(r.descriptor);assert.equal(f.files.size,0);
});
test('invalid inputs and unsupported budgets have no store or staging side effects',async()=>{
 const f=fixture();for(const input of [{jobId:'../../bad'},{deliveryId:'a/b'},{after:1500},{after:-2},{limit:0},{limit:26},{revision:-1}])await assert.rejects(()=>f.run(input));assert.equal(f.stats.peeks,0);
 for(const n of [undefined,-1,0,4095,16*1024*1024+1,NaN,Infinity]){if(n===undefined)continue;assert.throws(()=>E.create({store:f.store,artifacts:f.artifacts,authorize:async()=>true,maxPageBytes:n}));}
});
test('no startup/provider/network/normalization/SourceStorage mutation dependency',()=>{
 for(const pattern of [/\bfetch\s*\(/,/setInterval\s*\(/,/chrome\.storage/,/finishSubmit\s*\(/,/finishCollect\s*\(/,/createJob\s*\(/])assert.equal(pattern.test(source),false);
});
