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
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'ymb-phase4-metrika-browser-'));
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

async function saveCredentialThroughPopup(page, service, fields) {
  const cap = service[0].toUpperCase() + service.slice(1);
  await page.$eval(`#${service}Credentials`, (node) => { node.open = true; });
  for (const [selector, value] of Object.entries(fields)) {
    await page.$eval(selector, (node, next) => { node.value = next; }, value);
  }
  await page.click(`#save${cap}Credential`);
  await page.waitForFunction((buttonId) => document.querySelector(buttonId)?.disabled === false, {}, `#save${cap}Credential`);
  for (const selector of Object.keys(fields).filter((selector) => /ApiKey|OauthToken/.test(selector))) {
    assert.equal(await page.$eval(selector, (node) => node.value), '');
  }
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
    globalThis.__YMB_M4_FETCHES = [];
    globalThis.fetch = async (url, options = {}) => {
      const target = String(url || '');
      const method = String(options.method || 'GET').toUpperCase();
      const headers = options.headers || {};
      let auth = '';
      try {
        if (headers instanceof Headers) auth = headers.get('Authorization') || '';
        else {
          const key = Object.keys(headers).find((name) => String(name).toLowerCase() === 'authorization');
          auth = key ? String(headers[key] || '') : '';
        }
      } catch {}
      globalThis.__YMB_M4_FETCHES.push({
        url: target,
        method,
        has_authorization: auth.startsWith('OAuth ') && auth.length > 6,
        auth_scheme_exact: /^OAuth [^\\s].*$/.test(auth)
      });
      const json = (value, status = 200) => new Response(JSON.stringify(value), { status, headers: { 'Content-Type': 'application/json' } });
      if (!target.startsWith('https://api-metrika.yandex.net/')) throw new Error('CONTROLLED_BROWSER_UNEXPECTED_PROVIDER_HOST');
      if (target.includes('/management/v1/counters?per_page=1')) return json({ rows: 0, counters: [] });
      if (target.includes('/management/v1/counters?')) return json({ rows: 1, counters: [{ id: 123, name: 'QA counter', site: 'qa.invalid', status: 'Active', permission: 'own', owner_login: 'qa-owner', favorite: false, ignored: 'drop-me' }] });
      if (target.includes('/stat/v1/data?')) return json({ totals: [12, 8, 30], sampled: false, total_rows: 1, contains_sensitive_data: false });
      if (target.includes('/stat/v1/data/bytime?')) return json({ data: [{ metrics: [[1,2],[1,2],[3,4]] }], totals: [[3],[3],[7]], sampled: false, total_rows: 2 });
      if (/\/management\/v1\/counter\/123(?:\\?|$)/.test(target)) return json({ counter: { id: 123, name: 'QA counter', site: 'qa.invalid', status: 'Active', permission: 'own' } });
      throw new Error('CONTROLLED_BROWSER_UNEXPECTED_METRIKA_ROUTE');
    };
    return true;
  })()`);

  const page = await browser.newPage();
  await page.goto(`chrome-extension://${qa.extensionId}/popup.html`, { waitUntil: 'load' });
  await page.waitForSelector('#credentialsSection', { timeout: 15000 });
  await page.waitForFunction(() => document.querySelector('#versionBadge')?.textContent?.startsWith('v'));
  await page.waitForFunction(() => document.querySelector('#saveMetrikaCredential')?.disabled === false);

  const geometry = await page.evaluate(() => ({
    htmlWidth: document.documentElement.getBoundingClientRect().width,
    htmlHeight: document.documentElement.getBoundingClientRect().height,
    bodyWidth: document.body.getBoundingClientRect().width,
    bodyHeight: document.body.getBoundingClientRect().height,
    bodyScrollHeight: document.body.scrollHeight
  }));
  assert.equal(geometry.htmlWidth, 430);
  assert.equal(geometry.htmlHeight, 560);
  assert.equal(geometry.bodyWidth, 430);
  assert.equal(geometry.bodyHeight, 560);
  assert.ok(geometry.bodyScrollHeight >= geometry.bodyHeight);

  const ui = await page.evaluate(() => ({
    services: [...document.querySelectorAll('#activeService option')].map((option) => option.value),
    metrikaType: document.querySelector('#metrikaOauthToken')?.type,
    metrikaCost: document.querySelector('#metrikaCost')?.value,
    metrikaMaxDays: document.querySelector('#metrikaMaxReportDays')?.value,
    metrikaSaveText: document.querySelector('#saveMetrikaCredential')?.textContent,
    metrikaCheckText: document.querySelector('#checkMetrikaCredential')?.textContent
  }));
  assert.deepEqual(ui.services, ['wordstat', 'search', 'webmaster', 'metrika']);
  assert.equal(ui.metrikaType, 'password');
  assert.equal(ui.metrikaCost, '0 ₽');
  assert.equal(ui.metrikaMaxDays, '366');
  assert.equal(ui.metrikaSaveText, 'Save');
  assert.equal(ui.metrikaCheckText, 'Check');
  console.log('M15_POPUP_GEOMETRY_AND_FOUR_SERVICE_UI_PASS');

  await saveCredentialThroughPopup(page, 'wordstat', {
    '#wordstatApiKey': 'm4-wordstat-secret',
    '#wordstatFolderId': 'm4-wordstat-folder'
  });
  await saveCredentialThroughPopup(page, 'search', {
    '#searchApiKey': 'm4-search-secret',
    '#searchFolderId': 'm4-search-folder'
  });
  await saveCredentialThroughPopup(page, 'webmaster', {
    '#webmasterOauthToken': 'm4-webmaster-oauth'
  });
  await saveCredentialThroughPopup(page, 'metrika', {
    '#metrikaOauthToken': 'm4-metrika-oauth'
  });

  const publicBeforeCheck = await send(page, { type: 'YMB_GET_CREDENTIALS' });
  assert.equal(publicBeforeCheck.ok, true);
  assert.equal(publicBeforeCheck.credentials.wordstat.folder_id, 'm4-wordstat-folder');
  assert.equal(publicBeforeCheck.credentials.search.folder_id, 'm4-search-folder');
  assert.equal(publicBeforeCheck.credentials.metrika.has_oauth_token, true);
  const publicText = JSON.stringify(publicBeforeCheck);
  for (const secret of ['m4-wordstat-secret', 'm4-search-secret', 'm4-webmaster-oauth', 'm4-metrika-oauth']) {
    assert.equal(publicText.includes(secret), false);
    assert.equal(await page.evaluate((value) => document.body.innerText.includes(value), secret), false);
  }
  console.log('M15_CREDENTIAL_SAVE_RERENDER_SECRET_REDACTION_PASS');

  await page.$eval('#metrikaCredentials', (node) => { node.open = true; });
  await page.click('#checkMetrikaCredential');
  await page.waitForFunction(() => /проверено/i.test(document.querySelector('#metrikaCredentialState')?.textContent || '') && document.querySelector('#checkMetrikaCredential')?.disabled === false);
  assert.equal(await page.$eval('#metrikaOauthToken', (node) => node.value), '');

  const afterCheck = await send(page, { type: 'YMB_GET_CREDENTIALS' });
  assert.equal(afterCheck.credentials.metrika.check_state, 'PRESENT');
  let fetches = await workerEval(workerClient, 'globalThis.__YMB_M4_FETCHES');
  assert.equal(fetches.length, 1);
  assert.equal(fetches[0].method, 'GET');
  assert.equal(fetches[0].url, 'https://api-metrika.yandex.net/management/v1/counters?per_page=1');
  assert.equal(fetches[0].has_authorization, true);
  assert.equal(fetches[0].auth_scheme_exact, true);
  console.log('M05_M15_METRIKA_CHECK_ONE_GET_PASS');

  const direct = await workerEval(workerClient, `(async () => {
    const list = await globalThis.YMBPhase4ProviderRuntime.executeMetrika({ method: 'listCounters', page: 2, perPage: 10 });
    const summary = await globalThis.YMBPhase4ProviderRuntime.executeMetrika({ method: 'getTrafficSummary', counterId: 123, dateFrom: '2026-08-01', dateTo: '2026-08-07' });
    return {
      list: { ok: list.ok, status: list.http_status, prefix: String(list.report_text || '').split('\\n')[0], result: list.report_envelope?.result },
      summary: { ok: summary.ok, status: summary.http_status, prefix: String(summary.report_text || '').split('\\n')[0], result: summary.report_envelope?.result }
    };
  })()`);
  assert.equal(direct.list.ok, true);
  assert.equal(direct.list.status, 200);
  assert.equal(direct.list.prefix, 'METRIKA_RESULT_V1');
  assert.equal(direct.list.result.rows, 1);
  assert.equal(direct.list.result.counters[0].id, 123);
  assert.equal(Object.hasOwn(direct.list.result.counters[0], 'ignored'), false);
  assert.equal(direct.summary.ok, true);
  assert.equal(direct.summary.prefix, 'METRIKA_RESULT_V1');
  assert.deepEqual(direct.summary.result.metrics, { visits: 12, users: 8, pageviews: 30 });

  fetches = await workerEval(workerClient, 'globalThis.__YMB_M4_FETCHES');
  assert.equal(fetches.length, 3);
  assert.equal(fetches[1].url.includes('/management/v1/counters?offset=11&per_page=10'), true);
  assert.equal(fetches[2].url.includes('/stat/v1/data?'), true);
  assert.equal(fetches[2].url.includes('metrics=ym%3As%3Avisits%2Cym%3As%3Ausers%2Cym%3As%3Apageviews'), true);
  assert.equal(fetches.every((entry) => entry.method === 'GET'), true);
  assert.equal(fetches.every((entry) => entry.has_authorization && entry.auth_scheme_exact), true);
  console.log('M07_M09_CONTROLLED_WORKER_PROVIDER_BOUNDARY_PASS');

  const backupResponse = await send(page, { type: 'WS_EXPORT_BACKUP' });
  assert.equal(backupResponse.ok, true);
  const backup = backupResponse.backup;
  assert.equal(backup.backup_version, 3);
  assert.equal(backup.settings.credentials.wordstat.api_key, 'm4-wordstat-secret');
  assert.equal(backup.settings.credentials.wordstat.folder_id, 'm4-wordstat-folder');
  assert.equal(backup.settings.credentials.search.api_key, 'm4-search-secret');
  assert.equal(backup.settings.credentials.search.folder_id, 'm4-search-folder');
  assert.equal(backup.settings.credentials.webmaster.oauth_token, 'm4-webmaster-oauth');
  assert.equal(backup.settings.credentials.metrika.oauth_token, 'm4-metrika-oauth');
  assert.match(String(backup.integrity?.sha256 || ''), /^[a-f0-9]{64}$/);

  const mutate = await send(page, { type: 'YMB_SAVE_SERVICE_CREDENTIAL', service: 'metrika', credential: { oauth_token: 'm4-mutated-token' } });
  assert.equal(mutate.ok, true);
  const imported = await send(page, { type: 'WS_IMPORT_BACKUP', backup });
  assert.equal(imported.ok, true);
  const restored = await workerEval(workerClient, `(async () => {
    const c = await globalThis.YMBCredentialRuntime.load();
    return {
      wordstat: { api_key: c.wordstat.api_key, folder_id: c.wordstat.folder_id },
      search: { api_key: c.search.api_key, folder_id: c.search.folder_id },
      webmaster: { oauth_token: c.webmaster.oauth_token },
      metrika: { oauth_token: c.metrika.oauth_token, check_state: c.metrika.check_state }
    };
  })()`);
  assert.deepEqual(restored, {
    wordstat: { api_key: 'm4-wordstat-secret', folder_id: 'm4-wordstat-folder' },
    search: { api_key: 'm4-search-secret', folder_id: 'm4-search-folder' },
    webmaster: { oauth_token: 'm4-webmaster-oauth' },
    metrika: { oauth_token: 'm4-metrika-oauth', check_state: 'PRESENT' }
  });
  const publicAfterImport = await send(page, { type: 'YMB_GET_CREDENTIALS' });
  const publicAfterImportText = JSON.stringify(publicAfterImport);
  for (const secret of ['m4-wordstat-secret', 'm4-search-secret', 'm4-webmaster-oauth', 'm4-metrika-oauth', 'm4-mutated-token']) {
    assert.equal(publicAfterImportText.includes(secret), false);
  }
  console.log('M16_BACKUP_V3_FOUR_SERVICE_EXPORT_IMPORT_PASS');

  await page.reload({ waitUntil: 'load' });
  await page.waitForSelector('#credentialsSection', { timeout: 15000 });
  await page.waitForFunction(() => document.querySelector('#saveMetrikaCredential')?.disabled === false);
  const rerender = await page.evaluate(() => ({
    wordstat: document.querySelector('#wordstatApiKey')?.value || '',
    search: document.querySelector('#searchApiKey')?.value || '',
    webmaster: document.querySelector('#webmasterOauthToken')?.value || '',
    metrika: document.querySelector('#metrikaOauthToken')?.value || '',
    metrikaState: document.querySelector('#metrikaCredentialState')?.textContent || ''
  }));
  assert.deepEqual([rerender.wordstat, rerender.search, rerender.webmaster, rerender.metrika], ['', '', '', '']);
  assert.match(rerender.metrikaState, /проверено/i);
  for (const secret of ['m4-wordstat-secret', 'm4-search-secret', 'm4-webmaster-oauth', 'm4-metrika-oauth', 'm4-mutated-token']) {
    assert.equal(await page.evaluate((value) => document.body.innerText.includes(value), secret), false);
  }
  console.log('M15_REOPEN_RERENDER_SECRET_BLANK_PASS');

  fetches = await workerEval(workerClient, 'globalThis.__YMB_M4_FETCHES');
  assert.equal(fetches.length, 3);
  assert.equal(fetches.every((entry) => entry.url.startsWith('https://api-metrika.yandex.net/')), true);
  console.log('M19_CONTROLLED_REAL_YANDEX_REQUESTS=0');
  console.log('PHASE4_METRIKA_BROWSER_RUNTIME_PASS');
} finally {
  await browser.close();
  fs.rmSync(qa.tempRoot, { recursive: true, force: true });
}
