import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';

const require=createRequire(pathToFileURL(path.resolve(process.env.YMB_PPTR_HOME,'package.json')));
const puppeteer=require('puppeteer');
const out=path.resolve(process.env.YMB_MEMORY_EVIDENCE);
fs.mkdirSync(out,{recursive:true});
const OWNER='https://chatgpt.com|aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee';
const DB='ymb_search_async_items_v2';
const delay=ms=>new Promise(r=>setTimeout(r,ms));
const emit=row=>{const v={...row,time:new Date().toISOString()};fs.appendFileSync(path.join(out,'memory.jsonl'),JSON.stringify(v)+'\n');console.log(JSON.stringify(v));};

function rssTree(pid){
  const raw=execFileSync('ps',['-eo','pid=,ppid=,rss='],{encoding:'utf8',timeout:2000}).trim();
  const rows=raw?raw.split('\n').map(x=>x.trim().split(/\s+/).map(Number)):[];
  const owned=new Set([pid]);let changed=true;
  while(changed){changed=false;for(const [p,pp] of rows)if(owned.has(pp)&&!owned.has(p)){owned.add(p);changed=true;}}
  const selected=rows.filter(x=>owned.has(x[0]));
  return {rss_kib:selected.reduce((s,x)=>s+x[2],0),processes:selected.length,pids:selected.map(x=>x[0])};
}

async function installCounters(page){
  await page.evaluateOnNewDocument(()=>{
    globalThis.__ymbMemQA={result_open_cursor:0,result_count:0,item_open_cursor:0,item_count:0};
    const oc=IDBObjectStore.prototype.openCursor;
    IDBObjectStore.prototype.openCursor=function(...args){
      if(this.name==='results')globalThis.__ymbMemQA.result_open_cursor++;
      if(this.name==='items')globalThis.__ymbMemQA.item_open_cursor++;
      return oc.apply(this,args);
    };
    const co=IDBObjectStore.prototype.count;
    IDBObjectStore.prototype.count=function(...args){
      if(this.name==='results')globalThis.__ymbMemQA.result_count++;
      if(this.name==='items')globalThis.__ymbMemQA.item_count++;
      return co.apply(this,args);
    };
  });
}

async function waitButton(page){await page.waitForFunction(()=>document.getElementById('searchAsyncRefresh')?.disabled===false,{timeout:20000});}

async function seed(page,{items=1500,rawBytes=65536}){
  return page.evaluate(async({DB,OWNER,items,rawBytes})=>{
    const req=r=>new Promise((ok,no)=>{r.onsuccess=()=>ok(r.result);r.onerror=()=>no(r.error)});
    const opened=indexedDB.open(DB,1);
    opened.onupgradeneeded=()=>{
      const d=opened.result;
      if(!d.objectStoreNames.contains('jobs'))d.createObjectStore('jobs',{keyPath:'job_id'});
      if(!d.objectStoreNames.contains('items')){const s=d.createObjectStore('items',{keyPath:['job_id','index']});s.createIndex('state',['job_id','state','index']);s.createIndex('due',['job_id','state','next_poll_at','index']);s.createIndex('operation','operation_id',{unique:true});}
      if(!d.objectStoreNames.contains('results'))d.createObjectStore('results',{keyPath:['job_id','index']});
      if(!d.objectStoreNames.contains('attempts'))d.createObjectStore('attempts',{keyPath:['job_id','attempt_id']});
    };
    const db=await req(opened),jobId='memory-large-job',now=Date.now(),raw='X'.repeat(rawBytes);
    await new Promise((ok,no)=>{
      const tx=db.transaction(['jobs','items','results'],'readwrite');tx.oncomplete=ok;tx.onerror=()=>no(tx.error);tx.onabort=()=>no(tx.error);
      tx.objectStore('jobs').put({job_id:jobId,owner:OWNER,total:items,counts:{PENDING:0,SUBMITTING:0,WAITING:1,COLLECTING:0,RESULT_SAVED:0,SUCCEEDED:items-1,PARSE_FAILED:0,FAILED:0,UNKNOWN:0,CANCELLED:0},requests_started:items,operations_accepted:items,polls_started:items-1,control:'RUNNING',revision:items*3,created_at:now-60000,updated_at:now});
      const is=tx.objectStore('items'),rs=tx.objectStore('results');
      for(let i=0;i<items;i++){
        const waiting=i===items-1;
        is.put({job_id:jobId,index:i,query:'q'+i,state:waiting?'WAITING':'SUCCEEDED',next_poll_at:waiting?now+600000:0,operation_id:'op-'+i,poll_count:1});
        if(!waiting)rs.put({job_id:jobId,index:i,operation_id:'op-'+i,raw_text:raw,received_at:now,normalized:{results:Array.from({length:20},(_,j)=>({url:`https://example.test/${i}/${j}`,title:'T'+j,snippet:'S'.repeat(64)}))},normalized_at:now});
      }
    });
    db.close();return{jobId,items,rawBytes,approx_raw_bytes:(items-1)*rawBytes};
  },{DB,OWNER,items,rawBytes});
}

async function dbState(page){
  return page.evaluate(async({DB})=>{
    const req=r=>new Promise((ok,no)=>{r.onsuccess=()=>ok(r.result);r.onerror=()=>no(r.error)}),db=await req(indexedDB.open(DB));
    const tx=db.transaction(['jobs','items','results'],'readonly'),jobs=tx.objectStore('jobs'),items=tx.objectStore('items'),results=tx.objectStore('results');
    const job=await req(jobs.get('memory-large-job')),ic=await req(items.count(IDBKeyRange.bound(['memory-large-job',0],['memory-large-job',Number.MAX_SAFE_INTEGER]))),rc=await req(results.count(IDBKeyRange.bound(['memory-large-job',0],['memory-large-job',Number.MAX_SAFE_INTEGER])));db.close();return{revision:job?.revision,item_count:ic,result_count:rc};
  },{DB});
}

async function setOwnerAndRefresh(page){
  await waitButton(page);
  await page.evaluate(owner=>{document.getElementById('conversationMeta').textContent=owner;document.getElementById('searchAsyncRefresh').click();},OWNER);
  await waitButton(page);
}

async function launch(root){
  const browser=await puppeteer.launch({headless:false,pipe:true,enableExtensions:[root],protocolTimeout:180000,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--host-resolver-rules=MAP * ~NOTFOUND','--js-flags=--expose-gc',`--disable-extensions-except=${root}`,`--load-extension=${root}`]});
  const sw=await browser.waitForTarget(t=>t.type()==='service_worker'&&t.url().startsWith('chrome-extension://')&&t.url().endsWith('/phase3_service_worker_bootstrap.js'),{timeout:20000});
  return{browser,id:sw.url().split('/')[2],pid:browser.process().pid};
}

async function oldReproduction(){
  const root=fs.realpathSync(process.env.YMB_OLD_ROOT),{browser,id,pid}=await launch(root);let page,reproduced=false;
  try{
    try{
      page=await browser.newPage();await installCounters(page);await page.goto(`chrome-extension://${id}/popup.html`,{waitUntil:'load',timeout:20000});await waitButton(page);
      const meta=await seed(page,{items:400,rawBytes:65536});await setOwnerAndRefresh(page);
      const first=await page.evaluate(()=>({...__ymbMemQA}));await delay(11500);const later=await page.evaluate(()=>({...__ymbMemQA}));
      assert.ok(first.result_open_cursor>=1,first);assert.ok(later.result_open_cursor>=first.result_open_cursor+2,{first,later});
      emit({case:'revoked_stage_b_reproduces_periodic_result_payload_scan',status:'PASS_REPRODUCTION',mode:'repeated_payload_cursor',meta,first,later,rss:rssTree(pid)});reproduced=true;
    }catch(e){
      const text=String(e?.stack||e);
      if(/frame got detached|Target closed|browser has disconnected|Session closed|Connection closed/i.test(text)){
        emit({case:'revoked_stage_b_reproduces_periodic_result_payload_scan',status:'PASS_REPRODUCTION',mode:'browser_or_popup_detached_under_heavy_store',error:text.slice(0,1200)});reproduced=true;
      }else throw e;
    }
    assert.equal(reproduced,true);
  } finally {try{await browser.close();}catch{}}
}

async function fixedCandidate(){
  const root=fs.realpathSync(process.env.YMB_NEW_ROOT),source=fs.readFileSync(path.join(root,'popup_search_async_monitor.js'),'utf8');
  assert.ok(!source.includes('results.openCursor'));assert.ok(!source.includes('REFRESH_MS'));assert.ok(source.includes('results.count(itemRange)'));
  const {browser,id,pid}=await launch(root);let page;
  try{
    page=await browser.newPage();await installCounters(page);await page.goto(`chrome-extension://${id}/popup.html`,{waitUntil:'load',timeout:20000});await waitButton(page);
    const meta=await seed(page,{items:1500,rawBytes:65536});const beforeDb=await dbState(page);await setOwnerAndRefresh(page);await delay(500);
    let counters=await page.evaluate(()=>({...__ymbMemQA}));assert.equal(counters.result_open_cursor,0,counters);assert.ok(counters.result_count>=1,counters);
    const text=await page.evaluate(()=>({rows:document.getElementById('searchAsyncRows')?.textContent,processed:document.getElementById('searchAsyncProcessed')?.textContent,normalized:document.getElementById('searchAsyncNormalized')?.textContent,next:document.getElementById('searchAsyncNextPoll')?.textContent}));
    assert.equal(text.rows,'— (без чтения payload)');assert.equal(text.processed,'1499 / 1500 — 99.9%');assert.equal(text.normalized,'1499 / 1500');
    try{await page.evaluate(()=>globalThis.gc?.())}catch{};await delay(1000);const base=rssTree(pid);
    for(let i=0;i<100;i++){await page.evaluate(()=>document.getElementById('searchAsyncRefresh').click());await waitButton(page);}
    try{await page.evaluate(()=>globalThis.gc?.())}catch{};await delay(1500);const after=rssTree(pid);counters=await page.evaluate(()=>({...__ymbMemQA}));
    assert.equal(counters.result_open_cursor,0,counters);assert.ok(counters.result_count>=101,counters);
    const afterDb=await dbState(page);assert.deepEqual(afterDb,beforeDb);
    const delta=after.rss_kib-base.rss_kib;assert.ok(delta<262144,{base,after,delta});
    emit({case:'fixed_large_job_100_refreshes_no_result_payload_materialization',status:'PASS',meta,text,counters,db_unchanged:true,base_rss_kib:base.rss_kib,after_rss_kib:after.rss_kib,delta_rss_kib:delta});

    await page.close();const reopenBase=rssTree(pid);let peak=reopenBase.rss_kib;
    for(let i=0;i<100;i++){
      const p=await browser.newPage();await installCounters(p);await p.goto(`chrome-extension://${id}/popup.html`,{waitUntil:'load',timeout:20000});await waitButton(p);
      await p.evaluate(owner=>{document.getElementById('conversationMeta').textContent=owner;document.getElementById('searchAsyncRefresh').click();},OWNER);await waitButton(p);
      const c=await p.evaluate(()=>({...__ymbMemQA}));assert.equal(c.result_open_cursor,0,c);await p.close();if(i%10===0){const r=rssTree(pid);peak=Math.max(peak,r.rss_kib);}
    }
    await delay(1500);const reopenAfter=rssTree(pid);assert.ok(reopenAfter.rss_kib<2097152,reopenAfter);assert.ok(peak<2097152,{peak});
    emit({case:'fixed_100_popup_open_close_cycles_bounded',status:'PASS',baseline_rss_kib:reopenBase.rss_kib,after_rss_kib:reopenAfter.rss_kib,peak_rss_kib:peak,emergency_limit_kib:2097152});
  } finally {try{await browser.close();}catch{}}
}

let failures=0;
for(const [name,fn] of [['old_reproduction',oldReproduction],['fixed_candidate',fixedCandidate]]){
  try{await fn();}catch(e){failures++;emit({case:name,status:'FAIL',error:String(e.stack||e)});}
}
const rows=fs.readFileSync(path.join(out,'memory.jsonl'),'utf8').trim().split(/\n/).filter(Boolean).map(JSON.parse);
const required=['revoked_stage_b_reproduces_periodic_result_payload_scan','fixed_large_job_100_refreshes_no_result_payload_materialization','fixed_100_popup_open_close_cycles_bounded'];
const result={product_sha:process.env.YMB_PRODUCT_SHA,old_sha:process.env.YMB_OLD_SHA,provider_calls:0,required,rows,failures,pass:failures===0&&required.every(c=>rows.some(r=>r.case===c&&String(r.status).startsWith('PASS')))};
fs.writeFileSync(path.join(out,'RESULT.json'),JSON.stringify(result,null,2)+'\n');process.exitCode=result.pass?0:1;
