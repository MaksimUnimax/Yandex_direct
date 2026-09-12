/* B6 trusted worker binding for the shared Search admission guard.
 * Loaded after webmaster_worker_runtime.js so current credential/settings accessors are active.
 * Chat metadata is only a claim to cross-check against worker-owned durable state.
 */
(() => {
  "use strict";

  const SEARCH = "search";
  const MANUAL_OPERATIONS_KEY = "wsmb_manual_operations";
  const TERMINAL_MANUAL = new Set(["completed", "error", "cancelled"]);
  const fail = (code) => { throw Object.assign(new Error(code), { code, request_executed: false, automatic_retry: false }); };
  const clean = (value, max = 1000) => typeof value === "string" && value.length > 0 && value.length <= max && !/[\u0000-\u001f\u007f]/u.test(value);
  const sameId = (left, right) => String(left || "").toLowerCase() === String(right || "").toLowerCase();

  function createTrustedContextResolver({
    normalizeConversationKey,
    getBinding,
    getManualMode,
    getServiceContext,
    getAutoRun,
    getManualOperation,
    assertTabConversation,
    workerSessionId,
    isRunTerminal
  } = {}) {
    if ([normalizeConversationKey, getBinding, getManualMode, getServiceContext, getAutoRun, getManualOperation, assertTabConversation, isRunTerminal].some((fn) => typeof fn !== "function") || !clean(workerSessionId, 240)) {
      fail("SHARED_ADMISSION_BINDING_DEPENDENCY_REQUIRED");
    }

    async function trustedConversation(metadata) {
      if (!metadata || typeof metadata !== "object" || Array.isArray(metadata) || !clean(metadata.conversation_key, 1000)) fail("SHARED_ADMISSION_CONVERSATION_REQUIRED");
      let key;
      try { key = normalizeConversationKey(metadata.conversation_key); }
      catch { fail("SHARED_ADMISSION_CONVERSATION_INVALID"); }
      const binding = await getBinding(key);
      if (!binding || binding.conversation_key !== key || !clean(binding.conversation_id, 240)) fail("SHARED_ADMISSION_CONVERSATION_NOT_BOUND");
      const service = await getServiceContext(key);
      if (service?.active_service !== SEARCH) fail("SHARED_ADMISSION_SERVICE_MISMATCH");
      return { key, binding };
    }

    async function assertOwnerTab(tabId, key, binding, expectedConversationId = null) {
      const tab = Number(tabId);
      if (!Number.isInteger(tab) || tab <= 0) fail("SHARED_ADMISSION_OWNER_TAB_REQUIRED");
      let identity;
      try { identity = await assertTabConversation(tab, key, expectedConversationId || binding.conversation_id); }
      catch { fail("SHARED_ADMISSION_OWNER_MISMATCH"); }
      if (!identity || normalizeConversationKey(identity.conversation_key) !== key || !sameId(identity.conversation_id, binding.conversation_id)) fail("SHARED_ADMISSION_OWNER_MISMATCH");
      return tab;
    }

    async function resolveContext({ command, metadata, folderId, requestId } = {}) {
      if (!command || !["search", "genSearch"].includes(command.method) || !clean(folderId, 50) || !clean(requestId, 128)) fail("SHARED_ADMISSION_CONTEXT_INVALID");
      const { key, binding } = await trustedConversation(metadata);
      const claimedChannel = String(metadata?.policy?.channel || "");
      const claimedRunId = metadata?.run_id == null ? null : String(metadata.run_id);
      const manualMode = await getManualMode(key);
      const operation = await getManualOperation(key);

      if (manualMode === true && operation && !TERMINAL_MANUAL.has(String(operation.status || ""))) {
        if (!["requesting", "search_batch_requesting"].includes(String(operation.status || ""))) fail("SHARED_ADMISSION_MANUAL_STATE_INVALID");
        if (operation.conversation_key !== key || operation.active_service !== SEARCH || !clean(operation.operation_id, 128)) fail("SHARED_ADMISSION_MANUAL_STATE_INVALID");
        if (claimedChannel && claimedChannel !== "manual") fail("SHARED_ADMISSION_CHANNEL_MISMATCH");
        const opRunId = operation.run_id == null ? null : String(operation.run_id);
        if (claimedRunId !== opRunId) fail("SHARED_ADMISSION_RUN_MISMATCH");
        await assertOwnerTab(operation.tab_id, key, binding);
        if (opRunId) {
          const run = await getAutoRun(key);
          if (!run || run.run_id !== opRunId || run.status !== "paused" || run.active_service !== SEARCH || Number(run.tab_id) !== Number(operation.tab_id)) fail("SHARED_ADMISSION_PAUSED_RUN_MISMATCH");
        }
        return Object.freeze({
          authorized: true,
          owner: key,
          jobId: operation.operation_id,
          scopeId: operation.operation_id,
          runId: opRunId,
          channel: "manual"
        });
      }

      if (manualMode === true) fail("SHARED_ADMISSION_MANUAL_STATE_MISSING");
      if (!claimedRunId) fail("SHARED_ADMISSION_AUTORUN_REQUIRED");
      if (claimedChannel && claimedChannel !== "autorun") fail("SHARED_ADMISSION_CHANNEL_MISMATCH");
      const run = await getAutoRun(key);
      if (!run || isRunTerminal(run.status) || run.run_id !== claimedRunId || run.active_service !== SEARCH) fail("SHARED_ADMISSION_RUN_MISMATCH");
      if (run.status !== "requesting" || run.request_worker_session_id !== workerSessionId) fail("SHARED_ADMISSION_RUN_NOT_OWNED");
      await assertOwnerTab(run.tab_id, key, binding, run.conversation_id);
      if (run.conversation_id && !sameId(run.conversation_id, binding.conversation_id)) fail("SHARED_ADMISSION_RUN_CONVERSATION_MISMATCH");
      return Object.freeze({
        authorized: true,
        owner: key,
        jobId: run.run_id,
        scopeId: run.run_id,
        runId: run.run_id,
        channel: "autorun"
      });
    }

    return Object.freeze({ resolveContext });
  }

  function unavailableGuard(code = "SHARED_ADMISSION_UNAVAILABLE") {
    return Object.freeze({
      async executeLegacy() { fail(code); }
    });
  }

  function install(deps = {}) {
    const PolicyFactory = deps.policyFactory || globalThis.YMBSearchAsyncPolicy;
    const LegacyFactory = deps.legacyFactory || globalThis.YMBSearchLegacyAdmission;
    const normalizeKey = deps.normalizeConversationKey || (typeof normalizeConversationKey === "function" ? normalizeConversationKey : null);
    const bindingGetter = deps.getBinding || (typeof getBinding === "function" ? getBinding : null);
    const manualGetter = deps.getManualMode || (typeof getManualMode === "function" ? getManualMode : null);
    const serviceGetter = deps.getServiceContext || (typeof getServiceContext === "function" ? getServiceContext : null);
    const runGetter = deps.getAutoRun || (typeof getAutoRun === "function" ? getAutoRun : null);
    const tabAssert = deps.assertTabConversation || (typeof assertTabConversation === "function" ? assertTabConversation : null);
    const patchRun = deps.patchAutoRun || (typeof patchAutoRun === "function" ? patchAutoRun : null);
    const settingsGetter = deps.getSettings || (typeof getSettings === "function" ? getSettings : null);
    const policyGetter = deps.getSearchPolicy || (typeof getPolicyForService === "function" ? (() => getPolicyForService(SEARCH)) : null);
    const sessionId = deps.workerSessionId || (typeof WORKER_SESSION_ID === "string" ? WORKER_SESSION_ID : "");
    const runTerminal = deps.isRunTerminal || (globalThis.WordstatAutorunModel?.isTerminalStatus?.bind(globalThis.WordstatAutorunModel));
    const manualOperationGetter = deps.getManualOperation || (async (key) => {
      const data = await chrome.storage.local.get(MANUAL_OPERATIONS_KEY);
      return data?.[MANUAL_OPERATIONS_KEY]?.[key] || null;
    });

    if (!PolicyFactory?.create || !LegacyFactory?.create || !LegacyFactory?.createRunMirror || !settingsGetter || !policyGetter || !patchRun) fail("SHARED_ADMISSION_INSTALL_DEPENDENCY_REQUIRED");
    const resolver = createTrustedContextResolver({
      normalizeConversationKey: normalizeKey,
      getBinding: bindingGetter,
      getManualMode: manualGetter,
      getServiceContext: serviceGetter,
      getAutoRun: runGetter,
      getManualOperation: manualOperationGetter,
      assertTabConversation: tabAssert,
      workerSessionId: sessionId,
      isRunTerminal: runTerminal
    });
    const publishRunTotals = LegacyFactory.createRunMirror({ patchAutoRun: patchRun });
    const policy = PolicyFactory.create({
      getPolicy: policyGetter,
      getSettings: settingsGetter,
      getAutoRun: runGetter,
      workerId: `${sessionId}:search-admission`,
      publishRunTotals
    });
    const guard = LegacyFactory.create({ policy, resolveContext: resolver.resolveContext });
    if (typeof guard?.executeLegacy !== "function") fail("SHARED_ADMISSION_GUARD_INVALID");
    return Object.freeze({ ready: true, guard, policy, resolveContext: resolver.resolveContext, workerSessionId: sessionId });
  }

  globalThis.YMBSearchAdmissionWorkerBinding = Object.freeze({ createTrustedContextResolver, install, unavailableGuard });

  try {
    const installed = install();
    globalThis.YMBSearchAdmissionGuard = installed.guard;
    globalThis.YMBSearchAdmissionBinding = installed;
  } catch (error) {
    // Search fails closed if the governed guard cannot be initialized; other services stay loadable.
    const code = String(error?.code || "SHARED_ADMISSION_UNAVAILABLE");
    globalThis.YMBSearchAdmissionGuard = unavailableGuard(code);
    globalThis.YMBSearchAdmissionBinding = Object.freeze({ ready: false, code });
  }
})();
