(() => {
  "use strict";

  const ITEM_STATUSES = Object.freeze({
    PENDING: "PENDING",
    CLAIMED: "CLAIMED",
    REQUEST_STARTED: "REQUEST_STARTED",
    SUCCEEDED: "SUCCEEDED",
    FAILED_TERMINAL: "FAILED_TERMINAL",
    OUTCOME_UNKNOWN: "OUTCOME_UNKNOWN",
    SKIPPED: "SKIPPED",
    CANCELLED: "CANCELLED"
  });

  const JOB_STATUSES = Object.freeze({
    RUNNING: "RUNNING",
    PAUSED: "PAUSED",
    CANCELLING: "CANCELLING",
    CANCELLED: "CANCELLED",
    COMPLETED: "COMPLETED"
  });

  const TERMINAL_ITEM_STATUSES = new Set([
    ITEM_STATUSES.SUCCEEDED,
    ITEM_STATUSES.FAILED_TERMINAL,
    ITEM_STATUSES.OUTCOME_UNKNOWN,
    ITEM_STATUSES.SKIPPED,
    ITEM_STATUSES.CANCELLED
  ]);

  function fail(code, message) {
    const error = new Error(message || code);
    error.code = code;
    throw error;
  }

  function clone(value) {
    return value == null ? value : JSON.parse(JSON.stringify(value));
  }

  function nowValue(value) {
    const text = String(value || "").trim();
    return text || new Date().toISOString();
  }

  function canonicalize(value) {
    if (value === null) return "null";
    if (Array.isArray(value)) return `[${value.map(canonicalize).join(",")}]`;
    const type = typeof value;
    if (type === "string") return JSON.stringify(value);
    if (type === "number") return Number.isFinite(value) ? JSON.stringify(value) : JSON.stringify(String(value));
    if (type === "boolean") return value ? "true" : "false";
    if (type === "undefined") return '"[undefined]"';
    if (type !== "object") return JSON.stringify(String(value));
    const keys = Object.keys(value).sort();
    return `{${keys.map((key) => `${JSON.stringify(key)}:${canonicalize(value[key])}`).join(",")}}`;
  }

  function fnv32(text, seed = 2166136261) {
    let hash = seed >>> 0;
    for (let index = 0; index < text.length; index += 1) {
      hash ^= text.charCodeAt(index);
      hash = Math.imul(hash, 16777619);
    }
    return hash >>> 0;
  }

  function commandFingerprint(command) {
    const canonical = canonicalize(command);
    const a = fnv32(canonical, 2166136261);
    const b = fnv32(canonical, 3339675911 ^ canonical.length);
    return `${a.toString(16).padStart(8, "0")}${b.toString(16).padStart(8, "0")}`;
  }

  function normalizeLimit(value, { integer = false } = {}) {
    if (value === undefined || value === null || value === "") return null;
    const number = Number(value);
    if (!Number.isFinite(number) || number < 0) fail("INVALID_BATCH_LIMIT", "Batch limit должен быть неотрицательным числом.");
    if (integer && !Number.isInteger(number)) fail("INVALID_BATCH_LIMIT", "Request limit должен быть целым числом.");
    return number;
  }

  function normalizeLimits(raw = {}) {
    return {
      max_requests: normalizeLimit(raw.maxRequests ?? raw.max_requests, { integer: true }),
      max_cost_rub: normalizeLimit(raw.maxCostRub ?? raw.max_cost_rub)
    };
  }

  function itemById(job, itemId) {
    const id = String(itemId || "");
    const index = (job.items || []).findIndex((item) => item.item_id === id);
    if (index < 0) fail("BATCH_ITEM_NOT_FOUND", `Batch item не найден: ${id}`);
    return { index, item: job.items[index] };
  }

  function assertItemStatus(item, expected) {
    if (item.status !== expected) {
      fail(
        "INVALID_BATCH_ITEM_TRANSITION",
        `Недопустимый переход batch item ${item.item_id}: ${item.status} вместо ${expected}.`
      );
    }
  }

  function countStatuses(job) {
    const counts = Object.fromEntries(Object.values(ITEM_STATUSES).map((status) => [status, 0]));
    for (const item of job.items || []) {
      if (counts[item.status] === undefined) counts[item.status] = 0;
      counts[item.status] += 1;
    }
    return counts;
  }

  function hasInFlight(job) {
    return (job.items || []).some((item) => item.status === ITEM_STATUSES.CLAIMED || item.status === ITEM_STATUSES.REQUEST_STARTED);
  }

  function settleJob(job, now) {
    const next = job;
    const counts = countStatuses(next);
    const pending = counts[ITEM_STATUSES.PENDING] || 0;
    const inFlight = (counts[ITEM_STATUSES.CLAIMED] || 0) + (counts[ITEM_STATUSES.REQUEST_STARTED] || 0);

    if (next.status === JOB_STATUSES.CANCELLING) {
      if (inFlight === 0) {
        next.status = JOB_STATUSES.CANCELLED;
        next.completed_at = nowValue(now);
      }
      return next;
    }

    if (next.status === JOB_STATUSES.PAUSED) return next;

    if (pending === 0 && inFlight === 0) {
      next.status = JOB_STATUSES.COMPLETED;
      next.completed_at = next.completed_at || nowValue(now);
    } else if (next.status !== JOB_STATUSES.CANCELLED) {
      next.status = JOB_STATUSES.RUNNING;
    }
    return next;
  }

  function createJob({ jobId, service, commands, limits = {}, now = "" } = {}) {
    const id = String(jobId || "").trim();
    const serviceName = String(service || "").trim();
    if (!id) fail("BATCH_JOB_ID_REQUIRED", "jobId обязателен.");
    if (!serviceName) fail("BATCH_SERVICE_REQUIRED", "service обязателен.");
    if (!Array.isArray(commands) || commands.length === 0) fail("BATCH_COMMANDS_REQUIRED", "commands должен содержать хотя бы одну команду.");

    const createdAt = nowValue(now);
    const seenCanonical = new Map();
    const items = [];
    let duplicateCount = 0;

    for (const rawCommand of commands) {
      if (!rawCommand || typeof rawCommand !== "object" || Array.isArray(rawCommand)) {
        fail("INVALID_BATCH_COMMAND", "Каждая batch-команда должна быть объектом.");
      }
      const command = clone(rawCommand);
      const canonical = canonicalize(command);
      if (seenCanonical.has(canonical)) {
        duplicateCount += 1;
        continue;
      }
      const fingerprint = commandFingerprint(command);
      seenCanonical.set(canonical, fingerprint);
      items.push({
        item_id: `${id}:${fingerprint}`,
        fingerprint,
        command,
        status: ITEM_STATUSES.PENDING,
        claimed_by: null,
        claimed_at: null,
        request_id: null,
        request_worker_session_id: null,
        request_started_at: null,
        estimated_cost_rub: 0,
        request_executed: false,
        automatic_retry: false,
        result_ref: null,
        error: null,
        outcome_unknown_reason: null,
        completed_at: null,
        updated_at: createdAt
      });
    }

    if (items.length === 0) fail("BATCH_COMMANDS_REQUIRED", "После удаления точных дублей не осталось batch-команд.");

    return Object.freeze({
      schema_version: 1,
      job_id: id,
      service: serviceName,
      status: JOB_STATUSES.RUNNING,
      revision: 1,
      input_count: commands.length,
      duplicate_count: duplicateCount,
      items,
      active_item_id: null,
      limits: normalizeLimits(limits),
      totals: {
        requests_started: 0,
        estimated_cost_rub: 0
      },
      stop_reason: null,
      cancel_reason: null,
      created_at: createdAt,
      updated_at: createdAt,
      completed_at: null
    });
  }

  function mutable(job) {
    if (!job || typeof job !== "object") fail("INVALID_BATCH_JOB", "Некорректный batch job.");
    const next = clone(job);
    next.items = Array.isArray(next.items) ? next.items : [];
    next.totals = next.totals || { requests_started: 0, estimated_cost_rub: 0 };
    next.limits = next.limits || { max_requests: null, max_cost_rub: null };
    return next;
  }

  function budgetDecision(job, nextEstimatedCostRub = 0) {
    const nextCost = Math.max(0, Number(nextEstimatedCostRub || 0));
    const maxRequests = job.limits?.max_requests;
    const maxCost = job.limits?.max_cost_rub;
    const requests = Math.max(0, Number(job.totals?.requests_started || 0));
    const cost = Math.max(0, Number(job.totals?.estimated_cost_rub || 0));

    if (maxRequests !== null && maxRequests !== undefined && requests >= Number(maxRequests)) {
      return { allow: false, reason: "REQUEST_LIMIT_REACHED" };
    }
    if (maxCost !== null && maxCost !== undefined && cost + nextCost > Number(maxCost) + 1e-12) {
      return { allow: false, reason: "COST_LIMIT_REACHED" };
    }
    return { allow: true, reason: null };
  }

  function claimNext(job, { actorId = "", nextEstimatedCostRub = 0, now = "" } = {}) {
    const next = mutable(job);
    const timestamp = nowValue(now);

    if (next.status === JOB_STATUSES.PAUSED) return { job: Object.freeze(next), item: null, reason: "JOB_PAUSED" };
    if (next.status === JOB_STATUSES.CANCELLING) return { job: Object.freeze(next), item: null, reason: "JOB_CANCELLING" };
    if (next.status === JOB_STATUSES.CANCELLED) return { job: Object.freeze(next), item: null, reason: "JOB_CANCELLED" };
    if (next.status === JOB_STATUSES.COMPLETED) return { job: Object.freeze(next), item: null, reason: "JOB_COMPLETED" };
    if (next.items.some((item) => item.status === ITEM_STATUSES.OUTCOME_UNKNOWN)) {
      next.stop_reason = "OUTCOME_UNKNOWN_REQUIRES_RECONCILIATION";
      next.updated_at = timestamp;
      return { job: Object.freeze(next), item: null, reason: "OUTCOME_UNKNOWN_REQUIRES_RECONCILIATION" };
    }
    if (next.active_item_id || hasInFlight(next)) return { job: Object.freeze(next), item: null, reason: "ITEM_ACTIVE" };

    const budget = budgetDecision(next, nextEstimatedCostRub);
    if (!budget.allow) {
      next.stop_reason = budget.reason;
      next.updated_at = timestamp;
      return { job: Object.freeze(next), item: null, reason: budget.reason };
    }

    const index = next.items.findIndex((item) => item.status === ITEM_STATUSES.PENDING);
    if (index < 0) {
      settleJob(next, timestamp);
      const unknown = next.items.some((item) => item.status === ITEM_STATUSES.OUTCOME_UNKNOWN);
      const reason = unknown ? "OUTCOME_UNKNOWN_REQUIRES_RECONCILIATION" : "NO_PENDING_ITEMS";
      next.stop_reason = reason;
      next.updated_at = timestamp;
      return { job: Object.freeze(next), item: null, reason };
    }

    const actor = String(actorId || "").slice(0, 240) || null;
    const item = next.items[index];
    item.status = ITEM_STATUSES.CLAIMED;
    item.claimed_by = actor;
    item.claimed_at = timestamp;
    item.updated_at = timestamp;
    next.active_item_id = item.item_id;
    next.stop_reason = null;
    next.revision = Math.max(1, Number(next.revision || 1)) + 1;
    next.updated_at = timestamp;
    return { job: Object.freeze(next), item: clone(item), reason: null };
  }

  function markRequestStarted(job, itemId, { requestId = "", workerSessionId = "", estimatedCostRub = 0, now = "" } = {}) {
    const next = mutable(job);
    const timestamp = nowValue(now);
    const { item } = itemById(next, itemId);
    assertItemStatus(item, ITEM_STATUSES.CLAIMED);
    if (next.active_item_id !== item.item_id) fail("INVALID_BATCH_ITEM_TRANSITION", "Claimed item не является активным item job-а.");

    const request = String(requestId || "").trim();
    if (!request) fail("BATCH_REQUEST_ID_REQUIRED", "requestId обязателен на границе REQUEST_STARTED.");
    const cost = Number(estimatedCostRub || 0);
    if (!Number.isFinite(cost) || cost < 0) fail("INVALID_BATCH_COST", "estimatedCostRub должен быть неотрицательным числом.");

    const budget = budgetDecision(next, cost);
    if (!budget.allow) fail("BATCH_BUDGET_EXCEEDED_AT_START", budget.reason);

    item.status = ITEM_STATUSES.REQUEST_STARTED;
    item.request_id = request.slice(0, 240);
    item.request_worker_session_id = String(workerSessionId || "").slice(0, 240) || null;
    item.request_started_at = timestamp;
    item.estimated_cost_rub = cost;
    item.request_executed = true;
    item.automatic_retry = false;
    item.updated_at = timestamp;

    next.totals.requests_started = Math.max(0, Number(next.totals.requests_started || 0)) + 1;
    next.totals.estimated_cost_rub = Math.max(0, Number(next.totals.estimated_cost_rub || 0)) + cost;
    next.revision = Math.max(1, Number(next.revision || 1)) + 1;
    next.updated_at = timestamp;
    return Object.freeze(next);
  }

  function markSucceeded(job, itemId, { resultRef = "", requestExecuted = true, now = "" } = {}) {
    const next = mutable(job);
    const timestamp = nowValue(now);
    const { item } = itemById(next, itemId);
    assertItemStatus(item, ITEM_STATUSES.REQUEST_STARTED);
    item.status = ITEM_STATUSES.SUCCEEDED;
    item.result_ref = String(resultRef || "").slice(0, 500) || null;
    item.request_executed = requestExecuted !== false;
    item.automatic_retry = false;
    item.completed_at = timestamp;
    item.updated_at = timestamp;
    if (next.active_item_id === item.item_id) next.active_item_id = null;
    next.revision = Math.max(1, Number(next.revision || 1)) + 1;
    next.updated_at = timestamp;
    settleJob(next, timestamp);
    return Object.freeze(next);
  }

  function markFailedTerminal(job, itemId, { code = "PROVIDER_ERROR", message = "", requestExecuted = true, now = "" } = {}) {
    const next = mutable(job);
    const timestamp = nowValue(now);
    const { item } = itemById(next, itemId);
    assertItemStatus(item, ITEM_STATUSES.REQUEST_STARTED);
    item.status = ITEM_STATUSES.FAILED_TERMINAL;
    item.error = {
      code: String(code || "PROVIDER_ERROR").slice(0, 160),
      message: String(message || "").slice(0, 2000)
    };
    item.request_executed = requestExecuted !== false;
    item.automatic_retry = false;
    item.completed_at = timestamp;
    item.updated_at = timestamp;
    if (next.active_item_id === item.item_id) next.active_item_id = null;
    next.revision = Math.max(1, Number(next.revision || 1)) + 1;
    next.updated_at = timestamp;
    settleJob(next, timestamp);
    return Object.freeze(next);
  }

  function markOutcomeUnknown(job, itemId, { reason = "REQUEST_OUTCOME_UNKNOWN_NO_RETRY", now = "" } = {}) {
    const next = mutable(job);
    const timestamp = nowValue(now);
    const { item } = itemById(next, itemId);
    assertItemStatus(item, ITEM_STATUSES.REQUEST_STARTED);
    item.status = ITEM_STATUSES.OUTCOME_UNKNOWN;
    item.outcome_unknown_reason = String(reason || "REQUEST_OUTCOME_UNKNOWN_NO_RETRY").slice(0, 240);
    item.request_executed = true;
    item.automatic_retry = false;
    item.completed_at = timestamp;
    item.updated_at = timestamp;
    if (next.active_item_id === item.item_id) next.active_item_id = null;
    next.stop_reason = "OUTCOME_UNKNOWN_REQUIRES_RECONCILIATION";
    next.revision = Math.max(1, Number(next.revision || 1)) + 1;
    next.updated_at = timestamp;
    settleJob(next, timestamp);
    return Object.freeze(next);
  }

  function skip(job, itemId, { reason = "SKIPPED", now = "" } = {}) {
    const next = mutable(job);
    const timestamp = nowValue(now);
    const { item } = itemById(next, itemId);
    assertItemStatus(item, ITEM_STATUSES.PENDING);
    item.status = ITEM_STATUSES.SKIPPED;
    item.error = { code: "SKIPPED", message: String(reason || "SKIPPED").slice(0, 2000) };
    item.completed_at = timestamp;
    item.updated_at = timestamp;
    next.revision = Math.max(1, Number(next.revision || 1)) + 1;
    next.updated_at = timestamp;
    settleJob(next, timestamp);
    return Object.freeze(next);
  }

  function pause(job, { reason = "PAUSED", now = "" } = {}) {
    const next = mutable(job);
    const timestamp = nowValue(now);
    if ([JOB_STATUSES.CANCELLED, JOB_STATUSES.COMPLETED, JOB_STATUSES.CANCELLING].includes(next.status)) return Object.freeze(next);
    for (const item of next.items) {
      if (item.status === ITEM_STATUSES.CLAIMED) {
        item.status = ITEM_STATUSES.PENDING;
        item.claimed_by = null;
        item.claimed_at = null;
        item.updated_at = timestamp;
        if (next.active_item_id === item.item_id) next.active_item_id = null;
      }
    }
    next.status = JOB_STATUSES.PAUSED;
    next.stop_reason = String(reason || "PAUSED").slice(0, 240);
    next.revision = Math.max(1, Number(next.revision || 1)) + 1;
    next.updated_at = timestamp;
    return Object.freeze(next);
  }

  function resume(job, { now = "" } = {}) {
    const next = mutable(job);
    const timestamp = nowValue(now);
    if (next.status !== JOB_STATUSES.PAUSED) return Object.freeze(next);
    next.status = JOB_STATUSES.RUNNING;
    next.stop_reason = null;
    next.revision = Math.max(1, Number(next.revision || 1)) + 1;
    next.updated_at = timestamp;
    settleJob(next, timestamp);
    return Object.freeze(next);
  }

  function cancel(job, { reason = "CANCELLED", now = "" } = {}) {
    const next = mutable(job);
    const timestamp = nowValue(now);
    if ([JOB_STATUSES.CANCELLED, JOB_STATUSES.COMPLETED].includes(next.status)) return Object.freeze(next);
    for (const item of next.items) {
      if (item.status === ITEM_STATUSES.PENDING || item.status === ITEM_STATUSES.CLAIMED) {
        item.status = ITEM_STATUSES.CANCELLED;
        item.completed_at = timestamp;
        item.updated_at = timestamp;
        if (next.active_item_id === item.item_id) next.active_item_id = null;
      }
    }
    next.cancel_reason = String(reason || "CANCELLED").slice(0, 240);
    next.status = next.items.some((item) => item.status === ITEM_STATUSES.REQUEST_STARTED)
      ? JOB_STATUSES.CANCELLING
      : JOB_STATUSES.CANCELLED;
    if (next.status === JOB_STATUSES.CANCELLED) next.completed_at = timestamp;
    next.revision = Math.max(1, Number(next.revision || 1)) + 1;
    next.updated_at = timestamp;
    return Object.freeze(next);
  }

  function recover(job, { workerSessionId = "", now = "" } = {}) {
    const next = mutable(job);
    const timestamp = nowValue(now);
    const session = String(workerSessionId || "");

    for (const item of next.items) {
      if (item.status === ITEM_STATUSES.CLAIMED) {
        if (!session || item.claimed_by !== session) {
          item.status = next.status === JOB_STATUSES.CANCELLING ? ITEM_STATUSES.CANCELLED : ITEM_STATUSES.PENDING;
          if (item.status === ITEM_STATUSES.CANCELLED) item.completed_at = timestamp;
          item.claimed_by = null;
          item.claimed_at = null;
          item.updated_at = timestamp;
          if (next.active_item_id === item.item_id) next.active_item_id = null;
        }
      } else if (item.status === ITEM_STATUSES.REQUEST_STARTED) {
        const requestSession = String(item.request_worker_session_id || "");
        if (requestSession && session && requestSession !== session) {
          item.status = ITEM_STATUSES.OUTCOME_UNKNOWN;
          item.outcome_unknown_reason = "REQUEST_OUTCOME_UNKNOWN_NO_RETRY";
          item.automatic_retry = false;
          item.completed_at = timestamp;
          item.updated_at = timestamp;
          next.stop_reason = "OUTCOME_UNKNOWN_REQUIRES_RECONCILIATION";
          if (next.active_item_id === item.item_id) next.active_item_id = null;
        }
      }
    }

    next.revision = Math.max(1, Number(next.revision || 1)) + 1;
    next.updated_at = timestamp;
    settleJob(next, timestamp);
    return Object.freeze(next);
  }

  function progress(job) {
    const source = mutable(job);
    const counts = countStatuses(source);
    const pending = counts[ITEM_STATUSES.PENDING] || 0;
    const claimed = counts[ITEM_STATUSES.CLAIMED] || 0;
    const requesting = counts[ITEM_STATUSES.REQUEST_STARTED] || 0;
    const succeeded = counts[ITEM_STATUSES.SUCCEEDED] || 0;
    const failedTerminal = counts[ITEM_STATUSES.FAILED_TERMINAL] || 0;
    const outcomeUnknown = counts[ITEM_STATUSES.OUTCOME_UNKNOWN] || 0;
    const skipped = counts[ITEM_STATUSES.SKIPPED] || 0;
    const cancelled = counts[ITEM_STATUSES.CANCELLED] || 0;
    const terminal = source.items.filter((item) => TERMINAL_ITEM_STATUSES.has(item.status)).length;

    let nextSafeAction = "CLAIM_NEXT";
    if (source.status === JOB_STATUSES.PAUSED) nextSafeAction = "RESUME_OR_CANCEL";
    else if (source.status === JOB_STATUSES.CANCELLING) nextSafeAction = "WAIT_FOR_INFLIGHT_OUTCOME";
    else if (source.status === JOB_STATUSES.CANCELLED || source.status === JOB_STATUSES.COMPLETED) nextSafeAction = "NONE";
    else if (outcomeUnknown > 0 && claimed === 0 && requesting === 0) nextSafeAction = "RECONCILE_UNKNOWN";
    else if (claimed > 0 || requesting > 0) nextSafeAction = "WAIT_FOR_ACTIVE_ITEM";
    else if (pending === 0) nextSafeAction = "NONE";

    return Object.freeze({
      job_id: source.job_id,
      status: source.status,
      total: source.items.length,
      input_count: source.input_count,
      duplicate_count: source.duplicate_count,
      pending,
      claimed,
      requesting,
      succeeded,
      failed_terminal: failedTerminal,
      outcome_unknown: outcomeUnknown,
      skipped,
      cancelled,
      terminal,
      requests_started: Math.max(0, Number(source.totals?.requests_started || 0)),
      estimated_cost_rub: Math.max(0, Number(source.totals?.estimated_cost_rub || 0)),
      active_item_id: source.active_item_id || null,
      stop_reason: source.stop_reason || null,
      next_safe_action: nextSafeAction
    });
  }

  globalThis.YMBProviderBatchJobModel = Object.freeze({
    ITEM_STATUSES,
    JOB_STATUSES,
    canonicalize,
    commandFingerprint,
    createJob,
    budgetDecision,
    claimNext,
    markRequestStarted,
    markSucceeded,
    markFailedTerminal,
    markOutcomeUnknown,
    skip,
    pause,
    resume,
    cancel,
    recover,
    progress
  });
})();
