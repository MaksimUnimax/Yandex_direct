// Appended to the unchanged, hash-checked B15 helper prelude. QA, not product.
const profile=path.resolve(out,'owned-profile');
const OTHER_CID='77777777-6666-4555-8444-333333333333',OTHER_URL='https://chatgpt.com/c/'+OTHER_CID;
const scope=process.env.YMB_B16_SCOPE||'all';
async function launchOwned(){
 browser=await puppeteer.launch({headless:false,pipe:true,enableExtensions:true,userDataDir:profile,protocolTimeout:120000,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--host-resolver-rules=MAP * ~NOTFOUND',`--disable-extensions-except=${root}`,`--load-extension=${root}`]});
 pid=browser.process()?.pid;assert.ok(pid);await getWorker();await instrument();
}
async function openFixture(url=PAGE_URL){
 const p=await browser.newPage();await p.setViewport({width:1200,height:900});await p.setRequestInterception(true);
 p.on('request',r=>{if(r.isNavigationRequest()&&[PAGE_URL,OTHER_URL].includes(r.url()))void r.respond({status:200,contentType:'text/html; charset=utf-8',body:fixture});else void r.abort();});
 p.on('pageerror',e=>errors.push(String(e)));await p.goto(url,{waitUntil:'domcontentloaded',timeout:20000});return p;
}
async function configure(){
 tabId=await w.evaluate(async url=>(await chrome.tabs.query({})).find(t=>t.url===url).id,PAGE_URL);
 await until(async()=>w.evaluate(id=>new Promise(ok=>chrome.tabs.sendMessage(id,{type:'WS_GET_IDENTITY'},r=>{void chrome.runtime.lastError;ok(r?.ok===true);})),tabId),'CONTENT_NOT_READY');
 await w.evaluate(async({key,cid,tabId})=>{await chrome.storage.local.set({wsmb_conversation_bindings:{[key]:{binding_id:'b16',revision:1,origin:'https://chatgpt.com',conversation_id:cid,conversation_key:key}},wsmb_manual_modes:{[key]:true},ymb_service_contexts:{[key]:{active_service:'search'}},wsmb_auto_send:true,ymb_settings_schema_version:5});await YMBCredentialRuntime.save('search',{api_key:'QA_NOT_REAL_B16',folder_id:'qa-only',check_state:'PRESENT'});await new Promise(ok=>chrome.tabs.sendMessage(tabId,{type:'WS_APPLY_MANUAL_MODE',conversation_key:key,enabled:true,active_service:'search'},ok));},{key:KEY,cid:CID,tabId});
}
async function popupOpen(){
 await page.bringToFront();await w.evaluate(()=>chrome.action.openPopup());
 const t=await browser.waitForTarget(t=>t.type()==='page'&&t.url()===`chrome-extension://${extensionId}/popup.html`,{timeout:10000});
 const p=await t.asPage();await p.waitForFunction(()=>document.getElementById('conversationMeta')?.textContent.includes('99999999'),{timeout:15000});return p;
}
async function clickToggle(p,selector,value){await p.$eval(selector,(el,value)=>{if(el.checked!==value)el.click();},value);await delay(350);}
async function manualMode(enabled){const p=await popupOpen();try{await clickToggle(p,'#manualMode',enabled);await until(async()=>w.evaluate(async({key,enabled})=>(await getManualMode(key))===enabled,{key:KEY,enabled}),'MANUAL_TOGGLE_NOT_SAVED');}finally{await p.close();}}
async function actions(){return page.evaluate(()=>[...document.querySelectorAll('[data-ymb-owned]')].flatMap(e=>e.shadowRoot?[...e.shadowRoot.querySelectorAll('.ymb-action')]:[]).map(b=>({id:b.dataset.blockId,disabled:b.disabled,connected:b.isConnected,background:getComputedStyle(b).backgroundColor,left:b.getBoundingClientRect().left})));}
async function realm(p=page){for(const r of p.extensionRealms()){if((await r.extension())?.id===extensionId)return r;}throw new Error('EXTENSION_REALM_MISSING');}
async function retained(){
 const m=await page.metrics();const c=await page.createCDPSession();let dom;try{dom=await c.send('Memory.getDOMCounters');}finally{await c.detach();}
 const heap=await w.client.send('Runtime.getHeapUsage');
 const runtime=await(await realm()).evaluate(()=>{const r=globalThis.__YMB_FILE_DELIVERY_CONTENT_V2__;return{file_timer:!!r?.timer,inflight:r?.in_flight.size,send_inflight:r?.send_in_flight.size,manual_listener:!!r?.manual_handler};});
 return{rss:memory(),page:{heap_used:m.JSHeapUsedSize,heap_total:m.JSHeapTotalSize,nodes:m.Nodes,listeners:m.JSEventListeners},dom,worker_heap:heap,runtime};
}
try{
 await launchOwned();
 deadline=setTimeout(()=>{resourceStop=true;void browser.close();},360000);
 monitor=setInterval(()=>{try{const m=memory();fs.appendFileSync(path.join(out,'rss.jsonl'),JSON.stringify({stage,...m})+'\n');if(m.rss_kib>2097152){resourceStop=true;void browser.close();}}catch{}},250);
 emit({case:'exact_B15_single_install',status:'PASS',tree:tree(),chrome:await browser.version(),puppeteer:require('puppeteer/package.json').version,profile:'owned disposable; reused only for explicit browser restart',scope});
 page=await openFixture();await configure();
 if(scope!=='resource'){
 await runCase('real_popup_toggles_do_not_save_unsaved_fields',async()=>{
  const before=await w.evaluate(async key=>({prefix:(await publicSettingsState(key)).report_prefix,credential:(await YMBCredentialRuntime.settings()).credentials.search}),KEY);
  let p=await popupOpen();try{
   await p.$eval('#searchApiKey',e=>{e.value='UNSAVED_QA_ONLY';});await p.$eval('#reportPrefixText',e=>{e.value='UNSAVED_PREFIX_B16';});
   for(const [sel,value]of [['#debugMode',true],['#autoSend',false],['#wordstatAutorunEnabled',true],['#reportPrefixEnabled',true]])await clickToggle(p,sel,value);
   const r=await w.evaluate(async key=>({s:await publicSettingsState(key),credential:(await YMBCredentialRuntime.settings()).credentials.search}),KEY);
   assert.equal(r.s.debug_mode,true);assert.equal(r.s.auto_send,false);assert.equal(r.s.wordstat_policy.autorun_enabled,true);assert.equal(r.s.report_prefix.enabled,true);
   assert.equal(r.s.report_prefix.text,before.prefix.text);assert.equal(r.credential.api_key,before.credential.api_key);
  }finally{await p.close();}
  p=await popupOpen();try{const fields=await p.evaluate(()=>({debug:document.getElementById('debugMode').checked,auto:document.getElementById('autoSend').checked,key:document.getElementById('searchApiKey').value,prefix:document.getElementById('reportPrefixText').value}));assert.equal(fields.debug,true);assert.equal(fields.auto,false);assert.equal(fields.key,'');assert.equal(fields.prefix,before.prefix.text);
   await clickToggle(p,'#debugMode',false);await clickToggle(p,'#autoSend',true);await clickToggle(p,'#reportPrefixEnabled',false);
  }finally{await p.close();}return{real_popup_reopened:true,unsaved_secret_not_committed:true,secret_input_blank_on_reopen:true};
 });
 await runCase('real_popup_explicit_save_text_and_dedicated_secret',async()=>{
  let p=await popupOpen();try{
   await p.$eval('#reportPrefixText',e=>{e.value='B16 SAVED PREFIX';});await p.click('#saveSettingsTop');await until(async()=>w.evaluate(async key=>(await publicSettingsState(key)).report_prefix.text==='B16 SAVED PREFIX',KEY),'PREFIX_NOT_SAVED');
   await p.$eval('#searchApiKey',e=>{e.value='QA_B16_REPLACEMENT_NOT_REAL';});await p.$eval('#searchFolderId',e=>{e.value='qa-only';});await p.$eval('#saveSearchCredential',e=>e.click());
   await until(async()=>w.evaluate(async()=>(await YMBCredentialRuntime.settings()).credentials.search.api_key==='QA_B16_REPLACEMENT_NOT_REAL'),'SECRET_NOT_SAVED');
  }finally{await p.close();}
  p=await popupOpen();try{assert.equal(await p.$eval('#searchApiKey',e=>e.value),'');assert.equal(await p.$eval('#reportPrefixText',e=>e.value),'B16 SAVED PREFIX');}finally{await p.close();}
  assert.equal(await page.evaluate(()=>document.documentElement.outerHTML.includes('QA_B16_REPLACEMENT_NOT_REAL')),false);return{explicit_save_and_reopen:true,secret_not_in_chat_DOM:true};
 });
 await runCase('PRE_before_Copy_stable_external_action_and_native_lifecycle',async()=>{
  await resetDelivery();await page.evaluate(()=>{__fixture.append('SEARCH_ASYNC_BATCH_API_V1\n{"action":"status","jobId":"fixture"}');document.querySelector('button[aria-label="Copy"]').remove();});
  await until(async()=>(await actions()).some(a=>!a.disabled),'NO_ACTION_BEFORE_COPY');
  const b=(await actions())[0];assert.equal(b.background,'rgb(255, 216, 77)');
  const right=await page.$eval('pre',p=>p.getBoundingClientRect().right);assert.ok(Math.abs(b.left-right-10)<=1);
  const counts=await messageCounts();
  await page.evaluate(()=>{const surface=document.querySelector('[data-ymb-owned]').shadowRoot;window.__actionIdentity=surface.querySelector('.ymb-action');const pre=document.querySelector('pre');const copy=document.createElement('button');copy.type='button';copy.setAttribute('aria-label','Copy');copy.textContent='Copy';copy.dataset.fixture='local-copy';copy.addEventListener('click',()=>__fixture.copy++);pre.append(copy);window.__copyBefore=copy.outerHTML;});await delay(500);
  assert.equal(await page.evaluate(()=>document.querySelector('[data-fixture="local-copy"]').outerHTML===__copyBefore),true);
  await page.click('[data-fixture="local-copy"]');await page.$eval('[data-fixture="local-copy"]',b=>{b.textContent='Copied';b.setAttribute('aria-label','Copied');});await delay(300);
  await page.$eval('[data-fixture="local-copy"]',b=>b.remove());await delay(300);
  await page.evaluate(()=>{const b=document.createElement('button');b.textContent='Copy';b.setAttribute('aria-label','Copy');document.querySelector('pre').append(b);});await delay(300);
  assert.equal(await page.evaluate(()=>__actionIdentity===document.querySelector('[data-ymb-owned]').shadowRoot.querySelector('.ymb-action')&&__actionIdentity.isConnected&&!__actionIdentity.disabled),true);
  assert.equal((await messageCounts()).WS_EXECUTE_MANUAL_BLOCK||0,counts.WS_EXECUTE_MANUAL_BLOCK||0);
  await manualMode(false);await until(async()=>(await actions()).length===0,'MANUAL_OFF_RESIDUE');await manualMode(true);await until(async()=>(await actions()).length===1,'REENABLE_DUPLICATION');
  return{copy_dispatch:0,external_identity_stable:true,position_right_plus10:true,manual_off_on:true};
 });
 await runCase('readonly_CodeMirror_mutation_detach_and_full_block_capture',async()=>{
  await resetDelivery();await page.evaluate(()=>{document.getElementById('conversation-root').replaceChildren();const t=document.createElement('div');t.dataset.messageAuthorRole='assistant';t.dataset.messageId='b16-cm';const b=document.createElement('div');b.dataset.testid='code-block';b.style.cssText='width:65%;padding:20px';const cm=document.createElement('div');cm.className='cm-content';cm.contentEditable='false';for(const text of ['SEARCH_ASYNC_BATCH_API_V1','{"action":"start","jobId":"b16-cm","queries":["x"],"confirmBillable":true,"maxRequests":1,"maxCostRub":1}']){const l=document.createElement('div');l.className='cm-line';l.textContent=text;cm.append(l);}b.append(cm);t.append(b);document.getElementById('conversation-root').append(t);});
  await until(async()=>(await actions()).length===1&&(await actions())[0].disabled===false,'CM_ACTION_NOT_READY');
  const expected=await page.$eval('.cm-content',e=>e.innerText);const capture=await(await realm()).evaluate(()=>BB2ProvenWritingCapture.textFromBlock(document.querySelector('[data-testid="code-block"]')));assert.equal(capture,expected);
  const n=(await fx()).sends.length;await page.evaluate(()=>document.querySelector('[data-ymb-owned]').shadowRoot.querySelector('.ymb-action').click());await until(async()=>(await fx()).sends.length===n+1,'CM_RESULT_NOT_DELIVERED');await until(async()=>!(await outbox()),'CM_NOT_ACK');
  assert.equal(await w.evaluate(async key=>(await YMBSearchAsyncStore.getSummary('b16-cm',key)).total,KEY),1);
  await page.$eval('[data-message-id="b16-cm"]',e=>e.remove());await until(async()=>(await actions()).length===0,'DETACHED_ACTION_REMAINS');
  return{readonly_CM_shape:true,actual_CM_library:false,whole_block_equal:true,local_command:1,detached_controls:0};
 });
 await runCase('foreign_conversation_cannot_claim_or_read_large_file',async()=>{
  await resetDelivery();await page.$eval('#prompt-textarea',e=>{e.value='USER_BLOCK';});const d=await stageFile(64,'foreign');
  const other=await openFixture(OTHER_URL);try{
   await delay(1200);assert.equal(await other.evaluate(()=>__fixture.changes),0);
   const r=await(await realm(other)).evaluate(({key,id,ak})=>new Promise(ok=>chrome.runtime.sendMessage({type:'WS_GET_OUTBOX_ARTIFACT_CHUNK',conversation_key:key,delivery_id:id,artifact_key:ak,chunk_index:0},ok)),{key:KEY,id:d.id,ak:d.key});assert.equal(r.ok,false);assert.equal(Object.hasOwn(r,'chunk_base64'),false);
  }finally{await other.close();}await resetDelivery();assert.deepEqual(await artifactGone(d.key),{remaining:0,meta:false});return{foreign_file_exposed:false,fixture_cleanup_only:true};
 });
 await runCase('late_final_chunk_after_SPA_navigation_must_not_attach_to_other_chat',async()=>{
  await resetDelivery();await w.evaluate(()=>{globalThis.__b16_chunk_held=false;globalThis.__b16_chunk_release=null;const old=handleMessage;handleMessage=async(m,s)=>{const r=await old(m,s);if(m?.type==='WS_GET_OUTBOX_ARTIFACT_CHUNK'&&m.chunk_index===3&&r?.ok){__b16_chunk_held=true;await new Promise(ok=>{__b16_chunk_release=ok;});}return r;};});
  const d=await stageFile(1,'spa');await until(()=>w.evaluate(()=>__b16_chunk_held),'CHUNK_NOT_HELD');const before=await fx();
  await page.evaluate(url=>{history.pushState({},'',url);document.getElementById('conversation-root').replaceChildren();},OTHER_URL);
  await w.evaluate(()=>{__b16_chunk_release();__b16_chunk_release=null;});await delay(1700);
  const after=await fx();const detail={changes:after.changes-before.changes,sends:after.sends.length-before.sends.length,text:after.text};
  await page.evaluate(url=>history.pushState({},'',url),PAGE_URL);await resetDelivery();
  assert.equal(detail.changes,0,'old conversation payload must not reach the new conversation file input');assert.equal(detail.sends,0);assert.equal(detail.text,'');return{cross_conversation_attachment:0};
 });
 await runCase('active_delivery_Manual_OFF_fence_and_no_fake_cancellation',async()=>{
  await resetDelivery();await page.$eval('#prompt-textarea',e=>{e.value='USER_BLOCK';});const d=await stageFile(64,'cancel-fence');await delay(1200);
  const p=await popupOpen();try{assert.equal(await p.$eval('#manualMode',e=>e.disabled),true);}finally{await p.close();}
  const r=await(await realm()).evaluate(key=>new Promise(ok=>chrome.runtime.sendMessage({type:'WS_SET_MANUAL_MODE',conversation_key:key,enabled:false},ok)),KEY);
  assert.equal(r.ok,false);assert.equal(r.code,'MANUAL_OPERATION_ACTIVE');assert.equal((await outbox()).phase,'claimed');assert.equal((await artifactGone(d.key)).meta,true);
  await resetDelivery();return{active_operation_not_discarded:true,manual_off_is_blocked_not_cancelled:true,user_cancel_UI_not_present_in_candidate:true};
 });
 }
 if(scope!=='surface'&&!resourceStop){
 await runCase('eight_64MiB_full_delivery_cycles_with_idle_heap_DOM_and_RSS',async()=>{
  await resetDelivery();await w.evaluate(()=>chrome.storage.local.set({wsmb_auto_send:true}));await delay(5000);const before=await retained(),samples=[];
  for(let i=0;i<8;i++){
   await resetDelivery();await page.evaluate(()=>{__fixture.sends=[];__fixture.files=[];});const d=await stageFile(64,'b16-long-'+i);
   await until(async()=>(await fx()).sends.length===1,'STRESS_FILE_NOT_SENT',60000);await until(async()=>!(await outbox()),'STRESS_NOT_ACKED');assert.deepEqual(await artifactGone(d.key),{remaining:0,meta:false});await delay(5000);
   const m=await retained();assert.equal(m.runtime.inflight,0);assert.equal(m.runtime.send_inflight,0);assert.equal(m.runtime.manual_listener,false);samples.push(m);emit({case:'retained_64MiB_cycle',status:'RECORDED',cycle:i+1,metrics:m,no_forced_GC:true});
  }
  return{cycles:8,mib_each:64,idle_ms:5000,before,samples,no_forced_GC:true,universal_no_leak_claim:false};
 });
 await runCase('whole_browser_close_reopen_same_owned_profile_preserves_raw_and_does_not_send',async()=>{
  await resetDelivery();await w.evaluate(()=>chrome.storage.local.set({wsmb_auto_send:false}));const d=await stageFile(10,'browser-restart');await until(async()=>(await outbox())?.phase==='attachment_ready','BEFORE_RESTART_NOT_READY');
  const oldSession=await w.evaluate(async()=>{const S=YMBSearchAsyncStore;await S.createJob({jobId:'b16-profile',owner:'b16',queries:['saved'],parameters:{region:'225'},folderId:'qa',maxRequests:1,maxCostMicrorub:100,unitCostMicrorub:100,now:1});await S.claim({jobId:'b16-profile',owner:'b16',workerId:WORKER_SESSION_ID,attemptId:'a',kind:'submit',now:2});await S.finishSubmit({jobId:'b16-profile',owner:'b16',index:0,attemptId:'a',outcome:'received',operationId:'b16-op',rawText:'RAW-PRESERVED-B16',now:3});return WORKER_SESSION_ID;});
  const priorPid=pid;await browser.close();browser=null;await delay(500);await launchOwned();assert.notEqual(pid,priorPid);assert.notEqual(await w.evaluate(()=>WORKER_SESSION_ID),oldSession);
  assert.equal(await w.evaluate(async()=>(await YMBSearchAsyncStore.readResult('b16-profile','b16',0)).raw_text),'RAW-PRESERVED-B16');
  page=await openFixture();await delay(1600);assert.equal((await fx()).changes,0);assert.equal((await fx()).sends.length,0);assert.equal((await artifactGone(d.key)).meta,true);
  // New tab cannot silently steal old delivery ownership. Explicit QA cleanup only.
  await resetDelivery();assert.deepEqual(await artifactGone(d.key),{remaining:0,meta:false});return{actual_browser_closed:true,same_owned_profile:true,raw_preserved:true,no_duplicate_attachment:true,old_tab_not_stolen:true};
 });
 }
 assert.equal(tree(),target);emit({case:'exact_candidate_after_B16',status:'PASS',tree:target,errors,failed,independent_gate:false,release_allowed:false});
}catch(e){failed++;emit({case:stage,status:'FAIL_QUALIFICATION',error:String(e.stack||e),details:await diagnostics(),release_allowed:false});}
finally{clearInterval(monitor);clearTimeout(deadline);if(browser)try{await browser.close();}catch{}const remaining=[];for(const p of observedPids)try{const s=fs.readFileSync('/proc/'+p+'/stat','utf8');if(s.slice(s.lastIndexOf(')')+2).split(' ')[0]!=='Z')remaining.push(p);}catch{}emit({case:'owned_browser_cleanup',status:remaining.length?'FAIL':'PASS',remaining,peak_owned_rss_kib:peak,resource_stop:resourceStop,failed,release_allowed:false});if(remaining.length||failed||resourceStop)process.exitCode=1;}
