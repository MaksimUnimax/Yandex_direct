import test from 'node:test';
import assert from 'node:assert/strict';
import { createPhase3Runtime } from './helpers/phase3_runtime_harness.mjs';

const plain = (value) => JSON.parse(JSON.stringify(value));

test('Phase 3 runtime migrates legacy shared cloud credentials to schema v3', async () => {
  const { ctx, storage } = createPhase3Runtime({ wsmb_api_key: 'legacy-key', wsmb_folder_id: 'legacy-folder' });
  const settings = plain(await ctx.getSettings());
  assert.equal(settings.credentials.wordstat.api_key, 'legacy-key');
  assert.equal(settings.credentials.search.api_key, 'legacy-key');
  assert.equal(settings.credentials.webmaster.oauth_token, '');
  assert.equal(storage.state.ymb_settings_schema_version, 3);
});

test('partial service Save preserves an existing masked secret and resets Check state', async () => {
  const env = createPhase3Runtime({ ymb_service_credentials: {
    wordstat: { api_key: 'word-secret', folder_id: 'old-folder', checked_at: '2026-08-26T00:00:00Z', check_state: 'PRESENT' },
    search: { api_key: 'search-secret', folder_id: 'search-folder' }, webmaster: { oauth_token: 'oauth-secret', user_id: '7', check_state: 'PRESENT' }
  } });
  await env.ctx.YMBPhase3Runtime.saveServiceCredential('wordstat', { folder_id: 'new-folder' });
  assert.equal(env.storage.state.ymb_service_credentials.wordstat.api_key, 'word-secret');
  assert.equal(env.storage.state.ymb_service_credentials.wordstat.folder_id, 'new-folder');
  assert.equal(env.storage.state.ymb_service_credentials.wordstat.check_state, 'NOT_CHECKED');
  assert.equal(env.storage.state.ymb_service_credentials.wordstat.checked_at, null);
});

test('Wordstat and Search provider execution uses separate dedicated credentials', async () => {
  const env = createPhase3Runtime({ wsmb_api_key: 'legacy', wsmb_folder_id: 'legacy-folder' });
  await env.ctx.YMBPhase3Runtime.saveServiceCredential('wordstat', { api_key: 'word-key', folder_id: 'word-folder' });
  await env.ctx.YMBPhase3Runtime.saveServiceCredential('search', { api_key: 'search-key', folder_id: 'search-folder' });
  await env.ctx.YMBPhase3Runtime.executeCloudCommand('wordstat', { method: 'word' });
  await env.ctx.YMBPhase3Runtime.executeCloudCommand('search', { method: 'search' });
  assert.equal(env.requests[0].url, 'https://wordstat.example/word-folder');
  assert.equal(env.requests[0].options.headers.Authorization, 'Api-Key word-key');
  assert.equal(env.requests[1].url, 'https://search.example/search-folder');
  assert.equal(env.requests[1].options.headers.Authorization, 'Api-Key search-key');
});

test('Wordstat Check uses exactly one getRegionsTree request and stores PRESENT', async () => {
  const env = createPhase3Runtime({ ymb_service_credentials: {
    wordstat: { api_key: 'word-key', folder_id: 'word-folder' }, search: { api_key: '', folder_id: '' }, webmaster: { oauth_token: '', user_id: '' }
  } });
  const result = plain(await env.ctx.YMBPhase3Runtime.checkCloudCredential('wordstat'));
  assert.equal(result.ok, true);
  assert.equal(result.state, 'PRESENT');
  assert.equal(env.requests.length, 1);
  assert.equal(env.requests[0].url, 'https://wordstat.example/word-folder');
  assert.equal(env.requests[0].options.headers.Authorization, 'Api-Key word-key');
  assert.equal(env.storage.state.ymb_service_credentials.wordstat.check_state, 'PRESENT');
});

test('Search Check refuses zero-confirmation and executes exactly one request after explicit billable confirmation', async () => {
  const env = createPhase3Runtime({ ymb_service_credentials: {
    wordstat: { api_key: '', folder_id: '' }, search: { api_key: 'search-key', folder_id: 'search-folder' }, webmaster: { oauth_token: '', user_id: '' }
  } });
  await assert.rejects(() => env.ctx.YMBPhase3Runtime.checkCloudCredential('search'), (error) => {
    assert.equal(error.code, 'SEARCH_CHECK_CONFIRM_REQUIRED');
    assert.equal(error.request_executed, false);
    return true;
  });
  assert.equal(env.requests.length, 0);
  const result = plain(await env.ctx.YMBPhase3Runtime.checkCloudCredential('search', { confirmBillable: true }));
  assert.equal(result.ok, true);
  assert.equal(result.billable_request_confirmed, true);
  assert.equal(env.requests.length, 1);
  assert.equal(env.requests[0].url, 'https://search.example/search-folder');
  assert.equal(env.requests[0].options.headers.Authorization, 'Api-Key search-key');
  assert.equal(env.storage.state.ymb_service_credentials.search.check_state, 'PRESENT');
});

test('Webmaster Check performs exactly one GET /v4/user and stores derived user_id', async () => {
  const env = createPhase3Runtime();
  env.ctx.fetch = async (url, options = {}) => { env.requests.push({ url: String(url), options: structuredClone(options) }); return { ok: true, status: 200, text: async () => JSON.stringify({ user_id: 777 }) }; };
  const result = plain(await env.ctx.YMBPhase3Runtime.checkWebmasterCredential('oauth-secret'));
  assert.equal(env.requests.length, 1);
  assert.equal(env.requests[0].url, 'https://api.webmaster.yandex.net/v4/user');
  assert.equal(env.requests[0].options.method, 'GET');
  assert.equal(env.requests[0].options.headers.Authorization, 'OAuth oauth-secret');
  assert.equal(result.user_id, '777');
  assert.equal(env.storage.state.ymb_service_credentials.webmaster.user_id, '777');
  assert.equal(env.storage.state.ymb_service_credentials.webmaster.check_state, 'PRESENT');
});

test('Webmaster listHosts is one read-only request and produces WEBMASTER_RESULT_V1', async () => {
  const env = createPhase3Runtime({ ymb_service_credentials: {
    wordstat: { api_key: '', folder_id: '' }, search: { api_key: '', folder_id: '' },
    webmaster: { oauth_token: 'oauth', user_id: '42', check_state: 'PRESENT' }
  } });
  env.ctx.fetch = async (url, options = {}) => { env.requests.push({ url: String(url), options: structuredClone(options) }); return { ok: true, status: 200, text: async () => JSON.stringify({ hosts: [] }) }; };
  const result = plain(await env.ctx.YMBPhase3Runtime.executeWebmasterCommand({ method: 'listHosts' }));
  assert.equal(env.requests.length, 1);
  assert.equal(env.requests[0].url, 'https://api.webmaster.yandex.net/v4/user/42/hosts');
  assert.equal(env.requests[0].options.method, 'GET');
  assert.equal(result.ok, true);
  assert.match(result.report_text, /^WEBMASTER_RESULT_V1/);
});

test('Webmaster unknown outcome is never auto-retried', async () => {
  const env = createPhase3Runtime({ ymb_service_credentials: {
    wordstat: { api_key: '', folder_id: '' }, search: { api_key: '', folder_id: '' },
    webmaster: { oauth_token: 'oauth', user_id: '42', check_state: 'PRESENT' }
  } });
  env.ctx.fetch = async (url, options = {}) => { env.requests.push({ url: String(url), options: structuredClone(options) }); throw new Error('network down'); };
  await assert.rejects(() => env.ctx.YMBPhase3Runtime.executeWebmasterCommand({ method: 'listHosts' }), (error) => {
    assert.equal(error.code, 'REQUEST_OUTCOME_UNKNOWN_NO_RETRY');
    assert.equal(error.request_executed, 'UNKNOWN');
    assert.equal(error.automatic_retry, false);
    return true;
  });
  assert.equal(env.requests.length, 1);
});

test('v3 backup exports exact mapping and v2 import preserves existing Webmaster credential', async () => {
  const env = createPhase3Runtime({ ymb_service_credentials: {
    wordstat: { api_key: 'w', folder_id: 'wf' }, search: { api_key: 's', folder_id: 'sf' },
    webmaster: { oauth_token: 'oauth-existing', user_id: '9', check_state: 'PRESENT' }
  } });
  const v3 = plain(await env.ctx.YMBPhase3Runtime.exportSettingsBackup());
  assert.equal(v3.backup_version, 3);
  assert.equal(v3.settings.credentials.search.api_key, 's');
  assert.equal(v3.settings.credentials.webmaster.oauth_token, 'oauth-existing');

  const settingsV2 = { wordstat: { api_key: 'old-shared', folder_id: 'old-folder' }, auto_send: true };
  const sum = await env.ctx.YMBSettingsBackupV3Runtime.checksum(settingsV2);
  await env.ctx.YMBPhase3Runtime.importSettingsBackup({ format: 'YMB_SETTINGS_BACKUP', backup_version: 2, settings_schema_version: 2, contains_secrets: true, settings_sha256: sum, settings: settingsV2 });
  assert.equal(env.storage.state.ymb_service_credentials.wordstat.api_key, 'old-shared');
  assert.equal(env.storage.state.ymb_service_credentials.search.api_key, 'old-shared');
  assert.equal(env.storage.state.ymb_service_credentials.webmaster.oauth_token, 'oauth-existing');
});

test('Phase 3 settings import remains blocked during active Autorun before credential mutation', async () => {
  const source = createPhase3Runtime({ ymb_service_credentials: {
    wordstat: { api_key: 'incoming', folder_id: 'incoming-folder' }, search: { api_key: 'incoming-s', folder_id: 'incoming-sf' }, webmaster: { oauth_token: '', user_id: '' }
  } });
  const backup = plain(await source.ctx.YMBPhase3Runtime.exportSettingsBackup());
  const env = createPhase3Runtime({
    ymb_service_credentials: { wordstat: { api_key: 'keep', folder_id: 'keep-folder' }, search: { api_key: 'keep-s', folder_id: 'keep-sf' }, webmaster: { oauth_token: 'keep-oauth', user_id: '7' } },
    wsmb_auto_runs: { 'https://chatgpt.com|11111111-2222-4333-8444-555555555555': { status: 'waiting_command' } }
  });
  await assert.rejects(() => env.ctx.YMBPhase3Runtime.importSettingsBackup(backup), (error) => error?.code === 'IMPORT_ACTIVE_RUN');
  assert.equal(env.storage.state.ymb_service_credentials.wordstat.api_key, 'keep');
  assert.equal(env.storage.state.ymb_service_credentials.webmaster.oauth_token, 'keep-oauth');
});

test('Phase 3 settings import remains blocked during active Manual operation before credential mutation', async () => {
  const source = createPhase3Runtime({ ymb_service_credentials: {
    wordstat: { api_key: 'incoming', folder_id: 'incoming-folder' }, search: { api_key: 'incoming-s', folder_id: 'incoming-sf' }, webmaster: { oauth_token: '', user_id: '' }
  } });
  const backup = plain(await source.ctx.YMBPhase3Runtime.exportSettingsBackup());
  const env = createPhase3Runtime({
    ymb_service_credentials: { wordstat: { api_key: 'keep', folder_id: 'keep-folder' }, search: { api_key: 'keep-s', folder_id: 'keep-sf' }, webmaster: { oauth_token: 'keep-oauth', user_id: '7' } },
    wsmb_manual_operations: { 'https://chatgpt.com|11111111-2222-4333-8444-555555555555': { status: 'requesting' } }
  });
  await assert.rejects(() => env.ctx.YMBPhase3Runtime.importSettingsBackup(backup), (error) => error?.code === 'IMPORT_ACTIVE_MANUAL');
  assert.equal(env.storage.state.ymb_service_credentials.search.api_key, 'keep-s');
  assert.equal(env.storage.state.ymb_service_credentials.webmaster.oauth_token, 'keep-oauth');
});

test('public global state exposes folder/user metadata but no credential secrets', async () => {
  const env = createPhase3Runtime({ ymb_service_credentials: {
    wordstat: { api_key: 'w-secret', folder_id: 'wf' }, search: { api_key: 's-secret', folder_id: 'sf' },
    webmaster: { oauth_token: 'oauth-secret', user_id: '9', check_state: 'PRESENT' }
  } });
  const state = plain(await env.ctx.commonPublicSettingsFields());
  const json = JSON.stringify(state);
  assert.equal(json.includes('w-secret'), false);
  assert.equal(json.includes('s-secret'), false);
  assert.equal(json.includes('oauth-secret'), false);
  assert.equal(state.credential_status.wordstat.folder_id, 'wf');
  assert.equal(state.credential_status.search.folder_id, 'sf');
  assert.equal(state.credential_status.webmaster.user_id, '9');
  assert.equal(state.credential_capabilities.webmaster.state, 'PRESENT');
  assert.equal(state.settings_schema_version, 3);
});
