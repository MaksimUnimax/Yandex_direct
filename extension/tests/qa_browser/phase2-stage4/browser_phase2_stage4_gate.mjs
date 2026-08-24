import fs from 'node:fs';
import https from 'node:https';
import os from 'node:os';
import path from 'node:path';
import process from 'node:process';
import { Buffer } from 'node:buffer';
import puppeteer from 'puppeteer-core';

const [chromePath, extensionRoot, keyPath, certPath] = process.argv.slice(2);
if (!chromePath || !extensionRoot || !keyPath || !certPath) {
  throw new Error('usage: browser_phase2_stage4_gate.mjs <chrome> <extension-root> <tls-key> <tls-cert>');
}
for (const p of [chromePath, extensionRoot, keyPath, certPath]) {
  if (!fs.existsSync(p)) throw new Error(`HARNESS_INPUT_MISSING ${p}`);
}

const CID1 = '99999999-8888-4777-8666-555555555555';
const CID2 = '77777777-6666-4555-8444-333333333333';
const PROJECT_URL = `https://chatgpt.com/g/g-p-example-project/project-name/c/${CID1}`;
const SECOND_URL = `https://chatgpt.com/c/${CID2}`;
const KEY1 = `https://chatgpt.com|${CID1}`;
const KEY2 = `https://chatgpt.com|${CID2}`;
const SEARCH_COMMAND = 'SEARCH_API_V1\n{"method":"search","queryText":"controlled browser query"}';
const SEARCH_XML = `<?xml version="1.0" encoding="UTF-8"?><yandexsearch><response><results><grouping><group><doc><url>https://example.test/browser</url><domain>example.test</domain><title>Controlled browser result</title><passages><passage>browser <hlword>fixture</hlword></passage></passages><modtime>20260824T100000</modtime></doc></group></grouping></results></response></yandexsearch>`;
const SEARCH_RAW = Buffer.from(SEARCH_XML, 'utf8').toString('base64');

const providerHits = [];
const chatHits = [];
function fixtureHtml(conversationId) {
  const baselineId = `baseline-${conversationId}`;
  return `<!doctype html><html><head><meta charset="utf-8"><title>Controlled ChatGPT Fixture</title><style>
  body{font-family:Arial,sans-serif;margin:20px}.turn{margin:12px 0}.codewrap{position:relative;display:inline-block;min-width:420px}pre{padding:18px;background:#eee}.composer{position:fixed;bottom:20px;left:20px;right:20px;background:white;padding:10px;border:1px solid #aaa}#prompt-textarea{width:75%;height:72px}
  </style></head><body>
  <main id="conversation-root">
    <div class="turn" data-message-author-role="assistant" data-message-id="${baselineId}">
      <div class="codewrap"><pre data-testid="code-block"><code>controlled baseline block</code></pre><button id="native-copy" aria-label="Copy" type="button">Copy</button></div>
    </div>
  </main>
  <div class="composer"><textarea id="prompt-textarea"></textarea><button id="composer-submit-button" data-testid="send-button" aria-label="Send" type="button">Send</button><button id="voice" aria-label="Voice" type="button" hidden>Voice</button><button id="stop" data-testid="stop-button" aria-label="Stop" type="button" hidden>Stop</button></div>
  <script>
    window.__fixture = { sendHistory: [], copyClicks: 0, appended: [], sendCycles: 0 };
    const textarea = document.getElementById('prompt-textarea');
    const send = document.getElementById('composer-submit-button');
    const mic = document.getElementById('voice');
    const stop = document.getElementById('stop');
    document.getElementById('native-copy').addEventListener('click', () => { window.__fixture.copyClicks += 1; });
    window.__fixture.appendAssistant = (text, id) => {
      const turn = document.createElement('div'); turn.className='turn'; turn.dataset.messageAuthorRole='assistant'; turn.dataset.messageId=id;
      const pre = document.createElement('pre'); pre.dataset.testid='code-block'; const code=document.createElement('code'); code.textContent=text; pre.appendChild(code); turn.appendChild(pre);
      document.getElementById('conversation-root').appendChild(turn); window.__fixture.appended.push({id,text}); return id;
    };
    send.addEventListener('click', () => {
      const text = textarea.value; window.__fixture.sendHistory.push(text); window.__fixture.sendCycles += 1;
      textarea.value=''; textarea.dispatchEvent(new Event('input',{bubbles:true}));
      send.disabled=true; send.hidden=true; mic.hidden=true; stop.hidden=false;
      setTimeout(() => { stop.hidden=true; mic.hidden=false; }, 650);
      setTimeout(() => { mic.hidden=true; send.hidden=false; send.disabled=false; }, 1650);
    });
  </script>
  </body></html>`;
}

const server = https.createServer({ key: fs.readFileSync(keyPath), cert: fs.readFileSync(certPath) }, (req, res) => {
  const host = String(req.headers.host || '').split(':')[0].toLowerCase();
  if (host === 'searchapi.api.cloud.yandex.net') {
    const chunks = [];
    req.on('data', c => chunks.push(c));
    req.on('end', () => {
      providerHits.push({ host, method: req.method, url: req.url, headers: req.headers, body: Buffer.concat(chunks).toString('utf8'), remote: req.socket.remoteAddress });
      res.writeHead(200, { 'content-type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify({ rawData: SEARCH_RAW }));
    });
    return;
  }
  chatHits.push({ host, method: req.method, url: req.url, remote: req.socket.remoteAddress });
  const match = String(req.url || '').match(/\/c\/([0-9a-f-]{36})(?:$|[/?#])/i);
  const cid = match?.[1] || CID1;
  res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
  res.end(fixtureHtml(cid));
});
await new Promise((resolve, reject) => { server.once('error', reject); server.listen(8443, '127.0.0.1', resolve); });

const delay = ms => new Promise(r => setTimeout(r, ms));
function assert(condition, message) { if (!condition) throw new Error(message); }
async function waitUntil(fn, message, timeout = 15000, interval = 120) {
  const started = Date.now(); let last;
  while (Date.now() - started < timeout) {
    try { last = await fn(); if (last) return last; } catch (e) { last = e; }
    await delay(interval);
  }
  throw new Error(`${message}; last=${last instanceof Error ? last.message : JSON.stringify(last)}`);
}
async function runtimeSend(popup, message) {
  return await popup.evaluate((msg) => new Promise((resolve) => {
    chrome.runtime.sendMessage(msg, (response) => resolve({ response: response || null, error: chrome.runtime.lastError?.message || null }));
  }), message).then(({response,error}) => { if (error) throw new Error(error); return response; });
}
async function getState(popup, key) {
  const r = await runtimeSend(popup, { type:'WS_GET_STATE', conversation_key:key });
  if (!r?.ok || !r.state) throw new Error(`STATE_FAIL ${JSON.stringify(r)}`);
  return r.state;
}
async function openPopup(worker, browser, key) {
  const tab = await worker.evaluate(async () => await chrome.tabs.create({ url: chrome.runtime.getURL('popup.html'), active:false }));
  assert(tab?.id, 'POPUP_TAB_CREATE_FAIL');
  const target = await browser.waitForTarget(t => t.url().startsWith('chrome-extension://') && t.url().endsWith('/popup.html'), { timeout:10000 });
  const popup = await target.page(); assert(popup, 'POPUP_PAGE_FAIL');
  await popup.waitForFunction(expected => document.getElementById('conversationMeta')?.textContent === expected, { timeout:10000 }, key);
  return { popup, tabId:tab.id };
}
async function closePopup(worker, tabId) { try { await worker.evaluate(async id => { try { await chrome.tabs.remove(id); } catch {} }, tabId); } catch {} await delay(180); }
async function popupClick(popup, selector) {
  return await popup.evaluate(sel => {
    const el = document.querySelector(sel);
    if (!el) throw new Error(`POPUP_ELEMENT_MISSING ${sel}`);
    if (el.disabled) throw new Error(`POPUP_ELEMENT_DISABLED ${sel}`);
    el.click();
    return true;
  }, selector);
}
async function popupSelect(popup, id, value) {
  return await popup.evaluate(({id, value}) => {
    const el = document.getElementById(id);
    if (!el) throw new Error(`POPUP_ELEMENT_MISSING #${id}`);
    if (el.disabled) throw new Error(`POPUP_ELEMENT_DISABLED #${id}`);
    el.value = String(value);
    el.dispatchEvent(new Event('change', { bubbles:true }));
    return el.value;
  }, { id, value });
}
async function setFormValue(popup, id, value) {
  await popup.evaluate(({id, value}) => {
    const el = document.getElementById(id);
    if (!el) throw new Error(`POPUP_ELEMENT_MISSING #${id}`);
    const proto = Object.getPrototypeOf(el);
    const desc = Object.getOwnPropertyDescriptor(proto, 'value');
    if (desc?.set) desc.set.call(el, String(value)); else el.value = String(value);
    el.dispatchEvent(new Event('input',{bubbles:true}));
  }, { id, value });
}
async function setCheckedNoEvent(popup, id, checked) {
  await popup.evaluate(({id, checked}) => {
    const el = document.getElementById(id);
    if (!el) throw new Error(`POPUP_ELEMENT_MISSING #${id}`);
    el.checked = Boolean(checked);
  }, { id, checked });
}
async function popupChecked(popup, id) { return await popup.evaluate(id => Boolean(document.getElementById(id)?.checked), id); }
async function popupText(popup, id) { return await popup.evaluate(id => document.getElementById(id)?.textContent || '', id); }
async function actionCount(page) { return await page.evaluate(() => document.querySelector('#ymb-external-action-surface')?.shadowRoot?.querySelectorAll('.ymb-action').length || 0); }
async function actionLabels(page) { return await page.evaluate(() => [...(document.querySelector('#ymb-external-action-surface')?.shadowRoot?.querySelectorAll('.ymb-action') || [])].map(x=>x.textContent)); }
async function fixtureState(page) { return await page.evaluate(() => structuredClone(window.__fixture)); }

let browser;
try {
  browser = await puppeteer.launch({
    executablePath: chromePath,
    headless: false,
    protocolTimeout: 30000,
    userDataDir: fs.mkdtempSync(path.join(os.tmpdir(), 'ymb-stage4-browser-')),
    args: [
      '--no-sandbox','--disable-gpu','--no-proxy-server','--ignore-certificate-errors','--disable-background-networking','--disable-features=DnsOverHttps',
      `--disable-extensions-except=${extensionRoot}`, `--load-extension=${extensionRoot}`,
      '--host-resolver-rules=MAP chatgpt.com 127.0.0.1:8443, MAP chat.openai.com 127.0.0.1:8443, MAP searchapi.api.cloud.yandex.net 127.0.0.1:8443, EXCLUDE localhost'
    ]
  });
  const pages = await browser.pages();
  const fixture = pages[0] || await browser.newPage();
  await fixture.bringToFront();
  await fixture.goto(PROJECT_URL, { waitUntil:'domcontentloaded', timeout:20000 });
  const swTarget = await browser.waitForTarget(t => t.type()==='service_worker' && t.url().startsWith('chrome-extension://'), { timeout:15000 });
  const worker = await swTarget.worker(); assert(worker, 'MV3_WORKER_CONTEXT_FAIL');

  const identity = await worker.evaluate(async expectedUrl => {
    const tabs=await chrome.tabs.query({}); const tab=tabs.find(x=>x.url===expectedUrl); if(!tab)return null;
    return await new Promise(resolve=>chrome.tabs.sendMessage(tab.id,{type:'WS_GET_IDENTITY'},r=>resolve({tabId:tab.id,response:r||null,error:chrome.runtime.lastError?.message||null})));
  }, PROJECT_URL);
  assert(identity?.response?.ok === true, `B01_IDENTITY_FAIL ${JSON.stringify(identity)}`);
  assert(identity.response.conversation_key === KEY1, `B01_KEY_FAIL ${JSON.stringify(identity.response)}`);
  let p = await openPopup(worker,browser,KEY1);
  const b01 = await p.popup.evaluate(() => ({
    conversation:document.getElementById('conversationMeta')?.textContent||'', activeServiceDisabled:!!document.getElementById('activeService')?.disabled,
    bindDisabled:!!document.getElementById('bindConversation')?.disabled, manualDisabled:!!document.getElementById('manualMode')?.disabled
  }));
  assert(b01.conversation===KEY1 && !b01.activeServiceDisabled && !b01.bindDisabled, `B01_POPUP_FAIL ${JSON.stringify(b01)}`);
  console.log('B01_PROJECT_WORK_PASS');

  await popupClick(p.popup,'#bindConversation');
  await waitUntil(async()=> (await getState(p.popup,KEY1)).binding, 'BINDING_NOT_PERSISTED');
  console.log('BROWSER_STEP_BIND_PASS');
  await popupSelect(p.popup,'activeService','search');
  await setCheckedNoEvent(p.popup,'searchManualEnabled',true);
  await setCheckedNoEvent(p.popup,'searchAutorunEnabled',true);
  await setCheckedNoEvent(p.popup,'autoSend',true);
  await setFormValue(p.popup,'apiKey','qa-browser-key');
  await setFormValue(p.popup,'folderId','qa-browser-folder');
  await setFormValue(p.popup,'searchMaxRequestsRun','5');
  await setFormValue(p.popup,'searchMaxCostRun','5');
  await popupClick(p.popup,'#saveSettings');
  await waitUntil(async()=> { const s=await getState(p.popup,KEY1); return s.service_context?.active_service==='search' && s.search_policy?.manual_enabled===true && s.search_policy?.autorun_enabled===true && s.has_api_key===true; }, 'SEARCH_SETTINGS_NOT_SAVED');
  console.log('BROWSER_STEP_SEARCH_SETTINGS_PASS');

  let st = await getState(p.popup,KEY1); assert(st.manual_mode===false,'B02_INITIAL_WORKER_MANUAL_NOT_OFF');
  const beforeProvider = providerHits.length;
  await popupClick(p.popup,'#manualMode');
  await waitUntil(async()=> (await getState(p.popup,KEY1)).manual_mode===true, 'B02_WORKER_NOT_ON');
  await waitUntil(async()=> (await actionCount(fixture))===1, 'B02_ACTION_NOT_ARMED');
  assert((await actionLabels(fixture))[0]==='Яндекс','B02_ACTION_LABEL_FAIL');
  assert(providerHits.length===beforeProvider,'B02_PROVIDER_CALLED_ON_ARM');
  console.log('BROWSER_STEP_MANUAL_FIRST_ON_PASS');
  await fixture.evaluate(() => document.getElementById('native-copy')?.click());
  assert((await fixtureState(fixture)).copyClicks===1,'B02_NATIVE_COPY_FAIL');
  assert(providerHits.length===beforeProvider,'B02_NATIVE_COPY_DISPATCHED_PROVIDER');
  await fixture.evaluate(()=>{ const p=document.querySelector('pre'); p.appendChild(document.createElement('span')).textContent=' mutation'; document.body.dataset.qaMutation=String(Date.now()); });
  await delay(2400);
  assert((await getState(p.popup,KEY1)).manual_mode===true,'B02_WORKER_SELF_REVERT');
  assert((await actionCount(fixture))===1,'B02_ACTION_DUPLICATE_OR_LOST_AFTER_RESYNC');
  const oldPopupId=p.tabId; await closePopup(worker,oldPopupId); p=await openPopup(worker,browser,KEY1);
  assert(await popupChecked(p.popup,'manualMode')===true,'B02_POPUP_REOPEN_NOT_ON');
  assert((await actionCount(fixture))===1,'B02_ACTION_LOST_AFTER_POPUP_REOPEN');
  await popupClick(p.popup,'#manualMode');
  await waitUntil(async()=> (await getState(p.popup,KEY1)).manual_mode===false,'B02_WORKER_NOT_OFF');
  await waitUntil(async()=> (await actionCount(fixture))===0,'B02_ACTION_NOT_REMOVED_OFF');
  await popupClick(p.popup,'#manualMode');
  await waitUntil(async()=> (await getState(p.popup,KEY1)).manual_mode===true,'B02_SECOND_ON_WORKER_FAIL');
  await waitUntil(async()=> (await actionCount(fixture))===1,'B02_SECOND_ON_ACTION_FAIL');
  await delay(2200);
  assert((await getState(p.popup,KEY1)).manual_mode===true && (await actionCount(fixture))===1,'B02_SECOND_ON_NOT_STABLE');
  assert(providerHits.length===beforeProvider,'B02_REAL_PROVIDER_CALL_DETECTED');
  console.log('B02_MANUAL_ON_TRANSACTION_PASS');

  await popupClick(p.popup,'#manualMode');
  await waitUntil(async()=> (await getState(p.popup,KEY1)).manual_mode===false,'B03_MANUAL_OFF_PRECONDITION_FAIL');
  p.popup.on('dialog', async d => { try { await d.accept(); } catch {} });
  await popupClick(p.popup,'#startAuto');
  await waitUntil(async()=> { const s=await getState(p.popup,KEY1); return s.auto_run?.status==='waiting_command' ? s : null; }, 'B03_RUN_NOT_WAITING_COMMAND', 20000);
  console.log('BROWSER_STEP_AUTORUN_START_PASS');
  let fx = await fixtureState(fixture);
  assert(fx.sendHistory.length>=1 && fx.sendHistory[0].includes('Yandex Search'), `B03_START_PROMPT_NOT_SENT ${JSON.stringify(fx.sendHistory)}`);
  await fixture.evaluate((cmd)=>window.__fixture.appendAssistant(cmd,'search-turn-1'), SEARCH_COMMAND);
  await waitUntil(async()=> providerHits.length===beforeProvider+1, 'B03_PROVIDER_NOT_CALLED', 20000);
  await waitUntil(async()=> { const f=await fixtureState(fixture); return f.sendHistory.some(x=>String(x).startsWith('SEARCH_RESULT_V1')) ? f : null; }, 'B03_RESULT_NOT_DELIVERED', 20000);
  st = await waitUntil(async()=> { const s=await getState(p.popup,KEY1); return s.auto_run?.status==='waiting_command' && Number(s.auto_run?.requests_executed)===1 ? s : null; }, 'B03_RUN_NOT_RETURNED_TO_WAITING', 25000);
  assert(providerHits.length===beforeProvider+1, `B03_PROVIDER_DUPLICATE ${providerHits.length-beforeProvider}`);
  const hit=providerHits.at(-1); assert(hit.method==='POST' && hit.url==='/v2/web/search','B03_PROVIDER_SHAPE_FAIL');
  assert(String(hit.headers.authorization||'').startsWith('Api-Key qa-browser-key'),'B03_AUTH_HEADER_FAIL');
  const reqBody=JSON.parse(hit.body); assert(reqBody.folderId==='qa-browser-folder' && reqBody.responseFormat==='FORMAT_XML' && reqBody.query?.queryText==='controlled browser query','B03_REQUEST_BODY_FAIL');
  assert(String(hit.remote||'').includes('127.0.0.1') || String(hit.remote||'').includes('::ffff:127.0.0.1'),'B03_PROVIDER_NOT_LOOPBACK');
  console.log('BROWSER_STEP_SEARCH_DELIVERY_PASS');

  await closePopup(worker,p.tabId); p=await openPopup(worker,browser,KEY1);
  await waitUntil(async()=> await popupText(p.popup,'runStatus')==='waiting_command','B03_POPUP_REOPEN_RUN_TRUTH_FAIL');
  p.popup.on('dialog', async d => { try { await d.accept(); } catch {} });
  await popupClick(p.popup,'#pauseAuto');
  await waitUntil(async()=> (await getState(p.popup,KEY1)).auto_run?.status==='paused','B03_PAUSE_FAIL');

  const second = await browser.newPage(); await second.bringToFront(); await second.goto(SECOND_URL,{waitUntil:'domcontentloaded',timeout:20000});
  const p2=await openPopup(worker,browser,KEY2);
  const secondControls=await p2.popup.evaluate(()=>({run:document.getElementById('runStatus')?.textContent||'',pause:!!document.getElementById('pauseAuto')?.disabled,resume:!!document.getElementById('resumeAuto')?.disabled,finish:!!document.getElementById('finishAuto')?.disabled}));
  assert(secondControls.run==='—' && secondControls.pause && secondControls.resume && secondControls.finish,`B03_NON_OWNER_POPUP_CONTROL_FAIL ${JSON.stringify(secondControls)}`);
  await closePopup(worker,p2.tabId); await second.close(); await fixture.bringToFront();
  await closePopup(worker,p.tabId); p=await openPopup(worker,browser,KEY1); p.popup.on('dialog', async d=>{try{await d.accept();}catch{}});
  assert((await getState(p.popup,KEY1)).auto_run?.status==='paused','B03_OWNER_RUN_CHANGED_BY_SECOND_TAB');
  await popupClick(p.popup,'#resumeAuto');
  await waitUntil(async()=> (await getState(p.popup,KEY1)).auto_run?.status==='waiting_command','B03_RESUME_FAIL');
  await popupClick(p.popup,'#finishAuto');
  await waitUntil(async()=> ['stopped','error'].includes((await getState(p.popup,KEY1)).auto_run?.status),'B03_FINISH_FAIL');
  st=await getState(p.popup,KEY1); assert(st.auto_run?.status==='stopped',`B03_FINISH_STATUS ${st.auto_run?.status}`);
  assert(providerHits.length===beforeProvider+1,'B03_PROVIDER_CALLED_MORE_THAN_ONCE');
  console.log('B03_SEARCH_AUTORUN_PASS');
  console.log(`BROWSER_CONTROLLED_SEARCH_STUB_REQUESTS=${providerHits.length-beforeProvider}`);
  console.log('BROWSER_GATE_REAL_YANDEX_REQUESTS=0');
  console.log('PHASE2_STAGE4_BROWSER_GATE_PASS');
} finally {
  if (browser) await browser.close().catch(()=>{});
  await new Promise(resolve=>server.close(resolve));
}
