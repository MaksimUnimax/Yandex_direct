import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { webcrypto } from 'node:crypto';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');
const plain = (value) => JSON.parse(JSON.stringify(value));

function storageHarness(sharedState = {}) {
  return {
    state: sharedState,
    api: {
      async get(keys) {
        if (keys == null) return structuredClone(sharedState);
        if (typeof keys === 'string') return sharedState[keys] === undefined ? {} : { [keys]: structuredClone(sharedState[keys]) };
        if (Array.isArray(keys)) return Object.fromEntries(keys.filter((key) => sharedState[key] !== undefined).map((key) => [key, structuredClone(sharedState[key])]));
        const out = {};
        for (const [key, fallback] of Object.entries(keys || {})) out[key] = sharedState[key] === undefined ? structuredClone(fallback) : structuredClone(sharedState[key]);
        return out;
      },
      async set(values) { Object.assign(sharedState, structuredClone(values)); },
      async remove(keys) { for (const key of Array.isArray(keys) ? keys : [keys]) delete sharedState[key]; }
    }
  };
}

function contextFor(sharedState = {}) {
  const storage = storageHarness(sharedState);
  const ctx = {
    console, Date, JSON, Math, Object, Array, Set, Map, Promise, Error, String, Number, Boolean, RegExp,
    TextEncoder, Uint8Array, URL, URLSearchParams, crypto: webcrypto, structuredClone,
    globalThis: null,
    chrome: { storage: { local: storage.api } },
    YMBProduct: { VERSION: '0.1.3', BRIDGE_ID: 'yandex-marketing-bridge' }
  };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  for (const file of ['shared/webmaster_export_model.js', 'shared/webmaster_protocol.js']) {
    vm.runInContext(fs.readFileSync(path.resolve(src, file), 'utf8'), ctx, { filename: file });
  }
  return { ctx, storage };
}

test('W13-01 protocol exposes old four plus complete KW-001 Webmaster read surface', () => {
  const { ctx } = contextFor();
  const methods = plain(ctx.WebmasterProtocol.METHODS);
  for (const method of [
    'listHosts','getSummary','getDiagnostics','getPopularQueries',
    'getAllQueryHistory','getQueryHistory','getIndexingSamples','getInSearchSamples',
    'getExportRegions','getExportLimits','getExportDates',
    'projectQueryUrlExport','startQueryUrlExport','getQueryUrlExportStatus','collectQueryUrlExport',
    'getQueryUrlExportManifest','readQueryUrlExportChunk','listQueryUrlExportJobs'
  ]) assert.ok(methods.includes(method), method);
});

test('W13-02 accepted old Webmaster routes remain byte-for-byte equivalent in request semantics', () => {
  const { ctx } = contextFor();
  const P = ctx.WebmasterProtocol;
  assert.equal(P.buildRequest({ method: 'listHosts' }, '42').url, 'https://api.webmaster.yandex.net/v4/user/42/hosts');
  assert.equal(P.buildRequest({ method: 'getSummary', hostId: 'https:example.ru:443' }, '42').url, 'https://api.webmaster.yandex.net/v4/user/42/hosts/https%3Aexample.ru%3A443/summary');
  assert.equal(P.buildRequest({ method: 'getDiagnostics', hostId: 'h' }, '42').url, 'https://api.webmaster.yandex.net/v4/user/42/hosts/h/diagnostics');
  const popular = P.buildRequest({ method: 'getPopularQueries', hostId: 'h', orderBy: 'TOTAL_SHOWS' }, '42');
  assert.equal(popular.method, 'GET');
  assert.match(popular.url, /search-queries\/popular\?/);
  assert.match(popular.url, /order_by=TOTAL_SHOWS/);
  assert.match(popular.url, /device_type_indicator=ALL/);
});

test('W13-03 history routes repeat indicators and normalize all-query and query-specific shapes separately', () => {
  const { ctx } = contextFor();
  const P = ctx.WebmasterProtocol;
  const all = P.buildRequest({ method:'getAllQueryHistory', hostId:'h', queryIndicators:['TOTAL_SHOWS','TOTAL_CLICKS'], dateFrom:'2026-08-01', dateTo:'2026-08-31' }, '42');
  assert.match(all.url, /search-queries\/all\/history\?/);
  assert.match(all.url, /query_indicator=TOTAL_SHOWS&query_indicator=TOTAL_CLICKS/);
  const one = P.buildRequest({ method:'getQueryHistory', hostId:'h', queryId:'abc/def', queryIndicators:['AVG_SHOW_POSITION'] }, '42');
  assert.match(one.url, /search-queries\/abc%2Fdef\/history\?/);
  const normalizedAll = plain(P.normalizeProviderResult({ method:'getAllQueryHistory', hostId:'h' }, { indicators:{ TOTAL_SHOWS:[{date:'2026-08-01',value:12}] } }));
  assert.equal(normalizedAll.indicators.TOTAL_SHOWS[0].value, 12);
  const normalizedOne = plain(P.normalizeProviderResult({ method:'getQueryHistory', hostId:'h', queryId:'q' }, { queries:[{query_id:'q',query_text:'test',indicators:{TOTAL_CLICKS:[{date:'2026-08-01',value:3}]}}] }));
  assert.equal(normalizedOne.queries[0].query_text, 'test');
  assert.equal(normalizedOne.queries[0].indicators.TOTAL_CLICKS[0].value, 3);
});

test('W13-04 indexing and in-search sample routes are bounded to official 1..100 page size', () => {
  const { ctx } = contextFor();
  const P = ctx.WebmasterProtocol;
  const indexing = P.buildRequest({ method:'getIndexingSamples', hostId:'h', offset:10, limit:100 }, '42');
  assert.equal(indexing.url, 'https://api.webmaster.yandex.net/v4/user/42/hosts/h/indexing/samples?offset=10&limit=100');
  const inSearch = P.buildRequest({ method:'getInSearchSamples', hostId:'h', offset:20, limit:50 }, '42');
  assert.equal(inSearch.url, 'https://api.webmaster.yandex.net/v4/user/42/hosts/h/search-urls/in-search/samples?offset=20&limit=50');
  assert.throws(() => P.normalizeCommand({ method:'getIndexingSamples', hostId:'h', limit:101 }), /1 до 100/);
  const indexed = plain(P.normalizeProviderResult({method:'getIndexingSamples',hostId:'h'}, {count:1,samples:[{status:'HTTP_2XX',http_code:200,url:'https://x/',access_date:'2026-09-01'}]}));
  assert.equal(indexed.samples[0].access_date, '2026-09-01');
  const searched = plain(P.normalizeProviderResult({method:'getInSearchSamples',hostId:'h'}, {count:1,samples:[{url:'https://x/',last_access:'2026-09-01',title:'X'}]}));
  assert.equal(searched.samples[0].title, 'X');
});

test('W13-05 export metadata routes and shapes follow official enhanced-export resources', () => {
  const { ctx } = contextFor();
  const P = ctx.WebmasterProtocol;
  assert.equal(P.buildRequest({method:'getExportLimits',hostId:'h'},'42').url, 'https://api.webmaster.yandex.net/v4/user/42/hosts/h/pro/limits');
  assert.equal(P.buildRequest({method:'getExportDates',hostId:'h'},'42').url, 'https://api.webmaster.yandex.net/v4/user/42/hosts/h/pro/serp/dates');
  assert.equal(P.buildRequest({method:'getExportRegions',hostId:'h',filter:'Башк',limit:123},'42').url, 'https://api.webmaster.yandex.net/v4/user/42/hosts/h/pro/regions?filter=%D0%91%D0%B0%D1%88%D0%BA&limit=123');
  const limits = plain(P.normalizeProviderResult({method:'getExportLimits',hostId:'h'}, {limits:[{owner:'user-1',feature:'PRO_SERP',limit:1000,used:250,remaining:750,period_start:'2026-01-01',period_end:'2026-12-31',is_active:true,tariff_id:'t'}]}));
  assert.equal(limits.limits[0].remaining, 750);
  assert.equal(limits.limits[0].is_active, true);
  assert.deepEqual(plain(P.normalizeProviderResult({method:'getExportDates',hostId:'h'}, {dates:['2026-09-01']})).dates, ['2026-09-01']);
});

test('W13-06 export start is fail-closed on quota, PRO, paths, regions and payload size', () => {
  const { ctx } = contextFor();
  const P = ctx.WebmasterProtocol;
  assert.throws(() => P.normalizeCommand({method:'startQueryUrlExport',hostId:'h',dates:['2026-09-01'],paths:['/a']}), /confirmQuota/);
  assert.throws(() => P.normalizeCommand({method:'startQueryUrlExport',hostId:'h',dates:['2026-09-01'],paths:['/a'],confirmQuota:true,useProTariff:true}), /confirmProTariff/);
  assert.throws(() => P.normalizeCommand({method:'startQueryUrlExport',hostId:'h',dates:['2026-09-01'],paths:['https:\/\/x\/a'],confirmQuota:true}), /начинаться с \//);
  assert.throws(() => P.normalizeCommand({method:'startQueryUrlExport',hostId:'h',dates:['2026-09-01'],paths:['/a'],regionIds:[0],confirmQuota:true}), /от 1/);
  const dates = Array.from({length:50}, (_,i)=>`2026-08-${String((i%28)+1).padStart(2,'0')}`);
  const paths = Array.from({length:51}, (_,i)=>`/p${i}`);
  assert.throws(() => P.normalizeCommand({method:'startQueryUrlExport',hostId:'h',dates,paths,confirmQuota:true}), /Сумма dates \+ paths/);
  const command = P.normalizeCommand({method:'startQueryUrlExport',hostId:'h',dates:['2026-09-01'],paths:['/a','/b'],regionIds:[213],confirmQuota:true});
  const request = P.buildRequest(command,'42');
  assert.equal(request.method,'POST');
  assert.deepEqual(plain(request.body), {dates:['2026-09-01'],paths:['/a','/b'],region_ids:[213],use_pro_tariff:'false'});
});

test('W13-07 projection is local and computes URL×date quota units', () => {
  const { ctx } = contextFor();
  const P=ctx.WebmasterProtocol, E=ctx.YMBWebmasterExportModel;
  const command=P.normalizeCommand({method:'projectQueryUrlExport',hostId:'h',dates:['2026-09-01','2026-09-02'],paths:['/a','/b','/c']});
  assert.equal(P.isLocalMethod(command.method), true);
  assert.equal(E.projectExport(command).projected_quota_units, 6);
  assert.equal(E.projectExport(command).payload_items, 5);
});

test('W13-08 signed download allowlist rejects arbitrary origins and wrong Yandex paths', () => {
  const { ctx } = contextFor();
  const E=ctx.YMBWebmasterExportModel;
  assert.equal(E.assertSafeDownloadUrl('https://storage.mds.yandex.net/get-webmaster-download/12345678'), 'https://storage.mds.yandex.net/get-webmaster-download/12345678');
  assert.throws(() => E.assertSafeDownloadUrl('https://evil.example/get-webmaster-download/12345678'), /разрешённому Yandex/);
  assert.throws(() => E.assertSafeDownloadUrl('https://storage.mds.yandex.net/other/12345678'), /разрешённому Yandex/);
  assert.throws(() => E.assertSafeDownloadUrl('http://storage.mds.yandex.net/get-webmaster-download/12345678'), /разрешённому Yandex/);
});

test('W13-09 CSV parser handles comma/semicolon/TAB, quoted delimiters and required columns', () => {
  const { ctx } = contextFor();
  const E=ctx.YMBWebmasterExportModel;
  const semicolon = E.parseExportCsv('date;host;URL;query;region;clicks;impressions;position\n2026-09-01;h;https://x/a;"a;b";Москва;2;10;3,5\n');
  assert.equal(semicolon.rows[0].query, 'a;b');
  assert.equal(semicolon.rows[0].position, 3.5);
  const tab = E.parseExportCsv('дата\tхост\tURL\tзапрос\tрегион\tклики\tпоказы\tпозиция\n2026-09-01\th\thttps://x/a\tq\t213\t1\t5\t2.2\n');
  assert.equal(tab.rows[0].impressions, 5);
  assert.throws(() => E.parseExportCsv('date,host,URL\n2026-09-01,h,x\n'), /обязательные колонки/);
});

test('W13-10 durable export survives a fresh runtime context and exposes bounded chunks', async () => {
  const shared = {};
  const first = contextFor(shared).ctx.YMBWebmasterExportModel;
  const taskId='12345678-1234-1234-1234-123456789abc';
  await first.recordStart({hostId:'h',dates:['2026-09-01'],paths:['/a'],regionIds:[],useProTariff:false}, {task_id:taskId,free_quota_used:1,total_quota_used:1,free_quota_remaining:99}, 'r1');
  await first.recordStatus({hostId:'h',taskId}, {download_status:'SUCCESS',url:`https://storage.mds.yandex.net/get-webmaster-download/${taskId}`});
  const second = contextFor(shared).ctx.YMBWebmasterExportModel;
  const before = plain(await second.getManifest(taskId));
  assert.equal(before.download_status,'SUCCESS');
  assert.equal(Object.hasOwn(before,'download_url'),false);
  await second.recordCollected(taskId, 'date,host,URL,query,region,clicks,impressions,position\n2026-09-01,h,https://x/a,q1,213,1,5,2.2\n2026-09-01,h,https://x/b,q2,213,0,3,4.1\n');
  const third = contextFor(shared).ctx.YMBWebmasterExportModel;
  const chunk1=plain(await third.readChunk(taskId,0,1));
  assert.equal(chunk1.rows_returned,1); assert.equal(chunk1.next_offset,1); assert.equal(chunk1.complete,false);
  const chunk2=plain(await third.readChunk(taskId,1,500));
  assert.equal(chunk2.rows_returned,1); assert.equal(chunk2.next_offset,null); assert.equal(chunk2.complete,true);
  assert.equal((await third.listJobs({pendingOnly:true})).length,0);
  assert.match((await third.getManifest(taskId)).collection.raw_sha256,/^[0-9a-f]{64}$/);
});
