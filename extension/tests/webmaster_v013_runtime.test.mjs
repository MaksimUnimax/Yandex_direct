import test from 'node:test';
import assert from 'node:assert/strict';
import { createPhase5Runtime, response } from './helpers/phase5_runtime_harness.mjs';

const plain = (value) => JSON.parse(JSON.stringify(value));
const TASK = '12345678-1234-1234-1234-123456789abc';
const DOWNLOAD = `https://storage.mds.yandex.net/get-webmaster-download/${TASK}`;

function initialCredentials(extra = {}) {
  return {
    ymb_service_credentials: {
      wordstat: { api_key: 'word-key', folder_id: 'word-folder', check_state: 'PRESENT' },
      search: { api_key: 'search-key', folder_id: 'search-folder', check_state: 'PRESENT' },
      webmaster: { oauth_token: 'webmaster-oauth', user_id: '42', check_state: 'PRESENT' },
      metrika: { oauth_token: 'metrika-oauth', check_state: 'PRESENT' },
      direct: { oauth_token: 'direct-oauth', client_login: 'direct-client', check_state: 'PRESENT' }
    },
    ...extra
  };
}

test('W13-11 Phase5 delegation reaches expanded Phase3 history and sample GET routes without changing auth semantics', async () => {
  const env = createPhase5Runtime(initialCredentials());
  env.ctx.fetch = async (url, options = {}) => {
    env.requests.push({ url: String(url), options: structuredClone(options) });
    if (String(url).includes('/search-queries/all/history?')) return response(200, { indicators: { TOTAL_SHOWS: [{date:'2026-09-01',value:7}] } });
    if (String(url).includes('/indexing/samples?')) return response(200, { count:1, samples:[{status:'HTTP_2XX',http_code:200,url:'https://example.ru/a',access_date:'2026-09-01'}] });
    if (String(url).includes('/search-urls/in-search/samples?')) return response(200, { count:1, samples:[{url:'https://example.ru/a',last_access:'2026-09-01',title:'A'}] });
    throw new Error(`unexpected route ${url}`);
  };
  const history = plain(await env.ctx.YMBPhase5ProviderRuntime.executeWebmaster({method:'getAllQueryHistory',hostId:'h',queryIndicators:['TOTAL_SHOWS']}));
  assert.equal(history.report_envelope.result.indicators.TOTAL_SHOWS[0].value,7);
  const indexing = plain(await env.ctx.YMBPhase5ProviderRuntime.executeWebmaster({method:'getIndexingSamples',hostId:'h',limit:100}));
  assert.equal(indexing.report_envelope.result.samples[0].access_date,'2026-09-01');
  const inSearch = plain(await env.ctx.YMBPhase5ProviderRuntime.executeWebmaster({method:'getInSearchSamples',hostId:'h',limit:50}));
  assert.equal(inSearch.report_envelope.result.samples[0].title,'A');
  for (const request of env.requests) {
    assert.equal(request.options.method,'GET');
    assert.equal(request.options.headers.Authorization,'OAuth webmaster-oauth');
  }
});

test('W13-12 local projection executes zero network requests and reports physical request_executed=false', async () => {
  const env = createPhase5Runtime(initialCredentials());
  env.ctx.fetch = async () => { throw new Error('local method must not fetch'); };
  const result = plain(await env.ctx.YMBPhase5ProviderRuntime.executeWebmaster({method:'projectQueryUrlExport',hostId:'h',dates:['2026-09-01','2026-09-02'],paths:['/a','/b']}));
  assert.equal(result.report_envelope.request_executed,false);
  assert.equal(result.report_envelope.result.projection.projected_quota_units,4);
  assert.equal(env.requests.length,0);
});

test('W13-13 start POST serializes provider string tariff flag, persists quota/job and never exposes OAuth in result', async () => {
  const env = createPhase5Runtime(initialCredentials());
  env.ctx.fetch = async (url, options = {}) => {
    env.requests.push({ url:String(url), options:structuredClone(options) });
    return response(200, {task_id:TASK,free_quota_used:2,pro_quota_used:0,total_quota_used:2,free_quota_remaining:98,pro_quota_remaining:0});
  };
  const result = plain(await env.ctx.YMBPhase5ProviderRuntime.executeWebmaster({method:'startQueryUrlExport',hostId:'h',dates:['2026-09-01'],paths:['/a','/b'],regionIds:[213],confirmQuota:true}));
  assert.equal(env.requests.length,1);
  const request=env.requests[0];
  assert.equal(request.options.method,'POST');
  assert.equal(request.options.headers.Authorization,'OAuth webmaster-oauth');
  assert.equal(request.options.headers['Content-Type'],'application/json');
  assert.deepEqual(JSON.parse(request.options.body),{dates:['2026-09-01'],paths:['/a','/b'],region_ids:[213],use_pro_tariff:'false'});
  assert.equal(result.report_envelope.request_executed,true);
  assert.equal(result.report_envelope.result.manifest.task_id,TASK);
  assert.equal(result.report_envelope.result.manifest.quota.free_quota_remaining,98);
  assert.equal(JSON.stringify(result).includes('webmaster-oauth'),false);
  assert.equal(env.storage.state.ymb_webmaster_exports_v1[TASK].task_id,TASK);
});

test('W13-14 stateful start network uncertainty is UNKNOWN and automatic retry remains forbidden', async () => {
  const env = createPhase5Runtime(initialCredentials());
  env.ctx.fetch = async () => { throw new TypeError('network dropped'); };
  await assert.rejects(
    () => env.ctx.YMBPhase5ProviderRuntime.executeWebmaster({method:'startQueryUrlExport',hostId:'h',dates:['2026-09-01'],paths:['/a'],confirmQuota:true}),
    (error) => error.code === 'REQUEST_OUTCOME_UNKNOWN_NO_RETRY' && error.request_executed === 'UNKNOWN' && error.automatic_retry === false
  );
  assert.equal(env.storage.state.ymb_webmaster_exports_v1, undefined);
});

test('W13-15 status stores only an allowlisted signed Yandex download URL and strips it from public result', async () => {
  const env = createPhase5Runtime(initialCredentials({
    ymb_webmaster_exports_v1: {
      [TASK]: {task_id:TASK,host_id:'h',created_at:'2026-09-01T00:00:00Z',updated_at:'2026-09-01T00:00:00Z',download_status:'QUEUED',paths:['/a'],dates:['2026-09-01'],region_ids:[],use_pro_tariff:false,raw_storage_key:`ymb_webmaster_export_raw_v1:${TASK}`,rows_storage_key:`ymb_webmaster_export_rows_v1:${TASK}`}
    }
  }));
  env.ctx.fetch = async (url, options = {}) => {
    env.requests.push({url:String(url),options:structuredClone(options)});
    return response(200,{download_status:'SUCCESS',url:DOWNLOAD});
  };
  const result=plain(await env.ctx.YMBPhase5ProviderRuntime.executeWebmaster({method:'getQueryUrlExportStatus',hostId:'h',taskId:TASK}));
  assert.equal(result.report_envelope.result.download_status,'SUCCESS');
  assert.equal(result.report_envelope.result.download_available,true);
  assert.equal(Object.hasOwn(result.report_envelope.result,'url'),false);
  assert.equal(Object.hasOwn(result.report_envelope.result.manifest,'download_url'),false);
  assert.equal(env.storage.state.ymb_webmaster_exports_v1[TASK].download_url,DOWNLOAD);
});

test('W13-16 unsafe status download URL fails after provider execution and cannot enter durable store', async () => {
  const env = createPhase5Runtime(initialCredentials({
    ymb_webmaster_exports_v1: {
      [TASK]: {task_id:TASK,host_id:'h',download_status:'QUEUED',raw_storage_key:`ymb_webmaster_export_raw_v1:${TASK}`,rows_storage_key:`ymb_webmaster_export_rows_v1:${TASK}`}
    }
  }));
  env.ctx.fetch = async () => response(200,{download_status:'SUCCESS',url:`https://evil.example/get-webmaster-download/${TASK}`});
  await assert.rejects(
    () => env.ctx.YMBPhase5ProviderRuntime.executeWebmaster({method:'getQueryUrlExportStatus',hostId:'h',taskId:TASK}),
    (error) => error.code === 'UNSAFE_WEBMASTER_DOWNLOAD_URL' && error.request_executed === true
  );
  assert.notEqual(env.storage.state.ymb_webmaster_exports_v1[TASK].download_url,`https://evil.example/get-webmaster-download/${TASK}`);
});

test('W13-17 durable job survives reconstructed extension runtime; collect downloads without OAuth and chunk is local', async () => {
  const first = createPhase5Runtime(initialCredentials());
  first.ctx.fetch = async (url, options = {}) => {
    first.requests.push({url:String(url),options:structuredClone(options)});
    if (options.method === 'POST') return response(200,{task_id:TASK,free_quota_used:1,pro_quota_used:0,total_quota_used:1,free_quota_remaining:99,pro_quota_remaining:0});
    return response(200,{download_status:'SUCCESS',url:DOWNLOAD});
  };
  await first.ctx.YMBPhase5ProviderRuntime.executeWebmaster({method:'startQueryUrlExport',hostId:'h',dates:['2026-09-01'],paths:['/a'],confirmQuota:true});
  await first.ctx.YMBPhase5ProviderRuntime.executeWebmaster({method:'getQueryUrlExportStatus',hostId:'h',taskId:TASK});

  const restarted = createPhase5Runtime(plain(first.storage.state));
  const manifest = plain(await restarted.ctx.YMBPhase5ProviderRuntime.executeWebmaster({method:'getQueryUrlExportManifest',taskId:TASK}));
  assert.equal(manifest.report_envelope.request_executed,false);
  assert.equal(manifest.report_envelope.result.manifest.download_status,'SUCCESS');
  restarted.ctx.fetch = async (url, options = {}) => {
    restarted.requests.push({url:String(url),options:structuredClone(options)});
    if (String(url) !== DOWNLOAD) throw new Error('wrong download origin');
    return response(200,'date,host,URL,query,region,clicks,impressions,position\n2026-09-01,h,https://x/a,q1,213,1,4,2.1\n2026-09-01,h,https://x/b,q2,213,0,2,5.2\n');
  };
  const collected = plain(await restarted.ctx.YMBPhase5ProviderRuntime.executeWebmaster({method:'collectQueryUrlExport',hostId:'h',taskId:TASK}));
  assert.equal(collected.report_envelope.request_executed,true);
  assert.equal(collected.report_envelope.result.manifest.collection.row_count,2);
  assert.match(collected.report_envelope.result.manifest.collection.raw_sha256,/^[0-9a-f]{64}$/);
  assert.equal(restarted.requests.length,1);
  assert.equal(restarted.requests[0].options.headers.Authorization,undefined);
  assert.equal(restarted.requests[0].options.redirect,'error');
  const beforeNetworkCount=restarted.requests.length;
  const chunk=plain(await restarted.ctx.YMBPhase5ProviderRuntime.executeWebmaster({method:'readQueryUrlExportChunk',taskId:TASK,offset:1,limit:1}));
  assert.equal(chunk.report_envelope.request_executed,false);
  assert.equal(chunk.report_envelope.result.rows[0].query,'q2');
  assert.equal(restarted.requests.length,beforeNetworkCount);
  assert.ok(restarted.storage.state[`ymb_webmaster_export_raw_v1:${TASK}`].includes('q1'));
});

test('W13-18 policy migration expands only the accepted legacy default Webmaster allowlist', () => {
  const env = createPhase5Runtime(initialCredentials());
  const M=env.ctx.YMBPolicyModel;
  const migrated=plain(M.normalizeWebmasterPolicy({allowed_methods:['listHosts','getSummary','getDiagnostics','getPopularQueries'],tariff_checked_at:'2026-08-26'}));
  assert.ok(migrated.allowed_methods.includes('getAllQueryHistory'));
  assert.ok(migrated.allowed_methods.includes('startQueryUrlExport'));
  assert.ok(migrated.allowed_methods.includes('readQueryUrlExportChunk'));
  const explicit=plain(M.normalizeWebmasterPolicy({allowed_methods:['listHosts'],tariff_checked_at:'2026-08-26'}));
  assert.deepEqual(explicit.allowed_methods,['listHosts']);
});
