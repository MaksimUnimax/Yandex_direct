import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');
const plain = (value) => JSON.parse(JSON.stringify(value));

function loadRuntime() {
  const ctx = {
    console, JSON, Object, Array, Set, String, Number, Boolean, RegExp, Date, Error, Math, URL, URLSearchParams,
    globalThis: null
  };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  for (const file of [
    'shared/service_registry.js',
    'shared/policy_model.js',
    'shared/google_search_console_protocol.js',
    'shared/google_search_console_runtime.js'
  ]) {
    vm.runInContext(fs.readFileSync(path.join(src, file), 'utf8'), ctx, { filename: file });
  }
  return {
    Runtime: ctx.YMBGoogleSearchConsoleRuntime,
    Protocol: ctx.GoogleSearchConsoleProtocol,
    Policy: ctx.YMBPolicyModel
  };
}

function response(status, body) {
  const text = typeof body === 'string' ? body : JSON.stringify(body);
  return {
    ok: status >= 200 && status < 300,
    status,
    async text() { return text; }
  };
}

function fixture({ token = 'gsc-secret-token', fetchHandler, identityHandler } = {}) {
  const { Runtime } = loadRuntime();
  const identityCalls = [];
  const fetchCalls = [];
  const identity = {
    async getAccessToken(options) {
      identityCalls.push(plain(options));
      if (identityHandler) return identityHandler(options);
      return token;
    }
  };
  const fetchImpl = async (url, options) => {
    fetchCalls.push({ url, options: plain(options) });
    if (fetchHandler) return fetchHandler(url, options);
    return response(200, { siteEntry: [] });
  };
  const runtime = Runtime.create({
    identity,
    fetchImpl,
    now: () => 1000,
    uuid: () => 'runtime-test-uuid'
  });
  return { runtime, identityCalls, fetchCalls, token };
}

const analyticsCommand = {
  method: 'searchAnalytics',
  siteUrl: 'sc-domain:example.com',
  startDate: '2026-08-01',
  endDate: '2026-08-28',
  dimensions: ['query'],
  rowLimit: 100,
  startRow: 0
};

test('P9-04 runtime factory requires injected identity and fetch adapters and never falls back to ambient Chrome/fetch', () => {
  const { Runtime } = loadRuntime();
  assert.throws(() => Runtime.create({ fetchImpl: async () => {} }), (error) => error.code === 'GSC_IDENTITY_ADAPTER_REQUIRED');
  assert.throws(() => Runtime.create({ identity: { getAccessToken: async () => 'x' } }), (error) => error.code === 'GSC_FETCH_ADAPTER_REQUIRED');
});

test('P9-04 default autorun policy blocks before identity acquisition and before provider fetch', async () => {
  const { runtime, identityCalls, fetchCalls } = fixture();
  const result = await runtime.execute({ method: 'listSites' }, {
    channel: 'autorun',
    policy: {},
    run: { requests_executed: 0, estimated_cost_rub: 0 },
    request_id: 'gsc-policy-1'
  });
  assert.equal(result.ok, false);
  assert.equal(result.skipped, true);
  assert.equal(result.report_envelope.status, 'SKIPPED');
  assert.equal(result.report_envelope.reason, 'AUTORUN_DISABLED');
  assert.equal(result.report_envelope.request_executed, false);
  assert.equal(result.report_envelope.automatic_retry, false);
  assert.equal(identityCalls.length, 0);
  assert.equal(fetchCalls.length, 0);
});

test('P9-04 request ceiling blocks before identity acquisition and before provider fetch', async () => {
  const { runtime, identityCalls, fetchCalls } = fixture();
  const result = await runtime.execute({ method: 'listSites' }, {
    channel: 'manual',
    policy: { max_requests_per_run: 1 },
    run: { requests_executed: 1, estimated_cost_rub: 0 }
  });
  assert.equal(result.ok, false);
  assert.equal(result.skipped, true);
  assert.equal(result.report_envelope.reason, 'REQUEST_LIMIT');
  assert.equal(identityCalls.length, 0);
  assert.equal(fetchCalls.length, 0);
});

test('P9-04 missing non-interactive Google token fails before business provider request', async () => {
  const { runtime, identityCalls, fetchCalls } = fixture({ token: null });
  await assert.rejects(
    () => runtime.execute({ method: 'listSites' }, { channel: 'manual', policy: {} }),
    (error) => error.code === 'GSC_AUTH_REQUIRED' && error.request_executed === false && error.automatic_retry === false
  );
  assert.deepEqual(identityCalls, [{ interactive: false }]);
  assert.equal(fetchCalls.length, 0);
});

test('P9-04 identity adapter failure is fail-closed before provider and never becomes an interactive prompt', async () => {
  const { runtime, identityCalls, fetchCalls } = fixture({
    identityHandler: () => { throw Object.assign(new Error('not signed in'), { code: 'AUTH_REQUIRED' }); }
  });
  await assert.rejects(
    () => runtime.execute({ method: 'listSites' }, { channel: 'manual', policy: {} }),
    (error) => error.code === 'GSC_AUTH_REQUIRED' && error.request_executed === false && error.automatic_retry === false
  );
  assert.deepEqual(identityCalls, [{ interactive: false }]);
  assert.equal(fetchCalls.length, 0);
});

test('P9-04 listSites obtains a non-interactive token then performs exactly one readonly business GET without token leakage', async () => {
  const { runtime, identityCalls, fetchCalls, token } = fixture({
    fetchHandler: () => response(200, {
      siteEntry: [{ siteUrl: 'sc-domain:example.com', permissionLevel: 'siteOwner', ignored: token }]
    })
  });
  const result = await runtime.execute({ method: 'listSites' }, {
    channel: 'manual', policy: {}, request_id: 'gsc-list-1'
  });
  assert.equal(result.ok, true);
  assert.equal(identityCalls.length, 1);
  assert.deepEqual(identityCalls[0], { interactive: false });
  assert.equal(fetchCalls.length, 1);
  assert.equal(fetchCalls[0].url, 'https://www.googleapis.com/webmasters/v3/sites');
  assert.equal(fetchCalls[0].options.method, 'GET');
  assert.equal(fetchCalls[0].options.headers.Authorization, `Bearer ${token}`);
  assert.equal(fetchCalls[0].options.body, undefined);
  assert.deepEqual(plain(result.report_envelope.result), {
    provider: 'google_search_console',
    source: 'Sites',
    sites: [{ site_url: 'sc-domain:example.com', permission_level: 'siteOwner' }]
  });
  assert.equal(result.report_envelope.request_executed, true);
  assert.equal(result.report_envelope.automatic_retry, false);
  assert.equal(result.report_text.includes(token), false);
  assert.equal(JSON.stringify(result.report_envelope).includes(token), false);
});

test('P9-04 searchAnalytics performs one exact POST and preserves average-position provenance', async () => {
  const { runtime, fetchCalls, token } = fixture({
    fetchHandler: () => response(200, {
      rows: [{ keys: ['печать велеса'], clicks: 3, impressions: 12, ctr: 0.25, position: 4.5 }],
      responseAggregationType: 'byProperty'
    })
  });
  const result = await runtime.execute(analyticsCommand, {
    channel: 'manual', policy: {}, request_id: 'gsc-analytics-1'
  });
  assert.equal(fetchCalls.length, 1);
  assert.equal(fetchCalls[0].url, 'https://www.googleapis.com/webmasters/v3/sites/sc-domain%3Aexample.com/searchAnalytics/query');
  assert.equal(fetchCalls[0].options.method, 'POST');
  assert.equal(fetchCalls[0].options.headers.Authorization, `Bearer ${token}`);
  assert.equal(fetchCalls[0].options.headers['Content-Type'], 'application/json');
  assert.deepEqual(JSON.parse(fetchCalls[0].options.body), {
    startDate: '2026-08-01',
    endDate: '2026-08-28',
    type: 'web',
    dimensions: ['query'],
    rowLimit: 100,
    startRow: 0,
    dataState: 'final'
  });
  assert.equal(result.report_envelope.result.position_semantics, 'average_topmost_position_over_impressions');
  assert.deepEqual(plain(result.report_envelope.result.rows[0]), {
    keys: ['печать велеса'], clicks: 3, impressions: 12, ctr: 0.25, average_position: 4.5
  });
  assert.equal(Object.hasOwn(result.report_envelope.result.rows[0], 'rank'), false);
  assert.equal(result.report_text.includes(token), false);
});

test('P9-04 known HTTP provider error executes once and never retries', async () => {
  const { runtime, fetchCalls } = fixture({
    fetchHandler: () => response(403, { error: { status: 'PERMISSION_DENIED', message: 'Forbidden' } })
  });
  const result = await runtime.execute({ method: 'listSites' }, { channel: 'manual', policy: {} });
  assert.equal(fetchCalls.length, 1);
  assert.equal(result.ok, false);
  assert.equal(result.http_status, 403);
  assert.equal(result.report_envelope.status, 'ERROR');
  assert.equal(result.report_envelope.reason, 'PERMISSION_DENIED');
  assert.equal(result.report_envelope.request_executed, true);
  assert.equal(result.report_envelope.automatic_retry, false);
  assert.equal(result.report_envelope.result.error.message, 'Forbidden');
});

test('P9-04 network failure after provider initiation becomes OUTCOME_UNKNOWN and is never retried', async () => {
  const { runtime, fetchCalls } = fixture({
    fetchHandler: () => { throw new Error('socket reset'); }
  });
  await assert.rejects(
    () => runtime.execute({ method: 'listSites' }, { channel: 'manual', policy: {} }),
    (error) => error.code === 'REQUEST_OUTCOME_UNKNOWN_NO_RETRY' && error.request_executed === 'UNKNOWN' && error.automatic_retry === false
  );
  assert.equal(fetchCalls.length, 1);
});

test('P9-04 malformed successful provider body is an executed terminal parse error with no retry', async () => {
  const { runtime, fetchCalls } = fixture({ fetchHandler: () => response(200, '<html>not json</html>') });
  await assert.rejects(
    () => runtime.execute({ method: 'listSites' }, { channel: 'manual', policy: {} }),
    (error) => error.code === 'INVALID_GOOGLE_SEARCH_CONSOLE_RESPONSE' && error.request_executed === true && error.automatic_retry === false
  );
  assert.equal(fetchCalls.length, 1);
});

test('P9-04 runtime result service identity is always google_search_console and a command never expands into hidden pagination', async () => {
  const { runtime, fetchCalls } = fixture({
    fetchHandler: () => response(200, { rows: [{ keys: ['x'], clicks: 1, impressions: 1, ctr: 1, position: 1 }] })
  });
  const result = await runtime.execute({ ...analyticsCommand, startRow: 25000, rowLimit: 25000 }, { channel: 'manual', policy: {} });
  assert.equal(fetchCalls.length, 1);
  assert.equal(result.report_envelope.service, 'google_search_console');
  assert.equal(result.report_envelope.command.startRow, 25000);
  assert.equal(result.report_envelope.command.rowLimit, 25000);
});
