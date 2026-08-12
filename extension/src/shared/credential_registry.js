(() => {
  "use strict";

  const STATES = Object.freeze({
    PRESENT: "PRESENT",
    MISSING: "MISSING",
    INVALID_OR_EXPIRED: "INVALID_OR_EXPIRED",
    NO_ACCESS: "NO_ACCESS"
  });

  function wordstatCapability(settings) {
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

  globalThis.YMBCredentialRegistry = Object.freeze({ STATES, wordstatCapability });
})();
