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
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'ymb-phase5-direct-click-diagnostic-'));
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
const browser = await puppeteer.launch({
  headless: false,
  pipe: true,
  enableExtensions: true,
  args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage', `--disable-extensions-except=${qa.extensionPath}`, `--load-extension=${qa.extensionPath}`]
});

try {
  const workerTarget = await browser.waitForTarget(
    (target) => target.type() === 'service_worker' && target.url().startsWith(`chrome-extension://${qa.extensionId}/`),
    { timeout: 15000 }
  );
  const workerClient = await workerTarget.createCDPSession();
  await workerEval(workerClient, `(() => {
    globalThis.__YMB_D5_CLICK_FETCHES = [];
    globalThis.fetch = async (url, options = {}) => {
      const target = String(url || '');
      globalThis.__YMB_D5_CLICK_FETCHES.push({ target, method: String(options.method || 'GET').toUpperCase(), body: String(options.body || '') });
      if (target !== 'https://api.direct.yandex.com/json/v501/campaigns') throw new Error('CLICK_DIAG_UNEXPECTED_ROUTE');
      return new Response(JSON.stringify({ result: { Campaigns: [] } }), {
        status: 200,
        headers: { 'Content-Type': 'application/json', RequestId: 'click-diag', Units: '1/99/100' }
      });
    };
    return true;
  })()`);

  const page = await browser.newPage();
  await page.goto(`chrome-extension://${qa.extensionId}/popup.html`, { waitUntil: 'load' });
  await page.waitForSelector('#directCredentials', { timeout: 15000 });
  await page.waitForFunction(() => document.querySelector('#saveDirectCredential')?.disabled === false);
  await page.$eval('#directCredentials', (node) => { node.open = true; });
  await page.$eval('#directOauthToken', (node) => { node.value = 'click-diagnostic-secret'; });
  await page.$eval('#directClientLogin', (node) => { node.value = 'click-diagnostic-client'; });
  await page.click('#saveDirectCredential');
  await page.waitForFunction(() => document.querySelector('#saveDirectCredential')?.disabled === false);

  const publicSaved = await send(page, { type: 'YMB_GET_CREDENTIALS' });
  assert.equal(publicSaved?.credentials?.direct?.has_oauth_token, true);

  const afterSave = await page.evaluate(() => {
    const details = document.querySelector('#directCredentials');
    const button = document.querySelector('#checkDirectCredential');
    const rect = button?.getBoundingClientRect();
    return {
      activeService: document.querySelector('#activeService')?.value || '',
      detailsOpen: details?.open === true,
      buttonDisabled: button?.disabled === true,
      buttonRect: rect ? { width: rect.width, height: rect.height, x: rect.x, y: rect.y } : null,
      state: document.querySelector('#directCredentialState')?.textContent || ''
    };
  });

  await page.evaluate(() => document.querySelector('#checkDirectCredential')?.click());
  await page.waitForFunction(() => /проверено/i.test(document.querySelector('#directCredentialState')?.textContent || ''), { timeout: 5000 });

  const afterDomClick = await page.evaluate(() => ({
    state: document.querySelector('#directCredentialState')?.textContent || '',
    status: document.querySelector('#status')?.textContent || '',
    detailsOpen: document.querySelector('#directCredentials')?.open === true,
    buttonDisabled: document.querySelector('#checkDirectCredential')?.disabled === true
  }));
  const fetches = await workerEval(workerClient, 'globalThis.__YMB_D5_CLICK_FETCHES || []');
  const safe = { afterSave, afterDomClick, fetches };
  const serialized = JSON.stringify(safe);
  assert.equal(serialized.includes('click-diagnostic-secret'), false);
  assert.equal(fetches.length, 1);
  console.log(`DIRECT_CHECK_CLICK_DIAGNOSTIC=${serialized}`);
  console.log('PHASE5_DIRECT_CHECK_CLICK_DIAGNOSTIC_PASS');
} finally {
  await browser.close();
  fs.rmSync(qa.tempRoot, { recursive: true, force: true });
}
