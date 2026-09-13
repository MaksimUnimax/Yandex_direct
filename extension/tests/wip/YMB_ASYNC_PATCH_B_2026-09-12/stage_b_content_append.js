
;(() => {
  "use strict";

  const MESSAGE_TYPE = "YMB_ASYNC_POPUP_ACTION";
  const SEARCH_SERVICE = "search";
  const AUTORUN_INACTIVE = new Set(["paused", "stopped", "error"]);
  const inFlight = new Set();

  function canonicalConversationUrl() {
    const node = document.querySelector('link[rel="canonical"]');
    return String(node?.href || node?.getAttribute?.("href") || "").trim();
  }

  function currentConversationKey() {
    return String(BB2ConversationIdentity.identityFromCandidates([location.href, canonicalConversationUrl()])?.conversation_key || "");
  }

  function sendWorker(message) {
    return new Promise((resolve, reject) => {
      try {
        chrome.runtime.sendMessage(message, (response) => {
          const error = chrome.runtime.lastError;
          if (error) reject(new Error(error.message || String(error)));
          else resolve(response);
        });
      } catch (error) {
        reject(error);
      }
    });
  }

  function safeJobId(value) {
    const jobId = String(value || "").trim();
    if (!jobId || jobId.length > 256 || /[\u0000-\u001f\u007f]/.test(jobId)) return "";
    return jobId;
  }

  function buildManualBlock(message) {
    const jobId = safeJobId(message?.job_id);
    if (!jobId) throw Object.assign(new Error("Некорректный deferred Search job."), { code: "ASYNC_POPUP_JOB_INVALID" });
    if (message.action === "collect_one") {
      return `SEARCH_ASYNC_BATCH_API_V1\n${JSON.stringify({ action: "collectN", jobId, count: 1 })}`;
    }
    if (message.action === "export_page") {
      const revision = Number(message.revision);
      if (!Number.isSafeInteger(revision) || revision < 0) {
        throw Object.assign(new Error("Некорректная ревизия deferred Search job."), { code: "ASYNC_POPUP_REVISION_INVALID" });
      }
      return `SEARCH_ASYNC_BATCH_API_V1\n${JSON.stringify({ action: "exportPage", jobId, after: -1, limit: 25, revision })}`;
    }
    throw Object.assign(new Error("Неподдерживаемое popup-действие."), { code: "ASYNC_POPUP_ACTION_UNSUPPORTED" });
  }

  function autorunAllowsManual(state) {
    const run = state?.auto_run;
    if (!run) return true;
    return AUTORUN_INACTIVE.has(String(run.status || "").toLowerCase());
  }

  async function executePopupAction(message) {
    const currentKey = currentConversationKey();
    const requestedKey = String(message?.conversation_key || "");
    if (!currentKey || requestedKey !== currentKey) {
      return { ok: false, accepted: false, code: "ASYNC_POPUP_CONVERSATION_MISMATCH", request_executed: false };
    }
    const jobId = safeJobId(message?.job_id);
    if (!jobId) return { ok: false, accepted: false, code: "ASYNC_POPUP_JOB_INVALID", request_executed: false };
    if (!new Set(["collect_one", "export_page"]).has(message?.action)) {
      return { ok: false, accepted: false, code: "ASYNC_POPUP_ACTION_UNSUPPORTED", request_executed: false };
    }

    const lockKey = `${currentKey}\n${jobId}\n${message.action}`;
    if (inFlight.has(lockKey)) {
      return { ok: false, accepted: false, code: "ASYNC_POPUP_ACTION_IN_FLIGHT", request_executed: false };
    }
    inFlight.add(lockKey);
    try {
      const stateResponse = await sendWorker({ type: "WS_GET_STATE", conversation_key: currentKey });
      const state = stateResponse?.state;
      if (!stateResponse?.ok || !state) {
        return { ok: false, accepted: false, code: stateResponse?.code || "ASYNC_POPUP_STATE_UNAVAILABLE", error: stateResponse?.error || "Состояние Bridge недоступно.", request_executed: false };
      }
      if (state.manual_mode !== true) {
        return { ok: false, accepted: false, code: "ASYNC_POPUP_MANUAL_MODE_OFF", request_executed: false };
      }
      if (String(state.service_context?.active_service || "") !== SEARCH_SERVICE) {
        return { ok: false, accepted: false, code: "ASYNC_POPUP_SEARCH_NOT_ACTIVE", request_executed: false };
      }
      if (!autorunAllowsManual(state)) {
        return { ok: false, accepted: false, code: "ASYNC_POPUP_AUTORUN_NOT_PAUSED", request_executed: false };
      }

      let blockText;
      try { blockText = buildManualBlock(message); }
      catch (error) {
        return { ok: false, accepted: false, code: error?.code || "ASYNC_POPUP_ACTION_INVALID", error: error?.message || String(error), request_executed: false };
      }
      const response = await sendWorker({
        type: "WS_EXECUTE_MANUAL_BLOCK",
        conversation_key: currentKey,
        block_text: blockText,
        manual_request_token: BB2ManualControls.makeId("popup-async")
      });
      return {
        ok: response?.ok === true,
        accepted: response?.ok === true && response?.accepted !== false,
        code: response?.code || null,
        error: response?.error || null,
        request_executed: response?.request_executed ?? false
      };
    } catch (error) {
      return { ok: false, accepted: false, code: error?.code || "ASYNC_POPUP_ACTION_ERROR", error: error?.message || String(error), request_executed: false };
    } finally {
      inFlight.delete(lockKey);
    }
  }

  chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
    if (message?.type !== MESSAGE_TYPE) return false;
    void executePopupAction(message).then(sendResponse).catch((error) => sendResponse({
      ok: false,
      accepted: false,
      code: error?.code || "ASYNC_POPUP_ACTION_ERROR",
      error: error?.message || String(error),
      request_executed: false
    }));
    return true;
  });

  if (globalThis.__YMB_ASYNC_POPUP_CONTENT_TEST__ === true) {
    globalThis.__YMB_ASYNC_POPUP_CONTENT_TEST_API__ = Object.freeze({ safeJobId, buildManualBlock, autorunAllowsManual, executePopupAction });
  }
})();
