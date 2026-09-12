 // Supplemental cases only: main B15 unchanged successful matrix is not rerun.
 await runCase('manual_double_send_single_commit_and_single_click',async()=>{
  await resetDelivery();await w.evaluate(()=>chrome.storage.local.set({wsmb_auto_send:false}));
  const d=await stageFile(1,'double-send');await until(async()=>(await outbox())?.phase==='attachment_ready','NOT_READY');await delay(1100);
  const before=await fx(),counts=await messageCounts();
  await page.evaluate(()=>{const b=document.getElementById('composer-submit-button');b.click();b.click();});
  await until(async()=>!(await outbox()),'DOUBLE_SEND_NOT_ACKED');await delay(700);
  const after=await fx(),next=await messageCounts();
  assert.equal(after.sends.length-before.sends.length,1,'two manual clicks must not produce two DOM sends');
  assert.equal((next.WS_COMMIT_ATTACHMENT_SEND||0)-(counts.WS_COMMIT_ATTACHMENT_SEND||0),1,'one durable send authorization');
  assert.deepEqual(await artifactGone(d.key),{remaining:0,meta:false});
  return{send_count:1,commit_count:1,duplicate_click_blocked:true};
 });
 await runCase('corrupt_chunk_stops_before_DataTransfer_no_automatic_retry',async()=>{
  await resetDelivery();await w.evaluate(()=>chrome.storage.local.set({wsmb_auto_send:true}));
  await w.evaluate(()=>{const old=handleMessage;globalThis.__b15_corrupt=false;handleMessage=async(m,s)=>{const r=await old(m,s);if(__b15_corrupt&&m?.type==='WS_GET_OUTBOX_ARTIFACT_CHUNK'&&r?.ok)return{...r,sha256:'0'.repeat(64)};return r;};__b15_corrupt=true;});
  const before=await fx(),c=await messageCounts(),d=await stageFile(1,'corrupt');
  await until(async()=>(await messageCounts()).WS_GET_OUTBOX_ARTIFACT_CHUNK>(c.WS_GET_OUTBOX_ARTIFACT_CHUNK||0),'NO_CHUNK');await delay(2300);
  const after=await fx(),c2=await messageCounts();assert.equal(after.sends.length,before.sends.length);assert.equal(after.changes,before.changes);
  assert.equal(c2.WS_GET_OUTBOX_ARTIFACT_CHUNK-(c.WS_GET_OUTBOX_ARTIFACT_CHUNK||0),1);assert.equal((await outbox()).phase,'attachment_committed');
  assert.equal((await artifactGone(d.key)).meta,true);await w.evaluate(()=>{__b15_corrupt=false;});await resetDelivery();assert.deepEqual(await artifactGone(d.key),{remaining:0,meta:false});
  return{failed_chunk_calls:1,DataTransfer_changes:0,sends:0,committed_not_replayed:true,explicit_test_cleanup:true};
 });
 await runCase('page_reload_missing_attachment_never_reattaches_or_sends',async()=>{
  await resetDelivery();await w.evaluate(()=>chrome.storage.local.set({wsmb_auto_send:false}));const d=await stageFile(1,'reload');await until(async()=>(await outbox())?.phase==='attachment_ready','NOT_READY');
  const c=await messageCounts();await page.reload({waitUntil:'domcontentloaded'});await delay(2300);
  const s=await fx(),next=await messageCounts();assert.equal(s.sends.length,0);assert.equal(s.changes,0);assert.equal((await outbox()).phase,'attachment_ready');
  assert.equal(next.WS_GET_OUTBOX_ARTIFACT_CHUNK,c.WS_GET_OUTBOX_ARTIFACT_CHUNK);assert.equal((await artifactGone(d.key)).meta,true);
  await resetDelivery();assert.deepEqual(await artifactGone(d.key),{remaining:0,meta:false});return{no_reattachment:true,no_send:true,source_retained_until_explicit_cleanup:true};
 });
 await runCase('1500_item_real_worker_restart_pause_resume_cancel',async()=>{
  await resetDelivery();
  const oldSession=await w.evaluate(async()=>{const S=YMBSearchAsyncStore,j='b15-restart-1500',o='owner-large',now=1;
   await S.createJob({jobId:j,owner:o,queries:Array.from({length:1500},(_,i)=>'q'+i),parameters:{region:'225'},folderId:'qa',maxRequests:1500,maxCostMicrorub:150000,unitCostMicrorub:100,now});
   await S.control({jobId:j,owner:o,action:'pause',now:2});const paused=await S.claim({jobId:j,owner:o,workerId:WORKER_SESSION_ID,attemptId:'paused',kind:'submit',now:3});if(paused.allowed)throw new Error('PAUSE_IGNORED');await S.control({jobId:j,owner:o,action:'resume',now:4});
   for(let i=0;i<750;i++){const a='s'+i;await S.claim({jobId:j,owner:o,workerId:WORKER_SESSION_ID,attemptId:a,kind:'submit',now:5});await S.finishSubmit({jobId:j,owner:o,index:i,attemptId:a,outcome:'received',operationId:j+'-'+i,rawText:'saved-'+i,now:6});await S.finishNormalization({jobId:j,owner:o,index:i,normalized:{results:[{url:'https://example.test/'+i}]},now:7});}
   await S.claim({jobId:j,owner:o,workerId:WORKER_SESSION_ID,attemptId:'interrupted',kind:'submit',now:8});return WORKER_SESSION_ID;});
  const oldTarget=wTarget;await w.close();await getWorker(oldTarget);await instrument();assert.notEqual(await w.evaluate(()=>WORKER_SESSION_ID),oldSession);
  const r=await w.evaluate(async()=>{const S=YMBSearchAsyncStore,j='b15-restart-1500',o='owner-large';await S.recover({jobId:j,owner:o,workerId:WORKER_SESSION_ID,now:9});
   const recovered=await S.getSummary(j,o),blocked=await S.claim({jobId:j,owner:o,workerId:WORKER_SESSION_ID,attemptId:'no-replay',kind:'submit',now:10});await S.control({jobId:j,owner:o,action:'cancelPending',now:11});
   let count=0,after=-1,verifiedRaw=0;for(;;){const p=await S.pageItems(j,o,{after,limit:100});if(!p.rows.length)break;for(const i of p.rows){if(i.index!==count++)throw new Error('INDEX_LOST');if(i.state==='SUCCEEDED'){if((await S.readResult(j,o,i.index)).raw_text!=='saved-'+i.index)throw new Error('RAW_LOST');verifiedRaw++;}}after=p.next_after;}
   return{recovered,blocked,final:await S.getSummary(j,o),count,verifiedRaw};});
  assert.equal(r.recovered.counts.SUCCEEDED,750);assert.equal(r.recovered.counts.UNKNOWN,1);assert.equal(r.recovered.counts.PENDING,749);assert.equal(r.blocked.allowed,false);
  assert.equal(r.final.counts.CANCELLED,749);assert.equal(r.final.counts.UNKNOWN,1);assert.equal(r.final.requests_started,751);assert.equal(r.count,1500);assert.equal(r.verifiedRaw,750);
  return{items:1500,completed_raw_verified:750,unknown:1,cancelled_unsent:749,reservations_preserved:751,actual_worker_closed:true,no_provider_calls:true};
 });
 // No forced GC. A fresh post-restart worker begins this separate repeated-run trace.
 const endpoints=[];
 for(let i=0;i<3;i++){
  const ok=await runCase('64MiB_post_idle_repeat_'+i,async()=>{
   await resetDelivery();await w.evaluate(()=>chrome.storage.local.set({wsmb_auto_send:true}));const before=await fx(),d=await stageFile(64,'idle-repeat-'+i);
   await until(async()=>(await fx()).sends.length===before.sends.length+1,'REPEAT_NOT_SENT',60000);await until(async()=>!(await outbox()),'REPEAT_NOT_ACKED');
   assert.deepEqual(await artifactGone(d.key),{remaining:0,meta:false});await delay(5000);const m=memory();endpoints.push(m.rss_kib);return{mib:64,idle_ms:5000,post_idle_rss_kib:m.rss_kib,no_forced_GC:true};
  });if(!ok)break;
 }
 emit({case:'additional_idle_memory_observations',status:'RECORDED',endpoints_kib:endpoints,not_a_universal_leak_proof:true,release_allowed:false});
