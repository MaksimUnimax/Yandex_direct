import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createPhase5Runtime, response } from './helpers/phase5_runtime_harness.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');
const plain = (v) => JSON.parse(JSON.stringify(v));
const fullV014Methods = [
  'listHosts', 'getHostInfo', 'getSummary', 'getDiagnostics', 'getPopularQueries',
  'getAllQueryHistory', 'getQueryHistory', 'getIndexingSamples', 'getInSearchSamples',
  'getExportRegions', 'getExportLimits', 'getExportDates', 'startQueryUrlExport',
  'getQueryUrlExportStatus', 'collectQueryUrlExport', 'readQueryUrlExportChunk'
];
const v013DefaultMethods = fullV014Methods.filter((method) => method !== 'getHostInfo');

function loadPolicy() {
  const ctx = { console, Date, JSON, Math, Object, Array, Set, Map, Promise, Error, String, Number, Boolean, RegExp, globalThis: null };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(src, 'shared/policy_model.js'), 'utf8'), ctx, { filename: 'policy_model.js' });
  return ctx.YMBPolicyModel;
}

test('WM14-D01 manifest/product/package version are aligned at 0.1.4 and storage host permission remains narrow', () => {
  const manifest = JSON.parse(fs.readFileSync(path.join(src, 'manifest.json'), 'utf8'));
  const pkg = JSON.parse(fs.readFileSync(path.join(src, 'package.json'), 'utf8'));
  const productText = fs.readFileSync(path.join(src, 'shared/product.js'), 'utf8');
  assert.equal(manifest.version, '0.1.4');
  assert.equal(pkg.version, '0.1.4');
  assert.match(productText, /VERSION:\s*"0\.1\.4"/);
  assert.ok(manifest.host_permissions.includes('https://api.webmaster.yandex.net/*'));
  assert.ok(manifest.host_permissions.includes('https://storage.mds.yandex.net/*'));
  assert.equal(manifest.host_permissions.some((value) => value.includes('*.yandex.net')), false);
});

test('WM14-D02 legacy 4-method Webmaster default policy upgrades to the full v0.1.4 allowlist', () => {
  const Policy = loadPolicy();
  const legacy = { manual_enabled: true, autorun_enabled: false, allowed_methods: ['listHosts', 'getSummary', 'getDiagnostics', 'getPopularQueries'], max_requests_per_run: 17, max_cost_rub_per_run: 0, method_cost_rub: { listHosts: 0, getSummary: 0, getDiagnostics: 0, getPopularQueries: 0 } };
  const normalized = plain(Policy.normalizeWebmasterPolicy(legacy));
  for (const method of fullV014Methods) assert.ok(normalized.allowed_methods.includes(method), method);
  assert.equal(normalized.max_requests_per_run, 17);
  assert.equal(normalized.autorun_enabled, false);
  assert.equal(normalized.max_cost_rub_per_run, 0);
});

test('WM14-D03 exact v0.1.3 15-method default policy migrates forward to getHostInfo without shrinking', () => {
  const Policy = loadPolicy();
  const normalized = plain(Policy.normalizeWebmasterPolicy({
    allowed_methods: v013DefaultMethods,
    manual_enabled: true,
    autorun_enabled: false,
    max_requests_per_run: 31,
    method_cost_rub: Object.fromEntries(v013DefaultMethods.map((method) => [method, 0]))
  }));
  assert.deepEqual(new Set(normalized.allowed_methods), new Set(fullV014Methods));
  assert.equal(normalized.allowed_methods.length, fullV014Methods.length);
  assert.equal(normalized.max_requests_per_run, 31);
});

test('WM14-D04 explicit non-default Webmaster allowlists remain restrictive', () => {
  const Policy = loadPolicy();
  const normalized = plain(Policy.normalizeWebmasterPolicy({ allowed_methods: ['listHosts', 'getExportLimits'], manual_enabled: false }));
  assert.deepEqual(normalized.allowed_methods, ['listHosts', 'getExportLimits']);
  assert.equal(normalized.manual_enabled, false);
});

test('WM14-D05 Webmaster policy changes cannot mutate Wordstat/Search/Metrika/Direct credentials', async () => {
  const e = createPhase5Runtime({
    ymb_service_credentials: {
      wordstat: { api_key: 'w', folder_id: 'wf', check_state: 'PRESENT' },
      search: { api_key: 's', folder_id: 'sf', check_state: 'PRESENT' },
      webmaster: { oauth_token: 'wm', user_id: '42', check_state: 'PRESENT' },
      metrika: { oauth_token: 'm', check_state: 'PRESENT' },
      direct: { oauth_token: 'd', client_login: 'dl', check_state: 'PRESENT' }
    }
  });
  const before = structuredClone(e.storage.state.ymb_service_credentials);
  await e.ctx.YMBPhase5ProviderRuntime.saveWebmasterPolicy({ allowed_methods: ['listHosts', 'getExportLimits'], max_requests_per_run: 9 });
  assert.deepEqual(e.storage.state.ymb_service_credentials, before);
  assert.equal(e.storage.state.ymb_webmaster_policy.max_requests_per_run, 9);
});

test('WM14-D06 getHostInfo and existing Webmaster execution still delegate through Phase4 and Phase5', async () => {
  const e = createPhase5Runtime({ ymb_service_credentials: { webmaster: { oauth_token: 'wm', user_id: '42', check_state: 'PRESENT' } } });
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    if (String(url).endsWith('/hosts/https%3Aopenscript.ru%3A443')) return response(200, { host_id: 'https:openscript.ru:443', ascii_host_url: 'https://openscript.ru/', unicode_host_url: 'https://openscript.ru/', verified: true, host_data_status: 'OK' });
    return response(200, { dates: ['2026-08-31'] });
  };
  const info = plain(await e.ctx.YMBPhase5ProviderRuntime.execute('webmaster', { method: 'getHostInfo', hostId: 'https:openscript.ru:443' }));
  const dates = plain(await e.ctx.YMBPhase5ProviderRuntime.execute('webmaster', { method: 'getExportDates', hostId: 'https:openscript.ru:443' }));
  assert.equal(info.ok, true);
  assert.equal(info.report_envelope.result.webmaster_data_ready, true);
  assert.deepEqual(dates.report_envelope.result, { dates: ['2026-08-31'] });
  assert.equal(e.requests.length, 2);
});

test('WM14-D07 Metrika and Direct routes remain functional after loading the modified Phase3 runtime', async () => {
  const e = createPhase5Runtime({
    ymb_service_credentials: {
      webmaster: { oauth_token: 'wm', user_id: '42', check_state: 'PRESENT' },
      metrika: { oauth_token: 'm', check_state: 'PRESENT' },
      direct: { oauth_token: 'd', client_login: 'client', check_state: 'PRESENT' }
    }
  });
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    if (String(url).includes('api-metrika.yandex.net')) return response(200, { rows: 0, counters: [] });
    if (String(url).includes('api.direct.yandex.com')) return response(200, { result: { Campaigns: [] } }, { RequestId: 'd1', Units: '1/100/99' });
    throw new Error(`unexpected ${url}`);
  };
  const metrika = plain(await e.ctx.YMBPhase5ProviderRuntime.executeMetrika({ method: 'listCounters', page: 1, perPage: 1 }));
  const direct = plain(await e.ctx.YMBPhase5ProviderRuntime.executeDirect({ method: 'listCampaigns', limit: 1, offset: 0 }));
  assert.equal(metrika.ok, true);
  assert.equal(direct.ok, true);
  assert.equal(e.requests.length, 2);
});

test('WM14-D08 Wordstat still traverses the modified Phase3→Phase4→Phase5 provider chain exactly once', async () => {
  const e = createPhase5Runtime({
    ymb_service_credentials: {
      wordstat: { api_key: 'word-key', folder_id: 'word-folder', check_state: 'PRESENT' },
      webmaster: { oauth_token: 'wm', user_id: '42', check_state: 'PRESENT' }
    }
  });
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    return response(200, { phrases: [{ phrase: 'окна', views: 12 }] });
  };
  const result = plain(await e.ctx.YMBPhase5ProviderRuntime.execute('wordstat', { method: 'getTop', phrase: 'окна' }));
  assert.equal(result.ok, true);
  assert.equal(result.request_executed, true);
  assert.equal(e.requests.length, 1);
  assert.equal(e.requests[0].url, 'https://wordstat.example/word-folder');
  assert.equal(e.requests[0].options.method, 'POST');
  assert.equal(e.requests[0].options.headers.Authorization, 'Api-Key word-key');
  assert.deepEqual(result.report_envelope.result, { phrases: [{ phrase: 'окна', views: 12 }] });
});

test('WM14-D09 Search still traverses the modified Phase3→Phase4→Phase5 provider chain exactly once', async () => {
  const e = createPhase5Runtime({
    ymb_service_credentials: {
      search: { api_key: 'search-key', folder_id: 'search-folder', check_state: 'PRESENT' },
      webmaster: { oauth_token: 'wm', user_id: '42', check_state: 'PRESENT' }
    }
  });
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    return response(200, { raw: 'search-ok' });
  };
  const result = plain(await e.ctx.YMBPhase5ProviderRuntime.execute('search', { method: 'search', queryText: 'окна' }));
  assert.equal(result.ok, true);
  assert.equal(result.request_executed, true);
  assert.equal(e.requests.length, 1);
  assert.equal(e.requests[0].url, 'https://search.example/search-folder');
  assert.equal(e.requests[0].options.method, 'POST');
  assert.equal(e.requests[0].options.headers.Authorization, 'Api-Key search-key');
  assert.deepEqual(result.report_envelope.result, { raw: 'search-ok' });
});
