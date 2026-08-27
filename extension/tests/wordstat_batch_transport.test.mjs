import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');

function loadShared(files, seed = {}) {
  const ctx = {
    console, JSON, Object, Array, Set, Map, String, Number, Boolean, RegExp, Date, Error, Math,
    ...seed,
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

test('manifest exposes batch detection after preserving the accepted content runtime', () => {
  const manifest = JSON.parse(fs.readFileSync(path.join(src, 'manifest.json'), 'utf8'));
  const scripts = manifest.content_scripts?.[0]?.js || [];
  const protocolIndex = scripts.indexOf('shared/wordstat_batch_protocol.js');
  const transportIndex = scripts.indexOf('shared/wordstat_batch_transport.js');
  const contentIndex = scripts.indexOf('content_script.js');
  const integrationIndex = scripts.indexOf('wordstat_batch_content_integration.js');
  assert.ok(protocolIndex >= 0, 'batch protocol must be loaded in content context');
  assert.ok(transportIndex > protocolIndex, 'batch transport must load after batch protocol');
  assert.ok(contentIndex > transportIndex, 'accepted content runtime must load after batch transport prerequisites');
  assert.ok(integrationIndex > contentIndex, 'batch content adapter must wrap the accepted content runtime after it loads');
});

test('content adapter preserves ordinary Wordstat detection and adds batch detection only for Wordstat', () => {
  const ordinaryWordstat = {
    marker: 'ordinary-wordstat',
    isCommandText(text) { return String(text || '').trim().startsWith('WORDSTAT_API_V1'); }
  };
  const search = {
    marker: 'search',
    isCommandText(text) { return String(text || '').trim().startsWith('SEARCH_API_V1'); }
  };
  const ctx = loadShared([
    'shared/wordstat_batch_protocol.js',
    'shared/wordstat_batch_transport.js'
  ], {
    protocolForService(service) {
      if (service === 'wordstat') return ordinaryWordstat;
      if (service === 'search') return search;
      return null;
    }
  });
  vm.runInContext(fs.readFileSync(path.join(src, 'wordstat_batch_content_integration.js'), 'utf8'), ctx, { filename: 'wordstat_batch_content_integration.js' });
  const wordstat = ctx.protocolForService('wordstat');
  assert.equal(wordstat.marker, 'ordinary-wordstat');
  assert.equal(wordstat.isCommandText('WORDSTAT_API_V1\n{}'), true);
  assert.equal(wordstat.isCommandText(batchStartText()), true);
  assert.equal(wordstat.isCommandText('not a command'), false);
  assert.equal(ctx.protocolForService('search'), search);
  assert.equal(ctx.protocolForService('search').isCommandText(batchStartText()), false);
});

test('worker bootstrap loads batch prerequisites before base worker and adapter after accepted Phase 5 runtime', () => {
  const bootstrap = fs.readFileSync(path.join(src, 'phase3_service_worker_bootstrap.js'), 'utf8');
  for (const dependency of [
    'shared/provider_batch_job_model.js',
    'shared/wordstat_batch_protocol.js',
    'shared/wordstat_batch_runtime.js',
    'shared/wordstat_batch_transport.js'
  ]) assert.ok(bootstrap.includes(dependency), `bootstrap must load ${dependency}`);
  assert.ok(bootstrap.indexOf('shared/wordstat_batch_runtime.js') < bootstrap.indexOf('service_worker_bootstrap.js'));
  assert.ok(bootstrap.indexOf('webmaster_worker_runtime.js') < bootstrap.indexOf('wordstat_batch_worker_integration.js'));
});

test('worker adapter reuses existing Wordstat executor, policy, outbox and delivery lifecycle', () => {
  const integration = fs.readFileSync(path.join(src, 'wordstat_batch_worker_integration.js'), 'utf8');
  const baseWorker = fs.readFileSync(path.join(src, 'service_worker.js'), 'utf8');
  for (const marker of [
    'YMBWordstatBatchRuntime.create',
    'executeWordstatBatchCommand',
    'YMBWordstatBatchTransport.discover',
    'executeWordstatCommand',
    'getWordstatPolicy',
    'policyDecisionForService',
    'putOutbox',
    'baseExecuteManualBlock',
    'baseHandleAutoCommand',
    'globalThis.executeManualBlock = batchAwareManualBlock',
    'globalThis.handleAutoCommand = batchAwareAutoCommand'
  ]) assert.ok(integration.includes(marker), `batch worker adapter marker missing: ${marker}`);
  for (const marker of ['putOutbox', 'outboxOwnerFence', 'completeDelivery', 'WS_EXECUTE_MANUAL_BLOCK', 'WS_AUTO_COMMAND']) {
    assert.ok(baseWorker.includes(marker), `accepted worker lifecycle marker missing: ${marker}`);
  }
});

test('classic worker global handler rebinding is visible to an already-defined message dispatcher', async () => {
  const ctx = { globalThis: null, Promise };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  vm.runInContext(`
    "use strict";
    async function executeManualBlock() { return "base"; }
    async function handleMessage() { return executeManualBlock(); }
    globalThis.handleMessage = handleMessage;
  `, ctx);
  assert.equal(await ctx.handleMessage(), 'base');
  ctx.executeManualBlock = async () => 'batch-aware';
  assert.equal(await ctx.handleMessage(), 'batch-aware');
});

test('batch transport integration scripts are syntactically valid before Chrome loads them', () => {
  for (const file of [
    'shared/wordstat_batch_transport.js',
    'wordstat_batch_content_integration.js',
    'wordstat_batch_worker_integration.js',
    'phase3_service_worker_bootstrap.js'
  ]) {
    const source = fs.readFileSync(path.join(src, file), 'utf8');
    assert.doesNotThrow(() => new vm.Script(source, { filename: file }), `${file} must parse as a classic script`);
  }
});
