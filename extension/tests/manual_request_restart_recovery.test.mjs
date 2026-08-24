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
const fnNames = [...workerSource.matchAll(/^(?:async )?function\s+([A-Za-z0-9_]+)/gm)].map((m) => m[1]);

const ORIGIN = 'https://chatgpt.com';
const CID = '12121212-3434-4567-8787-909090909090';
const CKEY = `${ORIGIN}|${CID}`;
const IDENTITY = { origin: ORIGIN, conversation_id: CID, conversation_key: CKEY };
const clone = (value) => value === undefined ? undefined : structuredClone(value);

function staleOperation() {
  return {
    operation_id: 'manual-stale-request',
    request_token: 'manual-restart-token',
    conversation_key: CKEY,
    tab_id: 1,
    active_service: 'search',
    run_id: null,
    status: 'requesting',
    block_fingerprint: 'fingerprint',
    created_at: '2026-08-24T00:00:00.000Z',
    request_executed: false
  };
}

function harness({ outbox = null } = {}) {
  const store = {
    wsmb_manual_operations: { [CKEY]: staleOperation() },
    wsmb_outbox: outbox ? { [CKEY]: clone(outbox) } : {},
    ymb_debug_mode: false
  };
  const fetchCalls = [];
  const storage = {
    async get(keys) {
      if (keys == null) return clone(store);
      if (typeof keys === 'string') return Object.hasOwn(store, keys) ? { [keys]: clone(store[keys]) } : {};
      if (Array.isArray(keys)) {
        const result = {};
        for (const key of keys) if (Object.hasOwn(store, key)) result[key] = clone(store[key]);
        return result;
      }
      const result = clone(keys || {});
      for (const key of Object.keys(keys || {})) if (Object.hasOwn(store, key)) result[key] = clone(store[key]);
      return result;
    },
    async set(values) { Object.assign(store, clone(values)); },
    async remove(keys) { for (const key of (Array.isArray(keys) ? keys : [keys])) delete store[key]; }
  };
  let listener = null;
  const chrome = {
    storage: { local: storage },
    runtime: { id: 'test-extension', lastError: null, onMessage: { addListener(fn) { listener = fn; } } },
    tabs: {
      sendMessage(tabId, message, cb) {
        if (Number(tabId) === 1 && message?.type === 'WS_GET_IDENTITY') cb({ ok: true, identity: clone(IDENTITY), conversation_key: CKEY });
        else cb({ ok: true });
      }
    }
  };
  const ctx = vm.createContext({
    console, chrome, crypto: webcrypto, TextEncoder, TextDecoder, AbortController, performance,
    setTimeout, clearTimeout, URL, structuredClone, Response, Request, Headers, ReadableStream, Buffer,
    fetch: async (...args) => { fetchCalls.push(args); return new Response('{}', { status: 200 }); },
    importScripts: () => {}
  });
  ctx.globalThis = ctx;
  for (const file of [
    'shared/product.js','shared/conversation_identity.js','shared/manual_controls.js','shared/service_registry.js',
    'shared/block_command_discovery.js','shared/run_context_model.js','shared/credential_registry.js','shared/policy_model.js',
    'shared/cost_ledger_model.js','shared/wordstat_protocol.js','shared/search_xml.js','shared/search_protocol.js','shared/autorun_model.js'
  ]) vm.runInContext(fs.readFileSync(path.join(root, file), 'utf8'), ctx, { filename: file });
  vm.runInContext(workerSource, ctx, { filename: 'service_worker.js' });
  assert.equal(typeof listener, 'function');
  vm.runInContext(`globalThis.__RECOVERY_API=Object.freeze({${fnNames.join(',')}});`, ctx);
  return { api: ctx.__RECOVERY_API, store, fetchCalls };
}

test('worker restart converts abandoned Manual REQUESTING into one UNKNOWN error delivery without provider retry', async () => {
  const h = harness();
  await h.api.recoverPersistedRuntime();

  assert.equal(h.fetchCalls.length, 0, 'recovery must never retry the provider request');
  const operation = h.store.wsmb_manual_operations[CKEY];
  assert.equal(operation.status, 'delivering');
  assert.equal(operation.request_executed, 'UNKNOWN');
  assert.ok(operation.delivery_id);

  const outbox = h.store.wsmb_outbox[CKEY];
  assert.equal(outbox.type, 'manual');
  assert.equal(outbox.operation_id, operation.operation_id);
  assert.equal(outbox.delivery_id, operation.delivery_id);
  assert.equal(outbox.tab_id, 1);
  assert.match(outbox.report_text, /YMB_ERROR_V1/);
  assert.match(outbox.report_text, /REQUEST_OUTCOME_UNKNOWN_NO_RETRY/);

  const completed = await h.api.completeDelivery({ conversation_key: CKEY, delivery_id: outbox.delivery_id, confirmation_basis: 'microphone' }, { tab: { id: 1 } });
  assert.equal(completed.ok, true);
  assert.equal(h.store.wsmb_manual_operations[CKEY].status, 'completed');
  assert.equal(h.store.wsmb_outbox[CKEY], undefined);
});

test('restart after Manual outbox persistence reuses the existing delivery instead of creating a duplicate', async () => {
  const existing = {
    delivery_id: 'existing-manual-delivery',
    operation_id: 'manual-stale-request',
    type: 'manual',
    tab_id: 1,
    report_text: 'SEARCH_RESULT_V1\n{}',
    phase: 'claimed',
    provider_executions: 1,
    report_prefix_applied: false,
    created_at: '2026-08-24T00:00:01.000Z',
    conversation_key: CKEY,
    updated_at: '2026-08-24T00:00:01.000Z'
  };
  const h = harness({ outbox: existing });
  await h.api.recoverPersistedRuntime();

  assert.equal(h.fetchCalls.length, 0);
  assert.equal(h.store.wsmb_outbox[CKEY].delivery_id, existing.delivery_id);
  assert.equal(h.store.wsmb_outbox[CKEY].report_text, existing.report_text);
  const operation = h.store.wsmb_manual_operations[CKEY];
  assert.equal(operation.status, 'delivering');
  assert.equal(operation.delivery_id, existing.delivery_id);
});
