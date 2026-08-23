import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../src');
const c={console,TextDecoder,Uint8Array,Buffer}; c.globalThis=c; vm.createContext(c);
for(const f of ['product.js','search_xml.js','search_protocol.js']) vm.runInContext(fs.readFileSync(path.join(root,'shared',f),'utf8'),c);
const P=c.SearchProtocol;
test('SEARCH_API_V1 defaults and request mapping',()=>{
  const cmd=P.parseCommand('SEARCH_API_V1\n{"queryText":"оберег в машину"}');
  assert.equal(cmd.method,'search'); assert.equal(cmd.searchType,'SEARCH_TYPE_RU'); assert.equal(cmd.region,'225'); assert.equal(cmd.page,0); assert.equal(cmd.groupsOnPage,10); assert.equal(cmd.docsInGroup,1); assert.equal(cmd.maxPassages,4); assert.equal(cmd.l10n,'LOCALIZATION_RU');
  const req=P.buildRequest(cmd,'folder');
  assert.equal(req.url,'https://searchapi.api.cloud.yandex.net/v2/web/search');
  assert.equal(req.body.folderId,'folder'); assert.equal(req.body.responseFormat,'FORMAT_XML'); assert.equal(req.body.query.queryText,'оберег в машину'); assert.equal(req.body.groupSpec.groupsOnPage,'10');
});
test('Search validation boundaries',()=>{
  assert.equal(P.normalizeCommand({queryText:'x'.repeat(400)}).queryText.length,400);
  assert.throws(()=>P.normalizeCommand({queryText:'x'.repeat(401)}),e=>e.code==='FIELD_TOO_LONG');
  assert.equal(P.normalizeCommand({queryText:Array(40).fill('x').join(' ')}).queryText.split(/\s+/).length,40);
  assert.throws(()=>P.normalizeCommand({queryText:Array(41).fill('x').join(' ')}),e=>e.code==='QUERY_TOO_MANY_WORDS');
  for(const [field,value] of [['groupsOnPage',101],['docsInGroup',4],['maxPassages',6],['page',-1]]) assert.throws(()=>P.normalizeCommand({queryText:'x',[field]:value}),e=>e.code==='INVALID_FIELD');
  assert.throws(()=>P.normalizeCommand({queryText:'x',unknown:1}),e=>e.code==='UNSUPPORTED_FIELD');
  assert.throws(()=>P.normalizeCommand({queryText:'x',searchType:'SEARCH_TYPE_COM',region:'225'}),e=>e.code==='REGION_NOT_SUPPORTED');
  assert.throws(()=>P.normalizeCommand({queryText:'x',searchType:'SEARCH_TYPE_TR',l10n:'LOCALIZATION_RU'}),e=>e.code==='LOCALIZATION_NOT_SUPPORTED');
});
test('all registered Search enum values are accepted in a compatible command',()=>{
  for(const searchType of P.SEARCH_TYPES) {
    const cmd=P.normalizeCommand({queryText:'x',searchType});
    assert.equal(cmd.searchType,searchType);
  }
  for(const familyMode of P.FAMILY_MODES) assert.equal(P.normalizeCommand({queryText:'x',familyMode}).familyMode,familyMode);
  for(const fixTypoMode of P.FIX_TYPO_MODES) assert.equal(P.normalizeCommand({queryText:'x',fixTypoMode}).fixTypoMode,fixTypoMode);
  for(const sortMode of P.SORT_MODES) assert.equal(P.normalizeCommand({queryText:'x',sortMode}).sortMode,sortMode);
  for(const sortOrder of P.SORT_ORDERS) assert.equal(P.normalizeCommand({queryText:'x',sortOrder}).sortOrder,sortOrder);
  for(const groupMode of P.GROUP_MODES) assert.equal(P.normalizeCommand({queryText:'x',groupMode}).groupMode,groupMode);
  const localizationCases=[
    ['SEARCH_TYPE_RU','LOCALIZATION_RU'],['SEARCH_TYPE_RU','LOCALIZATION_UK'],['SEARCH_TYPE_RU','LOCALIZATION_BE'],['SEARCH_TYPE_RU','LOCALIZATION_KK'],
    ['SEARCH_TYPE_TR','LOCALIZATION_TR'],['SEARCH_TYPE_COM','LOCALIZATION_EN']
  ];
  const seen=new Set();
  for(const [searchType,l10n] of localizationCases) {
    assert.equal(P.normalizeCommand({queryText:'x',searchType,l10n}).l10n,l10n);
    seen.add(l10n);
  }
  assert.deepEqual([...seen].sort(),[...P.LOCALIZATIONS].sort());
});
test('assistant Search command cannot carry operator credentials or folder id',()=>{
  for(const [field,value] of [['apiKey','secret'],['authorization','Api-Key secret'],['folderId','folder']]) {
    assert.throws(()=>P.normalizeCommand({queryText:'x',[field]:value}),e=>e.code==='UNSUPPORTED_FIELD');
  }
  const req=P.buildRequest(P.normalizeCommand({queryText:'x'}),'operator-folder');
  assert.equal(req.body.folderId,'operator-folder');
  assert.equal(Object.hasOwn(req.body,'apiKey'),false);
  assert.equal(Object.hasOwn(req.body,'authorization'),false);
});
test('future Search methods stay disabled in the synchronous first slice',()=>{
  for(const method of ['searchAsync','imageSearch','generativeSearch']) {
    assert.throws(()=>P.normalizeCommand({queryText:'x',method}),e=>e.code==='UNSUPPORTED_METHOD');
  }
});
test('Search result envelope truth fields',()=>{
  const cmd=P.normalizeCommand({queryText:'x'});
  const env=P.buildResultEnvelope({requestId:'r1',command:cmd,httpStatus:200,result:{results:[],result_count:0,response_format:'FORMAT_XML'},elapsedMs:3,metadata:{request_executed:true,automatic_retry:false}});
  assert.equal(env.service,'search'); assert.equal(env.status,'OK'); assert.equal(env.request_executed,true); assert.equal(env.automatic_retry,false); assert.match(P.formatResultEnvelope(env),/^SEARCH_RESULT_V1\n/);
});
