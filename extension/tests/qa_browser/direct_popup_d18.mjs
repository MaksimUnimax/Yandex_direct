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
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'ymb-phase5-d18-'));
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

async function send(page, message) {
  return page.evaluate((payload) => new Promise((resolve, reject) => {
    chrome.runtime.sendMessage(payload, (response) => {
      const error = chrome.runtime.lastError;
      if (error) reject(new Error(error.message || String(error)));
      else resolve(response);
    });
  }), message);
}

async function waitCommonSave(page, selector) {
  await page.$eval(selector, (node) => node.click());
  await page.waitForFunction((sel) => {
    const button = document.querySelector(sel);
    const status = document.querySelector('#status');
    return button?.disabled === false && status?.textContent === 'Общие настройки сохранены.' && status?.dataset?.level === 'ok';
  }, { timeout: 10000 }, selector);
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
  await browser.waitForTarget(
    (target) => target.type() === 'service_worker' && target.url().startsWith(`chrome-extension://${qa.extensionId}/`),
    { timeout: 15000 }
  );
  const page = await browser.newPage();
  await page.goto(`chrome-extension://${qa.extensionId}/popup.html`, { waitUntil: 'load' });
  await page.waitForSelector('#saveSettingsTop', { timeout: 15000 });
  await page.waitForFunction(() => document.querySelector('#saveSettingsTop')?.disabled === false && document.querySelector('#saveSettings')?.disabled === false);

  const geometry = await page.evaluate(() => {
    const html = document.documentElement.getBoundingClientRect();
    const body = document.body.getBoundingClientRect();
    const main = document.querySelector('main');
    return {
      htmlWidth: Math.round(html.width), htmlHeight: Math.round(html.height),
      bodyWidth: Math.round(body.width), bodyHeight: Math.round(body.height),
      mainClientWidth: main?.clientWidth || 0, mainScrollWidth: main?.scrollWidth || 0,
      mainClientHeight: main?.clientHeight || 0, mainScrollHeight: main?.scrollHeight || 0,
      topText: document.querySelector('#saveSettingsTop')?.textContent || '',
      bottomText: document.querySelector('#saveSettings')?.textContent || ''
    };
  });
  assert.deepEqual([geometry.htmlWidth, geometry.htmlHeight, geometry.bodyWidth, geometry.bodyHeight], [430, 560, 430, 560]);
  assert.ok(geometry.mainScrollWidth <= geometry.mainClientWidth, `horizontal overflow ${JSON.stringify(geometry)}`);
  assert.ok(geometry.mainScrollHeight > geometry.mainClientHeight, `vertical scroll missing ${JSON.stringify(geometry)}`);
  assert.equal(geometry.topText, 'Сохранить общие настройки');
  assert.equal(geometry.bottomText, 'Сохранить общие настройки');
  console.log('D18_POPUP_430X560_PASS');

  await page.$eval('#directManualEnabled', (node) => { node.checked = false; });
  await waitCommonSave(page, '#saveSettingsTop');
  let policy = await send(page, { type: 'YMB_GET_DIRECT_POLICY' });
  assert.equal(policy?.ok, true);
  assert.equal(policy.policy.manual_enabled, false);
  assert.equal(policy.policy.autorun_enabled, false);

  await page.$eval('#directManualEnabled', (node) => { node.checked = true; });
  await waitCommonSave(page, '#saveSettings');
  policy = await send(page, { type: 'YMB_GET_DIRECT_POLICY' });
  assert.equal(policy?.ok, true);
  assert.equal(policy.policy.manual_enabled, true);
  assert.equal(policy.policy.autorun_enabled, false);
  console.log('D18_TOP_BOTTOM_COMMON_SAVE_EQUIVALENT_PASS');
  console.log('PHASE5_DIRECT_POPUP_D18_PASS');
} finally {
  await browser.close();
  fs.rmSync(qa.tempRoot, { recursive: true, force: true });
}
