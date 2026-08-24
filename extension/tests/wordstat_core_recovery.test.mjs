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
function harness({ response = { status: 200, body: { ok: true } } } = {}) {
  const store = { wsmb_api_key: 'wordstat-key', wsmb_folder_id: 'folder-id' };
  const fetchCalls = [];
  let listener = null;
  const storage = {
    async get(keys) {
      if (keys == null) return clone(store);
      if (typeof keys === 'string') return Object.hasOwn(store, keys) ? { [keys]: clone(store[keys]) } : {};
      if (Array.isArray(keys)) { const out = {}; for (const key of keys) if (Object.hasOwn(store,key)) out[key] = clone(store[key]); return out; }
      const out = clone(keys || {}); for (const key of Object.keys(keys || {})) if (Object.hasOwn(store,key)) out[key] = clone(store[key]); return out;
    },
    async set(values) { Object.assign(store, clone(values)); },
    async remove(keys) { for (const key of (Array.isArray(keys) ? keys : [keys])) delete store[key]; }
  };
  const chrome = {
    storage: { local: storage },
    runtime: { id: 'test', lastError: null, onMessage: { addListener(fn) { listener = fn; } } },
    tabs: { sendMessage(_id, _message, cb) { cb({ ok: true }); } }
  };
  const ctx = vm.createContext({
    console, chrome, crypto: webcrypto, TextEncoder, TextDecoder, AbortController, performance,
    setTimeout, clearTimeout, URL, structuredClone, Response, Request, Headers, ReadableStream, Buffer,
    fetch: async (...args) => {
      fetchCalls.push(args);
      return new Response(JSON.stringify(response.body), { status: response.status });
    },
    importScripts: () => {}
  });
  ctx.globalThis = ctx;
  for (const file of [
    'shared/product.js','shared/conversation_identity.js','shared/manual_controls.js','shared/service_registry.js',
    'shared/block_command_discovery.js','shared/run_context_model.js','shared/credential_registry.js','shared/policy_model.js',
    'shared/cost_ledger_model.js','shared/wordstat_protocol.js','shared/search_xml.js','shared/search_protocol.js','shared/autorun_model.js'
  ]) vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'), ctx, { filename:file });
  vm.runInContext(workerSource, ctx, { filename:'service_worker.js' });
  assert.equal(typeof listener, 'function');
  vm.runInContext(`globalThis.__WORDSTAT_API=Object.freeze({${FN_NAMES.join(',')}});`, ctx);
  return { api: ctx.__WORDSTAT_API, fetchCalls };
}

const cases = [
  ['getTop', { method:'getTop', phrase:'авто', numPhrases:10, regions:['225'], devices:['DEVICE_ALL'] }, '/v2/wordstat/topRequests'],
  ['getDynamics', { method:'getDynamics', phrase:'авто', period:'PERIOD_MONTHLY', fromDate:'2026-01-01T00:00:00Z', toDate:'2026-08-01T00:00:00Z', regions:['225'], devices:['DEVICE_ALL'] }, '/v2/wordstat/dynamics'],
  ['getRegionsDistribution', { method:'getRegionsDistribution', phrase:'авто', region:'REGION_ALL', devices:['DEVICE_ALL'] }, '/v2/wordstat/regions'],
  ['getRegionsTree', { method:'getRegionsTree' }, '/v2/wordstat/getRegionsTree']
];

for (const [method, command, endpoint] of cases) {
  test(`Wordstat ${method} performs one provider request and returns WORDSTAT_RESULT_V1`, async () => {
    const h = harness({ response: { status:200, body:{ method, sample:true } } });
    const text = `WORDSTAT_API_V1\n${JSON.stringify(command)}`;
    const result = await h.api.executeWordstatCore(text, { request_id:`req-${method}` });
    assert.equal(h.fetchCalls.length, 1);
    const [url, options] = h.fetchCalls[0];
    assert.equal(String(url).endsWith(endpoint), true);
    assert.equal(options.method, 'POST');
    assert.equal(options.headers.Authorization, 'Api-Key wordstat-key');
    assert.equal(result.ok, true);
    assert.match(result.report_text, /^WORDSTAT_RESULT_V1\n/);
    const envelope = JSON.parse(result.report_text.slice('WORDSTAT_RESULT_V1\n'.length));
    assert.equal(envelope.service, 'wordstat');
    assert.equal(envelope.operation, method);
    assert.equal(envelope.request_id, `req-${method}`);
  });
}

test('Wordstat HTTP error is returned as one truthful result and is not retried', async () => {
  const h = harness({ response:{ status:429, body:{ code:'TOO_MANY_REQUESTS', message:'limit' } } });
  const text = `WORDSTAT_API_V1\n${JSON.stringify({ method:'getTop', phrase:'авто' })}`;
  const result = await h.api.executeWordstatCore(text, { request_id:'req-http-error' });
  assert.equal(h.fetchCalls.length, 1);
  assert.equal(result.ok, false);
  assert.equal(result.http_status, 429);
  assert.match(result.report_text, /^WORDSTAT_RESULT_V1\n/);
  const envelope = JSON.parse(result.report_text.slice('WORDSTAT_RESULT_V1\n'.length));
  assert.equal(envelope.status, 'ERROR');
  assert.equal(envelope.reason, 'TOO_MANY_REQUESTS');
});
