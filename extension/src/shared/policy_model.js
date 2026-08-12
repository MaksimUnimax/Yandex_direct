(() => {
  "use strict";

  const DEFAULT_TARIFF_SOURCE = "https://aistudio.yandex.ru/docs/ru/search-api/pricing.html";
  const DEFAULT_TARIFF_CHECKED_AT = "2026-08-12";
  const DEFAULT_METHOD_COST_RUB = Object.freeze({
    getTop: 0.02,
    getDynamics: 0.02,
    getRegionsDistribution: 0.05,
    getRegionsTree: 0
  });
  const WORDSTAT_METHODS = Object.freeze(Object.keys(DEFAULT_METHOD_COST_RUB));

  function finiteNumber(value, fallback = 0) {
    const n = Number(value);
    return Number.isFinite(n) ? n : fallback;
  }

  function clampInteger(value, min, max, fallback) {
    const n = Number(value);
    if (!Number.isFinite(n)) return fallback;
    return Math.max(min, Math.min(max, Math.trunc(n)));
  }

  function normalizeAllowedMethods(value) {
    const input = Array.isArray(value) ? value.map(String) : WORDSTAT_METHODS;
    const set = new Set(input.filter((method) => WORDSTAT_METHODS.includes(method)));
    return WORDSTAT_METHODS.filter((method) => set.has(method));
  }

  function normalizeTariffs(raw = {}) {
    const result = {};
    for (const method of WORDSTAT_METHODS) {
      const candidate = finiteNumber(raw?.[method], DEFAULT_METHOD_COST_RUB[method]);
      result[method] = Math.max(0, Math.min(100000, candidate));
    }
    return Object.freeze(result);
  }

  function normalizeWordstatPolicy(raw = {}) {
    return Object.freeze({
      autorun_enabled: raw.autorun_enabled === true,
      manual_enabled: raw.manual_enabled !== false,
      allowed_methods: Object.freeze(normalizeAllowedMethods(raw.allowed_methods)),
      max_requests_per_run: clampInteger(raw.max_requests_per_run, 1, 100000, 500),
      max_cost_rub_per_run: Math.max(0, Math.min(1_000_000, finiteNumber(raw.max_cost_rub_per_run, 25))),
      max_requests_per_job: clampInteger(raw.max_requests_per_job, 1, 1_000_000, 5000),
      max_cost_rub_per_job: Math.max(0, Math.min(10_000_000, finiteNumber(raw.max_cost_rub_per_job, 250))),
      method_cost_rub: normalizeTariffs(raw.method_cost_rub),
      tariff_source: String(raw.tariff_source || DEFAULT_TARIFF_SOURCE).slice(0, 1000),
      tariff_checked_at: String(raw.tariff_checked_at || DEFAULT_TARIFF_CHECKED_AT).slice(0, 80)
    });
  }

  function costForMethod(policy, method) {
    const normalized = normalizeWordstatPolicy(policy);
    if (!WORDSTAT_METHODS.includes(method)) return null;
    return Number(normalized.method_cost_rub[method] || 0);
  }

  function decision({ policy, channel = "autorun", method, credentialState = "PRESENT", run = {}, jobTotals = {} } = {}) {
    const normalized = normalizeWordstatPolicy(policy);
    const cost = costForMethod(normalized, method);
    if (cost === null) return Object.freeze({ allow: false, reason: "OPERATION_DISABLED", estimated_cost_rub: 0, policy: normalized });
    if (credentialState !== "PRESENT") return Object.freeze({ allow: false, reason: "NO_CREDENTIALS", estimated_cost_rub: cost, policy: normalized });
    if (channel === "autorun" && normalized.autorun_enabled !== true) return Object.freeze({ allow: false, reason: "AUTORUN_DISABLED", estimated_cost_rub: cost, policy: normalized });
    if (channel === "manual" && normalized.manual_enabled !== true) return Object.freeze({ allow: false, reason: "MANUAL_DISABLED", estimated_cost_rub: cost, policy: normalized });
    if (!normalized.allowed_methods.includes(method)) return Object.freeze({ allow: false, reason: "OPERATION_DISABLED", estimated_cost_rub: cost, policy: normalized });

    const runRequests = Math.max(0, finiteNumber(run.requests_executed, 0));
    const runCost = Math.max(0, finiteNumber(run.estimated_cost_rub, 0));
    const jobRequests = Math.max(0, finiteNumber(jobTotals.requests_executed, 0));
    const jobCost = Math.max(0, finiteNumber(jobTotals.estimated_cost_rub, 0));

    if (runRequests + 1 > normalized.max_requests_per_run) return Object.freeze({ allow: false, reason: "REQUEST_LIMIT", estimated_cost_rub: cost, policy: normalized });
    if (jobRequests + 1 > normalized.max_requests_per_job) return Object.freeze({ allow: false, reason: "JOB_REQUEST_LIMIT", estimated_cost_rub: cost, policy: normalized });
    if (runCost + cost > normalized.max_cost_rub_per_run + 1e-9) return Object.freeze({ allow: false, reason: "COST_LIMIT", estimated_cost_rub: cost, policy: normalized });
    if (jobCost + cost > normalized.max_cost_rub_per_job + 1e-9) return Object.freeze({ allow: false, reason: "JOB_COST_LIMIT", estimated_cost_rub: cost, policy: normalized });

    return Object.freeze({ allow: true, reason: null, estimated_cost_rub: cost, policy: normalized });
  }

  globalThis.YMBPolicyModel = Object.freeze({
    DEFAULT_TARIFF_SOURCE,
    DEFAULT_TARIFF_CHECKED_AT,
    DEFAULT_METHOD_COST_RUB,
    WORDSTAT_METHODS,
    normalizeWordstatPolicy,
    costForMethod,
    decision
  });
})();
