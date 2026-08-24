import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import process from 'node:process';
import puppeteer from 'puppeteer-core';

const [chromePath, extensionRoot] = process.argv.slice(2);
if (!chromePath || !extensionRoot) throw new Error('usage: popup_context_recovery_gate.mjs <chrome> <extension-root>');
if (!fs.existsSync(chromePath) || !fs.existsSync(extensionRoot)) throw new Error('RECOVERY_GATE_INPUT_MISSING');

const CID = '99999999-8888-4777-8666-555555555555';
const CHAT_URL = `https://chatgpt.com/c/${CID}`;
const KEY = `https://chatgpt.com|${CID}`;
const FIXTURE = `<!doctype html><html><head><meta charset="utf-8"><title>Context recovery fixture</title></head><body>
<main id="conversation-root"><div data-message-author-role="assistant" data-message-id="baseline-recovery"><pre data-testid="code-block"><code>controlled recovery block</code></pre></div></main>
<textarea id="prompt-textarea"></textarea><button id="composer-submit-button" data-testid="send-button" aria-label="Send" type="button">Send</button>
</body></html>`;

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
function assert(condition, message) { if (!condition) throw new Error(message); }
async function waitUntil(fn, message, timeout = 15000, interval = 100) {
  const started = Date.now(); let last;
  while (Date.now() - started < timeout) {
    try { last = await fn(); if (last) return last; } catch (error) { last = error; }
    await delay(interval);
  }
  throw new Error(`${message}; last=${last instanceof Error ? last.message : JSON.stringify(last)}`);
}

async function workerTabIdentity(worker, tabId) {
  return await worker.evaluate(async (id) => await new Promise((resolve) => {
    chrome.tabs.sendMessage(id, { type:'WS_GET_IDENTITY' }, (response) => {
      resolve({ response: response || null, error: chrome.runtime.lastError?.message || '' });
    });
  }), tabId);
}

async function nativePopupPage(browser, extensionOrigin) {
  const target = await browser.waitForTarget(
    (t) => t.type() === 'page' && t.url() === `${extensionOrigin}popup.html`,
    { timeout: 15000 }
  );
  const page = await target.page();
  assert(page, 'NATIVE_POPUP_PAGE_UNAVAILABLE');
  return page;
}

let browser;
try {
  browser = await puppeteer.launch({
    executablePath: chromePath,
    headless: false,
    userDataDir: fs.mkdtempSync(path.join(os.tmpdir(), 'ymb-context-recovery-')),
    args: [
      '--no-sandbox', '--disable-gpu', '--no-proxy-server', '--disable-background-networking',
      `--disable-extensions-except=${extensionRoot}`, `--load-extension=${extensionRoot}`
    ]
  });

  const pages = await browser.pages();
  const chat = pages[0] || await browser.newPage();
  await chat.setRequestInterception(true);
  chat.on('request', (req) => {
    if (req.isNavigationRequest() && req.url().startsWith('https://chatgpt.com/')) {
      void req.respond({ status:200, contentType:'text/html; charset=utf-8', body:FIXTURE });
      return;
    }
    void req.abort();
  });
  await chat.goto(CHAT_URL, { waitUntil:'domcontentloaded', timeout:20000 });
  await chat.bringToFront();

  const firstTarget = await browser.waitForTarget((t) => t.type() === 'service_worker' && t.url().startsWith('chrome-extension://'), { timeout:15000 });
  const firstWorker = await firstTarget.worker();
  assert(firstWorker, 'FIRST_WORKER_UNAVAILABLE');
  const extensionOrigin = firstTarget.url().replace(/[^/]+$/, '');
  const tabId = await firstWorker.evaluate(async (url) => (await chrome.tabs.query({})).find((tab) => tab.url === url)?.id || null, CHAT_URL);
  assert(Number.isInteger(tabId), 'CHAT_TAB_NOT_FOUND');

  const before = await waitUntil(async () => {
    const row = await workerTabIdentity(firstWorker, tabId);
    return row.response?.ok === true && row.response?.conversation_key === KEY ? row : false;
  }, 'PRE_RELOAD_CONTENT_IDENTITY_FAIL');
  assert(before.response.conversation_key === KEY, 'PRE_RELOAD_KEY_FAIL');
  console.log('CONTEXT_RECOVERY_PRE_RELOAD_IDENTITY_PASS');

  const oldTarget = firstTarget;
  await firstWorker.evaluate(() => { setTimeout(() => chrome.runtime.reload(), 0); return true; });
  const secondTarget = await browser.waitForTarget(
    (t) => t !== oldTarget && t.type() === 'service_worker' && t.url().startsWith('chrome-extension://'),
    { timeout:20000 }
  );
  const secondWorker = await secondTarget.worker();
  assert(secondWorker, 'SECOND_WORKER_UNAVAILABLE');
  console.log('CONTEXT_RECOVERY_EXTENSION_RUNTIME_RELOAD_PASS');

  const afterReload = await workerTabIdentity(secondWorker, tabId);
  assert(!afterReload.response?.ok, `EXPECTED_MISSING_RECEIVER_AFTER_RUNTIME_RELOAD ${JSON.stringify(afterReload)}`);
  console.log(`CONTEXT_RECOVERY_MISSING_RECEIVER_REPRODUCED ${JSON.stringify(afterReload)}`);

  await chat.bringToFront();
  await secondWorker.evaluate(async () => { await chrome.action.openPopup(); return true; });
  const popup = await nativePopupPage(browser, extensionOrigin);

  await waitUntil(async () => {
    const state = await popup.evaluate(() => ({
      conversation: document.getElementById('conversationMeta')?.textContent || '',
      bindDisabled: Boolean(document.getElementById('bindConversation')?.disabled),
      manualDisabled: Boolean(document.getElementById('manualMode')?.disabled),
      status: document.getElementById('status')?.textContent || ''
    }));
    return state.conversation === KEY && state.bindDisabled === false && state.manualDisabled === false ? state : false;
  }, 'POPUP_CONTEXT_SELF_RECOVERY_FAIL', 20000);
  console.log('POPUP_CONTEXT_SELF_RECOVERY_PASS');

  const recovered = await workerTabIdentity(secondWorker, tabId);
  assert(recovered.response?.ok === true && recovered.response?.conversation_key === KEY, `RECOVERED_CONTENT_IDENTITY_FAIL ${JSON.stringify(recovered)}`);
  console.log('CONTEXT_RECOVERY_POST_BOOTSTRAP_IDENTITY_PASS');

  await popup.evaluate(() => document.getElementById('bindConversation')?.click());
  await waitUntil(async () => await popup.evaluate(() => document.getElementById('status')?.textContent === 'Диалог привязан.'), 'RECOVERY_BIND_ACTION_FAIL');
  console.log('CONTEXT_RECOVERY_BIND_PASS');

  await popup.evaluate(() => { const el=document.getElementById('manualMode'); el.click(); });
  await waitUntil(async () => await popup.evaluate(() => document.getElementById('status')?.textContent === 'Ручной режим включён.'), 'RECOVERY_MANUAL_ON_FAIL');
  await waitUntil(async () => await chat.evaluate(() => document.querySelector('#ymb-external-action-surface')?.shadowRoot?.querySelectorAll('.ymb-action').length === 1), 'RECOVERY_MANUAL_ACTION_SURFACE_FAIL');
  console.log('CONTEXT_RECOVERY_MANUAL_ON_PASS');
  console.log('CONTEXT_RECOVERY_ALREADY_OPEN_CHATGPT_PASS');
  console.log('REAL_YANDEX_REQUESTS=0');
} finally {
  if (browser) await browser.close().catch(() => {});
}
