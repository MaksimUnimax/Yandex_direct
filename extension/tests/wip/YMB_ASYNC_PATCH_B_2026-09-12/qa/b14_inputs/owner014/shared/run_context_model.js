(() => {
  "use strict";

  function fail(code, message) {
    const error = new Error(message || code);
    error.code = code;
    throw error;
  }

  function normalizeActiveService(value, registry, { required = false } = {}) {
    const service = String(value || "").trim().toLowerCase();
    if (!service) {
      if (required) fail("ACTIVE_SERVICE_MISSING", "Выберите активный сервис.");
      return "";
    }
    if (!registry?.isKnownService?.(service)) fail("UNKNOWN_SERVICE", `Неизвестный сервис: ${service}`);
    return service;
  }

  function assertServiceMatch(activeService, detectedService) {
    const active = String(activeService || "").trim().toLowerCase();
    const detected = String(detectedService || "").trim().toLowerCase();
    if (!active || !detected || active !== detected) {
      fail("SERVICE_NOT_ACTIVE", `Команда относится к ${detected || "unknown"}, активный сервис: ${active || "none"}.`);
    }
    return true;
  }

  function makeRunIdentity({ activeService, registry }) {
    return Object.freeze({ active_service: normalizeActiveService(activeService, registry, { required: true }) });
  }

  globalThis.YMBRunContextModel = Object.freeze({ normalizeActiveService, assertServiceMatch, makeRunIdentity });
})();
