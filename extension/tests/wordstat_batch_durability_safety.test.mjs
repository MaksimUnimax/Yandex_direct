import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');
const clone = (value) => value == null ? value : JSON.parse(JSON.stringify(value));

function loadFactory() {
  const ctx = {
    console, JSON, Object, Array, Set, String, Number, Boolean, RegExp, Date, Error, Math,
    crypto: { randomUUID: () => 'uuid' }, globalThis: null
  };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  for (const file of ['shared/provider_batch_job_model.js', 'shared/wordstat_batch_protocol.js', 'shared/wordstat_batch_runtime.js']) {
    vm.runInContext(fs.readFileSync(path.join(src, file), 'utf8'), ctx, { filename: file });
  }
  return ctx.YMBWordstatBatchRuntime;
}

function memoryStorage() {
  const state = {};
  return {
    state,
    async get(key) { return clone(state[key]); },
    async set(key, value) { state[key] = clone(value); }
  };
}

function startCommand(overrides = {}) {
  return {
    action: 'start', phrases: ['alpha'], numPhrases: 100,
    regions: ['225'], devices: ['DEVICE_ALL'], maxRequests: 1, maxCostRub: 1,
    ...overrides
  };
}

test('successful provider payload is durable in the batch checkpoint before caller delivery', async () => {
  const Factory = loadFactory();
  const storage = memoryStorage();
  const providerEnvelope = {
    service: 'wordstat', operation: 'getTop', status: 'OK', http_status: 200,
    request_executed: true, automatic_retry: false,
    result: { top: [{ phrase: 'alpha result', count: 42 }] }
  };
  const runtime = Factory.create({
    storage,
    workerSessionId: 'worker-A',
    estimateCostRub: () => 0.02,
    executeWordstat: async (_command, metadata) => ({
      ok: true,
      request_id: metadata.request_id,
      request_executed: true,
      report_envelope: clone(providerEnvelope)
    }),
    uid: (() => { let n = 0; return () => n++ === 0 ? 'job-1' : `req-${n}`; })(),
    now: () => '2026-08-27T13:30:00.000Z'
  });

  await runtime.handle(startCommand());
  await runtime.handle({ action: 'next', jobId: 'job-1' });

  const item = storage.state.ymb_wordstat_batch_jobs_v1['job-1'].items[0];
  assert.equal(item.status, 'SUCCEEDED');
  assert.deepEqual(item.result_payload, providerEnvelope, 'provider payload must survive worker loss after success persistence');
});

test('transport context cannot override authoritative batch request identity metadata', async () => {
  const Factory = loadFactory();
  const storage = memoryStorage();
  let observed = null;
  const runtime = Factory.create({
    storage,
    workerSessionId: 'worker-A',
    estimateCostRub: () => 0.02,
    executeWordstat: async (_command, metadata) => {
      observed = clone(metadata);
      return { ok: true, request_id: metadata.request_id, request_executed: true, report_envelope: { http_status: 200 } };
    },
    uid: (() => { let n = 0; return () => n++ === 0 ? 'job-1' : `req-${n}`; })(),
    now: () => '2026-08-27T13:31:00.000Z'
  });

  await runtime.handle(startCommand());
  await runtime.handle({ action: 'next', jobId: 'job-1' }, {
    request_id: 'context-must-not-win',
    job_id: 'wrong-job',
    batch_item_id: 'wrong-item',
    batch_worker_session_id: 'wrong-worker',
    channel: 'manual'
  });

  assert.equal(observed.job_id, 'job-1');
  assert.equal(observed.batch_worker_session_id, 'worker-A');
  assert.match(observed.request_id, /^req-/);
  assert.match(observed.batch_item_id, /^job-1:/);
  assert.equal(observed.channel, 'manual');
});
