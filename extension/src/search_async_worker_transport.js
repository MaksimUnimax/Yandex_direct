/* B7 Manual-only deferred Search command ingress and worker runtime binding.
 * No Autorun deferred path. No background polling/alarms. Compact reports only.
 */
(() => {
  "use strict";
  const PREFIX = "SEARCH_ASYNC_BATCH_API_V1";
  const RESULT_PREFIX = "SEARCH_ASYNC_BATCH_RESULT_V1";
  const MANUAL_STATUS = "search_async_requesting";
  const TERMINAL = new Set(["completed", "error", "cancelled"]);
  const fail = (code, message = code) => { throw Object.assign(new Error(message), { code, request_executed: false, automatic_retry: false }); };
  const validId = value => typeof value === "string" && /^[A-Za-z0-9_-]{1,128}$/.test(value);

  function create(deps = {}) {
    const {
      baseExecuteManualBlock,
      protocol,
      store,
      exportFactory,
      artifactStore,
      runtime: suppliedRuntime,
      runtimeFactory,
      transportFactory,
      normalizerFactory,
      searchXml,
      admissionBinding,
      asyncPolicyFactory,
      getSettings,
      getBinding,
      getManualMode,
      getServiceContext,
      getAutoRun,
      getManualOperation,
      setManualOperation,
      getConversationOutbox,
      assertTabConversation,
      normalizeConversationKey,
      blockDiscovery,
      ordinaryDiscovery,
      putOutbox,
      formatBridgeError,
      applyPrefixToReport,
      uid,
      nowIso,
      runContextModel,
      autorunModel,
      workerId,
      fetchImpl,
      providerEnabled = false,
      maxResponseBytes = 8 * 1024 * 1024,
      pollDelayMs = 5 * 60 * 1000,
      now = Date.now
    } = deps;
    const required = { baseExecuteManualBlock, protocol, store, admissionBinding, getSettings, getBinding, getManualMode,
      getServiceContext, getAutoRun, getManualOperation, setManualOperation, getConversationOutbox, assertTabConversation,
      normalizeConversationKey, blockDiscovery, putOutbox, formatBridgeError, applyPrefixToReport, uid, nowIso, runContextModel, autorunModel };
    for (const [name, value] of Object.entries(required)) if (!value || (typeof value !== "function" && typeof value !== "object")) fail("ASYNC_WORKER_DEPENDENCY_REQUIRED", name);
    if (admissionBinding.ready !== true || typeof admissionBinding.resolveContext !== "function" || !admissionBinding.policy) fail("ASYNC_SHARED_ADMISSION_NOT_READY");
    if (!validId(workerId)) fail("ASYNC_WORKER_ID_INVALID");

    const searchService = "search";
    const priceMicrorub = Number(asyncPolicyFactory?.PRICE_MICRORUB || 30500);
    if (!Number.isSafeInteger(priceMicrorub) || priceMicrorub <= 0) fail("ASYNC_PRICE_INVALID");

    async function manualAuthority({ key, operation, folderId, action }) {
      if (!operation || operation.status !== MANUAL_STATUS || operation.conversation_key !== key || operation.active_service !== searchService) fail("ASYNC_MANUAL_OPERATION_MISMATCH");
      if (String(operation.batch_job_id || "") === "" || !validId(operation.batch_job_id)) fail("ASYNC_JOB_ID_INVALID");
      const resolved = await admissionBinding.resolveContext({
        command: { method: "search" },
        metadata: { conversation_key: key, policy: { channel: "manual" }, run_id: operation.run_id || null },
        folderId,
        requestId: operation.operation_id
      });
      if (!resolved?.authorized || resolved.owner !== key || resolved.channel !== "manual") fail("ASYNC_MANUAL_AUTHORITY_REJECTED");
      if (action && !["start","submit","collect","submitN","collectN","normalize","recover","status","itemsPage","pause","resume","cancelPending","exportPage","normalizeSaved"].includes(action)) fail("ASYNC_ACTION_INVALID");
      return true;
    }

    async function currentCredential(folderId) {
      const settings = await getSettings();
      const record = settings?.credentials?.search;
      if (!record || typeof record.api_key !== "string" || !record.api_key.trim() || record.folder_id !== folderId) fail("ASYNC_CREDENTIAL_CONTEXT_CHANGED");
      return { api_key: record.api_key, folder_id: record.folder_id };
    }

    let runtime = suppliedRuntime || null;
    if (!runtime) {
      if (!runtimeFactory?.create || !transportFactory?.create || !normalizerFactory?.create || !searchXml || typeof fetchImpl !== "function") fail("ASYNC_RUNTIME_DEPENDENCY_REQUIRED");
      const transport = transportFactory.create({ fetchImpl, protocol, maxResponseBytes, timeoutMs: 20000 });
      const normalizeRaw = normalizerFactory.create({ xmlNormalizer: searchXml, maxRawBytes: maxResponseBytes, maxDepth: 48, maxNodes: 40000, maxResults: 250 });
      runtime = runtimeFactory.create({
        store, protocol, transport, policy: admissionBinding.policy, normalizeRaw,
        workerId, pollDelayMs, now,
        getCredential: async ({ folderId }) => currentCredential(folderId),
        authorize: async ({ jobId, owner, action }) => {
          const operation = await getManualOperation(owner);
          if (!operation || operation.batch_job_id !== jobId) return false;
          const credential = await currentCredential(operation.folder_id);
          return manualAuthority({ key: owner, operation, folderId: credential.folder_id, action });
        }
      });
    }
    for (const name of ["step","recover","control","normalizeSaved"]) if (typeof runtime?.[name] !== "function") fail("ASYNC_RUNTIME_INVALID");

    function discover(text) {
      const source = String(text || "").replace(/\u00a0/g, " ");
      const positions = [];
      let from = 0;
      while (from < source.length) {
        const index = source.indexOf(PREFIX, from);
        if (index < 0) break;
        positions.push(index); from = index + PREFIX.length;
      }
      if (!positions.length) return { async: false };
      if (positions.length !== 1) return { async: true, error: Object.assign(new Error("Один Manual block должен содержать ровно одну deferred Search команду."), { code: "ASYNC_SINGLE_COMMAND_REQUIRED" }) };
      const others = typeof ordinaryDiscovery === "function" ? ordinaryDiscovery(source) : [];
      if (Array.isArray(others) && others.length) return { async: true, error: Object.assign(new Error("Deferred Search нельзя смешивать с другой Bridge-командой в одном блоке."), { code: "ASYNC_SINGLE_COMMAND_REQUIRED" }) };
      const extracted = blockDiscovery.extractJsonObject(source, positions[0] + PREFIX.length);
      if (!extracted?.ok) return { async: true, error: Object.assign(new Error(extracted?.message || extracted?.code || "Некорректная deferred Search команда."), { code: extracted?.code || "ASYNC_COMMAND_INVALID" }) };
      try { return { async: true, command: protocol.normalizeCommand(extracted.raw) }; }
      catch (error) { return { async: true, error }; }
    }

    async function preflightManual(conversationKey, sender) {
      const key = normalizeConversationKey(conversationKey);
      const tabId = Number(sender?.tab?.id);
      if (!Number.isInteger(tabId) || tabId <= 0) fail("MANUAL_SENDER_TAB_REQUIRED", "Manual action должна исходить из вкладки ChatGPT.");
      const live = await assertTabConversation(tabId, key);
      const binding = await getBinding(key);
      if (!binding || binding.conversation_id !== live.conversation_id) fail("CONVERSATION_NOT_BOUND", "Сначала привяжите этот диалог в popup.");
      if (!(await getManualMode(key))) fail("MANUAL_MODE_DISABLED", "Ручной режим выключен.");
      if ((await getServiceContext(key))?.active_service !== searchService) fail("SERVICE_NOT_ACTIVE", "Deferred Search доступен только при активном сервисе Search.");
      const run = await getAutoRun(key);
      if (run && !autorunModel.isTerminalStatus(run.status) && run.status !== autorunModel.RUN_STATUSES.PAUSED) fail("AUTORUN_NOT_PAUSED", "Для Manual активный Autorun должен быть поставлен на паузу.");
      if (run?.status === autorunModel.RUN_STATUSES.PAUSED) {
        if (tabId !== Number(run.tab_id)) fail("AUTO_NON_OWNER_TAB");
        runContextModel.assertServiceMatch(run.active_service, searchService);
      }
      const existing = await getManualOperation(key);
      if (existing?.status === MANUAL_STATUS && existing.request_worker_session_id !== workerId &&
        existing.conversation_key === key && existing.active_service === searchService &&
        Number(existing.tab_id) === tabId && validId(existing.batch_job_id)) {
        await recoverManualOperations({ key, tabId });
        fail("ASYNC_RECOVERY_DELIVERY_PENDING", "Прерванная операция восстановлена без повторного запроса. Сначала завершите доставку её отчёта.");
      }
      if (existing && !TERMINAL.has(String(existing.status || ""))) fail("MANUAL_OPERATION_ACTIVE");
      if (await getConversationOutbox(key)) fail("DELIVERY_IN_PROGRESS");
      return { key, tabId, run };
    }

    function compactSummary(summary) {
      if (!summary || typeof summary !== "object") return null;
      return {
        job_id: summary.job_id || null,
        control: summary.control || null,
        total: Number(summary.total || 0),
        counts: summary.counts && typeof summary.counts === "object" ? { ...summary.counts } : {},
        requests_started: Number(summary.requests_started || 0),
        operations_accepted: Number(summary.operations_accepted || 0),
        polls_started: Number(summary.polls_started || 0),
        unresolved: Number(summary.unresolved || 0),
        all_successful: summary.all_successful === true,
        busy: summary.busy === true,
        revision: Number(summary.revision || 0)
      };
    }

    function compactRows(page) {
      const rows = Array.isArray(page?.rows) ? page.rows : [];
      return {
        rows: rows.map(row => ({
          index: Number(row.index), state: String(row.state || ""), operation_id: row.operation_id || null,
          poll_count: Number(row.poll_count || 0), error_code: row.error_code || null, parse_error: row.parse_error || null
        })),
        next_after: Number(page?.next_after ?? -1)
      };
    }

    async function executeCommand(command, context) {
      const { key, operation, folderId } = context;
      const jobId = command.jobId;
      await manualAuthority({ key, operation, folderId, action: command.action });
      if (command.action === "start") {
        await admissionBinding.policy.bindJob({ jobId, owner: key, folderId, scopeId: jobId, runId: operation.run_id || null });
        const progress = await store.createJob({
          jobId, owner: key, queries: command.queries, parameters: command.parameters, folderId,
          maxRequests: command.maxRequests, maxCostMicrorub: command.maxCostMicrorub,
          unitCostMicrorub: priceMicrorub, now: now()
        });
        return { ok: true, request_executed: false, provider_calls: 0, progress: compactSummary(progress) };
      }
      if (command.action === "normalizeSaved") {
        // One preserved item only; no collect, submit, budget reservation or raw replacement.
        const local = await runtime.normalizeSaved({ jobId, owner: key, index: command.index });
        return { ok: local.ok === true, request_executed: false, provider_calls: 0,
          index: command.index, normalized: local.normalized === true,
          already_normalized: local.already_normalized === true,
          ...(local.code ? { code: local.code } : {}),
          ...(local.raw_preserved ? { raw_preserved: true } : {}),
          progress: compactSummary(local.progress) };
      }
      if (command.action === "exportPage") {
        if (!exportFactory?.create || !artifactStore || !context.deliveryId || !context.staged) fail("ASYNC_EXPORT_NOT_READY");
        const exporter = exportFactory.create({ store, artifacts: artifactStore, now,
          authorize: async ({ jobId: checkedJob, owner, action }) => {
            if (owner !== key || checkedJob !== jobId || action !== "exportPage") return false;
            const live = await getManualOperation(key);
            if (live?.operation_id !== operation.operation_id || live?.batch_job_id !== jobId) return false;
            return manualAuthority({ key, operation: live, folderId, action });
          }
        });
        context.exporter = exporter;
        const exported = await exporter.stagePage({ jobId, owner: key, folderId,
          deliveryId: context.deliveryId, after: command.after, limit: command.limit, revision: command.revision });
        context.staged.push(exported.descriptor);
        return { ok: true, request_executed: false, provider_calls: 0, export_page: exported.report };
      }
      if (command.action === "status") return { ok: true, request_executed: false, provider_calls: 0, progress: compactSummary(await store.getSummary(jobId, key)) };
      if (command.action === "itemsPage") return { ok: true, request_executed: false, provider_calls: 0, page: compactRows(await store.pageItems(jobId, key, { after: command.after, limit: command.limit })) };
      if (["pause","resume","cancelPending"].includes(command.action)) {
        const progress = await runtime.control({ jobId, owner: key, action: command.action });
        return { ok: true, request_executed: false, provider_calls: 0, progress: compactSummary(progress) };
      }
      if (["submitN","collectN"].includes(command.action) && providerEnabled !== true) fail("ASYNC_PROVIDER_PERMISSION_REQUIRED", "Deferred provider transport ещё не включён в этой сборке.");
      if (!["submitN","collectN"].includes(command.action)) fail("ASYNC_ACTION_INVALID");
      await runtime.recover({ jobId, owner: key });
      const kind = command.action === "submitN" ? "submit" : "collect";
      if (!Number.isInteger(command.count) || command.count < 1 || command.count > 25) fail("ASYNC_SLICE_COUNT_INVALID");
      const execution = context.execution = { confirmed: 0, unknown: false, in_flight: false, processed: 0, normalized: 0 };
      let last = null;
      const started = now();
      for (let i = 0; i < command.count; i += 1) {
        const elapsed = now() - started;
        if (elapsed < 0 || elapsed >= 10000) break;
        // Revalidate BEFORE entering the uncertain network window. A later local
        // exception cannot erase an already confirmed request from this command.
        const live = await getManualOperation(key);
        if (live?.operation_id !== operation.operation_id) fail("ASYNC_MANUAL_OPERATION_CHANGED");
        await manualAuthority({ key, operation: live, folderId, action: kind });
        execution.in_flight = true;
        try { await saveExecution(context); }
        catch (error) { execution.in_flight = false; throw error; } // No runtime/fetch entered.
        try {
          last = await runtime.step({ jobId, owner: key, kind, attemptId: `${operation.operation_id}-${kind}-${i}` });
        } catch (error) {
          execution.in_flight = false;
          if (error?.request_executed === true) execution.confirmed++;
          else if (error?.request_executed !== false) execution.unknown = true;
          throw error;
        }
        execution.in_flight = false;
        execution.processed++;
        if (last.request_executed === true) execution.confirmed++;
        if (last.request_executed === "UNKNOWN") execution.unknown = true;
        await saveExecution(context);
        // searchAsync may already return a complete result; no GET is needed.
        if (last.outcome === "received" && Number.isInteger(last.index)) {
          const n = await runtime.normalizeSaved({ jobId, owner: key, index: last.index });
          if (n?.ok) execution.normalized++;
          else last = { ...last, ok: false, stop: true, code: n?.code || "ASYNC_NORMALIZATION_FAILED" };
        }
        if (last.outcome === "provider_error") last = { ...last, ok: false, stop: true, code: last.code || "ASYNC_PROVIDER_OPERATION_FAILED" };
        if (last.stop) break;
      }
      return {
        ok: last?.ok !== false,
        request_executed: executionOutcome(execution),
        provider_calls: execution.confirmed,
        processed: execution.processed, normalized: execution.normalized,
        bounded_stop: execution.processed < command.count,
        last: last ? { outcome: last.outcome || null, code: last.code || null, index: Number.isInteger(last.index) ? last.index : null, operation_id: last.operation_id || null } : null,
        progress: compactSummary(await store.getSummary(jobId, key))
      };
    }

    function executionOutcome(execution) {
      return execution?.unknown || execution?.in_flight ? "UNKNOWN" : Number(execution?.confirmed || 0) > 0;
    }

    async function saveExecution(context) {
      const current = await getManualOperation(context.key);
      if (current?.operation_id !== context.operation.operation_id) fail("ASYNC_MANUAL_OPERATION_CHANGED");
      await setManualOperation(context.key, { ...current, request_executed: executionOutcome(context.execution),
        execution_receipt: { ...context.execution }, execution_updated_at: nowIso() });
    }

    function report(command, result) {
      return `${RESULT_PREFIX}\n${JSON.stringify({ action: command?.action || null, job_id: command?.jobId || null, ...result })}`;
    }

    async function executeManualUnlocked(blockText, conversationKey, sender, manualRequestToken = "") {
      const found = discover(blockText);
      if (!found.async) return baseExecuteManualBlock(blockText, conversationKey, sender, manualRequestToken);
      let preflight;
      try { preflight = await preflightManual(conversationKey, sender); }
      catch (error) { return { ok: false, accepted: false, code: error.code || "ASYNC_MANUAL_PREFLIGHT_FAILED", error: error.message || String(error), request_executed: false }; }
      const { key, tabId, run } = preflight;
      const token = String(manualRequestToken || uid("manual-request"));
      const current = await getManualOperation(key);
      if (current?.request_token === token) return { ok: true, accepted: false, duplicate: true, operation_id: current.operation_id };
      const command = found.command || null;
      const settings = await getSettings();
      const credential = settings?.credentials?.search;
      if (!credential || typeof credential.folder_id !== "string" || !credential.folder_id) return { ok: false, accepted: false, code: "ASYNC_SEARCH_CREDENTIALS_NOT_READY", error: "Search credentials не готовы.", request_executed: false };
      const operation = {
        operation_id: uid("manual"), request_token: token, conversation_key: key, tab_id: tabId,
        active_service: searchService, run_id: run?.status === autorunModel.RUN_STATUSES.PAUSED ? run.run_id : null,
        status: MANUAL_STATUS, request_worker_session_id: workerId, batch_action: command?.action || null, batch_job_id: command?.jobId || null,
        folder_id: credential.folder_id, created_at: nowIso(), request_executed: false
      };
      await setManualOperation(key, operation);
      const deliveryId = uid("delivery");
      const exportContext = { key, operation, folderId: credential.folder_id, deliveryId, staged: [] };
      let result, reportText;
      try {
        if (found.error) throw found.error;
        result = await executeCommand(command, exportContext);
        reportText = report(command, result);
      } catch (error) {
        const prior = executionOutcome(exportContext.execution);
        const requestExecuted = prior === "UNKNOWN" || error?.request_executed === "UNKNOWN" ? "UNKNOWN"
          : prior === true || error?.request_executed === true;
        result = { ok: false, code: error.code || "ASYNC_COMMAND_FAILED", error: error.message || String(error), request_executed: requestExecuted,
          provider_calls: Number(exportContext.execution?.confirmed || 0) };
        reportText = formatBridgeError({ code: result.code, message: result.error, stage: "SEARCH_ASYNC_MANUAL", requestExecuted, service: searchService, channel: "manual", recoverable: requestExecuted !== "UNKNOWN", operation: command ? `async.${command.action}` : null, operationId: operation.operation_id, autorunContinues: false });
      }
      const requestExecuted = result.request_executed ?? false;
      const prefix = result.provider_calls > 0 ? await applyPrefixToReport(key, reportText) : { text: reportText, applied: false };
      try { await putOutbox(key, {
        delivery_id: deliveryId, operation_id: operation.operation_id, type: "manual", tab_id: tabId,
        report_text: prefix.text, phase: "claimed", provider_executions: requestExecuted === "UNKNOWN" ? null : Number(result.provider_calls || 0),
        report_prefix_applied: prefix.applied === true, created_at: nowIso(),
        ...(exportContext.staged.length ? { delivery_mode: "attachment_v2", artifact_descriptors: exportContext.staged } : {})
      }); } catch (error) {
        // A storage error may occur AFTER the outbox was written. Keep that artifact
        // for the existing delivery recovery; delete only if readback proves no commit.
        if (exportContext.staged.length) {
          let pending, readable = false;
          try { pending = await getConversationOutbox(key); readable = true; } catch {}
          if (readable && pending?.delivery_id !== deliveryId) {
            for (const descriptor of exportContext.staged) await exportContext.exporter.discard(descriptor);
          }
        }
        throw error;
      }
      const finalOperation = await getManualOperation(key);
      if (finalOperation?.operation_id !== operation.operation_id) fail("ASYNC_MANUAL_OPERATION_CHANGED");
      await setManualOperation(key, { ...finalOperation, status: "delivering", delivery_id: deliveryId, request_executed: requestExecuted, report_ready_at: nowIso() });
      return { ok: true, accepted: true, operation_id: operation.operation_id, delivery_id: deliveryId, report_text: prefix.text, request_executed: requestExecuted };
    }

    // Same-worker concurrent Manual invocations must not replace each other's
    // durable operation while export is staging. Other legacy blocks still delegate.
    let manualExecuting = false;
    async function executeManual(...args) {
      if (!String(args[0] || "").includes(PREFIX)) return baseExecuteManualBlock(...args);
      if (manualExecuting) return { ok: false, accepted: false, code: "MANUAL_OPERATION_ACTIVE", request_executed: false };
      manualExecuting = true;
      try { return await executeManualUnlocked(...args); } finally { manualExecuting = false; }
    }

    async function recoverManualOperations({ key, tabId } = {}) {
      // Explicit trusted Manual preflight only. No startup scan and no provider work.
      const operation = await getManualOperation(key);
      if (!operation || operation.status !== MANUAL_STATUS || operation.request_worker_session_id === workerId ||
        operation.conversation_key !== key || Number(operation.tab_id) !== tabId || !validId(operation.batch_job_id)) fail("ASYNC_RECOVERY_NOT_OWNED");
      const existing = await getConversationOutbox(key);
      if (existing) {
        if (existing.type !== "manual" || existing.operation_id !== operation.operation_id) fail("DELIVERY_IN_PROGRESS");
        await setManualOperation(key, { ...operation, status: "delivering", delivery_id: existing.delivery_id,
          request_executed: existing.provider_executions === null || operation.request_executed === "UNKNOWN" ? "UNKNOWN"
            : Number(existing.provider_executions || 0) > 0 || operation.request_executed === true,
          recovered_at: nowIso() });
        return { ok: true, request_executed: false, existing_delivery: true };
      }
      await manualAuthority({ key, operation, folderId: operation.folder_id, action: "recover" });
      let recoveryError = null;
      try { await runtime.recover({ jobId: operation.batch_job_id, owner: key }); }
      catch (error) { recoveryError = error?.code || "ASYNC_RECOVERY_STORAGE_FAILED"; }
      const receipt = operation.execution_receipt;
      const mayHaveSent = ["submitN", "collectN"].includes(operation.batch_action);
      // An old snapshot without a receipt is not proof of zero paid requests.
      const executed = receipt ? executionOutcome(receipt) : mayHaveSent ? "UNKNOWN" : (operation.request_executed ?? false);
      const deliveryId = uid("delivery");
      const text = formatBridgeError({ code: recoveryError || "ASYNC_OPERATION_INTERRUPTED_NO_REPLAY",
        message: "Восстановлено сохранённое состояние прерванной операции. Повторных запросов и повторной отправки сообщения не выполнялось.",
        stage: "SEARCH_ASYNC_RECOVERY", requestExecuted: executed, service: searchService, channel: "manual",
        recoverable: executed !== "UNKNOWN", operation: `async.${operation.batch_action}`, operationId: operation.operation_id, autorunContinues: false });
      await putOutbox(key, { delivery_id: deliveryId, operation_id: operation.operation_id, type: "manual", tab_id: tabId,
        report_text: text, phase: "claimed", provider_executions: executed === "UNKNOWN" ? null : Number(receipt?.confirmed || 0),
        report_prefix_applied: false, created_at: nowIso() });
      await setManualOperation(key, { ...operation, status: "delivering", delivery_id: deliveryId,
        request_executed: executed, recovered_at: nowIso() });
      return { ok: true, request_executed: false, existing_delivery: false };
    }

    return Object.freeze({ executeManual, executeCommand, discover, recoverManualOperations, report, providerEnabled });
  }

  function autoInstall() {
    const binding = globalThis.YMBSearchAdmissionBinding;
    if (!binding?.ready) return Object.freeze({ ready: false, code: "ASYNC_SHARED_ADMISSION_NOT_READY" });
    const providerEnabled = (() => {
      try { return (chrome.runtime.getManifest()?.host_permissions || []).includes("https://operation.api.cloud.yandex.net/*"); }
      catch { return false; }
    })();
    const manualGet = async key => {
      const data = await storageGet(KEYS.MANUAL_OPERATIONS);
      return data?.[KEYS.MANUAL_OPERATIONS]?.[key] || null;
    };
    const manualSet = async (key, value) => {
      const data = await storageGet(KEYS.MANUAL_OPERATIONS); const map = { ...(data?.[KEYS.MANUAL_OPERATIONS] || {}) };
      if (value) map[key] = value; else delete map[key]; await storageSet({ [KEYS.MANUAL_OPERATIONS]: map }); return value;
    };
    const worker = create({
      baseExecuteManualBlock: executeManualBlock,
      protocol: globalThis.SearchAsyncProtocol,
      store: globalThis.YMBSearchAsyncStore,
      exportFactory: globalThis.YMBSearchAsyncExport,
      artifactStore: globalThis.YMBFileArtifactStore,
      runtimeFactory: globalThis.YMBSearchAsyncRuntime,
      transportFactory: globalThis.YMBSearchAsyncTransport,
      normalizerFactory: globalThis.YMBSearchAsyncNormalizer,
      searchXml: globalThis.YMBSearchXml,
      admissionBinding: binding,
      asyncPolicyFactory: globalThis.YMBSearchAsyncPolicy,
      getSettings, getBinding, getManualMode, getServiceContext, getAutoRun,
      getManualOperation: manualGet, setManualOperation: manualSet, getConversationOutbox,
      assertTabConversation, normalizeConversationKey, blockDiscovery: globalThis.YMBBlockCommandDiscovery,
      ordinaryDiscovery: text => globalThis.YMBSearchBatchTransport?.discover?.(text, globalThis.YMBBlockCommandDiscovery, globalThis.YMBServiceRegistry) || [],
      putOutbox, formatBridgeError, applyPrefixToReport, uid, nowIso,
      runContextModel: globalThis.YMBRunContextModel, autorunModel: globalThis.WordstatAutorunModel,
      workerId: WORKER_SESSION_ID, fetchImpl: fetch.bind(globalThis), providerEnabled
    });
    executeManualBlock = worker.executeManual;
    return Object.freeze({ ready: true, worker, providerEnabled });
  }

  globalThis.YMBSearchAsyncWorkerTransport = Object.freeze({ create, autoInstall, PREFIX, RESULT_PREFIX, MANUAL_STATUS });
  try { globalThis.YMBSearchAsyncWorkerIntegration = autoInstall(); }
  catch (error) { globalThis.YMBSearchAsyncWorkerIntegration = Object.freeze({ ready: false, code: error?.code || "ASYNC_WORKER_INSTALL_FAILED" }); }
})();
