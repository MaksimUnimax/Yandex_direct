(() => {
  "use strict";

  const PREFIX = "SEARCH_API_V1";
  const RESULT_PREFIX = "SEARCH_RESULT_V1";
  const ENDPOINT = "/v2/web/search";
  const GEN_ENDPOINT = "/v2/gen/search";
  const RESPONSE_FORMAT = "FORMAT_XML";
  const CONSERVATIVE_SYNC_COST_RUB = 0.488;
  const GEN_SEARCH_SYNC_COST_RUB = 5.08;

  function productVersion() { return String(globalThis.YMBProduct?.VERSION || "0.1.1"); }

  const SEARCH_TYPES = new Set([
    "SEARCH_TYPE_RU", "SEARCH_TYPE_TR", "SEARCH_TYPE_COM",
    "SEARCH_TYPE_KK", "SEARCH_TYPE_BE", "SEARCH_TYPE_UZ"
  ]);
  const FAMILY_MODES = new Set(["FAMILY_MODE_NONE", "FAMILY_MODE_MODERATE", "FAMILY_MODE_STRICT"]);
  const FIX_TYPO_MODES = new Set(["FIX_TYPO_MODE_ON", "FIX_TYPO_MODE_OFF"]);
  const SORT_MODES = new Set(["SORT_MODE_BY_RELEVANCE", "SORT_MODE_BY_TIME"]);
  const SORT_ORDERS = new Set(["SORT_ORDER_ASC", "SORT_ORDER_DESC"]);
  const GROUP_MODES = new Set(["GROUP_MODE_FLAT", "GROUP_MODE_DEEP"]);
  const LOCALIZATIONS = new Set([
    "LOCALIZATION_RU", "LOCALIZATION_UK", "LOCALIZATION_BE",
    "LOCALIZATION_KK", "LOCALIZATION_TR", "LOCALIZATION_EN"
  ]);

  const LOCALIZATIONS_BY_SEARCH_TYPE = Object.freeze({
    SEARCH_TYPE_RU: new Set(["LOCALIZATION_RU", "LOCALIZATION_BE", "LOCALIZATION_KK", "LOCALIZATION_UK"]),
    SEARCH_TYPE_TR: new Set(["LOCALIZATION_TR"]),
    SEARCH_TYPE_COM: new Set(["LOCALIZATION_EN"]),
    SEARCH_TYPE_KK: new Set(),
    SEARCH_TYPE_BE: new Set(),
    SEARCH_TYPE_UZ: new Set()
  });
  const DEFAULT_LOCALIZATION_BY_SEARCH_TYPE = Object.freeze({
    SEARCH_TYPE_RU: "LOCALIZATION_RU",
    SEARCH_TYPE_TR: "LOCALIZATION_TR",
    SEARCH_TYPE_COM: "LOCALIZATION_EN"
  });
  const REGION_CAPABLE_SEARCH_TYPES = new Set(["SEARCH_TYPE_RU", "SEARCH_TYPE_TR"]);
  const METHODS = new Set(["search", "genSearch"]);
  const SEARCH_ALLOWED_FIELDS = new Set([
    "method", "queryText", "searchType", "region", "page", "groupsOnPage",
    "familyMode", "fixTypoMode", "sortMode", "sortOrder", "groupMode",
    "docsInGroup", "maxPassages", "l10n"
  ]);
  const GEN_SEARCH_ALLOWED_FIELDS = new Set(["method", "queryText", "confirmBillable"]);

  function fail(code, message) {
    const error = new Error(message || code);
    error.code = code;
    throw error;
  }

  function unicodeLength(text) {
    return Array.from(String(text || "")).length;
  }

  function asString(value, name, { required = false, max = 400, trim = true } = {}) {
    if (value === undefined || value === null || value === "") {
      if (required) fail("MISSING_FIELD", `Отсутствует обязательное поле: ${name}`);
      return undefined;
    }
    const text = trim ? String(value).trim() : String(value);
    if (required && !text) fail("MISSING_FIELD", `Отсутствует обязательное поле: ${name}`);
    if (unicodeLength(text) > max) fail("FIELD_TOO_LONG", `${name}: превышена максимальная длина ${max}`);
    return text;
  }

  function asInteger(value, name, { defaultValue, min = 0, max = Number.MAX_SAFE_INTEGER } = {}) {
    const candidate = value === undefined ? defaultValue : value;
    const number = typeof candidate === "number" ? candidate : Number(candidate);
    if (!Number.isSafeInteger(number) || number < min || number > max) {
      fail("INVALID_FIELD", `${name} должен быть целым числом от ${min} до ${max}.`);
    }
    return number;
  }

  function asEnum(value, name, values, defaultValue) {
    const candidate = value === undefined ? defaultValue : asString(value, name, { required: true, max: 80 });
    if (!values.has(candidate)) fail("INVALID_ENUM", `Неизвестное значение ${name}: ${candidate}`);
    return candidate;
  }

  function validateAllowedFields(raw, allowedFields) {
    for (const key of Object.keys(raw)) {
      if (!allowedFields.has(key)) fail("UNSUPPORTED_FIELD", `Поле ${key} не разрешено для метода ${raw.method || "search"} в SEARCH_API_V1.`);
    }
  }

  function normalizeQueryText(raw) {
    const queryText = asString(raw.queryText, "queryText", { required: true, max: 400 });
    const wordCount = queryText ? queryText.split(/\s+/u).filter(Boolean).length : 0;
    if (wordCount > 40) fail("QUERY_TOO_MANY_WORDS", "queryText: максимум 40 слов.");
    return queryText;
  }

  function parseCommand(text) {
    const source = String(text || "").replace(/\u00a0/g, " ").trim();
    if (!source.startsWith(PREFIX)) fail("NOT_SEARCH_COMMAND", `Команда должна начинаться с ${PREFIX}`);
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

    const method = raw.method === undefined ? "search" : asString(raw.method, "method", { required: true, max: 40 });
    if (!METHODS.has(method)) fail("UNSUPPORTED_METHOD", `Метод ${method} не разрешён.`);

    if (method === "genSearch") {
      validateAllowedFields(raw, GEN_SEARCH_ALLOWED_FIELDS);
      const queryText = normalizeQueryText(raw);
      if (raw.confirmBillable !== true) {
        fail("GEN_SEARCH_CONFIRM_REQUIRED", "genSearch требует явного confirmBillable:true для одного платного provider request.");
      }
      return Object.freeze({ method, queryText, confirmBillable: true });
    }

    validateAllowedFields(raw, SEARCH_ALLOWED_FIELDS);
    const queryText = normalizeQueryText(raw);
    const searchType = asEnum(raw.searchType, "searchType", SEARCH_TYPES, "SEARCH_TYPE_RU");
    const familyMode = asEnum(raw.familyMode, "familyMode", FAMILY_MODES, "FAMILY_MODE_MODERATE");
    const fixTypoMode = asEnum(raw.fixTypoMode, "fixTypoMode", FIX_TYPO_MODES, "FIX_TYPO_MODE_ON");
    const sortMode = asEnum(raw.sortMode, "sortMode", SORT_MODES, "SORT_MODE_BY_RELEVANCE");
    const sortOrder = asEnum(raw.sortOrder, "sortOrder", SORT_ORDERS, "SORT_ORDER_DESC");
    const groupMode = asEnum(raw.groupMode, "groupMode", GROUP_MODES, "GROUP_MODE_FLAT");
    const page = asInteger(raw.page, "page", { defaultValue: 0, min: 0, max: 1000000 });
    const groupsOnPage = asInteger(raw.groupsOnPage, "groupsOnPage", { defaultValue: 10, min: 1, max: 100 });
    const docsInGroup = asInteger(raw.docsInGroup, "docsInGroup", { defaultValue: 1, min: 1, max: 3 });
    const maxPassages = asInteger(raw.maxPassages, "maxPassages", { defaultValue: 4, min: 1, max: 5 });

    let region;
    if (raw.region !== undefined) {
      region = asString(raw.region, "region", { required: true, max: 100 });
      if (!REGION_CAPABLE_SEARCH_TYPES.has(searchType)) {
        fail("REGION_NOT_SUPPORTED", `region не поддерживается для ${searchType}.`);
      }
    } else if (searchType === "SEARCH_TYPE_RU") {
      region = "225";
    }

    let l10n;
    if (raw.l10n !== undefined) {
      l10n = asEnum(raw.l10n, "l10n", LOCALIZATIONS);
      const allowed = LOCALIZATIONS_BY_SEARCH_TYPE[searchType];
      if (!allowed?.has(l10n)) fail("LOCALIZATION_NOT_SUPPORTED", `l10n ${l10n} не поддерживается для ${searchType}.`);
    } else {
      l10n = DEFAULT_LOCALIZATION_BY_SEARCH_TYPE[searchType];
    }

    const normalized = {
      method,
      queryText,
      searchType,
      page,
      groupsOnPage,
      familyMode,
      fixTypoMode,
      sortMode,
      sortOrder,
      groupMode,
      docsInGroup,
      maxPassages
    };
    if (region !== undefined) normalized.region = region;
    if (l10n !== undefined) normalized.l10n = l10n;
    return Object.freeze(normalized);
  }

  function buildRequest(command, folderId) {
    const normalized = normalizeCommand(command);
    const folder = asString(folderId, "folderId", { required: true, max: 50 });

    if (normalized.method === "genSearch") {
      return Object.freeze({
        url: `https://searchapi.api.cloud.yandex.net${GEN_ENDPOINT}`,
        body: Object.freeze({
          messages: Object.freeze([Object.freeze({ content: normalized.queryText, role: "ROLE_USER" })]),
          folderId: folder,
          fixMisspell: true,
          getPartialResults: false
        })
      });
    }

    const body = {
      query: {
        searchType: normalized.searchType,
        queryText: normalized.queryText,
        familyMode: normalized.familyMode,
        page: String(normalized.page),
        fixTypoMode: normalized.fixTypoMode
      },
      sortSpec: {
        sortMode: normalized.sortMode,
        sortOrder: normalized.sortOrder
      },
      groupSpec: {
        groupMode: normalized.groupMode,
        groupsOnPage: String(normalized.groupsOnPage),
        docsInGroup: String(normalized.docsInGroup)
      },
      maxPassages: String(normalized.maxPassages),
      folderId: folder,
      responseFormat: RESPONSE_FORMAT
    };
    if (normalized.region !== undefined) body.region = normalized.region;
    if (normalized.l10n !== undefined) body.l10n = normalized.l10n;
    return Object.freeze({
      url: `https://searchapi.api.cloud.yandex.net${ENDPOINT}`,
      body: Object.freeze(body)
    });
  }

  function normalizeGenSearchProviderResult(parsed) {
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
      fail("INVALID_GEN_SEARCH_RESPONSE", "Yandex GenSearch вернул неожиданный JSON-ответ.");
    }

    const message = parsed.message && typeof parsed.message === "object" && !Array.isArray(parsed.message)
      ? Object.freeze({
          content: String(parsed.message.content ?? ""),
          role: String(parsed.message.role ?? "")
        })
      : null;
    const sources = Array.isArray(parsed.sources)
      ? parsed.sources.map((source) => Object.freeze({
          url: String(source?.url ?? ""),
          title: String(source?.title ?? ""),
          used: source?.used === true
        }))
      : [];
    const searchQueries = Array.isArray(parsed.searchQueries)
      ? parsed.searchQueries.map((query) => Object.freeze({
          text: String(query?.text ?? ""),
          reqId: String(query?.reqId ?? "")
        }))
      : [];
    const hints = Array.isArray(parsed.hints) ? parsed.hints.map((hint) => String(hint ?? "")) : [];

    return Object.freeze({
      mode: "generative",
      message,
      sources: Object.freeze(sources),
      searchQueries: Object.freeze(searchQueries),
      fixedMisspellQuery: String(parsed.fixedMisspellQuery ?? ""),
      isAnswerRejected: parsed.isAnswerRejected === true,
      isBulletAnswer: parsed.isBulletAnswer === true,
      hints: Object.freeze(hints),
      problematicAnswer: parsed.problematicAnswer ?? null
    });
  }

  function normalizeProviderResult(parsed) {
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
      fail("INVALID_SEARCH_RESPONSE", "Yandex Search вернул неожиданный JSON-ответ.");
    }
    if (typeof parsed.rawData === "string" && parsed.rawData.trim()) {
      const normalizer = globalThis.YMBSearchXml;
      if (!normalizer || typeof normalizer.normalizeBase64RawData !== "function") {
        fail("SEARCH_XML_NORMALIZER_UNAVAILABLE", "Модуль нормализации Search XML не загружен.");
      }
      return normalizer.normalizeBase64RawData(parsed.rawData);
    }
    return normalizeGenSearchProviderResult(parsed);
  }

  function attachGenSearchTransport(result, wireFormat, frameCount) {
    return Object.freeze({
      ...result,
      transport: Object.freeze({ wire_format: wireFormat, frame_count: frameCount })
    });
  }

  function normalizeGenSearchFrames(frames, wireFormat) {
    if (!Array.isArray(frames) || frames.length === 0) {
      fail("INVALID_GEN_SEARCH_RESPONSE", "Yandex GenSearch не вернул ни одного GenSearchResponse frame.");
    }
    for (const frame of frames) {
      if (!frame || typeof frame !== "object" || Array.isArray(frame)) {
        fail("INVALID_GEN_SEARCH_RESPONSE", "Yandex GenSearch вернул некорректный GenSearchResponse frame.");
      }
    }
    const finalResult = normalizeGenSearchProviderResult(frames[frames.length - 1]);
    return attachGenSearchTransport(finalResult, wireFormat, frames.length);
  }

  function parseProviderResponseText(command, rawText) {
    const normalizedCommand = normalizeCommand(command);
    const source = String(rawText ?? "");
    const trimmed = source.trim();
    if (!trimmed) {
      fail(normalizedCommand.method === "genSearch" ? "EMPTY_GEN_SEARCH_RESPONSE" : "INVALID_SEARCH_RESPONSE", "Yandex Search вернул пустой ответ.");
    }

    if (normalizedCommand.method !== "genSearch") {
      let parsed;
      try { parsed = JSON.parse(trimmed); }
      catch { fail("INVALID_SEARCH_RESPONSE", "Yandex Search вернул невалидный JSON-ответ."); }
      return normalizeProviderResult(parsed);
    }

    let parsed;
    try {
      parsed = JSON.parse(trimmed);
    } catch {
      const lines = source.split(/\r?\n/u).map((line) => line.trim()).filter(Boolean);
      if (lines.length === 0) fail("INVALID_GEN_SEARCH_RESPONSE", "Yandex GenSearch вернул пустой поток ответа.");
      const frames = [];
      for (const line of lines) {
        try { frames.push(JSON.parse(line)); }
        catch { fail("INVALID_GEN_SEARCH_RESPONSE", "Yandex GenSearch вернул невалидный JSON Lines frame."); }
      }
      return normalizeGenSearchFrames(frames, "json_lines");
    }

    if (Array.isArray(parsed)) return normalizeGenSearchFrames(parsed, "json_array");
    return attachGenSearchTransport(normalizeGenSearchProviderResult(parsed), "json_object", 1);
  }

  function commandFingerprint(command) {
    const json = JSON.stringify(command);
    let hash = 2166136261;
    for (let i = 0; i < json.length; i += 1) {
      hash ^= json.charCodeAt(i);
      hash = Math.imul(hash, 16777619);
    }
    return (hash >>> 0).toString(16).padStart(8, "0");
  }

  function safeErrorPayload(status, rawText, parsed) {
    const candidate = parsed && typeof parsed === "object" ? parsed : null;
    return {
      http_status: Number(status || 0),
      code: String(candidate?.code || candidate?.error?.code || candidate?.status || "YANDEX_API_ERROR").slice(0, 160),
      message: String(candidate?.message || candidate?.error?.message || candidate?.error || rawText || "Yandex API error").slice(0, 2000)
    };
  }

  function buildResultEnvelope({ requestId, command, httpStatus, result, elapsedMs, metadata = {} }) {
    return {
      bridge: String(globalThis.YMBProduct?.BRIDGE_ID || "yandex-marketing-bridge"),
      version: productVersion(),
      service: "search",
      operation: command?.method || null,
      request_id: requestId,
      run_id: metadata.run_id || null,
      status: metadata.status || (Number(httpStatus || 0) >= 200 && Number(httpStatus || 0) < 300 ? "OK" : "ERROR"),
      reason: metadata.reason || null,
      cost_estimate: metadata.cost_estimate || null,
      policy: metadata.policy || null,
      command,
      http_status: httpStatus,
      elapsed_ms: elapsedMs,
      result,
      ...(metadata.debug_logs ? { debug_logs: metadata.debug_logs } : {}),
      ...(metadata.request_executed !== undefined ? { request_executed: metadata.request_executed } : {}),
      ...(metadata.automatic_retry !== undefined ? { automatic_retry: metadata.automatic_retry } : {})
    };
  }

  function formatResultEnvelope(envelope) {
    return `${RESULT_PREFIX}\n${JSON.stringify(envelope, null, 2)}`;
  }

  function formatResultReport(args) {
    return formatResultEnvelope(buildResultEnvelope(args));
  }

  function buildSkippedEnvelope({ requestId, command, reason, metadata = {} }) {
    return buildResultEnvelope({
      requestId,
      command,
      httpStatus: 0,
      elapsedMs: 0,
      metadata: {
        ...metadata,
        status: "SKIPPED",
        reason,
        request_executed: metadata.request_executed ?? false,
        automatic_retry: metadata.automatic_retry ?? false
      },
      result: { skipped: true, reason }
    });
  }

  function formatSkippedReport(args) {
    return formatResultEnvelope(buildSkippedEnvelope(args));
  }

  function isCommandText(text) {
    return String(text || "").replace(/\u00a0/g, " ").trim().startsWith(PREFIX);
  }

  globalThis.SearchProtocol = Object.freeze({
    PREFIX,
    RESULT_PREFIX,
    ENDPOINT,
    GEN_ENDPOINT,
    RESPONSE_FORMAT,
    CONSERVATIVE_SYNC_COST_RUB,
    GEN_SEARCH_SYNC_COST_RUB,
    METHODS,
    SEARCH_TYPES,
    FAMILY_MODES,
    FIX_TYPO_MODES,
    SORT_MODES,
    SORT_ORDERS,
    GROUP_MODES,
    LOCALIZATIONS,
    LOCALIZATIONS_BY_SEARCH_TYPE,
    REGION_CAPABLE_SEARCH_TYPES,
    parseCommand,
    normalizeCommand,
    buildRequest,
    normalizeGenSearchProviderResult,
    normalizeProviderResult,
    parseProviderResponseText,
    commandFingerprint,
    safeErrorPayload,
    buildResultEnvelope,
    formatResultEnvelope,
    formatResultReport,
    buildSkippedEnvelope,
    formatSkippedReport,
    isCommandText
  });
})();