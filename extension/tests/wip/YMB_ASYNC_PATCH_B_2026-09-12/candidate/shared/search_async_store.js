/* YMB deferred Search: per-item durable state. No provider/network/UI calls. */
(() => {
  "use strict";
  const DB_NAME = "ymb_search_async_items_v2";
  const DB_VERSION = 1;
  const STATES = Object.freeze(["PENDING", "SUBMITTING", "WAITING", "COLLECTING", "RESULT_SAVED", "SUCCEEDED", "PARSE_FAILED", "FAILED", "UNKNOWN", "CANCELLED"]);
  const MAX_ITEMS = 1500;
  const MAX_PAGE = 100;
  const MAX_INDEX = Number.MAX_SAFE_INTEGER;
  const fail = (code) => { throw Object.assign(new Error(code), { code }); };
  const text = (v, max = 240) => {
    if (typeof v !== "string" || !v.length || v.length > max || /[\u0000-\u001f\u007f]/u.test(v)) fail("ASYNC_STORE_INVALID_TEXT");
    return v;
  };
  const uint = (v) => { if (!Number.isSafeInteger(v) || v < 0) fail("ASYNC_STORE_INVALID_INTEGER"); return v; };
  const req = (r) => new Promise((resolve, reject) => {
    r.onsuccess = () => resolve(r.result);
    r.onerror = () => reject(r.error || new Error("ASYNC_IDB_REQUEST_FAILED"));
  });
  function open() {
    return new Promise((resolve, reject) => {
      const r = indexedDB.open(DB_NAME, DB_VERSION);
      r.onupgradeneeded = () => {
        const db = r.result;
        if (!db.objectStoreNames.contains("jobs")) db.createObjectStore("jobs", { keyPath: "job_id" });
        if (!db.objectStoreNames.contains("items")) {
          const s = db.createObjectStore("items", { keyPath: ["job_id", "index"] });
          s.createIndex("state", ["job_id", "state", "index"], { unique: false });
          s.createIndex("due", ["job_id", "state", "next_poll_at", "index"], { unique: false });
          s.createIndex("operation", "operation_id", { unique: true });
        }
        if (!db.objectStoreNames.contains("results")) db.createObjectStore("results", { keyPath: ["job_id", "index"] });
        if (!db.objectStoreNames.contains("attempts")) db.createObjectStore("attempts", { keyPath: ["job_id", "attempt_id"] });
      };
      r.onsuccess = () => { const db = r.result; db.onversionchange = () => db.close(); resolve(db); };
      r.onerror = () => reject(r.error || new Error("ASYNC_IDB_OPEN_FAILED"));
      r.onblocked = () => reject(Object.assign(new Error("ASYNC_IDB_OPEN_BLOCKED"), { code: "ASYNC_IDB_OPEN_BLOCKED" }));
    });
  }
  async function transaction(names, mode, work) {
    const db = await open();
    try {
      return await new Promise((resolve, reject) => {
        const tx = db.transaction(names, mode, mode === "readwrite" ? { durability: "strict" } : undefined);
        let result, failure;
        tx.oncomplete = () => resolve(result);
        tx.onabort = () => reject(failure || tx.error || new Error("ASYNC_IDB_ABORTED"));
        tx.onerror = () => { failure ||= tx.error; };
        // work may await IDB requests only: never network, timers or hashing here.
        Promise.resolve().then(() => work(tx)).then((value) => { result = value; }).catch((error) => {
          failure = error;
          try { tx.abort(); } catch { reject(error); }
        });
      });
    } finally { db.close(); }
  }
  function guard(job, owner) {
    if (!job) fail("ASYNC_JOB_NOT_FOUND");
    if (typeof owner !== "string" || job.owner !== owner) fail("ASYNC_WRONG_OWNER");
  }
  function summary(job) {
    const active = ["PENDING", "SUBMITTING", "WAITING", "COLLECTING", "RESULT_SAVED"].reduce((s, k) => s + job.counts[k], 0);
    return {
      job_id: job.job_id, control: job.control, total: job.total, counts: { ...job.counts },
      requests_started: job.requests_started, operations_accepted: job.operations_accepted,
      polls_started: job.polls_started, reserved_microrub: job.reserved_microrub,
      max_requests: job.max_requests, max_cost_microrub: job.max_cost_microrub,
      all_successful: job.counts.SUCCEEDED === job.total,
      unresolved: active + job.counts.UNKNOWN + job.counts.PARSE_FAILED,
      busy: Boolean(job.lease), revision: job.revision
    };
  }
  function move(job, item, state) {
    if (!STATES.includes(state) || job.counts[item.state] < 1) fail("ASYNC_STATE_ACCOUNTING_INVALID");
    job.counts[item.state]--; job.counts[state]++; item.state = state;
  }
  function save(tx, job, item, now) {
    job.updated_at = uint(now); job.revision++;
    if (item) tx.objectStore("items").put(item);
    tx.objectStore("jobs").put(job);
  }
  async function jobFor(tx, jobId, owner) {
    const job = await req(tx.objectStore("jobs").get(text(jobId)));
    guard(job, owner); return job;
  }
  async function createJob({ jobId, owner, queries, parameters, folderId, maxRequests, maxCostMicrorub, unitCostMicrorub, now }) {
    text(jobId); text(owner, 1000); text(folderId, 50); uint(now); uint(maxRequests); uint(maxCostMicrorub); uint(unitCostMicrorub);
    if (!Array.isArray(queries) || !queries.length || queries.length > MAX_ITEMS) fail("ASYNC_JOB_SIZE_INVALID");
    if (maxRequests < queries.length || !unitCostMicrorub || !Number.isSafeInteger(unitCostMicrorub * maxRequests)) fail("ASYNC_JOB_LIMIT_INVALID");
    for (const q of queries) { text(q, 800); if (Array.from(q).length > 400) fail("ASYNC_QUERY_TOO_LONG"); }
    // parameters is already validated by the protocol. Secrets are never a config field.
    if (!parameters || typeof parameters !== "object" || Array.isArray(parameters)) fail("ASYNC_PARAMETERS_REQUIRED");
    const allowed = new Set(["searchType", "region", "page", "groupsOnPage", "docsInGroup", "groupMode", "familyMode", "fixTypoMode", "sortMode", "sortOrder", "l10n", "maxPassages"]);
    for (const k of Object.keys(parameters)) if (!allowed.has(k)) fail("ASYNC_PARAMETERS_FIELD_FORBIDDEN");
    if (JSON.stringify(parameters).length > 2048) fail("ASYNC_PARAMETERS_TOO_LARGE");
    return transaction(["jobs", "items"], "readwrite", async (tx) => {
      if (await req(tx.objectStore("jobs").get(jobId))) fail("ASYNC_JOB_ALREADY_EXISTS");
      const job = {
        job_id: jobId, owner, folder_id: folderId, parameters, total: queries.length,
        counts: Object.fromEntries(STATES.map((s) => [s, s === "PENDING" ? queries.length : 0])),
        max_requests: maxRequests, max_cost_microrub: maxCostMicrorub, unit_cost_microrub: unitCostMicrorub,
        requests_started: 0, operations_accepted: 0, polls_started: 0, reserved_microrub: 0,
        control: "RUNNING", lease: null, revision: 0, created_at: now, updated_at: now
      };
      tx.objectStore("jobs").add(job);
      queries.forEach((query, index) => tx.objectStore("items").add({
        job_id: jobId, index, query, state: "PENDING", next_poll_at: 0,
        submit_attempt: null, collect_attempt: null, last_settled_attempt: null, poll_count: 0
      }));
      return summary(job);
    });
  }
  async function claim({ jobId, owner, workerId, attemptId, kind, now }) {
    if (!["submit", "collect"].includes(kind)) fail("ASYNC_CLAIM_KIND_INVALID");
    text(workerId); text(attemptId); uint(now);
    return transaction(["jobs", "items", "attempts"], "readwrite", async (tx) => {
      const job = await jobFor(tx, jobId, owner);
      if (await req(tx.objectStore("attempts").get([jobId, attemptId]))) return { allowed: false, reason: "DUPLICATE_ATTEMPT" };
      if (job.lease) return { allowed: false, reason: "ITEM_ACTIVE" };
      if (job.control === "PAUSED") return { allowed: false, reason: "PAUSED" };
      if (kind === "submit") {
        if (job.control === "CANCELLED") return { allowed: false, reason: "CANCELLED" };
        if (job.counts.UNKNOWN) return { allowed: false, reason: "UNKNOWN_SUBMIT_REQUIRES_RECONCILIATION" };
        if (job.requests_started >= job.max_requests || job.unit_cost_microrub > job.max_cost_microrub - job.reserved_microrub) return { allowed: false, reason: "BUDGET_LIMIT" };
      }
      const s = tx.objectStore("items");
      const item = kind === "submit"
        ? await req(s.index("state").get(IDBKeyRange.bound([jobId, "PENDING", 0], [jobId, "PENDING", MAX_INDEX])))
        : await req(s.index("due").get(IDBKeyRange.bound([jobId, "WAITING", 0, 0], [jobId, "WAITING", now, MAX_INDEX])));
      if (!item) return { allowed: false, reason: kind === "submit" ? "NO_PENDING_ITEMS" : "NO_DUE_OPERATIONS" };
      const state = kind === "submit" ? "SUBMITTING" : "COLLECTING";
      move(job, item, state);
      item[`${kind}_attempt`] = attemptId;
      if (kind === "submit") { job.requests_started++; job.reserved_microrub += job.unit_cost_microrub; }
      else { job.polls_started++; item.poll_count++; }
      job.lease = { token: attemptId, worker: workerId, kind, index: item.index, started_at: now };
      tx.objectStore("attempts").add({ job_id: jobId, attempt_id: attemptId, kind, index: item.index, created_at: now });
      save(tx, job, item, now);
      return { allowed: true, item, folder_id: job.folder_id, parameters: job.parameters, progress: summary(job) };
    });
  }
  async function active(tx, args, kind) {
    const job = await jobFor(tx, args.jobId, args.owner);
    const item = await req(tx.objectStore("items").get([args.jobId, uint(args.index)]));
    if (!item) fail("ASYNC_ITEM_NOT_FOUND");
    text(args.attemptId);
    if (item.last_settled_attempt === args.attemptId) return { job, item, duplicate: true };
    if (!job.lease || job.lease.kind !== kind || job.lease.index !== item.index || job.lease.token !== args.attemptId || item[`${kind}_attempt`] !== args.attemptId) fail("ASYNC_STALE_ATTEMPT");
    return { job, item, duplicate: false };
  }
  async function finishSubmit(args) {
    uint(args.now);
    if (!["accepted", "unknown", "rejected"].includes(args.outcome)) fail("ASYNC_SUBMIT_OUTCOME_INVALID");
    if (args.outcome === "accepted") { text(args.operationId); uint(args.nextPollAt); }
    return transaction(["jobs", "items"], "readwrite", async (tx) => {
      const { job, item, duplicate } = await active(tx, args, "submit");
      if (duplicate) return { duplicate: true, progress: summary(job) };
      if (item.state !== "SUBMITTING") fail("ASYNC_ITEM_STATE_INVALID");
      if (args.outcome === "accepted") {
        item.operation_id = args.operationId; item.submitted_at = args.now; item.next_poll_at = args.nextPollAt;
        job.operations_accepted++; move(job, item, "WAITING");
      } else {
        item.error_code = String(args.errorCode || "SUBMIT_OUTCOME_UNKNOWN").slice(0, 120);
        move(job, item, args.outcome === "unknown" ? "UNKNOWN" : "FAILED");
      }
      item.last_settled_attempt = args.attemptId; job.lease = null;
      save(tx, job, item, args.now);
      return { duplicate: false, progress: summary(job) };
    });
  }
  async function finishCollect(args) {
    uint(args.now);
    if (!["waiting", "received", "provider_error", "read_error"].includes(args.outcome)) fail("ASYNC_COLLECT_OUTCOME_INVALID");
    if (["waiting", "read_error"].includes(args.outcome)) uint(args.nextPollAt);
    if (["received", "provider_error"].includes(args.outcome) && typeof args.rawText !== "string") fail("ASYNC_RAW_RESPONSE_REQUIRED");
    return transaction(["jobs", "items", "results"], "readwrite", async (tx) => {
      const { job, item, duplicate } = await active(tx, args, "collect");
      if (duplicate) return { duplicate: true, progress: summary(job) };
      if (item.state !== "COLLECTING" || !item.operation_id) fail("ASYNC_ITEM_STATE_INVALID");
      item.last_polled_at = args.now;
      if (["waiting", "read_error"].includes(args.outcome)) {
        item.next_poll_at = args.nextPollAt;
        item.last_read_error = args.outcome === "read_error" ? String(args.errorCode || "READ_FAILED").slice(0, 120) : null;
        move(job, item, "WAITING");
      } else {
        tx.objectStore("results").put({ job_id: args.jobId, index: args.index, operation_id: item.operation_id, raw_text: args.rawText, received_at: args.now });
        item.result_saved_at = args.now;
        if (args.outcome === "provider_error") item.error_code = String(args.errorCode || "PROVIDER_OPERATION_FAILED").slice(0, 120);
        move(job, item, args.outcome === "received" ? "RESULT_SAVED" : "FAILED");
      }
      item.last_settled_attempt = args.attemptId; job.lease = null;
      save(tx, job, item, args.now);
      return { duplicate: false, progress: summary(job) };
    });
  }
  async function finishNormalization({ jobId, owner, index, normalized, errorCode = null, now }) {
    uint(index); uint(now);
    return transaction(["jobs", "items", "results"], "readwrite", async (tx) => {
      const job = await jobFor(tx, jobId, owner);
      const item = await req(tx.objectStore("items").get([jobId, index]));
      if (!item) fail("ASYNC_ITEM_NOT_FOUND");
      if (item.state === "SUCCEEDED") return summary(job);
      if (!["RESULT_SAVED", "PARSE_FAILED"].includes(item.state)) fail("ASYNC_ITEM_STATE_INVALID");
      const record = await req(tx.objectStore("results").get([jobId, index]));
      if (!record) fail("ASYNC_RAW_RESULT_MISSING");
      if (errorCode) { item.parse_error = String(errorCode).slice(0, 120); move(job, item, "PARSE_FAILED"); }
      else {
        if (!normalized || !Array.isArray(normalized.results) || normalized.results.length > 300) fail("ASYNC_NORMALIZED_INVALID");
        record.normalized = normalized; record.normalized_at = now; tx.objectStore("results").put(record);
        item.parse_error = null; move(job, item, "SUCCEEDED");
      }
      save(tx, job, item, now); return summary(job);
    });
  }
  async function recover({ jobId, owner, workerId, now }) {
    text(workerId); uint(now);
    return transaction(["jobs", "items"], "readwrite", async (tx) => {
      const job = await jobFor(tx, jobId, owner);
      if (!job.lease || job.lease.worker === workerId) return summary(job);
      const item = await req(tx.objectStore("items").get([jobId, job.lease.index]));
      if (!item) fail("ASYNC_RECOVERY_ITEM_MISSING");
      if (item.state === "SUBMITTING") { move(job, item, "UNKNOWN"); item.error_code = "SUBMIT_INTERRUPTED_NO_RETRY"; }
      else if (item.state === "COLLECTING") { move(job, item, "WAITING"); item.next_poll_at = now; }
      else fail("ASYNC_RECOVERY_STATE_INVALID");
      job.lease = null; save(tx, job, item, now); return summary(job);
    });
  }
  async function control({ jobId, owner, action, now }) {
    uint(now);
    if (!["pause", "resume", "cancelPending"].includes(action)) fail("ASYNC_CONTROL_INVALID");
    return transaction(["jobs", "items"], "readwrite", async (tx) => {
      const job = await jobFor(tx, jobId, owner);
      if (action !== "cancelPending" && job.control === "CANCELLED") fail("ASYNC_CANCELLED_NO_RESUME");
      job.control = action === "pause" ? "PAUSED" : action === "resume" ? "RUNNING" : "CANCELLED";
      if (action === "cancelPending") {
        const r = tx.objectStore("items").index("state").openCursor(IDBKeyRange.bound([jobId, "PENDING", 0], [jobId, "PENDING", MAX_INDEX]));
        await new Promise((resolve, reject) => {
          r.onerror = () => reject(r.error);
          r.onsuccess = () => { const c = r.result; if (!c) { resolve(); return; } const item = c.value; move(job, item, "CANCELLED"); c.update(item); c.continue(); };
        });
      }
      save(tx, job, null, now); return summary(job);
    });
  }
  async function getSummary(jobId, owner) {
    return transaction(["jobs"], "readonly", async (tx) => summary(await jobFor(tx, jobId, owner)));
  }
  async function pageItems(jobId, owner, { after = -1, limit = MAX_PAGE } = {}) {
    if (!Number.isInteger(after) || after < -1 || after >= MAX_INDEX || !Number.isInteger(limit) || limit < 1 || limit > MAX_PAGE) fail("ASYNC_PAGE_INVALID");
    return transaction(["jobs", "items"], "readonly", async (tx) => {
      await jobFor(tx, jobId, owner);
      const r = tx.objectStore("items").openCursor(IDBKeyRange.bound([jobId, after + 1], [jobId, MAX_INDEX]));
      const rows = [];
      await new Promise((resolve, reject) => {
        r.onerror = () => reject(r.error);
        r.onsuccess = () => { const c = r.result; if (!c || rows.length === limit) { resolve(); return; } rows.push(c.value); c.continue(); };
      });
      return { rows, next_after: rows.length ? rows[rows.length - 1].index : after };
    });
  }
  async function readResult(jobId, owner, index) {
    uint(index);
    return transaction(["jobs", "results"], "readonly", async (tx) => { await jobFor(tx, jobId, owner); return req(tx.objectStore("results").get([jobId, index])); });
  }
  globalThis.YMBSearchAsyncStore = Object.freeze({
    DB_NAME, DB_VERSION, MAX_ITEMS, MAX_PAGE, STATES,
    createJob, claim, finishSubmit, finishCollect, finishNormalization, recover, control, getSummary, pageItems, readResult
  });
})();
