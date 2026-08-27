import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');

function clone(value) { return value == null ? value : JSON.parse(JSON.stringify(value)); }

function loadFactory() {
  const ctx = {
    console, JSON, Object, Array, Set, String, Number, Boolean, RegExp, Date, Error, Math,
    crypto: { randomUUID: () => 'uuid-fixed' }, globalThis: null
  };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  for (const file of ['shared/provider_batch_job_model.js', 'shared/wordstat_batch_protocol.js', 'shared/wordstat_batch_runtime.js']) {
    vm.runInContext(fs.readFileSync(path.join(src, file), 'utf8'), ctx, { filename: file });
  }
  return ctx.YMBWordstatBatchRuntime;
}

function memoryStorage(initial = {}) {
  const state = clone(initial);
  const writes = [];
  return {
    state,
    writes,
    async get(key) { return clone(state[key]); },
    async set(key, value) { state[key] = clone(value); writes.push(clone(value)); }
  };
}

function startCommand(overrides = {}) {
  return {
    action: 'start',
    phrases: ['alpha', 'beta'],
    numPhrases: 100,
    regions: ['225'],
    devices: ['DEVICE_ALL'],
    maxRequests: 2,
    maxCostRub: 1,
    ...overrides
  };
}

test('start creates a durable deduplicated Wordstat getTop job without provider traffic', async () => {
  const Factory = loadFactory();
  const storage = memoryStorage();
  let providerCalls = 0;
  const runtime = Factory.create({
    storage,
    workerSessionId: 'worker-A',
    executeWordstat: async () => { providerCalls += 1; throw new Error('must not run'); },
    estimateCostRub: () => 0.02,
    now: () => '2026-08-27T13:00:00.000Z',
    uid: () => 'batch-job-1'
  });

  const result = await runtime.handle(startCommand({ phrases: ['alpha', 'alpha', 'beta'] }));
  assert.equal(result.envelope.operation, 'batch.start');
  assert.equal(result.envelope.job_id, 'batch-job-1');
  assert.equal(result.envelope.progress.total, 2);
  assert.equal(result.envelope.progress.duplicate_count, 1);
  assert.equal(providerCalls, 0);
  assert.equal(storage.state.ymb_wordstat_batch_jobs_v1['batch-job-1'].status, 'RUNNING');
});

test('next persists CLAIMED and REQUEST_STARTED checkpoints before provider execution', async () => {
  const Factory = loadFactory();
  const storage = memoryStorage();
  let writesAtProviderStart = 0;
  const runtime = Factory.create({
    storage,
    workerSessionId: 'worker-A',
    executeWordstat: async (command, metadata) => {
      writesAtProviderStart = storage.writes.length;
      const job = storage.state.ymb_wordstat_batch_jobs_v1['batch-job-1'];
      assert.equal(job.items[0].status, 'REQUEST_STARTED');
      assert.equal(job.items[0].request_id, metadata.request_id);
      return {
        ok: true,
        request_id: metadata.request_id,
        report_envelope: { service: 'wordstat', operation: command.method, http_status: 200, request_executed: true, automatic_retry: false }
      };
    },
    estimateCostRub: () => 0.02,
    now: () => '2026-08-27T13:00:00.000Z',
    uid: (() => { let n = 0; return () => n++ === 0 ? 'batch-job-1' : `req-${n}`; })()
  });

  await runtime.handle(startCommand());
  const before = storage.writes.length;
  const result = await runtime.handle({ action: 'next', jobId: 'batch-job-1' });
  assert.ok(writesAtProviderStart >= before + 2);
  assert.equal(result.envelope.request_executed, true);
  assert.equal(result.envelope.progress.succeeded, 1);
  assert.equal(storage.state.ymb_wordstat_batch_jobs_v1['batch-job-1'].items[0].status, 'SUCCEEDED');
});

test('unknown provider outcome is persisted as OUTCOME_UNKNOWN and never reclaimed', async () => {
  const Factory = loadFactory();
  const storage = memoryStorage();
  let calls = 0;
  const runtime = Factory.create({
    storage,
    workerSessionId: 'worker-A',
    executeWordstat: async () => {
      calls += 1;
      const error = new Error('network outcome unknown');
      error.code = 'REQUEST_OUTCOME_UNKNOWN_NO_RETRY';
      error.request_executed = 'UNKNOWN';
      throw error;
    },
    estimateCostRub: () => 0.02,
    now: () => '2026-08-27T13:00:00.000Z',
    uid: (() => { let n = 0; return () => n++ === 0 ? 'batch-job-1' : `req-${n}`; })()
  });

  await runtime.handle(startCommand({ phrases: ['alpha'] }));
  const first = await runtime.handle({ action: 'next', jobId: 'batch-job-1' });
  assert.equal(first.envelope.request_executed, 'UNKNOWN');
  assert.equal(first.envelope.progress.outcome_unknown, 1);
  assert.equal(calls, 1);

  const second = await runtime.handle({ action: 'next', jobId: 'batch-job-1' });
  assert.equal(second.envelope.reason, 'JOB_COMPLETED');
  assert.equal(calls, 1);
});

test('known terminal provider failure advances queue without automatic retry', async () => {
  const Factory = loadFactory();
  const storage = memoryStorage();
  let calls = 0;
  const runtime = Factory.create({
    storage,
    workerSessionId: 'worker-A',
    executeWordstat: async (_command, metadata) => {
      calls += 1;
      return {
        ok: false,
        request_id: metadata.request_id,
        http_status: 429,
        report_envelope: {
          service: 'wordstat', operation: 'getTop', http_status: 429,
          status: 'ERROR', reason: 'QUOTA', request_executed: true, automatic_retry: false,
          result: { error: { code: 'QUOTA', message: 'quota' } }
        }
      };
    },
    estimateCostRub: () => 0.02,
    now: () => '2026-08-27T13:00:00.000Z',
    uid: (() => { let n = 0; return () => n++ === 0 ? 'batch-job-1' : `req-${n}`; })()
  });

  await runtime.handle(startCommand({ phrases: ['alpha', 'beta'] }));
  const first = await runtime.handle({ action: 'next', jobId: 'batch-job-1' });
  assert.equal(first.envelope.progress.failed_terminal, 1);
  assert.equal(first.envelope.automatic_retry, false);
  const second = await runtime.handle({ action: 'next', jobId: 'batch-job-1' });
  assert.equal(second.envelope.progress.failed_terminal, 2);
  assert.equal(calls, 2);
});

test('pause/resume/cancel/status are durable and never call provider', async () => {
  const Factory = loadFactory();
  const storage = memoryStorage();
  let calls = 0;
  const runtime = Factory.create({
    storage,
    workerSessionId: 'worker-A',
    executeWordstat: async () => { calls += 1; return {}; },
    estimateCostRub: () => 0.02,
    now: () => '2026-08-27T13:00:00.000Z',
    uid: () => 'batch-job-1'
  });

  await runtime.handle(startCommand());
  assert.equal((await runtime.handle({ action: 'pause', jobId: 'batch-job-1' })).envelope.progress.status, 'PAUSED');
  assert.equal((await runtime.handle({ action: 'status', jobId: 'batch-job-1' })).envelope.progress.status, 'PAUSED');
  assert.equal((await runtime.handle({ action: 'resume', jobId: 'batch-job-1' })).envelope.progress.status, 'RUNNING');
  assert.equal((await runtime.handle({ action: 'cancel', jobId: 'batch-job-1' })).envelope.progress.status, 'CANCELLED');
  assert.equal(calls, 0);
});

test('recovery marks prior worker REQUEST_STARTED as unknown before any new work', async () => {
  const Factory = loadFactory();
  const storage = memoryStorage();
  let calls = 0;
  const runtimeA = Factory.create({
    storage,
    workerSessionId: 'worker-A',
    executeWordstat: async () => {
      calls += 1;
      const error = new Error('simulate worker loss');
      error.request_executed = 'UNKNOWN';
      throw error;
    },
    estimateCostRub: () => 0.02,
    now: () => '2026-08-27T13:00:00.000Z',
    uid: (() => { let n = 0; return () => n++ === 0 ? 'batch-job-1' : `req-${n}`; })()
  });
  await runtimeA.handle(startCommand({ phrases: ['alpha', 'beta'] }));
  await runtimeA.handle({ action: 'next', jobId: 'batch-job-1' });

  const runtimeB = Factory.create({
    storage,
    workerSessionId: 'worker-B',
    executeWordstat: async () => { calls += 1; return {}; },
    estimateCostRub: () => 0.02,
    now: () => '2026-08-27T13:01:00.000Z',
    uid: () => 'unused'
  });
  const recovered = await runtimeB.recoverAll();
  assert.equal(recovered[0].progress.outcome_unknown, 1);
  assert.equal(calls, 1);
});
