import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../../src');
const clone = (value) => value == null ? value : JSON.parse(JSON.stringify(value));

function deferred() {
  let resolve;
  const promise = new Promise((r) => { resolve = r; });
  return { promise, resolve };
}

test('credential runtime must not let a stale migration write erase a concurrent Direct save', async () => {
  const state = {
    wsmb_api_key: '',
    wsmb_folder_id: '',
    ymb_settings_schema_version: 0
  };
  const firstSetStarted = deferred();
  const releaseFirstSet = deferred();
  let setCalls = 0;

  const storage = {
    async get(keys) {
      const snapshot = clone(state);
      if (typeof keys === 'string') return snapshot[keys] === undefined ? {} : { [keys]: snapshot[keys] };
      if (Array.isArray(keys)) return Object.fromEntries(keys.filter((key) => snapshot[key] !== undefined).map((key) => [key, snapshot[key]]));
      return snapshot;
    },
    async set(values) {
      setCalls += 1;
      if (setCalls === 1) {
        firstSetStarted.resolve();
        await releaseFirstSet.promise;
      }
      Object.assign(state, clone(values));
    }
  };

  const ctx = {
    console,
    JSON,
    Object,
    Array,
    Set,
    String,
    Number,
    Boolean,
    RegExp,
    Date,
    Error,
    Promise,
    structuredClone,
    chrome: { storage: { local: storage } },
    globalThis: null
  };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(src, 'shared/credential_store_model.js'), 'utf8'), ctx, { filename: 'credential_store_model.js' });
  vm.runInContext(fs.readFileSync(path.join(src, 'shared/credential_runtime.js'), 'utf8'), ctx, { filename: 'credential_runtime.js' });

  const staleStartupLoad = ctx.YMBCredentialRuntime.load();
  await firstSetStarted.promise;

  const saved = await ctx.YMBCredentialRuntime.save('direct', {
    oauth_token: 'controlled-direct-token',
    client_login: 'controlled-client',
    check_state: 'NOT_CHECKED'
  });
  assert.equal(saved.oauth_token, 'controlled-direct-token');
  assert.equal(state.ymb_service_credentials.direct.oauth_token, 'controlled-direct-token');

  releaseFirstSet.resolve();
  await staleStartupLoad;

  const final = await ctx.YMBCredentialRuntime.load({ persistMigration: false });
  assert.equal(final.direct.oauth_token, 'controlled-direct-token', 'stale migration write erased the concurrent Direct credential');
  assert.equal(final.direct.client_login, 'controlled-client');
});

test('concurrent saves to two service records must preserve both credentials', async () => {
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
  const firstGetReleased = deferred();
  const bothRead = deferred();
  let reads = 0;
  const snapshots = [];

  const storage = {
    async get(keys) {
      reads += 1;
      const snapshot = clone(state);
      snapshots.push(snapshot);
      if (reads === 2) bothRead.resolve();
      if (reads <= 2) await firstGetReleased.promise;
      if (Array.isArray(keys)) return Object.fromEntries(keys.filter((key) => snapshot[key] !== undefined).map((key) => [key, snapshot[key]]));
      return snapshot;
    },
    async set(values) { Object.assign(state, clone(values)); }
  };

  const ctx = { console, JSON, Object, Array, Set, String, Number, Boolean, RegExp, Date, Error, Promise, structuredClone, chrome: { storage: { local: storage } }, globalThis: null };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(src, 'shared/credential_store_model.js'), 'utf8'), ctx);
  vm.runInContext(fs.readFileSync(path.join(src, 'shared/credential_runtime.js'), 'utf8'), ctx);

  const directSave = ctx.YMBCredentialRuntime.save('direct', { oauth_token: 'direct-A' });
  const metrikaSave = ctx.YMBCredentialRuntime.save('metrika', { oauth_token: 'metrika-B' });
  await bothRead.promise;
  firstGetReleased.resolve();
  await Promise.all([directSave, metrikaSave]);

  const final = await ctx.YMBCredentialRuntime.load({ persistMigration: false });
  assert.equal(final.direct.oauth_token, 'direct-A', 'concurrent Metrika save erased Direct');
  assert.equal(final.metrika.oauth_token, 'metrika-B', 'concurrent Direct save erased Metrika');
});
