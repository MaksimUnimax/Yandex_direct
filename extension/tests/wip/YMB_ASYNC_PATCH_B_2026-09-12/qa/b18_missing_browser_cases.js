// B18 additional development qualification. Appended to exact B17/B16 helper
// prelude. Uses real installed product and popup, synthetic DOM and fetch only.
// No production byte changes and no independent Codex verdict.
const b18Secret = s => `QA_B18_${s.toUpperCase()}_NOT_REAL_SECRET`;
async function switchService(service) {
 const p=await popupOpen();try{await p.$eval('#activeService',(e,s)=>{e.value=s;e.dispatchEvent(new Event('change',{bubbles:true}));},service);
 await until(async()=>w.evaluate(async({key,s})=>(await getServiceContext(key)).active_service===s,{key:KEY,s:service}),'SERVICE_NOT_PERSISTED');}finally{await p.close();}
 await delay(500);
}
async function clearFixture(){await resetDelivery();await page.evaluate(()=>document.getElementById('conversation-root').replaceChildren());await until(async()=>(await actions()).length===0,'OLD_ACTION_NOT_REMOVED');}
async function providerFixture(){await w.evaluate(()=>{
 globalThis.__b18_hits=[];globalThis.__b18_captured=[];globalThis.__b18_response='normal';globalThis.__b18_active=0;globalThis.__b18_max_active=0;
 const old=handleMessage;handleMessage=async(m,s)=>{if(m?.type==='WS_EXECUTE_MANUAL_BLOCK')__b18_captured.push(m.block_text);return old(m,s);};
 globalThis.fetch=async(url,init)=>{
  const u=new URL(String(url));if(!['searchapi.api.cloud.yandex.net','api.webmaster.yandex.net','api-metrika.yandex.net','api.direct.yandex.com'].includes(u.hostname))throw new Error('B18_UNEXPECTED_HOST');
  const body=init?.body?JSON.parse(init.body):null;
  __b18_hits.push({host:u.hostname,path:u.pathname,method:init?.method||'GET',body,auth_present:!!init?.headers?.Authorization});
  __b18_active++;__b18_max_active=Math.max(__b18_max_active,__b18_active);
  try{
   await new Promise(ok=>setTimeout(ok,30));
   if(__b18_response==='unknown')throw new Error('controlled network outcome unknown');
   if(__b18_response==='http_error')return new Response(JSON.stringify({code:'CONTROLLED_ERROR',message:'Controlled safe error'}),{status:403});
   if(u.pathname.includes('/wordstat/'))return new Response(JSON.stringify({totalCount:42,results:[{phrase:'fixture result',count:42}],regions:[],associations:[]}));
   if(u.pathname==='/v2/web/search')return new Response(JSON.stringify({rawData:btoa('<yandexsearch><response><results><grouping><group><doc><url>https://example.test/fixture</url><domain>example.test</domain><title>Fixture</title></doc></group></grouping></results></response></yandexsearch>')}));
   if(u.hostname==='api.webmaster.yandex.net')return new Response(JSON.stringify({user_id:'123',hosts:[]}));
   if(u.hostname==='api-metrika.yandex.net')return new Response(JSON.stringify({counters:[]}));
   if(u.hostname==='api.direct.yandex.com')return new Response(JSON.stringify({result:{Campaigns:[]}}));
   throw new Error('B18_UNEXPECTED_PATH');
  }finally{__b18_active--;}
 };
});}
async function snap(){return w.evaluate(()=>({hits:__b18_hits.map(x=>({...x})),captured:[...__b18_captured],max_active:__b18_max_active}));}
async function external(text,{expectCalls=null}={}){
 await clearFixture();await w.evaluate(()=>chrome.storage.local.set({wsmb_auto_send:true}));const before=await snap(),f=await fx();
 await page.evaluate(t=>__fixture.append(t),text);await until(async()=>(await actions()).length===1&&!(await actions())[0].disabled,'EXTERNAL_NOT_READY');
 await page.evaluate(()=>document.getElementById('ymb-external-action-surface').shadowRoot.querySelector('.ymb-action').click());
 await until(async()=>(await fx()).sends.length===f.sends.length+1,'EXTERNAL_REPORT_NOT_SENT');await until(async()=>!(await outbox()),'EXTERNAL_NOT_ACK');
 const after=await snap(),sent=(await fx()).sends.at(-1).text;
 assert.equal(after.captured.length,before.captured.length+1);assert.equal(after.captured.at(-1),text);
 if(expectCalls!==null)assert.equal(after.hits.length-before.hits.length,expectCalls);
 for(const s of ['wordstat','search','webmaster','metrika','direct'])assert.ok(!sent.includes(b18Secret(s)),'secret in outgoing report');
 return{sent,hits:after.hits.slice(before.hits.length),captured:text,max_active:after.max_active};
}
async function plaques(){return page.evaluate(()=>{const r=document.getElementById('ymb-external-action-surface')?.shadowRoot;return r?[...r.querySelectorAll('.ymb-status')].map(e=>({key:e.dataset.statusKey||e.dataset.key,text:e.textContent})):[];});}
async function useRealPopupButton(selector){const p=await popupOpen();try{p.on('dialog',d=>void d.accept());await p.$eval(selector,e=>{if(e.disabled)throw new Error('DISABLED '+e.id);e.click();});await delay(350);}finally{await p.close();}}
async function runState(){return w.evaluate(async k=>publicRun(await getAutoRun(k)),KEY);}
try{
 await launchOwned();deadline=setTimeout(()=>{resourceStop=true;void browser.close();},420000);
 monitor=setInterval(()=>{try{const m=memory();fs.appendFileSync(path.join(out,'rss.jsonl'),JSON.stringify({stage,...m})+'\n');if(m.rss_kib>2097152){resourceStop=true;void browser.close();}}catch{}},250);
 emit({case:'B18_exact_input',status:'PASS',tree:tree(),chrome:await browser.version(),scope:'missing development assertions only'});
 page=await openFixture();await configure();await providerFixture();
 await runCase('popup_five_dedicated_credentials_explicit_save_and_check',async()=>{
  const forms=[['wordstat','wordstatApiKey','wordstatFolderId','saveWordstatCredential','checkWordstatCredential'],['search','searchApiKey','searchFolderId','saveSearchCredential','checkSearchCredential'],['webmaster','webmasterOauthToken',null,'saveWebmasterCredential','checkWebmasterCredential'],['metrika','metrikaOauthToken',null,'saveMetrikaCredential','checkMetrikaCredential'],['direct','directOauthToken',null,'saveDirectCredential','checkDirectCredential']];
  const before=(await snap()).hits.length;
  for(const [s,key,folder,save,check]of forms){let p=await popupOpen();try{
   p.on('dialog',d=>void d.accept());await p.$eval('#'+key,(e,v)=>{e.value=v;},b18Secret(s));if(folder)await p.$eval('#'+folder,e=>{e.value='qa-only';});
   await p.$eval('#'+save,e=>e.click());await until(async()=>w.evaluate(async({s,v})=>{const r=(await YMBCredentialRuntime.settings()).credentials[s];return(r.api_key||r.oauth_token)===v;},{s,v:b18Secret(s)}),'CREDENTIAL_NOT_SAVED_'+s);
   const checkBefore=(await snap()).hits.length;await p.$eval('#'+check,e=>e.click());await until(async()=>(await snap()).hits.length===checkBefore+1,'CHECK_NOT_EXECUTED_'+s);await until(async()=>w.evaluate(async s=>(await YMBCredentialRuntime.settings()).credentials[s].check_state==='PRESENT',s),'CREDENTIAL_CHECK_'+s);
  }finally{await p.close();}
   p=await popupOpen();try{assert.equal(await p.$eval('#'+key,e=>e.value),'');}finally{await p.close();}
  }
  const seen=(await snap()).hits.slice(before);assert.equal(seen.length,5);assert.ok(seen.every(x=>x.auth_present));
  assert.deepEqual(seen.map(x=>x.host),['searchapi.api.cloud.yandex.net','searchapi.api.cloud.yandex.net','api.webmaster.yandex.net','api-metrika.yandex.net','api.direct.yandex.com']);
  const publicText=await w.evaluate(async k=>JSON.stringify(await publicSettingsState(k)),KEY);const dom=await page.content();for(const s of forms.map(a=>a[0])){assert.ok(!publicText.includes(b18Secret(s)));assert.ok(!dom.includes(b18Secret(s)));}
  return{explicit_saves:5,checks:5,real_requests:0,public_secret_exposure:false};
 });
 await runCase('popup_service_policies_and_unsaved_fields_isolation',async()=>{
  const p=await popupOpen();try{
   await p.$eval('#searchApiKey',e=>{e.value='UNSAVED_SECRET_B18';});await p.$eval('#autoStartPromptText',e=>{e.value='UNSAVED_PROMPT_B18';});
   for(const sel of ['#searchManualEnabled','#searchAutorunEnabled','#webmasterManualEnabled','#metrikaManualEnabled','#directManualEnabled','#wordstatAutorunEnabled']){await clickToggle(p,sel,false);await clickToggle(p,sel,true);}
   const r=await w.evaluate(async key=>({s:await publicSettingsState(key),secret:(await YMBCredentialRuntime.settings()).credentials.search.api_key}),KEY);
   assert.equal(r.secret,b18Secret('search'));assert.ok(!JSON.stringify(r.s).includes('UNSAVED_PROMPT_B18'));
   assert.equal(r.s.search_policy.autorun_enabled,true);assert.equal(r.s.wordstat_policy.autorun_enabled,true);
  }finally{await p.close();}
  for(const s of ['webmaster','metrika','direct']){await switchService(s);const p=await popupOpen();try{assert.equal(await p.$eval('#startAuto',e=>e.disabled),true);}finally{await p.close();}}
  await switchService('wordstat');return{policy_toggles:6,future_autorun_locked:3,unsaved_fields_not_committed:true};
 });
 await runCase('manual_full_block_source_order_and_no_parallel_fanout',async()=>{
  await manualMode(true);
  const text='Prefix with braces {ignored}\nWORDSTAT_API_V1 {"method":"getTop","phrase":"a } \\\" b","numPhrases":3}\nWORDSTAT_API_V1 {"method":"getRegionsTree"}\ntrailing text';
  const r=await external(text,{expectCalls:2});assert.deepEqual(r.hits.map(h=>h.path),['/v2/wordstat/topRequests','/v2/wordstat/getRegionsTree']);assert.equal(r.max_active,1);return{whole_block_equal:true,source_order:true,provider_fixture_calls:2,max_concurrency:1};
 });
 for(const [label,text]of [['plain','raw text without a command'],['malformed','WORDSTAT_API_V1 {'],['validation','WORDSTAT_API_V1 {"method":"getTop"}'],['unsupported','WORDSTAT_API_V1 {"method":"deleteEverything"}']])await runCase('manual_local_error_'+label,async()=>{const r=await external(text,{expectCalls:0});assert.match(r.sent,/YMB_ERROR_V1/);return{one_admission_one_report:true,provider_calls:0};});
 await runCase('manual_injected_host_credentials_ignored_at_real_provider_boundary',async()=>{
  const r=await external('WORDSTAT_API_V1 '+JSON.stringify({method:'getTop',phrase:'guard',url:'https://attacker.invalid/',headers:{Authorization:'INJECTED'},api_key:'INJECTED',folderId:'WRONG'}),{expectCalls:1});
  assert.equal(r.hits[0].host,'searchapi.api.cloud.yandex.net');assert.equal(r.hits[0].body.folderId,'qa-only');assert.ok(!r.sent.includes('INJECTED'));return{fixed_host_and_folder:true};
 });
 await runCase('debug_OFF_ON_errors_delivered_and_diagnostics_redacted',async()=>{
  for(const debug of [false,true]){let p=await popupOpen();try{await clickToggle(p,'#debugMode',debug);}finally{await p.close();}
   const r=await external('WORDSTAT_API_V1 {"method":"getTop"}',{expectCalls:0});assert.match(r.sent,/YMB_ERROR_V1/);
   const d=await w.evaluate(async()=>{await diagnostic('B18_TEST',{api_key:'B18_SENSITIVE',Authorization:'B18_SENSITIVE',oauth_token:'B18_SENSITIVE',safe:'OK'});return getDiagnostics();});assert.ok(!JSON.stringify(d).includes('B18_SENSITIVE'));
  }return{debug_modes:2,error_deliveries:2,no_secret_in_diagnostics:true};
 });
 await runCase('legacy_block_adapters_and_local_cross_block_isolation',async()=>{
  await clearFixture();await page.evaluate(()=>{const root=document.getElementById('conversation-root');for(const [index,type]of ['pre','data','class','viewer'].entries()){const turn=document.createElement('div');turn.dataset.messageAuthorRole='assistant';turn.dataset.messageId='adapter-'+index;const block=document.createElement(type==='pre'?'pre':'div');if(type==='data')block.dataset.testid='code-block';if(type==='class')block.className='code-block';if(type==='viewer')block.id='code-block-viewer';block.style.cssText='width:65%;padding:8px';const code=document.createElement('code');code.textContent='ADAPTER '+index;block.append(code);turn.append(block);root.append(turn);}});
  await until(async()=>(await actions()).length===4,'LEGACY_ADAPTER_COUNT');const before=await snap();const s=(await fx()).sends.length;
  await page.evaluate(()=>document.getElementById('ymb-external-action-surface').shadowRoot.querySelectorAll('.ymb-action')[2].click());await until(async()=>(await fx()).sends.length===s+1,'LOCAL_BLOCK_RESULT');await until(async()=>!(await outbox()),'LOCAL_BLOCK_ACK');assert.equal((await snap()).captured.at(-1),'ADAPTER 2');assert.equal((await snap()).hits.length,before.hits.length);
  return{supported_forms:4,selected_block_only:true};
 });
 await runCase('generic_Copy_user_turn_and_conflicting_conversation_fail_closed',async()=>{
  await clearFixture();const before=await messageCounts();await page.evaluate(()=>{const u=document.createElement('div');u.dataset.messageAuthorRole='user';u.innerHTML='<pre><code>WORDSTAT_API_V1 {"method":"getRegionsTree"}</code></pre>';document.getElementById('conversation-root').append(u);const copy=document.createElement('button');copy.id='generic-copy';copy.textContent='Copy response';copy.setAttribute('aria-label','Copy response');copy.addEventListener('click',()=>__fixture.copy++);document.body.append(copy);});
  await delay(700);assert.equal((await actions()).length,0);await page.click('#generic-copy');assert.equal((await messageCounts()).WS_EXECUTE_MANUAL_BLOCK||0,before.WS_EXECUTE_MANUAL_BLOCK||0);
  await page.evaluate(url=>{const c=document.createElement('link');c.rel='canonical';c.href=url;document.head.append(c);__fixture.append('WORDSTAT_API_V1 {"method":"getRegionsTree"}');},OTHER_URL);
  await delay(2200);assert.ok((await actions()).every(a=>a.disabled));assert.equal((await messageCounts()).WS_EXECUTE_MANUAL_BLOCK||0,before.WS_EXECUTE_MANUAL_BLOCK||0);
  await page.evaluate(()=>{document.querySelector('link[rel="canonical"]').remove();document.getElementById('generic-copy').remove();});await delay(2000);return{generic_copy_dispatch:0,user_turn_controls:0,conflicting_identity_blocked:true};
 });
 await runCase('stable_operation_composer_picker_plaques_and_native_picker_noSend',async()=>{
  await clearFixture();await page.$eval('#prompt-textarea',e=>{e.value='USER_OWN_TEXT';});await page.evaluate(()=>__fixture.append('WORDSTAT_API_V1 {"method":"getTop"}'));await until(async()=>(await actions()).some(a=>!a.disabled),'ACTION');
  await page.evaluate(()=>document.getElementById('ymb-external-action-surface').shadowRoot.querySelector('.ymb-action').click());await until(async()=>!!(await outbox()),'OUTBOX_EXPECTED');
  await delay(1300);for(let i=0;i<3;i++)await page.evaluate(i=>{document.body.dataset.epoch=String(i);},i);
  const p=await plaques();assert.equal(p.filter(x=>x.key==='composer-occupied').length,1);assert.ok(p.filter(x=>x.key==='operation-state').length<=1);
  assert.equal(await page.$eval('#prompt-textarea',e=>e.value),'USER_OWN_TEXT');
  const pos=await page.evaluate(()=>{const r=document.getElementById('ymb-external-action-surface').shadowRoot;const e=r.querySelector('.ymb-status').parentElement;const s=getComputedStyle(e);return{right:s.right,top:s.top};});assert.deepEqual(pos,{right:'18px',top:'18px'});
  await page.$eval('#prompt-textarea',e=>{e.value='';e.dispatchEvent(new Event('input',{bubbles:true}));});await until(async()=>!(await outbox()),'OCCUPIED_ACK');await resetDelivery();
  const before=(await fx()).sends.length;const pop=await popupOpen();try{await pop.$eval('#pickSend',e=>e.click());}finally{await pop.close();}
  await delay(200);assert.equal((await plaques()).filter(x=>x.key==='picker-state').length,1);await page.click('#composer-submit-button');await delay(500);assert.equal((await fx()).sends.length,before);assert.ok((await plaques()).filter(x=>x.key==='picker-state').length<=1);
  await useRealPopupButton('#clearSend');return{stable_keys:['composer-occupied','operation-state','picker-state'],picker_intercepted:true};
 });
 await runCase('installed_Autorun_popup_pickup_pause_resume_stop_reload_and_owner',async()=>{
  await clearFixture();await manualMode(false);await switchService('wordstat');const p=await popupOpen();try{await clickToggle(p,'#wordstatAutorunEnabled',true);await p.$eval('#maxRequestsRun',e=>{e.value='10';});await p.$eval('#maxCostRun',e=>{e.value='10';});await p.$eval('#saveSettingsTop',e=>e.click());await delay(400);}finally{await p.close();}
  const before=(await snap()).hits.length;await useRealPopupButton('#startAuto');await until(async()=>(await runState())?.status==='waiting_command','AUTORUN_NOT_WAITING',20000);const first=await runState();assert.ok(first.run_id);
  const pop=await popupOpen();try{assert.equal(await pop.$eval('#startAuto',e=>e.disabled),true);assert.equal(await pop.$eval('#runStatus',e=>e.textContent),'waiting_command');}finally{await pop.close();}
  await page.evaluate(()=>{__fixture.arm();__fixture.append('WORDSTAT_API_V1 {"method":"getRegionsTree"}');document.querySelectorAll('button[aria-label="Copy"]').forEach(e=>e.remove());});
  await until(async()=>(await snap()).hits.length===before+1,'AUTO_PROVIDER_NOT_CALLED',20000);await until(async()=>(await runState())?.status==='waiting_command'&&(await runState()).requests_executed===1,'AUTO_DELIVERY_NOT_COMPLETE',20000);
  assert.equal((await runState()).run_id,first.run_id);assert.ok((await plaques()).filter(x=>x.key==='autorun-state').length<=1);
  await useRealPopupButton('#pauseAuto');await until(async()=>(await runState())?.status==='paused','AUTO_NOT_PAUSED');
  await manualMode(true);await delay(500);assert.equal((await runState()).status,'paused');await manualMode(false);
  const other=await openFixture(OTHER_URL);try{const r=await(await realm(other)).evaluate(({key,id})=>chrome.runtime.sendMessage({type:'WS_AUTO_COMMAND',conversation_key:key,run_id:id,assistant_turn_id:'foreign',command_text:'WORDSTAT_API_V1 {"method":"getRegionsTree"}'}),{key:KEY,id:first.run_id});assert.equal(r.ok,false);assert.equal(r.code,'AUTO_NON_OWNER_TAB');}finally{await other.close();}
  await page.reload({waitUntil:'domcontentloaded'});await delay(1300);assert.equal((await runState()).status,'paused');await useRealPopupButton('#resumeAuto');await until(async()=>(await runState()).status==='waiting_command','AUTO_RESUME');await useRealPopupButton('#finishAuto');await until(async()=>(await runState()).status==='stopped','AUTO_STOP');
  await page.evaluate(()=>{__fixture.arm();__fixture.append('WORDSTAT_API_V1 {"method":"getTop","phrase":"ignored after stop"}');});await delay(1800);assert.equal((await snap()).hits.length,before+1);await manualMode(true);
  return{one_RUN:true,provider_fixture_calls:1,Copy_not_required:true,reload_pause_persisted:true,foreign_tab_blocked:true,stopped_ignores_commands:true};
 });
 await runCase('same_install_runtime_reload_retains_settings_and_secret_backup_is_explicit',async()=>{
  await resetDelivery();const data=await w.evaluate(async()=>{const b=await exportSettingsBackup();globalThis.__b18_backup=b;return{version:b.backup_version,secrets:b.contains_secrets,hash:b.settings_sha256};});assert.equal(data.version,3);assert.equal(data.secrets,true);
  // Retain backup solely in QA driver for a fresh-install restore below, not page or logs.
  globalThis.b18Backup=await w.evaluate(()=>__b18_backup);const prev=wTarget;await w.evaluate(()=>{setTimeout(()=>chrome.runtime.reload(),0);});await getWorker(prev);await instrument();await providerFixture();
  const restored=await w.evaluate(async()=>{const b=await exportSettingsBackup();return{hash:b.settings_sha256,secret:(await YMBCredentialRuntime.settings()).credentials.search.api_key};});assert.equal(restored.hash,data.hash);assert.equal(restored.secret,b18Secret('search'));
  return{extension_reloaded_same_path:true,settings_preserved:true,version_upgrade_test:false};
 });
 await runCase('fresh_install_backup_restore_checksum_guard_and_no_secret_in_content',async()=>{
  assert.ok(globalThis.b18Backup);await browser.close();await delay(500);const oldPids=memory();assert.equal(oldPids.rss_kib,0);clearInterval(monitor);
  // New dedicated profile means separate extension storage, no owner state.
  browser=await puppeteer.launch({headless:false,pipe:true,enableExtensions:true,userDataDir:path.resolve(out,'fresh-install-profile'),protocolTimeout:30000,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--host-resolver-rules=MAP * ~NOTFOUND',`--disable-extensions-except=${root}`,`--load-extension=${root}`]});pid=browser.process().pid;await getWorker();await instrument();await providerFixture();
  const empty=await w.evaluate(async()=>(await YMBCredentialRuntime.settings()).credentials.search?.api_key||'');assert.equal(empty,'');
  const b=globalThis.b18Backup,mut=structuredClone(b);mut.settings.debug_mode=!mut.settings.debug_mode;
  const denied=await w.evaluate(async b=>{try{await importSettingsBackup(b);return null;}catch(e){return e.code;}},mut);assert.equal(denied,'BACKUP_CHECKSUM_MISMATCH');
  const done=await w.evaluate(async b=>{const r=await importSettingsBackup(b);return{imported:r.imported,round:(await exportSettingsBackup()).settings_sha256,publicState:await publicGlobalSettingsState()};},b);assert.equal(done.imported,true);assert.equal(done.round,b.settings_sha256);
  for(const s of ['wordstat','search','webmaster','metrika','direct'])assert.ok(!JSON.stringify(done.publicState).includes(b18Secret(s)));
  assert.equal((await snap()).hits.length,0);globalThis.b18Backup=null;return{fresh_install_empty:true,tampered_rejected:true,five_credentials_roundtrip:true,real_provider_calls:0};
 });
 assert.equal(tree(),target);emit({case:'B18_immutable_candidate',status:'PASS',tree:target,errors,failed,release_allowed:false});
}catch(e){failed++;emit({case:stage,status:'FAIL_QUALIFICATION',error:String(e.stack||e),release_allowed:false});}
