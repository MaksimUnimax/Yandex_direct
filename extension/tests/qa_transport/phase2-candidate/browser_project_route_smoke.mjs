import fs from 'node:fs';
import https from 'node:https';
import process from 'node:process';
import puppeteer from 'puppeteer-core';

const [chromePath, extensionRoot, keyPath, certPath] = process.argv.slice(2);
if (!chromePath || !extensionRoot || !keyPath || !certPath) {
  throw new Error('usage: browser_project_route_smoke.mjs <chrome> <extension-root> <key> <cert>');
}

const CID = '99999999-8888-4777-8666-555555555555';
const URL = `https://chatgpt.com/g/g-p-example-project/project-name/c/${CID}`;
const KEY = `https://chatgpt.com|${CID}`;
const serverHits = [];

const html = `<!doctype html><html><body>
<main>
<h1>Controlled ChatGPT Project route fixture</h1>
<div data-message-author-role="assistant"><pre>controlled fixture only</pre></div>
<textarea id="prompt-textarea"></textarea>
<button data-testid="send-button" type="button">Send</button>
</main>
</body></html>`;

const server = https.createServer({
  key: fs.readFileSync(keyPath),
  cert: fs.readFileSync(certPath)
}, (req, res) => {
  serverHits.push({ host: String(req.headers.host || ''), url: String(req.url || ''), method: req.method });
  res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
  res.end(html);
});

await new Promise((resolve, reject) => {
  server.once('error', reject);
  server.listen(8443, '127.0.0.1', resolve);
});

let browser;
try {
  browser = await puppeteer.launch({
    executablePath: chromePath,
    headless: false,
    userDataDir: fs.mkdtempSync('/tmp/ymb-cft-profile-'),
    args: [
      '--no-sandbox',
      '--disable-gpu',
      '--no-proxy-server',
      '--ignore-certificate-errors',
      `--disable-extensions-except=${extensionRoot}`,
      `--load-extension=${extensionRoot}`,
      '--host-resolver-rules=MAP chatgpt.com 127.0.0.1:8443, MAP searchapi.api.cloud.yandex.net 127.0.0.1:8443, EXCLUDE localhost'
    ]
  });

  const pages = await browser.pages();
  const fixture = pages[0] || await browser.newPage();
  await fixture.bringToFront();
  await fixture.goto(URL, { waitUntil: 'domcontentloaded', timeout: 20000 });

  const swTarget = await browser.waitForTarget(
    target => target.type() === 'service_worker' && target.url().startsWith('chrome-extension://'),
    { timeout: 15000 }
  );
  const extensionId = new URL(swTarget.url()).host;
  const worker = await swTarget.worker();
  if (!worker) throw new Error('MV3 service worker target has no worker context');

  const identityProbe = await worker.evaluate(async expectedUrl => {
    const tabs = await chrome.tabs.query({});
    const tab = tabs.find(item => item.url === expectedUrl);
    if (!tab) return { ok: false, error: 'fixture tab not found', tabs: tabs.map(item => item.url) };
    return await new Promise(resolve => {
      chrome.tabs.sendMessage(tab.id, { type: 'WS_GET_IDENTITY' }, response => {
        resolve({
          ok: Boolean(response?.ok),
          response: response || null,
          runtime_error: chrome.runtime.lastError?.message || null,
          tab_id: tab.id
        });
      });
    });
  }, URL);

  if (!identityProbe.ok) throw new Error(`CONTENT_IDENTITY_FAIL ${JSON.stringify(identityProbe)}`);
  if (identityProbe.response?.conversation_key !== KEY) {
    throw new Error(`CONTENT_IDENTITY_KEY_FAIL ${JSON.stringify(identityProbe.response)}`);
  }

  const popupTab = await worker.evaluate(async () => {
    return await chrome.tabs.create({ url: chrome.runtime.getURL('popup.html'), active: false });
  });
  if (!popupTab?.id) throw new Error('POPUP_BACKGROUND_TAB_CREATE_FAIL');

  const popupUrl = `chrome-extension://${extensionId}/popup.html`;
  const popupTarget = await browser.waitForTarget(target => target.url() === popupUrl, { timeout: 10000 });
  const popup = await popupTarget.page();
  if (!popup) throw new Error('POPUP_PAGE_TARGET_FAIL');

  await popup.waitForFunction(expected => {
    const meta = document.getElementById('conversationMeta');
    return meta?.textContent === expected;
  }, { timeout: 10000 }, KEY);

  const popupState = await popup.evaluate(() => ({
    conversation: document.getElementById('conversationMeta')?.textContent || '',
    activeServiceDisabled: Boolean(document.getElementById('activeService')?.disabled),
    bindDisabled: Boolean(document.getElementById('bindConversation')?.disabled),
    manualDisabled: Boolean(document.getElementById('manualMode')?.disabled),
    status: document.getElementById('status')?.textContent || ''
  }));

  if (popupState.conversation !== KEY) throw new Error(`POPUP_CONVERSATION_FAIL ${JSON.stringify(popupState)}`);
  if (popupState.activeServiceDisabled || popupState.bindDisabled || popupState.manualDisabled) {
    throw new Error(`POPUP_CONTROLS_STILL_DISABLED ${JSON.stringify(popupState)}`);
  }

  const providerHits = serverHits.filter(hit => hit.host.startsWith('searchapi.api.cloud.yandex.net'));
  if (providerHits.length) throw new Error(`UNEXPECTED_YANDEX_REQUESTS ${JSON.stringify(providerHits)}`);

  console.log(`CFT_EXTENSION_ID=${extensionId}`);
  console.log(`CFT_PROJECT_ROUTE=${URL}`);
  console.log(`CFT_CONVERSATION_KEY=${popupState.conversation}`);
  console.log(`CFT_POPUP_STATUS=${popupState.status}`);
  console.log('CFT_CONTENT_IDENTITY_PASS');
  console.log('CFT_POPUP_PROJECT_ROUTE_PASS');
  console.log('CFT_POPUP_CONTROLS_ENABLED_PASS');
  console.log('CFT_REAL_YANDEX_REQUESTS=0');
} finally {
  if (browser) await browser.close().catch(() => {});
  await new Promise(resolve => server.close(resolve));
}
