import test from 'node:test';
import assert from 'node:assert/strict';
import { createPhase5Runtime, response } from './helpers/phase5_runtime_harness.mjs';

const plain = (value) => JSON.parse(JSON.stringify(value));

function directEnv(overrides = {}) {
  return createPhase5Runtime({
    ymb_service_credentials: {
      wordstat: { api_key: 'word-key', folder_id: 'word-folder', check_state: 'PRESENT' },
      search: { api_key: 'search-key', folder_id: 'search-folder', check_state: 'PRESENT' },
      webmaster: { oauth_token: 'webmaster-token', user_id: '42', check_state: 'PRESENT' },
      metrika: { oauth_token: 'metrika-token', checked_at: null, check_state: 'PRESENT' },
      direct: { oauth_token: 'direct-secret-token', client_login: 'agency-client', checked_at: null, check_state: 'PRESENT' }
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

test('D-01 registry, worker owner and public Direct credential state are single and separate', async () => {
  const env = directEnv();
  const defs = plain(env.ctx.YMBServiceRegistry.DEFINITIONS).filter((item) => item.service === 'direct');
  assert.deepEqual(defs, [{ service: 'direct', prefix: 'DIRECT_API_V1' }]);
  assert.equal(env.listeners.length, 1);
  assert.equal(env.ctx.YMBPhase3Runtime, env.ctx.YMBPhase5Runtime);

  const publicState = plain(await env.ctx.commonPublicSettingsFields());
  assert.equal(publicState.credential_status.direct.has_oauth_token, true);
  assert.equal(publicState.credential_status.direct.client_login, 'agency-client');
  assert.equal(JSON.stringify(publicState).includes('direct-secret-token'), false);
  assert.equal(publicState.credential_status.webmaster.user_id, '42');
  assert.equal(publicState.credential_status.metrika.has_oauth_token, true);
});

test('D-02 protocol is strict, bounded and owns production v501 routes', () => {
  const env = directEnv();
  const P = env.ctx.DirectProtocol;
  const campaigns = plain(P.normalizeCommand({ method: 'listCampaigns', campaignIds: [7, 7, 9], limit: 1000, offset: 5 }));
  assert.deepEqual(campaigns, { method: 'listCampaigns', campaignIds: [7, 9], limit: 1000, offset: 5 });
  const request = plain(P.buildRequest(campaigns));
  assert.equal(request.method, 'POST');
  assert.equal(request.url, 'https://api.direct.yandex.com/json/v501/campaigns');
  assert.equal(request.body.method, 'get');
  assert.deepEqual(request.body.params.SelectionCriteria, { Ids: [7, 9] });
  assert.equal(request.body.params.Page.Limit, 1000);

  expectLocalReject(P, { method: 'listCampaigns', limit: 1001 }, 'INVALID_FIELD');
  expectLocalReject(P, { method: 'listAdGroups' }, 'MISSING_SELECTOR');
  expectLocalReject(P, { method: 'listAds', adIds: [0] }, 'INVALID_FIELD');
  expectLocalReject(P, { method: 'getCampaignPerformance', dateFrom: '2026-07-01', dateTo: '2026-08-01' }, 'DATE_RANGE_TOO_LARGE');
  expectLocalReject(P, { method: 'setCampaigns' }, 'UNSUPPORTED_METHOD');
  for (const forbidden of ['oauth_token', 'Authorization', 'Client-Login', 'headers', 'url', 'bid', 'strategy']) {
    expectLocalReject(P, { method: 'listCampaigns', [forbidden]: 'x' }, 'UNSUPPORTED_FIELD');
  }
  assert.equal(P.isCommandText('DIRECT_API_V1\n{"method":"listCampaigns"}'), true);
});

test('D-03 Direct Check performs exactly one Campaigns.get and preserves RequestId/Units truth', async () => {
  const env = directEnv();
  capture(env, async () => response(200, { result: { Campaigns: [{ Id: 1 }] } }, { RequestId: 'req-check-1', Units: '3/97/100' }));
  const result = plain(await env.ctx.YMBPhase5Runtime.checkDirectCredential());

  assert.equal(env.requests.length, 1);
  assert.equal(env.requests[0].url, 'https://api.direct.yandex.com/json/v501/campaigns');
  assert.equal(env.requests[0].options.method, 'POST');
  assert.equal(env.requests[0].options.headers.Authorization, 'Bearer direct-secret-token');
  assert.equal(env.requests[0].options.headers['Client-Login'], 'agency-client');
  assert.deepEqual(JSON.parse(env.requests[0].options.body), {
    method: 'get',
    params: { SelectionCriteria: {}, FieldNames: ['Id'], Page: { Limit: 1, Offset: 0 } }
  });
  assert.deepEqual(result, {
    ok: true,
    state: 'PRESENT',
    http_status: 200,
    campaigns_seen: 1,
    provider_request_id: 'req-check-1',
    provider_units: { spent: 3, remaining: 97, daily_limit: 100 },
    request_executed: true,
    automatic_retry: false
  });
  assert.equal(env.storage.state.ymb_service_credentials.direct.oauth_token, 'direct-secret-token');
  assert.equal(env.storage.state.ymb_service_credentials.direct.client_login, 'agency-client');
  assert.equal(env.storage.state.ymb_service_credentials.direct.check_state, 'PRESENT');
});

for (const [providerCode, state] of [[53, 'INVALID_OR_EXPIRED'], [54, 'NO_ACCESS'], [58, 'APP_ACCESS_NOT_APPROVED'], [513, 'DIRECT_ACCOUNT_MISSING'], [3000, 'NO_API_ACCESS'], [152, 'UNITS_EXHAUSTED'], [506, 'CONCURRENCY_LIMIT']]) {
  test(`D-03 Direct semantic error ${providerCode} maps to ${state} without retry`, async () => {
    const env = directEnv();
    capture(env, async () => response(200, { error: { error_code: providerCode, error_string: 'controlled', request_id: `provider-${providerCode}` } }, { Units: '1/9/10' }));
    const result = plain(await env.ctx.YMBPhase5Runtime.checkDirectCredential());
    assert.equal(env.requests.length, 1);
    assert.equal(result.ok, false);
    assert.equal(result.state, state);
    assert.equal(result.request_executed, true);
    assert.equal(result.automatic_retry, false);
    assert.equal(result.provider_request_id, `provider-${providerCode}`);
    assert.deepEqual(result.provider_units, { spent: 1, remaining: 9, daily_limit: 10 });
    assert.equal(env.storage.state.ymb_service_credentials.direct.check_state, state);
  });
}

test('D-03 Direct Check network failure is UNKNOWN and never retries', async () => {
  const env = directEnv();
  env.ctx.fetch = async (url, options = {}) => {
    env.requests.push({ url: String(url), options: structuredClone(options) });
    throw new Error('controlled network fault');
  };
  await assert.rejects(() => env.ctx.YMBPhase5Runtime.checkDirectCredential(), (error) => {
    assert.equal(error.code, 'DIRECT_CHECK_NETWORK_ERROR');
    assert.equal(error.request_executed, 'UNKNOWN');
    assert.equal(error.automatic_retry, false);
    return true;
  });
  assert.equal(env.requests.length, 1);
  assert.equal(env.storage.state.ymb_service_credentials.direct.check_state, 'NETWORK_ERROR');
});

test('D-04/D-05 listCampaigns uses one POST, allowlists data, carries Units and leaks no credential', async () => {
  const env = directEnv();
  capture(env, async () => response(200, {
    result: {
      Campaigns: [{ Id: 77, Name: 'Campaign', StartDate: '2026-08-01', EndDate: null, Type: 'TEXT_CAMPAIGN', Status: 'ACCEPTED', State: 'ON', Currency: 'RUB', SecretField: 'drop-me' }],
      LimitedBy: 100
    }
  }, { RequestId: 'req-list-1', Units: '2/98/100' }));

  const result = plain(await env.ctx.YMBPhase5Runtime.executeDirectCommand({ method: 'listCampaigns', campaignIds: [77], limit: 5 }));
  assert.equal(env.requests.length, 1);
  assert.equal(env.requests[0].options.method, 'POST');
  assert.equal(env.requests[0].options.headers.Authorization, 'Bearer direct-secret-token');
  assert.equal(env.requests[0].options.headers['Client-Login'], 'agency-client');
  assert.deepEqual(result.report_envelope.result, {
    campaigns: [{ id: 77, name: 'Campaign', start_date: '2026-08-01', end_date: null, type: 'TEXT_CAMPAIGN', status: 'ACCEPTED', state: 'ON', currency: 'RUB' }],
    limited_by: 100
  });
  assert.equal(result.report_envelope.provider_request_id, 'req-list-1');
  assert.deepEqual(result.report_envelope.provider_units, { spent: 2, remaining: 98, daily_limit: 100 });
  assert.equal(result.report_envelope.request_executed, true);
  assert.equal(result.report_envelope.automatic_retry, false);
  assert.equal(result.report_text.includes('direct-secret-token'), false);
  assert.equal(result.report_text.includes('agency-client'), false);
  assert.equal(result.report_text.includes('SecretField'), false);
});

test('D-06 reports are online-only TSV POST with fixed headers and no polling', async () => {
  const env = directEnv();
  const tsv = 'Date\tCampaignId\tCampaignName\tImpressions\tClicks\tCost\n2026-08-01\t77\tCampaign\t100\t4\t123456\n';
  capture(env, async () => response(200, tsv, { RequestId: 'report-1', Units: '4/96/100' }));
  const result = plain(await env.ctx.YMBPhase5Runtime.executeDirectCommand({ method: 'getCampaignPerformance', dateFrom: '2026-08-01', dateTo: '2026-08-01', campaignIds: [77], limit: 10 }));

  assert.equal(env.requests.length, 1);
  assert.equal(env.requests[0].url, 'https://api.direct.yandex.com/json/v501/reports');
  assert.equal(env.requests[0].options.method, 'POST');
  assert.equal(env.requests[0].options.headers.processingMode, 'online');
  assert.equal(env.requests[0].options.headers.skipReportHeader, 'true');
  assert.equal(env.requests[0].options.headers.skipReportSummary, 'true');
  const body = JSON.parse(env.requests[0].options.body);
  assert.equal(body.params.ReportType, 'CAMPAIGN_PERFORMANCE_REPORT');
  assert.equal(body.params.Format, 'TSV');
  assert.deepEqual(result.report_envelope.result.rows, [{ date: '2026-08-01', campaign_id: 77, campaign_name: 'Campaign', impressions: 100, clicks: 4, cost_micros: 123456 }]);
  assert.equal(result.report_envelope.result.row_count, 1);
});

test('D-06 async report response is terminal error and is never polled', async () => {
  const env = directEnv();
  capture(env, async () => response(201, '', { RequestId: 'async-report', Units: '1/99/100' }));
  const result = plain(await env.ctx.YMBPhase5Runtime.executeDirectCommand({ method: 'getCampaignPerformance', dateFrom: '2026-08-01', dateTo: '2026-08-01' }));
  assert.equal(env.requests.length, 1);
  assert.equal(result.ok, false);
  assert.equal(result.report_envelope.reason, 'REPORT_ASYNC_NOT_ALLOWED');
  assert.equal(result.report_envelope.request_executed, true);
  assert.equal(result.report_envelope.automatic_retry, false);
});

test('D-07 unknown Direct POST outcome is UNKNOWN and automatic retry remains forbidden', async () => {
  const env = directEnv();
  env.ctx.fetch = async (url, options = {}) => {
    env.requests.push({ url: String(url), options: structuredClone(options) });
    throw new Error('socket reset');
  };
  await assert.rejects(() => env.ctx.YMBPhase5Runtime.executeDirectCommand({ method: 'listCampaigns', limit: 1 }), (error) => {
    assert.equal(error.code, 'REQUEST_OUTCOME_UNKNOWN_NO_RETRY');
    assert.equal(error.request_executed, 'UNKNOWN');
    assert.equal(error.automatic_retry, false);
    return true;
  });
  assert.equal(env.requests.length, 1);
});

test('D-08 policy hard caps are enforced in model, not only popup HTML', async () => {
  const env = directEnv();
  const P = env.ctx.YMBPolicyModel;
  const policy = plain(P.normalizeDirectPolicy({
    autorun_enabled: true,
    manual_enabled: true,
    max_requests_per_run: 999,
    max_page_size: 9999,
    max_report_days: 999,
    max_report_rows: 9999
  }));
  assert.equal(policy.max_requests_per_run, 20);
  assert.equal(policy.max_page_size, 1000);
  assert.equal(policy.max_report_days, 31);
  assert.equal(policy.max_report_rows, 1000);
  assert.equal(policy.max_cost_rub_per_run, 0);

  const atLimit = plain(P.directDecision({ policy, channel: 'manual', method: 'listCampaigns', credentialState: 'PRESENT', run: { requests_executed: 20 } }));
  assert.deepEqual({ allow: atLimit.allow, reason: atLimit.reason }, { allow: false, reason: 'REQUEST_LIMIT' });

  const saved = plain(await env.ctx.YMBPhase5Runtime.saveDirectPolicy({ max_requests_per_run: 500, max_page_size: 5000, max_report_days: 100, max_report_rows: 5000 }));
  assert.equal(saved.max_requests_per_run, 20);
  assert.equal(saved.max_page_size, 1000);
  assert.equal(saved.max_report_days, 31);
  assert.equal(saved.max_report_rows, 1000);
});

test('D-09 Direct credential updates remain isolated from Webmaster and Metrika', async () => {
  const env = directEnv();
  const before = structuredClone(env.storage.state.ymb_service_credentials);
  const saved = plain(await env.ctx.YMBPhase5Runtime.saveServiceCredential('direct', { oauth_token: 'new-direct-token', client_login: 'new-client' }));
  assert.equal(saved.ok, true);
  assert.equal(saved.credential.has_oauth_token, true);
  assert.equal(saved.credential.client_login, 'new-client');
  assert.equal(env.storage.state.ymb_service_credentials.direct.oauth_token, 'new-direct-token');
  assert.equal(env.storage.state.ymb_service_credentials.webmaster.oauth_token, before.webmaster.oauth_token);
  assert.equal(env.storage.state.ymb_service_credentials.metrika.oauth_token, before.metrika.oauth_token);
  assert.equal(env.storage.state.ymb_service_credentials.wordstat.api_key, before.wordstat.api_key);
  assert.equal(env.storage.state.ymb_service_credentials.search.api_key, before.search.api_key);
});

test('D-10 Backup V3 exports Direct and old V3 payload without Direct preserves existing Direct credential/policy', async () => {
  const env = directEnv({
    ymb_direct_policy: { manual_enabled: false, max_requests_per_run: 7, max_page_size: 700, max_report_days: 14, max_report_rows: 500 }
  });
  const backup = plain(await env.ctx.YMBPhase5Runtime.exportSettingsBackup());
  assert.equal(backup.backup_version, 3);
  assert.equal(backup.settings_schema_version, 5);
  assert.equal(backup.settings.credentials.direct.oauth_token, 'direct-secret-token');
  assert.equal(backup.settings.credentials.direct.client_login, 'agency-client');
  assert.equal(backup.settings.direct_policy.max_requests_per_run, 7);

  delete backup.settings.credentials.direct;
  delete backup.settings.direct_policy;
  backup.settings_sha256 = await env.ctx.YMBSettingsBackupV3Runtime.checksum(backup.settings);

  const result = plain(await env.ctx.YMBPhase5Runtime.importSettingsBackup(backup));
  assert.equal(result.direct_credential_preserved_when_absent, true);
  assert.equal(result.direct_policy_preserved_when_absent, true);
  assert.equal(env.storage.state.ymb_service_credentials.direct.oauth_token, 'direct-secret-token');
  assert.equal(env.storage.state.ymb_service_credentials.direct.client_login, 'agency-client');
  assert.equal(env.storage.state.ymb_direct_policy.max_requests_per_run, 7);
  assert.equal(env.storage.state.ymb_direct_policy.max_page_size, 700);
});
