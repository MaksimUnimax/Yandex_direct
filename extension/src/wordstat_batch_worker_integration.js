(() => {
  "use strict";

  const SERVICE = "wordstat";
  const MANUAL_OPERATIONS_KEY = "wsmb_manual_operations";
  const TERMINAL_MANUAL_STATUSES = new Set(["completed", "error", "cancelled"]);
  const baseExecuteManualBlock = globalThis.executeManualBlock;
  const baseHandleAutoCommand = globalThis.handleAutoCommand;

  if (typeof baseExecuteManualBlock !== "function" || typeof baseHandleAutoCommand !== "function") {
    throw new Error("Wordstat batch integration requires the accepted service_worker runtime.");
  }

  function copy(value) {
    return value == null ? value : JSON.parse(JSON.stringify(value));
  }

  function errorRequestExecuted(error, fallback = "UNKNOWN") {
    if (error?.request_executed === "UNKNOWN") return "UNKNOWN";
    if (error?.request_executed === true) return true;
    if (error?.request_executed === false) return false;
    if (String(error?.code || "").startsWith("BATCH_")) return false;
    return fallback;
  }

  function batchAwareDiscovery(blockText) {
    const discovered = globalThis.YMBWordstatBatchTransport.discover(
      blockText,
      globalThis.YMBBlockCommandDiscovery,
      globalThis.YMBServiceRegistry
    );
    const items = [];
    for (const entry of discovered) {
      const base = {
        service: entry.service,
        prefix: entry.prefix,
        marker_index: entry.index,
        batch: entry.batch === true,
        request_executed: false,
        automatic_retry: false,
        status: "pending"
      };
      if (!entry.ok) {
        items.push({ ...base, status: "error", stage: "COMMAND_DISCOVERY", code: entry.code, message: entry.message });
        continue;
      }
      try {
        const protocol = entry.batch === true
          ? globalThis.WordstatBatchProtocol
          : globalThis.assertProtocolForService(entry.service);
        const command = protocol.normalizeCommand(entry.raw);
        items.push({
          ...base,
          stage: "VALIDATED",
          operation: entry.batch === true ? `batch.${command.action}` : command.method,
          command
        });
      } catch (error) {
        items.push({
          ...base,
          status: "error",
          stage: "COMMAND_VALIDATION",
          code: error?.code || "INVALID_COMMAND",
          message: error?.message || String(error)
        });
      }
    }
    return { items, marker_count: discovered.length };
  }

  async function globalWordstatAdmission({ command, context = {} }) {
    const settings = await globalThis.getSettings();
    const policy = await globalThis.getWordstatPolicy();
    const run = context.run_id && context.conversation_key
      ? (await globalThis.getAutoRun(context.conversation_key)) || {}
      : {};
    const capability = globalThis.publicCapability(settings, SERVICE);
    const decision = globalThis.policyDecisionForService(SERVICE, {
      policy,
      channel: String(context.channel || "manual"),
      method: String(command?.method || "getTop"),
      credentialState: capability.state,
      run
    });
    return {
      allow: decision.allow,
      reason: decision.reason,
      estimated_cost_rub: decision.estimated_cost_rub
    };
  }

  let batchRuntime = null;

  async function executePaidWordstat(command, metadata = {}) {
    const job = await batchRuntime.loadJob(metadata.job_id);
    const item = (job.items || []).find((candidate) => candidate.item_id === metadata.batch_item_id) || null;
    const checkpointCost = Math.max(0, Number(item?.estimated_cost_rub || 0));

    const settings = await globalThis.getSettings();
    const policy = await globalThis.getWordstatPolicy();
    const run = metadata.run_id && metadata.conversation_key
      ? (await globalThis.getAutoRun(metadata.conversation_key)) || {}
      : {};
    const decision = globalThis.policyDecisionForService(SERVICE, {
      policy,
      channel: String(metadata.channel || "manual"),
      method: String(command?.method || "getTop"),
      credentialState: globalThis.publicCapability(settings, SERVICE).state,
      run
    });
    if (!decision.allow) {
      const error = Object.assign(new Error(`Wordstat policy blocked batch provider execution: ${decision.reason}.`), {
        code: `BATCH_${decision.reason || "POLICY_DENIED"}`,
        request_executed: false,
        automatic_retry: false
      });
      throw error;
    }
    if (Math.abs(Number(decision.estimated_cost_rub || 0) - checkpointCost) > 1e-12) {
      throw Object.assign(new Error("Wordstat policy cost changed after batch checkpoint; provider execution stopped fail-closed."), {
        code: "BATCH_POLICY_COST_CHANGED",
        request_executed: false,
        automatic_retry: false
      });
    }

    if (metadata.run_id && metadata.conversation_key) {
      await globalThis.patchAutoRun(metadata.conversation_key, (current) => ({
        ...current,
        requests_attempted: String(metadata.channel || "") === "manual"
          ? Number(current.requests_attempted || 0) + 1
          : Number(current.requests_attempted || 0),
        requests_executed: Number(current.requests_executed || 0) + 1,
        estimated_cost_rub: Number((Number(current.estimated_cost_rub || 0) + checkpointCost).toFixed(6)),
        request_worker_session_id: batchRuntime.workerSessionId
      }));
    }

    return globalThis.executeWordstatCommand(command, {
      ...metadata,
      cost_estimate: {
        estimated_rub: checkpointCost,
        tariff_checked_at: decision.policy?.tariff_checked_at || policy.tariff_checked_at,
        tariff_source: decision.policy?.tariff_source || policy.tariff_source
      },
      policy: { channel: String(metadata.channel || "manual"), active_service: SERVICE }
    });
  }

  batchRuntime = globalThis.YMBWordstatBatchRuntime.create({
    model: globalThis.YMBProviderBatchJobModel,
    protocol: globalThis.WordstatBatchProtocol,
    executeWordstat: executePaidWordstat,
    estimateCostRub: async (command) => {
      const policy = await globalThis.getWordstatPolicy();
      return globalThis.YMBPolicyModel.estimateMethodCost(policy, command?.method || "getTop");
    },
    admit: globalWordstatAdmission
  });

  async function executeWordstatBatchCommand(command, context = {}) {
    const result = await batchRuntime.handle(command, context);
    const envelope = result.envelope;
    return {
      ok: envelope?.status !== "ERROR",
      request_id: envelope?.item?.request_id || null,
      request_executed: envelope?.request_executed ?? false,
      automatic_retry: false,
      report_envelope: envelope,
      report_text: globalThis.WordstatBatchProtocol.formatResultEnvelope(envelope),
      job: result.job
    };
  }

  async function batchAwareManualBlock(blockText, conversationKey, sender, manualRequestToken = "") {
    const source = String(blockText || "");
    const discovered = batchAwareDiscovery(source);
    if (!discovered.items.some((item) => item.batch === true)) {
      return baseExecuteManualBlock(blockText, conversationKey, sender, manualRequestToken);
    }

    const key = globalThis.normalizeConversationKey(conversationKey);
    const senderTabId = Number(sender?.tab?.id);
    if (!Number.isInteger(senderTabId)) {
      return { ok: false, accepted: false, code: "MANUAL_SENDER_TAB_REQUIRED", error: "Manual action должна исходить из вкладки ChatGPT." };
    }

    let liveIdentity;
    try { liveIdentity = await globalThis.assertTabConversation(senderTabId, key); }
    catch (error) { return { ok: false, accepted: false, code: error.code, error: error.message }; }

    const binding = await globalThis.getBinding(key);
    if (!binding || binding.conversation_id !== liveIdentity.conversation_id) {
      return { ok: false, accepted: false, code: "CONVERSATION_NOT_BOUND", error: "Сначала привяжите этот диалог в popup." };
    }
    if (!(await globalThis.getManualMode(key))) {
      return { ok: false, accepted: false, code: "MANUAL_MODE_DISABLED", error: "Ручной режим выключен." };
    }

    const serviceContext = await globalThis.getServiceContext(key);
    const mismatch = discovered.items.find((item) => item.service && item.service !== serviceContext.active_service);
    if (mismatch) {
      return {
        ok: false,
        accepted: false,
        code: "SERVICE_NOT_ACTIVE",
        error: `Активный сервис ${serviceContext.active_service}; команда ${mismatch.prefix} относится к ${mismatch.service}.`,
        request_executed: false
      };
    }

    const currentRun = await globalThis.getAutoRun(key);
    if (currentRun && !globalThis.WordstatAutorunModel.isTerminalStatus(currentRun.status)
      && currentRun.status !== globalThis.WordstatAutorunModel.RUN_STATUSES.PAUSED) {
      return { ok: false, accepted: false, code: "AUTORUN_NOT_PAUSED", error: "Для Manual активный Autorun должен быть поставлен на паузу." };
    }
    if (currentRun?.status === globalThis.WordstatAutorunModel.RUN_STATUSES.PAUSED) {
      if (senderTabId !== Number(currentRun.tab_id)) {
        return { ok: false, accepted: false, code: "AUTO_NON_OWNER_TAB", error: "Manual action должна выполняться во вкладке-owner paused Autorun." };
      }
      try { globalThis.YMBRunContextModel.assertServiceMatch(currentRun.active_service, serviceContext.active_service); }
      catch (error) { return { ok: false, accepted: false, code: error.code, error: error.message }; }
    }

    const manualData = await chrome.storage.local.get(MANUAL_OPERATIONS_KEY);
    const manualMap = { ...(manualData[MANUAL_OPERATIONS_KEY] || {}) };
    const existing = manualMap[key];
    if (existing && !TERMINAL_MANUAL_STATUSES.has(existing.status)) {
      return { ok: false, accepted: false, code: "MANUAL_OPERATION_ACTIVE", error: "Предыдущая ручная операция ещё не завершена." };
    }
    const requestToken = String(manualRequestToken || globalThis.uid("manual-request"));
    if (existing?.request_token === requestToken) {
      return { ok: true, accepted: false, duplicate: true, operation_id: existing.operation_id };
    }
    if (await globalThis.getConversationOutbox(key)) {
      return { ok: false, accepted: false, busy: true, code: "DELIVERY_IN_PROGRESS", error: "Сначала завершите текущую доставку для этого диалога." };
    }

    const operation = {
      operation_id: globalThis.uid("manual"),
      request_token: requestToken,
      conversation_key: key,
      tab_id: senderTabId,
      active_service: serviceContext.active_service,
      run_id: currentRun?.status === globalThis.WordstatAutorunModel.RUN_STATUSES.PAUSED ? currentRun.run_id : null,
      status: "requesting",
      block_fingerprint: globalThis.YMBBlockCommandDiscovery.textFingerprint(source),
      created_at: globalThis.nowIso(),
      request_executed: false,
      batch_transport: true
    };
    manualMap[key] = operation;
    await chrome.storage.local.set({ [MANUAL_OPERATIONS_KEY]: manualMap });

    const reports = [];
    let providerExecutions = 0;
    let requestExecutedSummary = false;

    for (const item of discovered.items) {
      if (item.status === "error") {
        reports.push(globalThis.formatBridgeError({
          code: item.code,
          message: item.message,
          stage: item.stage,
          requestExecuted: false,
          service: item.service,
          channel: "manual",
          recoverable: true,
          operation: item.operation || null,
          operationId: operation.operation_id,
          autorunContinues: false
        }));
        continue;
      }

      if (item.batch === true) {
        try {
          const result = await executeWordstatBatchCommand(item.command, {
            conversation_key: key,
            run_id: operation.run_id || null,
            channel: "manual"
          });
          const executed = result.request_executed;
          if (executed === true) {
            providerExecutions += 1;
            if (requestExecutedSummary !== "UNKNOWN") requestExecutedSummary = true;
          } else if (executed === "UNKNOWN") {
            requestExecutedSummary = "UNKNOWN";
          }
          reports.push(result.report_text);
          if (executed === "UNKNOWN") break;
        } catch (error) {
          const executed = errorRequestExecuted(error);
          if (executed === "UNKNOWN") requestExecutedSummary = "UNKNOWN";
          else if (executed === true && requestExecutedSummary !== "UNKNOWN") requestExecutedSummary = true;
          reports.push(globalThis.formatBridgeError({
            code: error?.code || "BATCH_RUNTIME_ERROR",
            message: error?.message || String(error),
            stage: "BATCH_RUNTIME",
            requestExecuted: executed,
            service: SERVICE,
            channel: "manual",
            recoverable: executed !== "UNKNOWN",
            runId: operation.run_id,
            operation: item.operation,
            operationId: operation.operation_id,
            autorunContinues: false
          }));
          if (executed === "UNKNOWN") break;
        }
        continue;
      }

      const settings = await globalThis.getSettings();
      const policy = await globalThis.getPolicyForService(item.service);
      const budgetRun = operation.run_id ? await globalThis.getAutoRun(key) : {};
      const decision = globalThis.policyDecisionForService(item.service, {
        policy,
        channel: "manual",
        method: item.command.method,
        credentialState: globalThis.publicCapability(settings, item.service).state,
        run: budgetRun || {}
      });
      if (!decision.allow) {
        const protocol = globalThis.assertProtocolForService(item.service);
        reports.push(protocol.formatSkippedReport({
          requestId: globalThis.uid("skip"),
          command: item.command,
          reason: decision.reason,
          metadata: {
            run_id: operation.run_id || null,
            cost_estimate: {
              estimated_rub: decision.estimated_cost_rub,
              tariff_checked_at: decision.policy.tariff_checked_at,
              tariff_source: decision.policy.tariff_source
            },
            policy: { channel: "manual", active_service: item.service },
            request_executed: false,
            automatic_retry: false
          }
        }));
        continue;
      }
      if (operation.run_id) {
        await globalThis.patchAutoRun(key, (run) => ({
          ...run,
          requests_attempted: Number(run.requests_attempted || 0) + 1,
          requests_executed: Number(run.requests_executed || 0) + 1,
          estimated_cost_rub: Number((Number(run.estimated_cost_rub || 0) + Number(decision.estimated_cost_rub || 0)).toFixed(6))
        }));
      }
      try {
        const result = await globalThis.executeServiceCommand(item.service, item.command, {
          conversation_key: key,
          run_id: operation.run_id || null,
          cost_estimate: {
            estimated_rub: decision.estimated_cost_rub,
            tariff_checked_at: decision.policy.tariff_checked_at,
            tariff_source: decision.policy.tariff_source
          },
          policy: { channel: "manual", active_service: item.service }
        });
        providerExecutions += 1;
        if (requestExecutedSummary !== "UNKNOWN") requestExecutedSummary = true;
        reports.push(result.report_text);
      } catch (error) {
        const executed = errorRequestExecuted(error);
        if (executed === "UNKNOWN") requestExecutedSummary = "UNKNOWN";
        else if (executed === true && requestExecutedSummary !== "UNKNOWN") requestExecutedSummary = true;
        reports.push(globalThis.formatBridgeError({
          code: error.code || "PROVIDER_ERROR",
          message: error.message || String(error),
          stage: "PROVIDER",
          requestExecuted: executed,
          service: item.service,
          channel: "manual",
          recoverable: executed !== "UNKNOWN",
          runId: operation.run_id,
          operation: item.command?.method || null,
          operationId: operation.operation_id,
          autorunContinues: false
        }));
        if (executed === "UNKNOWN") break;
      }
    }

    let reportText = reports.join("\n\n---\n\n");
    const prefixResult = providerExecutions > 0
      ? await globalThis.applyPrefixToReport(key, reportText)
      : { text: reportText, applied: false };
    reportText = prefixResult.text;

    const deliveryId = globalThis.uid("delivery");
    await globalThis.putOutbox(key, {
      delivery_id: deliveryId,
      operation_id: operation.operation_id,
      type: "manual",
      tab_id: senderTabId,
      report_text: reportText,
      phase: "claimed",
      provider_executions: requestExecutedSummary === "UNKNOWN" ? null : providerExecutions,
      report_prefix_applied: prefixResult.applied === true,
      created_at: globalThis.nowIso()
    });
    manualMap[key] = {
      ...operation,
      status: "delivering",
      delivery_id: deliveryId,
      request_executed: requestExecutedSummary,
      report_ready_at: globalThis.nowIso()
    };
    await chrome.storage.local.set({ [MANUAL_OPERATIONS_KEY]: manualMap });
    return {
      ok: true,
      accepted: true,
      operation_id: operation.operation_id,
      delivery_id: deliveryId,
      report_text: reportText,
      request_executed: requestExecutedSummary
    };
  }

  async function batchAwareAutoCommand(message, sender) {
    const commandText = String(message?.command_text || "");
    if (!globalThis.WordstatBatchProtocol.isCommandText(commandText)) {
      return baseHandleAutoCommand(message, sender);
    }

    const key = globalThis.normalizeConversationKey(message?.conversation_key);
    const runId = String(message?.run_id || "");
    const assistantTurnId = String(message?.assistant_turn_id || "");
    const senderTabId = Number(sender?.tab?.id);
    const currentRun = await globalThis.getAutoRun(key);

    if (!currentRun || currentRun.run_id !== runId) {
      return { ok: false, accepted: false, code: "AUTO_RUN_NOT_FOUND", error: "Autorun не найден." };
    }
    if (!Number.isInteger(senderTabId) || senderTabId !== Number(currentRun.tab_id)) {
      return { ok: false, accepted: false, code: "AUTO_NON_OWNER_TAB", error: "Команда появилась не во вкладке-owner активного Autorun." };
    }
    try { await globalThis.assertTabConversation(senderTabId, key, currentRun.conversation_id); }
    catch (error) { return { ok: false, accepted: false, code: error.code || "CONVERSATION_MISMATCH", error: error.message }; }
    if (await globalThis.getManualMode(key)) {
      return { ok: false, paused: true, code: "MANUAL_MODE_ACTIVE", error: "Ручной режим включён; Autorun не выполняет команду." };
    }
    if (currentRun.status !== globalThis.WordstatAutorunModel.RUN_STATUSES.WAITING_COMMAND) {
      return { ok: true, accepted: false, ignored: true, busy: true, status: currentRun.status };
    }
    if (assistantTurnId && currentRun.last_assistant_turn_id === assistantTurnId) {
      return { ok: true, accepted: false, ignored: true, duplicate: true, status: currentRun.status };
    }
    if (await globalThis.getConversationOutbox(key)) {
      return { ok: true, accepted: false, ignored: true, busy: true, code: "DELIVERY_IN_PROGRESS", status: currentRun.status, error: "Сначала завершите текущую доставку для этого диалога." };
    }

    try { globalThis.YMBRunContextModel.assertServiceMatch(currentRun.active_service, SERVICE); }
    catch (error) {
      return globalThis.stageAutorunError(key, currentRun, senderTabId, {
        code: error.code || "SERVICE_NOT_ACTIVE",
        message: error.message,
        stage: "SERVICE_ROUTING",
        requestExecuted: false,
        assistantTurnId
      });
    }

    let parsed;
    try { parsed = globalThis.WordstatBatchProtocol.parseCommand(commandText); }
    catch (error) {
      return globalThis.stageAutorunError(key, currentRun, senderTabId, {
        code: error.code || "INVALID_COMMAND",
        message: error.message || String(error),
        stage: "COMMAND_VALIDATION",
        requestExecuted: false,
        assistantTurnId
      });
    }

    const fingerprint = globalThis.WordstatBatchProtocol.commandFingerprint(parsed);
    if (currentRun.last_error?.request_executed === "UNKNOWN"
      && currentRun.last_command_fingerprint === fingerprint) {
      return {
        ok: false,
        accepted: false,
        code: "REQUEST_OUTCOME_UNKNOWN_NO_RETRY",
        error: "Предыдущий такой же batch next имеет неизвестный исход. Автоматический повтор запрещён."
      };
    }

    const isNext = parsed.action === "next";
    let run = await globalThis.patchAutoRun(key, (value) => ({
      ...value,
      last_assistant_turn_id: assistantTurnId,
      last_command_fingerprint: fingerprint,
      last_method: `batch.${parsed.action}`,
      last_phrase: parsed.phrases?.[0] || null,
      requests_attempted: Number(value.requests_attempted || 0) + (isNext ? 1 : 0),
      status: isNext ? globalThis.WordstatAutorunModel.RUN_STATUSES.REQUESTING : value.status,
      request_worker_session_id: isNext ? batchRuntime.workerSessionId : value.request_worker_session_id,
      last_error: null
    }));

    let result;
    try {
      result = await executeWordstatBatchCommand(parsed, {
        conversation_key: key,
        run_id: run.run_id,
        channel: "autorun"
      });
    } catch (error) {
      const executed = errorRequestExecuted(error);
      const latestRun = (await globalThis.getAutoRun(key)) || run;
      return globalThis.stageAutorunError(key, latestRun, senderTabId, {
        code: error.code || "BATCH_RUNTIME_ERROR",
        message: error.message || String(error),
        stage: "BATCH_RUNTIME",
        requestExecuted: executed,
        assistantTurnId,
        fingerprint,
        operation: `batch.${parsed.action}`,
        recoverable: executed !== "UNKNOWN",
        autorunContinues: executed !== "UNKNOWN"
      });
    }

    const executed = result.request_executed;
    const prefixResult = executed === true
      ? await globalThis.applyPrefixToReport(key, result.report_text)
      : { text: result.report_text, applied: false };
    const outgoingText = prefixResult.text;
    const deliveryId = globalThis.uid("delivery");

    await globalThis.putOutbox(key, {
      delivery_id: deliveryId,
      type: "autorun",
      run_id: run.run_id,
      tab_id: senderTabId,
      report_text: outgoingText,
      phase: "claimed",
      report_prefix_applied: prefixResult.applied === true,
      created_at: globalThis.nowIso()
    });

    run = await globalThis.patchAutoRun(key, (value) => ({
      ...value,
      status: globalThis.WordstatAutorunModel.RUN_STATUSES.DELIVERING,
      requests_skipped: Number(value.requests_skipped || 0) + (result.report_envelope?.status === "SKIPPED" ? 1 : 0),
      last_error: result.report_envelope?.status === "ERROR"
        ? {
            code: result.report_envelope?.reason || "BATCH_ITEM_ERROR",
            message: result.report_envelope?.reason || "Batch item failed.",
            request_executed: executed,
            automatic_retry: false
          }
        : null,
      delivery: {
        delivery_id: deliveryId,
        phase: "claimed",
        request_id: result.request_id,
        outgoing_text: outgoingText,
        report_prefix_applied: prefixResult.applied === true
      }
    }));

    return {
      ok: true,
      accepted: true,
      skipped: result.report_envelope?.status === "SKIPPED",
      report_text: outgoingText,
      result,
      run: globalThis.publicRun(run)
    };
  }

  globalThis.executeManualBlock = batchAwareManualBlock;
  globalThis.handleAutoCommand = batchAwareAutoCommand;
  globalThis.YMBWordstatBatchWorkerIntegration = Object.freeze({
    runtime: batchRuntime,
    discoverManualBlockItems: batchAwareDiscovery,
    executeWordstatBatchCommand
  });

  Promise.resolve(batchRuntime.recoverAll()).catch((error) => {
    if (typeof globalThis.diagnostic === "function") {
      return globalThis.diagnostic("WORDSTAT_BATCH_RECOVERY_ERROR", {
        code: error?.code || "BATCH_RECOVERY_ERROR",
        message: error?.message || String(error)
      }, { level: "error" });
    }
    return undefined;
  });
})();
