import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer';

const here = path.dirname(fileURLToPath(import.meta.url));
const sourceExtensionPath = fs.realpathSync(path.resolve(here, '../../src'));

function prepareQaExtension() {
  const sourceManifest = JSON.parse(fs.readFileSync(path.join(sourceExtensionPath, 'manifest.json'), 'utf8'));
  assert.equal(Object.hasOwn(sourceManifest, 'key'), false);
  assert.equal(sourceManifest.permissions.includes('identity'), false);
  assert.equal(sourceManifest.host_permissions.some((item) => String(item).includes('googleapis.com')), false);
  assert.equal(Object.hasOwn(sourceManifest, 'oauth2'), false);

  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'ymb-gsc-browser-'));
  const extensionPath = path.join(tempRoot, 'extension');
  fs.cpSync(sourceExtensionPath, extensionPath, { recursive: true });
  return { tempRoot, extensionPath };
}

async function workerEval(client, expression) {
  const result = await client.send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.text || 'service worker evaluation failed');
  return result.result?.value;
}

const qa = prepareQaExtension();
const browser = await puppeteer.launch({
  headless: false,
  pipe: true,
  enableExtensions: true,
  args: [
    '--no-sandbox',
    '--disable-gpu',
    '--disable-dev-shm-usage',
    `--disable-extensions-except=${qa.extensionPath}`,
    `--load-extension=${qa.extensionPath}`
  ]
});

try {
  const workerTarget = await browser.waitForTarget(
    (target) => target.type() === 'service_worker' && /^chrome-extension:\/\/[a-p]{32}\//.test(target.url()),
    { timeout: 15000 }
  );
  const extensionId = workerTarget.url().match(/^chrome-extension:\/\/([a-p]{32})\//)?.[1] || '';
  assert.match(extensionId, /^[a-p]{32}$/);
  const workerClient = await workerTarget.createCDPSession();

  const bootstrap = await workerEval(workerClient, `(() => {
    const gsc = globalThis.protocolForService('google_search_console');
    const search = globalThis.protocolForService('search');
    return {
      runtime_id: chrome.runtime.id,
      worker_service: globalThis.YMBGoogleSearchConsoleWorkerRuntime?.SERVICE || null,
      gsc_prefix: gsc?.PREFIX || null,
      search_prefix: search?.PREFIX || null
    };
  })()`);
  assert.equal(bootstrap.runtime_id, extensionId);
  assert.equal(bootstrap.worker_service, 'google_search_console');
  assert.equal(bootstrap.gsc_prefix, 'GOOGLE_SEARCH_CONSOLE_API_V1');
  assert.equal(bootstrap.search_prefix, 'SEARCH_API_V1');
  console.log('P9_GSC_BROWSER_EXISTING_IDENTITY_UNTOUCHED_PASS');
  console.log('P9_GSC_BROWSER_BOOTSTRAP_ROUTE_PASS');

  await workerEval(workerClient, `(async () => {
    globalThis.__YMB_GSC_TEST__ = true;
    globalThis.__YMB_GSC_BROWSER_CALLS = { identity: [], fetches: [] };
    globalThis.YMBGoogleSearchConsoleWorkerRuntime.configureForTest({
      identity: {
        async getAccessToken(options = {}) {
          globalThis.__YMB_GSC_BROWSER_CALLS.identity.push({ interactive: options?.interactive === true });
          return 'browser-gsc-secret';
        }
      },
      fetchImpl: async (url, options = {}) => {
        const target = String(url || '');
        const headers = options.headers || {};
        globalThis.__YMB_GSC_BROWSER_CALLS.fetches.push({
          url: target,
          method: String(options.method || 'GET').toUpperCase(),
          authorization: String(headers.Authorization || ''),
          content_type: String(headers['Content-Type'] || ''),
          body: String(options.body || '')
        });
        if (target === 'https://www.googleapis.com/webmasters/v3/sites') {
          return new Response(JSON.stringify({ siteEntry: [{ siteUrl: 'sc-domain:example.com', permissionLevel: 'siteOwner' }] }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
          });
        }
        if (target === 'https://www.googleapis.com/webmasters/v3/sites/sc-domain%3Aexample.com/searchAnalytics/query') {
          return new Response(JSON.stringify({
            rows: [{ keys: ['widget', 'https://example.com/page'], clicks: 5, impressions: 100, ctr: 0.05, position: 3.2 }],
            responseAggregationType: 'byProperty'
          }), { status: 200, headers: { 'Content-Type': 'application/json' } });
        }
        throw new Error('CONTROLLED_GSC_UNEXPECTED_PROVIDER_HOST');
      }
    });
    return true;
  })()`);

  const listSites = await workerEval(workerClient, `(async () => {
    const result = await globalThis.executeServiceCommand('google_search_console', { method: 'listSites' }, { channel: 'manual' });
    return { ok: result.ok, envelope: result.report_envelope, report_text: result.report_text, calls: globalThis.__YMB_GSC_BROWSER_CALLS };
  })()`);
  assert.equal(listSites.ok, true);
  assert.deepEqual(listSites.calls.identity, [{ interactive: false }]);
  assert.equal(listSites.calls.fetches.length, 1);
  assert.deepEqual(listSites.calls.fetches[0], {
    url: 'https://www.googleapis.com/webmasters/v3/sites',
    method: 'GET',
    authorization: 'Bearer browser-gsc-secret',
    content_type: '',
    body: ''
  });
  assert.equal(listSites.envelope.service, 'google_search_console');
  assert.equal(listSites.envelope.operation, 'listSites');
  assert.equal(listSites.envelope.request_executed, true);
  assert.equal(listSites.envelope.automatic_retry, false);
  assert.deepEqual(listSites.envelope.result.sites, [{ site_url: 'sc-domain:example.com', permission_level: 'siteOwner' }]);
  assert.equal(String(listSites.report_text).includes('browser-gsc-secret'), false);
  console.log('P9_GSC_BROWSER_LIST_SITES_ONE_REQUEST_PASS');

  const analytics = await workerEval(workerClient, `(async () => {
    const result = await globalThis.executeServiceCommand('google_search_console', {
      method: 'searchAnalytics',
      siteUrl: 'sc-domain:example.com',
      startDate: '2026-08-01',
      endDate: '2026-08-07',
      dimensions: ['query', 'page'],
      rowLimit: 25,
      startRow: 0,
      dataState: 'final'
    }, { channel: 'manual' });
    return { ok: result.ok, envelope: result.report_envelope, report_text: result.report_text, calls: globalThis.__YMB_GSC_BROWSER_CALLS };
  })()`);
  assert.equal(analytics.ok, true);
  assert.equal(analytics.calls.identity.length, 2);
  assert.deepEqual(analytics.calls.identity[1], { interactive: false });
  assert.equal(analytics.calls.fetches.length, 2);
  const request = analytics.calls.fetches[1];
  assert.equal(request.url, 'https://www.googleapis.com/webmasters/v3/sites/sc-domain%3Aexample.com/searchAnalytics/query');
  assert.equal(request.method, 'POST');
  assert.equal(request.authorization, 'Bearer browser-gsc-secret');
  assert.equal(request.content_type, 'application/json');
  assert.deepEqual(JSON.parse(request.body), {
    startDate: '2026-08-01',
    endDate: '2026-08-07',
    type: 'web',
    dimensions: ['query', 'page'],
    rowLimit: 25,
    startRow: 0,
    dataState: 'final'
  });
  assert.equal(analytics.envelope.result.position_semantics, 'average_topmost_position_over_impressions');
  assert.deepEqual(analytics.envelope.result.rows, [{
    keys: ['widget', 'https://example.com/page'],
    clicks: 5,
    impressions: 100,
    ctr: 0.05,
    average_position: 3.2
  }]);
  assert.equal(String(analytics.report_text).includes('browser-gsc-secret'), false);
  console.log('P9_GSC_BROWSER_SEARCH_ANALYTICS_ONE_REQUEST_PASS');

  const autorun = await workerEval(workerClient, `(async () => {
    const before = { identity: globalThis.__YMB_GSC_BROWSER_CALLS.identity.length, fetches: globalThis.__YMB_GSC_BROWSER_CALLS.fetches.length };
    const result = await globalThis.executeServiceCommand('google_search_console', { method: 'listSites' }, { channel: 'autorun' });
    return { result, before, after: { identity: globalThis.__YMB_GSC_BROWSER_CALLS.identity.length, fetches: globalThis.__YMB_GSC_BROWSER_CALLS.fetches.length } };
  })()`);
  assert.equal(autorun.result.ok, false);
  assert.equal(autorun.result.skipped, true);
  assert.equal(autorun.result.report_envelope.reason, 'AUTORUN_DISABLED');
  assert.deepEqual(autorun.after, autorun.before);
  console.log('P9_GSC_BROWSER_AUTORUN_NO_REQUEST_PASS');

  const storageText = await workerEval(workerClient, `chrome.storage.local.get(null).then((value) => JSON.stringify(value))`);
  assert.equal(String(storageText).includes('browser-gsc-secret'), false);
  assert.equal(String(listSites.report_text).includes('browser-gsc-secret'), false);
  assert.equal(String(analytics.report_text).includes('browser-gsc-secret'), false);
  console.log('P9_GSC_BROWSER_TOKEN_REDACTION_PASS');

  await workerEval(workerClient, `(() => {
    globalThis.YMBGoogleSearchConsoleWorkerRuntime.configureForTest(null);
    globalThis.__YMB_GSC_TEST__ = false;
    return true;
  })()`);
  console.log('P9_GSC_BROWSER_REAL_GOOGLE_REQUESTS=0');
  console.log('P9_GSC_BROWSER_REAL_YANDEX_REQUESTS=0');
  console.log('PHASE9_GSC_CONTROLLED_BROWSER_PASS');
} finally {
  await browser.close();
  fs.rmSync(qa.tempRoot, { recursive: true, force: true });
}
