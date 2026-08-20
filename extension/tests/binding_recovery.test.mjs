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
const popupSource = fs.readFileSync(path.join(root, 'popup.js'), 'utf8');
const FN_NAMES = [...workerSource.matchAll(/^(?:async )?function\s+([A-Za-z0-9_]+)/gm)].map((m) => m[1]);
const ORIGIN = 'https://chatgpt.com';
const CID = '99999999-8888-4777-8666-555555555555';
const CKEY = `${ORIGIN}|${CID}`;

function clone(value) { return value === undefined ? undefined : structuredClone(value); }
function harness() {
  const store = {};
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
  const tabCalls = [];
  let current = { origin: ORIGIN, conversation_id: CID, conversation_key: CKEY };
  const chrome = {
    storage: { local: storage },
    runtime: { id: 'test', lastError: null, onMessage: { addListener() {} } },
    tabs: { sendMessage(tabId, message, cb) { tabCalls.push({ tabId, message: clone(message) }); cb({ ok: true, identity: clone(current), conversation_key: current.conversation_key }); } }
  };
  const ctx = vm.createContext({ console, chrome, crypto: webcrypto, TextEncoder, TextDecoder, AbortController, performance, setTimeout, clearTimeout, URL, structuredClone, Response, Request, Headers, ReadableStream, Buffer, fetch: async () => new Response('{}', { status: 200 }), importScripts: () => {} });
  ctx.globalThis = ctx;
  for (const file of ['shared/product.js','shared/conversation_identity.js','shared/manual_controls.js','shared/service_registry.js','shared/block_command_discovery.js','shared/run_context_model.js','shared/credential_registry.js','shared/policy_model.js','shared/cost_ledger_model.js','shared/wordstat_protocol.js','shared/search_xml.js','shared/search_protocol.js','shared/autorun_model.js']) vm.runInContext(fs.readFileSync(path.join(root, file), 'utf8'), ctx, { filename: file });
  vm.runInContext(workerSource, ctx, { filename: 'service_worker.js' });
  vm.runInContext(`globalThis.__BINDING_API=Object.freeze({${FN_NAMES.join(',')}});`, ctx);
  return { api: ctx.__BINDING_API, store, tabCalls, setIdentity(value) { current = clone(value); } };
}

test('binding is created from live identity of the selected ChatGPT tab', async () => {
  const h = harness();
  const result = await h.api.bindConversationFromTab(17);
  assert.equal(result.conversation_key, CKEY);
  assert.equal(result.binding.conversation_key, CKEY);
  assert.equal(result.binding.origin, ORIGIN);
  assert.equal(result.binding.conversation_id, CID);
  assert.equal(result.binding.revision, 1);
  assert.equal(h.tabCalls.length, 1);
  assert.equal(h.tabCalls[0].tabId, 17);
  assert.equal(h.tabCalls[0].message.type, 'WS_GET_IDENTITY');
});

test('rebinding the same conversation preserves binding identity and increments revision', async () => {
  const h = harness();
  const first = await h.api.bindConversationFromTab(3);
  const second = await h.api.bindConversationFromTab(3);
  assert.equal(second.binding.binding_id, first.binding.binding_id);
  assert.equal(second.binding.revision, 2);
  const saved = h.store.wsmb_conversation_bindings[CKEY];
  assert.equal(saved.binding_id, first.binding.binding_id);
  assert.equal(saved.revision, 2);
});

test('popup binding asks worker to bind the active tab instead of trusting a typed conversation id', () => {
  assert.match(popupSource, /WS_BIND_CONVERSATION/);
  assert.match(popupSource, /tab_id:\s*context\.tab_id/);
  assert.doesNotMatch(popupSource, /WS_BIND_CONVERSATION[^\n]*conversation_key/);
});
