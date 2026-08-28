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

  function isPhase3RuntimeMessage(message) {
    return String(message?.type || "").startsWith("YMB_");
  }

  if (nativeAddListener) {
    const outerAddListener = function phase3CompatibleAddListener(listener) {
      if (typeof listener !== "function") return nativeAddListener(listener);
      return nativeAddListener((message, sender, sendResponse) => {
        // The accepted Phase-2 worker owns WS_* messages. Phase-3 YMB_* messages
        // must be left unanswered here so webmaster_worker_runtime.js is the
        // single responder; otherwise the legacy UNKNOWN_MESSAGE response races
        // the Phase-3 response in real Chrome.
        if (isPhase3RuntimeMessage(message)) return false;
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

  importScripts(
    "shared/provider_batch_job_model.js",
    "shared/wordstat_batch_protocol.js",
    "shared/wordstat_batch_runtime.js",
    "shared/wordstat_batch_transport.js"
  );
  importScripts("service_worker_bootstrap.js");

  if (outerWrapped) {
    try { runtimeEvent.addListener = nativeAddListener; } catch {}
  }

  importScripts("wordstat_batch_worker_transport.js");
  importScripts("webmaster_worker_runtime.js");
  importScripts(
    "shared/google_search_console_protocol.js",
    "shared/google_search_console_runtime.js",
    "google_search_console_worker_runtime.js"
  );
  importScripts(
    "shared/search_batch_protocol.js",
    "shared/search_batch_projection.js",
    "shared/search_batch_runtime.js",
    "shared/search_batch_transport.js",
    "search_batch_worker_transport.js"
  );
})();