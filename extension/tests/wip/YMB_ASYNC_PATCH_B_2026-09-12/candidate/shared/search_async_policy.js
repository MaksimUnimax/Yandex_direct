/* B4 policy adapter: persisted admission shared by deferred jobs.
 * Internal module; no command ingress, no provider calls, no automatic recovery.
 * Reads existing Search policy/credentials; never mutates other service settings.
 * All legacy callers must join admission before cross-mode concurrency is certified.
 */
(() => {
  "use strict";
  const DB_NAME = "ymb_search_async_admission_v1", DB_VERSION = 1;
  const PRICE_MICRORUB = 30500; // Conservative day-price ceiling, NOT an invoice.
  const TARIFF_SOURCE = "https://aistudio.yandex.ru/ru/docs/search-api/pricing";
  const TARIFF_CHECKED_AT = "2026-09-12";
  const fail = code => { throw Object.assign(new Error(code), { code }); };
  const str = (v, max = 240) => { if (typeof v !== "string" || !v || v.length > max || /[\u0000-\u001f\u007f]/u.test(v)) fail("ASYNC_POLICY_INVALID_TEXT"); return v; };
  const uint = v => { if (!Number.isSafeInteger(v) || v < 0) fail("ASYNC_POLICY_INVALID_NUMBER"); return v; };
  const request = r => new Promise((resolve, reject) => { r.onsuccess = () => resolve(r.result); r.onerror = () => reject(r.error || new Error("ASYNC_POLICY_IDB_REQUEST")); });
  function open() {
    return new Promise((resolve, reject) => {
      const r = indexedDB.open(DB_NAME, DB_VERSION);
      r.onupgradeneeded = () => {
        const db = r.result;
        if (!db.objectStoreNames.contains("bindings")) db.createObjectStore("bindings", { keyPath: "job_id" });
        if (!db.objectStoreNames.contains("scopes")) db.createObjectStore("scopes", { keyPath: "scope_id" });
        if (!db.objectStoreNames.contains("rates")) db.createObjectStore("rates", { keyPath: ["folder_id", "lane"] });
        if (!db.objectStoreNames.contains("attempts")) {
          const s = db.createObjectStore("attempts", { keyPath: ["job_id", "attempt_id"] });
          s.createIndex("unsettled", ["job_id", "status", "attempt_id"], { unique: false });
        }
      };
      r.onerror = () => reject(r.error || new Error("ASYNC_POLICY_IDB_OPEN"));
      r.onblocked = () => reject(new Error("ASYNC_POLICY_IDB_BLOCKED"));
      r.onsuccess = () => { r.result.onversionchange = () => r.result.close(); resolve(r.result); };
    });
  }
  async function tx(names, mode, work) {
    const db = await open();
    try {
      return await new Promise((resolve, reject) => {
        const t = db.transaction(names, mode, mode === "readwrite" ? { durability: "strict" } : undefined);
        let value, failure;
        t.oncomplete = () => resolve(value);
        t.onabort = () => reject(failure || t.error || new Error("ASYNC_POLICY_IDB_ABORTED"));
        t.onerror = () => { failure ||= t.error; };
        Promise.resolve().then(() => work(t)).then(v => { value = v; }, e => { failure = e; try { t.abort(); } catch { reject(e); } });
      });
    } finally { db.close(); }
  }
  function scopeKey(owner, scopeId, folderId) { return JSON.stringify([owner, scopeId, folderId]); }
  function freshScope(scope_id, legacy_run_id) {
    return { scope_id, legacy_run_id, submissions: 0, polls: 0, charge_microrub: 0, pending: 0, holds: 0, revision: 0 };
  }
  function checkBinding(b, args) {
    if (!b) fail("ASYNC_POLICY_BINDING_MISSING");
    if (b.owner !== args.owner) fail("ASYNC_POLICY_WRONG_OWNER");
    if (args.folderId !== undefined && b.folder_id !== args.folderId) fail("ASYNC_POLICY_FOLDER_MISMATCH");
  }
  function checkContext(a) {
    str(a.jobId,128); str(a.owner,1000); str(a.attemptId,128); str(a.folderId,50); uint(a.index);
    if (!["submit", "collect"].includes(a.kind)) fail("ASYNC_POLICY_KIND_INVALID");
  }
  function publicScope(s) { return { submissions: s.submissions, polls: s.polls, estimated_budget_charge_microrub: s.charge_microrub, pending: s.pending, holds: s.holds, revision: s.revision, invoice_confirmed: false }; }
  function sameAttempt(record, a) { return record.owner === a.owner && record.folder_id === a.folderId && record.kind === a.kind && record.index === a.index; }
  function create({ policyModel = globalThis.YMBPolicyModel, credentialRegistry = globalThis.YMBCredentialRegistry,
    getPolicy = globalThis.getSearchPolicy, getSettings = globalThis.getSettings, getAutoRun = globalThis.getAutoRun,
    workerId, now = Date.now, minIntervalMs = 200 } = {}) {
    str(workerId,128);
    if (!policyModel?.normalizeSearchPolicy || !policyModel?.searchDecision || !credentialRegistry?.capabilityForService ||
      [getPolicy,getSettings,getAutoRun,now].some(f => typeof f !== "function")) fail("ASYNC_POLICY_DEPENDENCY_REQUIRED");
    if (!Number.isSafeInteger(minIntervalMs) || minIntervalMs < 100) fail("ASYNC_POLICY_RATE_INVALID");
    const clock = () => uint(now());
    async function bindJob({ jobId, owner, folderId, scopeId, runId = null }) {
      str(jobId,128); str(owner,1000); str(folderId,50); str(scopeId,128);
      if (runId !== null) str(runId,128);
      const b = { job_id: jobId, owner, folder_id: folderId, scope_id: scopeKey(owner,scopeId,folderId), run_id: runId };
      return tx(["bindings","scopes"],"readwrite",async t => {
        const old = await request(t.objectStore("bindings").get(jobId));
        if (old) { if (JSON.stringify(old) !== JSON.stringify(b)) fail("ASYNC_POLICY_REBIND_FORBIDDEN"); return { bound: true, duplicate: true }; }
        const s = await request(t.objectStore("scopes").get(b.scope_id));
        if (s && s.legacy_run_id !== runId) fail("ASYNC_POLICY_SCOPE_RUN_MISMATCH");
        if (!s) t.objectStore("scopes").add(freshScope(b.scope_id,runId));
        t.objectStore("bindings").add(b); return { bound: true, duplicate: false };
      });
    }
    async function readBinding(jobId, owner, folderId) {
      str(jobId,128); str(owner,1000);
      return tx(["bindings"],"readonly",async t => { const b=await request(t.objectStore("bindings").get(jobId)); checkBinding(b,{owner,folderId}); return b; });
    }
    async function reserve(a) {
      checkContext(a);
      const binding = await readBinding(a.jobId,a.owner,a.folderId);
      // All external/Chrome reads finish BEFORE the IndexedDB transaction.
      const [rawPolicy, settings, legacy] = await Promise.all([getPolicy(), getSettings(), binding.run_id ? getAutoRun(a.owner) : null]);
      if (binding.run_id && (!legacy || legacy.run_id !== binding.run_id || legacy.active_service !== "search")) fail("ASYNC_POLICY_RUN_CHANGED");
      const policy = policyModel.normalizeSearchPolicy(rawPolicy || {});
      const capability = credentialRegistry.capabilityForService("search", settings);
      if (settings?.credentials?.search?.folder_id !== binding.folder_id) fail("ASYNC_POLICY_CREDENTIAL_CONTEXT_CHANGED");
      const externalRequests = legacy ? uint(legacy.requests_executed) : 0;
      const externalCost = legacy ? uint(Math.round(legacy.estimated_cost_rub * 1e6)) : 0;
      const at = clock();
      return tx(["bindings","scopes","attempts","rates"],"readwrite",async t => {
        const b=await request(t.objectStore("bindings").get(a.jobId));checkBinding(b,a);
        if (b.scope_id !== binding.scope_id) fail("ASYNC_POLICY_REBIND_FORBIDDEN");
        const old=await request(t.objectStore("attempts").get([a.jobId,a.attemptId]));
        if (old) { if (!sameAttempt(old,a)) fail("ASYNC_POLICY_ATTEMPT_COLLISION"); return { allowed:false, reason:"DUPLICATE_POLICY_ATTEMPT" }; }
        const s=await request(t.objectStore("scopes").get(b.scope_id));if(!s)fail("ASYNC_POLICY_SCOPE_MISSING");
        if(s.pending) return {allowed:false,reason:"POLICY_ATTEMPT_PENDING"};
        if(a.kind==="submit" && s.holds) return {allowed:false,reason:"POLICY_RECONCILIATION_REQUIRED"};
        // Use the REAL existing Search admission model with a local cost projection.
        // GET checks credentials/permissions but not a new Search request budget.
        const cost=a.kind==="submit"?PRICE_MICRORUB:0;
        const run=a.kind==="submit"?{requests_executed:uint(externalRequests+s.submissions),estimated_cost_rub:uint(externalCost+s.charge_microrub)/1e6}:{};
        const decision=policyModel.searchDecision({policy:{...policy,method_cost_rub:{...policy.method_cost_rub,search:cost/1e6}},channel:"manual",method:"search",credentialState:capability.state,run});
        if(!decision.allow)return{allowed:false,reason:decision.reason};
        const lane=a.kind;
        const rate=await request(t.objectStore("rates").get([b.folder_id,lane]));
        if(rate && at<rate.next_at)return{allowed:false,reason:"ASYNC_GLOBAL_RATE_WAIT",next_allowed_at:rate.next_at};
        const record={job_id:a.jobId,attempt_id:a.attemptId,owner:a.owner,folder_id:a.folderId,kind:a.kind,index:a.index,scope_id:b.scope_id,worker_id:workerId,status:"reserved",reserved_microrub:cost,created_at:at};
        s.pending++;if(a.kind==="submit")s.submissions++;else s.polls++;s.charge_microrub+=cost;s.revision++;
        t.objectStore("scopes").put(s);t.objectStore("attempts").add(record);
        t.objectStore("rates").put({folder_id:b.folder_id,lane,next_at:uint(at+minIntervalMs)});
        return{allowed:true,estimated_cost_rub:cost/1e6,tariff_source:TARIFF_SOURCE,tariff_checked_at:TARIFF_CHECKED_AT,progress:publicScope(s)};
      });
    }
    async function settle(a) {
      checkContext(a);
      if(![true,false,"UNKNOWN"].includes(a.request_executed)||typeof a.local_saved!=="boolean")fail("ASYNC_POLICY_SETTLEMENT_INVALID");
      if(a.http_status!==null&&a.http_status!==undefined && (!Number.isInteger(a.http_status)||a.http_status<100||a.http_status>599))fail("ASYNC_POLICY_SETTLEMENT_INVALID");
      if(![null,undefined,"accepted","waiting","received","provider_error","not_sent","rejected","unknown","read_error"].includes(a.outcome))fail("ASYNC_POLICY_SETTLEMENT_INVALID");
      if(a.operation_id!==null&&a.operation_id!==undefined && (typeof a.operation_id!=="string"||!/^[A-Za-z0-9_-]{1,240}$/.test(a.operation_id)))fail("ASYNC_POLICY_SETTLEMENT_INVALID");
      const stamp=JSON.stringify([a.request_executed,a.http_status??null,a.outcome??null,a.local_saved,a.operation_id??null]);
      const at=clock();
      return tx(["bindings","scopes","attempts"],"readwrite",async t=>{
        const b=await request(t.objectStore("bindings").get(a.jobId));checkBinding(b,a);
        const r=await request(t.objectStore("attempts").get([a.jobId,a.attemptId]));
        // Denied/throwing admission may have created no policy record; nothing to refund.
        if(!r){if(a.request_executed===false)return{settled:true,not_reserved:true};fail("ASYNC_POLICY_RESERVATION_MISSING");}
        if(!sameAttempt(r,a))fail("ASYNC_POLICY_ATTEMPT_COLLISION");
        if(r.status!=="reserved"){if(r.settlement===stamp)return{settled:true,duplicate:true};fail("ASYNC_POLICY_SETTLEMENT_CONFLICT");}
        const s=await request(t.objectStore("scopes").get(r.scope_id));if(!s||s.pending<1)fail("ASYNC_POLICY_ACCOUNTING_INVALID");
        s.pending--;
        const definitelyNotSent=a.request_executed===false;
        // Only definite HTTP auth/internal-server outcomes get a known-free credit.
        // Other completed Operation failures remain conservative estimates, not invoices.
        const free=definitelyNotSent||(a.request_executed===true&&[401,403,500].includes(a.http_status));
        if(free)s.charge_microrub-=r.reserved_microrub;
        if(definitelyNotSent){if(r.kind==="submit")s.submissions--;else s.polls--;}
        const uncertain=((r.kind==="submit"&&(a.request_executed==="UNKNOWN"||a.outcome==="unknown"))||!a.local_saved);
        if(uncertain)s.holds++;
        for(const k of ["pending","submissions","polls","charge_microrub","holds"])uint(s[k]);
        s.revision++;
        t.objectStore("scopes").put(s);
        t.objectStore("attempts").put({...r,status:uncertain?"unresolved":"settled",settlement:stamp,settled_at:at,budget_credit_microrub:free?r.reserved_microrub:0});
        return{settled:true,submit_blocked:s.holds>0,progress:publicScope(s)};
      });
    }
    async function recover({jobId,owner,workerId:requestedWorker}) {
      str(jobId,128);str(owner,1000);if(requestedWorker!==workerId)fail("ASYNC_POLICY_WORKER_MISMATCH");
      const at=clock();
      return tx(["bindings","scopes","attempts"],"readwrite",async t=>{
        const b=await request(t.objectStore("bindings").get(jobId));checkBinding(b,{owner});
        const s=await request(t.objectStore("scopes").get(b.scope_id));if(!s)fail("ASYNC_POLICY_SCOPE_MISSING");
        const r=await request(t.objectStore("attempts").index("unsettled").get(IDBKeyRange.bound([jobId,"reserved",""],[jobId,"reserved","\uffff"])));
        if(r){
          if(r.worker_id===workerId)return{allowed:false,reason:"POLICY_ATTEMPT_STILL_ACTIVE"};
          if(s.pending<1)fail("ASYNC_POLICY_ACCOUNTING_INVALID");
          // Recovery cannot prove that a network request was never sent. Never refund blindly.
          s.pending--;if(r.kind==="submit")s.holds++;s.revision++;t.objectStore("scopes").put(s);
          t.objectStore("attempts").put({...r,status:"unresolved",recovered_at:at,recovery_worker:workerId});
        }
        return{allowed:true,submit_blocked:s.holds>0,progress:publicScope(s)};
      });
    }
    async function getSummary(jobId,owner) {
      return tx(["bindings","scopes"],"readonly",async t=>{
        const b=await request(t.objectStore("bindings").get(jobId));checkBinding(b,{owner});
        const s=await request(t.objectStore("scopes").get(b.scope_id));if(!s)fail("ASYNC_POLICY_SCOPE_MISSING");return publicScope(s);
      });
    }
    return Object.freeze({bindJob,reserve,settle,recover,getSummary});
  }
  globalThis.YMBSearchAsyncPolicy=Object.freeze({create,DB_NAME,DB_VERSION,PRICE_MICRORUB,TARIFF_SOURCE,TARIFF_CHECKED_AT});
})();
