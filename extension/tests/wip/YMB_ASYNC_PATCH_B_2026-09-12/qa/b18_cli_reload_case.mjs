// B18 QA-only runtime.reload qualification on exact B17 product bytes.
// Before reload we establish the same controlled ChatGPT binding used by proven B15/B16.
// After reload we do NOT open an extension page or attach to the new worker. We reload the
// controlled chatgpt.com fixture, click the real extension content control and require a local
// async result to travel content -> worker -> delivery -> DOM. Zero provider requests.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';

const require=createRequire(pathToFileURL(path.resolve(process.env.YMB_PPTR_HOME,'package.json')));
const puppeteer=require('puppeteer');
const root=fs.realpathSync(process.env.YMB_BROWSER_CANDIDATE);
const out=path.resolve(process.env.YMB_BROWSER_EVIDENCE);
const fixture=fs.readFileSync(process.env.YMB_CHATGPT_FIXTURE,'utf8');
fs.mkdirSync(out,{recursive:true});
const TARGET='b20b74351d95becd67f32994e3e00899e9208b8c32c778a306f73f6703bfe508';
const CID='91919191-8282-4737-8646-555555555555';
const KEY='https://chatgpt.com|'+CID;
const PAGE_URL='https://chatgpt.com/c/'+CID;
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const delay=ms=>new Promise(r=>setTimeout(r,ms));
const emit=v=>{const line=JSON.stringify({...v,time:new Date().toISOString()})+'\n';fs.appendFileSync(path.join(out,'browser.jsonl'),line);process.stdout.write(line);};
async function until(fn,label,ms=15000){const end=Date.now()+ms;while(Date.now()<end){if(await fn())return;await delay(100);}throw new Error(label);}
function tree(){const rows=[];function walk(d){for(const x of fs.readdirSync(d,{withFileTypes:true})){const f=path.join(d,x.name);assert.equal(x.isSymbolicLink(),false);if(x.isDirectory())walk(f);else{assert.ok(x.isFile());rows.push([path.relative(root,f).split(path.sep).join('/'),hash(fs.readFileSync(f))]);}}}walk(root);rows.sort((a,b)=>a[0]<b[0]?-1:1);assert.equal(rows.length,67);return hash(Buffer.from(rows.map(([p,h])=>h+'  '+p+'\n').join('')));}
let browser,pid,monitor,deadline,peak=0,failed=0,stage='launch',page,workerTarget,worker,extensionId,tabId;const observed=new Set();
function memory(){if(!pid)return null;const raw=execFileSync('ps',['-eo','pid=,ppid=,rss='],{encoding:'utf8',timeout:1500}).trim();const rows=raw?raw.split('\n').map(l=>l.trim().split(/\s+/).map(Number)):[];const owned=new Set([pid]);let changed=true;while(changed){changed=false;for(const [p,pp] of rows)if(owned.has(pp)&&!owned.has(p)){owned.add(p);changed=true;}}const selected=rows.filter(r=>owned.has(r[0]));for(const r of selected)observed.add(r[0]);const rss=selected.reduce((s,r)=>s+r[2],0);peak=Math.max(peak,rss);return{rss_kib:rss,pids:selected.map(r=>r[0])};}
async function currentExtension(){const extensions=await browser.extensions();const list=[...extensions.values()].filter(e=>e.name==='Yandex Marketing Bridge — ChatGPT ↔ Yandex');assert.equal(list.length,1);return list[0];}
async function controlledNavigate(){
 if(!page){page=await browser.newPage();await page.setViewport({width:1200,height:900});await page.setRequestInterception(true);page.on('request',r=>{if(r.isNavigationRequest()&&r.url()===PAGE_URL)void r.respond({status:200,contentType:'text/html; charset=utf-8',body:fixture});else void r.abort();});}
 await page.goto(PAGE_URL,{waitUntil:'domcontentloaded',timeout:20000});
}
async function contentAction(){return page.evaluate(()=>{const host=document.getElementById('ymb-external-action-surface');const b=host?.shadowRoot?.querySelector('.ymb-action');return b?{present:true,disabled:b.disabled,text:b.textContent}:{present:false};});}
try{
 assert.equal(tree(),TARGET);
 browser=await puppeteer.launch({headless:false,pipe:true,enableExtensions:true,userDataDir:path.join(out,'owned-profile'),protocolTimeout:30000,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--host-resolver-rules=MAP * ~NOTFOUND',`--disable-extensions-except=${root}`,`--load-extension=${root}`]});
 pid=browser.process()?.pid;assert.ok(pid);deadline=setTimeout(()=>{void browser.close();},70000);monitor=setInterval(()=>{try{const m=memory();fs.appendFileSync(path.join(out,'rss.jsonl'),JSON.stringify({stage,...m})+'\n');}catch{}},250);
 const extension=await currentExtension();assert.equal(extension.enabled,true);assert.equal(extension.version,'0.1.4');extensionId=extension.id;
 workerTarget=await browser.waitForTarget(t=>t.type()==='service_worker'&&t.url().startsWith('chrome-extension://'+extensionId+'/')&&t.url().endsWith('/phase3_service_worker_bootstrap.js'),{timeout:15000});worker=await workerTarget.worker();assert.ok(worker);
 emit({case:'exact_cli_extension_and_initial_worker',status:'PASS',extension_id:extensionId,version:extension.version,tree:TARGET,memory:memory()});
 await controlledNavigate();
 tabId=await worker.evaluate(async url=>(await chrome.tabs.query({})).find(t=>t.url===url)?.id||null,PAGE_URL);assert.ok(tabId);
 await until(async()=>worker.evaluate(id=>new Promise(ok=>chrome.tabs.sendMessage(id,{type:'WS_GET_IDENTITY'},r=>{void chrome.runtime.lastError;ok(r?.ok===true);})),tabId),'CONTENT_NOT_READY');
 const before=await worker.evaluate(async({key,cid,tabId})=>{
   await chrome.storage.local.set({wsmb_conversation_bindings:{[key]:{binding_id:'b18-reload',revision:1,origin:'https://chatgpt.com',conversation_id:cid,conversation_key:key}},wsmb_manual_modes:{[key]:true},ymb_service_contexts:{[key]:{active_service:'search'}},wsmb_auto_send:true,ymb_settings_schema_version:5});
   await YMBCredentialRuntime.save('search',{api_key:'QA_B18_RELOAD_SEARCH',folder_id:'qa-only',check_state:'PRESENT'});
   await new Promise(ok=>chrome.tabs.sendMessage(tabId,{type:'WS_APPLY_MANUAL_MODE',conversation_key:key,enabled:true,active_service:'search'},()=>{void chrome.runtime.lastError;ok();}));
   const contexts=await chrome.runtime.getContexts({contextTypes:['BACKGROUND']});return{context:contexts[0]?.contextId||null,credential:(await YMBCredentialRuntime.settings()).credentials.search.api_key};
 },{key:KEY,cid:CID,tabId});
 assert.ok(before.context);assert.equal(before.credential,'QA_B18_RELOAD_SEARCH');emit({case:'pre_reload_controlled_binding_and_settings',status:'PASS',context:before.context});
 stage='runtime_reload';
 await worker.client.send('Runtime.evaluate',{expression:'setTimeout(()=>chrome.runtime.reload(),50); true',returnByValue:true,awaitPromise:false});
 await new Promise((resolve,reject)=>{const timer=setTimeout(()=>{browser.off('targetdestroyed',on);reject(new Error('OLD_WORKER_NOT_DESTROYED'));},10000);const on=t=>{if(t===workerTarget){clearTimeout(timer);browser.off('targetdestroyed',on);resolve();}};browser.on('targetdestroyed',on);});
 await delay(600);
 const afterExtension=await currentExtension();assert.equal(afterExtension.id,extensionId);assert.equal(afterExtension.enabled,true);assert.equal(afterExtension.version,'0.1.4');emit({case:'extension_registry_after_runtime_reload',status:'PASS',same_id:true,enabled:true,version:'0.1.4'});
 stage='post_reload_real_content_action';
 await controlledNavigate();
 await page.evaluate(()=>{__fixture.files=[];__fixture.sends=[];__fixture.inputs=0;__fixture.changes=0;document.getElementById('conversation-root').replaceChildren();__fixture.append('SEARCH_ASYNC_BATCH_API_V1\n'+JSON.stringify({action:'start',jobId:'b18-reload-local',queries:['fixture'],confirmBillable:true,maxRequests:1,maxCostRub:1}));});
 await until(async()=>{const a=await contentAction();return a.present&&!a.disabled;},'POST_RELOAD_YANDEX_CONTROL_NOT_READY',20000);
 await page.evaluate(()=>document.getElementById('ymb-external-action-surface').shadowRoot.querySelector('.ymb-action').click());
 await until(async()=>page.evaluate(()=>__fixture.sends.length===1),'POST_RELOAD_LOCAL_RESULT_NOT_SENT',20000);
 const result=await page.evaluate(()=>({sends:__fixture.sends.map(x=>({text:x.text,files:x.files?.length||0})),changes:__fixture.changes,inputs:__fixture.inputs,status:document.getElementById('ymb-file-delivery-status')?.textContent||''}));
 assert.equal(result.sends.length,1);assert.match(result.sends[0].text,/SEARCH_ASYNC_BATCH_RESULT_V1/);assert.ok(!result.sends[0].text.includes('QA_B18_RELOAD_SEARCH'));assert.equal(result.sends[0].files,0);
 await until(async()=>{const ext=await currentExtension();return (await ext.workers()).length===1;},'NEW_WORKER_NOT_OBSERVED');
 assert.equal(tree(),TARGET);emit({case:'post_reload_content_worker_delivery',status:'PASS',same_extension_id:true,local_result_sent:1,provider_calls:0,secret_exposure:false,new_worker_observed:true,product_changed:false});
}catch(error){failed++;emit({case:stage,status:'FAIL_QUALIFICATION',error:String(error.stack||error),release_allowed:false});process.exitCode=1;}
finally{
 clearInterval(monitor);clearTimeout(deadline);if(browser){try{await browser.close();}catch{}}
 const remaining=[];for(const p of observed){try{const stat=fs.readFileSync('/proc/'+p+'/stat','utf8');const state=stat.slice(stat.lastIndexOf(')')+2).split(' ')[0];if(state!=='Z')remaining.push(p);}catch{}}
 emit({case:'owned_browser_cleanup',status:remaining.length?'FAIL':'PASS',remaining,peak_owned_rss_kib:peak,failed,release_allowed:false});if(remaining.length)process.exitCode=1;
}
