/* global YMBWordstatBatchRuntime, WordstatBatchProtocol, YMBWordstatBatchTransport */
(() => {
  "use strict";

  const baseExecuteManualBlock = executeManualBlock;
  const baseHandleAutoCommand = handleAutoCommand;
  const WORDSTAT = YMBServiceRegistry.SERVICES.WORDSTAT;

  function batchPolicyRun(job, context = {}) {
    return {
      requests_executed: Number(job?.totals?.requests_started || 0),
      estimated_cost_rub: Number(job?.totals?.estimated_cost_rub || 0),
      ...(context?.policy_run && typeof context.policy_run === "object" ? clone(context.policy_run) : {})
    };
  }

  async function batchAdmission({ job, context = {} } = {}) {
    const [settings, policy] = await Promise.all([getSettings(), getWordstatPolicy()]);
    let run = null;
    if (context.conversation_key && context.run_id) {
      const candidate = await getAutoRun(context.conversation_key);
      if (candidate?.run_id === context.run_id) run = candidate;
    }
    const decision = policyDecisionForService(WORDSTAT, {
      policy,
      channel: context.channel === "autorun" ? "autorun" : "manual",
      method: "getTop",
      credentialState: publicCapability(settings, WORDSTAT).state,
      run: run || batchPolicyRun(job, context)
    });
    return {
      allow: decision.allow,
      reason: decision.reason,
      estimated_cost_rub: decision.estimated_cost_rub
    };
  }

  async function noteBatchProviderBoundary(metadata, estimatedCostRub) {
    const key = metadata?.conversation_key ? normalizeConversationKey(metadata.conversation_key) : "";
    const runId = String(metadata?.run_id || "");
    if (!key || !runId) return null;
    const current = await getAutoRun(key);
    if (!current || current.run_id !== runId) return null;
    return patchAutoRun(key, (run) => ({
      ...run,
      ...(metadata.channel === "autorun" ? {
        status: WordstatAutorunModel.RUN_STATUSES.REQUESTING,
        request_worker_session_id: WORKER_SESSION_ID
      } : {}),
      requests_attempted: Number(run.requests_attempted || 0) + 1,
      requests_executed: Number(run.requests_executed || 0) + 1,
      estimated_cost_rub: Number((Number(run.estimated_cost_rub || 0) + Number(estimatedCostRub || 0)).toFixed(6))
    }));
  }

  let batchRuntime = null;
  batchRuntime = YMBWordstatBatchRuntime.create({
    model: YMBProviderBatchJobModel,
    protocol: WordstatBatchProtocol,
    workerSessionId: `${WORKER_SESSION_ID}:wordstat-batch`,
    uid: () => uid("wordstat-batch"),
    estimateCostRub: async () => Number((await getWordstatPolicy()).method_cost_rub?.getTop || 0),
    admit: batchAdmission,
    executeWordstat: async (command, metadata = {}) => {
      const job = await batchRuntime.loadJob(metadata.job_id);
      const item = job.items?.find((candidate) => candidate.item_id === metadata.batch_item_id) || null;
      const estimatedCostRub = Number(item?.estimated_cost_rub || 0);
      await noteBatchProviderBoundary(metadata, estimatedCostRub);
      const policy = await getWordstatPolicy();
      return executeWordstatCommand(command, {
        ...metadata,
        cost_estimate: {
          estimated_rub: estimatedCostRub,
          tariff_checked_at: policy.tariff_checked_at,
          tariff_source: policy.tariff_source
        },
        policy: {
          channel: metadata.channel === "autorun" ? "autorun" : "manual",
          active_service: WORDSTAT
        }
      });
    }
  });

  function normalizedBatchCommand(rawCommand) {
    const command = WordstatBatchProtocol.normalizeCommand(rawCommand);
    if (command.action !== "start" || command.jobId) return command;
    return Object.freeze({ ...command, jobId: uid("wordstat-batch-job") });
  }

  async function executeWordstatBatchCommand(rawCommand, metadata = {}) {
    const command = normalizedBatchCommand(rawCommand);
    const handled = await batchRuntime.handle(command, metadata);
    const envelope = handled.envelope;
    return {
      ok: envelope.status !== "ERROR",
      request_id: envelope.item?.request_id || null,
      request_executed: envelope.request_executed,
      automatic_retry: false,
      report_envelope: envelope,
      report_text: WordstatBatchProtocol.formatResultEnvelope(envelope),
      job: handled.job,
      command
    };
  }

  function discoverBatchManualItem(blockText) {
    const discovered = YMBWordstatBatchTransport.discover(blockText, YMBBlockCommandDiscovery, YMBServiceRegistry);
    const batchItems = discovered.filter((item) => item.batch === true);
    if (!batchItems.length) return { batch: false, discovered };
    if (discovered.length !== 1 || batchItems.length !== 1) {
      return {
        batch: true,
        error: Object.assign(new Error("В первом Phase 6 slice один Manual block должен содержать ровно одну WORDSTAT_BATCH_API_V1 команду."), { code: "BATCH_SINGLE_COMMAND_REQUIRED" })
      };
    }
    const item = batchItems[0];
    if (!item.ok) return { batch: true, item, error: Object.assign(new Error(item.message || item.code), { code: item.code || "COMMAND_DISCOVERY" }) };
    try {
      return { batch: true, item, command: normalizedBatchCommand(item.raw) };
    } catch (error) {
      return { batch: true, item, error };
    }
  }

  async function executeBatchManualBlock(blockText, conversationKey, sender, manualRequestToken = "") {
    const discovered = discoverBatchManualItem(blockText);
    if (!discovered.batch) return baseExecuteManualBlock(blockText, conversationKey, sender, manualRequestToken);

    const key = normalizeConversationKey(conversationKey);
    const senderTabId = Number(sender?.tab?.id);
    if (!Number.isInteger(senderTabId)) return { ok: false, accepted: false, code: "MANUAL_SENDER_TAB_REQUIRED", error: "Manual action должна исходить из вкладки ChatGPT." };
    let liveIdentity;
    try { liveIdentity = await assertTabConversation(senderTabId, key); }
    catch (error) { return { ok: false, accepted: false, code: error.code, error: error.message }; }
    const binding = await getBinding(key);
    if (!binding || binding.conversation_id !== liveIdentity.conversation_id) return { ok: false, accepted: false, code: "CONVERSATION_NOT_BOUND", error: "Сначала привяжите этот диалог в popup." };
    if (!(await getManualMode(key))) return { ok: false, accepted: false, code: "MANUAL_MODE_DISABLED", error: "Ручной режим выключен." };
    const serviceContext = await getServiceContext(key);
    if (serviceContext.active_service !== WORDSTAT) return { ok: false, accepted: false, code: "SERVICE_NOT_ACTIVE", error: `Активный сервис ${serviceContext.active_service}; WORDSTAT_BATCH_API_V1 относится к wordstat.`, request_executed: false };

    const currentRun = await getAutoRun(key);
    if (currentRun && !WordstatAutorunModel.isTerminalStatus(currentRun.status) && currentRun.status !== WordstatAutorunModel.RUN_STATUSES.PAUSED) return { ok: false, accepted: false, code: "AUTORUN_NOT_PAUSED", error: "Для Manual активный Autorun должен быть поставлен на паузу." };
    if (currentRun?.status === WordstatAutorunModel.RUN_STATUSES.PAUSED) {
      if (senderTabId !== Number(currentRun.tab_id)) return { ok: false, accepted: false, code: "AUTO_NON_OWNER_TAB", error: "Manual action должна выполняться во вкладке-owner paused Autorun." };
      try { YMBRunContextModel.assertServiceMatch(currentRun.active_service, WORDSTAT); }
      catch (error) { return { ok: false, accepted: false, code: error.code, error: error.message }; }
    }

    const data = await storageGet(KEYS.MANUAL_OPERATIONS);
    const map = { ...(data[KEYS.MANUAL_OPERATIONS] || {}) };
    const existing = map[key];
    if (existing && !TERMINAL_MANUAL_STATUSES.has(existing.status)) return { ok: false, accepted: false, code: "MANUAL_OPERATION_ACTIVE", error: "Предыдущая ручная операция ещё не завершена." };
    const requestToken = String(manualRequestToken || uid("manual-request"));
    if (existing?.request_token === requestToken) return { ok: true, accepted: false, duplicate: true, operation_id: existing.operation_id };
    if (await getConversationOutbox(key)) return { ok: false, accepted: false, busy: true, code: "DELIVERY_IN_PROGRESS", error: "Сначала завершите текущую доставку для этого диалога." };

    const command = discovered.command || null;
    const operation = {
      operation_id: uid("manual"),
      request_token: requestToken,
      conversation_key: key,
      tab_id: senderTabId,
      active_service: WORDSTAT,
      run_id: currentRun?.status === WordstatAutorunModel.RUN_STATUSES.PAUSED ? currentRun.run_id : null,
      status: "batch_requesting",
      block_fingerprint: YMBBlockCommandDiscovery.textFingerprint(String(blockText || "")),
      batch_action: command?.action || null,
      batch_job_id: command?.jobId || null,
      created_at: nowIso(),
      request_executed: false
    };
    map[key] = operation;
    await storageSet({ [KEYS.MANUAL_OPERATIONS]: map });

    let reportText = "";
    let requestExecuted = false;
    let providerExecutions = 0;
    if (discovered.error) {
      reportText = formatBridgeError({
        code: discovered.error.code || "INVALID_BATCH_COMMAND",
        message: discovered.error.message || String(discovered.error),
        stage: "COMMAND_VALIDATION",
        requestExecuted: false,
        service: WORDSTAT,
        channel: "manual",
        recoverable: true,
        operation: command ? `batch.${command.action}` : null,
        operationId: operation.operation_id,
        autorunContinues: false
      });
    } else {
      try {
        const result = await executeWordstatBatchCommand(command, {
          channel: "manual",
          conversation_key: key,
          run_id: operation.run_id || null,
          operation_id: operation.operation_id
        });
        reportText = result.report_text;
        requestExecuted = result.request_executed;
        providerExecutions = requestExecuted === true ? 1 : 0;
      } catch (error) {
        requestExecuted = error?.request_executed ?? false;
        reportText = formatBridgeError({
          code: error?.code || "BATCH_RUNTIME_ERROR",
          message: error?.message || String(error),
          stage: "BATCH_RUNTIME",
          requestExecuted,
          service: WORDSTAT,
          channel: "manual",
          recoverable: requestExecuted !== "UNKNOWN",
          operation: command ? `batch.${command.action}` : null,
          operationId: operation.operation_id,
          autorunContinues: false
        });
      }
    }

    const prefixResult = providerExecutions > 0 ? await applyPrefixToReport(key, reportText) : { text: reportText, applied: false };
    reportText = prefixResult.text;
    const deliveryId = uid("delivery");
    await putOutbox(key, {
      delivery_id: deliveryId,
      operation_id: operation.operation_id,
      type: "manual",
      tab_id: senderTabId,
      report_text: reportText,
      phase: "claimed",
      provider_executions: requestExecuted === "UNKNOWN" ? null : providerExecutions,
      report_prefix_applied: prefixResult.applied === true,
      created_at: nowIso()
    });
    map[key] = {
      ...operation,
      status: "delivering",
      delivery_id: deliveryId,
      request_executed: requestExecuted,
      report_ready_at: nowIso()
    };
    await storageSet({ [KEYS.MANUAL_OPERATIONS]: map });
    return { ok: true, accepted: true, operation_id: operation.operation_id, delivery_id: deliveryId, report_text: reportText, request_executed: requestExecuted };
  }

  async function handleBatchAutoCommand(message, sender) {
    const commandText = String(message?.command_text || "");
    const detected = YMBWordstatBatchTransport.detect(commandText, YMBServiceRegistry);
    if (!detected?.batch) return baseHandleAutoCommand(message, sender);

    const key = normalizeConversationKey(message?.conversation_key);
    const runId = String(message?.run_id || "");
    const assistantTurnId = String(message?.assistant_turn_id || "");
    const senderTabId = Number(sender?.tab?.id);
    const currentRun = await getAutoRun(key);
    if (!currentRun || currentRun.run_id !== runId) return { ok: false, accepted: false, code: "AUTO_RUN_NOT_FOUND", error: "Autorun не найден." };
    if (!Number.isInteger(senderTabId) || senderTabId !== Number(currentRun.tab_id)) return { ok: false, accepted: false, code: "AUTO_NON_OWNER_TAB", error: "Команда появилась не во вкладке-owner активного Autorun." };
    try { await assertTabConversation(senderTabId, key, currentRun.conversation_id); }
    catch (error) { return { ok: false, accepted: false, code: error.code || "CONVERSATION_MISMATCH", error: error.message }; }
    if (await getManualMode(key)) return { ok: false, paused: true, code: "MANUAL_MODE_ACTIVE", error: "Ручной режим включён; Autorun не выполняет команду." };
    if (currentRun.status !== WordstatAutorunModel.RUN_STATUSES.WAITING_COMMAND) return { ok: true, accepted: false, ignored: true, busy: true, status: currentRun.status };
    if (assistantTurnId && currentRun.last_assistant_turn_id === assistantTurnId) return { ok: true, accepted: false, ignored: true, duplicate: true, status: currentRun.status };
    if (await getConversationOutbox(key)) return { ok: true, accepted: false, ignored: true, busy: true, code: "DELIVERY_IN_PROGRESS", status: currentRun.status, error: "Сначала завершите текущую доставку для этого диалога." };
    if (currentRun.active_service !== WORDSTAT) {
      return stageAutorunError(key, currentRun, senderTabId, {
        code: "SERVICE_NOT_ACTIVE",
        message: `Активный сервис ${currentRun.active_service}; WORDSTAT_BATCH_API_V1 относится к wordstat.`,
        stage: "SERVICE_ROUTING",
        requestExecuted: false,
        assistantTurnId
      });
    }

    let parsed;
    try { parsed = normalizedBatchCommand(WordstatBatchProtocol.parseCommand(commandText)); }
    catch (error) {
      return stageAutorunError(key, currentRun, senderTabId, {
        code: error.code || "INVALID_BATCH_COMMAND",
        message: error.message || String(error),
        stage: "COMMAND_VALIDATION",
        requestExecuted: false,
        assistantTurnId
      });
    }
    const fingerprint = WordstatBatchProtocol.commandFingerprint(parsed);
    if (currentRun.last_error?.request_executed === "UNKNOWN" && currentRun.last_command_fingerprint === fingerprint) {
      return { ok: false, accepted: false, code: "REQUEST_OUTCOME_UNKNOWN_NO_RETRY", error: "Предыдущая такая batch-команда имеет неизвестный исход. Автоматический повтор запрещён." };
    }

    let run = await patchAutoRun(key, (value) => ({
      ...value,
      last_assistant_turn_id: assistantTurnId,
      last_command_fingerprint: fingerprint,
      last_method: `batch.${parsed.action}`,
      last_phrase: null,
      last_error: null
    }));

    let result;
    try {
      result = await executeWordstatBatchCommand(parsed, {
        channel: "autorun",
        conversation_key: key,
        run_id: run.run_id
      });
    } catch (error) {
      const latestRun = await getAutoRun(key) || run;
      return stageAutorunError(key, latestRun, senderTabId, {
        code: error.code || "BATCH_RUNTIME_ERROR",
        message: error.message || String(error),
        stage: "BATCH_RUNTIME",
        requestExecuted: error?.request_executed ?? false,
        assistantTurnId,
        fingerprint,
        operation: `batch.${parsed.action}`,
        recoverable: (error?.request_executed ?? false) !== "UNKNOWN",
        autorunContinues: (error?.request_executed ?? false) !== "UNKNOWN"
      });
    }

    const requestExecuted = result.request_executed;
    const envelope = result.report_envelope;
    const prefixResult = requestExecuted === true ? await applyPrefixToReport(key, result.report_text) : { text: result.report_text, applied: false };
    const outgoingText = prefixResult.text;
    const deliveryId = uid("delivery");
    await putOutbox(key, {
      delivery_id: deliveryId,
      type: "autorun",
      run_id: run.run_id,
      tab_id: senderTabId,
      report_text: outgoingText,
      phase: "claimed",
      report_prefix_applied: prefixResult.applied === true,
      created_at: nowIso()
    });
    run = await patchAutoRun(key, (value) => ({
      ...value,
      status: WordstatAutorunModel.RUN_STATUSES.DELIVERING,
      requests_skipped: parsed.action === "next" && envelope.status === "SKIPPED"
        ? Number(value.requests_skipped || 0) + 1
        : Number(value.requests_skipped || 0),
      pause_requested: requestExecuted === "UNKNOWN" ? true : value.pause_requested === true,
      last_error: envelope.status === "ERROR" || requestExecuted === "UNKNOWN"
        ? { code: envelope.reason || "BATCH_ERROR", message: envelope.reason || "Batch command failed.", request_executed: requestExecuted, automatic_retry: false }
        : null,
      delivery: {
        delivery_id: deliveryId,
        phase: "claimed",
        request_id: result.request_id,
        outgoing_text: outgoingText,
        report_prefix_applied: prefixResult.applied === true
      }
    }));
    return { ok: true, accepted: true, report_text: outgoingText, result, run: publicRun(run) };
  }

  async function recoverBatchManualOperations() {
    const data = await storageGet(KEYS.MANUAL_OPERATIONS);
    const map = { ...(data[KEYS.MANUAL_OPERATIONS] || {}) };
    let changed = false;
    for (const [key, operation] of Object.entries(map)) {
      if (!operation || operation.status !== "batch_requesting") continue;
      const existing = await getConversationOutbox(key);
      if (existing?.operation_id === operation.operation_id) {
        map[key] = { ...operation, status: "delivering", delivery_id: existing.delivery_id, recovered_at: nowIso() };
        changed = true;
        continue;
      }
      let reportText;
      let requestExecuted = false;
      if (operation.batch_job_id) {
        try {
          const status = await executeWordstatBatchCommand({ action: "status", jobId: operation.batch_job_id }, { channel: "manual", conversation_key: key, run_id: operation.run_id || null });
          reportText = status.report_text;
          requestExecuted = Number(status.report_envelope?.progress?.outcome_unknown || 0) > 0 ? "UNKNOWN" : false;
        } catch (error) {
          reportText = formatBridgeError({ code: error.code || "BATCH_RECOVERY_ERROR", message: error.message || String(error), stage: "BATCH_RECOVERY", requestExecuted: false, service: WORDSTAT, channel: "manual", recoverable: true, operation: operation.batch_action ? `batch.${operation.batch_action}` : null, operationId: operation.operation_id, autorunContinues: false });
        }
      } else {
        reportText = formatBridgeError({ code: "BATCH_OPERATION_INTERRUPTED", message: "Batch operation была прервана до подтверждённого provider request; автоматический повтор не выполняется.", stage: "BATCH_RECOVERY", requestExecuted: false, service: WORDSTAT, channel: "manual", recoverable: true, operation: operation.batch_action ? `batch.${operation.batch_action}` : null, operationId: operation.operation_id, autorunContinues: false });
      }
      const deliveryId = uid("delivery");
      await putOutbox(key, { delivery_id: deliveryId, operation_id: operation.operation_id, type: "manual", tab_id: Number(operation.tab_id), report_text: reportText, phase: "claimed", provider_executions: requestExecuted === "UNKNOWN" ? null : 0, report_prefix_applied: false, created_at: nowIso() });
      map[key] = { ...operation, status: "delivering", delivery_id: deliveryId, request_executed: requestExecuted, report_ready_at: nowIso(), recovered_at: nowIso() };
      changed = true;
    }
    if (changed) await storageSet({ [KEYS.MANUAL_OPERATIONS]: map });
  }

  executeManualBlock = executeBatchManualBlock;
  handleAutoCommand = handleBatchAutoCommand;

  void batchRuntime.recoverAll()
    .then(recoverBatchManualOperations)
    .catch((error) => diagnostic("WORDSTAT_BATCH_RECOVERY_ERROR", { code: error?.code || "BATCH_RECOVERY_ERROR", message: error?.message || String(error) }, { level: "error" }));

  globalThis.YMBWordstatBatchWorkerTransport = Object.freeze({
    runtime: batchRuntime,
    executeWordstatBatchCommand
  });
})();
