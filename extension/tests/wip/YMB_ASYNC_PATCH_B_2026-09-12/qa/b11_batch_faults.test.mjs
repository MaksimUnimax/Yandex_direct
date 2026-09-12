// Complete legacy invocation paths with controlled provider/storage failures only.
import test from 'node:test';import assert from 'node:assert/strict';import crypto from 'node:crypto';
import {loadWorker,KEY,CID} from './b10_full_worker_harness.mjs';
const full=process.env.YMB_FULL;
const xml='<yandexsearch><response><found priority="all">1</found><results><grouping><group><doc><url>https://example.test/saved</url></doc></group></grouping></results></response></yandexsearch>';
const good=()=>new Response(JSON.stringify({rawData:Buffer.from(xml).toString('base64')}),{headers:{'content-type':'application/json'}});
const send=(h,raw)=>h.dispatch({type:'WS_EXECUTE_MANUAL_BLOCK',conversation_key:KEY,manual_request_token:crypto.randomUUID(),block_text:'SEARCH_BATCH_API_V1 '+JSON.stringify(raw)});
async function finish(h,auto=false){const e=h.data.wsmb_outbox?.[KEY];if(e)await h.dispatch({type:auto?'WS_AUTO_DELIVERY_COMPLETE':'WS_MANUAL_DELIVERY_COMPLETE',conversation_key:KEY,delivery_id:e.delivery_id,delivery_confirmed:true,confirmation_basis:'microphone',composer_empty:true});}
async function setup(n=2,network=good){const h=await loadWorker(full,{network});h.seedBoundChat();const jobId='batch-'+crypto.randomUUID();await send(h,{action:'start',jobId,queries:Array.from({length:n},(_,i)=>'query '+i),confirmBillable:true,maxRequests:n,maxCostRub:5});await finish(h);return{h,jobId,next:count=>send(h,{action:'nextN',jobId,count}),job:()=>h.context.YMBSearchBatchWorkerTransport.runtime.loadJob(jobId)};}
function runSeed(h){h.data.wsmb_manual_modes[KEY]=false;const run={run_id:'r-'+crypto.randomUUID(),active_service:'search',conversation_key:KEY,conversation_id:CID,tab_id:7,status:'waiting_command',requests_attempted:0,requests_executed:0,requests_skipped:0,estimated_cost_rub:0,sequence:0,permission_profile:'SEARCH',pause_requested:false,finish_requested:false};h.data.wsmb_auto_runs[KEY]=run;h.data.ymb_search_policy={autorun_enabled:true,manual_enabled:true,max_requests_per_run:20,max_cost_rub_per_run:50};return run;}
function failureOnSettlement(h){const proto=h.context.IDBObjectStore.prototype,put=proto.put;let hit=false;proto.put=function(v,...rest){if(this.name==='attempts'&&v.kind==='search'&&v.status==='settled'&&!hit){hit=true;throw new Error('settlement disk');}return put.call(this,v,...rest);};return{hit:()=>hit,restore:()=>proto.put=put};}
test('batch nextN stops on successful answer with settlement warning, preserving untouched next item',async()=>{
 const f=await setup(),inject=failureOnSettlement(f.h);let r;try{r=await f.next(2);}finally{inject.restore();}
 assert.ok(inject.hit());assert.equal(f.h.calls.fetch.length,1);assert.equal(r.request_executed,true);const job=await f.job();assert.equal(job.items[0].status,'SUCCEEDED');assert.equal(job.items[1].status,'PENDING');assert.equal(job.status,'PAUSED');assert.ok(job.items[0].result_payload);assert.match(r.report_text,/SHARED_ADMISSION|RECONCILIATION/);await finish(f.h);
 const again=await f.next(1);assert.equal(again.request_executed,false);assert.equal(f.h.calls.fetch.length,1);await finish(f.h);
});
test('batch Autorun propagates stop_required, pauses after delivery and never asks next item',async()=>{
 const f=await setup(),run=runSeed(f.h),inject=failureOnSettlement(f.h);let r;
 try{r=await f.h.dispatch({type:'WS_AUTO_COMMAND',conversation_key:KEY,run_id:run.run_id,assistant_turn_id:'t1',command_text:'SEARCH_BATCH_API_V1 '+JSON.stringify({action:'next',jobId:f.jobId})});}finally{inject.restore();}
 assert.ok(inject.hit());assert.equal(f.h.calls.fetch.length,1);assert.equal(r.result.stop_required,true);assert.equal(f.h.data.wsmb_auto_runs[KEY].pause_requested,true);await finish(f.h,true);assert.equal(f.h.data.wsmb_auto_runs[KEY].status,'paused');
 await f.h.dispatch({type:'WS_AUTO_COMMAND',conversation_key:KEY,run_id:run.run_id,assistant_turn_id:'t2',command_text:'SEARCH_BATCH_API_V1 '+JSON.stringify({action:'next',jobId:f.jobId})});assert.equal(f.h.calls.fetch.length,1);assert.equal((await f.job()).items[1].status,'PENDING');
});
test('batch unknown provider result is stored as UNKNOWN not terminal failure; remaining query not advanced',async()=>{
 const f=await setup(2,async()=>{throw new Error('network lost');});const r=await f.next(2);assert.equal(r.request_executed,'UNKNOWN');assert.equal(f.h.calls.fetch.length,1);assert.equal((await f.job()).items[0].status,'OUTCOME_UNKNOWN');assert.equal((await f.job()).items[1].status,'PENDING');await finish(f.h);
 await f.next(1);assert.equal(f.h.calls.fetch.length,1);assert.equal((await f.job()).items[1].status,'PENDING');await finish(f.h);
});
test('late saved-result write failure reports confirmed request, not false, and never executes next item',async()=>{
 const f=await setup(),put=f.h.context.chrome.storage.local.set;let hit=false;
 f.h.context.chrome.storage.local.set=async v=>{const j=v.ymb_search_batch_jobs_v1?.[f.jobId];if(j?.items[0]?.status==='SUCCEEDED'&&!hit){hit=true;throw new Error('result disk');}return put(v);};
 const r=await f.next(2);assert.ok(hit);assert.equal(f.h.calls.fetch.length,1);assert.equal(r.request_executed,true,r.report_text);assert.equal(f.h.data.wsmb_outbox[KEY].provider_executions,1);assert.equal((await f.job()).items[1].status,'PENDING');await finish(f.h);
 await f.next(1);assert.equal(f.h.calls.fetch.length,1);await finish(f.h);
});
test('first result survives second pre-network storage failure with correct partial execution count',async()=>{
 const f=await setup(),put=f.h.context.chrome.storage.local.set;let hit=false;
 f.h.context.chrome.storage.local.set=async v=>{const j=v.ymb_search_batch_jobs_v1?.[f.jobId];if(j?.items[1]?.status==='REQUEST_STARTED'&&!hit){hit=true;throw new Error('second intent disk');}return put(v);};
 const r=await f.next(2);assert.ok(hit);assert.equal(f.h.calls.fetch.length,1);assert.equal(r.request_executed,true,r.report_text);assert.equal(f.h.data.wsmb_outbox[KEY].provider_executions,1);const j=await f.job();assert.equal(j.items[0].status,'SUCCEEDED');assert.ok(j.items[0].result_payload);await finish(f.h);
});
for(const status of [401,429,500])test('batch HTTP '+status+' stops at first failed item and retains explicit response',async()=>{
 const f=await setup(2,async()=>new Response(JSON.stringify({error:'controlled rejection'}),{status}));const r=await f.next(2);assert.equal(f.h.calls.fetch.length,1);assert.equal(r.request_executed,true);const j=await f.job();assert.equal(j.items[0].status,'FAILED_TERMINAL');assert.equal(j.items[1].status,'PENDING');assert.ok(j.items[0].result_payload);await finish(f.h);
});
test('explicitly confirmed Check preserves existing exception to disabled Manual/method policy',async()=>{
 const h=await loadWorker(full,{network:good});h.seedBoundChat();h.data.ymb_search_policy={manual_enabled:false,allowed_methods:[]};const r=await h.dispatch({type:'YMB_CHECK_SERVICE_CREDENTIAL',service:'search',confirm_billable:true},{});assert.equal(h.calls.fetch.length,1);assert.equal(r.ok,true);assert.ok(!JSON.stringify(r).includes('TEST_SEARCH_NOT_REAL'));
});
test('Check reservation write failure never calls provider or marks credential PRESENT',async()=>{
 const h=await loadWorker(full,{network:good});h.seedBoundChat();const proto=h.context.IDBObjectStore.prototype,put=proto.put;let hit=false;
 proto.put=function(v,...rest){if(this.name==='scopes'&&!hit){hit=true;throw new Error('reservation disk');}return put.call(this,v,...rest);};
 let r;try{r=await h.dispatch({type:'YMB_CHECK_SERVICE_CREDENTIAL',service:'search',confirm_billable:true},{});}finally{proto.put=put;}
 assert.ok(hit);assert.equal(h.calls.fetch.length,0);assert.equal(r.ok,false);assert.notEqual(r.state,'PRESENT');assert.ok(!JSON.stringify(r).includes('TEST_SEARCH_NOT_REAL'));
});
for(const mode of ['http401','network'])test('Check '+mode+' does not retry and reports no false valid credential',async()=>{
 const h=await loadWorker(full,{network:async()=>{if(mode==='network')throw new Error('network');return new Response('{}',{status:401});}});h.seedBoundChat();const r=await h.dispatch({type:'YMB_CHECK_SERVICE_CREDENTIAL',service:'search',confirm_billable:true},{});assert.equal(h.calls.fetch.length,1);assert.notEqual(r.state,'PRESENT');assert.equal(r.ok,false);assert.ok(!JSON.stringify(r).includes('TEST_SEARCH_NOT_REAL'));
});
