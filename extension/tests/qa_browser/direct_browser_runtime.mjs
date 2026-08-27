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
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'ymb-phase5-direct-browser-'));
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
    globalThis.__YMB_D5_FETCHES = [];
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
      globalThis.__YMB_D5_FETCHES.push({
        url: target,
        method,
        authorization: readHeader('Authorization'),
        client_login: readHeader('Client-Login'),
        processing_mode: readHeader('processingMode'),
        body: String(options.body || '')
      });
      if (!target.startsWith('https://api.direct.yandex.com/json/v501/')) throw new Error('CONTROLLED_BROWSER_UNEXPECTED_PROVIDER_HOST');
      const commonHeaders = { 'Content-Type': 'application/json', RequestId: 'browser-request', Units: '2/98/100' };
      if (target.endsWith('/campaigns')) {
        const body = JSON.parse(String(options.body || '{}'));
        if (body?.params?.FieldNames?.length === 1 && body.params.FieldNames[0] === 'Id' && body?.params?.Page?.Limit === 1) {
          return new Response(JSON.stringify({ result: { Campaigns: [] } }), { status: 200, headers: commonHeaders });
        }
        return new Response(JSON.stringify({ result: { Campaigns: [{ Id: 77, Name: 'Browser campaign', StartDate: '2026-08-01', Type: 'TEXT_CAMPAIGN', Status: 'ACCEPTED', State: 'ON', Currency: 'RUB', Private: 'drop' }], LimitedBy: 100 } }), { status: 200, headers: commonHeaders });
      }
      if (target.endsWith('/reports')) {
        return new Response('Date\\tCampaignId\\tCampaignName\\tImpressions\\tClicks\\tCost\\n2026-08-01\\t77\\tBrowser campaign\\t100\\t5\\t123456\\n', { status: 200, headers: { RequestId: 'browser-report', Units: '3/97/100' } });
      }
      throw new Error('CONTROLLED_BROWSER_UNEXPECTED_DIRECT_ROUTE');
    };
    return true;
  })()`);

  const page = await browser.newPage();
  await page.goto(`chrome-extension://${qa.extensionId}/popup.html`, { waitUntil: 'load' });
  await page.waitForSelector('#directCredentials', { timeout: 15000 });
  await page.waitForFunction(() => document.querySelector('#saveDirectCredential')?.disabled === false);

  const ui = await page.evaluate(() => ({
    services: [...document.querySelectorAll('#activeService option')].map((option) => option.value),
    tokenType: document.querySelector('#directOauthToken')?.type,
    topSave: document.querySelector('#saveSettingsTop')?.textContent,
    bottomSave: document.querySelector('#saveSettings')?.textContent,
    cost: document.querySelector('#directCost')?.value,
    maxRequests: document.querySelector('#directMaxRequestsRun')?.value,
    maxPage: document.querySelector('#directMaxPageSize')?.value,
    maxDays: document.querySelector('#directMaxReportDays')?.value,
    maxRows: document.querySelector('#directMaxReportRows')?.value,
    directText: document.querySelector('#directCredentials')?.textContent || ''
  }));
  assert.deepEqual(ui.services, ['wordstat', 'search', 'webmaster', 'metrika', 'direct']);
  assert.equal(ui.tokenType, 'password');
  assert.equal(ui.topSave, 'Сохранить общие настройки');
  assert.equal(ui.bottomSave, 'Сохранить общие настройки');
  assert.equal(ui.cost, '0 ₽');
  assert.equal(ui.maxRequests, '20');
  assert.equal(ui.maxPage, '1000');
  assert.equal(ui.maxDays, '31');
  assert.equal(ui.maxRows, '1000');
  assert.match(ui.directText, /Direct Units/);
  console.log('D15_POPUP_FIVE_SERVICE_UI_PASS');

  await page.$eval('#directCredentials', (node) => { node.open = true; });
  await page.$eval('#directOauthToken', (node) => { node.value = 'browser-direct-secret'; });
  await page.$eval('#directClientLogin', (node) => { node.value = 'browser-client-login'; });
  await page.click('#saveDirectCredential');
  await page.waitForFunction(() => document.querySelector('#saveDirectCredential')?.disabled === false);
  assert.equal(await page.$eval('#directOauthToken', (node) => node.value), '');
  assert.equal(await page.$eval('#directClientLogin', (node) => node.value), 'browser-client-login');

  const publicSaved = await send(page, { type: 'YMB_GET_CREDENTIALS' });
  assert.equal(publicSaved.ok, true);
  assert.equal(publicSaved.credentials.direct.has_oauth_token, true);
  assert.equal(publicSaved.credentials.direct.client_login, 'browser-client-login');
  assert.equal(JSON.stringify(publicSaved).includes('browser-direct-secret'), false);
  assert.equal(await page.evaluate(() => document.body.innerText.includes('browser-direct-secret')), false);
  console.log('D05_D15_DIRECT_SECRET_RERENDER_REDACTION_PASS');

  await page.click('#checkDirectCredential');
  await page.waitForFunction(() => /проверено/i.test(document.querySelector('#directCredentialState')?.textContent || '') && document.querySelector('#checkDirectCredential')?.disabled === false);
  let fetches = await workerEval(workerClient, 'globalThis.__YMB_D5_FETCHES');
  assert.equal(fetches.length, 1);
  assert.equal(fetches[0].url, 'https://api.direct.yandex.com/json/v501/campaigns');
  assert.equal(fetches[0].method, 'POST');
  assert.equal(fetches[0].authorization, 'Bearer browser-direct-secret');
  assert.equal(fetches[0].client_login, 'browser-client-login');
  assert.deepEqual(JSON.parse(fetches[0].body), {
    method: 'get',
    params: { SelectionCriteria: {}, FieldNames: ['Id'], Page: { Limit: 1, Offset: 0 } }
  });
  assert.equal(await page.$eval('#directOauthToken', (node) => node.value), '');
  console.log('D03_D15_DIRECT_CHECK_ONE_POST_PASS');

  const provider = await workerEval(workerClient, `(async () => {
    const list = await globalThis.YMBPhase5ProviderRuntime.executeDirect({ method: 'listCampaigns', campaignIds: [77], limit: 10 });
    const report = await globalThis.YMBPhase5ProviderRuntime.executeDirect({ method: 'getCampaignPerformance', dateFrom: '2026-08-01', dateTo: '2026-08-01', campaignIds: [77], limit: 10 });
    return {
      list: { ok: list.ok, status: list.http_status, result: list.report_envelope?.result, requestId: list.report_envelope?.provider_request_id, units: list.report_envelope?.provider_units, text: list.report_text },
      report: { ok: report.ok, status: report.http_status, result: report.report_envelope?.result, requestId: report.report_envelope?.provider_request_id, units: report.report_envelope?.provider_units, text: report.report_text }
    };
  })()`);
  assert.equal(provider.list.ok, true);
  assert.equal(provider.list.status, 200);
  assert.equal(provider.list.result.campaigns[0].id, 77);
  assert.equal(Object.hasOwn(provider.list.result.campaigns[0], 'Private'), false);
  assert.equal(provider.list.requestId, 'browser-request');
  assert.deepEqual(provider.list.units, { spent: 2, remaining: 98, daily_limit: 100 });
  assert.equal(provider.list.text.includes('browser-direct-secret'), false);
  assert.equal(provider.list.text.includes('browser-client-login'), false);
  assert.equal(provider.report.ok, true);
  assert.equal(provider.report.result.row_count, 1);
  assert.equal(provider.report.result.rows[0].cost_micros, 123456);
  assert.equal(provider.report.requestId, 'browser-report');
  assert.deepEqual(provider.report.units, { spent: 3, remaining: 97, daily_limit: 100 });
  assert.equal(provider.report.text.includes('browser-direct-secret'), false);
  assert.equal(provider.report.text.includes('browser-client-login'), false);

  fetches = await workerEval(workerClient, 'globalThis.__YMB_D5_FETCHES');
  assert.equal(fetches.length, 3);
  assert.equal(fetches[1].url.endsWith('/campaigns'), true);
  const listBody = JSON.parse(fetches[1].body);
  assert.deepEqual(listBody.params.SelectionCriteria, { Ids: [77] });
  assert.equal(fetches[2].url.endsWith('/reports'), true);
  assert.equal(fetches[2].processing_mode, 'online');
  assert.equal(fetches.every((entry) => entry.authorization === 'Bearer browser-direct-secret'), true);
  assert.equal(fetches.every((entry) => entry.client_login === 'browser-client-login'), true);
  console.log('D04_D06_CONTROLLED_DIRECT_PROVIDER_BOUNDARY_PASS');

  const backupResponse = await send(page, { type: 'WS_EXPORT_BACKUP' });
  assert.equal(backupResponse.ok, true);
  const backup = backupResponse.backup;
  assert.equal(backup.backup_version, 3);
  assert.equal(backup.settings_schema_version, 5);
  assert.equal(backup.settings.credentials.direct.oauth_token, 'browser-direct-secret');
  assert.equal(backup.settings.credentials.direct.client_login, 'browser-client-login');
  assert.match(String(backup.settings_sha256 || ''), /^[a-f0-9]{64}$/);

  const mutate = await send(page, { type: 'YMB_SAVE_SERVICE_CREDENTIAL', service: 'direct', credential: { oauth_token: 'browser-mutated-secret', client_login: 'mutated-client' } });
  assert.equal(mutate.ok, true);
  const imported = await send(page, { type: 'WS_IMPORT_BACKUP', backup });
  assert.equal(imported.ok, true);
  const restored = await workerEval(workerClient, `(async () => {
    const c = await globalThis.YMBCredentialRuntime.load();
    return { token: c.direct.oauth_token, client: c.direct.client_login, state: c.direct.check_state };
  })()`);
  assert.deepEqual(restored, { token: 'browser-direct-secret', client: 'browser-client-login', state: 'PRESENT' });
  const publicAfterImport = await send(page, { type: 'YMB_GET_CREDENTIALS' });
  for (const secret of ['browser-direct-secret', 'browser-mutated-secret']) assert.equal(JSON.stringify(publicAfterImport).includes(secret), false);
  console.log('D14_BACKUP_V3_DIRECT_EXPORT_IMPORT_PASS');

  await page.reload({ waitUntil: 'load' });
  await page.waitForSelector('#directCredentials', { timeout: 15000 });
  await page.waitForFunction(() => document.querySelector('#saveDirectCredential')?.disabled === false);
  assert.equal(await page.$eval('#directOauthToken', (node) => node.value), '');
  assert.equal(await page.$eval('#directClientLogin', (node) => node.value), 'browser-client-login');
  assert.equal(await page.evaluate(() => document.body.innerText.includes('browser-direct-secret')), false);
  console.log('D15_POPUP_REOPEN_SECRET_BLANK_PASS');

  fetches = await workerEval(workerClient, 'globalThis.__YMB_D5_FETCHES');
  assert.equal(fetches.length, 3);
  assert.equal(fetches.every((entry) => entry.url.startsWith('https://api.direct.yandex.com/json/v501/')), true);
  console.log('D20_CONTROLLED_REAL_YANDEX_REQUESTS=0');
  console.log('PHASE5_DIRECT_BROWSER_RUNTIME_PASS');
} finally {
  await browser.close();
  fs.rmSync(qa.tempRoot, { recursive: true, force: true });
}
