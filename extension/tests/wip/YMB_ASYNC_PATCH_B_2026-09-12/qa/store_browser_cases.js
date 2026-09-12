/* Real IndexedDB contract tests; zero Yandex/provider traffic. */
(() => {
  const S = YMBSearchAsyncStore;
  const OWNER = 'https://chatgpt.com|11111111-1111-4111-8111-111111111111';
  const assert = (ok, label) => { if (!ok) throw new Error(label); };
  const equal = (a, b, label) => assert(JSON.stringify(a) === JSON.stringify(b), `${label}: ${JSON.stringify(a)} != ${JSON.stringify(b)}`);
  const rejects = async (fn, code) => { try { await fn(); } catch (e) { if (code) equal(e.code || e.name, code, 'error classification'); return; } throw new Error(`Expected rejection ${code}`); };
  const create = (id, n = 2, extra = {}) => S.createJob({ jobId: id, owner: OWNER, queries: Array.from({length:n}, (_, i) => `тест ${i}`), parameters: {region:'225', groupsOnPage:10}, folderId:'folder-test', maxRequests:n, maxCostMicrorub:n*30500, unitCostMicrorub:30500, now:1000, ...extra });
  const claim = (jobId, token, kind='submit', now=1000, owner=OWNER, workerId='worker-A') => S.claim({jobId, owner, workerId, attemptId:token, kind, now});
  const accepted = async (jobId, token, op, index, now=1000) => S.finishSubmit({jobId, owner:OWNER, index, attemptId:token, outcome:'accepted', operationId:op, nextPollAt:now+300000, now});
  const raw = JSON.stringify({id:'op',done:true,response:{rawData:'dGVzdA=='}});
  const collectDone = (id, token, index, outcome='received', extra={}) => S.finishCollect({jobId:id,owner:OWNER,index,attemptId:token,outcome,rawText:raw,now:302000,...extra});
  const normalized = {results:[{rank:1,url:'https://example.test/item',domain:'example.test',title:'Тест'}],result_count:1,response_format:'FORMAT_XML'};
  let seq=0;
  const id = prefix => `${prefix}-${++seq}`;
  async function accounting(jobId) {
    const p=await S.getSummary(jobId,OWNER);
    equal(Object.values(p.counts).reduce((a,b)=>a+b,0),p.total,'counts sum');
    const all=[]; let after=-1;
    for (;;) {const p=await S.pageItems(jobId,OWNER,{after,limit:100});all.push(...p.rows);if(!p.rows.length)break;after=p.next_after;}
    equal(all.length,p.total,'all item identities');
    equal(new Set(all.map(v=>v.index)).size,p.total,'unique indexes');
    for(const state of S.STATES)equal(all.filter(v=>v.state===state).length,p.counts[state],`state ${state}`);
    return p;
  }
  const cases={
    async create_duplicate_and_owner() {
      const j=id('create');const p=await create(j);equal(p.counts.PENDING,2,'pending');
      await rejects(()=>create(j),'ASYNC_JOB_ALREADY_EXISTS');
      for(const fn of [()=>S.getSummary(j,'other'),()=>S.pageItems(j,'other'),()=>S.readResult(j,'other',0),()=>claim(j,'bad','submit',1000,'other')])await rejects(fn,'ASYNC_WRONG_OWNER');
      equal((await accounting(j)).requests_started,0,'wrong owner sent nothing');
    },
    async concurrent_claim_exactly_one() {
      const j=id('race');await create(j);const r=await Promise.all([claim(j,'a'),claim(j,'b')]);
      equal(r.filter(v=>v.allowed).length,1,'one paid boundary');equal((await accounting(j)).requests_started,1,'one reserve');
      const winner=r[0].allowed?'a':'b';await accepted(j,winner,`${j}-op`,0);
      equal((await accounting(j)).operations_accepted,1,'accepted');
    },
    async repeated_attempt_never_admits_second_item() {
      const j=id('attempt');await create(j);const a=await claim(j,'once');await accepted(j,'once',`${j}-op`,a.item.index);
      const again=await claim(j,'once');assert(!again.allowed,'settled attempt must not authorize a second paid request');
      equal((await accounting(j)).requests_started,1,'repeat budget unchanged');
    },
    async budget_exhaustion_and_get_independence() {
      const j=id('budget');await create(j,2,{maxCostMicrorub:30500});await claim(j,'s');await accepted(j,'s',`${j}-op`,0);
      equal((await claim(j,'s2')).reason,'BUDGET_LIMIT','budget fence');
      const p=await claim(j,'p','collect',302000);assert(p.allowed,'GET permitted after budget exhaustion');
      await collectDone(j,'p',0);const done=await accounting(j);equal(done.reserved_microrub,30500,'GET free from Search estimate');equal(done.polls_started,1,'poll count');
    },
    async unknown_submit_recovery_is_fail_closed() {
      const j=id('recover');await create(j);await claim(j,'s');await S.recover({jobId:j,owner:OWNER,workerId:'worker-B',now:2000});
      const p=await accounting(j);equal(p.counts.UNKNOWN,1,'unknown');equal(p.reserved_microrub,30500,'reserve retained');
      equal((await claim(j,'again')).reason,'UNKNOWN_SUBMIT_REQUIRES_RECONCILIATION','no replay');
      await rejects(()=>accepted(j,'s',`${j}-late`,0),'ASYNC_STALE_ATTEMPT');
    },
    async collect_survives_another_unknown_submit() {
      const j=id('partial');await create(j,3);await claim(j,'one');await accepted(j,'one',`${j}-op`,0);await claim(j,'two');
      await S.recover({jobId:j,owner:OWNER,workerId:'worker-B',now:2000});
      const c=await claim(j,'p','collect',302000);assert(c.allowed,'known paid result still recoverable');
      await collectDone(j,'p',0);await accounting(j);
    },
    async poll_cooldown_and_network_read_error() {
      const j=id('cool');await create(j,1);await claim(j,'s');await accepted(j,'s',`${j}-op`,0);
      equal((await claim(j,'too-early','collect',2000)).reason,'NO_DUE_OPERATIONS','min time');
      await claim(j,'p','collect',302000);await collectDone(j,'p',0,'read_error',{nextPollAt:400000,errorCode:'NETWORK_ERROR'});
      equal((await claim(j,'p-early','collect',350000)).reason,'NO_DUE_OPERATIONS','error backoff');
      const row=(await S.pageItems(j,OWNER)).rows[0];equal(row.operation_id,`${j}-op`,'same operation');
      equal((await accounting(j)).requests_started,1,'no POST from read failure');
    },
    async interrupted_collect_restores_only_get() {
      const j=id('read-recovery');await create(j,1);await claim(j,'s');await accepted(j,'s',`${j}-op`,0);await claim(j,'p','collect',302000);
      await S.recover({jobId:j,owner:OWNER,workerId:'worker-new',now:303000});
      const p=await accounting(j);equal(p.counts.WAITING,1,'back to waiting');equal(p.requests_started,1,'no replay');
      await rejects(()=>collectDone(j,'p',0),'ASYNC_STALE_ATTEMPT');
      assert((await claim(j,'p2','collect',303000)).allowed,'later GET allowed');await collectDone(j,'p2',0);
    },
    async raw_first_parse_failure_local_repair_and_duplicate_commit() {
      const j=id('parse');await create(j,1);await claim(j,'s');await accepted(j,'s',`${j}-op`,0);await claim(j,'p','collect',302000);
      await collectDone(j,'p',0);const duplicate=await collectDone(j,'p',0);assert(duplicate.duplicate,'duplicate collect is idempotent');
      equal((await S.readResult(j,OWNER,0)).raw_text,raw,'raw retained');
      await S.finishNormalization({jobId:j,owner:OWNER,index:0,errorCode:'INVALID_XML',now:303000});
      equal((await S.readResult(j,OWNER,0)).raw_text,raw,'raw retained after parse failure');
      await S.finishNormalization({jobId:j,owner:OWNER,index:0,normalized,now:304000});
      const p=await accounting(j);assert(p.all_successful,'success only after parse');equal(p.requests_started,1,'parse never replays');
      equal((await S.readResult(j,OWNER,0)).normalized,normalized,'normalized retained');
    },
    async failure_not_empty_success() {
      const j=id('provider-error');await create(j,1);await claim(j,'s');await accepted(j,'s',`${j}-op`,0);await claim(j,'p','collect',302000);
      await collectDone(j,'p',0,'provider_error',{errorCode:'AUTH_FAILED'});const p=await accounting(j);
      equal(p.counts.FAILED,1,'failed not empty');assert(!p.all_successful,'not success');assert(await S.readResult(j,OWNER,0),'error evidence retained');
    },
    async raw_and_state_transaction_abort() {
      const j=id('abort');await create(j,1);await claim(j,'s');await accepted(j,'s',`${j}-op`,0);await claim(j,'p','collect',302000);
      const original=IDBObjectStore.prototype.put;let injected=false;
      IDBObjectStore.prototype.put=function(value,...rest){const r=original.call(this,value,...rest);if(this.name==='results'&&value.job_id===j){injected=true;this.transaction.abort();}return r;};
      try { await rejects(()=>collectDone(j,'p',0)); } finally {IDBObjectStore.prototype.put=original;}
      assert(injected,'abort injection reached');assert(!await S.readResult(j,OWNER,0),'aborted raw not committed');
      equal((await accounting(j)).counts.COLLECTING,1,'state rolled back together');
    },
    async operation_identity_collision_rolls_back() {
      const j=id('collision');await create(j,2);await claim(j,'a');await accepted(j,'a',`${j}-same`,0);await claim(j,'b');
      await rejects(()=>accepted(j,'b',`${j}-same`,1));
      const p=await accounting(j);equal(p.operations_accepted,1,'no false acceptance');equal(p.counts.SUBMITTING,1,'rollback retains unknown window');
    },
    async pause_cancel_and_known_operations_preserved() {
      const j=id('cancel');await create(j,3);await claim(j,'s');await S.control({jobId:j,owner:OWNER,action:'pause',now:2000});
      await accepted(j,'s',`${j}-op`,0);equal((await claim(j,'next')).reason,'PAUSED','pause prevents new work');
      await S.control({jobId:j,owner:OWNER,action:'cancelPending',now:3000});const p=await accounting(j);equal(p.counts.CANCELLED,2,'only pending cancelled');equal(p.counts.WAITING,1,'known operation not destroyed');
      assert((await claim(j,'p','collect',302000)).allowed,'cancelled pending does not discard accepted result');await collectDone(j,'p',0);
      await rejects(()=>S.control({jobId:j,owner:OWNER,action:'resume',now:303000}),'ASYNC_CANCELLED_NO_RESUME');
    },
    async cancel_cannot_be_cleared_through_pause() {
      const j=id('cancel-pause');await create(j);await S.control({jobId:j,owner:OWNER,action:'cancelPending',now:2000});
      await rejects(()=>S.control({jobId:j,owner:OWNER,action:'pause',now:3000}),'ASYNC_CANCELLED_NO_RESUME');
      equal((await accounting(j)).control,'CANCELLED','cancellation remains terminal');
    },
    async validation_and_paging_bounds() {
      await rejects(()=>create(id('size'),1501),'ASYNC_JOB_SIZE_INVALID');
      await rejects(()=>create(id('secret'),1,{parameters:{api_key:'not-a-real-secret'}}),'ASYNC_PARAMETERS_FIELD_FORBIDDEN');
      const j=id('page');await create(j,251);let a=-1;const lengths=[];for(;;){const p=await S.pageItems(j,OWNER,{after:a,limit:100});lengths.push(p.rows.length);if(!p.rows.length)break;a=p.next_after;}
      equal(lengths,[100,100,51,0],'paged no truncation');await rejects(()=>S.pageItems(j,OWNER,{limit:101}),'ASYNC_PAGE_INVALID');await accounting(j);
    }
  };
  window.runStoreCase=async name=>{try{await cases[name]();return{name,status:'PASS'};}catch(error){return{name,status:'FAIL',message:String(error.message),stack:error.stack};}};
  window.storeCaseNames=Object.keys(cases);
  window.scaleStore=async(n,run)=>{
    const j=id(`scale-${n}-${run}`);const started=performance.now();let gets=0,puts=0,maxJobBytes=0;
    const get=IDBObjectStore.prototype.get,put=IDBObjectStore.prototype.put,add=IDBObjectStore.prototype.add;
    const idxget=IDBIndex.prototype.get,all=IDBObjectStore.prototype.getAll;
    IDBObjectStore.prototype.get=function(...a){gets++;return get.apply(this,a);};
    IDBIndex.prototype.get=function(...a){gets++;return idxget.apply(this,a);};
    const countWrite=function(original,value,...a){puts++;if(this.name==='jobs')maxJobBytes=Math.max(maxJobBytes,new TextEncoder().encode(JSON.stringify(value)).byteLength);return original.call(this,value,...a);};
    IDBObjectStore.prototype.put=function(...a){return countWrite.call(this,put,...a);};
    IDBObjectStore.prototype.add=function(...a){return countWrite.call(this,add,...a);};
    IDBObjectStore.prototype.getAll=function(){throw new Error('Full-store read forbidden in scale path');};
    try{
      await create(j,n);
      for(let i=0;i<n;i++){
        const t=`${j}-s-${i}`;const c=await claim(j,t);assert(c.allowed,'submit granted');equal(c.item.index,i,'stable order');await accepted(j,t,`${j}-op-${i}`,i);
      }
      const submitted=performance.now();
      for(let i=0;i<n;i++){
        const t=`${j}-p-${i}`;const c=await claim(j,t,'collect',302000);assert(c.allowed,'GET granted');
        await collectDone(j,t,i,'received',{rawText:raw+' '.repeat(8192)});
        await S.finishNormalization({jobId:j,owner:OWNER,index:i,normalized,now:303000});
      }
      const p=await accounting(j);assert(p.all_successful,'complete');equal(p.requests_started,n,'requests');equal(p.polls_started,n,'polls');
      assert(maxJobBytes<4096,'job metadata must not grow into array');assert(gets<n*30+30,'bounded reads per item');assert(puts<n*20+20,'bounded writes per item');
      return {name:`scale-${n}-${run}`,status:'PASS',items:n,submit_ms:Math.round(submitted-started),total_ms:Math.round(performance.now()-started),gets,puts,max_job_bytes:maxJobBytes,all_successful:p.all_successful,job_id:j};
    }finally{IDBObjectStore.prototype.get=get;IDBObjectStore.prototype.put=put;IDBObjectStore.prototype.add=add;IDBIndex.prototype.get=idxget;IDBObjectStore.prototype.getAll=all;}
  };
})();
