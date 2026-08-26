(() => {
  "use strict";

  const IMPORT_TYPES = new Set(["WS_IMPORT_BACKUP", "WS_IMPORT_SETTINGS"]);
  const runtimeEvent = chrome.runtime?.onMessage || null;
  const nativeAddListener = runtimeEvent && typeof runtimeEvent.addListener === "function"
    ? runtimeEvent.addListener.bind(runtimeEvent)
    : null;
  let outerWrapped = false;

  function isManagedSettingsImport(message) {
    if (!IMPORT_TYPES.has(String(message?.type || ""))) return false;
    const backup = message?.backup || message?.settings;
    return [2, 3].includes(Number(backup?.backup_version || 0));
  }

  if (nativeAddListener) {
    const outerAddListener = function phase3CompatibleAddListener(listener) {
      if (typeof listener !== "function") return nativeAddListener(listener);
      return nativeAddListener((message, sender, sendResponse) => {
        if (!isManagedSettingsImport(message)) return listener(message, sender, sendResponse);
        const runtime = globalThis.YMBPhase3Runtime;
        if (!runtime || typeof runtime.importSettingsBackup !== "function") {
          sendResponse({ ok: false, code: "PHASE3_RUNTIME_UNAVAILABLE", error: "Phase 3 runtime не загружен.", request_executed: false, automatic_retry: false });
          return true;
        }
        Promise.resolve(runtime.importSettingsBackup(message?.backup || message?.settings))
          .then(async (result) => ({
            ok: true,
            result,
            state: typeof globalThis.publicGlobalSettingsState === "function" ? await globalThis.publicGlobalSettingsState() : null
          }))
          .then(sendResponse)
          .catch((error) => sendResponse({
            ok: false,
            code: error?.code || "SETTINGS_IMPORT_FAILED",
            error: error?.message || String(error),
            request_executed: error?.request_executed ?? false,
            automatic_retry: false
          }));
        return true;
      });
    };
    try {
      runtimeEvent.addListener = outerAddListener;
      outerWrapped = runtimeEvent.addListener === outerAddListener;
    } catch {}
  }

  importScripts("service_worker_bootstrap.js");

  if (outerWrapped) {
    try { runtimeEvent.addListener = nativeAddListener; } catch {}
  }

  importScripts("webmaster_worker_runtime.js");
})();
