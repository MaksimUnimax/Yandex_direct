/* Deferred Search is a separate orchestration protocol; sync/GenSearch unchanged. */
(() => {
  "use strict";
  const PREFIX = "SEARCH_ASYNC_BATCH_API_V1";
  const SUBMIT_URL = "https://searchapi.api.cloud.yandex.net/v2/web/searchAsync";
  const OPERATIONS_URL = "https://operation.api.cloud.yandex.net/operations/";
  const MAX_ITEMS = 1500;
  const MAX_SLICE = 25;
  const MIN_FIRST_POLL_MS = 5 * 60 * 1000;
  const KEYS = ["searchType", "region", "page", "groupsOnPage", "docsInGroup", "groupMode", "familyMode", "fixTypoMode", "sortMode", "sortOrder", "l10n", "maxPassages"];
  const ACTIONS = new Set(["start", "submit", "submitN", "collect", "collectN", "collectReady", "status", "itemsPage", "pause", "resume", "cancelPending", "exportPage", "normalizeSaved"]);
  const fail = code => { throw Object.assign(new Error(code), { code }); };
  function record(v) { if (!v || typeof v !== "object" || Array.isArray(v)) fail("ASYNC_OBJECT_REQUIRED"); return v; }
  function fields(raw, permitted) { for (const k of Object.keys(raw)) if (!permitted.includes(k)) fail("ASYNC_FIELD_FORBIDDEN"); }
  function integer(v, low, high) { if (!Number.isSafeInteger(v) || v < low || v > high) fail("ASYNC_INTEGER_INVALID"); return v; }
  function id(v) { if (typeof v !== "string" || !/^[A-Za-z0-9_-]{1,128}$/.test(v)) fail("ASYNC_ID_INVALID"); return v; }
  function operationId(v) { if (typeof v !== "string" || !/^[A-Za-z0-9_-]{1,240}$/.test(v)) fail("ASYNC_OPERATION_ID_INVALID"); return v; }
  function base() { if (!globalThis.SearchProtocol?.normalizeCommand || !globalThis.SearchProtocol?.buildRequest) fail("SYNC_SEARCH_PROTOCOL_MISSING"); return globalThis.SearchProtocol; }
  function normalizeCommand(raw) {
    record(raw); if (!ACTIONS.has(raw.action)) fail("ASYNC_ACTION_INVALID");
    const action = raw.action, jobId = id(raw.jobId);
    if (action === "start") {
      fields(raw, ["action", "jobId", "queries", "confirmBillable", "maxRequests", "maxCostRub", ...KEYS]);
      if (raw.confirmBillable !== true) fail("ASYNC_CONFIRM_REQUIRED");
      if (!Array.isArray(raw.queries) || !raw.queries.length || raw.queries.length > MAX_ITEMS) fail("ASYNC_JOB_SIZE_INVALID");
      integer(raw.maxRequests, raw.queries.length, MAX_ITEMS);
      if (typeof raw.maxCostRub !== "number" || !Number.isFinite(raw.maxCostRub) || raw.maxCostRub <= 0 || !Number.isSafeInteger(Math.round(raw.maxCostRub * 1e6))) fail("ASYNC_COST_LIMIT_INVALID");
      const params = Object.fromEntries(KEYS.filter(k => raw[k] !== undefined).map(k => [k, raw[k]]));
      const commands = raw.queries.map(queryText => base().normalizeCommand({ ...params, method: "search", queryText }));
      const queries = commands.map(c => c.queryText);
      if (new Set(queries).size !== queries.length) fail("ASYNC_DUPLICATE_QUERY");
      const parameters = Object.fromEntries(KEYS.filter(k => commands[0][k] !== undefined).map(k => [k, commands[0][k]]));
      return Object.freeze({ action, jobId, queries: Object.freeze(queries), parameters: Object.freeze(parameters), maxRequests: raw.maxRequests, maxCostMicrorub: Math.round(raw.maxCostRub * 1e6), confirmBillable: true });
    }
    if (["submit", "submitN", "collect", "collectN", "collectReady"].includes(action)) {
      fields(raw, ["action", "jobId", "count"]);
      const single = ["submit", "collect"].includes(action);
      const count = integer(raw.count ?? (single ? 1 : MAX_SLICE), 1, single ? 1 : MAX_SLICE);
      return Object.freeze({ action: action.startsWith("submit") ? "submitN" : "collectN", jobId, count });
    }
    if (action === "normalizeSaved") {
      fields(raw, ["action", "jobId", "index"]);
      return Object.freeze({ action, jobId, index: integer(raw.index, 0, MAX_ITEMS - 1) });
    }
    if (action === "exportPage") {
      fields(raw, ["action", "jobId", "after", "limit", "revision"]);
      const after = integer(raw.after ?? -1, -1, MAX_ITEMS - 1);
      const revision = raw.revision == null ? null : integer(raw.revision, 0, Number.MAX_SAFE_INTEGER);
      if (after >= 0 && revision === null) fail("EXPORT_REVISION_REQUIRED");
      return Object.freeze({ action, jobId, after, revision, limit: integer(raw.limit ?? 25, 1, 25) });
    }
    if (action === "itemsPage") {
      fields(raw, ["action", "jobId", "after", "limit"]);
      return Object.freeze({ action, jobId, after: integer(raw.after ?? -1, -1, MAX_ITEMS - 1), limit: integer(raw.limit ?? 100, 1, 100) });
    }
    fields(raw, ["action", "jobId"]);
    return Object.freeze({ action, jobId });
  }
  function parseCommand(input) {
    const str = String(input || "").trim();
    if (!str.startsWith(PREFIX)) fail("ASYNC_PREFIX_REQUIRED");
    const remainder = str.slice(PREFIX.length).trim();
    let raw; try { raw = JSON.parse(remainder); } catch { fail("ASYNC_JSON_INVALID"); }
    return normalizeCommand(raw);
  }
  function buildSubmitRequest(query, parameters, folderId) {
    record(parameters); fields(parameters, KEYS);
    const { body } = base().buildRequest({ ...parameters, method: "search", queryText: query }, folderId);
    return Object.freeze({ url: SUBMIT_URL, method: "POST", body });
  }
  function buildGetRequest(value) {
    return Object.freeze({ url: OPERATIONS_URL + encodeURIComponent(operationId(value)), method: "GET" });
  }
  function parseOperation(value, expectedId = null) {
    const op = record(typeof value === "string" ? JSON.parse(value) : value);
    const opId = operationId(op.id);
    if (expectedId !== null && opId !== operationId(expectedId)) fail("ASYNC_OPERATION_ID_MISMATCH");
    if (typeof op.done !== "boolean") fail("ASYNC_DONE_INVALID");
    const hasError = Object.hasOwn(op, "error"), hasResponse = Object.hasOwn(op, "response");
    if (hasError && hasResponse) fail("ASYNC_OPERATION_AMBIGUOUS");
    const common = { operation_id: opId, done: op.done, created_at: typeof op.createdAt === "string" ? op.createdAt : null, modified_at: typeof op.modifiedAt === "string" ? op.modifiedAt : null };
    if (hasError) {
      const error = record(op.error);
      if (!Number.isInteger(error.code) || error.code < 0) fail("ASYNC_PROVIDER_ERROR_INVALID");
      return Object.freeze({ ...common, outcome: "provider_error", error_code: error.code, error_message: String(error.message || "").slice(0, 800) });
    }
    if (!op.done) { if (hasResponse) fail("ASYNC_PREMATURE_RESPONSE"); return Object.freeze({ ...common, outcome: "waiting" }); }
    if (!hasResponse) fail("ASYNC_COMPLETED_RESPONSE_MISSING");
    const response = record(op.response);
    if (typeof response.rawData !== "string" || !response.rawData.length) fail("ASYNC_RAW_DATA_MISSING");
    // rawData remains the original string; normalization/storage is a separate step.
    return Object.freeze({ ...common, outcome: "received", rawData: response.rawData });
  }
  globalThis.SearchAsyncProtocol = Object.freeze({
    PREFIX, SUBMIT_URL, OPERATIONS_URL, MAX_ITEMS, MAX_SLICE, MIN_FIRST_POLL_MS,
    normalizeCommand, parseCommand, buildSubmitRequest, buildGetRequest, parseOperation
  });
})();
