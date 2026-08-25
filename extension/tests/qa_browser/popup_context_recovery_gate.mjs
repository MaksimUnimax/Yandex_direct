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

async function createNestedTargetSession(control, targetId) {
  const attached = await withTimeout(
    control.send('Target.attachToTarget', { targetId, flatten:false }),
    5000,
    'WORKER_TARGET_ATTACH'
  );
  const sessionId = attached?.sessionId;
  assert(Boolean(sessionId), 'WORKER_TARGET_SESSION_ID_MISSING');

  let nextId = 1;
  const pending = new Map();
  const onMessage = (event) => {
    if (event?.sessionId !== sessionId) return;
    let message;
    try { message = JSON.parse(event.message || '{}'); } catch { return; }
    if (!Number.isInteger(message.id)) return;
    const slot = pending.get(message.id);
    if (!slot) return;
    pending.delete(message.id);
    if (message.error) {
      slot.reject(new Error(`${message.error.message || 'CDP_CHILD_ERROR'} (${message.error.code ?? 'no-code'})`));
    } else {
      slot.resolve(message.result || {});
    }
  };
  control.on('Target.receivedMessageFromTarget', onMessage);

  return {
    sessionId,
    async send(method, params = {}) {
      const id = nextId++;
      const response = new Promise((resolve, reject) => pending.set(id, { resolve, reject }));
      try {
        await withTimeout(control.send('Target.sendMessageToTarget', {
          sessionId,
          message:JSON.stringify({ id, method, params })
        }), 5000, `WORKER_CHILD_SEND_${method}`);
        return await withTimeout(response, 8000, `WORKER_CHILD_RESPONSE_${method}`);
      } catch (error) {
        pending.delete(id);
        throw error;
      }
    },
    async detach() {
      control.off('Target.receivedMessageFromTarget', onMessage);
      for (const slot of pending.values()) slot.reject(new Error('WORKER_CHILD_SESSION_DETACHED'));
      pending.clear();
      await control.send('Target.detachFromTarget', { sessionId }).catch(() => {});
    }
  };
}

async function openExtensionWorkerTransport(page, extensionOrigin, extensionId) {
  const control = await page.target().createCDPSession();
  const versions = [];
  const onVersions = (event) => {
    for (const version of event?.versions || []) versions.push(version);
  };
  control.on('ServiceWorker.workerVersionUpdated', onVersions);

  let child = null;
  try {
    await withTimeout(control.send('ServiceWorker.enable'), 3000, 'SERVICE_WORKER_ENABLE');
    await withTimeout(control.send('Target.setDiscoverTargets', { discover:true }), 3000, 'TARGET_DISCOVERY_ENABLE');
    await withTimeout(control.send('ServiceWorker.startWorker', { scopeURL:extensionOrigin }), 10000, 'SERVICE_WORKER_START');
    console.log('CONTEXT_RECOVERY_REPLACEMENT_WORKER_WAKE_PASS');

    const targetInfo = await waitUntil(async () => {
      const result = await control.send('Target.getTargets');
      const direct = (result?.targetInfos || []).find((info) =>
        info.type === 'service_worker' && String(info.url || '').startsWith(extensionOrigin)
      );
      if (direct) return { ...direct, source:'Target.getTargets' };

      const version = [...versions].reverse().find((row) =>
        row?.targetId && String(row.scriptURL || '').startsWith(extensionOrigin) && row.runningStatus === 'running'
      );
      return version ? {
        targetId:version.targetId,
        type:'service_worker',
        url:version.scriptURL,
        source:'ServiceWorker.workerVersionUpdated',
        runningStatus:version.runningStatus,
        status:version.status
      } : false;
    }, 'CURRENT_EXTENSION_WORKER_TARGET_NOT_AVAILABLE', 12000, 120);
    console.log(`CONTEXT_RECOVERY_CDP_WORKER_TARGET ${JSON.stringify(targetInfo)}`);

    child = await createNestedTargetSession(control, targetInfo.targetId);
    await child.send('Runtime.enable');
    const runtimeId = await cdpEvaluate(child, 'globalThis.chrome?.runtime?.id || ""', 'WORKER_RUNTIME_ID');
    assert(runtimeId === extensionId, `WORKER_RUNTIME_ID_MISMATCH ${JSON.stringify({ runtimeId, extensionId, targetInfo })}`);
    console.log('CONTEXT_RECOVERY_REPLACEMENT_WORKER_SESSION_PASS');

    return {
      session:child,
      async close() {
        if (child) await child.detach().catch(() => {});
        control.off('ServiceWorker.workerVersionUpdated', onVersions);
        await control.detach().catch(() => {});
      }
    };
  } catch (error) {
    const targets = await control.send('Target.getTargets').catch(() => ({ targetInfos:[] }));
    console.log(`CONTEXT_RECOVERY_CDP_DIAGNOSTIC ${JSON.stringify({
      targets:(targets.targetInfos || []).filter((info) => info.type === 'service_worker' || String(info.url || '').startsWith(extensionOrigin)),
      versions:versions.slice(-12)
    })}`);
    if (child) await child.detach().catch(() => {});
    control.off('ServiceWorker.workerVersionUpdated', onVersions);
    await control.detach().catch(() => {});
    throw error;
  }
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
      href:location.href,
      readyState:document.readyState,
      runtimeId:chrome.runtime?.id || '',
      conversation:document.getElementById('conversationMeta')?.textContent || '',
      bindDisabled:Boolean(document.getElementById('bindConversation')?.disabled),
      manualDisabled:Boolean(document.getElementById('manualMode')?.disabled),
      status:document.getElementById('status')?.textContent || '',
      statusLevel:document.getElementById('status')?.dataset?.level || '',
      bootstrapError:globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_ERROR__ || '',
      bootstrapResult:globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_RESULT__ || null,
      popupRuntimePresent:Boolean(document.querySelector('script[data-ymb-popup-runtime="true"]')),
      scripts:[...document.scripts].map((script) => script.src || '(inline)'),
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
let workerTransport = null;
try {
  browser = await puppeteer.launch({
    executablePath:chromePath,
    headless:false,
    userDataDir:fs.mkdtempSync(path.join(os.tmpdir(), 'ymb-context-recovery-')),
    args:[
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
    url:location.href,
    marker:document.documentElement.dataset.ymbRecoveryMarker || '',
    expected
  }), documentMarker);
  assert(pageStable.url === CHAT_URL && pageStable.marker === documentMarker, `CHAT_PAGE_RELOADED_UNEXPECTEDLY ${JSON.stringify(pageStable)}`);
  console.log('CONTEXT_RECOVERY_CHAT_PAGE_REMAINED_OPEN_PASS');

  // Use the DevTools protocol itself as the transport after runtime.reload(). Puppeteer's target
  // manager may retain a stale MV3 worker handle, but ServiceWorker/Target domains expose the live
  // registered worker and its targetId directly. Starting/attaching the worker does not inject any
  // content script; the explicit missing-receiver assertion below must still fail before popup open.
  workerTransport = await openExtensionWorkerTransport(chat, extensionOrigin, extensionId);
  const currentWorkerSession = workerTransport.session;

  await chat.bringToFront();
  const activeTabs = await cdpActiveTabs(currentWorkerSession);
  console.log(`CONTEXT_RECOVERY_WORKER_ACTIVE_TABS ${JSON.stringify(activeTabs)}`);
  assert(activeTabs.length === 1 && activeTabs[0].id === tabId && activeTabs[0].url === CHAT_URL, `RECOVERY_ACTIVE_TAB_NOT_CHATGPT ${JSON.stringify(activeTabs)}`);

  const missingReceiver = await cdpTabIdentity(currentWorkerSession, tabId);
  console.log(`CONTEXT_RECOVERY_PRE_POPUP_IDENTITY_STATE ${JSON.stringify(missingReceiver)}`);
  assert(missingReceiver.response?.ok !== true, `RECOVERY_RECEIVER_UNEXPECTEDLY_STILL_LIVE ${JSON.stringify(missingReceiver)}`);
  assert(Boolean(missingReceiver.error), `RECOVERY_MISSING_RECEIVER_ERROR_NOT_REPORTED ${JSON.stringify(missingReceiver)}`);
  console.log('CONTEXT_RECOVERY_MISSING_RECEIVER_REPRODUCED_PASS');

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
  if (workerTransport) await workerTransport.close().catch(() => {});
  if (browser) await browser.close().catch(() => {});
}
