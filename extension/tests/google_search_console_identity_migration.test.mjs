import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { TextEncoder } from 'node:util';
import { webcrypto } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');
const read = (relative) => fs.readFileSync(path.join(src, relative), 'utf8');
const plain = (value) => JSON.parse(JSON.stringify(value));
const clone = (value) => value === undefined ? undefined : plain(value);

function createHarness() {
  const storage = Object.create(null);
  const runtime = { id: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' };
  const local = {
    async get(keys) {
      if (keys == null) return plain(storage);
      if (typeof keys === 'string') return { [keys]: clone(storage[keys]) };
      const list = Array.isArray(keys) ? keys : Object.keys(keys || {});
      return Object.fromEntries(list.map((key) => [key, clone(storage[key])]));
    },
    async set(values) {
      for (const [key, value] of Object.entries(values || {})) storage[key] = clone(value);
    }
  };
  const ctx = {
    console, JSON, Object, Array, Set, String, Number, Boolean, RegExp, Date, Error, Math,
    TextEncoder, crypto: webcrypto,
    chrome: { runtime, storage: { local } },
    globalThis: null
  };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  for (const file of [
    'shared/credential_store_model.js',
    'shared/credential_runtime.js',
    'shared/policy_model.js',
    'shared/settings_backup_v3_runtime.js'
  ]) vm.runInContext(read(file), ctx, { filename: file });
  return { ctx, storage, runtime };
}

function seedOldInstallation(storage) {
  storage.ymb_service_credentials = {
    wordstat: { api_key: 'fake-wordstat-key', folder_id: 'folder-wordstat', checked_at: '2026-08-27T10:00:00.000Z', check_state: 'PRESENT' },
    search: { api_key: 'fake-search-key', folder_id: 'folder-search', checked_at: '2026-08-27T10:01:00.000Z', check_state: 'PRESENT' },
    webmaster: { oauth_token: 'fake-webmaster-token', user_id: '12345', verified_at: '2026-08-27T10:02:00.000Z', check_state: 'PRESENT' },
    metrika: { oauth_token: 'fake-metrika-token', checked_at: '2026-08-27T10:03:00.000Z', check_state: 'PRESENT' },
    direct: { oauth_token: 'fake-direct-token', client_login: 'fake-client', checked_at: '2026-08-27T10:04:00.000Z', check_state: 'PRESENT' }
  };
  storage.wsmb_api_key = 'fake-wordstat-key';
  storage.wsmb_folder_id = 'folder-wordstat';
  storage.wsmb_auto_send = true;
  storage.wsmb_conversation_bindings = { 'https://chatgpt.com/c/example': { conversation_key: 'example', bound_at: '2026-08-27T10:05:00.000Z' } };
  storage.wsmb_manual_modes = { example: true };
  storage.wsmb_report_prefixes = { example: 'YMB' };
  storage.wsmb_auto_start_prompts = { example: 'continue' };
  storage.ymb_service_contexts = { example: { service: 'search' } };
  storage.ymb_wordstat_policy = { autorun_enabled: false, manual_enabled: true, allowed_methods: ['getTop'], max_requests_per_run: 7 };
  storage.ymb_search_policy = { autorun_enabled: false, manual_enabled: true, allowed_methods: ['search'], max_requests_per_run: 8, tariff_checked_at: '2026-08-28' };
  storage.ymb_webmaster_policy = { autorun_enabled: false, manual_enabled: true, allowed_methods: ['listHosts'], max_requests_per_run: 9 };
  storage.ymb_metrika_policy = { autorun_enabled: false, manual_enabled: true, allowed_methods: ['listCounters'], max_requests_per_run: 10 };
  storage.ymb_direct_policy = { autorun_enabled: false, manual_enabled: true, allowed_methods: ['listCampaigns'], max_requests_per_run: 11 };
  storage.ymb_debug_mode = true;
  storage.ymb_settings_schema_version = 5;
}

test('P9-06 preflight: Backup V3 can migrate existing Yandex settings across an intentional extension ID change without carrying Google auth', async () => {
  const { ctx, storage, runtime } = createHarness();
  seedOldInstallation(storage);

  const originalCredentials = plain(storage.ymb_service_credentials);
  const backup = plain(await ctx.YMBSettingsBackupV3Runtime.exportBackup());

  assert.equal(backup.format, 'YMB_SETTINGS_BACKUP');
  assert.equal(backup.backup_version, 3);
  assert.equal(backup.extension_id, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa');
  assert.equal(backup.contains_secrets, true);
  assert.match(backup.settings_sha256, /^[0-9a-f]{64}$/);
  assert.deepEqual(backup.settings.credentials, originalCredentials);
  assert.equal(backup.settings.debug_mode, true);
  assert.equal(backup.settings.manual_modes.example, true);
  assert.equal(backup.settings.service_contexts.example.service, 'search');

  const serialized = JSON.stringify(backup);
  assert.equal(serialized.includes('google_search_console'), false);
  assert.equal(serialized.includes('webmasters.readonly'), false);
  assert.equal(serialized.includes('fake-google-token'), false);

  for (const key of Object.keys(storage)) delete storage[key];
  runtime.id = 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb';

  const imported = plain(await ctx.YMBSettingsBackupV3Runtime.importBackup(backup));
  assert.equal(imported.imported, true);
  assert.equal(imported.backup_version, 3);
  assert.equal(imported.settings_schema_version, 5);
  assert.equal(imported.active_runtime_state_untouched, true);

  assert.deepEqual(plain(storage.ymb_service_credentials), originalCredentials);
  assert.equal(storage.wsmb_api_key, 'fake-wordstat-key');
  assert.equal(storage.wsmb_folder_id, 'folder-wordstat');
  assert.equal(storage.wsmb_manual_modes.example, true);
  assert.equal(storage.ymb_service_contexts.example.service, 'search');
  assert.equal(storage.ymb_debug_mode, true);
  assert.equal(storage.ymb_settings_schema_version, 5);

  const reexport = plain(await ctx.YMBSettingsBackupV3Runtime.exportBackup());
  assert.equal(reexport.extension_id, 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb');
  assert.deepEqual(reexport.settings.credentials, originalCredentials);
  assert.notEqual(reexport.extension_id, backup.extension_id);
  assert.equal(JSON.stringify(reexport).includes('fake-google-token'), false);
});

test('P9-06 preflight: production credential/backup models still have no persistent GSC token field', () => {
  const credentialModel = read('shared/credential_store_model.js');
  const backupRuntime = read('shared/settings_backup_v3_runtime.js');
  const manifest = JSON.parse(read('manifest.json'));

  assert.doesNotMatch(credentialModel, /google_search_console/i);
  assert.doesNotMatch(credentialModel, /webmasters\.readonly/i);
  assert.doesNotMatch(backupRuntime, /google_search_console/i);
  assert.doesNotMatch(backupRuntime, /webmasters\.readonly/i);

  assert.equal(manifest.permissions.includes('identity'), false);
  assert.equal(manifest.host_permissions.some((item) => String(item).includes('googleapis.com')), false);
  assert.equal(Object.hasOwn(manifest, 'oauth2'), false);
  assert.equal(typeof manifest.key, 'string');
  assert.match(manifest.key, /^[A-Za-z0-9+/]+={0,2}$/);
});
