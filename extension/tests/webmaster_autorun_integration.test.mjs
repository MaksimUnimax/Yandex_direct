import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { webcrypto } from 'node:crypto';
import { performance } from 'node:perf_hooks';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const CID = '99999999-8888-4777-8666-555555555555';
const ORIGIN = 'https://chatgpt.com';
const CKEY = `${ORIGIN}|${CID}`;
const IDENTITY = { origin: ORIGIN, conversation_id: CID, conversation_key: CKEY, status: 'confirmed', source: 'path', chat_path: `/c/${CID}` };
const clone = (value) => value === undefined ? undefined : structuredClone(value);

function binding() {
  return { binding_id: 'b-webmaster', revision: 1, origin: ORIGIN, conversation_id: CID, conversation_key: CKEY, bound_at: '2026-08-26T00:00:00Z', updated_at: '2026-08-26T00:00:00Z' };
}

function harness() {
  const store = {
    wsmb_conversation_bindings: { [CKEY]: binding() },
    ymb_service_contexts: { [CKEY]: { active_service: 'webmaster', updated_at: '2026-08-26T00:00:00Z' } },
    wsmb_manual_modes: { [CKEY]: false },
    wsmb_auto_runs: {},
    wsmb_outbox: {},
    wsmb_manual_operations: {},
    ymb_service_credentials: {
      wordstat: { api_key: '', folder_id: '' },
      search: { api_key: '', folder_id: '' },
      webmaster: { oauth_token: 'qa-fake-oauth', user_id: '42', verified_at: '2026-08-26T00:00:00Z', check_state: 'PRESENT' }
    }
  };
  const listeners = [];
  const fetchCalls = [];
  const storage = {
    async get(keys) {
      if (keys == null) return clone(store);
      if (typeof keys === 'string') return Object.hasOwn(store, keys) ? { [keys]: clone(store[keys]) } : {};
      if (Array.isArray(keys)) return Object.fromEntries(keys.filter((key) => Object.hasOwn(store, key)).map((key) => [key, clone(store[key])]));
      const out = clone(keys || {});
      for (const key of Object.keys(keys || {})) if (Object.hasOwn(store, key)) out[key] = clone(store[key]);
      return out;
    },
    async set(values) { Object.assign(store, clone(values)); },
    async remove(keys) { for (const key of (Array.isArray(keys) ? keys : [keys])) delete store[key]; }
  };
  const chrome = {
    storage: { local: storage },
    runtime: { id: 'test-extension', lastError: null, onMessage: { addListener(fn) { listeners.push(fn); } } },
    tabs: {
      async query() { return [{ id: 1, url: `${ORIGIN}/c/${CID}` }]; },
      async get(id) { return Number(id) === 1 ? { id: 1, url: `${ORIGIN}/c/${CID}` } : null; },
      sendMessage(id, message, callback) {
        if (Number(id) !== 1) return callback(null);
        if (['WS_GET_IDENTITY', 'WS_PAGE_CONTEXT'].includes(message?.type)) return callback({ ok: true, identity: IDENTITY, conversation_key: CKEY });
        callback({ ok: true });
      }
    }
  };
  const ctx = vm.createContext({
    console, chrome, crypto: webcrypto, performance,
    TextEncoder, TextDecoder, AbortController, URL, URLSearchParams,
    structuredClone, Response, Request, Headers, ReadableStream, Buffer,
    setTimeout, clearTimeout, atob, btoa,
    fetch: async (url, options = {}) => {
      fetchCalls.push({ url: String(url), options: clone(options) });
      return new Response(JSON.stringify({ hosts: [] }), { status: 200, headers: { 'Content-Type': 'application/json' } });
    }
  });
  ctx.globalThis = ctx;
  ctx.importScripts = (...items) => {
    for (const item of items) vm.runInContext(fs.readFileSync(path.join(root, item), 'utf8'), ctx, { filename: item });
  };
  vm.runInContext(fs.readFileSync(path.join(root, 'service_worker.js'), 'utf8'), ctx, { filename: 'service_worker.js' });
  vm.runInContext(fs.readFileSync(path.join(root, 'webmaster_worker_runtime.js'), 'utf8'), ctx, { filename: 'webmaster_worker_runtime.js' });
  vm.runInContext(`globalThis.__W17 = Object.freeze({
    startAutoRun,
    completeDelivery,
    handleAutoCommand,
    getAutoRun,
    getConversationOutbox,
    pauseAutoRun,
    resumeAutoRun,
    finishAutoRun
  });`, ctx, { filename: 'w17_export.js' });
  return { ctx, store, listeners, fetchCalls, api: ctx.__W17 };
}

test('W-17 Webmaster Autorun is default-off and rejects start locally with zero provider requests', async () => {
  const h = harness();
  const policy = clone(await h.ctx.YMBPhase3Runtime.getWebmasterPolicy());
  assert.equal(policy.autorun_enabled, false);
  await assert.rejects(() => h.api.startAutoRun(CKEY, 1), (error) => {
    assert.equal(error.code, 'AUTORUN_DISABLED');
    return true;
  });
  assert.equal(h.fetchCalls.length, 0);
  assert.equal(h.store.wsmb_auto_runs[CKEY], undefined);
  assert.equal(h.store.wsmb_outbox[CKEY], undefined);
});

test('W-17 controlled enable runs one read-only Webmaster command through the common Autorun lifecycle', async () => {
  const h = harness();
  const initialPolicy = clone(await h.ctx.YMBPhase3Runtime.getWebmasterPolicy());
  const enabled = clone(await h.ctx.YMBPhase3Runtime.saveWebmasterPolicy({ ...initialPolicy, autorun_enabled: true, max_requests_per_run: 2 }));
  assert.equal(enabled.autorun_enabled, true);

  const started = clone(await h.api.startAutoRun(CKEY, 1));
  assert.equal(started.active_service, 'webmaster');
  assert.equal(started.status, 'starting');
  assert.match(started.start_delivery.message_text, /WEBMASTER_API_V1/);
  assert.equal(h.fetchCalls.length, 0);

  const startOutbox = clone(await h.api.getConversationOutbox(CKEY));
  assert.equal(startOutbox.type, 'autorun_start');
  const startComplete = clone(await h.api.completeDelivery({
    conversation_key: CKEY,
    delivery_id: startOutbox.delivery_id,
    assistant_baseline_ids: ['baseline-turn'],
    confirmation_basis: 'qa_controlled_start'
  }, { tab: { id: 1 } }));
  assert.equal(startComplete.ok, true);
  const waiting = clone(await h.api.getAutoRun(CKEY));
  assert.equal(waiting.status, 'waiting_command');
  assert.equal(waiting.active_service, 'webmaster');

  const accepted = clone(await h.api.handleAutoCommand({
    conversation_key: CKEY,
    run_id: waiting.run_id,
    command_text: 'WEBMASTER_API_V1\n{"method":"listHosts"}',
    assistant_turn_id: 'assistant-webmaster-1'
  }, { tab: { id: 1 } }));
  assert.equal(accepted.ok, true);
  assert.equal(accepted.accepted, true);
  assert.equal(h.fetchCalls.length, 1);
  assert.equal(h.fetchCalls[0].url, 'https://api.webmaster.yandex.net/v4/user/42/hosts');
  assert.equal(h.fetchCalls[0].options.method, 'GET');
  assert.equal(h.fetchCalls[0].options.headers.Authorization, 'OAuth qa-fake-oauth');

  const resultOutbox = clone(await h.api.getConversationOutbox(CKEY));
  assert.equal(resultOutbox.type, 'autorun');
  assert.match(resultOutbox.report_text, /^WEBMASTER_RESULT_V1\n/);
  const resultComplete = clone(await h.api.completeDelivery({
    conversation_key: CKEY,
    delivery_id: resultOutbox.delivery_id,
    confirmation_basis: 'qa_controlled_result'
  }, { tab: { id: 1 } }));
  assert.equal(resultComplete.ok, true);
  const afterDelivery = clone(await h.api.getAutoRun(CKEY));
  assert.equal(afterDelivery.status, 'waiting_command');
  assert.equal(afterDelivery.sequence, 1);
  assert.equal(afterDelivery.requests_executed, 1);

  const duplicate = clone(await h.api.handleAutoCommand({
    conversation_key: CKEY,
    run_id: afterDelivery.run_id,
    command_text: 'WEBMASTER_API_V1\n{"method":"listHosts"}',
    assistant_turn_id: 'assistant-webmaster-1'
  }, { tab: { id: 1 } }));
  assert.equal(duplicate.accepted, false);
  assert.equal(duplicate.duplicate, true);
  assert.equal(h.fetchCalls.length, 1);

  const paused = clone(await h.api.pauseAutoRun(CKEY, 1));
  assert.equal(paused.status, 'paused');
  const resumed = clone(await h.api.resumeAutoRun(CKEY, 1));
  assert.equal(resumed.status, 'waiting_command');
  const finished = clone(await h.api.finishAutoRun(CKEY, 1));
  assert.equal(finished.status, 'stopped');
  assert.equal(h.fetchCalls.length, 1);
});
