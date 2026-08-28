import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');

function clone(value) { return value == null ? value : JSON.parse(JSON.stringify(value)); }

function loadContext(files) {
  const ctx = {
    console, JSON, Object, Array, Set, String, Number, Boolean, RegExp, Date, Error, Math,
    URL, TextDecoder, Uint8Array, Buffer,
    crypto: { randomUUID: () => 'uuid-fixed' },
    globalThis: null
  };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  for (const file of files) {
    vm.runInContext(fs.readFileSync(path.join(src, file), 'utf8'), ctx, { filename: file });
  }
  return ctx;
}

function loadProtocol() {
  return loadContext(['shared/search_protocol.js', 'shared/search_batch_protocol.js']).SearchBatchProtocol;
}

function loadProjection() {
  return loadContext(['shared/search_batch_projection.js']).YMBSearchBatchProjection;
}

function loadFactory() {
  return loadContext([
    'shared/provider_batch_job_model.js',
    'shared/search_protocol.js',
    'shared/search_batch_protocol.js',
    'shared/search_batch_projection.js',
    'shared/search_batch_runtime.js'
  ]).YMBSearchBatchRuntime;
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
    queries: ['alpha', 'beta'],
    searchType: 'SEARCH_TYPE_RU',
    region: '225',
    groupsOnPage: 10,
    maxRequests: 2,
    maxCostRub: 1,
    confirmBillable: true,
    ...overrides
  };
}

function searchEnvelope(query, domains, requestId = 'req') {
  const results = domains.map((domain, index) => ({
    rank: index + 1,
    url: `https://${domain}/p${index + 1}`,
    domain,
    title: `${query} ${index + 1}`,
    snippet: null,
    modtime: null
  }));
  return {
    bridge: 'yandex-marketing-bridge',
    version: '0.1.1',
    service: 'search',
    operation: 'search',
    request_id: requestId,
    status: 'OK',
    command: { method: 'search', queryText: query },
    http_status: 200,
    result: { results, result_count: results.length, response_format: 'FORMAT_XML' },
    request_executed: true,
    automatic_retry: false
  };
}

test('SEARCH_BATCH start is bounded, explicitly billable and remains inside Search service', () => {
  const protocol = loadProtocol();
  const command = protocol.normalizeCommand(startCommand({ queries: [' alpha ', 'beta', 'alpha'] }));
  assert.equal(protocol.PREFIX, 'SEARCH_BATCH_API_V1');
  assert.equal(protocol.RESULT_PREFIX, 'SEARCH_BATCH_RESULT_V1');
  assert.equal(command.action, 'start');
  assert.equal(command.searchType, 'SEARCH_TYPE_RU');
  assert.equal(command.region, '225');
  assert.equal(command.groupsOnPage, 10);
  assert.equal(command.maxRequests, 2);
  assert.equal(command.maxCostRub, 1);
  assert.equal(command.confirmBillable, true);
  assert.deepEqual(Array.from(command.queries), ['alpha', 'beta', 'alpha']);

  assert.throws(() => protocol.normalizeCommand(startCommand({ confirmBillable: false })), (e) => e.code === 'SEARCH_BATCH_CONFIRM_REQUIRED');
  assert.throws(() => protocol.normalizeCommand(startCommand({ queries: Array.from({ length: 501 }, (_, i) => `q${i}`), maxRequests: 500 })), (e) => e.code === 'TOO_MANY_SEARCH_BATCH_QUERIES');
  assert.throws(() => protocol.normalizeCommand(startCommand({ queries: ['alpha', 'alpha'], maxRequests: 2 })), (e) => e.code === 'SEARCH_BATCH_MAX_REQUESTS_EXCEEDS_QUERIES');
  assert.throws(() => protocol.normalizeCommand({ ...startCommand(), method: 'genSearch' }), (e) => e.code === 'UNSUPPORTED_SEARCH_BATCH_FIELD');
});

test('SEARCH_BATCH fixes ordinary Search semantics and management actions remain local-only contracts', () => {
  const protocol = loadProtocol();
  const ordinary = protocol.buildSearchCommand(protocol.normalizeCommand(startCommand()), 'alpha');
  assert.equal(ordinary.method, 'search');
  assert.equal(ordinary.queryText, 'alpha');
  assert.equal(ordinary.searchType, 'SEARCH_TYPE_RU');
  assert.equal(ordinary.region, '225');
  assert.equal(ordinary.page, 0);
  assert.equal(ordinary.groupsOnPage, 10);
  assert.equal(ordinary.docsInGroup, 1);
  assert.equal(ordinary.groupMode, 'GROUP_MODE_FLAT');
  assert.equal(ordinary.sortMode, 'SORT_MODE_BY_RELEVANCE');
  assert.equal(ordinary.sortOrder, 'SORT_ORDER_DESC');
  assert.equal(ordinary.familyMode, 'FAMILY_MODE_MODERATE');
  assert.equal(ordinary.fixTypoMode, 'FIX_TYPO_MODE_ON');

  for (const action of ['next', 'status', 'pause', 'resume', 'cancel']) {
    const command = protocol.normalizeCommand({ action, jobId: 'job-1' });
    assert.equal(command.action, action);
    assert.equal(command.jobId, 'job-1');
    assert.throws(() => protocol.normalizeCommand({ action }), (e) => e.code === 'MISSING_SEARCH_BATCH_JOB_ID');
  }

  const projection = protocol.normalizeCommand({ action: 'projection', jobId: 'job-1', offset: 2, limit: 50, topN: 20, targetDomains: ['Example.COM', 'www.test.ru'] });
  assert.equal(projection.offset, 2);
  assert.equal(projection.limit, 50);
  assert.equal(projection.topN, 20);
  assert.deepEqual(Array.from(projection.targetDomains), ['example.com', 'www.test.ru']);

  const overlap = protocol.normalizeCommand({ action: 'overlapPage', jobId: 'job-1', offset: 10, limit: 1000, topN: 10 });
  assert.equal(overlap.offset, 10);
  assert.equal(overlap.limit, 1000);
  assert.equal(overlap.topN, 10);
});

test('projection preserves ranked rows, unique domain order and sampled target-domain rank', () => {
  const projection = loadProjection();
  const job = {
    job_id: 'job-1',
    service: 'search',
    items: [
      {
        item_id: 'a', status: 'SUCCEEDED',
        command: { method: 'search', queryText: 'alpha', searchType: 'SEARCH_TYPE_RU', region: '225', groupsOnPage: 10 },
        result_payload: searchEnvelope('alpha', ['A.com', 'b.com', 'a.com'])
      },
      {
        item_id: 'b', status: 'FAILED_TERMINAL',
        command: { method: 'search', queryText: 'ignored', searchType: 'SEARCH_TYPE_RU', region: '225', groupsOnPage: 10 },
        result_payload: searchEnvelope('ignored', ['x.com'])
      }
    ]
  };

  const page = projection.projectPage(job, { offset: 0, limit: 10, topN: 3, targetDomains: ['b.com', 'missing.com'] });
  assert.equal(page.total_successful, 1);
  assert.equal(page.items.length, 1);
  assert.deepEqual(Array.from(page.items[0].top_domains), ['a.com', 'b.com']);
  assert.deepEqual(page.items[0].ranked_results.map((row) => row.rank), [1, 2, 3]);
  assert.equal(page.items[0].target_domains[0].domain, 'b.com');
  assert.equal(page.items[0].target_domains[0].best_rank_within_observed_topN, 2);
  assert.equal(page.items[0].target_domains[1].best_rank_within_observed_topN, null);
});

test('overlapPage is deterministic, paged and computes domain-set evidence without semantic labels', () => {
  const projection = loadProjection();
  const job = {
    job_id: 'job-1', service: 'search', items: [
      { item_id: 'a', status: 'SUCCEEDED', command: { method: 'search', queryText: 'alpha' }, result_payload: searchEnvelope('alpha', ['a.com', 'b.com', 'z.com']) },
      { item_id: 'b', status: 'SUCCEEDED', command: { method: 'search', queryText: 'beta' }, result_payload: searchEnvelope('beta', ['b.com', 'c.com', 'z.com']) },
      { item_id: 'c', status: 'SUCCEEDED', command: { method: 'search', queryText: 'gamma' }, result_payload: searchEnvelope('gamma', ['x.com', 'y.com']) }
    ]
  };

  const page = projection.overlapPage(job, { topN: 2, offset: 0, limit: 2 });
  assert.equal(page.total_successful, 3);
  assert.equal(page.total_pairs, 3);
  assert.equal(page.items.length, 2);
  const first = page.items[0];
  assert.equal(first.left_item_id, 'a');
  assert.equal(first.right_item_id, 'b');
  assert.deepEqual(Array.from(first.shared_domains), ['b.com']);
  assert.equal(first.shared_count, 1);
  assert.equal(first.union_count, 3);
  assert.ok(Math.abs(first.jaccard - (1 / 3)) < 1e-12);
  assert.equal(Object.hasOwn(first, 'cluster'), false);
  assert.equal(Object.hasOwn(first, 'same_page'), false);
});

test('Search batch start persists a deduplicated ordinary-search job with zero provider traffic', async () => {
  const Factory = loadFactory();
  const storage = memoryStorage();
  let providerCalls = 0;
  const runtime = Factory.create({
    storage,
    workerSessionId: 'worker-A',
    executeSearch: async () => { providerCalls += 1; throw new Error('must not run on start'); },
    estimateCostRub: () => 0.488,
    now: () => '2026-08-28T04:20:00.000Z',
    uid: () => 'search-job-1'
  });

  const result = await runtime.handle(startCommand({ queries: ['alpha', 'alpha', 'beta'] }));
  assert.equal(result.envelope.operation, 'batch.start');
  assert.equal(result.envelope.service, 'search');
  assert.equal(result.envelope.job_id, 'search-job-1');
  assert.equal(result.envelope.request_executed, false);
  assert.equal(result.envelope.progress.total, 2);
  assert.equal(result.envelope.progress.duplicate_count, 1);
  assert.equal(providerCalls, 0);
  assert.equal(storage.state.ymb_search_batch_jobs_v1['search-job-1'].status, 'RUNNING');
  const first = storage.state.ymb_search_batch_jobs_v1['search-job-1'].items[0].command;
  assert.equal(first.method, 'search');
  assert.equal(first.page, 0);
  assert.equal(first.docsInGroup, 1);
});

test('one Search batch next persists REQUEST_STARTED before exactly one provider call and persists the SERP payload', async () => {
  const Factory = loadFactory();
  const storage = memoryStorage();
  let providerCalls = 0;
  let writesAtProviderStart = 0;
  const runtime = Factory.create({
    storage,
    workerSessionId: 'worker-A',
    executeSearch: async (command, metadata) => {
      providerCalls += 1;
      writesAtProviderStart = storage.writes.length;
      const stored = storage.state.ymb_search_batch_jobs_v1['search-job-1'];
      assert.equal(stored.items[0].status, 'REQUEST_STARTED');
      assert.equal(stored.items[0].request_id, metadata.request_id);
      assert.equal(command.method, 'search');
      return {
        ok: true,
        request_id: metadata.request_id,
        request_executed: true,
        report_envelope: searchEnvelope(command.queryText, ['a.com', 'b.com'], metadata.request_id)
      };
    },
    estimateCostRub: () => 0.488,
    now: () => '2026-08-28T04:20:00.000Z',
    uid: (() => { let n = 0; return () => n++ === 0 ? 'search-job-1' : `req-${n}`; })()
  });

  await runtime.handle(startCommand());
  const before = storage.writes.length;
  const result = await runtime.handle({ action: 'next', jobId: 'search-job-1' });
  assert.ok(writesAtProviderStart >= before + 2);
  assert.equal(providerCalls, 1);
  assert.equal(result.envelope.request_executed, true);
  assert.equal(result.envelope.progress.succeeded, 1);
  const stored = storage.state.ymb_search_batch_jobs_v1['search-job-1'].items[0];
  assert.equal(stored.status, 'SUCCEEDED');
  assert.equal(stored.result_payload.result.result_count, 2);
  assert.equal(stored.automatic_retry, false);
});

test('Search batch local management/projection/overlap actions never contact provider', async () => {
  const Factory = loadFactory();
  const storage = memoryStorage();
  let providerCalls = 0;
  const runtime = Factory.create({
    storage,
    workerSessionId: 'worker-A',
    executeSearch: async (command, metadata) => {
      providerCalls += 1;
      return { ok: true, request_id: metadata.request_id, request_executed: true, report_envelope: searchEnvelope(command.queryText, command.queryText === 'alpha' ? ['a.com', 'b.com'] : ['b.com', 'c.com'], metadata.request_id) };
    },
    estimateCostRub: () => 0.488,
    now: () => '2026-08-28T04:20:00.000Z',
    uid: (() => { let n = 0; return () => n++ === 0 ? 'search-job-1' : `req-${n}`; })()
  });

  await runtime.handle(startCommand());
  await runtime.handle({ action: 'next', jobId: 'search-job-1' });
  await runtime.handle({ action: 'next', jobId: 'search-job-1' });
  assert.equal(providerCalls, 2);

  const status = await runtime.handle({ action: 'status', jobId: 'search-job-1' });
  const projection = await runtime.handle({ action: 'projection', jobId: 'search-job-1', offset: 0, limit: 10, topN: 10, targetDomains: ['b.com'] });
  const overlap = await runtime.handle({ action: 'overlapPage', jobId: 'search-job-1', offset: 0, limit: 10, topN: 10 });
  assert.equal(status.envelope.progress.succeeded, 2);
  assert.equal(projection.envelope.request_executed, false);
  assert.equal(projection.envelope.projection.items[0].target_domains[0].best_rank_within_observed_topN, 2);
  assert.equal(overlap.envelope.request_executed, false);
  assert.equal(overlap.envelope.projection.items[0].shared_count, 1);
  assert.equal(providerCalls, 2);
});

test('unknown Search provider outcome is durable and the same paid item is never automatically replayed', async () => {
  const Factory = loadFactory();
  const storage = memoryStorage();
  let calls = 0;
  const runtime = Factory.create({
    storage,
    workerSessionId: 'worker-A',
    executeSearch: async () => {
      calls += 1;
      const error = new Error('network outcome unknown');
      error.code = 'REQUEST_OUTCOME_UNKNOWN_NO_RETRY';
      error.request_executed = 'UNKNOWN';
      throw error;
    },
    estimateCostRub: () => 0.488,
    now: () => '2026-08-28T04:20:00.000Z',
    uid: (() => { let n = 0; return () => n++ === 0 ? 'search-job-1' : `req-${n}`; })()
  });

  await runtime.handle(startCommand({ queries: ['alpha'] , maxRequests: 1 }));
  const first = await runtime.handle({ action: 'next', jobId: 'search-job-1' });
  assert.equal(first.envelope.request_executed, 'UNKNOWN');
  assert.equal(first.envelope.progress.outcome_unknown, 1);
  assert.equal(first.envelope.progress.next_safe_action, 'RECONCILE_UNKNOWN');
  assert.equal(calls, 1);

  const second = await runtime.handle({ action: 'next', jobId: 'search-job-1' });
  assert.equal(second.envelope.reason, 'OUTCOME_UNKNOWN_REQUIRES_RECONCILIATION');
  assert.equal(calls, 1);
});

test('Search batch job cost ceiling and external admission both fail closed before another provider call', async () => {
  const Factory = loadFactory();
  const storage = memoryStorage();
  let calls = 0;
  const runtime = Factory.create({
    storage,
    workerSessionId: 'worker-A',
    executeSearch: async (command, metadata) => {
      calls += 1;
      return { ok: true, request_id: metadata.request_id, request_executed: true, report_envelope: searchEnvelope(command.queryText, ['a.com'], metadata.request_id) };
    },
    estimateCostRub: () => 0.488,
    now: () => '2026-08-28T04:20:00.000Z',
    uid: (() => { let n = 0; return () => n++ === 0 ? 'search-job-1' : `req-${n}`; })()
  });

  await runtime.handle(startCommand({ maxCostRub: 0.5 }));
  await runtime.handle({ action: 'next', jobId: 'search-job-1' });
  const blocked = await runtime.handle({ action: 'next', jobId: 'search-job-1' });
  assert.equal(blocked.envelope.reason, 'COST_LIMIT_REACHED');
  assert.equal(calls, 1);

  const storage2 = memoryStorage();
  let deniedCalls = 0;
  const denied = Factory.create({
    storage: storage2,
    workerSessionId: 'worker-B',
    executeSearch: async () => { deniedCalls += 1; return {}; },
    estimateCostRub: () => 0.488,
    admit: async () => ({ allow: false, reason: 'GLOBAL_SEARCH_COST_LIMIT', estimated_cost_rub: 0.488 }),
    now: () => '2026-08-28T04:20:00.000Z',
    uid: () => 'search-job-2'
  });
  await denied.handle(startCommand({ jobId: 'search-job-2' }));
  const skipped = await denied.handle({ action: 'next', jobId: 'search-job-2' });
  assert.equal(skipped.envelope.status, 'SKIPPED');
  assert.equal(skipped.envelope.reason, 'GLOBAL_SEARCH_COST_LIMIT');
  assert.equal(skipped.envelope.request_executed, false);
  assert.equal(deniedCalls, 0);
});
