import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { webcrypto } from 'node:crypto';
import { performance } from 'node:perf_hooks';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const workerSource = fs.readFileSync(path.join(root, 'service_worker.js'), 'utf8');
const FN_NAMES = [...workerSource.matchAll(/^(?:async )?function\s+([A-Za-z0-9_]+)/gm)].map((m) => m[1]);

function clone(value) { return value === undefined ? undefined : structuredClone(value); }
function plain(value) { return value === undefined ? undefined : JSON.parse(JSON.stringify(value)); }
function harness(initial = {}) {
  const store = clone(initial);
  const storage = {
    async get(keys) {
      if (keys == null) return clone(store);
      if (typeof keys === 'string') return Object.hasOwn(store, keys) ? { [keys]: clone(store[keys]) } : {};
      if (Array.isArray(keys)) { const out = {}; for (const key of keys) if (Object.hasOwn(store, key)) out[key] = clone(store[key]); return out; }
      const out = clone(keys || {}); for (const key of Object.keys(keys || {})) if (Object.hasOwn(store, key)) out[key] = clone(store[key]); return out;
    },
    async set(values) { Object.assign(store, clone(values)); },
    async remove(keys) { for (const key of (Array.isArray(keys) ? keys : [keys])) delete store[key]; }
  };
  let listener = null;
  const chrome = {
    storage: { local: storage },
    runtime: { id: 'test', lastError: null, onMessage: { addListener(fn) { listener = fn; } } },
    tabs: { sendMessage(_id, _message, cb) { cb({ ok: true }); } }
  };
  const ctx = vm.createContext({
    console, chrome, crypto: webcrypto, TextEncoder, TextDecoder, AbortController, performance,
    setTimeout, clearTimeout, URL, structuredClone, Response, Request, Headers, ReadableStream, Buffer,
    fetch: async () => new Response('{}', { status: 200 }), importScripts: () => {}
  });
  ctx.globalThis = ctx;
  for (const file of [
    'shared/product.js','shared/conversation_identity.js','shared/manual_controls.js','shared/service_registry.js',
    'shared/block_command_discovery.js','shared/run_context_model.js','shared/credential_registry.js','shared/policy_model.js',
    'shared/cost_ledger_model.js','shared/wordstat_protocol.js','shared/search_xml.js','shared/search_protocol.js','shared/autorun_model.js'
  ]) vm.runInContext(fs.readFileSync(path.join(root, file), 'utf8'), ctx, { filename: file });
  vm.runInContext(workerSource, ctx, { filename: 'service_worker.js' });
  assert.equal(typeof listener, 'function');
  vm.runInContext(`globalThis.__PROFILE_API=Object.freeze({${FN_NAMES.join(',')}});`, ctx);
  return { api: ctx.__PROFILE_API, store };
}

const sendProfile = { selector: 'button[data-testid="send-button"]', tag: 'button', source: 'picker' };
const copyProfiles = { chatgpt: [{ selector: 'button[data-testid="copy-turn-action-button"]', tag: 'button' }] };

test('legacy Send/Copy profiles remain visible in public state and settings export', async () => {
  const h = harness({ wsmb_send_button_profile: sendProfile, wsmb_copy_button_profiles: copyProfiles });
  const state = await h.api.commonPublicSettingsFields();
  assert.deepEqual(plain(state.send_button_profile), sendProfile);
  assert.deepEqual(plain(state.copy_button_profiles), copyProfiles);
  const backup = await h.api.exportSettingsBackup();
  assert.deepEqual(plain(backup.settings.send_button_profile), sendProfile);
  assert.deepEqual(plain(backup.settings.copy_button_profiles), copyProfiles);
});

test('settings import restores legacy Send/Copy profiles together with current settings', async () => {
  const h = harness({ wsmb_api_key: 'old-key' });
  const backup = await h.api.exportSettingsBackup();
  backup.settings.wordstat.api_key = 'new-key';
  backup.settings.send_button_profile = sendProfile;
  backup.settings.copy_button_profiles = copyProfiles;
  await h.api.importSettingsBackup(backup);
  assert.equal(h.store.wsmb_api_key, 'new-key');
  assert.deepEqual(h.store.wsmb_send_button_profile, sendProfile);
  assert.deepEqual(h.store.wsmb_copy_button_profiles, copyProfiles);
});

test('clearing Send profile does not erase Copy profiles and clearing Copy does not touch other settings', async () => {
  const h = harness({
    wsmb_api_key: 'keep-key',
    wsmb_send_button_profile: sendProfile,
    wsmb_copy_button_profiles: copyProfiles
  });
  await h.api.clearSendButtonProfile();
  assert.equal(Object.hasOwn(h.store, 'wsmb_send_button_profile'), false);
  assert.deepEqual(h.store.wsmb_copy_button_profiles, copyProfiles);
  await h.api.clearCopyButtonProfiles();
  assert.equal(Object.hasOwn(h.store, 'wsmb_copy_button_profiles'), false);
  assert.equal(h.store.wsmb_api_key, 'keep-key');
});

test('old export/import message names remain compatible with restored worker', async () => {
  const h = harness({ wsmb_send_button_profile: sendProfile, wsmb_copy_button_profiles: copyProfiles });
  const exported = await h.api.handleMessage({ type: 'WS_EXPORT_SETTINGS' }, {});
  assert.equal(exported.ok, true);
  assert.deepEqual(plain(exported.backup.settings.send_button_profile), sendProfile);
  exported.backup.settings.copy_button_profiles = { restored: [{ selector: '#copy' }] };
  const imported = await h.api.handleMessage({ type: 'WS_IMPORT_SETTINGS', backup: exported.backup }, {});
  assert.equal(imported.ok, true);
  assert.deepEqual(h.store.wsmb_copy_button_profiles, { restored: [{ selector: '#copy' }] });
});
