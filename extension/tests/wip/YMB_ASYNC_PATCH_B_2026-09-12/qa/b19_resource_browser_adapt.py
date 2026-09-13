"""QA-only deterministic adaptation of exact saved B17 browser resource harness.
Changes only: B19 tree guard + one stale-control race. Product bytes/assertions stay intact.
Usage: b19_resource_browser_adapt.py B17_BROWSER_SOURCE OUTPUT
"""
from pathlib import Path
import hashlib,sys,json
H=lambda b:hashlib.sha256(b).hexdigest()
src,out=map(Path,sys.argv[1:3]);b=src.read_bytes()
if H(b)!='1a30a1bf4327690233735d968584fadc0f871c7acaccba817a67bd7279eadeb2':raise ValueError('Unexpected B17 browser preimage')
s=b.decode();old_tree='b20b74351d95becd67f32994e3e00899e9208b8c32c778a306f73f6703bfe508';new_tree='b87246c1377cda57cb9135f92814ec6885a1b607a9539be3a27bbc2fb1918b86'
if s.count(old_tree)!=1:raise ValueError('tree guard mismatch')
s=s.replace(old_tree,new_tree)
old="""await runCase('durable_pause_survives_page_reload_without_reads_or_send',async()=>{\n await resetDelivery();await page.$eval('#prompt-textarea',e=>e.value='HOLD');const d=await stageFile(10,'b17-reload');await clickControl();await until(async()=>(await pausedState())?.paused,'PRE_RELOAD_PAUSE_MISSING');const counts=await messageCounts();await page.reload({waitUntil:'domcontentloaded'});await delay(2000);\n assert.equal((await pausedState()).paused,true);assert.equal((await fx()).changes,0);assert.equal((await fx()).sends.length,0);assert.equal((await messageCounts()).WS_GET_OUTBOX_ARTIFACT_CHUNK||0,counts.WS_GET_OUTBOX_ARTIFACT_CHUNK||0);assert.equal((await artifactGone(d.key)).meta,true);await resetDelivery();return{reload_pause_retained:true,automatic_materialization:0,artifact_deleted:false};\n});"""
new="""await runCase('durable_pause_survives_page_reload_without_reads_or_send',async()=>{\n await resetDelivery();await page.$eval('#prompt-textarea',e=>e.value='HOLD');const beforePoll=(await messageCounts()).WS_GET_OUTBOX||0;const d=await stageFile(10,'b17-reload');\n await until(async()=>{const e=await outbox(),c=await messageCounts();return e?.id===d.id&&(c.WS_GET_OUTBOX||0)>beforePoll;},'NEW_DELIVERY_NOT_OBSERVED_BY_CONTENT');await delay(250);\n await clickControl();await until(async()=>(await pausedState())?.paused,'PRE_RELOAD_PAUSE_MISSING');const counts=await messageCounts();await page.reload({waitUntil:'domcontentloaded'});await delay(2000);\n assert.equal((await pausedState()).paused,true);assert.equal((await fx()).changes,0);assert.equal((await fx()).sends.length,0);assert.equal((await messageCounts()).WS_GET_OUTBOX_ARTIFACT_CHUNK||0,counts.WS_GET_OUTBOX_ARTIFACT_CHUNK||0);assert.equal((await artifactGone(d.key)).meta,true);await resetDelivery();return{reload_pause_retained:true,automatic_materialization:0,artifact_deleted:false,qa_stale_control_race_removed:true};\n});"""
if s.count(old)!=1:raise ValueError('durable pause block mismatch')
s=s.replace(old,new)
# The original pause-write-failure test deliberately occupies the composer so file bytes are NOT read.
# Do not wait for an impossible chunk request; the assertion being tested is local stop vs durable pause write failure.
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(s)
assert out.read_text()!=b.decode();assert out.read_text().count(new_tree)==1
print(json.dumps({'source_sha256':H(b),'adapted_sha256':H(out.read_bytes()),'product_change':False,'tree':new_tree,'qa_changes':['B19 tree guard','wait new delivery poll before durable-pause click'],'kept_original_pause_write_failure_case':True},indent=2))
