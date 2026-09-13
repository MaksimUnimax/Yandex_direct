"""Apply exact QA-only fixes to the first B18 generated harness, never product.
Usage: b18_fixture_recheck.py FIRST_GENERATED_SCRIPT
All functional assertions remain. The first failing run is retained separately.
"""
from pathlib import Path
import hashlib,sys
H=lambda b:hashlib.sha256(b).hexdigest()
p=Path(sys.argv[1]);before=p.read_bytes()
if H(before)!='f17ab8878768d1255cf0ecb85f430dd6d3c44ee9b659f4729d14c5e136be4fdd':raise ValueError('Unknown first QA input')
s=before.decode()
old=""" const p=await popupOpen();try{await p.$eval('#activeService',(e,s)=>{e.value=s;e.dispatchEvent(new Event('change',{bubbles:true}));},service);
 await until(async()=>w.evaluate(async({key,s})=>(await getServiceContext(key)).active_service===s,{key:KEY,s:service}),'SERVICE_NOT_PERSISTED');}finally{await p.close();}"""
new=""" // Service selection intentionally requires Save and Manual OFF. A change event
 // alone is only an unsaved form edit, not the production persistence contract.
 if(await w.evaluate(async key=>getManualMode(key),KEY))await manualMode(false);
 const p=await popupOpen();try{await p.$eval('#activeService',(e,s)=>{if(e.disabled)throw new Error('SERVICE_DISABLED');e.value=s;e.dispatchEvent(new Event('change',{bubbles:true}));},service);
 await p.$eval('#saveSettingsTop',e=>e.click());
 await until(async()=>w.evaluate(async({key,s})=>(await getServiceContext(key)).active_service===s,{key:KEY,s:service}),'SERVICE_NOT_PERSISTED');}finally{await p.close();}"""
if s.count(old)!=1:raise ValueError('Service fixture mismatch')
s=s.replace(old,new)
old="  await manualMode(true);\n  const text="
new="  await switchService('wordstat');await manualMode(true);\n  const text="
if s.count(old)!=1:raise ValueError('Scenario isolation mismatch')
s=s.replace(old,new)
old="  globalThis.b18Backup=await w.evaluate(()=>__b18_backup);const prev=wTarget;await w.evaluate(()=>{setTimeout(()=>chrome.runtime.reload(),0);});await getWorker(prev);await instrument();await providerFixture();"
new="""  globalThis.b18Backup=await w.evaluate(()=>__b18_backup);const prev=wTarget;
  const destroyed=new Promise((resolve,reject)=>{const timer=setTimeout(()=>{browser.off('targetdestroyed',listener);reject(new Error('RELOAD_TARGET_NOT_DESTROYED'));},10000);const listener=t=>{if(t===prev){clearTimeout(timer);browser.off('targetdestroyed',listener);resolve();}};browser.on('targetdestroyed',listener);});
  // Return the debugger command before reload destroys its execution context.
  await w.client.send('Runtime.evaluate',{expression:'setTimeout(()=>chrome.runtime.reload(),50); true',returnByValue:true,awaitPromise:false});await destroyed;
  const wake=await browser.newPage();try{await wake.goto(`chrome-extension://${extensionId}/popup.html`,{waitUntil:'domcontentloaded',timeout:10000});await getWorker(prev);}finally{await wake.close();}
  await instrument();await providerFixture();"""
if s.count(old)!=1:raise ValueError('Reload fixture mismatch')
s=s.replace(old,new);after=s.encode()
if H(after)!='c7df7ea3a1b54322918f7b09cc7bb403384f0926a65a046b4581e70f04b7aa92':raise ValueError('Unknown fixed QA result')
p.write_bytes(after)
print('QA-only exact fixture adaptation PASS; production unchanged; first failures retained')
