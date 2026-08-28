import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createHash, generateKeyPairSync } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer';

const here = path.dirname(fileURLToPath(import.meta.url));
const sourceExtensionPath = fs.realpathSync(path.resolve(here, '../../src'));

function extensionIdFromPublicKey(publicKeyDer) {
  const digest = createHash('sha256').update(publicKeyDer).digest().subarray(0, 16);
  let id = '';
  for (const byte of digest) {
    id += String.fromCharCode(97 + ((byte >> 4) & 0x0f));
    id += String.fromCharCode(97 + (byte & 0x0f));
  }
  return id;
}

function prepareQaExtension() {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'ymb-search-batch-browser-'));
  const extensionPath = path.join(tempRoot, 'extension');
  fs.cpSync(sourceExtensionPath, extensionPath, { recursive: true });
  const { publicKey } = generateKeyPairSync('rsa', {
    modulusLength: 2048,
    publicKeyEncoding: { type: 'spki', format: 'der' },
    privateKeyEncoding: { type: 'pkcs8', format: 'pem' }
  });
  const manifestPath = path.join(extensionPath, 'manifest.json');
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  manifest.key = Buffer.from(publicKey).toString('base64');
  fs.writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
  return { tempRoot, extensionPath, extensionId: extensionIdFromPublicKey(Buffer.from(publicKey)) };
}

async function workerEval(client, expression) {
  const result = await client.send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  if (result.exceptionDetails) {
    const detail = result.exceptionDetails.exception?.description || result.exceptionDetails.text || 'service worker evaluation failed';
    throw new Error(detail);
  }
  return result.result?.value;
}

const qa = prepareQaExtension();
assert.match(qa.extensionId, /^[a-p]{32}$/);
const browser = await puppeteer.launch({
  headless: false,
  pipe: true,
  enableExtensions: true,
  args: [
    '--no-sandbox',
    '--disable-gpu',
    '--disable-dev-shm-usage',
    '--disable-background-networking',
    `--disable-extensions-except=${qa.extensionPath}`,
    `--load-extension=${qa.extensionPath}`
  ]
});

try {
  const workerTarget = await browser.waitForTarget(
    (target) => target.type() === 'service_worker' && target.url().startsWith(`chrome-extension://${qa.extensionId}/`),
    { timeout: 15000 }
  );
  const workerClient = await workerTarget.createCDPSession();

  await workerEval(workerClient, `(async () => {
    globalThis.__YMB_SEARCH_BATCH_FETCHES = [];
    await globalThis.YMBCredentialRuntime.save('search', {
      api_key: 'search-batch-browser-secret',
      folder_id: 'folder-search-batch'
    });
    await chrome.storage.local.set({
      ymb_search_policy: {
        autorun_enabled: true,
        manual_enabled: true,
        allowed_methods: ['search'],
        max_requests_per_run: 1000,
        max_cost_rub_per_run: 1000,
        method_cost_rub: { search: 0.488, genSearch: 5.08 },
        tariff_checked_at: '2026-08-28',
        tariff_source: 'controlled-browser-test'
      }
    });

    const b64 = (text) => btoa(unescape(encodeURIComponent(text)));
    const xmlFor = (query) => {
      const domains = query === 'alpha'
        ? ['a.test', 'shared.test', 'alpha-only.test']
        : query === 'beta'
          ? ['shared.test', 'b.test', 'beta-only.test']
          : ['unknown.test'];
      const docs = domains.map((domain, index) => '<doc><url>https://' + domain + '/p' + (index + 1) + '</url><domain>' + domain + '</domain><title>' + query + '-' + (index + 1) + '</title><passage>fixture</passage></doc>').join('');
      return '<yandexsearch><response>' + docs + '</response></yandexsearch>';
    };

    globalThis.fetch = async (url, options = {}) => {
      const target = String(url || '');
      const body = String(options.body || '');
      const parsedBody = body ? JSON.parse(body) : {};
      const query = String(parsedBody?.query?.queryText || '');
      const headers = options.headers || {};
      const readHeader = (name) => {
        try {
          if (headers instanceof Headers) return headers.get(name) || '';
          const key = Object.keys(headers).find((item) => String(item).toLowerCase() === String(name).toLowerCase());
          return key ? String(headers[key] || '') : '';
        } catch { return ''; }
      };
      globalThis.__YMB_SEARCH_BATCH_FETCHES.push({
        url: target,
        method: String(options.method || 'GET').toUpperCase(),
        authorization: readHeader('Authorization'),
        content_type: readHeader('Content-Type'),
        body,
        query
      });
      if (target !== 'https://searchapi.api.cloud.yandex.net/v2/web/search') {
        throw new Error('CONTROLLED_SEARCH_BATCH_UNEXPECTED_PROVIDER_HOST');
      }
      if (query === 'unknown') throw new Error('CONTROLLED_UNKNOWN_OUTCOME');
      return new Response(JSON.stringify({ rawData: b64(xmlFor(query)) }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      });
    };
    return true;
  })()`);

  const start = await workerEval(workerClient, `(async () => {
    const result = await globalThis.YMBSearchBatchWorkerTransport.executeSearchBatchCommand({
      action: 'start',
      jobId: 'browser-job-success',
      queries: ['alpha', 'beta'],
      searchType: 'SEARCH_TYPE_RU',
      region: '225',
      groupsOnPage: 10,
      maxRequests: 2,
      maxCostRub: 1,
      confirmBillable: true
    }, { channel: 'manual' });
    return { result, fetches: globalThis.__YMB_SEARCH_BATCH_FETCHES };
  })()`);
  assert.equal(start.result.report_envelope.operation, 'batch.start');
  assert.equal(start.result.request_executed, false);
  assert.equal(start.result.report_envelope.progress.total, 2);
  assert.equal(start.fetches.length, 0);
  console.log('PHASE8_SEARCH_BATCH_BROWSER_START_ZERO_PROVIDER_PASS');

  const first = await workerEval(workerClient, `(async () => {
    const result = await globalThis.YMBSearchBatchWorkerTransport.executeSearchBatchCommand({ action: 'next', jobId: 'browser-job-success' }, { channel: 'manual' });
    return { result, fetches: globalThis.__YMB_SEARCH_BATCH_FETCHES };
  })()`);
  assert.equal(first.result.request_executed, true);
  assert.equal(first.result.report_envelope.progress.succeeded, 1);
  assert.equal(first.fetches.length, 1);
  assert.equal(first.fetches[0].url, 'https://searchapi.api.cloud.yandex.net/v2/web/search');
  assert.equal(first.fetches[0].method, 'POST');
  assert.equal(first.fetches[0].authorization, 'Api-Key search-batch-browser-secret');
  assert.equal(first.fetches[0].query, 'alpha');
  const firstBody = JSON.parse(first.fetches[0].body);
  assert.equal(firstBody.query.searchType, 'SEARCH_TYPE_RU');
  assert.equal(firstBody.query.page, '0');
  assert.equal(firstBody.groupSpec.groupsOnPage, '10');
  assert.equal(firstBody.groupSpec.docsInGroup, '1');
  assert.equal(firstBody.region, '225');
  assert.equal(Object.hasOwn(firstBody, 'messages'), false);
  console.log('PHASE8_SEARCH_BATCH_BROWSER_FIRST_NEXT_ONE_PROVIDER_PASS');

  const second = await workerEval(workerClient, `(async () => {
    const result = await globalThis.YMBSearchBatchWorkerTransport.executeSearchBatchCommand({ action: 'next', jobId: 'browser-job-success' }, { channel: 'manual' });
    return { result, fetches: globalThis.__YMB_SEARCH_BATCH_FETCHES };
  })()`);
  assert.equal(second.result.request_executed, true);
  assert.equal(second.result.report_envelope.progress.succeeded, 2);
  assert.equal(second.result.report_envelope.progress.requests_started, 2);
  assert.equal(second.fetches.length, 2);
  assert.deepEqual(second.fetches.map((row) => row.query), ['alpha', 'beta']);
  assert.equal(second.result.report_envelope.progress.estimated_cost_rub, 0.976);
  console.log('PHASE8_SEARCH_BATCH_BROWSER_SECOND_NEXT_EXACTLY_ONCE_PASS');

  const local = await workerEval(workerClient, `(async () => {
    const before = globalThis.__YMB_SEARCH_BATCH_FETCHES.length;
    const status = await globalThis.YMBSearchBatchWorkerTransport.executeSearchBatchCommand({ action: 'status', jobId: 'browser-job-success' }, { channel: 'manual' });
    const projection = await globalThis.YMBSearchBatchWorkerTransport.executeSearchBatchCommand({ action: 'projection', jobId: 'browser-job-success', offset: 0, limit: 10, topN: 3, targetDomains: ['shared.test'] }, { channel: 'manual' });
    const overlap = await globalThis.YMBSearchBatchWorkerTransport.executeSearchBatchCommand({ action: 'overlapPage', jobId: 'browser-job-success', offset: 0, limit: 10, topN: 3 }, { channel: 'manual' });
    const after = globalThis.__YMB_SEARCH_BATCH_FETCHES.length;
    return { before, after, status: status.report_envelope, projection: projection.report_envelope, overlap: overlap.report_envelope };
  })()`);
  assert.equal(local.before, 2);
  assert.equal(local.after, 2);
  assert.equal(local.status.progress.succeeded, 2);
  assert.equal(local.projection.request_executed, false);
  assert.equal(local.projection.projection.items.length, 2);
  assert.equal(local.projection.projection.items[0].target_domains[0].best_rank_within_observed_topN, 2);
  assert.equal(local.projection.projection.items[1].target_domains[0].best_rank_within_observed_topN, 1);
  assert.equal(local.overlap.request_executed, false);
  assert.equal(local.overlap.projection.total_pairs, 1);
  assert.equal(local.overlap.projection.items[0].shared_count, 1);
  assert.deepEqual(local.overlap.projection.items[0].shared_domains, ['shared.test']);
  console.log('PHASE8_SEARCH_BATCH_BROWSER_LOCAL_PROJECTION_ZERO_PROVIDER_PASS');
  console.log('PHASE8_SEARCH_BATCH_BROWSER_OVERLAP_MATH_PASS');

  const unknown = await workerEval(workerClient, `(async () => {
    const start = await globalThis.YMBSearchBatchWorkerTransport.executeSearchBatchCommand({
      action: 'start', jobId: 'browser-job-unknown', queries: ['unknown'], searchType: 'SEARCH_TYPE_RU', region: '225', groupsOnPage: 10, maxRequests: 1, maxCostRub: 1, confirmBillable: true
    }, { channel: 'manual' });
    const before = globalThis.__YMB_SEARCH_BATCH_FETCHES.length;
    const first = await globalThis.YMBSearchBatchWorkerTransport.executeSearchBatchCommand({ action: 'next', jobId: 'browser-job-unknown' }, { channel: 'manual' });
    const afterFirst = globalThis.__YMB_SEARCH_BATCH_FETCHES.length;
    const second = await globalThis.YMBSearchBatchWorkerTransport.executeSearchBatchCommand({ action: 'next', jobId: 'browser-job-unknown' }, { channel: 'manual' });
    const afterSecond = globalThis.__YMB_SEARCH_BATCH_FETCHES.length;
    return { start: start.report_envelope, first: first.report_envelope, second: second.report_envelope, before, afterFirst, afterSecond };
  })()`);
  assert.equal(unknown.start.request_executed, false);
  assert.equal(unknown.before, 2);
  assert.equal(unknown.afterFirst, 3);
  assert.equal(unknown.afterSecond, 3);
  assert.equal(unknown.first.request_executed, 'UNKNOWN');
  assert.equal(unknown.first.automatic_retry, false);
  assert.equal(unknown.first.progress.outcome_unknown, 1);
  assert.equal(unknown.first.progress.next_safe_action, 'RECONCILE_UNKNOWN');
  assert.equal(unknown.second.request_executed, false);
  assert.equal(unknown.second.reason, 'OUTCOME_UNKNOWN_REQUIRES_RECONCILIATION');
  console.log('PHASE8_SEARCH_BATCH_BROWSER_UNKNOWN_NO_REPLAY_PASS');

  const fiveHundred = await workerEval(workerClient, `(async () => {
    const queries = Array.from({ length: 500 }, (_, index) => 'bulk-' + String(index + 1));
    const before = globalThis.__YMB_SEARCH_BATCH_FETCHES.length;
    const result = await globalThis.YMBSearchBatchWorkerTransport.executeSearchBatchCommand({
      action: 'start', jobId: 'browser-job-500', queries, searchType: 'SEARCH_TYPE_RU', region: '225', groupsOnPage: 10, maxRequests: 500, maxCostRub: 244, confirmBillable: true
    }, { channel: 'manual' });
    const after = globalThis.__YMB_SEARCH_BATCH_FETCHES.length;
    return { envelope: result.report_envelope, before, after };
  })()`);
  assert.equal(fiveHundred.before, 3);
  assert.equal(fiveHundred.after, 3);
  assert.equal(fiveHundred.envelope.progress.total, 500);
  assert.equal(fiveHundred.envelope.progress.requests_started, 0);
  assert.equal(fiveHundred.envelope.request_executed, false);
  console.log('PHASE8_SEARCH_BATCH_BROWSER_500_START_ZERO_PROVIDER_PASS');

  const safeState = await workerEval(workerClient, `(async () => {
    const data = await chrome.storage.local.get('ymb_search_batch_jobs_v1');
    return {
      fetches: globalThis.__YMB_SEARCH_BATCH_FETCHES,
      jobCount: Object.keys(data.ymb_search_batch_jobs_v1 || {}).length,
      storageText: JSON.stringify(data.ymb_search_batch_jobs_v1 || {})
    };
  })()`);
  assert.equal(safeState.jobCount, 3);
  assert.equal(safeState.fetches.length, 3);
  assert.equal(safeState.storageText.includes('search-batch-browser-secret'), false);
  assert.equal(safeState.fetches.every((row) => row.url === 'https://searchapi.api.cloud.yandex.net/v2/web/search'), true);
  console.log('PHASE8_SEARCH_BATCH_BROWSER_CREDENTIAL_NOT_PERSISTED_IN_JOB_PASS');
  console.log('PHASE8_SEARCH_BATCH_BROWSER_REAL_YANDEX_REQUESTS=0');
  console.log('PHASE8_SEARCH_BATCH_BROWSER_RUNTIME_PASS');
} finally {
  await browser.close();
  fs.rmSync(qa.tempRoot, { recursive: true, force: true });
}
