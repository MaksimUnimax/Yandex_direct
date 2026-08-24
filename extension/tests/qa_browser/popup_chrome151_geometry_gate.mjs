import fs from 'node:fs';
import https from 'node:https';
import os from 'node:os';
import path from 'node:path';
import process from 'node:process';
import puppeteer from 'puppeteer-core';

const [chromePath, extensionRoot, keyPath, certPath, expectedMode = 'fixed'] = process.argv.slice(2);
if (!chromePath || !extensionRoot || !keyPath || !certPath) {
  throw new Error('usage: popup_chrome151_geometry_gate.mjs <chrome> <extension-root> <tls-key> <tls-cert> [fixed|baseline]');
}
for (const p of [chromePath, extensionRoot, keyPath, certPath]) {
  if (!fs.existsSync(p)) throw new Error(`INPUT_MISSING ${p}`);
}

const CID = '11111111-2222-4333-8444-555555555555';
const CHAT_URL = `https://chatgpt.com/c/${CID}`;
const fixtureHtml = `<!doctype html><html><head><meta charset="utf-8"><title>Popup geometry fixture</title></head><body>
<main><div data-message-author-role="assistant" data-message-id="fixture-assistant"><pre data-testid="code-block"><code>fixture</code></pre></div></main>
<textarea id="prompt-textarea"></textarea><button id="composer-submit-button" data-testid="send-button" type="button">Send</button>
</body></html>`;

const server = https.createServer({ key: fs.readFileSync(keyPath), cert: fs.readFileSync(certPath) }, (_req, res) => {
  res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
  res.end(fixtureHtml);
});
await new Promise((resolve, reject) => { server.once('error', reject); server.listen(8443, '127.0.0.1', resolve); });

function assert(value, message) { if (!value) throw new Error(message); }
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

let browser;
try {
  browser = await puppeteer.launch({
    executablePath: chromePath,
    headless: false,
    protocolTimeout: 30000,
    userDataDir: fs.mkdtempSync(path.join(os.tmpdir(), 'ymb-popup-geometry-')),
    args: [
      '--no-sandbox', '--disable-gpu', '--no-proxy-server', '--ignore-certificate-errors', '--disable-background-networking', '--disable-features=DnsOverHttps',
      `--disable-extensions-except=${extensionRoot}`, `--load-extension=${extensionRoot}`,
      '--host-resolver-rules=MAP chatgpt.com 127.0.0.1:8443, EXCLUDE localhost'
    ]
  });

  const pages = await browser.pages();
  const fixture = pages[0] || await browser.newPage();
  await fixture.goto(CHAT_URL, { waitUntil: 'domcontentloaded', timeout: 20000 });
  const swTarget = await browser.waitForTarget(t => t.type() === 'service_worker' && t.url().startsWith('chrome-extension://'), { timeout: 15000 });
  const worker = await swTarget.worker();
  assert(worker, 'MV3_WORKER_CONTEXT_FAIL');

  const before = new Set(browser.targets());
  const openResult = await worker.evaluate(async () => {
    try {
      await chrome.action.openPopup();
      return { ok: true };
    } catch (error) {
      return { ok: false, error: error?.message || String(error) };
    }
  });
  assert(openResult?.ok, `ACTION_OPEN_POPUP_FAIL ${JSON.stringify(openResult)}`);

  const popupTarget = await browser.waitForTarget(
    t => !before.has(t) && t.url().startsWith('chrome-extension://') && t.url().endsWith('/popup.html'),
    { timeout: 10000 }
  );
  const popup = await popupTarget.page();
  assert(popup, 'ACTION_POPUP_PAGE_FAIL');
  await popup.waitForSelector('main', { timeout: 10000 });
  await delay(700);

  const geometry = await popup.evaluate(() => {
    const html = document.documentElement;
    const body = document.body;
    const main = document.querySelector('main');
    const rect = main?.getBoundingClientRect();
    return {
      innerWidth: window.innerWidth,
      innerHeight: window.innerHeight,
      htmlClientWidth: html.clientWidth,
      htmlClientHeight: html.clientHeight,
      htmlScrollWidth: html.scrollWidth,
      htmlScrollHeight: html.scrollHeight,
      bodyClientWidth: body.clientWidth,
      bodyClientHeight: body.clientHeight,
      bodyScrollWidth: body.scrollWidth,
      bodyScrollHeight: body.scrollHeight,
      mainClientWidth: main?.clientWidth || 0,
      mainClientHeight: main?.clientHeight || 0,
      mainScrollWidth: main?.scrollWidth || 0,
      mainScrollHeight: main?.scrollHeight || 0,
      mainRectWidth: rect?.width || 0,
      mainRectHeight: rect?.height || 0,
      mainOverflowY: main ? getComputedStyle(main).overflowY : '',
      rootOverflow: getComputedStyle(html).overflow,
      bodyOverflow: getComputedStyle(body).overflow
    };
  });

  console.log(`POPUP_GEOMETRY=${JSON.stringify(geometry)}`);
  const isWideRegression = geometry.innerWidth >= 760 || geometry.htmlClientWidth >= 760;
  if (expectedMode === 'baseline') {
    assert(isWideRegression, `BASELINE_CHROME151_REGRESSION_NOT_REPRODUCED ${JSON.stringify(geometry)}`);
    console.log('POPUP_CHROME151_BASELINE_REGRESSION_REPRODUCED');
  } else {
    assert(!isWideRegression, `POPUP_CHROME151_WIDTH_REGRESSION_PRESENT ${JSON.stringify(geometry)}`);
    assert(geometry.innerWidth >= 420 && geometry.innerWidth <= 460, `POPUP_FIXED_WIDTH_OUT_OF_RANGE ${JSON.stringify(geometry)}`);
    assert(geometry.innerHeight <= 600, `POPUP_FIXED_HEIGHT_OVER_LIMIT ${JSON.stringify(geometry)}`);
    assert(geometry.mainClientHeight <= 560, `POPUP_MAIN_HEIGHT_OUT_OF_RANGE ${JSON.stringify(geometry)}`);
    assert(geometry.mainScrollHeight > geometry.mainClientHeight, `POPUP_INTERNAL_SCROLL_NOT_ACTIVE ${JSON.stringify(geometry)}`);
    assert(geometry.mainOverflowY === 'auto', `POPUP_MAIN_OVERFLOW_NOT_AUTO ${JSON.stringify(geometry)}`);
    console.log('POPUP_CHROME151_ACTION_GEOMETRY_PASS');
  }
} finally {
  try { await browser?.close(); } catch {}
  await new Promise(resolve => server.close(resolve));
}
