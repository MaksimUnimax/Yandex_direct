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
async function withTimeout(promise, timeout, label) {
  let timer;
  try {
    return await Promise.race([
      promise,
      new Promise((_, reject) => { timer = setTimeout(() => reject(new Error(`${label}_TIMEOUT`)), timeout); })
    ]);
  } finally { clearTimeout(timer); }
}

async function workerTabIdentity(worker, tabId) {
  return await worker.evaluate(async (id) => await new Promise((resolve) => {
    chrome.tabs.sendMessage(id, { type:'WS_GET_IDENTITY' }, (response) => {
      resolve({ response: response || null, error: chrome.runtime.lastError?.message || '' });
    });
  }), tabId);
}

async function cdpEvaluate(session, expression, label, timeout = 5000) {
  const result = await withTimeout(session.send('Runtime.evaluate', {
    expression,
    awaitPromise:true,
    returnByValue:true
  }), timeout, label);
  if (result?.exceptionDetails) {
    const description = result.exceptionDetails.exception?.description || result.exceptionDetails.text || 'UNKNOWN_EXCEPTION';
    throw new Error(`${label}_EXCEPTION ${description}`);
  }
  return result?.result?.value;
}

async function wakeExtensionWorker(page, extensionOrigin) {
  const session = await page.target().createCDPSession();
  try {
    await withTimeout(session.send('ServiceWorker.enable'), 3000, 'SERVICE_WORKER_ENABLE');
    await withTimeout(
      session.send('ServiceWorker.startWorker', { scopeURL: extensionOrigin }),
      10000,
      'SERVICE_WORKER_START'
    );
  } finally {
    await session.detach().catch(() => {});
  }
}

async function currentExtensionWorkerSession(browser, extensionOrigin, extensionId) {
  return await waitUntil(async () => {
    const targets = browser.targets().filter((t) => t.type() === 'service_worker' && t.url().startsWith(extensionOrigin));
    for (const target of targets) {
      let session = null;
      try {
        session = await target.createCDPSession();
        await withTimeout(session.send('Runtime.enable'), 3000, 'WORKER_RUNTIME_ENABLE');
        const id = await cdpEvaluate(session, 'globalThis.chrome?.runtime?.id || ""', 'WORKER_RUNTIME_ID', 3000);
        if (id === extensionId) return { target, session };
      } catch {
        // A retained MV3 target may still point at a destroyed execution context. Retry with a fresh session.
      }
      if (session) await session.detach().catch(() => {});
    }
    return false;
  }, 'CURRENT_EXTENSION_WORKER_SESSION_NOT_AVAILABLE', 20000, 150);
}

async function cdpActiveTabs(session) {
  const json = await cdpEvaluate(
    session,
    '(async()=>JSON.stringify((await chrome.tabs.query({active:true,currentWindow:true})).map(tab=>({id:tab.id,url:tab.url||"",active:tab.active===true,windowId:tab.windowId}))))()',
    'WORKER_ACTIVE_TABS'
  );
  return JSON.parse(json || '[]');
}

async function cdpTabIdentity(session, tabId) {
  const expression = `(async()=>JSON.stringify(await new Promise(resolve=>{chrome.tabs.sendMessage(${JSON.stringify(tabId)},{type:"WS_GET_IDENTITY"},response=>resolve({response:response||null,error:chrome.runtime.lastError?.message||""}))})))()`;
  const json = await cdpEvaluate(session, expression, 'WORKER_TAB_IDENTITY');
  return JSON.parse(json || '{}');
}

async function cdpOpenActionPopup(session) {
  return await cdpEvaluate(session, '(async()=>{await chrome.action.openPopup();return true})()', 'WORKER_OPEN_ACTION_POPUP', 10000);
}

async function popupSnapshot(popup) {
  return await popup.evaluate(async () => {
    let activeTabs = [];
    let activeTabError = '';
    try {
      activeTabs = await new Promise((resolve) => {
        chrome.tabs.query({ active:true, currentWindow:true }, (tabs) => {
          activeTabError = chrome.runtime.lastError?.message || '';
          resolve((tabs || []).map((tab) => ({ id:tab.id, url:tab.url || '', active:tab.active === true, windowId:tab.windowId })));
        });
      });
    } catch (error) { activeTabError = error?.message || String(error); }
    return {
      href: location.href,
      readyState: document.readyState,
      runtimeId: chrome.runtime?.id || '',
      conversation: document.getElementById('conversationMeta')?.textContent || '',
      bindDisabled: Boolean(document.getElementById('bindConversation')?.disabled),
      manualDisabled: Boolean(document.getElementById('manualMode')?.disabled),
      status: document.getElementById('status')?.textContent || '',
      statusLevel: document.getElementById('status')?.dataset?.level || '',
      bootstrapError: globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_ERROR__ || '',
      bootstrapResult: globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_RESULT__ || null,
      popupRuntimePresent: Boolean(document.querySelector('script[data-ymb-popup-runtime="true"]')),
      scripts: [...document.scripts].map((script) => script.src || '(inline)'),
      activeTabs,
      activeTabError
    };
  });
}

async function waitForPopupBootstrapOutcome(popup, timeout = 8000) {
  const started = Date.now();
  let last = null;
  while (Date.now() - started < timeout) {
    last = await popupSnapshot(popup);
    if (last.bootstrapError || last.bootstrapResult) return last;
    await delay(100);
  }
  throw new Error(`POPUP_BOOTSTRAP_OUTCOME_TIMEOUT state=${JSON.stringify(last)}`);
}

let browser;
let currentWorkerSession = null;
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
  const documentMarker = await chat.evaluate(() => {
    const marker = `${Date.now()}-${Math.random()}`;
    document.documentElement.dataset.ymbRecoveryMarker = marker;
    return marker;
  });

  const firstTarget = await browser.waitForTarget((t) => t.type() === 'service_worker' && t.url().startsWith('chrome-extension://'), { timeout:15000 });
  const firstWorker = await firstTarget.worker();
  assert(firstWorker, 'FIRST_WORKER_UNAVAILABLE');
  const extensionOrigin = firstTarget.url().replace(/[^/]+$/, '');
  const extensionId = new URL(extensionOrigin).hostname;
  const tabId = await firstWorker.evaluate(async (url) => (await chrome.tabs.query({})).find((tab) => tab.url === url)?.id || null, CHAT_URL);
  assert(Number.isInteger(tabId), 'CHAT_TAB_NOT_FOUND');

  const before = await waitUntil(async () => {
    const row = await workerTabIdentity(firstWorker, tabId);
    return row.response?.ok === true && row.response?.conversation_key === KEY ? row : false;
  }, 'PRE_RELOAD_CONTENT_IDENTITY_FAIL');
  assert(before.response.conversation_key === KEY, 'PRE_RELOAD_KEY_FAIL');
  console.log('CONTEXT_RECOVERY_PRE_RELOAD_IDENTITY_PASS');

  await firstWorker.evaluate(() => { setTimeout(() => chrome.runtime.reload(), 0); return true; });
  await delay(800);
  console.log('CONTEXT_RECOVERY_RUNTIME_RELOAD_TRIGGERED_PASS');

  const pageStable = await chat.evaluate((expected) => ({
    url: location.href,
    marker: document.documentElement.dataset.ymbRecoveryMarker || '',
    expected
  }), documentMarker);
  assert(pageStable.url === CHAT_URL && pageStable.marker === documentMarker, `CHAT_PAGE_RELOADED_UNEXPECTEDLY ${JSON.stringify(pageStable)}`);
  console.log('CONTEXT_RECOVERY_CHAT_PAGE_REMAINED_OPEN_PASS');

  // runtime.reload() may leave the extension's MV3 worker stopped with no debuggable execution context.
  // Wake only the registered worker through a normal page-target CDP session. This does not inject page
  // scripts and cannot satisfy the recovery assertion by itself; the missing-receiver probe must still fail.
  await wakeExtensionWorker(chat, extensionOrigin);
  console.log('CONTEXT_RECOVERY_REPLACEMENT_WORKER_WAKE_PASS');

  // Attach a fresh CDP session to whichever MV3 service-worker execution context is current.
  // The target itself may be retained across runtime.reload(), so target identity is not a lifecycle signal.
  const currentWorker = await currentExtensionWorkerSession(browser, extensionOrigin, extensionId);
  currentWorkerSession = currentWorker.session;
  console.log('CONTEXT_RECOVERY_REPLACEMENT_WORKER_SESSION_PASS');

  await chat.bringToFront();
  const activeTabs = await cdpActiveTabs(currentWorkerSession);
  console.log(`CONTEXT_RECOVERY_WORKER_ACTIVE_TABS ${JSON.stringify(activeTabs)}`);
  assert(activeTabs.length === 1 && activeTabs[0].id === tabId && activeTabs[0].url === CHAT_URL, `RECOVERY_ACTIVE_TAB_NOT_CHATGPT ${JSON.stringify(activeTabs)}`);

  // Prove the exact owner-live failure condition before opening the popup: the already-open page
  // is still there, but the replacement extension runtime cannot reach the old content-script receiver.
  const missingReceiver = await cdpTabIdentity(currentWorkerSession, tabId);
  console.log(`CONTEXT_RECOVERY_PRE_POPUP_IDENTITY_STATE ${JSON.stringify(missingReceiver)}`);
  assert(missingReceiver.response?.ok !== true, `RECOVERY_RECEIVER_UNEXPECTEDLY_STILL_LIVE ${JSON.stringify(missingReceiver)}`);
  assert(Boolean(missingReceiver.error), `RECOVERY_MISSING_RECEIVER_ERROR_NOT_REPORTED ${JSON.stringify(missingReceiver)}`);
  console.log('CONTEXT_RECOVERY_MISSING_RECEIVER_REPRODUCED_PASS');

  // Open the actual toolbar action popup from the live extension context. No synthetic
  // chrome-extension:// page navigation is used; ChatGPT remains the active browser tab.
  await chat.bringToFront();
  const existingTargets = new Set(browser.targets());
  const openPromise = cdpOpenActionPopup(currentWorkerSession);
  const nativeTargetPromise = browser.waitForTarget(
    (t) => !existingTargets.has(t) && t.type() === 'page' && t.url() === `${extensionOrigin}popup.html`,
    { timeout:15000 }
  );
  const [nativeTarget] = await Promise.all([nativeTargetPromise, openPromise]);
  const popup = await nativeTarget.page();
  assert(popup, 'RECOVERY_NATIVE_POPUP_PAGE_FAIL');
  console.log('CONTEXT_RECOVERY_NATIVE_ACTION_POPUP_OPEN_PASS');

  const recoveredState = await waitForPopupBootstrapOutcome(popup, 10000);
  console.log(`CONTEXT_RECOVERY_POPUP_BOOTSTRAP_STATE ${JSON.stringify(recoveredState)}`);
  assert(!recoveredState.bootstrapError, `POPUP_BOOTSTRAP_ERROR ${JSON.stringify(recoveredState)}`);
  assert(recoveredState.bootstrapResult?.attempted === true, `POPUP_RECOVERY_NOT_ATTEMPTED ${JSON.stringify(recoveredState)}`);
  assert(recoveredState.bootstrapResult?.recovered === true, `POPUP_MISSING_RECEIVER_BRANCH_NOT_RECOVERED ${JSON.stringify(recoveredState)}`);
  assert(recoveredState.bootstrapResult?.tab_id === tabId, `POPUP_RECOVERY_WRONG_TAB ${JSON.stringify(recoveredState)}`);

  const readyState = await waitUntil(async () => {
    const state = await popupSnapshot(popup);
    return state.conversation === KEY && state.bindDisabled === false && state.manualDisabled === false ? state : false;
  }, 'POPUP_CONTEXT_SELF_RECOVERY_UI_FAIL', 12000);
  console.log(`CONTEXT_RECOVERY_POPUP_READY_STATE ${JSON.stringify(readyState)}`);
  console.log('POPUP_CONTEXT_SELF_RECOVERY_PASS');

  const recovered = await cdpTabIdentity(currentWorkerSession, tabId);
  assert(recovered.response?.ok === true && recovered.response?.conversation_key === KEY, `RECOVERED_CONTENT_IDENTITY_FAIL ${JSON.stringify(recovered)}`);
  console.log('CONTEXT_RECOVERY_POST_BOOTSTRAP_IDENTITY_PASS');

  await popup.evaluate(() => document.getElementById('bindConversation')?.click());
  await waitUntil(async () => await popup.evaluate(() => document.getElementById('status')?.textContent === 'Диалог привязан.'), 'RECOVERY_BIND_ACTION_FAIL');
  console.log('CONTEXT_RECOVERY_BIND_PASS');

  await popup.evaluate(() => document.getElementById('manualMode')?.click());
  await waitUntil(async () => await popup.evaluate(() => document.getElementById('status')?.textContent === 'Ручной режим включён.'), 'RECOVERY_MANUAL_ON_FAIL');
  await waitUntil(async () => await chat.evaluate(() => document.querySelector('#ymb-external-action-surface')?.shadowRoot?.querySelectorAll('.ymb-action').length === 1), 'RECOVERY_MANUAL_ACTION_SURFACE_FAIL');
  console.log('CONTEXT_RECOVERY_MANUAL_ON_PASS');

  console.log('CONTEXT_RECOVERY_ALREADY_OPEN_CHATGPT_PASS');
  console.log('REAL_YANDEX_REQUESTS=0');
} finally {
  if (currentWorkerSession) await currentWorkerSession.detach().catch(() => {});
  if (browser) await browser.close().catch(() => {});
}
