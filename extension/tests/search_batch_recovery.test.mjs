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
    console, JSON, Object, Array, Set, String, Number, Boolean, RegExp, Date, Error, Math, URL,
    crypto: { randomUUID: () => 'uuid-fixed' }, globalThis: null
  };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  for (const file of [
    'shared/provider_batch_job_model.js',
    'shared/search_protocol.js',
    'shared/search_batch_protocol.js',
    'shared/search_batch_projection.js',
    'shared/search_batch_runtime.js'
  ]) {
    vm.runInContext(fs.readFileSync(path.join(src, file), 'utf8'), ctx, { filename: file });
  }
  return ctx.YMBSearchBatchRuntime;
}

function memoryStorage() {
  const state = {};
  return {
    state,
    async get(key) { return clone(state[key]); },
    async set(key, value) { state[key] = clone(value); }
  };
}

function startCommand(jobId, queries) {
  return {
    action: 'start',
    jobId,
    queries,
    searchType: 'SEARCH_TYPE_RU',
    region: '225',
    groupsOnPage: 10,
    maxRequests: queries.length,
    maxCostRub: Math.max(1, queries.length),
    confirmBillable: true
  };
}

function okResult(command, requestId) {
  return {
    ok: true,
    request_id: requestId,
    request_executed: true,
    report_envelope: {
      service: 'search',
      operation: 'search',
      http_status: 200,
      request_executed: true,
      automatic_retry: false,
      command,
      result: {
        results: [
          { rank: 1, url: `https://${command.queryText}.test/`, domain: `${command.queryText}.test`, title: command.queryText }
        ],
        result_count: 1,
        response_format: 'FORMAT_XML'
      }
    }
  };
}

test('pause/resume plus a new worker session preserves completed evidence and never replays it', async () => {
  const Factory = loadFactory();
  const storage = memoryStorage();
  const calls = [];
  let requestNo = 0;
  const executeSearch = async (command) => {
    calls.push(command.queryText);
    requestNo += 1;
    return okResult(command, `req-${requestNo}`);
  };

  const runtimeA = Factory.create({
    storage,
    workerSessionId: 'worker-A',
    executeSearch,
    estimateCostRub: () => 0.488,
    now: () => '2026-08-28T05:00:00.000Z',
    uid: (() => { let n = 0; return () => `a-${++n}`; })()
  });

  await runtimeA.handle(startCommand('recovery-job', ['alpha', 'beta', 'gamma']));
  await runtimeA.handle({ action: 'next', jobId: 'recovery-job' });
  assert.deepEqual(calls, ['alpha']);
  assert.equal((await runtimeA.handle({ action: 'pause', jobId: 'recovery-job' })).envelope.progress.status, 'PAUSED');
  assert.equal((await runtimeA.handle({ action: 'resume', jobId: 'recovery-job' })).envelope.progress.status, 'RUNNING');
  await runtimeA.handle({ action: 'next', jobId: 'recovery-job' });
  assert.deepEqual(calls, ['alpha', 'beta']);

  const runtimeB = Factory.create({
    storage,
    workerSessionId: 'worker-B',
    executeSearch,
    estimateCostRub: () => 0.488,
    now: () => '2026-08-28T05:01:00.000Z',
    uid: (() => { let n = 0; return () => `b-${++n}`; })()
  });
  const recovered = await runtimeB.recoverAll();
  assert.equal(recovered.length, 1);
  assert.equal(recovered[0].progress.succeeded, 2);
  assert.equal(recovered[0].progress.pending, 1);

  const final = await runtimeB.handle({ action: 'next', jobId: 'recovery-job' });
  assert.deepEqual(calls, ['alpha', 'beta', 'gamma']);
  assert.equal(final.envelope.progress.succeeded, 3);
  assert.equal(final.envelope.progress.requests_started, 3);
});

test('unknown outcome survives worker-session recovery and blocks all later paid work without replay', async () => {
  const Factory = loadFactory();
  const storage = memoryStorage();
  let calls = 0;
  const runtimeA = Factory.create({
    storage,
    workerSessionId: 'worker-A',
    executeSearch: async () => {
      calls += 1;
      const error = new Error('controlled unknown outcome');
      error.code = 'REQUEST_OUTCOME_UNKNOWN_NO_RETRY';
      error.request_executed = 'UNKNOWN';
      throw error;
    },
    estimateCostRub: () => 0.488,
    now: () => '2026-08-28T05:02:00.000Z',
    uid: (() => { let n = 0; return () => `u-${++n}`; })()
  });

  await runtimeA.handle(startCommand('unknown-job', ['alpha', 'beta']));
  const first = await runtimeA.handle({ action: 'next', jobId: 'unknown-job' });
  assert.equal(first.envelope.request_executed, 'UNKNOWN');
  assert.equal(calls, 1);

  const runtimeB = Factory.create({
    storage,
    workerSessionId: 'worker-B',
    executeSearch: async () => { calls += 1; throw new Error('must not run'); },
    estimateCostRub: () => 0.488,
    now: () => '2026-08-28T05:03:00.000Z',
    uid: () => 'unused'
  });
  const recovered = await runtimeB.recoverAll();
  assert.equal(recovered[0].progress.outcome_unknown, 1);
  assert.equal(recovered[0].progress.next_safe_action, 'RECONCILE_UNKNOWN');
  const second = await runtimeB.handle({ action: 'next', jobId: 'unknown-job' });
  assert.equal(second.envelope.request_executed, false);
  assert.equal(second.envelope.reason, 'OUTCOME_UNKNOWN_REQUIRES_RECONCILIATION');
  assert.equal(calls, 1);
});

test('duplicate start is rejected locally and never contacts provider', async () => {
  const Factory = loadFactory();
  const storage = memoryStorage();
  let calls = 0;
  const runtime = Factory.create({
    storage,
    workerSessionId: 'worker-A',
    executeSearch: async () => { calls += 1; return {}; },
    estimateCostRub: () => 0.488,
    now: () => '2026-08-28T05:04:00.000Z',
    uid: () => 'unused'
  });
  const command = startCommand('duplicate-job', ['alpha']);
  await runtime.handle(command);
  await assert.rejects(runtime.handle(command), (error) => error?.code === 'SEARCH_BATCH_JOB_ALREADY_EXISTS');
  assert.equal(calls, 0);
});

test('concurrent duplicate next is rejected while an item is active and cannot create a second paid boundary', async () => {
  const Factory = loadFactory();
  const storage = memoryStorage();
  let calls = 0;
  let releaseFirst;
  let enteredFirst;
  const firstEntered = new Promise((resolve) => { enteredFirst = resolve; });
  const release = new Promise((resolve) => { releaseFirst = resolve; });

  const runtime = Factory.create({
    storage,
    workerSessionId: 'worker-A',
    executeSearch: async (command, metadata) => {
      calls += 1;
      if (calls === 1) {
        enteredFirst();
        await release;
      }
      return okResult(command, metadata.request_id);
    },
    estimateCostRub: () => 0.488,
    now: () => '2026-08-28T05:05:00.000Z',
    uid: (() => { let n = 0; return () => `d-${++n}`; })()
  });

  await runtime.handle(startCommand('double-next-job', ['alpha', 'beta']));
  const first = runtime.handle({ action: 'next', jobId: 'double-next-job' });
  await firstEntered;
  const duplicate = await runtime.handle({ action: 'next', jobId: 'double-next-job' });
  assert.equal(duplicate.envelope.request_executed, false);
  assert.equal(duplicate.envelope.reason, 'ITEM_ACTIVE');
  assert.equal(calls, 1);
  releaseFirst();
  const completed = await first;
  assert.equal(completed.envelope.progress.succeeded, 1);
  assert.equal(completed.envelope.progress.pending, 1);
  assert.equal(calls, 1);
});
