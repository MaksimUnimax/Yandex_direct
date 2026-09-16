/* B8: bounded local JSON export through the UNCHANGED Patch A artifact store.
 * A page is materialized, not the whole job. No fetch, normalization or source writes.
 * Revisions fence every page; a later mutation requires a new export sequence.
 */
(() => {
  "use strict";
  const SCHEMA = "YMB_SEARCH_ASYNC_EXPORT_PAGE_V1";
  const MAX_ITEMS = 25, MAX_PAGE_BYTES = 16 * 1024 * 1024;
  const JOB_STATES = Object.freeze(["PENDING", "SUBMITTING", "WAITING", "COLLECTING", "RESULT_SAVED", "SUCCEEDED", "PARSE_FAILED", "FAILED", "UNKNOWN", "CANCELLED"]);
  const DB_NAME = "ymb_search_async_items_v2";
  const fail = code => { throw Object.assign(new Error(code), { code, request_executed: false }); };
  const id = v => { if (typeof v !== "string" || !/^[A-Za-z0-9_-]{1,128}$/.test(v)) fail("EXPORT_ID_INVALID"); return v; };
  const uint = v => { if (!Number.isSafeInteger(v) || v < 0) fail("EXPORT_INTEGER_INVALID"); return v; };

  // Cross-chat recovery is deliberately metadata-only. Opening a missing DB is
  // aborted during upgrade so this read path cannot create durable state.
  async function readCrossOwnerJob({ jobId }) {
    id(jobId);
    if (typeof indexedDB === "undefined" || typeof indexedDB.open !== "function") fail("EXPORT_CROSS_OWNER_METADATA_UNAVAILABLE");
    let abortedMissing = false;
    const db = await new Promise((resolve, reject) => {
      const r = indexedDB.open(DB_NAME);
      r.onupgradeneeded = () => {
        abortedMissing = true;
        try { r.transaction.abort(); } catch {}
      };
      r.onsuccess = () => resolve(r.result);
      r.onerror = () => reject(Object.assign(new Error(abortedMissing ? "EXPORT_CROSS_OWNER_METADATA_UNAVAILABLE" : "EXPORT_CROSS_OWNER_METADATA_READ_FAILED"), {
        code: abortedMissing ? "EXPORT_CROSS_OWNER_METADATA_UNAVAILABLE" : "EXPORT_CROSS_OWNER_METADATA_READ_FAILED",
        request_executed: false
      }));
      r.onblocked = () => reject(Object.assign(new Error("EXPORT_CROSS_OWNER_METADATA_READ_FAILED"), {
        code: "EXPORT_CROSS_OWNER_METADATA_READ_FAILED", request_executed: false
      }));
    });
    try {
      if (!db.objectStoreNames.contains("jobs")) fail("EXPORT_CROSS_OWNER_METADATA_UNAVAILABLE");
      return await new Promise((resolve, reject) => {
        const tx = db.transaction(["jobs"], "readonly");
        const r = tx.objectStore("jobs").get(jobId);
        let value;
        r.onsuccess = () => { value = r.result || null; };
        r.onerror = () => reject(Object.assign(new Error("EXPORT_CROSS_OWNER_METADATA_READ_FAILED"), {
          code: "EXPORT_CROSS_OWNER_METADATA_READ_FAILED", request_executed: false
        }));
        tx.oncomplete = () => resolve(value);
        tx.onabort = () => reject(Object.assign(new Error("EXPORT_CROSS_OWNER_METADATA_READ_FAILED"), {
          code: "EXPORT_CROSS_OWNER_METADATA_READ_FAILED", request_executed: false
        }));
        tx.onerror = () => {};
      });
    } finally { db.close(); }
  }

  function terminalReadOwner(job, { jobId, owner, folderId, revision }) {
    if (!job) fail("ASYNC_JOB_NOT_FOUND");
    if (job.job_id !== jobId) fail("EXPORT_CROSS_OWNER_IDENTITY_MISMATCH");
    if (typeof job.owner !== "string" || !job.owner || job.owner === owner) fail("EXPORT_CROSS_OWNER_IDENTITY_MISMATCH");
    if (job.folder_id !== folderId) fail("EXPORT_FOLDER_MISMATCH");
    if (revision === null || job.revision !== revision) fail(revision === null ? "EXPORT_CROSS_OWNER_REVISION_REQUIRED" : "EXPORT_REVISION_CHANGED");
    if (!Number.isSafeInteger(job.total) || job.total < 1 || job.total > 1500 || !job.counts || typeof job.counts !== "object") fail("EXPORT_SNAPSHOT_INVALID");
    let total = 0;
    for (const state of JOB_STATES) {
      const count = job.counts[state];
      if (!Number.isSafeInteger(count) || count < 0) fail("EXPORT_SNAPSHOT_INVALID");
      total += count;
    }
    if (total !== job.total || job.counts.SUCCEEDED !== job.total || JOB_STATES.some(state => state !== "SUCCEEDED" && job.counts[state] !== 0)) {
      fail("EXPORT_CROSS_OWNER_NOT_TERMINAL");
    }
    if (job.lease) fail("EXPORT_JOB_BUSY");
    return job.owner;
  }

  // Exact UTF-8 JSON size for the supported plain-data domain. Stops BEFORE
  // stringify/encoding a record that would exceed the remaining page budget.
  function jsonBytes(value, budget) {
    uint(budget);
    let bytes = 0, nodes = 0;
    const active = new Set();
    const add = n => { bytes += n; if (bytes > budget) fail("EXPORT_BYTE_LIMIT"); };
    const string = s => {
      add(2);
      for (let i = 0; i < s.length; i++) {
        const c = s.charCodeAt(i);
        if (c === 34 || c === 92) add(2);
        else if (c < 32) add([8, 9, 10, 12, 13].includes(c) ? 2 : 6);
        else if (c < 128) add(1);
        else if (c < 2048) add(2);
        else if (c >= 0xD800 && c <= 0xDBFF) {
          const next = s.charCodeAt(i + 1);
          if (next >= 0xDC00 && next <= 0xDFFF) { add(4); i++; } else add(6);
        } else if (c >= 0xDC00 && c <= 0xDFFF) add(6);
        else add(3);
      }
    };
    const visit = (v, depth) => {
      if (++nodes > 200000 || depth > 32) fail("EXPORT_COMPLEXITY_LIMIT");
      if (v === null) { add(4); return; }
      if (typeof v === "string") { string(v); return; }
      if (typeof v === "boolean") { add(v ? 4 : 5); return; }
      if (typeof v === "number" && Number.isFinite(v)) { add(JSON.stringify(v).length); return; }
      if (!v || typeof v !== "object" || active.has(v)) fail("EXPORT_DATA_INVALID");
      const proto = Object.getPrototypeOf(v);
      if (!Array.isArray(v) && proto !== null && Object.getPrototypeOf(proto) !== null) fail("EXPORT_DATA_INVALID");
      if ("toJSON" in v) fail("EXPORT_DATA_INVALID");
      active.add(v); add(2);
      if (Array.isArray(v)) {
        for (let i = 0; i < v.length; i++) {
          const d = Object.getOwnPropertyDescriptor(v, String(i));
          if (!d || d.get || d.set) fail("EXPORT_DATA_INVALID");
          if (i) add(1); visit(d.value, depth + 1);
        }
      } else {
        let n = 0;
        for (const key of Object.keys(v)) {
          const d = Object.getOwnPropertyDescriptor(v, key);
          if (!d || d.get || d.set) fail("EXPORT_DATA_INVALID");
          if (d.value === undefined) continue; // JSON object semantics, not array semantics.
          if (n++) add(1); string(key); add(1); visit(d.value, depth + 1);
        }
      }
      active.delete(v);
    };
    visit(value, 0); return bytes;
  }

  function create({ store, artifacts, authorize, now = Date.now, maxPageBytes = MAX_PAGE_BYTES, crossOwnerJobReader = readCrossOwnerJob } = {}) {
    const methods = ["peekNext", "readItem", "readResult", "getSummary"];
    if (!store || methods.some(k => typeof store[k] !== "function") || !artifacts ||
      ["stageTextArtifact", "getMeta", "deleteArtifact"].some(k => typeof artifacts[k] !== "function") ||
      typeof authorize !== "function" || typeof now !== "function" || typeof crossOwnerJobReader !== "function") fail("EXPORT_DEPENDENCY_REQUIRED");
    if (!Number.isSafeInteger(maxPageBytes) || maxPageBytes < 4096 || maxPageBytes > MAX_PAGE_BYTES) fail("EXPORT_BUDGET_INVALID");
    let busy = false;
    async function allowed(args) {
      if (args.signal?.aborted) fail("EXPORT_ABORTED");
      if (await authorize({ jobId: args.jobId, owner: args.owner, action: "exportPage" }) !== true) fail("EXPORT_NOT_AUTHORIZED");
      if (args.signal?.aborted) fail("EXPORT_ABORTED");
    }
    function checkSummary(s, revision, total) {
      if (!s || !Number.isSafeInteger(s.revision) || !Number.isSafeInteger(s.total) || s.total < 1 || s.total > 1500) fail("EXPORT_SNAPSHOT_INVALID");
      if (s.busy || ["SUBMITTING", "COLLECTING"].some(k => s.counts?.[k] > 0)) fail("EXPORT_JOB_BUSY");
      if (revision !== null && s.revision !== revision) fail("EXPORT_REVISION_CHANGED");
      if (total !== undefined && s.total !== total) fail("EXPORT_REVISION_CHANGED");
    }
    function checkCrossOwnerSummary(s, crossOwner) {
      if (crossOwner && (s.all_successful !== true || s.unresolved !== 0 || s.busy === true)) fail("EXPORT_CROSS_OWNER_NOT_TERMINAL");
    }
    async function discard(descriptor) {
      if (descriptor?.artifact_key) await artifacts.deleteArtifact(descriptor.artifact_key);
    }
    async function stagePage(args) {
      if (busy) fail("EXPORT_BUSY");
      busy = true;
      let createdKey = null;
      try {
        const { jobId, owner, deliveryId, folderId, after = -1, limit = MAX_ITEMS, revision = null } = args || {};
        id(jobId); id(deliveryId);
        if (typeof owner !== "string" || !owner || typeof folderId !== "string" || !folderId) fail("EXPORT_CONTEXT_REQUIRED");
        if (!Number.isInteger(after) || after < -1 || after >= 1500 || !Number.isInteger(limit) || limit < 1 || limit > MAX_ITEMS) fail("EXPORT_PAGE_INVALID");
        if (revision !== null) uint(revision);
        if (after >= 0 && revision === null) fail("EXPORT_REVISION_REQUIRED");
        await allowed(args);
        // Same-owner remains the original path. Only ASYNC_WRONG_OWNER may enter
        // the terminal read-only recovery path; every other store error is final.
        let readOwner = owner, snapshot, crossOwner = false;
        try {
          snapshot = await store.peekNext({ jobId, owner, kind: "submit", now: uint(now()) });
        } catch (error) {
          if (error?.code !== "ASYNC_WRONG_OWNER") throw error;
          if (revision === null) fail("EXPORT_CROSS_OWNER_REVISION_REQUIRED");
          const job = await crossOwnerJobReader({ jobId });
          readOwner = terminalReadOwner(job, { jobId, owner, folderId, revision });
          crossOwner = true;
          // Re-authorize the CURRENT conversation after reading only terminal
          // job metadata and before reading any preserved result payload.
          await allowed(args);
          snapshot = await store.peekNext({ jobId, owner: readOwner, kind: "submit", now: uint(now()) });
        }
        checkSummary(snapshot.progress, revision);
        checkCrossOwnerSummary(snapshot.progress, crossOwner);
        if (snapshot.folder_id !== folderId) fail("EXPORT_FOLDER_MISMATCH");
        const s = snapshot.progress, frozenRevision = s.revision, total = s.total;
        if (after >= total) fail("EXPORT_PAGE_INVALID");
        const header = { schema: SCHEMA, job_id: jobId, revision: frozenRevision, total_items: total,
          folder_id: folderId, parameters: snapshot.parameters, job_summary: s, after };
        jsonBytes(header, 32768);
        const head = JSON.stringify(header).slice(0, -1) + ',"items":[';
        let used = jsonBytes(header, 32768) - 1 + 10;
        const parts = [head];
        let end = after, rows = 0, resultRows = 0, withRaw = 0, withNormalized = 0;
        const counts = {};
        for (let index = after + 1; index < total && rows < limit; index++) {
          await allowed(args);
          const item = await store.readItem(jobId, readOwner, index);
          if (!item || item.job_id !== jobId || item.index !== index) fail("EXPORT_ITEM_MISSING_OR_MISMATCHED");
          const result = await store.readResult(jobId, readOwner, index);
          if (result && (result.job_id !== jobId || result.index !== index || result.operation_id !== item.operation_id)) fail("EXPORT_RESULT_IDENTITY_MISMATCH");
          if (["RESULT_SAVED", "PARSE_FAILED", "SUCCEEDED"].includes(item.state) && (!result || typeof result.raw_text !== "string")) fail("EXPORT_RAW_RESULT_MISSING");
          if (item.state === "SUCCEEDED" && (!result?.normalized || !Array.isArray(result.normalized.results))) fail("EXPORT_NORMALIZED_RESULT_MISSING");
          if (result?.normalized && (!Array.isArray(result.normalized.results) || result.normalized.results.length > 300)) fail("EXPORT_NORMALIZED_INVALID");
          const record = { item, result: result || null };
          let size;
          try { size = jsonBytes(record, maxPageBytes - used - 2048 - (rows ? 1 : 0)); }
          catch (error) {
            if (error.code !== "EXPORT_BYTE_LIMIT") throw error;
            if (!rows) fail("EXPORT_SINGLE_RECORD_TOO_LARGE");
            break; // Exact continuation at the first unwritten item; never truncated data.
          }
          if (rows) { parts.push(","); used++; }
          parts.push(JSON.stringify(record)); used += size;
          rows++; end = index; counts[item.state] = (counts[item.state] || 0) + 1;
          if (typeof result?.raw_text === "string") withRaw++;
          if (result?.normalized) { withNormalized++; resultRows += result.normalized.results.length; }
        }
        const selection = { item_count: rows, result_row_count: resultRows, items_with_raw: withRaw,
          items_with_normalized: withNormalized, states: counts, next_after: end,
          has_more: end + 1 < total, all_job_items_in_this_file: after === -1 && rows === total };
        const tail = '],"page":' + JSON.stringify(selection) + '}\n';
        // ASCII JSON keys/counts here; do not infer bytes from arbitrary Unicode length.
        const tailBytes = 11 + jsonBytes(selection, 2000);
        if (used + tailBytes > maxPageBytes) fail("EXPORT_BYTE_LIMIT");
        parts.push(tail);
        const filename = `search-${jobId}-r${frozenRevision}-${after + 1}-${end}.json`;
        const key = `async-export:${deliveryId}`;
        if (await artifacts.getMeta(key)) fail("EXPORT_DELIVERY_ALREADY_STAGED");
        await allowed(args);
        const beforeStage = await store.getSummary(jobId, readOwner);
        checkSummary(beforeStage, frozenRevision, total);
        checkCrossOwnerSummary(beforeStage, crossOwner);
        let text = parts.join(""); parts.length = 0;
        const expectedBytes = used + tailBytes;
        createdKey = key; // Covers ambiguous staging completion too.
        const descriptor = await artifacts.stageTextArtifact({ artifactKey: key, deliveryId, filename,
          text, mimeType: "application/json;charset=utf-8" });
        text = null;
        if (!descriptor || descriptor.artifact_key !== key || descriptor.delivery_id !== deliveryId ||
          descriptor.status !== "ready" || descriptor.byte_length !== expectedBytes) fail("EXPORT_ARTIFACT_MISMATCH");
        await allowed(args);
        const afterStage = await store.getSummary(jobId, readOwner);
        checkSummary(afterStage, frozenRevision, total);
        checkCrossOwnerSummary(afterStage, crossOwner);
        createdKey = null;
        return { descriptor, report: { schema: SCHEMA, filename, bytes: descriptor.byte_length,
          integrity: "sha256_per_chunk", revision: frozenRevision, after, ...selection } };
      } catch (error) {
        if (createdKey) {
          try { await artifacts.deleteArtifact(createdKey); }
          catch { fail("EXPORT_CLEANUP_REQUIRED"); }
        }
        throw error;
      } finally { busy = false; }
    }
    return Object.freeze({ stagePage, discard });
  }
  globalThis.YMBSearchAsyncExport = Object.freeze({ create, jsonBytes, SCHEMA, MAX_ITEMS, MAX_PAGE_BYTES });
})();
