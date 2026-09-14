import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';

const require=createRequire(pathToFileURL(path.resolve(process.env.YMB_PPTR_HOME,'package.json')));
const puppeteer=require('puppeteer');
const out=path.resolve(process.env.YMB_MEMORY_EVIDENCE);fs.mkdirSync(out,{recursive:true});
const OWNER='https://chatgpt.com|aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee';
const DB='ymb_search_async_items_v2';
const delay=ms=>new Promise(r=>setTimeout(r,ms));
const emit=row=>{const v={...row,time:new Date().toISOString()};fs.appendFileSync(path.join(out,'lifecycle.jsonl'),JSON.stringify(v)+'\n');console.log(JSON.stringify(v));};

function rssTree(pid){
  const raw=execFileSync('ps',['-eo','pid=,ppid=,rss='],{encoding:'utf8',timeout:2000}).trim();
  const rows=raw?raw.split('\n').map(x=>x.trim().split(/\s+/).map(Number)):[];
  const owned=new Set([pid]);let changed=true;
  while(changed){changed=false;for(const [p,pp] of rows)if(owned.has(pp)&&!owned.has(p)){owned.add(p);changed=true;}}
  const selected=rows.filter(x=>owned.has(x[0]));
  return {rss_kib:selected.reduce((s,x)=>s+x[2],0),processes:selected.length,pids:selected.map(x=>x[0])};
}

async function launch(root){
  const browser=await puppeteer.launch({headless:false,pipe:true,enableExtensions:[root],protocolTimeout:180000,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--host-resolver-rules=MAP * ~NOTFOUND','--js-flags=--expose-gc',`--disable-extensions-except=${root}`,`--load-extension=${root}`]});
  const target=await browser.waitForTarget(t=>t.type()==='service_worker'&&t.url().startsWith('chrome-extension://')&&t.url().endsWith('/phase3_service_worker_bootstrap.js'),{timeout:20000});
  const worker=await target.worker();assert.ok(worker);await worker.evaluate(()=>{globalThis.__memFetchCalls=0;const orig=globalThis.fetch;globalThis.__memOrigFetch=orig;globalThis.fetch=(...args)=>{globalThis.__memFetchCalls++;return Promise.reject(new Error('MEM_QA_NETWORK_BLOCKED'));};});
  return{browser,id:target.url().split('/')[2],pid:browser.process().pid,worker};
}

async function installCounters(page){
  await page.evaluateOnNewDocument(()=>{
    globalThis.__ymbMemQA={result_open_cursor:0,result_count:0,item_open_cursor:0,item_count:0};
    const oc=IDBObjectStore.prototype.openCursor;IDBObjectStore.prototype.openCursor=function(...args){if(this.name==='results')__ymbMemQA.result_open_cursor++;if(this.name==='items')__ymbMemQA.item_open_cursor++;return oc.apply(this,args);};
    const co=IDBObjectStore.prototype.count;IDBObjectStore.prototype.count=function(...args){if(this.name==='results')__ymbMemQA.result_count++;if(this.name==='items')__ymbMemQA.item_count++;return co.apply(this,args);};
  });
}

async function seed(page,{items=1500,rawBytes=32768,rowsPerResult=8}={}){
  return page.evaluate(async({DB,OWNER,items,rawBytes,rowsPerResult})=>{
    const req=r=>new Promise((ok,no)=>{r.onsuccess=()=>ok(r.result);r.onerror=()=>no(r.error)});const opened=indexedDB.open(DB,1);
    opened.onupgradeneeded=()=>{const d=opened.result;if(!d.objectStoreNames.contains('jobs'))d.createObjectStore('jobs',{keyPath:'job_id'});if(!d.objectStoreNames.contains('items')){const s=d.createObjectStore('items',{keyPath:['job_id','index']});s.createIndex('state',['job_id','state','index']);s.createIndex('due',['job_id','state','next_poll_at','index']);s.createIndex('operation','operation_id',{unique:true});}if(!d.objectStoreNames.contains('results'))d.createObjectStore('results',{keyPath:['job_id','index']});if(!d.objectStoreNames.contains('attempts'))d.createObjectStore('attempts',{keyPath:['job_id','attempt_id']});};
    const db=await req(opened),jobId='memory-large-job',now=Date.now(),raw='X'.repeat(rawBytes);
    await new Promise((ok,no)=>{const tx=db.transaction(['jobs','items','results'],'readwrite');tx.oncomplete=ok;tx.onerror=()=>no(tx.error);tx.onabort=()=>no(tx.error);tx.objectStore('jobs').put({job_id:jobId,owner:OWNER,total:items,counts:{PENDING:0,SUBMITTING:0,WAITING:1,COLLECTING:0,RESULT_SAVED:0,SUCCEEDED:items-1,PARSE_FAILED:0,FAILED:0,UNKNOWN:0,CANCELLED:0},requests_started:items,operations_accepted:items,polls_started:items-1,control:'RUNNING',revision:items*3,created_at:now-60000,updated_at:now});const is=tx.objectStore('items'),rs=tx.objectStore('results');for(let i=0;i<items;i++){const waiting=i===items-1;is.put({job_id:jobId,index:i,query:'q'+i,state:waiting?'WAITING':'SUCCEEDED',next_poll_at:waiting?now+600000:0,operation_id:'op-'+i,poll_count:1});if(!waiting)rs.put({job_id:jobId,index:i,operation_id:'op-'+i,raw_text:raw,received_at:now,normalized:{results:Array.from({length:rowsPerResult},(_,j)=>({url:`https://example.test/${i}/${j}`,title:'T'+j,snippet:'S'.repeat(64)}))},normalized_at:now});}});db.close();return{items,rawBytes,rowsPerResult,approx_raw_bytes:(items-1)*rawBytes};
  },{DB,OWNER,items,rawBytes,rowsPerResult});
}

async function dbState(page){
  return page.evaluate(async DB=>{const req=r=>new Promise((ok,no)=>{r.onsuccess=()=>ok(r.result);r.onerror=()=>no(r.error)}),db=await req(indexedDB.open(DB));const tx=db.transaction(['jobs','items','results'],'readonly');const job=await req(tx.objectStore('jobs').get('memory-large-job'));const range=IDBKeyRange.bound(['memory-large-job',0],['memory-large-job',Number.MAX_SAFE_INTEGER]);const ic=await req(tx.objectStore('items').count(range)),rc=await req(tx.objectStore('results').count(range));db.close();return{revision:job?.revision,item_count:ic,result_count:rc};},DB);
}
async function waitButton(page){await page.waitForFunction(()=>document.getElementById('searchAsyncRefresh')?.disabled===false,{timeout:20000});}
async function refresh(page){await waitButton(page);await page.evaluate(owner=>{const e=document.getElementById('conversationMeta');if(e)e.textContent=owner;document.getElementById('searchAsyncRefresh').click();},OWNER);await delay(15);await waitButton(page);}

async function longHoldFixed(){
  const root=fs.realpathSync(process.env.YMB_FIXED_ROOT),source=fs.readFileSync(path.join(root,'popup_search_async_monitor.js'),'utf8');assert.ok(!source.includes('results.openCursor'));assert.ok(!source.includes('REFRESH_MS'));
  const {browser,id,pid,worker}=await launch(root);let page;
  try{
    page=await browser.newPage();await installCounters(page);await page.goto(`chrome-extension://${id}/popup.html`,{waitUntil:'load',timeout:20000});await waitButton(page);const meta=await seed(page);const beforeDb=await dbState(page);await refresh(page);await page.evaluate(owner=>{globalThis.__ownerPin=setInterval(()=>{const e=document.getElementById('conversationMeta');if(e)e.textContent=owner;},100);},OWNER);await delay(1000);try{await page.evaluate(()=>globalThis.gc?.())}catch{}
    const startCounters=await page.evaluate(()=>({...__ymbMemQA})),base=rssTree(pid),samples=[{sec:0,...base}];let peak=base.rss_kib;
    for(let i=1;i<=6;i++){await delay(10000);const r=rssTree(pid);samples.push({sec:i*10,...r});peak=Math.max(peak,r.rss_kib);}
    try{await page.evaluate(()=>globalThis.gc?.())}catch{};await delay(1500);const after=rssTree(pid),endCounters=await page.evaluate(()=>({...__ymbMemQA})),afterDb=await dbState(page),fetchCalls=await worker.evaluate(()=>globalThis.__memFetchCalls||0);
    const delta=after.rss_kib-base.rss_kib;assert.equal(startCounters.result_open_cursor,0,JSON.stringify(startCounters));assert.equal(endCounters.result_open_cursor,0,JSON.stringify(endCounters));assert.equal(endCounters.result_count,startCounters.result_count,JSON.stringify({startCounters,endCounters}));assert.deepEqual(afterDb,beforeDb);assert.equal(fetchCalls,0);assert.ok(peak<2097152,JSON.stringify({peak,samples}));assert.ok(delta<131072,JSON.stringify({base,after,delta,samples}));
    const row={case:'fixed_heavy_job_60s_idle_bounded',status:'PASS',meta,start_counters:startCounters,end_counters:endCounters,db_unchanged:true,base_rss_kib:base.rss_kib,after_rss_kib:after.rss_kib,delta_rss_kib:delta,peak_rss_kib:peak,samples,provider_calls:fetchCalls};emit(row);return row;
  }finally{try{await browser.close();}catch{}}
}

async function churn(root,{fixed}){
  const {browser,id,pid,worker}=await launch(root);let seedPage;
  try{
    seedPage=await browser.newPage();await seedPage.goto(`chrome-extension://${id}/popup.html`,{waitUntil:'load',timeout:20000});if(fixed)await waitButton(seedPage);await seed(seedPage);if(fixed)await refresh(seedPage);await seedPage.close();await delay(2500);const base=rssTree(pid);let peak=base.rss_kib,maxProcesses=base.processes;
    for(let i=0;i<100;i++){const p=await browser.newPage();await p.goto(`chrome-extension://${id}/popup.html`,{waitUntil:'load',timeout:20000});if(fixed)await refresh(p);await p.close();if(i%10===0){const r=rssTree(pid);peak=Math.max(peak,r.rss_kib);maxProcesses=Math.max(maxProcesses,r.processes);}}
    await delay(5000);const after=rssTree(pid),fetchCalls=await worker.evaluate(()=>globalThis.__memFetchCalls||0);assert.equal(fetchCalls,0);return{base_rss_kib:base.rss_kib,after_rss_kib:after.rss_kib,delta_rss_kib:after.rss_kib-base.rss_kib,peak_rss_kib:peak,base_processes:base.processes,after_processes:after.processes,max_processes:maxProcesses,provider_calls:fetchCalls};
  }finally{try{await browser.close();}catch{}}
}

async function differentialChurn(){
  const neutral=await churn(fs.realpathSync(process.env.YMB_NEUTRAL_ROOT),{fixed:false});const fixed=await churn(fs.realpathSync(process.env.YMB_FIXED_ROOT),{fixed:true});const neutralExcess=Math.max(0,neutral.delta_rss_kib),fixedExcess=Math.max(0,fixed.delta_rss_kib),extra=fixedExcess-neutralExcess,peakExtra=(fixed.peak_rss_kib-fixed.base_rss_kib)-(neutral.peak_rss_kib-neutral.base_rss_kib),processExtra=fixed.after_processes-neutral.after_processes;
  emit({case:'popup_tab_churn_control_differential',status:'DIAGNOSTIC',neutral,fixed,extra_residual_rss_kib:extra,extra_peak_growth_kib:peakExtra,extra_processes:processExtra});
  assert.ok(extra<262144,JSON.stringify({neutral,fixed,extra}));assert.ok(peakExtra<262144,JSON.stringify({neutral,fixed,peakExtra}));assert.ok(processExtra<=3,JSON.stringify({neutral,fixed,processExtra}));
  const row={case:'fixed_100_open_close_not_worse_than_neutral_control',status:'PASS',neutral,fixed,extra_residual_rss_kib:extra,extra_peak_growth_kib:peakExtra,extra_processes:processExtra};emit(row);return row;
}

let failures=0;
for(const [name,fn] of [['long_hold',longHoldFixed],['differential_churn',differentialChurn]]){try{await fn();}catch(e){failures++;emit({case:name,status:'FAIL',error:String(e.stack||e)});}}
const rows=fs.existsSync(path.join(out,'lifecycle.jsonl'))?fs.readFileSync(path.join(out,'lifecycle.jsonl'),'utf8').trim().split(/\n/).filter(Boolean).map(JSON.parse):[];const required=['fixed_heavy_job_60s_idle_bounded','fixed_100_open_close_not_worse_than_neutral_control'];const result={product_sha:process.env.YMB_PRODUCT_SHA,provider_calls:0,required,rows,failures,pass:failures===0&&required.every(c=>rows.some(r=>r.case===c&&r.status==='PASS'))};fs.writeFileSync(path.join(out,'RESULT.json'),JSON.stringify(result,null,2)+'\n');process.exitCode=result.pass?0:1;
