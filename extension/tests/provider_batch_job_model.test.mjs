import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');

function loadModel() {
  const ctx = {
    console, JSON, Object, Array, Set, Map, String, Number, Boolean, RegExp, Date, Error, Math,
    globalThis: null
  };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  vm.runInContext(
    fs.readFileSync(path.join(src, 'shared/provider_batch_job_model.js'), 'utf8'),
    ctx,
    { filename: 'provider_batch_job_model.js' }
  );
  return ctx.YMBProviderBatchJobModel;
}

const command = (phrase, extra = {}) => ({
  method: 'getTop',
  phrase,
  numPhrases: 100,
  regions: ['225'],
  devices: ['DEVICE_ALL'],
  ...extra
});

const NOW = '2026-08-27T12:30:00.000Z';

test('stable fingerprint is independent of object key order', () => {
  const model = loadModel();
  const a = { method: 'getTop', phrase: 'alpha', regions: ['225'], nested: { b: 2, a: 1 } };
  const b = { nested: { a: 1, b: 2 }, regions: ['225'], phrase: 'alpha', method: 'getTop' };
  assert.equal(model.commandFingerprint(a), model.commandFingerprint(b));
});

test('createJob removes exact duplicate commands but preserves distinct commands', () => {
  const model = loadModel();
  const job = model.createJob({
    jobId: 'job-1',
    service: 'wordstat',
    commands: [command('alpha'), command('alpha'), command('beta')],
    limits: { maxRequests: 10, maxCostRub: 100 },
    now: NOW
  });
  assert.equal(job.items.length, 2);
  assert.equal(job.input_count, 3);
  assert.equal(job.duplicate_count, 1);
  assert.equal(model.progress(job).pending, 2);
});

test('successful item is never reclaimed on normal progress', () => {
  const model = loadModel();
  let job = model.createJob({ jobId: 'job-2', service: 'wordstat', commands: [command('alpha'), command('beta')], now: NOW });
  ({ job } = model.claimNext(job, { actorId: 'worker-a', now: NOW }));
  const firstId = job.active_item_id;
  job = model.markRequestStarted(job, firstId, { requestId: 'req-1', workerSessionId: 'worker-a', estimatedCostRub: 0.02, now: NOW });
  job = model.markSucceeded(job, firstId, { resultRef: 'result-1', requestExecuted: true, now: NOW });
  const firstFingerprint = job.items.find((item) => item.item_id === firstId).fingerprint;
  ({ job } = model.claimNext(job, { actorId: 'worker-a', now: NOW }));
  assert.notEqual(job.active_item_id, firstId);
  assert.equal(job.items.find((item) => item.fingerprint === firstFingerprint).status, model.ITEM_STATUSES.SUCCEEDED);
});

test('stale CLAIMED item is safely released to PENDING during recovery', () => {
  const model = loadModel();
  let job = model.createJob({ jobId: 'job-3', service: 'wordstat', commands: [command('alpha')], now: NOW });
  ({ job } = model.claimNext(job, { actorId: 'worker-old', now: NOW }));
  assert.equal(model.progress(job).claimed, 1);
  job = model.recover(job, { workerSessionId: 'worker-new', now: NOW });
  assert.equal(model.progress(job).pending, 1);
  assert.equal(job.active_item_id, null);
});

test('stale REQUEST_STARTED becomes OUTCOME_UNKNOWN and is never auto-replayed', () => {
  const model = loadModel();
  let job = model.createJob({ jobId: 'job-4', service: 'wordstat', commands: [command('alpha')], now: NOW });
  ({ job } = model.claimNext(job, { actorId: 'worker-old', now: NOW }));
  const itemId = job.active_item_id;
  job = model.markRequestStarted(job, itemId, { requestId: 'req-unknown', workerSessionId: 'worker-old', estimatedCostRub: 0.02, now: NOW });
  job = model.recover(job, { workerSessionId: 'worker-new', now: NOW });
  const item = job.items.find((record) => record.item_id === itemId);
  assert.equal(item.status, model.ITEM_STATUSES.OUTCOME_UNKNOWN);
  assert.equal(job.active_item_id, null);
  const claimed = model.claimNext(job, { actorId: 'worker-new', now: NOW });
  assert.equal(claimed.item, null);
  assert.equal(claimed.job.items[0].status, model.ITEM_STATUSES.OUTCOME_UNKNOWN);
});

test('pause and resume do not replay completed items', () => {
  const model = loadModel();
  let job = model.createJob({ jobId: 'job-5', service: 'wordstat', commands: [command('alpha'), command('beta')], now: NOW });
  ({ job } = model.claimNext(job, { actorId: 'worker-a', now: NOW }));
  const firstId = job.active_item_id;
  job = model.markRequestStarted(job, firstId, { requestId: 'req-1', workerSessionId: 'worker-a', estimatedCostRub: 0, now: NOW });
  job = model.markSucceeded(job, firstId, { resultRef: 'result-1', now: NOW });
  job = model.pause(job, { reason: 'owner_pause', now: NOW });
  assert.equal(model.claimNext(job, { actorId: 'worker-a', now: NOW }).item, null);
  job = model.resume(job, { now: NOW });
  ({ job } = model.claimNext(job, { actorId: 'worker-a', now: NOW }));
  assert.notEqual(job.active_item_id, firstId);
  assert.equal(model.progress(job).succeeded, 1);
});

test('request limit prevents another item from being claimed', () => {
  const model = loadModel();
  let job = model.createJob({
    jobId: 'job-6', service: 'wordstat', commands: [command('alpha'), command('beta')],
    limits: { maxRequests: 1, maxCostRub: 100 }, now: NOW
  });
  ({ job } = model.claimNext(job, { actorId: 'worker-a', now: NOW }));
  const firstId = job.active_item_id;
  job = model.markRequestStarted(job, firstId, { requestId: 'req-1', workerSessionId: 'worker-a', estimatedCostRub: 0, now: NOW });
  job = model.markSucceeded(job, firstId, { resultRef: 'result-1', now: NOW });
  const next = model.claimNext(job, { actorId: 'worker-a', nextEstimatedCostRub: 0, now: NOW });
  assert.equal(next.item, null);
  assert.equal(next.reason, 'REQUEST_LIMIT_REACHED');
  assert.equal(model.progress(next.job).pending, 1);
});

test('cost limit is checked before claiming the next paid item', () => {
  const model = loadModel();
  let job = model.createJob({
    jobId: 'job-7', service: 'wordstat', commands: [command('alpha'), command('beta')],
    limits: { maxRequests: 10, maxCostRub: 0.03 }, now: NOW
  });
  ({ job } = model.claimNext(job, { actorId: 'worker-a', nextEstimatedCostRub: 0.02, now: NOW }));
  const firstId = job.active_item_id;
  job = model.markRequestStarted(job, firstId, { requestId: 'req-1', workerSessionId: 'worker-a', estimatedCostRub: 0.02, now: NOW });
  job = model.markSucceeded(job, firstId, { resultRef: 'result-1', now: NOW });
  const next = model.claimNext(job, { actorId: 'worker-a', nextEstimatedCostRub: 0.02, now: NOW });
  assert.equal(next.item, null);
  assert.equal(next.reason, 'COST_LIMIT_REACHED');
});

test('cancel marks only not-started work cancelled and does not falsify an in-flight outcome', () => {
  const model = loadModel();
  let job = model.createJob({ jobId: 'job-8', service: 'wordstat', commands: [command('alpha'), command('beta')], now: NOW });
  ({ job } = model.claimNext(job, { actorId: 'worker-a', now: NOW }));
  const firstId = job.active_item_id;
  job = model.markRequestStarted(job, firstId, { requestId: 'req-1', workerSessionId: 'worker-a', estimatedCostRub: 0, now: NOW });
  job = model.cancel(job, { reason: 'owner_cancel', now: NOW });
  const first = job.items.find((item) => item.item_id === firstId);
  const second = job.items.find((item) => item.item_id !== firstId);
  assert.equal(first.status, model.ITEM_STATUSES.REQUEST_STARTED);
  assert.equal(second.status, model.ITEM_STATUSES.CANCELLED);
  assert.equal(job.status, model.JOB_STATUSES.CANCELLING);
});

test('invalid transition fails closed', () => {
  const model = loadModel();
  const job = model.createJob({ jobId: 'job-9', service: 'wordstat', commands: [command('alpha')], now: NOW });
  const itemId = job.items[0].item_id;
  assert.throws(
    () => model.markSucceeded(job, itemId, { resultRef: 'impossible', now: NOW }),
    (error) => error?.code === 'INVALID_BATCH_ITEM_TRANSITION'
  );
});
