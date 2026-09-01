import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createHash, generateKeyPairSync } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer';

const here = path.dirname(fileURLToPath(import.meta.url));
const sourceExtensionPath = fs.realpathSync(path.resolve(here, '../../src'));
const hostId = 'https:openscript.ru:443';
const taskId = '2f1c5d3b-7d9b-4c3e-8a14-9d8b924a12ef';
const downloadUrl = `https://storage.mds.yandex.net/get-webmaster-download/${taskId}`;
const allV013Methods = [
  'listHosts', 'getSummary', 'getDiagnostics', 'getPopularQueries',
  'getAllQueryHistory', 'getQueryHistory', 'getIndexingSamples', 'getInSearchSamples',
  'getExportRegions', 'getExportLimits', 'getExportDates', 'startQueryUrlExport',
  'getQueryUrlExportStatus', 'collectQueryUrlExport', 'readQueryUrlExportChunk'
];

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
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'ymb-webmaster-v013-browser-'));
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

async function send(page, message) {
  return page.evaluate((payload) => new Promise((resolve, reject) => {
    chrome.runtime.sendMessage(payload, (response) => {
      const error = chrome.runtime.lastError;
      if (error) reject(new Error(error.message || String(error)));
      else resolve(response);
    });
  }), message);
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

  await workerEval(workerClient, `(() => {
    globalThis.__YMB_WM13_FETCHES = [];
    globalThis.fetch = async (url, options = {}) => {
      const target = String(url || '');
      const method = String(options.method || 'GET').toUpperCase();
      const headers = options.headers || {};
      const readHeader = (name) => {
        try {
          if (headers instanceof Headers) return headers.get(name) || '';
          const key = Object.keys(headers).find((item) => String(item).toLowerCase() === String(name).toLowerCase());
          return key ? String(headers[key] || '') : '';
        } catch { return ''; }
      };
      globalThis.__YMB_WM13_FETCHES.push({
        url: target,
        method,
        authorization: readHeader('Authorization'),
        content_type: readHeader('Content-Type'),
        body: String(options.body || '')
      });

      if (target === 'https://api.webmaster.yandex.net/v4/user') {
        return new Response(JSON.stringify({ user_id: 42 }), { status: 200, headers: { 'Content-Type': 'application/json' } });
      }
      if (target.includes('/search-queries/all/history')) {
        return new Response(JSON.stringify({ indicators: { TOTAL_SHOWS: [{ date: '2026-08-31T00:00:00+03:00', value: 10 }], TOTAL_CLICKS: [{ date: '2026-08-31T00:00:00+03:00', value: 2 }] } }), { status: 200, headers: { 'Content-Type': 'application/json' } });
      }
      if (target.endsWith('/pro/limits')) {
        return new Response(JSON.stringify({ limits: [{ owner: 'u', feature: 'PRO_SERP', limit: 100, used: 0, remaining: 100, period_start: '2026-09-01', period_end: '2026-09-01', is_active: false, tariff_id: 'base' }] }), { status: 200, headers: { 'Content-Type': 'application/json' } });
      }
      if (target.endsWith('/pro/serp/dates')) {
        return new Response(JSON.stringify({ dates: ['2026-08-31'] }), { status: 200, headers: { 'Content-Type': 'application/json' } });
      }
      if (target.includes('/pro/regions')) {
        return new Response(JSON.stringify({ regions: [{ id: 213, name: 'Москва' }] }), { status: 200, headers: { 'Content-Type': 'application/json' } });
      }
      if (target.endsWith('/pro/serp/queries/download/') && method === 'POST') {
        return new Response(JSON.stringify({ task_id: '${taskId}', free_quota_used: 1, pro_quota_used: 0, total_quota_used: 1, free_quota_remaining: 99, pro_quota_remaining: 0 }), { status: 200, headers: { 'Content-Type': 'application/json' } });
      }
      if (target.endsWith('/pro/serp/queries/download/${taskId}') && method === 'GET') {
        return new Response(JSON.stringify({ download_status: 'SUCCESS', url: '${downloadUrl}' }), { status: 200, headers: { 'Content-Type': 'application/json' } });
      }
      if (target === '${downloadUrl}' && method === 'GET') {
        return new Response('date,host,URL,query,region,clicks,impressions,position\\n2026-08-31,openscript.ru,https://openscript.ru/,"чат, gpt",Москва,2,10,3.5\\n', { status: 200, headers: { 'Content-Type': 'text/csv' } });
      }
      throw new Error('WM13_CONTROLLED_BROWSER_UNEXPECTED_NETWORK:' + target);
    };
    return true;
  })()`);

  const page = await browser.newPage();
  await page.goto(`chrome-extension://${qa.extensionId}/popup.html`, { waitUntil: 'load' });
  await page.waitForSelector('#webmasterCredentials', { timeout: 15000 });
  await page.waitForFunction(() => document.querySelector('#saveWebmasterCredential')?.disabled === false);

  const ui = await page.evaluate(() => {
    const html = document.documentElement.getBoundingClientRect();
    const body = document.body.getBoundingClientRect();
    return {
      version: document.querySelector('#versionBadge')?.textContent || '',
      services: [...document.querySelectorAll('#activeService option')].map((option) => option.value),
      tokenType: document.querySelector('#webmasterOauthToken')?.type,
      saveText: document.querySelector('#saveWebmasterCredential')?.textContent,
      checkText: document.querySelector('#checkWebmasterCredential')?.textContent,
      htmlWidth: Math.round(html.width), htmlHeight: Math.round(html.height),
      bodyWidth: Math.round(body.width), bodyHeight: Math.round(body.height)
    };
  });
  assert.equal(ui.version, 'v0.1.3');
  assert.deepEqual(ui.services, ['wordstat', 'search', 'webmaster', 'metrika', 'direct']);
  assert.equal(ui.tokenType, 'password');
  assert.equal(ui.saveText, 'Save');
  assert.equal(ui.checkText, 'Check');
  assert.deepEqual([ui.htmlWidth, ui.htmlHeight, ui.bodyWidth, ui.bodyHeight], [430, 560, 430, 560]);
  console.log('WM13_BROWSER_POPUP_430X560_FIVE_SERVICE_PASS');

  await page.$eval('#webmasterCredentials', (node) => { node.open = true; });
  await page.$eval('#webmasterOauthToken', (node) => { node.value = 'browser-webmaster-secret'; });
  await page.click('#saveWebmasterCredential');
  await page.waitForFunction(() => document.querySelector('#saveWebmasterCredential')?.disabled === false);
  assert.equal(await page.$eval('#webmasterOauthToken', (node) => node.value), '');
  const publicSaved = await send(page, { type: 'YMB_GET_CREDENTIALS' });
  assert.equal(publicSaved.ok, true);
  assert.equal(publicSaved.credentials.webmaster.has_oauth_token, true);
  assert.equal(JSON.stringify(publicSaved).includes('browser-webmaster-secret'), false);
  assert.equal(await page.evaluate(() => document.body.innerText.includes('browser-webmaster-secret')), false);
  console.log('WM13_BROWSER_WEBMASTER_SECRET_REDACTION_PASS');

  // saveCredential() refreshes the popup and deliberately re-opens only the active-service card.
  // Re-open the Webmaster card before clicking its hidden Check button. This follows the
  // already-proven Phase-3 browser route and tests the real visible operator action.
  await page.$eval('#webmasterCredentials', (node) => { node.open = true; });
  await page.click('#checkWebmasterCredential');
  await page.waitForFunction(() => document.querySelector('#webmasterUserId')?.textContent === '42');
  assert.match(await page.$eval('#webmasterCredentialState', (node) => node.textContent || ''), /проверено/i);
  let fetches = await workerEval(workerClient, 'globalThis.__YMB_WM13_FETCHES');
  assert.equal(fetches.length, 1);
  assert.equal(fetches[0].url, 'https://api.webmaster.yandex.net/v4/user');
  assert.equal(fetches[0].method, 'GET');
  assert.equal(fetches[0].authorization, 'OAuth browser-webmaster-secret');
  console.log('WM13_BROWSER_WEBMASTER_CHECK_ONE_GET_PASS');

  let policy = await send(page, { type: 'YMB_GET_WEBMASTER_POLICY' });
  assert.equal(policy.ok, true);
  for (const method of allV013Methods) assert.ok(policy.policy.allowed_methods.includes(method), `missing ${method}`);
  await page.click('#saveSettingsTop');
  await page.waitForFunction(() => document.querySelector('#saveSettingsTop')?.disabled === false && document.querySelector('#status')?.textContent === 'Общие настройки сохранены.');
  policy = await send(page, { type: 'YMB_GET_WEBMASTER_POLICY' });
  for (const method of allV013Methods) assert.ok(policy.policy.allowed_methods.includes(method), `common Save shrank ${method}`);
  console.log('WM13_BROWSER_COMMON_SAVE_FULL_POLICY_PASS');

  const provider = await workerEval(workerClient, `(async () => {
    const history = await globalThis.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'getAllQueryHistory', hostId: '${hostId}', queryIndicators: ['TOTAL_SHOWS', 'TOTAL_CLICKS'], dateFrom: '2026-08-31', dateTo: '2026-08-31' });
    const limits = await globalThis.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'getExportLimits', hostId: '${hostId}' });
    const dates = await globalThis.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'getExportDates', hostId: '${hostId}' });
    const regions = await globalThis.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'getExportRegions', hostId: '${hostId}', filter: 'Моск', limit: 10 });
    const start = await globalThis.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'startQueryUrlExport', hostId: '${hostId}', dates: ['2026-08-31'], paths: ['/'], regionIds: [213], confirmQuota: true, expectedQuotaUnits: 1 });
    const status = await globalThis.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'getQueryUrlExportStatus', hostId: '${hostId}', taskId: '${taskId}' });
    const collect = await globalThis.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'collectQueryUrlExport', hostId: '${hostId}', taskId: '${taskId}', previewLimit: 1 });
    const chunk = await globalThis.YMBPhase5ProviderRuntime.executeWebmaster({ method: 'readQueryUrlExportChunk', taskId: '${taskId}', offset: 0, limit: 1 });
    const jobs = (await chrome.storage.local.get('ymb_webmaster_query_url_exports_v1')).ymb_webmaster_query_url_exports_v1 || {};
    return {
      history: history.report_envelope,
      limits: limits.report_envelope,
      dates: dates.report_envelope,
      regions: regions.report_envelope,
      start: start.report_envelope,
      status: status.report_envelope,
      collect: collect.report_envelope,
      chunk: chunk.report_envelope,
      job: jobs['${taskId}'] || null
    };
  })()`);

  assert.equal(provider.history.result.indicators.TOTAL_SHOWS[0].value, 10);
  assert.equal(provider.limits.result.limits[0].remaining, 100);
  assert.deepEqual(provider.dates.result.dates, ['2026-08-31']);
  assert.equal(provider.regions.result.regions[0].id, 213);
  assert.equal(provider.start.result.task_id, taskId);
  assert.equal(provider.start.result.projection.quota_units, 1);
  assert.equal(provider.status.result.download_status, 'SUCCESS');
  assert.equal(Object.hasOwn(provider.status.result, 'url'), false);
  assert.equal(provider.collect.result.manifest.row_count, 1);
  assert.equal(provider.collect.result.preview.rows[0].query, 'чат, gpt');
  assert.equal(provider.chunk.request_executed, false);
  assert.equal(provider.chunk.result.chunk.total, 1);
  assert.equal(provider.job.row_count, 1);
  assert.match(provider.job.raw_sha256, /^[0-9a-f]{64}$/);
  assert.equal(JSON.stringify(provider).includes('browser-webmaster-secret'), false);
  console.log('WM13_BROWSER_PROVIDER_EXPORT_LIFECYCLE_PASS');

  fetches = await workerEval(workerClient, 'globalThis.__YMB_WM13_FETCHES');
  assert.equal(fetches.length, 8, JSON.stringify(fetches));
  const apiFetches = fetches.slice(0, 7);
  const storageFetch = fetches[7];
  assert.ok(apiFetches.every((entry) => entry.url.startsWith('https://api.webmaster.yandex.net/')));
  assert.ok(apiFetches.every((entry) => entry.authorization === 'OAuth browser-webmaster-secret'));
  assert.equal(apiFetches.filter((entry) => entry.method === 'POST').length, 1);
  assert.equal(storageFetch.url, downloadUrl);
  assert.equal(storageFetch.method, 'GET');
  assert.equal(storageFetch.authorization, '');
  const startFetch = apiFetches.find((entry) => entry.method === 'POST');
  assert.deepEqual(JSON.parse(startFetch.body), { dates: ['2026-08-31'], paths: ['/'], region_ids: [213], use_pro_tariff: 'false' });
  console.log('WM13_BROWSER_BOUNDARY_ACCOUNTING_PASS');

  const backupResponse = await send(page, { type: 'WS_EXPORT_BACKUP' });
  assert.equal(backupResponse.ok, true);
  assert.equal(backupResponse.backup.settings.credentials.webmaster.oauth_token, 'browser-webmaster-secret');
  const mutated = await send(page, { type: 'YMB_SAVE_SERVICE_CREDENTIAL', service: 'webmaster', credential: { oauth_token: 'browser-mutated-webmaster-secret' } });
  assert.equal(mutated.ok, true);
  const imported = await send(page, { type: 'WS_IMPORT_BACKUP', backup: backupResponse.backup });
  assert.equal(imported.ok, true);
  const restored = await workerEval(workerClient, `(async () => {
    const credentials = await globalThis.YMBCredentialRuntime.load();
    return { token: credentials.webmaster.oauth_token, userId: credentials.webmaster.user_id, state: credentials.webmaster.check_state };
  })()`);
  assert.deepEqual(restored, { token: 'browser-webmaster-secret', userId: '42', state: 'PRESENT' });
  const publicAfterImport = await send(page, { type: 'YMB_GET_CREDENTIALS' });
  for (const secret of ['browser-webmaster-secret', 'browser-mutated-webmaster-secret']) assert.equal(JSON.stringify(publicAfterImport).includes(secret), false);
  console.log('WM13_BROWSER_BACKUP_SERVICE_ISOLATION_PASS');

  await page.reload({ waitUntil: 'load' });
  await page.waitForSelector('#webmasterCredentials', { timeout: 15000 });
  await page.waitForFunction(() => document.querySelector('#saveWebmasterCredential')?.disabled === false);
  assert.equal(await page.$eval('#webmasterOauthToken', (node) => node.value), '');
  assert.equal(await page.evaluate(() => document.body.innerText.includes('browser-webmaster-secret')), false);
  console.log('WM13_BROWSER_REOPEN_SECRET_BLANK_PASS');

  console.log('WM13_CONTROLLED_REAL_YANDEX_REQUESTS=0');
  console.log('WEBMASTER_V013_BROWSER_RUNTIME_PASS');
} finally {
  await browser.close();
  fs.rmSync(qa.tempRoot, { recursive: true, force: true });
}
