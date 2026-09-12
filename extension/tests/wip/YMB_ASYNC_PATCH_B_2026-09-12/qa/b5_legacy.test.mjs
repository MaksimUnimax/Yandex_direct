import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {webcrypto,randomUUID} from 'node:crypto';
import * as fake from './idb_test_double.mjs';
const base=new URL('../owner014/',import.meta.url),cand=new URL('../candidate/',import.meta.url);
let seq=0;
const xml='<?xml version="1.0" encoding="utf-8"?><yandexsearch><response><found>1</found><results><grouping><group><doc><url>https://example.test/item</url><domain>example.test</domain><title>Тест</title><passages><passage>Описание</passage></passages></doc></group></grouping></results></response></yandexsearch>';
const FixedDate=class extends Date {constructor(...a){super(...(a.length?a:['2026-09-12T06:00:00Z']));} static now(){return 1789192800000;}};
function setup({patched=true,withGuard=true,rawPolicy={},maxRequests=100,initialRun={}}={}){
 const n=++seq,owner=`legacy-owner-${n}`,runId=`run-${n}`,folder=`folder-${n}`,key=`SYNTHETIC-${n}`;
 let now=1000;const run={run_id:runId,active_service:'search',requests_executed:0,estimated_cost_rub:0,status:'requesting',unrelated:'PRESERVED',...initialRun};
 const settings={credentials:{search:{api_key:key,folder_id:folder},wordstat:{api_key:'WS',folder_id:'WS-FOLDER'},webmaster:{oauth_token:'WM',user_id:'123'},metrika:{oauth_token:'M'},direct:{oauth_token:'D',client_login:'client'}}};
 const wire=[];let handler=(url,init)=>{
  if(url.includes('/v2/web/search'))return new Response(JSON.stringify({rawData:Buffer.from(xml).toString('base64')}));
  if(url.includes('/v2/gen/search'))return new Response(JSON.stringify({message:{content:'Answer',role:'ROLE_ASSISTANT'},sources:[]}));
  if(url.includes('wordstat'))return new Response(JSON.stringify({regions:[]}));
  if(url.includes('webmaster'))return new Response(JSON.stringify({hosts:[]}));
  if(url.includes('metrika'))return new Response(JSON.stringify({counters:[]}));
  if(url.includes('direct'))return new Response(JSON.stringify({result:{Campaigns:[]}}));
  throw new Error('Unexpected fixture route '+url);
 };
 const ctx=vm.createContext({...fake,console,TextEncoder,TextDecoder,URL,Date:FixedDate,atob,btoa,Uint8Array,crypto:{...webcrypto,randomUUID},performance:{now:()=>100},setTimeout,clearTimeout,
  chrome:{storage:{local:{get:async()=>({}),set:async()=>{}}}},
  fetch:async(url,init)=>{wire.push({url,init});return handler(url,init);}});ctx.globalThis=ctx;
 const load=p=>vm.runInContext(fs.readFileSync(p,'utf8'),ctx,{filename:String(p)});
 for(const f of ['product.js','service_registry.js','policy_model.js','credential_registry.js','wordstat_protocol.js','search_xml.js','search_protocol.js','webmaster_protocol.js','metrika_protocol.js','direct_protocol.js'])load(new URL('shared/'+f,base));
 ctx.YMBCredentialRuntime={settings:async()=>settings,save:async(service,value)=>Object.assign(settings.credentials[service],value),load:async()=>settings.credentials};
 load(patched?new URL('legacy/shared/phase3_provider_runtime.js',cand):new URL('shared/phase3_provider_runtime.js',base));
 for(const f of ['phase4_provider_runtime.js','phase5_provider_runtime.js'])load(new URL('shared/'+f,base));
 load(new URL('shared/search_async_policy.js',cand));load(new URL('shared/search_legacy_admission.js',cand));
 const publish=ctx.YMBSearchLegacyAdmission.createRunMirror({patchAutoRun:async(k,fn)=>{assert.equal(k,owner);Object.assign(run,fn({...run}));return run;}});
 const p=ctx.YMBSearchAsyncPolicy.create({workerId:`w-${n}`,getPolicy:async()=>({manual_enabled:true,autorun_enabled:true,max_requests_per_run:maxRequests,max_cost_rub_per_run:100,...rawPolicy}),getSettings:async()=>settings,getAutoRun:async()=>run,now:()=>now,publishRunTotals:publish});
 let resolver=async({metadata})=>({authorized:metadata.conversation_key===owner,owner,jobId:`legacy-${n}-${metadata.policy?.channel||'manual'}`,scopeId:'shared',runId:metadata.run_id??null,channel:metadata.policy?.channel||'manual'});
 const guard=ctx.YMBSearchLegacyAdmission.create({policy:p,resolveContext:a=>resolver(a),now:()=>now,sleep:async ms=>{now+=ms;}});if(withGuard)ctx.YMBSearchAdmissionGuard=guard;
 const metadata=(id='request-1')=>({request_id:id,conversation_key:owner,run_id:runId,policy:{channel:'manual',active_service:'search'}});
 const execute=(method='search',extra={})=>ctx.YMBPhase5ProviderRuntime.execute('search',{method,queryText:'тест',...(method==='genSearch'?{confirmBillable:true}:{})},metadata(extra.id));
 return{ctx,wire,settings,run,p,guard,owner,runId,folder,metadata,execute,tick:()=>{now+=2000;},setWire:fn=>{handler=fn;},setResolver:fn=>{resolver=fn;}};
}
const parsed=r=>JSON.parse(JSON.stringify(r));
function comparable(r){const x=parsed(r);const clean=v=>{if(v&&typeof v==='object')for(const k of Object.keys(v)){if(k==='folderId')v[k]='FOLDER';else if(k==='conversation_key')v[k]='OWNER';else if(k==='run_id')v[k]='RUN';else clean(v[k]);}};clean(x);if(x.report_envelope)x.report_text=JSON.stringify(x.report_envelope);return x;}
for(const method of ['search','genSearch'])test(`actual ${method} provider produces same result with optional guard absent`,async()=>{
 const before=setup({patched:false,withGuard:false}),after=setup({withGuard:false});
 const a=await before.execute(method),b=await after.execute(method);assert.deepEqual(comparable(a),comparable(b));assert.equal(before.wire.length,1);assert.equal(after.wire.length,1);
});
for(const method of ['search','genSearch'])test(`actual ${method} provider enters common gate before fetch; output preserved`,async()=>{
 const f=setup();let saw=false;const oldFetch=f.ctx.fetch;f.ctx.fetch=async(...a)=>{saw=true;assert.equal(f.run.requests_executed,1);return oldFetch(...a);};
 const r=await f.execute(method);assert.ok(saw);assert.equal(r.ok,true);assert.equal(r.request_executed,true);assert.equal(f.run.requests_executed,1);assert.equal(f.run.estimated_cost_rub,method==='search'?.488:5.08);assert.equal(f.run.unrelated,'PRESERVED');
});
test('real legacy sender and deferred reservation compete in same run',async()=>{
 const f=setup({maxRequests:1});const j='async-'+seq;await f.p.bindJob({jobId:j,owner:f.owner,folderId:f.folder,scopeId:'different-alias',runId:f.runId});
 const a={jobId:j,owner:f.owner,folderId:f.folder,index:0,attemptId:'d1',kind:'submit'};
 const outcomes=await Promise.allSettled([f.execute(),f.p.reserve(a)]);const sync=outcomes[0].status==='fulfilled';const d=outcomes[1].status==='fulfilled'&&outcomes[1].value.allowed;
 assert.equal(Number(sync)+Number(d),1);assert.equal(f.wire.length,Number(sync));assert.equal(f.run.requests_executed,1);
 if(d)await f.p.settle({...a,request_executed:true,http_status:200,outcome:'accepted',local_saved:true});
});
test('second legacy request cannot spend the same last budget slot',async()=>{
 const f=setup({maxRequests:1});await f.execute();f.tick();await assert.rejects(()=>f.execute('search',{id:'request-2'}),e=>e.code==='SHARED_ADMISSION_DENIED'&&e.request_executed===false);assert.equal(f.wire.length,1);
});
test('same admitted request ID never replays legacy network callback',async()=>{
 const f=setup();await f.execute();f.tick();await assert.rejects(()=>f.execute(),e=>e.code==='SHARED_ADMISSION_DENIED');assert.equal(f.wire.length,1);
});
test('unknown legacy fetch blocks following deferred sends',async()=>{
 const f=setup();f.setWire(()=>{throw new Error('network');});await assert.rejects(()=>f.execute(),e=>e.request_executed==='UNKNOWN');assert.equal(f.wire.length,1);
 const j='async-'+seq;await f.p.bindJob({jobId:j,owner:f.owner,folderId:f.folder,scopeId:'alias',runId:f.runId});
 const r=await f.p.reserve({jobId:j,owner:f.owner,folderId:f.folder,index:0,attemptId:'a',kind:'submit'});assert.equal(r.reason,'POLICY_RECONCILIATION_REQUIRED');
});
for(const status of [401,403,500])test(`legacy HTTP ${status} preserves provider report and credits estimate`,async()=>{
 const f=setup();f.setWire(()=>new Response(JSON.stringify({code:'ERROR',message:'fixture'}),{status}));const r=await f.execute();assert.equal(r.http_status,status);assert.equal(r.ok,false);assert.ok(r.report_text);assert.equal(f.run.estimated_cost_rub,0);assert.equal(f.run.requests_executed,1);
});
test('legacy body parse failure still records that request happened, no automatic retry',async()=>{
 const f=setup();f.setWire(()=>new Response('not-json'));await assert.rejects(()=>f.execute('genSearch'),e=>e.request_executed===true&&e.automatic_retry===false);assert.equal(f.wire.length,1);assert.equal(f.run.requests_executed,1);
});
test('credential or command preflight failure performs neither fetch nor admission',async()=>{
 const f=setup();let admissions=0;f.ctx.YMBSearchAdmissionGuard={executeLegacy:async()=>{admissions++;}};delete f.settings.credentials.search.api_key;await assert.rejects(()=>f.execute(),e=>e.code==='API_KEY_MISSING');assert.equal(f.wire.length,0);assert.equal(admissions,0);
});
test('missing active guard method fails closed, not silent legacy fallback',async()=>{
 const f=setup();f.ctx.YMBSearchAdmissionGuard={};await assert.rejects(()=>f.execute(),e=>e.code==='SHARED_ADMISSION_UNAVAILABLE'&&e.request_executed===false);assert.equal(f.wire.length,0);
});
test('context resolver denies owner before any provider callback',async()=>{
 const f=setup();f.setResolver(async()=>({authorized:false}));await assert.rejects(()=>f.execute(),e=>e.code==='SHARED_ADMISSION_CONTEXT_INVALID');assert.equal(f.wire.length,0);
});
test('context resolver errors do not leak supplied exception details',async()=>{
 const f=setup();f.setResolver(async()=>{throw new Error('SECRET');});await assert.rejects(()=>f.execute(),e=>e.code==='SHARED_ADMISSION_CONTEXT_UNAVAILABLE'&&!e.message.includes('SECRET'));assert.equal(f.wire.length,0);
});
test('credential Check still requires its existing explicit billable confirmation',async()=>{
 const f=setup();await assert.rejects(()=>f.ctx.YMBPhase3ProviderRuntime.checkCloud('search'),e=>e.code==='SEARCH_CHECK_CONFIRM_REQUIRED');assert.equal(f.wire.length,0);
});
test('explicit Check works even when Manual disabled or old key marked invalid',async()=>{
 const f=setup({rawPolicy:{manual_enabled:false,autorun_enabled:false,allowed_methods:[],max_cost_rub_per_run:0}});f.settings.credentials.search.check_state='INVALID_OR_EXPIRED';
 const r=await f.ctx.YMBPhase3ProviderRuntime.checkCloud('search',{confirmBillable:true});assert.equal(r.ok,true);assert.equal(r.state,'PRESENT');assert.equal(f.wire.length,1);assert.equal(f.run.requests_executed,0);
});
test('plain metadata cannot forge private credential Check capability',async()=>{
 const f=setup({rawPolicy:{manual_enabled:false}});await assert.rejects(()=>f.ctx.YMBPhase3ProviderRuntime.executeCloud('search',{queryText:'x'},{...f.metadata(),channel:'credential_check',credentialCheckAuthorized:true}),e=>e.code==='SHARED_ADMISSION_DENIED');assert.equal(f.wire.length,0);
});
test('context resolver cannot promote arbitrary operation to credential Check',async()=>{
 const f=setup();f.setResolver(async()=>({authorized:true,channel:'credential_check'}));await assert.rejects(()=>f.execute(),e=>e.code==='SHARED_CHECK_CONSENT_REQUIRED');assert.equal(f.wire.length,0);
});
for(const [service,command] of [['wordstat',{method:'getRegionsTree'}],['webmaster',{method:'listHosts'}],['metrika',{method:'listCounters'}],['direct',{method:'listCampaigns'}]])test(`actual ${service} route ignores Search gate and preserves result`,async()=>{
 const a=setup({patched:false,withGuard:false}),b=setup();b.ctx.YMBSearchAdmissionGuard={executeLegacy:()=>{throw new Error('must not call Search guard');}};
 const ra=await a.ctx.YMBPhase5ProviderRuntime.execute(service,command,{request_id:'stable-id'});const rb=await b.ctx.YMBPhase5ProviderRuntime.execute(service,command,{request_id:'stable-id'});
 assert.deepEqual(comparable(ra),comparable(rb));assert.equal(b.wire.length,1);assert.equal(b.run.requests_executed,0);
});
test('settlement storage failure preserves received report and marks stop',async()=>{
 const f=setup();const policy={bindJob:a=>f.p.bindJob(a),reserve:a=>f.p.reserve(a),settle:async()=>{throw new Error('idb-failure');}};
 f.ctx.YMBSearchAdmissionGuard=f.ctx.YMBSearchLegacyAdmission.create({policy,resolveContext:async()=>({authorized:true,owner:f.owner,jobId:'legacy-test-'+seq,scopeId:'shared',runId:f.runId,channel:'manual'})});
 const r=await f.execute();assert.equal(r.ok,true);assert.ok(r.report_text.includes('SEARCH_RESULT_V1'));assert.equal(r.admission_warning,'SHARED_ADMISSION_SETTLEMENT_FAILED');assert.equal(r.stop_required,true);assert.equal(f.wire.length,1);
 f.tick();await assert.rejects(()=>f.execute('search',{id:'next'}));assert.equal(f.wire.length,1);
});
test('run mirror serializes writes and rejects same revision conflict',async()=>{
 const f=setup();const pub=f.ctx.YMBSearchLegacyAdmission.createRunMirror({patchAutoRun:async(k,fn)=>{await new Promise(r=>setTimeout(r,1));Object.assign(f.run,fn({...f.run}));}});
 const m={owner:f.owner,runId:f.runId,scopeId:'scope',requests_executed:2,estimated_cost_rub:1,revision:2};
 await Promise.all([pub(m),pub({...m,requests_executed:1,estimated_cost_rub:.488,revision:1})]);assert.equal(f.run.requests_executed,2);
 await assert.rejects(()=>pub({...m,requests_executed:3}),e=>e.code==='SHARED_RUN_MIRROR_REVISION_CONFLICT');assert.equal(f.run.unrelated,'PRESERVED');
});
test('run mirror refuses changed/missing run and never creates a replacement',async()=>{
 const f=setup();const pub=f.ctx.YMBSearchLegacyAdmission.createRunMirror({patchAutoRun:async(k,fn)=>fn(null)});await assert.rejects(()=>pub({owner:f.owner,runId:f.runId,scopeId:'scope',requests_executed:1,estimated_cost_rub:.488,revision:1}),e=>e.code==='SHARED_RUN_MIRROR_CHANGED');
});
test('admission-rate waiting is bounded and never retries a provider callback',async()=>{
 const f=setup();let reservations=0,fetches=0,time=0,waits=0;
 const policy={bindJob:async()=>{},reserve:async()=>++reservations===1?{allowed:false,reason:'ASYNC_GLOBAL_RATE_WAIT',next_allowed_at:200}:{allowed:true},settle:async()=>({settled:true})};
 const context=()=>({authorized:true,owner:f.owner,jobId:'rate',scopeId:'shared',runId:null,channel:'manual'});
 const guard=f.ctx.YMBSearchLegacyAdmission.create({policy,resolveContext:context,now:()=>time,sleep:async ms=>{waits++;time+=ms;}});
 const result=await guard.executeLegacy({command:{method:'search'},folderId:f.folder,requestId:'r'},async()=>{fetches++;return{ok:true,request_executed:true,http_status:200};});assert.ok(result.ok);assert.equal(reservations,2);assert.equal(fetches,1);assert.equal(waits,1);
});
test('permanent rate denial and stalled clock cannot spin indefinitely',async()=>{
 const f=setup();let reservations=0,fetches=0,sleeps=0;
 const policy={bindJob:async()=>{},reserve:async()=>{reservations++;return{allowed:false,reason:'ASYNC_GLOBAL_RATE_WAIT',next_allowed_at:200};},settle:async()=>{}};
 const guard=f.ctx.YMBSearchLegacyAdmission.create({policy,resolveContext:()=>({authorized:true,owner:f.owner,jobId:'rate2',scopeId:'s',runId:null,channel:'manual'}),now:()=>0,sleep:async()=>{sleeps++;}});
 await assert.rejects(()=>guard.executeLegacy({command:{method:'search'},folderId:f.folder,requestId:'r'},async()=>{fetches++;}),e=>e.request_executed===false);assert.equal(reservations,3);assert.equal(sleeps,2);assert.equal(fetches,0);
});
test('authorization changes during rate wait stop before provider',async()=>{
 const f=setup();let checks=0,fetches=0;
 const policy={bindJob:async()=>{},reserve:async()=>({allowed:false,reason:'ASYNC_GLOBAL_RATE_WAIT',next_allowed_at:100}),settle:async()=>{}};
 const guard=f.ctx.YMBSearchLegacyAdmission.create({policy,resolveContext:()=>({authorized:++checks===1,owner:f.owner,jobId:'rate3',scopeId:'s',runId:null,channel:'manual'}),now:()=>0,sleep:async()=>{}});
 await assert.rejects(()=>guard.executeLegacy({command:{method:'search'},folderId:f.folder,requestId:'r'},async()=>{fetches++;}));assert.equal(fetches,0);assert.equal(checks,2);
});
test('provider rechecks credentials after admission, changed key is not sent',async()=>{
 const f=setup();const guard=f.ctx.YMBSearchAdmissionGuard;f.ctx.YMBSearchAdmissionGuard={executeLegacy:async(a,once)=>guard.executeLegacy(a,async()=>{f.settings.credentials.search.api_key='CHANGED';return once();})};
 await assert.rejects(()=>f.execute(),e=>e.code==='SHARED_ADMISSION_CREDENTIAL_CHANGED'&&e.request_executed===false);assert.equal(f.wire.length,0);assert.equal(f.run.requests_executed,0);assert.equal(f.run.estimated_cost_rub,0);
});
