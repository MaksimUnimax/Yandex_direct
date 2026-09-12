(() => {
  "use strict";

  const PREFIX = "DIRECT_API_V1";
  const RESULT_PREFIX = "DIRECT_RESULT_V1";
  const BASE_URL = "https://api.direct.yandex.com/json/v501";
  const REPORTS_URL = `${BASE_URL}/reports`;
  const METHODS = Object.freeze(["listCampaigns", "listAdGroups", "listAds", "listKeywords", "getCampaignPerformance"]);
  const METHOD_SET = new Set(METHODS);
  const JSON_SERVICE_BY_METHOD = Object.freeze({
    listCampaigns: "campaigns",
    listAdGroups: "adgroups",
    listAds: "ads",
    listKeywords: "keywords"
  });
  const CAMPAIGN_FIELDS = Object.freeze(["Id", "Name", "StartDate", "EndDate", "Type", "Status", "State", "Currency"]);
  const ADGROUP_FIELDS = Object.freeze(["Id", "Name", "CampaignId", "Status", "ServingStatus", "Type"]);
  const AD_FIELDS = Object.freeze(["Id", "CampaignId", "AdGroupId", "Status", "State", "Type", "Subtype"]);
  const KEYWORD_FIELDS = Object.freeze(["Id", "Keyword", "State", "Status", "ServingStatus", "AdGroupId", "CampaignId", "Bid", "ContextBid", "StrategyPriority"]);
  const REPORT_FIELDS = Object.freeze(["Date", "CampaignId", "CampaignName", "Impressions", "Clicks", "Cost"]);
  const FIELD_SETS = Object.freeze({
    listCampaigns: new Set(["method", "campaignIds", "limit", "offset"]),
    listAdGroups: new Set(["method", "campaignIds", "adGroupIds", "limit", "offset"]),
    listAds: new Set(["method", "campaignIds", "adGroupIds", "adIds", "limit", "offset"]),
    listKeywords: new Set(["method", "campaignIds", "adGroupIds", "keywordIds", "limit", "offset"]),
    getCampaignPerformance: new Set(["method", "dateFrom", "dateTo", "campaignIds", "limit", "offset"])
  });

  function productVersion() { return String(globalThis.YMBProduct?.VERSION || "0.1.1"); }
  function fail(code, message) { const error = new Error(message || code); error.code = code; throw error; }
  function text(value) { return String(value ?? "").trim(); }
  function clone(value) { return value == null ? value : JSON.parse(JSON.stringify(value)); }

  function asInteger(value, name, { defaultValue, min = 0, max = Number.MAX_SAFE_INTEGER } = {}) {
    const candidate = value === undefined ? defaultValue : value;
    if (typeof candidate !== "number" || !Number.isSafeInteger(candidate) || candidate < min || candidate > max) {
      fail("INVALID_FIELD", `${name} должен быть целым числом от ${min} до ${max}.`);
    }
    return candidate;
  }

  function asIdArray(value, name, { max, optional = true } = {}) {
    if (value === undefined || value === null) return optional ? [] : fail("MISSING_FIELD", `Отсутствует обязательное поле: ${name}`);
    if (!Array.isArray(value)) fail("INVALID_FIELD", `${name} должен быть массивом ID.`);
    if (value.length === 0) return optional ? [] : fail("INVALID_FIELD", `${name} должен быть непустым массивом ID.`);
    if (value.length > max) fail("TOO_MANY_IDS", `${name} содержит больше ${max} ID.`);
    const out = [];
    const seen = new Set();
    for (const item of value) {
      if (typeof item !== "number" || !Number.isSafeInteger(item) || item <= 0) fail("INVALID_FIELD", `${name} должен содержать только положительные safe integer ID.`);
      if (!seen.has(item)) { seen.add(item); out.push(item); }
    }
    return out;
  }

  function asDate(value, name) {
    if (value === undefined || value === null || value === "") fail("MISSING_FIELD", `Отсутствует обязательное поле: ${name}`);
    const candidate = text(value);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(candidate)) fail("INVALID_DATE", `${name} должен быть в формате YYYY-MM-DD.`);
    const [year, month, day] = candidate.split("-").map(Number);
    const date = new Date(Date.UTC(year, month - 1, day));
    if (date.getUTCFullYear() !== year || date.getUTCMonth() !== month - 1 || date.getUTCDate() !== day) fail("INVALID_DATE", `${name} содержит некорректную дату.`);
    return candidate;
  }

  function dateOrdinal(ymd) {
    const [year, month, day] = ymd.split("-").map(Number);
    return Math.floor(Date.UTC(year, month - 1, day) / 86400000);
  }

  function normalizePage(raw) {
    return {
      limit: asInteger(raw.limit, "limit", { defaultValue: raw.method === "getCampaignPerformance" ? 1000 : 100, min: 1, max: 1000 }),
      offset: asInteger(raw.offset, "offset", { defaultValue: 0, min: 0 })
    };
  }

  function requireSelector(normalized, names) {
    if (!names.some((name) => Array.isArray(normalized[name]) && normalized[name].length > 0)) {
      fail("MISSING_SELECTOR", `Для ${normalized.method} требуется хотя бы один ID-селектор: ${names.join(", ")}.`);
    }
  }

  function normalizeCommand(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) fail("INVALID_JSON_ROOT", "Команда должна быть JSON-объектом.");
    const method = text(raw.method);
    if (!method) fail("MISSING_FIELD", "Отсутствует обязательное поле: method");
    if (!METHOD_SET.has(method)) fail("UNSUPPORTED_METHOD", `Метод ${method} не разрешён.`);
    const allowed = FIELD_SETS[method];
    for (const key of Object.keys(raw)) if (!allowed.has(key)) fail("UNSUPPORTED_FIELD", `Поле ${key} не разрешено для ${method}.`);
    const page = normalizePage({ ...raw, method });

    if (method === "listCampaigns") {
      return Object.freeze({ method, campaignIds: Object.freeze(asIdArray(raw.campaignIds, "campaignIds", { max: 10 })), ...page });
    }
    if (method === "listAdGroups") {
      const normalized = { method, campaignIds: asIdArray(raw.campaignIds, "campaignIds", { max: 10 }), adGroupIds: asIdArray(raw.adGroupIds, "adGroupIds", { max: 1000 }), ...page };
      requireSelector(normalized, ["campaignIds", "adGroupIds"]);
      normalized.campaignIds = Object.freeze(normalized.campaignIds); normalized.adGroupIds = Object.freeze(normalized.adGroupIds);
      return Object.freeze(normalized);
    }
    if (method === "listAds") {
      const normalized = { method, campaignIds: asIdArray(raw.campaignIds, "campaignIds", { max: 10 }), adGroupIds: asIdArray(raw.adGroupIds, "adGroupIds", { max: 1000 }), adIds: asIdArray(raw.adIds, "adIds", { max: 1000 }), ...page };
      requireSelector(normalized, ["campaignIds", "adGroupIds", "adIds"]);
      normalized.campaignIds = Object.freeze(normalized.campaignIds); normalized.adGroupIds = Object.freeze(normalized.adGroupIds); normalized.adIds = Object.freeze(normalized.adIds);
      return Object.freeze(normalized);
    }
    if (method === "listKeywords") {
      const normalized = { method, campaignIds: asIdArray(raw.campaignIds, "campaignIds", { max: 10 }), adGroupIds: asIdArray(raw.adGroupIds, "adGroupIds", { max: 1000 }), keywordIds: asIdArray(raw.keywordIds, "keywordIds", { max: 1000 }), ...page };
      requireSelector(normalized, ["campaignIds", "adGroupIds", "keywordIds"]);
      normalized.campaignIds = Object.freeze(normalized.campaignIds); normalized.adGroupIds = Object.freeze(normalized.adGroupIds); normalized.keywordIds = Object.freeze(normalized.keywordIds);
      return Object.freeze(normalized);
    }

    const dateFrom = asDate(raw.dateFrom, "dateFrom");
    const dateTo = asDate(raw.dateTo, "dateTo");
    const span = dateOrdinal(dateTo) - dateOrdinal(dateFrom) + 1;
    if (span <= 0) fail("INVALID_DATE_RANGE", "dateFrom не может быть позже dateTo.");
    if (span > 31) fail("DATE_RANGE_TOO_LARGE", "Период Direct отчёта не может превышать 31 календарный день.");
    return Object.freeze({ method, dateFrom, dateTo, campaignIds: Object.freeze(asIdArray(raw.campaignIds, "campaignIds", { max: 10 })), ...page });
  }

  function parseCommand(sourceText) {
    const source = String(sourceText || "").replace(/\u00a0/g, " ").trim();
    if (!source.startsWith(PREFIX)) fail("NOT_DIRECT_COMMAND", `Команда должна начинаться с ${PREFIX}`);
    const rest = source.slice(PREFIX.length).trim();
    if (!rest) fail("MISSING_JSON", `После ${PREFIX} должен идти JSON-объект.`);
    let raw;
    try { raw = JSON.parse(rest); }
    catch (error) { fail("INVALID_JSON", `Некорректный JSON: ${error.message}`); }
    return normalizeCommand(raw);
  }

  function selectionFor(command) {
    const selection = {};
    if (command.method === "listCampaigns") {
      if (command.campaignIds?.length) selection.Ids = [...command.campaignIds];
      return selection;
    }
    if (command.campaignIds?.length) selection.CampaignIds = [...command.campaignIds];
    if (command.method === "listAdGroups") {
      if (command.adGroupIds?.length) selection.Ids = [...command.adGroupIds];
      return selection;
    }
    if (command.adGroupIds?.length) selection.AdGroupIds = [...command.adGroupIds];
    if (command.method === "listAds" && command.adIds?.length) selection.Ids = [...command.adIds];
    if (command.method === "listKeywords" && command.keywordIds?.length) selection.Ids = [...command.keywordIds];
    return selection;
  }

  function fieldsFor(command) {
    if (command.method === "listCampaigns") return CAMPAIGN_FIELDS;
    if (command.method === "listAdGroups") return ADGROUP_FIELDS;
    if (command.method === "listAds") return AD_FIELDS;
    if (command.method === "listKeywords") return KEYWORD_FIELDS;
    return REPORT_FIELDS;
  }

  function buildRequest(command, { reportName = "YMB-P5-report" } = {}) {
    const normalized = normalizeCommand(command);
    if (normalized.method !== "getCampaignPerformance") {
      const service = JSON_SERVICE_BY_METHOD[normalized.method];
      const body = {
        method: "get",
        params: {
          SelectionCriteria: selectionFor(normalized),
          FieldNames: [...fieldsFor(normalized)],
          Page: { Limit: normalized.limit, Offset: normalized.offset }
        }
      };
      return Object.freeze({ kind: "json", method: "POST", url: `${BASE_URL}/${service}`, body });
    }

    const criteria = { DateFrom: normalized.dateFrom, DateTo: normalized.dateTo };
    if (normalized.campaignIds.length) {
      criteria.Filter = [{ Field: "CampaignId", Operator: "IN", Values: normalized.campaignIds.map(String) }];
    }
    const safeReportName = text(reportName).replace(/[\r\n\t]/g, " ").slice(0, 200) || "YMB-P5-report";
    const body = {
      params: {
        SelectionCriteria: criteria,
        FieldNames: [...REPORT_FIELDS],
        ReportName: safeReportName,
        ReportType: "CAMPAIGN_PERFORMANCE_REPORT",
        DateRangeType: "CUSTOM_DATE",
        Format: "TSV",
        IncludeVAT: "YES",
        Page: { Limit: normalized.limit, Offset: normalized.offset }
      }
    };
    return Object.freeze({ kind: "report", method: "POST", url: REPORTS_URL, body });
  }

  function positiveId(value, name) {
    const number = typeof value === "number" ? value : Number(value);
    if (!Number.isSafeInteger(number) || number <= 0) fail("INVALID_DIRECT_RESPONSE", `Yandex Direct вернул некорректный ${name}.`);
    return number;
  }
  function nullableText(value) { return value === undefined || value === null ? null : String(value); }
  function exactNonNegativeInteger(value, name) {
    const source = typeof value === "number" ? String(value) : text(value);
    if (!/^\d+$/.test(source)) fail("INVALID_DIRECT_RESPONSE", `Yandex Direct вернул некорректный ${name}.`);
    const number = Number(source);
    if (!Number.isSafeInteger(number) || number < 0) fail("INVALID_DIRECT_RESPONSE", `Yandex Direct вернул ${name} за пределами safe integer.`);
    return number;
  }

  function normalizeCampaign(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) fail("INVALID_DIRECT_RESPONSE", "Некорректный Campaign объект.");
    return {
      id: positiveId(raw.Id, "Campaign.Id"),
      name: nullableText(raw.Name),
      start_date: nullableText(raw.StartDate),
      end_date: nullableText(raw.EndDate),
      type: nullableText(raw.Type),
      status: nullableText(raw.Status),
      state: nullableText(raw.State),
      currency: nullableText(raw.Currency)
    };
  }
  function normalizeAdGroup(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) fail("INVALID_DIRECT_RESPONSE", "Некорректный AdGroup объект.");
    return {
      id: positiveId(raw.Id, "AdGroup.Id"),
      name: nullableText(raw.Name),
      campaign_id: positiveId(raw.CampaignId, "AdGroup.CampaignId"),
      status: nullableText(raw.Status),
      serving_status: nullableText(raw.ServingStatus),
      type: nullableText(raw.Type)
    };
  }
  function normalizeAd(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) fail("INVALID_DIRECT_RESPONSE", "Некорректный Ad объект.");
    return {
      id: positiveId(raw.Id, "Ad.Id"),
      campaign_id: positiveId(raw.CampaignId, "Ad.CampaignId"),
      ad_group_id: positiveId(raw.AdGroupId, "Ad.AdGroupId"),
      status: nullableText(raw.Status),
      state: nullableText(raw.State),
      type: nullableText(raw.Type),
      subtype: nullableText(raw.Subtype)
    };
  }
  function normalizeKeyword(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) fail("INVALID_DIRECT_RESPONSE", "Некорректный Keyword объект.");
    return {
      id: positiveId(raw.Id, "Keyword.Id"),
      keyword: nullableText(raw.Keyword),
      state: nullableText(raw.State),
      status: nullableText(raw.Status),
      serving_status: nullableText(raw.ServingStatus),
      ad_group_id: positiveId(raw.AdGroupId, "Keyword.AdGroupId"),
      campaign_id: positiveId(raw.CampaignId, "Keyword.CampaignId"),
      bid_micros: raw.Bid === undefined || raw.Bid === null ? null : exactNonNegativeInteger(raw.Bid, "Keyword.Bid"),
      context_bid_micros: raw.ContextBid === undefined || raw.ContextBid === null ? null : exactNonNegativeInteger(raw.ContextBid, "Keyword.ContextBid"),
      strategy_priority: nullableText(raw.StrategyPriority)
    };
  }

  function limitedBy(result) {
    if (result?.LimitedBy === undefined || result?.LimitedBy === null) return null;
    const number = Number(result.LimitedBy);
    return Number.isSafeInteger(number) && number >= 0 ? number : null;
  }

  function providerError(parsed) {
    const value = parsed?.error;
    return value && typeof value === "object" && !Array.isArray(value) ? value : null;
  }
  function providerErrorCode(parsed) {
    const error = providerError(parsed);
    const value = error?.error_code ?? error?.code;
    const number = Number(value);
    return Number.isSafeInteger(number) ? number : null;
  }
  function providerErrorText(parsed) {
    const error = providerError(parsed);
    return text(error?.error_string || error?.message || error?.error_detail || "");
  }
  function providerRequestIdFromBody(parsed) {
    const error = providerError(parsed);
    return text(error?.request_id || parsed?.result?.RequestId || parsed?.request_id || "") || null;
  }

  function normalizeJsonProviderResult(command, parsed) {
    const normalized = normalizeCommand(command);
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) fail("INVALID_DIRECT_RESPONSE", "Yandex Direct вернул неожиданный JSON-ответ.");
    if (providerError(parsed)) fail("DIRECT_SEMANTIC_ERROR", "Yandex Direct вернул semantic error вместо result.");
    const result = parsed.result;
    if (!result || typeof result !== "object" || Array.isArray(result)) fail("INVALID_DIRECT_RESPONSE", "Yandex Direct не вернул result.");
    if (normalized.method === "listCampaigns") {
      if (!Array.isArray(result.Campaigns)) fail("INVALID_DIRECT_RESPONSE", "Yandex Direct не вернул Campaigns[].");
      return { campaigns: result.Campaigns.map(normalizeCampaign), limited_by: limitedBy(result) };
    }
    if (normalized.method === "listAdGroups") {
      if (!Array.isArray(result.AdGroups)) fail("INVALID_DIRECT_RESPONSE", "Yandex Direct не вернул AdGroups[].");
      return { ad_groups: result.AdGroups.map(normalizeAdGroup), limited_by: limitedBy(result) };
    }
    if (normalized.method === "listAds") {
      if (!Array.isArray(result.Ads)) fail("INVALID_DIRECT_RESPONSE", "Yandex Direct не вернул Ads[].");
      return { ads: result.Ads.map(normalizeAd), limited_by: limitedBy(result) };
    }
    if (normalized.method === "listKeywords") {
      if (!Array.isArray(result.Keywords)) fail("INVALID_DIRECT_RESPONSE", "Yandex Direct не вернул Keywords[].");
      return { keywords: result.Keywords.map(normalizeKeyword), limited_by: limitedBy(result) };
    }
    fail("INVALID_DIRECT_RESPONSE", "Для Reports требуется TSV-нормализатор.");
  }

  function parseTsvLine(line) {
    const fields = [];
    let current = ""; let quoted = false;
    for (let i = 0; i < line.length; i += 1) {
      const ch = line[i];
      if (quoted) {
        if (ch === '"' && line[i + 1] === '"') { current += '"'; i += 1; continue; }
        if (ch === '"') { quoted = false; continue; }
        current += ch; continue;
      }
      if (ch === '"') { quoted = true; continue; }
      if (ch === "\t") { fields.push(current); current = ""; continue; }
      current += ch;
    }
    if (quoted) fail("INVALID_DIRECT_REPORT", "Незакрытая кавычка в TSV отчёте Direct.");
    fields.push(current);
    return fields;
  }

  function normalizeReportResult(command, rawText) {
    const normalized = normalizeCommand(command);
    if (normalized.method !== "getCampaignPerformance") fail("INVALID_DIRECT_RESPONSE", "TSV ответ допустим только для getCampaignPerformance.");
    const source = String(rawText ?? "").replace(/^\uFEFF/, "").replace(/\r\n/g, "\n").replace(/\r/g, "\n");
    const lines = source.split("\n").filter((line) => line.length > 0);
    if (!lines.length) fail("INVALID_DIRECT_REPORT", "Yandex Direct вернул пустой TSV отчёт.");
    const header = parseTsvLine(lines[0]);
    if (header.length !== REPORT_FIELDS.length || header.some((value, index) => value !== REPORT_FIELDS[index])) {
      fail("INVALID_DIRECT_REPORT_HEADER", `Неожиданный TSV header Direct: ${header.join("|")}`);
    }
    const rows = [];
    for (let i = 1; i < lines.length; i += 1) {
      const values = parseTsvLine(lines[i]);
      if (values.length !== REPORT_FIELDS.length) fail("INVALID_DIRECT_REPORT_ROW", `TSV row ${i} имеет неверное число колонок.`);
      const [date, campaignId, campaignName, impressions, clicks, cost] = values;
      if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) fail("INVALID_DIRECT_REPORT_ROW", `TSV row ${i}: некорректная Date.`);
      rows.push({
        date,
        campaign_id: positiveId(campaignId, `TSV row ${i} CampaignId`),
        campaign_name: campaignName,
        impressions: exactNonNegativeInteger(impressions, `TSV row ${i} Impressions`),
        clicks: exactNonNegativeInteger(clicks, `TSV row ${i} Clicks`),
        cost_micros: exactNonNegativeInteger(cost, `TSV row ${i} Cost`)
      });
    }
    return { date_from: normalized.dateFrom, date_to: normalized.dateTo, rows, row_count: rows.length };
  }

  function parseUnitsHeader(value) {
    const source = text(value);
    const match = /^(\d+)\/(\d+)\/(\d+)$/.exec(source);
    if (!match) return null;
    const values = match.slice(1).map(Number);
    if (!values.every((number) => Number.isSafeInteger(number) && number >= 0)) return null;
    return { spent: values[0], remaining: values[1], daily_limit: values[2] };
  }

  function responseMetadata(headers, parsed = null) {
    const get = headers && typeof headers.get === "function" ? (name) => headers.get(name) : () => null;
    const requestId = text(get("RequestId") || get("Request-Id") || providerRequestIdFromBody(parsed) || "") || null;
    return { provider_request_id: requestId, provider_units: parseUnitsHeader(get("Units")) };
  }

  function safeErrorPayload(status, rawText, parsed) {
    const error = providerError(parsed);
    const providerCode = providerErrorCode(parsed);
    const providerMessage = providerErrorText(parsed);
    const fallback = text(rawText).slice(0, 2000) || "Yandex Direct API error";
    return {
      http_status: Number(status || 0),
      provider_code: providerCode,
      code: providerCode === null ? "YANDEX_DIRECT_API_ERROR" : `DIRECT_${providerCode}`,
      message: (providerMessage || fallback).slice(0, 2000),
      detail: error?.error_detail == null ? null : String(error.error_detail).slice(0, 2000),
      provider_request_id: providerRequestIdFromBody(parsed)
    };
  }

  function isInvalidTokenCompatibility1002(parsed) {
    if (providerErrorCode(parsed) !== 1002) return false;
    const source = `${providerErrorText(parsed)} ${text(providerError(parsed)?.error_detail)}`.toLowerCase();
    return /oauth|token|токен|авторизац/.test(source) && /invalid|incorrect|wrong|невер|некоррект|ист[её]к/.test(source);
  }

  function checkStateForProviderError(parsed) {
    const code = providerErrorCode(parsed);
    if (code === 53 || isInvalidTokenCompatibility1002(parsed)) return "INVALID_OR_EXPIRED";
    if (code === 54) return "NO_ACCESS";
    if (code === 58) return "APP_ACCESS_NOT_APPROVED";
    if (code === 513) return "DIRECT_ACCOUNT_MISSING";
    if (code === 3000) return "NO_API_ACCESS";
    if (code === 152) return "UNITS_EXHAUSTED";
    if (code === 506) return "CONCURRENCY_LIMIT";
    return "NOT_CHECKED";
  }

  function buildResultEnvelope({ requestId, command, httpStatus, result, elapsedMs, metadata = {} }) {
    const envelope = {
      bridge: String(globalThis.YMBProduct?.BRIDGE_ID || "yandex-marketing-bridge"),
      version: productVersion(),
      service: "direct",
      operation: command?.method || null,
      request_id: requestId,
      run_id: metadata.run_id || null,
      status: metadata.status || (Number(httpStatus || 0) >= 200 && Number(httpStatus || 0) < 300 ? "OK" : "ERROR"),
      reason: metadata.reason || null,
      cost_estimate: metadata.cost_estimate || null,
      policy: metadata.policy || null,
      command: clone(command),
      http_status: Number(httpStatus || 0),
      elapsed_ms: Number(elapsedMs || 0),
      result
    };
    if (metadata.provider_request_id !== undefined) envelope.provider_request_id = metadata.provider_request_id || null;
    if (metadata.provider_units !== undefined) envelope.provider_units = metadata.provider_units || null;
    if (metadata.request_executed !== undefined) envelope.request_executed = metadata.request_executed;
    if (metadata.automatic_retry !== undefined) envelope.automatic_retry = metadata.automatic_retry;
    return envelope;
  }

  function formatResultEnvelope(envelope) { return `${RESULT_PREFIX}\n${JSON.stringify(envelope, null, 2)}`; }
  function buildSkippedEnvelope({ requestId, command, reason, metadata = {} }) {
    return buildResultEnvelope({ requestId, command, httpStatus: 0, elapsedMs: 0, result: { skipped: true, reason }, metadata: { ...metadata, status: "SKIPPED", reason, request_executed: metadata.request_executed ?? false, automatic_retry: false } });
  }
  function formatSkippedReport(args) { return formatResultEnvelope(buildSkippedEnvelope(args)); }
  function commandFingerprint(command) {
    const json = JSON.stringify(command); let hash = 2166136261;
    for (let i = 0; i < json.length; i += 1) { hash ^= json.charCodeAt(i); hash = Math.imul(hash, 16777619); }
    return (hash >>> 0).toString(16).padStart(8, "0");
  }
  function isCommandText(value) { return String(value || "").replace(/\u00a0/g, " ").trim().startsWith(PREFIX); }

  globalThis.DirectProtocol = Object.freeze({
    PREFIX, RESULT_PREFIX, BASE_URL, REPORTS_URL, METHODS,
    CAMPAIGN_FIELDS, ADGROUP_FIELDS, AD_FIELDS, KEYWORD_FIELDS, REPORT_FIELDS,
    parseCommand, normalizeCommand, buildRequest,
    normalizeJsonProviderResult, normalizeReportResult,
    providerError, providerErrorCode, providerErrorText, providerRequestIdFromBody,
    parseUnitsHeader, responseMetadata, safeErrorPayload,
    isInvalidTokenCompatibility1002, checkStateForProviderError,
    buildResultEnvelope, formatResultEnvelope, buildSkippedEnvelope, formatSkippedReport,
    commandFingerprint, isCommandText
  });
})();
