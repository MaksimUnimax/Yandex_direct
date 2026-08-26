(() => {
  "use strict";

  const STORAGE_KEY = "ymb_service_credentials";
  const SETTINGS_SCHEMA_VERSION = 3;
  const BACKUP_VERSION = 3;
  const SERVICES = Object.freeze(["wordstat", "search", "webmaster"]);
  const CHECK_STATES = new Set(["", "PRESENT", "MISSING", "INVALID_OR_EXPIRED", "NO_ACCESS", "NETWORK_ERROR", "NOT_CHECKED"]);

  function clone(value) { return value == null ? value : JSON.parse(JSON.stringify(value)); }
  function text(value) { return String(value ?? "").trim(); }
  function validIso(value) {
    const v = text(value);
    return v && !Number.isNaN(Date.parse(v)) ? v : null;
  }
  function normalizeCheckState(value) {
    const v = text(value);
    return CHECK_STATES.has(v) ? v : "";
  }

  function normalizeCloudRecord(raw = {}) {
    return Object.freeze({
      api_key: text(raw.api_key ?? raw.apiKey),
      folder_id: text(raw.folder_id ?? raw.folderId),
      checked_at: validIso(raw.checked_at ?? raw.checkedAt),
      check_state: normalizeCheckState(raw.check_state ?? raw.checkState)
    });
  }

  function normalizeWebmasterRecord(raw = {}) {
    const userId = text(raw.user_id ?? raw.userId);
    return Object.freeze({
      oauth_token: text(raw.oauth_token ?? raw.oauthToken),
      user_id: /^\d+$/.test(userId) ? userId : "",
      verified_at: validIso(raw.verified_at ?? raw.verifiedAt),
      check_state: normalizeCheckState(raw.check_state ?? raw.checkState)
    });
  }

  function hasOwnRecord(raw, service) {
    return Boolean(raw && typeof raw === "object" && !Array.isArray(raw) && raw[service] && typeof raw[service] === "object" && !Array.isArray(raw[service]));
  }

  function normalizeCredentials(raw = {}, { legacyApiKey = "", legacyFolderId = "" } = {}) {
    const source = raw && typeof raw === "object" && !Array.isArray(raw) ? raw : {};
    const legacyCloud = { api_key: text(legacyApiKey), folder_id: text(legacyFolderId), checked_at: null, check_state: "" };
    const wordstat = normalizeCloudRecord(hasOwnRecord(source, "wordstat") ? source.wordstat : legacyCloud);
    const search = normalizeCloudRecord(hasOwnRecord(source, "search") ? source.search : legacyCloud);
    const webmaster = normalizeWebmasterRecord(hasOwnRecord(source, "webmaster") ? source.webmaster : {});
    return Object.freeze({ wordstat, search, webmaster });
  }

  function migrateStorageRecord(raw = {}, legacyApiKey = "", legacyFolderId = "") {
    const normalized = normalizeCredentials(raw, { legacyApiKey, legacyFolderId });
    const changed = JSON.stringify(raw && typeof raw === "object" && !Array.isArray(raw) ? raw : {}) !== JSON.stringify(normalized);
    return Object.freeze({ credentials: normalized, changed });
  }

  function normalizeBackupCredentials(settings = {}, backupVersion = BACKUP_VERSION) {
    const version = Number(backupVersion || 0);
    if (version === 2) {
      const cloud = settings?.wordstat && typeof settings.wordstat === "object" ? settings.wordstat : {};
      return normalizeCredentials({}, { legacyApiKey: cloud.api_key, legacyFolderId: cloud.folder_id });
    }
    if (version === BACKUP_VERSION) {
      return normalizeCredentials(settings?.credentials || {});
    }
    const error = new Error(`Неподдерживаемая версия backup: ${backupVersion}`);
    error.code = "UNSUPPORTED_BACKUP_VERSION";
    throw error;
  }

  function exportCredentialPayload(raw = {}, { legacyApiKey = "", legacyFolderId = "" } = {}) {
    return clone(normalizeCredentials(raw, { legacyApiKey, legacyFolderId }));
  }

  function publicCredentialStatus(raw = {}, { legacyApiKey = "", legacyFolderId = "" } = {}) {
    const c = normalizeCredentials(raw, { legacyApiKey, legacyFolderId });
    return Object.freeze({
      wordstat: Object.freeze({ has_api_key: Boolean(c.wordstat.api_key), has_folder_id: Boolean(c.wordstat.folder_id), folder_id: c.wordstat.folder_id || null, checked_at: c.wordstat.checked_at, check_state: c.wordstat.check_state }),
      search: Object.freeze({ has_api_key: Boolean(c.search.api_key), has_folder_id: Boolean(c.search.folder_id), folder_id: c.search.folder_id || null, checked_at: c.search.checked_at, check_state: c.search.check_state }),
      webmaster: Object.freeze({ has_oauth_token: Boolean(c.webmaster.oauth_token), has_user_id: Boolean(c.webmaster.user_id), user_id: c.webmaster.user_id || null, verified_at: c.webmaster.verified_at, check_state: c.webmaster.check_state })
    });
  }

  function withServiceCredential(raw = {}, service, nextRecord = {}, options = {}) {
    const normalized = normalizeCredentials(raw, options);
    const value = String(service || "").trim();
    if (!SERVICES.includes(value)) {
      const error = new Error(`Неизвестный сервис: ${service || "unknown"}`);
      error.code = "UNKNOWN_SERVICE";
      throw error;
    }
    const next = clone(normalized);
    next[value] = value === "webmaster" ? normalizeWebmasterRecord(nextRecord) : normalizeCloudRecord(nextRecord);
    return Object.freeze(next);
  }

  globalThis.YMBCredentialStoreModel = Object.freeze({
    STORAGE_KEY,
    SETTINGS_SCHEMA_VERSION,
    BACKUP_VERSION,
    SERVICES,
    normalizeCloudRecord,
    normalizeWebmasterRecord,
    normalizeCredentials,
    migrateStorageRecord,
    normalizeBackupCredentials,
    exportCredentialPayload,
    publicCredentialStatus,
    withServiceCredential
  });
})();
