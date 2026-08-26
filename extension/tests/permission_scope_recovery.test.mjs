import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../src');

test('manifest allows only ChatGPT pages plus official Yandex API hosts required by enabled services',()=>{
  const manifest=JSON.parse(fs.readFileSync(path.join(root,'manifest.json'),'utf8'));
  assert.deepEqual(manifest.host_permissions,[
    'https://chatgpt.com/*',
    'https://chat.openai.com/*',
    'https://searchapi.api.cloud.yandex.net/*',
    'https://api.webmaster.yandex.net/*'
  ]);
  assert.equal(manifest.host_permissions.some(x=>/https:\/\/(www\.)?yandex\.ru/i.test(x)),false);
  assert.deepEqual(manifest.content_scripts[0].matches,['https://chatgpt.com/*','https://chat.openai.com/*']);
  assert.equal(manifest.background.service_worker,'phase3_service_worker_bootstrap.js');
});

test('package npm test points to the real top-level Node test suite',()=>{
  const pkg=JSON.parse(fs.readFileSync(path.join(root,'package.json'),'utf8'));
  assert.equal(pkg.scripts?.test,'node --test ../tests/*.test.mjs');
  const testsDir=path.resolve(root,'../tests');
  assert.equal(fs.existsSync(testsDir),true);
  assert.ok(fs.readdirSync(testsDir).some(name=>name.endsWith('.test.mjs')));
});

test('service registry exposes Wordstat, synchronous Search, and Phase-3 Webmaster only',()=>{
  const ctx=vm.createContext({}); ctx.globalThis=ctx;
  vm.runInContext(fs.readFileSync(path.join(root,'shared/service_registry.js'),'utf8'),ctx);
  assert.deepEqual(Array.from(ctx.YMBServiceRegistry.DEFINITIONS, x=>x.service),['wordstat','search','webmaster']);
  for(const future of ['image','generative','async-search','search-async','metrika','direct']) assert.equal(ctx.YMBServiceRegistry.isKnownService(future),false);
});

test('Search protocol is locked to one synchronous search method and official endpoint',()=>{
  const ctx=vm.createContext({}); ctx.globalThis=ctx;
  vm.runInContext(fs.readFileSync(path.join(root,'shared/search_protocol.js'),'utf8'),ctx);
  assert.equal(ctx.SearchProtocol.ENDPOINT,'/v2/web/search');
  assert.equal(ctx.SearchProtocol.RESPONSE_FORMAT,'FORMAT_XML');
  assert.equal(ctx.SearchProtocol.normalizeCommand({method:'search',queryText:'test'}).method,'search');
  for(const method of ['searchAsync','imageSearch','generativeSearch']) {
    assert.throws(()=>ctx.SearchProtocol.normalizeCommand({method,queryText:'test'}));
  }
});
