// A separate single-install API venue for runtime.reload, on unchanged B17.
// The previous CLI-installed reload failed; that result remains historical FAIL.
// No --load-extension / --disable-extensions-except is used in this venue.
try {
 stage='api_single_install';
 browser=await puppeteer.launch({headless:false,pipe:true,enableExtensions:true,userDataDir:path.resolve(out,'api-profile'),protocolTimeout:15000,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--host-resolver-rules=MAP * ~NOTFOUND']});
 pid=browser.process().pid;
 deadline=setTimeout(()=>{resourceStop=true;void browser.close();},60000);
 monitor=setInterval(()=>{try{const m=memory();fs.appendFileSync(path.join(out,'rss.jsonl'),JSON.stringify({stage,...m})+'\n');if(m.rss_kib>2097152){resourceStop=true;void browser.close();}}catch{}},250);
 const installed=await browser.installExtension(root);await getWorker();assert.equal(extensionId,installed);await instrument();
 assert.equal(tree(),target);
 emit({case:'exact_API_single_install',status:'PASS',tree:target,extension_id:installed,chrome:await browser.version(),CLI_install:false});
 const before=await w.evaluate(async()=>{
  for(const service of ['wordstat','search','webmaster','metrika','direct'])await YMBCredentialRuntime.save(service,service==='wordstat'||service==='search'?{api_key:'QA_RELOAD_'+service,folder_id:'qa-only',check_state:'PRESENT'}:{oauth_token:'QA_RELOAD_'+service,check_state:'PRESENT'});
  await chrome.storage.local.set({ymb_debug_mode:true,wsmb_auto_send:false});
  const b=await exportSettingsBackup();return{hash:b.settings_sha256,worker_session:WORKER_SESSION_ID,version:chrome.runtime.getManifest().version,network:__b15_network};
 });
 assert.equal(before.network,0);
 stage='reload_same_unpacked_folder';
 page=await browser.newPage();await page.goto(`chrome-extension://${extensionId}/popup.html`,{waitUntil:'domcontentloaded',timeout:10000});
 await page.evaluate(()=>{setTimeout(()=>chrome.runtime.reload(),50);return true;});
 await delay(750);
 let session=null,observed=[];
 await until(async()=>{
  for(const t of browser.targets()){
   if(t.type()!=='service_worker'||t.url()!==`chrome-extension://${installed}/phase3_service_worker_bootstrap.js`)continue;
   let c;
   try{
    c=await t.createCDPSession();const r=await c.send('Runtime.evaluate',{expression:'JSON.stringify({session:typeof WORKER_SESSION_ID==="string"?WORKER_SESSION_ID:null,ready:globalThis.YMBSearchAdmissionBinding?.ready})',returnByValue:true},{timeout:1500});
    const v=JSON.parse(r.result.value);observed.push(v);
    if(v.session&&v.session!==before.worker_session&&v.ready===true){session=v.session;wTarget=t;w=await t.worker();return true;}
   }catch(e){observed.push({error:String(e.message).slice(0,180)});}finally{if(c)await c.detach().catch(()=>{});}
  }
  return false;
 },'API_INSTALLED_RELOAD_NEW_SESSION_NOT_READY',20000);
 await instrument();
 const after=await w.evaluate(async()=>{
  const b=await exportSettingsBackup(),c=(await YMBCredentialRuntime.settings()).credentials;
  return{hash:b.settings_sha256,worker_session:WORKER_SESSION_ID,all_five_same:['wordstat','search','webmaster','metrika','direct'].every(s=>(c[s].api_key||c[s].oauth_token)==='QA_RELOAD_'+s),version:chrome.runtime.getManifest().version,public:await publicGlobalSettingsState(),network:__b15_network};
 });
 assert.notEqual(after.worker_session,before.worker_session);assert.equal(after.worker_session,session);assert.equal(after.hash,before.hash);assert.equal(after.all_five_same,true);assert.equal(after.version,before.version);assert.equal(after.network,0);assert.ok(!JSON.stringify(after.public).includes('QA_RELOAD_'));
 const popup=await browser.newPage();try{await popup.goto(`chrome-extension://${installed}/popup.html`,{waitUntil:'domcontentloaded',timeout:10000});assert.equal(await popup.$eval('#searchApiKey',e=>e.value),'');}finally{await popup.close();}
 emit({case:'same_folder_runtime_reload_five_credentials_and_settings',status:'PASS',new_worker_session:true,version_changed:false,all_five_same:true,settings_checksum_same:true,public_secret_exposure:false,live_provider_calls:0,observed});
 assert.equal(tree(),target);assert.equal(resourceStop,false);
 emit({case:'reload_product_immutable',status:'PASS',tree:target,independent_gate:false,release_allowed:false});
} catch(error) {
 failed++;emit({case:stage,status:'FAIL_QUALIFICATION',error:String(error.stack||error),targets:browser?.targets().map(t=>({type:t.type(),url:t.url()})),release_allowed:false});
}
