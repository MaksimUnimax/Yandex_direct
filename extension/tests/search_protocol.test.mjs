import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../src');
const ctx=vm.createContext({console,TextEncoder,TextDecoder,URL,Buffer}); ctx.globalThis=ctx;
for (const f of ['shared/search_xml.js','shared/search_protocol.js']) vm.runInContext(fs.readFileSync(path.join(root,f),'utf8'),ctx,{filename:f});
const P=ctx.SearchProtocol;
test('SEARCH_API_V1 canonical defaults, fingerprint and exact request body',()=>{
  const c=P.parseCommand('SEARCH_API_V1\n{"method":"search","queryText":"оберег в машину"}');
  assert.equal(c.method,'search'); assert.equal(c.searchType,'SEARCH_TYPE_RU'); assert.equal(c.page,0); assert.equal(c.groupsOnPage,10); assert.equal(c.docsInGroup,1); assert.equal(c.maxPassages,4); assert.equal(c.l10n,'LOCALIZATION_RU');
  assert.equal(P.commandFingerprint(c),P.commandFingerprint({...c}));
  const r=P.buildRequest(c,'folder-1'); assert.equal(r.method,'POST'); assert.equal(r.url,'https://searchapi.api.cloud.yandex.net/v2/web/search'); assert.equal(r.body.folderId,'folder-1'); assert.equal(r.body.responseFormat,'FORMAT_XML'); assert.equal(r.body.query.queryText,'оберег в машину');
});
test('SEARCH_API_V1 rejects invalid bounds before any provider transport',()=>{
  const ok=(q)=>P.normalizeCommand({method:'search',queryText:q}); assert.equal(ok('x'.repeat(400)).queryText.length,400); assert.equal(ok(Array(40).fill('x').join(' ')).queryText.split(/\s+/).length,40);
  for (const bad of [{method:'search',queryText:''},{method:'search',queryText:'x'.repeat(401)},{method:'search',queryText:Array(41).fill('x').join(' ')},{method:'search',queryText:'x',page:-1},{method:'search',queryText:'x',groupsOnPage:101},{method:'search',queryText:'x',docsInGroup:4},{method:'search',queryText:'x',maxPassages:6},{method:'search',queryText:'x',searchType:'NOPE'}]) assert.throws(()=>P.normalizeCommand(bad));
});
