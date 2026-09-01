import test from 'node:test';
import assert from 'node:assert/strict';
import { createPhase5Runtime, response } from './helpers/phase5_runtime_harness.mjs';

const hostId = 'https:openscript.ru:443';
const taskId = '2f1c5d3b-7d9b-4c3e-8a14-9d8b924a12ef';
const downloadUrl = `https://storage.mds.yandex.net/get-webmaster-download/${taskId}`;
const plain = (v) => JSON.parse(JSON.stringify(v));

function env() {
  return createPhase5Runtime({
    ymb_service_credentials: {
      wordstat: { api_key: 'word', folder_id: 'wf', check_state: 'PRESENT' },
      search: { api_key: 'search', folder_id: 'sf', check_state: 'PRESENT' },
      webmaster: { oauth_token: 'wm-oauth', user_id: '42', verified_at: '2026-09-01T00:00:00.000Z', check_state: 'PRESENT' },
      metrika: { oauth_token: 'metrika', check_state: 'PRESENT' },
      direct: { oauth_token: 'direct', check_state: 'PRESENT' }
    }
  });
}

test('WM13-R01 existing listHosts remains one OAuth GET through the Phase5 stack', async () => {
  const e = env();
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    return response(200, { hosts: [{ host_id: hostId, ascii_host_url: 'https://openscript.ru', unicode_host_url: 'https://openscript.ru', verified: true }] });
  };
  const result = plain(await e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'listHosts' }));
  assert.equal(result.ok, true);
  assert.equal(result.request_executed, true);
  assert.equal(e.requests.length, 1);
  assert.equal(e.requests[0].options.method, 'GET');
  assert.equal(e.requests[0].options.headers.Authorization, 'OAuth wm-oauth');
  assert.equal(result.report_envelope.result.hosts[0].host_id, hostId);
});

test('WM13-R02 query history is one GET and normalizes time-series indicators', async () => {
  const e = env();
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    return response(200, { indicators: { TOTAL_SHOWS: [{ date: '2026-08-31T00:00:00+03:00', value: 11 }], TOTAL_CLICKS: [{ date: '2026-08-31T00:00:00+03:00', value: 2 }], UNKNOWN: [{ date: 'x', value: 99 }] } });
  };
  const result = plain(await e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'getAllQueryHistory', hostId, queryIndicators: ['TOTAL_SHOWS', 'TOTAL_CLICKS'], dateFrom: '2026-08-31', dateTo: '2026-08-31' }));
  assert.equal(result.ok, true);
  assert.equal(e.requests.length, 1);
  assert.match(e.requests[0].url, /search-queries\/all\/history/);
  assert.equal(result.report_envelope.result.indicators.TOTAL_SHOWS[0].value, 11);
  assert.equal(Object.hasOwn(result.report_envelope.result.indicators, 'UNKNOWN'), false);
});

test('WM13-R03 URL sample methods stay single-request and preserve only analysis fields', async () => {
  const e = env();
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    if (String(url).includes('/indexing/samples')) return response(200, { count: 1, samples: [{ url: 'https://openscript.ru/a', status: 'HTTP_2XX', http_code: 200, access_date: '2026-08-31T00:00:00+03:00', internal: 'drop' }] });
    return response(200, { count: 1, samples: [{ url: 'https://openscript.ru/b', last_access: '2026-08-31T00:00:00+03:00', title: 'B', internal: 'drop' }] });
  };
  const indexing = plain(await e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'getIndexingSamples', hostId, limit: 100 }));
  const inSearch = plain(await e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'getInSearchSamples', hostId, limit: 100 }));
  assert.equal(e.requests.length, 2);
  assert.deepEqual(indexing.report_envelope.result.samples[0], { url: 'https://openscript.ru/a', status: 'HTTP_2XX', http_code: 200, access_date: '2026-08-31T00:00:00+03:00' });
  assert.deepEqual(inSearch.report_envelope.result.samples[0], { url: 'https://openscript.ru/b', last_access: '2026-08-31T00:00:00+03:00', title: 'B' });
});

test('WM13-R04 enhanced-export discovery performs exactly one provider GET per command', async () => {
  const e = env();
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    if (String(url).endsWith('/pro/limits')) return response(200, { limits: [{ owner: 'user', feature: 'PRO_SERP', limit: 100, used: 0, remaining: 100, period_start: '2026-09-01', period_end: '2026-09-01', is_active: false, tariff_id: 'base' }] });
    if (String(url).endsWith('/pro/serp/dates')) return response(200, { dates: ['2026-08-31'] });
    return response(200, { regions: [{ id: 213, name: 'Москва' }] });
  };
  await e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'getExportLimits', hostId });
  await e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'getExportDates', hostId });
  await e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'getExportRegions', hostId, filter: 'Моск', limit: 10 });
  assert.equal(e.requests.length, 3);
  assert.ok(e.requests.every((r) => r.options.method === 'GET'));
  assert.ok(e.requests.every((r) => r.options.headers.Authorization === 'OAuth wm-oauth'));
});

test('WM13-R05 start export is exactly one explicit POST, stores task durability, and sends no secret in durable state', async () => {
  const e = env();
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    return response(200, { task_id: taskId, free_quota_used: 2, pro_quota_used: 0, total_quota_used: 2, free_quota_remaining: 98, pro_quota_remaining: 0 });
  };
  const result = plain(await e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'startQueryUrlExport', hostId, dates: ['2026-08-31'], paths: ['/', '/docs'], regionIds: [213], confirmQuota: true, expectedQuotaUnits: 2 }));
  assert.equal(result.ok, true);
  assert.equal(result.request_executed, true);
  assert.equal(e.requests.length, 1);
  assert.equal(e.requests[0].options.method, 'POST');
  assert.equal(e.requests[0].options.headers.Authorization, 'OAuth wm-oauth');
  assert.equal(e.requests[0].options.headers['Content-Type'], 'application/json');
  assert.deepEqual(JSON.parse(e.requests[0].options.body), { dates: ['2026-08-31'], paths: ['/', '/docs'], region_ids: [213], use_pro_tariff: 'false' });
  const stored = e.storage.state.ymb_webmaster_query_url_exports_v1[taskId];
  assert.equal(stored.task_id, taskId);
  assert.equal(stored.host_id, hostId);
  assert.equal(stored.projection.quota_units, 2);
  assert.equal(stored.download_status, 'SUBMITTED');
  assert.equal(JSON.stringify(stored).includes('wm-oauth'), false);
});

test('WM13-R06 uncertain start POST is fenced UNKNOWN and never fabricates a durable task', async () => {
  const e = env();
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    throw new Error('network cut after initiation');
  };
  await assert.rejects(
    () => e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'startQueryUrlExport', hostId, dates: ['2026-08-31'], paths: ['/'], confirmQuota: true, expectedQuotaUnits: 1 }),
    (error) => error.code === 'REQUEST_OUTCOME_UNKNOWN_NO_RETRY' && error.request_executed === 'UNKNOWN' && error.automatic_retry === false
  );
  assert.equal(e.requests.length, 1);
  assert.equal(e.storage.state.ymb_webmaster_query_url_exports_v1, undefined);
});

test('WM13-R07 status is a separate GET and stores only an allowlisted download URL', async () => {
  const e = env();
  e.storage.state.ymb_webmaster_query_url_exports_v1 = { [taskId]: { task_id: taskId, host_id: hostId, download_status: 'SUBMITTED', projection: { quota_units: 1 }, quota: {}, created_at: '2026-09-01T00:00:00.000Z', rows: null, columns: [], raw_csv: null, raw_sha256: null, raw_bytes: 0, row_count: 0 } };
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    return response(200, { download_status: 'SUCCESS', url: downloadUrl });
  };
  const result = plain(await e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'getQueryUrlExportStatus', hostId, taskId }));
  assert.equal(e.requests.length, 1);
  assert.equal(e.requests[0].options.method, 'GET');
  assert.equal(result.report_envelope.result.download_status, 'SUCCESS');
  assert.equal(Object.hasOwn(result.report_envelope.result, 'url'), false, 'ephemeral storage URL must not be echoed to ChatGPT');
  assert.equal(e.storage.state.ymb_webmaster_query_url_exports_v1[taskId].download_url, downloadUrl);
});

test('WM13-R08 status rejects a non-Yandex download host even after a successful provider response', async () => {
  const e = env();
  e.storage.state.ymb_webmaster_query_url_exports_v1 = { [taskId]: { task_id: taskId, host_id: hostId, download_status: 'SUBMITTED', rows: null, columns: [], raw_csv: null, raw_sha256: null, raw_bytes: 0, row_count: 0 } };
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    return response(200, { download_status: 'SUCCESS', url: `https://evil.example/get-webmaster-download/${taskId}` });
  };
  await assert.rejects(() => e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'getQueryUrlExportStatus', hostId, taskId }), (error) => error.code === 'WEBMASTER_EXPORT_UNSAFE_DOWNLOAD_URL' && error.request_executed === true);
  assert.equal(e.requests.length, 1);
  assert.equal(e.storage.state.ymb_webmaster_query_url_exports_v1[taskId].download_url, undefined);
});

test('WM13-R09 collect is one storage GET, sends no OAuth header, parses quoted CSV, and preserves raw checksum/accounting', async () => {
  const e = env();
  e.storage.state.ymb_webmaster_query_url_exports_v1 = { [taskId]: { task_id: taskId, host_id: hostId, download_status: 'SUCCESS', download_url: downloadUrl, projection: { quota_units: 2 }, quota: { total_quota_used: 2 }, created_at: '2026-09-01T00:00:00.000Z', rows: null, columns: [], raw_csv: null, raw_sha256: null, raw_bytes: 0, row_count: 0 } };
  const csv = 'date,host,URL,query,region,clicks,impressions,position\n2026-08-31,openscript.ru,https://openscript.ru/,"чат, gpt",Москва,2,10,3.5\n2026-08-31,openscript.ru,https://openscript.ru/docs,docs,Москва,1,5,7\n';
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    assert.equal(String(url), downloadUrl);
    return response(200, csv);
  };
  const result = plain(await e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'collectQueryUrlExport', hostId, taskId, previewLimit: 1 }));
  assert.equal(e.requests.length, 1);
  assert.equal(e.requests[0].options.method, 'GET');
  assert.equal(Object.hasOwn(e.requests[0].options.headers, 'Authorization'), false);
  assert.equal(result.report_envelope.result.manifest.row_count, 2);
  assert.equal(result.report_envelope.result.preview.rows[0].query, 'чат, gpt');
  const stored = e.storage.state.ymb_webmaster_query_url_exports_v1[taskId];
  assert.equal(stored.raw_csv, csv);
  assert.equal(stored.rows.length, 2);
  assert.match(stored.raw_sha256, /^[0-9a-f]{64}$/);
  assert.equal(stored.raw_bytes, new TextEncoder().encode(csv).byteLength);
});

test('WM13-R10 chunk read is local-only: zero additional network requests and deterministic pagination', async () => {
  const e = env();
  e.storage.state.ymb_webmaster_query_url_exports_v1 = { [taskId]: { task_id: taskId, host_id: hostId, download_status: 'SUCCESS', projection: {}, quota: {}, rows: [{ query: 'q1' }, { query: 'q2' }, { query: 'q3' }], columns: ['query'], raw_csv: 'x', raw_sha256: 'a'.repeat(64), raw_bytes: 1, row_count: 3, created_at: '2026-09-01T00:00:00.000Z', collected_at: '2026-09-01T01:00:00.000Z' } };
  e.ctx.fetch = async () => { throw new Error('local chunk read must not fetch'); };
  const result = plain(await e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'readQueryUrlExportChunk', taskId, offset: 1, limit: 1 }));
  assert.equal(result.request_executed, false);
  assert.equal(e.requests.length, 0);
  assert.deepEqual(result.report_envelope.result.chunk.rows, [{ query: 'q2' }]);
  assert.equal(result.report_envelope.result.chunk.has_more, true);
});

test('WM13-R11 collect before SUCCESS is a local SKIPPED result and causes zero download traffic', async () => {
  const e = env();
  e.storage.state.ymb_webmaster_query_url_exports_v1 = { [taskId]: { task_id: taskId, host_id: hostId, download_status: 'IN_PROGRESS', projection: {}, quota: {}, rows: null, columns: [], raw_csv: null, raw_sha256: null, raw_bytes: 0, row_count: 0 } };
  e.ctx.fetch = async () => { throw new Error('must not fetch before SUCCESS'); };
  const result = plain(await e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'collectQueryUrlExport', hostId, taskId }));
  assert.equal(result.ok, true);
  assert.equal(result.request_executed, false);
  assert.equal(result.report_envelope.status, 'SKIPPED');
  assert.equal(result.report_envelope.reason, 'WEBMASTER_EXPORT_NOT_READY');
  assert.equal(e.requests.length, 0);
});
