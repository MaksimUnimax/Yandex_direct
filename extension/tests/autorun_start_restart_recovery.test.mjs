import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { webcrypto } from 'node:crypto';
import { performance } from 'node:perf_hooks';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const rawWorkerSource = fs.readFileSync(path.join(root, 'service_worker.js'), 'utf8');
const bootstrapStart = rawWorkerSource.lastIndexOf('\nvoid recoverPersistedRuntime().catch');
assert.notEqual(bootstrapStart, -1, 'worker recovery bootstrap not found');
const workerSource = rawWorkerSource.slice(0, bootstrapStart);
const FN_NAMES = [...workerSource.matchAll(/^(?:async )?function\s+([A-Za-z0-9_]+)/gm)].map((m) => m[1]);

const CID = '99999999-8888-4777-8666-555555555555';
const ORIGIN = 'https://chatgpt.com';
const CKEY = `${ORIGIN}|${CID}`;
const START_TEXT = 'SEARCH START PROMPT';
const IDENTITY = { origin: ORIGIN, conversation_id: CID, status: 'confirmed', source: 'path', chat_path: `/c/${CID}` };

function clone(value) { return value === undefined ? undefined : structuredClone(value); }
function startingRun() {
  return {
    run_id: 'run-start-restart',
    active_service: 'search',
    permission_profile: 'SEARCH',
    requests_attempted: 0,
    requests_executed: 0,
    requests_skipped: 0,
    estimated_cost_rub: 0,
    conversation_key: CKEY,
    origin: ORIGIN,
    conversation_id: CID,
    binding_snapshot: { binding_id:'b-start', revision:1, origin:ORIGIN, conversation_id:CID, conversation_key:CKEY },
    tab_id: 1,
    status: 'starting',
    sequence: 0,
    pause_requested: false,
    finish_requested: false,
    assistant_baseline_ids: [],
    watch_id: null,
    start_delivery: { phase: 'none', message_text: START_TEXT },
    delivery: null,
    created_at: '2026-08-24T00:00:00Z'
  };
}
function existingStartOutbox() {
  return {
    delivery_id: 'existing-start-delivery',
    type: 'autorun_start',
    run_id: 'run-start-restart',
    tab_id: 1,
    conversation_key: CKEY,
    report_text: START_TEXT,
    phase: 'claimed',
    created_at: '2026-08-24T00:00:01Z',
    updated_at: '2026-08-24T00:00:01Z'
  };
}

function harness(initial = {}) {
  const store = clone(initial);
  const fetchCalls = [];
  let listener = null;
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
  const chrome = {
    storage: { local: storage },
    runtime: { id: 'test-extension', lastError: null, onMessage: { addListener(fn) { listener = fn; } } },
    tabs: {
      async query() { return [{ id:1, url:`${ORIGIN}/c/${CID}` }]; },
      async get(id) { return Number(id) === 1 ? { id:1, url:`${ORIGIN}/c/${CID}` } : null; },
      sendMessage(_id, message, cb) {
        if (['WS_GET_IDENTITY','WS_PAGE_CONTEXT'].includes(message?.type)) return cb({ ok:true, identity:IDENTITY, conversation_key:CKEY });
        cb({ ok:true });
      }
    }
  };
  const ctx = vm.createContext({
    console, chrome, crypto:webcrypto, TextEncoder, TextDecoder, AbortController, performance,
    setTimeout, clearTimeout, URL, structuredClone, Response, Request, Headers, ReadableStream, Buffer,
    fetch: async (...args) => { fetchCalls.push(args); return new Response('{}', { status:200 }); },
    importScripts: () => {}
  });
  ctx.globalThis = ctx;
  for (const file of [
    'shared/product.js','shared/conversation_identity.js','shared/manual_controls.js','shared/service_registry.js',
    'shared/block_command_discovery.js','shared/run_context_model.js','shared/credential_registry.js','shared/policy_model.js',
    'shared/cost_ledger_model.js','shared/wordstat_protocol.js','shared/search_xml.js','shared/search_protocol.js','shared/autorun_model.js'
  ]) vm.runInContext(fs.readFileSync(path.join(root, file), 'utf8'), ctx, { filename:file });
  vm.runInContext(workerSource, ctx, { filename:'service_worker.js' });
  assert.equal(typeof listener, 'function');
  vm.runInContext(`globalThis.__API=Object.freeze({${FN_NAMES.join(',')},KEYS});`, ctx);
  return { api:ctx.__API, store, fetchCalls };
}

function baseStore(extra = {}) {
  return {
    wsmb_auto_runs: { [CKEY]: startingRun() },
    ...extra
  };
}

test('worker restart restores missing autorun_start outbox for persisted STARTING run', async () => {
  const h = harness(baseStore());
  await h.api.recoverPersistedRuntime();
  assert.equal(h.fetchCalls.length, 0);
  const run = h.store.wsmb_auto_runs[CKEY];
  assert.equal(run.run_id, 'run-start-restart');
  assert.equal(run.status, 'starting');
  assert.equal(run.start_delivery.phase, 'none');
  const entry = h.store.wsmb_outbox?.[CKEY];
  assert.ok(entry, 'autorun_start outbox must be restored');
  assert.equal(entry.type, 'autorun_start');
  assert.equal(entry.run_id, run.run_id);
  assert.equal(entry.tab_id, 1);
  assert.equal(entry.report_text, START_TEXT);
  assert.equal(entry.phase, 'claimed');

  const deliveryId = entry.delivery_id;
  await h.api.recoverPersistedRuntime();
  assert.equal(h.store.wsmb_outbox[CKEY].delivery_id, deliveryId, 'recovery must be idempotent');
  assert.equal(h.fetchCalls.length, 0);
});

test('worker restart preserves an already persisted matching autorun_start outbox', async () => {
  const existing = existingStartOutbox();
  const h = harness(baseStore({ wsmb_outbox:{ [CKEY]:existing } }));
  await h.api.recoverPersistedRuntime();
  assert.deepEqual(h.store.wsmb_outbox[CKEY], existing);
  assert.equal(h.store.wsmb_auto_runs[CKEY].status, 'starting');
  assert.equal(h.fetchCalls.length, 0);
});
