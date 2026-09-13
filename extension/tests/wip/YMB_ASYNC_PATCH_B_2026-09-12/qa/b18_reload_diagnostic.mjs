// B18 bounded classification probe. Unchanged B17 versus minimal MV3 control.
// Exactly one browser owned by this test. No credentials/provider calls/policy edits.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
const require=createRequire(pathToFileURL(path.join(process.env.YMB_PPTR_HOME,'package.json'))),puppeteer=require('puppeteer');
const root=fs.realpathSync(process.env.YMB_BROWSER_CANDIDATE),out=path.resolve(process.env.YMB_BROWSER_EVIDENCE);
fs.mkdirSync(out,{recursive:true});const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const target='b20b74351d95becd67f32994e3e00899e9208b8c32c778a306f73f6703bfe508';
const emit=o=>{const s=JSON.stringify({...o,time:new Date().toISOString()})+'\n';fs.appendFileSync(path.join(out,'diagnostic.jsonl'),s);process.stdout.write(s);};
const delay=ms=>new Promise(r=>setTimeout(r,ms));
function tree(){const a=[];function walk(d){for(const f of fs.readdirSync(d,{withFileTypes:true})){assert.ok(!f.isSymbolicLink());const p=path.join(d,f.name);if(f.isDirectory())walk(p);else a.push([path.relative(root,p),hash(fs.readFileSync(p))]);}}walk(root);a.sort((a,b)=>a[0]<b[0]?-1:1);assert.equal(a.length,67);return hash(a.map(([p,h])=>h+'  '+p+'\n').join(''));}
assert.equal(tree(),target);
const control=path.join(out,'minimal-control');fs.mkdirSync(control);
const controlFiles={
 'manifest.json':JSON.stringify({manifest_version:3,name:'B18 reload diagnostic control',version:'1.0.0',permissions:['storage'],background:{service_worker:'worker.js'},action:{default_popup:'popup.html'}}),
 'worker.js':"globalThis.session=crypto.randomUUID();chrome.runtime.onMessage.addListener((m,s,r)=>r({session}));chrome.runtime.onInstalled.addListener(()=>{});",
 'popup.html':'<!doctype html><meta charset="utf-8"><title>B18 control</title>'
};
for(const [n,b]of Object.entries(controlFiles))fs.writeFileSync(path.join(control,n),b);
let browser,pid,timer,watchdog,failed=0,peak=0;const owned=new Map();
function processes(){const rows=execFileSync('ps',['-eo','pid=,ppid=,rss='],{encoding:'utf8',timeout:1500}).trim().split('\n').map(l=>l.trim().split(/\s+/).map(Number));const ids=new Set([pid]);for(let last=0;last!==ids.size;){last=ids.size;for(const [p,pp]of rows)if(ids.has(pp))ids.add(p);}const all=rows.filter(a=>ids.has(a[0]));for(const [p]of all){try{const st=fs.readFileSync('/proc/'+p+'/stat','utf8').split(') ')[1].split(' ');owned.set(p,st[19]);}catch{}}const rss=all.reduce((s,a)=>s+a[2],0);peak=Math.max(peak,rss);return rss;}
const inspect=async(t,expression)=>{let c;try{c=await t.createCDPSession();return await c.send('Runtime.evaluate',{expression,returnByValue:true},{timeout:1500});}catch(e){return{error:String(e.message).slice(0,240)};}finally{if(c)await c.detach().catch(()=>{});}};
try{
 browser=await puppeteer.launch({headless:false,pipe:true,enableExtensions:true,protocolTimeout:5000,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--host-resolver-rules=MAP * ~NOTFOUND']});pid=browser.process().pid;
 watchdog=setTimeout(()=>void browser.close(),100000);
 timer=setInterval(()=>{try{const rss=processes();if(rss>2097152){failed++;emit({stage:'resource',status:'FAIL_RESOURCE',rss});void browser.close();}}catch{}},500);
 const outcomes=[];
 for(const [label,folder,script]of [['control',control,'worker.js'],['B17',root,'phase3_service_worker_bootstrap.js']]){
  const id=await browser.installExtension(folder),url=`chrome-extension://${id}/${script}`;
  const t=await browser.waitForTarget(t=>t.type()==='service_worker'&&t.url()===url,{timeout:10000}),w=await t.worker();
  const expression=label==='B17'?'JSON.stringify({session:WORKER_SESSION_ID,ready:YMBSearchAdmissionBinding.ready})':'JSON.stringify({session:globalThis.session,ready:true})';
  const before=JSON.parse(await w.evaluate(expression));
  const rawBefore=await inspect(t,expression);
  await w.evaluate(()=>chrome.storage.local.set({b18_probe_marker:'kept'}));
  const p=await browser.newPage();await p.goto(`chrome-extension://${id}/popup.html`,{waitUntil:'domcontentloaded',timeout:5000});
  const events=[];const cb=t=>{if(t.url().startsWith(`chrome-extension://${id}/`))events.push({type:t.type(),url:t.url()});};
  browser.on('targetcreated',cb);browser.on('targetdestroyed',cb);
  emit({stage:'before',label,status:'RECORDED',before,rawBefore,tree:tree()});
  await p.evaluate(()=>{setTimeout(()=>chrome.runtime.reload(),50);return true;});await delay(500);
  let after=null,popup=null;const samples=[];
  for(let i=0;i<8;i++){
   const list=[];for(const tar of browser.targets())if(tar.type()==='service_worker'&&tar.url()===url)list.push(await inspect(tar,expression));
   const info=[...(await browser.extensions()).values()].filter(x=>x.id===id).map(x=>({id:x.id,name:x.name,version:x.version}));
   samples.push({i,list,installed:info});
   const found=list.find(r=>{try{return JSON.parse(r.result?.value).session!==before.session&&JSON.parse(r.result.value).ready===true;}catch{return false;}});
   if(found){after=JSON.parse(found.result.value);break;}await delay(200);
  }
  try{const q=await browser.newPage();try{await q.goto(`chrome-extension://${id}/popup.html`,{waitUntil:'domcontentloaded',timeout:4000});popup=await q.evaluate(async()=>({marker:(await chrome.storage.local.get('b18_probe_marker')).b18_probe_marker,id:chrome.runtime.id}));}finally{await q.close().catch(()=>{});}}catch(e){popup={error:String(e.message)};}
  emit({stage:'attached_reload',label,status:after&&popup?.marker==='kept'?'PASS_DIAGNOSTIC':'UNRESOLVED',after,popup,events,samples});
  outcomes.push({label,passed:!!(after&&popup?.marker==='kept')});
  browser.off('targetcreated',cb);browser.off('targetdestroyed',cb);
  // A debugger attachment can keep old execution context alive. Detaching here
  // is diagnostic only; it must never be silently counted as the original test.
  if(!after){try{await w.client.detach();}catch{}await delay(500);const list=[];for(const tar of browser.targets())if(tar.type()==='service_worker'&&tar.url()===url)list.push(await inspect(tar,expression));emit({stage:'after_explicit_debugger_detach',label,status:'RECORDED',list});}
  await browser.uninstallExtension(id).catch(e=>emit({stage:'uninstall',label,error:String(e.message)}));
 }
 assert.equal(tree(),target);emit({stage:'comparison',status:'DIAGNOSTIC_COMPLETE',outcomes,product_changed:false,release_allowed:false});
}catch(e){failed++;emit({stage:'probe',status:'FAIL_HARNESS',error:String(e.stack||e)});}
finally{
 clearInterval(timer);clearTimeout(watchdog);if(browser)await browser.close().catch(()=>{});
 function living(){const out=[];for(const [p,start]of owned){try{const s=fs.readFileSync('/proc/'+p+'/stat','utf8').split(') ')[1].split(' ');if(s[19]===start&&s[0]!=='Z')out.push({pid:p,state:s[0]});}catch{}}return out;}
 const initial=living();let rest=initial;const begin=Date.now();while(rest.length&&Date.now()-begin<2000){await delay(100);rest=living();}
 emit({stage:'cleanup',status:rest.length?'FAIL':'PASS',initial,remaining:rest,peak_rss_kib:peak,forced_kill:false});if(rest.length)failed++;
 process.exitCode=failed?1:0;
}
