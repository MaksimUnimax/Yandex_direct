import test from 'node:test';
import assert from 'node:assert/strict';
import { createPhase5Runtime, response } from '../helpers/phase5_runtime_harness.mjs';

const plain = (value) => JSON.parse(JSON.stringify(value));

function directEnv(overrides = {}) {
  return createPhase5Runtime({
    ymb_service_credentials: {
      wordstat: { api_key: 'word-key', folder_id: 'word-folder', check_state: 'PRESENT' },
      search: { api_key: 'search-key', folder_id: 'search-folder', check_state: 'PRESENT' },
      webmaster: { oauth_token: 'webmaster-token', user_id: '42', check_state: 'PRESENT' },
      metrika: { oauth_token: 'metrika-token', check_state: 'PRESENT' },
      direct: { oauth_token: 'qa-direct-token', client_login: 'qa-client-login', check_state: 'PRESENT' }
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

function localReject(P, command, expectedCode) {
  assert.throws(() => P.normalizeCommand(command), (error) => error?.code === expectedCode);
}

test('official D-02 strict command surface, cardinality, bounds and injection locks', () => {
  const { ctx } = directEnv();
  const P = ctx.DirectProtocol;
  localReject(P, {}, 'MISSING_FIELD');
  localReject(P, { method: 'unknown' }, 'UNSUPPORTED_METHOD');
  localReject(P, { method: 'listCampaigns', custom: 1 }, 'UNSUPPORTED_FIELD');
  localReject(P, { method: 'listCampaigns', campaignIds: Array.from({ length: 11 }, (_, i) => i + 1) }, 'TOO_MANY_IDS');
  localReject(P, { method: 'listAdGroups', adGroupIds: Array.from({ length: 1001 }, (_, i) => i + 1) }, 'TOO_MANY_IDS');
  localReject(P, { method: 'listAds', adIds: [Number.MAX_SAFE_INTEGER + 1] }, 'INVALID_FIELD');
  localReject(P, { method: 'listKeywords', keywordIds: [-1] }, 'INVALID_FIELD');
  localReject(P, { method: 'listCampaigns', limit: 0 }, 'INVALID_FIELD');
  localReject(P, { method: 'listCampaigns', limit: 1001 }, 'INVALID_FIELD');
  localReject(P, { method: 'listCampaigns', offset: -1 }, 'INVALID_FIELD');
  localReject(P, { method: 'getCampaignPerformance', dateFrom: '2026-08-01', dateTo: '2026-09-01' }, 'DATE_RANGE_TOO_LARGE');
  localReject(P, { method: 'getCampaignPerformance', dateFrom: '2026-08-02', dateTo: '2026-08-01' }, 'INVALID_DATE_RANGE');
  localReject(P, { method: 'getCampaignPerformance', dateFrom: '2026-02-30', dateTo: '2026-03-01' }, 'INVALID_DATE');
  localReject(P, { method: 'getCampaignPerformance', dateFrom: '2026-08-01', dateTo: '2026-08-01', campaignIds: Array.from({ length: 11 }, (_, i) => i + 1) }, 'TOO_MANY_IDS');
  for (const field of ['oauth_token', 'Authorization', 'Client-Login', 'headers', 'url', 'service', 'providerMethod', 'FieldNames', 'SelectionCriteria', 'reportType', 'filters', 'processingMode', 'Payment-Token', 'Use-Operator-Units']) {
    localReject(P, { method: 'listCampaigns', [field]: field === 'processingMode' ? 'offline' : 'x' }, 'UNSUPPORTED_FIELD');
  }
});

test('official D-04 backup tamper rejection and blank Direct OAuth preservation', async () => {
  const env = directEnv();
  const before = structuredClone(env.storage.state.ymb_service_credentials);
  await env.ctx.YMBPhase5Runtime.saveServiceCredential('direct', { client_login: 'changed-client-only' });
  assert.equal(env.storage.state.ymb_service_credentials.direct.oauth_token, 'qa-direct-token');
  assert.equal(env.storage.state.ymb_service_credentials.direct.client_login, 'changed-client-only');
  assert.equal(env.storage.state.ymb_service_credentials.webmaster.oauth_token, before.webmaster.oauth_token);
  assert.equal(env.storage.state.ymb_service_credentials.webmaster.user_id, before.webmaster.user_id);
  assert.equal(env.storage.state.ymb_service_credentials.webmaster.check_state, before.webmaster.check_state);
  assert.equal(env.storage.state.ymb_service_credentials.metrika.oauth_token, before.metrika.oauth_token);
  assert.equal(env.storage.state.ymb_service_credentials.metrika.check_state, before.metrika.check_state);

  const backup = plain(await env.ctx.YMBPhase5Runtime.exportSettingsBackup());
  assert.equal(Object.keys(backup.settings.credentials).sort().join(','), 'direct,metrika,search,webmaster,wordstat');
  const snapshot = structuredClone(env.storage.state);
  backup.settings.credentials.direct.client_login = 'tampered-client';
  await assert.rejects(() => env.ctx.YMBPhase5Runtime.importSettingsBackup(backup));
  assert.deepEqual(env.storage.state, snapshot);
});

test('official D-05 Direct Check zero/one campaign and complete compatibility error matrix', async () => {
  for (const campaigns of [[], [{ Id: 1 }]]) {
    const env = directEnv();
    capture(env, async () => response(200, { result: { Campaigns: campaigns } }, { RequestId: 'check-ok', Units: '1/9/10' }));
    const result = plain(await env.ctx.YMBPhase5Runtime.checkDirectCredential());
    assert.equal(result.ok, true);
    assert.equal(result.state, 'PRESENT');
    assert.equal(result.campaigns_seen, campaigns.length);
    assert.equal(env.requests.length, 1);
    const hit = env.requests[0];
    assert.equal(hit.url, 'https://api.direct.yandex.com/json/v501/campaigns');
    assert.equal(hit.options.method, 'POST');
    assert.equal(hit.options.headers.Authorization, 'Bearer qa-direct-token');
    assert.equal(hit.options.headers['Accept-Language'], 'ru');
    assert.equal(hit.options.headers['Content-Type'], 'application/json; charset=utf-8');
    assert.equal(hit.options.headers['Client-Login'], 'qa-client-login');
    assert.deepEqual(JSON.parse(hit.options.body), { method: 'get', params: { SelectionCriteria: {}, FieldNames: ['Id'], Page: { Limit: 1, Offset: 0 } } });
  }

  const cases = [
    [53, 'invalid token', 'INVALID_OR_EXPIRED'],
    [54, 'no access', 'NO_ACCESS'],
    [58, 'app access', 'APP_ACCESS_NOT_APPROVED'],
    [152, 'units', 'UNITS_EXHAUSTED'],
    [506, 'parallel', 'CONCURRENCY_LIMIT'],
    [513, 'account', 'DIRECT_ACCOUNT_MISSING'],
    [3000, 'api access', 'NO_API_ACCESS'],
    [1002, 'OAuth token invalid', 'INVALID_OR_EXPIRED'],
    [1002, 'generic provider error', 'NOT_CHECKED'],
    [55, 'not allowed', 'NOT_CHECKED']
  ];
  for (const [code, text, state] of cases) {
    const env = directEnv();
    capture(env, async () => response(200, { error: { error_code: code, error_string: text, request_id: `check-${code}` } }, { Units: '1/9/10' }));
    const result = plain(await env.ctx.YMBPhase5Runtime.checkDirectCredential());
    assert.equal(result.ok, false, `code ${code}`);
    assert.equal(result.state, state, `code ${code}`);
    assert.equal(result.request_executed, true);
    assert.equal(result.automatic_retry, false);
    assert.equal(env.requests.length, 1);
  }
});

test('official D-06 policy defaults and hard caps are exact', async () => {
  const env = directEnv();
  const defaults = plain(await env.ctx.YMBPhase5Runtime.getDirectPolicy());
  assert.equal(defaults.autorun_enabled, false);
  assert.equal(defaults.manual_enabled, true);
  assert.deepEqual(defaults.allowed_methods, ['listCampaigns', 'listAdGroups', 'listAds', 'listKeywords', 'getCampaignPerformance']);
  assert.equal(defaults.max_requests_per_run, 20);
  assert.equal(defaults.max_page_size, 1000);
  assert.equal(defaults.max_report_days, 31);
  assert.equal(defaults.max_report_rows, 1000);
  assert.equal(defaults.max_cost_rub_per_run, 0);
  assert.deepEqual(defaults.method_cost_rub, { listCampaigns: 0, listAdGroups: 0, listAds: 0, listKeywords: 0, getCampaignPerformance: 0 });
  const capped = plain(await env.ctx.YMBPhase5Runtime.saveDirectPolicy({ autorun_enabled: true, manual_enabled: false, max_requests_per_run: 999, max_page_size: 9999, max_report_days: 999, max_report_rows: 9999 }));
  assert.equal(capped.autorun_enabled, true);
  assert.equal(capped.manual_enabled, false);
  assert.equal(capped.max_requests_per_run, 20);
  assert.equal(capped.max_page_size, 1000);
  assert.equal(capped.max_report_days, 31);
  assert.equal(capped.max_report_rows, 1000);
  assert.equal(capped.max_cost_rub_per_run, 0);
});

const objectCases = [
  {
    label: 'D-07 listCampaigns',
    command: { method: 'listCampaigns', campaignIds: [11], limit: 7, offset: 2 },
    route: '/campaigns',
    expectedFields: ['Id','Name','StartDate','EndDate','Type','Status','State','Currency'],
    provider: { result: { Campaigns: [{ Id: 11, Name: 'C', StartDate: '2026-08-01', EndDate: null, Type: 'TEXT_CAMPAIGN', Status: 'ACCEPTED', State: 'ON', Currency: 'RUB', Funds: 999, Notification: 'drop' }] } },
    verify(result) { assert.deepEqual(result.campaigns[0], { id:11, name:'C', start_date:'2026-08-01', end_date:null, type:'TEXT_CAMPAIGN', status:'ACCEPTED', state:'ON', currency:'RUB' }); }
  },
  {
    label: 'D-08 listAdGroups',
    command: { method: 'listAdGroups', campaignIds: [11], adGroupIds: [21], limit: 7, offset: 2 },
    route: '/adgroups',
    expectedFields: ['Id','Name','CampaignId','Status','ServingStatus','Type'],
    provider: { result: { AdGroups: [{ Id:21, Name:'G', CampaignId:11, Status:'ACCEPTED', ServingStatus:'ELIGIBLE', Type:'TEXT_AD_GROUP', DynamicTextAdGroup:{drop:true} }] } },
    verify(result) { assert.deepEqual(result.ad_groups[0], { id:21, name:'G', campaign_id:11, status:'ACCEPTED', serving_status:'ELIGIBLE', type:'TEXT_AD_GROUP' }); }
  },
  {
    label: 'D-09 listAds',
    command: { method: 'listAds', campaignIds: [11], adGroupIds: [21], adIds: [31], limit: 7, offset: 2 },
    route: '/ads',
    expectedFields: ['Id','CampaignId','AdGroupId','Status','State','Type','Subtype'],
    provider: { result: { Ads: [{ Id:31, CampaignId:11, AdGroupId:21, Status:'ACCEPTED', State:'ON', Type:'TEXT_AD', Subtype:'NONE', TextAd:{Href:'drop',Text:'drop'} }] } },
    verify(result) { assert.deepEqual(result.ads[0], { id:31, campaign_id:11, ad_group_id:21, status:'ACCEPTED', state:'ON', type:'TEXT_AD', subtype:'NONE' }); }
  },
  {
    label: 'D-10 listKeywords',
    command: { method: 'listKeywords', campaignIds: [11], adGroupIds: [21], keywordIds: [41], limit: 7, offset: 2 },
    route: '/keywords',
    expectedFields: ['Id','Keyword','State','Status','ServingStatus','AdGroupId','CampaignId','Bid','ContextBid','StrategyPriority'],
    provider: { result: { Keywords: [{ Id:41, Keyword:'query', State:'ON', Status:'ACCEPTED', ServingStatus:'ELIGIBLE', AdGroupId:21, CampaignId:11, Bid:'123456', ContextBid:654321, StrategyPriority:'NORMAL', Productivity:{drop:true}, StatisticsSearch:{drop:true}, StatisticsNetwork:{drop:true} }] } },
    verify(result) { assert.deepEqual(result.keywords[0], { id:41, keyword:'query', state:'ON', status:'ACCEPTED', serving_status:'ELIGIBLE', ad_group_id:21, campaign_id:11, bid_micros:123456, context_bid_micros:654321, strategy_priority:'NORMAL' }); }
  }
];

for (const c of objectCases) {
  test(`official ${c.label} exact trusted request and allowlisted response`, async () => {
    const env = directEnv();
    capture(env, async () => response(200, c.provider, { RequestId: 'object-read', Units: '2/8/10', 'Units-Used-Login': 'private-login' }));
    const out = plain(await env.ctx.YMBPhase5Runtime.executeDirectCommand(c.command));
    assert.equal(env.requests.length, 1);
    const hit = env.requests[0];
    assert.equal(hit.url, `https://api.direct.yandex.com/json/v501${c.route}`);
    assert.equal(hit.options.method, 'POST');
    const body = JSON.parse(hit.options.body);
    assert.equal(body.method, 'get');
    assert.deepEqual(body.params.FieldNames, c.expectedFields);
    assert.equal(body.params.Page.Limit, 7);
    assert.equal(body.params.Page.Offset, 2);
    c.verify(out.report_envelope.result);
    assert.equal(JSON.stringify(out.report_envelope).includes('private-login'), false);
    if (c.command.method === 'listKeywords') {
      const requestText = JSON.stringify(body);
      for (const forbidden of ['Productivity','StatisticsSearch','StatisticsNetwork']) assert.equal(requestText.includes(forbidden), false);
    }
  });
}

test('official D-11 report request is exact online-only trusted shape', async () => {
  const env = directEnv();
  capture(env, async () => response(200, 'Date\tCampaignId\tCampaignName\tImpressions\tClicks\tCost\n2026-08-01\t11\tCampaign\t100\t4\t123456\n', { RequestId:'report-req', Units:'3/7/10' }));
  const out = plain(await env.ctx.YMBPhase5Runtime.executeDirectCommand({ method:'getCampaignPerformance', dateFrom:'2026-08-01', dateTo:'2026-08-01', campaignIds:[11], limit:10 }));
  assert.equal(env.requests.length, 1);
  const hit = env.requests[0];
  assert.equal(hit.url, 'https://api.direct.yandex.com/json/v501/reports');
  assert.equal(hit.options.headers.processingMode, 'online');
  assert.equal(hit.options.headers.skipReportHeader, 'true');
  assert.equal(hit.options.headers.skipReportSummary, 'true');
  assert.equal(Object.hasOwn(hit.options.headers, 'returnMoneyInMicros'), false);
  assert.equal(Object.hasOwn(hit.options.headers, 'skipColumnHeader'), false);
  const body = JSON.parse(hit.options.body);
  assert.equal(body.params.ReportType, 'CAMPAIGN_PERFORMANCE_REPORT');
  assert.equal(body.params.DateRangeType, 'CUSTOM_DATE');
  assert.equal(body.params.Format, 'TSV');
  assert.equal(body.params.IncludeVAT, 'YES');
  assert.deepEqual(body.params.FieldNames, ['Date','CampaignId','CampaignName','Impressions','Clicks','Cost']);
  assert.deepEqual(body.params.SelectionCriteria, { DateFrom:'2026-08-01', DateTo:'2026-08-01', Filter:[{ Field:'CampaignId', Operator:'IN', Values:['11'] }] });
  assert.equal(out.report_envelope.result.rows[0].cost_micros, 123456);
});

test('official D-12 HTTP 201/202 are terminal and offline/custom report controls are locally impossible', async () => {
  for (const status of [201, 202]) {
    const env = directEnv();
    capture(env, async () => response(status, '', { RequestId:`async-${status}`, Units:'1/9/10' }));
    const out = plain(await env.ctx.YMBPhase5Runtime.executeDirectCommand({ method:'getCampaignPerformance', dateFrom:'2026-08-01', dateTo:'2026-08-01' }));
    assert.equal(env.requests.length, 1);
    assert.equal(out.ok, false);
    assert.equal(out.report_envelope.reason, 'REPORT_ASYNC_NOT_ALLOWED');
    assert.equal(out.report_envelope.request_executed, true);
    assert.equal(out.report_envelope.automatic_retry, false);
  }
  const { ctx } = directEnv();
  for (const command of [
    { method:'getCampaignPerformance', dateFrom:'2026-08-01', dateTo:'2026-08-01', processingMode:'offline' },
    { method:'getCampaignPerformance', dateFrom:'2026-08-01', dateTo:'2026-08-01', processingMode:'auto' },
    { method:'getCampaignPerformance', dateFrom:'2026-08-01', dateTo:'2026-08-01', ReportType:'SEARCH_QUERY_PERFORMANCE_REPORT' },
    { method:'getCampaignPerformance', dateFrom:'2026-08-01', dateTo:'2026-08-01', FieldNames:['Cost'] }
  ]) localReject(ctx.DirectProtocol, command, 'UNSUPPORTED_FIELD');
});

test('official D-13 semantic/server/malformed responses never become OK', async () => {
  for (const code of [53,54,55,58,152,506,513,1002,3000,4000,4001,4002,8000]) {
    const env = directEnv();
    capture(env, async () => response(200, { error:{ error_code:code, error_string:'controlled', request_id:`semantic-${code}` } }, { Units:'1/9/10' }));
    const out = plain(await env.ctx.YMBPhase5Runtime.executeDirectCommand({ method:'listCampaigns', limit:1 }));
    assert.equal(out.ok, false, `code ${code}`);
    assert.equal(out.report_envelope.status, 'ERROR', `code ${code}`);
    assert.equal(out.report_envelope.reason, `DIRECT_${code}`, `code ${code}`);
    assert.equal(out.report_envelope.request_executed, true);
    assert.equal(out.report_envelope.automatic_retry, false);
    assert.equal(env.requests.length, 1);
  }
  {
    const env = directEnv();
    capture(env, async () => response(500, 'server failure', { RequestId:'server-500' }));
    const out = plain(await env.ctx.YMBPhase5Runtime.executeDirectCommand({ method:'listCampaigns', limit:1 }));
    assert.equal(out.ok, false);
    assert.equal(out.report_envelope.status, 'ERROR');
    assert.equal(out.report_envelope.request_executed, true);
  }
  {
    const env = directEnv();
    capture(env, async () => response(200, '{malformed-json', { RequestId:'malformed' }));
    await assert.rejects(() => env.ctx.YMBPhase5Runtime.executeDirectCommand({ method:'listCampaigns', limit:1 }), (error) => {
      assert.equal(error.code, 'INVALID_DIRECT_RESPONSE');
      assert.equal(error.request_executed, true);
      assert.equal(error.automatic_retry, false);
      return true;
    });
    assert.equal(env.requests.length, 1);
  }
});

test('official D-14 unknown transport outcome is UNKNOWN/no-retry for JSON and Reports', async () => {
  for (const command of [
    { method:'listCampaigns', limit:1 },
    { method:'getCampaignPerformance', dateFrom:'2026-08-01', dateTo:'2026-08-01', limit:1 }
  ]) {
    const env = directEnv();
    env.ctx.fetch = async (url, options = {}) => { env.requests.push({ url:String(url), options:structuredClone(options) }); throw new Error('controlled socket reset'); };
    await assert.rejects(() => env.ctx.YMBPhase5Runtime.executeDirectCommand(command), (error) => {
      assert.equal(error.code, 'REQUEST_OUTCOME_UNKNOWN_NO_RETRY');
      assert.equal(error.request_executed, 'UNKNOWN');
      assert.equal(error.automatic_retry, false);
      return true;
    });
    assert.equal(env.requests.length, 1);
  }
});

test('official D-15 RequestId/Units truth is preserved without fabrication or RUB inference', async () => {
  const P = directEnv().ctx.DirectProtocol;
  assert.deepEqual(plain(P.parseUnitsHeader('9/1/10')), { spent:9, remaining:1, daily_limit:10 });
  assert.equal(P.parseUnitsHeader(''), null);
  assert.equal(P.parseUnitsHeader('9/x/10'), null);
  assert.equal(P.parseUnitsHeader('9/1'), null);

  for (const units of [null, 'broken', '9/1/10']) {
    const env = directEnv();
    const headers = { RequestId:'units-truth', 'Units-Used-Login':'should-not-emit' };
    if (units !== null) headers.Units = units;
    capture(env, async () => response(200, { result:{ Campaigns:[] } }, headers));
    const out = plain(await env.ctx.YMBPhase5Runtime.executeDirectCommand({ method:'listCampaigns', limit:1 }));
    assert.equal(out.report_envelope.provider_request_id, 'units-truth');
    assert.deepEqual(out.report_envelope.provider_units, units === '9/1/10' ? { spent:9, remaining:1, daily_limit:10 } : null);
    assert.equal(JSON.stringify(out.report_envelope).includes('should-not-emit'), false);
    assert.equal(JSON.stringify(out.report_envelope).toLowerCase().includes('rub'), false);
    assert.equal(env.requests.length, 1);
  }
});

test('official D-21 all write/future/mutation surfaces reject locally with zero provider requests', async () => {
  const env = directEnv();
  const methods = [
    'add','update','delete','suspendCampaign','resumeCampaign','archiveCampaign','unarchiveCampaign',
    'moderateAd','suspendAd','resumeAd','archiveAd','unarchiveAd','addKeyword','updateKeyword','deleteKeyword','suspendKeyword','resumeKeyword',
    'setBid','setAuto','setBids','finance','payment','AgencyClients','Feeds','Strategies','SEARCH_QUERY_PERFORMANCE_REPORT'
  ];
  for (const method of methods) {
    await assert.rejects(() => env.ctx.YMBPhase5Runtime.executeDirectCommand({ method }), (error) => {
      assert.equal(error.code, 'UNSUPPORTED_METHOD');
      assert.equal(error.request_executed, false);
      return true;
    });
  }
  for (const [field, value] of [['Payment-Token','x'],['Use-Operator-Units','true'],['url','https://evil.invalid'],['headers',{}],['SelectionCriteria',{}],['FieldNames',['Id']],['processingMode','offline']]) {
    await assert.rejects(() => env.ctx.YMBPhase5Runtime.executeDirectCommand({ method:'listCampaigns', [field]:value }), (error) => {
      assert.equal(error.code, 'UNSUPPORTED_FIELD');
      assert.equal(error.request_executed, false);
      return true;
    });
  }
  assert.equal(env.requests.length, 0);
});
