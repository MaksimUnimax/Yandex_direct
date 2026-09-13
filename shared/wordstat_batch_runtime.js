(() => {
  "use strict";

  const STORAGE_KEY = "ymb_wordstat_batch_jobs_v1";

  function fail(code, message) {
    const error = new Error(message || code);
    error.code = code;
    throw error;
  }

  function clone(value) {
    return value == null ? value : JSON.parse(JSON.stringify(value));
  }

  function defaultUid() {
    const random = globalThis.crypto?.randomUUID?.() || Math.random().toString(36).slice(2);
    return `wordstat-batch-${random}`;
  }

  function defaultNow() {
    return new Date().toISOString();
  }

  function defaultStorage() {
    const local = globalThis.chrome?.storage?.local;
    if (!local) fail("BATCH_STORAGE_UNAVAILABLE", "Chrome storage недоступен для Wordstat batch runtime.");
    return {
      async get(key) {
        const data = await local.get(key);
        return clone(data?.[key]);
      },
      async set(key, value) {
        await local.set({ [key]: clone(value) });
      }
    };
  }

  function providerError(result) {
    const envelope = result?.report_envelope || {};
    const payload = envelope?.result?.error || result?.error || {};
    return {
      code: String(envelope.reason || payload.code || result?.code || `HTTP_${Number(result?.http_status || envelope?.http_status || 0) || 0}`).slice(0, 160),
      message: String(payload.message || result?.error || envelope.reason || "Wordstat provider returned a terminal error.").slice(0, 2000)
    };
  }

  function create(deps = {}) {
    const Model = deps.model || globalThis.YMBProviderBatchJobModel;
    const Protocol = deps.protocol || globalThis.WordstatBatchProtocol;
    if (!Model || !Protocol) fail("BATCH_RUNTIME_PREREQUISITE_MISSING", "Wordstat batch model/protocol недоступны.");

    const storage = deps.storage || defaultStorage();
    const executeWordstat = deps.executeWordstat;
    if (typeof executeWordstat !== "function") fail("BATCH_EXECUTOR_REQUIRED", "Wordstat batch executor обязателен.");
    const estimateCostRub = typeof deps.estimateCostRub === "function" ? deps.estimateCostRub : (() => 0);
    const admit = typeof deps.admit === "function"
      ? deps.admit
      : async ({ estimated_cost_rub: estimatedCostRub }) => ({ allow: true, reason: "ALLOW", estimated_cost_rub: estimatedCostRub });
    const workerSessionId = String(deps.workerSessionId || `batch-worker-${globalThis.crypto?.randomUUID?.() || Math.random().toString(36).slice(2)}`);
    const now = typeof deps.now === "function" ? deps.now : defaultNow;
    const uid = typeof deps.uid === "function" ? deps.uid : defaultUid;

    async function loadMap() {
      const value = await storage.get(STORAGE_KEY);
      return value && typeof value === "object" && !Array.isArray(value) ? clone(value) : {};
    }

    async function saveMap(map) {
      await storage.set(STORAGE_KEY, clone(map));
      return map;
    }

    async function loadJob(jobId) {
      const id = String(jobId || "").trim();
      const map = await loadMap();
      const job = map[id];
      if (!job) fail("BATCH_JOB_NOT_FOUND", `Wordstat batch job не найден: ${id || "<empty>"}.`);
      return { map, job: clone(job) };
    }

    async function persistJob(map, job) {
      map[job.job_id] = clone(job);
      await saveMap(map);
      return clone(job);
    }

    function progress(job) {
      return Model.progress(job);
    }

    function withResultPayload(job, itemId, payload) {
      const nextJob = clone(job);
      const current = nextJob.items?.find((candidate) => candidate.item_id === itemId) || null;
      if (current) current.result_payload = clone(payload);
      return nextJob;
    }

    function envelope(command, job, {
      status = "OK",
      reason = null,
      item = null,
      providerResult = null,
      requestExecuted = false,
      automaticRetry = false
    } = {}) {
      return Protocol.buildResultEnvelope({
        command,
        jobId: job?.job_id || command?.jobId || null,
        status,
        reason,
        progress: job ? progress(job) : null,
        item: item ? clone(item) : null,
        providerResult: providerResult ? clone(providerResult) : null,
        requestExecuted,
        automaticRetry,
        costEstimate: job ? {
          estimated_rub: Number(job.totals?.estimated_cost_rub || 0),
          max_rub: job.limits?.max_cost_rub ?? null
        } : null,
        policy: job ? {
          max_requests: job.limits?.max_requests ?? null,
          max_cost_rub: job.limits?.max_cost_rub ?? null
        } : null
      });
    }

    async function start(command) {
      const jobId = String(command.jobId || uid()).trim();
      if (!jobId) fail("BATCH_JOB_ID_REQUIRED", "Не удалось сформировать jobId.");
      const map = await loadMap();
      if (map[jobId]) fail("BATCH_JOB_ALREADY_EXISTS", `Wordstat batch job уже существует: ${jobId}.`);
      const commands = command.phrases.map((phrase) => ({
        method: "getTop",
        phrase,
        numPhrases: command.numPhrases,
        regions: [...command.regions],
        devices: [...command.devices]
      }));
      const job = Model.createJob({
        jobId,
        service: "wordstat",
        commands,
        limits: { maxRequests: command.maxRequests, maxCostRub: command.maxCostRub },
        now: now()
      });
      await persistJob(map, job);
      return { job, envelope: envelope(command, job) };
    }

    async function status(command) {
      const { job } = await loadJob(command.jobId);
      return { job, envelope: envelope(command, job) };
    }

    async function pause(command) {
      const { map, job } = await loadJob(command.jobId);
      const nextJob = Model.pause(job, { reason: "OWNER_PAUSE", now: now() });
      await persistJob(map, nextJob);
      return { job: nextJob, envelope: envelope(command, nextJob) };
    }

    async function resume(command) {
      const { map, job } = await loadJob(command.jobId);
      const nextJob = Model.resume(job, { now: now() });
      await persistJob(map, nextJob);
      return { job: nextJob, envelope: envelope(command, nextJob) };
    }

    async function cancel(command) {
      const { map, job } = await loadJob(command.jobId);
      const nextJob = Model.cancel(job, { reason: "OWNER_CANCEL", now: now() });
      await persistJob(map, nextJob);
      return { job: nextJob, envelope: envelope(command, nextJob) };
    }

    async function next(command, context = {}) {
      const loaded = await loadJob(command.jobId);
      const map = loaded.map;
      let job = loaded.job;
      const baseEstimatedCostRub = Math.max(0, Number(await estimateCostRub({ method: "getTop" }, clone(job), clone(context)) || 0));
      const admission = await admit({
        command: { method: "getTop" },
        job: clone(job),
        context: clone(context),
        estimated_cost_rub: baseEstimatedCostRub
      });
      const allowed = admission?.allow !== false;
      const admissionReason = String(admission?.reason || (allowed ? "ALLOW" : "BATCH_ADMISSION_DENIED"));
      const estimatedCostRub = Math.max(0, Number(admission?.estimated_cost_rub ?? baseEstimatedCostRub) || 0);
      if (!allowed) {
        return {
          job,
          envelope: envelope(command, job, {
            status: "SKIPPED",
            reason: admissionReason,
            requestExecuted: false,
            automaticRetry: false
          })
        };
      }

      const claimed = Model.claimNext(job, {
        actorId: workerSessionId,
        nextEstimatedCostRub: estimatedCostRub,
        now: now()
      });
      job = claimed.job;
      await persistJob(map, job);

      if (!claimed.item) {
        return {
          job,
          envelope: envelope(command, job, { reason: claimed.reason || null, requestExecuted: false, automaticRetry: false })
        };
      }

      const item = claimed.item;
      const requestId = String(uid()).trim();
      if (!requestId) fail("BATCH_REQUEST_ID_REQUIRED", "Не удалось сформировать requestId.");

      job = Model.markRequestStarted(job, item.item_id, {
        requestId,
        workerSessionId,
        estimatedCostRub,
        now: now()
      });
      await persistJob(map, job);

      let providerResult = null;
      let requestExecuted = true;
      try {
        const result = await executeWordstat(item.command, {
          ...clone(context),
          request_id: requestId,
          job_id: job.job_id,
          batch_item_id: item.item_id,
          batch_worker_session_id: workerSessionId
        });
        providerResult = result?.report_envelope || result || null;
        if (result?.ok === false) {
          const error = providerError(result);
          job = Model.markFailedTerminal(job, item.item_id, {
            code: error.code,
            message: error.message,
            requestExecuted: result?.request_executed !== false,
            now: now()
          });
          requestExecuted = result?.request_executed ?? true;
        } else {
          job = Model.markSucceeded(job, item.item_id, {
            resultRef: String(result?.request_id || requestId),
            requestExecuted: result?.request_executed !== false,
            now: now()
          });
          requestExecuted = result?.request_executed ?? true;
        }
      } catch (error) {
        requestExecuted = error?.request_executed ?? "UNKNOWN";
        providerResult = {
          status: "ERROR",
          reason: error?.code || "PROVIDER_ERROR",
          request_executed: requestExecuted,
          automatic_retry: false,
          error: { code: error?.code || "PROVIDER_ERROR", message: error?.message || String(error) }
        };
        if (requestExecuted === "UNKNOWN") {
          job = Model.markOutcomeUnknown(job, item.item_id, {
            reason: error?.code || "REQUEST_OUTCOME_UNKNOWN_NO_RETRY",
            now: now()
          });
        } else {
          job = Model.markFailedTerminal(job, item.item_id, {
            code: error?.code || "PROVIDER_ERROR",
            message: error?.message || String(error),
            requestExecuted: requestExecuted === true,
            now: now()
          });
        }
      }

      job = withResultPayload(job, item.item_id, providerResult);
      await persistJob(map, job);
      const currentItem = job.items.find((candidate) => candidate.item_id === item.item_id) || item;
      return {
        job,
        envelope: envelope(command, job, {
          status: currentItem.status === Model.ITEM_STATUSES.SUCCEEDED ? "OK" : "ERROR",
          reason: currentItem.error?.code || currentItem.outcome_unknown_reason || null,
          item: currentItem,
          providerResult,
          requestExecuted,
          automaticRetry: false
        })
      };
    }

    async function handle(rawCommand, context = {}) {
      const command = Protocol.normalizeCommand(rawCommand);
      if (command.action === "start") return start(command);
      if (command.action === "status") return status(command);
      if (command.action === "pause") return pause(command);
      if (command.action === "resume") return resume(command);
      if (command.action === "cancel") return cancel(command);
      if (command.action === "next") return next(command, context);
      fail("UNSUPPORTED_BATCH_ACTION", `Batch action ${command.action} не поддерживается.`);
    }

    async function recoverAll() {
      const map = await loadMap();
      const recovered = [];
      let changed = false;
      for (const [jobId, rawJob] of Object.entries(map)) {
        const before = JSON.stringify(rawJob);
        const job = Model.recover(rawJob, { workerSessionId, now: now() });
        map[jobId] = clone(job);
        if (JSON.stringify(job) !== before) changed = true;
        recovered.push({ job: clone(job), progress: progress(job) });
      }
      if (changed) await saveMap(map);
      return recovered;
    }

    return Object.freeze({
      STORAGE_KEY,
      workerSessionId,
      handle,
      recoverAll,
      loadJob: async (jobId) => (await loadJob(jobId)).job
    });
  }

  globalThis.YMBWordstatBatchRuntime = Object.freeze({ STORAGE_KEY, create });
})();
