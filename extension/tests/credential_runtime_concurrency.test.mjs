import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');
const clone = (value) => value == null ? value : JSON.parse(JSON.stringify(value));

function deferred() {
  let resolve;
  const promise = new Promise((r) => { resolve = r; });
  return { promise, resolve };
}

function runtimeWithStorage(storage) {
  const ctx = {
    console, JSON, Object, Array, Set, String, Number, Boolean, RegExp, Date, Error, Promise, structuredClone,
    chrome: { storage: { local: storage } }, globalThis: null
  };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(src, 'shared/credential_store_model.js'), 'utf8'), ctx, { filename: 'credential_store_model.js' });
  vm.runInContext(fs.readFileSync(path.join(src, 'shared/credential_runtime.js'), 'utf8'), ctx, { filename: 'credential_runtime.js' });
  return ctx.YMBCredentialRuntime;
}

test('stale migration cannot erase a concurrent Direct credential save', async () => {
  const state = { wsmb_api_key: '', wsmb_folder_id: '', ymb_settings_schema_version: 0 };
  const firstSetStarted = deferred();
  const releaseFirstSet = deferred();
  let setCalls = 0;
  const storage = {
    async get(keys) {
      const snapshot = clone(state);
      if (Array.isArray(keys)) return Object.fromEntries(keys.filter((key) => snapshot[key] !== undefined).map((key) => [key, snapshot[key]]));
      return snapshot;
    },
    async set(values) {
      setCalls += 1;
      if (setCalls === 1) { firstSetStarted.resolve(); await releaseFirstSet.promise; }
      Object.assign(state, clone(values));
    }
  };
  const runtime = runtimeWithStorage(storage);
  const startupLoad = runtime.load();
  await firstSetStarted.promise;
  const savePromise = runtime.save('direct', { oauth_token: 'controlled-direct-token', client_login: 'controlled-client', check_state: 'NOT_CHECKED' });
  // The save is intentionally queued behind the migration mutation now.
  releaseFirstSet.resolve();
  await startupLoad;
  await savePromise;
  const final = await runtime.load({ persistMigration: false });
  assert.equal(final.direct.oauth_token, 'controlled-direct-token');
  assert.equal(final.direct.client_login, 'controlled-client');
});

test('concurrent Direct and Metrika saves preserve both independent records', async () => {
  const state = {
    ymb_service_credentials: {
      wordstat: { api_key: '', folder_id: '', checked_at: null, check_state: '' },
      search: { api_key: '', folder_id: '', checked_at: null, check_state: '' },
      webmaster: { oauth_token: '', user_id: '', verified_at: null, check_state: '' },
      metrika: { oauth_token: '', checked_at: null, check_state: '' },
      direct: { oauth_token: '', client_login: '', checked_at: null, check_state: '' }
    },
    ymb_settings_schema_version: 5
  };
  const storage = {
    async get(keys) {
      const snapshot = clone(state);
      if (Array.isArray(keys)) return Object.fromEntries(keys.filter((key) => snapshot[key] !== undefined).map((key) => [key, snapshot[key]]));
      return snapshot;
    },
    async set(values) { await new Promise((resolve) => setTimeout(resolve, 1)); Object.assign(state, clone(values)); }
  };
  const runtime = runtimeWithStorage(storage);
  await Promise.all([
    runtime.save('direct', { oauth_token: 'direct-A', client_login: 'direct-client' }),
    runtime.save('metrika', { oauth_token: 'metrika-B' })
  ]);
  const final = await runtime.load({ persistMigration: false });
  assert.equal(final.direct.oauth_token, 'direct-A');
  assert.equal(final.direct.client_login, 'direct-client');
  assert.equal(final.metrika.oauth_token, 'metrika-B');
});

test('backup runtime participates in the same credential mutation lock', () => {
  const credentialRuntime = fs.readFileSync(path.join(src, 'shared/credential_runtime.js'), 'utf8');
  const backupRuntime = fs.readFileSync(path.join(src, 'shared/settings_backup_v3_runtime.js'), 'utf8');
  assert.match(credentialRuntime, /withExclusiveMutation/);
  assert.match(backupRuntime, /CredentialRuntime\.withExclusiveMutation/);
});
