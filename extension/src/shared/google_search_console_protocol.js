(() => {
  "use strict";

  const PREFIX = "GOOGLE_SEARCH_CONSOLE_API_V1";
  const RESULT_PREFIX = "GOOGLE_SEARCH_CONSOLE_RESULT_V1";
  const BASE_URL = "https://www.googleapis.com/webmasters/v3";
  const METHODS = Object.freeze(["listSites", "searchAnalytics"]);
  const METHOD_SET = new Set(METHODS);
  const DIMENSIONS = new Set(["query", "page", "country", "device", "date"]);
  const FILTER_DIMENSIONS = new Set(["query", "page", "country", "device"]);
  const FILTER_OPERATORS = new Set(["equals", "contains", "notEquals", "notContains"]);
  const DATA_STATES = new Set(["final", "all"]);
  const TYPES = new Set(["web"]);
  const LIST_FIELDS = new Set(["method"]);
  const ANALYTICS_FIELDS = new Set(["method", "siteUrl", "startDate", "endDate", "type", "dimensions", "rowLimit", "startRow", "dataState", "filters"]);

  function productVersion() { return String(globalThis.YMBProduct?.VERSION || "0.1.1"); }
  function fail(code, message) { const error = new Error(message || code); error.code = code; throw error; }
  function unicodeLength(text) { return Array.from(String(text || "")).length; }

  function asString(value, name, { required = false, max = 4000 } = {}) {
    if (value === undefined || value === null || value === "") {
      if (required) fail("MISSING_FIELD", `Отсутствует обязательное поле: ${name}`);
      return undefined;
    }
    const text = String(value).trim();
    if (required && !text) fail("MISSING_FIELD", `Отсутствует обязательное поле: ${name}`);
    if (unicodeLength(text) > max) fail("FIELD_TOO_LONG", `${name}: превышена максимальная длина ${max}`);
    return text;
  }

  function asInteger(value, name, { defaultValue, min = 0, max = Number.MAX_SAFE_INTEGER } = {}) {
    const candidate = value === undefined ? defaultValue : value;
    const number = typeof candidate === "number" ? candidate : Number(candidate);
    if (!Number.isSafeInteger(number) || number < min || number > max) fail("INVALID_FIELD", `${name} должен быть целым числом от ${min} до ${max}.`);
    return number;
  }

  function asEnum(value, name, values, { defaultValue, required = false } = {}) {
    const candidate = value === undefined ? defaultValue : asString(value, name, { required: true, max: 100 });
    if (candidate === undefined) {
      if (required) fail("MISSING_FIELD", `Отсутствует обязательное поле: ${name}`);
      return undefined;
    }
    if (!values.has(candidate)) fail("INVALID_ENUM", `Неизвестное значение ${name}: ${candidate}`);
    return candidate;
  }

  function asDate(value, name) {
    const text = asString(value, name, { required: true, max: 10 });
    const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(text);
    if (!match) fail("INVALID_DATE", `${name} должен быть датой YYYY-MM-DD.`);
    const year = Number(match[1]); const month = Number(match[2]); const day = Number(match[3]);
    const date = new Date(Date.UTC(year, month - 1, day));
    if (date.getUTCFullYear() !== year || date.getUTCMonth() !== month - 1 || date.getUTCDate() !== day) fail("INVALID_DATE", `${name} должен быть корректной датой YYYY-MM-DD.`);
    return text;
  }

  function normalizeStringArray(value, name, allowed, { maxItems = 10 } = {}) {
    if (value === undefined) return Object.freeze([]);
    if (!Array.isArray(value)) fail("INVALID_FIELD", `${name} должен быть массивом.`);
    if (value.length > maxItems) fail("INVALID_FIELD", `${name}: слишком много элементов.`);
    const out = [];
    const seen = new Set();
    for (const raw of value) {
      const current = asString(raw, name, { required: true, max: 100 });
      if (!allowed.has(current)) fail("INVALID_ENUM", `Неизвестное значение ${name}: ${current}`);
      if (seen.has(current)) continue;
      seen.add(current);
      out.push(current);
    }
    return Object.freeze(out);
  }

  function normalizeFilters(value) {
    if (value === undefined) return Object.freeze([]);
    if (!Array.isArray(value)) fail("INVALID_FIELD", "filters должен быть массивом.");
    if (value.length > 20) fail("INVALID_FIELD", "filters: максимум 20 элементов.");
    return Object.freeze(value.map((raw, index) => {
      if (!raw || typeof raw !== "object" || Array.isArray(raw)) fail("INVALID_FIELD", `filters[${index}] должен быть объектом.`);
      const allowed = new Set(["dimension", "operator", "expression"]);
      for (const key of Object.keys(raw)) if (!allowed.has(key)) fail("UNSUPPORTED_FIELD", `Поле filters[${index}].${key} не разрешено.`);
      const dimension = asEnum(raw.dimension, `filters[${index}].dimension`, FILTER_DIMENSIONS, { required: true });
      const operator = asEnum(raw.operator, `filters[${index}].operator`, FILTER_OPERATORS, { required: true });
      const expression = asString(raw.expression, `filters[${index}].expression`, { required: true, max: 4096 });
      return Object.freeze({ dimension, operator, expression });
    }));
  }

  function parseCommand(text) {
    const source = String(text || "").replace(/\u00a0/g, " ").trim();
    if (!source.startsWith(PREFIX)) fail("NOT_GOOGLE_SEARCH_CONSOLE_COMMAND", `Команда должна начинаться с ${PREFIX}`);
    const rest = source.slice(PREFIX.length).trim();
    if (!rest) fail("MISSING_JSON", `После ${PREFIX} должен идти JSON-объект.`);
    let raw;
    try { raw = JSON.parse(rest); } catch (error) { fail("INVALID_JSON", `Некорректный JSON: ${error.message}`); }
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) fail("INVALID_JSON_ROOT", "Команда должна быть JSON-объектом.");
    return normalizeCommand(raw);
  }

  function normalizeCommand(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) fail("INVALID_JSON_ROOT", "Команда должна быть JSON-объектом.");
    const method = asString(raw.method, "method", { required: true, max: 80 });
    if (!METHOD_SET.has(method)) fail("UNSUPPORTED_METHOD", `Метод ${method} не разрешён.`);
    const allowed = method === "listSites" ? LIST_FIELDS : ANALYTICS_FIELDS;
    for (const key of Object.keys(raw)) if (!allowed.has(key)) fail("UNSUPPORTED_FIELD", `Поле ${key} не разрешено для ${method}.`);
    if (method === "listSites") return Object.freeze({ method });

    const siteUrl = asString(raw.siteUrl, "siteUrl", { required: true, max: 4000 });
    const startDate = asDate(raw.startDate, "startDate");
    const endDate = asDate(raw.endDate, "endDate");
    if (startDate > endDate) fail("INVALID_DATE_RANGE", "startDate не может быть позже endDate.");
    const type = asEnum(raw.type, "type", TYPES, { defaultValue: "web" });
    const dimensions = normalizeStringArray(raw.dimensions, "dimensions", DIMENSIONS, { maxItems: 5 });
    const rowLimit = asInteger(raw.rowLimit, "rowLimit", { defaultValue: 1000, min: 1, max: 25000 });
    const startRow = asInteger(raw.startRow, "startRow", { defaultValue: 0, min: 0 });
    const dataState = asEnum(raw.dataState, "dataState", DATA_STATES, { defaultValue: "final" });
    const filters = normalizeFilters(raw.filters);
    return Object.freeze({ method, siteUrl, startDate, endDate, type, dimensions, rowLimit, startRow, dataState, filters });
  }

  function buildRequest(command) {
    const normalized = normalizeCommand(command);
    if (normalized.method === "listSites") return Object.freeze({ method: "GET", url: `${BASE_URL}/sites` });
    const body = {
      startDate: normalized.startDate,
      endDate: normalized.endDate,
      type: normalized.type,
      dimensions: [...normalized.dimensions],
      rowLimit: normalized.rowLimit,
      startRow: normalized.startRow,
      dataState: normalized.dataState
    };
    if (normalized.filters.length) {
      body.dimensionFilterGroups = [{
        groupType: "and",
        filters: normalized.filters.map((filter) => ({ dimension: filter.dimension, operator: filter.operator, expression: filter.expression }))
      }];
    }
    return Object.freeze({
      method: "POST",
      url: `${BASE_URL}/sites/${encodeURIComponent(normalized.siteUrl)}/searchAnalytics/query`,
      body: Object.freeze(body)
    });
  }

  function finiteOrZero(value) { const number = Number(value); return Number.isFinite(number) ? number : 0; }

  function normalizeProviderResult(command, parsed) {
    const normalized = normalizeCommand(command);
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) fail("INVALID_GOOGLE_SEARCH_CONSOLE_RESPONSE", "Google Search Console вернул неожиданный JSON-ответ.");
    if (normalized.method === "listSites") {
      const sites = (Array.isArray(parsed.siteEntry) ? parsed.siteEntry : []).map((row) => ({
        site_url: String(row?.siteUrl || ""),
        permission_level: String(row?.permissionLevel || "")
      })).filter((row) => row.site_url);
      return { provider: "google_search_console", source: "Sites", sites };
    }
    const rows = (Array.isArray(parsed.rows) ? parsed.rows : []).map((row) => ({
      keys: Array.isArray(row?.keys) ? row.keys.map((value) => String(value)) : [],
      clicks: finiteOrZero(row?.clicks),
      impressions: finiteOrZero(row?.impressions),
      ctr: finiteOrZero(row?.ctr),
      average_position: finiteOrZero(row?.position)
    }));
    return {
      provider: "google_search_console",
      source: "Search Analytics",
      position_semantics: "average_topmost_position_over_impressions",
      rows,
      response_aggregation_type: parsed.responseAggregationType == null ? null : String(parsed.responseAggregationType)
    };
  }

  function safeErrorPayload(status, rawText, parsed) {
    const candidate = parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : null;
    const error = candidate?.error && typeof candidate.error === "object" ? candidate.error : candidate;
    const code = error?.status || error?.code || "GOOGLE_SEARCH_CONSOLE_API_ERROR";
    const message = error?.message || rawText || "Google Search Console API error";
    return { http_status: Number(status || 0), code: String(code).slice(0, 160), message: String(message).slice(0, 2000) };
  }

  function commandFingerprint(command) {
    const json = JSON.stringify(command);
    let hash = 2166136261;
    for (let i = 0; i < json.length; i += 1) { hash ^= json.charCodeAt(i); hash = Math.imul(hash, 16777619); }
    return (hash >>> 0).toString(16).padStart(8, "0");
  }

  function buildResultEnvelope({ requestId, command, httpStatus, result, elapsedMs, metadata = {} }) {
    return {
      bridge: String(globalThis.YMBProduct?.BRIDGE_ID || "yandex-marketing-bridge"),
      version: productVersion(),
      service: "google_search_console",
      operation: command?.method || null,
      request_id: requestId,
      run_id: metadata.run_id || null,
      status: metadata.status || (Number(httpStatus || 0) >= 200 && Number(httpStatus || 0) < 300 ? "OK" : "ERROR"),
      reason: metadata.reason || null,
      cost_estimate: metadata.cost_estimate || null,
      policy: metadata.policy || null,
      command,
      http_status: Number(httpStatus || 0),
      elapsed_ms: Number(elapsedMs || 0),
      result,
      ...(metadata.request_executed !== undefined ? { request_executed: metadata.request_executed } : {}),
      ...(metadata.automatic_retry !== undefined ? { automatic_retry: metadata.automatic_retry } : {})
    };
  }

  function formatResultEnvelope(envelope) { return `${RESULT_PREFIX}\n${JSON.stringify(envelope, null, 2)}`; }
  function formatResultReport(args) { return formatResultEnvelope(buildResultEnvelope(args)); }
  function buildSkippedEnvelope({ requestId, command, reason, metadata = {} }) {
    return buildResultEnvelope({
      requestId, command, httpStatus: 0, elapsedMs: 0,
      metadata: { ...metadata, status: "SKIPPED", reason, request_executed: metadata.request_executed ?? false, automatic_retry: metadata.automatic_retry ?? false },
      result: { skipped: true, reason }
    });
  }
  function formatSkippedReport(args) { return formatResultEnvelope(buildSkippedEnvelope(args)); }
  function isCommandText(text) { return String(text || "").replace(/\u00a0/g, " ").trim().startsWith(PREFIX); }

  globalThis.GoogleSearchConsoleProtocol = Object.freeze({
    PREFIX, RESULT_PREFIX, BASE_URL, METHODS, DIMENSIONS, FILTER_DIMENSIONS, FILTER_OPERATORS, DATA_STATES, TYPES,
    parseCommand, normalizeCommand, buildRequest, normalizeProviderResult, safeErrorPayload,
    commandFingerprint, buildResultEnvelope, formatResultEnvelope, formatResultReport,
    buildSkippedEnvelope, formatSkippedReport, isCommandText
  });
})();
