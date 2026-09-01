import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { gzipSync } from 'node:zlib';
import { createPhase5Runtime, response } from './helpers/phase5_runtime_harness.mjs';

const hostId = 'https:openscript.ru:443';
const taskId = '2f1c5d3b-7d9b-4c3e-8a14-9d8b924a12ef';
const downloadUrl = `https://storage.mds.yandex.net/get-webmaster-download/${taskId}`;
const plain = (value) => JSON.parse(JSON.stringify(value));
const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');

function env(initial = {}) {
  return createPhase5Runtime({
    ymb_service_credentials: {
      wordstat: { api_key: 'word', folder_id: 'wf', check_state: 'PRESENT' },
      search: { api_key: 'search', folder_id: 'sf', check_state: 'PRESENT' },
      webmaster: { oauth_token: 'wm-oauth', user_id: '42', verified_at: '2026-09-01T00:00:00.000Z', check_state: 'PRESENT' },
      metrika: { oauth_token: 'metrika', check_state: 'PRESENT' },
      direct: { oauth_token: 'direct', check_state: 'PRESENT' }
    },
    ...initial
  });
}

function readyJob(overrides = {}) {
  return {
    task_id: taskId,
    host_id: hostId,
    download_status: 'SUCCESS',
    download_url: downloadUrl,
    projection: { quota_units: 1 },
    quota: { total_quota_used: 1 },
    created_at: '2026-09-01T00:00:00.000Z',
    updated_at: '2026-09-01T00:00:00.000Z',
    collected_at: null,
    rows: null,
    columns: [],
    downloaded_sha256: null,
    downloaded_bytes: 0,
    compression: null,
    csv_sha256: null,
    csv_bytes: 0,
    raw_csv: null,
    raw_sha256: null,
    raw_bytes: 0,
    row_count: 0,
    parse_warning: null,
    ...overrides
  };
}

function exportEnv(job = readyJob()) {
  return env({ ymb_webmaster_query_url_exports_v1: { [taskId]: job } });
}

test('WM14-R01 getHostInfo is exactly one OAuth GET and exposes provider readiness without mutation', async () => {
  const e = env();
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    return response(200, {
      host_id: hostId,
      ascii_host_url: 'https://openscript.ru/',
      unicode_host_url: 'https://openscript.ru/',
      verified: true,
      host_data_status: 'NOT_LOADED',
      host_display_name: 'OpenScript'
    });
  };
  const result = plain(await e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'getHostInfo', hostId }));
  assert.equal(result.ok, true);
  assert.equal(result.request_executed, true);
  assert.equal(result.automatic_retry, false);
  assert.equal(e.requests.length, 1);
  assert.equal(e.requests[0].options.method, 'GET');
  assert.equal(e.requests[0].options.headers.Authorization, 'OAuth wm-oauth');
  assert.equal(e.requests[0].options.body, undefined);
  assert.equal(result.report_envelope.result.host_data_status, 'NOT_LOADED');
  assert.equal(result.report_envelope.result.webmaster_data_ready, false);
});

test('WM14-R02 plain CSV collection stays one storage GET and records NONE compression with separate accounting', async () => {
  const e = exportEnv();
  const csv = 'date,host,URL,query,region,clicks,impressions,position\n2026-08-31,openscript.ru,https://openscript.ru/,docs,Москва,1,5,7\n';
  const csvBytes = Buffer.from(csv, 'utf8');
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    return response(200, csv, { 'Content-Type': 'text/csv' }, { url: downloadUrl });
  };
  const result = plain(await e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'collectQueryUrlExport', hostId, taskId, previewLimit: 5 }));
  assert.equal(e.requests.length, 1);
  assert.equal(e.requests[0].options.method, 'GET');
  assert.equal(Object.hasOwn(e.requests[0].options.headers, 'Authorization'), false);
  const manifest = result.report_envelope.result.manifest;
  assert.equal(manifest.compression, 'NONE');
  assert.equal(manifest.downloaded_bytes, csvBytes.length);
  assert.equal(manifest.csv_bytes, csvBytes.length);
  assert.equal(manifest.downloaded_sha256, sha256(csvBytes));
  assert.equal(manifest.csv_sha256, sha256(csvBytes));
  assert.equal(manifest.raw_sha256, manifest.csv_sha256);
  assert.equal(manifest.raw_bytes, manifest.csv_bytes);
  assert.equal(manifest.row_count, 1);
  assert.equal(result.report_envelope.result.preview.rows[0].query, 'docs');
  const stored = e.storage.state.ymb_webmaster_query_url_exports_v1[taskId];
  assert.equal(stored.raw_csv, csv);
});

test('WM14-R03 gzip CSV with Cyrillic and quoted comma is decompressed locally with no second request', async () => {
  const e = exportEnv();
  const csv = 'date,host,URL,query,region,clicks,impressions,position\n2026-08-31,openscript.ru,https://openscript.ru/,"чат, gpt",Москва,2,10,3.5\n2026-08-31,openscript.ru,https://openscript.ru/docs,документация,Москва,1,5,7\n';
  const csvBytes = Buffer.from(csv, 'utf8');
  const gzipBytes = gzipSync(csvBytes);
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    return response(200, gzipBytes, { 'Content-Type': 'application/gzip' }, { url: downloadUrl });
  };
  const result = plain(await e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'collectQueryUrlExport', hostId, taskId, previewLimit: 2 }));
  assert.equal(e.requests.length, 1, 'gzip collect must still use one storage GET');
  assert.equal(Object.hasOwn(e.requests[0].options.headers, 'Authorization'), false);
  const manifest = result.report_envelope.result.manifest;
  assert.equal(manifest.compression, 'GZIP');
  assert.equal(manifest.downloaded_bytes, gzipBytes.length);
  assert.equal(manifest.csv_bytes, csvBytes.length);
  assert.equal(manifest.downloaded_sha256, sha256(gzipBytes));
  assert.equal(manifest.csv_sha256, sha256(csvBytes));
  assert.notEqual(manifest.downloaded_sha256, manifest.csv_sha256);
  assert.equal(manifest.row_count, 2);
  assert.equal(manifest.parse_warning, null);
  assert.equal(result.report_envelope.result.preview.rows[0].query, 'чат, gpt');
  assert.equal(result.report_envelope.result.preview.rows[1].query, 'документация');
  const stored = e.storage.state.ymb_webmaster_query_url_exports_v1[taskId];
  assert.equal(stored.raw_csv, csv);
  assert.equal(stored.compression, 'GZIP');
  assert.equal(stored.raw_sha256, stored.csv_sha256);
  assert.equal(stored.raw_bytes, stored.csv_bytes);
});

test('WM14-R04 valid empty gzip becomes EMPTY_REPORT instead of a fake CSV header error', async () => {
  const e = exportEnv();
  const gzipBytes = gzipSync(Buffer.alloc(0));
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    return response(200, gzipBytes, { 'Content-Type': 'application/octet-stream' }, { url: downloadUrl });
  };
  const result = plain(await e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'collectQueryUrlExport', hostId, taskId, previewLimit: 20 }));
  const manifest = result.report_envelope.result.manifest;
  assert.equal(e.requests.length, 1);
  assert.equal(manifest.compression, 'GZIP');
  assert.equal(manifest.row_count, 0);
  assert.deepEqual(manifest.columns, []);
  assert.equal(manifest.parse_warning, 'EMPTY_REPORT');
  assert.equal(manifest.csv_bytes, 0);
  assert.equal(result.report_envelope.result.preview.returned, 0);
  assert.deepEqual(result.report_envelope.result.preview.rows, []);
});

test('WM14-R05 corrupt gzip fails explicitly after one storage GET and is never auto-retried', async () => {
  const e = exportEnv();
  const corrupt = Uint8Array.from([0x1f, 0x8b, 0x08, 0x00, 0x01, 0x02, 0x03]);
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    return response(200, corrupt, { 'Content-Type': 'application/gzip' }, { url: downloadUrl });
  };
  await assert.rejects(
    () => e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'collectQueryUrlExport', hostId, taskId }),
    (error) => error.code === 'WEBMASTER_EXPORT_GZIP_DECOMPRESSION_FAILED' && error.request_executed === true && error.automatic_retry === false
  );
  assert.equal(e.requests.length, 1);
  const stored = e.storage.state.ymb_webmaster_query_url_exports_v1[taskId];
  assert.equal(stored.raw_csv, null);
  assert.equal(stored.row_count, 0);
});

test('WM14-R06 invalid UTF-8 after successful download is explicit and keeps one-request boundary', async () => {
  const e = exportEnv();
  const invalidUtf8 = Uint8Array.from([0xff, 0xfe, 0xfd]);
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    return response(200, invalidUtf8, { 'Content-Type': 'application/octet-stream' }, { url: downloadUrl });
  };
  await assert.rejects(
    () => e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'collectQueryUrlExport', hostId, taskId }),
    (error) => error.code === 'WEBMASTER_EXPORT_INVALID_UTF8' && error.request_executed === true && error.automatic_retry === false
  );
  assert.equal(e.requests.length, 1);
});

test('WM14-R07 collect-before-ready remains local SKIPPED even after binary pipeline changes', async () => {
  const e = exportEnv(readyJob({ download_status: 'IN_PROGRESS', download_url: null }));
  e.ctx.fetch = async () => { throw new Error('must not fetch before SUCCESS'); };
  const result = plain(await e.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'collectQueryUrlExport', hostId, taskId }));
  assert.equal(result.ok, true);
  assert.equal(result.request_executed, false);
  assert.equal(result.automatic_retry, false);
  assert.equal(result.report_envelope.status, 'SKIPPED');
  assert.equal(result.report_envelope.reason, 'WEBMASTER_EXPORT_NOT_READY');
  assert.equal(e.requests.length, 0);
});
