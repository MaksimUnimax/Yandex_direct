import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import crypto from 'node:crypto';
import * as fake from './idb_test_double.mjs';
const root=new URL('../',import.meta.url);
const source=p=>fs.readFileSync(new URL(p,root),'utf8');
const base=source('baseline/shared/search_protocol.js');
assert.equal(crypto.createHash('sha256').update(base).digest('hex'),'48cb17f0a846f87e2057d65945dce23788e5c3c90810b7542557d762c2f301b7');
const ctx=vm.createContext({...fake,URL,TextEncoder,TextDecoder,Uint8Array,AbortController,setTimeout,clearTimeout,console});ctx.globalThis=ctx;
vm.runInContext(base,ctx);
for(const f of ['store','protocol','transport','runtime'])vm.runInContext(source(`candidate/shared/search_async_${f}.js`),ctx,{filename:`search_async_${f}.js`});
const S=ctx.YMBSearchAsyncStore,F=ctx.YMBSearchAsyncRuntime,P=ctx.SearchAsyncProtocol,T=ctx.YMBSearchAsyncTransport;
const owner='https://chatgpt.com|11111111-1111-4111-8111-111111111111';
const cred={api_key:'FAKE_TEST_KEY_NOT_REAL_123456',folder_id:'folder'};
const parsed={results:[{rank:1,url:'https://example.test/page',title:'example',domain:'example.test'}],result_count:1,response_format:'FORMAT_XML'};
const response=v=>new Response(JSON.stringify(v),{headers:{'Content-Type':'application/json'}});
let sequence=0;
async function fixture(n=3, overrides={}) {
 const jobId='rt-'+(++sequence),state={time:1000,fetches:0,events:[],policy:[],authorized:true,parseFail:false};
 await S.createJob({jobId,owner,queries:Array.from({length:n},(_,i)=>`query ${i}`),parameters:{region:'225'},folderId:'folder',maxRequests:n,maxCostMicrorub:n*100,unitCostMicrorub:100,now:1000});
 const fetchImpl=async(url,init)=>{state.fetches++;state.events.push('fetch');return overrides.fetchImpl?overrides.fetchImpl(url,init,state):response({id:jobId+'-op-'+state.fetches,done:false});};
 const policy={reserve:async c=>{state.policy.push({type:'reserve',...c});state.events.push('reserve');return overrides.reserve?overrides.reserve(c,state):{allowed:true};},settle:async c=>{state.policy.push({type:'settle',...c});state.events.push('settle');if(overrides.settle)return overrides.settle(c,state);},recover:async()=>({allowed:true})};
 const opts={store:S,protocol:P,transport:T.create({fetchImpl,maxResponseBytes:1024*1024,timeoutMs:overrides.timeoutMs||1000}),authorize:async()=>state.authorized,getCredential:async()=>overrides.credential||cred,policy,normalizeRaw:async({rawData})=>{state.events.push('parse');assert.ok(await S.readResult(jobId,owner,0),'must save raw before parser');if(state.parseFail)throw new Error('parse failed');assert.equal(rawData,'eA==');return parsed;},workerId:'worker1',now:()=>state.time,...overrides.runtime};
 const R=F.create(opts);
 const step=(kind='submit',attemptId='attempt1',extra={})=>R.step({jobId,owner,kind,attemptId,...extra});
 const stats=()=>S.getSummary(jobId,owner);
 const item=(i=0)=>S.readItem(jobId,owner,i);
 const raw=(i=0)=>S.readResult(jobId,owner,i);
 return {R,S,P,state,jobId,owner,opts,step,stats,item,raw};
}
async function acceptDirect(f,index=0,token='seed') {
 const c=await S.claim({jobId:f.jobId,owner,workerId:'worker1',kind:'submit',attemptId:token,now:1000});assert.equal(c.item.index,index);
 await S.finishSubmit({jobId:f.jobId,owner,index,attemptId:token,operationId:f.jobId+'-known-'+index,outcome:'accepted',nextPollAt:301000,now:1000});
}
async function counts(f) {
 const p=await f.stats();assert.equal(Object.values(p.counts).reduce((a,b)=>a+b,0),p.total);
 let seen=0,after=-1;for(;;){const page=await S.pageItems(f.jobId,owner,{after});seen+=page.rows.length;if(!page.rows.length)break;after=page.next_after;}assert.equal(seen,p.total);return p;
}
test('B3 runtime requires explicit authorization, policy and normalizer, creates no work',async()=>{
 const f=await fixture();assert.equal(f.state.fetches,0);assert.equal((await f.stats()).requests_started,0);
 for(const name of ['authorize','getCredential','policy','normalizeRaw','transport'])assert.throws(()=>F.create({...f.opts,[name]:null}));
});
test('B3 complete state reservation and policy precede exactly one POST',async()=>{
 const f=await fixture(2,{fetchImpl:async(_u,_i,st)=>{const p=await S.getSummary('rt-'+sequence,owner);assert.equal(p.counts.SUBMITTING,1);return response({id:'op-reserved',done:false});}});
 const r=await f.step();assert.equal(r.ok,true);assert.equal(r.outcome,'accepted');assert.equal(f.state.fetches,1);assert.deepEqual(f.state.events,['reserve','fetch','settle']);
 assert.equal((await f.stats()).counts.WAITING,1);assert.equal((await f.stats()).polls_started,0);
});
test('B3 immediate complete submit stores raw with operation, does not add GET',async()=>{
 const f=await fixture(1,{fetchImpl:async()=>response({id:'op-complete',done:true,response:{rawData:'eA=='}})});
 const r=await f.step();assert.equal(r.outcome,'received');assert.equal((await f.item()).state,'RESULT_SAVED');assert.equal((await f.raw()).operation_id,'op-complete');assert.equal(f.state.fetches,1);
 assert.equal((await f.stats()).polls_started,0);assert.ok(!JSON.stringify(r).includes('rawData'));assert.ok(!JSON.stringify(r).includes(cred.api_key));
 await f.R.normalizeSaved({jobId:f.jobId,owner,index:0});assert.equal((await counts(f)).all_successful,true);assert.equal(f.state.fetches,1);
});
test('B3 early error at submit is preserved, not empty-success',async()=>{
 const f=await fixture(1,{fetchImpl:async()=>response({id:'op-early-error',done:false,error:{code:13,message:'failed'}})});
 const r=await f.step();assert.equal(r.stop,true);assert.equal(r.outcome,'provider_error');assert.equal((await f.item()).state,'FAILED');assert.ok((await f.raw()).raw_text.includes('error'));
 assert.equal((await counts(f)).all_successful,false);assert.equal(f.state.fetches,1);
});
test('B3 authorization failure does not reserve or fetch',async()=>{
 const f=await fixture();f.state.authorized=false;await assert.rejects(()=>f.step(),{code:'ASYNC_RUNTIME_NOT_AUTHORIZED'});assert.equal(f.state.fetches,0);assert.equal((await f.stats()).requests_started,0);
});
test('B3 wrong owner fails before credentials/fetch',async()=>{
 const f=await fixture();await assert.rejects(()=>f.step('submit','a',{owner:'wrong'}),{code:'ASYNC_WRONG_OWNER'});assert.equal(f.state.fetches,0);assert.equal((await f.stats()).requests_started,0);
});
test('B3 credential context mismatch never claims or consumes budget',async()=>{
 const f=await fixture(1,{credential:{...cred,folder_id:'wrong'}});const r=await f.step();assert.equal(r.code,'ASYNC_CREDENTIAL_CONTEXT_CHANGED');assert.equal(f.state.fetches,0);assert.equal((await f.stats()).reserved_microrub,0);
});
test('B3 global admission denied rolls back proven-unsent reserve, retains dedupe',async()=>{
 const f=await fixture(2,{reserve:async()=>({allowed:false})});const r=await f.step();assert.equal(r.request_executed,false);assert.equal((await f.stats()).counts.PENDING,2);assert.equal((await f.stats()).reserved_microrub,0);
 assert.equal(f.state.fetches,0);assert.equal((await f.step()).code,'DUPLICATE_ATTEMPT');assert.equal(f.state.policy.filter(p=>p.type==='reserve').length,1);
});
test('B3 abort during external admission: no POST and no paid reserve',async()=>{
 const c=new AbortController();const f=await fixture(1,{reserve:async()=>{c.abort();return{allowed:true};}});const r=await f.step('submit','a',{signal:c.signal});assert.equal(r.request_executed,false);assert.equal((await f.stats()).reserved_microrub,0);assert.equal(f.state.fetches,0);
});
test('B3 a cancelled pending queue stays cancelled after an unsent reservation',async()=>{
 let f;f=await fixture(2,{reserve:async()=>{await f.R.control({jobId:f.jobId,owner,action:'cancelPending'});return{allowed:false};}});
 await f.step();const p=await counts(f);assert.equal(p.counts.CANCELLED,2);assert.equal(p.reserved_microrub,0);assert.equal(f.state.fetches,0);
});
test('B3 interruption after POST is UNKNOWN; a new command cannot replay',async()=>{
 const f=await fixture(2,{fetchImpl:async()=>{throw new Error('wire lost '+cred.api_key);}});const r=await f.step();assert.equal(r.outcome,'unknown');assert.equal(f.state.fetches,1);assert.equal((await f.item()).state,'UNKNOWN');
 const next=await f.step('submit','a2');assert.equal(next.code,'UNKNOWN_SUBMIT_REQUIRES_RECONCILIATION');assert.equal(f.state.fetches,1);assert.equal(JSON.stringify(r).includes(cred.api_key),false);assert.equal((await counts(f)).reserved_microrub,100);
});
test('B3 storage commit failure after accepted POST stops progression and survives recovery',async()=>{
 const f=await fixture(2);const bad=F.create({...f.opts,store:{...S,finishSubmit:async()=>{throw new Error('disk failure');}}});
 const r=await bad.step({jobId:f.jobId,owner,kind:'submit',attemptId:'failed-store'});assert.equal(r.code,'ASYNC_PERSISTENCE_FAILED');assert.equal((await f.item()).state,'SUBMITTING');assert.equal(f.state.fetches,1);
 const restart=F.create({...f.opts,workerId:'worker2'});await restart.recover({jobId:f.jobId,owner});assert.equal((await f.item()).state,'UNKNOWN');assert.equal(f.state.fetches,1);
 assert.equal((await restart.step({jobId:f.jobId,owner,kind:'submit',attemptId:'after-restart'})).code,'UNKNOWN_SUBMIT_REQUIRES_RECONCILIATION');
});
test('B3 raw read-result commit failure never becomes parsed success',async()=>{
 const f=await fixture(1,{fetchImpl:async()=>response({id:'op',done:true,response:{rawData:'eA=='}})});
 const original=fake.IDBObjectStore.prototype.put;
 fake.IDBObjectStore.prototype.put=function(value,...rest){const r=original.call(this,value,...rest);if(this.name==='results'&&value.job_id===f.jobId)this.transaction.abort();return r;};
 try {assert.equal((await f.step()).code,'ASYNC_PERSISTENCE_FAILED');} finally{fake.IDBObjectStore.prototype.put=original;}
 assert.equal((await f.item()).state,'SUBMITTING');assert.equal(await f.raw(),undefined);assert.equal(f.state.events.includes('parse'),false);
});
test('B3 policy settlement failure preserves known operation and pauses new work',async()=>{
 const f=await fixture(2,{settle:async()=>{throw new Error('policy disk');}});const r=await f.step();assert.equal(r.code,'ASYNC_POLICY_RECONCILIATION_REQUIRED');assert.equal((await f.stats()).control,'PAUSED');assert.equal((await f.item()).state,'WAITING');
 assert.equal((await f.step('submit','a2')).code,'PAUSED');assert.equal(f.state.fetches,1);
});
test('B3 GET waiting, failed read, then success use same saved ID',async()=>{
 const f=await fixture(1,{fetchImpl:async(url,_i,st)=>{assert.ok(url.endsWith(f.jobId+'-known-0'));if(st.fetches===2)throw new Error('read failure');return response({id:f.jobId+'-known-0',done:st.fetches===3,...(st.fetches===3?{response:{rawData:'eA=='}}:{})});}});
 await acceptDirect(f);assert.equal((await f.step('collect','too-soon')).code,'NO_DUE_OPERATIONS');assert.equal(f.state.fetches,0);
 f.state.time=301000;assert.equal((await f.step('collect','p1')).outcome,'waiting');f.state.time=602000;assert.equal((await f.step('collect','p2')).outcome,'read_error');assert.equal((await f.item()).state,'WAITING');
 f.state.time=903000;assert.equal((await f.step('collect','p3')).outcome,'received');assert.equal((await f.stats()).requests_started,1);assert.equal((await f.stats()).polls_started,3);assert.ok(await f.raw());
});
test('B3 unknown second submission does not discard earlier accepted result',async()=>{
 const f=await fixture(3,{fetchImpl:async()=>response({id:f.jobId+'-known-0',done:true,response:{rawData:'eA=='}})});await acceptDirect(f);
 await S.claim({jobId:f.jobId,owner,workerId:'old-worker',kind:'submit',attemptId:'unknown',now:1000});await f.R.recover({jobId:f.jobId,owner});
 f.state.time=301000;assert.equal((await f.step('collect','p')).outcome,'received');assert.equal((await f.stats()).counts.UNKNOWN,1);assert.equal(f.state.fetches,1);
});
test('B3 recovery of interrupted GET makes no network request and keeps ID',async()=>{
 const f=await fixture();await acceptDirect(f);await S.claim({jobId:f.jobId,owner,workerId:'old-worker',kind:'collect',attemptId:'interrupted',now:301000});f.state.time=302000;
 const r=await f.R.recover({jobId:f.jobId,owner});assert.equal(r.request_executed,false);assert.equal(f.state.fetches,0);assert.equal((await f.item()).state,'WAITING');assert.equal((await f.item()).operation_id,f.jobId+'-known-0');
});
test('B3 parse failure retains raw; retry is local and never calls wire',async()=>{
 const f=await fixture(1,{fetchImpl:async()=>response({id:'op-parse',done:true,response:{rawData:'eA=='}})});await f.step();const original=(await f.raw()).raw_text;f.state.parseFail=true;
 const fail=await f.R.normalizeSaved({jobId:f.jobId,owner,index:0});assert.equal(fail.raw_preserved,true);assert.equal((await f.item()).state,'PARSE_FAILED');assert.equal((await f.raw()).raw_text,original);
 f.state.parseFail=false;await f.R.normalizeSaved({jobId:f.jobId,owner,index:0});assert.equal((await counts(f)).all_successful,true);assert.equal(f.state.fetches,1);
});
test('B3 malformed saved response cannot become empty successful search',async()=>{
 const f=await fixture(1);const c=await S.claim({jobId:f.jobId,owner,workerId:'worker1',attemptId:'seed',kind:'submit',now:1000});
 await S.finishSubmit({jobId:f.jobId,owner,index:c.item.index,attemptId:'seed',outcome:'received',operationId:'expected',rawText:JSON.stringify({id:'other',done:true,response:{rawData:'eA=='}}),now:1000});
 const r=await f.R.normalizeSaved({jobId:f.jobId,owner,index:0});assert.equal(r.code,'ASYNC_NORMALIZATION_FAILED');assert.equal(f.state.fetches,0);assert.equal((await f.item()).state,'PARSE_FAILED');
});
test('B3 read failure is not relabelled as parse failure',async()=>{
 const f=await fixture(1,{fetchImpl:async()=>response({id:'op-readfail',done:true,response:{rawData:'eA=='}})});await f.step();
 const R=F.create({...f.opts,store:{...S,readResult:async()=>{throw new Error('disk unreadable');}}});await assert.rejects(()=>R.normalizeSaved({jobId:f.jobId,owner,index:0}));assert.equal((await f.item()).state,'RESULT_SAVED');
});
test('B3 a persisted successful result is never overwritten on repeated normalize',async()=>{
 const f=await fixture(1,{fetchImpl:async()=>response({id:'op-once',done:true,response:{rawData:'eA=='}})});await f.step();await f.R.normalizeSaved({jobId:f.jobId,owner,index:0});f.state.parseFail=true;
 assert.equal((await f.R.normalizeSaved({jobId:f.jobId,owner,index:0})).already_normalized,true);assert.equal((await f.item()).state,'SUCCEEDED');assert.equal(f.state.fetches,1);
});
test('B3 exact same attempt after successful submit cannot pay for next item',async()=>{
 const f=await fixture();await f.step();assert.equal((await f.step()).code,'DUPLICATE_ATTEMPT');assert.equal(f.state.fetches,1);assert.equal((await counts(f)).requests_started,1);
});
test('B3 duplicate parallel execution grants one network boundary',async()=>{
 const f=await fixture();const result=await Promise.all([f.step(),f.step()]);assert.equal(result.filter(r=>r.code==='ASYNC_RUNTIME_BUSY').length,1);assert.equal(f.state.fetches,1);
});
test('B3 two runtime instances with same worker cannot both claim the selected item',async()=>{
 const f=await fixture();const other=F.create(f.opts);const r=await Promise.all([f.step(),other.step({jobId:f.jobId,owner,kind:'submit',attemptId:'other'})]);
 assert.equal(f.state.fetches,1);assert.equal(r.filter(v=>v.ok===true).length,1);await counts(f);
});
test('B3 explicit slice count executes serially; replay stops at settled slot',async()=>{
 const f=await fixture(5);const args={jobId:f.jobId,owner,kind:'submit',commandId:'slice1',count:3};const r=await f.R.slice(args);assert.equal(r.processed,3);assert.equal(r.network_attempts,3);assert.equal(f.state.fetches,3);
 const second=await f.R.slice(args);assert.equal(second.network_attempts,0);assert.equal(second.last.code,'DUPLICATE_ATTEMPT');assert.equal(f.state.fetches,3);
});
test('B3 slice elapsed time bounds new work, never silently executes entire job',async()=>{
 const f=await fixture(10,{fetchImpl:async(_u,_i,st)=>{st.time+=10001;return response({id:'time-limited',done:false});}});const r=await f.R.slice({jobId:f.jobId,owner,kind:'submit',commandId:'bounded',count:10});assert.equal(r.processed,1);assert.equal(r.bounded_stop,true);assert.equal(f.state.fetches,1);
});
test('B3 slice stops immediately on unknown outcome',async()=>{
 const f=await fixture(10,{fetchImpl:async()=>{throw new Error('network');}});const r=await f.R.slice({jobId:f.jobId,owner,kind:'submit',commandId:'fail',count:10});assert.equal(r.processed,1);assert.equal(f.state.fetches,1);assert.equal((await f.stats()).counts.UNKNOWN,1);
});
test('B3 malformed slice count and identity rejected locally',async()=>{
 const f=await fixture();for(const count of [0,-1,26,1.5])await assert.rejects(()=>f.R.slice({jobId:f.jobId,owner,kind:'submit',commandId:'c',count}));assert.equal(f.state.fetches,0);await assert.rejects(()=>f.step('submit','../unsafe'));
});
test('B3 no full-store read or full-response return during 100 explicit item operations',async()=>{
 const f=await fixture(100);const original=fake.IDBObjectStore.prototype.getAll;fake.IDBObjectStore.prototype.getAll=function(){throw new Error('forbidden full store read');};
 try{for(let i=0;i<100;i++){const r=await f.step('submit','a-'+i);assert.equal(r.ok,true);assert.ok(JSON.stringify(r).length<2048);}}finally{fake.IDBObjectStore.prototype.getAll=original;}
 assert.equal(f.state.fetches,100);assert.equal((await counts(f)).counts.WAITING,100);
});
