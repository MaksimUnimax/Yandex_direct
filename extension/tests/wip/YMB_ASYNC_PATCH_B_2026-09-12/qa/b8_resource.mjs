// Node-only resource diagnostics of bounded pages + unchanged Patch A. NOT Chrome
// RSS, real IndexedDB, DOM File/DataTransfer, or a full extension release gate.
import fs from 'node:fs';import vm from 'node:vm';import crypto from 'node:crypto';import assert from 'node:assert/strict';
import * as fake from './idb_artifact_fixture.mjs';
const ctx=vm.createContext({...fake,crypto:crypto.webcrypto,TextEncoder,Uint8Array,ArrayBuffer,console});ctx.globalThis=ctx;
for(const p of ['../inputs/file_artifact_store.js','../candidate/b8/search_async_export.js'])vm.runInContext(fs.readFileSync(new URL(p,import.meta.url),'utf8'),ctx);
const A=ctx.YMBFileArtifactStore,E=ctx.YMBSearchAsyncExport;
const out=new URL('../evidence/B8_RESOURCE.jsonl',import.meta.url);fs.writeFileSync(out,'');
const emit=v=>{const s=JSON.stringify(v)+'\n';fs.appendFileSync(out,s);process.stdout.write(s);};
const mem=()=>({rss:process.memoryUsage().rss,heapUsed:process.memoryUsage().heapUsed,arrayBuffers:process.memoryUsage().arrayBuffers});
emit({venue:'Node '+process.version+' / preserved IDB test double / forced GC between cycles, not Chrome',source_sha256:crypto.createHash('sha256').update(fs.readFileSync(new URL('../candidate/b8/search_async_export.js',import.meta.url))).digest('hex'),page_cap_bytes:E.MAX_PAGE_BYTES,bytes_per_source_record:1024*1024});
const originalGet=fake.IDBObjectStore.prototype.get,originalAll=fake.IDBObjectStore.prototype.getAll;let chunkReads=0;
fake.IDBObjectStore.prototype.get=function(...a){if(this.name==='chunks')chunkReads++;return originalGet.apply(this,a);};
fake.IDBObjectStore.prototype.getAll=function(){throw new Error('Full-store materialization prohibited in this path');};
try{
 for(const [cycle,mb]of [1,10,32,64,64,64].entries()){
  global.gc?.();const before=mem(),started=performance.now();const job='scale-'+cycle;
  const summary={job_id:job,total:mb,revision:1,busy:false,counts:{RESULT_SAVED:mb},all_successful:false};let reads=0;
  const store={async peekNext(){return{folder_id:'folder',parameters:{region:'225'},progress:summary};},async getSummary(){return summary;},
   async readItem(j,o,i){return{job_id:job,index:i,state:'RESULT_SAVED',query:'query '+i,operation_id:'op-'+i};},
   async readResult(j,o,i){reads++;return{job_id:job,index:i,operation_id:'op-'+i,raw_text:'x'.repeat(1024*1024-String(i).length)+i};}};
  const api=E.create({store,artifacts:A,authorize:async()=>true});let after=-1,revision=null,pages=0,exported=0,maxPage=0,stagePeak=before.rss;const startChunks=chunkReads;
  for(;;){
   const r=await api.stagePage({jobId:job,owner:'owner',folderId:'folder',deliveryId:job+'-page-'+pages,after,revision});
   stagePeak=Math.max(stagePeak,process.memoryUsage().rss);maxPage=Math.max(maxPage,r.report.bytes);exported+=r.report.item_count;pages++;
   let total=0;
   for(let i=0;i<r.descriptor.chunk_count;i++){
    const c=await A.getChunk(r.descriptor.artifact_key,i);assert.ok(c.bytes.byteLength<=256*1024);
    assert.equal(c.sha256,crypto.createHash('sha256').update(c.bytes).digest('hex'));total+=c.bytes.byteLength;
   }
   assert.equal(total,r.report.bytes);await api.discard(r.descriptor);assert.equal(await A.getMeta(r.descriptor.artifact_key),undefined);
   if(!r.report.has_more)break;after=r.report.next_after;revision=r.report.revision;
  }
  assert.equal(exported,mb);assert.ok(maxPage<=E.MAX_PAGE_BYTES);assert.ok(reads<=mb+pages);global.gc?.();
  emit({cycle:cycle+1,source_payload_mib:mb,status:'PASS',exported_records:exported,pages,source_record_reads:reads,chunk_reads:chunkReads-startChunks,max_page_bytes:maxPage,
   before,after:mem(),sampled_stage_peak_rss:stagePeak,process_max_rss_kib:process.resourceUsage().maxRSS,duration_ms:Math.round(performance.now()-started),source_deleted:false});
 }
}finally{fake.IDBObjectStore.prototype.get=originalGet;fake.IDBObjectStore.prototype.getAll=originalAll;}
emit({status:'PASS',browser_resource_proof:'NOT_RUN',provider_calls:0,release_allowed:false});
