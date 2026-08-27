(() => {
  "use strict";

  const Model = globalThis.YMBCredentialStoreModel;
  const CredentialRuntime = globalThis.YMBCredentialRuntime;
  const Policy = globalThis.YMBPolicyModel;
  if (!Model || !CredentialRuntime || !Policy) throw new Error("Phase 5 settings backup prerequisites are unavailable.");

  const BACKUP_FORMAT = "YMB_SETTINGS_BACKUP";
  const BACKUP_VERSION = Model.BACKUP_VERSION;
  const SETTINGS_SCHEMA_VERSION = Model.SETTINGS_SCHEMA_VERSION;
  const ROLLBACK_KEY = "ymb_settings_migration_rollback_backup";
  const KEYS = Object.freeze({
    API_KEY: "wsmb_api_key", FOLDER_ID: "wsmb_folder_id", AUTO_SEND: "wsmb_auto_send",
    CONVERSATION_BINDINGS: "wsmb_conversation_bindings", MANUAL_MODES: "wsmb_manual_modes",
    MANUAL_OPERATIONS: "wsmb_manual_operations", REPORT_PREFIXES: "wsmb_report_prefixes",
    AUTO_START_PROMPTS: "wsmb_auto_start_prompts", AUTO_RUNS: "wsmb_auto_runs",
    SERVICE_CONTEXTS: "ymb_service_contexts", WORDSTAT_POLICY: "ymb_wordstat_policy",
    SEARCH_POLICY: "ymb_search_policy", WEBMASTER_POLICY: "ymb_webmaster_policy", METRIKA_POLICY: "ymb_metrika_policy", DIRECT_POLICY: "ymb_direct_policy",
    DEBUG_MODE: "ymb_debug_mode", SETTINGS_SCHEMA: "ymb_settings_schema_version",
    SEND_BUTTON_PROFILE: "wsmb_send_button_profile", COPY_BUTTON_PROFILES: "wsmb_copy_button_profiles"
  });
  const TERMINAL_RUN_STATUSES = new Set(["stopped", "error"]);
  const TERMINAL_MANUAL_STATUSES = new Set(["completed", "error", "cancelled"]);

  function clone(value) { return value == null ? value : JSON.parse(JSON.stringify(value)); }
  function trim(value) { return String(value ?? "").trim(); }
  function record(value) { return value && typeof value === "object" && !Array.isArray(value) ? value : {}; }
  function stableJson(value) {
    if (value === null || typeof value !== "object") return JSON.stringify(value);
    if (Array.isArray(value)) return `[${value.map((item) => stableJson(item)).join(",")}]`;
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stableJson(value[key])}`).join(",")}}`;
  }
  function mergeRecords(current, incoming) { return { ...record(current), ...record(incoming) }; }
  function mergeArrays(current, incoming) {
    const out = []; const seen = new Set();
    for (const item of [...(Array.isArray(current) ? current : []), ...(Array.isArray(incoming) ? incoming : [])]) {
      const fp = stableJson(item); if (seen.has(fp)) continue; seen.add(fp); out.push(clone(item));
    }
    return out;
  }
  function mergeCopyProfiles(currentValue, incomingValue) {
    if (Array.isArray(currentValue) || Array.isArray(incomingValue)) return mergeArrays(currentValue, incomingValue);
    const current = record(currentValue); const incoming = record(incomingValue); const out = clone(current);
    for (const [key, next] of Object.entries(incoming)) {
      const old = current[key];
      if (Array.isArray(old) || Array.isArray(next)) out[key] = mergeArrays(old, next);
      else if (old && next && typeof old === "object" && typeof next === "object") out[key] = { ...clone(old), ...clone(next) };
      else if (next !== undefined && next !== null) out[key] = clone(next);
    }
    return out;
  }
  function hasActiveRun(data) { return Object.values(record(data[KEYS.AUTO_RUNS])).some((run) => run && !TERMINAL_RUN_STATUSES.has(String(run.status || ""))); }
  function hasActiveManual(data) { return Object.values(record(data[KEYS.MANUAL_OPERATIONS])).some((op) => op && !TERMINAL_MANUAL_STATUSES.has(String(op.status || ""))); }
  function canonical(value) {
    if (value === null || typeof value !== "object") return JSON.stringify(value);
    if (Array.isArray(value)) return `[${value.map((item) => canonical(item === undefined ? null : item)).join(",")}]`;
    return `{${Object.keys(value).sort().filter((key) => value[key] !== undefined).map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
  }
  async function checksum(settings) {
    const bytes = new TextEncoder().encode(canonical(settings)); const digest = await crypto.subtle.digest("SHA-256", bytes);
    return [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
  }

  async function exportBackup() {
    const data = await chrome.storage.local.get(Object.values(KEYS).concat(Model.STORAGE_KEY));
    const credentials = Model.exportCredentialPayload(data[Model.STORAGE_KEY], { legacyApiKey: data[KEYS.API_KEY], legacyFolderId: data[KEYS.FOLDER_ID] });
    const settings = {
      credentials,
      auto_send: data[KEYS.AUTO_SEND] !== false,
      send_button_profile: clone(data[KEYS.SEND_BUTTON_PROFILE] || null),
      copy_button_profiles: clone(data[KEYS.COPY_BUTTON_PROFILES] || {}),
      conversation_bindings: clone(data[KEYS.CONVERSATION_BINDINGS] || {}),
      manual_modes: clone(data[KEYS.MANUAL_MODES] || {}),
      report_prefixes: clone(data[KEYS.REPORT_PREFIXES] || {}),
      auto_start_prompts: clone(data[KEYS.AUTO_START_PROMPTS] || {}),
      service_contexts: clone(data[KEYS.SERVICE_CONTEXTS] || {}),
      wordstat_policy: Policy.normalizeWordstatPolicy(data[KEYS.WORDSTAT_POLICY] || {}),
      search_policy: Policy.normalizeSearchPolicy(data[KEYS.SEARCH_POLICY] || {}),
      webmaster_policy: Policy.normalizeWebmasterPolicy(data[KEYS.WEBMASTER_POLICY] || {}),
      metrika_policy: Policy.normalizeMetrikaPolicy(data[KEYS.METRIKA_POLICY] || {}),
      direct_policy: Policy.normalizeDirectPolicy(data[KEYS.DIRECT_POLICY] || {}),
      debug_mode: data[KEYS.DEBUG_MODE] === true
    };
    return {
      format: BACKUP_FORMAT,
      backup_version: BACKUP_VERSION,
      settings_schema_version: SETTINGS_SCHEMA_VERSION,
      exported_at: new Date().toISOString(),
      extension_version: String(globalThis.YMBProduct?.VERSION || "0.1.1"),
      extension_id: String(chrome.runtime?.id || ""),
      contains_secrets: true,
      settings_sha256: await checksum(settings),
      settings,
      schema: "YMB_SETTINGS_BACKUP_V3",
      version: String(globalThis.YMBProduct?.VERSION || "0.1.1")
    };
  }

  async function validate(backup) {
    if (!backup || typeof backup !== "object" || Array.isArray(backup)) throw Object.assign(new Error("Некорректный backup."), { code: "INVALID_BACKUP" });
    if (backup.format !== BACKUP_FORMAT) throw Object.assign(new Error("Неподдерживаемый формат backup."), { code: "UNSUPPORTED_BACKUP_FORMAT" });
    const version = Number(backup.backup_version || 0);
    if (![2, BACKUP_VERSION].includes(version)) throw Object.assign(new Error("Неподдерживаемая версия backup."), { code: "UNSUPPORTED_BACKUP_VERSION" });
    if (backup.contains_secrets !== true) throw Object.assign(new Error("Backup не помечен как содержащий секреты."), { code: "INVALID_BACKUP_SECRET_MARKER" });
    const settings = backup.settings;
    if (!settings || typeof settings !== "object" || Array.isArray(settings)) throw Object.assign(new Error("Некорректный backup settings payload."), { code: "INVALID_BACKUP_SETTINGS" });
    const supplied = trim(backup.settings_sha256).toLowerCase();
    if (!/^[0-9a-f]{64}$/.test(supplied)) throw Object.assign(new Error("В backup отсутствует корректная контрольная сумма настроек."), { code: "BACKUP_CHECKSUM_MISSING" });
    if (supplied !== await checksum(settings)) throw Object.assign(new Error("Backup изменён или повреждён: контрольная сумма не совпадает."), { code: "BACKUP_CHECKSUM_MISMATCH" });
    return settings;
  }

  async function importBackup(backup) {
    const incoming = await validate(backup); const version = Number(backup.backup_version || 0);
    const imported = Model.normalizeBackupCredentials(incoming, version);
    const incomingCredentialMap = record(incoming.credentials);
    const incomingHasMetrika = version === BACKUP_VERSION && Object.prototype.hasOwnProperty.call(incomingCredentialMap, "metrika") && Object.keys(record(incomingCredentialMap.metrika)).length > 0;
    const incomingHasDirect = version === BACKUP_VERSION && Object.prototype.hasOwnProperty.call(incomingCredentialMap, "direct") && Object.keys(record(incomingCredentialMap.direct)).length > 0;
    const incomingHasDirectPolicy = Object.prototype.hasOwnProperty.call(incoming, "direct_policy") && incoming.direct_policy && typeof incoming.direct_policy === "object" && !Array.isArray(incoming.direct_policy);

    return CredentialRuntime.withExclusiveMutation(async () => {
      // Re-read inside the same credential mutation queue used by per-service Save.
      // This prevents a backup import from restoring a stale credential snapshot over
      // a save that completed while validation was running.
      const data = await chrome.storage.local.get(Object.values(KEYS).concat(Model.STORAGE_KEY));
      if (hasActiveRun(data)) throw Object.assign(new Error("Нельзя импортировать настройки во время активного Autorun."), { code: "IMPORT_ACTIVE_RUN" });
      if (hasActiveManual(data)) throw Object.assign(new Error("Нельзя импортировать настройки во время активной Manual-операции."), { code: "IMPORT_ACTIVE_MANUAL" });

      const rollback = await exportBackup();
      await chrome.storage.local.set({ [ROLLBACK_KEY]: { ...rollback, rollback_context: { reason: "settings_import", created_at: new Date().toISOString(), incoming_settings_schema_version: Number(backup.settings_schema_version || version) } } });

      const current = Model.normalizeCredentials(data[Model.STORAGE_KEY], { legacyApiKey: data[KEYS.API_KEY], legacyFolderId: data[KEYS.FOLDER_ID] });
      let credentials;
      if (version === 2) {
        credentials = Model.normalizeCredentials({ wordstat: imported.wordstat, search: imported.search, webmaster: current.webmaster, metrika: current.metrika, direct: current.direct });
      } else {
        credentials = Model.normalizeCredentials({
          ...imported,
          metrika: incomingHasMetrika ? imported.metrika : current.metrika,
          direct: incomingHasDirect ? imported.direct : current.direct
        });
      }

      await chrome.storage.local.set({
        [Model.STORAGE_KEY]: clone(credentials),
        [KEYS.API_KEY]: credentials.wordstat.api_key,
        [KEYS.FOLDER_ID]: credentials.wordstat.folder_id,
        [KEYS.AUTO_SEND]: incoming.auto_send !== false,
        [KEYS.SEND_BUTTON_PROFILE]: clone(incoming.send_button_profile || data[KEYS.SEND_BUTTON_PROFILE] || null),
        [KEYS.COPY_BUTTON_PROFILES]: mergeCopyProfiles(data[KEYS.COPY_BUTTON_PROFILES], incoming.copy_button_profiles),
        [KEYS.CONVERSATION_BINDINGS]: mergeRecords(data[KEYS.CONVERSATION_BINDINGS], incoming.conversation_bindings),
        [KEYS.MANUAL_MODES]: mergeRecords(data[KEYS.MANUAL_MODES], incoming.manual_modes),
        [KEYS.REPORT_PREFIXES]: mergeRecords(data[KEYS.REPORT_PREFIXES], incoming.report_prefixes),
        [KEYS.AUTO_START_PROMPTS]: mergeRecords(data[KEYS.AUTO_START_PROMPTS], incoming.auto_start_prompts),
        [KEYS.SERVICE_CONTEXTS]: mergeRecords(data[KEYS.SERVICE_CONTEXTS], incoming.service_contexts),
        [KEYS.WORDSTAT_POLICY]: Policy.normalizeWordstatPolicy(incoming.wordstat_policy || data[KEYS.WORDSTAT_POLICY] || {}),
        [KEYS.SEARCH_POLICY]: Policy.normalizeSearchPolicy(incoming.search_policy || data[KEYS.SEARCH_POLICY] || {}),
        [KEYS.WEBMASTER_POLICY]: Policy.normalizeWebmasterPolicy(incoming.webmaster_policy || data[KEYS.WEBMASTER_POLICY] || {}),
        [KEYS.METRIKA_POLICY]: Policy.normalizeMetrikaPolicy(incoming.metrika_policy || data[KEYS.METRIKA_POLICY] || {}),
        [KEYS.DIRECT_POLICY]: Policy.normalizeDirectPolicy(incomingHasDirectPolicy ? incoming.direct_policy : (data[KEYS.DIRECT_POLICY] || {})),
        [KEYS.DEBUG_MODE]: incoming.debug_mode === true,
        [KEYS.SETTINGS_SCHEMA]: SETTINGS_SCHEMA_VERSION
      });
      return {
        imported: true,
        backup_version: version,
        settings_schema_version: SETTINGS_SCHEMA_VERSION,
        settings_sha256: trim(backup.settings_sha256).toLowerCase(),
        active_runtime_state_untouched: true,
        metrika_credential_preserved_when_absent: !incomingHasMetrika,
        direct_credential_preserved_when_absent: !incomingHasDirect,
        direct_policy_preserved_when_absent: !incomingHasDirectPolicy
      };
    });
  }

  globalThis.YMBSettingsBackupV3Runtime = Object.freeze({ exportBackup, validate, importBackup, checksum });
})();
