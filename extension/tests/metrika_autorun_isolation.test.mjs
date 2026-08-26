import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { webcrypto } from 'node:crypto';
import { performance } from 'node:perf_hooks';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const CID = '44444444-3333-4222-8111-000000000004';
const ORIGIN = 'https://chatgpt.com';
const CKEY = `${ORIGIN}|${CID}`;
const IDENTITY = { origin: ORIGIN, conversation_id: CID, conversation_key: CKEY, status: 'confirmed', source: 'path', chat_path: `/c/${CID}` };
const clone = (value) => value === undefined ? undefined : structuredClone(value);

function binding() {
  return { binding_id: 'b-metrika', revision: 1, origin: ORIGIN, conversation_id: CID, conversation_key: CKEY, bound_at: '2026-08-26T00:00:00Z', updated_at: '2026-08-26T00:00:00Z' };
}

function harness({ activeService = 'metrika', providerMode = 'unexpected' } = {}) {
  const store = {
    wsmb_conversation_bindings: { [CKEY]: binding() },
    ymb_service_contexts: { [CKEY]: { active_service: activeService, updated_at: '2026-08-26T00:00:00Z' } },
    wsmb_manual_modes: { [CKEY]: false },
    wsmb_auto_runs: {},
    wsmb_outbox: {},
    wsmb_manual_operations: {},
    ymb_service_credentials: {
      wordstat: { api_key: 'qa-wordstat-key', folder_id: 'qa-wordstat-folder', check_state: 'PRESENT' },
      search: { api_key: 'qa-search-key', folder_id: 'qa-search-folder', check_state: 'PRESENT' },
      webmaster: { oauth_token: 'qa-webmaster-oauth', user_id: '42', verified_at: '2026-08-26T00:00:00Z', check_state: 'PRESENT' },
      metrika: { oauth_token: 'qa-metrika-oauth', checked_at: '2026-08-26T00:00:00Z', check_state: 'PRESENT' }
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
      if (providerMode === 'metrika-ok') {
        return new Response(JSON.stringify({ rows: 0, counters: [] }), { status: 200, headers: { 'Content-Type': 'application/json' } });
      }
      throw new Error(`M13_M17_UNEXPECTED_PROVIDER_REQUEST ${url}`);
    }
  });
  ctx.globalThis = ctx;
  ctx.importScripts = (...items) => {
    for (const item of items) vm.runInContext(fs.readFileSync(path.join(root, item), 'utf8'), ctx, { filename: item });
  };
  vm.runInContext(fs.readFileSync(path.join(root, 'service_worker.js'), 'utf8'), ctx, { filename: 'service_worker.js' });
  vm.runInContext(fs.readFileSync(path.join(root, 'webmaster_worker_runtime.js'), 'utf8'), ctx, { filename: 'webmaster_worker_runtime.js' });
  vm.runInContext(`globalThis.__M13M17 = Object.freeze({
    startAutoRun,
    completeDelivery,
    handleAutoCommand,
    getAutoRun,
    getConversationOutbox,
    pauseAutoRun,
    resumeAutoRun,
    finishAutoRun
  });`, ctx, { filename: 'm13_m17_export.js' });
  return { ctx, store, listeners, fetchCalls, api: ctx.__M13M17 };
}

async function completeCurrentOutbox(h, basis) {
  const outbox = clone(await h.api.getConversationOutbox(CKEY));
  assert.ok(outbox?.delivery_id, `OUTBOX_MISSING_${basis}`);
  const completed = clone(await h.api.completeDelivery({
    conversation_key: CKEY,
    delivery_id: outbox.delivery_id,
    assistant_baseline_ids: ['baseline-turn'],
    confirmation_basis: basis
  }, { tab: { id: 1 } }));
  assert.equal(completed.ok, true);
  return outbox;
}

async function expectRoutingReject(h, commandText, assistantTurnId) {
  const run = clone(await h.api.getAutoRun(CKEY));
  const response = clone(await h.api.handleAutoCommand({
    conversation_key: CKEY,
    run_id: run.run_id,
    command_text: commandText,
    assistant_turn_id: assistantTurnId
  }, { tab: { id: 1 } }));
  assert.equal(response.ok, true);
  assert.equal(response.accepted, true);
  const outbox = clone(await h.api.getConversationOutbox(CKEY));
  assert.match(outbox.report_text, /^YMB_ERROR_V1\n/);
  assert.equal(h.fetchCalls.length, 0);
  return outbox;
}

test('M-13 active Webmaster rejects METRIKA_API_V1 before provider initiation', async () => {
  const h = harness({ activeService: 'webmaster' });
  const policy = clone(await h.ctx.YMBPhase3Runtime.getWebmasterPolicy());
  await h.ctx.YMBPhase3Runtime.saveWebmasterPolicy({ ...policy, autorun_enabled: true, max_requests_per_run: 5 });
  const started = clone(await h.api.startAutoRun(CKEY, 1));
  assert.equal(started.active_service, 'webmaster');
  await completeCurrentOutbox(h, 'm13-webmaster-start');
  await expectRoutingReject(h, 'METRIKA_API_V1\n{"method":"listCounters"}', 'm13-metrika-into-webmaster');
  assert.equal((await h.api.getAutoRun(CKEY)).active_service, 'webmaster');
  assert.equal(h.fetchCalls.length, 0);
});

test('M-13 active Metrika rejects Wordstat, Search and Webmaster before provider initiation', async () => {
  const h = harness({ activeService: 'metrika' });
  const policy = clone(await h.ctx.YMBPhase4Runtime.getMetrikaPolicy());
  await h.ctx.YMBPhase4Runtime.saveMetrikaPolicy({ ...policy, autorun_enabled: true, max_requests_per_run: 5 });
  const started = clone(await h.api.startAutoRun(CKEY, 1));
  assert.equal(started.active_service, 'metrika');
  await completeCurrentOutbox(h, 'm13-metrika-start');

  const commands = [
    ['WORDSTAT_API_V1\n{"method":"getRegionsTree"}', 'm13-wordstat-into-metrika'],
    ['SEARCH_API_V1\n{"method":"search","queryText":"qa"}', 'm13-search-into-metrika'],
    ['WEBMASTER_API_V1\n{"method":"listHosts"}', 'm13-webmaster-into-metrika']
  ];
  for (const [command, turn] of commands) {
    await expectRoutingReject(h, command, turn);
    assert.equal((await h.api.getAutoRun(CKEY)).active_service, 'metrika');
    await completeCurrentOutbox(h, `${turn}-complete`);
  }
  assert.equal(h.fetchCalls.length, 0);
  assert.equal((await h.api.getAutoRun(CKEY)).requests_executed, 0);
});

test('M-17 Metrika Autorun is default-off and start rejects locally with zero provider requests', async () => {
  const h = harness({ activeService: 'metrika' });
  const policy = clone(await h.ctx.YMBPhase4Runtime.getMetrikaPolicy());
  assert.equal(policy.autorun_enabled, false);
  await assert.rejects(() => h.api.startAutoRun(CKEY, 1), (error) => {
    assert.equal(error.code, 'AUTORUN_DISABLED');
    return true;
  });
  assert.equal(h.fetchCalls.length, 0);
  assert.equal(h.store.wsmb_auto_runs[CKEY], undefined);
  assert.equal(h.store.wsmb_outbox[CKEY], undefined);
});

test('M-17 controlled Metrika Autorun executes one request, one delivery, duplicate fence and unchanged lifecycle controls', async () => {
  const h = harness({ activeService: 'metrika', providerMode: 'metrika-ok' });
  const initial = clone(await h.ctx.YMBPhase4Runtime.getMetrikaPolicy());
  const enabled = clone(await h.ctx.YMBPhase4Runtime.saveMetrikaPolicy({ ...initial, autorun_enabled: true, max_requests_per_run: 2 }));
  assert.equal(enabled.autorun_enabled, true);

  const started = clone(await h.api.startAutoRun(CKEY, 1));
  assert.equal(started.active_service, 'metrika');
  assert.equal(started.status, 'starting');
  assert.match(started.start_delivery.message_text, /METRIKA_API_V1/);
  assert.equal(h.fetchCalls.length, 0);

  await completeCurrentOutbox(h, 'm17-start');
  const waiting = clone(await h.api.getAutoRun(CKEY));
  assert.equal(waiting.status, 'waiting_command');
  assert.equal(waiting.active_service, 'metrika');

  const accepted = clone(await h.api.handleAutoCommand({
    conversation_key: CKEY,
    run_id: waiting.run_id,
    command_text: 'METRIKA_API_V1\n{"method":"listCounters"}',
    assistant_turn_id: 'assistant-metrika-1'
  }, { tab: { id: 1 } }));
  assert.equal(accepted.ok, true);
  assert.equal(accepted.accepted, true);
  assert.equal(h.fetchCalls.length, 1);
  const url = new URL(h.fetchCalls[0].url);
  assert.equal(url.origin, 'https://api-metrika.yandex.net');
  assert.equal(url.pathname, '/management/v1/counters');
  assert.equal(url.searchParams.get('offset'), '1');
  assert.equal(url.searchParams.get('per_page'), '100');
  assert.equal(h.fetchCalls[0].options.method, 'GET');
  assert.equal(h.fetchCalls[0].options.headers.Authorization, 'OAuth qa-metrika-oauth');

  const resultOutbox = clone(await h.api.getConversationOutbox(CKEY));
  assert.equal(resultOutbox.type, 'autorun');
  assert.match(resultOutbox.report_text, /^METRIKA_RESULT_V1\n/);
  await completeCurrentOutbox(h, 'm17-result');

  const afterDelivery = clone(await h.api.getAutoRun(CKEY));
  assert.equal(afterDelivery.status, 'waiting_command');
  assert.equal(afterDelivery.sequence, 1);
  assert.equal(afterDelivery.requests_executed, 1);

  const duplicate = clone(await h.api.handleAutoCommand({
    conversation_key: CKEY,
    run_id: afterDelivery.run_id,
    command_text: 'METRIKA_API_V1\n{"method":"listCounters"}',
    assistant_turn_id: 'assistant-metrika-1'
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
