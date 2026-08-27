import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');

function loadProtocol() {
  const ctx = { console, JSON, Object, Array, Set, String, Number, Boolean, RegExp, Date, Error, Math, globalThis: null };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(src, 'shared/wordstat_batch_protocol.js'), 'utf8'), ctx, { filename: 'wordstat_batch_protocol.js' });
  return ctx.WordstatBatchProtocol;
}

test('start normalizes a bounded getTop seed manifest', () => {
  const protocol = loadProtocol();
  const command = protocol.parseCommand(`WORDSTAT_BATCH_API_V1 ${JSON.stringify({
    action: 'start',
    phrases: ['alpha', 'beta'],
    numPhrases: 250,
    regions: ['225'],
    devices: ['DEVICE_ALL'],
    maxRequests: 20,
    maxCostRub: 1
  })}`);
  assert.equal(command.action, 'start');
  assert.deepEqual([...command.phrases], ['alpha', 'beta']);
  assert.equal(command.numPhrases, 250);
  assert.equal(command.maxRequests, 20);
  assert.equal(command.maxCostRub, 1);
});

test('start rejects empty, oversized and malformed phrase manifests', () => {
  const protocol = loadProtocol();
  assert.throws(() => protocol.normalizeCommand({ action: 'start', phrases: [] }), (e) => e.code === 'INVALID_BATCH_PHRASES');
  assert.throws(() => protocol.normalizeCommand({ action: 'start', phrases: Array.from({ length: 501 }, (_, i) => `p${i}`) }), (e) => e.code === 'TOO_MANY_BATCH_PHRASES');
  assert.throws(() => protocol.normalizeCommand({ action: 'start', phrases: [''] }), (e) => e.code === 'INVALID_BATCH_PHRASE');
});

test('next/status/pause/resume/cancel require jobId', () => {
  const protocol = loadProtocol();
  for (const action of ['next', 'status', 'pause', 'resume', 'cancel']) {
    assert.throws(() => protocol.normalizeCommand({ action }), (e) => e.code === 'MISSING_BATCH_JOB_ID');
    assert.equal(protocol.normalizeCommand({ action, jobId: 'job-1' }).jobId, 'job-1');
  }
});

test('unsupported action fails closed', () => {
  const protocol = loadProtocol();
  assert.throws(() => protocol.normalizeCommand({ action: 'runEverythingForever', jobId: 'x' }), (e) => e.code === 'UNSUPPORTED_BATCH_ACTION');
});

test('result envelope is explicitly batch-scoped and preserves progress/provider truth', () => {
  const protocol = loadProtocol();
  const envelope = protocol.buildResultEnvelope({
    command: { action: 'next', jobId: 'job-1' },
    jobId: 'job-1',
    status: 'OK',
    progress: { total: 2, succeeded: 1, pending: 1 },
    item: { item_id: 'i1', status: 'SUCCEEDED' },
    providerResult: { service: 'wordstat', operation: 'getTop', http_status: 200, request_executed: true },
    requestExecuted: true,
    automaticRetry: false
  });
  assert.equal(envelope.service, 'wordstat');
  assert.equal(envelope.operation, 'batch.next');
  assert.equal(envelope.job_id, 'job-1');
  assert.equal(envelope.request_executed, true);
  assert.equal(envelope.automatic_retry, false);
  assert.equal(envelope.provider_result.http_status, 200);
  assert.match(protocol.formatResultEnvelope(envelope), /^WORDSTAT_BATCH_RESULT_V1\n/);
});
