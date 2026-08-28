(() => {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const TERMINAL_RUNS = new Set(["stopped", "error"]);
  const CHATGPT_HOSTS = new Set(["chatgpt.com", "chat.openai.com"]);
  const SERVICES = new Set(["wordstat", "search", "webmaster", "metrika", "direct", "google_search_console"]);
  const PERSISTENT_CREDENTIAL_SERVICES = new Set(["wordstat", "search", "webmaster", "metrika", "direct"]);
  const PRODUCTION_AUTORUN_LOCKED = new Set(["webmaster", "metrika", "direct", "google_search_console"]);
  const GSC_AUTH_PORT = "YMB_GSC_AUTH_V1";
  const SERVICE_PROTOCOL = Object.freeze({
    wordstat: "WORDSTAT_API_V1",
    search: "SEARCH_API_V1",
    webmaster: "WEBMASTER_API_V1",
    metrika: "METRIKA_API_V1",
    direct: "DIRECT_API_V1",
    google_search_console: "GOOGLE_SEARCH_CONSOLE_API_V1"
  });

  let context = { page_available: false, available: false, tab_id: null, conversation_key: "", identity: null, error: "" };
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

  function gscRequest(action, payload = {}) {
    return new Promise((resolve, reject) => {
      let port;
      let settled = false;
      let timer = null;
      const finish = (fn, value) => {
        if (settled) return;
        settled = true;
        if (timer) clearTimeout(timer);
        fn(value);
      };
      try {
        port = chrome.runtime.connect({ name: GSC_AUTH_PORT });
      } catch (error) {
        reject(error);
        return;
      }
      port.onMessage.addListener((response) => {
        if (!response?.ok) {
          const error = new Error(response?.error || response?.code || "Google Search Console operation failed.");
          error.code = response?.code || "GSC_AUTH_RUNTIME_ERROR";
          error.request_executed = response?.request_executed ?? false;
          finish(reject, error);
          return;
        }
        finish(resolve, response);
      });
      port.onDisconnect.addListener(() => {
        if (settled) return;
        const message = chrome.runtime.lastError?.message || "Google Search Console auth channel closed before completion.";
        finish(reject, new Error(message));
      });
      timer = setTimeout(() => finish(reject, new Error("Google Search Console auth operation timed out.")), 120000);
      port.postMessage({ action, ...payload });
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

  function normalizeService(value) {
    const service = String(value || "").trim();
    return SERVICES.has(service) ? service : "wordstat";
  }
  function asNumber(id, fallback = 0) { const value = Number($(id).value); return Number.isFinite(value) ? value : fallback; }
  function asPositiveInt(id, fallback = 1) { const value = Math.trunc(asNumber(id, fallback)); return value > 0 ? value : fallback; }

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
    const current = lastState?.search_policy || {};
    const currentMethods = Array.isArray(current.allowed_methods) ? current.allowed_methods.map(String) : [];
    const genSearchEnabled = currentMethods.length ? currentMethods.includes("genSearch") : true;
    const currentGenSearchCost = Number(current.method_cost_rub?.genSearch);
    return {
      autorun_enabled: $("searchAutorunEnabled").checked,
      manual_enabled: $("searchManualEnabled").checked,
      // Common Save must not silently disable a method that this popup does not
      // expose as a toggle. Preserve the authoritative GenSearch enablement state;
      // an explicit stored disable remains disabled.
      allowed_methods: genSearchEnabled ? ["search", "genSearch"] : ["search"],
      max_requests_per_run: asPositiveInt("searchMaxRequestsRun", 100),
      max_cost_rub_per_run: Math.max(0, asNumber("searchMaxCostRun", 10)),
      method_cost_rub: {
        search: Math.max(0, asNumber("costSearch", 0.488)),
        genSearch: Number.isFinite(currentGenSearchCost) && currentGenSearchCost >= 0 ? currentGenSearchCost : 5.08
      },
      tariff_checked_at: $("searchTariffCheckedAt").value.trim(),
      tariff_source: $("searchTariffSource").value.trim()
    };
  }

  function webmasterPolicyFromForm() {
    return {
      autorun_enabled: false,
      manual_enabled: $("webmasterManualEnabled").checked,
      allowed_methods: ["listHosts", "getSummary", "getDiagnostics", "getPopularQueries"],
      max_requests_per_run: asPositiveInt("webmasterMaxRequestsRun", 50),
      max_cost_rub_per_run: 0,
      method_cost_rub: { listHosts: 0, getSummary: 0, getDiagnostics: 0, getPopularQueries: 0 }
    };
  }

  function metrikaPolicyFromForm() {
    return {
      autorun_enabled: false,
      manual_enabled: $("metrikaManualEnabled").checked,
      allowed_methods: ["listCounters", "getCounter", "getTrafficSummary", "getTrafficByTime"],
      max_requests_per_run: asPositiveInt("metrikaMaxRequestsRun", 50),
      max_report_days: Math.min(366, asPositiveInt("metrikaMaxReportDays", 366)),
      max_cost_rub_per_run: 0,
      method_cost_rub: { listCounters: 0, getCounter: 0, getTrafficSummary: 0, getTrafficByTime: 0 }
    };
  }

  function directPolicyFromForm() {
    return {
      autorun_enabled: false,
      manual_enabled: $("directManualEnabled").checked,
      allowed_methods: ["listCampaigns", "listAdGroups", "listAds", "listKeywords", "getCampaignPerformance"],
      max_requests_per_run: Math.min(20, asPositiveInt("directMaxRequestsRun", 20)),
      max_page_size: Math.min(1000, asPositiveInt("directMaxPageSize", 1000)),
      max_report_days: Math.min(31, asPositiveInt("directMaxReportDays", 31)),
      max_report_rows: Math.min(1000, asPositiveInt("directMaxReportRows", 1000)),
      max_cost_rub_per_run: 0,
      method_cost_rub: { listCampaigns: 0, listAdGroups: 0, listAds: 0, listKeywords: 0, getCampaignPerformance: 0 }
    };
  }

  function googleSearchConsolePolicyFromForm() {
    return {
      autorun_enabled: false,
      manual_enabled: $("googleSearchConsoleManualEnabled").checked,
      allowed_methods: ["listSites", "searchAnalytics"],
      max_requests_per_run: asPositiveInt("googleSearchConsoleMaxRequestsRun", 50),
      max_cost_rub_per_run: 0,
      method_cost_rub: { listSites: 0, searchAnalytics: 0 }
    };
  }

  function policyForService(service, state = lastState) {
    if (service === "search") return state?.search_policy || {};
    if (service === "webmaster") return state?.webmaster_policy || {};
    if (service === "metrika") return state?.metrika_policy || {};
    if (service === "direct") return state?.direct_policy || {};
    if (service === "google_search_console") return state?.google_search_console_policy || {};
    return state?.wordstat_policy || {};
  }

  function reportPrefixFromForm() { return { enabled: $("reportPrefixEnabled").checked, text: $("reportPrefixText").value, interval: 1 }; }

  async function resolveContext() {
    context = { page_available: false, available: false, tab_id: null, conversation_key: "", identity: null, error: "" };
    const tab = await queryActiveTab();
    if (!tab || !Number.isInteger(Number(tab.id))) return context;
    let host = "";
    try { host = new URL(tab.url || "").hostname; } catch { return context; }
    if (!CHATGPT_HOSTS.has(host)) return context;
    context = { ...context, page_available: true, tab_id: Number(tab.id) };
    try {
      const page = await tabSend(Number(tab.id), { type: "WS_GET_IDENTITY" });
      const key = String(page?.conversation_key || page?.identity?.conversation_key || "").trim();
      if (!page?.ok || !key) {
        context = { ...context, error: "Не удалось подтвердить текущий ChatGPT-диалог." };
        return context;
      }
      context = { page_available: true, available: true, tab_id: Number(tab.id), conversation_key: key, identity: page.identity || null, error: "" };
    } catch (error) {
      context = { ...context, error: `Нет связи с текущей страницей ChatGPT: ${error?.message || error}` };
    }
    return context;
  }

  function isActiveRun(run) { return Boolean(run && !TERMINAL_RUNS.has(String(run.status || ""))); }
  function copyProfileCount(value) {
    if (Array.isArray(value)) return value.filter(Boolean).length;
    if (!value || typeof value !== "object") return 0;
    if (Array.isArray(value.profiles)) return value.profiles.filter(Boolean).length;
    return Object.values(value).reduce((total, item) => total + (Array.isArray(item) ? item.filter(Boolean).length : (item && typeof item === "object" ? 1 : 0)), 0);
  }

  function checkStateText(status, { configured = false } = {}) {
    const state = String(status?.check_state || "").trim();
    if (state === "PRESENT") return "проверено";
    if (state === "INVALID_OR_EXPIRED") return "неверный / истёк";
    if (state === "NO_ACCESS") return "нет доступа";
    if (state === "NETWORK_ERROR") return "ошибка сети";
    if (state === "QUOTA") return "квота / временно недоступно";
    if (state === "APP_ACCESS_NOT_APPROVED") return "приложение не допущено к Direct API";
    if (state === "DIRECT_ACCOUNT_MISSING") return "аккаунт Direct не найден";
    if (state === "NO_API_ACCESS") return "нет доступа к Direct API";
    if (state === "UNITS_EXHAUSTED") return "Units исчерпаны";
    if (state === "CONCURRENCY_LIMIT") return "лимит параллельных запросов";
    if (state === "UNCONFIGURED") return "OAuth client_id не привязан";
    if (state === "AUTH_REQUIRED") return "не подключён";
    if (state === "MISSING") return "не настроен";
    if (state === "NOT_CHECKED") return configured ? "сохранён, не проверен" : "не проверен";
    return configured ? "сохранён" : "не настроен";
  }
  function checkMetaText(status, timestampKey) {
    const state = checkStateText(status, { configured: true });
    const stamp = String(status?.[timestampKey] || "").trim();
    return stamp ? `${state}; ${stamp}` : state;
  }

  function renderCredentialState(state, activeService) {
    const credentials = state?.credential_status || {};
    const wordstat = credentials.wordstat || {};
    const search = credentials.search || {};
    const webmaster = credentials.webmaster || {};
    const metrika = credentials.metrika || {};
    const direct = credentials.direct || {};
    const googleSearchConsole = state?.google_search_console_auth_status || { configured: false, check_state: "UNCONFIGURED" };

    $("wordstatApiKey").value = "";
    $("wordstatApiKey").placeholder = wordstat.has_api_key ? "Ключ сохранён; пусто = не менять" : "Введите API key";
    $("wordstatFolderId").value = wordstat.folder_id || "";
    $("wordstatCredentialState").textContent = checkStateText(wordstat, { configured: wordstat.has_api_key && wordstat.has_folder_id });
    $("wordstatCheckMeta").textContent = checkMetaText(wordstat, "checked_at");

    $("searchApiKey").value = "";
    $("searchApiKey").placeholder = search.has_api_key ? "Ключ сохранён; пусто = не менять" : "Введите API key";
    $("searchFolderId").value = search.folder_id || "";
    $("searchCredentialState").textContent = checkStateText(search, { configured: search.has_api_key && search.has_folder_id });
    $("searchCheckMeta").textContent = checkMetaText(search, "checked_at");

    $("webmasterOauthToken").value = "";
    $("webmasterOauthToken").placeholder = webmaster.has_oauth_token ? "OAuth сохранён; пусто = не менять" : "Введите OAuth token";
    $("webmasterUserId").textContent = webmaster.user_id || "—";
    $("webmasterCredentialState").textContent = checkStateText(webmaster, { configured: webmaster.has_oauth_token });
    $("webmasterCheckMeta").textContent = checkMetaText(webmaster, "verified_at");

    $("metrikaOauthToken").value = "";
    $("metrikaOauthToken").placeholder = metrika.has_oauth_token ? "OAuth сохранён; пусто = не менять" : "Введите OAuth token";
    $("metrikaCredentialState").textContent = checkStateText(metrika, { configured: metrika.has_oauth_token });
    $("metrikaCheckMeta").textContent = checkMetaText(metrika, "checked_at");

    $("directOauthToken").value = "";
    $("directOauthToken").placeholder = direct.has_oauth_token ? "OAuth сохранён; пусто = не менять" : "Введите OAuth token";
    $("directClientLogin").value = direct.client_login || "";
    $("directCredentialState").textContent = checkStateText(direct, { configured: direct.has_oauth_token });
    $("directCheckMeta").textContent = checkMetaText(direct, "checked_at");

    const gscConfigured = googleSearchConsole.configured === true;
    const gscPresent = googleSearchConsole.check_state === "PRESENT";
    $("googleSearchConsoleCredentialState").textContent = checkStateText(googleSearchConsole, { configured: gscConfigured });
    $("googleSearchConsoleCheckMeta").textContent = gscConfigured
      ? (gscPresent ? "Chrome Identity: подключено. Check access доступен." : "Chrome Identity настроен; нажмите Connect Google.")
      : "OAuth client_id ещё не привязан к стабильному ID расширения.";
    $("connectGoogleSearchConsole").disabled = !gscConfigured || gscPresent;
    $("checkGoogleSearchConsoleAccess").disabled = !gscConfigured || !gscPresent;
    $("disconnectGoogleSearchConsole").disabled = !gscConfigured || !gscPresent;

    for (const service of SERVICES) {
      const card = $(`${service}Credentials`);
      if (card) card.open = service === activeService;
    }
  }

  function renderState(state) {
    rendering = true;
    try {
      lastState = state || {};
      $("versionBadge").textContent = `v${state?.product_version || "0.1.1"}`;
      $("conversationMeta").textContent = context.available ? context.conversation_key : "не определён";
      const service = normalizeService(state?.service_context?.active_service);
      $("activeService").value = service;
      $("activeService").disabled = !context.available || isActiveRun(state?.auto_run) || state?.manual_mode === true;
      $("bindConversation").disabled = !context.page_available;
      $("bindConversation").textContent = state?.binding ? "Перепривязать диалог" : "Привязать диалог";

      renderCredentialState(state, service);

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
      else if (activeRun) $("manualModeMeta").textContent = `Выключен: автоматический режим выполняет только ${SERVICE_PROTOCOL[normalizeService(run?.active_service)]}.`;
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

      const wmp = state?.webmaster_policy || {};
      $("webmasterManualEnabled").checked = wmp.manual_enabled !== false;
      $("webmasterMaxRequestsRun").value = String(wmp.max_requests_per_run ?? 50);
      $("webmasterCost").value = "0 ₽";

      const mp = state?.metrika_policy || {};
      $("metrikaManualEnabled").checked = mp.manual_enabled !== false;
      $("metrikaMaxRequestsRun").value = String(mp.max_requests_per_run ?? 50);
      $("metrikaMaxReportDays").value = String(mp.max_report_days ?? 366);
      $("metrikaCost").value = "0 ₽";

      const dp = state?.direct_policy || {};
      $("directManualEnabled").checked = dp.manual_enabled !== false;
      $("directMaxRequestsRun").value = String(dp.max_requests_per_run ?? 20);
      $("directMaxPageSize").value = String(dp.max_page_size ?? 1000);
      $("directMaxReportDays").value = String(dp.max_report_days ?? 31);
      $("directMaxReportRows").value = String(dp.max_report_rows ?? 1000);
      $("directCost").value = "0 ₽";

      const gp = state?.google_search_console_policy || {};
      $("googleSearchConsoleManualEnabled").checked = gp.manual_enabled !== false;
      $("googleSearchConsoleMaxRequestsRun").value = String(gp.max_requests_per_run ?? 50);
      $("googleSearchConsoleCost").value = "0 ₽";

      const activePolicy = policyForService(service, state);
      if (state?.manual_mode !== true && activePolicy?.manual_enabled !== true) {
        $("manualMode").disabled = true;
        $("manualModeMeta").textContent = `Ручной режим ${service} запрещён политикой.`;
      }

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

      const productionAutorunLocked = PRODUCTION_AUTORUN_LOCKED.has(service);
      $("startAuto").disabled = productionAutorunLocked || !context.available || !state?.binding || activeRun || state?.manual_mode === true || manualBusy || activePolicy?.autorun_enabled !== true;
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
    const node = $("diagnosticsText"); if (!node) return;
    const visible = visibleDiagnostics(); node.value = visible.length ? JSON.stringify(visible, null, 2) : "";
  }
  async function loadDiagnostics() {
    const response = await runtimeSend({ type: "WS_GET_DIAGNOSTICS" });
    if (response?.ok === false) throw new Error(response?.error || response?.code || "Не удалось прочитать диагностику.");
    lastDiagnostics = Array.isArray(response?.diagnostics) ? response.diagnostics : []; renderDiagnostics(); return lastDiagnostics;
  }

  async function refresh() {
    await resolveContext();
    const response = context.available
      ? await runtimeSend({ type: "WS_GET_STATE", conversation_key: context.conversation_key })
      : await runtimeSend({ type: "WS_GET_GLOBAL_STATE", page_context_error: "CHATGPT_CONTEXT_UNAVAILABLE" });
    if (!response?.ok || !response.state) throw new Error(response?.error || response?.code || "Не удалось прочитать состояние расширения.");
    renderState(response.state); await loadDiagnostics(); return response.state;
  }

  async function saveAll() {
    const message = {
      type: "WS_SAVE_SETTINGS",
      auto_send: $("autoSend").checked,
      debug_mode: $("debugMode").checked,
      wordstat_policy: wordstatPolicyFromForm(),
      search_policy: searchPolicyFromForm()
    };
    if (context.available) {
      message.conversation_key = context.conversation_key;
      message.tab_id = context.tab_id;
      message.active_service = normalizeService($("activeService").value);
      message.report_prefix = reportPrefixFromForm();
    }
    const response = await runtimeSend(message);
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось сохранить настройки.");
    const webmaster = await runtimeSend({ type: "YMB_SAVE_WEBMASTER_POLICY", policy: webmasterPolicyFromForm() });
    if (!webmaster?.ok) throw new Error(webmaster?.error || webmaster?.code || "Не удалось сохранить Webmaster policy.");
    const metrika = await runtimeSend({ type: "YMB_SAVE_METRIKA_POLICY", policy: metrikaPolicyFromForm() });
    if (!metrika?.ok) throw new Error(metrika?.error || metrika?.code || "Не удалось сохранить Metrika policy.");
    const direct = await runtimeSend({ type: "YMB_SAVE_DIRECT_POLICY", policy: directPolicyFromForm() });
    if (!direct?.ok) throw new Error(direct?.error || direct?.code || "Не удалось сохранить Direct policy.");
    const googleSearchConsole = await gscRequest("save_policy", { policy: googleSearchConsolePolicyFromForm() });
    if (!googleSearchConsole?.ok) throw new Error(googleSearchConsole?.error || googleSearchConsole?.code || "Не удалось сохранить Google Search Console policy.");
    if (response.state) renderState({
      ...response.state,
      webmaster_policy: webmaster.policy || response.state.webmaster_policy,
      metrika_policy: metrika.policy || response.state.metrika_policy,
      direct_policy: direct.policy || response.state.direct_policy,
      google_search_console_policy: googleSearchConsole.policy || response.state.google_search_console_policy
    });
    return response.state || null;
  }

  async function persistTogglePatch(patch) {
    const response = await runtimeSend({ type: "WS_PATCH_TOGGLES", ...(context.available ? { conversation_key: context.conversation_key, tab_id: context.tab_id } : {}), ...patch });
    if (!response?.ok || !response.state) throw new Error(response?.error || response?.code || "Не удалось сохранить переключатель.");
    renderState(response.state); return response.state;
  }

  async function saveCredential(service) {
    const value = normalizeService(service); const credential = {};
    if (value === "wordstat") {
      credential.folder_id = $("wordstatFolderId").value.trim(); const secret = $("wordstatApiKey").value.trim(); if (secret) credential.api_key = secret;
    } else if (value === "search") {
      credential.folder_id = $("searchFolderId").value.trim(); const secret = $("searchApiKey").value.trim(); if (secret) credential.api_key = secret;
    } else if (value === "webmaster") {
      const secret = $("webmasterOauthToken").value.trim(); if (secret) credential.oauth_token = secret;
    } else if (value === "metrika") {
      const secret = $("metrikaOauthToken").value.trim(); if (secret) credential.oauth_token = secret;
    } else if (value === "direct") {
      const secret = $("directOauthToken").value.trim(); if (secret) credential.oauth_token = secret;
      credential.client_login = $("directClientLogin").value.trim();
    }
    const response = await runtimeSend({ type: "YMB_SAVE_SERVICE_CREDENTIAL", service: value, credential });
    if (!response?.ok) throw new Error(response?.error || response?.code || `Не удалось сохранить ${value} credentials.`);
    await refresh(); return response;
  }

  async function checkCredential(service) {
    const value = normalizeService(service); const message = { type: "YMB_CHECK_SERVICE_CREDENTIAL", service: value };
    if (value === "search") {
      if (!confirm("Search Check выполнит ровно один платный Search-запрос. Продолжить? Автоматического повтора не будет.")) return { ok: false, cancelled: true, request_executed: false };
      message.confirm_billable = true;
    }
    const response = await runtimeSend(message); await refresh();
    if (!response?.ok) throw new Error(response?.error || response?.code || `Проверка ${value} не пройдена.`);
    return response;
  }

  async function withButton(button, fn) {
    const wasDisabled = button.disabled; button.disabled = true;
    try { await fn(); } catch (error) { showStatus(error.message || String(error), "error"); } finally { button.disabled = wasDisabled; }
  }

  function onSaveSettingsClick(event) {
    const button = event.currentTarget;
    void withButton(button, async () => {
      await resolveContext(); await saveAll(); await refresh(); showStatus("Общие настройки сохранены.", "ok");
    });
  }

  $("saveSettingsTop").addEventListener("click", onSaveSettingsClick);
  $("saveSettings").addEventListener("click", onSaveSettingsClick);

  for (const service of PERSISTENT_CREDENTIAL_SERVICES) {
    const cap = service[0].toUpperCase() + service.slice(1);
    $("save" + cap + "Credential").addEventListener("click", () => withButton($("save" + cap + "Credential"), async () => {
      const result = await saveCredential(service); showStatus(result.changed === false ? `${service}: изменений нет.` : `${service}: credentials сохранены.`, "ok");
    }));
    $("check" + cap + "Credential").addEventListener("click", () => withButton($("check" + cap + "Credential"), async () => {
      const result = await checkCredential(service); if (result?.cancelled) return showStatus("Search Check отменён; запрос не выполнялся."); showStatus(`${service}: Check пройден.`, "ok");
    }));
  }

  $("connectGoogleSearchConsole").addEventListener("click", () => withButton($("connectGoogleSearchConsole"), async () => {
    await gscRequest("connect");
    await refresh();
    showStatus("Google Search Console подключён через Chrome Identity.", "ok");
  }));
  $("checkGoogleSearchConsoleAccess").addEventListener("click", () => withButton($("checkGoogleSearchConsoleAccess"), async () => {
    const result = await gscRequest("check_access");
    await refresh();
    showStatus("Google Search Console: доступ подтверждён; properties: " + Number(result.site_count || 0) + ".", "ok");
  }));
  $("disconnectGoogleSearchConsole").addEventListener("click", () => withButton($("disconnectGoogleSearchConsole"), async () => {
    await gscRequest("disconnect");
    await refresh();
    showStatus("Google Search Console: cached authorization очищена.", "ok");
  }));

  $("activeService").addEventListener("change", () => {
    if (rendering) return;
    const service = normalizeService($("activeService").value); const policy = policyForService(service);
    for (const current of SERVICES) { const card = $(`${current}Credentials`); if (card) card.open = current === service; }
    $("startAuto").disabled = PRODUCTION_AUTORUN_LOCKED.has(service) || !context.available || !lastState?.binding || isActiveRun(lastState?.auto_run) || lastState?.manual_mode === true || policy?.autorun_enabled !== true;
    showStatus(`Выбран ${service}. Нажмите «Сохранить общие настройки», чтобы закрепить выбор.`);
  });

  $("bindConversation").addEventListener("click", () => withButton($("bindConversation"), async () => {
    await resolveContext();
    if (!context.page_available || !Number.isInteger(Number(context.tab_id))) throw new Error("Откройте конкретный диалог ChatGPT.");
    const response = await runtimeSend({ type: "WS_BIND_CONVERSATION", tab_id: context.tab_id });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось привязать диалог.");
    await refresh(); showStatus("Диалог привязан.", "ok");
  }));

  $("manualMode").addEventListener("change", async () => {
    if (rendering) return;
    const enabled = $("manualMode").checked; const previous = !enabled; let workerCommitted = false;
    try {
      await resolveContext(); if (!context.available) throw new Error("Откройте конкретный диалог ChatGPT.");
      const committedService = normalizeService(lastState?.service_context?.active_service);
      if (enabled && normalizeService($("activeService").value) !== committedService) throw new Error("Сначала сохраните выбранный активный сервис.");
      if (enabled) {
        const applied = await tabSend(context.tab_id, { type: "WS_APPLY_MANUAL_MODE", conversation_key: context.conversation_key, enabled: true, active_service: committedService });
        if (!applied?.ok || applied.applied !== true) throw new Error(applied?.error || applied?.code || "Страница не подтвердила ручной режим.");
        try {
          const committed = await runtimeSend({ type: "WS_SET_MANUAL_MODE", conversation_key: context.conversation_key, enabled: true, tab_id: context.tab_id });
          if (!committed?.ok) throw new Error(committed?.error || committed?.code || "Worker не сохранил ручной режим."); workerCommitted = true;
        } catch (error) {
          try { await tabSend(context.tab_id, { type: "WS_APPLY_MANUAL_MODE", conversation_key: context.conversation_key, enabled: false, active_service: committedService }); } catch {}
          throw error;
        }
      } else {
        const committed = await runtimeSend({ type: "WS_SET_MANUAL_MODE", conversation_key: context.conversation_key, enabled: false, tab_id: context.tab_id });
        if (!committed?.ok) throw new Error(committed?.error || committed?.code || "Worker не выключил ручной режим."); workerCommitted = true;
        const applied = await tabSend(context.tab_id, { type: "WS_APPLY_MANUAL_MODE", conversation_key: context.conversation_key, enabled: false, active_service: committedService });
        if (!applied?.ok || applied.applied !== true) throw new Error(applied?.error || applied?.code || "Worker выключен, но страница не подтвердила очистку ручного режима.");
      }
      await refresh(); showStatus(enabled ? "Ручной режим включён." : "Ручной режим выключен.", "ok");
    } catch (error) {
      if (enabled) $("manualMode").checked = false; else $("manualMode").checked = workerCommitted ? false : previous;
      showStatus(error.message || String(error), "error");
    }
  });

  for (const [id, key] of [["autoSend", "auto_send"], ["debugMode", "debug_mode"], ["wordstatAutorunEnabled", "wordstat_autorun_enabled"], ["searchAutorunEnabled", "search_autorun_enabled"]]) {
    $(id).addEventListener("change", async () => {
      if (rendering) return; const enabled = $(id).checked;
      try { await persistTogglePatch({ [key]: enabled }); showStatus("Изменение сохранено сразу.", "ok"); }
      catch (error) { $(id).checked = !enabled; showStatus(error.message || String(error), "error"); }
    });
  }

  $("reportPrefixEnabled").addEventListener("change", async () => {
    if (rendering) return; const enabled = $("reportPrefixEnabled").checked;
    try {
      if (!context.available) throw new Error("Префикс привязан к конкретному диалогу ChatGPT.");
      await persistTogglePatch({ report_prefix_enabled: enabled }); showStatus("Переключатель префикса сохранён сразу.", "ok");
    } catch (error) { $("reportPrefixEnabled").checked = !enabled; showStatus(error.message || String(error), "error"); }
  });

  $("saveAutoStartPrompt").addEventListener("click", () => withButton($("saveAutoStartPrompt"), async () => {
    if (!context.available) throw new Error("Откройте конкретный диалог ChatGPT.");
    const service = normalizeService($("activeService").value);
    if (PRODUCTION_AUTORUN_LOCKED.has(service)) throw new Error(`${service}: Autorun в production popup первой версии запрещён.`);
    const response = await runtimeSend({ type: "WS_SAVE_AUTO_START_PROMPT", conversation_key: context.conversation_key, active_service: service, text: $("autoStartPromptText").value, tab_id: context.tab_id });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось сохранить стартовый текст.");
    await refresh(); showStatus("Стартовый текст сохранён.", "ok");
  }));

  $("resetAutoStartPrompt").addEventListener("click", () => withButton($("resetAutoStartPrompt"), async () => {
    if (!context.available) throw new Error("Откройте конкретный диалог ChatGPT.");
    const service = normalizeService($("activeService").value);
    if (PRODUCTION_AUTORUN_LOCKED.has(service)) throw new Error(`${service}: Autorun в production popup первой версии запрещён.`);
    const response = await runtimeSend({ type: "WS_RESET_AUTO_START_PROMPT", conversation_key: context.conversation_key, active_service: service, tab_id: context.tab_id });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось вернуть стандартный текст.");
    await refresh(); showStatus("Стандартный стартовый текст восстановлен.", "ok");
  }));

  $("startAuto").addEventListener("click", () => withButton($("startAuto"), async () => {
    await resolveContext(); if (!context.available) throw new Error("Откройте конкретный диалог ChatGPT.");
    const service = normalizeService($("activeService").value);
    if (PRODUCTION_AUTORUN_LOCKED.has(service)) throw new Error(`${service}: Autorun в production popup первой версии запрещён.`);
    await saveAll();
    const policy = service === "search" ? searchPolicyFromForm() : wordstatPolicyFromForm();
    if (!confirm(`Запустить ${service}? Максимум ${policy.max_requests_per_run} запросов / ${policy.max_cost_rub_per_run} ₽. Автоматический повтор запроса при неизвестном исходе запрещён.`)) return;
    const response = await runtimeSend({ type: "WS_START_AUTORUN", conversation_key: context.conversation_key, tab_id: context.tab_id });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось запустить автоматический режим.");
    await refresh(); showStatus(`Автоматический режим ${service} запущен.`, "ok");
  }));

  $("pauseAuto").addEventListener("click", () => withButton($("pauseAuto"), async () => {
    await resolveContext(); if (!context.available) throw new Error("Откройте конкретный диалог ChatGPT.");
    const response = await runtimeSend({ type: "WS_PAUSE_AUTORUN", conversation_key: context.conversation_key, tab_id: context.tab_id });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось поставить на паузу.");
    await refresh(); showStatus("Пауза включена.", "ok");
  }));
  $("resumeAuto").addEventListener("click", () => withButton($("resumeAuto"), async () => {
    await resolveContext(); if (!context.available) throw new Error("Откройте конкретный диалог ChatGPT.");
    const response = await runtimeSend({ type: "WS_RESUME_AUTORUN", conversation_key: context.conversation_key, tab_id: context.tab_id });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось продолжить.");
    await refresh(); showStatus("Работа продолжена.", "ok");
  }));
  $("finishAuto").addEventListener("click", () => withButton($("finishAuto"), async () => {
    if (!confirm("Завершить текущий автоматический режим Bridge?")) return;
    await resolveContext(); if (!context.available) throw new Error("Откройте конкретный диалог ChatGPT.");
    const response = await runtimeSend({ type: "WS_FINISH_AUTORUN", conversation_key: context.conversation_key, tab_id: context.tab_id });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось завершить.");
    await refresh(); showStatus("Автоматический режим завершён.", "ok");
  }));

  $("pickSend").addEventListener("click", () => withButton($("pickSend"), async () => {
    await resolveContext(); if (!context.available) throw new Error("Откройте конкретный диалог ChatGPT.");
    const response = await tabSend(context.tab_id, { type: "WS_START_SEND_BUTTON_PICKER", conversation_key: context.conversation_key });
    if (!response?.ok || response.started !== true) throw new Error(response?.error || response?.code || "Не удалось начать выбор Send.");
    showStatus("Выбор Send запущен. Нажмите нужную кнопку в ChatGPT.", "ok");
  }));
  $("pickCopy").addEventListener("click", () => withButton($("pickCopy"), async () => {
    await resolveContext(); if (!context.available) throw new Error("Откройте конкретный диалог ChatGPT.");
    const response = await tabSend(context.tab_id, { type: "WS_START_COPY_BUTTON_PICKER", conversation_key: context.conversation_key });
    if (!response?.ok || response.started !== true) throw new Error(response?.error || response?.code || "Не удалось начать выбор Copy.");
    showStatus("Выбор Copy запущен. Нажмите нужную кнопку в ChatGPT.", "ok");
  }));
  $("clearSend").addEventListener("click", () => withButton($("clearSend"), async () => {
    const response = await runtimeSend({ type: "WS_CLEAR_SEND_BUTTON_PROFILE" });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось сбросить Send.");
    await refresh(); showStatus("Настройка Send сброшена.", "ok");
  }));
  $("clearCopy").addEventListener("click", () => withButton($("clearCopy"), async () => {
    const response = await runtimeSend({ type: "WS_CLEAR_COPY_BUTTON_PROFILES" });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось сбросить Copy.");
    await refresh(); showStatus("Настройки Copy сброшены.", "ok");
  }));

  $("diagnosticsFilter").addEventListener("change", () => renderDiagnostics());
  $("copyDiagnostics").addEventListener("click", () => withButton($("copyDiagnostics"), async () => {
    const text = $("diagnosticsText").value;
    if (!text) throw new Error("Нет диагностики для копирования.");
    if (!navigator?.clipboard?.writeText) throw new Error("Буфер обмена недоступен.");
    await navigator.clipboard.writeText(text); showStatus("Диагностика скопирована.", "ok");
  }));
  $("clearDiagnostics").addEventListener("click", () => withButton($("clearDiagnostics"), async () => {
    const response = await runtimeSend({ type: "WS_CLEAR_DIAGNOSTICS" });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Не удалось очистить диагностику.");
    lastDiagnostics = []; renderDiagnostics(); showStatus("Диагностика очищена.", "ok");
  }));

  $("exportSettings").addEventListener("click", () => withButton($("exportSettings"), async () => {
    const response = await runtimeSend({ type: "WS_EXPORT_BACKUP" });
    if (!response?.ok) throw new Error(response?.error || response?.code || "Экспорт не создан.");
    const blob = new Blob([JSON.stringify(response.backup, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob); const link = document.createElement("a");
    link.href = url; link.download = `yandex-marketing-bridge-settings-${new Date().toISOString().slice(0, 10)}.json`; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    showStatus("Экспорт создан. Файл содержит секреты настроенных сервисов — храните его как секрет.", "ok");
  }));

  $("importSettings").addEventListener("click", () => $("importFile").click());
  $("importFile").addEventListener("change", async () => {
    try {
      const file = $("importFile").files?.[0]; if (!file) return;
      const backup = JSON.parse(await file.text()); const response = await runtimeSend({ type: "WS_IMPORT_BACKUP", backup });
      if (!response?.ok) throw new Error(response?.error || response?.code || "Импорт не выполнен.");
      await refresh(); showStatus("Импорт выполнен.", "ok");
    } catch (error) { showStatus(error.message || String(error), "error"); }
    finally { $("importFile").value = ""; }
  });

  if (globalThis.__YMB_POPUP_TEST__ === true) {
    globalThis.__YMB_POPUP_TEST_API__ = Object.freeze({
      resolveContext, renderState, saveAll, persistTogglePatch, saveCredential, checkCredential,
      wordstatPolicyFromForm, searchPolicyFromForm, webmasterPolicyFromForm, metrikaPolicyFromForm, directPolicyFromForm, googleSearchConsolePolicyFromForm, policyForService, gscRequest,
      reportPrefixFromForm, isActiveRun, normalizeService, renderCredentialState, onSaveSettingsClick,
      loadDiagnostics, renderDiagnostics, visibleDiagnostics, copyProfileCount
    });
  }

  refresh().then(() => {
    const bootstrapError = String(globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_ERROR__ || "").trim();
    if (bootstrapError) return showStatus(bootstrapError, "error");
    if (context.available) return showStatus("Готово.");
    if (context.page_available) return showStatus(context.error || "Не удалось подтвердить текущий ChatGPT-диалог.", "error");
    return showStatus("Откройте конкретный диалог ChatGPT.", "error");
  }).catch((error) => showStatus(error.message || String(error), "error"));
})();
