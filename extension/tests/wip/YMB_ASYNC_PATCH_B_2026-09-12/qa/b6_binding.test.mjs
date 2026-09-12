import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const source = fs.readFileSync(new URL('../candidate/search_admission_worker_binding.js', import.meta.url), 'utf8');
const ctx = vm.createContext({ console }); ctx.globalThis = ctx;
vm.runInContext(source, ctx, { filename: 'search_admission_worker_binding.js' });
const F = ctx.YMBSearchAdmissionWorkerBinding;

const KEY='https://chatgpt.com|11111111-1111-4111-8111-111111111111';
const CID='11111111-1111-4111-8111-111111111111';
const binding={conversation_key:KEY,conversation_id:CID};
function harness(overrides={}){
  const state={
    manual:true,
    service:{active_service:'search'},
    operation:{operation_id:'manual-1',conversation_key:KEY,tab_id:7,active_service:'search',run_id:null,status:'requesting'},
    run:null,
    binding,
    identity:{conversation_key:KEY,conversation_id:CID},
    ...overrides
  };
  const resolver=F.createTrustedContextResolver({
    normalizeConversationKey:v=>{if(v!==KEY)throw new Error('bad key');return v;},
    getBinding:async()=>state.binding,
    getManualMode:async()=>state.manual,
    getServiceContext:async()=>state.service,
    getAutoRun:async()=>state.run,
    getManualOperation:async()=>state.operation,
    assertTabConversation:async(tab,key,expected)=>{if(tab!==7||key!==KEY||expected&&expected.toLowerCase()!==CID.toLowerCase())throw new Error('owner');return state.identity;},
    workerSessionId:'worker-1',
    isRunTerminal:s=>['stopped','error'].includes(s)
  });
  return {state,resolver};
}
const call=(resolver,meta={})=>resolver.resolveContext({command:{method:'search'},metadata:{conversation_key:KEY,policy:{channel:'manual'},run_id:null,...meta},folderId:'folder',requestId:'req-1'});
const rejects=async(fn,code)=>{await assert.rejects(fn,e=>e.code===code,code)};

test('manual trusted state resolves from durable operation, not arbitrary metadata job ids',async()=>{
  const {resolver}=harness(); const r=await call(resolver,{job_id:'evil',batch_job_id:'evil2'});
  assert.deepEqual({...r},{authorized:true,owner:KEY,jobId:'manual-1',scopeId:'manual-1',runId:null,channel:'manual'});
});
test('manual claimed channel mismatch fails closed',async()=>{const {resolver}=harness();await rejects(()=>call(resolver,{policy:{channel:'autorun'}}),'SHARED_ADMISSION_CHANNEL_MISMATCH');});
test('manual enabled without live operation fails closed',async()=>{const {resolver}=harness({operation:null});await rejects(()=>call(resolver),'SHARED_ADMISSION_MANUAL_STATE_MISSING');});
test('manual delivering state cannot authorize a new provider call',async()=>{const {resolver}=harness({operation:{operation_id:'manual-1',conversation_key:KEY,tab_id:7,active_service:'search',run_id:null,status:'delivering'}});await rejects(()=>call(resolver),'SHARED_ADMISSION_MANUAL_STATE_INVALID');});
test('manual active service must remain search',async()=>{const {resolver}=harness({service:{active_service:'wordstat'}});await rejects(()=>call(resolver),'SHARED_ADMISSION_SERVICE_MISMATCH');});
test('binding is mandatory',async()=>{const {resolver}=harness({binding:null});await rejects(()=>call(resolver),'SHARED_ADMISSION_CONVERSATION_NOT_BOUND');});
test('live owner tab identity is mandatory',async()=>{const {resolver,state}=harness();state.identity={conversation_key:KEY,conversation_id:'22222222-2222-4222-8222-222222222222'};await rejects(()=>call(resolver),'SHARED_ADMISSION_OWNER_MISMATCH');});
test('paused autorun used by manual must match run, service and owner tab',async()=>{
  const run={run_id:'run-1',status:'paused',active_service:'search',tab_id:7,conversation_id:CID};
  const op={operation_id:'manual-2',conversation_key:KEY,tab_id:7,active_service:'search',run_id:'run-1',status:'requesting'};
  const {resolver}=harness({run,operation:op}); const r=await call(resolver,{run_id:'run-1'}); assert.equal(r.runId,'run-1'); assert.equal(r.channel,'manual');
});
test('manual run id from metadata must equal durable operation',async()=>{const {resolver}=harness();await rejects(()=>call(resolver,{run_id:'run-x'}),'SHARED_ADMISSION_RUN_MISMATCH');});
test('manual paused run mismatch fails closed',async()=>{
  const op={operation_id:'manual-2',conversation_key:KEY,tab_id:7,active_service:'search',run_id:'run-1',status:'requesting'};
  const {resolver}=harness({operation:op,run:{run_id:'run-1',status:'running',active_service:'search',tab_id:7,conversation_id:CID}});
  await rejects(()=>call(resolver,{run_id:'run-1'}),'SHARED_ADMISSION_PAUSED_RUN_MISMATCH');
});
test('autorun resolves only current requesting run owned by this worker session',async()=>{
  const run={run_id:'run-9',status:'requesting',active_service:'search',tab_id:7,conversation_id:CID,request_worker_session_id:'worker-1'};
  const {resolver}=harness({manual:false,operation:null,run});
  const r=await resolver.resolveContext({command:{method:'genSearch'},metadata:{conversation_key:KEY,policy:{channel:'autorun'},run_id:'run-9'},folderId:'folder',requestId:'req-2'});
  assert.deepEqual({...r},{authorized:true,owner:KEY,jobId:'run-9',scopeId:'run-9',runId:'run-9',channel:'autorun'});
});
test('autorun missing run id fails closed',async()=>{const {resolver}=harness({manual:false,operation:null});await rejects(()=>call(resolver,{policy:{channel:'autorun'}}),'SHARED_ADMISSION_AUTORUN_REQUIRED');});
test('autorun worker session mismatch fails closed',async()=>{
 const run={run_id:'run-9',status:'requesting',active_service:'search',tab_id:7,conversation_id:CID,request_worker_session_id:'other'};
 const {resolver}=harness({manual:false,operation:null,run});await rejects(()=>resolver.resolveContext({command:{method:'search'},metadata:{conversation_key:KEY,policy:{channel:'autorun'},run_id:'run-9'},folderId:'folder',requestId:'req'}),'SHARED_ADMISSION_RUN_NOT_OWNED');
});
test('autorun non-requesting or terminal run fails closed',async()=>{
 for(const status of ['paused','stopped','error']){const run={run_id:'run-9',status,active_service:'search',tab_id:7,conversation_id:CID,request_worker_session_id:'worker-1'};const {resolver}=harness({manual:false,operation:null,run});await assert.rejects(()=>resolver.resolveContext({command:{method:'search'},metadata:{conversation_key:KEY,policy:{channel:'autorun'},run_id:'run-9'},folderId:'folder',requestId:'req'}));}
});
test('metadata cannot create credential-check authority through resolver',async()=>{const {resolver}=harness({manual:false,operation:null});await rejects(()=>resolver.resolveContext({command:{method:'search'},metadata:{conversation_key:KEY,policy:{channel:'credential_check'}},folderId:'folder',requestId:'req'}),'SHARED_ADMISSION_AUTORUN_REQUIRED');});
test('unavailable guard always fails closed without network callback contract',async()=>{const g=F.unavailableGuard('X');await rejects(()=>g.executeLegacy(),'X');});

test('install composes resolver, policy and legacy guard without exposing chat metadata as authority',async()=>{
 let capturedResolver,createdPolicy=false,mirror=false;
 const policyFactory={create(args){createdPolicy=typeof args.getSettings==='function'&&typeof args.getPolicy==='function';return {bindJob:async()=>{},reserve:async()=>({allowed:true}),settle:async()=>{},recover:async()=>{}};}};
 const legacyFactory={createRunMirror({patchAutoRun}){mirror=typeof patchAutoRun==='function';return async()=>{};},create({policy,resolveContext}){capturedResolver=resolveContext;return {executeLegacy:async()=>({policy,ctx:await resolveContext({command:{method:'search'},metadata:{conversation_key:KEY,policy:{channel:'manual'},run_id:null},folderId:'folder',requestId:'req'})})};}};
 const {state}=harness();
 const installed=F.install({policyFactory,legacyFactory,normalizeConversationKey:v=>v,getBinding:async()=>binding,getManualMode:async()=>true,getServiceContext:async()=>({active_service:'search'}),getAutoRun:async()=>null,getManualOperation:async()=>state.operation,assertTabConversation:async()=>state.identity,patchAutoRun:async()=>{},getSettings:async()=>({}),getSearchPolicy:async()=>({}),workerSessionId:'worker-1',isRunTerminal:()=>false});
 assert.equal(installed.ready,true);assert.equal(createdPolicy,true);assert.equal(mirror,true);assert.equal(typeof capturedResolver,'function');const r=await installed.guard.executeLegacy();assert.equal(r.ctx.jobId,'manual-1');
});
test('search batch manual state resolves to durable manual operation and ignores batch metadata authority',async()=>{
 const op={operation_id:'manual-batch-1',conversation_key:KEY,tab_id:7,active_service:'search',run_id:null,status:'search_batch_requesting',batch_job_id:'user-visible-job'};
 const {resolver}=harness({operation:op});
 const r=await call(resolver,{job_id:'attacker-job',batch_item_id:'attacker-item'});
 assert.equal(r.jobId,'manual-batch-1');assert.equal(r.scopeId,'manual-batch-1');
});
