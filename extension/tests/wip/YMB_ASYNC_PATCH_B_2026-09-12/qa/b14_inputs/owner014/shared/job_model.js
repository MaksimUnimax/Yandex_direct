(() => {
  "use strict";

  const JOB_ID_RE = /^[A-Za-z0-9][A-Za-z0-9._-]{0,119}$/;

  function fail(code, message) {
    const error = new Error(message || code);
    error.code = code;
    throw error;
  }

  function normalizeJobId(value, { required = false } = {}) {
    const text = String(value || "").trim();
    if (!text) {
      if (required) fail("JOB_ID_MISSING", "Укажите Job ID текущего заказа.");
      return "";
    }
    if (!JOB_ID_RE.test(text)) {
      fail("INVALID_JOB_ID", "Job ID: только A-Z/a-z/0-9, точка, подчёркивание и дефис; максимум 120 символов, без слешей.");
    }
    return text;
  }

  function normalizeActiveService(value, registry, { required = false } = {}) {
    const service = String(value || "").trim().toLowerCase();
    if (!service) {
      if (required) fail("ACTIVE_SERVICE_MISSING", "Выберите активный сервис перед запуском.");
      return "";
    }
    if (!registry?.isKnownService?.(service)) fail("UNKNOWN_SERVICE", `Неизвестный сервис: ${service}`);
    return service;
  }

  function assertServiceMatch(activeService, detectedService) {
    const active = String(activeService || "").trim().toLowerCase();
    const detected = String(detectedService || "").trim().toLowerCase();
    if (!active || !detected || active !== detected) {
      fail("SERVICE_NOT_ACTIVE", `Команда предназначена сервису ${detected || "unknown"}, активный RUN: ${active || "none"}.`);
    }
    return true;
  }

  function makeRunIdentity({ jobId, activeService, registry }) {
    return Object.freeze({
      job_id: normalizeJobId(jobId, { required: true }),
      active_service: normalizeActiveService(activeService, registry, { required: true })
    });
  }

  globalThis.YMBJobModel = Object.freeze({
    JOB_ID_RE,
    normalizeJobId,
    normalizeActiveService,
    assertServiceMatch,
    makeRunIdentity
  });
})();
