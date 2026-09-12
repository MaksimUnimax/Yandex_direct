import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import crypto from 'node:crypto';
const base = fs.readFileSync(new URL('../baseline/shared/search_xml.js',import.meta.url),'utf8');
const context=vm.createContext({URL,TextDecoder,Uint8Array,atob});context.globalThis=context;
vm.runInContext(base,context);
vm.runInContext(fs.readFileSync(new URL('../candidate/shared/search_async_normalizer.js',import.meta.url),'utf8'),context);
const X=context.YMBSearchXml, Factory=context.YMBSearchAsyncNormalizer;
const norm=Factory.create({maxRawBytes:8*1024*1024});
const b64=x=>Buffer.from(x,'utf8').toString('base64');
const run=x=>norm({rawData:b64(x)});
const copy=x=>JSON.parse(JSON.stringify(x));
const wrapped=inner=>`<?xml version="1.0" encoding="utf-8"?><yandexsearch><request><query>тест</query></request><response>${inner}</response></yandexsearch>`;
const doc=`<doc><url>https://example.test/path?a=1&amp;b=2</url><domain>example.test</domain><title>Кольцо &quot;Песок&quot; 💍</title><passages><passage>Это <hlword>тест</hlword> &amp; текст</passage></passages><modtime>20260912T010203</modtime></doc>`;
const groups=(count=1)=>`<results><grouping><group>${doc.repeat(count)}</group></grouping></results>`;
function rejected(xml,code){assert.throws(()=>run(xml),e=>!code||e.code===code);}
test('baseline mapper exact-byte identity is recorded, global unchanged',()=>{
 assert.equal(context.YMBSearchXml,X);assert.equal(typeof X.normalizeBase64RawData,'function');
 assert.equal(crypto.createHash('sha256').update(base).digest('hex'),process.env.YMB_EXPECTED_XML_SHA||'790d14469db165795c84c34a6b6e8bf68a259e477d01fb648ff3101244cecffd');
});
test('new guard requires trusted local byte/complexity budgets',()=>{
 for(const maxRawBytes of [undefined,0,NaN,Infinity,-1,1e10,'1'])assert.throws(()=>Factory.create({maxRawBytes}));
 for(const extra of [{maxNodes:40001},{maxDepth:49},{maxResults:301}])assert.throws(()=>Factory.create({maxRawBytes:1024,...extra}));
});
test('normalizes Unicode/entity/rank/snippet/modtime exactly as ordinary Search',()=>{
 const xml=wrapped(groups(3));const got=run(xml);const original=X.normalizeXml(xml);
 assert.deepEqual(copy({results:got.results,result_count:got.result_count,response_format:got.response_format}),copy(original));
 assert.equal(got.results[0].url,'https://example.test/path?a=1&b=2');assert.equal(got.results[0].title,'Кольцо "Песок" 💍');assert.equal(got.results[0].modtime,'20260912T010203');
 assert.equal(got.validation.usable_for_url_comparison,true);assert.equal(got.validation.empty_proven,false);
});
for(const xml of ['<html/>','<response/>','',wrapped(''),wrapped('<found priority="all">7</found>'),wrapped('<found priority="all">0</found><found priority="strict">3</found>')])test(`does not invent empty success: ${xml.slice(0,80)}`,()=>rejected(xml));
test('documented XML code 15 is a proven empty result, not arbitrary provider error',()=>{
 const r=run(wrapped('<error code="15">Ничего не найдено</error>'));assert.equal(r.results.length,0);assert.equal(r.validation.empty_proven,true);assert.equal(r.validation.xml_error_code,15);assert.equal(r.validation.usable_for_url_comparison,false);
});
test('explicit zero found is an empty observation; optional other fields absent',()=>{
 const r=run(wrapped('<found priority="all">0</found>'));assert.equal(r.validation.empty_proven,true);
});
for(const code of ['1','2','18','42'])test(`XML provider error ${code} cannot become empty success`,()=>rejected(wrapped(`<error code="${code}">error</error>`),'ASYNC_XML_PROVIDER_ERROR'));
test('ambiguous docs plus error or zero count rejected without row loss',()=>{
 rejected(wrapped(groups()+'<error code="15">empty</error>'),'ASYNC_XML_AMBIGUOUS_RESULT');rejected(wrapped(groups()+'<found>0</found>'),'ASYNC_XML_AMBIGUOUS_RESULT');
});
test('300 document rows preserved, 301 explicitly rejected without truncation',()=>{
 assert.equal(run(wrapped(groups(300))).results.length,300);rejected(wrapped(groups(301)),'ASYNC_XML_DOC_STRUCTURE_INVALID');
});
test('missing URL remains a row with null URL and explicit non-usable marker',()=>{
 const r=run(wrapped('<results><grouping><group><doc><title>Test</title></doc></group></grouping></results>'));
 assert.equal(r.results.length,1);assert.equal(r.results[0].url,null);assert.deepEqual(copy(r.validation.missing_url_ranks),[1]);assert.equal(r.validation.usable_for_url_comparison,false);
});
for(const url of ['javascript:alert(1)','file:///etc/passwd','https://user:password@example.test/','not-url'])test(`URL is preserved but not usable: ${url}`,()=>{
 const r=run(wrapped(groups().replace(/<url>[^<]+<\/url>/,`<url>${url}</url>`)));assert.equal(r.results[0].url,url);assert.deepEqual(copy(r.validation.unsafe_url_ranks),[1]);
});
test('valid CDATA/comments preserve accepted sync mapping',()=>{
 const xml=wrapped(groups().replace('Кольцо &quot;Песок&quot; 💍','<![CDATA[Title <raw>]]><!--a comment-->'));const r=run(xml);assert.deepEqual(copy(r.results),copy(X.normalizeXml(xml).results));
});
for(const xml of [wrapped(groups()).slice(0,-1),'<yandexsearch><response></yandexsearch>',wrapped(groups())+'<extra/>',wrapped(groups())+'x','<yandexsearch><response></response><response></response></yandexsearch>',wrapped('<doc/>'),wrapped(groups().replace('</title>','</TITLE>'))])test(`malformed/truncated structure fails: ${xml.slice(-65)}`,()=>rejected(xml));
for(const entity of ['&bogus;','&unclosed','&#0;','&#xD800;','&#x110000;','&#xFFFF;','&amp','&;'])test(`invalid entity rejected: ${entity}`,()=>rejected(wrapped(groups().replace('Кольцо &quot;Песок&quot; 💍',entity))));
test('DTD and external entity expansion never reached',()=>{
 rejected('<!DOCTYPE yandexsearch [<!ENTITY x SYSTEM "https://evil.invalid/">]>'+wrapped(groups()),'ASYNC_XML_DTD_UNSUPPORTED');
});
for(const bad of ['<doc a="x" a="y">','<doc a=noquotes>','<doc xmlns="ns">','<x:doc>','<doc a="<bad">'])test(`unsupported/invalid attributes rejected: ${bad}`,()=>rejected(wrapped(groups().replace('<doc>',bad))));
test('depth and node budgets applied before recursive legacy normalization',()=>{
 rejected(wrapped('<results>'+('<x>'.repeat(60))+'</x>'.repeat(60)+'</results>'),'ASYNC_XML_COMPLEXITY_LIMIT');
 const tiny=Factory.create({maxRawBytes:65536,maxNodes:8});assert.throws(()=>tiny({rawData:b64(wrapped(groups()))}),e=>e.code==='ASYNC_XML_COMPLEXITY_LIMIT');
});
test('byte limit enforced before decoding, not after allocating whole payload',()=>{
 const low=Factory.create({maxRawBytes:10});assert.throws(()=>low({rawData:b64(' '.repeat(100))}),e=>e.code==='ASYNC_XML_BYTE_BUDGET');
});
for(const rawData of ['====','QQ=Q','Q Q=','QR==','QUL=','[object Object]',null,42])test(`invalid/noncanonical base64 rejected: ${rawData}`,()=>assert.throws(()=>norm({rawData}),e=>e.code==='ASYNC_BASE64_INVALID'));
test('invalid UTF8 is not silently replaced',()=>assert.throws(()=>norm({rawData:Buffer.from([0xC3,0x28]).toString('base64')}),e=>e.code==='ASYNC_XML_UTF8_INVALID'));
test('BOM before XML declaration allowed; XML 1.1 or another encoding unsupported',()=>{
 assert.equal(run('\uFEFF'+wrapped(groups())).result_count,1);rejected(wrapped(groups()).replace('1.0','1.1'));rejected(wrapped(groups()).replace('utf-8','windows-1251'));
});
test('literal invalid XML code point in comment also rejected',()=>rejected(wrapped(groups())+'<!--\u0000-->','ASYNC_XML_CHARACTER_INVALID'));
test('optional fields and unknown metadata do not require fabricating data',()=>{
 const r=run(wrapped('<future>provider extension</future><results><grouping><group><doc/></group></grouping></results>'));
 assert.equal(r.results.length,1);for(const k of ['url','domain','title','snippet','modtime'])assert.equal(r.results[0][k],null);
});
test('attribute > cannot slip through the legacy tokenizer',()=>{
 rejected(wrapped(groups().replace('<doc>','<doc note="a>b">')),'ASYNC_XML_ATTRIBUTE_UNSUPPORTED');
});
test('error 15 with positive found total is contradictory, not empty proof',()=>{
 rejected(wrapped('<found>9</found><error code="15">empty</error>'),'ASYNC_XML_AMBIGUOUS_RESULT');
});
