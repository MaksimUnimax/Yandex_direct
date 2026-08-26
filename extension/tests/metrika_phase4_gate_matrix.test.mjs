import test from 'node:test';
import assert from 'node:assert/strict';
import { createPhase4Runtime } from './helpers/phase4_runtime_harness.mjs';

const plain = (value) => JSON.parse(JSON.stringify(value));

function response(status, body) {
  return {
    ok: status >= 200 && status < 300,
    status,
    text: async () => typeof body === 'string' ? body : JSON.stringify(body)
  };
}

function metrikaEnv(overrides = {}) {
  return createPhase4Runtime({
    ymb_service_credentials: {
      wordstat: { api_key: 'word-key', folder_id: 'word-folder', check_state: 'PRESENT' },
      search: { api_key: 'search-key', folder_id: 'search-folder', check_state: 'PRESENT' },
      webmaster: { oauth_token: 'webmaster-token', user_id: '42', check_state: 'PRESENT' },
      metrika: { oauth_token: 'fake-metrika-oauth', checked_at: null, check_state: 'PRESENT' }
    },
    ...overrides
  });
}

function capture(env, responder) {
  env.ctx.fetch = async (url, options = {}) => {
    env.requests.push({ url: String(url), options: structuredClone(options) });
    return responder(url, options);
  };
}

function expectLocalReject(protocol, raw, code) {
  assert.throws(() => protocol.normalizeCommand(raw), (error) => error?.code === code);
}

test('M-01 registry contains exactly one Metrika service/prefix and worker keeps one YMB listener owner', () => {
  const env = metrikaEnv();
  const defs = plain(env.ctx.YMBServiceRegistry.DEFINITIONS).filter((item) => item.service === 'metrika');
  assert.deepEqual(defs, [{ service: 'metrika', prefix: 'METRIKA_API_V1' }]);
  assert.equal(env.listeners.length, 1);
  assert.equal(env.ctx.YMBPhase3Runtime, env.ctx.YMBPhase4Runtime);
});

test('M-02 protocol is strict, bounded, and maps local page to provider offset', () => {
  const env = metrikaEnv();
  const P = env.ctx.MetrikaProtocol;
  const list = plain(P.normalizeCommand({ method: 'listCounters', page: 3, perPage: 100, permission: 'view' }));
  assert.deepEqual(list, { method: 'listCounters', page: 3, perPage: 100, permission: 'view' });
  const url = new URL(P.buildRequest(list).url);
  assert.equal(url.pathname, '/management/v1/counters');
  assert.deepEqual(Object.fromEntries(url.searchParams), { offset: '201', per_page: '100', permission: 'view' });

  expectLocalReject(P, { method: 'listCounters', perPage: 1001 }, 'INVALID_FIELD');
  expectLocalReject(P, { method: 'listCounters', permission: 'admin' }, 'INVALID_ENUM');
  expectLocalReject(P, { method: 'getCounter', counterId: 0 }, 'INVALID_FIELD');
  expectLocalReject(P, { method: 'getTrafficSummary', counterId: 1, metrics: 'ym:s:bounceRate' }, 'UNSUPPORTED_FIELD');
  expectLocalReject(P, { method: 'getTrafficSummary', counterId: 1, dateFrom: '2025-01-01', dateTo: '2026-01-02' }, 'DATE_RANGE_TOO_LARGE');
  expectLocalReject(P, { method: 'getTrafficByTime', counterId: 1, group: 'hour' }, 'INVALID_ENUM');
  for (const forbidden of ['oauth_token', 'Authorization', 'headers', 'url', 'dimensions', 'filters', 'preset']) {
    expectLocalReject(P, { method: 'getTrafficSummary', counterId: 1, [forbidden]: 'x' }, 'UNSUPPORTED_FIELD');
  }
  expectLocalReject(P, { method: 'createCounter' }, 'UNSUPPORTED_METHOD');
});

test('M-02 report builder owns fixed metrics and defaults to a bounded seven-day period', () => {
  const env = metrikaEnv();
  const P = env.ctx.MetrikaProtocol;
  const cmd = plain(P.normalizeCommand({ method: 'getTrafficSummary', counterId: 123 }));
  assert.match(cmd.dateFrom, /^\d{4}-\d{2}-\d{2}$/);
  assert.match(cmd.dateTo, /^\d{4}-\d{2}-\d{2}$/);
  const span = Math.floor((Date.parse(cmd.dateTo + 'T00:00:00Z') - Date.parse(cmd.dateFrom + 'T00:00:00Z')) / 86400000) + 1;
  assert.equal(span, 7);
  const url = new URL(P.buildRequest(cmd).url);
  assert.equal(url.pathname, '/stat/v1/data');
  assert.equal(url.searchParams.get('ids'), '123');
  assert.equal(url.searchParams.get('metrics'), 'ym:s:visits,ym:s:users,ym:s:pageviews');
  assert.equal(url.searchParams.has('dimensions'), false);
  assert.equal(url.searchParams.has('filters'), false);
});

test('M-05 Metrika Check accepts 200 with empty counters, uses exact one GET, and stores PRESENT', async () => {
  const env = metrikaEnv();
  capture(env, async () => response(200, { rows: 0, counters: [] }));
  const result = plain(await env.ctx.YMBPhase4Runtime.checkMetrikaCredential());
  assert.equal(env.requests.length, 1);
  assert.equal(env.requests[0].url, 'https://api-metrika.yandex.net/management/v1/counters?per_page=1');
  assert.equal(env.requests[0].options.method, 'GET');
  assert.equal(env.requests[0].options.headers.Authorization, 'OAuth fake-metrika-oauth');
  assert.deepEqual({ ok: result.ok, state: result.state, http_status: result.http_status, counters_seen: result.counters_seen, request_executed: result.request_executed, automatic_retry: result.automatic_retry },
    { ok: true, state: 'PRESENT', http_status: 200, counters_seen: 0, request_executed: true, automatic_retry: false });
  assert.equal(env.storage.state.ymb_service_credentials.metrika.check_state, 'PRESENT');
});

for (const [status, state] of [[401, 'INVALID_OR_EXPIRED'], [403, 'NO_ACCESS'], [420, 'QUOTA'], [429, 'QUOTA']]) {
  test(`M-05 Metrika Check ${status} maps to ${state} with no retry`, async () => {
    const env = metrikaEnv();
    capture(env, async () => response(status, { errors: [{ error_type: 'controlled', message: 'controlled' }] }));
    const result = plain(await env.ctx.YMBPhase4Runtime.checkMetrikaCredential());
    assert.equal(env.requests.length, 1);
    assert.equal(result.ok, false);
    assert.equal(result.state, state);
    assert.equal(result.request_executed, true);
    assert.equal(result.automatic_retry, false);
    assert.equal(env.storage.state.ymb_service_credentials.metrika.check_state, state);
  });
}

test('M-05 Check malformed HTTP 200 is executed=true and does not mark credential PRESENT', async () => {
  const env = metrikaEnv();
  capture(env, async () => response(200, { unexpected: true }));
  await assert.rejects(() => env.ctx.YMBPhase4Runtime.checkMetrikaCredential(), (error) => {
    assert.equal(error.code, 'INVALID_METRIKA_RESPONSE');
    assert.equal(error.request_executed, true);
    assert.equal(error.automatic_retry, false);
    return true;
  });
  assert.equal(env.requests.length, 1);
  assert.equal(env.storage.state.ymb_service_credentials.metrika.check_state, 'NOT_CHECKED');
});

test('M-05 Check network fault is UNKNOWN, stores NETWORK_ERROR and never retries', async () => {
  const env = metrikaEnv();
  env.ctx.fetch = async (url, options = {}) => {
    env.requests.push({ url: String(url), options: structuredClone(options) });
    throw new Error('controlled network fault');
  };
  await assert.rejects(() => env.ctx.YMBPhase4Runtime.checkMetrikaCredential(), (error) => {
    assert.equal(error.code, 'METRIKA_CHECK_NETWORK_ERROR');
    assert.equal(error.request_executed, 'UNKNOWN');
    assert.equal(error.automatic_retry, false);
    return true;
  });
  assert.equal(env.requests.length, 1);
  assert.equal(env.storage.state.ymb_service_credentials.metrika.check_state, 'NETWORK_ERROR');
});

test('M-06 Metrika policy defaults are read-only, zero-cost, autorun-off and 366-day bounded', async () => {
  const env = metrikaEnv();
  const policy = plain(await env.ctx.YMBPhase4Runtime.getMetrikaPolicy());
  assert.equal(policy.manual_enabled, true);
  assert.equal(policy.autorun_enabled, false);
  assert.deepEqual(policy.allowed_methods, ['listCounters', 'getCounter', 'getTrafficSummary', 'getTrafficByTime']);
  assert.equal(policy.max_requests_per_run, 50);
  assert.equal(policy.max_report_days, 366);
  assert.equal(policy.max_cost_rub_per_run, 0);
  assert.deepEqual(policy.method_cost_rub, { listCounters: 0, getCounter: 0, getTrafficSummary: 0, getTrafficByTime: 0 });
});

test('M-07 listCounters uses one OAuth GET, allowlists result and never leaks token', async () => {
  const env = metrikaEnv();
  capture(env, async () => response(200, {
    rows: 1,
    counters: [{ id: 77, name: 'Site', site: 'example.test', status: 'Active', permission: 'own', owner_login: 'owner', favorite: true, type: 'simple', code_status: 'CS_OK', activity_status: 'active', measurement_token: 'must-drop', grants: [{ user: 'x' }] }]
  }));
  const result = plain(await env.ctx.YMBPhase4Runtime.executeMetrikaCommand({ method: 'listCounters', page: 2, perPage: 10 }));
  assert.equal(env.requests.length, 1);
  const url = new URL(env.requests[0].url);
  assert.equal(url.searchParams.get('offset'), '11');
  assert.equal(url.searchParams.get('per_page'), '10');
  assert.equal(env.requests[0].options.headers.Authorization, 'OAuth fake-metrika-oauth');
  assert.deepEqual(result.report_envelope.result, { rows: 1, counters: [{ id: 77, name: 'Site', site: 'example.test', status: 'Active', permission: 'own', owner_login: 'owner', favorite: true, type: 'simple', code_status: 'CS_OK', activity_status: 'active' }] });
  assert.equal(result.report_text.includes('fake-metrika-oauth'), false);
  assert.equal(result.report_text.includes('measurement_token'), false);
  assert.equal(result.report_envelope.request_executed, true);
  assert.equal(result.report_envelope.automatic_retry, false);
});

test('M-08 getCounter uses one safe GET and allowlists counter metadata', async () => {
  const env = metrikaEnv();
  capture(env, async () => response(200, { counter: { id: 9, name: 'Counter', site: 'x.test', status: 'Active', permission: 'view', owner_login: 'o', favorite: false, type: 'simple', code_status: 'OK', activity_status: 'active', measurement_token: 'drop' } }));
  const result = plain(await env.ctx.YMBPhase4Runtime.executeMetrikaCommand({ method: 'getCounter', counterId: 9 }));
  assert.equal(env.requests.length, 1);
  assert.equal(env.requests[0].url, 'https://api-metrika.yandex.net/management/v1/counter/9');
  assert.equal(result.report_envelope.result.counter.id, 9);
  assert.equal(Object.hasOwn(result.report_envelope.result.counter, 'measurement_token'), false);
});

test('M-09 getTrafficSummary owns fixed report shape and preserves truth metadata', async () => {
  const env = metrikaEnv();
  capture(env, async () => response(200, {
    totals: [100, 60, 240], sampled: true, sample_share: 0.5, sample_size: 500, sample_space: 1000,
    contains_sensitive_data: false, data_lag: 15, total_rows: 1, total_rows_rounded: false,
    data: [{ dimensions: [{ name: 'ignore' }], metrics: [100, 60, 240] }]
  }));
  const result = plain(await env.ctx.YMBPhase4Runtime.executeMetrikaCommand({ method: 'getTrafficSummary', counterId: 7, dateFrom: '2026-08-01', dateTo: '2026-08-07' }));
  assert.equal(env.requests.length, 1);
  const url = new URL(env.requests[0].url);
  assert.equal(url.pathname, '/stat/v1/data');
  assert.equal(url.searchParams.get('metrics'), 'ym:s:visits,ym:s:users,ym:s:pageviews');
  assert.deepEqual(result.report_envelope.result, {
    counter_id: 7, date_from: '2026-08-01', date_to: '2026-08-07',
    metrics: { visits: 100, users: 60, pageviews: 240 },
    sampled: true, sample_share: 0.5, sample_size: 500, sample_space: 1000,
    contains_sensitive_data: false, data_lag: 15, total_rows: 1, total_rows_rounded: false
  });
});

test('M-10 getTrafficByTime preserves metric-array order and truth metadata', async () => {
  const env = metrikaEnv();
  capture(env, async () => response(200, {
    data: [{ metrics: [[10, 20, 30], [5, 8, 11], [18, 33, 49]] }],
    totals: [[60], [24], [100]],
    sampled: false, sample_share: 1, sample_size: 3, sample_space: 3,
    contains_sensitive_data: false, data_lag: 0, total_rows: 3, total_rows_rounded: false
  }));
  const result = plain(await env.ctx.YMBPhase4Runtime.executeMetrikaCommand({ method: 'getTrafficByTime', counterId: 7, dateFrom: '2026-08-01', dateTo: '2026-08-03', group: 'day' }));
  assert.equal(env.requests.length, 1);
  const url = new URL(env.requests[0].url);
  assert.equal(url.pathname, '/stat/v1/data/bytime');
  assert.equal(url.searchParams.get('group'), 'day');
  assert.deepEqual(result.report_envelope.result.series, { visits: [10, 20, 30], users: [5, 8, 11], pageviews: [18, 33, 49] });
  assert.deepEqual(result.report_envelope.result.totals, { visits: 60, users: 24, pageviews: 100 });
  assert.equal(result.report_envelope.result.total_rows, 3);
});

for (const status of [400, 401, 403, 404, 420, 429, 500]) {
  test(`M-11 provider error ${status} is truthful and never retried`, async () => {
    const env = metrikaEnv();
    capture(env, async () => response(status, { errors: [{ error_type: `E${status}`, message: 'controlled' }] }));
    const result = plain(await env.ctx.YMBPhase4Runtime.executeMetrikaCommand({ method: 'listCounters' }));
    assert.equal(env.requests.length, 1);
    assert.equal(result.ok, false);
    assert.equal(result.http_status, status);
    assert.equal(result.report_envelope.request_executed, true);
    assert.equal(result.report_envelope.automatic_retry, false);
    assert.equal(result.report_envelope.reason, status === 420 || status === 429 ? 'QUOTA' : `E${status}`);
    assert.equal(result.report_text.includes('fake-metrika-oauth'), false);
  });
}

test('M-11 malformed successful JSON fails after executed provider request and never retries', async () => {
  const env = metrikaEnv();
  capture(env, async () => response(200, '{bad-json'));
  await assert.rejects(() => env.ctx.YMBPhase4Runtime.executeMetrikaCommand({ method: 'listCounters' }), (error) => {
    assert.equal(error.code, 'INVALID_METRIKA_RESPONSE');
    assert.equal(error.request_executed, true);
    assert.equal(error.automatic_retry, false);
    return true;
  });
  assert.equal(env.requests.length, 1);
});

test('M-12 network fault after provider initiation is UNKNOWN with no blind replay', async () => {
  const env = metrikaEnv();
  env.ctx.fetch = async (url, options = {}) => {
    env.requests.push({ url: String(url), options: structuredClone(options) });
    throw new Error('controlled post-initiation fault');
  };
  await assert.rejects(() => env.ctx.YMBPhase4Runtime.executeMetrikaCommand({ method: 'getCounter', counterId: 1 }), (error) => {
    assert.equal(error.code, 'REQUEST_OUTCOME_UNKNOWN_NO_RETRY');
    assert.equal(error.request_executed, 'UNKNOWN');
    assert.equal(error.automatic_retry, false);
    return true;
  });
  assert.equal(env.requests.length, 1);
});

test('M-03/M-04 Metrika credential is isolated, public state redacts it, and old V3 backup preserves it', async () => {
  const env = metrikaEnv();
  const status = plain(await env.ctx.YMBCredentialRuntime.status());
  assert.deepEqual(status.metrika, { has_oauth_token: true, checked_at: null, check_state: 'PRESENT' });
  assert.equal(JSON.stringify(status).includes('fake-metrika-oauth'), false);
  assert.equal(env.storage.state.ymb_service_credentials.webmaster.oauth_token, 'webmaster-token');

  const backup = plain(await env.ctx.YMBPhase4Runtime.exportSettingsBackup());
  assert.equal(backup.backup_version, 3);
  assert.equal(backup.settings.credentials.metrika.oauth_token, 'fake-metrika-oauth');
  delete backup.settings.credentials.metrika;
  delete backup.settings.metrika_policy;
  backup.settings_sha256 = await env.ctx.YMBSettingsBackupV3Runtime.checksum(backup.settings);
  await env.ctx.YMBPhase4Runtime.importSettingsBackup(backup);
  assert.equal(env.storage.state.ymb_service_credentials.metrika.oauth_token, 'fake-metrika-oauth');
  assert.equal(env.storage.state.ymb_service_credentials.webmaster.oauth_token, 'webmaster-token');
});

test('M-04 new V3 backup round-trip restores Metrika only to Metrika and checksum tamper rejects', async () => {
  const env = metrikaEnv();
  const backup = plain(await env.ctx.YMBPhase4Runtime.exportSettingsBackup());
  await env.ctx.YMBCredentialRuntime.save('metrika', { oauth_token: 'mutated-token', checked_at: null, check_state: 'NOT_CHECKED' });
  await env.ctx.YMBPhase4Runtime.importSettingsBackup(backup);
  assert.equal(env.storage.state.ymb_service_credentials.metrika.oauth_token, 'fake-metrika-oauth');
  assert.equal(env.storage.state.ymb_service_credentials.webmaster.oauth_token, 'webmaster-token');

  const tampered = structuredClone(backup);
  tampered.settings.credentials.metrika.oauth_token = 'tampered';
  await assert.rejects(() => env.ctx.YMBPhase4Runtime.importSettingsBackup(tampered), (error) => error?.code === 'BACKUP_CHECKSUM_MISMATCH');
  assert.equal(env.storage.state.ymb_service_credentials.metrika.oauth_token, 'fake-metrika-oauth');
});

test('M-18 deferred/write-like and raw report methods reject before provider initiation', async () => {
  const env = metrikaEnv();
  for (const method of ['createCounter', 'updateCounter', 'deleteCounter', 'createGoal', 'importOfflineConversions', 'logsPrepare', 'rawReport']) {
    await assert.rejects(() => env.ctx.YMBPhase4Runtime.executeMetrikaCommand({ method }), (error) => error?.code === 'UNSUPPORTED_METHOD');
  }
  assert.equal(env.requests.length, 0);
});
