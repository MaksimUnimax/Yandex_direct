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
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'ymb-gensearch-browser-'));
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
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.text || 'service worker evaluation failed');
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
    globalThis.__YMB_GENSEARCH_FETCHES = [];
    await globalThis.YMBCredentialRuntime.save('search', {
      api_key: 'browser-search-secret',
      folder_id: 'folder-1'
    });
    globalThis.fetch = async (url, options = {}) => {
      const target = String(url || '');
      const headers = options.headers || {};
      const readHeader = (name) => {
        try {
          if (headers instanceof Headers) return headers.get(name) || '';
          const key = Object.keys(headers).find((item) => String(item).toLowerCase() === String(name).toLowerCase());
          return key ? String(headers[key] || '') : '';
        } catch { return ''; }
      };
      globalThis.__YMB_GENSEARCH_FETCHES.push({
        url: target,
        method: String(options.method || 'GET').toUpperCase(),
        authorization: readHeader('Authorization'),
        content_type: readHeader('Content-Type'),
        body: String(options.body || '')
      });
      if (target !== 'https://searchapi.api.cloud.yandex.net/v2/gen/search') {
        throw new Error('CONTROLLED_GENSEARCH_UNEXPECTED_PROVIDER_HOST');
      }
      const payload = [{
        message: { content: 'Контролируемый GenSearch ответ', role: 'ROLE_ASSISTANT' },
        sources: [
          { url: 'https://example.test/used', title: 'Used source', used: true },
          { url: 'https://example.test/not-used', title: 'Not used source', used: false }
        ],
        searchQueries: [{ text: 'печать велеса', reqId: 'browser-req-1' }],
        fixedMisspellQuery: '',
        isAnswerRejected: false,
        isBulletAnswer: false,
        hints: ['Как использовать символ?'],
        problematicAnswer: false
      }];
      return new Response(JSON.stringify(payload), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      });
    };
    return true;
  })()`);

  const executed = await workerEval(workerClient, `(async () => {
    const result = await globalThis.YMBPhase3ProviderRuntime.execute(
      'search',
      { method: 'genSearch', queryText: 'печать велеса', confirmBillable: true },
      { channel: 'manual', operation: 'genSearch' }
    );
    return {
      ok: result.ok,
      http_status: result.http_status,
      request_id: result.request_id,
      envelope: result.report_envelope,
      report_text: result.report_text,
      fetches: globalThis.__YMB_GENSEARCH_FETCHES
    };
  })()`);

  assert.equal(executed.ok, true);
  assert.equal(executed.http_status, 200);
  assert.match(executed.request_id, /^search-/);
  assert.equal(executed.fetches.length, 1);
  const request = executed.fetches[0];
  assert.equal(request.url, 'https://searchapi.api.cloud.yandex.net/v2/gen/search');
  assert.equal(request.method, 'POST');
  assert.equal(request.authorization, 'Api-Key browser-search-secret');
  assert.equal(request.content_type, 'application/json');

  const body = JSON.parse(request.body);
  assert.deepEqual(body, {
    messages: [{ content: 'печать велеса', role: 'ROLE_USER' }],
    folderId: 'folder-1',
    fixMisspell: true,
    getPartialResults: false
  });
  assert.equal(Object.hasOwn(body, 'searchType'), false);
  assert.equal(Object.hasOwn(body, 'region'), false);
  console.log('GENSEARCH_BROWSER_ONE_REQUEST_PASS');
  console.log('GENSEARCH_BROWSER_PROVIDER_CONTRACT_PASS');

  const envelope = executed.envelope;
  assert.equal(envelope.service, 'search');
  assert.equal(envelope.operation, 'genSearch');
  assert.equal(envelope.status, 'OK');
  assert.equal(envelope.request_executed, true);
  assert.equal(envelope.automatic_retry, false);
  assert.equal(envelope.result.mode, 'generative');
  assert.equal(envelope.result.message.content, 'Контролируемый GenSearch ответ');
  assert.equal(envelope.result.sources[0].used, true);
  assert.equal(envelope.result.sources[1].used, false);
  assert.equal(envelope.result.searchQueries[0].text, 'печать велеса');
  assert.equal(envelope.result.searchQueries[0].reqId, 'browser-req-1');
  assert.equal(envelope.result.transport.wire_format, 'json_array');
  assert.equal(envelope.result.transport.frame_count, 1);
  assert.equal(Object.hasOwn(envelope.result, 'aliceFanout'), false);
  assert.equal(Object.hasOwn(envelope.result, 'ALICE_FANOUT_OBSERVED'), false);
  assert.equal(String(executed.report_text).includes('browser-search-secret'), false);
  console.log('GENSEARCH_BROWSER_RESPONSE_PROVENANCE_PASS');
  console.log('GENSEARCH_BROWSER_NO_RETRY_PASS');

  // A normal common-settings Save must preserve the current GenSearch policy
  // state even though the popup does not expose a GenSearch enable/disable toggle.
  await workerEval(workerClient, `(async () => {
    await chrome.storage.local.set({
      ymb_search_policy: {
        autorun_enabled: false,
        manual_enabled: true,
        allowed_methods: ['search', 'genSearch'],
        max_requests_per_run: 100,
        max_cost_rub_per_run: 10,
        method_cost_rub: { search: 0.488, genSearch: 5.08 },
        tariff_checked_at: '2026-08-28',
        tariff_source: 'https://aistudio.yandex.ru/docs/ru/search-api/pricing.html'
      }
    });
    return true;
  })()`);

  const popup = await browser.newPage();
  await popup.goto(`chrome-extension://${qa.extensionId}/popup.html`, { waitUntil: 'load', timeout: 15000 });
  await popup.waitForFunction(() => document.getElementById('status')?.textContent === 'Готово.', { timeout: 15000 });
  await popup.click('#saveSettings');
  await popup.waitForFunction(() => document.getElementById('status')?.textContent === 'Общие настройки сохранены.', { timeout: 15000 });
  let savedSearchPolicy = await workerEval(workerClient, `chrome.storage.local.get('ymb_search_policy').then(x => x.ymb_search_policy)`);
  assert.deepEqual(savedSearchPolicy.allowed_methods, ['search', 'genSearch']);
  assert.equal(savedSearchPolicy.method_cost_rub.genSearch, 5.08);
  console.log('GENSEARCH_BROWSER_POPUP_SAVE_PRESERVES_ENABLED_PASS');

  await workerEval(workerClient, `(async () => {
    const row = (await chrome.storage.local.get('ymb_search_policy')).ymb_search_policy;
    await chrome.storage.local.set({ ymb_search_policy: { ...row, allowed_methods: ['search'] } });
    return true;
  })()`);
  await popup.reload({ waitUntil: 'load', timeout: 15000 });
  await popup.waitForFunction(() => document.getElementById('status')?.textContent === 'Готово.', { timeout: 15000 });
  await popup.click('#saveSettings');
  await popup.waitForFunction(() => document.getElementById('status')?.textContent === 'Общие настройки сохранены.', { timeout: 15000 });
  savedSearchPolicy = await workerEval(workerClient, `chrome.storage.local.get('ymb_search_policy').then(x => x.ymb_search_policy)`);
  assert.deepEqual(savedSearchPolicy.allowed_methods, ['search']);
  assert.equal(savedSearchPolicy.method_cost_rub.genSearch, 5.08);
  console.log('GENSEARCH_BROWSER_POPUP_SAVE_PRESERVES_EXPLICIT_DISABLE_PASS');
  await popup.close();

  const fetchesAfter = await workerEval(workerClient, 'globalThis.__YMB_GENSEARCH_FETCHES');
  assert.equal(fetchesAfter.length, 1);
  console.log('GENSEARCH_BROWSER_REAL_YANDEX_REQUESTS=0');
  console.log('AI_NATIVE_GENSEARCH_BROWSER_RUNTIME_PASS');
} finally {
  await browser.close();
  fs.rmSync(qa.tempRoot, { recursive: true, force: true });
}
