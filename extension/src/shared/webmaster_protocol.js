(() => {
  "use strict";

  const PREFIX = "WEBMASTER_API_V1";
  const RESULT_PREFIX = "WEBMASTER_RESULT_V1";
  const BASE_URL = "https://api.webmaster.yandex.net/v4";
  const METHODS = Object.freeze([
    "listHosts", "getSummary", "getDiagnostics", "getPopularQueries",
    "getAllQueryHistory", "getQueryHistory",
    "getIndexingSamples", "getInSearchSamples",
    "getExportRegions", "getExportLimits", "getExportDates",
    "projectQueryUrlExport", "startQueryUrlExport", "getQueryUrlExportStatus", "collectQueryUrlExport",
    "getQueryUrlExportManifest", "readQueryUrlExportChunk", "listQueryUrlExportJobs"
  ]);
  const METHOD_SET = new Set(METHODS);
  const LOCAL_METHODS = new Set(["projectQueryUrlExport", "getQueryUrlExportManifest", "readQueryUrlExportChunk", "listQueryUrlExportJobs"]);
  const DOWNLOAD_METHODS = new Set(["collectQueryUrlExport"]);
  const ORDER_BY = new Set(["TOTAL_SHOWS", "TOTAL_CLICKS"]);
  const QUERY_INDICATORS = new Set(["TOTAL_SHOWS", "TOTAL_CLICKS", "AVG_SHOW_POSITION", "AVG_CLICK_POSITION"]);
  const DEVICE_TYPES = new Set(["ALL", "DESKTOP", "MOBILE_AND_TABLET", "MOBILE", "TABLET"]);
  const COMMON_FIELDS = new Set(["method"]);
  const HOST_FIELDS = new Set(["method", "hostId"]);
  const POPULAR_FIELDS = new Set([
    "method", "hostId", "orderBy", "queryIndicator", "deviceTypeIndicator",
    "dateFrom", "dateTo", "offset", "limit"
  ]);
  const HISTORY_FIELDS = new Set(["method", "hostId", "queryIndicators", "deviceTypeIndicator", "dateFrom", "dateTo"]);
  const QUERY_HISTORY_FIELDS = new Set([...HISTORY_FIELDS, "queryId"]);
  const SAMPLE_FIELDS = new Set(["method", "hostId", "offset", "limit"]);
  const EXPORT_REGIONS_FIELDS = new Set(["method", "hostId", "filter", "limit"]);
  const EXPORT_START_FIELDS = new Set(["method", "hostId", "dates", "paths", "regionIds", "useProTariff", "confirmQuota", "confirmProTariff"]);
  const EXPORT_TASK_FIELDS = new Set(["method", "hostId", "taskId"]);
  const EXPORT_MANIFEST_FIELDS = new Set(["method", "taskId"]);
  const EXPORT_CHUNK_FIELDS = new Set(["method", "taskId", "offset", "limit"]);
  const EXPORT_LIST_FIELDS = new Set(["method", "pendingOnly"]);
  const MAX_EXPORT_PAYLOAD_ITEMS = 100;
  const MAX_EXPORT_CHUNK_SIZE = 500;

  function productVersion() { return String(globalThis.YMBProduct?.VERSION || "0.1.3"); }
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

  function asBoolean(value, name, { defaultValue = false } = {}) {
    const candidate = value === undefined ? defaultValue : value;
    if (typeof candidate !== "boolean") fail("INVALID_FIELD", `${name} должен быть boolean.`);
    return candidate;
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

  function asDate(value, name, { strictDay = false } = {}) {
    const text = asString(value, name, { required: false, max: 64 });
    if (text === undefined) return undefined;
    if (strictDay) {
      if (!/^\d{4}-\d{2}-\d{2}$/.test(text) || Number.isNaN(Date.parse(`${text}T00:00:00Z`))) fail("INVALID_DATE", `${name} должен быть датой YYYY-MM-DD.`);
      return text;
    }
    if (!/^\d{4}-\d{2}-\d{2}(?:[Tt ][0-9:.+\-Zz]+)?$/.test(text) || Number.isNaN(Date.parse(text))) {
      fail("INVALID_DATE", `${name} должен быть корректной датой или RFC3339 datetime.`);
    }
    return text;
  }

  function asStringArray(value, name, { required = false, maxItems = 100, itemMax = 2000, map = (item) => item } = {}) {
    if (value === undefined || value === null) {
      if (required) fail("MISSING_FIELD", `Отсутствует обязательное поле: ${name}`);
      return undefined;
    }
    if (!Array.isArray(value)) fail("INVALID_FIELD", `${name} должен быть массивом.`);
    if (required && !value.length) fail("EMPTY_FIELD", `${name} не должен быть пустым.`);
    if (value.length > maxItems) fail("TOO_MANY_ITEMS", `${name}: максимум ${maxItems} элементов.`);
    const out = value.map((item, index) => map(asString(item, `${name}[${index}]`, { required: true, max: itemMax }), index));
    return Object.freeze(out);
  }

  function asIntegerArray(value, name, { required = false, maxItems = 1000 } = {}) {
    if (value === undefined || value === null) {
      if (required) fail("MISSING_FIELD", `Отсутствует обязательное поле: ${name}`);
      return undefined;
    }
    if (!Array.isArray(value)) fail("INVALID_FIELD", `${name} должен быть массивом.`);
    if (value.length > maxItems) fail("TOO_MANY_ITEMS", `${name}: максимум ${maxItems} элементов.`);
    return Object.freeze(value.map((item, index) => asInteger(item, `${name}[${index}]`, { min: 1 })));
  }

  function asQueryIndicators(value) {
    if (value === undefined) return Object.freeze([...QUERY_INDICATORS]);
    if (!Array.isArray(value) || !value.length) fail("INVALID_FIELD", "queryIndicators должен быть непустым массивом.");
    const result = [];
    for (const item of value) {
      const indicator = asEnum(item, "queryIndicators", QUERY_INDICATORS, { required: true });
      if (!result.includes(indicator)) result.push(indicator);
    }
    return Object.freeze(result);
  }

  function validateRange(dateFrom, dateTo) {
    if (dateFrom && dateTo && Date.parse(dateFrom) > Date.parse(dateTo)) fail("INVALID_DATE_RANGE", "dateFrom не может быть позже dateTo.");
  }

  function allowedFieldsForMethod(method) {
    if (method === "listHosts") return COMMON_FIELDS;
    if (["getSummary", "getDiagnostics", "getExportLimits", "getExportDates"].includes(method)) return HOST_FIELDS;
    if (method === "getPopularQueries") return POPULAR_FIELDS;
    if (method === "getAllQueryHistory") return HISTORY_FIELDS;
    if (method === "getQueryHistory") return QUERY_HISTORY_FIELDS;
    if (["getIndexingSamples", "getInSearchSamples"].includes(method)) return SAMPLE_FIELDS;
    if (method === "getExportRegions") return EXPORT_REGIONS_FIELDS;
    if (["projectQueryUrlExport", "startQueryUrlExport"].includes(method)) return EXPORT_START_FIELDS;
    if (["getQueryUrlExportStatus", "collectQueryUrlExport"].includes(method)) return EXPORT_TASK_FIELDS;
    if (method === "getQueryUrlExportManifest") return EXPORT_MANIFEST_FIELDS;
    if (method === "readQueryUrlExportChunk") return EXPORT_CHUNK_FIELDS;
    if (method === "listQueryUrlExportJobs") return EXPORT_LIST_FIELDS;
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

  function normalizeExportCommand(raw, method) {
    const hostId = asString(raw.hostId, "hostId", { required: true, max: 1000 });
    const dates = asStringArray(raw.dates, "dates", { required: true, maxItems: MAX_EXPORT_PAYLOAD_ITEMS, itemMax: 10, map: (item, index) => asDate(item, `dates[${index}]`, { strictDay: true }) });
    const paths = asStringArray(raw.paths, "paths", {
      required: true, maxItems: MAX_EXPORT_PAYLOAD_ITEMS, itemMax: 4096,
      map: (item, index) => { if (!item.startsWith("/")) fail("INVALID_EXPORT_PATH", `paths[${index}] должен начинаться с /.`); return item; }
    });
    if (dates.length + paths.length > MAX_EXPORT_PAYLOAD_ITEMS) fail("EXPORT_PAYLOAD_LIMIT", `Сумма dates + paths не должна превышать ${MAX_EXPORT_PAYLOAD_ITEMS}.`);
    const regionIds = asIntegerArray(raw.regionIds, "regionIds", { maxItems: 10000 }) || Object.freeze([]);
    const useProTariff = asBoolean(raw.useProTariff, "useProTariff", { defaultValue: false });
    const confirmQuota = asBoolean(raw.confirmQuota, "confirmQuota", { defaultValue: false });
    const confirmProTariff = asBoolean(raw.confirmProTariff, "confirmProTariff", { defaultValue: false });
    if (method === "startQueryUrlExport" && confirmQuota !== true) fail("WEBMASTER_EXPORT_QUOTA_CONFIRM_REQUIRED", "startQueryUrlExport требует confirmQuota:true.");
    if (method === "startQueryUrlExport" && useProTariff === true && confirmProTariff !== true) fail("WEBMASTER_EXPORT_PRO_CONFIRM_REQUIRED", "useProTariff:true требует confirmProTariff:true.");
    return Object.freeze({ method, hostId, dates, paths, regionIds, useProTariff, confirmQuota, confirmProTariff });
  }

  function normalizeCommand(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) fail("INVALID_JSON_ROOT", "Команда должна быть JSON-объектом.");
    const method = asString(raw.method, "method", { required: true, max: 80 });
    if (!METHOD_SET.has(method)) fail("UNSUPPORTED_METHOD", `Метод ${method} не разрешён.`);
    const allowed = allowedFieldsForMethod(method);
    for (const key of Object.keys(raw)) if (!allowed.has(key)) fail("UNSUPPORTED_FIELD", `Поле ${key} не разрешено для ${method}.`);

    if (method === "listHosts") return Object.freeze({ method });
    if (["projectQueryUrlExport", "startQueryUrlExport"].includes(method)) return normalizeExportCommand(raw, method);
    if (method === "getQueryUrlExportManifest") return Object.freeze({ method, taskId: asString(raw.taskId, "taskId", { required: true, max: 160 }) });
    if (method === "readQueryUrlExportChunk") return Object.freeze({ method, taskId: asString(raw.taskId, "taskId", { required: true, max: 160 }), offset: asInteger(raw.offset, "offset", { defaultValue: 0, min: 0 }), limit: asInteger(raw.limit, "limit", { defaultValue: 200, min: 1, max: MAX_EXPORT_CHUNK_SIZE }) });
    if (method === "listQueryUrlExportJobs") return Object.freeze({ method, pendingOnly: asBoolean(raw.pendingOnly, "pendingOnly", { defaultValue: false }) });

    const hostId = asString(raw.hostId, "hostId", { required: true, max: 1000 });
    if (["getSummary", "getDiagnostics", "getExportLimits", "getExportDates"].includes(method)) return Object.freeze({ method, hostId });
    if (["getQueryUrlExportStatus", "collectQueryUrlExport"].includes(method)) return Object.freeze({ method, hostId, taskId: asString(raw.taskId, "taskId", { required: true, max: 160 }) });

    if (method === "getPopularQueries") {
      const orderBy = asEnum(raw.orderBy, "orderBy", ORDER_BY, { required: true });
      const queryIndicator = asEnum(raw.queryIndicator, "queryIndicator", QUERY_INDICATORS);
      const deviceTypeIndicator = asEnum(raw.deviceTypeIndicator, "deviceTypeIndicator", DEVICE_TYPES, { defaultValue: "ALL" });
      const dateFrom = asDate(raw.dateFrom, "dateFrom");
      const dateTo = asDate(raw.dateTo, "dateTo");
      validateRange(dateFrom, dateTo);
      const offset = asInteger(raw.offset, "offset", { defaultValue: 0, min: 0 });
      const limit = asInteger(raw.limit, "limit", { defaultValue: 500, min: 1, max: 500 });
      const normalized = { method, hostId, orderBy, deviceTypeIndicator, offset, limit };
      if (queryIndicator !== undefined) normalized.queryIndicator = queryIndicator;
      if (dateFrom !== undefined) normalized.dateFrom = dateFrom;
      if (dateTo !== undefined) normalized.dateTo = dateTo;
      return Object.freeze(normalized);
    }

    if (["getAllQueryHistory", "getQueryHistory"].includes(method)) {
      const queryIndicators = asQueryIndicators(raw.queryIndicators);
      const deviceTypeIndicator = asEnum(raw.deviceTypeIndicator, "deviceTypeIndicator", DEVICE_TYPES, { defaultValue: "ALL" });
      const dateFrom = asDate(raw.dateFrom, "dateFrom");
      const dateTo = asDate(raw.dateTo, "dateTo");
      validateRange(dateFrom, dateTo);
      const normalized = { method, hostId, queryIndicators, deviceTypeIndicator };
      if (method === "getQueryHistory") normalized.queryId = asString(raw.queryId, "queryId", { required: true, max: 1000 });
      if (dateFrom !== undefined) normalized.dateFrom = dateFrom;
      if (dateTo !== undefined) normalized.dateTo = dateTo;
      return Object.freeze(normalized);
    }

    if (["getIndexingSamples", "getInSearchSamples"].includes(method)) {
      return Object.freeze({ method, hostId, offset: asInteger(raw.offset, "offset", { defaultValue: 0, min: 0, max: 50000 }), limit: asInteger(raw.limit, "limit", { defaultValue: 100, min: 1, max: 100 }) });
    }

    if (method === "getExportRegions") {
      const normalized = { method, hostId, limit: asInteger(raw.limit, "limit", { defaultValue: 100, min: 1, max: 10000 }) };
      const filter = asString(raw.filter, "filter", { required: false, max: 500 });
      if (filter !== undefined) normalized.filter = filter;
      return Object.freeze(normalized);
    }

    fail("UNSUPPORTED_METHOD", `Метод ${method} не реализован.`);
  }

  function normalizeUserId(userId) {
    const text = String(userId ?? "").trim();
    if (!/^\d+$/.test(text)) fail("WEBMASTER_USER_ID_MISSING", "Webmaster user_id отсутствует или некорректен.");
    return text;
  }

  function queryString(entries) {
    return entries
      .filter(([, value]) => value !== undefined && value !== null && value !== "")
      .flatMap(([key, value]) => Array.isArray(value) ? value.map((item) => [key, item]) : [[key, value]])
      .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`)
      .join("&");
  }

  function buildRequest(command, userId) {
    const normalized = normalizeCommand(command);
    if (LOCAL_METHODS.has(normalized.method) || DOWNLOAD_METHODS.has(normalized.method)) fail("LOCAL_METHOD_NO_PROVIDER_REQUEST", `${normalized.method} не строит прямой Webmaster API request.`);
    const uid = normalizeUserId(userId);
    const userBase = `${BASE_URL}/user/${encodeURIComponent(uid)}`;
    if (normalized.method === "listHosts") return Object.freeze({ method: "GET", url: `${userBase}/hosts`, kind: "json" });
    const hostBase = `${userBase}/hosts/${encodeURIComponent(normalized.hostId)}`;
    if (normalized.method === "getSummary") return Object.freeze({ method: "GET", url: `${hostBase}/summary`, kind: "json" });
    if (normalized.method === "getDiagnostics") return Object.freeze({ method: "GET", url: `${hostBase}/diagnostics`, kind: "json" });
    if (normalized.method === "getPopularQueries") {
      const qs = queryString([["order_by", normalized.orderBy], ["query_indicator", normalized.queryIndicator], ["device_type_indicator", normalized.deviceTypeIndicator], ["date_from", normalized.dateFrom], ["date_to", normalized.dateTo], ["offset", normalized.offset], ["limit", normalized.limit]]);
      return Object.freeze({ method: "GET", url: `${hostBase}/search-queries/popular?${qs}`, kind: "json" });
    }
    if (["getAllQueryHistory", "getQueryHistory"].includes(normalized.method)) {
      const qs = queryString([["query_indicator", normalized.queryIndicators], ["device_type_indicator", normalized.deviceTypeIndicator], ["date_from", normalized.dateFrom], ["date_to", normalized.dateTo]]);
      const suffix = normalized.method === "getAllQueryHistory" ? "all/history" : `${encodeURIComponent(normalized.queryId)}/history`;
      return Object.freeze({ method: "GET", url: `${hostBase}/search-queries/${suffix}?${qs}`, kind: "json" });
    }
    if (normalized.method === "getIndexingSamples") return Object.freeze({ method: "GET", url: `${hostBase}/indexing/samples?${queryString([["offset", normalized.offset], ["limit", normalized.limit]])}`, kind: "json" });
    if (normalized.method === "getInSearchSamples") return Object.freeze({ method: "GET", url: `${hostBase}/search-urls/in-search/samples?${queryString([["offset", normalized.offset], ["limit", normalized.limit]])}`, kind: "json" });
    if (normalized.method === "getExportRegions") return Object.freeze({ method: "GET", url: `${hostBase}/pro/regions?${queryString([["filter", normalized.filter], ["limit", normalized.limit]])}`, kind: "json" });
    if (normalized.method === "getExportLimits") return Object.freeze({ method: "GET", url: `${hostBase}/pro/limits`, kind: "json" });
    if (normalized.method === "getExportDates") return Object.freeze({ method: "GET", url: `${hostBase}/pro/serp/dates`, kind: "json" });
    if (normalized.method === "startQueryUrlExport") return Object.freeze({ method: "POST", url: `${hostBase}/pro/serp/queries/download/`, kind: "json", body: { dates: [...normalized.dates], paths: [...normalized.paths], region_ids: [...normalized.regionIds], use_pro_tariff: normalized.useProTariff ? "true" : "false" } });
    if (normalized.method === "getQueryUrlExportStatus") return Object.freeze({ method: "GET", url: `${hostBase}/pro/serp/queries/download/${encodeURIComponent(normalized.taskId)}`, kind: "json" });
    fail("UNSUPPORTED_METHOD", `Для ${normalized.method} provider request не определён.`);
  }

  function normalizeIndicators(value) {
    const source = value && typeof value === "object" && !Array.isArray(value) ? value : {};
    const out = {};
    for (const indicator of QUERY_INDICATORS) {
      const rows = Array.isArray(source[indicator]) ? source[indicator] : [];
      if (!rows.length && !Object.hasOwn(source, indicator)) continue;
      out[indicator] = rows.map((row) => ({ date: row?.date ?? null, value: Number.isFinite(Number(row?.value)) ? Number(row.value) : null }));
    }
    return out;
  }

  function normalizeHost(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) return null;
    const out = { host_id: String(raw.host_id || ""), ascii_host_url: String(raw.ascii_host_url || ""), unicode_host_url: String(raw.unicode_host_url || ""), verified: raw.verified === true };
    if (raw.main_mirror && typeof raw.main_mirror === "object" && !Array.isArray(raw.main_mirror)) out.main_mirror = { host_id: String(raw.main_mirror.host_id || ""), ascii_host_url: String(raw.main_mirror.ascii_host_url || ""), unicode_host_url: String(raw.main_mirror.unicode_host_url || ""), verified: raw.main_mirror.verified === true };
    return out;
  }

  function normalizeSampleRow(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) return null;
    const allowed = ["url", "http_code", "access_date", "last_access", "status", "title"];
    const out = {};
    for (const key of allowed) if (raw[key] !== undefined) out[key] = raw[key];
    return out;
  }

  function normalizeProviderResult(command, parsed) {
    const normalized = normalizeCommand(command);
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) fail("INVALID_WEBMASTER_RESPONSE", "Yandex Webmaster вернул неожиданный JSON-ответ.");
    if (normalized.method === "listHosts") return { hosts: (Array.isArray(parsed.hosts) ? parsed.hosts : []).map(normalizeHost).filter(Boolean) };
    if (normalized.method === "getSummary") return { sqi: parsed.sqi ?? null, excluded_pages_count: parsed.excluded_pages_count ?? null, searchable_pages_count: parsed.searchable_pages_count ?? null, site_problems: parsed.site_problems && typeof parsed.site_problems === "object" ? parsed.site_problems : {} };
    if (normalized.method === "getDiagnostics") {
      const source = parsed.problems && typeof parsed.problems === "object" && !Array.isArray(parsed.problems) ? parsed.problems : parsed;
      const problems = {};
      for (const [code, value] of Object.entries(source || {})) if (value && typeof value === "object" && !Array.isArray(value)) problems[String(code)] = { severity: value.severity ?? null, state: value.state ?? null, last_state_update: value.last_state_update ?? null };
      return { problems };
    }
    if (normalized.method === "getPopularQueries") {
      const queries = Array.isArray(parsed.queries) ? parsed.queries.map((row) => ({ query_id: String(row?.query_id || ""), query_text: String(row?.query_text || ""), indicators: row?.indicators && typeof row.indicators === "object" && !Array.isArray(row.indicators) ? row.indicators : {} })) : [];
      return { queries, date_from: parsed.date_from ?? null, date_to: parsed.date_to ?? null, count: Number.isFinite(Number(parsed.count)) ? Number(parsed.count) : queries.length };
    }
    if (normalized.method === "getAllQueryHistory") return { indicators: normalizeIndicators(parsed.indicators) };
    if (normalized.method === "getQueryHistory") {
      const queries = Array.isArray(parsed.queries) ? parsed.queries.map((row) => ({
        query_id: String(row?.query_id || ""),
        query_text: String(row?.query_text || ""),
        indicators: normalizeIndicators(row?.indicators)
      })) : [];
      return { queries };
    }
    if (["getIndexingSamples", "getInSearchSamples"].includes(normalized.method)) {
      const candidateArrays = [parsed.samples, parsed.urls, parsed.items];
      const source = candidateArrays.find(Array.isArray) || [];
      return { count: Number.isFinite(Number(parsed.count)) ? Number(parsed.count) : source.length, samples: source.map(normalizeSampleRow).filter(Boolean) };
    }
    if (normalized.method === "getExportRegions") {
      const source = Array.isArray(parsed.regions) ? parsed.regions : Array.isArray(parsed.items) ? parsed.items : [];
      return { count: Number.isFinite(Number(parsed.count)) ? Number(parsed.count) : source.length, regions: source.map((row) => ({ id: Number.isFinite(Number(row?.id ?? row?.region_id)) ? Number(row?.id ?? row?.region_id) : null, name: String(row?.name ?? row?.region_name ?? "") })) };
    }
    if (normalized.method === "getExportLimits") {
      const source = Array.isArray(parsed.limits) ? parsed.limits : [];
      return { limits: source.map((row) => ({
        owner: String(row?.owner || ""),
        feature: String(row?.feature || ""),
        limit: Number.isFinite(Number(row?.limit)) ? Number(row.limit) : null,
        used: Number.isFinite(Number(row?.used)) ? Number(row.used) : null,
        remaining: Number.isFinite(Number(row?.remaining)) ? Number(row.remaining) : null,
        period_start: row?.period_start == null ? null : String(row.period_start),
        period_end: row?.period_end == null ? null : String(row.period_end),
        is_active: row?.is_active === true,
        tariff_id: row?.tariff_id == null ? null : String(row.tariff_id)
      })) };
    }
    if (normalized.method === "getExportDates") {
      const source = Array.isArray(parsed.dates) ? parsed.dates : [];
      return { dates: source.map(String), count: source.length };
    }
    if (normalized.method === "startQueryUrlExport") return {
      task_id: String(parsed.task_id || ""),
      free_quota_used: Number(parsed.free_quota_used || 0), pro_quota_used: Number(parsed.pro_quota_used || 0), total_quota_used: Number(parsed.total_quota_used || 0),
      free_quota_remaining: Number(parsed.free_quota_remaining || 0), pro_quota_remaining: Number(parsed.pro_quota_remaining || 0)
    };
    if (normalized.method === "getQueryUrlExportStatus") return {
      download_status: String(parsed.download_status || "UNKNOWN"),
      download_available: String(parsed.download_status || "") === "SUCCESS" && typeof parsed.url === "string" && parsed.url.length > 0,
      error_code: parsed.error_code == null ? null : String(parsed.error_code),
      error_message: parsed.error_message == null ? null : String(parsed.error_message)
    };
    fail("INVALID_WEBMASTER_RESPONSE", `Нормализация ответа для ${normalized.method} не определена.`);
  }

  function safeErrorPayload(status, rawText, parsed) {
    const candidate = parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : null;
    const code = candidate?.error_code || candidate?.code || candidate?.error?.code || candidate?.status || "YANDEX_WEBMASTER_API_ERROR";
    const message = candidate?.error_message || candidate?.message || candidate?.error?.message || candidate?.error || rawText || "Yandex Webmaster API error";
    return { http_status: Number(status || 0), code: String(code).slice(0, 160), message: String(message).slice(0, 2000) };
  }

  function commandFingerprint(command) {
    const json = JSON.stringify(command); let hash = 2166136261;
    for (let i = 0; i < json.length; i += 1) { hash ^= json.charCodeAt(i); hash = Math.imul(hash, 16777619); }
    return (hash >>> 0).toString(16).padStart(8, "0");
  }

  function buildResultEnvelope({ requestId, command, httpStatus, result, elapsedMs, metadata = {} }) {
    return {
      bridge: String(globalThis.YMBProduct?.BRIDGE_ID || "yandex-marketing-bridge"), version: productVersion(), service: "webmaster", operation: command?.method || null,
      request_id: requestId, run_id: metadata.run_id || null, status: metadata.status || (Number(httpStatus || 0) >= 200 && Number(httpStatus || 0) < 300 ? "OK" : "ERROR"),
      reason: metadata.reason || null, cost_estimate: metadata.cost_estimate || null, policy: metadata.policy || null, command, http_status: Number(httpStatus || 0), elapsed_ms: Number(elapsedMs || 0), result,
      ...(metadata.request_executed !== undefined ? { request_executed: metadata.request_executed } : {}), ...(metadata.automatic_retry !== undefined ? { automatic_retry: metadata.automatic_retry } : {})
    };
  }
  function formatResultEnvelope(envelope) { return `${RESULT_PREFIX}\n${JSON.stringify(envelope, null, 2)}`; }
  function formatResultReport(args) { return formatResultEnvelope(buildResultEnvelope(args)); }
  function buildSkippedEnvelope({ requestId, command, reason, metadata = {} }) { return buildResultEnvelope({ requestId, command, httpStatus: 0, elapsedMs: 0, metadata: { ...metadata, status: "SKIPPED", reason, request_executed: metadata.request_executed ?? false, automatic_retry: metadata.automatic_retry ?? false }, result: { skipped: true, reason } }); }
  function formatSkippedReport(args) { return formatResultEnvelope(buildSkippedEnvelope(args)); }
  function isCommandText(text) { return String(text || "").replace(/\u00a0/g, " ").trim().startsWith(PREFIX); }
  function isLocalMethod(method) { return LOCAL_METHODS.has(String(method || "")); }
  function isDownloadMethod(method) { return DOWNLOAD_METHODS.has(String(method || "")); }

  globalThis.WebmasterProtocol = Object.freeze({
    PREFIX, RESULT_PREFIX, BASE_URL, METHODS, LOCAL_METHODS, DOWNLOAD_METHODS, ORDER_BY, QUERY_INDICATORS, DEVICE_TYPES,
    MAX_EXPORT_PAYLOAD_ITEMS, MAX_EXPORT_CHUNK_SIZE,
    parseCommand, normalizeCommand, buildRequest, normalizeProviderResult, safeErrorPayload,
    commandFingerprint, buildResultEnvelope, formatResultEnvelope, formatResultReport, buildSkippedEnvelope, formatSkippedReport, isCommandText,
    isLocalMethod, isDownloadMethod
  });
})();
