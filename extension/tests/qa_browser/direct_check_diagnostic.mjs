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
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'ymb-phase5-direct-check-diagnostic-'));
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

  const mock = `(() => {
    globalThis.__YMB_D5_DIAG_FETCHES = [];
    globalThis.fetch = async (url, options = {}) => {
      const target = String(url || '');
      const method = String(options.method || 'GET').toUpperCase();
      globalThis.__YMB_D5_DIAG_FETCHES.push({ target, method, body: String(options.body || '') });
      if (target !== 'https://api.direct.yandex.com/json/v501/campaigns') throw new Error('DIAG_UNEXPECTED_PROVIDER_ROUTE');
      return new Response(JSON.stringify({ result: { Campaigns: [] } }), {
        status: 200,
        headers: { 'Content-Type': 'application/json', RequestId: 'diag-request', Units: '1/99/100' }
      });
    };
  })();\n`;
  fs.writeFileSync(path.join(extensionPath, 'qa_direct_fetch_mock.js'), mock, 'utf8');
  const bootstrapPath = path.join(extensionPath, 'phase3_service_worker_bootstrap.js');
  const bootstrap = fs.readFileSync(bootstrapPath, 'utf8');
  fs.writeFileSync(bootstrapPath, `importScripts(\"qa_direct_fetch_mock.js\");\n${bootstrap}`, 'utf8');

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
  const page = await browser.newPage();
  await page.goto(`chrome-extension://${qa.extensionId}/popup.html`, { waitUntil: 'load' });
  await page.waitForSelector('#directCredentials', { timeout: 15000 });
  await page.waitForFunction(() => document.querySelector('#saveDirectCredential')?.disabled === false);

  await page.$eval('#directCredentials', (node) => { node.open = true; });
  await page.$eval('#directOauthToken', (node) => { node.value = 'diagnostic-secret'; });
  await page.$eval('#directClientLogin', (node) => { node.value = 'diagnostic-client'; });
  await page.click('#saveDirectCredential');
  await page.waitForFunction(() => document.querySelector('#saveDirectCredential')?.disabled === false);

  const before = await page.evaluate(() => ({
    state: document.querySelector('#directCredentialState')?.textContent || '',
    meta: document.querySelector('#directCheckMeta')?.textContent || '',
    status: document.querySelector('#status')?.textContent || '',
    checkDisabled: document.querySelector('#checkDirectCredential')?.disabled === true
  }));

  await page.click('#checkDirectCredential');
  await new Promise((resolve) => setTimeout(resolve, 1500));

  const after = await page.evaluate(() => ({
    state: document.querySelector('#directCredentialState')?.textContent || '',
    meta: document.querySelector('#directCheckMeta')?.textContent || '',
    status: document.querySelector('#status')?.textContent || '',
    statusLevel: document.querySelector('#status')?.dataset?.level || '',
    checkDisabled: document.querySelector('#checkDirectCredential')?.disabled === true,
    tokenFieldBlank: (document.querySelector('#directOauthToken')?.value || '') === '',
    clientLogin: document.querySelector('#directClientLogin')?.value || ''
  }));

  const publicStatus = await send(page, { type: 'YMB_GET_CREDENTIALS' });
  const fetches = await workerEval(workerClient, 'globalThis.__YMB_D5_DIAG_FETCHES || []');
  const stored = await workerEval(workerClient, `(async () => {
    const status = await globalThis.YMBCredentialRuntime.status();
    return status.direct;
  })()`);

  const safe = {
    before,
    after,
    publicDirect: publicStatus?.credentials?.direct || null,
    stored,
    fetches: fetches.map((entry) => ({ target: entry.target, method: entry.method, body: entry.body }))
  };
  const serialized = JSON.stringify(safe);
  assert.equal(serialized.includes('diagnostic-secret'), false);
  console.log(`DIRECT_CHECK_DIAGNOSTIC=${serialized}`);
  console.log('PHASE5_DIRECT_CHECK_DIAGNOSTIC_COMPLETE');
} finally {
  await browser.close();
  fs.rmSync(qa.tempRoot, { recursive: true, force: true });
}
