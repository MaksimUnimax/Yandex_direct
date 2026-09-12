import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import * as fake from './idb_test_double.mjs';

const KEY='https://chatgpt.com|11111111-1111-4111-8111-111111111111';
const CID='11111111-1111-4111-8111-111111111111';
const manualOps={ [KEY]: {operation_id:'manual-1',conversation_key:KEY,tab_id:7,active_service:'search',run_id:null,status:'requesting'} };
const policyModel={
  normalizeSearchPolicy(v={}){return {manual_enabled:v.manual_enabled!==false,autorun_enabled:v.autorun_enabled!==false,allowed_methods:Array.isArray(v.allowed_methods)?v.allowed_methods:['search','genSearch'],max_requests_per_run:Number(v.max_requests_per_run||100),max_cost_rub_per_run:Number(v.max_cost_rub_per_run||100),method_cost_rub:{search:0.488,genSearch:5.08,...(v.method_cost_rub||{})}};},
  searchDecision({policy,channel,method,credentialState,run={}}){
    const p=this.normalizeSearchPolicy(policy);const cost=Number(p.method_cost_rub[method]||0);
    if(credentialState!=='PRESENT')return{allow:false,reason:'CREDENTIALS_NOT_READY',estimated_cost_rub:cost,policy:p};
    if(channel==='manual'&&p.manual_enabled!==true)return{allow:false,reason:'MANUAL_DISABLED',estimated_cost_rub:cost,policy:p};
    if(!p.allowed_methods.includes(method))return{allow:false,reason:'METHOD_NOT_ALLOWED',estimated_cost_rub:cost,policy:p};
    if(Number(run.requests_executed||0)>=p.max_requests_per_run)return{allow:false,reason:'MAX_REQUESTS',estimated_cost_rub:cost,policy:p};
    if(Number(run.estimated_cost_rub||0)+cost>p.max_cost_rub_per_run)return{allow:false,reason:'MAX_COST',estimated_cost_rub:cost,policy:p};
    return{allow:true,reason:null,estimated_cost_rub:cost,policy:p};
  }
};
const ctx=vm.createContext({
  ...fake,console,crypto:globalThis.crypto,structuredClone,TextEncoder,setTimeout,clearTimeout,
  YMBPolicyModel:policyModel,
  YMBCredentialRegistry:{capabilityForService(){return {state:'PRESENT'};}},
  WordstatAutorunModel:{isTerminalStatus:s=>['stopped','error'].includes(s)},
  WORKER_SESSION_ID:'worker-1',
  normalizeConversationKey:v=>{if(v!==KEY)throw new Error('bad key');return v;},
  getBinding:async()=>({conversation_key:KEY,conversation_id:CID}),
  getManualMode:async()=>true,
  getServiceContext:async()=>({active_service:'search'}),
  getAutoRun:async()=>null,
  assertTabConversation:async()=>({conversation_key:KEY,conversation_id:CID}),
  patchAutoRun:async()=>null,
  getSettings:async()=>({credentials:{search:{api_key:'x',folder_id:'folder'}}}),
  getPolicyForService:async()=>({manual_enabled:true,allowed_methods:['search','genSearch'],max_requests_per_run:10,max_cost_rub_per_run:10,method_cost_rub:{search:0.488,genSearch:5.08}}),
  chrome:{storage:{local:{get:async key=>({[key]:manualOps})}}}
});ctx.globalThis=ctx;
for(const file of ['search_async_policy.js','search_legacy_admission.js'])vm.runInContext(fs.readFileSync(new URL('../candidate/shared/'+file,import.meta.url),'utf8'),ctx,{filename:file});
vm.runInContext(fs.readFileSync(new URL('../candidate/search_admission_worker_binding.js',import.meta.url),'utf8'),ctx,{filename:'search_admission_worker_binding.js'});

test('auto install with actual B5 factories becomes ready',()=>{assert.equal(ctx.YMBSearchAdmissionBinding.ready,true);assert.equal(typeof ctx.YMBSearchAdmissionGuard.executeLegacy,'function');});
test('actual composed guard calls provider once after trusted resolver and ledger',async()=>{
 let calls=0;const result=await ctx.YMBSearchAdmissionGuard.executeLegacy({command:{method:'search'},metadata:{conversation_key:KEY,run_id:null,policy:{channel:'manual'}},folderId:'folder',requestId:'req-1'},async()=>{calls++;return{ok:true,request_executed:true,http_status:200,report_text:'ok'};});
 assert.equal(calls,1);assert.equal(result.report_text,'ok');
});
test('duplicate request id cannot execute provider twice',async()=>{
 let calls=0;await assert.rejects(()=>ctx.YMBSearchAdmissionGuard.executeLegacy({command:{method:'search'},metadata:{conversation_key:KEY,run_id:null,policy:{channel:'manual'}},folderId:'folder',requestId:'req-1'},async()=>{calls++;return{ok:true,request_executed:true,http_status:200};}));assert.equal(calls,0);
});
test('spoofed autorun channel is rejected before provider',async()=>{
 let calls=0;await assert.rejects(()=>ctx.YMBSearchAdmissionGuard.executeLegacy({command:{method:'search'},metadata:{conversation_key:KEY,run_id:null,policy:{channel:'autorun'}},folderId:'folder',requestId:'req-2'},async()=>{calls++;return{ok:true,request_executed:true,http_status:200};}));assert.equal(calls,0);
});
