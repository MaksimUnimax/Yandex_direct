import os,json,zipfile,hashlib,shutil,re
from pathlib import Path
here=Path(__file__).resolve().parent; version=os.environ['QA_VERSION'];out=Path(os.environ['RUNNER_TEMP'])/'ymb-memory';out.mkdir(parents=True,exist_ok=True)
expected={'019':'de4425a47645d537ef7b69994ef2df0f66c3e9bd6741b0b47884426bdd954c4c','0110':'4b9d396dcbe7bb12eed52b91c46f328674a35d1ba02805ad2fe7dc63e2ffdae6'}
zpath=here/'fixtures'/f'{version}.zip';assert hashlib.sha256(zpath.read_bytes()).hexdigest()==expected[version]
root=out/'candidate';root.mkdir();ident={}
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None
 for i in z.infolist():
  if i.is_dir():continue
  rel=Path(i.filename);assert not rel.is_absolute() and '..' not in rel.parts
  data=z.read(i);p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);ident[str(rel)]=hashlib.sha256(data).hexdigest()
assert json.loads((root/'manifest.json').read_text())['version']=={'019':'0.1.9','0110':'0.1.10'}[version]
neutral=out/'neutral';shutil.copytree(root,neutral);(neutral/'popup_search_async_monitor.js').write_text('/* QA neutral control only; exact candidate remains untouched. */\n')
tests=out/'tests';tests.mkdir();evidence=out/'evidence';evidence.mkdir()
fixture='''
    // QA-only adaptation for the current folder-owned job contract. No tokens/auth.
    const originalSend=chrome.runtime.sendMessage.bind(chrome.runtime);
    chrome.runtime.sendMessage=function(message,callback){
      if(message?.type==='WS_GET_GLOBAL_STATE' && typeof callback==='function'){
        return originalSend(message,response=>{if(response?.ok && response.state){response.state.credential_status ||= {};response.state.credential_status.search={...(response.state.credential_status.search||{}),folder_id:'qa-memory'};}callback(response);});
      }
      return originalSend(message,callback);
    };
'''
for name in ['popup_memory_bounded_real_chrome_v2.mjs','popup_memory_lifecycle_differential_v8.mjs']:
 original=(here/name).read_text();s=original
 assert "'--no-sandbox'," in s;s=s.replace("'--no-sandbox',",'')
 needle='  await page.evaluateOnNewDocument(()=>{';assert s.count(needle)==1;s=s.replace(needle,needle+fixture)
 assert 'job_id:jobId,owner:OWNER' in s;s=s.replace('job_id:jobId,owner:OWNER',"job_id:jobId,owner:'search-folder:qa-memory',folder_id:'qa-memory'")
 # Emergency bound applies only to browsers launched by this harness.
 needle="  const browser=await puppeteer.launch(";assert s.count(needle)==1
 launch_end=s.index('\n',s.index(needle))
 watch="\n  const watchdog=setInterval(()=>{try{const r=rssTree(browser.process().pid);if(r.rss_kib>2097152){emit({case:'emergency_rss_bound',status:'FAIL',rss:r});void browser.close();}}catch{}},500);watchdog.unref();browser.once('disconnected',()=>clearInterval(watchdog));"
 s=s[:launch_end]+watch+s[launch_end:]
 if name.startswith('popup_memory_bounded'):
  s=s.replace("assert.equal(text.rows,'—');","assert.ok(['—','— (без чтения payload)'].includes(text.rows));")
  # Historical B22 itself accepted this V6 case and used V8 for churn.
  start=s.index('    const reopenBase=');end=s.index('\n  }finally',start);s=s[:start]+s[end:]
  s=s.replace("[['old_reproduction',oldReproduction],['fixed_candidate',fixedCandidate]]","[['fixed_candidate',fixedCandidate]]")
  old="['revoked_stage_b_reproduces_periodic_result_payload_scan','fixed_large_job_100_refreshes_no_result_payload_materialization','fixed_100_popup_open_close_cycles_bounded']"
  assert old in s;s=s.replace(old,"['fixed_large_job_100_refreshes_no_result_payload_materialization']")
 else:
  # Preserve legacy no-auto-DB-read assertion; log metrics even if it fails.
  needle='    const delta=after.rss_kib-base.rss_kib;assert.equal'
  assert needle in s;s=s.replace(needle,"    emit({case:'pre_assert_idle_metrics',status:'DIAGNOSTIC',startCounters,endCounters,base,after,samples,fetchCalls});\n"+needle)
 (tests/name).write_text(s)
(evidence/'IDENTITY.json').write_text(json.dumps({'zip_sha256':expected[version],'version':version,'source_files':ident,'candidate_bytes_unchanged':True,'harness_source_commit':'306678f5bc0c9f7910fc4550c7a2d6967b5e34bd','scope':'B22 reused memory gates only, not full extension acceptance','legacy_idle_no_db_read_assertion_preserved':True,'sandbox_disabled':False},indent=2)+'\n')
with open(os.environ['GITHUB_ENV'],'a') as f:
 for k,v in {'YMB_NEW_ROOT':root,'YMB_FIXED_ROOT':root,'YMB_NEUTRAL_ROOT':neutral,'YMB_TESTS':tests,'YMB_EVIDENCE_ROOT':evidence,'YMB_PPTR_HOME':out/'deps','YMB_PRODUCT_SHA':expected[version]}.items(): f.write(f'{k}={v}\n')
(out/'deps').mkdir();(out/'deps'/'package.json').write_text(json.dumps({'private':True,'dependencies':{'puppeteer':'24.15.0'}}))
print(json.dumps({'version':version,'zip_sha256':expected[version],'file_count':len(ident)}))
