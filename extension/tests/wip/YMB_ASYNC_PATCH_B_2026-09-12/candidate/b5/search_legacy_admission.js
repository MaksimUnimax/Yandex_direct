/* B5 shared-admission boundary for the existing Search provider.
 * No network here. executeOnce is the unchanged legacy provider body.
 * resolveContext is a trusted worker adapter, NEVER chat metadata authority.
 */
(() => {
  "use strict";
  const failure = (code, executed = false) => Object.assign(new Error(code), {
    code, request_executed: executed, automatic_retry: false
  });
  const text = (v, max) => typeof v === "string" && v.length > 0 && v.length <= max && !/[\u0000-\u001f\u007f]/u.test(v);
  function create({ policy, resolveContext, now = Date.now, sleep = ms => new Promise(resolve => setTimeout(resolve, ms)), maxRateWaitMs = 5000 } = {}) {
    if (!policy || ["bindJob", "reserve", "settle"].some(k => typeof policy[k] !== "function") || typeof resolveContext !== "function") throw failure("SHARED_ADMISSION_DEPENDENCY_REQUIRED");
    if (typeof now !== "function" || typeof sleep !== "function" || !Number.isInteger(maxRateWaitMs) || maxRateWaitMs < 0 || maxRateWaitMs > 5000) throw failure("SHARED_ADMISSION_WAIT_INVALID");
    async function executeLegacy({ command, metadata = {}, folderId, requestId, credentialCheckAuthorized = false }, executeOnce) {
      if (typeof executeOnce !== "function" || !["search", "genSearch"].includes(command?.method) || !text(requestId,128) || !text(folderId,50)) throw failure("SHARED_ADMISSION_REQUEST_INVALID");
      let c;
      try {
        c = credentialCheckAuthorized === true && command.method === "search"
          ? { authorized:true, owner:"credential-check", jobId:`check-${requestId}`, scopeId:`check-${requestId}`, runId:null, channel:"credential_check" }
          : await resolveContext({ command, metadata, folderId, requestId });
      } catch { throw failure("SHARED_ADMISSION_CONTEXT_UNAVAILABLE"); }
      if (c?.channel === "credential_check" && credentialCheckAuthorized !== true) throw failure("SHARED_CHECK_CONSENT_REQUIRED");
      if (!c || c.authorized !== true || !text(c.owner,1000) || !text(c.jobId,128) || !text(c.scopeId,128) ||
        !["manual", "autorun", "credential_check"].includes(c.channel) || (c.runId !== null && !text(c.runId,128))) throw failure("SHARED_ADMISSION_CONTEXT_INVALID");
      const attempt = { jobId:c.jobId, owner:c.owner, folderId, index:0, attemptId:requestId, kind:command.method };
      try { await policy.bindJob({ jobId:c.jobId, owner:c.owner, folderId, scopeId:c.scopeId, runId:c.runId, mode:credentialCheckAuthorized?"credential_check":"legacy", channel:c.channel, credentialCheckConfirmed:credentialCheckAuthorized }); }
      catch { throw failure("SHARED_ADMISSION_BIND_FAILED"); }
      let reservation;
      const started=now();
      try {
        for (let check=0;check<3;check++) {
          reservation = await policy.reserve(attempt);
          if (reservation?.allowed || reservation?.reason !== "ASYNC_GLOBAL_RATE_WAIT") break;
          const at=now(), wait=reservation.next_allowed_at-at;
          if (check===2 || !Number.isSafeInteger(wait) || wait<=0 || at<started || at-started+wait>maxRateWaitMs) break;
          // Wait for local admission only. The provider callback is still untouched.
          await sleep(wait);
          if (!credentialCheckAuthorized) {
            const current=await resolveContext({command,metadata,folderId,requestId});
            if (current?.authorized !== true || ["owner","jobId","scopeId","runId","channel"].some(k=>current[k]!==c[k])) throw failure("SHARED_ADMISSION_CONTEXT_CHANGED");
          }
        }
      }
      catch {
        // Admission may have committed before a UI mirror failed. No provider
        // callback has been invoked: a not-sent settlement is safe, not a retry.
        try { await policy.settle({ ...attempt, request_executed:false, http_status:null, outcome:"not_sent", local_saved:true }); } catch {}
        throw failure("SHARED_ADMISSION_RESERVATION_FAILED");
      }
      if (reservation?.allowed !== true) {
        const e=failure("SHARED_ADMISSION_DENIED");
        e.reason=String(reservation?.reason || "DENIED").slice(0,120);
        if (Number.isSafeInteger(reservation?.next_allowed_at)) e.next_allowed_at=reservation.next_allowed_at;
        throw e;
      }
      let result, originalError;
      try { result=await executeOnce(); } catch (e) { originalError=e; }
      const value=originalError || result;
      const executed=[true,false,"UNKNOWN"].includes(value?.request_executed) ? value.request_executed : "UNKNOWN";
      const http=Number.isInteger(value?.http_status) ? value.http_status : null;
      const outcome=executed===false ? "not_sent" : executed==="UNKNOWN" ? "unknown" : originalError || result?.ok===false ? "rejected" : "received";
      try {
        // This receipt concerns network/accounting, not proof of chat delivery.
        // The old caller still owns persistence of report_text/outbox.
        await policy.settle({ ...attempt, request_executed:executed, http_status:http, outcome, local_saved:true });
      } catch {
        // Preserve a received report instead of replacing it with an accounting
        // error. A failed settlement leaves a pending reservation / explicit hold.
        if (originalError) { originalError.admission_warning="SHARED_ADMISSION_SETTLEMENT_FAILED"; throw originalError; }
        return { ...result, admission_warning:"SHARED_ADMISSION_SETTLEMENT_FAILED", stop_required:true };
      }
      if (originalError) throw originalError;
      return result;
    }
    return Object.freeze({ executeLegacy });
  }
  function createRunMirror({ patchAutoRun } = {}) {
    if (typeof patchAutoRun !== "function") throw failure("SHARED_RUN_MIRROR_REQUIRED");
    // A single shared mirror instance serializes our own storage callbacks.
    // Do not allocate one per request or overwrite unrelated run fields.
    let tail=Promise.resolve();
    return async function publishRunTotals(m) {
      const apply=async()=>{
        if (!text(m.owner,1000) || !text(m.runId,128) || !text(m.scopeId,1500) ||
          !Number.isSafeInteger(m.revision) || m.revision<0 || !Number.isSafeInteger(m.requests_executed) || m.requests_executed<0 ||
          !Number.isFinite(m.estimated_cost_rub) || m.estimated_cost_rub<0) throw failure("SHARED_RUN_MIRROR_INVALID");
        let found=false;
        await patchAutoRun(m.owner, r=>{
          if (!r || r.run_id!==m.runId || r.active_service!=="search") throw failure("SHARED_RUN_MIRROR_CHANGED");
          const previous=r.search_admission_mirror;
          if (previous && previous.scope_id!==m.scopeId) throw failure("SHARED_RUN_MIRROR_SCOPE_CHANGED");
          found=true;
          if (previous && previous.revision>m.revision) return r;
          if (previous && previous.revision===m.revision &&
            (r.requests_executed!==m.requests_executed || r.estimated_cost_rub!==m.estimated_cost_rub)) throw failure("SHARED_RUN_MIRROR_REVISION_CONFLICT");
          return {...r,requests_executed:m.requests_executed,estimated_cost_rub:m.estimated_cost_rub,
            search_admission_mirror:{scope_id:m.scopeId,revision:m.revision}};
        });
        if (!found) throw failure("SHARED_RUN_MIRROR_CHANGED");
      };
      const next=tail.then(apply,apply);tail=next.catch(()=>null);return next;
    };
  }
  globalThis.YMBSearchLegacyAdmission=Object.freeze({create,createRunMirror});
})();
