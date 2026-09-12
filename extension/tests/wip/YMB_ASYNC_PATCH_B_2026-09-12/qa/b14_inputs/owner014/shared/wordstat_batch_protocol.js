(() => {
  "use strict";

  const PREFIX = "WORDSTAT_BATCH_API_V1";
  const RESULT_PREFIX = "WORDSTAT_BATCH_RESULT_V1";
  const ACTIONS = Object.freeze(new Set(["start", "next", "status", "pause", "resume", "cancel"]));
  const DEVICES = new Set(["DEVICE_ALL", "DEVICE_DESKTOP", "DEVICE_PHONE", "DEVICE_TABLET"]);

  function productVersion() {
    return String(globalThis.YMBProduct?.VERSION || "0.1.1");
  }

  function fail(code, message) {
    const error = new Error(message || code);
    error.code = code;
    throw error;
  }

  function batchFieldCode(name) {
    const field = String(name || "FIELD")
      .replace(/([a-z0-9])([A-Z])/g, "$1_$2")
      .replace(/[^A-Za-z0-9]+/g, "_")
      .replace(/^_+|_+$/g, "")
      .toUpperCase();
    return `MISSING_BATCH_${field || "FIELD"}`;
  }

  function asString(value, name, { required = false, max = 400 } = {}) {
    if (value === undefined || value === null || value === "") {
      if (required) fail(batchFieldCode(name), `${name} обязателен.`);
      return undefined;
    }
    const text = String(value).trim();
    if (!text && required) fail(batchFieldCode(name), `${name} обязателен.`);
    if (text.length > max) fail("BATCH_FIELD_TOO_LONG", `${name}: превышена максимальная длина ${max}.`);
    return text || undefined;
  }

  function positiveInt(value, name, { min = 1, max = Number.MAX_SAFE_INTEGER, fallback = undefined } = {}) {
    if (value === undefined || value === null || value === "") return fallback;
    const number = Number(value);
    if (!Number.isInteger(number) || number < min || number > max) fail("INVALID_BATCH_NUMBER", `${name} должен быть целым числом от ${min} до ${max}.`);
    return number;
  }

  function nonNegativeNumber(value, name, { max = Number.MAX_SAFE_INTEGER, fallback = undefined } = {}) {
    if (value === undefined || value === null || value === "") return fallback;
    const number = Number(value);
    if (!Number.isFinite(number) || number < 0 || number > max) fail("INVALID_BATCH_NUMBER", `${name} должен быть неотрицательным числом.`);
    return number;
  }

  function normalizePhrases(value) {
    if (!Array.isArray(value) || value.length === 0) fail("INVALID_BATCH_PHRASES", "phrases должен быть непустым массивом.");
    if (value.length > 500) fail("TOO_MANY_BATCH_PHRASES", "phrases: максимум 500 значений в одном batch job.");
    return Object.freeze(value.map((item, index) => {
      const phrase = String(item ?? "").trim();
      if (!phrase || phrase.length > 400) fail("INVALID_BATCH_PHRASE", `phrases[${index}] должен содержать от 1 до 400 символов.`);
      return phrase;
    }));
  }

  function normalizeRegions(value) {
    const source = value === undefined ? ["225"] : value;
    if (!Array.isArray(source) || source.length < 1 || source.length > 100) fail("INVALID_BATCH_REGIONS", "regions должен содержать от 1 до 100 значений.");
    return Object.freeze(source.map((item, index) => {
      const region = String(item ?? "").trim();
      if (!region || region.length > 80) fail("INVALID_BATCH_REGION", `regions[${index}] некорректен.`);
      return region;
    }));
  }

  function normalizeDevices(value) {
    const source = value === undefined ? ["DEVICE_ALL"] : value;
    if (!Array.isArray(source) || source.length < 1 || source.length > 3) fail("INVALID_BATCH_DEVICES", "devices должен содержать от 1 до 3 значений.");
    const devices = source.map((item) => String(item ?? "").trim());
    for (const device of devices) if (!DEVICES.has(device)) fail("INVALID_BATCH_DEVICE", `Неизвестное устройство: ${device}`);
    return Object.freeze(devices);
  }

  function normalizeCommand(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) fail("INVALID_BATCH_JSON_ROOT", "Batch-команда должна быть JSON-объектом.");
    const action = String(raw.action || "").trim();
    if (!ACTIONS.has(action)) fail("UNSUPPORTED_BATCH_ACTION", `Batch action ${action || "<empty>"} не поддерживается.`);

    if (action === "start") {
      const phrases = normalizePhrases(raw.phrases);
      const jobId = asString(raw.jobId, "jobId", { max: 240 });
      const numPhrases = positiveInt(raw.numPhrases, "numPhrases", { min: 1, max: 2000, fallback: 100 });
      const regions = normalizeRegions(raw.regions);
      const devices = normalizeDevices(raw.devices);
      const maxRequests = positiveInt(raw.maxRequests, "maxRequests", { min: 1, max: 500, fallback: phrases.length });
      const maxCostRub = nonNegativeNumber(raw.maxCostRub, "maxCostRub", { max: 100000, fallback: undefined });
      return Object.freeze({
        action,
        ...(jobId ? { jobId } : {}),
        phrases,
        numPhrases,
        regions,
        devices,
        maxRequests,
        ...(maxCostRub !== undefined ? { maxCostRub } : {})
      });
    }

    const jobId = asString(raw.jobId, "jobId", { required: true, max: 240 });
    return Object.freeze({ action, jobId });
  }

  function parseCommand(text) {
    const source = String(text || "").replace(/\u00a0/g, " ").trim();
    if (!source.startsWith(PREFIX)) fail("NOT_WORDSTAT_BATCH_COMMAND", `Команда должна начинаться с ${PREFIX}.`);
    const rest = source.slice(PREFIX.length).trim();
    if (!rest) fail("MISSING_BATCH_JSON", `После ${PREFIX} должен идти JSON-объект.`);
    let raw;
    try { raw = JSON.parse(rest); }
    catch (error) { fail("INVALID_BATCH_JSON", `Некорректный JSON: ${error.message}`); }
    return normalizeCommand(raw);
  }

  function canonicalize(value) {
    if (value === null) return "null";
    if (Array.isArray(value)) return `[${value.map(canonicalize).join(",")}]`;
    if (typeof value !== "object") return JSON.stringify(value);
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonicalize(value[key])}`).join(",")}}`;
  }

  function commandFingerprint(command) {
    const json = canonicalize(command);
    let hash = 2166136261;
    for (let index = 0; index < json.length; index += 1) {
      hash ^= json.charCodeAt(index);
      hash = Math.imul(hash, 16777619);
    }
    return (hash >>> 0).toString(16).padStart(8, "0");
  }

  function buildResultEnvelope({
    command,
    jobId = null,
    status = "OK",
    reason = null,
    progress = null,
    item = null,
    providerResult = null,
    requestExecuted = false,
    automaticRetry = false,
    costEstimate = null,
    policy = null,
    metadata = {}
  } = {}) {
    const normalized = normalizeCommand(command);
    const resolvedJobId = String(jobId || normalized.jobId || "").trim() || null;
    return Object.freeze({
      bridge: String(globalThis.YMBProduct?.BRIDGE_ID || "yandex-marketing-bridge"),
      version: productVersion(),
      service: "wordstat",
      operation: `batch.${normalized.action}`,
      job_id: resolvedJobId,
      run_id: metadata.run_id || null,
      status: String(status || "OK"),
      reason: reason == null ? null : String(reason),
      command: normalized,
      progress: progress || null,
      item: item || null,
      provider_result: providerResult || null,
      cost_estimate: costEstimate || null,
      policy: policy || null,
      request_executed: requestExecuted,
      automatic_retry: automaticRetry === true
    });
  }

  function formatResultEnvelope(envelope) {
    return `${RESULT_PREFIX}\n${JSON.stringify(envelope, null, 2)}`;
  }

  function isCommandText(text) {
    return String(text || "").replace(/\u00a0/g, " ").trim().startsWith(PREFIX);
  }

  globalThis.WordstatBatchProtocol = Object.freeze({
    PREFIX,
    RESULT_PREFIX,
    ACTIONS,
    normalizeCommand,
    parseCommand,
    commandFingerprint,
    buildResultEnvelope,
    formatResultEnvelope,
    isCommandText
  });
})();
