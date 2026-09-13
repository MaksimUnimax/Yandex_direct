/* B3 internal orchestration. Not a command ingress or UI adapter. No startup work. */
(() => {
  "use strict";
  const fail = code => { throw Object.assign(new Error(code), { code }); };
  const id = value => {
    if (typeof value !== "string" || !/^[A-Za-z0-9_-]{1,128}$/.test(value)) fail("ASYNC_RUNTIME_ID_INVALID");
    return value;
  };
  const uint = value => {
    if (!Number.isSafeInteger(value) || value < 0) fail("ASYNC_RUNTIME_INTEGER_INVALID");
    return value;
  };
  function create({ store = globalThis.YMBSearchAsyncStore, protocol = globalThis.SearchAsyncProtocol,
    transport, authorize, getCredential, policy, normalizeRaw, workerId, now = Date.now,
    pollDelayMs = 300000, sliceBudgetMs = 10000 } = {}) {
    const methods = ["peekNext", "claim", "finishSubmit", "finishCollect", "finishNormalization", "getSummary", "readItem", "readResult", "recover", "control"];
    if (!store || methods.some(name => typeof store[name] !== "function") || !protocol?.parseOperation || !transport?.execute ||
      typeof authorize !== "function" || typeof getCredential !== "function" || typeof normalizeRaw !== "function" ||
      !policy || ["reserve", "settle", "recover"].some(name => typeof policy[name] !== "function") || typeof now !== "function") fail("ASYNC_RUNTIME_DEPENDENCY_REQUIRED");
    id(workerId); uint(pollDelayMs); uint(sliceBudgetMs);
    if (pollDelayMs < protocol.MIN_FIRST_POLL_MS || sliceBudgetMs < 1 || sliceBudgetMs > 10000) fail("ASYNC_RUNTIME_BUDGET_INVALID");
    // Single flight inside this worker instance; store reservations protect other instances.
    // Global rate/cost reservations are deliberately mandatory, not a default allow.
    let busy = false;
    const allowed = async (args, action) => {
      if (await authorize({ jobId: args.jobId, owner: args.owner, action }) !== true) fail("ASYNC_RUNTIME_NOT_AUTHORIZED");
    };
    const clock = () => uint(now());
    async function locked(work) {
      if (busy) return { ok: false, stop: true, code: "ASYNC_RUNTIME_BUSY", request_executed: false };
      busy = true;
      try { return await work(); } finally { busy = false; }
    }
    async function normalization(args) {
      await allowed(args, "normalize");
      const item = await store.readItem(args.jobId, args.owner, uint(args.index));
      if (!item) fail("ASYNC_ITEM_NOT_FOUND");
      if (item.state === "SUCCEEDED") return { ok: true, already_normalized: true, progress: await store.getSummary(args.jobId, args.owner) };
      if (!["RESULT_SAVED", "PARSE_FAILED"].includes(item.state)) fail("ASYNC_ITEM_STATE_INVALID");
      // One original record only, never all batch results. Read failures are not parse failures.
      const record = await store.readResult(args.jobId, args.owner, args.index);
      if (!record || record.operation_id !== item.operation_id) fail("ASYNC_RAW_RESULT_MISSING");
      let normalized;
      try {
        const operation = protocol.parseOperation(record.raw_text, item.operation_id);
        if (operation.outcome !== "received") fail("ASYNC_NORMALIZATION_RESPONSE_INVALID");
        normalized = await normalizeRaw({ rawData: operation.rawData, query: item.query });
        if (!normalized || !Array.isArray(normalized.results) || normalized.results.length > 300) fail("ASYNC_NORMALIZED_INVALID");
      } catch {
        const progress = await store.finishNormalization({ ...args, errorCode: "ASYNC_NORMALIZATION_FAILED", now: clock() });
        return { ok: false, stop: true, code: "ASYNC_NORMALIZATION_FAILED", raw_preserved: true, progress };
      }
      const progress = await store.finishNormalization({ ...args, normalized, now: clock() });
      return { ok: true, normalized: true, progress };
    }
    async function one(args) {
      const { jobId, owner, attemptId, kind, signal } = args;
      id(jobId); id(attemptId);
      if (!["submit", "collect"].includes(kind)) fail("ASYNC_RUNTIME_KIND_INVALID");
      await allowed(args, kind);
      if (signal?.aborted) return { ok: false, stop: true, code: "ASYNC_ABORTED", request_executed: false };
      const preview = await store.peekNext({ jobId, owner, kind, now: clock() });
      if (!preview.item) return { ok: true, stop: true, code: kind === "submit" ? "NO_PENDING_ITEMS" : "NO_DUE_OPERATIONS", request_executed: false, progress: preview.progress };
      let credential;
      try { credential = await getCredential({ jobId, owner, service: "search", folderId: preview.folder_id }); }
      catch { return { ok: false, stop: true, code: "ASYNC_CREDENTIAL_UNAVAILABLE", request_executed: false }; }
      let claim = null, policyAttempted = false, admissionReason = null, wire;
      const context = { jobId, owner, attemptId, kind, index: preview.item.index, folderId: preview.folder_id };
      try {
        wire = await transport.execute({ kind, query: preview.item.query, parameters: preview.parameters,
          operationId: preview.item.operation_id, credential, expectedFolderId: preview.folder_id, signal,
          admit: async () => {
            await allowed(args, kind);
            if (signal?.aborted) return { allowed: false };
            const decision = await store.claim({ jobId, owner, attemptId, kind, workerId, now: clock(), expectedIndex: preview.item.index });
            if (decision.allowed !== true) { admissionReason = decision.reason; return { allowed: false }; }
            claim = decision;
            policyAttempted = true;
            const reserved = await policy.reserve(context);
            return { allowed: reserved?.allowed === true };
          }
        });
      } catch {
        wire = { ok: false, request_executed: claim ? "UNKNOWN" : false, code: "ASYNC_TRANSPORT_EXCEPTION", outcome: kind === "submit" ? "unknown" : "read_error" };
      } finally { credential = null; }
      if (!claim) return { ok: false, stop: true, request_executed: false, code: admissionReason || wire?.code || "ASYNC_NOT_ADMITTED" };
      if (![true, false, "UNKNOWN"].includes(wire?.request_executed)) wire = { ok: false, request_executed: "UNKNOWN", code: "ASYNC_TRANSPORT_CONTRACT_INVALID" };
      let localSaved = false, resultState = null;
      const settlement = { jobId, owner, attemptId, index: claim.item.index, now: clock() };
      try {
        if (kind === "submit") {
          const op = wire.ok ? wire.operation : null;
          resultState = wire.request_executed === false ? "not_sent" : op ?
            (op.outcome === "waiting" ? "accepted" : op.outcome) : wire.outcome === "rejected" ? "rejected" : "unknown";
          await store.finishSubmit({ ...settlement, outcome: resultState, operationId: op?.operation_id,
            nextPollAt: clock() + pollDelayMs, rawText: wire.raw_text,
            errorCode: op?.outcome === "provider_error" ? `PROVIDER_${op.error_code}` : wire.code });
        } else {
          const op = wire.ok ? wire.operation : null;
          resultState = op?.outcome || "read_error";
          await store.finishCollect({ ...settlement, outcome: resultState, nextPollAt: clock() + pollDelayMs,
            rawText: wire.raw_text, errorCode: op?.outcome === "provider_error" ? `PROVIDER_${op.error_code}` : wire.code });
        }
        localSaved = true;
      } catch {
        // Keep the in-flight lease: no retry and no next item after a failed durable write.
        // Explicit recovery under a new trusted worker session reconciles it later.
      }
      let policySaved = !policyAttempted;
      if (policyAttempted) {
        try {
          await policy.settle({ ...context, request_executed: wire.request_executed,
            http_status: wire.http_status ?? null, outcome: resultState, local_saved: localSaved,
            operation_id: wire.operation?.operation_id || null });
          policySaved = true;
        } catch {
          // Per-job hold supplements (not replaces) the external policy's durable ledger.
          try { await store.control({ jobId, owner, action: "pause", now: clock() }); } catch {}
        }
      }
      if (!localSaved || !policySaved) return { ok: false, stop: true,
        code: !localSaved ? "ASYNC_PERSISTENCE_FAILED" : "ASYNC_POLICY_RECONCILIATION_REQUIRED",
        request_executed: wire.request_executed, index: claim.item.index };
      const result = { ok: wire.ok === true, stop: !wire.ok || resultState === "provider_error",
        outcome: resultState, request_executed: wire.request_executed, index: claim.item.index,
        operation_id: wire.operation?.operation_id || claim.item.operation_id || null,
        progress: await store.getSummary(jobId, owner) };
      // No raw/normalized arrays leave this boundary. Parsing is a separate local action.
      if (!wire.ok) result.code = wire.code || "ASYNC_REQUEST_FAILED";
      return result;
    }
    async function step(args) { return locked(() => one(args)); }
    async function slice({ jobId, owner, commandId, kind, count = 1, signal } = {}) {
      id(commandId);
      if (commandId.length > 90 || !Number.isInteger(count) || count < 1 || count > protocol.MAX_SLICE) fail("ASYNC_RUNTIME_SLICE_INVALID");
      return locked(async () => {
        const started = clock();
        let processed = 0, networkAttempts = 0, last = null;
        for (let index = 0; index < count; index++) {
          if (signal?.aborted || clock() - started >= sliceBudgetMs) break;
          last = await one({ jobId, owner, kind, signal, attemptId: `${commandId}-${kind}-${index}` });
          processed++;
          if (last.request_executed !== false) networkAttempts++;
          if (last.stop) break;
        }
        return { ok: last?.ok ?? false, processed, network_attempts: networkAttempts,
          requested_count: count, last, bounded_stop: processed < count };
      });
    }
    async function recover({ jobId, owner }) {
      id(jobId);
      return locked(async () => {
        await allowed({ jobId, owner }, "recover");
        await store.recover({ jobId, owner, workerId, now: clock() });
        // The policy adapter must reconcile its own interrupted reservation, locally.
        if ((await policy.recover({ jobId, owner, workerId }))?.allowed !== true) fail("ASYNC_POLICY_RECONCILIATION_REQUIRED");
        return { ok: true, request_executed: false, progress: await store.getSummary(jobId, owner) };
      });
    }
    async function control({ jobId, owner, action }) {
      id(jobId); await allowed({ jobId, owner }, action);
      return store.control({ jobId, owner, action, now: clock() });
    }
    return Object.freeze({ step, slice, recover, control,
      normalizeSaved: args => locked(() => normalization(args)) });
  }
  globalThis.YMBSearchAsyncRuntime = Object.freeze({ create });
})();
