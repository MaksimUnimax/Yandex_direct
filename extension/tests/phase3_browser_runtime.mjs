import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createHash, generateKeyPairSync } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer';

const here = path.dirname(fileURLToPath(import.meta.url));
const sourceExtensionPath = fs.realpathSync(path.resolve(here, '../src'));

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
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'ymb-phase3-browser-'));
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

  return {
    tempRoot,
    extensionPath,
    extensionId: extensionIdFromPublicKey(Buffer.from(publicKey))
  };
}

const qa = prepareQaExtension();
assert.match(qa.extensionId, /^[a-p]{32}$/);

// Use Puppeteer's bundled Chrome for Testing. This avoids branded Chrome's
// extension-loading restrictions and keeps the browser version paired with
// the Puppeteer version used by this QA harness.
const browser = await puppeteer.launch({
  headless: false,
  pipe: true,
  enableExtensions: [qa.extensionPath],
  args: [
    '--no-sandbox',
    '--disable-gpu',
    '--disable-dev-shm-usage'
  ]
});

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

try {
  const extensions = await browser.extensions();
  const installed = extensions.get(qa.extensionId);
  assert.ok(installed, `QA extension ${qa.extensionId} was not installed by Puppeteer`);
  assert.equal(installed.name, 'Yandex Marketing Bridge');

  const page = await browser.newPage();
  await page.goto(`chrome-extension://${qa.extensionId}/popup.html`, { waitUntil: 'load' });
  await page.waitForSelector('#credentialsSection', { timeout: 15000 });

  const workerTarget = await browser.waitForTarget(
    (target) => target.type() === 'service_worker' && target.url().startsWith(`chrome-extension://${qa.extensionId}/`),
    { timeout: 15000 }
  );
  assert.equal(new URL(workerTarget.url()).host, qa.extensionId);
  const workerClient = await workerTarget.createCDPSession();

  // Hard provider fence for this browser gate. Every product provider request is
  // captured here and answered locally; no real Yandex request can leave Chrome.
  await workerEval(workerClient, `(() => {
    globalThis.__YMB_BROWSER_MODE = 'ok';
    globalThis.__YMB_BROWSER_FETCHES = [];
    globalThis.fetch = async (url, options = {}) => {
      const target = String(url || '');
      const headers = options.headers || {};
      let hasAuthorization = false;
      try {
        hasAuthorization = headers instanceof Headers
          ? headers.has('Authorization')
          : Object.keys(headers).some((key) => String(key).toLowerCase() === 'authorization');
      } catch {}
      globalThis.__YMB_BROWSER_FETCHES.push({
        url: target,
        method: String(options.method || 'GET').toUpperCase(),
        has_authorization: hasAuthorization
      });
      const json = (value, status = 200) => new Response(JSON.stringify(value), {
        status,
        headers: { 'Content-Type': 'application/json' }
      });
      if (target.endsWith('/v4/user')) {
        if (globalThis.__YMB_BROWSER_MODE === 'webmaster401') return json({ code: 'UNAUTHORIZED', message: 'invalid token' }, 401);
        return json({ user_id: 321 }, 200);
      }
      if (target.includes('/v2/wordstat/getRegionsTree')) return json({ regions: [] }, 200);
      if (target.includes('/v4/user/321/hosts')) return json({ hosts: [] }, 200);
      return json({}, 200);
    };
    return true;
  })()`);

  await page.waitForFunction(() => document.querySelector('#versionBadge')?.textContent?.startsWith('v'));

  const geometry = await page.evaluate(() => ({
    htmlWidth: document.documentElement.getBoundingClientRect().width,
    htmlHeight: document.documentElement.getBoundingClientRect().height,
    bodyWidth: document.body.getBoundingClientRect().width,
    bodyHeight: document.body.getBoundingClientRect().height
  }));
  assert.equal(geometry.htmlWidth, 430);
  assert.equal(geometry.htmlHeight, 560);
  assert.equal(geometry.bodyWidth, 430);
  assert.equal(geometry.bodyHeight, 560);

  const ui = await page.evaluate(() => ({
    services: [...document.querySelectorAll('#activeService option')].map((option) => option.value),
    wordstatType: document.querySelector('#wordstatApiKey')?.type,
    searchType: document.querySelector('#searchApiKey')?.type,
    webmasterType: document.querySelector('#webmasterOauthToken')?.type,
    webmasterCost: document.querySelector('#webmasterCost')?.value
  }));
  assert.deepEqual(ui.services, ['wordstat', 'search', 'webmaster']);
  assert.equal(ui.wordstatType, 'password');
  assert.equal(ui.searchType, 'password');
  assert.equal(ui.webmasterType, 'password');
  assert.equal(ui.webmasterCost, '0 ₽');

  await page.$eval('#wordstatApiKey', (node) => { node.value = 'browser-word-secret'; });
  await page.$eval('#wordstatFolderId', (node) => { node.value = 'browser-word-folder'; });
  await page.click('#saveWordstatCredential');
  await page.waitForFunction(() => document.querySelector('#wordstatApiKey')?.value === '');
  await page.click('#checkWordstatCredential');
  await page.waitForFunction(() => /проверено/i.test(document.querySelector('#wordstatCredentialState')?.textContent || ''));

  await page.$eval('#searchApiKey', (node) => { node.value = 'browser-search-secret'; });
  await page.$eval('#searchFolderId', (node) => { node.value = 'browser-search-folder'; });
  await page.click('#saveSearchCredential');
  await page.waitForFunction(() => document.querySelector('#searchApiKey')?.value === '');

  await page.$eval('#webmasterOauthToken', (node) => { node.value = 'browser-invalid-oauth'; });
  await page.click('#saveWebmasterCredential');
  await page.waitForFunction(() => document.querySelector('#webmasterOauthToken')?.value === '');
  await workerEval(workerClient, `globalThis.__YMB_BROWSER_MODE = 'webmaster401'`);
  await page.click('#checkWebmasterCredential');
  await page.waitForFunction(() => /неверный|истёк/i.test(document.querySelector('#webmasterCredentialState')?.textContent || ''));
  const invalidLeak = await page.evaluate(() => ({
    text: document.body.innerText.includes('browser-invalid-oauth'),
    input: document.querySelector('#webmasterOauthToken')?.value || ''
  }));
  assert.equal(invalidLeak.text, false);
  assert.equal(invalidLeak.input, '');

  await page.$eval('#webmasterOauthToken', (node) => { node.value = 'browser-valid-oauth'; });
  await page.click('#saveWebmasterCredential');
  await page.waitForFunction(() => document.querySelector('#webmasterOauthToken')?.value === '');
  await workerEval(workerClient, `globalThis.__YMB_BROWSER_MODE = 'ok'`);
  await page.click('#checkWebmasterCredential');
  await page.waitForFunction(() => document.querySelector('#webmasterUserId')?.textContent === '321');
  assert.equal(await page.$eval('#webmasterOauthToken', (node) => node.value), '');
  assert.equal(await page.evaluate(() => document.body.innerText.includes('browser-valid-oauth')), false);

  const publicCredentials = await send(page, { type: 'YMB_GET_CREDENTIALS' });
  assert.equal(publicCredentials.ok, true);
  assert.equal(publicCredentials.credentials.webmaster.user_id, '321');
  assert.equal(JSON.stringify(publicCredentials).includes('browser-valid-oauth'), false);
  assert.equal(JSON.stringify(publicCredentials).includes('browser-word-secret'), false);
  assert.equal(JSON.stringify(publicCredentials).includes('browser-search-secret'), false);

  const listHosts = await workerEval(workerClient, `(async () => {
    const result = await globalThis.YMBPhase3Runtime.executeWebmasterCommand({ method: 'listHosts' });
    return { ok: result.ok, http_status: result.http_status, report_prefix: String(result.report_text || '').split('\\n')[0] };
  })()`);
  assert.deepEqual(listHosts, { ok: true, http_status: 200, report_prefix: 'WEBMASTER_RESULT_V1' });

  const backupResponse = await send(page, { type: 'WS_EXPORT_BACKUP' });
  assert.equal(backupResponse.ok, true);
  const backup = backupResponse.backup;
  assert.equal(backup.backup_version, 3);
  assert.equal(backup.settings.credentials.wordstat.api_key, 'browser-word-secret');
  assert.equal(backup.settings.credentials.wordstat.folder_id, 'browser-word-folder');
  assert.equal(backup.settings.credentials.search.api_key, 'browser-search-secret');
  assert.equal(backup.settings.credentials.search.folder_id, 'browser-search-folder');
  assert.equal(backup.settings.credentials.webmaster.oauth_token, 'browser-valid-oauth');
  assert.equal(backup.settings.credentials.webmaster.user_id, '321');

  const mutate = await send(page, {
    type: 'YMB_SAVE_SERVICE_CREDENTIAL',
    service: 'search',
    credential: { api_key: 'mutated-search-secret', folder_id: 'mutated-folder' }
  });
  assert.equal(mutate.ok, true);
  const importResponse = await send(page, { type: 'WS_IMPORT_BACKUP', backup });
  assert.equal(importResponse.ok, true);
  const restored = await workerEval(workerClient, `(async () => {
    const c = await globalThis.YMBPhase3Runtime.loadCredentials();
    return {
      wordstat: { api_key: c.wordstat.api_key, folder_id: c.wordstat.folder_id },
      search: { api_key: c.search.api_key, folder_id: c.search.folder_id },
      webmaster: { oauth_token: c.webmaster.oauth_token, user_id: c.webmaster.user_id }
    };
  })()`);
  assert.deepEqual(restored, {
    wordstat: { api_key: 'browser-word-secret', folder_id: 'browser-word-folder' },
    search: { api_key: 'browser-search-secret', folder_id: 'browser-search-folder' },
    webmaster: { oauth_token: 'browser-valid-oauth', user_id: '321' }
  });

  const fetches = await workerEval(workerClient, `globalThis.__YMB_BROWSER_FETCHES`);
  assert.equal(fetches.length, 4);
  assert.deepEqual(fetches.map((entry) => entry.method), ['POST', 'GET', 'GET', 'GET']);
  assert.equal(fetches[0].url.includes('/v2/wordstat/getRegionsTree'), true);
  assert.equal(fetches[1].url.endsWith('/v4/user'), true);
  assert.equal(fetches[2].url.endsWith('/v4/user'), true);
  assert.equal(fetches[3].url.includes('/v4/user/321/hosts'), true);
  assert.equal(fetches.every((entry) => entry.has_authorization === true), true);

  console.log('PHASE3_BROWSER_RUNTIME_PASS');
} finally {
  await browser.close();
  fs.rmSync(qa.tempRoot, { recursive: true, force: true });
}
