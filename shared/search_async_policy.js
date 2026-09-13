/* B5: shared admission for Search, GenSearch and deferred calls.
 * Internal factory only. No startup, provider requests or secret persistence.
 * Legacy callers must disable their old pre-increment while the guard is active.
 * UI counters are a versioned mirror; the transactional ledger owns the budget.
 */
(() => {
  "use strict";
  const DB_NAME = "ymb_search_async_admission_v1", DB_VERSION = 2;
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
  const paid = kind => kind !== "collect";
  function freshScope(scope_id, legacy_run_id, seedRequests, seedCost) {
    return { scope_id, legacy_run_id, schema_version: 2, seed_requests: seedRequests, seed_cost_microrub: seedCost,
      submissions: 0, polls: 0, charge_microrub: 0, pending: 0, holds: 0, revision: 0 };
  }
  function requireScope(s) {
    if (!s) fail("ASYNC_POLICY_SCOPE_MISSING");
    if (s.schema_version !== 2) fail("SHARED_ADMISSION_MIGRATION_REQUIRED");
    uint(s.seed_requests); uint(s.seed_cost_microrub);
    return s;
  }
  function checkBinding(b, args) {
    if (!b) fail("ASYNC_POLICY_BINDING_MISSING");
    if (b.owner !== args.owner) fail("ASYNC_POLICY_WRONG_OWNER");
    if (args.folderId !== undefined && b.folder_id !== args.folderId) fail("ASYNC_POLICY_FOLDER_MISMATCH");
  }
  function checkContext(a) {
    str(a.jobId,128); str(a.owner,1000); str(a.attemptId,128); str(a.folderId,50); uint(a.index);
    if (!["submit", "collect", "search", "genSearch"].includes(a.kind)) fail("ASYNC_POLICY_KIND_INVALID");
  }
  function publicScope(s) { return { submissions: s.submissions, polls: s.polls,
    estimated_budget_charge_microrub: s.charge_microrub,
    total_requests: uint(s.seed_requests + s.submissions),
    total_cost_microrub: uint(s.seed_cost_microrub + s.charge_microrub),
    pending: s.pending, holds: s.holds, revision: s.revision, invoice_confirmed: false }; }
  function sameAttempt(record, a) { return record.owner === a.owner && record.folder_id === a.folderId && record.kind === a.kind && record.index === a.index; }
  function create({ policyModel = globalThis.YMBPolicyModel, credentialRegistry = globalThis.YMBCredentialRegistry,
    getPolicy = globalThis.getSearchPolicy, getSettings = globalThis.getSettings, getAutoRun = globalThis.getAutoRun,
    workerId, now = Date.now, minIntervalMs = 200, publishRunTotals = null } = {}) {
    str(workerId,128);
    if (!policyModel?.normalizeSearchPolicy || !policyModel?.searchDecision || !credentialRegistry?.capabilityForService ||
      [getPolicy,getSettings,getAutoRun,now].some(f => typeof f !== "function")) fail("ASYNC_POLICY_DEPENDENCY_REQUIRED");
    if (!Number.isSafeInteger(minIntervalMs) || minIntervalMs < 100) fail("ASYNC_POLICY_RATE_INVALID");
    const clock = () => uint(now());
    async function bindJob({ jobId, owner, folderId, scopeId, runId = null, mode = "deferred", channel = "manual", credentialCheckConfirmed = false }) {
      str(jobId,128); str(owner,1000); str(folderId,50); str(scopeId,128);
      if (runId !== null) str(runId,128);
      if (!["deferred", "legacy", "credential_check"].includes(mode) || !["manual", "autorun", "credential_check"].includes(channel)) fail("SHARED_ADMISSION_BINDING_INVALID");
      if (mode === "credential_check" ? channel !== "credential_check" || runId !== null || credentialCheckConfirmed !== true : channel === "credential_check") fail("SHARED_CHECK_CONSENT_REQUIRED");
      if (mode === "deferred" && channel !== "manual") fail("SHARED_DEFERRED_AUTORUN_NOT_SUPPORTED");
      if (runId && typeof publishRunTotals !== "function") fail("SHARED_RUN_MIRROR_REQUIRED");
      const legacy = runId ? await getAutoRun(owner) : null;
      if (runId && (!legacy || legacy.run_id !== runId || legacy.active_service !== "search")) fail("ASYNC_POLICY_RUN_CHANGED");
      const seedRequests = legacy ? uint(legacy.requests_executed) : 0;
      const seedCost = legacy ? uint(Math.round(legacy.estimated_cost_rub * 1e6)) : 0;
      // One canonical budget per existing run, regardless of caller-supplied scope alias.
      const canonicalScope = runId ? `run:${runId}` : scopeId;
      const b = { job_id: jobId, owner, folder_id: folderId, scope_id: scopeKey(owner,canonicalScope,folderId), run_id: runId, mode, channel };
      return tx(["bindings","scopes"],"readwrite",async t => {
        const old = await request(t.objectStore("bindings").get(jobId));
        if (old) { if (JSON.stringify(old) !== JSON.stringify(b)) fail("ASYNC_POLICY_REBIND_FORBIDDEN"); return { bound: true, duplicate: true }; }
        const s = await request(t.objectStore("scopes").get(b.scope_id));
        if (s) { requireScope(s); if (s.legacy_run_id !== runId) fail("ASYNC_POLICY_SCOPE_RUN_MISMATCH"); }
        if (!s) t.objectStore("scopes").add(freshScope(b.scope_id,runId,seedRequests,seedCost));
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
      // Counters are seeded only once at bind. Adding the live mirror here would
      // count the same legacy or deferred request twice.
      if ((binding.mode !== "deferred") !== ["search", "genSearch"].includes(a.kind) || (binding.mode === "credential_check" && a.kind !== "search")) fail("SHARED_ADMISSION_MODE_MISMATCH");
      const at = clock();
      return tx(["bindings","scopes","attempts","rates"],"readwrite",async t => {
        const b=await request(t.objectStore("bindings").get(a.jobId));checkBinding(b,a);
        if (b.scope_id !== binding.scope_id) fail("ASYNC_POLICY_REBIND_FORBIDDEN");
        const old=await request(t.objectStore("attempts").get([a.jobId,a.attemptId]));
        if (old) { if (!sameAttempt(old,a)) fail("ASYNC_POLICY_ATTEMPT_COLLISION"); return { allowed:false, reason:"DUPLICATE_POLICY_ATTEMPT" }; }
        const s=requireScope(await request(t.objectStore("scopes").get(b.scope_id)));
        if(s.pending) return {allowed:false,reason:"POLICY_ATTEMPT_PENDING"};
        if(paid(a.kind) && s.holds) return {allowed:false,reason:"POLICY_RECONCILIATION_REQUIRED"};
        // Use the REAL existing Search admission model with a local cost projection.
        // GET checks credentials/permissions but not a new Search request budget.
        const method = a.kind === "genSearch" ? "genSearch" : "search";
        const cost = a.kind === "submit" ? PRICE_MICRORUB : a.kind === "collect" ? 0 : uint(Math.round(policy.method_cost_rub[method] * 1e6));
        const run = paid(a.kind) ? { requests_executed: uint(s.seed_requests+s.submissions), estimated_cost_rub: uint(s.seed_cost_microrub+s.charge_microrub)/1e6 } : {};
        const check = b.mode === "credential_check";
        // Existing credential Check is a separately confirmed single request, not
        // Manual/Autorun work. It must still be possible to re-check an invalid key.
        const effectivePolicy = check ? {...policy, manual_enabled:true, allowed_methods:["search"], max_requests_per_run:1, max_cost_rub_per_run:cost/1e6} : policy;
        const credentialState = check && capability.has_api_key && capability.has_folder_id ? "PRESENT" : capability.state;
        const decision=policyModel.searchDecision({policy:{...effectivePolicy,method_cost_rub:{...policy.method_cost_rub,[method]:cost/1e6}},channel:check?"manual":b.channel,method,credentialState,run});
        if(!decision.allow)return{allowed:false,reason:decision.reason};
        const lane=a.kind;
        const rate=await request(t.objectStore("rates").get([b.folder_id,lane]));
        if(rate && at<rate.next_at)return{allowed:false,reason:"ASYNC_GLOBAL_RATE_WAIT",next_allowed_at:rate.next_at};
        const record={job_id:a.jobId,attempt_id:a.attemptId,owner:a.owner,folder_id:a.folderId,kind:a.kind,index:a.index,scope_id:b.scope_id,worker_id:workerId,status:"reserved",reserved_microrub:cost,created_at:at};
        s.pending++;if(paid(a.kind))s.submissions++;else s.polls++;s.charge_microrub+=cost;s.revision++;
        t.objectStore("scopes").put(s);t.objectStore("attempts").add(record);
        t.objectStore("rates").put({folder_id:b.folder_id,lane,next_at:uint(at+(lane === "genSearch" ? Math.max(1000,minIntervalMs) : minIntervalMs))});
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
        const s=requireScope(await request(t.objectStore("scopes").get(r.scope_id)));if(s.pending<1)fail("ASYNC_POLICY_ACCOUNTING_INVALID");
        s.pending--;
        const definitelyNotSent=a.request_executed===false;
        // Only definite HTTP auth/internal-server outcomes get a known-free credit.
        // Other completed Operation failures remain conservative estimates, not invoices.
        const free=definitelyNotSent||(a.request_executed===true&&[401,403,500].includes(a.http_status));
        if(free)s.charge_microrub-=r.reserved_microrub;
        if(definitelyNotSent){if(paid(r.kind))s.submissions--;else s.polls--;}
        const uncertain=((paid(r.kind)&&(a.request_executed==="UNKNOWN"||a.outcome==="unknown"))||!a.local_saved);
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
        const s=requireScope(await request(t.objectStore("scopes").get(b.scope_id)));
        const r=await request(t.objectStore("attempts").index("unsettled").get(IDBKeyRange.bound([jobId,"reserved",""],[jobId,"reserved","\uffff"])));
        if(r){
          if(r.worker_id===workerId)return{allowed:false,reason:"POLICY_ATTEMPT_STILL_ACTIVE"};
          if(s.pending<1)fail("ASYNC_POLICY_ACCOUNTING_INVALID");
          // Recovery cannot prove that a network request was never sent. Never refund blindly.
          s.pending--;if(paid(r.kind))s.holds++;s.revision++;t.objectStore("scopes").put(s);
          t.objectStore("attempts").put({...r,status:"unresolved",recovered_at:at,recovery_worker:workerId});
        }
        return{allowed:true,submit_blocked:s.holds>0,progress:publicScope(s)};
      });
    }
    async function getSummary(jobId,owner) {
      return tx(["bindings","scopes"],"readonly",async t=>{
        const b=await request(t.objectStore("bindings").get(jobId));checkBinding(b,{owner});
        const s=requireScope(await request(t.objectStore("scopes").get(b.scope_id)));return publicScope(s);
      });
    }
    async function publish(jobId, owner, result) {
      const binding = await readBinding(jobId, owner);
      if (binding.run_id) {
        const progress = await getSummary(jobId, owner);
        await publishRunTotals({ owner, runId: binding.run_id, scopeId: binding.scope_id,
          requests_executed: progress.total_requests, estimated_cost_rub: progress.total_cost_microrub / 1e6,
          revision: progress.revision });
      }
      return result;
    }
    // IDB commits precede any Chrome/run-mirror write. A mirror error is explicit;
    // callers must stop and reconcile, never silently return an admission PASS.
    return Object.freeze({bindJob,
      reserve: async a => { const r=await reserve(a); return r.allowed ? publish(a.jobId,a.owner,r) : r; },
      settle: async a => publish(a.jobId,a.owner,await settle(a)),
      recover: async a => publish(a.jobId,a.owner,await recover(a)), getSummary});
  }
  globalThis.YMBSearchAsyncPolicy=Object.freeze({create,DB_NAME,DB_VERSION,PRICE_MICRORUB,TARIFF_SOURCE,TARIFF_CHECKED_AT});
})();
