import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';

const require=createRequire(pathToFileURL(path.resolve(process.env.YMB_PPTR_HOME,'package.json')));
const puppeteer=require('puppeteer');
const root=fs.realpathSync(process.env.YMB_BROWSER_CANDIDATE);
const out=path.resolve(process.env.YMB_BROWSER_EVIDENCE);
fs.mkdirSync(out,{recursive:true});
const fixture=fs.readFileSync(process.env.YMB_CHATGPT_FIXTURE,'utf8');
const CID='99999999-8888-4777-8666-555555555555';
const KEY='https://chatgpt.com|'+CID;
const PAGE_URL='https://chatgpt.com/c/'+CID;
const delay=ms=>new Promise(r=>setTimeout(r,ms));
const emit=v=>{const row={...v,time:new Date().toISOString()};fs.appendFileSync(path.join(out,'targeted.jsonl'),JSON.stringify(row)+'\n');console.log(JSON.stringify(row));};
async function until(fn,label,ms=20000){const end=Date.now()+ms;let last;while(Date.now()<end){try{last=await fn();if(last)return last;}catch(e){last=String(e)}await delay(100);}throw new Error(label+' last='+JSON.stringify(last));}
let browser,page,wakePage,extensionId,tabId;
async function rpc(message){
  if(!wakePage) throw new Error('WAKE_PAGE_NOT_READY');
  const reply=await wakePage.evaluate(msg=>new Promise(resolve=>{
    let done=false;const timer=setTimeout(()=>{if(!done){done=true;resolve({qa_timeout:true,response:null,error:null});}},3000);
    try{chrome.runtime.sendMessage(msg,response=>{const error=chrome.runtime.lastError?.message||null;if(done)return;done=true;clearTimeout(timer);resolve({qa_timeout:false,response:response??null,error});});}
    catch(e){if(done)return;done=true;clearTimeout(timer);resolve({qa_timeout:false,response:null,error:String(e)});}
  }),message);
  if(reply.qa_timeout) throw new Error('RUNTIME_MESSAGE_TIMEOUT '+String(message?.type||''));
  if(reply.error) throw new Error('RUNTIME_MESSAGE_ERROR '+reply.error);
  return reply.response;
}
async function worker(){
  for(let attempt=0;attempt<3;attempt++){
    let t=browser.targets().find(x=>x.type()==='service_worker'&&extensionId&&x.url()===`chrome-extension://${extensionId}/phase3_service_worker_bootstrap.js`);
    if(t){const w=await t.worker();if(w){try{await w.evaluate(()=>true);return w;}catch{}}}
    if(wakePage) await rpc({type:'WS_GET_STATE',conversation_key:KEY}).catch(()=>{});
    await delay(100);
    t=browser.targets().find(x=>x.type()==='service_worker'&&extensionId&&x.url()===`chrome-extension://${extensionId}/phase3_service_worker_bootstrap.js`);
    if(t){const w=await t.worker();if(w){try{await w.evaluate(()=>true);return w;}catch{}}}
  }
  throw new Error('LIVE_MV3_WORKER_UNAVAILABLE');
}
async function sw(fn,arg){for(let n=0;n<3;n++){const w=await worker();try{return await w.evaluate(fn,arg);}catch(e){if(n===2)throw e;await rpc({type:'WS_GET_STATE',conversation_key:KEY}).catch(()=>{});await delay(100);}}}
async function outboxViaRpc(){const r=await rpc({type:'WS_GET_OUTBOX',conversation_key:KEY});return r?.outbox||null;}
async function snapshot(){
  const dom=await page.evaluate(()=>({sends:__fixture.sends,files:__fixture.files,text:document.getElementById('prompt-textarea').value,status:document.getElementById('ymb-file-delivery-status')?.textContent||'',previews:[...document.querySelectorAll('#previews [role="group"]')].map(x=>({text:x.textContent,busy:x.getAttribute('aria-busy')})),userTurns:[...document.querySelectorAll('[data-message-author-role="user"]')].map(x=>({id:x.getAttribute('data-message-id'),text:x.textContent}))}));
  const e=await outboxViaRpc().catch(err=>({__qa_error:String(err)}));
  const state=e?.__qa_error?{worker_error:e.__qa_error}:e?{delivery_id:e.delivery_id,phase:e.phase,report_text:e.report_text,send_click_dispatched:e.send_click_dispatched,send_marker:e.send_marker,expected_attachment_names:e.expected_attachment_names,confirmation_message_id:e.confirmation_message_id}:null;
  return{dom,state};
}
async function reset(text=''){
  await sw(async key=>{await clearOutbox(key);const d=await chrome.storage.local.get('wsmb_manual_operations');const m=d.wsmb_manual_operations||{};delete m[key];await chrome.storage.local.set({wsmb_manual_operations:m});},KEY);
  await page.evaluate(text=>{__fixture.sends=[];__fixture.files=[];__fixture.inputs=0;__fixture.changes=0;__fixture.errors=[];document.querySelectorAll('[data-message-author-role="user"]').forEach(x=>x.remove());const c=document.getElementById('prompt-textarea');c.value=text;c.dispatchEvent(new Event('input',{bubbles:true}));document.getElementById('previews').replaceChildren();document.getElementById('upload-files').value='';__fixture.arm();},text);
}
async function stage(label,report){
  return sw(async({label,report,key,tabId})=>{const d='test15-'+label,ak='artifact-'+d;const descriptor=await YMBFileArtifactStore.stageTextArtifact({artifactKey:ak,deliveryId:d,filename:d+'.txt',text:'x'.repeat(1024*1024)});const s=(await chrome.storage.local.get('wsmb_manual_operations')).wsmb_manual_operations||{};s[key]={operation_id:d,delivery_id:d,status:'delivering',conversation_key:key,tab_id:tabId,active_service:'search',request_executed:false};await chrome.storage.local.set({wsmb_manual_operations:s});await putOutbox(key,{delivery_id:d,operation_id:d,type:'manual',tab_id:tabId,phase:'claimed',report_text:report,delivery_mode:'attachment_v2',artifact_descriptors:[descriptor],provider_executions:0});return{delivery_id:d,filename:descriptor.filename,bytes:descriptor.byte_length};},{label,report,key:KEY,tabId});
}
let failures=0;
async function run(name,fn){try{const details=await fn();emit({case:name,status:'PASS',...details});}catch(e){failures++;emit({case:name,status:'FAIL',error:String(e.stack||e),snapshot:await snapshot().catch(x=>({snapshot_error:String(x)}))});}}
try{
  browser=await puppeteer.launch({headless:false,pipe:true,enableExtensions:[root],protocolTimeout:120000,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--host-resolver-rules=MAP * ~NOTFOUND',`--disable-extensions-except=${root}`,`--load-extension=${root}`]});
  const first=await browser.waitForTarget(t=>t.type()==='service_worker'&&t.url().startsWith('chrome-extension://')&&t.url().endsWith('/phase3_service_worker_bootstrap.js'),{timeout:20000});
  extensionId=first.url().split('/')[2];
  wakePage=await browser.newPage();
  await wakePage.goto(`chrome-extension://${extensionId}/popup.html`,{waitUntil:'domcontentloaded',timeout:10000});
  page=await browser.newPage();
  await page.setRequestInterception(true);
  page.on('request',r=>{if(r.isNavigationRequest()&&r.url()===PAGE_URL)void r.respond({status:200,contentType:'text/html; charset=utf-8',body:fixture});else void r.abort();});
  await page.goto(PAGE_URL,{waitUntil:'domcontentloaded',timeout:20000});
  tabId=await until(()=>sw(async url=>(await chrome.tabs.query({})).find(t=>t.url===url)?.id||0,PAGE_URL),'TAB_NOT_FOUND',10000);
  await until(()=>sw(async({tabId})=>new Promise(ok=>chrome.tabs.sendMessage(tabId,{type:'WS_GET_IDENTITY'},r=>{void chrome.runtime.lastError;ok(r?.ok===true);})),{tabId}),'CONTENT_NOT_READY',10000);
  await sw(async({key,cid,tabId})=>{await chrome.storage.local.set({wsmb_conversation_bindings:{[key]:{binding_id:'targeted',revision:1,origin:'https://chatgpt.com',conversation_id:cid,conversation_key:key}},wsmb_manual_modes:{[key]:true},ymb_service_contexts:{[key]:{active_service:'search'}},wsmb_auto_send:true,ymb_settings_schema_version:5});await new Promise(ok=>chrome.tabs.sendMessage(tabId,{type:'WS_APPLY_MANUAL_MODE',conversation_key:key,enabled:true,active_service:'search'},()=>{void chrome.runtime.lastError;ok();}));},{key:KEY,cid:CID,tabId});
  emit({case:'venue_ready',status:'PASS',extension_id:extensionId,provider_calls:0});
  await run('test15_blank_composer_auto_send_exactly_once',async()=>{await reset('');const meta=await stage('auto','TEST15 patched auto file');await until(async()=>{const x=await page.evaluate(()=>__fixture.sends.length);return x===1?x:false;},'AUTO_SEND_NOT_OBSERVED',20000);await until(async()=>{const e=await outboxViaRpc();return e?.phase==='committed'?e.phase:false;},'OUTBOX_NOT_COMMITTED',10000);await delay(1500);const snap=await snapshot();assert.equal(snap.dom.sends.length,1);assert.equal(snap.dom.sends[0].text,'TEST15 patched auto file');assert.equal(snap.dom.sends[0].files.length,1);assert.equal(snap.dom.sends[0].files[0].name,meta.filename);assert.equal(snap.state.phase,'committed');assert.equal(snap.state.send_click_dispatched,true);return{meta,snapshot:snap};});
  await run('occupied_user_draft_is_preserved',async()=>{await reset('USER DRAFT EXACT');await stage('userdraft','TEST15 user draft file');await delay(2500);const snap=await snapshot();assert.equal(snap.dom.sends.length,0);assert.equal(snap.dom.text,'USER DRAFT EXACT');assert.equal(snap.state.phase,'claimed');return{snapshot:snap};});
  await run('bridge_owned_inline_collision_characterization',async()=>{await reset('SEARCH_ASYNC_BATCH_RESULT_V1 {"action":"exportPage","jobId":"owner-smoke-016-01","ok":true}');await stage('bridgeinline','TEST15 bridge inline file');await delay(3000);const snap=await snapshot();return{observed_send_count:snap.dom.sends.length,observed_composer:snap.dom.text,observed_phase:snap.state?.phase,snapshot:snap};});
}catch(e){failures++;emit({case:'launch_or_venue',status:'FAIL',error:String(e.stack||e),snapshot:page?await snapshot().catch(x=>({snapshot_error:String(x)})):null});}
finally{try{await browser?.close();}catch{}}
const rows=fs.existsSync(path.join(out,'targeted.jsonl'))?fs.readFileSync(path.join(out,'targeted.jsonl'),'utf8').trim().split(/\n/).filter(Boolean).map(JSON.parse):[];
const result={source_commit:'64c1016c179de52b6e950830877f0d42a446e5e8',product_tree_sha256:process.env.YMB_PRODUCT_TREE,zip_sha256:'3e23a70d09fab91f84cf3c9998499ce078f1467b46540dbac7fa07ac60a6765e',provider_calls:0,rows,failures,pass:failures===0&&rows.some(r=>r.case==='test15_blank_composer_auto_send_exactly_once'&&r.status==='PASS')};
fs.writeFileSync(path.join(out,'TARGETED_RESULT.json'),JSON.stringify(result,null,2)+'\n');
process.exitCode=result.pass?0:1;
