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

test('manifest exposes batch classifier before the unchanged content transport', () => {
  const manifest = JSON.parse(fs.readFileSync(path.join(src, 'manifest.json'), 'utf8'));
  const scripts = manifest.content_scripts?.[0]?.js || [];
  const ordinaryIndex = scripts.indexOf('shared/wordstat_protocol.js');
  const protocolIndex = scripts.indexOf('shared/wordstat_batch_protocol.js');
  const transportIndex = scripts.indexOf('shared/wordstat_batch_transport.js');
  const bridgeIndex = scripts.indexOf('shared/wordstat_batch_content_bridge.js');
  const contentIndex = scripts.indexOf('content_script.js');
  assert.ok(ordinaryIndex >= 0);
  assert.ok(protocolIndex > ordinaryIndex, 'batch protocol must load after ordinary Wordstat protocol');
  assert.ok(transportIndex > protocolIndex, 'batch transport must load after batch protocol');
  assert.ok(bridgeIndex > transportIndex, 'content bridge must load after batch transport');
  assert.ok(contentIndex > bridgeIndex, 'accepted content script must load after the batch-aware proxy');
});

test('content bridge extends only Wordstat command detection and keeps registry unchanged', () => {
  const ctx = loadShared([
    'shared/product.js',
    'shared/service_registry.js',
    'shared/wordstat_protocol.js',
    'shared/wordstat_batch_protocol.js',
    'shared/wordstat_batch_transport.js',
    'shared/wordstat_batch_content_bridge.js'
  ]);
  assert.equal(ctx.YMBServiceRegistry.DEFINITIONS.length, 5);
  assert.equal(ctx.WordstatProtocol.isCommandText(batchStartText()), true);
  assert.equal(ctx.WordstatProtocol.isCommandText('WORDSTAT_API_V1\n{}'), true);
  assert.equal(ctx.YMBWordstatBatchTransport.protocolForText(batchStartText(), 'search', ctx.YMBWordstatBatchContentBridge.ordinaryProtocol), null);
});

test('worker bootstrap loads batch model/runtime before accepted worker and adapter after it', () => {
  const bootstrap = fs.readFileSync(path.join(src, 'phase3_service_worker_bootstrap.js'), 'utf8');
  const acceptedWorkerIndex = bootstrap.indexOf('importScripts("service_worker_bootstrap.js")');
  assert.ok(acceptedWorkerIndex > 0);
  for (const dependency of [
    'shared/provider_batch_job_model.js',
    'shared/wordstat_batch_protocol.js',
    'shared/wordstat_batch_runtime.js',
    'shared/wordstat_batch_transport.js'
  ]) {
    const index = bootstrap.indexOf(dependency);
    assert.ok(index >= 0 && index < acceptedWorkerIndex, `${dependency} must load before accepted worker`);
  }
  const adapterIndex = bootstrap.indexOf('wordstat_batch_worker_transport.js');
  assert.ok(adapterIndex > acceptedWorkerIndex, 'batch worker adapter must load after accepted worker');
});

test('worker adapter reuses existing Wordstat executor, policy, run state and outbox lifecycle', () => {
  const adapter = fs.readFileSync(path.join(src, 'wordstat_batch_worker_transport.js'), 'utf8');
  for (const marker of [
    'YMBWordstatBatchRuntime.create',
    'executeWordstatBatchCommand',
    'YMBWordstatBatchTransport.discover',
    'executeWordstatCommand',
    'WordstatBatchProtocol.formatResultEnvelope',
    'policyDecisionForService',
    'publicCapability',
    'getWordstatPolicy',
    'getAutoRun',
    'patchAutoRun',
    'putOutbox',
    'baseExecuteManualBlock',
    'baseHandleAutoCommand'
  ]) assert.ok(adapter.includes(marker), `worker transport marker missing: ${marker}`);
  assert.equal(adapter.includes('YMBServiceRegistry.DEFINITIONS ='), false);
});

test('first transport slice is explicit one-checkpoint execution, not a hidden advance loop', () => {
  const adapter = fs.readFileSync(path.join(src, 'wordstat_batch_worker_transport.js'), 'utf8');
  assert.ok(adapter.includes('batchRuntime.handle(command, metadata)'));
  assert.equal(adapter.includes('while (true)'), false);
  assert.equal(adapter.includes('setInterval('), false);
});
