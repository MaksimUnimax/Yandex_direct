import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import * as fake from './idb_test_double.mjs';
const base=new URL('../owner014/',import.meta.url);
const source=process.env.YMB_POLICY_TARGET||new URL('../candidate/shared/search_async_policy.js',import.meta.url);
const ctx=vm.createContext({...fake,console});ctx.globalThis=ctx;
for(const p of [new URL('shared/policy_model.js',base),new URL('shared/credential_registry.js',base),source])vm.runInContext(fs.readFileSync(p,'utf8'),ctx,{filename:String(p)});
const F=ctx.YMBSearchAsyncPolicy;let seq=0;
const eq=(a,b)=>assert.equal(JSON.stringify(a),JSON.stringify(b));
const rejected=(fn,c)=>assert.rejects(fn,e=>e.code===c);
function fixture(extra={}){
 const suffix=++seq,owner=`owner-${suffix}`,runId=`run-${suffix}`,folder=`folder-${suffix}`;
 const run={run_id:runId,active_service:'search',requests_executed:0,estimated_cost_rub:0,...extra.run};
 const settings={credentials:{search:{api_key:'SYNTHETIC_ONLY',folder_id:folder},wordstat:{api_key:'WS_SYNTHETIC',folder_id:'ws-folder'}}};
 const policy={manual_enabled:true,autorun_enabled:true,allowed_methods:['search','genSearch'],max_requests_per_run:100,max_cost_rub_per_run:100,...extra.policy};
 let now=1000,broken=false;const mirrors=[];
 const make=worker=>F.create({workerId:worker,getPolicy:async()=>policy,getSettings:async()=>settings,getAutoRun:async()=>run,now:()=>now,
   publishRunTotals:async m=>{if(broken)throw new Error('mirror write failed');mirrors.push(m);if((run.revision??-1)<=m.revision){Object.assign(run,{requests_executed:m.requests_executed,estimated_cost_rub:m.estimated_cost_rub,revision:m.revision});}}});
 const p=make('worker-A');
 const bind=(id,mode='deferred',opts={})=>p.bindJob({jobId:id,owner,folderId:folder,scopeId:'shared',runId,...opts,mode});
 const args=(id,kind='submit',attempt='a',index=0)=>({jobId:id,owner,folderId:folder,kind,attemptId:attempt,index});
 const done=(a,ext={})=>p.settle({...a,request_executed:true,http_status:200,outcome:'received',local_saved:true,...ext});
 return{p,owner,runId,folder,settings,policy,run,mirrors,make,bind,args,done,tick:()=>{now+=2000;},breakMirror:()=>{broken=true;},fixMirror:()=>{broken=false;},j:s=>`${s}-${suffix}`};
}
test('B4 baseline and protected policy model are unchanged',()=>{
 const p=ctx.YMBPolicyModel;const original=p.DEFAULT_SEARCH_METHOD_COST_RUB;
 assert.equal(original.search,.488);assert.equal(original.genSearch,5.08);
 for(const service of ['wordstat','webmaster','metrika','direct'])assert.ok(p.normalizePolicyForService(service,{}));
 assert.equal(ctx.YMBCredentialRegistry.capabilityForService('wordstat',{credentials:{wordstat:{api_key:'x',folder_id:'f'}}}).state,'PRESENT');
});
test('same transaction handles legacy search and deferred race: one admission',async()=>{
 const f=fixture();const a=f.j('legacy'),b=f.j('async');await f.bind(a,'legacy');await f.bind(b);
 const r=await Promise.all([f.p.reserve(f.args(a,'search')),f.p.reserve(f.args(b))]);
 assert.equal(r.filter(x=>x.allowed).length,1);assert.equal((await f.p.getSummary(a,f.owner)).submissions,1);
 await f.done(r[0].allowed?f.args(a,'search'):f.args(b));
});
test('canonical run scope cannot be bypassed by different aliases',async()=>{
 const f=fixture({policy:{max_requests_per_run:1}});const a=f.j('a'),b=f.j('b');await f.bind(a,'legacy',{scopeId:'alias-A'});await f.bind(b,'deferred',{scopeId:'alias-B'});
 assert.equal((await f.p.reserve(f.args(a,'search'))).allowed,true);await f.done(f.args(a,'search'));f.tick();
 assert.equal((await f.p.reserve(f.args(b))).reason,'REQUEST_LIMIT');
});
test('seeded previous charges counted once, then mirrored without double counting',async()=>{
 const f=fixture({run:{requests_executed:2,estimated_cost_rub:.976},policy:{max_requests_per_run:4,max_cost_rub_per_run:1.4945}});
 const a=f.j('a'),b=f.j('b');await f.bind(a,'legacy');await f.bind(b);
 assert.ok((await f.p.reserve(f.args(a,'search'))).allowed);await f.done(f.args(a,'search'));f.tick();
 assert.ok((await f.p.reserve(f.args(b))).allowed);await f.done(f.args(b));
 const s=await f.p.getSummary(a,f.owner);assert.equal(s.total_requests,4);assert.equal(s.total_cost_microrub,1494500);
 assert.equal(f.run.requests_executed,4);assert.equal(f.run.estimated_cost_rub,1.4945);
});
test('binding another job after mirror update does not re-seed the same scope',async()=>{
 const f=fixture();const a=f.j('a'),b=f.j('b');await f.bind(a);await f.p.reserve(f.args(a));await f.done(f.args(a));f.tick();await f.bind(b,'legacy');await f.p.reserve(f.args(b,'search'));await f.done(f.args(b,'search'));
 assert.equal((await f.p.getSummary(b,f.owner)).total_cost_microrub,518500);
});
test('mixed modes use their own estimates and common cost ceiling',async()=>{
 const f=fixture({policy:{max_cost_rub_per_run:5.5985}});const a=f.j('a'),b=f.j('b');await f.bind(a,'legacy');await f.bind(b);
 for(const [j,kind,token] of [[a,'search','s'],[a,'genSearch','g'],[b,'submit','d']]){assert.ok((await f.p.reserve(f.args(j,kind,token))).allowed);await f.done(f.args(j,kind,token));f.tick();}
 assert.equal((await f.p.getSummary(b,f.owner)).total_cost_microrub,5598500);assert.equal((await f.p.reserve(f.args(b,'submit','too-much'))).reason,'COST_LIMIT');
});
test('GET after exhausted paid budget is allowed and has no Search charge',async()=>{
 const f=fixture({policy:{max_cost_rub_per_run:.0305,max_requests_per_run:1}});const a=f.j('a');await f.bind(a);await f.p.reserve(f.args(a));await f.done(f.args(a));f.tick();
 const c=f.args(a,'collect','c');assert.ok((await f.p.reserve(c)).allowed);await f.done(c);const s=await f.p.getSummary(a,f.owner);assert.equal(s.total_requests,1);assert.equal(s.polls,1);assert.equal(s.total_cost_microrub,30500);
});
for(const kind of ['submit','search','genSearch'])test(`UNKNOWN ${kind} blocks all new paid modes but not GET`,async()=>{
 const f=fixture();const a=f.j('a'),b=f.j('b');await f.bind(a,kind==='submit'?'deferred':'legacy');await f.bind(b);const r=f.args(a,kind);await f.p.reserve(r);await f.done(r,{request_executed:'UNKNOWN',http_status:null,outcome:'unknown'});f.tick();
 assert.equal((await f.p.reserve(f.args(b))).reason,'POLICY_RECONCILIATION_REQUIRED');const c=f.args(b,'collect','get');assert.ok((await f.p.reserve(c)).allowed);await f.done(c);
});
for(const kind of ['search','genSearch','submit','collect'])test(`not-sent ${kind} refunds only the reservation once`,async()=>{
 const f=fixture();const a=f.j('a');await f.bind(a,['search','genSearch'].includes(kind)?'legacy':'deferred');const r=f.args(a,kind);await f.p.reserve(r);const end={request_executed:false,http_status:null,outcome:'not_sent'};await f.done(r,end);await f.done(r,end);
 const s=await f.p.getSummary(a,f.owner);assert.equal(s.total_requests,0);assert.equal(s.total_cost_microrub,0);assert.equal(s.pending,0);assert.equal(s.polls,0);assert.equal((await f.p.reserve(r)).reason,'DUPLICATE_POLICY_ATTEMPT');
});
for(const status of [401,403,500])test(`HTTP ${status} definite known-free credit is idempotent`,async()=>{
 const f=fixture();const a=f.j('a');await f.bind(a,'legacy');const r=f.args(a,'search');await f.p.reserve(r);const end={http_status:status,outcome:'rejected'};await f.done(r,end);await f.done(r,end);
 const s=await f.p.getSummary(a,f.owner);assert.equal(s.total_requests,1);assert.equal(s.total_cost_microrub,0);
});
test('legacy autorun channel cannot bypass disabled autorun',async()=>{
 const f=fixture({policy:{autorun_enabled:false}});const a=f.j('a');await f.bind(a,'legacy',{channel:'autorun'});assert.equal((await f.p.reserve(f.args(a,'search'))).reason,'AUTORUN_DISABLED');
});
test('deferred remains manual-only; unknown modes and channels rejected',async()=>{
 const f=fixture();await rejected(()=>f.bind(f.j('a'),'deferred',{channel:'autorun'}),'SHARED_DEFERRED_AUTORUN_NOT_SUPPORTED');await rejected(()=>f.bind(f.j('b'),'bad'),'SHARED_ADMISSION_BINDING_INVALID');await rejected(()=>f.bind(f.j('c'),'legacy',{channel:'admin'}),'SHARED_ADMISSION_BINDING_INVALID');
});
test('legacy cannot masquerade as cheap deferred and vice versa',async()=>{
 const f=fixture();const a=f.j('a'),b=f.j('b');await f.bind(a,'legacy');await f.bind(b);await rejected(()=>f.p.reserve(f.args(a)),'SHARED_ADMISSION_MODE_MISMATCH');await rejected(()=>f.p.reserve(f.args(b,'genSearch')),'SHARED_ADMISSION_MODE_MISMATCH');
});
test('method switch must obey original allowlist',async()=>{
 const f=fixture({policy:{allowed_methods:['search']}});const a=f.j('a');await f.bind(a,'legacy');assert.equal((await f.p.reserve(f.args(a,'genSearch'))).reason,'OPERATION_DISABLED');
});
test('wrong owner and changed folder deny before any reservation',async()=>{
 const f=fixture();const a=f.j('a');await f.bind(a,'legacy');await rejected(()=>f.p.reserve({...f.args(a,'search'),owner:'other'}),'ASYNC_POLICY_WRONG_OWNER');f.settings.credentials.search.folder_id='changed';await rejected(()=>f.p.reserve(f.args(a,'search')),'ASYNC_POLICY_CREDENTIAL_CONTEXT_CHANGED');assert.equal((await f.p.getSummary(a,f.owner)).submissions,0);
});
test('credential errors unchanged and secrets are not persisted',async()=>{
 const f=fixture();const a=f.j('a');await f.bind(a,'legacy');f.settings.credentials.search.check_state='NO_ACCESS';assert.equal((await f.p.reserve(f.args(a,'search'))).reason,'CREDENTIAL_NO_ACCESS');
 assert.ok(!JSON.stringify(await f.p.getSummary(a,f.owner)).includes('SYNTHETIC_ONLY'));
});
test('changing legacy run identity aborts before reserve',async()=>{
 const f=fixture();const a=f.j('a');await f.bind(a);f.run.run_id='changed';await rejected(()=>f.p.reserve(f.args(a)),'ASYNC_POLICY_RUN_CHANGED');
});
test('legacy run requires an explicit mirror implementation',async()=>{
 const f=fixture();const p=F.create({workerId:'w',getPolicy:async()=>f.policy,getSettings:async()=>f.settings,getAutoRun:async()=>f.run});await rejected(()=>p.bindJob({jobId:f.j('a'),owner:f.owner,folderId:f.folder,scopeId:'x',runId:f.runId}),'SHARED_RUN_MIRROR_REQUIRED');
});
test('mirror failure cannot become permission to fetch',async()=>{
 const f=fixture();const a=f.j('a');await f.bind(a);f.breakMirror();await assert.rejects(()=>f.p.reserve(f.args(a)));const s=await f.p.getSummary(a,f.owner);assert.equal(s.pending,1);f.fixMirror();await f.done(f.args(a),{request_executed:false,outcome:'not_sent',http_status:null});assert.equal((await f.p.getSummary(a,f.owner)).total_requests,0);
});
test('record transaction abort rolls back budget and rate alongside attempt',async()=>{
 const f=fixture();const a=f.j('a');await f.bind(a);const put=fake.IDBObjectStore.prototype.add;
 fake.IDBObjectStore.prototype.add=function(v,...x){const r=put.call(this,v,...x);if(this.name==='attempts'&&v.job_id===a)this.transaction.abort();return r;};
 try{await assert.rejects(()=>f.p.reserve(f.args(a)));}finally{fake.IDBObjectStore.prototype.add=put;}
 assert.equal((await f.p.getSummary(a,f.owner)).pending,0);assert.equal((await f.p.getSummary(a,f.owner)).total_requests,0);assert.ok((await f.p.reserve(f.args(a))).allowed);
});
test('recovery of legacy network uncertainty retains charge and blocks submit',async()=>{
 const f=fixture();const a=f.j('a'),b=f.j('b');await f.bind(a,'legacy');await f.bind(b);await f.p.reserve(f.args(a,'genSearch'));const p=f.make('worker-B');const r=await p.recover({jobId:a,owner:f.owner,workerId:'worker-B'});assert.ok(r.submit_blocked);assert.equal((await p.getSummary(a,f.owner)).total_cost_microrub,5080000);await rejected(()=>f.done(f.args(a,'genSearch')),'ASYNC_POLICY_SETTLEMENT_CONFLICT');
});
test('recovery of GET does not create a paid unknown hold',async()=>{
 const f=fixture();const a=f.j('a');await f.bind(a);await f.p.reserve(f.args(a,'collect'));const p=f.make('worker-B');const r=await p.recover({jobId:a,owner:f.owner,workerId:'worker-B'});assert.equal(r.submit_blocked,false);assert.equal((await p.getSummary(a,f.owner)).total_cost_microrub,0);
});
test('different budget scopes still share folder rate per API lane',async()=>{
 const f=fixture();const a=f.j('a'),b=f.j('b');await f.bind(a,'legacy',{runId:null,scopeId:'x'});await f.bind(b,'legacy',{runId:null,scopeId:'y'});
 await f.p.reserve(f.args(a,'genSearch'));await f.done(f.args(a,'genSearch'));assert.equal((await f.p.reserve(f.args(b,'genSearch'))).reason,'ASYNC_GLOBAL_RATE_WAIT');
 assert.ok((await f.p.reserve(f.args(b,'search','s'))).allowed);
});
test('legacy and deferred settled attempt collision cannot change kind/index',async()=>{
 const f=fixture();const a=f.j('a');await f.bind(a,'legacy');await f.p.reserve(f.args(a,'search'));await f.done(f.args(a,'search'));await rejected(()=>f.p.reserve(f.args(a,'genSearch')),'ASYNC_POLICY_ATTEMPT_COLLISION');await rejected(()=>f.done(f.args(a,'search','a',1)),'ASYNC_POLICY_ATTEMPT_COLLISION');
});
test('settlement error does not return false successful receipt',async()=>{
 const f=fixture();const a=f.j('a');await f.bind(a);await f.p.reserve(f.args(a));f.breakMirror();await assert.rejects(()=>f.done(f.args(a)));f.fixMirror();assert.ok((await f.done(f.args(a))).duplicate);assert.equal((await f.p.getSummary(a,f.owner)).total_requests,1);
});
test('per-attempt record sizes bounded on 10/100/500/1500, no getAll',async()=>{
 for(const n of [10,100,500,1500]){
  const f=fixture({policy:{max_requests_per_run:2000,max_cost_rub_per_run:2000}});const a=f.j('a'),b=f.j('b');await f.bind(a,'legacy',{runId:null});await f.bind(b,'deferred',{runId:null});let max=0,writes=0;
  const add=fake.IDBObjectStore.prototype.add,put=fake.IDBObjectStore.prototype.put,all=fake.IDBObjectStore.prototype.getAll;
  const count=(original,self,value,...args)=>{writes++;max=Math.max(max,Buffer.byteLength(JSON.stringify(value)));return original.call(self,value,...args);};
  fake.IDBObjectStore.prototype.add=function(...args){return count(add,this,...args);};fake.IDBObjectStore.prototype.put=function(...args){return count(put,this,...args);};fake.IDBObjectStore.prototype.getAll=()=>{throw new Error('getAll forbidden');};
  try{for(let i=0;i<n;i++){const j=i%2?a:b,kind=i%2?'search':'submit',c=f.args(j,kind,`r-${i}`);assert.ok((await f.p.reserve(c)).allowed);await f.done(c);f.tick();}assert.equal((await f.p.getSummary(a,f.owner)).total_requests,n);assert.ok(max<2048);assert.equal(writes,5*n);
    console.log('B5_STORAGE_AMPLIFICATION',JSON.stringify({n,writes,max_record_bytes:max,venue:'deterministic double; not browser memory'}));
  }finally{fake.IDBObjectStore.prototype.add=add;fake.IDBObjectStore.prototype.put=put;fake.IDBObjectStore.prototype.getAll=all;}
 }
});
test('settlement forbids malformed or credential-shaped public fields',async()=>{
 const f=fixture();const a=f.j('a');await f.bind(a);const c=f.args(a);await f.p.reserve(c);
 for(const extra of [{request_executed:'yes'},{http_status:900},{outcome:'API-KEY:SECRET'},{operation_id:'https://evil.invalid/'},{local_saved:null}])await rejected(()=>f.done(c,extra),'ASYNC_POLICY_SETTLEMENT_INVALID');
 assert.equal((await f.p.getSummary(a,f.owner)).pending,1);await f.done(c);
});
test('same binding may repeat but cannot switch owner folder run channel or mode',async()=>{
 const f=fixture();const a=f.j('a');await f.bind(a);assert.ok((await f.bind(a)).duplicate);
 for(const x of [{owner:'other'},{folderId:'other'},{runId:null},{mode:'legacy'}]){
  await assert.rejects(()=>f.p.bindJob({jobId:a,owner:f.owner,folderId:f.folder,scopeId:'shared',runId:f.runId,...x}));
 }
 assert.equal((await f.p.getSummary(a,f.owner)).submissions,0);
});
test('original policy, settings and all unrelated service records remain unchanged',async()=>{
 const f=fixture();const a=f.j('a'),before=JSON.stringify({policy:f.policy,settings:f.settings});await f.bind(a);await f.p.reserve(f.args(a));await f.done(f.args(a));assert.equal(JSON.stringify({policy:f.policy,settings:f.settings}),before);
});
test('failed local receipt creates common hold even after successful HTTP',async()=>{
 const f=fixture();const a=f.j('a'),b=f.j('b');await f.bind(a,'legacy');await f.bind(b);const c=f.args(a,'search');await f.p.reserve(c);await f.done(c,{local_saved:false});f.tick();assert.equal((await f.p.reserve(f.args(b))).reason,'POLICY_RECONCILIATION_REQUIRED');
});
test('independent unbound owners do not share budget or output',async()=>{
 const f=fixture(),g=fixture();const a=f.j('a'),b=g.j('a');await f.bind(a);await g.bind(b);await f.p.reserve(f.args(a));await f.done(f.args(a));assert.equal((await g.p.getSummary(b,g.owner)).total_requests,0);await rejected(()=>f.p.getSummary(a,g.owner),'ASYNC_POLICY_WRONG_OWNER');
});
test('same-worker recovery cannot refund a possibly active request',async()=>{
 const f=fixture();const a=f.j('a');await f.bind(a,'legacy');await f.p.reserve(f.args(a,'search'));const r=await f.p.recover({jobId:a,owner:f.owner,workerId:'worker-A'});assert.equal(r.allowed,false);assert.equal((await f.p.getSummary(a,f.owner)).pending,1);
});
test('settlement from an unreserved attempt cannot refund another attempt',async()=>{
 const f=fixture();const a=f.j('a');await f.bind(a);await f.p.reserve(f.args(a));const c=f.args(a,'submit','never');await rejected(()=>f.done(c),'ASYNC_POLICY_RESERVATION_MISSING');await f.done(c,{request_executed:false,outcome:'not_sent'});assert.equal((await f.p.getSummary(a,f.owner)).pending,1);assert.equal((await f.p.getSummary(a,f.owner)).total_cost_microrub,30500);
});
test('credential-check binding requires independent confirmation and no run',async()=>{
 const f=fixture();const input={jobId:f.j('check'),owner:f.owner,folderId:f.folder,scopeId:'check',mode:'credential_check',channel:'credential_check'};
 await rejected(()=>f.p.bindJob(input),'SHARED_CHECK_CONSENT_REQUIRED');await rejected(()=>f.p.bindJob({...input,credentialCheckConfirmed:true,runId:f.runId}),'SHARED_CHECK_CONSENT_REQUIRED');
 assert.ok((await f.p.bindJob({...input,credentialCheckConfirmed:true})).bound);await rejected(()=>f.p.reserve(f.args(input.jobId,'genSearch')),'SHARED_ADMISSION_MODE_MISMATCH');
});
test('old B4 record without migration proof is neither erased nor admitted',async()=>{
 const f=fixture(),a=f.j('legacy-v1');const db=await new Promise((resolve,reject)=>{const r=fake.indexedDB.open(F.DB_NAME,F.DB_VERSION);r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error);});
 const scope=JSON.stringify([f.owner,`run:${f.runId}`,f.folder]);
 await new Promise((resolve,reject)=>{const tx=db.transaction(['scopes'],'readwrite');tx.oncomplete=resolve;tx.onabort=()=>reject(tx.error);tx.objectStore('scopes').add({scope_id:scope,legacy_run_id:f.runId,submissions:1,pending:1,charge_microrub:30500});});
 await rejected(()=>f.bind(a),'SHARED_ADMISSION_MIGRATION_REQUIRED');
 const record=await new Promise(resolve=>{const r=db.transaction(['scopes'],'readonly').objectStore('scopes').get(scope);r.onsuccess=()=>resolve(r.result);});assert.equal(record.pending,1);assert.equal(record.charge_microrub,30500);
});
