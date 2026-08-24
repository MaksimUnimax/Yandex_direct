(() => {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const TERMINAL_RUNS = new Set(["stopped", "error"]);
  const CHATGPT_HOSTS = new Set(["chatgpt.com", "chat.openai.com"]);

  let context = { available: false, tab_id: null, conversation_key: "", identity: null };
  let lastState = null;
  let rendering = false;
  let lastDiagnostics = [];

  function runtimeSend(message) {
    return new Promise((resolve, reject) => {
      try {
        chrome.runtime.sendMessage(message, (response) => {
          const error = chrome.runtime.lastError;
          if (error) reject(new Error(error.message || String(error)));
          else resolve(response);
        });
      } catch (error) { reject(error); }
    });
  }

  function tabSend(tabId, message) {
    return new Promise((resolve, reject) => {
      try {
        chrome.tabs.sendMessage(tabId, message, (response) => {
          const error = chrome.runtime.lastError;
          if (error) reject(new Error(error.message || String(error)));
          else resolve(response);
        });
      } catch (error) { reject(error); }
    });
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

  function showStatus(text, level = "") {
    const node = $("status");
    node.textContent = String(text || "");
    node.dataset.level = level;
  }

  function asNumber(id, fallback = 0) {
    const value = Number($(id).value);
    return Number.isFinite(value) ? value : fallback;
  }

  function asPositiveInt(id, fallback = 1) {
    const value = Math.trunc(asNumber(id, fallback));
    return value > 0 ? value : fallback;
  }

  function wordstatPolicyFromForm() {
    return {
      autorun_enabled: $("wordstatAutorunEnabled").checked,
      manual_enabled: true,
      allowed_methods: ["getTop", "getDynamics", "getRegionsDistribution", "getRegionsTree"],
      max_requests_per_run: asPositiveInt("maxRequestsRun", 100),
      max_cost_rub_per_run: Math.max(0, asNumber("maxCostRun", 10)),
      method_cost_rub: {
        getTop: Math.max(0, asNumber("costGetTop", 0.02)),
        getDynamics: Math.max(0, asNumber("costGetDynamics", 0.02)),
        getRegionsDistribution: Math.max(0, asNumber("costGetRegionsDistribution", 0.05)),
        getRegionsTree: Math.max(0, asNumber("costGetRegionsTree", 0))
      },
      tariff_checked_at: $("tariffCheckedAt").value.trim(),
      tariff_source: $("tariffSource").value.trim()
    };
  }

  function searchPolicyFromForm() {
    return {
      autorun_enabled: $("searchAutorunEnabled").checked,
      manual_enabled: $("searchManualEnabled").checked,
      allowed_methods: ["search"],
      max_requests_per_run: asPositiveInt("searchMaxRequestsRun", 100),
      max_cost_rub_per_run: Math.max(0, asNumber("searchMaxCostRun", 10)),
      method_cost_rub: { search: Math.max(0, asNumber("costSearch", 0.488)) },
      tariff_checked_at: $("searchTariffCheckedAt").value.trim(),
      tariff_source: $("searchTariffSource").value.trim()
    };
  }

  function reportPrefixFromForm() {
    return {
      enabled: $("reportPrefixEnabled").checked,
      text: $("reportPrefixText").value,
      interval: 1
    };
  }

  async function resolveContext() {
    context = { available: false, tab_id: null, conversation_key: "", identity: null };
    const tab = await queryActiveTab();
    if (!tab || !Number.isInteger(Number(tab.id))) return context;
    let host = "";
    try { host = new URL(tab.url || "").hostname; } catch { return context; }
    if (!CHATGPT_HOSTS.has(host)) return context;
    try {
      const page = await tabSend(Number(tab.id), { type: "WS_GET_IDENTITY" });
      const key = String(page?.conversation_key || page?.identity?.conversation_key || "");
      if (!page?.ok || !key) return context;
      context = { available: true, tab_id: Number(tab.id), conversation_key: key, identity: page.identity || null };
    } catch { /* content script may be restarting */ }
    return context;
  }

  function isActiveRun(run) {
    return Boolean(run && !TERMINAL_RUNS.has(String(run.status || "")));
  }

  function copyProfileCount(value) {
    if (Array.isArray(value)) return value.filter(Boolean).length;
    if (!value || typeof value !== "object") return 0;
    if (Array.isArray(value.profiles)) return value.profiles.filter(Boolean).length;
    return Object.values(value).reduce((total, item) => total + (Array.isArray(item) ? item.filter(Boolean).length : (item && typeof item === "object" ? 1 : 0)), 0);
  }

  function renderState(state) {
    rendering = true;
    try {
      lastState = state || {};
      $("versionBadge").textContent = `v${state?.product_version || "0.1.1"}`;
      $("conversationMeta").textContent = context.available ? context.conversation_key : "не определён";
      const service = state?.service_context?.active_service === "search" ? "search" : "wordstat";
      $("activeService").value = service;
      $("activeService").disabled = !context.available || isActiveRun(state?.auto_run) || state?.manual_mode === true;
      $("bindConversation").disabled = !context.available;
      $("bindConversation").textContent = state?.binding ? "Перепривязать диалог" : "Привязать диалог";

      const run = state?.auto_run || null;
      $("runStatus").textContent = run?.status || "—";
      $("runRequests").textContent = `${Number(run?.requests_attempted || 0)} / ${Number(run?.requests_executed || 0)} / ${Number(run?.requests_skipped || 0)}`;
      $("runCost").textContent = `${Number(run?.estimated_cost_rub || 0).toFixed(3)} ₽`;
      $("runSequence").textContent = String(Number(run?.sequence || 0));
      $("lastCommand").textContent = run?.last_method || run?.last_phrase || "—";

      $("manualMode").checked = state?.manual_mode === true;
      const manualBusy = Boolean(state?.manual_operation && !["completed", "error", "cancelled"].includes(state.manual_operation.status));
      const activeRun = isActiveRun(run);
      const paused = run?.status === "paused";
      const runOwnedHere = !activeRun || (context.available && Number(run?.tab_id) === Number(context.tab_id));
      $("manualMode").disabled = !context.available || manualBusy || (activeRun && (!paused || !runOwnedHere));
      if (manualBusy) $("manualModeMeta").textContent = "Предыдущая ручная операция ещё выполняется или доставляется.";
      else if (state?.manual_mode) $("manualModeMeta").textContent = `Включён для ${service}: используйте отдельную кнопку «Яндекс» у блока.`;
      else if (paused) $("manualModeMeta").textContent = "Автоматический режим на паузе: ручной режим можно включить для точечного запроса.";
      else if (activeRun) $("manualModeMeta").textContent = `Выключен: автоматический режим выполняет только ${run?.active_service === "search" ? "SEARCH_API_V1" : "WORDSTAT_API_V1"}.`;
      else $("manualModeMeta").textContent = "Выключен.";

      const wp = state?.wordstat_policy || {};
      $("wordstatAutorunEnabled").checked = wp.autorun_enabled === true;
      $("maxRequestsRun").value = String(wp.max_requests_per_run ?? 100);
      $("maxCostRun").value = String(wp.max_cost_rub_per_run ?? 10);
      $("costGetTop").value = String(wp.method_cost_rub?.getTop ?? 0.02);
      $("costGetDynamics").value = String(wp.method_cost_rub?.getDynamics ?? 0.02);
      $("costGetRegionsDistribution").value = String(wp.method_cost_rub?.getRegionsDistribution ?? 0.05);
      $("costGetRegionsTree").value = String(wp.method_cost_rub?.getRegionsTree ?? 0);
      $("tariffCheckedAt").value = wp.tariff_checked_at || "2026-08-12";
      $("tariffSource").value = wp.tariff_source || "https://aistudio.yandex.ru/docs/ru/search-api/pricing.html";

      const sp = state?.search_policy || {};
      $("searchManualEnabled").checked = sp.manual_enabled === true;
      $("searchAutorunEnabled").checked = sp.autorun_enabled === true;
      $("searchMaxRequestsRun").value = String(sp.max_requests_per_run ?? 100);
      $("searchMaxCostRun").value = String(sp.max_cost_rub_per_run ?? 10);
      $("costSearch").value = String(sp.method_cost_rub?.search ?? 0.488);
      $("searchTariffCheckedAt").value = sp.tariff_checked_at || "2026-08-19";
      $("searchTariffSource").value = sp.tariff_source || "https://aistudio.yandex.ru/docs/ru/search-api/pricing.html";

      const activePolicy = service === "search" ? sp : wp;
      if (state?.manual_mode !== true && activePolicy?.manual_enabled !== true) {
        $("manualMode").disabled = true;
        $("manualModeMeta").textContent = `Ручной режим ${service} запрещён политикой.`;
      }

      $("folderId").value = state?.folder_id || "";
      $("apiKey").value = "";
      $("apiKey").placeholder = state?.has_api_key ? "Ключ сохранён; оставьте пустым, чтобы не менять" : "Введите API key";
      $("autoSend").checked = state?.auto_send !== false;
      $("debugMode").checked = state?.debug_mode === true;

      const sendProfile = state?.send_button_profile || null;
      const copyCount = copyProfileCount(state?.copy_button_profiles);
      $("sendProfileMeta").textContent = sendProfile?.selector ? `Send настроен: ${sendProfile.selector}` : "Send не настроен.";
      $("copyProfileMeta").textContent = copyCount ? `Сохранено Copy-профилей: ${copyCount}` : "Copy не настроен.";
      $("pickSend").disabled = !context.available;
      $("pickCopy").disabled = !context.available;
      $("clearSend").disabled = !sendProfile;
      $("clearCopy").disabled = copyCount === 0;

      const prefix = state?.report_prefix || {};
      $("reportPrefixEnabled").checked = prefix.enabled === true;
      $("reportPrefixText").value = prefix.text || "";
      $("autoStartPromptText").value = state?.auto_start_prompt?.text || "";

      $("startAuto").disabled = !context.available || !state?.binding || activeRun || state?.manual_mode === true || manualBusy || activePolicy?.autorun_enabled !== true;
      $("pauseAuto").disabled = !activeRun || paused || !runOwnedHere;
      $("resumeAuto").disabled = !activeRun || !paused || state?.manual_mode === true || manualBusy || !runOwnedHere;
      $("finishAuto").disabled = !activeRun || !runOwnedHere;
    } finally { rendering = false; }
  }

  function visibleDiagnostics() {
    const filter = $("diagnosticsFilter")?.value || "all";
    if (filter === "error") return lastDiagnostics.filter((record) => String(record?.level || "").toLowerCase() === "error");
    if (filter === "current") return lastDiagnostics.filter((record) => String(record?.conversation_key || record?.detail?.conversation_key || "") === context.conversation_key);
    return lastDiagnostics;
  }

  function renderDiagnostics() {
    const node = $("diagnosticsText");
    if (!node) return;
    const visible = visibleDiagnostics();
    node.value = visible.length ? JSON.stringify(visible, null, 2) : "";
  }

  async function loadDiagnostics() {
    const response = await runtimeSend({ type: "WS_GET_DIAGNOSTICS" });
    if (response?.ok === false) throw new Error(response?.error || response?.code || "Не удалось прочитать диагностику.");
    lastDiagnostics = Array.isArray(response?.diagnostics) ? response.diagnostics : [];
    renderDiagnostics();
    return lastDiagnostics;
  }

  async function refresh() {
    await resolveContext();
    const response = context.available
      ? await runtimeSend({ type: "WS_GET_STATE", conversation_key: context.conversation_key })
      : await runtimeSend({ type: "WS_GET_GLOBAL_STATE", page_context_error: "CHATGPT_CONTEXT_UNAVAILABLE" });
    if (!response?.ok || !response.state) throw new Error(response?.error || response?.code || "Не удалось прочитать состояние расширения.");
    renderState(response.state);
    await loadDiagnostics();
    return response.state;
  }

  async function saveAll({ includeKey = true } = {}) {
    const message = {
      type: "WS_SAVE_SETTINGS",
      folder_id: $("folderId").value.trim(),
      auto_send: $("autoSend").checked,
      debug_mode: $("debugMode").checked,
      wordstat_policy: wordstatPolicyFromForm(),
      search_policy: searchPolicyFromForm()
    };
    const apiKey = $("apiKey").value.trim();
    if (includeKey && apiKey) message.api_key = apiKey;
    if (context.available) {
      message.conversation_key = context.conversation_key;
      message.active_service = $("activeService").value;
      message.report_prefix = reportPrefixFromForm();
    }
    const response = await runtimeSend(message);
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось сохранить настройки.");
    if (response.state) renderState(response.state);
    return response.state || null;
  }

  async function persistTogglePatch(patch) {
    const response = await runtimeSend({ type: "WS_PATCH_TOGGLES", ...(context.available ? { conversation_key: context.conversation_key } : {}), ...patch });
    if (!response?.ok || !response.state) throw new Error(response?.error || response?.code || "Не удалось сохранить переключатель.");
    renderState(response.state);
    return response.state;
  }

  async function withButton(button, fn) {
    const wasDisabled = button.disabled;
    button.disabled = true;
    try { await fn(); }
    catch (error) { showStatus(error.message || String(error), "error"); }
    finally { button.disabled = wasDisabled; }
  }

  $("saveSettings").addEventListener("click", () => withButton($("saveSettings"), async () => {
    await resolveContext();
    await saveAll();
    await refresh();
    showStatus("Настройки сохранены.", "ok");
  }));

  $("activeService").addEventListener("change", () => {
    if (rendering) return;
    const service = $("activeService").value;
    const policy = service === "search" ? lastState?.search_policy : lastState?.wordstat_policy;
    $("startAuto").disabled = !context.available || !lastState?.binding || isActiveRun(lastState?.auto_run) || lastState?.manual_mode === true || policy?.autorun_enabled !== true;
    showStatus(`Выбран ${service}. Нажмите «Сохранить», чтобы закрепить выбор.`);
  });

  $("bindConversation").addEventListener("click", () => withButton($("bindConversation"), async () => {
    await resolveContext();
    if (!context.available) throw new Error("Откройте конкретный диалог ChatGPT.");
    const response = await runtimeSend({ type: "WS_BIND_CONVERSATION", tab_id: context.tab_id });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось привязать диалог.");
    await refresh();
    showStatus("Диалог привязан.", "ok");
  }));

  $("manualMode").addEventListener("change", async () => {
    if (rendering) return;
    const enabled = $("manualMode").checked;
    const previous = !enabled;
    let workerCommitted = false;
    try {
      await resolveContext();
      if (!context.available) throw new Error("Откройте конкретный диалог ChatGPT.");
      const committedService = lastState?.service_context?.active_service === "search" ? "search" : "wordstat";
      if (enabled && $("activeService").value !== committedService) throw new Error("Сначала сохраните выбранный активный сервис.");
      const committed = await runtimeSend({ type: "WS_SET_MANUAL_MODE", conversation_key: context.conversation_key, enabled, tab_id: context.tab_id });
      if (!committed?.ok) throw new Error(committed?.error || committed?.code || "Worker не сохранил ручной режим.");
      workerCommitted = true;
      const applied = await tabSend(context.tab_id, { type: "WS_APPLY_MANUAL_MODE", conversation_key: context.conversation_key, enabled, active_service: committedService });
      if (!applied?.ok || applied.applied !== true) {
        if (enabled) {
          const rollback = await runtimeSend({ type: "WS_SET_MANUAL_MODE", conversation_key: context.conversation_key, enabled: false, tab_id: context.tab_id });
          if (rollback?.ok) {
            try { await tabSend(context.tab_id, { type: "WS_APPLY_MANUAL_MODE", conversation_key: context.conversation_key, enabled: false, active_service: committedService }); } catch {}
          }
        }
        throw new Error(applied?.error || applied?.code || "Страница не подтвердила ручной режим.");
      }
      await refresh();
      showStatus(enabled ? "Ручной режим включён." : "Ручной режим выключен.", "ok");
    } catch (error) {
      if (enabled) $("manualMode").checked = false;
      else $("manualMode").checked = workerCommitted ? false : previous;
      showStatus(error.message || String(error), "error");
    }
  });

  for (const [id, key] of [["autoSend", "auto_send"], ["debugMode", "debug_mode"], ["wordstatAutorunEnabled", "wordstat_autorun_enabled"], ["searchAutorunEnabled", "search_autorun_enabled"]]) {
    $(id).addEventListener("change", async () => {
      if (rendering) return;
      const enabled = $(id).checked;
      try { await persistTogglePatch({ [key]: enabled }); showStatus("Изменение сохранено сразу.", "ok"); }
      catch (error) { $(id).checked = !enabled; showStatus(error.message || String(error), "error"); }
    });
  }

  $("reportPrefixEnabled").addEventListener("change", async () => {
    if (rendering) return;
    const enabled = $("reportPrefixEnabled").checked;
    try {
      if (!context.available) throw new Error("Префикс привязан к конкретному диалогу ChatGPT.");
      await persistTogglePatch({ report_prefix_enabled: enabled });
      showStatus("Переключатель префикса сохранён сразу.", "ok");
    } catch (error) {
      $("reportPrefixEnabled").checked = !enabled;
      showStatus(error.message || String(error), "error");
    }
  });

  $("saveAutoStartPrompt").addEventListener("click", () => withButton($("saveAutoStartPrompt"), async () => {
    if (!context.available) throw new Error("Откройте конкретный диалог ChatGPT.");
    const response = await runtimeSend({ type: "WS_SAVE_AUTO_START_PROMPT", conversation_key: context.conversation_key, active_service: $("activeService").value, text: $("autoStartPromptText").value });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось сохранить стартовый текст.");
    await refresh();
    showStatus("Стартовый текст сохранён.", "ok");
  }));

  $("resetAutoStartPrompt").addEventListener("click", () => withButton($("resetAutoStartPrompt"), async () => {
    if (!context.available) throw new Error("Откройте конкретный диалог ChatGPT.");
    const response = await runtimeSend({ type: "WS_RESET_AUTO_START_PROMPT", conversation_key: context.conversation_key, active_service: $("activeService").value });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось вернуть стандартный текст.");
    await refresh();
    showStatus("Стандартный стартовый текст восстановлен.", "ok");
  }));

  $("startAuto").addEventListener("click", () => withButton($("startAuto"), async () => {
    await resolveContext();
    if (!context.available) throw new Error("Откройте конкретный диалог ChatGPT.");
    await saveAll();
    const service = $("activeService").value;
    const policy = service === "search" ? searchPolicyFromForm() : wordstatPolicyFromForm();
    if (!confirm(`Запустить ${service}? Максимум ${policy.max_requests_per_run} запросов / ${policy.max_cost_rub_per_run} ₽. Автоматический повтор запроса при неизвестном исходе запрещён.`)) return;
    const response = await runtimeSend({ type: "WS_START_AUTORUN", conversation_key: context.conversation_key, tab_id: context.tab_id });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось запустить автоматический режим.");
    await refresh();
    showStatus(`Автоматический режим ${service} запущен.`, "ok");
  }));

  $("pauseAuto").addEventListener("click", () => withButton($("pauseAuto"), async () => {
    await resolveContext();
    if (!context.available) throw new Error("Откройте конкретный диалог ChatGPT.");
    const response = await runtimeSend({ type: "WS_PAUSE_AUTORUN", conversation_key: context.conversation_key, tab_id: context.tab_id });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось поставить на паузу.");
    await refresh(); showStatus("Пауза включена.", "ok");
  }));

  $("resumeAuto").addEventListener("click", () => withButton($("resumeAuto"), async () => {
    await resolveContext();
    if (!context.available) throw new Error("Откройте конкретный диалог ChatGPT.");
    const response = await runtimeSend({ type: "WS_RESUME_AUTORUN", conversation_key: context.conversation_key, tab_id: context.tab_id });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось продолжить.");
    await refresh(); showStatus("Работа продолжена.", "ok");
  }));

  $("finishAuto").addEventListener("click", () => withButton($("finishAuto"), async () => {
    if (!confirm("Завершить текущий автоматический режим Yandex?")) return;
    await resolveContext();
    if (!context.available) throw new Error("Откройте конкретный диалог ChatGPT.");
    const response = await runtimeSend({ type: "WS_FINISH_AUTORUN", conversation_key: context.conversation_key, tab_id: context.tab_id });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось завершить.");
    await refresh(); showStatus("Автоматический режим завершён.", "ok");
  }));

  $("pickSend").addEventListener("click", () => withButton($("pickSend"), async () => {
    await resolveContext();
    if (!context.available) throw new Error("Откройте конкретный диалог ChatGPT.");
    const response = await tabSend(context.tab_id, { type: "WS_START_SEND_BUTTON_PICKER", conversation_key: context.conversation_key });
    if (!response?.ok || response.started !== true) throw new Error(response?.error || response?.code || "Не удалось начать выбор Send.");
    showStatus("Выбор Send запущен. Нажмите нужную кнопку в ChatGPT.", "ok");
  }));

  $("pickCopy").addEventListener("click", () => withButton($("pickCopy"), async () => {
    await resolveContext();
    if (!context.available) throw new Error("Откройте конкретный диалог ChatGPT.");
    const response = await tabSend(context.tab_id, { type: "WS_START_COPY_BUTTON_PICKER", conversation_key: context.conversation_key });
    if (!response?.ok || response.started !== true) throw new Error(response?.error || response?.code || "Не удалось начать выбор Copy.");
    showStatus("Выбор Copy запущен. Нажмите нужную кнопку в ChatGPT.", "ok");
  }));

  $("clearSend").addEventListener("click", () => withButton($("clearSend"), async () => {
    const response = await runtimeSend({ type: "WS_CLEAR_SEND_BUTTON_PROFILE" });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось сбросить Send.");
    await refresh();
    showStatus("Настройка Send сброшена.", "ok");
  }));

  $("clearCopy").addEventListener("click", () => withButton($("clearCopy"), async () => {
    const response = await runtimeSend({ type: "WS_CLEAR_COPY_BUTTON_PROFILES" });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось сбросить Copy.");
    await refresh();
    showStatus("Настройки Copy сброшены.", "ok");
  }));

  $("diagnosticsFilter").addEventListener("change", () => renderDiagnostics());

  $("copyDiagnostics").addEventListener("click", () => withButton($("copyDiagnostics"), async () => {
    const text = $("diagnosticsText").value;
    if (!text) throw new Error("Нет диагностики для копирования.");
    if (!navigator?.clipboard?.writeText) throw new Error("Буфер обмена недоступен.");
    await navigator.clipboard.writeText(text);
    showStatus("Диагностика скопирована.", "ok");
  }));

  $("clearDiagnostics").addEventListener("click", () => withButton($("clearDiagnostics"), async () => {
    const response = await runtimeSend({ type: "WS_CLEAR_DIAGNOSTICS" });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось очистить диагностику.");
    lastDiagnostics = [];
    renderDiagnostics();
    showStatus("Диагностика очищена.", "ok");
  }));

  $("exportSettings").addEventListener("click", () => withButton($("exportSettings"), async () => {
    const response = await runtimeSend({ type: "WS_EXPORT_BACKUP" });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Экспорт не создан.");
    const blob = new Blob([JSON.stringify(response.backup, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `yandex-marketing-bridge-settings-${new Date().toISOString().slice(0, 10)}.json`;
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    showStatus("Экспорт создан. Файл содержит API key — храните его как секрет.", "ok");
  }));

  $("importSettings").addEventListener("click", () => $("importFile").click());
  $("importFile").addEventListener("change", async () => {
    try {
      const file = $("importFile").files?.[0];
      if (!file) return;
      const backup = JSON.parse(await file.text());
      const response = await runtimeSend({ type: "WS_IMPORT_BACKUP", backup });
      if (!response?.ok) throw new Error(response?.error || response?.code || "Импорт не выполнен.");
      await refresh();
      showStatus("Импорт выполнен.", "ok");
    } catch (error) { showStatus(error.message || String(error), "error"); }
    finally { $("importFile").value = ""; }
  });

  if (globalThis.__YMB_POPUP_TEST__ === true) {
    globalThis.__YMB_POPUP_TEST_API__ = Object.freeze({
      resolveContext, renderState, saveAll, persistTogglePatch,
      wordstatPolicyFromForm, searchPolicyFromForm, reportPrefixFromForm, isActiveRun,
      loadDiagnostics, renderDiagnostics, visibleDiagnostics, copyProfileCount
    });
  }

  refresh().then(() => showStatus("Готово.")).catch((error) => showStatus(error.message || String(error), "error"));
})();
