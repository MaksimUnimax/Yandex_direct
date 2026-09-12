// Exact full candidate contract checks. No installed Chrome/real IDB/provider calls.
import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import path from 'node:path';import vm from 'node:vm';import crypto from 'node:crypto';
import {loadWorker,KEY} from './b10_full_worker_harness.mjs';
const full=path.resolve(process.env.YMB_FULL||'');if(!process.env.YMB_FULL)throw new Error('YMB_FULL required');
const c=vm.createContext({console,TextDecoder,Uint8Array,URL,atob});c.globalThis=c;
for(const p of ['shared/search_protocol.js','shared/search_async_protocol.js','shared/search_xml.js','shared/search_async_normalizer.js'])vm.runInContext(fs.readFileSync(path.join(full,p),'utf8'),c,{filename:p});
const P=c.SearchAsyncProtocol, S=c.SearchProtocol;
const start=extra=>({action:'start',jobId:'contract-job',queries:['браслет'],maxRequests:1,maxCostRub:1,confirmBillable:true,...extra});
const fail=(fn,code)=>assert.throws(fn,e=>e.code===code);
const send=(h,raw)=>h.dispatch({type:'WS_EXECUTE_MANUAL_BLOCK',conversation_key:KEY,manual_request_token:crypto.randomUUID(),block_text:P.PREFIX+' '+JSON.stringify(raw)});
const finish=async h=>{const d=h.data.wsmb_outbox?.[KEY];if(d)await h.dispatch({type:'WS_MANUAL_DELIVERY_COMPLETE',conversation_key:KEY,delivery_id:d.delivery_id,delivery_confirmed:true,confirmation_basis:'microphone',composer_empty:true});};
const xml=n=>'<yandexsearch><response><found priority="all">'+n+'</found><results><grouping>'+Array.from({length:n},(_,i)=>'<group><doc><url>https://example.test/'+i+'</url><title>Row '+i+'</title></doc></group>').join('')+'</grouping></results></response></yandexsearch>';
const raw=n=>Buffer.from(xml(n)).toString('base64');

test('inherited Search validator already enforces 400 Unicode code points without splitting astral characters',()=>{
 for(const character of ['a','я','💎']){const q=character.repeat(400);assert.equal(P.normalizeCommand(start({queries:[q]})).queries[0],q);fail(()=>P.normalizeCommand(start({queries:[q+character]})),'FIELD_TOO_LONG');}
});
test('inherited 40 whitespace-token boundary applies both at start and request reconstruction',()=>{
 for(const sep of [' ','\t','\n','\u00a0','\u2003']){
  const q=Array(40).fill('x').join(sep);assert.equal(P.normalizeCommand(start({queries:[q]})).queries[0],q);assert.equal(P.buildSubmitRequest(q,{},'folder').body.query.queryText,q);
  const over=q+sep+'x';fail(()=>P.normalizeCommand(start({queries:[over]})),'QUERY_TOO_MANY_WORDS');fail(()=>P.buildSubmitRequest(over,{},'folder'),'QUERY_TOO_MANY_WORDS');
 }
});
test('valid grouping 100 by 3 is preserved, not falsely promised as 300 returned results',()=>{
 const p={groupMode:'GROUP_MODE_DEEP',groupsOnPage:100,docsInGroup:3,maxPassages:5};
 const actual=P.buildSubmitRequest('q',p,'folder'),previous=S.buildRequest({queryText:'q',...p},'folder');assert.equal(JSON.stringify(actual.body),JSON.stringify(previous.body));
 assert.equal(actual.body.groupSpec.groupsOnPage,'100');assert.equal(actual.body.groupSpec.docsInGroup,'3');assert.equal(actual.body.responseFormat,'FORMAT_XML');
});
test('group and passage limits reject invalid values before constructing a provider request',()=>{
 for(const p of [{groupsOnPage:0},{groupsOnPage:101},{docsInGroup:0},{docsInGroup:4},{maxPassages:0},{maxPassages:6},{page:-1}])fail(()=>P.buildSubmitRequest('q',p,'folder'),'INVALID_FIELD');
});
test('1500 queries are an explicit local job limit, no truncation or silent dedupe',()=>{
 const q=Array.from({length:1500},(_,i)=>'q'+i);const r=P.normalizeCommand(start({queries:q,maxRequests:1500}));assert.equal(r.queries.length,1500);assert.equal(r.queries[1499],'q1499');
 fail(()=>P.normalizeCommand(start({queries:[...q,'excess'],maxRequests:1501})),'ASYNC_JOB_SIZE_INVALID');fail(()=>P.normalizeCommand(start({queries:['q',' q '],maxRequests:2})),'ASYNC_DUPLICATE_QUERY');
});
test('submit/collect aliases are bounded; collectReady is not an implicit whole-job drain',()=>{
 for(const action of ['submit','collect']){const r=P.normalizeCommand({action,jobId:'j'});assert.equal(r.count,1);fail(()=>P.normalizeCommand({action,jobId:'j',count:2}),'ASYNC_INTEGER_INVALID');}
 for(const action of ['submitN','collectN','collectReady']){const r=P.normalizeCommand({action,jobId:'j'});assert.equal(r.count,25);assert.equal(r.action,action==='submitN'?'submitN':'collectN');fail(()=>P.normalizeCommand({action,jobId:'j',count:26}),'ASYNC_INTEGER_INVALID');}
});
test('local pages require bounded sizes and a revision when continuing export',()=>{
 assert.equal(P.normalizeCommand({action:'itemsPage',jobId:'j'}).limit,100);fail(()=>P.normalizeCommand({action:'itemsPage',jobId:'j',limit:101}),'ASYNC_INTEGER_INVALID');
 assert.equal(P.normalizeCommand({action:'exportPage',jobId:'j'}).limit,25);fail(()=>P.normalizeCommand({action:'exportPage',jobId:'j',limit:26}),'ASYNC_INTEGER_INVALID');fail(()=>P.normalizeCommand({action:'exportPage',jobId:'j',after:0}),'EXPORT_REVISION_REQUIRED');
 assert.equal(P.normalizeCommand({action:'exportPage',jobId:'j',after:0,revision:7}).revision,7);
});
test('local repair selects exactly one saved item, not injected data or an arbitrary URL',()=>{
 assert.equal(P.normalizeCommand({action:'normalizeSaved',jobId:'j',index:1499}).index,1499);
 fail(()=>P.normalizeCommand({action:'normalizeSaved',jobId:'j',index:1500}),'ASYNC_INTEGER_INVALID');
 for(const k of ['rawData','queryText','count','url','headers','api_key'])fail(()=>P.normalizeCommand({action:'normalizeSaved',jobId:'j',index:0,[k]:'injected'}),'ASYNC_FIELD_FORBIDDEN');
});
test('unsupported provider features are refused rather than silently advertised or routed',()=>{
 for(const field of ['responseFormat','metadata','period','userAgent','folderId','Authorization'])fail(()=>P.normalizeCommand(start({[field]:'unsupported'})),'ASYNC_FIELD_FORBIDDEN');
 for(const action of ['cancelOperation','drain','pollForever','getAll','searchAsync'])fail(()=>P.normalizeCommand({action,jobId:'j'}),'ASYNC_ACTION_INVALID');
});
test('only fixed documented POST and GET addresses can be built; cancelPending has no provider URL',()=>{
 assert.equal(P.buildSubmitRequest('q',{},'folder').url,'https://searchapi.api.cloud.yandex.net/v2/web/searchAsync');assert.equal(P.buildGetRequest('op').url,'https://operation.api.cloud.yandex.net/operations/op');
 for(const op of ['../cancel','op/cancel','https://other.test','op?x=1'])fail(()=>P.buildGetRequest(op),'ASYNC_OPERATION_ID_INVALID');
 assert.equal(P.normalizeCommand({action:'cancelPending',jobId:'j'}).action,'cancelPending');
});
test('Operation accepted or failed is never a completed search result solely because HTTP was 200',()=>{
 assert.equal(P.parseOperation({id:'op',done:false}).outcome,'waiting');assert.equal(P.parseOperation({id:'op',done:true,error:{code:13,message:'x'}}).outcome,'provider_error');
 fail(()=>P.parseOperation({id:'other',done:false},'op'),'ASYNC_OPERATION_ID_MISMATCH');fail(()=>P.parseOperation({id:'op',done:true}),'ASYNC_COMPLETED_RESPONSE_MISSING');
});
test('250 docs accepted by production-sized guard; 251 rejected rather than truncated',()=>{
 const n=c.YMBSearchAsyncNormalizer.create({xmlNormalizer:c.YMBSearchXml,maxRawBytes:8*1024*1024,maxResults:250});
 const result=n({rawData:raw(250)});assert.equal(result.results.length,250);assert.equal(result.results[249].url,'https://example.test/249');
 fail(()=>n({rawData:raw(251)}),'ASYNC_XML_DOC_STRUCTURE_INVALID');
});
test('all declared manifest paths exist; versions agree; no new operation host or alarms activated',()=>{
 const m=JSON.parse(fs.readFileSync(path.join(full,'manifest.json'),'utf8')),p=JSON.parse(fs.readFileSync(path.join(full,'package.json'),'utf8'));
 assert.equal(m.version,p.version);assert.match(fs.readFileSync(path.join(full,'shared/product.js'),'utf8'),new RegExp('VERSION: "'+m.version.replaceAll('.','\\.')+'"'));
 assert.equal(m.host_permissions.includes('https://operation.api.cloud.yandex.net/*'),false);assert.equal((m.permissions||[]).includes('alarms'),false);assert.equal(m.host_permissions.includes('<all_urls>'),false);
 for(const name of [m.background.service_worker,m.action.default_popup,...m.content_scripts.flatMap(s=>s.js)])assert.ok(fs.existsSync(path.join(full,name)),name);
});
test('actual full initializer declares provider unavailable and performs no startup requests',async()=>{
 const h=await loadWorker(full);assert.equal(h.context.YMBSearchAsyncWorkerIntegration.ready,true);assert.equal(h.context.YMBSearchAsyncWorkerIntegration.providerEnabled,false);assert.equal(h.calls.fetch.length,0);
});
for(const action of ['submit','submitN','collect','collectN','collectReady'])test('actual permission boundary blocks '+action+' without provider initiation',async()=>{
 const h=await loadWorker(full);h.seedBoundChat();const r=await send(h,{action,jobId:'not-required-for-disabled-transport'});assert.match(r.report_text,/ASYNC_PROVIDER_PERMISSION_REQUIRED/);assert.equal(r.request_executed,false);assert.equal(h.calls.fetch.length,0);await finish(h);
});
test('invalid long query is rejected before any job is persisted or network is called',async()=>{
 const h=await loadWorker(full);h.seedBoundChat();const j='invalid-'+crypto.randomUUID();const r=await send(h,start({jobId:j,queries:['x'.repeat(401)]}));assert.match(r.report_text,/FIELD_TOO_LONG/);assert.equal(h.calls.fetch.length,0);await assert.rejects(()=>h.context.YMBSearchAsyncStore.getSummary(j,KEY),e=>e.code==='ASYNC_JOB_NOT_FOUND');await finish(h);
});
test('all local control/status/export actions execute with network capability disabled',async()=>{
 const h=await loadWorker(full);h.seedBoundChat();const j='local-'+crypto.randomUUID();
 for(const request of [start({jobId:j}),{action:'status',jobId:j},{action:'itemsPage',jobId:j},{action:'pause',jobId:j},{action:'resume',jobId:j},{action:'cancelPending',jobId:j},{action:'exportPage',jobId:j}]){
  const r=await send(h,request);assert.equal(r.accepted,true,JSON.stringify(r));assert.equal(r.request_executed,false);assert.ok(!r.report_text.includes('YMB_ERROR_V1'),r.report_text);assert.equal(h.calls.fetch.length,0);await finish(h);
 }
});
test('full worker uses 250-result bound and preserves raw on oversized provider response',async()=>{
 const h=await loadWorker(full);h.seedBoundChat();const s=h.context.YMBSearchAsyncStore;
 for(const n of [250,251]){
  const j='result-'+n+'-'+crypto.randomUUID();await s.createJob({jobId:j,owner:KEY,folderId:'folder',queries:['q'],parameters:{region:'225'},maxRequests:1,maxCostMicrorub:30500,unitCostMicrorub:30500,now:1});
  await s.claim({jobId:j,owner:KEY,workerId:'seed',attemptId:'s',kind:'submit',now:2});const rawText=JSON.stringify({id:j+'-op',done:true,response:{rawData:raw(n)}});
  await s.finishSubmit({jobId:j,owner:KEY,index:0,attemptId:'s',outcome:'received',operationId:j+'-op',rawText,now:3});
  const r=await send(h,{action:'normalizeSaved',jobId:j,index:0});assert.equal((await s.readResult(j,KEY,0)).raw_text,rawText);assert.equal(h.calls.fetch.length,0);
  assert.equal((await s.getSummary(j,KEY)).counts[n===250?'SUCCEEDED':'PARSE_FAILED'],1,r.report_text);await finish(h);
 }
});
test('readiness permission cannot be enabled from command JSON and deferred Autorun is not exposed',async()=>{
 const h=await loadWorker(full);h.seedBoundChat();for(const field of ['providerEnabled','host_permissions','autorun','autoPoll']){
  const r=await send(h,start({jobId:'inject-'+crypto.randomUUID(),[field]:true}));assert.match(r.report_text,/ASYNC_FIELD_FORBIDDEN/);assert.equal(h.calls.fetch.length,0);await finish(h);
 }
});
test('saved READMEs no longer claim Phase-1-only 0.1.0 and explicitly distinguish unaccepted candidate from release',()=>{
 for(const name of ['README.md','README.txt']){const s=fs.readFileSync(path.join(full,name),'utf8');assert.ok(s.includes('RELEASE_ALLOWED = NO'),name);assert.ok(s.includes('0.1.4'),name);assert.ok(s.includes('operation.api.cloud.yandex.net'),name);assert.ok(s.includes('normalizeSaved'),name);assert.ok(s.includes('exportPage'),name);assert.ok(!s.includes('Version: 0.1.0'),name);assert.ok(!s.includes('Future Search/Webmaster/Metrika/Direct adapters are NOT executable'),name);}
});
