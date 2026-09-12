// B3 runtime + B4 real policy/normalizer seams. Store, operation parsing and wire are fixtures.
// The IDB backend remains the preserved deterministic double, never browser evidence.
import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import vm from 'node:vm';import crypto from 'node:crypto';import * as fake from './idb_test_double.mjs';
const ctx=vm.createContext({...fake,console,URL,TextDecoder,Uint8Array,atob});ctx.globalThis=ctx;
for(const name of ['policy_model','credential_registry','search_xml'])vm.runInContext(fs.readFileSync(new URL(`../baseline/shared/${name}.js`,import.meta.url),'utf8'),ctx);
for(const name of ['normalizer','policy','runtime'])vm.runInContext(fs.readFileSync(new URL(`../candidate/shared/search_async_${name}.js`,import.meta.url),'utf8'),ctx);
const runtimeSource=fs.readFileSync(new URL('../candidate/shared/search_async_runtime.js',import.meta.url));
const owner='https://chatgpt.com|11111111-1111-4111-8111-111111111111';let n=0;
const xml='<yandexsearch><response><results><grouping><group><doc><url>https://example.test/item</url><title>Тест 💎</title></doc></group></grouping></results></response></yandexsearch>';
const raw=x=>JSON.stringify({id:'op-1',done:true,response:{rawData:Buffer.from(x).toString('base64')}});
async function fixture(options={}){
 const jobId='seam-'+(++n),folderId='folder-'+n;
 const state={now:100000,wireCalls:0,localClaims:0,finish:null,normalization:null,control:null,failWrite:false,events:[],
  item:{index:0,query:'тест',state:'RESULT_SAVED',operation_id:'op-1'},record:{operation_id:'op-1',raw_text:raw(xml)},
  settings:{credentials:{search:{api_key:'SYNTHETIC_NOT_A_KEY',folder_id:folderId}}},searchPolicy:{max_requests_per_run:20,max_cost_rub_per_run:10},...options};
 const policyOptions={workerId:'worker-A',getPolicy:async()=>state.searchPolicy,getSettings:async()=>state.settings,getAutoRun:async()=>null,now:()=>state.now};
 const policy=ctx.YMBSearchAsyncPolicy.create(policyOptions);await policy.bindJob({jobId,owner,folderId,scopeId:jobId});
 const store={
  peekNext:async()=>({item:state.item,folder_id:folderId,parameters:{},progress:{}}),
  claim:async()=>{state.localClaims++;state.events.push('local-claim');return{allowed:true,item:state.item};},
  finishSubmit:async a=>{state.events.push('local-settle');if(state.failWrite)throw new Error('injected durable-write failure');state.finish=a;},
  finishCollect:async a=>{if(state.failWrite)throw new Error('injected durable-write failure');state.finish=a;},
  finishNormalization:async a=>{state.normalization=a;return{state:a.errorCode?'PARSE_FAILED':'SUCCEEDED'};},
  getSummary:async()=>({fixture:true}),readItem:async()=>state.item,readResult:async()=>state.record,
  recover:async()=>{state.events.push('local-recover');},control:async a=>{state.control=a.action;}
 };
 const protocol={MIN_FIRST_POLL_MS:300000,MAX_SLICE:25,parseOperation(text,id){const op=JSON.parse(text);if(op.id!==id)throw new Error('operation mismatch');return{outcome:'received',rawData:op.response.rawData};}};
 const transport={execute:async a=>{const d=await a.admit();if(!d.allowed)return{ok:false,request_executed:false,code:'ASYNC_ADMISSION_DENIED'};
  state.events.push('wire');state.wireCalls++;state.atWire=await policy.getSummary(jobId,owner);
  return state.wire||{ok:true,request_executed:true,http_status:200,operation:{operation_id:'op-1',outcome:'waiting'},raw_text:'{"id":"op-1","done":false}'};}};
 const makeRuntime=(p=policy,workerId='worker-A')=>ctx.YMBSearchAsyncRuntime.create({store,protocol,transport,
  authorize:async a=>a.owner===owner,getCredential:async()=>state.settings.credentials.search,policy:p,
  normalizeRaw:ctx.YMBSearchAsyncNormalizer.create({maxRawBytes:1024*1024}),workerId,now:()=>state.now});
 const runtime=makeRuntime();const args=extra=>({jobId,owner,attemptId:'attempt-1',kind:'submit',index:0,...extra});
 return{jobId,folderId,state,policy,store,runtime,args,policyOptions,makeRuntime};
}
test('B3 runtime exact bytes unchanged for new dependency seam tests',()=>assert.equal(crypto.createHash('sha256').update(runtimeSource).digest('hex'),'e8be98e7bd692321e44ff3af147415f235c9e4367de508982dc60f88b596de6f'));
test('real normalizer feeds B3 local normalization, no provider or policy reservation',async()=>{
 const f=await fixture();const r=await f.runtime.normalizeSaved(f.args());assert.equal(r.normalized,true);assert.equal(f.state.normalization.normalized.results[0].title,'Тест 💎');assert.equal(f.state.normalization.normalized.validation.usable_for_url_comparison,true);assert.equal(f.state.wireCalls,0);assert.equal((await f.policy.getSummary(f.jobId,owner)).submissions,0);
});
test('XML 15 empty is explicit observation through B3, not fabricated rows',async()=>{
 const f=await fixture({record:{operation_id:'op-1',raw_text:raw('<yandexsearch><response><error code="15">empty</error></response></yandexsearch>')}});const r=await f.runtime.normalizeSaved(f.args());assert.equal(r.normalized,true);assert.equal(f.state.normalization.normalized.validation.empty_proven,true);assert.equal(f.state.normalization.normalized.result_count,0);
});
for(const content of ['<broken>', '<yandexsearch><response/></yandexsearch>', '<yandexsearch><response><error code="2">bad query</error></response></yandexsearch>'])test('rejected XML remains saved with failed-normalization state, never replayed: '+content,async()=>{
 const f=await fixture({record:{operation_id:'op-1',raw_text:raw(content)}});const before=f.state.record.raw_text;const r=await f.runtime.normalizeSaved(f.args());assert.equal(r.ok,false);assert.equal(r.raw_preserved,true);assert.equal(f.state.normalization.errorCode,'ASYNC_NORMALIZATION_FAILED');assert.equal(f.state.record.raw_text,before);assert.equal(f.state.wireCalls,0);
});
test('real policy commit precedes fake wire; B3 settles exact context once',async()=>{
 const f=await fixture();const r=await f.runtime.step(f.args());assert.equal(r.ok,true);assert.deepEqual(f.state.events,['local-claim','wire','local-settle']);assert.equal(f.state.atWire.pending,1);assert.equal(f.state.atWire.estimated_budget_charge_microrub,30500);assert.equal(f.state.finish.operationId,'op-1');const p=await f.policy.getSummary(f.jobId,owner);assert.equal(p.pending,0);assert.equal(p.submissions,1);assert.equal('raw_text' in r,false);
});
test('live manual policy disabled gives no wire invocation and no leaked reservation',async()=>{
 const f=await fixture();f.state.searchPolicy.manual_enabled=false;const r=await f.runtime.step(f.args());assert.equal(r.request_executed,false);assert.equal(f.state.wireCalls,0);assert.equal(f.state.finish.outcome,'not_sent');const p=await f.policy.getSummary(f.jobId,owner);assert.equal(p.submissions,0);assert.equal(p.pending,0);
});
test('B3 uncertain submit drives real policy hold; subsequent submit gets zero wire work',async()=>{
 const f=await fixture({wire:{ok:false,request_executed:'UNKNOWN',code:'ASYNC_TIMEOUT',outcome:'unknown'}});await f.runtime.step(f.args());assert.equal((await f.policy.getSummary(f.jobId,owner)).holds,1);f.state.now+=1000;const r=await f.runtime.step(f.args({attemptId:'second'}));assert.equal(r.request_executed,false);assert.equal(f.state.wireCalls,1);assert.equal((await f.policy.getSummary(f.jobId,owner)).estimated_budget_charge_microrub,30500);
});
test('B3 uncertain GET saved as read_error does not create unknown paid-submit hold',async()=>{
 const f=await fixture({wire:{ok:false,request_executed:'UNKNOWN',code:'ASYNC_TIMEOUT',outcome:'read_error'}});const r=await f.runtime.step(f.args({kind:'collect'}));assert.equal(r.outcome,'read_error');const p=await f.policy.getSummary(f.jobId,owner);assert.equal(p.holds,0);assert.equal(p.submissions,0);assert.equal(p.polls,1);assert.equal(p.estimated_budget_charge_microrub,0);
});
test('durable local write failure preserves policy hold rather than a success report',async()=>{
 const f=await fixture({failWrite:true});const r=await f.runtime.step(f.args());assert.equal(r.code,'ASYNC_PERSISTENCE_FAILED');assert.equal(f.state.wireCalls,1);const p=await f.policy.getSummary(f.jobId,owner);assert.equal(p.holds,1);assert.equal(p.pending,0);assert.equal(p.estimated_budget_charge_microrub,30500);
});
test('wrong owner stops B3 before local claim or policy access',async()=>{
 const f=await fixture();await assert.rejects(()=>f.runtime.step(f.args({owner:'another-chat'})),e=>e.code==='ASYNC_RUNTIME_NOT_AUTHORIZED');assert.equal(f.state.localClaims,0);assert.equal(f.state.wireCalls,0);
});
test('stale GET recovery calls real policy after local recovery without provider replay',async()=>{
 const f=await fixture();await f.policy.reserve({...f.args({kind:'collect'}),folderId:f.folderId});const p=ctx.YMBSearchAsyncPolicy.create({...f.policyOptions,workerId:'worker-B'});const runtime=f.makeRuntime(p,'worker-B');const r=await runtime.recover(f.args());assert.equal(r.ok,true);assert.equal(r.request_executed,false);assert.equal(f.state.wireCalls,0);assert.equal((await p.getSummary(f.jobId,owner)).holds,0);assert.deepEqual(f.state.events,['local-recover']);
});
