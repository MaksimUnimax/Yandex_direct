"""B18 second QA-only readiness correction. Never changes product bytes.
Usage: b18_ready_recheck.py SECOND_GENERATED_SCRIPT
Preserves every functional assertion; adds explicit asynchronous preconditions.
"""
from pathlib import Path
import hashlib,sys
H=lambda b:hashlib.sha256(b).hexdigest()
p=Path(sys.argv[1]);raw=p.read_bytes()
if H(raw)!='c7df7ea3a1b54322918f7b09cc7bb403384f0926a65a046b4581e70f04b7aa92':raise ValueError('Unknown second QA input')
s=raw.decode()
pairs=[
("await until(async()=>(await actions()).length===4,'LEGACY_ADAPTER_COUNT');", "await until(async()=>{const a=await actions();return a.length===4&&a.every(x=>!x.disabled);},'LEGACY_ADAPTER_COUNT_AND_ADMISSION');"),
("const pop=await popupOpen();try{await pop.$eval('#pickSend',e=>e.click());}finally{await pop.close();}\n  await delay(200);", "const pop=await popupOpen();try{await pop.$eval('#pickSend',e=>e.click());await until(async()=>(await plaques()).filter(x=>x.key==='picker-state').length===1,'PICKER_MESSAGE_NOT_APPLIED');}finally{await pop.close();}\n  await delay(200);"),
("const other=await openFixture(OTHER_URL);try{const r=await(await realm(other)).evaluate", "const other=await openFixture(OTHER_URL);try{await until(async()=>{for(const r of other.extensionRealms())if((await r.extension())?.id===extensionId)return true;return false;},'FOREIGN_CONTENT_NOT_READY');const r=await(await realm(other)).evaluate")]
for old,new in pairs:
 if s.count(old)!=1:raise ValueError('Readiness preimage mismatch')
 s=s.replace(old,new)
a=s.index('  globalThis.b18Backup=await w.evaluate(()=>__b18_backup);const prev=wTarget;')
b=s.index('  const restored=await w.evaluate',a)
s=s[:a]+'''  globalThis.b18Backup=await w.evaluate(()=>__b18_backup);
  const beforeSession=await w.evaluate(()=>WORKER_SESSION_ID),events=[];
  const changed=t=>{if(t.url().startsWith('chrome-extension://'))events.push({type:t.type(),url:t.url()});};
  browser.on('targetcreated',changed);browser.on('targetdestroyed',changed);
  // Reload through an extension page, not an evaluation in the dying worker.
  // A new persisted worker session proves bootstrap restart even if the debugger
  // target object's lifecycle differs from the page-owned lifecycle.
  const control=await browser.newPage();await control.goto(`chrome-extension://${extensionId}/popup.html`,{waitUntil:'domcontentloaded'});
  await control.evaluate(()=>{setTimeout(()=>chrome.runtime.reload(),50);return true;});await delay(500);
  try{await control.close();}catch{}
  const wake=await browser.newPage();
  try{
   await wake.goto(`chrome-extension://${extensionId}/popup.html`,{waitUntil:'domcontentloaded',timeout:10000});
   await until(async()=>{
    for(const t of browser.targets()){
     if(t.type()!=='service_worker'||t.url()!==`chrome-extension://${extensionId}/phase3_service_worker_bootstrap.js`)continue;
     let c;try{c=await t.createCDPSession();const r=await c.send('Runtime.evaluate',{expression:'JSON.stringify({session:typeof WORKER_SESSION_ID === "string"?WORKER_SESSION_ID:null,ready:globalThis.YMBSearchAdmissionBinding?.ready})',returnByValue:true},{timeout:2000});const value=JSON.parse(r.result.value);if(value.session&&value.session!==beforeSession&&value.ready){wTarget=t;w=await t.worker();return true;}}catch{}finally{if(c)await c.detach().catch(()=>{});}
    }return false;
   },'NEW_BOOTSTRAP_SESSION_NOT_OBSERVED',20000);
  }finally{await wake.close();browser.off('targetcreated',changed);browser.off('targetdestroyed',changed);emit({case:'reload_target_events',status:'RECORDED',events});}
  await instrument();await providerFixture();
''' +s[b:]
post=s.encode()
if H(post)!='a6e4cf87d1c5724bc251d887607c42313741378861a8315ff42704e3d3905f6e':raise ValueError('Wrong qualified QA postimage')
p.write_bytes(post)
print('QA readiness synchronization changed only; same product/assertion objectives; prior FAIL retained')
