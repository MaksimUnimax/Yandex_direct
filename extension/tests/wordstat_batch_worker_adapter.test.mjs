import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');
const clone = (value) => value == null ? value : JSON.parse(JSON.stringify(value));

function createHarness({ capabilityState = 'PRESENT', autorunEnabled = true } = {}) {
  const state = {};
  const metrics = { providerCalls: 0, policyCalls: [], baseManualCalls: 0, baseAutoCalls: 0 };
  let uidCounter = 0;

  const local = {
    async get(keys) {
      if (typeof keys === 'string') return { [keys]: clone(state[keys]) };
      const list = Array.isArray(keys) ? keys : Object.keys(keys || {});
      return Object.fromEntries(list.map((key) => [key, clone(state[key])]));
    },
    async set(values) {
      for (const [key, value] of Object.entries(values || {})) state[key] = clone(value);
    },
    async remove(keys) {
      for (const key of Array.isArray(keys) ? keys : [keys]) delete state[key];
    }
  };

  const ctx = {
    console, JSON, Object, Array, Set, String, Number, Boolean, RegExp, Date, Error, Math, Promise,
    crypto: { randomUUID: () => `crypto-${++uidCounter}` },
    chrome: { storage: { local } },
    performance: { now: () => 1 },
    globalThis: null
  };
  ctx.globalThis = ctx;
  vm.createContext(ctx);

  for (const file of [
    'shared/service_registry.js',
    'shared/block_command_discovery.js',
    'shared/run_context_model.js',
    'shared/policy_model.js',
    'shared/autorun_model.js',
    'shared/provider_batch_job_model.js',
    'shared/wordstat_batch_protocol.js',
    'shared/wordstat_batch_runtime.js',
    'shared/wordstat_batch_transport.js'
  ]) vm.runInContext(fs.readFileSync(path.join(src, file), 'utf8'), ctx, { filename: file });

  const policy = ctx.YMBPolicyModel.normalizeWordstatPolicy({
    autorun_enabled: autorunEnabled,
    manual_enabled: true,
    max_requests_per_run: 10,
    max_cost_rub_per_run: 10,
    method_cost_rub: { getTop: 0.02 }
  });

  ctx.WORKER_SESSION_ID = 'worker-A';
  ctx.KEYS = { MANUAL_OPERATIONS: 'manual_operations' };
  ctx.TERMINAL_MANUAL_STATUSES = new Set(['completed', 'error', 'cancelled']);
  ctx.clone = clone;
  ctx.nowIso = () => '2026-08-27T13:40:00.000Z';
  ctx.uid = (prefix = 'id') => `${prefix}-${++uidCounter}`;
  ctx.normalizeConversationKey = (value) => String(value || '').trim();
  ctx.storageGet = (keys) => local.get(keys);
  ctx.storageSet = (values) => local.set(values);
  ctx.getSettings = async () => ({ apiKey: capabilityState === 'PRESENT' ? 'saved' : '', folderId: 'folder' });
  ctx.getWordstatPolicy = async () => policy;
  ctx.publicCapability = () => ({ state: capabilityState });
  ctx.policyDecisionForService = (service, args) => {
    metrics.policyCalls.push({ service, channel: args.channel, method: args.method, credentialState: args.credentialState });
    return ctx.YMBPolicyModel.decisionForService(service, args);
  };
  ctx.getAutoRun = async (key) => clone(state.auto_runs?.[key] || null);
  ctx.patchAutoRun = async (key, mutate) => {
    const map = { ...(state.auto_runs || {}) };
    map[key] = clone(mutate(clone(map[key])));
    state.auto_runs = map;
    return clone(map[key]);
  };
  ctx.executeWordstatCommand = async (command, metadata) => {
    metrics.providerCalls += 1;
    return {
      ok: true,
      request_id: metadata.request_id,
      request_executed: true,
      report_envelope: {
        service: 'wordstat', operation: command.method, status: 'OK', http_status: 200,
        request_executed: true, automatic_retry: false,
        result: { phrase: command.phrase, evidence: 'provider' }
      }
    };
  };

  ctx.executeManualBlock = async () => { metrics.baseManualCalls += 1; return { ok: true, base: true }; };
  ctx.handleAutoCommand = async () => { metrics.baseAutoCalls += 1; return { ok: true, base: true }; };
  ctx.assertTabConversation = async (tabId) => {
    if (Number(tabId) !== 7) throw Object.assign(new Error('wrong owner'), { code: 'AUTO_NON_OWNER_TAB' });
    return { origin: 'https://chatgpt.com', conversation_id: 'conv-1', conversation_key: 'conv-key' };
  };
  ctx.getBinding = async () => ({ conversation_id: 'conv-1' });
  ctx.getManualMode = async () => true;
  ctx.getServiceContext = async () => ({ active_service: 'wordstat' });
  ctx.getConversationOutbox = async (key) => clone(state.outbox?.[key] || null);
  ctx.putOutbox = async (key, entry) => {
    const map = { ...(state.outbox || {}) };
    map[key] = clone(entry);
    state.outbox = map;
    return clone(map[key]);
  };
  ctx.applyPrefixToReport = async (_key, text) => ({ text, applied: false });
  ctx.formatBridgeError = ({ code, message }) => `BRIDGE_ERROR ${code}: ${message}`;
  ctx.diagnostic = async () => {};
  ctx.stageAutorunError = async (_key, _run, _tab, payload) => ({ ok: true, error_delivery: true, code: payload.code });
  ctx.publicRun = (run) => clone(run);

  vm.runInContext(fs.readFileSync(path.join(src, 'wordstat_batch_worker_transport.js'), 'utf8'), ctx, { filename: 'wordstat_batch_worker_transport.js' });

  return { ctx, state, metrics, flush: () => new Promise((resolve) => setImmediate(resolve)) };
}

function start(jobId = 'job-1') {
  return {
    action: 'start', jobId, phrases: ['alpha'], numPhrases: 100,
    regions: ['225'], devices: ['DEVICE_ALL'], maxRequests: 1, maxCostRub: 1
  };
}

test('worker adapter management actions never contact provider; one next contacts it exactly once', async () => {
  const { ctx, metrics, flush } = createHarness();
  await flush();
  const api = ctx.YMBWordstatBatchWorkerTransport;

  const started = await api.executeWordstatBatchCommand(start(), { channel: 'manual' });
  assert.equal(started.report_envelope.operation, 'batch.start');
  assert.equal(metrics.providerCalls, 0);
  await api.executeWordstatBatchCommand({ action: 'status', jobId: 'job-1' }, { channel: 'manual' });
  await api.executeWordstatBatchCommand({ action: 'pause', jobId: 'job-1' }, { channel: 'manual' });
  await api.executeWordstatBatchCommand({ action: 'resume', jobId: 'job-1' }, { channel: 'manual' });
  assert.equal(metrics.providerCalls, 0);

  const next = await api.executeWordstatBatchCommand({ action: 'next', jobId: 'job-1' }, { channel: 'manual' });
  assert.equal(metrics.providerCalls, 1);
  assert.equal(next.request_executed, true);
  assert.equal(next.report_envelope.progress.succeeded, 1);
  assert.equal(next.report_envelope.item.result_payload.result.evidence, 'provider');
});

test('credential absence is denied by existing Wordstat policy before claim/network', async () => {
  const { ctx, state, metrics, flush } = createHarness({ capabilityState: 'MISSING' });
  await flush();
  const api = ctx.YMBWordstatBatchWorkerTransport;
  await api.executeWordstatBatchCommand(start('job-denied'), { channel: 'manual' });
  const result = await api.executeWordstatBatchCommand({ action: 'next', jobId: 'job-denied' }, { channel: 'manual' });
  assert.equal(result.report_envelope.status, 'SKIPPED');
  assert.equal(result.report_envelope.reason, 'NO_CREDENTIALS');
  assert.equal(metrics.providerCalls, 0);
  assert.equal(state.ymb_wordstat_batch_jobs_v1['job-denied'].items[0].status, 'PENDING');
  assert.deepEqual(metrics.policyCalls.at(-1), { service: 'wordstat', channel: 'manual', method: 'getTop', credentialState: 'MISSING' });
});

test('autorun-disabled global Wordstat policy blocks batch next before provider', async () => {
  const { ctx, metrics, flush } = createHarness({ autorunEnabled: false });
  await flush();
  const api = ctx.YMBWordstatBatchWorkerTransport;
  await api.executeWordstatBatchCommand(start('job-auto-denied'), { channel: 'autorun' });
  const result = await api.executeWordstatBatchCommand({ action: 'next', jobId: 'job-auto-denied' }, { channel: 'autorun' });
  assert.equal(result.report_envelope.status, 'SKIPPED');
  assert.equal(result.report_envelope.reason, 'AUTORUN_DISABLED');
  assert.equal(metrics.providerCalls, 0);
});

test('Manual batch start preserves owner fence and stages result through existing manual outbox', async () => {
  const { ctx, state, metrics, flush } = createHarness();
  await flush();
  const text = `WORDSTAT_BATCH_API_V1\n${JSON.stringify(start('job-manual'))}`;

  const wrongOwner = await ctx.executeManualBlock(text, 'conv-key', { tab: { id: 8 } }, 'token-wrong');
  assert.equal(wrongOwner.accepted, false);
  assert.equal(wrongOwner.code, 'AUTO_NON_OWNER_TAB');
  assert.equal(metrics.providerCalls, 0);
  assert.equal(state.outbox, undefined);

  const accepted = await ctx.executeManualBlock(text, 'conv-key', { tab: { id: 7 } }, 'token-ok');
  assert.equal(accepted.accepted, true);
  assert.equal(metrics.providerCalls, 0, 'batch start is management-only');
  assert.match(accepted.report_text, /^WORDSTAT_BATCH_RESULT_V1/);
  assert.equal(state.outbox['conv-key'].type, 'manual');
  assert.equal(state.outbox['conv-key'].tab_id, 7);
  assert.equal(state.manual_operations['conv-key'].status, 'delivering');
  assert.equal(state.manual_operations['conv-key'].active_service, 'wordstat');
});

test('ordinary Manual block still delegates to the accepted pre-Phase-6 path', async () => {
  const { ctx, metrics, flush } = createHarness();
  await flush();
  const result = await ctx.executeManualBlock('WORDSTAT_API_V1\n{"method":"getTop","phrase":"ordinary"}', 'conv-key', { tab: { id: 7 } }, 'ordinary-token');
  assert.equal(result.base, true);
  assert.equal(metrics.baseManualCalls, 1);
});
