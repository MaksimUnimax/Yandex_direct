import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { webcrypto } from 'node:crypto';
import { performance } from 'node:perf_hooks';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const CID = '77777777-6666-4555-8444-333333333333';
const ORIGIN = 'https://chatgpt.com';
const CKEY = `${ORIGIN}|${CID}`;
const IDENTITY = { origin: ORIGIN, conversation_id: CID, conversation_key: CKEY, status: 'confirmed', source: 'path', chat_path: `/c/${CID}` };
const clone = (value) => value === undefined ? undefined : structuredClone(value);

function harness() {
  const store = {
    wsmb_conversation_bindings: { [CKEY]: { binding_id: 'b-w13', revision: 1, origin: ORIGIN, conversation_id: CID, conversation_key: CKEY, bound_at: '2026-08-26T00:00:00Z', updated_at: '2026-08-26T00:00:00Z' } },
    ymb_service_contexts: { [CKEY]: { active_service: 'webmaster', updated_at: '2026-08-26T00:00:00Z' } },
    wsmb_manual_modes: { [CKEY]: false },
    wsmb_auto_runs: {},
    wsmb_outbox: {},
    wsmb_manual_operations: {},
    ymb_service_credentials: {
      wordstat: { api_key: 'qa-wordstat-key', folder_id: 'qa-wordstat-folder' },
      search: { api_key: 'qa-search-key', folder_id: 'qa-search-folder' },
      webmaster: { oauth_token: 'qa-webmaster-oauth', user_id: '42', verified_at: '2026-08-26T00:00:00Z', check_state: 'PRESENT' }
    }
  };
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
    runtime: { id: 'test-extension', lastError: null, onMessage: { addListener() {} } },
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
      throw new Error(`W13_UNEXPECTED_PROVIDER_REQUEST ${url}`);
    }
  });
  ctx.globalThis = ctx;
  ctx.importScripts = (...items) => {
    for (const item of items) vm.runInContext(fs.readFileSync(path.join(root, item), 'utf8'), ctx, { filename: item });
  };
  vm.runInContext(fs.readFileSync(path.join(root, 'service_worker.js'), 'utf8'), ctx, { filename: 'service_worker.js' });
  vm.runInContext(fs.readFileSync(path.join(root, 'webmaster_worker_runtime.js'), 'utf8'), ctx, { filename: 'webmaster_worker_runtime.js' });
  vm.runInContext(`globalThis.__W13 = Object.freeze({ startAutoRun, completeDelivery, handleAutoCommand, getAutoRun, getConversationOutbox });`, ctx, { filename: 'w13_export.js' });
  return { ctx, store, fetchCalls, api: ctx.__W13 };
}

async function completeCurrentOutbox(h, basis) {
  const outbox = clone(await h.api.getConversationOutbox(CKEY));
  assert.ok(outbox?.delivery_id, `W13_OUTBOX_MISSING_${basis}`);
  const completed = clone(await h.api.completeDelivery({ conversation_key: CKEY, delivery_id: outbox.delivery_id, confirmation_basis: basis }, { tab: { id: 1 } }));
  assert.equal(completed.ok, true);
}

async function expectServiceRoutingReject(h, commandText, assistantTurnId) {
  const run = clone(await h.api.getAutoRun(CKEY));
  const response = clone(await h.api.handleAutoCommand({
    conversation_key: CKEY,
    run_id: run.run_id,
    command_text: commandText,
    assistant_turn_id: assistantTurnId
  }, { tab: { id: 1 } }));
  const outbox = clone(await h.api.getConversationOutbox(CKEY));
  assert.ok(outbox, `W13_ERROR_OUTBOX_MISSING_${assistantTurnId}`);
  assert.match(outbox.report_text, /^YMB_ERROR_V1\n/);
  assert.equal(h.fetchCalls.length, 0, `W13_PROVIDER_CALLED_${assistantTurnId}`);
  assert.notEqual(response?.accepted, true, `W13_WRONG_SERVICE_ACCEPTED_${assistantTurnId}`);
  return outbox;
}

test('W-13 Webmaster, Search and Wordstat Autorun service routing stays isolated before provider initiation', async () => {
  const h = harness();
  const initialPolicy = clone(await h.ctx.YMBPhase3Runtime.getWebmasterPolicy());
  await h.ctx.YMBPhase3Runtime.saveWebmasterPolicy({ ...initialPolicy, autorun_enabled: true, max_requests_per_run: 5 });

  const started = clone(await h.api.startAutoRun(CKEY, 1));
  assert.equal(started.active_service, 'webmaster');
  await completeCurrentOutbox(h, 'w13_start');

  await expectServiceRoutingReject(h, 'SEARCH_API_V1\n{"method":"search","queryText":"qa"}', 'w13-search-into-webmaster');
  assert.equal((await h.api.getAutoRun(CKEY)).active_service, 'webmaster');
  await completeCurrentOutbox(h, 'w13_search_into_webmaster');

  await expectServiceRoutingReject(h, 'WORDSTAT_API_V1\n{"method":"getRegionsTree"}', 'w13-wordstat-into-webmaster');
  assert.equal((await h.api.getAutoRun(CKEY)).active_service, 'webmaster');
  await completeCurrentOutbox(h, 'w13_wordstat_into_webmaster');

  // Controlled run-state substitutions exercise the reverse routing edge without invoking any provider.
  h.store.wsmb_auto_runs[CKEY].active_service = 'search';
  await expectServiceRoutingReject(h, 'WEBMASTER_API_V1\n{"method":"listHosts"}', 'w13-webmaster-into-search');
  assert.equal((await h.api.getAutoRun(CKEY)).active_service, 'search');
  await completeCurrentOutbox(h, 'w13_webmaster_into_search');

  h.store.wsmb_auto_runs[CKEY].active_service = 'wordstat';
  await expectServiceRoutingReject(h, 'WEBMASTER_API_V1\n{"method":"listHosts"}', 'w13-webmaster-into-wordstat');
  assert.equal((await h.api.getAutoRun(CKEY)).active_service, 'wordstat');
  await completeCurrentOutbox(h, 'w13_webmaster_into_wordstat');

  assert.equal(h.fetchCalls.length, 0);
  assert.equal((await h.api.getAutoRun(CKEY)).requests_executed, 0);
});
