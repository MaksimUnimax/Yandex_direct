import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import * as fake from './idb_test_double.mjs';
const ctx=vm.createContext({...fake,TextEncoder,console});ctx.globalThis=ctx;
vm.runInContext(fs.readFileSync(new URL('../candidate/shared/search_async_store.js',import.meta.url),'utf8'),ctx);
const S=ctx.YMBSearchAsyncStore;
const owner='https://chatgpt.com|11111111-1111-4111-8111-111111111111';
let seq=0;
async function setup(n=2){const jobId='b3-'+(++seq);await S.createJob({jobId,owner,queries:Array.from({length:n},(_,i)=>'query '+i),parameters:{region:'225'},folderId:'folder',maxRequests:n,maxCostMicrorub:n*100,unitCostMicrorub:100,now:1000});return jobId;}
const claim=(jobId,extra={})=>S.claim({jobId,owner,workerId:'w1',attemptId:'a1',kind:'submit',now:1000,...extra});
const finish=(jobId,extra={})=>S.finishSubmit({jobId,owner,index:0,attemptId:'a1',operationId:'op-'+jobId,outcome:'accepted',nextPollAt:301000,now:1000,...extra});
const raw=JSON.stringify({id:'op',done:true,response:{rawData:'eA=='}});

test('B3: immediate submit result persisted atomically, no collect needed',async()=>{
 const j=await setup();await claim(j);await finish(j,{outcome:'received',rawText:raw});
 const p=await S.getSummary(j,owner);assert.equal(p.counts.RESULT_SAVED,1);assert.equal(p.polls_started,0);assert.equal(p.operations_accepted,1);
 assert.equal((await S.readResult(j,owner,0)).raw_text,raw);
});
test('B3: early provider error on submit retains operation and evidence',async()=>{
 const j=await setup();await claim(j);await finish(j,{outcome:'provider_error',rawText:raw,errorCode:'PROVIDER_13'});
 const p=await S.getSummary(j,owner);assert.equal(p.counts.FAILED,1);assert.equal(p.operations_accepted,1);
 assert.equal((await S.readResult(j,owner,0)).operation_id,'op-'+j);assert.equal(p.polls_started,0);
});
test('B3: known-unsent attempt returns item without charging, never reused',async()=>{
 const j=await setup();await claim(j);await finish(j,{outcome:'not_sent',errorCode:'ADMISSION_DENIED'});
 const p=await S.getSummary(j,owner);assert.equal(p.counts.PENDING,2);assert.equal(p.requests_started,0);assert.equal(p.reserved_microrub,0);
 assert.equal((await claim(j)).reason,'DUPLICATE_ATTEMPT');
 assert.equal((await claim(j,{attemptId:'a2'})).allowed,true);
});
test('B3: preview identity mismatch rejects claim without consuming next item',async()=>{
 const j=await setup();const r=await claim(j,{expectedIndex:1});assert.equal(r.allowed,false);assert.equal(r.reason,'CANDIDATE_CHANGED');
 assert.equal((await S.getSummary(j,owner)).requests_started,0);
});
test('B3: preview reads one item and context, no state writes',async()=>{
 const j=await setup();const before=await S.getSummary(j,owner);
 const p=await S.peekNext({jobId:j,owner,kind:'submit',now:1000});assert.equal(p.item.index,0);assert.equal(p.folder_id,'folder');
 assert.deepEqual(await S.getSummary(j,owner),before);
 await assert.rejects(()=>S.peekNext({jobId:j,owner:'wrong',kind:'submit',now:1000}),{code:'ASYNC_WRONG_OWNER'});
});
test('B3: normalization recovery reads exact single item without scanning',async()=>{
 const j=await setup();const item=await S.readItem(j,owner,1);assert.equal(item.index,1);assert.equal(item.query,'query 1');
 await assert.rejects(()=>S.readItem(j,'wrong',1),{code:'ASYNC_WRONG_OWNER'});
});
