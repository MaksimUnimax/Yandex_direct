(() => {
  "use strict";

  const CHATGPT_HOSTS = new Set(["chatgpt.com", "chat.openai.com"]);
  const CONTENT_FILES = Object.freeze([
    "shared/product.js",
    "shared/conversation_identity.js",
    "shared/service_registry.js",
    "shared/wordstat_protocol.js",
    "shared/search_xml.js",
    "shared/search_protocol.js",
    "shared/metrika_protocol.js",
    "shared/autorun_model.js",
    "shared/manual_controls.js",
    "shared/composer_send.js",
    "shared/proven_writing_block_capture.js",
    "content_script.js"
  ]);

  const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  function setBootstrapStatus(text, level = "") {
    const node = document.getElementById("status");
    if (!node) return;
    node.textContent = String(text || "");
    node.dataset.level = level;
  }

  function preserveBootstrapFailureThroughStartup(errorText) {
    const node = document.getElementById("status");
    if (!node || typeof MutationObserver !== "function") return null;
    const expected = String(errorText || "");
    const observer = new MutationObserver(() => {
      if (node.textContent === expected && node.dataset.level === "error") return;
      observer.disconnect();
      setBootstrapStatus(expected, "error");
    });
    observer.observe(node, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ["data-level"] });
    return observer;
  }

  function queryActiveTab() {
    return new Promise((resolve, reject) => {
      try {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          const error = chrome.runtime.lastError;
          if (error) reject(new Error(error.message || String(error)));
          else resolve(Array.isArray(tabs) ? tabs[0] || null : null);
        });
      } catch (error) { reject(error); }
    });
  }

  function tabIdentity(tabId) {
    return new Promise((resolve) => {
      try {
        chrome.tabs.sendMessage(tabId, { type: "WS_GET_IDENTITY" }, (response) => {
          const error = chrome.runtime.lastError;
          if (error) { resolve({ delivered: false, error: error.message || String(error), response: null }); return; }
          resolve({ delivered: true, error: "", response: response || null });
        });
      } catch (error) { resolve({ delivered: false, error: error.message || String(error), response: null }); }
    });
  }

  function usableIdentityProbe(probe) {
    if (probe?.delivered !== true) return false;
    const response = probe.response;
    if (response?.ok !== true) return false;
    const conversationKey = String(response?.conversation_key || response?.identity?.conversation_key || "").trim();
    return Boolean(conversationKey);
  }

  async function injectContentBundle(tabId) {
    if (!chrome.scripting?.executeScript) throw new Error("Chrome scripting API недоступен; невозможно восстановить связь с открытым ChatGPT.");
    for (const file of CONTENT_FILES) await chrome.scripting.executeScript({ target: { tabId }, files: [file] });
  }

  function isChatGptTab(tab) {
    if (!tab || !Number.isInteger(Number(tab.id))) return false;
    try { return CHATGPT_HOSTS.has(new URL(tab.url || "").hostname); } catch { return false; }
  }

  async function ensureCurrentChatContext() {
    const tab = await queryActiveTab();
    if (!isChatGptTab(tab)) return { attempted: false, recovered: false, reason: "ACTIVE_TAB_NOT_CHATGPT" };
    const tabId = Number(tab.id); let sawLiveReceiver = false;
    for (let attempt = 0; attempt < 3; attempt += 1) {
      const probe = await tabIdentity(tabId);
      if (usableIdentityProbe(probe)) return { attempted: true, recovered: false, tab_id: tabId, response: probe.response };
      if (probe.delivered) sawLiveReceiver = true;
      if (attempt < 2) await wait(120);
    }
    if (sawLiveReceiver) throw new Error("Связь с ChatGPT есть, но текущий диалог не удалось подтвердить.");

    setBootstrapStatus("Восстанавливаю связь с текущим ChatGPT…");
    await injectContentBundle(tabId);
    let lastError = "";
    for (let attempt = 0; attempt < 25; attempt += 1) {
      const probe = await tabIdentity(tabId);
      if (usableIdentityProbe(probe)) {
        setBootstrapStatus("Связь с ChatGPT восстановлена.", "ok");
        return { attempted: true, recovered: true, tab_id: tabId, response: probe.response };
      }
      if (probe.delivered) lastError = "content script отвечает, но не подтвердил текущий диалог";
      else lastError = probe.error || lastError;
      await wait(80);
    }
    throw new Error(`Не удалось восстановить связь с открытым ChatGPT${lastError ? `: ${lastError}` : "."}`);
  }

  function publishBootstrapResult(result) {
    const source = result && typeof result === "object" ? result : {};
    globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_RESULT__ = Object.freeze({
      attempted: source.attempted === true,
      recovered: source.recovered === true,
      reason: typeof source.reason === "string" ? source.reason : "",
      tab_id: Number.isInteger(Number(source.tab_id)) ? Number(source.tab_id) : null
    });
  }

  function loadPopupRuntime() {
    const script = document.createElement("script");
    script.src = chrome.runtime.getURL("popup.js");
    script.dataset.ymbPopupRuntime = "true";
    script.addEventListener("error", () => setBootstrapStatus("Не удалось загрузить popup.js.", "error"), { once: true });
    (document.body || document.documentElement).appendChild(script);
  }

  void ensureCurrentChatContext()
    .then((result) => publishBootstrapResult(result))
    .catch((error) => {
      const message = String(error?.message || error || "UNKNOWN");
      setBootstrapStatus(message, "error");
      globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_ERROR__ = message;
      preserveBootstrapFailureThroughStartup(message);
    })
    .finally(() => loadPopupRuntime());

  if (globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_TEST__ === true) {
    globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_API__ = Object.freeze({ CONTENT_FILES, isChatGptTab, tabIdentity, usableIdentityProbe, injectContentBundle, ensureCurrentChatContext, publishBootstrapResult, preserveBootstrapFailureThroughStartup });
  }
})();
