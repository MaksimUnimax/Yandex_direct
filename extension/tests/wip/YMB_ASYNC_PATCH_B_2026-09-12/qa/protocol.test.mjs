import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import vm from 'node:vm';import path from 'node:path';import {fileURLToPath} from 'node:url';import crypto from 'node:crypto';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const baseFile=process.env.YMB_SEARCH_PROTOCOL || (fs.existsSync(root+'/baseline/shared/search_protocol.js') ? root+'/baseline/shared/search_protocol.js' : path.resolve(root,'../../../src/shared/search_protocol.js'));
assert.equal(crypto.createHash('sha256').update(fs.readFileSync(baseFile)).digest('hex'),'48cb17f0a846f87e2057d65945dce23788e5c3c90810b7542557d762c2f301b7','exact owner-baseline SearchProtocol bytes');
const ctx=vm.createContext({console,URL,TextEncoder,TextDecoder});ctx.globalThis=ctx;
vm.runInContext(fs.readFileSync(baseFile,'utf8'),ctx);const old=ctx.SearchProtocol;
const syncBefore=JSON.stringify(old.buildRequest({queryText:'браслет',region:'213'},'test-folder'));
vm.runInContext(fs.readFileSync(root+'/candidate/shared/search_async_protocol.js','utf8'),ctx);
const P=ctx.SearchAsyncProtocol;
const start=extra=>({action:'start',jobId:'job-1',queries:['браслет','подвеска'],confirmBillable:true,maxRequests:2,maxCostRub:1,...extra});
const rejects=(fn,code)=>assert.throws(fn,e=>e.code===code);
test('separate protocol leaves ordinary Search and GenSearch untouched',()=>{
 assert.equal(ctx.SearchProtocol,old);assert.equal(JSON.stringify(old.buildRequest({queryText:'браслет',region:'213'},'test-folder')),syncBefore);
 assert.equal(old.METHODS.has('searchAsync'),false);
 assert.match(old.buildRequest({method:'genSearch',queryText:'test',confirmBillable:true},'test-folder').url,/\/v2\/gen\/search$/);
});
test('async request preserves all normalized existing search parameters',()=>{
 for(const params of [{region:'213',groupsOnPage:100,docsInGroup:3,groupMode:'GROUP_MODE_DEEP',page:4},{searchType:'SEARCH_TYPE_COM',l10n:'LOCALIZATION_EN'},{searchType:'SEARCH_TYPE_TR',region:'983'}]){
  const expected=old.buildRequest({method:'search',queryText:'test',...params},'test-folder');
  const actual=P.buildSubmitRequest('test',params,'test-folder');assert.equal(JSON.stringify(actual.body),JSON.stringify(expected.body));assert.equal(actual.url,P.SUBMIT_URL);assert.equal(actual.method,'POST');
 }
});
for(const field of ['url','headers','apiKey','folderId','method','service'])test(`start rejects injected field ${field}`,()=>rejects(()=>P.normalizeCommand(start({[field]:'injected'})),'ASYNC_FIELD_FORBIDDEN'));
test('billable consent and explicit limits required',()=>{
 rejects(()=>P.normalizeCommand(start({confirmBillable:false})),'ASYNC_CONFIRM_REQUIRED');
 rejects(()=>P.normalizeCommand(start({maxRequests:1})),'ASYNC_INTEGER_INVALID');
 for(const x of [0,-1,Infinity,NaN,'1'])rejects(()=>P.normalizeCommand(start({maxCostRub:x})),'ASYNC_COST_LIMIT_INVALID');
});
test('1500 is explicit new-protocol limit, no truncation',()=>{
 const queries=Array.from({length:1500},(_,i)=>'query '+i);const c=P.normalizeCommand(start({queries,maxRequests:1500}));assert.equal(c.queries.length,1500);assert.equal(c.queries[1499],'query 1499');
 rejects(()=>P.normalizeCommand(start({queries:[...queries,'extra'],maxRequests:1501})),'ASYNC_JOB_SIZE_INVALID');
});
test('duplicate normalized query is rejected rather than silently charging twice',()=>rejects(()=>P.normalizeCommand(start({queries:[' test ','test']})),'ASYNC_DUPLICATE_QUERY'));
test('empty invalid root/queries and oversized Unicode queries rejected by existing protocol',()=>{
 for(const value of [null,[],42,'bad'])rejects(()=>P.normalizeCommand(value),'ASYNC_OBJECT_REQUIRED');
 rejects(()=>P.normalizeCommand(start({queries:[]})),'ASYNC_JOB_SIZE_INVALID');
 assert.throws(()=>P.normalizeCommand(start({queries:['x'.repeat(401)],maxRequests:1})));
});
test('all six legacy search types retain localization constraints',()=>{
 for(const searchType of ['SEARCH_TYPE_RU','SEARCH_TYPE_TR','SEARCH_TYPE_COM','SEARCH_TYPE_KK','SEARCH_TYPE_BE','SEARCH_TYPE_UZ'])assert.equal(P.normalizeCommand(start({searchType})).parameters.searchType,searchType);
 assert.throws(()=>P.normalizeCommand(start({searchType:'SEARCH_TYPE_COM',region:'225'})));
});
test('marker parser rejects trailing extra envelopes instead of repairing',()=>{
 const text=P.PREFIX+'\n'+JSON.stringify(start());assert.equal(P.parseCommand(text).jobId,'job-1');rejects(()=>P.parseCommand(text+'\n{}'),'ASYNC_JSON_INVALID');rejects(()=>P.parseCommand('SEARCH_API_V1 {}'),'ASYNC_PREFIX_REQUIRED');
});
test('slice/page limits bounded; no implicit full-job action',()=>{
 for(const action of ['submit','collect']){assert.equal(P.normalizeCommand({action,jobId:'job-1'}).count,1);rejects(()=>P.normalizeCommand({action,jobId:'job-1',count:2}),'ASYNC_INTEGER_INVALID');}
 for(const action of ['submitN','collectN','collectReady']){assert.equal(P.normalizeCommand({action,jobId:'job-1'}).count,25);rejects(()=>P.normalizeCommand({action,jobId:'job-1',count:26}),'ASYNC_INTEGER_INVALID');}
 assert.equal(P.normalizeCommand({action:'itemsPage',jobId:'job-1'}).limit,100);rejects(()=>P.normalizeCommand({action:'itemsPage',jobId:'job-1',limit:101}),'ASYNC_INTEGER_INVALID');
});
test('status pause resume cancel cannot carry unexpected provider arguments',()=>{for(const action of ['status','pause','resume','cancelPending'])rejects(()=>P.normalizeCommand({action,jobId:'job-1',queryText:'inject'}),'ASYNC_FIELD_FORBIDDEN');});
test('operation GET fixed origin/path; arbitrary URLs forbidden',()=>{
 assert.equal(P.buildGetRequest('operation-123').url,'https://operation.api.cloud.yandex.net/operations/operation-123');
 for(const id of ['../secrets','https://evil.invalid/','a?b=1','a/b','a%2fb','a\nb',''])rejects(()=>P.buildGetRequest(id),'ASYNC_OPERATION_ID_INVALID');
});
test('Operation accepted is waiting, not a successful Search result',()=>{const p=P.parseOperation({id:'operation-1',done:false});assert.equal(p.outcome,'waiting');assert.equal(Object.hasOwn(p,'rawData'),false);});
test('Operation errors distinct from empty results including early provider errors',()=>{
 for(const done of [false,true]){const p=P.parseOperation({id:'op',done,error:{code:13,message:'failure'}});assert.equal(p.outcome,'provider_error');assert.equal(Object.hasOwn(p,'rawData'),false);}
});
test('Operation complete requires one valid response',()=>{
 rejects(()=>P.parseOperation({id:'op',done:true}),'ASYNC_COMPLETED_RESPONSE_MISSING');rejects(()=>P.parseOperation({id:'op',done:true,response:{}}),'ASYNC_RAW_DATA_MISSING');
 rejects(()=>P.parseOperation({id:'op',done:true,response:{rawData:'x'},error:{code:13}}),'ASYNC_OPERATION_AMBIGUOUS');
 rejects(()=>P.parseOperation({id:'op',done:false,response:{rawData:'x'}}),'ASYNC_PREMATURE_RESPONSE');
 rejects(()=>P.parseOperation({id:'op',done:'false'}),'ASYNC_DONE_INVALID');
});
test('mismatched operation fails; raw response remains unmodified',()=>{
 rejects(()=>P.parseOperation({id:'other',done:false},'expected'),'ASYNC_OPERATION_ID_MISMATCH');
 const p=P.parseOperation(JSON.stringify({id:'op',done:true,response:{rawData:'dGVzdA=='}}),'op');assert.equal(p.rawData,'dGVzdA==');assert.equal(p.outcome,'received');
});
test('transport builder cannot change method or add credential-bearing headers',()=>{
 for(const field of ['method','url','headers','api_key'])rejects(()=>P.buildSubmitRequest('test',{[field]:'bad'},'folder'),'ASYNC_FIELD_FORBIDDEN');
 const r=P.buildGetRequest('op');assert.equal(Object.hasOwn(r,'headers'),false);assert.equal(Object.hasOwn(r,'body'),false);
});
