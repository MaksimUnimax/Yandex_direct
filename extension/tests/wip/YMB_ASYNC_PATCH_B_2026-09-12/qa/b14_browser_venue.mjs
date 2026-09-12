// B14 development venue qualification. One fresh owned Chrome; unchanged B13 ZIP.
// No ChatGPT page, user profile, provider credentials/calls, policy changes or release.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const require=createRequire(pathToFileURL(path.resolve(process.env.YMB_PPTR_HOME,'package.json')));
const puppeteer=require('puppeteer');
const root=fs.realpathSync(process.env.YMB_BROWSER_CANDIDATE);
const out=path.resolve(process.env.YMB_BROWSER_EVIDENCE);
fs.mkdirSync(out,{recursive:true});
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const target='f591b39a381993c44284561236b9c5a278761db3d6b04059c59974e037c33f47';
const emit=v=>{const s=JSON.stringify({...v,time:new Date().toISOString()})+'\n';fs.appendFileSync(path.join(out,'browser.jsonl'),s);process.stdout.write(s);};
function tree(){const rows=[];function walk(dir){for(const x of fs.readdirSync(dir,{withFileTypes:true})){const f=path.join(dir,x.name);assert.equal(x.isSymbolicLink(),false);if(x.isDirectory())walk(f);else{assert.ok(x.isFile());rows.push([path.relative(root,f).split(path.sep).join('/'),hash(fs.readFileSync(f))]);}}}walk(root);rows.sort((a,b)=>a[0]<b[0]?-1:1);assert.equal(rows.length,67);return hash(Buffer.from(rows.map(([p,h])=>h+'  '+p+'\n').join('')));}
assert.equal(tree(),target);
let browser,monitor,deadline,pid,stage='launch',resourceStop=false,timedOut=false,peak=0;
const observedPids=new Set();
function memory(){if(!pid)return null;const rows=execFileSync('ps',['-eo','pid=,ppid=,rss='],{encoding:'utf8',timeout:1500}).trim().split('\n').map(l=>l.trim().split(/\s+/).map(Number));const owned=new Set([pid]);let changed=true;while(changed){changed=false;for(const [p,pp] of rows)if(owned.has(pp)&&!owned.has(p)){owned.add(p);changed=true;}}const selected=rows.filter(r=>owned.has(r[0]));for(const row of selected)observedPids.add(row[0]);const rssKiB=selected.reduce((s,r)=>s+r[2],0);peak=Math.max(peak,rssKiB);return{rss_kib:rssKiB,pids:selected.map(r=>r[0])};}
let errors=[];
try{
 browser=await puppeteer.launch({headless:false,pipe:true,enableExtensions:[root],protocolTimeout:30000,args:[
  '--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking',
  '--host-resolver-rules=MAP * ~NOTFOUND',`--disable-extensions-except=${root}`,`--load-extension=${root}`
 ]});
 pid=browser.process()?.pid;assert.ok(pid);
 deadline=setTimeout(()=>{timedOut=true;void browser.close();},150000);
 monitor=setInterval(()=>{try{const m=memory();fs.appendFileSync(path.join(out,'rss.jsonl'),JSON.stringify({stage,...m})+'\n');if(m.rss_kib>1572864){resourceStop=true;void browser.close();}}catch{}},250);
 emit({case:'owned_chrome_launch',status:'PASS',chrome:await browser.version(),puppeteer:require('puppeteer/package.json').version,pid,exact_tree:target});
 stage='worker_load';
 const t=await browser.waitForTarget(t=>t.type()==='service_worker'&&t.url().startsWith('chrome-extension://')&&t.url().endsWith('/phase3_service_worker_bootstrap.js'),{timeout:20000});
 const w=await t.worker();assert.ok(w);
 w.on('error',e=>errors.push(String(e)));
 const ready=await w.evaluate(()=>({binding:YMBSearchAdmissionBinding?.ready,async:YMBSearchAsyncWorkerIntegration?.ready,provider:YMBSearchAsyncWorkerIntegration?.providerEnabled,store:!!YMBSearchAsyncStore?.createJob,artifacts:!!YMBFileArtifactStore?.stageTextArtifact,permissions:chrome.runtime.getManifest().host_permissions}));
 assert.equal(ready.binding,true);assert.equal(ready.async,true);assert.equal(ready.provider,false);assert.equal(ready.store,true);assert.equal(ready.artifacts,true);assert.ok(!ready.permissions.includes('https://operation.api.cloud.yandex.net/*'));
 emit({case:'exact_extension_worker_and_modules',status:'PASS',readiness:ready,extension_url:t.url(),memory:memory()});
 // Guard accidental transport after attaching; no API keys are ever installed.
 await w.evaluate(()=>{globalThis.__b14_network_calls=0;globalThis.fetch=async()=>{__b14_network_calls++;throw new Error('B14_NETWORK_FORBIDDEN');};});
 stage='real_idb_states';
 const state=await w.evaluate(async()=>{
  const S=YMBSearchAsyncStore,owner='b14-fixture-owner',jobId='b14-fixture-job';
  await S.createJob({jobId,owner,queries:['one','two'],parameters:{region:'225'},folderId:'qa-only',maxRequests:2,maxCostMicrorub:200,unitCostMicrorub:100,now:1});
  const first=await S.claim({jobId,owner,workerId:'fixture-A',attemptId:'first',kind:'submit',now:1});
  await S.finishSubmit({jobId,owner,index:first.item.index,attemptId:'first',outcome:'accepted',operationId:'qa-op',nextPollAt:2,now:1});
  await S.claim({jobId,owner,workerId:'fixture-A',attemptId:'second',kind:'submit',now:2});
  await S.recover({jobId,owner,workerId:'fixture-B',now:3});
  const blocked=await S.claim({jobId,owner,workerId:'fixture-B',attemptId:'third',kind:'submit',now:3});
  let denied=false;try{await S.getSummary(jobId,'other-owner');}catch(e){denied=e.code==='ASYNC_WRONG_OWNER';}
  return{summary:await S.getSummary(jobId,owner),rows:(await S.pageItems(jobId,owner)).rows.length,blocked,denied};
 });
 assert.equal(state.summary.counts.WAITING,1);assert.equal(state.summary.counts.UNKNOWN,1);assert.equal(state.rows,2);assert.equal(state.blocked.allowed,false);assert.equal(state.denied,true);
 emit({case:'actual_indexeddb_atomic_state_and_owner',status:'PASS',state,network:'no provider; synthetic state outcomes only'});
 // This records real Chrome/IDB storage behavior, NOT content/File/DataTransfer delivery.
 for(const [cycle,mib] of [1,10,32,64,64,64].entries()){
  stage=`artifact_${mib}MiB_cycle${cycle+1}`;const before=memory(),started=Date.now();
  const r=await w.evaluate(async({cycle,mib})=>{
   const A=YMBFileArtifactStore,key='b14-artifact-'+cycle;let text='x'.repeat(mib*1024*1024);
   const d=await A.stageTextArtifact({artifactKey:key,deliveryId:key,filename:'qa.txt',text});text=null;
   const get=IDBObjectStore.prototype.get,all=IDBObjectStore.prototype.getAll;let reads=0,bytes=0,maxChunk=0;
   IDBObjectStore.prototype.get=function(...a){if(this.name==='chunks')reads++;return get.apply(this,a);};
   IDBObjectStore.prototype.getAll=function(){throw new Error('B14_FULL_STORE_READ_FORBIDDEN');};
   try{for(let i=0;i<d.chunk_count;i++){const c=await A.getChunk(key,i);const h=[...new Uint8Array(await crypto.subtle.digest('SHA-256',c.bytes))].map(b=>b.toString(16).padStart(2,'0')).join('');if(h!==c.sha256)throw new Error('B14_CHUNK_HASH_MISMATCH');bytes+=c.bytes.byteLength;maxChunk=Math.max(maxChunk,c.bytes.byteLength);}}
   finally{IDBObjectStore.prototype.get= get;IDBObjectStore.prototype.getAll=all;}
   await A.deleteArtifact(key);
   const req=r=>new Promise((resolve,reject)=>{r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error);});
   const db=await req(indexedDB.open(A.DB_NAME,A.DB_VERSION));let remaining;try{remaining=await req(db.transaction('chunks','readonly').objectStore('chunks').index('artifact_key').count(IDBKeyRange.only(key)));}finally{db.close();}
   return{bytes,chunks:d.chunk_count,reads,maxChunk,remaining,meta_absent:!(await A.getMeta(key)),provider_calls:__b14_network_calls};
  },{cycle,mib});
  assert.equal(r.bytes,mib*1024*1024);assert.equal(r.reads,r.chunks);assert.ok(r.maxChunk<=256*1024);assert.equal(r.remaining,0);assert.equal(r.meta_absent,true);assert.equal(r.provider_calls,0);
  await new Promise(r=>setTimeout(r,500));emit({case:'real_idb_artifact_cycle',status:'PASS',cycle:cycle+1,mib,...r,before,after:memory(),duration_ms:Date.now()-started,peak_owned_rss_kib:peak,scope:'store/read/checksum/delete only; not File/DataTransfer or UI'});
 }
 assert.equal(tree(),target);assert.equal(resourceStop,false);assert.equal(timedOut,false);
 emit({case:'immutable_tree_and_bounded_venue_complete',status:'PASS',peak_owned_rss_kib:peak,worker_errors:errors,independent_gate:false,full_resource_gate:false,release_allowed:false});
}catch(error){emit({case:stage,status:resourceStop?'FAIL_RESOURCE':timedOut?'FAIL_HARNESS_TIMEOUT':stage==='launch'?'BLOCKED_VENUE':'FAIL_QUALIFICATION',error:String(error.stack||error),release_allowed:false});process.exitCode=1;}
finally{
 clearInterval(monitor);clearTimeout(deadline);
 if(browser){try{await browser.close();}catch{}}
 let ownedLeft=[];for(const p of observedPids){try{const stat=fs.readFileSync('/proc/'+p+'/stat','utf8');if(stat.slice(stat.lastIndexOf(')')+2).split(' ')[0]!=='Z')ownedLeft.push(p);}catch{}}
 emit({case:'owned_browser_cleanup',status:ownedLeft.length?'FAIL':'PASS',owned_pids_remaining:ownedLeft,release_allowed:false});if(ownedLeft.length)process.exitCode=1;
}
