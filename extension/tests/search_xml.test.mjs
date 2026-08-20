import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../src');
const c={console,TextDecoder,Uint8Array,Buffer,atob:s=>Buffer.from(s,'base64').toString('binary')}; c.globalThis=c; vm.createContext(c); vm.runInContext(fs.readFileSync(path.join(root,'shared/search_xml.js'),'utf8'),c);
const X=c.YMBSearchXml;
test('Search XML normalization handles entities highlights passages and optional fields',()=>{
  const xml=`<?xml version="1.0"?><yandexsearch><response><results><grouping><group><doc><url>https://example.test/a?x=1&amp;y=2</url><domain>example.test</domain><title>Лучший <hlword>оберег</hlword></title><modtime>20260819T120000</modtime><passages><passage>Первый &amp; важный</passage><passage>Второй <hlword>фрагмент</hlword></passage></passages></doc><doc><url>https://example.test/b</url></doc></group></grouping></results></response></yandexsearch>`;
  const out=X.normalizeXml(xml); assert.equal(out.result_count,2); assert.equal(out.results[0].rank,1); assert.equal(out.results[0].url,'https://example.test/a?x=1&y=2'); assert.equal(out.results[0].title,'Лучший оберег'); assert.equal(out.results[0].snippet,'Первый & важный … Второй фрагмент'); assert.equal(out.results[1].title,null); assert.equal(out.results[1].snippet,null);
});
test('Base64 UTF-8 decode and malformed input fail closed',()=>{
  const xml='<response><doc><url>https://пример.рф/</url></doc></response>'; const b64=Buffer.from(xml,'utf8').toString('base64'); assert.equal(X.normalizeBase64RawData(b64).results[0].url,'https://пример.рф/');
  assert.throws(()=>X.decodeBase64Utf8('%%%'),e=>e.code==='INVALID_SEARCH_BASE64');
  assert.throws(()=>X.normalizeXml('<response><doc></response>'),e=>e.code==='INVALID_SEARCH_XML');
});
