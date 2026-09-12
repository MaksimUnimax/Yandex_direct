import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import vm from 'node:vm';import crypto from 'node:crypto';
import * as fake from './idb_test_double.mjs';
const ctx=vm.createContext({...fake,console});ctx.globalThis=ctx;
for(const name of ['policy_model','credential_registry'])vm.runInContext(fs.readFileSync(new URL(`../baseline/shared/${name}.js`,import.meta.url),'utf8'),ctx);
const model=ctx.YMBPolicyModel,registry=ctx.YMBCredentialRegistry;
const baselineDecisions=JSON.stringify(['wordstat','search','webmaster','metrika','direct'].map(s=>model.decisionForService(s,{channel:'manual',credentialState:'PRESENT',method:model.normalizePolicyForService(s).allowed_methods[0]})));
vm.runInContext(fs.readFileSync(new URL('../candidate/shared/search_async_policy.js',import.meta.url),'utf8'),ctx);
const Factory=ctx.YMBSearchAsyncPolicy;let serial=0;
const OWNER='https://chatgpt.com|11111111-1111-4111-8111-111111111111';
function setup(overrides={}){
 const tag='policy-'+(++serial);const state={now:100000,policy:{max_requests_per_run:2000,max_cost_rub_per_run:100},settings:{credentials:{search:{api_key:'SYNTHETIC-NOT-A-REAL-KEY',folder_id:tag,check_state:'PRESENT'},wordstat:{api_key:'WORDSTAT-UNCHANGED',folder_id:'other'}}},run:null,...overrides};
 const options={workerId:'worker-A',getPolicy:async()=>state.policy,getSettings:async()=>state.settings,getAutoRun:async()=>state.run,now:()=>state.now};
 const P=Factory.create(options);const bind=(jobId=tag,extra={})=>P.bindJob({jobId,owner:OWNER,folderId:state.settings.credentials.search.folder_id,scopeId:tag,...extra});
 const args=(jobId=tag,attemptId='a',extra={})=>({jobId,owner:OWNER,folderId:state.settings.credentials.search.folder_id,attemptId,kind:'submit',index:0,...extra});
 const settle=(a,extra={})=>P.settle({...a,request_executed:true,http_status:200,outcome:'accepted',local_saved:true,operation_id:null,...extra});
 return{tag,state,P,bind,args,settle,options};
}
const rejected=(fn,code)=>assert.rejects(fn,e=>!code||e.code===code);
test('existing policy and credential modules remain exact global objects',()=>{
 assert.equal(ctx.YMBPolicyModel,model);assert.equal(ctx.YMBCredentialRegistry,registry);
 assert.equal(JSON.stringify(['wordstat','search','webmaster','metrika','direct'].map(s=>model.decisionForService(s,{channel:'manual',credentialState:'PRESENT',method:model.normalizePolicyForService(s).allowed_methods[0]}))),baselineDecisions);
});
test('dependencies and sub-100ms rate limit fail closed',()=>{
 const f=setup();assert.throws(()=>Factory.create({...f.options,minIntervalMs:99}));assert.throws(()=>Factory.create({...f.options,getPolicy:null}));
});
test('binding idempotent and immutable across owner/folder/scope',async()=>{
 const f=setup();assert.equal((await f.bind()).duplicate,false);assert.equal((await f.bind()).duplicate,true);
 for(const extra of [{owner:'other'},{folderId:'other'},{scopeId:'other'},{runId:'other'}])await rejected(()=>f.bind(f.tag,extra),'ASYNC_POLICY_REBIND_FORBIDDEN');
});
test('wrong owner and folder rejected without reserved budget',async()=>{
 const f=setup();await f.bind();await rejected(()=>f.P.reserve(f.args(f.tag,'x',{owner:'bad'})),'ASYNC_POLICY_WRONG_OWNER');await rejected(()=>f.P.reserve(f.args(f.tag,'x',{folderId:'bad'})),'ASYNC_POLICY_FOLDER_MISMATCH');assert.equal((await f.P.getSummary(f.tag,OWNER)).submissions,0);
});
test('reads live existing policy and never edits it or other credentials',async()=>{
 const f=setup();await f.bind();const original=JSON.stringify([f.state.policy,f.state.settings]);await f.P.reserve(f.args());assert.equal(JSON.stringify([f.state.policy,f.state.settings]),original);await f.settle(f.args());f.state.now+=201;
 f.state.policy.manual_enabled=false;assert.equal((await f.P.reserve(f.args(f.tag,'b'))).reason,'MANUAL_DISABLED');
});
test('existing search allowlist forbids async when ordinary search disabled',async()=>{
 const f=setup();await f.bind();f.state.policy.allowed_methods=['genSearch'];assert.equal((await f.P.reserve(f.args())).reason,'OPERATION_DISABLED');
});
for(const check_state of ['NO_ACCESS','INVALID_OR_EXPIRED'])test(`existing credential state ${check_state} blocks new requests`,async()=>{
 const f=setup();await f.bind();f.state.settings.credentials.search.check_state=check_state;assert.equal((await f.P.reserve(f.args())).allowed,false);
});
test('key removal and folder switch prevent admission',async()=>{
 const f=setup();await f.bind();f.state.settings.credentials.search.api_key='';assert.equal((await f.P.reserve(f.args())).reason,'NO_CREDENTIALS');
 const g=setup();await g.bind();const a=g.args();g.state.settings.credentials.search.folder_id='changed';await rejected(()=>g.P.reserve(a),'ASYNC_POLICY_CREDENTIAL_CONTEXT_CHANGED');
});
test('real policy uses conservative deferred cost, not sync tariff',async()=>{
 const f=setup();await f.bind();const r=await f.P.reserve(f.args());assert.equal(r.estimated_cost_rub,.0305);assert.equal(r.progress.estimated_budget_charge_microrub,30500);assert.equal(model.normalizeSearchPolicy().method_cost_rub.search,.488);
});
test('shared scoped limit prevents splitting two jobs to bypass a one-request budget',async()=>{
 const f=setup();f.state.policy.max_requests_per_run=1;await f.bind();await f.bind(f.tag+'-second');assert.equal((await f.P.reserve(f.args())).allowed,true);await f.settle(f.args());f.state.now+=201;
 assert.equal((await f.P.reserve(f.args(f.tag+'-second','second'))).reason,'REQUEST_LIMIT');
});
test('concurrent jobs in same scope grant exactly one reservation',async()=>{
 const f=setup();await f.bind();await f.bind(f.tag+'-second');const r=await Promise.all([f.P.reserve(f.args()),f.P.reserve(f.args(f.tag+'-second'))]);assert.equal(r.filter(x=>x.allowed).length,1);assert.equal((await f.P.getSummary(f.tag,OWNER)).pending,1);
});
test('same folder global rate spans scopes and has distinct POST/GET lanes',async()=>{
 const f=setup();await f.bind();await f.bind(f.tag+'-second',{scopeId:'different-scope'});await f.P.reserve(f.args());await f.settle(f.args());
 const a=f.args(f.tag+'-second','second');assert.equal((await f.P.reserve(a)).reason,'ASYNC_GLOBAL_RATE_WAIT');assert.equal((await f.P.reserve({...a,kind:'collect'})).allowed,true);
});
test('budget cost stops before exceeding saved maxCost',async()=>{
 const f=setup();f.state.policy.max_cost_rub_per_run=.030499;await f.bind();assert.equal((await f.P.reserve(f.args())).reason,'COST_LIMIT');assert.equal((await f.P.getSummary(f.tag,OWNER)).submissions,0);
});
test('known GET remains collectable after search budget exhaustion',async()=>{
 const f=setup();f.state.policy.max_cost_rub_per_run=.0305;f.state.policy.max_requests_per_run=1;await f.bind();await f.P.reserve(f.args());await f.settle(f.args());
 const a=f.args(f.tag,'get',{kind:'collect'});assert.equal((await f.P.reserve(a)).allowed,true);await f.settle(a,{outcome:'received'});const s=await f.P.getSummary(f.tag,OWNER);assert.equal(s.submissions,1);assert.equal(s.polls,1);assert.equal(s.estimated_budget_charge_microrub,30500);
});
test('definitive no-fetch refund is exactly once and does not reuse attempt identity',async()=>{
 const f=setup();await f.bind();await f.P.reserve(f.args());const s={request_executed:false,http_status:null,outcome:'not_sent'};await f.settle(f.args(),s);assert.equal((await f.settle(f.args(),s)).duplicate,true);
 const p=await f.P.getSummary(f.tag,OWNER);assert.equal(p.submissions,0);assert.equal(p.estimated_budget_charge_microrub,0);f.state.now+=201;assert.equal((await f.P.reserve(f.args())).reason,'DUPLICATE_POLICY_ATTEMPT');
});
for(const http_status of [401,403,500])test(`definitive HTTP ${http_status} credited once, request count retained`,async()=>{
 const f=setup();await f.bind();await f.P.reserve(f.args());await f.settle(f.args(),{http_status,outcome:'rejected'});const p=await f.P.getSummary(f.tag,OWNER);assert.equal(p.submissions,1);assert.equal(p.estimated_budget_charge_microrub,0);
});
test('UNKNOWN is not refunded; next POST blocked but known GET remains possible',async()=>{
 const f=setup();await f.bind();await f.P.reserve(f.args());await f.settle(f.args(),{request_executed:'UNKNOWN',http_status:null,outcome:'unknown'});f.state.now+=201;
 const p=await f.P.getSummary(f.tag,OWNER);assert.equal(p.estimated_budget_charge_microrub,30500);assert.equal(p.holds,1);assert.equal((await f.P.reserve(f.args(f.tag,'again'))).reason,'POLICY_RECONCILIATION_REQUIRED');assert.equal((await f.P.reserve(f.args(f.tag,'get',{kind:'collect'}))).allowed,true);
});
test('settlement conflict cannot refund a previously accepted attempt',async()=>{
 const f=setup();await f.bind();await f.P.reserve(f.args());await f.settle(f.args());await rejected(()=>f.settle(f.args(),{request_executed:false,outcome:'not_sent'}),'ASYNC_POLICY_SETTLEMENT_CONFLICT');assert.equal((await f.P.getSummary(f.tag,OWNER)).estimated_budget_charge_microrub,30500);
});
test('local persistence failure holds further submission',async()=>{
 const f=setup();await f.bind();await f.P.reserve(f.args());await f.settle(f.args(),{local_saved:false});f.state.now+=201;assert.equal((await f.P.reserve(f.args(f.tag,'again'))).reason,'POLICY_RECONCILIATION_REQUIRED');
});
test('own active reservation cannot be recovered; new worker conservatively restores',async()=>{
 const f=setup();await f.bind();await f.P.reserve(f.args());assert.equal((await f.P.recover({jobId:f.tag,owner:OWNER,workerId:'worker-A'})).allowed,false);
 const newP=Factory.create({...f.options,workerId:'worker-B'});const r=await newP.recover({jobId:f.tag,owner:OWNER,workerId:'worker-B'});assert.equal(r.allowed,true);assert.equal(r.submit_blocked,true);assert.equal(r.progress.pending,0);assert.equal(r.progress.estimated_budget_charge_microrub,30500);
 const again=await newP.recover({jobId:f.tag,owner:OWNER,workerId:'worker-B'});assert.equal(again.progress.holds,1);
});
test('recovery from wrong owner or wrong worker rejected',async()=>{
 const f=setup();await f.bind();await rejected(()=>f.P.recover({jobId:f.tag,owner:'bad',workerId:'worker-A'}),'ASYNC_POLICY_WRONG_OWNER');await rejected(()=>f.P.recover({jobId:f.tag,owner:OWNER,workerId:'wrong'}),'ASYNC_POLICY_WORKER_MISMATCH');
});
test('legacy run id and totals consulted, not reset to an empty budget',async()=>{
 const f=setup();f.state.run={run_id:'r1',active_service:'search',requests_executed:1,estimated_cost_rub:.488};f.state.policy.max_requests_per_run=1;await f.bind(f.tag,{runId:'r1'});assert.equal((await f.P.reserve(f.args())).reason,'REQUEST_LIMIT');
 f.state.policy.max_requests_per_run=10;f.state.policy.max_cost_rub_per_run=.5;assert.equal((await f.P.reserve(f.args())).reason,'COST_LIMIT');f.state.run.run_id='r2';await rejected(()=>f.P.reserve(f.args()),'ASYNC_POLICY_RUN_CHANGED');
});
test('transaction abort does not leave partial reservation/counters or a consumed token',async()=>{
 const f=setup();await f.bind();const original=fake.IDBObjectStore.prototype.add;let reached=false;
 fake.IDBObjectStore.prototype.add=function(v){const r=original.call(this,v);if(this.name==='attempts'&&v.job_id===f.tag){reached=true;this.transaction.abort();}return r;};
 try{await rejected(()=>f.P.reserve(f.args()));}finally{fake.IDBObjectStore.prototype.add=original;}
 assert.equal(reached,true);const p=await f.P.getSummary(f.tag,OWNER);assert.equal(p.pending,0);assert.equal(p.submissions,0);assert.equal((await f.P.reserve(f.args())).allowed,true);
});
test('failed settlement transaction preserves reservation for explicit recovery',async()=>{
 const f=setup();await f.bind();await f.P.reserve(f.args());const original=fake.IDBObjectStore.prototype.put;let reached=false;
 fake.IDBObjectStore.prototype.put=function(v){const r=original.call(this,v);if(this.name==='attempts'&&v.job_id===f.tag){reached=true;this.transaction.abort();}return r;};
 try{await rejected(()=>f.settle(f.args()));}finally{fake.IDBObjectStore.prototype.put=original;}
 assert.equal(reached,true);assert.equal((await f.P.getSummary(f.tag,OWNER)).pending,1);assert.equal((await f.P.reserve(f.args(f.tag,'again'))).reason,'POLICY_ATTEMPT_PENDING');
});
test('no-record denied reservation can settle only a definite non-send',async()=>{
 const f=setup();await f.bind();assert.equal((await f.settle(f.args(),{request_executed:false})).not_reserved,true);await rejected(()=>f.settle(f.args()),'ASYNC_POLICY_RESERVATION_MISSING');
});
test('same token cannot switch the protected index or kind',async()=>{
 const f=setup();await f.bind();await f.P.reserve(f.args());await rejected(()=>f.P.reserve(f.args(f.tag,'a',{index:1})),'ASYNC_POLICY_ATTEMPT_COLLISION');await rejected(()=>f.settle(f.args(f.tag,'a',{kind:'collect'})),'ASYNC_POLICY_ATTEMPT_COLLISION');
});
test('record contents contain no credential keys/raw body and no full-store reads in normal path',async()=>{
 const f=setup();await f.bind();const original=fake.IDBObjectStore.prototype.getAll,add=fake.IDBObjectStore.prototype.add,put=fake.IDBObjectStore.prototype.put;const captures=[];
 fake.IDBObjectStore.prototype.getAll=function(){throw new Error('full store read');};
 for(const [k,old]of [['add',add],['put',put]])fake.IDBObjectStore.prototype[k]=function(v){captures.push(JSON.stringify(v));return old.call(this,v);};
 try{await f.P.reserve(f.args());await f.settle(f.args());}finally{fake.IDBObjectStore.prototype.getAll=original;fake.IDBObjectStore.prototype.add=add;fake.IDBObjectStore.prototype.put=put;}
 for(const record of captures){assert.equal(record.includes('SYNTHETIC-NOT-A-REAL-KEY'),false);assert.equal(record.includes('WORDSTAT-UNCHANGED'),false);assert.ok(record.length<4096);}
});
for(const n of [10,100,500,1500])test(`per-record policy accounting ${n}; NOT a browser scale proof`,async()=>{
 const f=setup();await f.bind();let writes=0,maxBytes=0;const put=fake.IDBObjectStore.prototype.put,add=fake.IDBObjectStore.prototype.add;
 for(const[k,old]of [['add',add],['put',put]])fake.IDBObjectStore.prototype[k]=function(v){writes++;maxBytes=Math.max(maxBytes,Buffer.byteLength(JSON.stringify(v)));return old.call(this,v);};
 try{for(let i=0;i<n;i++){const a=f.args(f.tag,'scale-'+i,{index:i});assert.equal((await f.P.reserve(a)).allowed,true);await f.settle(a);f.state.now+=201;}}finally{fake.IDBObjectStore.prototype.put=put;fake.IDBObjectStore.prototype.add=add;}
 const p=await f.P.getSummary(f.tag,OWNER);assert.equal(p.submissions,n);assert.equal(p.estimated_budget_charge_microrub,n*30500);assert.equal(p.pending,0);assert.equal(writes,5*n);assert.ok(maxBytes<4096);console.log(JSON.stringify({scale_items:n,writes,max_record_bytes:maxBytes,venue:'deterministic IDB test double; not Chrome'}));
});
test('settlement accepts only bounded control metadata, never raw payload objects',async()=>{
 const f=setup();await f.bind();await f.P.reserve(f.args());
 for(const bad of [{outcome:{raw:'x'.repeat(10000)}},{outcome:'x'.repeat(10000)},{operation_id:'x'.repeat(10000)},{http_status:10000}])await rejected(()=>f.settle(f.args(),bad),'ASYNC_POLICY_SETTLEMENT_INVALID');
 assert.equal((await f.P.getSummary(f.tag,OWNER)).pending,1);
});
test('a scope cannot silently combine two different legacy runs',async()=>{
 const f=setup();await f.bind(f.tag,{runId:'r1'});await rejected(()=>f.bind(f.tag+'-second',{runId:'r2'}),'ASYNC_POLICY_SCOPE_RUN_MISMATCH');
});
test('interrupted GET does not lock unrelated new submissions as an unknown POST',async()=>{
 const f=setup();await f.bind();const a=f.args(f.tag,'get',{kind:'collect'});await f.P.reserve(a);await f.settle(a,{request_executed:'UNKNOWN',http_status:null,outcome:'read_error'});f.state.now+=201;
 const r=await f.P.reserve(f.args(f.tag,'submit-after-read'));assert.equal(r.allowed,true);
});
test('recovering a stale GET keeps no unknown-paid-request hold',async()=>{
 const f=setup();await f.bind();await f.P.reserve(f.args(f.tag,'get',{kind:'collect'}));
 const p=Factory.create({...f.options,workerId:'worker-B'});const r=await p.recover({jobId:f.tag,owner:OWNER,workerId:'worker-B'});assert.equal(r.submit_blocked,false);assert.equal(r.progress.holds,0);assert.equal(r.progress.estimated_budget_charge_microrub,0);
});
