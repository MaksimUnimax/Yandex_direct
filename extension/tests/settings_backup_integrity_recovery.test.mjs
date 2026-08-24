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
const bootstrapSource = fs.readFileSync(path.join(root, 'service_worker_bootstrap.js'), 'utf8');
const FN_NAMES = [...workerSource.matchAll(/^(?:async )?function\s+([A-Za-z0-9_]+)/gm)].map((m) => m[1]);
function clone(value) { return value === undefined ? undefined : structuredClone(value); }
function canonical(value) {
  if (value === null || typeof value !== 'object') return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map((item) => canonical(item === undefined ? null : item)).join(',')}]`;
  return `{${Object.keys(value).sort().filter((key) => value[key] !== undefined).map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(',')}}`;
}
async function sha256(value) {
  const digest = await webcrypto.subtle.digest('SHA-256', new TextEncoder().encode(canonical(value)));
  return Buffer.from(digest).toString('hex');
}
async function makeBackup(settings, runtimeId = 'source-extension') {
  return {
    format: 'YMB_SETTINGS_BACKUP',
    backup_version: 2,
    settings_schema_version: 2,
    exported_at: '2026-08-20T00:00:00.000Z',
    extension_version: '0.1.1',
    extension_id: runtimeId,
    contains_secrets: true,
    settings_sha256: await sha256(settings),
    settings
  };
}
function harness(initial = {}, runtimeId = 'test-extension') {
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
    storage:{local:storage},
    runtime:{id:runtimeId,lastError:null,onMessage:{addListener(fn){listener=fn;}}},
    tabs:{sendMessage(_id,_message,cb){cb({ok:true});}}
  };
  const ctx=vm.createContext({console,chrome,crypto:webcrypto,TextEncoder,TextDecoder,AbortController,performance,setTimeout,clearTimeout,URL,structuredClone,Response,Request,Headers,ReadableStream,Buffer,fetch:async()=>new Response('{}',{status:200}),importScripts:()=>{}});
  ctx.globalThis=ctx;
  for (const file of ['shared/product.js','shared/conversation_identity.js','shared/manual_controls.js','shared/service_registry.js','shared/block_command_discovery.js','shared/run_context_model.js','shared/credential_registry.js','shared/policy_model.js','shared/cost_ledger_model.js','shared/wordstat_protocol.js','shared/search_xml.js','shared/search_protocol.js','shared/autorun_model.js']) {
    vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),ctx,{filename:file});
  }
  vm.runInContext(workerSource,ctx,{filename:'service_worker.js'});
  assert.equal(typeof listener,'function');
  vm.runInContext(`globalThis.__BACKUP_API=Object.freeze({${FN_NAMES.join(',')}});`,ctx);
  return { api:ctx.__BACKUP_API, store };
}

function bootstrapHarness(initial = {}, runtimeId = 'target-extension') {
  const store = clone(initial);
  const writes = [];
  const imported = [];
  let listener = null;
  const storage = {
    async get(keys) {
      if (keys == null) return clone(store);
      if (typeof keys === 'string') return Object.hasOwn(store, keys) ? { [keys]: clone(store[keys]) } : {};
      if (Array.isArray(keys)) { const out = {}; for (const key of keys) if (Object.hasOwn(store, key)) out[key] = clone(store[key]); return out; }
      const out = clone(keys || {}); for (const key of Object.keys(keys || {})) if (Object.hasOwn(store, key)) out[key] = clone(store[key]); return out;
    },
    async set(values) {
      writes.push(clone(values));
      Object.assign(store, clone(values));
    }
  };
  const chrome = {
    storage: { local: storage },
    runtime: { id: runtimeId, onMessage: { addListener(fn) { listener = fn; } } }
  };
  let ctx;
  ctx = vm.createContext({
    console, chrome, crypto: webcrypto, TextEncoder, structuredClone,
    setTimeout, clearTimeout,
    __YMB_BOOTSTRAP_TEST__: true,
    importScripts(name) {
      imported.push(name);
      assert.equal(name, 'service_worker.js');
      ctx.exportSettingsBackup = async () => {
        const settings = {
          wordstat: {
            api_key: String(store.wsmb_api_key || ''),
            folder_id: String(store.wsmb_folder_id || '')
          },
          auto_send: store.wsmb_auto_send !== false
        };
        return makeBackup(settings, runtimeId);
      };
      ctx.validateSettingsBackupEnvelope = async (backup) => {
        if (!backup || backup.format !== 'YMB_SETTINGS_BACKUP') throw Object.assign(new Error('bad backup'), { code: 'INVALID_BACKUP' });
        if (backup.backup_version !== 2 || backup.settings_schema_version !== 2) throw Object.assign(new Error('bad version'), { code: 'UNSUPPORTED_BACKUP_VERSION' });
        if (backup.settings_sha256 !== await sha256(backup.settings)) throw Object.assign(new Error('bad checksum'), { code: 'BACKUP_CHECKSUM_MISMATCH' });
        return clone(backup.settings);
      };
      ctx.publicGlobalSettingsState = async () => ({ product_version: '0.1.1' });
      ctx.YMBPolicyModel = {
        normalizeWordstatPolicy(value) { return clone(value || {}); },
        normalizeSearchPolicy(value) { return clone(value || {}); }
      };
      ctx.chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
        sendResponse({ ok: true, delegated: true, type: message?.type || null });
        return false;
      });
    }
  });
  ctx.globalThis = ctx;
  vm.runInContext(bootstrapSource, ctx, { filename: 'service_worker_bootstrap.js' });
  async function send(message) {
    assert.equal(typeof listener, 'function');
    return new Promise((resolve, reject) => {
      let settled = false;
      const sendResponse = (value) => { if (!settled) { settled = true; resolve(clone(value)); } };
      try {
        const result = listener(clone(message), {}, sendResponse);
        if (result !== true && !settled) queueMicrotask(() => { if (!settled) reject(new Error('listener did not respond')); });
      } catch (error) { reject(error); }
    });
  }
  return { chrome: ctx.chrome, store, writes, imported, send, testApi: ctx.__YMB_BOOTSTRAP_TEST_API__ };
}

test('settings export is versioned, secret-marked and carries canonical SHA-256 over settings payload', async () => {
  const h = harness({ wsmb_api_key: 'SECRET-KEY-A', wsmb_folder_id: 'folder-a', wsmb_auto_send: false, ymb_debug_mode: true }, 'source-extension');
  const backup = await h.api.exportSettingsBackup();
  assert.equal(backup.format, 'YMB_SETTINGS_BACKUP');
  assert.equal(backup.backup_version, 2);
  assert.equal(backup.settings_schema_version, 2);
  assert.equal(backup.extension_id, 'source-extension');
  assert.equal(backup.contains_secrets, true);
  assert.equal(backup.settings.wordstat.api_key, 'SECRET-KEY-A');
  assert.match(backup.settings_sha256, /^[0-9a-f]{64}$/);
  assert.equal(backup.settings_sha256, await sha256(backup.settings));
});

test('tampered settings backup is rejected before any settings mutation', async () => {
  const source = harness({ wsmb_api_key: 'new-key', wsmb_folder_id: 'new-folder' }, 'source-extension');
  const backup = await source.api.exportSettingsBackup();
  const tampered = clone(backup);
  tampered.settings.wordstat.api_key = 'attacker-key';
  const target = harness({ wsmb_api_key: 'old-key', wsmb_folder_id: 'old-folder' }, 'target-extension');
  await assert.rejects(() => target.api.importSettingsBackup(tampered), (error) => error?.code === 'BACKUP_CHECKSUM_MISMATCH');
  assert.equal(target.store.wsmb_api_key, 'old-key');
  assert.equal(target.store.wsmb_folder_id, 'old-folder');
  assert.equal(Object.hasOwn(target.store, 'ymb_settings_schema_version'), false);
});

test('missing checksum and unsupported backup version are rejected without mutation', async () => {
  const source = harness({ wsmb_api_key: 'new-key' });
  const backup = await source.api.exportSettingsBackup();
  const target = harness({ wsmb_api_key: 'old-key' });
  const missing = clone(backup);
  delete missing.settings_sha256;
  await assert.rejects(() => target.api.importSettingsBackup(missing), (error) => error?.code === 'BACKUP_CHECKSUM_MISSING');
  const unsupported = clone(backup);
  unsupported.backup_version = 999;
  await assert.rejects(() => target.api.importSettingsBackup(unsupported), (error) => error?.code === 'UNSUPPORTED_BACKUP_VERSION');
  assert.equal(target.store.wsmb_api_key, 'old-key');
});

test('intact checksummed backup restores settings across different extension identities', async () => {
  const copies = { restored: [{ selector: '#copy' }] };
  const source = harness({
    wsmb_api_key: 'cross-key', wsmb_folder_id: 'cross-folder', wsmb_auto_send: false,
    ymb_debug_mode: true, wsmb_copy_button_profiles: copies,
    ymb_service_contexts: { 'https://chatgpt.com|abc': { active_service: 'search', updated_at: '2026-08-20T00:00:00.000Z' } }
  }, 'source-extension');
  const backup = await source.api.exportSettingsBackup();
  const target = harness({ wsmb_api_key: 'old-key', wsmb_folder_id: 'old-folder' }, 'target-extension');
  const result = await target.api.importSettingsBackup(backup);
  assert.equal(result.imported, true);
  assert.equal(target.store.wsmb_api_key, 'cross-key');
  assert.equal(target.store.wsmb_folder_id, 'cross-folder');
  assert.equal(target.store.wsmb_auto_send, false);
  assert.equal(target.store.ymb_debug_mode, true);
  assert.deepEqual(target.store.wsmb_copy_button_profiles, copies);
  assert.equal(target.store.ymb_service_contexts['https://chatgpt.com|abc'].active_service, 'search');
});

test('bootstrap stores the old checksummed backup before the import settings mutation', async () => {
  const h = bootstrapHarness({ wsmb_api_key: 'old-key', wsmb_folder_id: 'old-folder', wsmb_auto_send: true });
  assert.deepEqual(h.imported, ['service_worker.js']);
  await h.chrome.storage.local.set({
    wsmb_api_key: 'new-key',
    wsmb_folder_id: 'new-folder',
    ymb_wordstat_policy: {},
    ymb_search_policy: {},
    ymb_settings_schema_version: 2
  });
  assert.equal(h.writes.length, 2);
  const rollback = h.writes[0].ymb_settings_migration_rollback_backup;
  assert.ok(rollback);
  assert.equal(rollback.format, 'YMB_SETTINGS_BACKUP');
  assert.equal(rollback.settings.wordstat.api_key, 'old-key');
  assert.equal(rollback.settings.wordstat.folder_id, 'old-folder');
  assert.equal(rollback.extension_id, 'target-extension');
  assert.equal(rollback.settings_sha256, await sha256(rollback.settings));
  assert.equal(rollback.rollback_context.reason, 'settings_import');
  assert.equal(rollback.rollback_context.incoming_settings_schema_version, 2);
  assert.equal(h.writes[1].wsmb_api_key, 'new-key');
  assert.equal(h.store.wsmb_api_key, 'new-key');
  assert.equal(h.store.ymb_settings_migration_rollback_backup.settings.wordstat.api_key, 'old-key');
});

test('bootstrap does not create a rollback backup for ordinary storage writes', async () => {
  const h = bootstrapHarness({ wsmb_api_key: 'old-key', wsmb_folder_id: 'old-folder' });
  await h.chrome.storage.local.set({ ymb_debug_mode: true });
  assert.equal(h.writes.length, 1);
  assert.equal(h.writes[0].ymb_debug_mode, true);
  assert.equal(Object.hasOwn(h.store, 'ymb_settings_migration_rollback_backup'), false);
});

test('legacy report prefix storage is exposed through the current key and preserved in place', async () => {
  const legacy = {
    'https://chatgpt.com|legacy': { enabled: true, text: 'LEGACY PREFIX', interval: 2, delivered_count: 7 }
  };
  const h = bootstrapHarness({ wsmb_report_prefix_configs: legacy });
  const result = await h.chrome.storage.local.get('wsmb_report_prefixes');
  assert.equal(canonical(result.wsmb_report_prefixes), canonical(legacy));
  assert.deepEqual(h.store.wsmb_report_prefixes, legacy);
  assert.deepEqual(h.store.wsmb_report_prefix_configs, legacy);
});

test('current report prefix entries win conflicts while unique legacy entries are retained', async () => {
  const legacy = {
    same: { enabled: true, text: 'LEGACY' },
    legacyOnly: { enabled: true, text: 'ONLY LEGACY' }
  };
  const current = {
    same: { enabled: false, text: 'CURRENT' },
    currentOnly: { enabled: true, text: 'ONLY CURRENT' }
  };
  const expected = {
    same: current.same,
    legacyOnly: legacy.legacyOnly,
    currentOnly: current.currentOnly
  };
  const h = bootstrapHarness({ wsmb_report_prefix_configs: legacy, wsmb_report_prefixes: current });
  const result = await h.chrome.storage.local.get('wsmb_report_prefixes');
  assert.equal(canonical(result.wsmb_report_prefixes), canonical(expected));
  assert.deepEqual(h.store.wsmb_report_prefix_configs, legacy);
  assert.equal(canonical(h.store.wsmb_report_prefixes), canonical(expected));
});

test('array storage reads used by settings export receive merged legacy report prefixes', async () => {
  const legacy = { old: { enabled: true, text: 'OLD' } };
  const h = bootstrapHarness({ wsmb_api_key: 'key', wsmb_report_prefix_configs: legacy });
  const result = await h.chrome.storage.local.get(['wsmb_api_key', 'wsmb_report_prefixes']);
  assert.equal(result.wsmb_api_key, 'key');
  assert.equal(canonical(result.wsmb_report_prefixes), canonical(legacy));
  assert.deepEqual(h.store.wsmb_report_prefix_configs, legacy);
});

test('runtime import merges settings while preserving active Autorun and Manual safety state', async () => {
  const RUN = 'https://chatgpt.com|aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa';
  const MANUAL = 'https://chatgpt.com|bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb';
  const LOCAL = 'https://chatgpt.com|cccccccc-cccc-4ccc-8ccc-cccccccccccc';
  const INCOMING = 'https://chatgpt.com|dddddddd-dddd-4ddd-8ddd-dddddddddddd';
  const runRecord = { status: 'waiting_command', run_id: 'run-live', active_service: 'search', requests_executed: 3 };
  const manualRecord = { status: 'requesting', operation_id: 'manual-live', active_service: 'wordstat' };
  const h = bootstrapHarness({
    wsmb_api_key: 'keep-secret',
    wsmb_folder_id: 'old-folder',
    wsmb_auto_send: true,
    wsmb_auto_runs: { [RUN]: runRecord },
    wsmb_manual_operations: { [MANUAL]: manualRecord },
    wsmb_conversation_bindings: {
      [RUN]: { binding_id: 'run-current' },
      [MANUAL]: { binding_id: 'manual-current' },
      [LOCAL]: { binding_id: 'local-current' }
    },
    wsmb_manual_modes: { [RUN]: false, [MANUAL]: true, [LOCAL]: true },
    wsmb_report_prefixes: {
      [RUN]: { enabled: true, text: 'RUN CURRENT' },
      [MANUAL]: { enabled: true, text: 'MANUAL CURRENT' },
      [LOCAL]: { enabled: true, text: 'LOCAL CURRENT' }
    },
    wsmb_auto_start_prompts: { [RUN]: { text: 'RUN PROMPT' }, [MANUAL]: { text: 'MANUAL PROMPT' } },
    ymb_service_contexts: {
      [RUN]: { active_service: 'search' },
      [MANUAL]: { active_service: 'wordstat' },
      [LOCAL]: { active_service: 'wordstat' }
    },
    wsmb_send_button_profile: { selector: '#current-send' },
    wsmb_copy_button_profiles: { chatgpt: [{ selector: '#current-copy' }] },
    ymb_wordstat_policy: { autorun_enabled: false, max_requests_per_run: 10 },
    ymb_search_policy: { autorun_enabled: true, max_requests_per_run: 20 }
  });
  assert.equal(h.testApi.runtimeListenerWrapped, true);
  const settings = {
    wordstat: { api_key: '', folder_id: 'new-folder' },
    auto_send: false,
    send_button_profile: { selector: '#incoming-send' },
    copy_button_profiles: { chatgpt: [{ selector: '#incoming-copy' }] },
    conversation_bindings: {
      [RUN]: { binding_id: 'run-imported' },
      [MANUAL]: { binding_id: 'manual-imported' },
      [INCOMING]: { binding_id: 'incoming-new' }
    },
    manual_modes: { [RUN]: true, [MANUAL]: false, [INCOMING]: true },
    report_prefixes: {
      [RUN]: { enabled: false, text: 'RUN IMPORTED' },
      [MANUAL]: { enabled: false, text: 'MANUAL IMPORTED' },
      [INCOMING]: { enabled: true, text: 'INCOMING PREFIX' }
    },
    auto_start_prompts: { [RUN]: { text: 'RUN IMPORTED PROMPT' }, [INCOMING]: { text: 'INCOMING PROMPT' } },
    service_contexts: {
      [RUN]: { active_service: 'wordstat' },
      [MANUAL]: { active_service: 'search' },
      [INCOMING]: { active_service: 'search' }
    },
    wordstat_policy: { autorun_enabled: true, max_requests_per_run: 99 },
    search_policy: { autorun_enabled: false, max_requests_per_run: 99 },
    debug_mode: true
  };
  const backup = await makeBackup(settings);
  const response = await h.send({ type: 'WS_IMPORT_BACKUP', backup });
  assert.equal(response.ok, true);
  assert.equal(response.result.imported, true);
  assert.equal(response.result.preserved_active_conversations, 2);
  assert.equal(response.result.active_runtime_state_untouched, true);
  assert.deepEqual(h.store.wsmb_auto_runs[RUN], runRecord);
  assert.deepEqual(h.store.wsmb_manual_operations[MANUAL], manualRecord);
  assert.equal(h.store.wsmb_api_key, 'keep-secret');
  assert.equal(h.store.wsmb_folder_id, 'new-folder');
  assert.equal(h.store.wsmb_auto_send, false);
  assert.equal(h.store.wsmb_conversation_bindings[RUN].binding_id, 'run-current');
  assert.equal(h.store.wsmb_conversation_bindings[MANUAL].binding_id, 'manual-current');
  assert.equal(h.store.wsmb_conversation_bindings[LOCAL].binding_id, 'local-current');
  assert.equal(h.store.wsmb_conversation_bindings[INCOMING].binding_id, 'incoming-new');
  assert.equal(h.store.wsmb_manual_modes[RUN], false);
  assert.equal(h.store.wsmb_manual_modes[MANUAL], true);
  assert.equal(h.store.wsmb_manual_modes[INCOMING], true);
  assert.equal(h.store.wsmb_report_prefixes[RUN].text, 'RUN CURRENT');
  assert.equal(h.store.wsmb_report_prefixes[MANUAL].text, 'MANUAL CURRENT');
  assert.equal(h.store.wsmb_report_prefixes[LOCAL].text, 'LOCAL CURRENT');
  assert.equal(h.store.wsmb_report_prefixes[INCOMING].text, 'INCOMING PREFIX');
  assert.equal(h.store.wsmb_auto_start_prompts[RUN].text, 'RUN PROMPT');
  assert.equal(h.store.wsmb_auto_start_prompts[INCOMING].text, 'INCOMING PROMPT');
  assert.equal(h.store.ymb_service_contexts[RUN].active_service, 'search');
  assert.equal(h.store.ymb_service_contexts[MANUAL].active_service, 'wordstat');
  assert.equal(h.store.ymb_service_contexts[LOCAL].active_service, 'wordstat');
  assert.equal(h.store.ymb_service_contexts[INCOMING].active_service, 'search');
  assert.deepEqual(h.store.wsmb_send_button_profile, { selector: '#incoming-send' });
  assert.deepEqual(h.store.wsmb_copy_button_profiles.chatgpt, [{ selector: '#current-copy' }, { selector: '#incoming-copy' }]);
  assert.equal(h.store.ymb_wordstat_policy.max_requests_per_run, 99);
  assert.equal(h.store.ymb_search_policy.max_requests_per_run, 99);
  assert.equal(h.store.ymb_debug_mode, true);
  assert.equal(h.store.ymb_settings_migration_rollback_backup.settings.wordstat.api_key, 'keep-secret');
});

test('bootstrap delegates non-import runtime messages to the worker listener unchanged', async () => {
  const h = bootstrapHarness();
  const response = await h.send({ type: 'WS_GET_GLOBAL_STATE' });
  assert.deepEqual(response, { ok: true, delegated: true, type: 'WS_GET_GLOBAL_STATE' });
});
