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
const DIRECT_COMMAND = 'DIRECT_API_V1\n{"method":"listCampaigns","campaignIds":[77],"limit":10}';
const providerHits = [];

function fixtureHtml() {
  return `<!doctype html><html><head><meta charset="utf-8"><title>Direct Codex Addendum v2</title><style>
  body{font-family:Arial,sans-serif;margin:20px}.turn{margin:12px 0}.codewrap{position:relative;display:inline-block;min-width:420px}pre{padding:18px;background:#eee}.composer{position:fixed;bottom:20px;left:20px;right:20px;background:white;padding:10px;border:1px solid #aaa}#prompt-textarea{width:75%;height:72px}
  </style></head><body><main id="conversation-root"></main>
  <div class="composer"><textarea id="prompt-textarea"></textarea><button id="composer-submit-button" data-testid="send-button" aria-label="Send" type="button">Send</button><button id="voice" aria-label="Voice" type="button" hidden>Voice</button><button id="stop" data-testid="stop-button" aria-label="Stop" type="button" hidden>Stop</button></div>
  <script>
    window.__fixture={sendHistory:[],sendCycles:0,appended:[]};
    const textarea=document.getElementById('prompt-textarea'); const send=document.getElementById('composer-submit-button'); const mic=document.getElementById('voice'); const stop=document.getElementById('stop');
    window.__fixture.appendAssistant=(text,id)=>{const turn=document.createElement('div');turn.className='turn';turn.dataset.messageAuthorRole='assistant';turn.dataset.messageId=id;const wrap=document.createElement('div');wrap.className='codewrap';const pre=document.createElement('pre');pre.dataset.testid='code-block';const code=document.createElement('code');code.textContent=text;pre.appendChild(code);const copy=document.createElement('button');copy.type='button';copy.setAttribute('aria-label','Copy');copy.textContent='Copy';wrap.appendChild(pre);wrap.appendChild(copy);turn.appendChild(wrap);document.getElementById('conversation-root').appendChild(turn);window.__fixture.appended.push({id,text});};
    send.addEventListener('click',()=>{const text=textarea.value;window.__fixture.sendHistory.push(text);window.__fixture.sendCycles+=1;textarea.value='';textarea.dispatchEvent(new Event('input',{bubbles:true}));send.disabled=true;send.hidden=true;stop.hidden=false;setTimeout(()=>{stop.hidden=true;mic.hidden=false;},250);setTimeout(()=>{mic.hidden=true;send.hidden=false;send.disabled=false;},700);});
  </script></body></html>`;
}

const server=https.createServer({key:fs.readFileSync(keyPath),cert:fs.readFileSync(certPath)},(req,res)=>{
  const host=String(req.headers.host||'').split(':')[0].toLowerCase();
  if(host==='api.direct.yandex.com'){
    const chunks=[]; req.on('data',(chunk)=>chunks.push(chunk)); req.on('end',()=>{
      const body=Buffer.concat(chunks).toString('utf8');
      providerHits.push({url:req.url,method:req.method,headers:req.headers,body,remote:req.socket.remoteAddress});
      setTimeout(()=>{
        if(req.url==='/json/v501/campaigns'){
          res.writeHead(200,{'content-type':'application/json; charset=utf-8',RequestId:'codex-v2-list',Units:'2/98/100'});
          res.end(JSON.stringify({result:{Campaigns:[{Id:77,Name:'Codex v2 campaign',StartDate:'2026-08-01',EndDate:null,Type:'TEXT_CAMPAIGN',Status:'ACCEPTED',State:'ON',Currency:'RUB'}]}}));
          return;
        }
        res.writeHead(404);res.end('not found');
      },650);
    }); return;
  }
  res.writeHead(200,{'content-type':'text/html; charset=utf-8'});res.end(fixtureHtml());
});

const delay=(ms)=>new Promise((resolve)=>setTimeout(resolve,ms));
async function waitUntil(fn,message,timeout=25000,interval=120){const started=Date.now();let last;while(Date.now()-started<timeout){try{last=await fn();if(last)return last;}catch(error){last=error;}await delay(interval);}throw new Error(`${message}; last=${last instanceof Error?last.message:JSON.stringify(last)}`);}
async function runtimeSend(page,message){return page.evaluate((payload)=>new Promise((resolve)=>{chrome.runtime.sendMessage(payload,(response)=>resolve({response:response||null,error:chrome.runtime.lastError?.message||null}));}),message).then(({response,error})=>{if(error)throw new Error(error);return response;});}
async function getState(page){const r=await runtimeSend(page,{type:'WS_GET_STATE',conversation_key:KEY});if(!r?.ok||!r.state)throw new Error(`STATE_FAIL ${JSON.stringify(r)}`);return r.state;}
async function tabRuntimeSend(worker,tabId,message){return worker.evaluate(async({tabId,message})=>{const rows=await chrome.scripting.executeScript({target:{tabId},world:'ISOLATED',func:(payload)=>new Promise((resolve)=>{chrome.runtime.sendMessage(payload,(response)=>resolve({response:response||null,error:chrome.runtime.lastError?.message||null}));}),args:[message]});return rows?.[0]?.result||null;},{tabId,message});}
async function applyManual(worker,tabId,enabled,service){return worker.evaluate(async({tabId,key,enabled,service})=>new Promise((resolve)=>chrome.tabs.sendMessage(tabId,{type:'WS_APPLY_MANUAL_MODE',conversation_key:key,enabled,active_service:service},(response)=>resolve({response:response||null,error:chrome.runtime.lastError?.message||null}))),{tabId,key:KEY,enabled,service});}
async function fixtureState(page){return page.evaluate(()=>({sendHistory:[...(window.__fixture?.sendHistory||[])],sendCycles:Number(window.__fixture?.sendCycles||0),composer:document.getElementById('prompt-textarea')?.value||''}));}
async function actionState(page){return page.evaluate(()=>{const buttons=[...(document.querySelector('#ymb-external-action-surface')?.shadowRoot?.querySelectorAll('.ymb-action')||[])];const button=buttons.at(-1);return{count:buttons.length,disabled:button?Boolean(button.disabled):null,label:button?.textContent||''};});}
async function clickAction(page,{allowDisabled=false}={}){return page.evaluate((allow)=>{const buttons=[...(document.querySelector('#ymb-external-action-surface')?.shadowRoot?.querySelectorAll('.ymb-action')||[])];const button=buttons.at(-1);if(!button)throw new Error('NO_MANUAL_ACTION');if(button.disabled&&!allow)throw new Error('MANUAL_ACTION_NOT_READY');button.click();return{disabled:Boolean(button.disabled),count:buttons.length};},allowDisabled);}
async function waitRun(page,status){return waitUntil(async()=>{const state=await getState(page);return state.auto_run?.status===status?state:false;},`RUN_NOT_${status}`);}
async function finishRun(page,tabId){const result=await runtimeSend(page,{type:'WS_FINISH_AUTORUN',conversation_key:KEY,tab_id:tabId});assert.equal(result?.ok,true,`FINISH_FAIL ${JSON.stringify(result)}`);return waitRun(page,'stopped');}

await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(8443,'127.0.0.1',resolve);});
let browser;
try{
  browser=await puppeteer.launch({headless:false,pipe:true,enableExtensions:true,protocolTimeout:30000,userDataDir:fs.mkdtempSync(path.join(os.tmpdir(),'ymb-direct-codex-v2-')),args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--no-proxy-server','--ignore-certificate-errors','--disable-background-networking','--disable-features=DnsOverHttps',`--disable-extensions-except=${extensionRoot}`,`--load-extension=${extensionRoot}`,'--host-resolver-rules=MAP chatgpt.com 127.0.0.1:8443, MAP chat.openai.com 127.0.0.1:8443, MAP api.direct.yandex.com 127.0.0.1:8443, EXCLUDE localhost']});
  const pages=await browser.pages();const fixture=pages[0]||await browser.newPage();await fixture.bringToFront();await fixture.goto(PROJECT_URL,{waitUntil:'domcontentloaded',timeout:20000});
  const swTarget=await browser.waitForTarget((t)=>t.type()==='service_worker'&&t.url().startsWith('chrome-extension://'),{timeout:15000});const worker=await swTarget.worker();assert.ok(worker,'MV3 worker missing');
  const extensionId=new URL(swTarget.url()).host;assert.match(extensionId,/^[a-p]{32}$/);
  const identity=await worker.evaluate(async(expectedUrl)=>{const tabs=await chrome.tabs.query({});const tab=tabs.find((item)=>item.url===expectedUrl);if(!tab)return null;return new Promise((resolve)=>chrome.tabs.sendMessage(tab.id,{type:'WS_GET_IDENTITY'},(response)=>resolve({tabId:tab.id,response:response||null,error:chrome.runtime.lastError?.message||null})));},PROJECT_URL);
  assert.equal(identity?.response?.ok,true,`IDENTITY_FAIL ${JSON.stringify(identity)}`);assert.equal(identity.response.conversation_key,KEY);const chatTabId=identity.tabId;

  // D19 uses a normal installed extension page. It intentionally does not depend
  // on action-popup active-tab discovery.
  const extensionPage=await browser.newPage();await extensionPage.goto(`chrome-extension://${extensionId}/popup.html`,{waitUntil:'load'});await extensionPage.waitForSelector('#directCredentials',{timeout:15000});await extensionPage.waitForFunction(()=>document.querySelector('#saveSettingsTop')?.disabled===false,{timeout:15000});
  const originals={wordstat:{api_key:'qa-w-secret',folder_id:'qa-w-folder'},search:{api_key:'qa-s-secret',folder_id:'qa-s-folder'},webmaster:{oauth_token:'qa-wm-secret'},metrika:{oauth_token:'qa-m-secret'},direct:{oauth_token:'qa-d-secret',client_login:'qa-d-client'}};
  for(const [service,credential] of Object.entries(originals)){const saved=await runtimeSend(extensionPage,{type:'YMB_SAVE_SERVICE_CREDENTIAL',service,credential});assert.equal(saved?.ok,true,`SAVE_${service}`);}
  const exported=await runtimeSend(extensionPage,{type:'WS_EXPORT_BACKUP'});assert.equal(exported?.ok,true);const backup=exported.backup;assert.equal(backup.backup_version,3);assert.equal(backup.settings_schema_version,5);assert.equal(backup.settings.credentials.wordstat.api_key,originals.wordstat.api_key);assert.equal(backup.settings.credentials.search.api_key,originals.search.api_key);assert.equal(backup.settings.credentials.webmaster.oauth_token,originals.webmaster.oauth_token);assert.equal(backup.settings.credentials.metrika.oauth_token,originals.metrika.oauth_token);assert.equal(backup.settings.credentials.direct.oauth_token,originals.direct.oauth_token);assert.equal(backup.settings.credentials.direct.client_login,originals.direct.client_login);
  const mutated={wordstat:{api_key:'mut-w',folder_id:'mut-wf'},search:{api_key:'mut-s',folder_id:'mut-sf'},webmaster:{oauth_token:'mut-wm'},metrika:{oauth_token:'mut-m'},direct:{oauth_token:'mut-d',client_login:'mut-dc'}};for(const [service,credential] of Object.entries(mutated))assert.equal((await runtimeSend(extensionPage,{type:'YMB_SAVE_SERVICE_CREDENTIAL',service,credential}))?.ok,true);
  const tampered=structuredClone(backup);tampered.settings.credentials.direct.client_login='tampered';const tamper=await runtimeSend(extensionPage,{type:'WS_IMPORT_BACKUP',backup:tampered});assert.equal(tamper?.ok,false);let loaded=await worker.evaluate(async()=>globalThis.YMBCredentialRuntime.load());assert.equal(loaded.direct.oauth_token,'mut-d');
  const imported=await runtimeSend(extensionPage,{type:'WS_IMPORT_BACKUP',backup});assert.equal(imported?.ok,true);loaded=await worker.evaluate(async()=>globalThis.YMBCredentialRuntime.load());assert.equal(loaded.wordstat.api_key,originals.wordstat.api_key);assert.equal(loaded.wordstat.folder_id,originals.wordstat.folder_id);assert.equal(loaded.search.api_key,originals.search.api_key);assert.equal(loaded.search.folder_id,originals.search.folder_id);assert.equal(loaded.webmaster.oauth_token,originals.webmaster.oauth_token);assert.equal(loaded.metrika.oauth_token,originals.metrika.oauth_token);assert.equal(loaded.direct.oauth_token,originals.direct.oauth_token);assert.equal(loaded.direct.client_login,originals.direct.client_login);
  await extensionPage.reload({waitUntil:'load'});await extensionPage.waitForSelector('#directCredentials',{timeout:15000});for(const id of ['wordstatApiKey','searchApiKey','webmasterOauthToken','metrikaOauthToken','directOauthToken'])assert.equal(await extensionPage.$eval(`#${id}`,(node)=>node.value),'');for(const secret of [originals.wordstat.api_key,originals.search.api_key,originals.webmaster.oauth_token,originals.metrika.oauth_token,originals.direct.oauth_token])assert.equal(await extensionPage.evaluate((value)=>document.body.innerText.includes(value),secret),false);
  console.log('D19_FIVE_SERVICE_BACKUP_UI_MAPPING_PASS');

  // Establish the same controlled binding shape used by the accepted Manual
  // lifecycle harness, then keep all conversation-bound messages tied to the real
  // ChatGPT tab id.
  await worker.evaluate(async({key,cid})=>{const now=new Date().toISOString();await chrome.storage.local.set({wsmb_conversation_bindings:{[key]:{binding_id:'qa-codex-v2-binding',revision:1,origin:'https://chatgpt.com',conversation_id:cid,conversation_key:key,bound_at:now,updated_at:now}},wsmb_manual_modes:{[key]:false},ymb_service_contexts:{[key]:{active_service:'direct',updated_at:now}},wsmb_auto_send:true,ymb_debug_mode:true});},{key:KEY,cid:CID});
  assert.equal((await runtimeSend(extensionPage,{type:'WS_SAVE_SERVICE_CONTEXT',conversation_key:KEY,active_service:'direct',tab_id:chatTabId}))?.ok,true);
  assert.equal((await runtimeSend(extensionPage,{type:'YMB_SAVE_DIRECT_POLICY',policy:{manual_enabled:true,autorun_enabled:false,max_requests_per_run:20,max_page_size:1000,max_report_days:31,max_report_rows:1000}}))?.ok,true);

  // D17 busy fence: worker commit + real content apply, then verify a blocked second
  // click cannot create a second provider execution while the first request is live.
  const manualOn=await runtimeSend(extensionPage,{type:'WS_SET_MANUAL_MODE',conversation_key:KEY,enabled:true,tab_id:chatTabId});assert.equal(manualOn?.ok,true);const appliedOn=await applyManual(worker,chatTabId,true,'direct');assert.equal(appliedOn?.error,null);assert.equal(appliedOn?.response?.ok,true);assert.equal(appliedOn?.response?.applied,true);
  await fixture.bringToFront();await fixture.evaluate((command)=>window.__fixture.appendAssistant(command,'manual-fence-v2'),DIRECT_COMMAND);await waitUntil(async()=>{const s=await actionState(fixture);return s.count>=1&&s.disabled===false&&s.label==='Яндекс';},'MANUAL_ACTION_NOT_READY');const beforeManual=providerHits.length;await clickAction(fixture);await waitUntil(async()=>providerHits.length===beforeManual+1,'MANUAL_PROVIDER_NOT_STARTED');await waitUntil(async()=>(await actionState(fixture)).disabled===true,'MANUAL_ACTION_NOT_DISABLED');const blocked=await clickAction(fixture,{allowDisabled:true});assert.equal(blocked.disabled,true);await delay(250);assert.equal(providerHits.length,beforeManual+1,'BLOCKED_MANUAL_CLICK_REPLAYED_PROVIDER');await waitUntil(async()=>{const f=await fixtureState(fixture);return f.sendHistory.some((text)=>String(text).startsWith('DIRECT_RESULT_V1'));},'MANUAL_RESULT_NOT_DELIVERED');await waitUntil(async()=>(await actionState(fixture)).disabled===false,'MANUAL_ACTION_NOT_REENABLED');assert.equal(providerHits.length,beforeManual+1);console.log('D17_MANUAL_BUSY_FENCE_SINGLE_PROVIDER_PASS');
  const manualOff=await runtimeSend(extensionPage,{type:'WS_SET_MANUAL_MODE',conversation_key:KEY,enabled:false,tab_id:chatTabId});assert.equal(manualOff?.ok,true);const appliedOff=await applyManual(worker,chatTabId,false,'direct');assert.equal(appliedOff?.error,null);assert.equal(appliedOff?.response?.ok,true);assert.equal(appliedOff?.response?.applied,true);

  // D16 direction 1: active Search + Direct prefix must be local SERVICE_NOT_ACTIVE
  // with zero Direct provider traffic.
  assert.equal((await runtimeSend(extensionPage,{type:'WS_SAVE_SERVICE_CONTEXT',conversation_key:KEY,active_service:'search',tab_id:chatTabId}))?.ok,true);await worker.evaluate(async()=>{const policy=globalThis.YMBPolicyModel.normalizeSearchPolicy({manual_enabled:true,autorun_enabled:true,max_requests_per_run:5,max_cost_rub_per_run:5});await chrome.storage.local.set({ymb_search_policy:policy});});let started=await runtimeSend(extensionPage,{type:'WS_START_AUTORUN',conversation_key:KEY,tab_id:chatTabId});assert.equal(started?.ok,true,`SEARCH_START_FAIL ${JSON.stringify(started)}`);let state=await waitRun(extensionPage,'waiting_command');const beforeIsolation=providerHits.length;const mismatch=await tabRuntimeSend(worker,chatTabId,{type:'WS_AUTO_COMMAND',conversation_key:KEY,run_id:state.auto_run.run_id,command_text:DIRECT_COMMAND,assistant_turn_id:'search-active-direct-prefix'});assert.equal(mismatch?.error,null);assert.equal(mismatch?.response?.code,'SERVICE_NOT_ACTIVE');state=await waitRun(extensionPage,'waiting_command');assert.equal(providerHits.length,beforeIsolation);console.log('D16_NON_DIRECT_ACTIVE_DIRECT_PREFIX_ZERO_TRAFFIC_PASS');await finishRun(extensionPage,chatTabId);

  // D20 Direct default OFF is enforced locally.
  assert.equal((await runtimeSend(extensionPage,{type:'WS_SAVE_SERVICE_CONTEXT',conversation_key:KEY,active_service:'direct',tab_id:chatTabId}))?.ok,true);assert.equal((await runtimeSend(extensionPage,{type:'YMB_SAVE_DIRECT_POLICY',policy:{manual_enabled:true,autorun_enabled:false,max_requests_per_run:20,max_page_size:1000,max_report_days:31,max_report_rows:1000}}))?.ok,true);const beforeDisabled=providerHits.length;const disabled=await runtimeSend(extensionPage,{type:'WS_START_AUTORUN',conversation_key:KEY,tab_id:chatTabId});assert.equal(disabled?.ok,false);assert.equal(disabled?.code,'AUTORUN_DISABLED');assert.equal(providerHits.length,beforeDisabled);console.log('D20_DIRECT_AUTORUN_DEFAULT_DISABLED_LOCAL_PASS');

  // Controlled enablement exists only in this QA route; production popup remains locked.
  assert.equal((await runtimeSend(extensionPage,{type:'YMB_SAVE_DIRECT_POLICY',policy:{manual_enabled:true,autorun_enabled:true,max_requests_per_run:20,max_page_size:1000,max_report_days:31,max_report_rows:1000}}))?.ok,true);const beforeDirectAutorunStart=providerHits.length;started=await runtimeSend(extensionPage,{type:'WS_START_AUTORUN',conversation_key:KEY,tab_id:chatTabId});assert.equal(started?.ok,true,`DIRECT_START_FAIL ${JSON.stringify(started)}`);state=await waitRun(extensionPage,'waiting_command');assert.equal(state.auto_run.active_service,'direct');await delay(3200);assert.equal(providerHits.length,beforeDirectAutorunStart,'STALE_MANUAL_TURN_REPLAYED_ON_DIRECT_AUTORUN_START');console.log('D16_STALE_MANUAL_TURN_BASELINE_FENCE_PASS');

  // D16 direction 2: active Direct rejects every other registered prefix locally.
  for(const [name,command] of [['wordstat','WORDSTAT_API_V1\n{}'],['search','SEARCH_API_V1\n{}'],['webmaster','WEBMASTER_API_V1\n{}'],['metrika','METRIKA_API_V1\n{}']]){const before=providerHits.length;const r=await tabRuntimeSend(worker,chatTabId,{type:'WS_AUTO_COMMAND',conversation_key:KEY,run_id:state.auto_run.run_id,command_text:command,assistant_turn_id:`direct-active-${name}`});assert.equal(r?.error,null,name);assert.equal(r?.response?.code,'SERVICE_NOT_ACTIVE',name);state=await waitRun(extensionPage,'waiting_command');assert.equal(state.auto_run.active_service,'direct');assert.equal(providerHits.length,before,name);}
  console.log('D16_DIRECT_ACTIVE_OTHER_PREFIXES_ZERO_TRAFFIC_PASS');

  // D20 one fingerprint admission -> one provider request -> one delivery; duplicate
  // assistant turn is ignored and cannot replay the POST.
  const beforeAuto=providerHits.length;const sendsBefore=(await fixtureState(fixture)).sendHistory.length;const turnId='direct-autorun-v2-turn';const admission=await tabRuntimeSend(worker,chatTabId,{type:'WS_AUTO_COMMAND',conversation_key:KEY,run_id:state.auto_run.run_id,command_text:DIRECT_COMMAND,assistant_turn_id:turnId});assert.equal(admission?.error,null);assert.equal(admission?.response?.accepted,true);await waitUntil(async()=>providerHits.length===beforeAuto+1,'DIRECT_AUTORUN_PROVIDER_NOT_CALLED');state=await waitUntil(async()=>{const s=await getState(extensionPage);return s.auto_run?.status==='waiting_command'&&Number(s.auto_run?.requests_executed)===1?s:false;},'DIRECT_AUTORUN_NOT_RETURNED');await waitUntil(async()=>(await fixtureState(fixture)).sendHistory.length>=sendsBefore+1,'DIRECT_AUTORUN_RESULT_NOT_DELIVERED');assert.equal(providerHits.length,beforeAuto+1);assert.equal(state.auto_run.active_service,'direct');assert.equal(state.service_context.active_service,'direct');const duplicate=await tabRuntimeSend(worker,chatTabId,{type:'WS_AUTO_COMMAND',conversation_key:KEY,run_id:state.auto_run.run_id,command_text:DIRECT_COMMAND,assistant_turn_id:turnId});assert.equal(duplicate?.error,null);assert.equal(duplicate?.response?.duplicate,true);await delay(500);assert.equal(providerHits.length,beforeAuto+1);console.log('D20_DIRECT_AUTORUN_ONE_FINGERPRINT_ONE_PROVIDER_ONE_DELIVERY_PASS');

  assert.equal((await runtimeSend(extensionPage,{type:'WS_PAUSE_AUTORUN',conversation_key:KEY,tab_id:chatTabId}))?.ok,true);await waitRun(extensionPage,'paused');assert.equal((await runtimeSend(extensionPage,{type:'WS_RESUME_AUTORUN',conversation_key:KEY,tab_id:chatTabId}))?.ok,true);await waitRun(extensionPage,'waiting_command');state=await finishRun(extensionPage,chatTabId);assert.equal(state.auto_run.active_service,'direct');assert.equal(providerHits.length,beforeAuto+1);console.log('D20_DIRECT_AUTORUN_PAUSE_RESUME_FINISH_PASS');

  const safe=JSON.stringify(providerHits.map((hit)=>({url:hit.url,method:hit.method,body:hit.body})));for(const secret of [originals.wordstat.api_key,originals.search.api_key,originals.webmaster.oauth_token,originals.metrika.oauth_token,originals.direct.oauth_token])assert.equal(safe.includes(secret),false);assert.equal(providerHits.every((hit)=>String(hit.remote||'').includes('127.0.0.1')||String(hit.remote||'').includes('::ffff:127.0.0.1')),true);console.log(`DIRECT_CONTROLLED_PROVIDER_REQUESTS=${providerHits.length}`);console.log('DIRECT_REAL_YANDEX_REQUESTS=0');console.log('PHASE5_DIRECT_CODEX_BROWSER_ADDENDUM_PASS');
}finally{if(browser)await browser.close().catch(()=>{});await new Promise((resolve)=>server.close(resolve));}
