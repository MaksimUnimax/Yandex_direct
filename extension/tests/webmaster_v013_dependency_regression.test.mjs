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

function loadPolicy() {
  const ctx = { console, Date, JSON, Math, Object, Array, Set, Map, Promise, Error, String, Number, Boolean, RegExp, globalThis: null };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(src, 'shared/policy_model.js'), 'utf8'), ctx, { filename: 'policy_model.js' });
  return ctx.YMBPolicyModel;
}

test('WM13-D01 manifest/product/package version are aligned at 0.1.3 and storage host permission is narrow', () => {
  const manifest = JSON.parse(fs.readFileSync(path.join(src, 'manifest.json'), 'utf8'));
  const pkg = JSON.parse(fs.readFileSync(path.join(src, 'package.json'), 'utf8'));
  const productText = fs.readFileSync(path.join(src, 'shared/product.js'), 'utf8');
  assert.equal(manifest.version, '0.1.3');
  assert.equal(pkg.version, '0.1.3');
  assert.match(productText, /VERSION:\s*"0\.1\.3"/);
  assert.ok(manifest.host_permissions.includes('https://api.webmaster.yandex.net/*'));
  assert.ok(manifest.host_permissions.includes('https://storage.mds.yandex.net/*'));
  assert.equal(manifest.host_permissions.some((value) => value.includes('*.yandex.net')), false);
});

test('WM13-D02 legacy 4-method Webmaster policy upgrades to the full v0.1.3 allowlist instead of popup Save silently disabling new methods', () => {
  const Policy = loadPolicy();
  const legacy = { manual_enabled: true, autorun_enabled: false, allowed_methods: ['listHosts', 'getSummary', 'getDiagnostics', 'getPopularQueries'], max_requests_per_run: 17, max_cost_rub_per_run: 0, method_cost_rub: { listHosts: 0, getSummary: 0, getDiagnostics: 0, getPopularQueries: 0 } };
  const normalized = plain(Policy.normalizeWebmasterPolicy(legacy));
  for (const method of ['listHosts', 'getSummary', 'getDiagnostics', 'getPopularQueries', 'getAllQueryHistory', 'getQueryHistory', 'getIndexingSamples', 'getInSearchSamples', 'getExportRegions', 'getExportLimits', 'getExportDates', 'startQueryUrlExport', 'getQueryUrlExportStatus', 'collectQueryUrlExport', 'readQueryUrlExportChunk']) assert.ok(normalized.allowed_methods.includes(method), method);
  assert.equal(normalized.max_requests_per_run, 17);
  assert.equal(normalized.autorun_enabled, false);
  assert.equal(normalized.max_cost_rub_per_run, 0);
});

test('WM13-D03 explicit non-legacy Webmaster allowlists remain restrictive', () => {
  const Policy = loadPolicy();
  const normalized = plain(Policy.normalizeWebmasterPolicy({ allowed_methods: ['listHosts', 'getExportLimits'], manual_enabled: false }));
  assert.deepEqual(normalized.allowed_methods, ['listHosts', 'getExportLimits']);
  assert.equal(normalized.manual_enabled, false);
});

test('WM13-D04 Webmaster policy changes cannot mutate Wordstat/Search/Metrika/Direct credentials', async () => {
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

test('WM13-D05 new Webmaster execution still delegates through Phase4 and Phase5 without bypassing prior-service wrappers', async () => {
  const e = createPhase5Runtime({ ymb_service_credentials: { webmaster: { oauth_token: 'wm', user_id: '42', check_state: 'PRESENT' } } });
  e.ctx.fetch = async (url, options = {}) => {
    e.requests.push({ url: String(url), options: structuredClone(options) });
    return response(200, { dates: ['2026-08-31'] });
  };
  const result = plain(await e.ctx.YMBPhase5ProviderRuntime.execute('webmaster', { method: 'getExportDates', hostId: 'https:openscript.ru:443' }));
  assert.equal(result.ok, true);
  assert.deepEqual(result.report_envelope.result, { dates: ['2026-08-31'] });
  assert.equal(e.requests.length, 1);
});

test('WM13-D06 Metrika and Direct routes remain functional after loading the expanded Phase3 runtime', async () => {
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
    if (String(url).includes('api.direct.yandex.com')) return response(200, { result: { Campaigns: [] } }, { 'RequestId': 'd1', 'Units': '1/100/99' });
    throw new Error(`unexpected ${url}`);
  };
  const metrika = plain(await e.ctx.YMBPhase5ProviderRuntime.executeMetrika({ method: 'listCounters', page: 1, perPage: 1 }));
  const direct = plain(await e.ctx.YMBPhase5ProviderRuntime.executeDirect({ method: 'listCampaigns', limit: 1, offset: 0 }));
  assert.equal(metrika.ok, true);
  assert.equal(direct.ok, true);
  assert.equal(e.requests.length, 2);
});
