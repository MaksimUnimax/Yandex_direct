import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import process from 'node:process';
import puppeteer from 'puppeteer-core';

const [chromePath, extensionRoot] = process.argv.slice(2);
if (!chromePath || !extensionRoot) throw new Error('usage: real_profile_binding_gate.mjs <chrome> <extension-root>');
if (!fs.existsSync(chromePath) || !fs.existsSync(extensionRoot)) throw new Error('REAL_PROFILE_BINDING_GATE_INPUT_MISSING');

const CID = '6a82924e-5ed0-83eb-84a2-851ddad40c88';
const KEY = `https://chatgpt.com|${CID}`;
const DIRECT_URL = `https://chatgpt.com/c/${CID}`;
const PROJECT_URL = 'https://chatgpt.com/g/g-p-real-profile/project-name';

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
function assert(condition, message) { if (!condition) throw new Error(message); }
async function waitUntil(fn, message, timeout = 15000, interval = 100) {
  const started = Date.now();
  let last;
  while (Date.now() - started < timeout) {
    try {
      last = await fn();
      if (last) return last;
    } catch (error) {
      last = error;
    }
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
  } finally {
    clearTimeout(timer);
  }
}

function fixture(canonicalUrl = '') {
  const canonical = canonicalUrl ? `<link rel="canonical" href="${canonicalUrl}">` : '';
  return `<!doctype html><html><head><meta charset="utf-8">${canonical}<title>Real profile binding fixture</title></head><body>
  <main id="conversation-root">
    <section data-turn="assistant" data-turn-id="turn-real-profile">
      <div data-message-author-role="assistant" data-message-id="message-real-profile">
        <pre class="overflow-visible! px-0!" data-start="0" data-end="30"><div class="cm-content" role="textbox" aria-multiline="true" aria-readonly="true" contenteditable="false">WORDSTAT_API_V1\n{"method":"getTop","phrase":"test"}</div><button type="button" aria-label="Копировать">Copy</button></pre>
      </div>
    </section>
  </main>
  <textarea id="prompt-textarea"></textarea>
  <button id="composer-submit-button" data-testid="send-button" aria-label="Send" type="button">Send</button>
  </body></html>`;
}

async function cdpEvaluate(session, expression, label, timeout = 5000) {
  const result = await withTimeout(session.send('Runtime.evaluate', {
    expression,
    awaitPromise: true,
    returnByValue: true
  }), timeout, label);
  if (result?.exceptionDetails) {
    const description = result.exceptionDetails.exception?.description || result.exceptionDetails.text || 'UNKNOWN_EXCEPTION';
    throw new Error(`${label}_EXCEPTION ${description}`);
  }
  return result?.result?.value;
}

async function createNestedTargetSession(control, targetId) {
  const attached = await withTimeout(control.send('Target.attachToTarget', { targetId, flatten: false }), 5000, 'TARGET_ATTACH');
  const sessionId = attached?.sessionId;
  assert(Boolean(sessionId), 'TARGET_SESSION_ID_MISSING');
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
    if (message.error) slot.reject(new Error(`${message.error.message || 'CDP_CHILD_ERROR'} (${message.error.code ?? 'no-code'})`));
    else slot.resolve(message.result || {});
  };
  control.on('Target.receivedMessageFromTarget', onMessage);
  return {
    async send(method, params = {}) {
      const id = nextId++;
      const response = new Promise((resolve, reject) => pending.set(id, { resolve, reject }));
      try {
        await withTimeout(control.send('Target.sendMessageToTarget', { sessionId, message: JSON.stringify({ id, method, params }) }), 5000, `CHILD_SEND_${method}`);
        return await withTimeout(response, 8000, `CHILD_RESPONSE_${method}`);
      } catch (error) {
        pending.delete(id);
        throw error;
      }
    },
    async detach() {
      control.off('Target.receivedMessageFromTarget', onMessage);
      for (const slot of pending.values()) slot.reject(new Error('CHILD_SESSION_DETACHED'));
      pending.clear();
      await control.send('Target.detachFromTarget', { sessionId }).catch(() => {});
    }
  };
}

async function popupSnapshot(session) {
  const json = await cdpEvaluate(session, `(async()=>{
    let activeTabs=[]; let activeTabError='';
    try {
      activeTabs=await new Promise(resolve=>chrome.tabs.query({active:true,currentWindow:true},tabs=>{
        activeTabError=chrome.runtime.lastError?.message||'';
        resolve((tabs||[]).map(tab=>({id:tab.id,url:tab.url||'',active:tab.active===true,windowId:tab.windowId})));
      }));
    } catch(error) { activeTabError=error?.message||String(error); }
    return JSON.stringify({
      href:location.href,
      readyState:document.readyState,
      runtimeId:chrome.runtime?.id||'',
      conversation:document.getElementById('conversationMeta')?.textContent||'',
      bindDisabled:Boolean(document.getElementById('bindConversation')?.disabled),
      manualDisabled:Boolean(document.getElementById('manualMode')?.disabled),
      manualChecked:Boolean(document.getElementById('manualMode')?.checked),
      status:document.getElementById('status')?.textContent||'',
      statusLevel:document.getElementById('status')?.dataset?.level||'',
      bootstrapError:globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_ERROR__||'',
      bootstrapResult:globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_RESULT__||null,
      activeTabs,
      activeTabError
    });
  })()`, 'POPUP_SNAPSHOT');
  return JSON.parse(json || '{}');
}

async function findTabTarget(control, visibleUrl) {
  const pageTarget = await waitUntil(async () => {
    const result = await control.send('Target.getTargets');
    return (result?.targetInfos || []).find((info) => info.type === 'page' && info.url === visibleUrl) || false;
  }, 'CHATGPT_PAGE_TARGET_NOT_FOUND');
  const filter = [{ type: 'tab', exclude: false }, { exclude: true }];
  return await waitUntil(async () => {
    const result = await control.send('Target.getTargets', { filter });
    const tabs = result?.targetInfos || [];
    return tabs.find((info) => info.type === 'tab' && info.url === visibleUrl)
      || tabs.find((info) => info.type === 'tab' && pageTarget.parentId && info.targetId === pageTarget.parentId)
      || false;
  }, 'CHATGPT_TAB_TARGET_NOT_FOUND');
}

async function openNativePopup(control, extensionId, tabTargetId) {
  const popupUrl = `chrome-extension://${extensionId}/popup.html`;
  const before = await control.send('Target.getTargets');
  const beforeIds = new Set((before?.targetInfos || []).map((info) => info.targetId));
  await withTimeout(control.send('Extensions.triggerAction', { id: extensionId, targetId: tabTargetId }), 10000, 'EXTENSIONS_TRIGGER_ACTION');
  const popupTarget = await waitUntil(async () => {
    const result = await control.send('Target.getTargets');
    return (result?.targetInfos || []).find((info) => info.url === popupUrl && (!beforeIds.has(info.targetId) || info.type === 'page' || info.type === 'other')) || false;
  }, 'NATIVE_POPUP_TARGET_NOT_FOUND');
  const session = await createNestedTargetSession(control, popupTarget.targetId);
  await session.send('Runtime.enable');
  return session;
}

async function waitPopupReady(session) {
  return await waitUntil(async () => {
    const state = await popupSnapshot(session);
    return state.conversation === KEY && state.bindDisabled === false && state.manualDisabled === false ? state : false;
  }, 'REAL_PROFILE_POPUP_CONTEXT_NOT_READY', 12000);
}

async function bindAndEnableManual(session, chat, label) {
  await cdpEvaluate(session, `(()=>{document.getElementById('bindConversation')?.click();return true})()`, `${label}_BIND_CLICK`);
  await waitUntil(async () => await cdpEvaluate(session, `document.getElementById('status')?.textContent==='Диалог привязан.'`, `${label}_BIND_STATUS`), `${label}_BIND_FAIL`);
  console.log(`${label}_BIND_PASS`);

  await cdpEvaluate(session, `(()=>{document.getElementById('manualMode')?.click();return true})()`, `${label}_MANUAL_CLICK`);
  await waitUntil(async () => await cdpEvaluate(session, `document.getElementById('status')?.textContent==='Ручной режим включён.'`, `${label}_MANUAL_STATUS`), `${label}_MANUAL_ON_FAIL`);
  await waitUntil(async () => await chat.evaluate(() => document.querySelector('#ymb-external-action-surface')?.shadowRoot?.querySelectorAll('.ymb-action').length === 1), `${label}_ACTION_SURFACE_FAIL`);
  console.log(`${label}_MANUAL_ON_PASS`);
}

async function runScenario({ label, visibleUrl, canonicalUrl = '', lateInstall, expectRecovered }) {
  let browser = null;
  let control = null;
  let popupSession = null;
  try {
    browser = await puppeteer.launch({
      executablePath: chromePath,
      headless: false,
      userDataDir: fs.mkdtempSync(path.join(os.tmpdir(), `ymb-real-profile-${label.toLowerCase()}-`)),
      ignoreDefaultArgs: ['--disable-extensions'],
      args: ['--no-sandbox', '--disable-gpu', '--no-proxy-server', '--disable-background-networking']
    });
    control = await browser.target().createCDPSession();
    await control.send('Target.setDiscoverTargets', { discover: true });

    const pages = await browser.pages();
    const chat = pages[0] || await browser.newPage();
    await chat.setRequestInterception(true);
    chat.on('request', (req) => {
      if (req.isNavigationRequest() && req.url().startsWith('https://chatgpt.com/')) {
        void req.respond({ status: 200, contentType: 'text/html; charset=utf-8', body: fixture(canonicalUrl) });
        return;
      }
      void req.abort();
    });

    let extensionId = '';
    if (!lateInstall) {
      const loaded = await withTimeout(control.send('Extensions.loadUnpacked', { path: path.resolve(extensionRoot) }), 15000, `${label}_LOAD_UNPACKED_EARLY`);
      extensionId = loaded?.id || '';
      assert(Boolean(extensionId), `${label}_EXTENSION_ID_MISSING_EARLY`);
      console.log(`${label}_EXTENSION_LOADED_BEFORE_CHAT_PASS`);
    }

    await chat.goto(visibleUrl, { waitUntil: 'domcontentloaded', timeout: 20000 });
    await chat.bringToFront();
    const marker = await chat.evaluate(() => {
      const value = `${Date.now()}-${Math.random()}`;
      document.documentElement.dataset.ymbRealProfileMarker = value;
      return value;
    });
    console.log(`${label}_CHAT_OPEN_PASS`);

    if (lateInstall) {
      const loaded = await withTimeout(control.send('Extensions.loadUnpacked', { path: path.resolve(extensionRoot) }), 15000, `${label}_LOAD_UNPACKED_LATE`);
      extensionId = loaded?.id || '';
      assert(Boolean(extensionId), `${label}_EXTENSION_ID_MISSING_LATE`);
      console.log(`${label}_LATE_EXTENSION_INSTALL_PASS`);
    } else {
      // Declarative content script startup is asynchronous relative to DOMContentLoaded.
      await delay(500);
    }

    const installed = await control.send('Extensions.getExtensions');
    const extensionInfo = (installed?.extensions || []).find((row) => row.id === extensionId);
    assert(extensionInfo?.enabled === true, `${label}_EXTENSION_NOT_ENABLED`);

    const pageState = await chat.evaluate((expected) => ({ url: location.href, marker: document.documentElement.dataset.ymbRealProfileMarker || '', expected }), marker);
    assert(pageState.url === visibleUrl && pageState.marker === marker, `${label}_CHAT_PAGE_CHANGED_BEFORE_ACTION ${JSON.stringify(pageState)}`);

    const tabTarget = await findTabTarget(control, visibleUrl);
    popupSession = await openNativePopup(control, extensionId, tabTarget.targetId);
    console.log(`${label}_NATIVE_ACTION_POPUP_OPEN_PASS`);

    const bootstrapState = await waitUntil(async () => {
      const state = await popupSnapshot(popupSession);
      return state.bootstrapError || state.bootstrapResult ? state : false;
    }, `${label}_BOOTSTRAP_OUTCOME_TIMEOUT`, 12000);
    console.log(`${label}_BOOTSTRAP_STATE ${JSON.stringify(bootstrapState)}`);
    assert(!bootstrapState.bootstrapError, `${label}_BOOTSTRAP_ERROR ${JSON.stringify(bootstrapState)}`);
    assert(bootstrapState.bootstrapResult?.attempted === true, `${label}_BOOTSTRAP_NOT_ATTEMPTED`);
    assert(bootstrapState.bootstrapResult?.recovered === expectRecovered, `${label}_RECOVERED_MISMATCH ${JSON.stringify(bootstrapState)}`);

    const ready = await waitPopupReady(popupSession);
    console.log(`${label}_POPUP_READY_STATE ${JSON.stringify(ready)}`);
    assert(ready.conversation === KEY, `${label}_WRONG_CONVERSATION_KEY ${ready.conversation}`);
    assert(ready.bindDisabled === false, `${label}_BIND_DISABLED`);
    assert(ready.manualDisabled === false, `${label}_MANUAL_DISABLED`);
    console.log(`${label}_IDENTITY_AND_CONTROLS_PASS`);

    await bindAndEnableManual(popupSession, chat, label);

    const finalPage = await chat.evaluate((expected) => ({ url: location.href, marker: document.documentElement.dataset.ymbRealProfileMarker || '', expected }), marker);
    assert(finalPage.url === visibleUrl && finalPage.marker === marker, `${label}_CHAT_PAGE_CHANGED ${JSON.stringify(finalPage)}`);
    console.log(`${label}_CHAT_DOM_STABLE_PASS`);
  } finally {
    if (popupSession) await popupSession.detach().catch(() => {});
    if (control) await control.detach().catch(() => {});
    if (browser) await browser.close().catch(() => {});
  }
}

await runScenario({
  label: 'REAL_ID_LATE_INSTALL',
  visibleUrl: DIRECT_URL,
  canonicalUrl: '',
  lateInstall: true,
  expectRecovered: true
});

await runScenario({
  label: 'CANONICAL_LIVE_RECEIVER',
  visibleUrl: PROJECT_URL,
  canonicalUrl: DIRECT_URL,
  lateInstall: false,
  expectRecovered: false
});

console.log('REAL_PROFILE_BINDING_BROWSER_GATE_PASS');
console.log('REAL_YANDEX_REQUESTS=0');
