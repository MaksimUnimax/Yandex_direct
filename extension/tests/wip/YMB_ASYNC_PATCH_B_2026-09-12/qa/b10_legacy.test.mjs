// Existing full invocation paths on the same composition. No installed browser.
import test from 'node:test';import assert from 'node:assert/strict';import crypto from 'node:crypto';
import {loadWorker,KEY,CID} from './b10_full_worker_harness.mjs';
const full=process.env.YMB_FULL;
const xml='<yandexsearch><response><found priority="all">0</found></response></yandexsearch>';
const network=async url=>new Response(JSON.stringify(String(url).includes('/v2/gen/search')?{message:{content:'Answer',role:'ROLE_ASSISTANT'},sources:[]}:{rawData:Buffer.from(xml).toString('base64')}),{headers:{'content-type':'application/json'}});
const send=(h,text)=>h.dispatch({type:'WS_EXECUTE_MANUAL_BLOCK',conversation_key:KEY,manual_request_token:crypto.randomUUID(),block_text:text});
async function finish(h,type='WS_MANUAL_DELIVERY_COMPLETE'){const e=h.data.wsmb_outbox?.[KEY];if(e)return h.dispatch({type,conversation_key:KEY,delivery_id:e.delivery_id,delivery_confirmed:true,confirmation_basis:'microphone',composer_empty:true});}
function seedRun(h,status='waiting_command'){
 const run={run_id:'run-'+crypto.randomUUID(),active_service:'search',conversation_key:KEY,conversation_id:CID,tab_id:7,status,requests_attempted:0,requests_executed:0,requests_skipped:0,estimated_cost_rub:0,sequence:0,permission_profile:'SEARCH',pause_requested:false,finish_requested:false};h.data.wsmb_auto_runs[KEY]=run;h.data.ymb_search_policy={autorun_enabled:true,manual_enabled:true,max_requests_per_run:20,max_cost_rub_per_run:50};return run;
}
for(const method of ['search','genSearch'])test(`full legacy Autorun ${method}, then acknowledgement counts once`,async()=>{
 const h=await loadWorker(full,{network});h.seedBoundChat();h.data.wsmb_manual_modes[KEY]=false;const run=seedRun(h);
 const r=await h.dispatch({type:'WS_AUTO_COMMAND',conversation_key:KEY,run_id:run.run_id,assistant_turn_id:'turn-'+crypto.randomUUID(),command_text:'SEARCH_API_V1 '+JSON.stringify({method,queryText:'test',...(method==='genSearch'?{confirmBillable:true}:{})})});
 assert.equal(h.calls.fetch.length,1,JSON.stringify(r));assert.equal(h.data.wsmb_auto_runs[KEY].requests_attempted,1);assert.equal(h.data.wsmb_auto_runs[KEY].requests_executed,1);assert.equal(h.data.wsmb_auto_runs[KEY].estimated_cost_rub,method==='search'?0.488:5.08);await finish(h,'WS_AUTO_DELIVERY_COMPLETE');
 assert.equal(h.calls.fetch.length,1);assert.equal(h.data.wsmb_auto_runs[KEY].status,'waiting_command');
});
test('full Search credential Check requires consent and still works with Manual off and invalid recorded key state',async()=>{
 const h=await loadWorker(full,{network});h.seedBoundChat();h.data.wsmb_manual_modes[KEY]=false;h.data.ymb_service_credentials.search.check_state='INVALID_OR_EXPIRED';
 const no=await h.dispatch({type:'YMB_CHECK_SERVICE_CREDENTIAL',service:'search',confirm_billable:false},{});assert.equal(no.code,'SEARCH_CHECK_CONFIRM_REQUIRED');assert.equal(h.calls.fetch.length,0);
 const yes=await h.dispatch({type:'YMB_CHECK_SERVICE_CREDENTIAL',service:'search',confirm_billable:true},{});assert.equal(yes.ok,true,JSON.stringify(yes));assert.equal(h.calls.fetch.length,1);assert.equal(yes.state,'PRESENT');
});
test('full old Search batch start/nextN preserves request count and result payload',async()=>{
 const h=await loadWorker(full,{network});h.seedBoundChat();const jobId='batch-'+crypto.randomUUID();
 const start=await send(h,'SEARCH_BATCH_API_V1 '+JSON.stringify({action:'start',jobId,queries:['one','two'],confirmBillable:true,maxRequests:2,maxCostRub:3}));assert.match(start.report_text,/SEARCH_BATCH_RESULT_V1/);assert.equal(h.calls.fetch.length,0);await finish(h);
 const next=await send(h,'SEARCH_BATCH_API_V1 '+JSON.stringify({action:'nextN',jobId,count:2}));assert.equal(h.calls.fetch.length,2,next.report_text);assert.equal(next.request_executed,true);await finish(h);assert.equal(h.calls.fetch.length,2);
});
test('full old Search batch next in Autorun shares the run ledger',async()=>{
 const h=await loadWorker(full,{network});h.seedBoundChat();const jobId='batch-'+crypto.randomUUID();
 await send(h,'SEARCH_BATCH_API_V1 '+JSON.stringify({action:'start',jobId,queries:['one'],confirmBillable:true,maxRequests:1,maxCostRub:3}));await finish(h);h.data.wsmb_manual_modes[KEY]=false;const run=seedRun(h);
 const r=await h.dispatch({type:'WS_AUTO_COMMAND',conversation_key:KEY,run_id:run.run_id,assistant_turn_id:'turn-'+crypto.randomUUID(),command_text:'SEARCH_BATCH_API_V1 '+JSON.stringify({action:'next',jobId})});assert.equal(h.calls.fetch.length,1,JSON.stringify(r));assert.equal(h.data.wsmb_auto_runs[KEY].requests_executed,1);assert.equal(h.data.wsmb_auto_runs[KEY].requests_attempted,1);await finish(h,'WS_AUTO_DELIVERY_COMPLETE');
});
test('paused Search run plus Manual ordinary command uses shared ledger without double budget increase',async()=>{
 const h=await loadWorker(full,{network});h.seedBoundChat();const run=seedRun(h,'paused');const r=await send(h,'SEARCH_API_V1 '+JSON.stringify({method:'search',queryText:'manual paused'}));assert.equal(r.request_executed,true,r.report_text);assert.equal(h.calls.fetch.length,1);assert.equal(h.data.wsmb_auto_runs[KEY].requests_attempted,1);assert.equal(h.data.wsmb_auto_runs[KEY].requests_executed,1);assert.equal(h.data.wsmb_auto_runs[KEY].estimated_cost_rub,0.488);assert.equal(h.data.wsmb_auto_runs[KEY].status,'paused');await finish(h);
});
test('deferred marker presented in Autorun never initiates deferred provider work',async()=>{
 const h=await loadWorker(full,{network,permissionFixture:true});h.seedBoundChat();h.data.wsmb_manual_modes[KEY]=false;const run=seedRun(h);const r=await h.dispatch({type:'WS_AUTO_COMMAND',conversation_key:KEY,run_id:run.run_id,assistant_turn_id:'turn',command_text:'SEARCH_ASYNC_BATCH_API_V1 '+JSON.stringify({action:'submitN',jobId:'job',count:25})});assert.equal(h.calls.fetch.length,0);assert.ok(r.report_text||r.code,JSON.stringify(r));
});
test('full ordinary Search Autorun pauses after settlement failure while preserving the received report',async()=>{
 const h=await loadWorker(full,{network});h.seedBoundChat();h.data.wsmb_manual_modes[KEY]=false;const run=seedRun(h);const proto=h.context.IDBObjectStore.prototype,put=proto.put;let injected=false;
 proto.put=function(v,...rest){if(this.name==='attempts'&&v.kind==='search'&&v.status==='settled'&&!injected){injected=true;throw new Error('settlement disk failure');}return put.call(this,v,...rest);};
 let r;try{r=await h.dispatch({type:'WS_AUTO_COMMAND',conversation_key:KEY,run_id:run.run_id,assistant_turn_id:'turn-'+crypto.randomUUID(),command_text:'SEARCH_API_V1 '+JSON.stringify({method:'search',queryText:'test fault'})});}finally{proto.put=put;}
 assert.ok(injected);assert.equal(h.calls.fetch.length,1);assert.match(r.report_text,/SEARCH_RESULT_V1/);assert.equal(r.result.stop_required,true);assert.equal(h.data.wsmb_auto_runs[KEY].pause_requested,true);
 await finish(h,'WS_AUTO_DELIVERY_COMPLETE');assert.equal(h.data.wsmb_auto_runs[KEY].status,'paused');
 const next=await h.dispatch({type:'WS_AUTO_COMMAND',conversation_key:KEY,run_id:run.run_id,assistant_turn_id:'later',command_text:'SEARCH_API_V1 '+JSON.stringify({method:'search',queryText:'different'})});assert.equal(next.accepted,false);assert.equal(h.calls.fetch.length,1);
});
