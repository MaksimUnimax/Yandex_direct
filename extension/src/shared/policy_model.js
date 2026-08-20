(() => {
  "use strict";

  const DEFAULT_TARIFF_SOURCE = "https://aistudio.yandex.ru/docs/ru/search-api/pricing.html";
  const DEFAULT_TARIFF_CHECKED_AT = "2026-08-12";
  const SEARCH_TARIFF_CHECKED_AT = "2026-08-19";
  const DEFAULT_METHOD_COST_RUB = Object.freeze({
    getTop: 0.02,
    getDynamics: 0.02,
    getRegionsDistribution: 0.05,
    getRegionsTree: 0
  });
  const DEFAULT_SEARCH_METHOD_COST_RUB = Object.freeze({ search: 0.488 });
  const WORDSTAT_METHODS = Object.freeze(Object.keys(DEFAULT_METHOD_COST_RUB));
  const SEARCH_METHODS = Object.freeze(Object.keys(DEFAULT_SEARCH_METHOD_COST_RUB));

  function finiteNumber(value, fallback = 0) {
    const n = Number(value);
    return Number.isFinite(n) ? n : fallback;
  }
  function clampInteger(value, min, max, fallback) {
    const n = Number(value);
    if (!Number.isFinite(n)) return fallback;
    return Math.max(min, Math.min(max, Math.trunc(n)));
  }
  function normalizeAllowedMethods(value, methods) {
    const input = Array.isArray(value) ? value.map(String) : methods;
    const set = new Set(input.filter((method) => methods.includes(method)));
    return methods.filter((method) => set.has(method));
  }
  function normalizeTariffs(raw = {}, defaults = DEFAULT_METHOD_COST_RUB, methods = WORDSTAT_METHODS) {
    const result = {};
    for (const method of methods) {
      const candidate = finiteNumber(raw?.[method], defaults[method]);
      result[method] = Math.max(0, Math.min(100000, candidate));
    }
    return Object.freeze(result);
  }
  function normalizePolicy(raw, { methods, defaults, tariffCheckedAt, maxRequestsPerRun = 500, maxCostRubPerRun = 25 }) {
    return Object.freeze({
      autorun_enabled: raw?.autorun_enabled === true,
      manual_enabled: raw?.manual_enabled !== false,
      allowed_methods: Object.freeze(normalizeAllowedMethods(raw?.allowed_methods, methods)),
      max_requests_per_run: clampInteger(raw?.max_requests_per_run, 1, 100000, maxRequestsPerRun),
      max_cost_rub_per_run: Math.max(0, Math.min(1_000_000, finiteNumber(raw?.max_cost_rub_per_run, maxCostRubPerRun))),
      method_cost_rub: normalizeTariffs(raw?.method_cost_rub, defaults, methods),
      tariff_source: String(raw?.tariff_source || DEFAULT_TARIFF_SOURCE).slice(0, 1000),
      tariff_checked_at: String(raw?.tariff_checked_at || tariffCheckedAt).slice(0, 80)
    });
  }
  function normalizeWordstatPolicy(raw = {}) {
    return normalizePolicy(raw, {
      methods: WORDSTAT_METHODS,
      defaults: DEFAULT_METHOD_COST_RUB,
      tariffCheckedAt: DEFAULT_TARIFF_CHECKED_AT
    });
  }
  function normalizeSearchPolicy(raw = {}) {
    return normalizePolicy(raw, {
      methods: SEARCH_METHODS,
      defaults: DEFAULT_SEARCH_METHOD_COST_RUB,
      tariffCheckedAt: SEARCH_TARIFF_CHECKED_AT
    });
  }
  function costFrom(normalizer, methods, policy, method) {
    const normalized = normalizer(policy);
    if (!methods.includes(method)) return null;
    return Number(normalized.method_cost_rub[method] || 0);
  }
  function costForMethod(policy, method) {
    return costFrom(normalizeWordstatPolicy, WORDSTAT_METHODS, policy, method);
  }
  function searchCostForMethod(policy, method) {
    return costFrom(normalizeSearchPolicy, SEARCH_METHODS, policy, method);
  }
  function decide({ normalizer, costResolver, policy, channel = "autorun", method, credentialState = "PRESENT", run = {} } = {}) {
    const normalized = normalizer(policy);
    const cost = costResolver(normalized, method);
    if (cost === null) return Object.freeze({ allow: false, reason: "OPERATION_DISABLED", estimated_cost_rub: 0, policy: normalized });
    if (credentialState !== "PRESENT") return Object.freeze({ allow: false, reason: "NO_CREDENTIALS", estimated_cost_rub: cost, policy: normalized });
    if (channel === "autorun" && normalized.autorun_enabled !== true) return Object.freeze({ allow: false, reason: "AUTORUN_DISABLED", estimated_cost_rub: cost, policy: normalized });
    if (channel === "manual" && normalized.manual_enabled !== true) return Object.freeze({ allow: false, reason: "MANUAL_DISABLED", estimated_cost_rub: cost, policy: normalized });
    if (!normalized.allowed_methods.includes(method)) return Object.freeze({ allow: false, reason: "OPERATION_DISABLED", estimated_cost_rub: cost, policy: normalized });
    const runRequests = Math.max(0, finiteNumber(run.requests_executed, 0));
    const runCost = Math.max(0, finiteNumber(run.estimated_cost_rub, 0));
    const enforceRunBudget = channel === "autorun" || Boolean(run?.run_id);
    if (enforceRunBudget && runRequests + 1 > normalized.max_requests_per_run) return Object.freeze({ allow: false, reason: "REQUEST_LIMIT", estimated_cost_rub: cost, policy: normalized });
    if (enforceRunBudget && runCost + cost > normalized.max_cost_rub_per_run + 1e-9) return Object.freeze({ allow: false, reason: "COST_LIMIT", estimated_cost_rub: cost, policy: normalized });
    return Object.freeze({ allow: true, reason: null, estimated_cost_rub: cost, policy: normalized });
  }
  function decision(args = {}) {
    return decide({ ...args, normalizer: normalizeWordstatPolicy, costResolver: costForMethod });
  }
  function searchDecision(args = {}) {
    return decide({ ...args, normalizer: normalizeSearchPolicy, costResolver: searchCostForMethod });
  }
  function normalizePolicyForService(service, raw = {}) {
    if (String(service || "") === "search") return normalizeSearchPolicy(raw);
    return normalizeWordstatPolicy(raw);
  }
  function decisionForService(service, args = {}) {
    return String(service || "") === "search" ? searchDecision(args) : decision(args);
  }

  globalThis.YMBPolicyModel = Object.freeze({
    DEFAULT_TARIFF_SOURCE,
    DEFAULT_TARIFF_CHECKED_AT,
    SEARCH_TARIFF_CHECKED_AT,
    DEFAULT_METHOD_COST_RUB,
    DEFAULT_SEARCH_METHOD_COST_RUB,
    WORDSTAT_METHODS,
    SEARCH_METHODS,
    normalizeWordstatPolicy,
    normalizeSearchPolicy,
    normalizePolicyForService,
    costForMethod,
    searchCostForMethod,
    decision,
    searchDecision,
    decisionForService
  });
})();
