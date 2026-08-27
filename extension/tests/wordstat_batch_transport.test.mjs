import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');

function loadShared(files) {
  const ctx = {
    console, JSON, Object, Array, Set, String, Number, Boolean, RegExp, Date, Error, Math,
    globalThis: null
  };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  for (const file of files) {
    vm.runInContext(fs.readFileSync(path.join(src, file), 'utf8'), ctx, { filename: file });
  }
  return ctx;
}

function batchStartText() {
  return 'WORDSTAT_BATCH_API_V1\n' + JSON.stringify({
    action: 'start', phrases: ['alpha'], numPhrases: 100,
    regions: ['225'], devices: ['DEVICE_ALL'], maxRequests: 1, maxCostRub: 1
  });
}

test('batch remains a Wordstat orchestration protocol and is not a sixth service', () => {
  const ctx = loadShared(['shared/service_registry.js', 'shared/wordstat_batch_protocol.js']);
  const text = batchStartText();
  assert.equal(ctx.YMBServiceRegistry.DEFINITIONS.length, 5);
  assert.equal(ctx.YMBServiceRegistry.detect(text), null);
  const command = ctx.WordstatBatchProtocol.parseCommand(text);
  const envelope = ctx.WordstatBatchProtocol.buildResultEnvelope({ command, jobId: 'job-1' });
  assert.equal(envelope.service, 'wordstat');
  assert.equal(envelope.operation, 'batch.start');
});

test('transport helper recognizes batch as semantic wordstat without mutating registry', () => {
  const transportPath = path.join(src, 'shared/wordstat_batch_transport.js');
  assert.equal(fs.existsSync(transportPath), true, 'wordstat_batch_transport.js must exist');
  const ctx = loadShared([
    'shared/service_registry.js',
    'shared/block_command_discovery.js',
    'shared/wordstat_batch_protocol.js',
    'shared/wordstat_batch_transport.js'
  ]);
  const before = ctx.YMBServiceRegistry.DEFINITIONS.length;
  const detected = ctx.YMBWordstatBatchTransport.detect(batchStartText(), ctx.YMBServiceRegistry);
  assert.equal(detected.service, 'wordstat');
  assert.equal(detected.batch, true);
  assert.equal(detected.prefix, 'WORDSTAT_BATCH_API_V1');
  assert.equal(ctx.YMBServiceRegistry.DEFINITIONS.length, before);
  assert.equal(ctx.YMBServiceRegistry.detect(batchStartText()), null);
});

test('manual discovery can merge ordinary Wordstat and batch commands in source order', () => {
  const transportPath = path.join(src, 'shared/wordstat_batch_transport.js');
  assert.equal(fs.existsSync(transportPath), true, 'wordstat_batch_transport.js must exist');
  const ctx = loadShared([
    'shared/service_registry.js',
    'shared/block_command_discovery.js',
    'shared/wordstat_batch_protocol.js',
    'shared/wordstat_batch_transport.js'
  ]);
  const text = [
    'WORDSTAT_API_V1\n{"method":"getTop","phrase":"ordinary","numPhrases":10,"regions":["225"],"devices":["DEVICE_ALL"]}',
    batchStartText()
  ].join('\n\n');
  const items = ctx.YMBWordstatBatchTransport.discover(text, ctx.YMBBlockCommandDiscovery, ctx.YMBServiceRegistry);
  assert.equal(items.length, 2);
  assert.equal(items[0].prefix, 'WORDSTAT_API_V1');
  assert.equal(items[0].batch, false);
  assert.equal(items[1].prefix, 'WORDSTAT_BATCH_API_V1');
  assert.equal(items[1].batch, true);
  assert.equal(items[1].service, 'wordstat');
});

test('autorun protocol selection accepts batch only for active Wordstat', () => {
  const transportPath = path.join(src, 'shared/wordstat_batch_transport.js');
  assert.equal(fs.existsSync(transportPath), true, 'wordstat_batch_transport.js must exist');
  const ctx = loadShared([
    'shared/service_registry.js',
    'shared/wordstat_batch_protocol.js',
    'shared/wordstat_batch_transport.js'
  ]);
  const ordinary = { id: 'ordinary' };
  assert.equal(ctx.YMBWordstatBatchTransport.protocolForText(batchStartText(), 'wordstat', ordinary), ctx.WordstatBatchProtocol);
  assert.equal(ctx.YMBWordstatBatchTransport.protocolForText(batchStartText(), 'search', ordinary), null);
  assert.equal(ctx.YMBWordstatBatchTransport.protocolForText('WORDSTAT_API_V1\n{}', 'wordstat', ordinary), ordinary);
});

test('manifest exposes batch protocol and transport helper to the existing content transport', () => {
  const manifest = JSON.parse(fs.readFileSync(path.join(src, 'manifest.json'), 'utf8'));
  const scripts = manifest.content_scripts?.[0]?.js || [];
  const protocolIndex = scripts.indexOf('shared/wordstat_batch_protocol.js');
  const transportIndex = scripts.indexOf('shared/wordstat_batch_transport.js');
  const contentIndex = scripts.indexOf('content_script.js');
  assert.ok(protocolIndex >= 0, 'batch protocol must be loaded in content context');
  assert.ok(transportIndex > protocolIndex, 'batch transport must load after batch protocol');
  assert.ok(contentIndex > transportIndex, 'content script must load after batch transport');
});

test('worker wiring reuses batch runtime, existing Wordstat executor and existing outbox lifecycle', () => {
  const worker = fs.readFileSync(path.join(src, 'service_worker.js'), 'utf8');
  for (const dependency of [
    'shared/provider_batch_job_model.js',
    'shared/wordstat_batch_protocol.js',
    'shared/wordstat_batch_runtime.js',
    'shared/wordstat_batch_transport.js'
  ]) assert.ok(worker.includes(dependency), `worker must load ${dependency}`);
  for (const marker of [
    'YMBWordstatBatchRuntime.create',
    'executeWordstatBatchCommand',
    'YMBWordstatBatchTransport.discover',
    'executeWordstatCommand',
    'WordstatBatchProtocol.formatResultEnvelope',
    'putOutbox'
  ]) assert.ok(worker.includes(marker), `worker transport marker missing: ${marker}`);
});

test('content autorun scanner delegates command selection to batch-aware transport helper', () => {
  const content = fs.readFileSync(path.join(src, 'content_script.js'), 'utf8');
  assert.ok(content.includes('YMBWordstatBatchTransport.protocolForText'));
  assert.ok(content.includes('WordstatBatchProtocol'));
});
