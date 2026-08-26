import fs from 'node:fs';
import https from 'node:https';
import os from 'node:os';
import path from 'node:path';
import process from 'node:process';
import puppeteer from 'puppeteer-core';

const [chromePath, extensionRoot, keyPath, certPath] = process.argv.slice(2);
if (!chromePath || !extensionRoot || !keyPath || !certPath) {
  throw new Error('usage: lifecycle_button_gating_gate.mjs <chrome> <extension-root> <tls-key> <tls-cert>');
}
for (const p of [chromePath, extensionRoot, keyPath, certPath]) {
  if (!fs.existsSync(p)) throw new Error(`HARNESS_INPUT_MISSING ${p}`);
}

const CID = '99999999-8888-4777-8666-555555555555';
const CHAT_URL = `https://chatgpt.com/c/${CID}`;
const CKEY = `https://chatgpt.com|${CID}`;
const providerHits = [];

function fixtureHtml() {
  return `<!doctype html><html><head><meta charset="utf-8"><link rel="canonical" href="${CHAT_URL}"><title>Lifecycle Button QA</title></head><body>
  <main id="conversation-root">
    <div data-message-author-role="assistant" data-message-id="qa-lifecycle-block">
      <pre data-testid="code-block"><code>controlled lifecycle baseline block</code></pre>
      <button aria-label="Copy" type="button">Copy</button>
    </div>
  </main>
  <textarea id="prompt-textarea"></textarea>
  <button id="composer-submit-button" data-testid="send-button" aria-label="Send" type="button">Send</button>
  <script>
    const composer=document.getElementById('prompt-textarea');
    const send=document.getElementById('composer-submit-button');
    send.addEventListener('click',()=>{ composer.value=''; composer.dispatchEvent(new Event('input',{bubbles:true})); });
  </script>
  </body></html>`;
}

const server = https.createServer({ key:fs.readFileSync(keyPath), cert:fs.readFileSync(certPath) }, (req,res) => {
  const host=String(req.headers.host||'').split(':')[0].toLowerCase();
  if (host === 'searchapi.api.cloud.yandex.net') {
    const chunks=[]; req.on('data',c=>chunks.push(c)); req.on('end',()=>{
      providerHits.push({method:req.method,url:req.url,body:Buffer.concat(chunks).toString('utf8')});
      res.writeHead(500,{'content-type':'application/json'}); res.end(JSON.stringify({code:'QA_PROVIDER_MUST_NOT_BE_CALLED'}));
    });
    return;
  }
  res.writeHead(200,{'content-type':'text/html; charset=utf-8'}); res.end(fixtureHtml());
});
await new Promise((resolve,reject)=>{ server.once('error',reject); server.listen(8443,'127.0.0.1',resolve); });

const delay=ms=>new Promise(r=>setTimeout(r,ms));
function assert(condition,message){ if(!condition) throw new Error(message); }
async function waitUntil(fn,message,timeout=15000,interval=100){
  const started=Date.now(); let last;
  while(Date.now()-started<timeout){
    try{ last=await fn(); if(last) return last; }catch(error){ last=error; }
    await delay(interval);
  }
  throw new Error(`${message}; last=${last instanceof Error?last.message:JSON.stringify(last)}`);
}

async function openPopup(worker,browser,key){
  const owner=await worker.evaluate(async expectedKey=>{
    const tabs=await chrome.tabs.query({active:true,currentWindow:true});
    const active=tabs?.[0]||null;
    if(!active?.id) return {active:null,identity:null};
    const identity=await new Promise(resolve=>chrome.tabs.sendMessage(active.id,{type:'WS_GET_IDENTITY'},response=>resolve({response:response||null,error:chrome.runtime.lastError?.message||null})));
    return {active:{id:active.id,url:active.url||''},identity,expectedKey};
  },key);
  assert(owner?.active?.id,`POPUP_OWNER_ACTIVE_TAB_MISSING ${JSON.stringify(owner)}`);
  assert(owner.identity?.response?.ok===true && owner.identity.response.conversation_key===key,`POPUP_OWNER_CONTEXT_FAIL ${JSON.stringify(owner)}`);
  const tab=await worker.evaluate(async ownerTabId=>{
    const created=await chrome.tabs.create({url:'about:blank',active:false});
    if(!created?.id) return null;
    await chrome.tabs.update(ownerTabId,{active:true});
    await chrome.tabs.update(created.id,{url:chrome.runtime.getURL('popup.html')});
    return {id:created.id};
  },owner.active.id);
  assert(tab?.id,'POPUP_TAB_CREATE_FAIL');
  const popup=await waitUntil(async()=>{
    for(const page of await browser.pages()){
      if(!page.url().startsWith('chrome-extension://')||!page.url().endsWith('/popup.html')) continue;
      const current=await page.evaluate(()=>new Promise(resolve=>chrome.tabs.getCurrent(t=>resolve(t?.id||null)))).catch(()=>null);
      if(Number(current)===Number(tab.id)) return page;
    }
    return null;
  },'POPUP_TAB_TARGET_FAIL',12000,80);
  const bootstrap=await waitUntil(async()=>await popup.evaluate(()=>{
    const error=globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_ERROR__||'';
    const result=globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_RESULT__||null;
    if(!error&&!result) return null;
    return {error,result,status:document.getElementById('status')?.textContent||''};
  }),'POPUP_BOOTSTRAP_OUTCOME_TIMEOUT',12000,80);
  if(bootstrap.error) throw new Error(`POPUP_BOOTSTRAP_ERROR ${bootstrap.error}`);
  assert(bootstrap.result?.attempted===true,`POPUP_BOOTSTRAP_NOT_ATTEMPTED ${JSON.stringify(bootstrap)}`);
  await popup.waitForFunction(expected=>document.getElementById('conversationMeta')?.textContent===expected,{timeout:12000},key);
  await waitUntil(async()=>{
    const state=await popup.evaluate(()=>({text:document.getElementById('status')?.textContent||'',level:document.getElementById('status')?.dataset?.level||''}));
    if(state.level==='error') throw new Error(`POPUP_INITIAL_ERROR ${state.text}`);
    return state.text==='Готово.'?state:false;
  },'POPUP_INITIAL_REFRESH_NOT_COMPLETE',12000,80);
  return {popup,tabId:tab.id,ownerTabId:owner.active.id};
}
async function popupClick(popup,selector){
  await popup.evaluate(sel=>{const el=document.querySelector(sel);if(!el)throw new Error(`POPUP_ELEMENT_MISSING ${sel}`);if(el.disabled)throw new Error(`POPUP_ELEMENT_DISABLED ${sel}`);el.click();},selector);
}
async function waitPopupStatus(popup,expected,message){
  return waitUntil(async()=>{
    const state=await popup.evaluate(()=>({text:document.getElementById('status')?.textContent||'',level:document.getElementById('status')?.dataset?.level||''}));
    if(state.level==='error') throw new Error(`POPUP_ERROR ${state.text}`);
    return state.text===expected?state:false;
  },message,15000,80);
}
async function runtimeState(popup){
  return popup.evaluate(key=>new Promise(resolve=>chrome.runtime.sendMessage({type:'WS_GET_STATE',conversation_key:key},r=>resolve(r||null))),CKEY);
}
async function actionSnapshot(page){
  return page.evaluate(()=>{
    const root=document.querySelector('#ymb-external-action-surface')?.shadowRoot;
    const buttons=[...(root?.querySelectorAll('.ymb-action')||[])];
    return {count:buttons.length,disabled:buttons.length===1?buttons[0].disabled:null,title:buttons.length===1?buttons[0].title:'',label:buttons.length===1?buttons[0].textContent:''};
  });
}
async function refreshContent(worker,tabId){
  const result=await worker.evaluate(async id=>await new Promise(resolve=>chrome.tabs.sendMessage(id,{type:'WS_REFRESH_STATE'},r=>resolve({response:r||null,error:chrome.runtime.lastError?.message||null}))),tabId);
  assert(!result.error && result.response?.ok===true,`CONTENT_REFRESH_FAIL ${JSON.stringify(result)}`);
}
async function setMapRecord(worker,storageKey,key,value){
  await worker.evaluate(async ({storageKey,key,value})=>{
    const data=await chrome.storage.local.get(storageKey); const map={...(data[storageKey]||{})};
    if(value===null) delete map[key]; else map[key]=value;
    await chrome.storage.local.set({[storageKey]:map});
  },{storageKey,key,value});
}
async function storageSnapshot(worker){
  return worker.evaluate(async()=>await chrome.storage.local.get(['wsmb_manual_operations','wsmb_outbox','ymb_content_error_queue']));
}
async function clearQaTransientState(worker){
  await worker.evaluate(async()=>await chrome.storage.local.set({wsmb_manual_operations:{},wsmb_outbox:{},ymb_content_error_queue:{}}));
}
async function clickDisabledAction(page){
  return page.evaluate(()=>{
    const button=document.querySelector('#ymb-external-action-surface')?.shadowRoot?.querySelector('.ymb-action');
    if(!button) throw new Error('YMB_ACTION_MISSING');
    const before={disabled:button.disabled,title:button.title};
    button.click();
    return {before,afterDisabled:button.disabled};
  });
}

let browser;
try{
  browser=await puppeteer.launch({
    executablePath:chromePath, headless:false, protocolTimeout:30000,
    userDataDir:fs.mkdtempSync(path.join(os.tmpdir(),'ymb-lifecycle-button-')),
    args:['--no-sandbox','--disable-gpu','--no-proxy-server','--ignore-certificate-errors','--disable-background-networking','--disable-features=DnsOverHttps',`--disable-extensions-except=${extensionRoot}`,`--load-extension=${extensionRoot}`,'--host-resolver-rules=MAP chatgpt.com 127.0.0.1:8443, MAP chat.openai.com 127.0.0.1:8443, MAP searchapi.api.cloud.yandex.net 127.0.0.1:8443, EXCLUDE localhost']
  });
  const pages=await browser.pages(); const fixture=pages[0]||await browser.newPage(); await fixture.bringToFront(); await fixture.goto(CHAT_URL,{waitUntil:'domcontentloaded',timeout:20000});
  const swTarget=await browser.waitForTarget(t=>t.type()==='service_worker'&&t.url().startsWith('chrome-extension://'),{timeout:15000});
  const worker=await swTarget.worker(); assert(worker,'MV3_WORKER_CONTEXT_FAIL');
  const identity=await worker.evaluate(async expectedUrl=>{
    const tabs=await chrome.tabs.query({}); const tab=tabs.find(x=>x.url===expectedUrl); if(!tab)return null;
    return await new Promise(resolve=>chrome.tabs.sendMessage(tab.id,{type:'WS_GET_IDENTITY'},r=>resolve({tabId:tab.id,response:r||null,error:chrome.runtime.lastError?.message||null})));
  },CHAT_URL);
  assert(identity?.response?.ok===true && identity.response.conversation_key===CKEY,`IDENTITY_FAIL ${JSON.stringify(identity)}`);

  const {popup,ownerTabId}=await openPopup(worker,browser,CKEY);
  await popupClick(popup,'#bindConversation');
  await waitPopupStatus(popup,'Диалог привязан.','BIND_NOT_COMPLETE');
  await popupClick(popup,'#manualMode');
  await waitPopupStatus(popup,'Ручной режим включён.','MANUAL_ON_NOT_COMPLETE');
  await waitUntil(async()=>{const r=await runtimeState(popup);return r?.ok&&r.state?.manual_mode===true?r.state:false;},'WORKER_MANUAL_NOT_ON');
  await waitUntil(async()=>{const s=await actionSnapshot(fixture);return s.count===1&&s.disabled===false?s:false;},'INITIAL_ACTION_NOT_ENABLED');
  console.log('LIFECYCLE_BUTTON_INITIAL_ENABLED_PASS');

  await clearQaTransientState(worker);
  await refreshContent(worker,ownerTabId);

  const op={operation_id:'qa-lifecycle-operation',request_token:'qa-lifecycle-token',conversation_key:CKEY,tab_id:ownerTabId,active_service:'wordstat',run_id:null,status:'requesting',request_executed:false,created_at:new Date().toISOString()};
  await setMapRecord(worker,'wsmb_manual_operations',CKEY,op);
  await refreshContent(worker,ownerTabId);
  const blockedOp=await waitUntil(async()=>{const s=await actionSnapshot(fixture);return s.count===1&&s.disabled===true?s:false;},'MANUAL_OPERATION_DID_NOT_DISABLE_ACTION');
  assert(/ручной операции/i.test(blockedOp.title),`MANUAL_OPERATION_TITLE_FAIL ${JSON.stringify(blockedOp)}`);
  console.log('LIFECYCLE_MANUAL_OPERATION_DISABLED_PASS');
  const beforeOpClick=JSON.stringify(await storageSnapshot(worker));
  const opClick=await clickDisabledAction(fixture); assert(opClick.before.disabled===true,'MANUAL_OPERATION_ACTION_NOT_DISABLED_AT_CLICK');
  await delay(500);
  const afterOpClick=JSON.stringify(await storageSnapshot(worker));
  assert(afterOpClick===beforeOpClick,'MANUAL_OPERATION_BLOCKED_CLICK_MUTATED_RUNTIME_STATE');
  assert(providerHits.length===0,`MANUAL_OPERATION_BLOCKED_CLICK_PROVIDER_HIT ${providerHits.length}`);
  console.log('LIFECYCLE_MANUAL_OPERATION_BLOCKED_CLICK_NO_DISPATCH_PASS');
  await setMapRecord(worker,'wsmb_manual_operations',CKEY,null);
  await refreshContent(worker,ownerTabId);
  await waitUntil(async()=>{const s=await actionSnapshot(fixture);return s.count===1&&s.disabled===false?s:false;},'MANUAL_OPERATION_CLEAR_DID_NOT_REENABLE_ACTION');
  console.log('LIFECYCLE_MANUAL_OPERATION_CLEAR_REENABLE_PASS');

  const delivery={delivery_id:'qa-lifecycle-delivery',type:'qa_hold',phase:'qa_hold',conversation_key:CKEY,tab_id:ownerTabId,report_text:'',created_at:new Date().toISOString(),updated_at:new Date().toISOString()};
  await setMapRecord(worker,'wsmb_outbox',CKEY,delivery);
  const blockedDelivery=await waitUntil(async()=>{const s=await actionSnapshot(fixture);return s.count===1&&s.disabled===true?s:false;},'DELIVERY_DID_NOT_DISABLE_ACTION',7000,80);
  assert(/доставки/i.test(blockedDelivery.title),`DELIVERY_TITLE_FAIL ${JSON.stringify(blockedDelivery)}`);
  console.log('LIFECYCLE_DELIVERY_DISABLED_PASS');
  const beforeDeliveryClick=JSON.stringify(await storageSnapshot(worker));
  const deliveryClick=await clickDisabledAction(fixture); assert(deliveryClick.before.disabled===true,'DELIVERY_ACTION_NOT_DISABLED_AT_CLICK');
  await delay(700);
  const afterDeliveryClick=JSON.stringify(await storageSnapshot(worker));
  assert(afterDeliveryClick===beforeDeliveryClick,'DELIVERY_BLOCKED_CLICK_MUTATED_RUNTIME_STATE');
  assert(providerHits.length===0,`DELIVERY_BLOCKED_CLICK_PROVIDER_HIT ${providerHits.length}`);
  console.log('LIFECYCLE_DELIVERY_BLOCKED_CLICK_NO_DISPATCH_PASS');
  await setMapRecord(worker,'wsmb_outbox',CKEY,null);
  await waitUntil(async()=>{const s=await actionSnapshot(fixture);return s.count===1&&s.disabled===false?s:false;},'DELIVERY_CLEAR_DID_NOT_REENABLE_ACTION',7000,80);
  console.log('LIFECYCLE_DELIVERY_CLEAR_REENABLE_PASS');

  assert(providerHits.length===0,`REAL_OR_CONTROLLED_PROVIDER_REQUEST_UNEXPECTED ${providerHits.length}`);
  console.log('LIFECYCLE_GATE_PROVIDER_HITS=0');
  console.log('LIFECYCLE_GATE_REAL_YANDEX_REQUESTS=0');
  console.log('LIFECYCLE_BUTTON_GATING_BROWSER_GATE_PASS');
} finally {
  try{await browser?.close();}catch{}
  await new Promise(resolve=>server.close(()=>resolve()));
}
