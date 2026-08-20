(() => {
  "use strict";

  const STATES = Object.freeze({
    PRESENT: "PRESENT",
    MISSING: "MISSING",
    INVALID_OR_EXPIRED: "INVALID_OR_EXPIRED",
    NO_ACCESS: "NO_ACCESS"
  });

  function sharedYandexCapability(settings) {
    const apiKey = String(settings?.apiKey || "").trim();
    const folderId = String(settings?.folderId || "").trim();
    if (!apiKey || !folderId) {
      return Object.freeze({
        state: STATES.MISSING,
        has_api_key: Boolean(apiKey),
        has_folder_id: Boolean(folderId)
      });
    }
    return Object.freeze({ state: STATES.PRESENT, has_api_key: true, has_folder_id: true });
  }

  function wordstatCapability(settings) { return sharedYandexCapability(settings); }
  function searchCapability(settings) { return sharedYandexCapability(settings); }
  function capabilityForService(service, settings) {
    const value = String(service || "").trim().toLowerCase();
    if (value === "search") return searchCapability(settings);
    if (value === "wordstat") return wordstatCapability(settings);
    return Object.freeze({ state: STATES.NO_ACCESS, has_api_key: Boolean(String(settings?.apiKey || "").trim()), has_folder_id: Boolean(String(settings?.folderId || "").trim()) });
  }

  globalThis.YMBCredentialRegistry = Object.freeze({
    STATES,
    sharedYandexCapability,
    wordstatCapability,
    searchCapability,
    capabilityForService
  });
})();
