// Complete B9/B10 worker; operation-host capability simulated ONLY in getManifest.
// Real saved modules; Chrome, IDB, network and clock fixtures. No live requests.
import test from 'node:test';import assert from 'node:assert/strict';import crypto from 'node:crypto';
import {loadWorker,KEY} from './b10_full_worker_harness.mjs';
const full=process.env.YMB_FULL;if(!full)throw new Error('YMB_FULL required');
const xml='<yandexsearch><response><found priority="all">1</found><results><grouping><group><doc><url>https://example.test/item</url><domain>example.test</domain><title>Test 💎</title></doc></group></grouping></results></response></yandexsearch>';
const encoded=Buffer.from(xml).toString('base64');
const response=v=>new Response(JSON.stringify(v),{headers:{'content-type':'application/json'}});
const cmd=raw=>'SEARCH_ASYNC_BATCH_API_V1 '+JSON.stringify(raw);
const send=(h,raw,token=crypto.randomUUID())=>h.dispatch({type:'WS_EXECUTE_MANUAL_BLOCK',conversation_key:KEY,manual_request_token:token,block_text:cmd(raw)});
async function finish(h){const e=h.data.wsmb_outbox?.[KEY];if(e)assert.equal((await h.dispatch({type:'WS_MANUAL_DELIVERY_COMPLETE',conversation_key:KEY,delivery_id:e.delivery_id,delivery_confirmed:true,confirmation_basis:'microphone',composer_empty:true})).ok,true);}
function envelope(r){const p=r.report_text.indexOf('\n');return JSON.parse(r.report_text.slice(p+1));}
let epoch=1000000;
async function setup(count=2){
 const clock={now:epoch+=1000000}, ops=[], traffic=[];let h;
 const route={submit:()=>null,collect:op=>({id:op,done:false})};
 const network=async(url,init)=>{traffic.push({url:String(url),method:init.method,body:init.body});clock.now+=250;
  if(String(url).endsWith('/searchAsync')){const op='op-'+crypto.randomUUID();ops.push(op);return route.submit(op,h)??response({id:op,done:false});}
  if(String(url).includes('/operations/'))return response(await route.collect(String(url).split('/').at(-1),h));
  throw new Error('UNEXPECTED_ENDPOINT');};
 h=await loadWorker(full,{permissionFixture:true,clock,network});h.seedBoundChat();
 const jobId='job-'+crypto.randomUUID();const r=await send(h,{action:'start',jobId,queries:Array.from({length:count},(_,i)=>'query '+i),confirmBillable:true,maxRequests:count,maxCostRub:10});
 assert.equal(envelope(r).ok,true,r.report_text);await finish(h);
 return{h,jobId,clock,ops,traffic,route,network,submit:n=>send(h,{action:'submitN',jobId,count:n}),collect:n=>send(h,{action:'collectN',jobId,count:n}),summary:()=>h.context.YMBSearchAsyncStore.getSummary(jobId,KEY)};
}
test('full deferred submit shares trusted policy session and persists operation before returning',async()=>{
 const f=await setup();const r=await f.submit(1);assert.equal(r.request_executed,true,r.report_text);assert.equal(f.traffic.length,1);assert.equal(f.traffic[0].method,'POST');assert.equal((await f.summary()).counts.WAITING,1);assert.equal((await f.summary()).requests_started,1);await finish(f.h);
});
test('not-due then waiting collect never replays submit or invents a result',async()=>{
 const f=await setup(1);assert.equal((await f.submit(1)).request_executed,true);await finish(f.h);assert.equal((await f.collect(1)).request_executed,false);assert.equal(f.traffic.length,1);await finish(f.h);
 f.clock.now+=300000;const r=await f.collect(1);assert.equal(r.request_executed,true);assert.equal(f.traffic.length,2);assert.equal(f.traffic[1].method,'GET');assert.equal((await f.summary()).counts.WAITING,1);await finish(f.h);
});
test('collect successful raw result normalizes and exports through A without another provider call',async()=>{
 const f=await setup(1);assert.equal((await f.submit(1)).request_executed,true);await finish(f.h);f.clock.now+=300000;f.route.collect=op=>({id:op,done:true,response:{rawData:encoded}});
 const r=await f.collect(1);assert.equal(r.request_executed,true);assert.equal((await f.summary()).all_successful,true);await finish(f.h);
 const result=await f.h.context.YMBSearchAsyncStore.readResult(f.jobId,KEY,0);assert.equal(result.normalized.results[0].url,'https://example.test/item');assert.equal(JSON.parse(result.raw_text).id,f.ops[0]);
 const e=await send(f.h,{action:'exportPage',jobId:f.jobId});assert.equal(envelope(e).export_page.item_count,1);assert.equal(f.traffic.length,2);await finish(f.h);
});
test('submit with an already-completed response is normalized locally, not stranded awaiting an impossible GET',async()=>{
 const f=await setup(1);f.route.submit=op=>response({id:op,done:true,response:{rawData:encoded}});const r=await f.submit(1);assert.equal(r.request_executed,true);assert.equal(f.traffic.length,1);assert.equal((await f.summary()).all_successful,true,r.report_text);await finish(f.h);
});
test('provider operation error is not reported as a successful command',async()=>{
 const f=await setup(1);f.route.submit=op=>response({id:op,done:true,error:{code:13,message:'provider failed'}});const r=await f.submit(1);assert.equal(r.request_executed,true);assert.equal(envelope(r).ok,false);assert.equal((await f.summary()).counts.FAILED,1);assert.equal(f.traffic.length,1);await finish(f.h);
});
test('unknown POST is retained, stops the slice and cannot be retried by the next command',async()=>{
 const f=await setup(2);f.route.submit=()=>{throw new Error('wire interrupted');};const r=await f.submit(2);assert.equal(r.request_executed,'UNKNOWN',r.report_text);assert.equal(f.traffic.length,1);assert.equal((await f.summary()).counts.UNKNOWN,1);await finish(f.h);
 const again=await f.submit(1);assert.equal(again.request_executed,false);assert.equal(f.traffic.length,1);await finish(f.h);
});
test('loss of Manual authorization after a confirmed first step does not rewrite its outcome to false',async()=>{
 const f=await setup(2);f.route.submit=(op,h)=>{h.data.wsmb_manual_modes[KEY]=false;return response({id:op,done:false});};
 const r=await f.submit(2);assert.equal(f.traffic.length,1);assert.equal(r.request_executed,true,r.report_text);assert.equal(f.h.data.wsmb_outbox[KEY].provider_executions,1);assert.equal((await f.summary()).counts.WAITING,1);await finish(f.h);
});
test('normalization failure stops the collect slice and does not mask PARSE_FAILED with ok',async()=>{
 const f=await setup(2);assert.equal((await f.submit(2)).request_executed,true);await finish(f.h);f.clock.now+=300000;f.route.collect=op=>({id:op,done:true,response:{rawData:Buffer.from('broken XML').toString('base64')}});
 const before=f.traffic.length;const r=await f.collect(2);assert.equal(r.request_executed,true);assert.equal(f.traffic.length-before,1);assert.equal(envelope(r).ok,false);assert.equal((await f.summary()).counts.PARSE_FAILED,1);assert.equal((await f.summary()).counts.WAITING,1);await finish(f.h);
});
test('one slow result exhausts the local slice time budget before starting a second provider request',async()=>{
 const f=await setup(2);f.route.submit=op=>{f.clock.now+=11000;return response({id:op,done:false});};const r=await f.submit(2);assert.equal(r.request_executed,true);assert.equal(f.traffic.length,1);assert.equal((await f.summary()).counts.PENDING,1);await finish(f.h);
});
test('restart after outbox commit reattaches delivery locally without replaying provider',async()=>{
 const f=await setup(1);const put=f.h.context.chrome.storage.local.set;
 f.h.context.chrome.storage.local.set=async values=>{const op=values.wsmb_manual_operations?.[KEY];if(op?.batch_action==='submitN'&&op.status==='delivering')throw new Error('local write interrupted');return put(values);};
 await f.submit(1);assert.equal(f.traffic.length,1);assert.equal(f.h.data.wsmb_manual_operations[KEY].status,'search_async_requesting');assert.ok(f.h.data.wsmb_outbox[KEY]);
 const second=await loadWorker(full,{permissionFixture:true,seed:f.h.data,clock:f.clock,network:f.network});
 const r=await send(second,{action:'status',jobId:f.jobId});assert.ok(['DELIVERY_IN_PROGRESS','ASYNC_RECOVERY_DELIVERY_PENDING'].includes(r.code),JSON.stringify(r));assert.equal(second.data.wsmb_manual_operations[KEY].status,'delivering');assert.equal(f.traffic.length,1);await finish(second);
 const status=await send(second,{action:'status',jobId:f.jobId});assert.equal(envelope(status).ok,true);await finish(second);
});
test('restart with no outbox recovers interrupted submit locally; next explicit command cannot replay it',async()=>{
 const f=await setup(1);const s=f.h.context.YMBSearchAsyncStore;
 await s.claim({jobId:f.jobId,owner:KEY,workerId:'old-worker',attemptId:'interrupted',kind:'submit',now:f.clock.now});
 f.h.data.wsmb_manual_operations[KEY]={operation_id:'manual-old',request_token:'old',conversation_key:KEY,tab_id:7,active_service:'search',status:'search_async_requesting',batch_action:'submitN',batch_job_id:f.jobId,folder_id:'folder',run_id:null,request_worker_session_id:'old-worker',request_executed:false};
 const second=await loadWorker(full,{permissionFixture:true,seed:f.h.data,clock:f.clock,network:f.network});const r=await send(second,{action:'status',jobId:f.jobId});assert.ok(['DELIVERY_IN_PROGRESS','ASYNC_RECOVERY_DELIVERY_PENDING'].includes(r.code),JSON.stringify(r));
 assert.equal(second.data.wsmb_manual_operations[KEY].status,'delivering');assert.equal(second.data.wsmb_manual_operations[KEY].request_executed,'UNKNOWN');assert.equal((await s.getSummary(f.jobId,KEY)).counts.UNKNOWN,1);assert.equal(f.traffic.length,0);await finish(second);
 const again=await send(second,{action:'submitN',jobId:f.jobId,count:1});assert.equal(again.request_executed,false);assert.equal(f.traffic.length,0);await finish(second);
});
test('execution receipt write failure before first runtime call is proven not sent',async()=>{
 const f=await setup(1);const put=f.h.context.chrome.storage.local.set;let injected=false;
 f.h.context.chrome.storage.local.set=async values=>{const e=values.wsmb_manual_operations?.[KEY]?.execution_receipt;if(e?.in_flight&&!injected){injected=true;throw new Error('receipt disk failure');}return put(values);};
 const r=await f.submit(1);assert.ok(injected);assert.equal(r.request_executed,false,r.report_text);assert.equal(f.traffic.length,0);assert.equal((await f.summary()).counts.PENDING,1);await finish(f.h);
});
test('post-fetch receipt write failure retains confirmed provenance and stops next request',async()=>{
 const f=await setup(2);const put=f.h.context.chrome.storage.local.set;let injected=false;
 f.h.context.chrome.storage.local.set=async values=>{const e=values.wsmb_manual_operations?.[KEY]?.execution_receipt;if(e&&!e.in_flight&&e.confirmed===1&&!injected){injected=true;throw new Error('receipt disk failure');}return put(values);};
 const r=await f.submit(2);assert.ok(injected);assert.equal(r.request_executed,true,r.report_text);assert.equal(f.traffic.length,1);assert.equal(f.h.data.wsmb_outbox[KEY].provider_executions,1);assert.equal((await f.summary()).counts.PENDING,1);await finish(f.h);
});
test('small durable receipts at 25 full network steps never carry payload or item arrays',async()=>{
 const f=await setup(25);const put=f.h.context.chrome.storage.local.set;const receipts=[];
 f.h.context.chrome.storage.local.set=async values=>{const r=values.wsmb_manual_operations?.[KEY]?.execution_receipt;if(r)receipts.push(structuredClone(r));return put(values);};
 const r=await f.submit(25);assert.equal(r.request_executed,true);assert.equal(f.traffic.length,25);assert.equal((await f.summary()).counts.WAITING,25);
 assert.ok(receipts.length<=52&&receipts.length>=50);assert.ok(receipts.every(v=>JSON.stringify(v).length<150));assert.equal(receipts.at(-1).confirmed,25);assert.equal(receipts.at(-1).in_flight,false);await finish(f.h);
});
test('concurrent explicit deferred commands cannot cross the Manual invocation fence',async()=>{
 const f=await setup(2);const [a,b]=await Promise.all([f.submit(1),f.submit(1)]);assert.equal([a,b].filter(v=>v.accepted).length,1);assert.equal([a,b].find(v=>!v.accepted).code,'MANUAL_OPERATION_ACTIVE');assert.equal(f.traffic.length,1);await finish(f.h);
});
test('current-worker in-flight operation remains blocked rather than recovered',async()=>{
 const f=await setup(1);const worker=f.h.context.YMBSearchAdmissionBinding.workerSessionId;
 f.h.data.wsmb_manual_operations[KEY]={operation_id:'active',request_worker_session_id:worker,conversation_key:KEY,tab_id:7,active_service:'search',status:'search_async_requesting',batch_job_id:f.jobId,folder_id:'folder'};
 const r=await send(f.h,{action:'status',jobId:f.jobId});assert.equal(r.code,'MANUAL_OPERATION_ACTIVE');assert.equal(f.traffic.length,0);assert.equal(f.h.data.wsmb_outbox[KEY],undefined);
});
test('foreign-tab recovery attempt does not mutate interrupted state or stage an outbox',async()=>{
 const f=await setup(1);f.h.data.wsmb_manual_operations[KEY]={operation_id:'interrupted',request_worker_session_id:'old',conversation_key:KEY,tab_id:7,active_service:'search',status:'search_async_requesting',batch_job_id:f.jobId,folder_id:'folder'};
 const before=JSON.stringify(f.h.data.wsmb_manual_operations);const r=await f.h.dispatch({type:'WS_EXECUTE_MANUAL_BLOCK',conversation_key:KEY,block_text:cmd({action:'status',jobId:f.jobId})},{tab:{id:8}});assert.equal(r.code,'CONVERSATION_MISMATCH');assert.equal(JSON.stringify(f.h.data.wsmb_manual_operations),before);assert.equal(f.traffic.length,0);
});
