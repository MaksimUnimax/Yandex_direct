import test from 'node:test';
import assert from 'node:assert/strict';
import { createPhase3Runtime } from './helpers/phase3_runtime_harness.mjs';

const plain = (value) => JSON.parse(JSON.stringify(value));

function webmasterEnv() {
  return createPhase3Runtime({
    ymb_service_credentials: {
      wordstat: { api_key: '', folder_id: '' },
      search: { api_key: '', folder_id: '' },
      webmaster: { oauth_token: 'fake-webmaster-oauth', user_id: '42', check_state: 'PRESENT' }
    }
  });
}

function response(status, body) {
  return {
    ok: status >= 200 && status < 300,
    status,
    text: async () => typeof body === 'string' ? body : JSON.stringify(body)
  };
}

function capture(env, responder) {
  env.ctx.fetch = async (url, options = {}) => {
    env.requests.push({ url: String(url), options: structuredClone(options) });
    return responder(url, options);
  };
}

test('W-05 Webmaster Check maps 403 to NO_ACCESS with one request and no retry', async () => {
  const env = createPhase3Runtime({ ymb_service_credentials: {
    wordstat: { api_key: '', folder_id: '' }, search: { api_key: '', folder_id: '' },
    webmaster: { oauth_token: 'fake-webmaster-oauth', user_id: '', check_state: 'NOT_CHECKED' }
  } });
  capture(env, async () => response(403, { error_code: 'INVALID_USER_ID', error_message: 'denied' }));
  const result = plain(await env.ctx.YMBPhase3Runtime.checkWebmasterCredential());
  assert.equal(env.requests.length, 1);
  assert.equal(env.requests[0].url, 'https://api.webmaster.yandex.net/v4/user');
  assert.equal(env.requests[0].options.method, 'GET');
  assert.equal(env.requests[0].options.headers.Authorization, 'OAuth fake-webmaster-oauth');
  assert.deepEqual({ ok: result.ok, state: result.state, http_status: result.http_status, request_executed: result.request_executed, automatic_retry: result.automatic_retry },
    { ok: false, state: 'NO_ACCESS', http_status: 403, request_executed: true, automatic_retry: false });
  assert.equal(env.storage.state.ymb_service_credentials.webmaster.check_state, 'NO_ACCESS');
  assert.equal(env.storage.state.ymb_service_credentials.webmaster.user_id, '');
});

test('W-05 Webmaster Check network fault is UNKNOWN, stores NETWORK_ERROR and never retries', async () => {
  const env = createPhase3Runtime({ ymb_service_credentials: {
    wordstat: { api_key: '', folder_id: '' }, search: { api_key: '', folder_id: '' },
    webmaster: { oauth_token: 'fake-webmaster-oauth', user_id: '', check_state: 'NOT_CHECKED' }
  } });
  env.ctx.fetch = async (url, options = {}) => {
    env.requests.push({ url: String(url), options: structuredClone(options) });
    throw new Error('controlled network fault');
  };
  await assert.rejects(() => env.ctx.YMBPhase3Runtime.checkWebmasterCredential(), (error) => {
    assert.equal(error.code, 'WEBMASTER_CHECK_NETWORK_ERROR');
    assert.equal(error.request_executed, 'UNKNOWN');
    assert.equal(error.automatic_retry, false);
    return true;
  });
  assert.equal(env.requests.length, 1);
  assert.equal(env.storage.state.ymb_service_credentials.webmaster.check_state, 'NETWORK_ERROR');
});

test('W-08 getSummary uses one encoded GET and preserves summary fields', async () => {
  const env = webmasterEnv();
  capture(env, async () => response(200, {
    sqi: 91,
    excluded_pages_count: 2,
    searchable_pages_count: 17,
    site_problems: { FATAL: 1 }
  }));
  const result = plain(await env.ctx.YMBPhase3Runtime.executeWebmasterCommand({ method: 'getSummary', hostId: 'https:example.test:443' }));
  assert.equal(env.requests.length, 1);
  assert.equal(env.requests[0].options.method, 'GET');
  assert.equal(env.requests[0].url, 'https://api.webmaster.yandex.net/v4/user/42/hosts/https%3Aexample.test%3A443/summary');
  assert.deepEqual(result.report_envelope.result, {
    sqi: 91,
    excluded_pages_count: 2,
    searchable_pages_count: 17,
    site_problems: { FATAL: 1 }
  });
  assert.equal(result.report_envelope.request_executed, true);
  assert.equal(result.report_envelope.automatic_retry, false);
});

test('W-09 getDiagnostics uses one GET and preserves governed problem fields only', async () => {
  const env = webmasterEnv();
  capture(env, async () => response(200, { problems: {
    FATAL: { severity: 'FATAL', state: 'PRESENT', last_state_update: '2026-08-25T00:00:00Z', secret_extra: 'drop-me' },
    INFO: { severity: 'INFO', state: 'ABSENT', last_state_update: '2026-08-24T00:00:00Z' }
  } }));
  const result = plain(await env.ctx.YMBPhase3Runtime.executeWebmasterCommand({ method: 'getDiagnostics', hostId: 'host-id' }));
  assert.equal(env.requests.length, 1);
  assert.equal(env.requests[0].url, 'https://api.webmaster.yandex.net/v4/user/42/hosts/host-id/diagnostics');
  assert.deepEqual(result.report_envelope.result, { problems: {
    FATAL: { severity: 'FATAL', state: 'PRESENT', last_state_update: '2026-08-25T00:00:00Z' },
    INFO: { severity: 'INFO', state: 'ABSENT', last_state_update: '2026-08-24T00:00:00Z' }
  } });
  assert.equal(result.report_text.includes('drop-me'), false);
});

test('W-10 getPopularQueries maps every query field safely and normalizes result', async () => {
  const env = webmasterEnv();
  capture(env, async () => response(200, {
    queries: [{ query_id: 'q1', query_text: 'тест', indicators: { TOTAL_SHOWS: 9 }, ignored: 'drop' }],
    date_from: '2026-08-01', date_to: '2026-08-20', count: 1
  }));
  const result = plain(await env.ctx.YMBPhase3Runtime.executeWebmasterCommand({
    method: 'getPopularQueries',
    hostId: 'https:пример.рф:443',
    orderBy: 'TOTAL_CLICKS',
    queryIndicator: 'AVG_CLICK_POSITION',
    deviceTypeIndicator: 'MOBILE',
    dateFrom: '2026-08-01',
    dateTo: '2026-08-20',
    offset: 7,
    limit: 19
  }));
  assert.equal(env.requests.length, 1);
  const url = new URL(env.requests[0].url);
  assert.equal(decodeURIComponent(url.pathname), '/v4/user/42/hosts/https:пример.рф:443/search-queries/popular');
  assert.deepEqual(Object.fromEntries(url.searchParams), {
    order_by: 'TOTAL_CLICKS',
    query_indicator: 'AVG_CLICK_POSITION',
    device_type_indicator: 'MOBILE',
    date_from: '2026-08-01',
    date_to: '2026-08-20',
    offset: '7',
    limit: '19'
  });
  assert.deepEqual(result.report_envelope.result, {
    queries: [{ query_id: 'q1', query_text: 'тест', indicators: { TOTAL_SHOWS: 9 } }],
    date_from: '2026-08-01', date_to: '2026-08-20', count: 1
  });
  assert.equal(result.report_text.includes('fake-webmaster-oauth'), false);
});

for (const fixture of [
  [401, 'UNAUTHORIZED'],
  [403, 'INVALID_USER_ID'],
  [404, 'HOST_NOT_VERIFIED'],
  [404, 'HOST_NOT_INDEXED'],
  [404, 'HOST_NOT_LOADED'],
  [429, 'QUOTA_EXCEEDED'],
  [429, 'TOO_MANY_REQUESTS_ERROR'],
  [500, 'INTERNAL_ERROR']
]) {
  const [status, code] = fixture;
  test(`W-11 provider error ${status} ${code} is truthful and not retried`, async () => {
    const env = webmasterEnv();
    capture(env, async () => response(status, { error_code: code, error_message: `controlled ${code}` }));
    const result = plain(await env.ctx.YMBPhase3Runtime.executeWebmasterCommand({ method: 'listHosts' }));
    assert.equal(env.requests.length, 1);
    assert.equal(result.ok, false);
    assert.equal(result.http_status, status);
    assert.equal(result.report_envelope.status, 'ERROR');
    assert.equal(result.report_envelope.reason, code);
    assert.equal(result.report_envelope.request_executed, true);
    assert.equal(result.report_envelope.automatic_retry, false);
    assert.equal(result.report_envelope.result.error.code, code);
    assert.equal(result.report_text.includes('fake-webmaster-oauth'), false);
    assert.equal(result.report_text.includes('Authorization'), false);
  });
}

test('W-11 malformed successful provider JSON fails as executed=true with no retry', async () => {
  const env = webmasterEnv();
  capture(env, async () => response(200, '{not-json'));
  await assert.rejects(() => env.ctx.YMBPhase3Runtime.executeWebmasterCommand({ method: 'listHosts' }), (error) => {
    assert.equal(error.code, 'INVALID_WEBMASTER_RESPONSE');
    assert.equal(error.request_executed, true);
    assert.equal(error.automatic_retry, false);
    return true;
  });
  assert.equal(env.requests.length, 1);
});

test('W-12 network fault after Webmaster initiation is UNKNOWN and has no blind replay', async () => {
  const env = webmasterEnv();
  env.ctx.fetch = async (url, options = {}) => {
    env.requests.push({ url: String(url), options: structuredClone(options) });
    throw new Error('controlled post-initiation failure');
  };
  await assert.rejects(() => env.ctx.YMBPhase3Runtime.executeWebmasterCommand({ method: 'getSummary', hostId: 'host' }), (error) => {
    assert.equal(error.code, 'REQUEST_OUTCOME_UNKNOWN_NO_RETRY');
    assert.equal(error.request_executed, 'UNKNOWN');
    assert.equal(error.automatic_retry, false);
    return true;
  });
  assert.equal(env.requests.length, 1);
});

test('W-18 deferred/write-like Webmaster method rejects before any provider initiation', async () => {
  const env = webmasterEnv();
  for (const method of ['addHost', 'deleteHost', 'verifyHost', 'submitRecrawl', 'addSitemap', 'deleteSitemap', 'exportQueries']) {
    await assert.rejects(() => env.ctx.YMBPhase3Runtime.executeWebmasterCommand({ method }), (error) => error?.code === 'UNSUPPORTED_METHOD');
  }
  assert.equal(env.requests.length, 0);
});
