import test from 'node:test';
import assert from 'node:assert/strict';
import { createPhase5Runtime, response } from './helpers/phase5_runtime_harness.mjs';

const plain = (value) => JSON.parse(JSON.stringify(value));

function envWithAllCredentials() {
  return createPhase5Runtime({
    ymb_service_credentials: {
      wordstat: { api_key: 'word-key', folder_id: 'word-folder', check_state: 'PRESENT' },
      search: { api_key: 'search-key', folder_id: 'search-folder', check_state: 'PRESENT' },
      webmaster: { oauth_token: 'webmaster-oauth', user_id: '42', verified_at: '2026-08-26T00:00:00.000Z', check_state: 'PRESENT' },
      metrika: { oauth_token: 'metrika-oauth', checked_at: '2026-08-26T00:00:00.000Z', check_state: 'PRESENT' },
      direct: { oauth_token: 'direct-oauth', client_login: 'direct-client', checked_at: '2026-08-26T00:00:00.000Z', check_state: 'PRESENT' }
    }
  });
}

test('D-21 Phase 5 keeps Webmaster Check and listHosts on the accepted Phase 3 routes', async () => {
  const env = envWithAllCredentials();
  env.ctx.fetch = async (url, options = {}) => {
    env.requests.push({ url: String(url), options: structuredClone(options) });
    if (String(url) === 'https://api.webmaster.yandex.net/v4/user') return response(200, { user_id: 42 });
    if (String(url) === 'https://api.webmaster.yandex.net/v4/user/42/hosts') return response(200, { hosts: [] });
    throw new Error(`unexpected route: ${url}`);
  };

  const checked = plain(await env.ctx.YMBPhase5ProviderRuntime.checkWebmaster());
  assert.equal(checked.ok, true);
  assert.equal(checked.user_id, '42');
  assert.equal(env.requests.length, 1);
  assert.equal(env.requests[0].options.method, 'GET');
  assert.equal(env.requests[0].options.headers.Authorization, 'OAuth webmaster-oauth');

  const listed = plain(await env.ctx.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'listHosts' }));
  assert.equal(listed.ok, true);
  assert.deepEqual(listed.report_envelope.result, { hosts: [] });
  assert.equal(listed.report_text.startsWith('WEBMASTER_RESULT_V1\n'), true);
  assert.equal(env.requests.length, 2);
  assert.equal(env.requests[1].url, 'https://api.webmaster.yandex.net/v4/user/42/hosts');
  assert.equal(env.requests[1].options.method, 'GET');
  assert.equal(env.requests[1].options.headers.Authorization, 'OAuth webmaster-oauth');

  const credentials = env.storage.state.ymb_service_credentials;
  assert.equal(credentials.metrika.oauth_token, 'metrika-oauth');
  assert.equal(credentials.direct.oauth_token, 'direct-oauth');
  assert.equal(credentials.direct.client_login, 'direct-client');
});

test('D-21 Phase 5 keeps Metrika Check and listCounters on the accepted Phase 4 routes', async () => {
  const env = envWithAllCredentials();
  env.ctx.fetch = async (url, options = {}) => {
    env.requests.push({ url: String(url), options: structuredClone(options) });
    if (String(url) === 'https://api-metrika.yandex.net/management/v1/counters?per_page=1') return response(200, { rows: 0, counters: [] });
    if (String(url).startsWith('https://api-metrika.yandex.net/management/v1/counters?')) {
      return response(200, { rows: 1, counters: [{ id: 123, name: 'Compat counter', site: 'compat.invalid', status: 'Active', permission: 'own', owner_login: 'owner', favorite: false, private: 'drop' }] });
    }
    throw new Error(`unexpected route: ${url}`);
  };

  const checked = plain(await env.ctx.YMBPhase5ProviderRuntime.checkMetrika());
  assert.equal(checked.ok, true);
  assert.equal(checked.counters_seen, 0);
  assert.equal(env.requests.length, 1);
  assert.equal(env.requests[0].options.method, 'GET');
  assert.equal(env.requests[0].options.headers.Authorization, 'OAuth metrika-oauth');

  const listed = plain(await env.ctx.YMBPhase5ProviderRuntime.executeMetrika({ method: 'listCounters', page: 1, perPage: 10 }));
  assert.equal(listed.ok, true);
  assert.equal(listed.report_text.startsWith('METRIKA_RESULT_V1\n'), true);
  assert.equal(listed.report_envelope.result.rows, 1);
  assert.equal(listed.report_envelope.result.counters[0].id, 123);
  assert.equal(Object.hasOwn(listed.report_envelope.result.counters[0], 'private'), false);
  assert.equal(env.requests.length, 2);
  assert.equal(env.requests[1].url, 'https://api-metrika.yandex.net/management/v1/counters?offset=1&per_page=10');
  assert.equal(env.requests[1].options.method, 'GET');
  assert.equal(env.requests[1].options.headers.Authorization, 'OAuth metrika-oauth');

  const credentials = env.storage.state.ymb_service_credentials;
  assert.equal(credentials.webmaster.oauth_token, 'webmaster-oauth');
  assert.equal(credentials.webmaster.user_id, '42');
  assert.equal(credentials.direct.oauth_token, 'direct-oauth');
  assert.equal(credentials.direct.client_login, 'direct-client');
});

test('D-21 Direct saves and policy changes cannot mutate prior-service credentials or policies', async () => {
  const env = envWithAllCredentials();
  env.storage.state.ymb_webmaster_policy = { manual_enabled: false, max_requests_per_run: 17 };
  env.storage.state.ymb_metrika_policy = { manual_enabled: false, max_requests_per_run: 19, max_report_days: 90 };
  const credentialsBefore = structuredClone(env.storage.state.ymb_service_credentials);
  const webmasterPolicyBefore = structuredClone(env.storage.state.ymb_webmaster_policy);
  const metrikaPolicyBefore = structuredClone(env.storage.state.ymb_metrika_policy);

  await env.ctx.YMBPhase5Runtime.saveServiceCredential('direct', { oauth_token: 'new-direct-oauth', client_login: 'new-direct-client' });
  await env.ctx.YMBPhase5Runtime.saveDirectPolicy({ manual_enabled: false, max_requests_per_run: 3, max_page_size: 300, max_report_days: 7, max_report_rows: 200 });

  const after = env.storage.state.ymb_service_credentials;
  assert.deepEqual(after.wordstat, credentialsBefore.wordstat);
  assert.deepEqual(after.search, credentialsBefore.search);
  assert.deepEqual(after.webmaster, credentialsBefore.webmaster);
  assert.deepEqual(after.metrika, credentialsBefore.metrika);
  assert.equal(after.direct.oauth_token, 'new-direct-oauth');
  assert.equal(after.direct.client_login, 'new-direct-client');
  assert.deepEqual(env.storage.state.ymb_webmaster_policy, webmasterPolicyBefore);
  assert.deepEqual(env.storage.state.ymb_metrika_policy, metrikaPolicyBefore);
});
