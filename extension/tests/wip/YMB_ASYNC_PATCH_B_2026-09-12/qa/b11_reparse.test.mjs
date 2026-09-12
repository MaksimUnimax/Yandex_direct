// Real complete worker and existing normalizer/store; Chrome/IDB are fixtures.
// All setup records are synthetic. No provider calls, including setup.
import test from 'node:test';import assert from 'node:assert/strict';import crypto from 'node:crypto';
import {loadWorker,KEY} from './b10_full_worker_harness.mjs';
const full=process.env.YMB_FULL;
const xml='<yandexsearch><response><found priority="all">1</found><results><grouping><group><doc><url>https://example.test/kept</url><title>💎 Saved</title></doc></group></grouping></results></response></yandexsearch>';
const text=raw=>'SEARCH_ASYNC_BATCH_API_V1 '+JSON.stringify(raw);
const send=(h,raw,token=crypto.randomUUID())=>h.dispatch({type:'WS_EXECUTE_MANUAL_BLOCK',conversation_key:KEY,manual_request_token:token,block_text:text(raw)});
async function finish(h){const e=h.data.wsmb_outbox?.[KEY];if(e)await h.dispatch({type:'WS_MANUAL_DELIVERY_COMPLETE',conversation_key:KEY,delivery_id:e.delivery_id,delivery_confirmed:true,confirmation_basis:'microphone',composer_empty:true});}
const envelope=r=>JSON.parse(r.report_text.slice(r.report_text.indexOf('\n')+1));
async function setup({broken=false,state='PARSE_FAILED',owner=KEY}={}){
 const h=await loadWorker(full);h.seedBoundChat();const jobId='repair-'+crypto.randomUUID(),s=h.context.YMBSearchAsyncStore;
 await s.createJob({jobId,owner,folderId:'folder',queries:['saved query'],parameters:{region:'225'},maxRequests:1,maxCostMicrorub:30500,unitCostMicrorub:30500,now:1});
 if(state!=='PENDING'){
  await s.claim({jobId,owner,workerId:'fixture-seed',attemptId:'seed',kind:'submit',now:2});
  await s.finishSubmit({jobId,owner,index:0,attemptId:'seed',outcome:'received',operationId:jobId+'-op',rawText:JSON.stringify({id:jobId+'-op',done:true,response:{rawData:Buffer.from(broken?'bad XML':xml).toString('base64')}}),now:3});
  if(state==='PARSE_FAILED')await s.finishNormalization({jobId,owner,index:0,errorCode:'OLD_PARSER_FAILURE',now:4});
 }
 const raw=await s.readResult(jobId,owner,0),before=await s.getSummary(jobId,owner);
 return{h,s,jobId,raw,before,run:(extra={})=>send(h,{action:'normalizeSaved',jobId,index:0,...extra})};
}
test('explicit normalizeSaved repairs preserved PARSE_FAILED without permission or network and preserves raw/budget',async()=>{
 const f=await setup();const r=await f.run();const e=envelope(r);assert.equal(e.ok,true,r.report_text);assert.equal(e.normalized,true);assert.equal(e.index,0);assert.equal(r.request_executed,false);assert.equal(f.h.calls.fetch.length,0);assert.equal(f.h.context.YMBSearchAsyncWorkerIntegration.providerEnabled,false);
 const rec=await f.s.readResult(f.jobId,KEY,0),after=await f.s.getSummary(f.jobId,KEY);assert.equal(rec.raw_text,f.raw.raw_text);assert.equal(rec.operation_id,f.raw.operation_id);assert.equal(rec.normalized.results[0].url,'https://example.test/kept');assert.equal(after.counts.SUCCEEDED,1);assert.equal(after.requests_started,f.before.requests_started);assert.equal(after.reserved_microrub,f.before.reserved_microrub);assert.equal(f.h.data.wsmb_outbox[KEY].provider_executions,0);assert.ok(!r.report_text.includes('rawData'));await finish(f.h);
});
test('RESULT_SAVED can be parsed locally and successful repeat does not rewrite result or revision',async()=>{
 const f=await setup({state:'RESULT_SAVED'});assert.equal(envelope(await f.run()).ok,true);await finish(f.h);const before=JSON.stringify(await f.s.readResult(f.jobId,KEY,0)),sum=await f.s.getSummary(f.jobId,KEY);
 const r=await f.run();assert.equal(envelope(r).already_normalized,true);assert.equal(JSON.stringify(await f.s.readResult(f.jobId,KEY,0)),before);assert.equal((await f.s.getSummary(f.jobId,KEY)).revision,sum.revision);assert.equal(f.h.calls.fetch.length,0);await finish(f.h);
});
test('broken original stays PARSE_FAILED with truthful error; local retry never purchases replacement',async()=>{
 const f=await setup({broken:true});const r=await f.run();const e=envelope(r);assert.equal(e.ok,false);assert.equal(e.code,'ASYNC_NORMALIZATION_FAILED');assert.equal(e.raw_preserved,true);assert.equal((await f.s.getSummary(f.jobId,KEY)).counts.PARSE_FAILED,1);assert.equal((await f.s.readResult(f.jobId,KEY,0)).raw_text,f.raw.raw_text);assert.equal(f.h.calls.fetch.length,0);assert.equal(r.request_executed,false);await finish(f.h);
});
for(const extra of [{index:-1},{index:1500},{index:0.5},{index:'0'},{count:25},{rawData:'injected'},{queryText:'changed'},{url:'https://evil.invalid'}])test('local normalization rejects invalid or modifying input '+JSON.stringify(extra),async()=>{
 const f=await setup();const r=await f.run(extra);assert.ok(!r.report_text.includes('"ok":true'),r.report_text);assert.equal((await f.s.getSummary(f.jobId,KEY)).revision,f.before.revision);assert.equal(f.h.calls.fetch.length,0);await finish(f.h);
});
test('local normalization of missing or pending item cannot fabricate a result',async()=>{
 const f=await setup({state:'PENDING'});const r=await f.run();assert.match(r.report_text,/ASYNC_ITEM_STATE_INVALID/);await finish(f.h);const m=await f.run({index:1});assert.match(m.report_text,/ASYNC_ITEM_NOT_FOUND/);assert.equal((await f.s.getSummary(f.jobId,KEY)).counts.PENDING,1);assert.equal(f.h.calls.fetch.length,0);await finish(f.h);
});
test('local normalization remains owner-bound and blocked with Manual off',async()=>{
 const f=await setup({owner:'different-owner'});const r=await f.run();assert.match(r.report_text,/ASYNC_WRONG_OWNER/);assert.equal(f.h.calls.fetch.length,0);await finish(f.h);
 f.h.data.wsmb_manual_modes[KEY]=false;assert.equal((await f.run()).code,'MANUAL_MODE_DISABLED');
});
test('outbox failure after local parse leaves saved raw and normalized result; worker restart never causes provider retry',async()=>{
 const f=await setup();const put=f.h.context.chrome.storage.local.set;let hit=false;
 f.h.context.chrome.storage.local.set=async v=>{if(v.wsmb_outbox?.[KEY]&&!hit){hit=true;throw new Error('outbox disk');}return put(v);};
 await f.run();assert.ok(hit);assert.equal((await f.s.getSummary(f.jobId,KEY)).all_successful,true);assert.equal((await f.s.readResult(f.jobId,KEY,0)).raw_text,f.raw.raw_text);
 const second=await loadWorker(full,{seed:f.h.data});const r=await send(second,{action:'normalizeSaved',jobId:f.jobId,index:0});assert.ok(['ASYNC_RECOVERY_DELIVERY_PENDING','DELIVERY_IN_PROGRESS'].includes(r.code),JSON.stringify(r));assert.equal(second.data.wsmb_manual_operations[KEY].request_executed,false);assert.equal(second.calls.fetch.length,0);await finish(second);
 assert.equal(envelope(await send(second,{action:'normalizeSaved',jobId:f.jobId,index:0})).already_normalized,true);await finish(second);
});
test('simultaneous repair clicks produce one admission and one delivery',async()=>{
 const f=await setup();const [a,b]=await Promise.all([f.run(),f.run()]);assert.equal([a,b].filter(x=>x.accepted).length,1);assert.equal([a,b].find(x=>!x.accepted).code,'MANUAL_OPERATION_ACTIVE');assert.equal(f.h.calls.fetch.length,0);await finish(f.h);
});
