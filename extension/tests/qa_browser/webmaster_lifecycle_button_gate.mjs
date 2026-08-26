import fs from 'node:fs';
import https from 'node:https';
import os from 'node:os';
import path from 'node:path';
import process from 'node:process';
import puppeteer from 'puppeteer-core';

const [chromePath, extensionRoot, keyPath, certPath] = process.argv.slice(2);
for (const p of [chromePath, extensionRoot, keyPath, certPath]) {
  if (!p || !fs.existsSync(p)) throw new Error(`HARNESS_INPUT_MISSING ${p || '<empty>'}`);
}

const CID = '99999999-8888-4777-8666-555555555555';
const CHAT_URL = `https://chatgpt.com/c/${CID}`;
const CKEY = `https://chatgpt.com|${CID}`;
const providerHits = [];
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
function assert(condition, message) { if (!condition) throw new Error(message); }
async function waitUntil(fn, message, timeout = 15000, interval = 80) {
  const started = Date.now(); let last;
  while (Date.now() - started < timeout) {
    try { last = await fn(); if (last) return last; } catch (error) { last = error; }
    await delay(interval);
  }
  throw new Error(`${message}; last=${last instanceof Error ? last.message : JSON.stringify(last)}`);
}

function fixtureHtml() {
  return `<!doctype html><html><head><meta charset="utf-8"><link rel="canonical" href="${CHAT_URL}"><title>Webmaster Lifecycle QA</title></head><body>
  <main id="conversation-root">
    <div data-message-author-role="assistant" data-message-id="qa-webmaster-lifecycle-block">
      <pre data-testid="code-block"><code>controlled Webmaster lifecycle blocker fixture</code></pre>
      <button aria-label="Copy" type="button">Copy</button>
    </div>
  </main>
  <textarea id="prompt-textarea"></textarea>
  <button id="composer-submit-button" data-testid="send-button" aria-label="Send" type="button">Send</button>
  <script>
    const composer=document.getElementById('prompt-textarea');
    document.getElementById('composer-submit-button').addEventListener('click',()=>{
      composer.value=''; composer.dispatchEvent(new Event('input',{bubbles:true}));
    });
  </script></body></html>`;
}

const server = https.createServer({ key: fs.readFileSync(keyPath), cert: fs.readFileSync(certPath) }, (req, res) => {
  const host = String(req.headers.host || '').split(':')[0].toLowerCase();
  if (host === 'api.webmaster.yandex.net' || host === 'searchapi.api.cloud.yandex.net') {
    const chunks = [];
    req.on('data', (c) => chunks.push(c));
    req.on('end', () => {
      providerHits.push({ host, method: req.method, url: req.url, body_bytes: Buffer.concat(chunks).length });
      res.writeHead(500, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ code: 'QA_PROVIDER_MUST_NOT_BE_CALLED' }));
    });
    return;
  }
  res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
  res.end(fixtureHtml());
});
await new Promise((resolve, reject) => { server.once('error', reject); server.listen(8443, '127.0.0.1', resolve); });

async function openPopup(worker, browser) {
  const owner = await worker.evaluate(async (expectedKey) => {
    const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
    const active = tabs?.[0] || null;
    if (!active?.id) return { active: null, identity: null };
    const identity = await new Promise((resolve) => chrome.tabs.sendMessage(active.id, { type: 'WS_GET_IDENTITY' }, (response) => resolve({ response: response || null, error: chrome.runtime.lastError?.message || null })));
    return { active: { id: active.id, url: active.url || '' }, identity, expectedKey };
  }, CKEY);
  assert(owner?.active?.id, `POPUP_OWNER_ACTIVE_TAB_MISSING ${JSON.stringify(owner)}`);
  assert(owner.identity?.response?.ok === true && owner.identity.response.conversation_key === CKEY, `POPUP_OWNER_CONTEXT_FAIL ${JSON.stringify(owner)}`);
  const tab = await worker.evaluate(async (ownerTabId) => {
    const created = await chrome.tabs.create({ url: 'about:blank', active: false });
    if (!created?.id) return null;
    await chrome.tabs.update(ownerTabId, { active: true });
    await chrome.tabs.update(created.id, { url: chrome.runtime.getURL('popup.html') });
    return { id: created.id };
  }, owner.active.id);
  assert(tab?.id, 'POPUP_TAB_CREATE_FAIL');
  const popup = await waitUntil(async () => {
    for (const page of await browser.pages()) {
      if (!page.url().startsWith('chrome-extension://') || !page.url().endsWith('/popup.html')) continue;
      const current = await page.evaluate(() => new Promise((resolve) => chrome.tabs.getCurrent((t) => resolve(t?.id || null)))).catch(() => null);
      if (Number(current) === Number(tab.id)) return page;
    }
    return null;
  }, 'POPUP_TAB_TARGET_FAIL', 12000);
  await popup.waitForFunction((expected) => document.getElementById('conversationMeta')?.textContent === expected, { timeout: 12000 }, CKEY);
  await waitUntil(async () => {
    const state = await popup.evaluate(() => ({ text: document.getElementById('status')?.textContent || '', level: document.getElementById('status')?.dataset?.level || '' }));
    if (state.level === 'error') throw new Error(`POPUP_INITIAL_ERROR ${state.text}`);
    return state.text === 'Готово.' ? state : false;
  }, 'POPUP_INITIAL_REFRESH_NOT_COMPLETE', 12000);
  return { popup, ownerTabId: owner.active.id };
}

async function popupClick(popup, selector) {
  await popup.evaluate((sel) => {
    const el = document.querySelector(sel);
    if (!el) throw new Error(`POPUP_ELEMENT_MISSING ${sel}`);
    if (el.disabled) throw new Error(`POPUP_ELEMENT_DISABLED ${sel}`);
    el.click();
  }, selector);
}
async function waitPopupStatus(popup, expected, message) {
  return waitUntil(async () => {
    const state = await popup.evaluate(() => ({ text: document.getElementById('status')?.textContent || '', level: document.getElementById('status')?.dataset?.level || '' }));
    if (state.level === 'error') throw new Error(`POPUP_ERROR ${state.text}`);
    return state.text === expected ? state : false;
  }, message);
}
async function runtimeState(popup) {
  return popup.evaluate((key) => new Promise((resolve) => chrome.runtime.sendMessage({ type: 'WS_GET_STATE', conversation_key: key }, (r) => resolve(r || null))), CKEY);
}
async function actionSnapshot(page) {
  return page.evaluate(() => {
    const root = document.querySelector('#ymb-external-action-surface')?.shadowRoot;
    const buttons = [...(root?.querySelectorAll('.ymb-action') || [])];
    return { count: buttons.length, disabled: buttons.length === 1 ? buttons[0].disabled : null, title: buttons.length === 1 ? buttons[0].title : '', label: buttons.length === 1 ? buttons[0].textContent : '' };
  });
}
async function refreshContent(worker, tabId) {
  const result = await worker.evaluate(async (id) => await new Promise((resolve) => chrome.tabs.sendMessage(id, { type: 'WS_REFRESH_STATE' }, (r) => resolve({ response: r || null, error: chrome.runtime.lastError?.message || null }))), tabId);
  assert(!result.error && result.response?.ok === true, `CONTENT_REFRESH_FAIL ${JSON.stringify(result)}`);
}
async function setMapRecord(worker, storageKey, key, value) {
  await worker.evaluate(async ({ storageKey, key, value }) => {
    const data = await chrome.storage.local.get(storageKey);
    const map = { ...(data[storageKey] || {}) };
    if (value === null) delete map[key]; else map[key] = value;
    await chrome.storage.local.set({ [storageKey]: map });
  }, { storageKey, key, value });
}
async function storageSnapshot(worker) {
  return worker.evaluate(async () => await chrome.storage.local.get(['wsmb_manual_operations', 'wsmb_outbox', 'ymb_content_error_queue']));
}
async function clearTransient(worker) {
  await worker.evaluate(async () => await chrome.storage.local.set({ wsmb_manual_operations: {}, wsmb_outbox: {}, ymb_content_error_queue: {} }));
}
async function clickDisabledAction(page) {
  return page.evaluate(() => {
    const button = document.querySelector('#ymb-external-action-surface')?.shadowRoot?.querySelector('.ymb-action');
    if (!button) throw new Error('YMB_ACTION_MISSING');
    const before = { disabled: button.disabled, title: button.title };
    button.click();
    return { before, afterDisabled: button.disabled };
  });
}

let browser;
try {
  browser = await puppeteer.launch({
    executablePath: chromePath,
    headless: false,
    protocolTimeout: 30000,
    userDataDir: fs.mkdtempSync(path.join(os.tmpdir(), 'ymb-webmaster-lifecycle-')),
    args: [
      '--no-sandbox', '--disable-gpu', '--no-proxy-server', '--ignore-certificate-errors', '--disable-background-networking', '--disable-features=DnsOverHttps',
      `--disable-extensions-except=${extensionRoot}`, `--load-extension=${extensionRoot}`,
      '--host-resolver-rules=MAP chatgpt.com 127.0.0.1:8443, MAP chat.openai.com 127.0.0.1:8443, MAP api.webmaster.yandex.net 127.0.0.1:8443, MAP searchapi.api.cloud.yandex.net 127.0.0.1:8443, EXCLUDE localhost'
    ]
  });
  const pages = await browser.pages();
  const fixture = pages[0] || await browser.newPage();
  await fixture.bringToFront();
  await fixture.goto(CHAT_URL, { waitUntil: 'domcontentloaded', timeout: 20000 });
  const swTarget = await browser.waitForTarget((t) => t.type() === 'service_worker' && t.url().startsWith('chrome-extension://'), { timeout: 15000 });
  const worker = await swTarget.worker();
  assert(worker, 'MV3_WORKER_CONTEXT_FAIL');

  const { popup, ownerTabId } = await openPopup(worker, browser);
  await popupClick(popup, '#bindConversation');
  await waitPopupStatus(popup, 'Диалог привязан.', 'BIND_NOT_COMPLETE');

  await popup.select('#activeService', 'webmaster');
  await popupClick(popup, '#saveSettings');
  await waitPopupStatus(popup, 'Общие настройки сохранены.', 'WEBMASTER_SERVICE_SAVE_NOT_COMPLETE');
  const serviceState = await waitUntil(async () => {
    const r = await runtimeState(popup);
    return r?.ok && r.state?.service_context?.active_service === 'webmaster' ? r.state : false;
  }, 'WEBMASTER_ACTIVE_SERVICE_NOT_COMMITTED');
  assert(serviceState.webmaster_policy?.manual_enabled === true, 'WEBMASTER_MANUAL_POLICY_NOT_ENABLED');
  console.log('W14_WEBMASTER_ACTIVE_SERVICE_PASS');

  await popupClick(popup, '#manualMode');
  await waitPopupStatus(popup, 'Ручной режим включён.', 'WEBMASTER_MANUAL_ON_NOT_COMPLETE');
  await waitUntil(async () => {
    const r = await runtimeState(popup);
    return r?.ok && r.state?.manual_mode === true && r.state?.service_context?.active_service === 'webmaster' ? r.state : false;
  }, 'WEBMASTER_WORKER_MANUAL_NOT_ON');
  await waitUntil(async () => { const s = await actionSnapshot(fixture); return s.count === 1 && s.disabled === false ? s : false; }, 'WEBMASTER_INITIAL_ACTION_NOT_ENABLED');
  console.log('W14_WEBMASTER_INITIAL_ACTION_ENABLED_PASS');

  await clearTransient(worker);
  await refreshContent(worker, ownerTabId);
  const op = {
    operation_id: 'qa-webmaster-lifecycle-operation', request_token: 'qa-webmaster-lifecycle-token', conversation_key: CKEY,
    tab_id: ownerTabId, active_service: 'webmaster', run_id: null, status: 'requesting', request_executed: false, created_at: new Date().toISOString()
  };
  await setMapRecord(worker, 'wsmb_manual_operations', CKEY, op);
  await refreshContent(worker, ownerTabId);
  const blockedOp = await waitUntil(async () => { const s = await actionSnapshot(fixture); return s.count === 1 && s.disabled === true ? s : false; }, 'WEBMASTER_OPERATION_DID_NOT_DISABLE_ACTION');
  assert(/ручной операции/i.test(blockedOp.title), `WEBMASTER_OPERATION_TITLE_FAIL ${JSON.stringify(blockedOp)}`);
  const beforeOpClick = JSON.stringify(await storageSnapshot(worker));
  const opClick = await clickDisabledAction(fixture);
  assert(opClick.before.disabled === true, 'WEBMASTER_OPERATION_ACTION_NOT_DISABLED_AT_CLICK');
  await delay(500);
  assert(JSON.stringify(await storageSnapshot(worker)) === beforeOpClick, 'WEBMASTER_OPERATION_BLOCKED_CLICK_MUTATED_STATE');
  assert(providerHits.length === 0, `WEBMASTER_OPERATION_BLOCKED_CLICK_PROVIDER_HIT ${providerHits.length}`);
  console.log('W14_WEBMASTER_OPERATION_BLOCKED_NO_DISPATCH_PASS');

  await setMapRecord(worker, 'wsmb_manual_operations', CKEY, null);
  await refreshContent(worker, ownerTabId);
  await waitUntil(async () => { const s = await actionSnapshot(fixture); return s.count === 1 && s.disabled === false ? s : false; }, 'WEBMASTER_OPERATION_CLEAR_DID_NOT_REENABLE_ACTION');
  console.log('W14_WEBMASTER_OPERATION_REENABLE_PASS');

  const delivery = { delivery_id: 'qa-webmaster-lifecycle-delivery', type: 'qa_hold', phase: 'qa_hold', conversation_key: CKEY, tab_id: ownerTabId, report_text: '', created_at: new Date().toISOString(), updated_at: new Date().toISOString() };
  await setMapRecord(worker, 'wsmb_outbox', CKEY, delivery);
  const blockedDelivery = await waitUntil(async () => { const s = await actionSnapshot(fixture); return s.count === 1 && s.disabled === true ? s : false; }, 'WEBMASTER_DELIVERY_DID_NOT_DISABLE_ACTION', 7000);
  assert(/доставки/i.test(blockedDelivery.title), `WEBMASTER_DELIVERY_TITLE_FAIL ${JSON.stringify(blockedDelivery)}`);
  const beforeDeliveryClick = JSON.stringify(await storageSnapshot(worker));
  const deliveryClick = await clickDisabledAction(fixture);
  assert(deliveryClick.before.disabled === true, 'WEBMASTER_DELIVERY_ACTION_NOT_DISABLED_AT_CLICK');
  await delay(700);
  assert(JSON.stringify(await storageSnapshot(worker)) === beforeDeliveryClick, 'WEBMASTER_DELIVERY_BLOCKED_CLICK_MUTATED_STATE');
  assert(providerHits.length === 0, `WEBMASTER_DELIVERY_BLOCKED_CLICK_PROVIDER_HIT ${providerHits.length}`);
  console.log('W14_WEBMASTER_DELIVERY_BLOCKED_NO_DISPATCH_PASS');

  await setMapRecord(worker, 'wsmb_outbox', CKEY, null);
  await waitUntil(async () => { const s = await actionSnapshot(fixture); return s.count === 1 && s.disabled === false ? s : false; }, 'WEBMASTER_DELIVERY_CLEAR_DID_NOT_REENABLE_ACTION', 7000);
  console.log('W14_WEBMASTER_DELIVERY_REENABLE_PASS');

  assert(providerHits.length === 0, `W14_PROVIDER_HITS_UNEXPECTED ${providerHits.length}`);
  console.log('W14_WEBMASTER_PROVIDER_HITS=0');
  console.log('W14_WEBMASTER_REAL_YANDEX_REQUESTS=0');
  console.log('W14_WEBMASTER_LIFECYCLE_BROWSER_PASS');
} finally {
  try { await browser?.close(); } catch {}
  await new Promise((resolve) => server.close(() => resolve()));
}
