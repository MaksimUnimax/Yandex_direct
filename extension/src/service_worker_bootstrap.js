(() => {
  "use strict";

  const ROLLBACK_KEY = "ymb_settings_migration_rollback_backup";
  const SETTINGS_SCHEMA_KEY = "ymb_settings_schema_version";
  const SETTINGS_SCHEMA_VERSION = 2;
  const LEGACY_REPORT_PREFIX_KEY = "wsmb_report_prefix_configs";
  const REPORT_PREFIX_KEY = "wsmb_report_prefixes";
  const API_KEY = "wsmb_api_key";
  const FOLDER_ID_KEY = "wsmb_folder_id";
  const AUTO_SEND_KEY = "wsmb_auto_send";
  const CONVERSATION_BINDINGS_KEY = "wsmb_conversation_bindings";
  const MANUAL_MODES_KEY = "wsmb_manual_modes";
  const MANUAL_OPERATIONS_KEY = "wsmb_manual_operations";
  const AUTO_START_PROMPTS_KEY = "wsmb_auto_start_prompts";
  const AUTO_RUNS_KEY = "wsmb_auto_runs";
  const SERVICE_CONTEXTS_KEY = "ymb_service_contexts";
  const WORDSTAT_POLICY_KEY = "ymb_wordstat_policy";
  const SEARCH_POLICY_KEY = "ymb_search_policy";
  const DEBUG_MODE_KEY = "ymb_debug_mode";
  const SEND_BUTTON_PROFILE_KEY = "wsmb_send_button_profile";
  const COPY_BUTTON_PROFILES_KEY = "wsmb_copy_button_profiles";
  const TERMINAL_RUN_STATUSES = new Set(["stopped", "error"]);
  const TERMINAL_MANUAL_STATUSES = new Set(["completed", "error", "cancelled"]);
  const IMPORT_MESSAGE_TYPES = new Set(["WS_IMPORT_BACKUP", "WS_IMPORT_SETTINGS"]);

  const originalGet = chrome.storage.local.get.bind(chrome.storage.local);
  const originalSet = chrome.storage.local.set.bind(chrome.storage.local);
  const runtimeEvent = chrome.runtime?.onMessage || null;
  const originalAddRuntimeListener = runtimeEvent && typeof runtimeEvent.addListener === "function"
    ? runtimeEvent.addListener.bind(runtimeEvent)
    : null;
  let preservingRollback = false;

  function clone(value) {
    return value == null ? value : JSON.parse(JSON.stringify(value));
  }

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
    return Object.hasOwn(values, API_KEY)
      && Object.hasOwn(values, FOLDER_ID_KEY)
      && Object.hasOwn(values, WORDSTAT_POLICY_KEY)
      && Object.hasOwn(values, SEARCH_POLICY_KEY);
  }

  chrome.storage.local.set = async function guardedStorageSet(values) {
    if (!preservingRollback && isSettingsImportMutation(values)) {
      preservingRollback = true;
      try {
        if (typeof globalThis.exportSettingsBackup !== "function") {
          throw Object.assign(new Error("Не удалось подготовить локальную копию настроек перед импортом."), { code: "ROLLBACK_BACKUP_UNAVAILABLE" });
        }
        const rollback = await globalThis.exportSettingsBackup();
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

  function mergeRecordMaps(currentValue, incomingValue) {
    return { ...isRecordMap(currentValue), ...isRecordMap(incomingValue) };
  }

  function preserveActiveConversationEntries(mergedValue, currentValue, activeConversationKeys) {
    const merged = { ...isRecordMap(mergedValue) };
    const current = isRecordMap(currentValue);
    for (const key of activeConversationKeys) {
      if (Object.hasOwn(current, key)) merged[key] = clone(current[key]);
      else delete merged[key];
    }
    return merged;
  }

  function stableJson(value) {
    if (value === null || typeof value !== "object") return JSON.stringify(value);
    if (Array.isArray(value)) return `[${value.map((item) => stableJson(item)).join(",")}]`;
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stableJson(value[key])}`).join(",")}}`;
  }

  function mergeArraysWithoutLoss(currentValue, incomingValue) {
    const result = [];
    const seen = new Set();
    for (const item of [...(Array.isArray(currentValue) ? currentValue : []), ...(Array.isArray(incomingValue) ? incomingValue : [])]) {
      const fingerprint = stableJson(item);
      if (seen.has(fingerprint)) continue;
      seen.add(fingerprint);
      result.push(clone(item));
    }
    return result;
  }

  function mergeCopyProfilesWithoutLoss(currentValue, incomingValue) {
    if (Array.isArray(currentValue) || Array.isArray(incomingValue)) {
      return mergeArraysWithoutLoss(currentValue, incomingValue);
    }
    const current = isRecordMap(currentValue);
    const incoming = isRecordMap(incomingValue);
    const out = { ...clone(current) };
    for (const [key, incomingItem] of Object.entries(incoming)) {
      const currentItem = current[key];
      if (Array.isArray(currentItem) || Array.isArray(incomingItem)) {
        out[key] = mergeArraysWithoutLoss(currentItem, incomingItem);
      } else if (currentItem && incomingItem && typeof currentItem === "object" && typeof incomingItem === "object") {
        out[key] = { ...clone(currentItem), ...clone(incomingItem) };
      } else if (incomingItem !== undefined && incomingItem !== null) {
        out[key] = clone(incomingItem);
      }
    }
    return out;
  }

  function activeConversationKeys(current) {
    const active = new Set();
    for (const [key, run] of Object.entries(isRecordMap(current[AUTO_RUNS_KEY]))) {
      if (run && !TERMINAL_RUN_STATUSES.has(String(run.status || ""))) active.add(key);
    }
    for (const [key, operation] of Object.entries(isRecordMap(current[MANUAL_OPERATIONS_KEY]))) {
      if (operation && !TERMINAL_MANUAL_STATUSES.has(String(operation.status || ""))) active.add(key);
    }
    return active;
  }

  function importedApiKey(incoming, current) {
    const text = String(incoming?.wordstat?.api_key || "").trim();
    return text || String(current[API_KEY] || "");
  }

  function importedFolderId(incoming, current) {
    const text = String(incoming?.wordstat?.folder_id || "").trim();
    return text || String(current[FOLDER_ID_KEY] || "");
  }

  function normalizedPolicy(service, value, fallback) {
    const model = globalThis.YMBPolicyModel;
    if (!model) return clone(value || fallback || {});
    if (service === "search" && typeof model.normalizeSearchPolicy === "function") return model.normalizeSearchPolicy(value || fallback || {});
    if (service === "wordstat" && typeof model.normalizeWordstatPolicy === "function") return model.normalizeWordstatPolicy(value || fallback || {});
    return clone(value || fallback || {});
  }

  async function compatibleSettingsImport(backup) {
    if (typeof globalThis.validateSettingsBackupEnvelope !== "function") {
      throw Object.assign(new Error("Проверка backup недоступна."), { code: "SETTINGS_IMPORT_VALIDATOR_UNAVAILABLE" });
    }
    const incoming = await globalThis.validateSettingsBackupEnvelope(backup);
    const keys = [
      API_KEY, FOLDER_ID_KEY, AUTO_SEND_KEY, CONVERSATION_BINDINGS_KEY, MANUAL_MODES_KEY,
      MANUAL_OPERATIONS_KEY, REPORT_PREFIX_KEY, AUTO_START_PROMPTS_KEY, AUTO_RUNS_KEY,
      SERVICE_CONTEXTS_KEY, WORDSTAT_POLICY_KEY, SEARCH_POLICY_KEY, DEBUG_MODE_KEY,
      SEND_BUTTON_PROFILE_KEY, COPY_BUTTON_PROFILES_KEY
    ];
    const current = await chrome.storage.local.get(keys);
    const activeKeys = activeConversationKeys(current);

    const mergedBindings = preserveActiveConversationEntries(
      mergeRecordMaps(current[CONVERSATION_BINDINGS_KEY], incoming.conversation_bindings),
      current[CONVERSATION_BINDINGS_KEY], activeKeys
    );
    const mergedManualModes = preserveActiveConversationEntries(
      mergeRecordMaps(current[MANUAL_MODES_KEY], incoming.manual_modes),
      current[MANUAL_MODES_KEY], activeKeys
    );
    const mergedPrefixes = preserveActiveConversationEntries(
      mergeRecordMaps(current[REPORT_PREFIX_KEY], incoming.report_prefixes),
      current[REPORT_PREFIX_KEY], activeKeys
    );
    const mergedPrompts = preserveActiveConversationEntries(
      mergeRecordMaps(current[AUTO_START_PROMPTS_KEY], incoming.auto_start_prompts),
      current[AUTO_START_PROMPTS_KEY], activeKeys
    );
    const mergedServiceContexts = preserveActiveConversationEntries(
      mergeRecordMaps(current[SERVICE_CONTEXTS_KEY], incoming.service_contexts),
      current[SERVICE_CONTEXTS_KEY], activeKeys
    );

    const values = {
      [API_KEY]: importedApiKey(incoming, current),
      [FOLDER_ID_KEY]: importedFolderId(incoming, current),
      [AUTO_SEND_KEY]: incoming.auto_send !== false,
      [SEND_BUTTON_PROFILE_KEY]: incoming.send_button_profile || current[SEND_BUTTON_PROFILE_KEY] || null,
      [COPY_BUTTON_PROFILES_KEY]: mergeCopyProfilesWithoutLoss(current[COPY_BUTTON_PROFILES_KEY], incoming.copy_button_profiles),
      [CONVERSATION_BINDINGS_KEY]: mergedBindings,
      [MANUAL_MODES_KEY]: mergedManualModes,
      [REPORT_PREFIX_KEY]: mergedPrefixes,
      [AUTO_START_PROMPTS_KEY]: mergedPrompts,
      [SERVICE_CONTEXTS_KEY]: mergedServiceContexts,
      [WORDSTAT_POLICY_KEY]: normalizedPolicy("wordstat", incoming.wordstat_policy, current[WORDSTAT_POLICY_KEY]),
      [SEARCH_POLICY_KEY]: normalizedPolicy("search", incoming.search_policy, current[SEARCH_POLICY_KEY]),
      [DEBUG_MODE_KEY]: incoming.debug_mode === true,
      [SETTINGS_SCHEMA_KEY]: SETTINGS_SCHEMA_VERSION
    };

    await chrome.storage.local.set(values);
    return {
      imported: true,
      backup_version: SETTINGS_SCHEMA_VERSION,
      settings_sha256: String(backup?.settings_sha256 || "").toLowerCase(),
      preserved_active_conversations: activeKeys.size,
      active_runtime_state_untouched: true
    };
  }

  function isImportMessage(message) {
    return IMPORT_MESSAGE_TYPES.has(String(message?.type || ""));
  }

  async function handleCompatibleImportMessage(message) {
    const result = await compatibleSettingsImport(message?.backup || message?.settings);
    const state = typeof globalThis.publicGlobalSettingsState === "function"
      ? await globalThis.publicGlobalSettingsState()
      : null;
    return { ok: true, result, state };
  }

  let runtimeListenerWrapped = false;
  let wrappedAddListener = null;
  if (originalAddRuntimeListener) {
    wrappedAddListener = function addCompatibleRuntimeListener(listener) {
      if (typeof listener !== "function") return originalAddRuntimeListener(listener);
      return originalAddRuntimeListener((message, sender, sendResponse) => {
        if (!isImportMessage(message)) return listener(message, sender, sendResponse);
        Promise.resolve(handleCompatibleImportMessage(message))
          .then(sendResponse)
          .catch((error) => sendResponse({
            ok: false,
            code: error?.code || "SETTINGS_IMPORT_FAILED",
            error: error?.message || String(error),
            request_executed: false,
            automatic_retry: false
          }));
        return true;
      });
    };
    try {
      runtimeEvent.addListener = wrappedAddListener;
      runtimeListenerWrapped = runtimeEvent.addListener === wrappedAddListener;
    } catch {}
  }

  importScripts("service_worker.js");

  if (runtimeListenerWrapped) {
    try { runtimeEvent.addListener = originalAddRuntimeListener; } catch {}
  }

  if (globalThis.__YMB_BOOTSTRAP_TEST__ === true) {
    globalThis.__YMB_BOOTSTRAP_TEST_API__ = Object.freeze({
      compatibleSettingsImport,
      mergeCopyProfilesWithoutLoss,
      activeConversationKeys,
      preserveActiveConversationEntries,
      runtimeListenerWrapped
    });
  }
})();