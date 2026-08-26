(() => {
  "use strict";

  const PREFIX = "METRIKA_API_V1";
  const RESULT_PREFIX = "METRIKA_RESULT_V1";
  const MANAGEMENT_BASE_URL = "https://api-metrika.yandex.net/management/v1";
  const REPORTS_BASE_URL = "https://api-metrika.yandex.net/stat/v1";
  const METHODS = Object.freeze(["listCounters", "getCounter", "getTrafficSummary", "getTrafficByTime"]);
  const METHOD_SET = new Set(METHODS);
  const PERMISSIONS = new Set(["own", "view", "edit"]);
  const GROUPS = new Set(["day", "week", "month"]);
  const FIXED_METRICS = Object.freeze(["ym:s:visits", "ym:s:users", "ym:s:pageviews"]);
  const FIXED_METRICS_QUERY = FIXED_METRICS.join(",");
  const LIST_FIELDS = new Set(["method", "page", "perPage", "permission"]);
  const COUNTER_FIELDS = new Set(["method", "counterId"]);
  const REPORT_FIELDS = new Set(["method", "counterId", "dateFrom", "dateTo"]);
  const BYTIME_FIELDS = new Set(["method", "counterId", "dateFrom", "dateTo", "group"]);
  const COUNTER_ALLOWLIST = Object.freeze(["id", "name", "site", "status", "permission", "owner_login", "favorite", "type", "code_status", "activity_status"]);

  function productVersion() { return String(globalThis.YMBProduct?.VERSION || "0.1.1"); }
  function fail(code, message) { const error = new Error(message || code); error.code = code; throw error; }
  function text(value) { return String(value ?? "").trim(); }
  function asPositiveSafeInteger(value, name) {
    const source = typeof value === "number" ? String(value) : text(value);
    if (!/^\d+$/.test(source)) fail("INVALID_FIELD", `${name} должен быть положительным целым числом.`);
    const number = Number(source);
    if (!Number.isSafeInteger(number) || number <= 0) fail("INVALID_FIELD", `${name} должен быть положительным safe integer.`);
    return number;
  }
  function asInteger(value, name, { defaultValue, min = 0, max = Number.MAX_SAFE_INTEGER } = {}) {
    const candidate = value === undefined ? defaultValue : value;
    const number = typeof candidate === "number" ? candidate : Number(candidate);
    if (!Number.isSafeInteger(number) || number < min || number > max) fail("INVALID_FIELD", `${name} должен быть целым числом от ${min} до ${max}.`);
    return number;
  }
  function asEnum(value, name, allowed, { defaultValue, optional = false } = {}) {
    if (value === undefined || value === null || value === "") {
      if (optional) return undefined;
      if (defaultValue !== undefined) return defaultValue;
      fail("MISSING_FIELD", `Отсутствует обязательное поле: ${name}`);
    }
    const candidate = text(value);
    if (!allowed.has(candidate)) fail("INVALID_ENUM", `Неизвестное значение ${name}: ${candidate}`);
    return candidate;
  }
  function formatDate(date) {
    const y = date.getFullYear(); const m = String(date.getMonth() + 1).padStart(2, "0"); const d = String(date.getDate()).padStart(2, "0");
    return `${y}-${m}-${d}`;
  }
  function localToday() { return formatDate(new Date()); }
  function daysAgo(days) { const date = new Date(); date.setHours(12, 0, 0, 0); date.setDate(date.getDate() - Number(days || 0)); return formatDate(date); }
  function asDate(value, name, fallback) {
    const candidate = value === undefined || value === null || value === "" ? fallback : text(value);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(candidate || "")) fail("INVALID_DATE", `${name} должен быть в формате YYYY-MM-DD.`);
    const [year, month, day] = candidate.split("-").map(Number); const date = new Date(year, month - 1, day, 12, 0, 0, 0);
    if (date.getFullYear() !== year || date.getMonth() !== month - 1 || date.getDate() !== day) fail("INVALID_DATE", `${name} содержит некорректную дату.`);
    return candidate;
  }
  function dateOrdinal(ymd) { const [year, month, day] = ymd.split("-").map(Number); return Math.floor(Date.UTC(year, month - 1, day) / 86400000); }
  function normalizeDateRange(raw) {
    const dateTo = asDate(raw.dateTo, "dateTo", localToday()); const dateFrom = asDate(raw.dateFrom, "dateFrom", daysAgo(6));
    const span = dateOrdinal(dateTo) - dateOrdinal(dateFrom) + 1;
    if (span <= 0) fail("INVALID_DATE_RANGE", "dateFrom не может быть позже dateTo.");
    if (span > 366) fail("DATE_RANGE_TOO_LARGE", "Период отчёта не может превышать 366 календарных дней.");
    return { dateFrom, dateTo };
  }
  function fieldsForMethod(method) {
    if (method === "listCounters") return LIST_FIELDS;
    if (method === "getCounter") return COUNTER_FIELDS;
    if (method === "getTrafficSummary") return REPORT_FIELDS;
    if (method === "getTrafficByTime") return BYTIME_FIELDS;
    return new Set(["method"]);
  }
  function normalizeCommand(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) fail("INVALID_JSON_ROOT", "Команда должна быть JSON-объектом.");
    const method = text(raw.method);
    if (!method) fail("MISSING_FIELD", "Отсутствует обязательное поле: method");
    if (!METHOD_SET.has(method)) fail("UNSUPPORTED_METHOD", `Метод ${method} не разрешён.`);
    const allowed = fieldsForMethod(method); for (const key of Object.keys(raw)) if (!allowed.has(key)) fail("UNSUPPORTED_FIELD", `Поле ${key} не разрешено для ${method}.`);
    if (method === "listCounters") {
      const normalized = { method, page: asInteger(raw.page, "page", { defaultValue: 1, min: 1 }), perPage: asInteger(raw.perPage, "perPage", { defaultValue: 100, min: 1, max: 1000 }) };
      const permission = asEnum(raw.permission, "permission", PERMISSIONS, { optional: true }); if (permission !== undefined) normalized.permission = permission;
      return Object.freeze(normalized);
    }
    const counterId = asPositiveSafeInteger(raw.counterId, "counterId");
    if (method === "getCounter") return Object.freeze({ method, counterId });
    const dates = normalizeDateRange(raw);
    if (method === "getTrafficSummary") return Object.freeze({ method, counterId, ...dates });
    return Object.freeze({ method, counterId, ...dates, group: asEnum(raw.group, "group", GROUPS, { defaultValue: "day" }) });
  }
  function parseCommand(sourceText) {
    const source = String(sourceText || "").replace(/\u00a0/g, " ").trim();
    if (!source.startsWith(PREFIX)) fail("NOT_METRIKA_COMMAND", `Команда должна начинаться с ${PREFIX}`);
    const rest = source.slice(PREFIX.length).trim(); if (!rest) fail("MISSING_JSON", `После ${PREFIX} должен идти JSON-объект.`);
    let raw; try { raw = JSON.parse(rest); } catch (error) { fail("INVALID_JSON", `Некорректный JSON: ${error.message}`); }
    return normalizeCommand(raw);
  }
  function queryString(entries) { return entries.filter(([, value]) => value !== undefined && value !== null && value !== "").map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`).join("&"); }
  function buildRequest(command) {
    const normalized = normalizeCommand(command);
    if (normalized.method === "listCounters") {
      const offset = ((normalized.page - 1) * normalized.perPage) + 1;
      if (!Number.isSafeInteger(offset) || offset <= 0) fail("INVALID_FIELD", "page/perPage дают небезопасный provider offset.");
      const qs = queryString([["offset", offset], ["per_page", normalized.perPage], ["permission", normalized.permission]]);
      return Object.freeze({ method: "GET", url: `${MANAGEMENT_BASE_URL}/counters?${qs}` });
    }
    if (normalized.method === "getCounter") return Object.freeze({ method: "GET", url: `${MANAGEMENT_BASE_URL}/counter/${encodeURIComponent(String(normalized.counterId))}` });
    const base = normalized.method === "getTrafficSummary" ? `${REPORTS_BASE_URL}/data` : `${REPORTS_BASE_URL}/data/bytime`;
    const qs = queryString([["ids", normalized.counterId], ["metrics", FIXED_METRICS_QUERY], ["date1", normalized.dateFrom], ["date2", normalized.dateTo], ["group", normalized.method === "getTrafficByTime" ? normalized.group : undefined]]);
    return Object.freeze({ method: "GET", url: `${base}?${qs}` });
  }
  function normalizeCounter(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) return null; const out = {};
    for (const key of COUNTER_ALLOWLIST) {
      if (!Object.prototype.hasOwnProperty.call(raw, key)) continue; const value = raw[key];
      if (key === "id") { const number = Number(value); out.id = Number.isSafeInteger(number) && number > 0 ? number : null; }
      else if (key === "favorite") out.favorite = value === true || value === 1;
      else out[key] = value == null ? null : String(value);
    }
    return out;
  }
  function truthFields(parsed) {
    return {
      sampled: parsed?.sampled === true,
      sample_share: Number.isFinite(Number(parsed?.sample_share)) ? Number(parsed.sample_share) : null,
      sample_size: Number.isFinite(Number(parsed?.sample_size)) ? Number(parsed.sample_size) : null,
      sample_space: Number.isFinite(Number(parsed?.sample_space)) ? Number(parsed.sample_space) : null,
      contains_sensitive_data: parsed?.contains_sensitive_data === true,
      data_lag: Number.isFinite(Number(parsed?.data_lag)) ? Number(parsed.data_lag) : null,
      total_rows: Number.isFinite(Number(parsed?.total_rows)) ? Number(parsed.total_rows) : null,
      total_rows_rounded: parsed?.total_rows_rounded === true
    };
  }
  function numberOrNull(value) { const n = Number(value); return Number.isFinite(n) ? n : null; }
  function metricTriple(values) { const source = Array.isArray(values) ? values : []; return { visits: numberOrNull(source[0]), users: numberOrNull(source[1]), pageviews: numberOrNull(source[2]) }; }
  function metricSeries(rows) {
    const first = Array.isArray(rows) && rows[0] && typeof rows[0] === "object" ? rows[0] : {}; const metrics = Array.isArray(first.metrics) ? first.metrics : [];
    return { visits: Array.isArray(metrics[0]) ? metrics[0].map(numberOrNull) : [], users: Array.isArray(metrics[1]) ? metrics[1].map(numberOrNull) : [], pageviews: Array.isArray(metrics[2]) ? metrics[2].map(numberOrNull) : [] };
  }
  function bytimeTotals(rawTotals) { const source = Array.isArray(rawTotals) ? rawTotals : []; return metricTriple(source.map((item) => Array.isArray(item) ? item[0] : item)); }
  function normalizeProviderResult(command, parsed) {
    const normalized = normalizeCommand(command);
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) fail("INVALID_METRIKA_RESPONSE", "Yandex Metrika вернула неожиданный JSON-ответ.");
    if (normalized.method === "listCounters") { const counters = Array.isArray(parsed.counters) ? parsed.counters.map(normalizeCounter).filter(Boolean) : []; return { rows: Number.isFinite(Number(parsed.rows)) ? Number(parsed.rows) : counters.length, counters }; }
    if (normalized.method === "getCounter") { const counter = normalizeCounter(parsed.counter || parsed); if (!counter) fail("INVALID_METRIKA_RESPONSE", "Yandex Metrika не вернула объект счётчика."); return { counter }; }
    if (normalized.method === "getTrafficSummary") return { counter_id: normalized.counterId, date_from: normalized.dateFrom, date_to: normalized.dateTo, metrics: metricTriple(parsed.totals), ...truthFields(parsed) };
    return { counter_id: normalized.counterId, date_from: normalized.dateFrom, date_to: normalized.dateTo, group: normalized.group, series: metricSeries(parsed.data), totals: bytimeTotals(parsed.totals), ...truthFields(parsed) };
  }
  function safeErrorPayload(status, rawText, parsed) {
    const candidate = parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : null;
    const code = (Number(status) === 420 || Number(status) === 429) ? "QUOTA" : (candidate?.error_code || candidate?.code || candidate?.error?.code || candidate?.errors?.[0]?.error_type || candidate?.status || "YANDEX_METRIKA_API_ERROR");
    const message = candidate?.error_message || candidate?.message || candidate?.error?.message || candidate?.errors?.[0]?.message || candidate?.error || rawText || "Yandex Metrika API error";
    return { http_status: Number(status || 0), code: String(code).slice(0, 160), message: String(message).slice(0, 2000) };
  }
  function buildResultEnvelope({ requestId, command, httpStatus, result, elapsedMs, metadata = {} }) {
    return { bridge: String(globalThis.YMBProduct?.BRIDGE_ID || "yandex-marketing-bridge"), version: productVersion(), service: "metrika", operation: command?.method || null, request_id: requestId, run_id: metadata.run_id || null, status: metadata.status || (Number(httpStatus || 0) >= 200 && Number(httpStatus || 0) < 300 ? "OK" : "ERROR"), reason: metadata.reason || null, cost_estimate: metadata.cost_estimate || null, policy: metadata.policy || null, command, http_status: Number(httpStatus || 0), elapsed_ms: Number(elapsedMs || 0), result, ...(metadata.request_executed !== undefined ? { request_executed: metadata.request_executed } : {}), ...(metadata.automatic_retry !== undefined ? { automatic_retry: metadata.automatic_retry } : {}) };
  }
  function formatResultEnvelope(envelope) { return `${RESULT_PREFIX}\n${JSON.stringify(envelope, null, 2)}`; }
  function buildSkippedEnvelope({ requestId, command, reason, metadata = {} }) { return buildResultEnvelope({ requestId, command, httpStatus: 0, elapsedMs: 0, result: { skipped: true, reason }, metadata: { ...metadata, status: "SKIPPED", reason, request_executed: metadata.request_executed ?? false, automatic_retry: false } }); }
  function formatSkippedReport(args) { return formatResultEnvelope(buildSkippedEnvelope(args)); }
  function commandFingerprint(command) { const json = JSON.stringify(command); let hash = 2166136261; for (let i = 0; i < json.length; i += 1) { hash ^= json.charCodeAt(i); hash = Math.imul(hash, 16777619); } return (hash >>> 0).toString(16).padStart(8, "0"); }
  function isCommandText(value) { return String(value || "").replace(/\u00a0/g, " ").trim().startsWith(PREFIX); }

  globalThis.MetrikaProtocol = Object.freeze({ PREFIX, RESULT_PREFIX, MANAGEMENT_BASE_URL, REPORTS_BASE_URL, METHODS, PERMISSIONS, GROUPS, FIXED_METRICS, parseCommand, normalizeCommand, buildRequest, normalizeProviderResult, safeErrorPayload, buildResultEnvelope, formatResultEnvelope, buildSkippedEnvelope, formatSkippedReport, commandFingerprint, isCommandText });
})();
