(() => {
  "use strict";

  function finite(value) {
    const n = Number(value);
    return Number.isFinite(n) ? n : 0;
  }

  function normalizeTotals(raw = {}) {
    return Object.freeze({
      requests_attempted: Math.max(0, Math.trunc(finite(raw.requests_attempted))),
      requests_executed: Math.max(0, Math.trunc(finite(raw.requests_executed))),
      requests_skipped: Math.max(0, Math.trunc(finite(raw.requests_skipped))),
      estimated_cost_rub: Math.max(0, finite(raw.estimated_cost_rub))
    });
  }

  function noteAttempt(raw) {
    const current = normalizeTotals(raw);
    return Object.freeze({ ...current, requests_attempted: current.requests_attempted + 1 });
  }

  function noteExecuted(raw, estimatedCostRub = 0) {
    const current = normalizeTotals(raw);
    return Object.freeze({
      ...current,
      requests_executed: current.requests_executed + 1,
      estimated_cost_rub: Number((current.estimated_cost_rub + Math.max(0, finite(estimatedCostRub))).toFixed(6))
    });
  }

  function noteSkipped(raw) {
    const current = normalizeTotals(raw);
    return Object.freeze({ ...current, requests_skipped: current.requests_skipped + 1 });
  }

  globalThis.YMBCostLedgerModel = Object.freeze({ normalizeTotals, noteAttempt, noteExecuted, noteSkipped });
})();
