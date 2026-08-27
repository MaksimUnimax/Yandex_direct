import assert from 'node:assert/strict';
import fs from 'node:fs';
import https from 'node:https';
import os from 'node:os';
import path from 'node:path';
import { Buffer } from 'node:buffer';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer';

const here = path.dirname(fileURLToPath(import.meta.url));
const extensionRoot = fs.realpathSync(path.resolve(here, '../../../src'));
const keyPath = path.resolve(here, 'qa-chatgpt-local.key.pem');
const certPath = path.resolve(here, 'qa-chatgpt-local.cert.pem');
const CID1 = '99999999-8888-4777-8666-555555555555';
const CID2 = '77777777-6666-4555-8444-333333333333';
const PROJECT_URL = `https://chatgpt.com/g/g-p-example-project/project-name/c/${CID1}`;
const SECOND_URL = `https://chatgpt.com/c/${CID2}`;
const KEY1 = `https://chatgpt.com|${CID1}`;
const SEARCH_COMMAND = 'SEARCH_API_V1\n{"method":"search","queryText":"controlled browser query"}';
const SEARCH_XML = `<?xml version="1.0" encoding="UTF-8"?><yandexsearch><response><results><grouping><group><doc><url>https://example.test/browser</url><domain>example.test</domain><title>Controlled browser result</title><passages><passage>browser <hlword>fixture</hlword></passage></passages><modtime>20260824T100000</modtime></doc></group></grouping></results></response></yandexsearch>`;
const SEARCH_RAW = Buffer.from(SEARCH_XML, 'utf8').toString('base64');
const providerHits = [];

function fixtureHtml(conversationId) {
  const baselineId = `baseline-${conversationId}`;
  return `<!doctype html><html><head><meta charset="utf-8"><title>Phase2 Stage4 compat</title><style>
  body{font-family:Arial,sans-serif;margin:20px}.turn{margin:12px 0}.codewrap{position:relative;display:inline-block;min-width:420px}pre{padding:18px;background:#eee}.composer{position:fixed;bottom:20px;left:20px;right:20px;background:white;padding:10px;border:1px solid #aaa}#prompt-textarea{width:75%;height:72px}
  </style></head><body>
  <main id="conversation-root"><div class="turn" data-message-author-role="assistant" data-message-id="${baselineId}"><div class="codewrap"><pre data-testid="code-block"><code>controlled baseline block</code></pre><button id="native-copy" aria-label="Copy" type="button">Copy</button></div></div></main>
  <div class="composer"><textarea id="prompt-textarea"></textarea><button id="composer-submit-button" data-testid="send-button" aria-label="Send" type="button">Send</button><button id="voice" aria-label="Voice" type="button" hidden>Voice</button><button id="stop" data-testid="stop-button" aria-label="Stop" type="button" hidden>Stop</button></div>
  <script>
    window.__fixture={sendHistory:[],sendCycles:0,copyClicks:0,appended:[]};
    const textarea=document.getElementById('prompt-textarea');const send=document.getElementById('composer-submit-button');const mic=document.getElementById('voice');const stop=document.getElementById('stop');
    document.getElementById('native-copy').addEventListener('click',()=>window.__fixture.copyClicks+=1);
    window.__fixture.appendAssistant=(text,id)=>{const turn=document.createElement('div');turn.className='turn';turn.dataset.messageAuthorRole='assistant';turn.dataset.messageId=id;const wrap=document.createElement('div');wrap.className='codewrap';const pre=document.createElement('pre');pre.dataset.testid='code-block';const code=document.createElement('code');code.textContent=text;pre.appendChild(code);wrap.appendChild(pre);turn.appendChild(wrap);document.getElementById('conversation-root').appendChild(turn);window.__fixture.appended.push({id,text});};
    send.addEventListener('click',()=>{const text=textarea.value;window.__fixture.sendHistory.push(text);window.__fixture.sendCycles+=1;textarea.value='';textarea.dispatchEvent(new Event('input',{bubbles:true}));send.disabled=true;send.hidden=true;stop.hidden=false;setTimeout(()=>{stop.hidden=true;mic.hidden=false;},350);setTimeout(()=>{mic.hidden=true;send.hidden=false;send.disabled=false;},900);});
  </script></body></html>`;
}

const server=https.createServer({key:fs.readFileSync(keyPath),cert:fs.readFileSync(certPath)},(req,res)=>{
  const host=String(req.headers.host||'').split(':')[0].toLowerCase();
  if(host==='searchapi.api.cloud.yandex.net'){
    const chunks=[];req.on('data',(chunk)=>chunks.push(chunk));req.on('end',()=>{
      providerHits.push({url:req.url,method:req.method,headers:req.headers,body:Buffer.concat(chunks).toString('utf8'),remote:req.socket.remoteAddress});
      res.writeHead(200,{'content-type':'application/json; charset=utf-8'});res.end(JSON.stringify({rawData:SEARCH_RAW}));
    });return;
  }
  const match=String(req.url||'').match(/\/c\/([0-9a-f-]{36})(?:$|[/?#])/i);const cid=match?.[1]||CID1;
  res.writeHead(200,{'content-type':'text/html; charset=utf-8'});res.end(fixtureHtml(cid));
});

const delay=(ms)=>new Promise((resolve)=>setTimeout(resolve,ms));
async function waitUntil(fn,message,timeout=25000,interval=120){const started=Date.now();let last;while(Date.now()-started<timeout){try{last=await fn();if(last)return last;}catch(error){last=error;}await delay(interval);}throw new Error(`${message}; last=${last instanceof Error?last.message:JSON.stringify(last)}`);}
async function runtimeSend(page,message){return page.evaluate((payload)=>new Promise((resolve)=>chrome.runtime.sendMessage(payload,(response)=>resolve({response:response||null,error:chrome.runtime.lastError?.message||null}))),message).then(({response,error})=>{if(error)throw new Error(error);return response;});}
async function tabRuntimeSend(worker,tabId,message){return worker.evaluate(async({tabId,message})=>{const rows=await chrome.scripting.executeScript({target:{tabId},world:'ISOLATED',func:(payload)=>new Promise((resolve)=>chrome.runtime.sendMessage(payload,(response)=>resolve({response:response||null,error:chrome.runtime.lastError?.message||null}))),args:[message]});return rows?.[0]?.result||null;},{tabId,message});}
async function getState(page,key=KEY1){const r=await runtimeSend(page,{type:'WS_GET_STATE',conversation_key:key});if(!r?.ok||!r.state)throw new Error(`STATE_FAIL ${JSON.stringify(r)}`);return r.state;}
async function applyManual(worker,tabId,enabled){return worker.evaluate(async({tabId,key,enabled})=>new Promise((resolve)=>chrome.tabs.sendMessage(tabId,{type:'WS_APPLY_MANUAL_MODE',conversation_key:key,enabled,active_service:'search'},(response)=>resolve({response:response||null,error:chrome.runtime.lastError?.message||null}))),{tabId,key:KEY1,enabled});}
async function actionState(page){return page.evaluate(()=>{const buttons=[...(document.querySelector('#ymb-external-action-surface')?.shadowRoot?.querySelectorAll('.ymb-action')||[])];return{count:buttons.length,labels:buttons.map((button)=>button.textContent||''),disabled:buttons.map((button)=>Boolean(button.disabled))};});}
async function fixtureState(page){return page.evaluate(()=>({sendHistory:[...(window.__fixture?.sendHistory||[])],sendCycles:Number(window.__fixture?.sendCycles||0),copyClicks:Number(window.__fixture?.copyClicks||0),composer:document.getElementById('prompt-textarea')?.value||''}));}
async function waitRun(page,status){return waitUntil(async()=>{const state=await getState(page);return state.auto_run?.status===status?state:false;},`RUN_NOT_${status}`);}

await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(8443,'127.0.0.1',resolve);});
let browser;
try{
  browser=await puppeteer.launch({headless:false,pipe:true,enableExtensions:true,protocolTimeout:30000,userDataDir:fs.mkdtempSync(path.join(os.tmpdir(),'ymb-phase2-stage4-compat-')),args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--no-proxy-server','--ignore-certificate-errors','--disable-background-networking','--disable-features=DnsOverHttps',`--disable-extensions-except=${extensionRoot}`,`--load-extension=${extensionRoot}`,'--host-resolver-rules=MAP chatgpt.com 127.0.0.1:8443, MAP chat.openai.com 127.0.0.1:8443, MAP searchapi.api.cloud.yandex.net 127.0.0.1:8443, EXCLUDE localhost']});
  const pages=await browser.pages();const fixture=pages[0]||await browser.newPage();await fixture.bringToFront();await fixture.goto(PROJECT_URL,{waitUntil:'domcontentloaded',timeout:20000});
  const swTarget=await browser.waitForTarget((target)=>target.type()==='service_worker'&&target.url().startsWith('chrome-extension://'),{timeout:15000});const worker=await swTarget.worker();assert.ok(worker,'MV3 worker missing');
  const extensionId=new URL(swTarget.url()).host;const identity=await worker.evaluate(async(expectedUrl)=>{const tabs=await chrome.tabs.query({});const tab=tabs.find((item)=>item.url===expectedUrl);if(!tab)return null;return new Promise((resolve)=>chrome.tabs.sendMessage(tab.id,{type:'WS_GET_IDENTITY'},(response)=>resolve({tabId:tab.id,response:response||null,error:chrome.runtime.lastError?.message||null})));},PROJECT_URL);
  assert.equal(identity?.response?.ok,true,`B01_IDENTITY_FAIL ${JSON.stringify(identity)}`);assert.equal(identity.response.conversation_key,KEY1);const ownerTabId=identity.tabId;console.log('B01_PROJECT_WORK_IDENTITY_PASS');

  const extensionPage=await browser.newPage();await extensionPage.goto(`chrome-extension://${extensionId}/popup.html`,{waitUntil:'load'});await extensionPage.waitForSelector('#saveSettingsTop',{timeout:15000});
  const bind=await runtimeSend(extensionPage,{type:'WS_BIND_CONVERSATION',tab_id:ownerTabId});assert.equal(bind?.ok,true,`B01_BIND_FAIL ${JSON.stringify(bind)}`);await waitUntil(async()=>(await getState(extensionPage)).binding,'B01_BINDING_NOT_PERSISTED');console.log('B01_BINDING_PASS');

  const credential=await runtimeSend(extensionPage,{type:'YMB_SAVE_SERVICE_CREDENTIAL',service:'search',credential:{api_key:'qa-browser-key',folder_id:'qa-browser-folder'}});assert.equal(credential?.ok,true);await worker.evaluate(async()=>{if(typeof globalThis.saveSearchPolicy==='function'){await globalThis.saveSearchPolicy({manual_enabled:true,autorun_enabled:true,max_requests_per_run:5,max_cost_rub_per_run:5});return;}const policy=globalThis.YMBPolicyModel.normalizeSearchPolicy({manual_enabled:true,autorun_enabled:true,max_requests_per_run:5,max_cost_rub_per_run:5});await chrome.storage.local.set({ymb_search_policy:policy});});assert.equal((await runtimeSend(extensionPage,{type:'WS_SAVE_SERVICE_CONTEXT',conversation_key:KEY1,active_service:'search',tab_id:ownerTabId}))?.ok,true);await worker.evaluate(async()=>chrome.storage.local.set({wsmb_auto_send:true,ymb_debug_mode:true}));let state=await getState(extensionPage);assert.equal(state.service_context?.active_service,'search');assert.equal(state.search_policy?.manual_enabled,true);assert.equal(state.search_policy?.autorun_enabled,true);console.log('BROWSER_STEP_SEARCH_SETTINGS_PASS');

  const beforeManualProvider=providerHits.length;const manualOn=await runtimeSend(extensionPage,{type:'WS_SET_MANUAL_MODE',conversation_key:KEY1,enabled:true,tab_id:ownerTabId});assert.equal(manualOn?.ok,true);const appliedOn=await applyManual(worker,ownerTabId,true);assert.equal(appliedOn?.error,null);assert.equal(appliedOn?.response?.ok,true);await waitUntil(async()=>{const s=await actionState(fixture);return s.count===1&&s.labels[0]==='Яндекс';},'B02_ACTION_NOT_ARMED');assert.equal(providerHits.length,beforeManualProvider);await fixture.evaluate(()=>document.getElementById('native-copy')?.click());assert.equal((await fixtureState(fixture)).copyClicks,1);assert.equal(providerHits.length,beforeManualProvider);console.log('BROWSER_STEP_NATIVE_COPY_PASS');
  await fixture.evaluate(()=>{const pre=document.querySelector('pre');pre.appendChild(document.createElement('span')).textContent=' mutation';document.body.dataset.qaMutation=String(Date.now());});await delay(2200);assert.equal((await actionState(fixture)).count,1);assert.equal((await getState(extensionPage)).manual_mode,true);assert.equal(providerHits.length,beforeManualProvider);console.log('B02_MANUAL_RESYNC_SINGLE_ACTION_PASS');
  await fixture.reload({waitUntil:'domcontentloaded',timeout:20000});await waitUntil(async()=>{const s=await actionState(fixture);return s.count===1&&s.labels[0]==='Яндекс';},'B02_REMOUNT_ACTION_NOT_RESTORED');assert.equal(providerHits.length,beforeManualProvider);assert.equal((await getState(extensionPage)).manual_mode,true);console.log('B02_MANUAL_REMOUNT_NO_REPLAY_PASS');
  const manualOff=await runtimeSend(extensionPage,{type:'WS_SET_MANUAL_MODE',conversation_key:KEY1,enabled:false,tab_id:ownerTabId});assert.equal(manualOff?.ok,true);const appliedOff=await applyManual(worker,ownerTabId,false);assert.equal(appliedOff?.response?.ok,true);await waitUntil(async()=>(await actionState(fixture)).count===0,'B02_ACTION_NOT_REMOVED');assert.equal(providerHits.length,beforeManualProvider);console.log('B02_MANUAL_ON_OFF_TRANSACTION_PASS');

  const started=await runtimeSend(extensionPage,{type:'WS_START_AUTORUN',conversation_key:KEY1,tab_id:ownerTabId});assert.equal(started?.ok,true,`B03_START_FAIL ${JSON.stringify(started)}`);state=await waitRun(extensionPage,'waiting_command');assert.equal(state.auto_run.active_service,'search');await waitUntil(async()=>(await fixtureState(fixture)).sendHistory.some((text)=>String(text).includes('Yandex Search')),'B03_START_PROMPT_NOT_SENT');console.log('BROWSER_STEP_AUTORUN_START_PASS');
  const beforeSearch=providerHits.length;await fixture.evaluate((command)=>window.__fixture.appendAssistant(command,'search-compat-turn'),SEARCH_COMMAND);await waitUntil(async()=>providerHits.length===beforeSearch+1,'B03_PROVIDER_NOT_CALLED');await waitUntil(async()=>(await fixtureState(fixture)).sendHistory.some((text)=>String(text).startsWith('SEARCH_RESULT_V1')),'B03_RESULT_NOT_DELIVERED');state=await waitUntil(async()=>{const s=await getState(extensionPage);return s.auto_run?.status==='waiting_command'&&Number(s.auto_run?.requests_executed)===1?s:false;},'B03_RUN_NOT_RETURNED');assert.equal(providerHits.length,beforeSearch+1);const hit=providerHits.at(-1);assert.equal(hit.method,'POST');assert.equal(hit.url,'/v2/web/search');assert.ok(String(hit.headers.authorization||'').startsWith('Api-Key qa-browser-key'));const body=JSON.parse(hit.body);assert.equal(body.folderId,'qa-browser-folder');assert.equal(body.responseFormat,'FORMAT_XML');assert.equal(body.query?.queryText,'controlled browser query');assert.ok(String(hit.remote||'').includes('127.0.0.1')||String(hit.remote||'').includes('::ffff:127.0.0.1'));console.log('BROWSER_STEP_SEARCH_DELIVERY_PASS');

  const paused=await runtimeSend(extensionPage,{type:'WS_PAUSE_AUTORUN',conversation_key:KEY1,tab_id:ownerTabId});assert.equal(paused?.ok,true);await waitRun(extensionPage,'paused');const second=await browser.newPage();await second.bringToFront();await second.goto(SECOND_URL,{waitUntil:'domcontentloaded',timeout:20000});const secondIdentity=await worker.evaluate(async(expectedUrl)=>{const tabs=await chrome.tabs.query({});const tab=tabs.find((item)=>item.url===expectedUrl);if(!tab)return null;return new Promise((resolve)=>chrome.tabs.sendMessage(tab.id,{type:'WS_GET_IDENTITY'},(response)=>resolve({tabId:tab.id,response:response||null,error:chrome.runtime.lastError?.message||null})));},SECOND_URL);assert.equal(secondIdentity?.response?.ok,true);const foreignResume=await tabRuntimeSend(worker,secondIdentity.tabId,{type:'WS_RESUME_AUTORUN',conversation_key:KEY1,tab_id:secondIdentity.tabId});assert.equal(foreignResume?.error,null);assert.notEqual(foreignResume?.response?.ok,true,'B03_NON_OWNER_RESUME_WAS_ACCEPTED');assert.equal((await getState(extensionPage)).auto_run?.status,'paused');await second.close();console.log('B03_NON_OWNER_CONTROL_FENCE_PASS');
  const resumed=await runtimeSend(extensionPage,{type:'WS_RESUME_AUTORUN',conversation_key:KEY1,tab_id:ownerTabId});assert.equal(resumed?.ok,true);await waitRun(extensionPage,'waiting_command');const finished=await runtimeSend(extensionPage,{type:'WS_FINISH_AUTORUN',conversation_key:KEY1,tab_id:ownerTabId});assert.equal(finished?.ok,true);state=await waitRun(extensionPage,'stopped');assert.equal(state.auto_run.active_service,'search');assert.equal(providerHits.length,beforeSearch+1);console.log('B03_SEARCH_AUTORUN_PASS');

  const safe=JSON.stringify(providerHits.map((row)=>({url:row.url,method:row.method,body:row.body})));assert.equal(safe.includes('qa-browser-key'),false);assert.equal(providerHits.length,beforeSearch+1);console.log(`BROWSER_CONTROLLED_SEARCH_STUB_REQUESTS=${providerHits.length-beforeManualProvider}`);console.log('BROWSER_GATE_REAL_YANDEX_REQUESTS=0');console.log('PHASE2_STAGE4_COMPAT_BROWSER_GATE_PASS');
}finally{if(browser)await browser.close().catch(()=>{});await new Promise((resolve)=>server.close(resolve));}
