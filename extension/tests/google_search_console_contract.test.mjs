import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');
const plain = (value) => JSON.parse(JSON.stringify(value));

function context() {
  const ctx = { console, JSON, Object, Array, Set, String, Number, Boolean, RegExp, Date, Error, Math, URL, URLSearchParams, globalThis: null };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  return ctx;
}

function load(relativePath, exportName) {
  const ctx = context();
  vm.runInContext(fs.readFileSync(path.join(src, relativePath), 'utf8'), ctx, { filename: relativePath });
  return ctx[exportName];
}

function loadRegistry() { return load('shared/service_registry.js', 'YMBServiceRegistry'); }
function loadPolicy() { return load('shared/policy_model.js', 'YMBPolicyModel'); }
function loadGsc() { return load('shared/google_search_console_protocol.js', 'GoogleSearchConsoleProtocol'); }

const originalFive = [
  ['wordstat', 'WORDSTAT_API_V1'],
  ['search', 'SEARCH_API_V1'],
  ['webmaster', 'WEBMASTER_API_V1'],
  ['metrika', 'METRIKA_API_V1'],
  ['direct', 'DIRECT_API_V1']
];

test('P9-03 service registry preserves the five Yandex definitions and appends explicit Google Search Console', () => {
  const registry = loadRegistry();
  assert.deepEqual(plain(registry.DEFINITIONS.slice(0, 5).map(({ service, prefix }) => [service, prefix])), originalFive);
  assert.equal(registry.SERVICES.GOOGLE_SEARCH_CONSOLE, 'google_search_console');
  assert.deepEqual(plain(registry.DEFINITIONS[5]), {
    service: 'google_search_console',
    prefix: 'GOOGLE_SEARCH_CONSOLE_API_V1'
  });
  assert.equal(registry.isKnownService('google_search_console'), true);
  assert.equal(registry.detect('GOOGLE_SEARCH_CONSOLE_API_V1 {"method":"listSites"}').service, 'google_search_console');
  assert.equal(registry.detect('WEBMASTER_API_V1 {"method":"listHosts"}').service, 'webmaster');
});

test('P9-03 protocol exposes only listSites and searchAnalytics as read-only first-slice methods', () => {
  const protocol = loadGsc();
  assert.equal(protocol.PREFIX, 'GOOGLE_SEARCH_CONSOLE_API_V1');
  assert.equal(protocol.RESULT_PREFIX, 'GOOGLE_SEARCH_CONSOLE_RESULT_V1');
  assert.deepEqual([...protocol.METHODS], ['listSites', 'searchAnalytics']);
  assert.deepEqual(plain(protocol.normalizeCommand({ method: 'listSites' })), { method: 'listSites' });
  for (const method of ['addSite', 'deleteSite', 'submitSitemap', 'inspectUrl', 'indexUrl', 'search']) {
    assert.throws(() => protocol.normalizeCommand({ method }), (error) => error.code === 'UNSUPPORTED_METHOD');
  }
});

test('P9-03 protocol never accepts OAuth/access-token material in command JSON', () => {
  const protocol = loadGsc();
  for (const field of ['accessToken', 'oauthToken', 'oauth_token', 'authorization', 'Authorization']) {
    assert.throws(
      () => protocol.normalizeCommand({ method: 'listSites', [field]: 'secret-token' }),
      (error) => error.code === 'UNSUPPORTED_FIELD'
    );
  }
});

test('P9-03 listSites maps to one official readonly GET without auth material in the protocol request', () => {
  const protocol = loadGsc();
  const request = protocol.buildRequest({ method: 'listSites' });
  assert.deepEqual(plain(request), {
    method: 'GET',
    url: 'https://www.googleapis.com/webmasters/v3/sites'
  });
  assert.equal(JSON.stringify(request).includes('Authorization'), false);
  assert.equal(JSON.stringify(request).includes('token'), false);
});

test('P9-03 searchAnalytics freezes bounded defaults and official first-slice fields', () => {
  const protocol = loadGsc();
  const command = protocol.parseCommand(
    'GOOGLE_SEARCH_CONSOLE_API_V1 {"method":"searchAnalytics","siteUrl":"sc-domain:example.com","startDate":"2026-08-01","endDate":"2026-08-28"}'
  );
  assert.deepEqual(plain(command), {
    method: 'searchAnalytics',
    siteUrl: 'sc-domain:example.com',
    startDate: '2026-08-01',
    endDate: '2026-08-28',
    type: 'web',
    dimensions: [],
    rowLimit: 1000,
    startRow: 0,
    dataState: 'final',
    filters: []
  });
});

test('P9-03 searchAnalytics validates dates, bounds, dimensions, type and filter operators fail-closed', () => {
  const protocol = loadGsc();
  const base = { method: 'searchAnalytics', siteUrl: 'https://example.com/', startDate: '2026-08-01', endDate: '2026-08-28' };
  assert.throws(() => protocol.normalizeCommand({ ...base, startDate: '2026-99-99' }), (error) => error.code === 'INVALID_DATE');
  assert.throws(() => protocol.normalizeCommand({ ...base, startDate: '2026-08-29' }), (error) => error.code === 'INVALID_DATE_RANGE');
  assert.throws(() => protocol.normalizeCommand({ ...base, rowLimit: 25001 }), (error) => error.code === 'INVALID_FIELD');
  assert.throws(() => protocol.normalizeCommand({ ...base, rowLimit: 0 }), (error) => error.code === 'INVALID_FIELD');
  assert.throws(() => protocol.normalizeCommand({ ...base, startRow: -1 }), (error) => error.code === 'INVALID_FIELD');
  assert.throws(() => protocol.normalizeCommand({ ...base, type: 'image' }), (error) => error.code === 'INVALID_ENUM');
  assert.throws(() => protocol.normalizeCommand({ ...base, dimensions: ['query', 'hour'] }), (error) => error.code === 'INVALID_ENUM');
  assert.throws(
    () => protocol.normalizeCommand({ ...base, filters: [{ dimension: 'query', operator: 'includingRegex', expression: 'x.*' }] }),
    (error) => error.code === 'INVALID_ENUM'
  );
  assert.throws(
    () => protocol.normalizeCommand({ ...base, filters: [{ dimension: 'date', operator: 'equals', expression: '2026-08-01' }] }),
    (error) => error.code === 'INVALID_ENUM'
  );
});

test('P9-03 searchAnalytics builds exactly one official POST body with explicit pagination', () => {
  const protocol = loadGsc();
  const request = protocol.buildRequest({
    method: 'searchAnalytics',
    siteUrl: 'https://example.com/',
    startDate: '2026-08-01',
    endDate: '2026-08-28',
    dimensions: ['query', 'page', 'device'],
    rowLimit: 25000,
    startRow: 25000,
    dataState: 'all',
    filters: [
      { dimension: 'query', operator: 'contains', expression: 'велес' },
      { dimension: 'country', operator: 'equals', expression: 'rus' }
    ]
  });
  assert.equal(request.method, 'POST');
  assert.equal(request.url, 'https://www.googleapis.com/webmasters/v3/sites/https%3A%2F%2Fexample.com%2F/searchAnalytics/query');
  assert.deepEqual(plain(request.body), {
    startDate: '2026-08-01',
    endDate: '2026-08-28',
    type: 'web',
    dimensions: ['query', 'page', 'device'],
    rowLimit: 25000,
    startRow: 25000,
    dataState: 'all',
    dimensionFilterGroups: [{
      groupType: 'and',
      filters: [
        { dimension: 'query', operator: 'contains', expression: 'велес' },
        { dimension: 'country', operator: 'equals', expression: 'rus' }
      ]
    }]
  });
  assert.equal(JSON.stringify(request.body).includes('token'), false);
  assert.equal(JSON.stringify(request.body).includes('Authorization'), false);
});

test('P9-03 provider normalization preserves GSC average-position provenance instead of relabeling rank', () => {
  const protocol = loadGsc();
  const result = protocol.normalizeProviderResult(
    { method: 'searchAnalytics', siteUrl: 'sc-domain:example.com', startDate: '2026-08-01', endDate: '2026-08-28' },
    {
      rows: [{ keys: ['печать велеса'], clicks: 4, impressions: 20, ctr: 0.2, position: 3.75 }],
      responseAggregationType: 'byProperty'
    }
  );
  assert.equal(result.provider, 'google_search_console');
  assert.equal(result.source, 'Search Analytics');
  assert.equal(result.position_semantics, 'average_topmost_position_over_impressions');
  assert.deepEqual(plain(result.rows[0]), {
    keys: ['печать велеса'],
    clicks: 4,
    impressions: 20,
    ctr: 0.2,
    average_position: 3.75
  });
  assert.equal(Object.hasOwn(result.rows[0], 'rank'), false);
  assert.equal(Object.hasOwn(result.rows[0], 'live_rank'), false);
  assert.equal(Object.hasOwn(result.rows[0], 'exact_serp_rank'), false);
});

test('P9-03 listSites normalization exposes only site URL and permission level', () => {
  const protocol = loadGsc();
  const result = protocol.normalizeProviderResult({ method: 'listSites' }, {
    siteEntry: [
      { siteUrl: 'sc-domain:example.com', permissionLevel: 'siteOwner', privateField: 'drop' },
      { siteUrl: 'https://www.example.org/', permissionLevel: 'siteRestrictedUser' }
    ]
  });
  assert.deepEqual(plain(result), {
    provider: 'google_search_console',
    source: 'Sites',
    sites: [
      { site_url: 'sc-domain:example.com', permission_level: 'siteOwner' },
      { site_url: 'https://www.example.org/', permission_level: 'siteRestrictedUser' }
    ]
  });
});

test('P9-03 result envelopes use a distinct service/provenance surface', () => {
  const protocol = loadGsc();
  const command = protocol.normalizeCommand({ method: 'listSites' });
  const envelope = protocol.buildResultEnvelope({
    requestId: 'gsc-test-1', command, httpStatus: 200, elapsedMs: 2,
    result: { provider: 'google_search_console', source: 'Sites', sites: [] },
    metadata: { request_executed: true, automatic_retry: false }
  });
  assert.equal(envelope.service, 'google_search_console');
  assert.equal(envelope.operation, 'listSites');
  assert.equal(envelope.request_executed, true);
  assert.equal(envelope.automatic_retry, false);
  assert.equal(protocol.formatResultEnvelope(envelope).startsWith('GOOGLE_SEARCH_CONSOLE_RESULT_V1\n'), true);
});

test('P9-03 Google Search Console policy is free-but-bounded and autorun is off by default', () => {
  const policy = loadPolicy();
  assert.deepEqual([...policy.GOOGLE_SEARCH_CONSOLE_METHODS], ['listSites', 'searchAnalytics']);
  const normalized = plain(policy.normalizeGoogleSearchConsolePolicy({}));
  assert.equal(normalized.manual_enabled, true);
  assert.equal(normalized.autorun_enabled, false);
  assert.equal(normalized.max_requests_per_run > 0, true);
  assert.equal(normalized.max_requests_per_run <= 50, true);
  assert.equal(normalized.max_cost_rub_per_run, 0);
  assert.deepEqual(normalized.method_cost_rub, { listSites: 0, searchAnalytics: 0 });
  assert.equal(normalized.allowed_methods.includes('listSites'), true);
  assert.equal(normalized.allowed_methods.includes('searchAnalytics'), true);

  const manual = plain(policy.decisionForService('google_search_console', {
    channel: 'manual', method: 'searchAnalytics', credentialState: 'PRESENT', run: { requests_executed: 0, estimated_cost_rub: 0 }
  }));
  assert.equal(manual.allow, true);
  const autorun = plain(policy.decisionForService('google_search_console', {
    channel: 'autorun', method: 'searchAnalytics', credentialState: 'PRESENT', run: { requests_executed: 0, estimated_cost_rub: 0 }
  }));
  assert.equal(autorun.allow, false);
  assert.equal(autorun.reason, 'AUTORUN_DISABLED');
});
