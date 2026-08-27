import assert from 'node:assert/strict';
import fs from 'node:fs';
import https from 'node:https';
import os from 'node:os';
import path from 'node:path';
import { Buffer } from 'node:buffer';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer';

const here = path.dirname(fileURLToPath(import.meta.url));
const extensionRoot = fs.realpathSync(path.resolve(here, '../../src'));
const keyPath = path.resolve(here, 'phase2-stage4/qa-chatgpt-local.key.pem');
const certPath = path.resolve(here, 'phase2-stage4/qa-chatgpt-local.cert.pem');
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

function fixtureHtml() {
  return `<!doctype html><html><head><meta charset="utf-8"><title>Phase2 Stage4 worker compat</title><style>
  body{font-family:Arial,sans-serif;margin:20px}.turn{margin:12px 0}.codewrap{position:relative;display:inline-block;min-width:420px}pre{padding:18px;background:#eee}.composer{position:fixed;bottom:20px;left:20px;right:20px;background:white;padding:10px;border:1px solid #aaa}#prompt-textarea{width:75%;height:72px}
  </style></head><body><main id="conversation-root">
  <div class="turn" data-message-author-role="assistant" data-message-id="baseline"><div class="codewrap"><pre data-testid="code-block"><code>controlled baseline block</code></pre><button id="native-copy" aria-label="Copy" type="button">Copy</button></div></div>
  </main><div class="composer"><textarea id="prompt-textarea"></textarea><button id="composer-submit-button" data-testid="send-button" aria-label="Send" type="button">Send</button><button id="voice" aria-label="Voice" type="button" hidden>Voice</button><button id="stop" data-testid="stop-button" aria-label="Stop" type="button" hidden>Stop</button></div>
  <script>
    window.__fixture={sendHistory:[],copyClicks:0,sendCycles:0,appended:[]};
    const textarea=document.getElementById('prompt-textarea');const send=document.getElementById('composer-submit-button');const mic=document.getElementById('voice');const stop=document.getElementById('stop');
    document.getElementById('native-copy').addEventListener('click',()=>window.__fixture.copyClicks+=1);
    window.__fixture.appendAssistant=(text,id)=>{const turn=document.createElement('div');turn.className='turn';turn.dataset.messageAuthorRole='assistant';turn.dataset.messageId=id;const pre=document.createElement('pre');pre.dataset.testid='code-block';const code=document.createElement('code');code.textContent=text;pre.appendChild(code);turn.appendChild(pre);document.getElementById('conversation-root').appendChild(turn);window.__fixture.appended.push({id,text});};
    send.addEventListener('click',()=>{const text=textarea.value;window.__fixture.sendHistory.push(text);window.__fixture.sendCycles+=1;textarea.value='';textarea.dispatchEvent(new Event('input',{bubbles:true}));send.disabled=true;send.hidden=true;stop.hidden=false;setTimeout(()=>{stop.hidden=true;mic.hidden=false;},300);setTimeout(()=>{mic.hidden=true;send.hidden=false;send.disabled=false;},750);});
  </script></body></html>`;
}

const server = https.createServer({ key: fs.readFileSync(keyPath), cert: fs.readFileSync(certPath) }, (req, res) => {
  const host = String(req.headers.host || '').split(':')[0].toLowerCase();
  if (host === 'searchapi.api.cloud.yandex.net') {
    const chunks = [];
    req.on('data', (chunk) => chunks.push(chunk));
    req.on('end', () => {
      providerHits.push({ method:req.method, url:req.url, headers:req.headers, body:Buffer.concat(chunks).toString('utf8'), remote:req.socket.remoteAddress });
      res.writeHead(200, { 'content-type':'application/json; charset=utf-8' });
      res.end(JSON.stringify({ rawData: SEARCH_RAW }));
    });
    return;
  }
  res.writeHead(200, { 'content-type':'text/html; charset=utf-8' });
  res.end(fixtureHtml());
});

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
async function waitUntil(fn, message, timeout=25000, interval=120) {
  const started=Date.now(); let last;
  while (Date.now()-started<timeout) { try { last=await fn(); if (last) return last; } catch (error) { last=error; } await delay(interval); }
  throw new Error(`${message}; last=${last instanceof Error?last.message:JSON.stringify(last)}`);
}
async function runtimeSend(page, message) {
  return page.evaluate((payload)=>new Promise((resolve)=>chrome.runtime.sendMessage(payload,(response)=>resolve({response:response||null,error:chrome.runtime.lastError?.message||null}))),message)
    .then(({response,error})=>{if(error)throw new Error(error);return response;});
}
async function getState(page, key) {
  const r=await runtimeSend(page,{type:'WS_GET_STATE',conversation_key:key});
  if(!r?.ok||!r.state)throw new Error(`STATE_FAIL ${JSON.stringify(r)}`);
  return r.state;
}
async function applyManual(worker, tabId, key, enabled, service) {
  return worker.evaluate(async({tabId,key,enabled,service})=>new Promise((resolve)=>chrome.tabs.sendMessage(tabId,{type:'WS_APPLY_MANUAL_MODE',conversation_key:key,enabled,active_service:service},(response)=>resolve({response:response||null,error:chrome.runtime.lastError?.message||null}))),{tabId,key,enabled,service});
}
async function actionCount(page){return page.evaluate(()=>document.querySelector('#ymb-external-action-surface')?.shadowRoot?.querySelectorAll('.ymb-action').length||0);}
async function actionLabels(page){return page.evaluate(()=>[...(document.querySelector('#ymb-external-action-surface')?.shadowRoot?.querySelectorAll('.ymb-action')||[])].map((x)=>x.textContent));}
async function fixtureState(page){return page.evaluate(()=>({sendHistory:[...(window.__fixture?.sendHistory||[])],copyClicks:Number(window.__fixture?.copyClicks||0),sendCycles:Number(window.__fixture?.sendCycles||0)}));}

await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(8443,'127.0.0.1',resolve);});
let browser;
try {
  browser=await puppeteer.launch({headless:false,pipe:true,enableExtensions:true,protocolTimeout:30000,userDataDir:fs.mkdtempSync(path.join(os.tmpdir(),'ymb-phase2-stage4-worker-')),args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--no-proxy-server','--ignore-certificate-errors','--disable-background-networking','--disable-features=DnsOverHttps',`--disable-extensions-except=${extensionRoot}`,`--load-extension=${extensionRoot}`,'--host-resolver-rules=MAP chatgpt.com 127.0.0.1:8443, MAP chat.openai.com 127.0.0.1:8443, MAP searchapi.api.cloud.yandex.net 127.0.0.1:8443, EXCLUDE localhost']});
  const pages=await browser.pages(); const fixture=pages[0]||await browser.newPage(); await fixture.bringToFront(); await fixture.goto(PROJECT_URL,{waitUntil:'domcontentloaded',timeout:20000});
  const swTarget=await browser.waitForTarget((t)=>t.type()==='service_worker'&&t.url().startsWith('chrome-extension://'),{timeout:15000}); const worker=await swTarget.worker(); assert.ok(worker);
  const extensionId=new URL(swTarget.url()).host; const control=await browser.newPage(); await control.goto(`chrome-extension://${extensionId}/popup.html`,{waitUntil:'load'});
  const identity=await worker.evaluate(async(expectedUrl)=>{const tabs=await chrome.tabs.query({});const tab=tabs.find((x)=>x.url===expectedUrl);if(!tab)return null;return new Promise((resolve)=>chrome.tabs.sendMessage(tab.id,{type:'WS_GET_IDENTITY'},(response)=>resolve({tabId:tab.id,response:response||null,error:chrome.runtime.lastError?.message||null})));},PROJECT_URL);
  assert.equal(identity?.response?.ok,true,`B01_IDENTITY_FAIL ${JSON.stringify(identity)}`); assert.equal(identity.response.conversation_key,KEY1); const tabId=identity.tabId;

  const bind=await runtimeSend(control,{type:'WS_BIND_CONVERSATION',tab_id:tabId}); assert.equal(bind?.ok,true,`B01_BIND_FAIL ${JSON.stringify(bind)}`);
  const cred=await runtimeSend(control,{type:'YMB_SAVE_SERVICE_CREDENTIAL',service:'search',credential:{api_key:'qa-browser-key',folder_id:'qa-browser-folder'}}); assert.equal(cred?.ok,true,`B01_SEARCH_CREDENTIAL_FAIL ${JSON.stringify(cred)}`);
  const saved=await runtimeSend(control,{type:'WS_SAVE_SETTINGS',conversation_key:KEY1,tab_id:tabId,active_service:'search',auto_send:true,debug_mode:true,wordstat_policy:{autorun_enabled:false,manual_enabled:true,max_requests_per_run:100,max_cost_rub_per_run:10},search_policy:{autorun_enabled:true,manual_enabled:true,allowed_methods:['search'],max_requests_per_run:5,max_cost_rub_per_run:5,method_cost_rub:{search:0.488},tariff_checked_at:new Date().toISOString(),tariff_source:'qa-controlled'}}); assert.equal(saved?.ok,true,`B01_SETTINGS_FAIL ${JSON.stringify(saved)}`);
  let state=await getState(control,KEY1); assert.equal(state.binding,true); assert.equal(state.service_context?.active_service,'search'); assert.equal(state.search_policy?.manual_enabled,true); assert.equal(state.search_policy?.autorun_enabled,true); assert.equal(state.credential_status?.search?.has_api_key,true); assert.equal(state.credential_status?.search?.folder_id,'qa-browser-folder');
  console.log('B01_PROJECT_WORK_PASS'); console.log('BROWSER_STEP_SEARCH_SETTINGS_PASS');

  const beforeProvider=providerHits.length;
  const manualOn=await runtimeSend(control,{type:'WS_SET_MANUAL_MODE',conversation_key:KEY1,enabled:true,tab_id:tabId}); assert.equal(manualOn?.ok,true); const appliedOn=await applyManual(worker,tabId,KEY1,true,'search'); assert.equal(appliedOn?.response?.ok,true); assert.equal(appliedOn?.response?.applied,true);
  await waitUntil(async()=>await actionCount(fixture)===1,'B02_ACTION_NOT_ARMED'); assert.deepEqual(await actionLabels(fixture),['Яндекс']); assert.equal(providerHits.length,beforeProvider);
  await fixture.evaluate(()=>document.getElementById('native-copy')?.click()); assert.equal((await fixtureState(fixture)).copyClicks,1); assert.equal(providerHits.length,beforeProvider);
  await fixture.evaluate(()=>{const p=document.querySelector('pre');p.appendChild(document.createElement('span')).textContent=' mutation';document.body.dataset.qaMutation=String(Date.now());}); await delay(1800); state=await getState(control,KEY1); assert.equal(state.manual_mode,true); assert.equal(await actionCount(fixture),1);
  const manualOff=await runtimeSend(control,{type:'WS_SET_MANUAL_MODE',conversation_key:KEY1,enabled:false,tab_id:tabId}); assert.equal(manualOff?.ok,true); const appliedOff=await applyManual(worker,tabId,KEY1,false,'search'); assert.equal(appliedOff?.response?.ok,true); await waitUntil(async()=>await actionCount(fixture)===0,'B02_ACTION_NOT_REMOVED');
  const manualOn2=await runtimeSend(control,{type:'WS_SET_MANUAL_MODE',conversation_key:KEY1,enabled:true,tab_id:tabId}); assert.equal(manualOn2?.ok,true); const appliedOn2=await applyManual(worker,tabId,KEY1,true,'search'); assert.equal(appliedOn2?.response?.ok,true); await waitUntil(async()=>await actionCount(fixture)===1,'B02_ACTION_NOT_REARMED'); await delay(1200); assert.equal(providerHits.length,beforeProvider);
  console.log('B02_MANUAL_ON_TRANSACTION_PASS');

  await runtimeSend(control,{type:'WS_SET_MANUAL_MODE',conversation_key:KEY1,enabled:false,tab_id:tabId}); await applyManual(worker,tabId,KEY1,false,'search'); await waitUntil(async()=>await actionCount(fixture)===0,'B03_MANUAL_NOT_OFF');
  const started=await runtimeSend(control,{type:'WS_START_AUTORUN',conversation_key:KEY1,tab_id:tabId}); assert.equal(started?.ok,true,`B03_START_FAIL ${JSON.stringify(started)}`); await waitUntil(async()=>(await getState(control,KEY1)).auto_run?.status==='waiting_command','B03_RUN_NOT_WAITING');
  await waitUntil(async()=>(await fixtureState(fixture)).sendHistory.length>=1,'B03_START_PROMPT_NOT_SENT'); assert.match((await fixtureState(fixture)).sendHistory[0],/Yandex Search/i);
  await fixture.evaluate((cmd)=>window.__fixture.appendAssistant(cmd,'search-turn-1'),SEARCH_COMMAND); await waitUntil(async()=>providerHits.length===beforeProvider+1,'B03_PROVIDER_NOT_CALLED'); await waitUntil(async()=>(await fixtureState(fixture)).sendHistory.some((x)=>String(x).startsWith('SEARCH_RESULT_V1')),'B03_RESULT_NOT_DELIVERED');
  state=await waitUntil(async()=>{const s=await getState(control,KEY1);return s.auto_run?.status==='waiting_command'&&Number(s.auto_run?.requests_executed)===1?s:false;},'B03_NOT_RETURNED_WAITING'); assert.equal(providerHits.length,beforeProvider+1);
  const hit=providerHits.at(-1); assert.equal(hit.method,'POST'); assert.equal(hit.url,'/v2/web/search'); assert.ok(String(hit.headers.authorization||'').startsWith('Api-Key qa-browser-key')); const reqBody=JSON.parse(hit.body); assert.equal(reqBody.folderId,'qa-browser-folder'); assert.equal(reqBody.responseFormat,'FORMAT_XML'); assert.equal(reqBody.query?.queryText,'controlled browser query');
  const paused=await runtimeSend(control,{type:'WS_PAUSE_AUTORUN',conversation_key:KEY1,tab_id:tabId}); assert.equal(paused?.ok,true); await waitUntil(async()=>(await getState(control,KEY1)).auto_run?.status==='paused','B03_PAUSE_FAIL');
  const second=await browser.newPage(); await second.goto(SECOND_URL,{waitUntil:'domcontentloaded',timeout:20000}); const secondIdentity=await worker.evaluate(async(expectedUrl)=>{const tabs=await chrome.tabs.query({});const tab=tabs.find((x)=>x.url===expectedUrl);if(!tab)return null;return new Promise((resolve)=>chrome.tabs.sendMessage(tab.id,{type:'WS_GET_IDENTITY'},(response)=>resolve({tabId:tab.id,response:response||null,error:chrome.runtime.lastError?.message||null})));},SECOND_URL); assert.equal(secondIdentity?.response?.conversation_key,KEY2); const secondState=await getState(control,KEY2); assert.ok(!secondState.auto_run||['stopped','error'].includes(secondState.auto_run.status)); assert.equal((await getState(control,KEY1)).auto_run?.status,'paused'); await second.close();
  const resumed=await runtimeSend(control,{type:'WS_RESUME_AUTORUN',conversation_key:KEY1,tab_id:tabId}); assert.equal(resumed?.ok,true); await waitUntil(async()=>(await getState(control,KEY1)).auto_run?.status==='waiting_command','B03_RESUME_FAIL'); const finished=await runtimeSend(control,{type:'WS_FINISH_AUTORUN',conversation_key:KEY1,tab_id:tabId}); assert.equal(finished?.ok,true); await waitUntil(async()=>(await getState(control,KEY1)).auto_run?.status==='stopped','B03_FINISH_FAIL'); assert.equal(providerHits.length,beforeProvider+1);
  console.log('B03_SEARCH_AUTORUN_PASS'); console.log(`BROWSER_CONTROLLED_SEARCH_STUB_REQUESTS=${providerHits.length-beforeProvider}`); console.log('BROWSER_GATE_REAL_YANDEX_REQUESTS=0'); console.log('PHASE2_STAGE4_WORKER_COMPAT_PASS');
} finally {
  if(browser)await browser.close().catch(()=>{});
  await new Promise((resolve)=>server.close(resolve));
}
