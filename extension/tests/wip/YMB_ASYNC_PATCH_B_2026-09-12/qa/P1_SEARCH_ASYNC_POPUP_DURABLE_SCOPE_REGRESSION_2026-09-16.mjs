import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import { indexedDB, IDBKeyRange, IDBObjectStore, IDBIndex } from './idb_test_double.mjs';

const storeSource = fs.readFileSync(new URL('../../../../src/shared/search_async_store.js', import.meta.url), 'utf8');
const monitorSource = fs.readFileSync(new URL('../../../../src/popup_search_async_monitor.js', import.meta.url), 'utf8');

const at = (value, path) => Array.isArray(path) ? path.map((key) => value[key]) : value[path];
if (typeof IDBObjectStore.prototype.count !== 'function') {
  IDBObjectStore.prototype.count = function count(range = null) {
    return this.transaction.enqueue(() => this.transaction.rows(this.name).filter((value) => !range || range.includes(at(value, this.definition.keyPath))).length);
  };
}
if (typeof IDBIndex.prototype.count !== 'function') {
  IDBIndex.prototype.count = function count(range = null) {
    return this.store.transaction.enqueue(() => this.store.transaction.rows(this.store.name).filter((value) => !range || range.includes(at(value, this.definition.path))).length);
  };
}
// The deterministic test double predates the browser-valid no-range form of
// objectStore.openCursor() used by the popup monitor. Adapt only the fake: all
// production job ids are validated ASCII identifiers, so this range is complete.
const fakeOpenCursor = IDBObjectStore.prototype.openCursor;
IDBObjectStore.prototype.openCursor = function openCursor(range) {
  return fakeOpenCursor.call(this, range || IDBKeyRange.bound('', '\uffff'));
};

function baseContext(extra = {}) {
  const context = vm.createContext({ console, structuredClone, indexedDB, IDBKeyRange, setImmediate, clearImmediate, ...extra });
  context.globalThis = context;
  return context;
}

function loadStore() {
  const context = baseContext();
  vm.runInContext(storeSource, context);
  return context.YMBSearchAsyncStore;
}

function monitorHarness({ folderId = 'folder', service = 'search', conversationKey = 'https://chatgpt.com|11111111-1111-4111-8111-111111111111' } = {}) {
  const nodes = new Map();
  const ids = [
    'conversationMeta','searchAsyncRefresh','searchAsyncCollectOne','searchAsyncExport','searchAsyncActionStatus',
    'searchAsyncJob','searchAsyncState','searchAsyncProcessed','searchAsyncSucceeded','searchAsyncRemaining','searchAsyncWaiting',
    'searchAsyncPendingWorking','searchAsyncIssues','searchAsyncRows','searchAsyncNormalized','searchAsyncNextPoll','searchAsyncElapsed','searchAsyncRevision'
  ];
  for (const id of ids) nodes.set(id, { id, textContent: '', disabled: false, hidden: false, dataset: {} });
  nodes.get('conversationMeta').textContent = conversationKey;
  const document = { getElementById: (id) => nodes.get(id) || null };
  const calls = { runtime: [], tabs: 0, provider: 0 };
  let activeService = service;
  const chrome = {
    runtime: {
      lastError: null,
      sendMessage(message, callback) {
        calls.runtime.push(structuredClone(message));
        callback({
          ok: true,
          state: {
            credential_status: { search: { folder_id: folderId } },
            service_context: { active_service: activeService }
          }
        });
      }
    },
    tabs: {
      query() { calls.tabs += 1; throw new Error('tabs query is forbidden during local refresh'); },
      sendMessage() { calls.tabs += 1; throw new Error('tab provider/action path is forbidden during local refresh'); }
    }
  };
  const context = baseContext({
    document,
    chrome,
    fetch: () => { calls.provider += 1; throw new Error('provider network forbidden'); },
    Date
  });
  context.__YMB_ASYNC_MONITOR_TEST__ = true;
  vm.runInContext(monitorSource, context);
  return {
    api: context.__YMB_ASYNC_MONITOR_TEST_API__, nodes, calls,
    setService(value) { activeService = value; }
  };
}

async function start(store, suffix) {
  const folderId = `folder-${suffix}`;
  const owner = `search-folder:${folderId}`;
  const jobId = `popup-${suffix}`;
  await store.createJob({
    jobId, owner, queries: ['q'], parameters: { region: '225' }, folderId,
    maxRequests: 1, maxCostMicrorub: 30500, unitCostMicrorub: 30500, now: 1000
  });
  return { folderId, owner, jobId };
}

async function submitWaiting(store, ids) {
  const claim = await store.claim({ jobId: ids.jobId, owner: ids.owner, workerId: 'worker', attemptId: `submit-${ids.jobId}`, kind: 'submit', now: 1100 });
  assert.equal(claim.allowed, true);
  await store.finishSubmit({
    jobId: ids.jobId, owner: ids.owner, index: 0, attemptId: `submit-${ids.jobId}`, now: 1200,
    outcome: 'accepted', operationId: `op-${ids.jobId}`, nextPollAt: 5000
  });
}

async function collectSuccess(store, ids) {
  const claim = await store.claim({ jobId: ids.jobId, owner: ids.owner, workerId: 'worker', attemptId: `collect-${ids.jobId}`, kind: 'collect', now: 6000 });
  assert.equal(claim.allowed, true);
  await store.finishCollect({
    jobId: ids.jobId, owner: ids.owner, index: 0, attemptId: `collect-${ids.jobId}`, now: 6100,
    outcome: 'received', rawText: '<response/>', nextPollAt: 0
  });
  await store.finishNormalization({
    jobId: ids.jobId, owner: ids.owner, index: 0, now: 6200,
    normalized: { results: [{ url: 'https://example.test/' }] }
  });
}

test('A start creates durable job and popup local snapshot sees it immediately', async () => {
  const store = loadStore(); const ids = await start(store, 'a');
  const { api } = monitorHarness({ folderId: ids.folderId });
  const snapshot = await api.snapshotForFolder(ids.folderId, 1000);
  assert.equal(api.durableJobOwner(ids.folderId), ids.owner);
  assert.equal(snapshot.job_id, ids.jobId); assert.equal(snapshot.counts.PENDING, 1); assert.equal(snapshot.revision, 0);
});

test('B popup reload sees the same persisted durable job', async () => {
  const store = loadStore(); const ids = await start(store, 'b');
  const first = monitorHarness({ folderId: ids.folderId });
  assert.equal((await first.api.snapshotForFolder(ids.folderId, 1000)).job_id, ids.jobId);
  const reloaded = monitorHarness({ folderId: ids.folderId });
  assert.equal((await reloaded.api.snapshotForFolder(ids.folderId, 1001)).job_id, ids.jobId);
});

test('C submit persistence WAITING=1 revision=2 is visible to popup', async () => {
  const store = loadStore(); const ids = await start(store, 'c'); await submitWaiting(store, ids);
  const { api } = monitorHarness({ folderId: ids.folderId });
  const snapshot = await api.snapshotForFolder(ids.folderId, 1300);
  assert.equal(snapshot.counts.WAITING, 1); assert.equal(snapshot.counts.PENDING, 0); assert.equal(snapshot.revision, 2);
});

test('D service-worker/store runtime restart does not hide the persisted job', async () => {
  const store = loadStore(); const ids = await start(store, 'd'); await submitWaiting(store, ids);
  const restartedStore = loadStore();
  const summary = await restartedStore.getSummary(ids.jobId, ids.owner);
  assert.equal(summary.counts.WAITING, 1);
  const reloadedPopup = monitorHarness({ folderId: ids.folderId });
  assert.equal((await reloadedPopup.api.snapshotForFolder(ids.folderId, 1300)).job_id, ids.jobId);
});

test('E NO_DUE_OPERATIONS leaves the same popup job and revision intact', async () => {
  const store = loadStore(); const ids = await start(store, 'e'); await submitWaiting(store, ids);
  const early = await store.claim({ jobId: ids.jobId, owner: ids.owner, workerId: 'worker', attemptId: `early-${ids.jobId}`, kind: 'collect', now: 2000 });
  assert.equal(early.allowed, false); assert.equal(early.reason, 'NO_DUE_OPERATIONS');
  const { api } = monitorHarness({ folderId: ids.folderId });
  const snapshot = await api.snapshotForFolder(ids.folderId, 2000);
  assert.equal(snapshot.job_id, ids.jobId); assert.equal(snapshot.counts.WAITING, 1); assert.equal(snapshot.revision, 2);
});

test('F successful collect and normalization render SUCCEEDED=1 normalized=1 revision=5', async () => {
  const store = loadStore(); const ids = await start(store, 'f'); await submitWaiting(store, ids); await collectSuccess(store, ids);
  const { api } = monitorHarness({ folderId: ids.folderId });
  const snapshot = await api.snapshotForFolder(ids.folderId, 6300);
  assert.equal(snapshot.counts.SUCCEEDED, 1); assert.equal(snapshot.counts.WAITING, 0); assert.equal(snapshot.normalized_items, 1); assert.equal(snapshot.revision, 5);
});

test('G Wordstat/Search service switching does not hide or destroy Search durable job', async () => {
  const store = loadStore(); const ids = await start(store, 'g'); await submitWaiting(store, ids);
  const popup = monitorHarness({ folderId: ids.folderId, service: 'wordstat' });
  assert.equal((await popup.api.refreshSnapshot()).job_id, ids.jobId);
  popup.setService('search'); assert.equal((await popup.api.refreshSnapshot()).job_id, ids.jobId);
  popup.setService('wordstat'); assert.equal((await popup.api.refreshSnapshot()).job_id, ids.jobId);
  assert.equal((await store.getSummary(ids.jobId, ids.owner)).revision, 2);
});

test('H popup refresh is local/read-only and never enters provider or tab action transport', async () => {
  const store = loadStore(); const ids = await start(store, 'h');
  const popup = monitorHarness({ folderId: ids.folderId });
  const before = await store.getSummary(ids.jobId, ids.owner);
  const snapshot = await popup.api.refreshSnapshot();
  const after = await store.getSummary(ids.jobId, ids.owner);
  assert.equal(snapshot.job_id, ids.jobId); assert.equal(popup.calls.provider, 0); assert.equal(popup.calls.tabs, 0);
  assert.equal(JSON.stringify(after), JSON.stringify(before));
  assert.deepEqual(popup.calls.runtime.map((message) => message.type), ['WS_GET_GLOBAL_STATE']);
});

test('I only a truly absent durable job renders Нет локального deferred Search job', async () => {
  loadStore();
  const popup = monitorHarness({ folderId: 'folder-with-no-job' });
  const snapshot = await popup.api.refreshSnapshot();
  assert.equal(snapshot, null);
  assert.equal(popup.nodes.get('searchAsyncJob').textContent, '—');
  assert.equal(popup.nodes.get('searchAsyncState').textContent, 'Нет локального deferred Search job');
});
