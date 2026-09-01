(() => {
  "use strict";

  const PREFIX = "WEBMASTER_API_V1";
  const RESULT_PREFIX = "WEBMASTER_RESULT_V1";
  const BASE_URL = "https://api.webmaster.yandex.net/v4";
  const METHODS = Object.freeze([
    "listHosts", "getHostInfo", "getSummary", "getDiagnostics", "getPopularQueries",
    "getAllQueryHistory", "getQueryHistory",
    "getIndexingSamples", "getInSearchSamples",
    "getExportRegions", "getExportLimits", "getExportDates",
    "startQueryUrlExport", "getQueryUrlExportStatus", "collectQueryUrlExport", "readQueryUrlExportChunk"
  ]);
  const METHOD_SET = new Set(METHODS);
  const ORDER_BY = new Set(["TOTAL_SHOWS", "TOTAL_CLICKS"]);
  const QUERY_INDICATORS = new Set(["TOTAL_SHOWS", "TOTAL_CLICKS", "AVG_SHOW_POSITION", "AVG_CLICK_POSITION"]);
  const DEVICE_TYPES = new Set(["ALL", "DESKTOP", "MOBILE_AND_TABLET", "MOBILE", "TABLET"]);
  const DOWNLOAD_STATUSES = new Set(["IN_PROGRESS", "SUCCESS", "FAILED"]);
  const HOST_DATA_STATUSES = new Set(["NOT_LOADED", "NOT_INDEXED", "OK"]);
  const LOCAL_METHODS = new Set(["readQueryUrlExportChunk"]);
  const DOWNLOAD_METHODS = new Set(["collectQueryUrlExport"]);
  const COMMON_FIELDS = new Set(["method"]);
  const HOST_FIELDS = new Set(["method", "hostId"]);
  const POPULAR_FIELDS = new Set(["method", "hostId", "orderBy", "queryIndicator", "deviceTypeIndicator", "dateFrom", "dateTo", "offset", "limit"]);
  const HISTORY_ALL_FIELDS = new Set(["method", "hostId", "queryIndicators", "deviceTypeIndicator", "dateFrom", "dateTo"]);
  const HISTORY_ONE_FIELDS = new Set(["method", "hostId", "queryId", "queryIndicators", "deviceTypeIndicator", "dateFrom", "dateTo"]);
  const SAMPLE_FIELDS = new Set(["method", "hostId", "offset", "limit"]);
  const REGION_FIELDS = new Set(["method", "hostId", "filter", "limit"]);
  const EXPORT_START_FIELDS = new Set(["method", "hostId", "dates", "paths", "regionIds", "useProTariff", "confirmQuota", "expectedQuotaUnits", "confirmProTariff"]);
  const EXPORT_STATUS_FIELDS = new Set(["method", "hostId", "taskId"]);
  const EXPORT_COLLECT_FIELDS = new Set(["method", "hostId", "taskId", "previewLimit"]);
  const EXPORT_CHUNK_FIELDS = new Set(["method", "taskId", "offset", "limit"]);

  function productVersion() { return String(globalThis.YMBProduct?.VERSION || "0.1.4"); }
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

  function asInteger(value, name, { defaultValue, min = 0, max = Number.MAX_SAFE_INTEGER, required = false } = {}) {
    if ((value === undefined || value === null || value === "") && required) fail("MISSING_FIELD", `Отсутствует обязательное поле: ${name}`);
    const candidate = value === undefined || value === null || value === "" ? defaultValue : value;
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

  function asDate(value, name, { dateOnly = false } = {}) {
    const text = asString(value, name, { required: false, max: 64 });
    if (text === undefined) return undefined;
    if (dateOnly) {
      if (!/^\d{4}-\d{2}-\d{2}$/.test(text) || Number.isNaN(Date.parse(`${text}T00:00:00Z`))) fail("INVALID_DATE", `${name} должен быть датой YYYY-MM-DD.`);
      return text;
    }
    if (!/^\d{4}-\d{2}-\d{2}(?:[Tt ][0-9:.+\-Zz]+)?$/.test(text) || Number.isNaN(Date.parse(text))) fail("INVALID_DATE", `${name} должен быть корректной датой или RFC3339 datetime.`);
    return text;
  }

  function asStringArray(value, name, { min = 1, max = 100, itemMax = 2000, normalizeItem } = {}) {
    if (!Array.isArray(value) || value.length < min || value.length > max) fail("INVALID_FIELD", `${name} должен быть массивом от ${min} до ${max} элементов.`);
    const out = value.map((item, index) => {
      const text = asString(item, `${name}[${index}]`, { required: true, max: itemMax });
      return normalizeItem ? normalizeItem(text, index) : text;
    });
    if (new Set(out).size !== out.length) fail("DUPLICATE_FIELD_VALUE", `${name} не должен содержать дубликаты.`);
    return Object.freeze(out);
  }

  function asPositiveIntegerArray(value, name, { max = 1000, defaultValue = [] } = {}) {
    const source = value === undefined ? defaultValue : value;
    if (!Array.isArray(source) || source.length > max) fail("INVALID_FIELD", `${name} должен быть массивом не более ${max} элементов.`);
    const out = source.map((item, index) => asInteger(item, `${name}[${index}]`, { min: 1, max: 2147483647, required: true }));
    if (new Set(out).size !== out.length) fail("DUPLICATE_FIELD_VALUE", `${name} не должен содержать дубликаты.`);
    return Object.freeze(out);
  }

  function asQueryIndicators(value) {
    if (value === undefined) return Object.freeze([...QUERY_INDICATORS]);
    if (!Array.isArray(value) || value.length < 1 || value.length > QUERY_INDICATORS.size) fail("INVALID_FIELD", "queryIndicators должен быть непустым массивом документированных индикаторов.");
    const out = value.map((item) => asEnum(item, "queryIndicators", QUERY_INDICATORS, { required: true }));
    if (new Set(out).size !== out.length) fail("DUPLICATE_FIELD_VALUE", "queryIndicators не должен содержать дубликаты.");
    return Object.freeze(out);
  }

  function normalizeTaskId(value) {
    const taskId = asString(value, "taskId", { required: true, max: 128 });
    if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(taskId)) fail("INVALID_TASK_ID", "taskId должен быть UUID.");
    return taskId;
  }

  function allowedFieldsForMethod(method) {
    if (method === "listHosts") return COMMON_FIELDS;
    if (["getHostInfo", "getSummary", "getDiagnostics", "getExportLimits", "getExportDates"].includes(method)) return HOST_FIELDS;
    if (method === "getPopularQueries") return POPULAR_FIELDS;
    if (method === "getAllQueryHistory") return HISTORY_ALL_FIELDS;
    if (method === "getQueryHistory") return HISTORY_ONE_FIELDS;
    if (["getIndexingSamples", "getInSearchSamples"].includes(method)) return SAMPLE_FIELDS;
    if (method === "getExportRegions") return REGION_FIELDS;
    if (method === "startQueryUrlExport") return EXPORT_START_FIELDS;
    if (method === "getQueryUrlExportStatus") return EXPORT_STATUS_FIELDS;
    if (method === "collectQueryUrlExport") return EXPORT_COLLECT_FIELDS;
    if (method === "readQueryUrlExportChunk") return EXPORT_CHUNK_FIELDS;
    return COMMON_FIELDS;
  }

  function validateFields(raw, allowed, method) {
    for (const key of Object.keys(raw)) if (!allowed.has(key)) fail("UNSUPPORTED_FIELD", `Поле ${key} не разрешено для ${method}.`);
  }

  function normalizeHistoryRange(raw, method, { withQueryId = false } = {}) {
    const hostId = asString(raw.hostId, "hostId", { required: true, max: 1000 });
    const queryIndicators = asQueryIndicators(raw.queryIndicators);
    const deviceTypeIndicator = asEnum(raw.deviceTypeIndicator, "deviceTypeIndicator", DEVICE_TYPES, { defaultValue: "ALL" });
    const dateFrom = asDate(raw.dateFrom, "dateFrom");
    const dateTo = asDate(raw.dateTo, "dateTo");
    if (dateFrom && dateTo && Date.parse(dateFrom) > Date.parse(dateTo)) fail("INVALID_DATE_RANGE", "dateFrom не может быть позже dateTo.");
    const out = { method, hostId, queryIndicators, deviceTypeIndicator };
    if (withQueryId) out.queryId = asString(raw.queryId, "queryId", { required: true, max: 1000 });
    if (dateFrom !== undefined) out.dateFrom = dateFrom;
    if (dateTo !== undefined) out.dateTo = dateTo;
    return Object.freeze(out);
  }

  function normalizeCommand(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) fail("INVALID_JSON_ROOT", "Команда должна быть JSON-объектом.");
    const method = asString(raw.method, "method", { required: true, max: 80 });
    if (!METHOD_SET.has(method)) fail("UNSUPPORTED_METHOD", `Метод ${method} не разрешён.`);
    validateFields(raw, allowedFieldsForMethod(method), method);

    if (method === "listHosts") return Object.freeze({ method });
    if (["getHostInfo", "getSummary", "getDiagnostics", "getExportLimits", "getExportDates"].includes(method)) return Object.freeze({ method, hostId: asString(raw.hostId, "hostId", { required: true, max: 1000 }) });

    if (method === "getPopularQueries") {
      const hostId = asString(raw.hostId, "hostId", { required: true, max: 1000 });
      const orderBy = asEnum(raw.orderBy, "orderBy", ORDER_BY, { required: true });
      const queryIndicator = asEnum(raw.queryIndicator, "queryIndicator", QUERY_INDICATORS);
      const deviceTypeIndicator = asEnum(raw.deviceTypeIndicator, "deviceTypeIndicator", DEVICE_TYPES, { defaultValue: "ALL" });
      const dateFrom = asDate(raw.dateFrom, "dateFrom");
      const dateTo = asDate(raw.dateTo, "dateTo");
      if (dateFrom && dateTo && Date.parse(dateFrom) > Date.parse(dateTo)) fail("INVALID_DATE_RANGE", "dateFrom не может быть позже dateTo.");
      const normalized = { method, hostId, orderBy, deviceTypeIndicator, offset: asInteger(raw.offset, "offset", { defaultValue: 0, min: 0 }), limit: asInteger(raw.limit, "limit", { defaultValue: 500, min: 1, max: 500 }) };
      if (queryIndicator !== undefined) normalized.queryIndicator = queryIndicator;
      if (dateFrom !== undefined) normalized.dateFrom = dateFrom;
      if (dateTo !== undefined) normalized.dateTo = dateTo;
      return Object.freeze(normalized);
    }

    if (method === "getAllQueryHistory") return normalizeHistoryRange(raw, method);
    if (method === "getQueryHistory") return normalizeHistoryRange(raw, method, { withQueryId: true });

    if (["getIndexingSamples", "getInSearchSamples"].includes(method)) {
      return Object.freeze({ method, hostId: asString(raw.hostId, "hostId", { required: true, max: 1000 }), offset: asInteger(raw.offset, "offset", { defaultValue: 0, min: 0, max: 50000 }), limit: asInteger(raw.limit, "limit", { defaultValue: 50, min: 1, max: 100 }) });
    }

    if (method === "getExportRegions") {
      const out = { method, hostId: asString(raw.hostId, "hostId", { required: true, max: 1000 }) };
      const filter = asString(raw.filter, "filter", { max: 300 });
      if (filter !== undefined) out.filter = filter;
      if (raw.limit !== undefined) out.limit = asInteger(raw.limit, "limit", { min: 1, max: 5000 });
      return Object.freeze(out);
    }

    if (method === "startQueryUrlExport") {
      const hostId = asString(raw.hostId, "hostId", { required: true, max: 1000 });
      const dates = asStringArray(raw.dates, "dates", { min: 1, max: 100, itemMax: 10, normalizeItem: (value, index) => asDate(value, `dates[${index}]`, { dateOnly: true }) });
      const paths = asStringArray(raw.paths, "paths", { min: 1, max: 100, itemMax: 4000, normalizeItem: (value, index) => {
        if (!value.startsWith("/")) fail("INVALID_EXPORT_PATH", `paths[${index}] должен начинаться с '/'.`);
        return value;
      } });
      if (dates.length + paths.length > 100) fail("EXPORT_PAYLOAD_CARDINALITY_LIMIT", "Суммарное количество dates + paths не должно превышать 100.");
      const regionIds = asPositiveIntegerArray(raw.regionIds, "regionIds", { max: 5000, defaultValue: [] });
      const useProTariff = raw.useProTariff === true;
      if (raw.useProTariff !== undefined && typeof raw.useProTariff !== "boolean") fail("INVALID_FIELD", "useProTariff должен быть boolean.");
      const quotaUnits = dates.length * paths.length;
      if (raw.confirmQuota !== true) fail("EXPORT_QUOTA_CONFIRM_REQUIRED", `startQueryUrlExport требует confirmQuota:true. Проекция расхода: ${quotaUnits}.`);
      const expectedQuotaUnits = asInteger(raw.expectedQuotaUnits, "expectedQuotaUnits", { min: 1, max: 100000000, required: true });
      if (expectedQuotaUnits !== quotaUnits) fail("EXPORT_QUOTA_PROJECTION_MISMATCH", `expectedQuotaUnits=${expectedQuotaUnits}, но paths×dates=${quotaUnits}.`);
      if (!useProTariff && quotaUnits > 100) fail("EXPORT_BASE_QUOTA_REQUEST_TOO_LARGE", "Базовый режим не может подтверждать выгрузку более 100 quota units за одну команду.");
      if (useProTariff && raw.confirmProTariff !== true) fail("EXPORT_PRO_TARIFF_CONFIRM_REQUIRED", "useProTariff:true требует confirmProTariff:true.");
      return Object.freeze({ method, hostId, dates, paths, regionIds, useProTariff, confirmQuota: true, expectedQuotaUnits, confirmProTariff: useProTariff ? true : false });
    }

    if (method === "getQueryUrlExportStatus") return Object.freeze({ method, hostId: asString(raw.hostId, "hostId", { required: true, max: 1000 }), taskId: normalizeTaskId(raw.taskId) });
    if (method === "collectQueryUrlExport") return Object.freeze({ method, hostId: asString(raw.hostId, "hostId", { required: true, max: 1000 }), taskId: normalizeTaskId(raw.taskId), previewLimit: asInteger(raw.previewLimit, "previewLimit", { defaultValue: 50, min: 0, max: 200 }) });
    return Object.freeze({ method, taskId: normalizeTaskId(raw.taskId), offset: asInteger(raw.offset, "offset", { defaultValue: 0, min: 0, max: 100000000 }), limit: asInteger(raw.limit, "limit", { defaultValue: 200, min: 1, max: 500 }) });
  }

  function parseCommand(text) {
    const source = String(text || "").replace(/\u00a0/g, " ").trim();
    if (!source.startsWith(PREFIX)) fail("NOT_WEBMASTER_COMMAND", `Команда должна начинаться с ${PREFIX}`);
    const rest = source.slice(PREFIX.length).trim();
    if (!rest) fail("MISSING_JSON", `После ${PREFIX} должен идти JSON-объект.`);
    let raw;
    try { raw = JSON.parse(rest); } catch (error) { fail("INVALID_JSON", `Некорректный JSON: ${error.message}`); }
    return normalizeCommand(raw);
  }

  function normalizeUserId(userId) {
    const text = String(userId ?? "").trim();
    if (!/^\d+$/.test(text)) fail("WEBMASTER_USER_ID_MISSING", "Webmaster user_id отсутствует или некорректен.");
    return text;
  }

  function queryString(entries) {
    const out = [];
    for (const [key, value] of entries) {
      if (value === undefined || value === null || value === "") continue;
      const values = Array.isArray(value) ? value : [value];
      for (const item of values) out.push(`${encodeURIComponent(key)}=${encodeURIComponent(String(item))}`);
    }
    return out.join("&");
  }

  function projectQueryUrlExport(command) {
    const normalized = normalizeCommand(command);
    if (normalized.method !== "startQueryUrlExport") fail("EXPORT_START_REQUIRED", "projectQueryUrlExport требует startQueryUrlExport manifest.");
    return Object.freeze({
      paths: normalized.paths.length,
      dates: normalized.dates.length,
      regions: normalized.regionIds.length,
      quota_units: normalized.paths.length * normalized.dates.length,
      payload_cardinality: normalized.paths.length + normalized.dates.length,
      tariff_mode: normalized.useProTariff ? "PRO" : "BASE"
    });
  }

  function buildRequest(command, userId) {
    const normalized = normalizeCommand(command);
    if (LOCAL_METHODS.has(normalized.method) || DOWNLOAD_METHODS.has(normalized.method)) fail("LOCAL_METHOD_NO_API_REQUEST", `${normalized.method} не строит запрос к api.webmaster.yandex.net.`);
    const uid = normalizeUserId(userId);
    const userBase = `${BASE_URL}/user/${encodeURIComponent(uid)}`;
    if (normalized.method === "listHosts") return Object.freeze({ method: "GET", url: `${userBase}/hosts` });
    const hostBase = `${userBase}/hosts/${encodeURIComponent(normalized.hostId)}`;
    if (normalized.method === "getHostInfo") return Object.freeze({ method: "GET", url: hostBase });
    if (normalized.method === "getSummary") return Object.freeze({ method: "GET", url: `${hostBase}/summary` });
    if (normalized.method === "getDiagnostics") return Object.freeze({ method: "GET", url: `${hostBase}/diagnostics` });
    if (normalized.method === "getPopularQueries") {
      const qs = queryString([["order_by", normalized.orderBy], ["query_indicator", normalized.queryIndicator], ["device_type_indicator", normalized.deviceTypeIndicator], ["date_from", normalized.dateFrom], ["date_to", normalized.dateTo], ["offset", normalized.offset], ["limit", normalized.limit]]);
      return Object.freeze({ method: "GET", url: `${hostBase}/search-queries/popular?${qs}` });
    }
    if (normalized.method === "getAllQueryHistory" || normalized.method === "getQueryHistory") {
      const base = normalized.method === "getAllQueryHistory" ? `${hostBase}/search-queries/all/history` : `${hostBase}/search-queries/${encodeURIComponent(normalized.queryId)}/history`;
      const qs = queryString([["query_indicator", normalized.queryIndicators], ["device_type_indicator", normalized.deviceTypeIndicator], ["date_from", normalized.dateFrom], ["date_to", normalized.dateTo]]);
      return Object.freeze({ method: "GET", url: `${base}${qs ? `?${qs}` : ""}` });
    }
    if (normalized.method === "getIndexingSamples") return Object.freeze({ method: "GET", url: `${hostBase}/indexing/samples?${queryString([["offset", normalized.offset], ["limit", normalized.limit]])}` });
    if (normalized.method === "getInSearchSamples") return Object.freeze({ method: "GET", url: `${hostBase}/search-urls/in-search/samples?${queryString([["offset", normalized.offset], ["limit", normalized.limit]])}` });
    if (normalized.method === "getExportRegions") {
      const qs = queryString([["filter", normalized.filter], ["limit", normalized.limit]]);
      return Object.freeze({ method: "GET", url: `${hostBase}/pro/regions${qs ? `?${qs}` : ""}` });
    }
    if (normalized.method === "getExportLimits") return Object.freeze({ method: "GET", url: `${hostBase}/pro/limits` });
    if (normalized.method === "getExportDates") return Object.freeze({ method: "GET", url: `${hostBase}/pro/serp/dates` });
    if (normalized.method === "startQueryUrlExport") {
      return Object.freeze({ method: "POST", url: `${hostBase}/pro/serp/queries/download/`, body: { dates: [...normalized.dates], paths: [...normalized.paths], region_ids: [...normalized.regionIds], use_pro_tariff: normalized.useProTariff ? "true" : "false" } });
    }
    return Object.freeze({ method: "GET", url: `${hostBase}/pro/serp/queries/download/${encodeURIComponent(normalized.taskId)}` });
  }

  function normalizeHost(raw, { includeReadiness = false } = {}) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) return null;
    const out = { host_id: String(raw.host_id || ""), ascii_host_url: String(raw.ascii_host_url || ""), unicode_host_url: String(raw.unicode_host_url || ""), verified: raw.verified === true };
    if (raw.main_mirror && typeof raw.main_mirror === "object" && !Array.isArray(raw.main_mirror)) out.main_mirror = { host_id: String(raw.main_mirror.host_id || ""), ascii_host_url: String(raw.main_mirror.ascii_host_url || ""), unicode_host_url: String(raw.main_mirror.unicode_host_url || ""), verified: raw.main_mirror.verified === true };
    if (includeReadiness) {
      const hostDataStatus = raw.host_data_status == null ? null : String(raw.host_data_status);
      out.host_data_status = hostDataStatus;
      out.webmaster_data_ready = hostDataStatus === "OK";
      if (raw.host_display_name != null) out.host_display_name = String(raw.host_display_name);
    }
    return out;
  }

  function normalizeIndicatorMap(raw) {
    const source = raw && typeof raw === "object" && !Array.isArray(raw) ? raw : {};
    const indicators = {};
    for (const key of QUERY_INDICATORS) {
      const rows = Array.isArray(source[key]) ? source[key] : null;
      if (!rows) continue;
      indicators[key] = rows.map((row) => ({ date: row?.date ?? null, value: Number.isFinite(Number(row?.value)) ? Number(row.value) : row?.value ?? null }));
    }
    return indicators;
  }

  function normalizeSamples(parsed, kind) {
    const samples = Array.isArray(parsed.samples) ? parsed.samples.map((row) => kind === "indexing"
      ? { url: String(row?.url || ""), status: row?.status ?? null, http_code: Number.isFinite(Number(row?.http_code)) ? Number(row.http_code) : null, access_date: row?.access_date ?? null }
      : { url: String(row?.url || ""), last_access: row?.last_access ?? null, title: String(row?.title || "") }) : [];
    return { count: Number.isFinite(Number(parsed.count)) ? Number(parsed.count) : samples.length, samples };
  }

  function normalizeProviderResult(command, parsed) {
    const normalized = normalizeCommand(command);
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) fail("INVALID_WEBMASTER_RESPONSE", "Yandex Webmaster вернул неожиданный JSON-ответ.");
    if (normalized.method === "listHosts") return { hosts: (Array.isArray(parsed.hosts) ? parsed.hosts : []).map((host) => normalizeHost(host)).filter(Boolean) };
    if (normalized.method === "getHostInfo") {
      const host = normalizeHost(parsed, { includeReadiness: true });
      if (!host) fail("INVALID_WEBMASTER_RESPONSE", "Yandex Webmaster не вернул корректную информацию о сайте.");
      return host;
    }
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
    if (normalized.method === "getAllQueryHistory" || normalized.method === "getQueryHistory") return { ...(parsed.query_id !== undefined ? { query_id: String(parsed.query_id) } : {}), ...(parsed.query_text !== undefined ? { query_text: String(parsed.query_text) } : {}), indicators: normalizeIndicatorMap(parsed.indicators) };
    if (normalized.method === "getIndexingSamples") return normalizeSamples(parsed, "indexing");
    if (normalized.method === "getInSearchSamples") return normalizeSamples(parsed, "search");
    if (normalized.method === "getExportRegions") return { regions: (Array.isArray(parsed.regions) ? parsed.regions : []).map((row) => ({ id: Number(row?.id), name: String(row?.name || "") })).filter((row) => Number.isSafeInteger(row.id) && row.id > 0) };
    if (normalized.method === "getExportLimits") return { limits: (Array.isArray(parsed.limits) ? parsed.limits : []).map((row) => ({ owner: String(row?.owner || ""), feature: String(row?.feature || ""), limit: Number(row?.limit || 0), used: Number(row?.used || 0), remaining: Number(row?.remaining || 0), period_start: row?.period_start ?? null, period_end: row?.period_end ?? null, is_active: row?.is_active === true, tariff_id: row?.tariff_id == null ? null : String(row.tariff_id) })) };
    if (normalized.method === "getExportDates") return { dates: (Array.isArray(parsed.dates) ? parsed.dates : []).map(String) };
    if (normalized.method === "startQueryUrlExport") {
      const taskId = normalizeTaskId(parsed.task_id);
      return { task_id: taskId, free_quota_used: Number(parsed.free_quota_used || 0), pro_quota_used: Number(parsed.pro_quota_used || 0), total_quota_used: Number(parsed.total_quota_used || 0), free_quota_remaining: Number(parsed.free_quota_remaining || 0), pro_quota_remaining: Number(parsed.pro_quota_remaining || 0), projection: projectQueryUrlExport(normalized) };
    }
    if (normalized.method === "getQueryUrlExportStatus") {
      const status = asEnum(parsed.download_status, "download_status", DOWNLOAD_STATUSES, { required: true });
      const out = { download_status: status };
      if (parsed.url != null) out.url = String(parsed.url);
      if (parsed.error_code != null) out.error_code = String(parsed.error_code);
      if (parsed.error_message != null) out.error_message = String(parsed.error_message);
      return out;
    }
    fail("LOCAL_RESULT_NORMALIZATION_REQUIRED", `${normalized.method} нормализуется локальным export runtime.`);
  }

  function safeErrorPayload(status, rawText, parsed) {
    const candidate = parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : null;
    const code = candidate?.error_code || candidate?.code || candidate?.error?.code || candidate?.status || "YANDEX_WEBMASTER_API_ERROR";
    const message = candidate?.error_message || candidate?.message || candidate?.error?.message || candidate?.error || rawText || "Yandex Webmaster API error";
    const out = { http_status: Number(status || 0), code: String(code).slice(0, 160), message: String(message).slice(0, 2000) };
    if (Array.isArray(candidate?.unavailable_dates)) out.unavailable_dates = candidate.unavailable_dates.map(String);
    if (Number.isFinite(Number(candidate?.limit))) out.limit = Number(candidate.limit);
    return out;
  }

  function commandFingerprint(command) {
    const json = JSON.stringify(normalizeCommand(command));
    let hash = 2166136261;
    for (let i = 0; i < json.length; i += 1) { hash ^= json.charCodeAt(i); hash = Math.imul(hash, 16777619); }
    return (hash >>> 0).toString(16).padStart(8, "0");
  }

  function buildResultEnvelope({ requestId, command, httpStatus, result, elapsedMs, metadata = {} }) {
    return { bridge: String(globalThis.YMBProduct?.BRIDGE_ID || "yandex-marketing-bridge"), version: productVersion(), service: "webmaster", operation: command?.method || null, request_id: requestId, run_id: metadata.run_id || null, status: metadata.status || (Number(httpStatus || 0) >= 200 && Number(httpStatus || 0) < 300 ? "OK" : "ERROR"), reason: metadata.reason || null, cost_estimate: metadata.cost_estimate || null, policy: metadata.policy || null, command, http_status: Number(httpStatus || 0), elapsed_ms: Number(elapsedMs || 0), result, ...(metadata.request_executed !== undefined ? { request_executed: metadata.request_executed } : {}), ...(metadata.automatic_retry !== undefined ? { automatic_retry: metadata.automatic_retry } : {}) };
  }

  function formatResultEnvelope(envelope) { return `${RESULT_PREFIX}\n${JSON.stringify(envelope, null, 2)}`; }
  function formatResultReport(args) { return formatResultEnvelope(buildResultEnvelope(args)); }
  function buildSkippedEnvelope({ requestId, command, reason, metadata = {} }) { return buildResultEnvelope({ requestId, command, httpStatus: 0, elapsedMs: 0, metadata: { ...metadata, status: "SKIPPED", reason, request_executed: metadata.request_executed ?? false, automatic_retry: metadata.automatic_retry ?? false }, result: { skipped: true, reason } }); }
  function formatSkippedReport(args) { return formatResultEnvelope(buildSkippedEnvelope(args)); }
  function isCommandText(text) { return String(text || "").replace(/\u00a0/g, " ").trim().startsWith(PREFIX); }
  function isLocalMethod(method) { return LOCAL_METHODS.has(String(method || "")); }
  function isDownloadMethod(method) { return DOWNLOAD_METHODS.has(String(method || "")); }

  globalThis.WebmasterProtocol = Object.freeze({
    PREFIX, RESULT_PREFIX, BASE_URL, METHODS, ORDER_BY, QUERY_INDICATORS, DEVICE_TYPES, DOWNLOAD_STATUSES, HOST_DATA_STATUSES,
    parseCommand, normalizeCommand, buildRequest, normalizeProviderResult, safeErrorPayload, projectQueryUrlExport,
    commandFingerprint, buildResultEnvelope, formatResultEnvelope, formatResultReport, buildSkippedEnvelope, formatSkippedReport,
    isCommandText, isLocalMethod, isDownloadMethod
  });
})();