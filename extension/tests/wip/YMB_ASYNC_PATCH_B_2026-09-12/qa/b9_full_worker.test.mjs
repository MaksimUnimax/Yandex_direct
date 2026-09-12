import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {loadWorker,KEY,CID} from './b9_full_worker_harness.mjs';
const full=process.env.YMB_FULL;
if(!full)throw new Error('YMB_FULL required');
const xml='<yandexsearch><response><found priority="all">1</found><results><grouping><group><doc><url>https://example.test/</url><domain>example.test</domain><title>Test 💎</title></doc></group></grouping></results></response></yandexsearch>';
const body=(url)=>url.includes('/v2/web/search')?{rawData:Buffer.from(xml).toString('base64')}:url.includes('/v2/gen/search')?{message:{content:'Answer',role:'ROLE_ASSISTANT'},sources:[]}:url.includes('wordstat')?{regions:[]}:url.includes('webmaster')?{hosts:[]}:url.includes('metrika')?{counters:[]}:{result:{Campaigns:[]}};
const network=async url=>new Response(JSON.stringify(body(String(url))),{headers:{'content-type':'application/json'}});
const asyncText=raw=>'SEARCH_ASYNC_BATCH_API_V1\n'+JSON.stringify(raw);
async function manual(h,text,token=crypto.randomUUID(),tab=7){return h.dispatch({type:'WS_EXECUTE_MANUAL_BLOCK',block_text:text,conversation_key:KEY,manual_request_token:token},{tab:{id:tab}});}
async function finish(h){const d=h.data.wsmb_outbox?.[KEY]?.delivery_id;if(d)return h.dispatch({type:'WS_MANUAL_DELIVERY_COMPLETE',conversation_key:KEY,delivery_id:d,delivery_confirmed:true,confirmation_basis:'microphone',composer_empty:true});}
async function newJob(h,count=2){const jobId='job-'+crypto.randomUUID();const r=await manual(h,asyncText({action:'start',jobId,queries:Array.from({length:count},(_,i)=>'тест '+i),confirmBillable:true,maxRequests:count,maxCostRub:10}));assert.equal(r.request_executed,false);assert.match(r.report_text,/SEARCH_ASYNC_BATCH_RESULT_V1/);await finish(h);return jobId;}
async function exportJob(h,jobId){return manual(h,asyncText({action:'exportPage',jobId}));}
async function readArtifact(h,d){let text='';const decoder=new TextDecoder();for(let i=0;i<d.chunk_count;i++){const c=await h.context.YMBFileArtifactStore.getChunk(d.artifact_key,i);assert.equal(crypto.createHash('sha256').update(c.bytes).digest('hex'),c.sha256);text+=decoder.decode(c.bytes,{stream:true});}return JSON.parse(text+decoder.decode());}

test('complete worker loads real baseline/admission/async/file modules with zero startup provider calls',async()=>{
 const h=await loadWorker(full);assert.equal(h.context.YMBSearchAdmissionBinding.ready,true);assert.equal(h.context.YMBSearchAsyncWorkerIntegration.ready,true);assert.ok(h.context.YMBFileDeliveryWorkerTransport);assert.ok(h.context.YMBSearchAsyncExport);assert.equal(h.calls.fetch.length,0);assert.equal(new Set(h.calls.imports).size,h.calls.imports.length);
});
test('file-aware outbox and exporter initialize before async worker captures dependencies',async()=>{
 const h=await loadWorker(full);const i=n=>h.calls.imports.indexOf(n);assert.ok(i('file_delivery_worker_transport.js')<i('search_async_worker_transport.js'));assert.ok(i('shared/search_async_export.js')<i('search_async_worker_transport.js'));assert.ok(i('search_batch_worker_transport.js')<i('search_async_worker_transport.js'));
});
test('manifest references all content files; operation host and alarms remain disabled',async()=>{
 const m=JSON.parse(fs.readFileSync(path.join(full,'manifest.json')));for(const group of m.content_scripts)for(const name of group.js)assert.ok(fs.statSync(path.join(full,name)).isFile());assert.ok(!m.permissions.includes('alarms'));assert.ok(!m.host_permissions.includes('https://operation.api.cloud.yandex.net/*'));
 const h=await loadWorker(full);assert.equal(h.context.YMBSearchAsyncWorkerIntegration.providerEnabled,false);
});
test('real Manual start -> binary export -> existing outbox succeeds in composed worker',async()=>{
 const h=await loadWorker(full);h.seedBoundChat();const job=await newJob(h);const r=await exportJob(h,job);assert.match(r.report_text,/"export_page"/,'export must not silently degrade to ASYNC_EXPORT_NOT_READY');const entry=h.data.wsmb_outbox[KEY];assert.equal(entry.delivery_mode,'attachment_v2');const d=entry.artifact_descriptors[0];assert.equal(d.delivery_id,r.delivery_id);const exported=await readArtifact(h,d);assert.equal(exported.items.length,2);assert.equal(exported.items[0].item.query,'тест 0');assert.equal(exported.items[0].result,null);assert.equal(h.calls.fetch.length,0);await finish(h);assert.equal(await h.context.YMBFileArtifactStore.getMeta(d.artifact_key),undefined);
});
test('actual per-item store raw+normalized evidence is exported without provider work or record loss',async()=>{
 const h=await loadWorker(full);h.seedBoundChat();const job=await newJob(h,1);const s=h.context.YMBSearchAsyncStore;const claim=await s.claim({jobId:job,owner:KEY,workerId:'seed',attemptId:'seed-1',kind:'submit',now:1});assert.equal(claim.allowed,true);const op='op-'+crypto.randomUUID();const raw=JSON.stringify({id:op,done:true,response:{rawData:Buffer.from(xml).toString('base64')}});
 await s.finishSubmit({jobId:job,owner:KEY,index:0,attemptId:'seed-1',outcome:'received',operationId:op,rawText:raw,now:2});const normalized=h.context.YMBSearchAsyncNormalizer.create({maxRawBytes:8*1024*1024})({rawData:Buffer.from(xml).toString('base64')});await s.finishNormalization({jobId:job,owner:KEY,index:0,normalized,now:3});
 const r=await exportJob(h,job);assert.match(r.report_text,/"export_page"/);const d=h.data.wsmb_outbox[KEY].artifact_descriptors[0];const f=await readArtifact(h,d);assert.equal(f.items[0].result.raw_text,raw);assert.equal(f.items[0].result.normalized.results[0].url,'https://example.test/');assert.equal(h.calls.fetch.length,0);await finish(h);assert.ok(await s.readResult(job,KEY,0));
});
for(const [label,setup,code]of [['Manual disabled',h=>h.data.wsmb_manual_modes[KEY]=false,'MANUAL_MODE_DISABLED'],['different service',h=>h.data.ymb_service_contexts[KEY].active_service='wordstat','SERVICE_NOT_ACTIVE'],['unbound conversation',h=>delete h.data.wsmb_conversation_bindings[KEY],'CONVERSATION_NOT_BOUND']])test('full worker rejects '+label+' before any provider or new job',async()=>{
 const h=await loadWorker(full);h.seedBoundChat();setup(h);const r=await manual(h,asyncText({action:'status',jobId:'job'}));assert.equal(r.code,code);assert.equal(h.calls.fetch.length,0);assert.equal(h.data.wsmb_outbox[KEY],undefined);
});
test('actual sender-tab mismatch is rejected before async job operation',async()=>{const h=await loadWorker(full);h.seedBoundChat();const r=await manual(h,asyncText({action:'status',jobId:'job'}),'t',8);assert.equal(r.code,'CONVERSATION_MISMATCH');assert.equal(h.calls.fetch.length,0);});
test('async submit remains disabled in the composed permission set',async()=>{const h=await loadWorker(full);h.seedBoundChat();const job=await newJob(h);const r=await manual(h,asyncText({action:'submitN',jobId:job,count:1}));assert.match(r.report_text,/ASYNC_PROVIDER_PERMISSION_REQUIRED/);assert.equal(h.calls.fetch.length,0);await finish(h);});
test('foreign-owner artifact chunk message fails before reading a stored part',async()=>{
 const h=await loadWorker(full);h.seedBoundChat();const job=await newJob(h);await exportJob(h,job);const entry=h.data.wsmb_outbox[KEY];assert.equal(entry.delivery_mode,'attachment_v2');const d=entry.artifact_descriptors[0];const r=await h.dispatch({type:'WS_GET_OUTBOX_ARTIFACT_CHUNK',conversation_key:KEY,delivery_id:entry.delivery_id,artifact_key:d.artifact_key,chunk_index:0},{tab:{id:8}});assert.equal(r.code,'AUTO_NON_OWNER_TAB');await finish(h);assert.equal(h.calls.fetch.length,0);
});
test('actual WS attachment messages keep one outbox, return only one chunk and clean up after acknowledgement',async()=>{
 const h=await loadWorker(full);h.seedBoundChat();const job=await newJob(h);await exportJob(h,job);const e=h.data.wsmb_outbox[KEY];assert.equal(e.delivery_mode,'attachment_v2');const d=e.artifact_descriptors[0];const common={conversation_key:KEY,delivery_id:e.delivery_id};
 const c=await h.dispatch({...common,type:'WS_GET_OUTBOX_ARTIFACT_CHUNK',artifact_key:d.artifact_key,chunk_index:0});assert.equal(c.ok,true);assert.ok(Buffer.from(c.chunk_base64,'base64').length<=256*1024);
 for(const [type,extra] of [['WS_MARK_ATTACHMENT_COMMITTED',{}],['WS_MARK_ATTACHMENT_READY',{attached_filenames:[d.filename]}],['WS_COMMIT_ATTACHMENT_SEND',{}]])assert.equal((await h.dispatch({...common,type,...extra})).ok,true);
 assert.equal(h.data.wsmb_outbox[KEY].phase,'committed');await finish(h);assert.equal(h.data.wsmb_manual_operations[KEY].status,'completed');assert.equal(await h.context.YMBFileArtifactStore.getMeta(d.artifact_key),undefined);assert.equal(h.calls.fetch.length,0);
});
for(const [service,marker,command] of [['search','SEARCH_API_V1',{method:'search',queryText:'тест'}],['search','SEARCH_API_V1',{method:'genSearch',queryText:'тест',confirmBillable:true}],['wordstat','WORDSTAT_API_V1',{method:'getRegionsTree'}],['webmaster','WEBMASTER_API_V1',{method:'listHosts'}],['metrika','METRIKA_API_V1',{method:'listCounters'}],['direct','DIRECT_API_V1',{method:'listCampaigns'}]])test(`old ${service}.${command.method} runs through full Manual dispatcher exactly once on controlled network`,async()=>{
 const h=await loadWorker(full,{network});h.seedBoundChat(service);const result=await manual(h,marker+' '+JSON.stringify(command));assert.equal(result.request_executed,true,result.report_text);assert.equal(h.calls.fetch.length,1);assert.match(result.report_text,/_RESULT_V1/);for(const secret of ['TEST_SEARCH_NOT_REAL','TEST_WORDSTAT_NOT_REAL','TEST_WM_NOT_REAL','TEST_METRIKA_NOT_REAL','TEST_DIRECT_NOT_REAL'])assert.ok(!result.report_text.includes(secret));await finish(h);
});
test('both message families have one responder after wrapper composition',async()=>{const h=await loadWorker(full);h.seedBoundChat();assert.equal((await h.dispatch({type:'YMB_GET_CREDENTIALS'})).ok,true);assert.equal((await h.dispatch({type:'WS_GET_GLOBAL_STATE'})).ok,true);assert.equal(h.calls.fetch.length,0);});
test('small legacy report stays text, large report uses existing A binary store after B wrapper installation',async()=>{
 const h=await loadWorker(full);h.seedBoundChat();await h.run(`putOutbox(${JSON.stringify(KEY)},{delivery_id:'small-'+crypto.randomUUID(),type:'manual',report_text:'small',phase:'claimed',tab_id:7})`);assert.equal(h.data.wsmb_outbox[KEY].delivery_mode,undefined);await h.run(`clearOutbox(${JSON.stringify(KEY)})`);
 await h.run(`putOutbox(${JSON.stringify(KEY)},{delivery_id:'large-'+crypto.randomUUID(),type:'manual',report_text:'x'.repeat(1100000),phase:'claimed',tab_id:7})`);const e=h.data.wsmb_outbox[KEY];assert.equal(e.delivery_mode,'attachment_v2');assert.ok(e.report_text.length<1000);assert.equal(e.artifact_descriptors[0].byte_length,1100000);await h.run(`clearOutbox(${JSON.stringify(KEY)})`);assert.equal(await h.context.YMBFileArtifactStore.getMeta(e.artifact_descriptors[0].artifact_key),undefined);assert.equal(h.calls.fetch.length,0);
});
