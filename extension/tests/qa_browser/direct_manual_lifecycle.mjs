import assert from 'node:assert/strict';
import fs from 'node:fs';
import https from 'node:https';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer';

const here = path.dirname(fileURLToPath(import.meta.url));
const extensionRoot = fs.realpathSync(path.resolve(here, '../../src'));
const keyPath = path.resolve(here, 'phase2-stage4/qa-chatgpt-local.key.pem');
const certPath = path.resolve(here, 'phase2-stage4/qa-chatgpt-local.cert.pem');
const CID = '99999999-8888-4777-8666-555555555555';
const PROJECT_URL = `https://chatgpt.com/g/g-p-example-project/project-name/c/${CID}`;
const KEY = `https://chatgpt.com|${CID}`;
const LIST_COMMAND = 'DIRECT_API_V1\n{"method":"listCampaigns","campaignIds":[77],"limit":10}';
const REPORT_COMMAND = 'DIRECT_API_V1\n{"method":"getCampaignPerformance","dateFrom":"2026-08-01","dateTo":"2026-08-01","campaignIds":[77],"limit":10}';

const providerHits = [];
function fixtureHtml() {
  return `<!doctype html><html><head><meta charset="utf-8"><title>Direct lifecycle fixture</title><style>
  body{font-family:Arial,sans-serif;margin:20px}.turn{margin:12px 0}.codewrap{position:relative;display:inline-block;min-width:420px}pre{padding:18px;background:#eee}.composer{position:fixed;bottom:20px;left:20px;right:20px;background:white;padding:10px;border:1px solid #aaa}#prompt-textarea{width:75%;height:72px}
  </style></head><body>
  <main id="conversation-root"></main>
  <div class="composer"><textarea id="prompt-textarea"></textarea><button id="composer-submit-button" data-testid="send-button" aria-label="Send" type="button">Send</button><button id="voice" aria-label="Voice" type="button" hidden>Voice</button><button id="stop" data-testid="stop-button" aria-label="Stop" type="button" hidden>Stop</button></div>
  <script>
    window.__fixture = { sendHistory: [], copyClicks: 0, appended: [], sendCycles: 0 };
    const textarea = document.getElementById('prompt-textarea');
    const send = document.getElementById('composer-submit-button');
    const mic = document.getElementById('voice');
    const stop = document.getElementById('stop');
    window.__fixture.appendAssistant = (text, id) => {
      const turn = document.createElement('div'); turn.className='turn'; turn.dataset.messageAuthorRole='assistant'; turn.dataset.messageId=id;
      const wrap=document.createElement('div'); wrap.className='codewrap';
      const pre = document.createElement('pre'); pre.dataset.testid='code-block'; const code=document.createElement('code'); code.textContent=text; pre.appendChild(code);
      const copy=document.createElement('button'); copy.type='button'; copy.setAttribute('aria-label','Copy'); copy.textContent='Copy'; copy.addEventListener('click',()=>{window.__fixture.copyClicks += 1;});
      wrap.appendChild(pre); wrap.appendChild(copy); turn.appendChild(wrap); document.getElementById('conversation-root').appendChild(turn);
      window.__fixture.appended.push({id,text}); return id;
    };
    send.addEventListener('click', () => {
      const text = textarea.value; window.__fixture.sendHistory.push(text); window.__fixture.sendCycles += 1;
      textarea.value=''; textarea.dispatchEvent(new Event('input',{bubbles:true}));
      send.disabled=true; send.hidden=true; mic.hidden=true; stop.hidden=false;
      setTimeout(() => { stop.hidden=true; mic.hidden=false; }, 250);
      setTimeout(() => { mic.hidden=true; send.hidden=false; send.disabled=false; }, 650);
    });
  </script></body></html>`;
}

const server = https.createServer({ key: fs.readFileSync(keyPath), cert: fs.readFileSync(certPath) }, (req, res) => {
  const host = String(req.headers.host || '').split(':')[0].toLowerCase();
  if (host === 'api.direct.yandex.com') {
    const chunks = [];
    req.on('data', (chunk) => chunks.push(chunk));
    req.on('end', () => {
      const body = Buffer.concat(chunks).toString('utf8');
      providerHits.push({ host, method: req.method, url: req.url, headers: req.headers, body, remote: req.socket.remoteAddress });
      if (req.url === '/json/v501/campaigns') {
        res.writeHead(200, { 'content-type':'application/json; charset=utf-8', RequestId:'lifecycle-list', Units:'2/98/100' });
        res.end(JSON.stringify({ result:{ Campaigns:[{ Id:77, Name:'Lifecycle campaign', StartDate:'2026-08-01', Type:'TEXT_CAMPAIGN', Status:'ACCEPTED', State:'ON', Currency:'RUB' }] } }));
        return;
      }
      if (req.url === '/json/v501/reports') {
        res.writeHead(200, { 'content-type':'text/tab-separated-values; charset=utf-8', RequestId:'lifecycle-report', Units:'3/97/100' });
        res.end('Date\tCampaignId\tCampaignName\tImpressions\tClicks\tCost\n2026-08-01\t77\tLifecycle campaign\t100\t5\t123456\n');
        return;
      }
      res.writeHead(404); res.end('not found');
    });
    return;
  }
  res.writeHead(200, { 'content-type':'text/html; charset=utf-8' });
  res.end(fixtureHtml());
});

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
async function waitUntil(fn, message, timeout = 15000, interval = 120) {
  const started = Date.now(); let last;
  while (Date.now() - started < timeout) {
    try { last = await fn(); if (last) return last; } catch (error) { last = error; }
    await delay(interval);
  }
  throw new Error(`${message}; last=${last instanceof Error ? last.message : JSON.stringify(last)}`);
}
async function runtimeSend(popup, message) {
  const result = await popup.evaluate((msg) => new Promise((resolve) => chrome.runtime.sendMessage(msg, (response) => resolve({ response:response || null, error:chrome.runtime.lastError?.message || null }))), message);
  if (result.error) throw new Error(result.error);
  return result.response;
}
async function getState(popup) {
  const response = await runtimeSend(popup, { type:'WS_GET_STATE', conversation_key:KEY });
  if (!response?.ok || !response.state) throw new Error(`STATE_FAIL ${JSON.stringify(response)}`);
  return response.state;
}
async function openPopup(worker, browser, chatTabId, chatWindowId) {
  const existingTargets = new Set(browser.targets());
  const tab = await worker.evaluate(async ({ chatTabId, chatWindowId }) => {
    await chrome.tabs.update(chatTabId, { active:true });
    try { await chrome.windows.update(chatWindowId, { focused:true }); } catch {}
    return await chrome.tabs.create({ url:chrome.runtime.getURL('popup.html'), active:false, windowId:chatWindowId });
  }, { chatTabId, chatWindowId });
  assert.ok(tab?.id, 'POPUP_TAB_CREATE_FAIL');
  const target = await browser.waitForTarget((t) => !existingTargets.has(t) && t.url().startsWith('chrome-extension://') && t.url().endsWith('/popup.html'), { timeout:10000 });
  const popup = await target.page();
  assert.ok(popup, 'POPUP_PAGE_FAIL');
  await popup.waitForFunction((expected) => document.getElementById('conversationMeta')?.textContent === expected, { timeout:10000 }, KEY);
  await waitUntil(async () => (await popup.evaluate(() => document.getElementById('status')?.textContent || '')) === 'Готово.', 'POPUP_NOT_READY', 10000);
  return { popup, tabId:tab.id };
}
async function closePopup(worker, tabId) { try { await worker.evaluate(async (id) => { try { await chrome.tabs.remove(id); } catch {} }, tabId); } catch {} await delay(150); }
async function popupClick(popup, selector) {
  await popup.evaluate((sel) => { const el=document.querySelector(sel); if(!el) throw new Error(`MISSING ${sel}`); if(el.disabled) throw new Error(`DISABLED ${sel}`); el.click(); }, selector);
}
async function popupSelect(popup, id, value) {
  await popup.evaluate(({id,value}) => { const el=document.getElementById(id); if(!el) throw new Error(`MISSING #${id}`); el.value=String(value); el.dispatchEvent(new Event('change',{bubbles:true})); }, {id,value});
}
async function setChecked(popup, id, checked) { await popup.evaluate(({id,checked}) => { const el=document.getElementById(id); if(!el) throw new Error(`MISSING #${id}`); el.checked=Boolean(checked); }, {id,checked}); }
async function waitStatus(popup, expected, message) {
  await waitUntil(async () => { const status=await popup.evaluate(() => ({text:document.getElementById('status')?.textContent||'',level:document.getElementById('status')?.dataset?.level||''})); if(status.level==='error') throw new Error(status.text); return status.text===expected; }, message);
}
async function actionCount(page) { return page.evaluate(() => document.querySelector('#ymb-external-action-surface')?.shadowRoot?.querySelectorAll('.ymb-action').length || 0); }
async function clickLatestAction(page) { return page.evaluate(() => { const buttons=[...(document.querySelector('#ymb-external-action-surface')?.shadowRoot?.querySelectorAll('.ymb-action') || [])]; const button=buttons.at(-1); if(!button) throw new Error('NO_MANUAL_ACTION'); button.click(); return buttons.length; }); }
async function fixtureState(page) { return page.evaluate(() => ({ sendHistory:[...(window.__fixture?.sendHistory||[])], copyClicks:Number(window.__fixture?.copyClicks||0), composer:document.getElementById('prompt-textarea')?.value||'', sendCycles:Number(window.__fixture?.sendCycles||0) })); }

await new Promise((resolve, reject) => { server.once('error', reject); server.listen(8443, '127.0.0.1', resolve); });
let browser;
try {
  browser = await puppeteer.launch({
    headless:false,
    pipe:true,
    enableExtensions:true,
    protocolTimeout:30000,
    userDataDir:fs.mkdtempSync(path.join(os.tmpdir(),'ymb-direct-lifecycle-')),
    args:[
      '--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--no-proxy-server','--ignore-certificate-errors','--disable-background-networking','--disable-features=DnsOverHttps',
      `--disable-extensions-except=${extensionRoot}`,`--load-extension=${extensionRoot}`,
      '--host-resolver-rules=MAP chatgpt.com 127.0.0.1:8443, MAP chat.openai.com 127.0.0.1:8443, MAP api.direct.yandex.com 127.0.0.1:8443, EXCLUDE localhost'
    ]
  });
  const pages = await browser.pages();
  const fixture = pages[0] || await browser.newPage();
  await fixture.bringToFront();
  await fixture.goto(PROJECT_URL, { waitUntil:'domcontentloaded', timeout:20000 });
  const swTarget = await browser.waitForTarget((t) => t.type()==='service_worker' && t.url().startsWith('chrome-extension://'), { timeout:15000 });
  const worker = await swTarget.worker();
  assert.ok(worker, 'MV3 worker missing');

  const identity = await worker.evaluate(async (expectedUrl) => {
    const tabs = await chrome.tabs.query({});
    const tab = tabs.find((item) => item.url === expectedUrl);
    if (!tab) return null;
    return await new Promise((resolve) => chrome.tabs.sendMessage(tab.id, { type:'WS_GET_IDENTITY' }, (response) => resolve({ tabId:tab.id, windowId:tab.windowId, response:response || null, error:chrome.runtime.lastError?.message || null })));
  }, PROJECT_URL);
  assert.equal(identity?.response?.ok, true, `IDENTITY_FAIL ${JSON.stringify(identity)}`);
  assert.equal(identity.response.conversation_key, KEY, `IDENTITY_KEY_FAIL ${JSON.stringify(identity.response)}`);
  assert.ok(Number.isInteger(identity.tabId) && Number.isInteger(identity.windowId), `IDENTITY_TAB_WINDOW_FAIL ${JSON.stringify(identity)}`);

  let p = await openPopup(worker, browser, identity.tabId, identity.windowId);
  await popupClick(p.popup, '#bindConversation');
  await waitStatus(p.popup, 'Диалог привязан.', 'BIND_FAIL');

  const geometry = await p.popup.evaluate(() => {
    const html = document.documentElement.getBoundingClientRect();
    const body = document.body.getBoundingClientRect();
    const main = document.querySelector('main');
    return {
      htmlWidth: Math.round(html.width), htmlHeight: Math.round(html.height),
      bodyWidth: Math.round(body.width), bodyHeight: Math.round(body.height),
      mainClientWidth: main?.clientWidth || 0, mainScrollWidth: main?.scrollWidth || 0,
      mainClientHeight: main?.clientHeight || 0, mainScrollHeight: main?.scrollHeight || 0
    };
  });
  assert.deepEqual([geometry.htmlWidth, geometry.htmlHeight, geometry.bodyWidth, geometry.bodyHeight], [430,560,430,560]);
  assert.ok(geometry.mainScrollWidth <= geometry.mainClientWidth, `D18_HORIZONTAL_OVERFLOW ${JSON.stringify(geometry)}`);
  assert.ok(geometry.mainScrollHeight > geometry.mainClientHeight, `D18_VERTICAL_SCROLL_NOT_NEEDED ${JSON.stringify(geometry)}`);
  console.log('D18_POPUP_430X560_PASS');

  const saveCredential = await runtimeSend(p.popup, { type:'YMB_SAVE_SERVICE_CREDENTIAL', service:'direct', credential:{ oauth_token:'lifecycle-direct-secret', client_login:'lifecycle-client' } });
  assert.equal(saveCredential?.ok, true);
  await popupSelect(p.popup, 'activeService', 'direct');
  await setChecked(p.popup, 'directManualEnabled', false);
  await setChecked(p.popup, 'autoSend', false);
  await popupClick(p.popup, '#saveSettingsTop');
  await waitStatus(p.popup, 'Общие настройки сохранены.', 'TOP_COMMON_SAVE_FAIL');
  let state = await getState(p.popup);
  assert.equal(state.service_context?.active_service, 'direct');
  assert.equal(state.direct_policy?.manual_enabled, false);

  await setChecked(p.popup, 'directManualEnabled', true);
  await popupClick(p.popup, '#saveSettings');
  await waitStatus(p.popup, 'Общие настройки сохранены.', 'BOTTOM_COMMON_SAVE_FAIL');
  state = await getState(p.popup);
  assert.equal(state.service_context?.active_service, 'direct');
  assert.equal(state.direct_policy?.manual_enabled, true);
  assert.equal(state.direct_policy?.autorun_enabled, false);
  console.log('D18_TOP_BOTTOM_COMMON_SAVE_EQUIVALENT_PASS');
  console.log('D17_DIRECT_LIFECYCLE_SETTINGS_PASS');

  await popupClick(p.popup, '#manualMode');
  await waitStatus(p.popup, 'Ручной режим включён.', 'MANUAL_ON_FAIL');
  await waitUntil(async () => (await getState(p.popup)).manual_mode === true, 'MANUAL_STATE_NOT_ON');

  await fixture.evaluate((command) => window.__fixture.appendAssistant(command, 'direct-list-turn'), LIST_COMMAND);
  await waitUntil(async () => (await actionCount(fixture)) >= 1, 'LIST_ACTION_NOT_ARMED');
  const beforeList = providerHits.length;
  await clickLatestAction(fixture);
  await waitUntil(async () => providerHits.length === beforeList + 1, 'LIST_PROVIDER_NOT_CALLED', 20000);
  await waitUntil(async () => (await fixtureState(fixture)).composer.startsWith('DIRECT_RESULT_V1'), 'LIST_RESULT_NOT_FILLED', 20000);
  let fx = await fixtureState(fixture);
  assert.equal(fx.sendHistory.length, 0);
  assert.equal(fx.sendCycles, 0);
  assert.match(fx.composer, /"operation":"listCampaigns"/);
  assert.equal(providerHits.length, beforeList + 1);
  assert.equal(providerHits.at(-1).url, '/json/v501/campaigns');
  const listBody = JSON.parse(providerHits.at(-1).body);
  assert.deepEqual(listBody.params.SelectionCriteria, { Ids:[77] });
  console.log('D17_DIRECT_MANUAL_LIST_AUTOSEND_FALSE_PASS');

  await fixture.evaluate(() => { const textarea=document.getElementById('prompt-textarea'); textarea.value=''; textarea.dispatchEvent(new Event('input',{bubbles:true})); });
  await closePopup(worker, p.tabId);
  await fixture.bringToFront();
  p = await openPopup(worker, browser, identity.tabId, identity.windowId);
  assert.equal((await getState(p.popup)).manual_mode, true);
  await setChecked(p.popup, 'autoSend', true);
  await popupClick(p.popup, '#saveSettings');
  await waitStatus(p.popup, 'Общие настройки сохранены.', 'AUTOSEND_TRUE_SAVE_FAIL');

  await fixture.evaluate((command) => window.__fixture.appendAssistant(command, 'direct-report-turn'), REPORT_COMMAND);
  await waitUntil(async () => (await actionCount(fixture)) >= 2, 'REPORT_ACTION_NOT_ARMED');
  const beforeReport = providerHits.length;
  await clickLatestAction(fixture);
  await waitUntil(async () => providerHits.length === beforeReport + 1, 'REPORT_PROVIDER_NOT_CALLED', 20000);
  await waitUntil(async () => (await fixtureState(fixture)).sendHistory.some((text) => String(text).startsWith('DIRECT_RESULT_V1')), 'REPORT_RESULT_NOT_SENT', 25000);
  fx = await fixtureState(fixture);
  assert.equal(fx.sendHistory.filter((text) => String(text).startsWith('DIRECT_RESULT_V1')).length, 1);
  assert.equal(providerHits.length, beforeReport + 1);
  assert.equal(providerHits.at(-1).url, '/json/v501/reports');
  assert.equal(String(providerHits.at(-1).headers.processingmode || ''), 'online');
  console.log('D17_DIRECT_MANUAL_REPORT_AUTOSEND_TRUE_PASS');

  const hitsBeforeRemount = providerHits.length;
  await fixture.reload({ waitUntil:'domcontentloaded', timeout:20000 });
  await delay(1800);
  assert.equal(providerHits.length, hitsBeforeRemount);
  state = await getState(p.popup);
  assert.equal(state.manual_mode, true);
  assert.equal(providerHits.length, hitsBeforeRemount);
  console.log('D17_DIRECT_REMOUNT_NO_REPLAY_PASS');

  const secretText = JSON.stringify({ providerHits:providerHits.map((hit)=>({url:hit.url,method:hit.method,body:hit.body})), state });
  assert.equal(secretText.includes('lifecycle-direct-secret'), false);
  assert.equal(providerHits.length, 2);
  console.log('D17_DIRECT_NO_DUPLICATE_PROVIDER_PASS');
  console.log('D20_DIRECT_LIFECYCLE_REAL_YANDEX_REQUESTS=0');
  console.log('PHASE5_DIRECT_MANUAL_LIFECYCLE_PASS');
} finally {
  if (browser) await browser.close().catch(() => {});
  await new Promise((resolve) => server.close(resolve));
}
