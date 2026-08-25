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
    'TARGET_ATTACH'
  );
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
    if (message.error) {
      slot.reject(new Error(`${message.error.message || 'CDP_CHILD_ERROR'} (${message.error.code ?? 'no-code'})`));
    } else {
      slot.resolve(message.result || {});
    }
  };
  control.on('Target.receivedMessageFromTarget', onMessage);

  return {
    async send(method, params = {}) {
      const id = nextId++;
      const response = new Promise((resolve, reject) => pending.set(id, { resolve, reject }));
      try {
        await withTimeout(control.send('Target.sendMessageToTarget', {
          sessionId,
          message:JSON.stringify({ id, method, params })
        }), 5000, `CHILD_SEND_${method}`);
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
      status:document.getElementById('status')?.textContent||'',
      statusLevel:document.getElementById('status')?.dataset?.level||'',
      bootstrapError:globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_ERROR__||'',
      bootstrapResult:globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_RESULT__||null,
      popupRuntimePresent:Boolean(document.querySelector('script[data-ymb-popup-runtime="true"]')),
      activeTabs,
      activeTabError
    });
  })()`, 'POPUP_SNAPSHOT');
  return JSON.parse(json || '{}');
}

async function waitForPopupBootstrapOutcome(session, timeout = 10000) {
  const started = Date.now();
  let last = null;
  while (Date.now() - started < timeout) {
    last = await popupSnapshot(session);
    if (last.bootstrapError || last.bootstrapResult) return last;
    await delay(100);
  }
  throw new Error(`POPUP_BOOTSTRAP_OUTCOME_TIMEOUT state=${JSON.stringify(last)}`);
}

let browser;
let control = null;
let popupSession = null;
try {
  browser = await puppeteer.launch({
    executablePath:chromePath,
    headless:false,
    userDataDir:fs.mkdtempSync(path.join(os.tmpdir(), 'ymb-context-recovery-')),
    ignoreDefaultArgs:['--disable-extensions'],
    args:[
      '--no-sandbox', '--disable-gpu', '--no-proxy-server', '--disable-background-networking'
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
  console.log('CONTEXT_RECOVERY_CHATGPT_OPEN_BEFORE_EXTENSION_PASS');

  control = await browser.target().createCDPSession();
  await control.send('Target.setDiscoverTargets', { discover:true });

  const chatTarget = await waitUntil(async () => {
    const result = await control.send('Target.getTargets');
    return (result?.targetInfos || []).find((info) => info.type === 'page' && info.url === CHAT_URL) || false;
  }, 'CHATGPT_CDP_TARGET_NOT_FOUND');
  console.log(`CONTEXT_RECOVERY_CHATGPT_TARGET_PASS ${chatTarget.targetId}`);

  const loaded = await withTimeout(
    control.send('Extensions.loadUnpacked', { path:path.resolve(extensionRoot) }),
    15000,
    'EXTENSIONS_LOAD_UNPACKED'
  );
  const extensionId = loaded?.id || '';
  assert(Boolean(extensionId), 'EXTENSIONS_LOAD_UNPACKED_ID_MISSING');
  const extensionOrigin = `chrome-extension://${extensionId}/`;
  const popupUrl = `${extensionOrigin}popup.html`;
  console.log(`CONTEXT_RECOVERY_LATE_UNPACKED_INSTALL_PASS ${extensionId}`);

  const installed = await control.send('Extensions.getExtensions');
  const extensionInfo = (installed?.extensions || []).find((row) => row.id === extensionId);
  assert(extensionInfo?.enabled === true, `EXTENSION_NOT_ENABLED ${JSON.stringify(extensionInfo || null)}`);

  const pageAfterInstall = await chat.evaluate((expected) => ({
    url:location.href,
    marker:document.documentElement.dataset.ymbRecoveryMarker || '',
    expected
  }), documentMarker);
  assert(pageAfterInstall.url === CHAT_URL && pageAfterInstall.marker === documentMarker, `CHAT_PAGE_RELOADED_DURING_EXTENSION_INSTALL ${JSON.stringify(pageAfterInstall)}`);
  console.log('CONTEXT_RECOVERY_CHAT_PAGE_REMAINED_OPEN_PASS');

  await chat.bringToFront();
  const targetsBeforeAction = await control.send('Target.getTargets');
  const beforeIds = new Set((targetsBeforeAction?.targetInfos || []).map((info) => info.targetId));

  await withTimeout(
    control.send('Extensions.triggerAction', { id:extensionId, targetId:chatTarget.targetId }),
    10000,
    'EXTENSIONS_TRIGGER_ACTION'
  );
  console.log('CONTEXT_RECOVERY_NATIVE_ACTION_TRIGGER_PASS');

  const popupTarget = await waitUntil(async () => {
    const result = await control.send('Target.getTargets');
    return (result?.targetInfos || []).find((info) =>
      info.url === popupUrl && (!beforeIds.has(info.targetId) || info.type === 'page' || info.type === 'other')
    ) || false;
  }, 'NATIVE_POPUP_CDP_TARGET_NOT_FOUND', 15000, 80);
  console.log(`CONTEXT_RECOVERY_NATIVE_ACTION_POPUP_OPEN_PASS ${popupTarget.targetId}`);

  popupSession = await createNestedTargetSession(control, popupTarget.targetId);
  await popupSession.send('Runtime.enable');

  const recoveredState = await waitForPopupBootstrapOutcome(popupSession, 12000);
  console.log(`CONTEXT_RECOVERY_POPUP_BOOTSTRAP_STATE ${JSON.stringify(recoveredState)}`);
  assert(recoveredState.runtimeId === extensionId, `POPUP_RUNTIME_ID_MISMATCH ${JSON.stringify(recoveredState)}`);
  assert(!recoveredState.bootstrapError, `POPUP_BOOTSTRAP_ERROR ${JSON.stringify(recoveredState)}`);
  assert(recoveredState.bootstrapResult?.attempted === true, `POPUP_RECOVERY_NOT_ATTEMPTED ${JSON.stringify(recoveredState)}`);
  assert(recoveredState.bootstrapResult?.recovered === true, `POPUP_MISSING_RECEIVER_BRANCH_NOT_RECOVERED ${JSON.stringify(recoveredState)}`);
  assert(recoveredState.activeTabs?.length === 1 && recoveredState.activeTabs[0].url === CHAT_URL, `POPUP_ACTIVE_TAB_NOT_CHATGPT ${JSON.stringify(recoveredState)}`);
  assert(recoveredState.bootstrapResult?.tab_id === recoveredState.activeTabs[0].id, `POPUP_RECOVERY_WRONG_TAB ${JSON.stringify(recoveredState)}`);
  console.log('CONTEXT_RECOVERY_MISSING_RECEIVER_REPRODUCED_PASS');

  const readyState = await waitUntil(async () => {
    const state = await popupSnapshot(popupSession);
    return state.conversation === KEY && state.bindDisabled === false && state.manualDisabled === false ? state : false;
  }, 'POPUP_CONTEXT_SELF_RECOVERY_UI_FAIL', 12000);
  console.log(`CONTEXT_RECOVERY_POPUP_READY_STATE ${JSON.stringify(readyState)}`);
  console.log('POPUP_CONTEXT_SELF_RECOVERY_PASS');

  await cdpEvaluate(popupSession, `(()=>{document.getElementById('bindConversation')?.click();return true})()`, 'POPUP_BIND_CLICK');
  await waitUntil(async () => await cdpEvaluate(
    popupSession,
    `document.getElementById('status')?.textContent==='Диалог привязан.'`,
    'POPUP_BIND_STATUS'
  ), 'RECOVERY_BIND_ACTION_FAIL');
  console.log('CONTEXT_RECOVERY_BIND_PASS');

  await cdpEvaluate(popupSession, `(()=>{document.getElementById('manualMode')?.click();return true})()`, 'POPUP_MANUAL_CLICK');
  await waitUntil(async () => await cdpEvaluate(
    popupSession,
    `document.getElementById('status')?.textContent==='Ручной режим включён.'`,
    'POPUP_MANUAL_STATUS'
  ), 'RECOVERY_MANUAL_ON_FAIL');
  await waitUntil(async () => await chat.evaluate(() =>
    document.querySelector('#ymb-external-action-surface')?.shadowRoot?.querySelectorAll('.ymb-action').length === 1
  ), 'RECOVERY_MANUAL_ACTION_SURFACE_FAIL');
  console.log('CONTEXT_RECOVERY_MANUAL_ON_PASS');

  const finalPage = await chat.evaluate((expected) => ({
    url:location.href,
    marker:document.documentElement.dataset.ymbRecoveryMarker || '',
    expected
  }), documentMarker);
  assert(finalPage.url === CHAT_URL && finalPage.marker === documentMarker, `CHAT_PAGE_CHANGED_DURING_RECOVERY ${JSON.stringify(finalPage)}`);
  console.log('CONTEXT_RECOVERY_ALREADY_OPEN_CHATGPT_PASS');
  console.log('REAL_YANDEX_REQUESTS=0');
} finally {
  if (popupSession) await popupSession.detach().catch(() => {});
  if (control) await control.detach().catch(() => {});
  if (browser) await browser.close().catch(() => {});
}
