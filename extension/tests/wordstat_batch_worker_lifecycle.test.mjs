import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');
const clone = (value) => value == null ? value : JSON.parse(JSON.stringify(value));

function createHarness({ manualMode = true, beforeAdapter = null } = {}) {
  const state = { liveConversationId: 'conv-1', tabAvailable: true };
  const metrics = { providerCalls: 0, policyCalls: 0 };
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
    autorun_enabled: true,
    manual_enabled: true,
    max_requests_per_run: 10,
    max_cost_rub_per_run: 10,
    method_cost_rub: { getTop: 0.02 }
  });

  ctx.WORKER_SESSION_ID = 'worker-new';
  ctx.KEYS = { MANUAL_OPERATIONS: 'manual_operations' };
  ctx.TERMINAL_MANUAL_STATUSES = new Set(['completed', 'error', 'cancelled']);
  ctx.clone = clone;
  ctx.nowIso = () => '2026-08-27T14:00:00.000Z';
  ctx.uid = (prefix = 'id') => `${prefix}-${++uidCounter}`;
  ctx.normalizeConversationKey = (value) => String(value || '').trim();
  ctx.storageGet = (keys) => local.get(keys);
  ctx.storageSet = (values) => local.set(values);
  ctx.getSettings = async () => ({ apiKey: 'saved', folderId: 'folder' });
  ctx.getWordstatPolicy = async () => policy;
  ctx.publicCapability = () => ({ state: 'PRESENT' });
  ctx.policyDecisionForService = (service, args) => {
    metrics.policyCalls += 1;
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
        service: 'wordstat',
        operation: command.method,
        status: 'OK',
        http_status: 200,
        request_executed: true,
        automatic_retry: false,
        result: { phrase: command.phrase }
      }
    };
  };
  ctx.executeManualBlock = async () => ({ ok: true, base: true });
  ctx.handleAutoCommand = async () => ({ ok: true, base: true });
  ctx.assertTabConversation = async (tabId, _key, expectedConversationId = null) => {
    if (!state.tabAvailable) throw Object.assign(new Error('tab closed'), { code: 'TAB_UNAVAILABLE' });
    if (Number(tabId) !== 7) throw Object.assign(new Error('wrong owner'), { code: 'AUTO_NON_OWNER_TAB' });
    if (expectedConversationId && String(expectedConversationId) !== String(state.liveConversationId)) {
      throw Object.assign(new Error('conversation changed'), { code: 'CONVERSATION_MISMATCH' });
    }
    return { origin: 'https://chatgpt.com', conversation_id: state.liveConversationId, conversation_key: 'conv-key' };
  };
  ctx.getBinding = async () => ({ conversation_id: state.liveConversationId });
  ctx.getManualMode = async () => manualMode;
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

  if (typeof beforeAdapter === 'function') beforeAdapter(ctx, state);
  vm.runInContext(fs.readFileSync(path.join(src, 'wordstat_batch_worker_transport.js'), 'utf8'), ctx, { filename: 'wordstat_batch_worker_transport.js' });

  async function flush() {
    for (let index = 0; index < 6; index += 1) {
      await new Promise((resolve) => setImmediate(resolve));
    }
  }

  return { ctx, state, metrics, flush };
}

function start(jobId, { phrases = ['alpha'], maxRequests = 10, maxCostRub = 10 } = {}) {
  return {
    action: 'start', jobId, phrases, numPhrases: 100,
    regions: ['225'], devices: ['DEVICE_ALL'], maxRequests, maxCostRub
  };
}

function autoRun(ctx, overrides = {}) {
  return {
    run_id: 'run-1', tab_id: 7, conversation_id: 'conv-1', active_service: 'wordstat',
    status: ctx.WordstatAutorunModel.RUN_STATUSES.WAITING_COMMAND,
    requests_attempted: 0, requests_executed: 0, requests_skipped: 0, estimated_cost_rub: 0,
    pause_requested: false, last_error: null, delivery: null,
    ...overrides
  };
}

function batchText(command) {
  return `WORDSTAT_BATCH_API_V1\n${JSON.stringify(command)}`;
}

test('Manual double-submit cannot cross the paid provider boundary twice', async () => {
  const { ctx, metrics, flush } = createHarness();
  await flush();
  await ctx.YMBWordstatBatchWorkerTransport.executeWordstatBatchCommand(start('job-double'), { channel: 'manual' });
  const text = batchText({ action: 'next', jobId: 'job-double' });

  const first = await ctx.executeManualBlock(text, 'conv-key', { tab: { id: 7 } }, 'token-first');
  assert.equal(first.accepted, true);
  assert.equal(metrics.providerCalls, 1);

  const duplicate = await ctx.executeManualBlock(text, 'conv-key', { tab: { id: 7 } }, 'token-second');
  assert.equal(duplicate.accepted, false);
  assert.equal(duplicate.code, 'MANUAL_OPERATION_ACTIVE');
  assert.equal(metrics.providerCalls, 1);
});

test('stale Autorun assistant event is ignored after delivery and never replays provider work', async () => {
  const { ctx, state, metrics, flush } = createHarness({ manualMode: false });
  await flush();
  await ctx.YMBWordstatBatchWorkerTransport.executeWordstatBatchCommand(start('job-stale'), { channel: 'autorun' });
  state.auto_runs = { 'conv-key': autoRun(ctx) };
  const message = {
    conversation_key: 'conv-key', run_id: 'run-1', assistant_turn_id: 'turn-next-stale',
    command_text: batchText({ action: 'next', jobId: 'job-stale' })
  };

  const first = await ctx.handleAutoCommand(message, { tab: { id: 7 } });
  assert.equal(first.accepted, true);
  assert.equal(metrics.providerCalls, 1);
  assert.equal(state.auto_runs['conv-key'].last_assistant_turn_id, 'turn-next-stale');

  delete state.outbox['conv-key'];
  state.auto_runs['conv-key'] = {
    ...state.auto_runs['conv-key'],
    status: ctx.WordstatAutorunModel.RUN_STATUSES.WAITING_COMMAND,
    delivery: null
  };
  const stale = await ctx.handleAutoCommand(message, { tab: { id: 7 } });
  assert.equal(stale.accepted, false);
  assert.equal(stale.duplicate, true);
  assert.equal(metrics.providerCalls, 1);
});

test('worker restart with closed owner tab recovers stale REQUEST_STARTED as OUTCOME_UNKNOWN without provider replay', async () => {
  const { ctx, state, metrics, flush } = createHarness({
    beforeAdapter(runtimeCtx, runtimeState) {
      let job = runtimeCtx.YMBProviderBatchJobModel.createJob({
        jobId: 'job-restart',
        service: 'wordstat',
        commands: [{ method: 'getTop', phrase: 'alpha', numPhrases: 100, regions: ['225'], devices: ['DEVICE_ALL'] }],
        limits: { maxRequests: 10, maxCostRub: 10 },
        now: '2026-08-27T13:50:00.000Z'
      });
      ({ job } = runtimeCtx.YMBProviderBatchJobModel.claimNext(job, {
        actorId: 'worker-old:wordstat-batch', nextEstimatedCostRub: 0.02, now: '2026-08-27T13:50:01.000Z'
      }));
      job = runtimeCtx.YMBProviderBatchJobModel.markRequestStarted(job, job.active_item_id, {
        requestId: 'req-old', workerSessionId: 'worker-old:wordstat-batch', estimatedCostRub: 0.02,
        now: '2026-08-27T13:50:02.000Z'
      });
      runtimeState.ymb_wordstat_batch_jobs_v1 = { 'job-restart': clone(job) };
      runtimeState.manual_operations = {
        'conv-key': {
          operation_id: 'manual-restart', request_token: 'token-restart', conversation_key: 'conv-key', tab_id: 7,
          active_service: 'wordstat', run_id: null, status: 'batch_requesting', batch_action: 'next',
          batch_job_id: 'job-restart', request_executed: false, created_at: '2026-08-27T13:50:00.000Z'
        }
      };
      runtimeState.tabAvailable = false;
    }
  });
  await flush();

  const recoveredJob = state.ymb_wordstat_batch_jobs_v1['job-restart'];
  assert.equal(metrics.providerCalls, 0);
  assert.equal(recoveredJob.items[0].status, 'OUTCOME_UNKNOWN');
  assert.equal(recoveredJob.items[0].request_id, 'req-old');
  assert.equal(recoveredJob.items[0].automatic_retry, false);
  assert.equal(recoveredJob.stop_reason, 'OUTCOME_UNKNOWN_REQUIRES_RECONCILIATION');
  assert.equal(state.manual_operations['conv-key'].status, 'delivering');
  assert.equal(state.manual_operations['conv-key'].request_executed, 'UNKNOWN');
  assert.equal(state.outbox['conv-key'].type, 'manual');
  assert.equal(state.outbox['conv-key'].tab_id, 7);
  assert.equal(state.outbox['conv-key'].provider_executions, null);

  const blocked = await ctx.YMBWordstatBatchWorkerTransport.executeWordstatBatchCommand(
    { action: 'next', jobId: 'job-restart' },
    { channel: 'manual' }
  );
  assert.equal(blocked.request_executed, false);
  assert.equal(blocked.report_envelope.reason, 'OUTCOME_UNKNOWN_REQUIRES_RECONCILIATION');
  assert.equal(metrics.providerCalls, 0);
});

test('batch maxRequests stops a second pending item before another provider call', async () => {
  const { ctx, metrics, flush } = createHarness();
  await flush();
  const api = ctx.YMBWordstatBatchWorkerTransport;
  await api.executeWordstatBatchCommand(start('job-request-budget', {
    phrases: ['alpha', 'beta'], maxRequests: 1, maxCostRub: 10
  }), { channel: 'manual' });

  const first = await api.executeWordstatBatchCommand({ action: 'next', jobId: 'job-request-budget' }, { channel: 'manual' });
  assert.equal(first.request_executed, true);
  assert.equal(metrics.providerCalls, 1);
  const second = await api.executeWordstatBatchCommand({ action: 'next', jobId: 'job-request-budget' }, { channel: 'manual' });
  assert.equal(second.request_executed, false);
  assert.equal(second.report_envelope.reason, 'REQUEST_LIMIT_REACHED');
  assert.equal(second.report_envelope.progress.pending, 1);
  assert.equal(metrics.providerCalls, 1);
});

test('batch maxCostRub can be stricter than global Wordstat policy and blocks before provider', async () => {
  const { ctx, metrics, flush } = createHarness();
  await flush();
  const api = ctx.YMBWordstatBatchWorkerTransport;
  await api.executeWordstatBatchCommand(start('job-cost-budget', {
    phrases: ['alpha'], maxRequests: 10, maxCostRub: 0.01
  }), { channel: 'manual' });

  const result = await api.executeWordstatBatchCommand({ action: 'next', jobId: 'job-cost-budget' }, { channel: 'manual' });
  assert.equal(result.request_executed, false);
  assert.equal(result.report_envelope.reason, 'COST_LIMIT_REACHED');
  assert.equal(result.report_envelope.progress.pending, 1);
  assert.equal(metrics.providerCalls, 0);
  assert.ok(metrics.policyCalls >= 1, 'existing Wordstat policy must still admit before batch-specific cost guard');
});
