import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const ctx = { console, Date, globalThis: null };
ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(here, '../src/shared/credential_store_model.js'), 'utf8'), ctx, { filename: 'credential_store_model.js' });
const M = ctx.YMBCredentialStoreModel;
const plain = (value) => JSON.parse(JSON.stringify(value));

test('schema-v3 identities are stable', () => {
  assert.equal(M.STORAGE_KEY, 'ymb_service_credentials');
  assert.equal(M.SETTINGS_SCHEMA_VERSION, 3);
  assert.equal(M.BACKUP_VERSION, 3);
  assert.deepEqual([...M.SERVICES], ['wordstat', 'search', 'webmaster']);
});

test('legacy shared Cloud credential seeds Wordstat and Search only', () => {
  const c = plain(M.normalizeCredentials({}, { legacyApiKey: ' legacy-key ', legacyFolderId: ' folder-1 ' }));
  assert.equal(c.wordstat.api_key, 'legacy-key');
  assert.equal(c.wordstat.folder_id, 'folder-1');
  assert.equal(c.search.api_key, 'legacy-key');
  assert.equal(c.search.folder_id, 'folder-1');
  assert.equal(c.webmaster.oauth_token, '');
  assert.equal(c.webmaster.user_id, '');
});

test('dedicated records take precedence and may diverge', () => {
  const c = plain(M.normalizeCredentials({
    wordstat: { api_key: 'w', folder_id: 'wf' },
    search: { api_key: 's', folder_id: 'sf' },
    webmaster: { oauth_token: 'wm', user_id: '123' }
  }, { legacyApiKey: 'legacy', legacyFolderId: 'legacy-folder' }));
  assert.equal(c.wordstat.api_key, 'w');
  assert.equal(c.search.api_key, 's');
  assert.equal(c.webmaster.oauth_token, 'wm');
  assert.equal(c.webmaster.user_id, '123');
});

test('migration is idempotent and keeps compatibility seed out of Webmaster', () => {
  const first = M.migrateStorageRecord({}, 'k', 'f');
  assert.equal(first.changed, true);
  const second = M.migrateStorageRecord(plain(first.credentials), 'other', 'other-folder');
  assert.equal(second.changed, false);
  assert.equal(second.credentials.wordstat.api_key, 'k');
  assert.equal(second.credentials.search.api_key, 'k');
  assert.equal(second.credentials.webmaster.oauth_token, '');
});

test('V2 backup migrates shared Wordstat credential into dedicated Wordstat/Search', () => {
  const c = plain(M.normalizeBackupCredentials({ wordstat: { api_key: 'v2-key', folder_id: 'v2-folder' } }, 2));
  assert.equal(c.wordstat.api_key, 'v2-key');
  assert.equal(c.search.api_key, 'v2-key');
  assert.equal(c.webmaster.oauth_token, '');
});

test('V3 backup preserves exact service mapping', () => {
  const c = plain(M.normalizeBackupCredentials({ credentials: {
    wordstat: { api_key: 'w', folder_id: 'wf' },
    search: { api_key: 's', folder_id: 'sf' },
    webmaster: { oauth_token: 'oauth', user_id: '777', verified_at: '2026-08-26T00:00:00Z', check_state: 'PRESENT' }
  } }, 3));
  assert.equal(c.wordstat.api_key, 'w');
  assert.equal(c.search.api_key, 's');
  assert.equal(c.webmaster.oauth_token, 'oauth');
  assert.equal(c.webmaster.user_id, '777');
  assert.equal(c.webmaster.check_state, 'PRESENT');
});

test('invalid Webmaster user id is cleared fail-closed', () => {
  const c = M.normalizeWebmasterRecord({ oauth_token: 'oauth', user_id: 'not-number', check_state: 'PRESENT' });
  assert.equal(c.oauth_token, 'oauth');
  assert.equal(c.user_id, '');
});

test('public status exposes no secrets', () => {
  const status = plain(M.publicCredentialStatus({
    wordstat: { api_key: 'word-secret', folder_id: 'wf' },
    search: { api_key: 'search-secret', folder_id: 'sf' },
    webmaster: { oauth_token: 'oauth-secret', user_id: '42', verified_at: '2026-08-26T00:00:00Z', check_state: 'PRESENT' }
  }));
  const json = JSON.stringify(status);
  assert.equal(json.includes('word-secret'), false);
  assert.equal(json.includes('search-secret'), false);
  assert.equal(json.includes('oauth-secret'), false);
  assert.equal(status.webmaster.user_id, '42');
  assert.equal(status.webmaster.has_oauth_token, true);
});

test('withServiceCredential changes one service only', () => {
  const base = {
    wordstat: { api_key: 'w', folder_id: 'wf' },
    search: { api_key: 's', folder_id: 'sf' },
    webmaster: { oauth_token: 'wm', user_id: '1' }
  };
  const next = plain(M.withServiceCredential(base, 'search', { api_key: 's2', folder_id: 'sf2' }));
  assert.equal(next.wordstat.api_key, 'w');
  assert.equal(next.search.api_key, 's2');
  assert.equal(next.webmaster.oauth_token, 'wm');
  assert.throws(() => M.withServiceCredential(base, 'metrika', {}), (e) => e?.code === 'UNKNOWN_SERVICE');
});
