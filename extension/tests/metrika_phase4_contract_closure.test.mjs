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

function envWithMetrika(overrides = {}) {
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

test('M-05 non-empty Check is PRESENT and sends exact Accept plus OAuth headers once', async () => {
  const env = envWithMetrika();
  env.ctx.fetch = async (url, options = {}) => {
    env.requests.push({ url: String(url), options: structuredClone(options) });
    return response(200, { rows: 1, counters: [{ id: 123 }] });
  };
  const result = plain(await env.ctx.YMBPhase4Runtime.checkMetrikaCredential());
  assert.equal(result.ok, true);
  assert.equal(result.state, 'PRESENT');
  assert.equal(result.counters_seen, 1);
  assert.equal(result.request_executed, true);
  assert.equal(result.automatic_retry, false);
  assert.equal(env.requests.length, 1);
  assert.equal(env.requests[0].url, 'https://api-metrika.yandex.net/management/v1/counters?per_page=1');
  assert.equal(env.requests[0].options.method, 'GET');
  assert.equal(env.requests[0].options.headers.Accept, 'application/json');
  assert.equal(env.requests[0].options.headers.Authorization, 'OAuth fake-metrika-oauth');
});

test('M-06 policy rejects locally for channel, operation and request ceiling with zero-cost semantics', () => {
  const env = envWithMetrika();
  const P = env.ctx.YMBPolicyModel;
  const locked = P.normalizeMetrikaPolicy({ manual_enabled: false, autorun_enabled: false, allowed_methods: ['listCounters'], max_requests_per_run: 2 });

  let decision = plain(P.metrikaDecision({ policy: locked, channel: 'manual', method: 'listCounters', credentialState: 'PRESENT', run: {} }));
  assert.deepEqual({ allow: decision.allow, reason: decision.reason, cost: decision.estimated_cost_rub }, { allow: false, reason: 'MANUAL_DISABLED', cost: 0 });

  decision = plain(P.metrikaDecision({ policy: locked, channel: 'autorun', method: 'listCounters', credentialState: 'PRESENT', run: {} }));
  assert.deepEqual({ allow: decision.allow, reason: decision.reason, cost: decision.estimated_cost_rub }, { allow: false, reason: 'AUTORUN_DISABLED', cost: 0 });

  const manual = P.normalizeMetrikaPolicy({ ...locked, manual_enabled: true });
  decision = plain(P.metrikaDecision({ policy: manual, channel: 'manual', method: 'getCounter', credentialState: 'PRESENT', run: {} }));
  assert.deepEqual({ allow: decision.allow, reason: decision.reason }, { allow: false, reason: 'OPERATION_DISABLED' });

  decision = plain(P.metrikaDecision({ policy: manual, channel: 'manual', method: 'listCounters', credentialState: 'PRESENT', run: { requests_executed: 2 } }));
  assert.deepEqual({ allow: decision.allow, reason: decision.reason }, { allow: false, reason: 'REQUEST_LIMIT' });

  decision = plain(P.metrikaDecision({ policy: manual, channel: 'manual', method: 'listCounters', credentialState: 'MISSING', run: {} }));
  assert.deepEqual({ allow: decision.allow, reason: decision.reason }, { allow: false, reason: 'NO_CREDENTIALS' });
  assert.equal(env.requests.length, 0);
});

test('M-10/M-18 bytime preserves every truth field and allowed constructors remain GET-only', async () => {
  const env = envWithMetrika();
  env.ctx.fetch = async (url, options = {}) => {
    env.requests.push({ url: String(url), options: structuredClone(options) });
    return response(200, {
      data: [{ metrics: [[10, 20], [6, 12], [30, 60]] }],
      totals: [[30], [18], [90]],
      sampled: true,
      sample_share: 0.75,
      sample_size: 750,
      sample_space: 1000,
      contains_sensitive_data: true,
      data_lag: 4,
      total_rows: 2,
      total_rows_rounded: true
    });
  };
  const result = plain(await env.ctx.YMBPhase4Runtime.executeMetrikaCommand({ method: 'getTrafficByTime', counterId: 9, dateFrom: '2026-08-01', dateTo: '2026-08-02', group: 'day' }));
  assert.deepEqual(result.report_envelope.result.series, { visits: [10, 20], users: [6, 12], pageviews: [30, 60] });
  assert.deepEqual(result.report_envelope.result.totals, { visits: 30, users: 18, pageviews: 90 });
  assert.deepEqual({
    sampled: result.report_envelope.result.sampled,
    sample_share: result.report_envelope.result.sample_share,
    sample_size: result.report_envelope.result.sample_size,
    sample_space: result.report_envelope.result.sample_space,
    contains_sensitive_data: result.report_envelope.result.contains_sensitive_data,
    data_lag: result.report_envelope.result.data_lag,
    total_rows: result.report_envelope.result.total_rows,
    total_rows_rounded: result.report_envelope.result.total_rows_rounded
  }, {
    sampled: true,
    sample_share: 0.75,
    sample_size: 750,
    sample_space: 1000,
    contains_sensitive_data: true,
    data_lag: 4,
    total_rows: 2,
    total_rows_rounded: true
  });
  assert.equal(env.requests.length, 1);
  assert.equal(env.requests[0].options.method, 'GET');

  const protocol = env.ctx.MetrikaProtocol;
  for (const command of [
    { method: 'listCounters' },
    { method: 'getCounter', counterId: 9 },
    { method: 'getTrafficSummary', counterId: 9, dateFrom: '2026-08-01', dateTo: '2026-08-02' },
    { method: 'getTrafficByTime', counterId: 9, dateFrom: '2026-08-01', dateTo: '2026-08-02', group: 'week' }
  ]) {
    assert.equal(protocol.buildRequest(command).method, 'GET');
  }
});

test('M-18 unsupported/write-like direct runtime rejection is explicit request_executed=false and zero-provider', async () => {
  const env = envWithMetrika();
  for (const method of ['createCounter', 'updateCounter', 'deleteCounter', 'createGoal', 'importOfflineConversions', 'logsPrepare', 'rawReport']) {
    await assert.rejects(() => env.ctx.YMBPhase4Runtime.executeMetrikaCommand({ method }), (error) => {
      assert.equal(error.code, 'UNSUPPORTED_METHOD');
      assert.equal(error.request_executed, false);
      assert.equal(error.automatic_retry, false);
      return true;
    });
  }
  assert.equal(env.requests.length, 0);
});

test('M-03 missing Metrika credential never falls back to another service credential', async () => {
  const env = envWithMetrika({
    ymb_service_credentials: {
      wordstat: { api_key: 'word-key', folder_id: 'word-folder', check_state: 'PRESENT' },
      search: { api_key: 'search-key', folder_id: 'search-folder', check_state: 'PRESENT' },
      webmaster: { oauth_token: 'webmaster-token', user_id: '42', check_state: 'PRESENT' },
      metrika: { oauth_token: '', checked_at: null, check_state: 'MISSING' }
    }
  });
  await assert.rejects(() => env.ctx.YMBPhase4Runtime.executeMetrikaCommand({ method: 'listCounters' }), (error) => {
    assert.equal(error.code, 'METRIKA_OAUTH_MISSING');
    assert.equal(error.request_executed, false);
    assert.equal(error.automatic_retry, false);
    return true;
  });
  assert.equal(env.requests.length, 0);
});
