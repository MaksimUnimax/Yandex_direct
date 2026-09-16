import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const source = fs.readFileSync(new URL('../../../../src/shared/search_async_export.js', import.meta.url), 'utf8');
const ctx = vm.createContext({ TextEncoder, console, URL });
ctx.globalThis = ctx;
vm.runInContext(source, ctx, { filename: 'search_async_export.js' });
const E = ctx.YMBSearchAsyncExport;
const STATES = ['PENDING', 'SUBMITTING', 'WAITING', 'COLLECTING', 'RESULT_SAVED', 'SUCCEEDED', 'PARSE_FAILED', 'FAILED', 'UNKNOWN', 'CANCELLED'];
const counts = (x = {}) => Object.assign(Object.fromEntries(STATES.map(s => [s, 0])), x);
const progress = (x = {}) => ({
  job_id: 'job1', control: 'RUNNING', total: 1, counts: counts({ SUCCEEDED: 1 }),
  requests_started: 1, operations_accepted: 1, polls_started: 0,
  unresolved: 0, all_successful: true, busy: false, revision: 5, ...x
});
const terminalJob = (x = {}) => ({
  job_id: 'job1', owner: 'old-owner', folder_id: 'folder1', total: 1,
  counts: counts({ SUCCEEDED: 1 }), lease: null, revision: 5, ...x
});

function storeFixture({ storedOwner = 'old-owner', p = progress() } = {}) {
  let current = structuredClone(p);
  const guard = owner => {
    if (owner !== storedOwner) throw Object.assign(new Error('ASYNC_WRONG_OWNER'), { code: 'ASYNC_WRONG_OWNER', request_executed: false });
  };
  return {
    setProgress: value => { current = structuredClone(value); },
    async peekNext({ owner }) {
      guard(owner);
      return { folder_id: 'folder1', parameters: { searchType: 'SEARCH_TYPE_RU' }, progress: structuredClone(current) };
    },
    async readItem(jobId, owner, index) {
      guard(owner);
      return { job_id: jobId, index, state: 'SUCCEEDED', operation_id: 'op1', poll_count: 0 };
    },
    async readResult(jobId, owner, index) {
      guard(owner);
      return { job_id: jobId, index, operation_id: 'op1', raw_text: '<xml/>', normalized: { results: [{ rank: 1, url: 'https://example.com' }] } };
    },
    async getSummary(jobId, owner) {
      guard(owner);
      return structuredClone(current);
    }
  };
}

function artifactFixture() {
  const records = new Map();
  return {
    records,
    async getMeta(key) { return records.get(key)?.descriptor || null; },
    async deleteArtifact(key) { records.delete(key); },
    async stageTextArtifact({ artifactKey, deliveryId, filename, text, mimeType }) {
      const descriptor = {
        artifact_key: artifactKey,
        delivery_id: deliveryId,
        filename,
        mime_type: mimeType,
        status: 'ready',
        byte_length: new TextEncoder().encode(text).length
      };
      records.set(artifactKey, { descriptor, text });
      return descriptor;
    }
  };
}

function fixture({ requester = 'new-owner', storedOwner = 'old-owner', job = terminalJob(), store = storeFixture({ storedOwner }), authorized = true } = {}) {
  let metadataReads = 0;
  let authCalls = 0;
  const artifacts = artifactFixture();
  const api = E.create({
    store,
    artifacts,
    now: () => 1000,
    authorize: async ({ jobId, owner, action }) => {
      authCalls++;
      assert.equal(jobId, 'job1');
      assert.equal(owner, requester);
      assert.equal(action, 'exportPage');
      return authorized;
    },
    crossOwnerJobReader: async ({ jobId }) => {
      metadataReads++;
      assert.equal(jobId, 'job1');
      return structuredClone(job);
    }
  });
  return {
    api,
    store,
    artifacts,
    get metadataReads() { return metadataReads; },
    get authCalls() { return authCalls; }
  };
}

const args = (x = {}) => ({
  jobId: 'job1', owner: 'new-owner', folderId: 'folder1', deliveryId: 'd1',
  after: -1, limit: 1, revision: 5, ...x
});

test('same-owner export is unchanged and bypasses cross-owner metadata', async () => {
  const store = storeFixture({ storedOwner: 'same-owner' });
  const artifacts = artifactFixture();
  let reads = 0;
  const api = E.create({
    store,
    artifacts,
    now: () => 1000,
    authorize: async ({ owner }) => owner === 'same-owner',
    crossOwnerJobReader: async () => { reads++; return terminalJob({ owner: 'same-owner' }); }
  });
  const out = await api.stagePage(args({ owner: 'same-owner' }));
  assert.equal(out.report.item_count, 1);
  assert.equal(reads, 0);
});

test('cross-owner exact terminal snapshot exports read-only', async () => {
  const h = fixture();
  const out = await h.api.stagePage(args());
  assert.equal(out.report.revision, 5);
  assert.equal(out.report.item_count, 1);
  assert.equal(out.report.all_job_items_in_this_file, true);
  assert.equal(h.metadataReads, 1);
  assert.ok(h.authCalls >= 4);
  const saved = h.artifacts.records.get('async-export:d1');
  assert.ok(saved);
  assert.equal(JSON.parse(saved.text).items[0].result.normalized.results[0].rank, 1);
});

test('cross-owner first page requires explicit revision', async () => {
  const h = fixture();
  await assert.rejects(h.api.stagePage(args({ revision: null })), error => error.code === 'EXPORT_CROSS_OWNER_REVISION_REQUIRED' && error.request_executed === false);
  assert.equal(h.metadataReads, 0);
});

test('cross-owner folder and revision mismatches fail closed', async () => {
  await assert.rejects(fixture().api.stagePage(args({ folderId: 'other' })), error => error.code === 'EXPORT_FOLDER_MISMATCH');
  await assert.rejects(fixture().api.stagePage(args({ revision: 4 })), error => error.code === 'EXPORT_REVISION_CHANGED');
});

test('cross-owner active unresolved failed cancelled and leased jobs fail closed', async () => {
  for (const job of [
    terminalJob({ counts: counts({ PENDING: 1 }) }),
    terminalJob({ counts: counts({ PARSE_FAILED: 1 }) }),
    terminalJob({ counts: counts({ FAILED: 1 }) }),
    terminalJob({ counts: counts({ CANCELLED: 1 }) }),
    terminalJob({ lease: { token: 'x' } })
  ]) {
    await assert.rejects(fixture({ job }).api.stagePage(args()), error => ['EXPORT_CROSS_OWNER_NOT_TERMINAL', 'EXPORT_JOB_BUSY'].includes(error.code));
  }
});

test('current chat authorization is required before metadata disclosure', async () => {
  const h = fixture({ authorized: false });
  await assert.rejects(h.api.stagePage(args()), error => error.code === 'EXPORT_NOT_AUTHORIZED');
  assert.equal(h.metadataReads, 0);
});

test('terminal invariant is rechecked after staging and orphan artifact is cleaned', async () => {
  const store = storeFixture({ storedOwner: 'old-owner' });
  const h = fixture({ store });
  const stage = h.artifacts.stageTextArtifact;
  h.artifacts.stageTextArtifact = async input => {
    const descriptor = await stage.call(h.artifacts, input);
    store.setProgress(progress({ all_successful: false, unresolved: 1, counts: counts({ PARSE_FAILED: 1 }) }));
    return descriptor;
  };
  await assert.rejects(h.api.stagePage(args()), error => error.code === 'EXPORT_CROSS_OWNER_NOT_TERMINAL');
  assert.equal(h.artifacts.records.has('async-export:d1'), false);
});

test('export source stays provider-free mutation-free and metadata DB access is readonly', () => {
  assert.doesNotMatch(source, /\bfetch\s*\(/);
  assert.doesNotMatch(source, /\bXMLHttpRequest\b/);
  assert.doesNotMatch(source, /\bfinishSubmit\b|\bfinishCollect\b|\bcreateJob\b|\bcontrol\s*\(/);
  assert.match(source, /transaction\(\["jobs"\], "readonly"\)/);
});

test('worker export branch still declares zero provider calls and owner-guarded status/items stay strict', () => {
  const worker = fs.readFileSync(new URL('../../../../src/search_async_worker_transport.js', import.meta.url), 'utf8');
  const start = worker.indexOf('if (command.action === "exportPage")');
  const end = worker.indexOf('if (command.action === "status")', start);
  assert.ok(start > 0 && end > start);
  const block = worker.slice(start, end);
  assert.match(block, /request_executed:\s*false,\s*provider_calls:\s*0/);
  assert.doesNotMatch(block, /runtime\.(?:step|recover|control|normalizeSaved)/);
  assert.match(worker, /store\.getSummary\(jobId,\s*key\)/);
  assert.match(worker, /store\.pageItems\(jobId,\s*key,/);
});

function installFakeIdb(job) {
  let opens = 0;
  let closes = 0;
  const modes = [];
  ctx.indexedDB = {
    open(name) {
      opens++;
      assert.equal(name, 'ymb_search_async_items_v2');
      const request = { transaction: { abort() { throw new Error('unexpected abort'); } } };
      const db = {
        objectStoreNames: { contains: value => value === 'jobs' },
        close() { closes++; },
        transaction(names, mode) {
          assert.deepEqual(Array.from(names), ['jobs']);
          modes.push(mode);
          const tx = {};
          tx.objectStore = name => {
            assert.equal(name, 'jobs');
            return {
              get(key) {
                assert.equal(key, 'job1');
                const getRequest = {};
                queueMicrotask(() => {
                  getRequest.result = structuredClone(job);
                  getRequest.onsuccess?.();
                  queueMicrotask(() => tx.oncomplete?.());
                });
                return getRequest;
              }
            };
          };
          return tx;
        }
      };
      queueMicrotask(() => {
        request.result = db;
        request.onsuccess?.();
      });
      return request;
    }
  };
  return {
    get opens() { return opens; },
    get closes() { return closes; },
    modes
  };
}

test('production default IndexedDB fallback reads jobs readonly and closes DB', async () => {
  const idb = installFakeIdb(terminalJob());
  const store = storeFixture({ storedOwner: 'old-owner' });
  const artifacts = artifactFixture();
  const api = E.create({ store, artifacts, now: () => 1000, authorize: async ({ owner }) => owner === 'new-owner' });
  const out = await api.stagePage(args({ deliveryId: 'd-default' }));
  assert.equal(out.report.item_count, 1);
  assert.equal(idb.opens, 1);
  assert.equal(idb.closes, 1);
  assert.deepEqual(idb.modes, ['readonly']);
  delete ctx.indexedDB;
});

test('production default path fails closed without IndexedDB', async () => {
  delete ctx.indexedDB;
  const api = E.create({
    store: storeFixture({ storedOwner: 'old-owner' }),
    artifacts: artifactFixture(),
    now: () => 1000,
    authorize: async () => true
  });
  await assert.rejects(
    api.stagePage(args({ deliveryId: 'd-no-idb' })),
    error => error.code === 'EXPORT_CROSS_OWNER_METADATA_UNAVAILABLE' && error.request_executed === false
  );
});
