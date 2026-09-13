(() => {
  "use strict";

  const PREFIX = "SEARCH_BATCH_API_V1";
  const RESULT_PREFIX = "SEARCH_BATCH_RESULT_V1";
  const ACTIONS = Object.freeze(new Set(["start", "next", "nextN", "status", "pause", "resume", "cancel", "projection", "overlapPage"]));
  const START_FIELDS = new Set(["action", "jobId", "queries", "searchType", "region", "groupsOnPage", "maxRequests", "maxCostRub", "confirmBillable"]);
  const JOB_ONLY_FIELDS = new Set(["action", "jobId"]);
  const NEXT_N_FIELDS = new Set(["action", "jobId", "count"]);
  const PROJECTION_FIELDS = new Set(["action", "jobId", "offset", "limit", "topN", "targetDomains"]);
  const OVERLAP_FIELDS = new Set(["action", "jobId", "offset", "limit", "topN"]);

  function productVersion() { return String(globalThis.YMBProduct?.VERSION || "0.1.2"); }

  function fail(code, message) {
    const error = new Error(message || code);
    error.code = code;
    throw error;
  }

  function Search() {
    const protocol = globalThis.SearchProtocol;
    if (!protocol || typeof protocol.normalizeCommand !== "function") fail("SEARCH_BATCH_SEARCH_PROTOCOL_MISSING", "SearchProtocol недоступен для Search batch.");
    return protocol;
  }

  function validateFields(raw, allowed) {
    for (const key of Object.keys(raw)) {
      if (!allowed.has(key)) fail("UNSUPPORTED_SEARCH_BATCH_FIELD", `Поле ${key} не разрешено для SEARCH_BATCH_API_V1 action ${raw.action || "<empty>"}.`);
    }
  }

  function asString(value, name, { required = false, max = 400 } = {}) {
    if (value === undefined || value === null || value === "") {
      if (required) fail(`MISSING_SEARCH_BATCH_${String(name).replace(/([a-z])([A-Z])/g, "$1_$2").toUpperCase()}`, `${name} обязателен.`);
      return undefined;
    }
    const text = String(value).trim();
    if (required && !text) fail(`MISSING_SEARCH_BATCH_${String(name).replace(/([a-z])([A-Z])/g, "$1_$2").toUpperCase()}`, `${name} обязателен.`);
    if (Array.from(text).length > max) fail("SEARCH_BATCH_FIELD_TOO_LONG", `${name}: максимум ${max} символов.`);
    return text || undefined;
  }

  function integer(value, name, { min = 0, max = Number.MAX_SAFE_INTEGER, fallback, required = false } = {}) {
    if (value === undefined || value === null || value === "") {
      if (required) fail(`MISSING_SEARCH_BATCH_${String(name).replace(/([a-z])([A-Z])/g, "$1_$2").toUpperCase()}`, `${name} обязателен.`);
      return fallback;
    }
    const number = Number(value);
    if (!Number.isSafeInteger(number) || number < min || number > max) fail("INVALID_SEARCH_BATCH_NUMBER", `${name} должен быть целым числом от ${min} до ${max}.`);
    return number;
  }

  function nonNegative(value, name, { max = Number.MAX_SAFE_INTEGER, required = false, fallback } = {}) {
    if (value === undefined || value === null || value === "") {
      if (required) fail(`MISSING_SEARCH_BATCH_${String(name).replace(/([a-z])([A-Z])/g, "$1_$2").toUpperCase()}`, `${name} обязателен.`);
      return fallback;
    }
    const number = Number(value);
    if (!Number.isFinite(number) || number < 0 || number > max) fail("INVALID_SEARCH_BATCH_NUMBER", `${name} должен быть неотрицательным числом.`);
    return number;
  }

  function normalizeDomain(value, index = 0) {
    const domain = String(value ?? "").trim().toLowerCase().replace(/\.$/u, "");
    if (!domain || domain.length > 253 || /\s/u.test(domain)) fail("INVALID_SEARCH_BATCH_TARGET_DOMAIN", `targetDomains[${index}] некорректен.`);
    return domain;
  }

  function baseSearchTemplate(raw, queryText) {
    const source = {
      method: "search",
      queryText,
      searchType: raw.searchType === undefined ? "SEARCH_TYPE_RU" : raw.searchType,
      groupsOnPage: raw.groupsOnPage === undefined ? 10 : raw.groupsOnPage,
      page: 0,
      docsInGroup: 1,
      groupMode: "GROUP_MODE_FLAT",
      sortMode: "SORT_MODE_BY_RELEVANCE",
      sortOrder: "SORT_ORDER_DESC",
      familyMode: "FAMILY_MODE_MODERATE",
      fixTypoMode: "FIX_TYPO_MODE_ON"
    };
    if (raw.region !== undefined) source.region = raw.region;
    return source;
  }

  function normalizeStart(raw) {
    validateFields(raw, START_FIELDS);
    if (raw.confirmBillable !== true) fail("SEARCH_BATCH_CONFIRM_REQUIRED", "Search batch start требует confirmBillable:true для явной авторизации bounded paid job.");
    if (!Array.isArray(raw.queries) || raw.queries.length === 0) fail("INVALID_SEARCH_BATCH_QUERIES", "queries должен быть непустым массивом.");
    if (raw.queries.length > 500) fail("TOO_MANY_SEARCH_BATCH_QUERIES", "queries: максимум 500 значений.");

    const normalizedQueries = raw.queries.map((value, index) => {
      const query = asString(value, `queries[${index}]`, { required: true, max: 400 });
      try { return Search().normalizeCommand(baseSearchTemplate(raw, query)).queryText; }
      catch (error) {
        if (error?.code) throw error;
        fail("INVALID_SEARCH_BATCH_QUERY", `queries[${index}] некорректен.`);
      }
    });
    const uniqueCount = new Set(normalizedQueries).size;
    const maxRequests = integer(raw.maxRequests, "maxRequests", { min: 1, max: 500, required: true });
    if (maxRequests > uniqueCount) fail("SEARCH_BATCH_MAX_REQUESTS_EXCEEDS_QUERIES", `maxRequests ${maxRequests} превышает ${uniqueCount} уникальных запросов.`);
    const maxCostRub = nonNegative(raw.maxCostRub, "maxCostRub", { max: 100000, required: true });
    const jobId = asString(raw.jobId, "jobId", { max: 240 });
    const sample = Search().normalizeCommand(baseSearchTemplate(raw, normalizedQueries[0]));
    return Object.freeze({
      action: "start",
      ...(jobId ? { jobId } : {}),
      queries: Object.freeze(normalizedQueries),
      searchType: sample.searchType,
      ...(sample.region !== undefined ? { region: sample.region } : {}),
      groupsOnPage: sample.groupsOnPage,
      maxRequests,
      maxCostRub,
      confirmBillable: true
    });
  }

  function normalizeJobOnly(raw, action) {
    validateFields(raw, JOB_ONLY_FIELDS);
    return Object.freeze({ action, jobId: asString(raw.jobId, "jobId", { required: true, max: 240 }) });
  }

  function normalizeNextN(raw) {
    validateFields(raw, NEXT_N_FIELDS);
    return Object.freeze({
      action: "nextN",
      jobId: asString(raw.jobId, "jobId", { required: true, max: 240 }),
      count: integer(raw.count, "count", { min: 1, max: 100, required: true })
    });
  }

  function normalizeProjection(raw) {
    validateFields(raw, PROJECTION_FIELDS);
    const domains = raw.targetDomains === undefined ? [] : raw.targetDomains;
    if (!Array.isArray(domains) || domains.length > 20) fail("INVALID_SEARCH_BATCH_TARGET_DOMAINS", "targetDomains должен содержать не более 20 доменов.");
    return Object.freeze({
      action: "projection",
      jobId: asString(raw.jobId, "jobId", { required: true, max: 240 }),
      offset: integer(raw.offset, "offset", { min: 0, max: 1_000_000, fallback: 0 }),
      limit: integer(raw.limit, "limit", { min: 1, max: 100, fallback: 20 }),
      topN: integer(raw.topN, "topN", { min: 1, max: 100, fallback: 10 }),
      targetDomains: Object.freeze(domains.map((domain, index) => normalizeDomain(domain, index)))
    });
  }

  function normalizeOverlap(raw) {
    validateFields(raw, OVERLAP_FIELDS);
    return Object.freeze({
      action: "overlapPage",
      jobId: asString(raw.jobId, "jobId", { required: true, max: 240 }),
      offset: integer(raw.offset, "offset", { min: 0, max: 10_000_000, fallback: 0 }),
      limit: integer(raw.limit, "limit", { min: 1, max: 1000, fallback: 100 }),
      topN: integer(raw.topN, "topN", { min: 1, max: 100, fallback: 10 })
    });
  }

  function normalizeCommand(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) fail("INVALID_SEARCH_BATCH_JSON_ROOT", "Search batch команда должна быть JSON-объектом.");
    const action = String(raw.action || "").trim();
    if (!ACTIONS.has(action)) fail("UNSUPPORTED_SEARCH_BATCH_ACTION", `Search batch action ${action || "<empty>"} не поддерживается.`);
    if (action === "start") return normalizeStart(raw);
    if (action === "nextN") return normalizeNextN(raw);
    if (["next", "status", "pause", "resume", "cancel"].includes(action)) return normalizeJobOnly(raw, action);
    if (action === "projection") return normalizeProjection(raw);
    return normalizeOverlap(raw);
  }

  function parseCommand(text) {
    const source = String(text || "").replace(/\u00a0/g, " ").trim();
    if (!source.startsWith(PREFIX)) fail("NOT_SEARCH_BATCH_COMMAND", `Команда должна начинаться с ${PREFIX}.`);
    const rest = source.slice(PREFIX.length).trim();
    if (!rest) fail("MISSING_SEARCH_BATCH_JSON", `После ${PREFIX} должен идти JSON-объект.`);
    let raw;
    try { raw = JSON.parse(rest); }
    catch (error) { fail("INVALID_SEARCH_BATCH_JSON", `Некорректный JSON: ${error.message}`); }
    return normalizeCommand(raw);
  }

  function buildSearchCommand(startCommand, queryText) {
    const start = normalizeCommand(startCommand);
    if (start.action !== "start") fail("SEARCH_BATCH_START_REQUIRED", "buildSearchCommand требует start manifest.");
    const raw = baseSearchTemplate(start, queryText);
    return Search().normalizeCommand(raw);
  }

  function canonicalize(value) {
    if (value === null) return "null";
    if (Array.isArray(value)) return `[${value.map(canonicalize).join(",")}]`;
    if (typeof value !== "object") return JSON.stringify(value);
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonicalize(value[key])}`).join(",")}}`;
  }

  function commandFingerprint(command) {
    const json = canonicalize(normalizeCommand(command));
    let hash = 2166136261;
    for (let index = 0; index < json.length; index += 1) { hash ^= json.charCodeAt(index); hash = Math.imul(hash, 16777619); }
    return (hash >>> 0).toString(16).padStart(8, "0");
  }

  function buildResultEnvelope({ command, jobId = null, status = "OK", reason = null, progress = null, item = null, providerResult = null, projection = null, chunk = null, requestExecuted = false, automaticRetry = false, costEstimate = null, policy = null, metadata = {} } = {}) {
    const normalized = normalizeCommand(command);
    return Object.freeze({
      bridge: String(globalThis.YMBProduct?.BRIDGE_ID || "yandex-marketing-bridge"),
      version: productVersion(),
      service: "search",
      operation: `batch.${normalized.action}`,
      job_id: String(jobId || normalized.jobId || "").trim() || null,
      run_id: metadata.run_id || null,
      status: String(status || "OK"),
      reason: reason == null ? null : String(reason),
      command: normalized,
      progress: progress || null,
      item: item || null,
      provider_result: providerResult || null,
      projection: projection || null,
      chunk: chunk || null,
      cost_estimate: costEstimate || null,
      policy: policy || null,
      request_executed: requestExecuted,
      automatic_retry: automaticRetry === true
    });
  }

  function formatResultEnvelope(envelope) { return `${RESULT_PREFIX}\n${JSON.stringify(envelope, null, 2)}`; }
  function isCommandText(text) { return String(text || "").replace(/\u00a0/g, " ").trim().startsWith(PREFIX); }

  globalThis.SearchBatchProtocol = Object.freeze({
    PREFIX, RESULT_PREFIX, ACTIONS,
    normalizeCommand, parseCommand, buildSearchCommand, commandFingerprint,
    buildResultEnvelope, formatResultEnvelope, isCommandText
  });
})();
