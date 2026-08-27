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
  const ctx = { console, JSON, Object, Array, Set, String, Number, Boolean, RegExp, Date, Error, Math, crypto: { randomUUID: () => 'uuid' }, globalThis: null };
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

test('batch admission denial does not claim an item or contact Wordstat', async () => {
  const Factory = loadFactory();
  const storage = memoryStorage();
  let providerCalls = 0;
  const runtime = Factory.create({
    storage,
    workerSessionId: 'worker-A',
    executeWordstat: async () => { providerCalls += 1; return {}; },
    admit: async () => ({ allow: false, reason: 'AUTORUN_DISABLED', estimated_cost_rub: 0.02 }),
    estimateCostRub: () => 0.02,
    uid: (() => { let n = 0; return () => n++ === 0 ? 'job-1' : `req-${n}`; })(),
    now: () => '2026-08-27T13:10:00.000Z'
  });

  await runtime.handle({
    action: 'start', phrases: ['alpha'], numPhrases: 100, regions: ['225'], devices: ['DEVICE_ALL'], maxRequests: 1, maxCostRub: 1
  }, { channel: 'autorun' });

  const result = await runtime.handle({ action: 'next', jobId: 'job-1' }, { channel: 'autorun' });
  assert.equal(result.envelope.reason, 'AUTORUN_DISABLED');
  assert.equal(result.envelope.request_executed, false);
  assert.equal(providerCalls, 0);
  assert.equal(storage.state.ymb_wordstat_batch_jobs_v1['job-1'].items[0].status, 'PENDING');
});

test('admission may supply the exact paid estimate used by checkpoint accounting', async () => {
  const Factory = loadFactory();
  const storage = memoryStorage();
  const runtime = Factory.create({
    storage,
    workerSessionId: 'worker-A',
    executeWordstat: async (_command, metadata) => ({ ok: true, request_id: metadata.request_id, request_executed: true, report_envelope: { http_status: 200, request_executed: true } }),
    admit: async () => ({ allow: true, reason: 'ALLOW', estimated_cost_rub: 0.07 }),
    estimateCostRub: () => 0.02,
    uid: (() => { let n = 0; return () => n++ === 0 ? 'job-1' : `req-${n}`; })(),
    now: () => '2026-08-27T13:10:00.000Z'
  });

  await runtime.handle({ action: 'start', phrases: ['alpha'], numPhrases: 100, regions: ['225'], devices: ['DEVICE_ALL'], maxRequests: 1, maxCostRub: 1 }, { channel: 'manual' });
  const result = await runtime.handle({ action: 'next', jobId: 'job-1' }, { channel: 'manual' });
  assert.equal(result.envelope.progress.estimated_cost_rub, 0.07);
});
