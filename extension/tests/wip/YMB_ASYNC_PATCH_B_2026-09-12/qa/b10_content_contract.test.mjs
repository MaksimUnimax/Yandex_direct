// Worker public-state + exact content admission function. NOT live DOM validation.
import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import path from 'node:path';import vm from 'node:vm';
import {loadWorker,KEY} from './b10_full_worker_harness.mjs';
const full=process.env.YMB_FULL;
const source=fs.readFileSync(path.join(full,'content_script.js'),'utf8');
const begin=source.indexOf('  function manualActionBlockReason('),end=source.indexOf('\n  function refreshActionAvailability',begin);
assert.ok(begin>=0&&end>begin);
const ctx=vm.createContext({});vm.runInContext(source.slice(begin,end)+'\nglobalThis.reason=manualActionBlockReason;',ctx);
const reason=(op,delivery=false,admission=false)=>ctx.reason({manual_operation:op},delivery,admission);
test('content can offer explicit recovery only for stale async state flagged by worker',()=>{
 assert.equal(reason({status:'search_async_requesting',recovery_available:true}),'');
 for(const op of [{status:'search_async_requesting'},{status:'search_async_requesting',recovery_available:false},{status:'requesting',recovery_available:true},{status:'search_batch_requesting',recovery_available:true},{status:'delivering',recovery_available:true}])assert.equal(reason(op),'MANUAL_OPERATION_ACTIVE');
 assert.equal(reason({status:'search_async_requesting',recovery_available:true},true),'DELIVERY_IN_PROGRESS');
 assert.equal(reason({status:'search_async_requesting',recovery_available:true},false,true),'MANUAL_OPERATION_ACTIVE');
});
test('worker exposes only local recovery availability, not worker identity or authority from the message',async()=>{
 const h=await loadWorker(full);h.seedBoundChat();const operation={operation_id:'manual-stale',conversation_key:KEY,tab_id:7,active_service:'search',status:'search_async_requesting',batch_job_id:'job-stale',folder_id:'folder',request_worker_session_id:'old'};
 h.data.wsmb_manual_operations[KEY]=operation;
 const state=()=>h.dispatch({type:'WS_GET_STATE',conversation_key:KEY});
 const r=await state();assert.equal(r.state.manual_operation.recovery_available,true);assert.equal('request_worker_session_id' in r.state.manual_operation,false);assert.equal(h.calls.fetch.length,0);assert.equal(h.data.wsmb_outbox[KEY],undefined);assert.equal(h.data.wsmb_manual_operations[KEY].status,'search_async_requesting');
 operation.request_worker_session_id=h.context.YMBSearchAdmissionBinding.workerSessionId;assert.equal((await state()).state.manual_operation.recovery_available,false);
 operation.request_worker_session_id='old';operation.active_service='wordstat';assert.equal((await state()).state.manual_operation.recovery_available,false);
 operation.active_service='search';h.data.wsmb_manual_modes[KEY]=false;assert.equal((await state()).state.manual_operation.recovery_available,false);
});
test('recovery-delivery response enters normal outbox wait, not a second content-error report',async()=>{
 const b=source.indexOf('  async function onManualAction('),e=source.indexOf('\n  function createAction',b);assert.ok(b>=0&&e>b);
 const calls=[];const c=vm.createContext({currentConversationKey:()=>KEY,manualEnabled:true,manualActionBlockReason:()=>'',refreshActionAvailability:()=>{},stableBlockId:()=>1,manualInFlight:new Set(),manualAdmissionHold:false,deliveryLifecycleHold:false,
  BB2ManualControls:{makeId:()=> 'qa-token'},BB2ProvenWritingCapture:{textFromBlock:()=> 'SEARCH_ASYNC_BATCH_API_V1 {}'},STATUS_KEYS:{OPERATION:'op'},activeService:'search',setStatus:(...x)=>calls.push(['status',...x]),sendWorker:async()=>({ok:false,accepted:false,code:'ASYNC_RECOVERY_DELIVERY_PENDING',request_executed:false}),scheduleOutboxPoll:d=>calls.push(['poll',d]),queueContentError:x=>calls.push(['error',x]),syncState:async()=>calls.push(['sync'])});
 vm.runInContext(source.slice(b,e)+'\nglobalThis.action=onManualAction;',c);await c.action({isConnected:true},{});
 assert.equal(c.deliveryLifecycleHold,true);assert.equal(calls.filter(x=>x[0]==='poll').length,1);assert.equal(calls.filter(x=>x[0]==='error').length,0);assert.equal(calls.filter(x=>x[0]==='sync').length,1);
});
