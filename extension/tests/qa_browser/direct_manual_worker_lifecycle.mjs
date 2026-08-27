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
  return `<!doctype html><html><head><meta charset="utf-8"><title>Direct worker lifecycle</title><style>
  body{font-family:Arial,sans-serif;margin:20px}.turn{margin:12px 0}.codewrap{position:relative;display:inline-block;min-width:420px}pre{padding:18px;background:#eee}.composer{position:fixed;bottom:20px;left:20px;right:20px;background:white;padding:10px;border:1px solid #aaa}#prompt-textarea{width:75%;height:72px}
  </style></head><body><main id="conversation-root"></main>
  <div class="composer"><textarea id="prompt-textarea"></textarea><button id="composer-submit-button" data-testid="send-button" aria-label="Send" type="button">Send</button><button id="voice" aria-label="Voice" type="button" hidden>Voice</button><button id="stop" data-testid="stop-button" aria-label="Stop" type="button" hidden>Stop</button></div>
  <script>
    window.__fixture={sendHistory:[],sendCycles:0,appended:[]};
    const textarea=document.getElementById('prompt-textarea'); const send=document.getElementById('composer-submit-button'); const mic=document.getElementById('voice'); const stop=document.getElementById('stop');
    window.__fixture.appendAssistant=(text,id)=>{const turn=document.createElement('div');turn.className='turn';turn.dataset.messageAuthorRole='assistant';turn.dataset.messageId=id;const wrap=document.createElement('div');wrap.className='codewrap';const pre=document.createElement('pre');pre.dataset.testid='code-block';const code=document.createElement('code');code.textContent=text;pre.appendChild(code);const copy=document.createElement('button');copy.type='button';copy.setAttribute('aria-label','Copy');copy.textContent='Copy';wrap.appendChild(pre);wrap.appendChild(copy);turn.appendChild(wrap);document.getElementById('conversation-root').appendChild(turn);window.__fixture.appended.push({id,text});};
    send.addEventListener('click',()=>{const text=textarea.value;window.__fixture.sendHistory.push(text);window.__fixture.sendCycles+=1;textarea.value='';textarea.dispatchEvent(new Event('input',{bubbles:true}));send.disabled=true;send.hidden=true;stop.hidden=false;setTimeout(()=>{stop.hidden=true;mic.hidden=false;},250);setTimeout(()=>{mic.hidden=true;send.hidden=false;send.disabled=false;},650);});
  </script></body></html>`;
}

const server=https.createServer({key:fs.readFileSync(keyPath),cert:fs.readFileSync(certPath)},(req,res)=>{
  const host=String(req.headers.host||'').split(':')[0].toLowerCase();
  if(host==='api.direct.yandex.com'){
    const chunks=[]; req.on('data',(chunk)=>chunks.push(chunk)); req.on('end',()=>{
      const body=Buffer.concat(chunks).toString('utf8'); providerHits.push({url:req.url,method:req.method,headers:req.headers,body});
      if(req.url==='/json/v501/campaigns'){res.writeHead(200,{'content-type':'application/json; charset=utf-8',RequestId:'manual-list',Units:'2/98/100'});res.end(JSON.stringify({result:{Campaigns:[{Id:77,Name:'Manual lifecycle campaign',StartDate:'2026-08-01',Type:'TEXT_CAMPAIGN',Status:'ACCEPTED',State:'ON',Currency:'RUB'}]}}));return;}
      if(req.url==='/json/v501/reports'){res.writeHead(200,{'content-type':'text/tab-separated-values; charset=utf-8',RequestId:'manual-report',Units:'3/97/100'});res.end('Date\tCampaignId\tCampaignName\tImpressions\tClicks\tCost\n2026-08-01\t77\tManual lifecycle campaign\t100\t5\t123456\n');return;}
      res.writeHead(404);res.end('not found');
    }); return;
  }
  res.writeHead(200,{'content-type':'text/html; charset=utf-8'});res.end(fixtureHtml());
});

const delay=(ms)=>new Promise((resolve)=>setTimeout(resolve,ms));
async function waitUntil(fn,message,timeout=20000,interval=120){const started=Date.now();let last;while(Date.now()-started<timeout){try{last=await fn();if(last)return last;}catch(error){last=error;}await delay(interval);}throw new Error(`${message}; last=${last instanceof Error?last.message:JSON.stringify(last)}`);}
async function actionCount(page){return page.evaluate(()=>document.querySelector('#ymb-external-action-surface')?.shadowRoot?.querySelectorAll('.ymb-action').length||0);}
async function clickLatestAction(page){return page.evaluate(()=>{const buttons=[...(document.querySelector('#ymb-external-action-surface')?.shadowRoot?.querySelectorAll('.ymb-action')||[])];const button=buttons.at(-1);if(!button)throw new Error('NO_MANUAL_ACTION');button.click();return buttons.length;});}
async function fixtureState(page){return page.evaluate(()=>({sendHistory:[...(window.__fixture?.sendHistory||[])],sendCycles:Number(window.__fixture?.sendCycles||0),composer:document.getElementById('prompt-textarea')?.value||''}));}

await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(8443,'127.0.0.1',resolve);});
let browser;
try{
  browser=await puppeteer.launch({headless:false,pipe:true,enableExtensions:true,protocolTimeout:30000,userDataDir:fs.mkdtempSync(path.join(os.tmpdir(),'ymb-direct-worker-lifecycle-')),args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--no-proxy-server','--ignore-certificate-errors','--disable-background-networking','--disable-features=DnsOverHttps',`--disable-extensions-except=${extensionRoot}`,`--load-extension=${extensionRoot}`,'--host-resolver-rules=MAP chatgpt.com 127.0.0.1:8443, MAP chat.openai.com 127.0.0.1:8443, MAP api.direct.yandex.com 127.0.0.1:8443, EXCLUDE localhost']});
  const pages=await browser.pages();const fixture=pages[0]||await browser.newPage();await fixture.goto(PROJECT_URL,{waitUntil:'domcontentloaded',timeout:20000});
  const swTarget=await browser.waitForTarget((t)=>t.type()==='service_worker'&&t.url().startsWith('chrome-extension://'),{timeout:15000});const worker=await swTarget.worker();assert.ok(worker,'MV3 worker missing');

  const identity=await worker.evaluate(async(expectedUrl)=>{const tabs=await chrome.tabs.query({});const tab=tabs.find((item)=>item.url===expectedUrl);if(!tab)return null;return await new Promise((resolve)=>chrome.tabs.sendMessage(tab.id,{type:'WS_GET_IDENTITY'},(response)=>resolve({tabId:tab.id,response:response||null,error:chrome.runtime.lastError?.message||null})));},PROJECT_URL);
  assert.equal(identity?.response?.ok,true,`IDENTITY_FAIL ${JSON.stringify(identity)}`);assert.equal(identity.response.conversation_key,KEY);const tabId=identity.tabId;

  const setup=await worker.evaluate(async({key,cid,tabId})=>{
    const now=new Date().toISOString();
    await chrome.storage.local.set({
      wsmb_conversation_bindings:{[key]:{binding_id:'qa-direct-binding',revision:1,origin:'https://chatgpt.com',conversation_id:cid,conversation_key:key,bound_at:now,updated_at:now}},
      wsmb_manual_modes:{[key]:true},
      ymb_service_contexts:{[key]:{active_service:'direct',updated_at:now}},
      wsmb_auto_send:false
    });
    await globalThis.YMBPhase5Runtime.saveServiceCredential('direct',{oauth_token:'worker-lifecycle-secret',client_login:'worker-lifecycle-client'});
    await globalThis.YMBPhase5Runtime.saveDirectPolicy({manual_enabled:true,autorun_enabled:false});
    return await new Promise((resolve)=>chrome.tabs.sendMessage(tabId,{type:'WS_APPLY_MANUAL_MODE',conversation_key:key,enabled:true,active_service:'direct'},(response)=>resolve({response:response||null,error:chrome.runtime.lastError?.message||null})));
  },{key:KEY,cid:CID,tabId});
  assert.equal(setup?.response?.ok,true,`MANUAL_APPLY_FAIL ${JSON.stringify(setup)}`);
  console.log('D17_DIRECT_LIFECYCLE_SETTINGS_PASS');

  await fixture.evaluate((command)=>window.__fixture.appendAssistant(command,'direct-list-turn'),LIST_COMMAND);
  await waitUntil(async()=>await actionCount(fixture)>=1,'LIST_ACTION_NOT_ARMED');
  const beforeList=providerHits.length;await clickLatestAction(fixture);await waitUntil(async()=>providerHits.length===beforeList+1,'LIST_PROVIDER_NOT_CALLED');
  await waitUntil(async()=>(await fixtureState(fixture)).composer.startsWith('DIRECT_RESULT_V1'),'LIST_RESULT_NOT_FILLED');
  let fx=await fixtureState(fixture);assert.equal(fx.sendHistory.length,0);assert.equal(fx.sendCycles,0);assert.match(fx.composer,/"operation"\s*:\s*"listCampaigns"/);assert.equal(providerHits.at(-1).url,'/json/v501/campaigns');assert.deepEqual(JSON.parse(providerHits.at(-1).body).params.SelectionCriteria,{Ids:[77]});
  console.log('D17_DIRECT_MANUAL_LIST_AUTOSEND_FALSE_PASS');

  await fixture.click('#composer-submit-button');
  await waitUntil(async()=>(await fixtureState(fixture)).sendHistory.length===1,'MANUAL_USER_SEND_NOT_RECORDED');
  await delay(1000);
  await worker.evaluate(async()=>chrome.storage.local.set({wsmb_auto_send:true}));

  await fixture.evaluate((command)=>window.__fixture.appendAssistant(command,'direct-report-turn'),REPORT_COMMAND);
  await waitUntil(async()=>await actionCount(fixture)>=2,'REPORT_ACTION_NOT_ARMED');
  const beforeReport=providerHits.length;await clickLatestAction(fixture);await waitUntil(async()=>providerHits.length===beforeReport+1,'REPORT_PROVIDER_NOT_CALLED');
  await waitUntil(async()=>(await fixtureState(fixture)).sendHistory.filter((text)=>String(text).startsWith('DIRECT_RESULT_V1')).length>=2,'REPORT_RESULT_NOT_AUTOSENT',25000);
  fx=await fixtureState(fixture);const directSends=fx.sendHistory.filter((text)=>String(text).startsWith('DIRECT_RESULT_V1'));assert.equal(directSends.length,2);assert.equal(providerHits.at(-1).url,'/json/v501/reports');assert.equal(String(providerHits.at(-1).headers.processingmode||''),'online');
  console.log('D17_DIRECT_MANUAL_REPORT_AUTOSEND_TRUE_PASS');

  const hitsBeforeRemount=providerHits.length;await fixture.reload({waitUntil:'domcontentloaded',timeout:20000});await delay(1800);assert.equal(providerHits.length,hitsBeforeRemount);
  const persisted=await worker.evaluate(async(key)=>{const data=await chrome.storage.local.get(['wsmb_manual_modes','ymb_service_contexts']);return{manual:data.wsmb_manual_modes?.[key]===true,service:data.ymb_service_contexts?.[key]?.active_service||null};},KEY);assert.deepEqual(persisted,{manual:true,service:'direct'});
  console.log('D17_DIRECT_REMOUNT_NO_REPLAY_PASS');
  assert.equal(providerHits.length,2);const safe=JSON.stringify(providerHits.map((hit)=>({url:hit.url,method:hit.method,body:hit.body})));assert.equal(safe.includes('worker-lifecycle-secret'),false);
  console.log('D17_DIRECT_NO_DUPLICATE_PROVIDER_PASS');
  console.log('D20_DIRECT_LIFECYCLE_REAL_YANDEX_REQUESTS=0');
  console.log('PHASE5_DIRECT_MANUAL_LIFECYCLE_PASS');
}finally{if(browser)await browser.close().catch(()=>{});await new Promise((resolve)=>server.close(resolve));}
