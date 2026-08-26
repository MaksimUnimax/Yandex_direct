(() => {
  "use strict";

  const PREFIX = "WEBMASTER_API_V1";
  const RESULT_PREFIX = "WEBMASTER_RESULT_V1";
  const BASE_URL = "https://api.webmaster.yandex.net/v4";
  const METHODS = Object.freeze(["listHosts", "getSummary", "getDiagnostics", "getPopularQueries"]);
  const METHOD_SET = new Set(METHODS);
  const ORDER_BY = new Set(["TOTAL_SHOWS", "TOTAL_CLICKS"]);
  const QUERY_INDICATORS = new Set(["TOTAL_SHOWS", "TOTAL_CLICKS", "AVG_SHOW_POSITION", "AVG_CLICK_POSITION"]);
  const DEVICE_TYPES = new Set(["ALL", "DESKTOP", "MOBILE_AND_TABLET", "MOBILE", "TABLET"]);
  const COMMON_FIELDS = new Set(["method"]);
  const HOST_FIELDS = new Set(["method", "hostId"]);
  const POPULAR_FIELDS = new Set([
    "method", "hostId", "orderBy", "queryIndicator", "deviceTypeIndicator",
    "dateFrom", "dateTo", "offset", "limit"
  ]);

  function productVersion() { return String(globalThis.YMBProduct?.VERSION || "0.1.1"); }
  function fail(code, message) { const error = new Error(message || code); error.code = code; throw error; }
  function unicodeLength(text) { return Array.from(String(text || "")).length; }

  function asString(value, name, { required = false, max = 1000 } = {}) {
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

  function asEnum(value, name, values, { required = false, defaultValue } = {}) {
    const candidate = value === undefined ? defaultValue : asString(value, name, { required: true, max: 80 });
    if (candidate === undefined) {
      if (required) fail("MISSING_FIELD", `Отсутствует обязательное поле: ${name}`);
      return undefined;
    }
    if (!values.has(candidate)) fail("INVALID_ENUM", `Неизвестное значение ${name}: ${candidate}`);
    return candidate;
  }

  function asDate(value, name) {
    const text = asString(value, name, { required: false, max: 64 });
    if (text === undefined) return undefined;
    if (!/^\d{4}-\d{2}-\d{2}(?:[Tt ][0-9:.+\-Zz]+)?$/.test(text) || Number.isNaN(Date.parse(text))) {
      fail("INVALID_DATE", `${name} должен быть корректной датой или RFC3339 datetime.`);
    }
    return text;
  }

  function allowedFieldsForMethod(method) {
    if (method === "listHosts") return COMMON_FIELDS;
    if (method === "getSummary" || method === "getDiagnostics") return HOST_FIELDS;
    if (method === "getPopularQueries") return POPULAR_FIELDS;
    return COMMON_FIELDS;
  }

  function parseCommand(text) {
    const source = String(text || "").replace(/\u00a0/g, " ").trim();
    if (!source.startsWith(PREFIX)) fail("NOT_WEBMASTER_COMMAND", `Команда должна начинаться с ${PREFIX}`);
    const rest = source.slice(PREFIX.length).trim();
    if (!rest) fail("MISSING_JSON", `После ${PREFIX} должен идти JSON-объект.`);
    let raw;
    try { raw = JSON.parse(rest); }
    catch (error) { fail("INVALID_JSON", `Некорректный JSON: ${error.message}`); }
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) fail("INVALID_JSON_ROOT", "Команда должна быть JSON-объектом.");
    return normalizeCommand(raw);
  }

  function normalizeCommand(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) fail("INVALID_JSON_ROOT", "Команда должна быть JSON-объектом.");
    const method = asString(raw.method, "method", { required: true, max: 80 });
    if (!METHOD_SET.has(method)) fail("UNSUPPORTED_METHOD", `Метод ${method} не разрешён.`);
    const allowed = allowedFieldsForMethod(method);
    for (const key of Object.keys(raw)) {
      if (!allowed.has(key)) fail("UNSUPPORTED_FIELD", `Поле ${key} не разрешено для ${method}.`);
    }

    if (method === "listHosts") return Object.freeze({ method });

    const hostId = asString(raw.hostId, "hostId", { required: true, max: 1000 });
    if (method === "getSummary" || method === "getDiagnostics") return Object.freeze({ method, hostId });

    const orderBy = asEnum(raw.orderBy, "orderBy", ORDER_BY, { required: true });
    const queryIndicator = asEnum(raw.queryIndicator, "queryIndicator", QUERY_INDICATORS);
    const deviceTypeIndicator = asEnum(raw.deviceTypeIndicator, "deviceTypeIndicator", DEVICE_TYPES, { defaultValue: "ALL" });
    const dateFrom = asDate(raw.dateFrom, "dateFrom");
    const dateTo = asDate(raw.dateTo, "dateTo");
    if (dateFrom && dateTo && Date.parse(dateFrom) > Date.parse(dateTo)) fail("INVALID_DATE_RANGE", "dateFrom не может быть позже dateTo.");
    const offset = asInteger(raw.offset, "offset", { defaultValue: 0, min: 0 });
    const limit = asInteger(raw.limit, "limit", { defaultValue: 500, min: 1, max: 500 });
    const normalized = { method, hostId, orderBy, deviceTypeIndicator, offset, limit };
    if (queryIndicator !== undefined) normalized.queryIndicator = queryIndicator;
    if (dateFrom !== undefined) normalized.dateFrom = dateFrom;
    if (dateTo !== undefined) normalized.dateTo = dateTo;
    return Object.freeze(normalized);
  }

  function normalizeUserId(userId) {
    const text = String(userId ?? "").trim();
    if (!/^\d+$/.test(text)) fail("WEBMASTER_USER_ID_MISSING", "Webmaster user_id отсутствует или некорректен.");
    return text;
  }

  function queryString(entries) {
    return entries
      .filter(([, value]) => value !== undefined && value !== null && value !== "")
      .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`)
      .join("&");
  }

  function buildRequest(command, userId) {
    const normalized = normalizeCommand(command);
    const uid = normalizeUserId(userId);
    const userBase = `${BASE_URL}/user/${encodeURIComponent(uid)}`;
    if (normalized.method === "listHosts") return Object.freeze({ method: "GET", url: `${userBase}/hosts` });
    const hostBase = `${userBase}/hosts/${encodeURIComponent(normalized.hostId)}`;
    if (normalized.method === "getSummary") return Object.freeze({ method: "GET", url: `${hostBase}/summary` });
    if (normalized.method === "getDiagnostics") return Object.freeze({ method: "GET", url: `${hostBase}/diagnostics` });
    const qs = queryString([
      ["order_by", normalized.orderBy],
      ["query_indicator", normalized.queryIndicator],
      ["device_type_indicator", normalized.deviceTypeIndicator],
      ["date_from", normalized.dateFrom],
      ["date_to", normalized.dateTo],
      ["offset", normalized.offset],
      ["limit", normalized.limit]
    ]);
    return Object.freeze({ method: "GET", url: `${hostBase}/search-queries/popular?${qs}` });
  }

  function normalizeHost(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) return null;
    const out = {
      host_id: String(raw.host_id || ""),
      ascii_host_url: String(raw.ascii_host_url || ""),
      unicode_host_url: String(raw.unicode_host_url || ""),
      verified: raw.verified === true
    };
    if (raw.main_mirror && typeof raw.main_mirror === "object" && !Array.isArray(raw.main_mirror)) {
      out.main_mirror = {
        host_id: String(raw.main_mirror.host_id || ""),
        ascii_host_url: String(raw.main_mirror.ascii_host_url || ""),
        unicode_host_url: String(raw.main_mirror.unicode_host_url || ""),
        verified: raw.main_mirror.verified === true
      };
    }
    return out;
  }

  function normalizeProviderResult(command, parsed) {
    const normalized = normalizeCommand(command);
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) fail("INVALID_WEBMASTER_RESPONSE", "Yandex Webmaster вернул неожиданный JSON-ответ.");
    if (normalized.method === "listHosts") {
      const source = Array.isArray(parsed.hosts) ? parsed.hosts : [];
      return { hosts: source.map(normalizeHost).filter(Boolean) };
    }
    if (normalized.method === "getSummary") {
      return {
        sqi: parsed.sqi ?? null,
        excluded_pages_count: parsed.excluded_pages_count ?? null,
        searchable_pages_count: parsed.searchable_pages_count ?? null,
        site_problems: parsed.site_problems && typeof parsed.site_problems === "object" ? parsed.site_problems : {}
      };
    }
    if (normalized.method === "getDiagnostics") {
      const source = parsed.problems && typeof parsed.problems === "object" && !Array.isArray(parsed.problems) ? parsed.problems : parsed;
      const problems = {};
      for (const [code, value] of Object.entries(source || {})) {
        if (!value || typeof value !== "object" || Array.isArray(value)) continue;
        problems[String(code)] = {
          severity: value.severity ?? null,
          state: value.state ?? null,
          last_state_update: value.last_state_update ?? null
        };
      }
      return { problems };
    }
    const queries = Array.isArray(parsed.queries) ? parsed.queries.map((row) => ({
      query_id: String(row?.query_id || ""),
      query_text: String(row?.query_text || ""),
      indicators: row?.indicators && typeof row.indicators === "object" && !Array.isArray(row.indicators) ? row.indicators : {}
    })) : [];
    return {
      queries,
      date_from: parsed.date_from ?? null,
      date_to: parsed.date_to ?? null,
      count: Number.isFinite(Number(parsed.count)) ? Number(parsed.count) : queries.length
    };
  }

  function safeErrorPayload(status, rawText, parsed) {
    const candidate = parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : null;
    const code = candidate?.error_code || candidate?.code || candidate?.error?.code || candidate?.status || "YANDEX_WEBMASTER_API_ERROR";
    const message = candidate?.error_message || candidate?.message || candidate?.error?.message || candidate?.error || rawText || "Yandex Webmaster API error";
    return {
      http_status: Number(status || 0),
      code: String(code).slice(0, 160),
      message: String(message).slice(0, 2000)
    };
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
      service: "webmaster",
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

  globalThis.WebmasterProtocol = Object.freeze({
    PREFIX, RESULT_PREFIX, BASE_URL, METHODS, ORDER_BY, QUERY_INDICATORS, DEVICE_TYPES,
    parseCommand, normalizeCommand, buildRequest, normalizeProviderResult, safeErrorPayload,
    commandFingerprint, buildResultEnvelope, formatResultEnvelope, formatResultReport,
    buildSkippedEnvelope, formatSkippedReport, isCommandText
  });
})();
