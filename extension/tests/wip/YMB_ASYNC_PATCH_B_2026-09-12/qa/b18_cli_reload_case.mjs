// B18 QA-only runtime.reload qualification on exact B17 product bytes.
// We deliberately never call worker()/evaluate on the PRE-reload worker. State is saved through
// the real popup/runtime messaging. After reload, and only then, we attach to the newly exposed
// worker and prove a new background context plus durable settings. No post-reload popup/navigation.
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
fs.mkdirSync(out,{recursive:true});
const TARGET='b20b74351d95becd67f32994e3e00899e9208b8c32c778a306f73f6703bfe508';
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const delay=ms=>new Promise(r=>setTimeout(r,ms));
const emit=v=>{const line=JSON.stringify({...v,time:new Date().toISOString()})+'\n';fs.appendFileSync(path.join(out,'browser.jsonl'),line);process.stdout.write(line);};
async function until(fn,label,ms=15000){const end=Date.now()+ms;while(Date.now()<end){const value=await fn();if(value)return value;await delay(100);}throw new Error(label);}
function tree(){const rows=[];function walk(d){for(const x of fs.readdirSync(d,{withFileTypes:true})){const f=path.join(d,x.name);assert.equal(x.isSymbolicLink(),false);if(x.isDirectory())walk(f);else{assert.ok(x.isFile());rows.push([path.relative(root,f).split(path.sep).join('/'),hash(fs.readFileSync(f))]);}}}walk(root);rows.sort((a,b)=>a[0]<b[0]?-1:1);assert.equal(rows.length,67);return hash(Buffer.from(rows.map(([p,h])=>h+'  '+p+'\n').join('')));}
let browser,pid,monitor,deadline,peak=0,failed=0,stage='launch';const observed=new Set();
function memory(){if(!pid)return null;const raw=execFileSync('ps',['-eo','pid=,ppid=,rss='],{encoding:'utf8',timeout:1500}).trim();const rows=raw?raw.split('\n').map(l=>l.trim().split(/\s+/).map(Number)):[];const owned=new Set([pid]);let changed=true;while(changed){changed=false;for(const [p,pp] of rows)if(owned.has(pp)&&!owned.has(p)){owned.add(p);changed=true;}}const selected=rows.filter(r=>owned.has(r[0]));for(const r of selected)observed.add(r[0]);const rss=selected.reduce((s,r)=>s+r[2],0);peak=Math.max(peak,rss);return{rss_kib:rss,pids:selected.map(r=>r[0])};}
async function currentExtension(){const extensions=await browser.extensions();const list=[...extensions.values()].filter(e=>e.name==='Yandex Marketing Bridge — ChatGPT ↔ Yandex');assert.equal(list.length,1);return list[0];}
async function popupBeforeReload(extension,targetPage){
 const waiting=browser.waitForTarget(t=>t.type()==='page'&&t.url().startsWith('chrome-extension://'+extension.id+'/')&&t.url().endsWith('/popup.html'),{timeout:8000});
 await extension.triggerAction(targetPage);const target=await waiting;const page=await target.asPage();assert.ok(page);await page.waitForFunction(()=>document.readyState==='complete'||document.readyState==='interactive',{timeout:5000});return page;
}
try{
 assert.equal(tree(),TARGET);
 browser=await puppeteer.launch({headless:false,pipe:true,enableExtensions:true,userDataDir:path.join(out,'owned-profile'),protocolTimeout:20000,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--host-resolver-rules=MAP * ~NOTFOUND',`--disable-extensions-except=${root}`,`--load-extension=${root}`]});
 pid=browser.process()?.pid;assert.ok(pid);deadline=setTimeout(()=>{void browser.close();},60000);monitor=setInterval(()=>{try{const m=memory();fs.appendFileSync(path.join(out,'rss.jsonl'),JSON.stringify({stage,...m})+'\n');}catch{}},250);
 const extension=await currentExtension();assert.equal(extension.enabled,true);assert.equal(extension.version,'0.1.4');const extensionId=extension.id;
 // Service-worker target may be visible to Puppeteer, but this test does not obtain/evaluate it pre-reload.
 const visibleBefore=browser.targets().filter(t=>t.type()==='service_worker'&&t.url().startsWith('chrome-extension://'+extensionId+'/')).length;
 const targetPage=await browser.newPage();await targetPage.goto('data:text/html,<title>B18 reload action target</title><body>target</body>',{waitUntil:'domcontentloaded'});
 const popup=await popupBeforeReload(extension,targetPage);
 const before=await popup.evaluate(async()=>{
   for(const s of ['wordstat','search','webmaster','metrika','direct']){
     const credential=['wordstat','search'].includes(s)?{api_key:'B18_RELOAD_'+s,folder_id:'qa-only'}:{oauth_token:'B18_RELOAD_'+s};
     const r=await chrome.runtime.sendMessage({type:'YMB_SAVE_SERVICE_CREDENTIAL',service:s,credential});if(!r?.ok)throw new Error('SAVE_FAILED_'+s);
   }
   const backup=await chrome.runtime.sendMessage({type:'WS_EXPORT_BACKUP'});if(!backup?.ok)throw new Error('BACKUP_FAILED');
   const contexts=await chrome.runtime.getContexts({contextTypes:['BACKGROUND']});
   return{hash:backup.backup.settings_sha256,context:contexts[0]?.contextId||null,version:chrome.runtime.getManifest().version,saved_five:true};
 });
 assert.ok(before.context);emit({case:'pre_reload_popup_messages_no_worker_evaluate',status:'PASS',extension_id:extensionId,before,visible_worker_targets:visibleBefore,worker_evaluate_calls:0,tree:TARGET,memory:memory()});
 stage='runtime_reload';
 await popup.evaluate(()=>{setTimeout(()=>chrome.runtime.reload(),50);return true;});
 await delay(900);
 const afterExtension=await currentExtension();assert.equal(afterExtension.id,extensionId);assert.equal(afterExtension.enabled,true);assert.equal(afterExtension.version,before.version);
 emit({case:'extension_registry_after_runtime_reload',status:'PASS',same_id:true,enabled:true,version:afterExtension.version});
 stage='new_worker_state_after_reload';
 const workers=await until(async()=>{const list=await afterExtension.workers();return list.length===1?list:null;},'NEW_WORKER_NOT_AVAILABLE',12000);
 const worker=workers[0];
 const after=await worker.evaluate(async()=>{
   const backup=await new Promise(resolve=>chrome.runtime.sendMessage({type:'WS_EXPORT_BACKUP'},resolve));if(!backup?.ok)throw new Error('BACKUP_AFTER_FAILED');
   const contexts=await chrome.runtime.getContexts({contextTypes:['BACKGROUND']});const c=backup.backup.settings.credentials;
   const publicState=await new Promise(resolve=>chrome.runtime.sendMessage({type:'WS_GET_STATE'},resolve));
   return{hash:backup.backup.settings_sha256,context:contexts[0]?.contextId||null,version:chrome.runtime.getManifest().version,all_five_same:['wordstat','search','webmaster','metrika','direct'].every(s=>(c[s].api_key||c[s].oauth_token)==='B18_RELOAD_'+s),public_secret_exposure:JSON.stringify(publicState).includes('B18_RELOAD_'),worker_session:globalThis.WORKER_SESSION_ID||null};
 });
 assert.ok(after.context);assert.notEqual(after.context,before.context);assert.equal(after.hash,before.hash);assert.equal(after.version,before.version);assert.equal(after.all_five_same,true);assert.equal(after.public_secret_exposure,false);assert.ok(after.worker_session);
 assert.equal(tree(),TARGET);emit({case:'runtime_reload_new_worker_and_persisted_state',status:'PASS',before,after,product_changed:false,pre_reload_worker_evaluate_calls:0,post_reload_worker_attached:true,direct_extension_navigation_after_reload:false,popup_action_after_reload:false,real_provider_calls:0});
}catch(error){failed++;emit({case:stage,status:'FAIL_QUALIFICATION',error:String(error.stack||error),release_allowed:false});process.exitCode=1;}
finally{
 clearInterval(monitor);clearTimeout(deadline);if(browser){try{await browser.close();}catch{}}
 const remaining=[];for(const p of observed){try{const stat=fs.readFileSync('/proc/'+p+'/stat','utf8');const state=stat.slice(stat.lastIndexOf(')')+2).split(' ')[0];if(state!=='Z')remaining.push(p);}catch{}}
 emit({case:'owned_browser_cleanup',status:remaining.length?'FAIL':'PASS',remaining,peak_owned_rss_kib:peak,failed,release_allowed:false});if(remaining.length)process.exitCode=1;
}
