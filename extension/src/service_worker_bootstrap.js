(() => {
  "use strict";

  const ROLLBACK_KEY = "ymb_settings_migration_rollback_backup";
  const SETTINGS_SCHEMA_KEY = "ymb_settings_schema_version";
  const SETTINGS_SCHEMA_VERSION = 2;
  const LEGACY_REPORT_PREFIX_KEY = "wsmb_report_prefix_configs";
  const REPORT_PREFIX_KEY = "wsmb_report_prefixes";
  const originalGet = chrome.storage.local.get.bind(chrome.storage.local);
  const originalSet = chrome.storage.local.set.bind(chrome.storage.local);
  let preservingRollback = false;

  function isRecordMap(value) {
    return value && typeof value === "object" && !Array.isArray(value) ? value : {};
  }

  function requestsReportPrefixes(keys) {
    if (keys == null) return true;
    if (typeof keys === "string") return keys === REPORT_PREFIX_KEY;
    if (Array.isArray(keys)) return keys.includes(REPORT_PREFIX_KEY);
    return typeof keys === "object" && Object.hasOwn(keys, REPORT_PREFIX_KEY);
  }

  chrome.storage.local.get = async function compatibleStorageGet(keys) {
    if (!requestsReportPrefixes(keys)) return originalGet(keys);
    const [requested, prefixData] = await Promise.all([
      originalGet(keys),
      originalGet([LEGACY_REPORT_PREFIX_KEY, REPORT_PREFIX_KEY])
    ]);
    const legacy = isRecordMap(prefixData[LEGACY_REPORT_PREFIX_KEY]);
    const current = isRecordMap(prefixData[REPORT_PREFIX_KEY]);
    if (!Object.keys(legacy).length) return requested;
    const merged = { ...legacy, ...current };
    requested[REPORT_PREFIX_KEY] = merged;
    if (Object.keys(merged).some((key) => !Object.hasOwn(current, key))) {
      try { await originalSet({ [REPORT_PREFIX_KEY]: merged }); } catch {}
    }
    return requested;
  };

  function isSettingsImportMutation(values) {
    if (!values || typeof values !== "object" || Array.isArray(values)) return false;
    if (Number(values[SETTINGS_SCHEMA_KEY]) !== SETTINGS_SCHEMA_VERSION) return false;
    return Object.hasOwn(values, "wsmb_api_key")
      && Object.hasOwn(values, "wsmb_folder_id")
      && Object.hasOwn(values, "ymb_wordstat_policy")
      && Object.hasOwn(values, "ymb_search_policy");
  }

  chrome.storage.local.set = async function guardedStorageSet(values) {
    if (!preservingRollback && isSettingsImportMutation(values)) {
      preservingRollback = true;
      try {
        if (typeof exportSettingsBackup !== "function") {
          throw Object.assign(new Error("Не удалось подготовить локальную копию настроек перед импортом."), { code: "ROLLBACK_BACKUP_UNAVAILABLE" });
        }
        const rollback = await exportSettingsBackup();
        await originalSet({
          [ROLLBACK_KEY]: {
            ...rollback,
            rollback_context: {
              reason: "settings_import",
              created_at: new Date().toISOString(),
              incoming_settings_schema_version: SETTINGS_SCHEMA_VERSION
            }
          }
        });
      } finally {
        preservingRollback = false;
      }
    }
    return originalSet(values);
  };

  importScripts("service_worker.js");
})();
