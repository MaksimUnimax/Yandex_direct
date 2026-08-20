(() => {
  "use strict";

  const ROLLBACK_KEY = "ymb_settings_migration_rollback_backup";
  const SETTINGS_SCHEMA_KEY = "ymb_settings_schema_version";
  const SETTINGS_SCHEMA_VERSION = 2;
  const originalSet = chrome.storage.local.set.bind(chrome.storage.local);
  let preservingRollback = false;

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
