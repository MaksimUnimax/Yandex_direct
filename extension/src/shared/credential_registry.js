(() => {
  "use strict";

  const STATES = Object.freeze({
    PRESENT: "PRESENT",
    MISSING: "MISSING",
    INVALID_OR_EXPIRED: "INVALID_OR_EXPIRED",
    NO_ACCESS: "NO_ACCESS"
  });

  function recordForService(settings, service) {
    const credentials = settings?.credentials;
    if (!credentials || typeof credentials !== "object" || Array.isArray(credentials)) return null;
    const record = credentials[String(service || "")];
    return record && typeof record === "object" && !Array.isArray(record) ? record : null;
  }

  function cloudCredentialRecord(settings, service) {
    const dedicated = recordForService(settings, service);
    if (dedicated) {
      return {
        api_key: String(dedicated.api_key || "").trim(),
        folder_id: String(dedicated.folder_id || "").trim(),
        check_state: String(dedicated.check_state || "").trim()
      };
    }
    return {
      api_key: String(settings?.apiKey || "").trim(),
      folder_id: String(settings?.folderId || "").trim(),
      check_state: ""
    };
  }

  function cloudCapability(settings, service) {
    const credential = cloudCredentialRecord(settings, service);
    if (credential.check_state === STATES.INVALID_OR_EXPIRED) {
      return Object.freeze({ state: STATES.INVALID_OR_EXPIRED, has_api_key: Boolean(credential.api_key), has_folder_id: Boolean(credential.folder_id) });
    }
    if (credential.check_state === STATES.NO_ACCESS) {
      return Object.freeze({ state: STATES.NO_ACCESS, has_api_key: Boolean(credential.api_key), has_folder_id: Boolean(credential.folder_id) });
    }
    if (!credential.api_key || !credential.folder_id) {
      return Object.freeze({ state: STATES.MISSING, has_api_key: Boolean(credential.api_key), has_folder_id: Boolean(credential.folder_id) });
    }
    return Object.freeze({ state: STATES.PRESENT, has_api_key: true, has_folder_id: true });
  }

  function wordstatCapability(settings) { return cloudCapability(settings, "wordstat"); }
  function searchCapability(settings) { return cloudCapability(settings, "search"); }

  function webmasterCapability(settings) {
    const credential = recordForService(settings, "webmaster") || settings?.webmaster || {};
    const oauthToken = String(credential.oauth_token || credential.oauthToken || "").trim();
    const userId = String(credential.user_id ?? credential.userId ?? "").trim();
    const checkState = String(credential.check_state || credential.checkState || "").trim();
    if (checkState === STATES.INVALID_OR_EXPIRED) {
      return Object.freeze({ state: STATES.INVALID_OR_EXPIRED, has_oauth_token: Boolean(oauthToken), has_user_id: Boolean(userId) });
    }
    if (checkState === STATES.NO_ACCESS) {
      return Object.freeze({ state: STATES.NO_ACCESS, has_oauth_token: Boolean(oauthToken), has_user_id: Boolean(userId) });
    }
    if (!oauthToken || !/^\d+$/.test(userId)) {
      return Object.freeze({ state: STATES.MISSING, has_oauth_token: Boolean(oauthToken), has_user_id: /^\d+$/.test(userId) });
    }
    return Object.freeze({ state: STATES.PRESENT, has_oauth_token: true, has_user_id: true });
  }

  function capabilityForService(service, settings) {
    const value = String(service || "");
    if (value === "search") return searchCapability(settings);
    if (value === "wordstat") return wordstatCapability(settings);
    if (value === "webmaster") return webmasterCapability(settings);
    return Object.freeze({ state: STATES.NO_ACCESS, has_api_key: false, has_folder_id: false });
  }

  globalThis.YMBCredentialRegistry = Object.freeze({
    STATES,
    wordstatCapability,
    searchCapability,
    webmasterCapability,
    capabilityForService
  });
})();
