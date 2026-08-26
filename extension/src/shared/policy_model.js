(() => {
  "use strict";

  const DEFAULT_TARIFF_SOURCE = "https://aistudio.yandex.ru/docs/ru/search-api/pricing.html";
  const DEFAULT_TARIFF_CHECKED_AT = "2026-08-12";
  const SEARCH_TARIFF_CHECKED_AT = "2026-08-19";
  const WEBMASTER_POLICY_SOURCE = "https://yandex.ru/dev/webmaster/doc/ru/";
  const WEBMASTER_POLICY_CHECKED_AT = "2026-08-26";
  const DEFAULT_METHOD_COST_RUB = Object.freeze({
    getTop: 0.02,
    getDynamics: 0.02,
    getRegionsDistribution: 0.05,
    getRegionsTree: 0
  });
  const DEFAULT_SEARCH_METHOD_COST_RUB = Object.freeze({ search: 0.488 });
  const DEFAULT_WEBMASTER_METHOD_COST_RUB = Object.freeze({
    listHosts: 0,
    getSummary: 0,
    getDiagnostics: 0,
    getPopularQueries: 0
  });
  const WORDSTAT_METHODS = Object.freeze(Object.keys(DEFAULT_METHOD_COST_RUB));
  const SEARCH_METHODS = Object.freeze(["search"]);
  const WEBMASTER_METHODS = Object.freeze(Object.keys(DEFAULT_WEBMASTER_METHOD_COST_RUB));

  function asBoolean(value, fallback) {
    return typeof value === "boolean" ? value : fallback;
  }

  function asPositiveInt(value, fallback) {
    const number = Number(value);
    return Number.isInteger(number) && number > 0 ? number : fallback;
  }

  function asNonNegativeNumber(value, fallback) {
    const number = Number(value);
    return Number.isFinite(number) && number >= 0 ? number : fallback;
  }

  function normalizeMethodList(value, fallback, allowedMethods) {
    if (!Array.isArray(value)) return [...fallback];
    return [...new Set(value.map((item) => String(item)).filter((item) => allowedMethods.includes(item)))];
  }

  function normalizeCostMap(value, defaults, allowedMethods) {
    const out = { ...defaults };
    if (value && typeof value === "object") {
      for (const method of allowedMethods) {
        if (!Object.prototype.hasOwnProperty.call(value, method)) continue;
        const number = Number(value[method]);
        if (Number.isFinite(number) && number >= 0) out[method] = number;
      }
    }
    return Object.freeze(out);
  }

  function normalizePolicy(raw = {}, {
    defaultAutorunEnabled = false,
    defaultManualEnabled = true,
    defaultMethods = [],
    allowedMethods = [],
    defaultMaxRequests = 100,
    defaultMaxCostRub = 10,
    defaultCosts = {},
    defaultTariffCheckedAt = DEFAULT_TARIFF_CHECKED_AT,
    defaultTariffSource = DEFAULT_TARIFF_SOURCE
  } = {}) {
    return Object.freeze({
      autorun_enabled: asBoolean(raw.autorun_enabled, defaultAutorunEnabled),
      manual_enabled: asBoolean(raw.manual_enabled, defaultManualEnabled),
      allowed_methods: Object.freeze(normalizeMethodList(raw.allowed_methods, defaultMethods, allowedMethods)),
      max_requests_per_run: asPositiveInt(raw.max_requests_per_run, defaultMaxRequests),
      max_cost_rub_per_run: asNonNegativeNumber(raw.max_cost_rub_per_run, defaultMaxCostRub),
      method_cost_rub: normalizeCostMap(raw.method_cost_rub, defaultCosts, allowedMethods),
      tariff_checked_at: String(raw.tariff_checked_at || defaultTariffCheckedAt),
      tariff_source: String(raw.tariff_source || defaultTariffSource)
    });
  }

  function normalizeWordstatPolicy(raw = {}) {
    return normalizePolicy(raw, {
      defaultMethods: WORDSTAT_METHODS,
      allowedMethods: WORDSTAT_METHODS,
      defaultCosts: DEFAULT_METHOD_COST_RUB,
      defaultTariffCheckedAt: DEFAULT_TARIFF_CHECKED_AT,
      defaultTariffSource: DEFAULT_TARIFF_SOURCE
    });
  }

  function normalizeSearchPolicy(raw = {}) {
    return normalizePolicy(raw, {
      defaultMethods: SEARCH_METHODS,
      allowedMethods: SEARCH_METHODS,
      defaultCosts: DEFAULT_SEARCH_METHOD_COST_RUB,
      defaultTariffCheckedAt: SEARCH_TARIFF_CHECKED_AT,
      defaultTariffSource: DEFAULT_TARIFF_SOURCE
    });
  }

  function normalizeWebmasterPolicy(raw = {}) {
    return normalizePolicy(raw, {
      defaultAutorunEnabled: false,
      defaultManualEnabled: true,
      defaultMethods: WEBMASTER_METHODS,
      allowedMethods: WEBMASTER_METHODS,
      defaultMaxRequests: 50,
      defaultMaxCostRub: 0,
      defaultCosts: DEFAULT_WEBMASTER_METHOD_COST_RUB,
      defaultTariffCheckedAt: WEBMASTER_POLICY_CHECKED_AT,
      defaultTariffSource: WEBMASTER_POLICY_SOURCE
    });
  }

  function normalizePolicyForService(service, raw = {}) {
    const value = String(service || "");
    if (value === "search") return normalizeSearchPolicy(raw);
    if (value === "wordstat") return normalizeWordstatPolicy(raw);
    if (value === "webmaster") return normalizeWebmasterPolicy(raw);
    throw Object.assign(new Error(`Неизвестный сервис: ${service || "unknown"}`), { code: "UNKNOWN_SERVICE" });
  }

  function estimateMethodCost(policy, method) {
    return asNonNegativeNumber(policy.method_cost_rub?.[method], 0);
  }

  function decision({
    policy,
    channel,
    method,
    credentialState,
    run = {}
  }) {
    const methodName = String(method || "");
    const executed = Number(run.requests_executed || 0);
    const estimatedRunCost = Number(run.estimated_cost_rub || 0);
    const estimatedMethodCost = estimateMethodCost(policy, methodName);

    let allow = true;
    let reason = "ALLOW";
    if (credentialState !== "PRESENT") {
      allow = false;
      reason = credentialState === "NO_ACCESS" ? "CREDENTIAL_NO_ACCESS" : "NO_CREDENTIALS";
    } else if (channel === "autorun" && policy.autorun_enabled !== true) {
      allow = false;
      reason = "AUTORUN_DISABLED";
    } else if (channel === "manual" && policy.manual_enabled !== true) {
      allow = false;
      reason = "MANUAL_DISABLED";
    } else if (!policy.allowed_methods.includes(methodName)) {
      allow = false;
      reason = "OPERATION_DISABLED";
    } else if (executed >= policy.max_requests_per_run) {
      allow = false;
      reason = "REQUEST_LIMIT";
    } else if (estimatedRunCost + estimatedMethodCost > policy.max_cost_rub_per_run + Number.EPSILON) {
      allow = false;
      reason = "COST_LIMIT";
    }

    return Object.freeze({
      allow,
      reason,
      estimated_cost_rub: estimatedMethodCost,
      policy
    });
  }

  function wordstatDecision(args = {}) {
    const policy = normalizeWordstatPolicy(args.policy || {});
    return decision({ ...args, policy });
  }

  function searchDecision(args = {}) {
    const policy = normalizeSearchPolicy(args.policy || {});
    return decision({ ...args, policy });
  }

  function webmasterDecision(args = {}) {
    const policy = normalizeWebmasterPolicy(args.policy || {});
    return decision({ ...args, policy });
  }

  function decisionForService(service, args = {}) {
    const value = String(service || "");
    if (value === "search") return searchDecision(args);
    if (value === "wordstat") return wordstatDecision(args);
    if (value === "webmaster") return webmasterDecision(args);
    return Object.freeze({
      allow: false,
      reason: "SERVICE_NOT_AVAILABLE",
      estimated_cost_rub: 0,
      policy: null
    });
  }

  globalThis.YMBPolicyModel = Object.freeze({
    DEFAULT_METHOD_COST_RUB,
    DEFAULT_SEARCH_METHOD_COST_RUB,
    DEFAULT_WEBMASTER_METHOD_COST_RUB,
    WORDSTAT_METHODS,
    SEARCH_METHODS,
    WEBMASTER_METHODS,
    SEARCH_TARIFF_CHECKED_AT,
    WEBMASTER_POLICY_CHECKED_AT,
    WEBMASTER_POLICY_SOURCE,
    normalizeWordstatPolicy,
    normalizeSearchPolicy,
    normalizeWebmasterPolicy,
    normalizePolicyForService,
    estimateMethodCost,
    wordstatDecision,
    searchDecision,
    webmasterDecision,
    decisionForService
  });
})();
