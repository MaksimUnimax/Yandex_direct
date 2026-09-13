// Reload qualification without a debugger attached to the worker being reloaded.
// getContexts + real runtime messages observe both sides; no synthetic worker globals.
try {
 stage='single_install_no_worker_debugger';
 browser=await puppeteer.launch({headless:false,pipe:true,enableExtensions:true,targetFilter:t=>t.type()!=='service_worker',userDataDir:path.resolve(out,'unattached-profile'),protocolTimeout:10000,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--host-resolver-rules=MAP * ~NOTFOUND']});pid=browser.process().pid;
 deadline=setTimeout(()=>{resourceStop=true;void browser.close();},45000);
 monitor=setInterval(()=>{try{const m=memory();fs.appendFileSync(path.join(out,'rss.jsonl'),JSON.stringify({stage,...m})+'\n');if(m.rss_kib>2097152){resourceStop=true;void browser.close();}}catch{}},250);
 extensionId=await browser.installExtension(root);assert.equal(tree(),target);
 assert.ok(!browser.targets().some(t=>t.type()==='service_worker'),'worker debugger must not be attached in this isolated venue');
 page=await browser.newPage();await page.goto(`chrome-extension://${extensionId}/popup.html`,{waitUntil:'domcontentloaded',timeout:8000});
 const before=await page.evaluate(async()=>{
  for(const s of ['wordstat','search','webmaster','metrika','direct']){
   const credential=['wordstat','search'].includes(s)?{api_key:'QA_NO_DEBUG_'+s,folder_id:'qa-only'}:{oauth_token:'QA_NO_DEBUG_'+s};
   const r=await chrome.runtime.sendMessage({type:'YMB_SAVE_SERVICE_CREDENTIAL',service:s,credential});if(!r.ok)throw new Error('SAVE_FAILED_'+s);
  }
  const r=await chrome.runtime.sendMessage({type:'WS_EXPORT_BACKUP'});if(!r.ok)throw new Error('BACKUP_FAILED');
  const contexts=await chrome.runtime.getContexts({contextTypes:['BACKGROUND']});
  return {hash:r.backup.settings_sha256,version:chrome.runtime.getManifest().version,background_contexts:contexts.map(c=>c.contextId),saved_five:true};
 });assert.equal(before.background_contexts.length,1);emit({case:'pre_reload_actual_message_and_context',status:'PASS',...before});
 stage='unattached_same_folder_runtime_reload';
 await page.evaluate(()=>{setTimeout(()=>chrome.runtime.reload(),50);return true;});await delay(500);
 let after=null;const attempts=[];
 for(let i=0;i<5&&!after;i++){
  let p;try{
   p=await browser.newPage();await p.goto(`chrome-extension://${extensionId}/popup.html`,{waitUntil:'domcontentloaded',timeout:1500});
   after=await p.evaluate(async()=>{
    const r=await chrome.runtime.sendMessage({type:'WS_EXPORT_BACKUP'});if(!r.ok)throw new Error('AFTER_BACKUP_FAILED');
    const c=r.backup.settings.credentials;
    const contexts=await chrome.runtime.getContexts({contextTypes:['BACKGROUND']});
    const state=await chrome.runtime.sendMessage({type:'WS_GET_STATE'});
    return {hash:r.backup.settings_sha256,version:chrome.runtime.getManifest().version,background_contexts:contexts.map(c=>c.contextId),all_five_same:['wordstat','search','webmaster','metrika','direct'].every(s=>(c[s].api_key||c[s].oauth_token)==='QA_NO_DEBUG_'+s),public_secret_exposure:JSON.stringify(state).includes('QA_NO_DEBUG_'),password_blank:document.getElementById('searchApiKey').value===''};
   });
  }catch(e){attempts.push(String(e.message));}finally{if(p)await p.close().catch(()=>{});}if(!after)await delay(250);
 }
 assert.ok(after,'No functioning extension page after unattached reload: '+attempts.join('; '));
 assert.equal(after.hash,before.hash);assert.equal(after.version,before.version);assert.equal(after.background_contexts.length,1);assert.notEqual(after.background_contexts[0],before.background_contexts[0]);assert.equal(after.all_five_same,true);assert.equal(after.public_secret_exposure,false);assert.equal(after.password_blank,true);
 emit({case:'same_folder_reload_without_worker_debugger',status:'PASS',before,after,attempts,version_changed:false,network_checks_executed:false,real_provider_calls:0});
 assert.equal(tree(),target);emit({case:'unattached_reload_product_immutable',status:'PASS',tree:target,release_allowed:false});
} catch(e) {
 failed++;emit({case:stage,status:'FAIL_QUALIFICATION',error:String(e.stack||e),release_allowed:false});
}
