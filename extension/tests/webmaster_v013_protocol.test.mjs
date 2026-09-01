import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');

function protocol() {
  const ctx = { console, Date, JSON, Math, Object, Array, Set, Map, Promise, Error, String, Number, Boolean, RegExp, encodeURIComponent, globalThis: null, YMBProduct: { VERSION: '0.1.3', BRIDGE_ID: 'yandex-marketing-bridge' } };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(src, 'shared/webmaster_protocol.js'), 'utf8'), ctx, { filename: 'webmaster_protocol.js' });
  return ctx.WebmasterProtocol;
}

const P = protocol();
const hostId = 'https:example.com:443';
const userId = '42';
const taskId = '2f1c5d3b-7d9b-4c3e-8a14-9d8b924a12ef';
const plain = (v) => JSON.parse(JSON.stringify(v));

test('WM13-P01 preserves the four accepted Phase-3 routes byte-for-byte in semantics', () => {
  assert.equal(P.buildRequest({ method: 'listHosts' }, userId).url, 'https://api.webmaster.yandex.net/v4/user/42/hosts');
  assert.equal(P.buildRequest({ method: 'getSummary', hostId }, userId).url, 'https://api.webmaster.yandex.net/v4/user/42/hosts/https%3Aexample.com%3A443/summary');
  assert.equal(P.buildRequest({ method: 'getDiagnostics', hostId }, userId).url, 'https://api.webmaster.yandex.net/v4/user/42/hosts/https%3Aexample.com%3A443/diagnostics');
  const popular = P.buildRequest({ method: 'getPopularQueries', hostId, orderBy: 'TOTAL_SHOWS', limit: 25 }, userId);
  assert.equal(popular.method, 'GET');
  assert.match(popular.url, /\/search-queries\/popular\?/);
  assert.match(popular.url, /order_by=TOTAL_SHOWS/);
  assert.match(popular.url, /device_type_indicator=ALL/);
  assert.match(popular.url, /limit=25/);
});

test('WM13-P02 all-query history uses repeated documented query_indicator parameters', () => {
  const req = P.buildRequest({ method: 'getAllQueryHistory', hostId, queryIndicators: ['TOTAL_SHOWS', 'TOTAL_CLICKS'], deviceTypeIndicator: 'DESKTOP', dateFrom: '2026-08-01', dateTo: '2026-08-31' }, userId);
  assert.equal(req.method, 'GET');
  assert.match(req.url, /\/search-queries\/all\/history\?/);
  assert.match(req.url, /query_indicator=TOTAL_SHOWS&query_indicator=TOTAL_CLICKS/);
  assert.match(req.url, /device_type_indicator=DESKTOP/);
});

test('WM13-P03 single-query history percent-encodes query id and keeps range', () => {
  const req = P.buildRequest({ method: 'getQueryHistory', hostId, queryId: 'query/id 7', queryIndicators: ['AVG_SHOW_POSITION'], dateFrom: '2026-08-01', dateTo: '2026-08-02' }, userId);
  assert.match(req.url, /\/search-queries\/query%2Fid%207\/history\?/);
  assert.match(req.url, /query_indicator=AVG_SHOW_POSITION/);
});

test('WM13-P04 indexing and in-search samples are bounded to 100 rows per provider request', () => {
  assert.equal(P.buildRequest({ method: 'getIndexingSamples', hostId, offset: 100, limit: 100 }, userId).url, 'https://api.webmaster.yandex.net/v4/user/42/hosts/https%3Aexample.com%3A443/indexing/samples?offset=100&limit=100');
  assert.equal(P.buildRequest({ method: 'getInSearchSamples', hostId, offset: 200, limit: 50 }, userId).url, 'https://api.webmaster.yandex.net/v4/user/42/hosts/https%3Aexample.com%3A443/search-urls/in-search/samples?offset=200&limit=50');
  assert.throws(() => P.normalizeCommand({ method: 'getIndexingSamples', hostId, limit: 101 }), /limit/);
});

test('WM13-P05 enhanced-export discovery routes are exact GET resources', () => {
  assert.equal(P.buildRequest({ method: 'getExportLimits', hostId }, userId).url, 'https://api.webmaster.yandex.net/v4/user/42/hosts/https%3Aexample.com%3A443/pro/limits');
  assert.equal(P.buildRequest({ method: 'getExportDates', hostId }, userId).url, 'https://api.webmaster.yandex.net/v4/user/42/hosts/https%3Aexample.com%3A443/pro/serp/dates');
  assert.equal(P.buildRequest({ method: 'getExportRegions', hostId, filter: 'Моск', limit: 123 }, userId).url, 'https://api.webmaster.yandex.net/v4/user/42/hosts/https%3Aexample.com%3A443/pro/regions?filter=%D0%9C%D0%BE%D1%81%D0%BA&limit=123');
});

test('WM13-P06 start export requires explicit quota projection confirmation', () => {
  const base = { method: 'startQueryUrlExport', hostId, dates: ['2026-08-30', '2026-08-31'], paths: ['/a', '/b'], regionIds: [] };
  assert.throws(() => P.normalizeCommand(base), (error) => error.code === 'EXPORT_QUOTA_CONFIRM_REQUIRED');
  assert.throws(() => P.normalizeCommand({ ...base, confirmQuota: true, expectedQuotaUnits: 3 }), (error) => error.code === 'EXPORT_QUOTA_PROJECTION_MISMATCH');
  const normalized = plain(P.normalizeCommand({ ...base, confirmQuota: true, expectedQuotaUnits: 4 }));
  assert.equal(normalized.useProTariff, false);
  assert.deepEqual(plain(P.projectQueryUrlExport(normalized)), { paths: 2, dates: 2, regions: 0, quota_units: 4, payload_cardinality: 4, tariff_mode: 'BASE' });
});

test('WM13-P07 PRO mode is fail-closed without an independent explicit confirmation', () => {
  const base = { method: 'startQueryUrlExport', hostId, dates: ['2026-08-31'], paths: ['/a'], regionIds: [], useProTariff: true, confirmQuota: true, expectedQuotaUnits: 1 };
  assert.throws(() => P.normalizeCommand(base), (error) => error.code === 'EXPORT_PRO_TARIFF_CONFIRM_REQUIRED');
  const req = P.buildRequest({ ...base, confirmProTariff: true }, userId);
  assert.equal(req.method, 'POST');
  assert.equal(req.url, 'https://api.webmaster.yandex.net/v4/user/42/hosts/https%3Aexample.com%3A443/pro/serp/queries/download/');
  assert.deepEqual(plain(req.body), { dates: ['2026-08-31'], paths: ['/a'], region_ids: [], use_pro_tariff: 'true' });
});

test('WM13-P08 base export refuses >100 projected quota units and >100 dates+paths cardinality', () => {
  const dates = Array.from({ length: 11 }, (_, i) => `2026-08-${String(i + 1).padStart(2, '0')}`);
  const paths = Array.from({ length: 10 }, (_, i) => `/p${i}`);
  assert.throws(() => P.normalizeCommand({ method: 'startQueryUrlExport', hostId, dates, paths, confirmQuota: true, expectedQuotaUnits: 110 }), (error) => error.code === 'EXPORT_BASE_QUOTA_REQUEST_TOO_LARGE');
  const tooManyPaths = Array.from({ length: 91 }, (_, i) => `/x${i}`);
  assert.throws(() => P.normalizeCommand({ method: 'startQueryUrlExport', hostId, dates, paths: tooManyPaths, useProTariff: true, confirmQuota: true, expectedQuotaUnits: 1001, confirmProTariff: true }), (error) => error.code === 'EXPORT_PAYLOAD_CARDINALITY_LIMIT');
});

test('WM13-P09 status route is one GET and local/download methods cannot fabricate Webmaster API requests', () => {
  const req = P.buildRequest({ method: 'getQueryUrlExportStatus', hostId, taskId }, userId);
  assert.equal(req.method, 'GET');
  assert.equal(req.url, `https://api.webmaster.yandex.net/v4/user/42/hosts/https%3Aexample.com%3A443/pro/serp/queries/download/${taskId}`);
  assert.throws(() => P.buildRequest({ method: 'collectQueryUrlExport', hostId, taskId }, userId), (error) => error.code === 'LOCAL_METHOD_NO_API_REQUEST');
  assert.throws(() => P.buildRequest({ method: 'readQueryUrlExportChunk', taskId, offset: 0, limit: 20 }, userId), (error) => error.code === 'LOCAL_METHOD_NO_API_REQUEST');
});

test('WM13-P10 provider normalizers keep only stable evidence fields', () => {
  assert.deepEqual(plain(P.normalizeProviderResult({ method: 'getIndexingSamples', hostId }, { count: 1, samples: [{ url: 'https://example.com/a', status: 'HTTP_2XX', http_code: 200, access_date: '2026-08-31T00:00:00+03:00', secret: 'drop' }] })), { count: 1, samples: [{ url: 'https://example.com/a', status: 'HTTP_2XX', http_code: 200, access_date: '2026-08-31T00:00:00+03:00' }] });
  assert.deepEqual(plain(P.normalizeProviderResult({ method: 'getExportLimits', hostId }, { limits: [{ owner: 'u', feature: 'PRO_SERP', limit: 100, used: 3, remaining: 97, period_start: '2026-09-01', period_end: '2026-09-01', is_active: false, tariff_id: 't', extra: 'drop' }] })), { limits: [{ owner: 'u', feature: 'PRO_SERP', limit: 100, used: 3, remaining: 97, period_start: '2026-09-01', period_end: '2026-09-01', is_active: false, tariff_id: 't' }] });
});
