import fs from 'node:fs';

function replaceOnce(source, needle, replacement, label) {
  const first = source.indexOf(needle);
  if (first < 0) throw new Error(`PATCH_MISSING:${label}`);
  if (source.indexOf(needle, first + needle.length) >= 0) throw new Error(`PATCH_AMBIGUOUS:${label}`);
  return source.slice(0, first) + replacement + source.slice(first + needle.length);
}

const htmlPath = 'extension/src/popup.html';
let html = fs.readFileSync(htmlPath, 'utf8');
html = replaceOnce(
  html,
  '<p class="lead">ChatGPT ↔ Yandex Marketing APIs. Wordstat + Search + Webmaster + Metrika + Direct.</p>',
  '<p class="lead">ChatGPT ↔ Marketing APIs. Yandex services + read-only Google Search Console.</p>',
  'html-lead'
);
html = replaceOnce(
  html,
  '          <option value="direct">Direct</option>\n',
  '          <option value="direct">Direct</option>\n          <option value="google_search_console">Google Search Console</option>\n',
  'html-service-option'
);
html = replaceOnce(
  html,
  '<span><strong>Ручной режим Yandex</strong><small id="manualModeMeta">Выключен.</small></span>',
  '<span><strong>Ручной режим Bridge</strong><small id="manualModeMeta">Выключен.</small></span>',
  'html-manual-label'
);
html = replaceOnce(
  html,
  '      <h2>Ключи и доступы Yandex</h2>\n      <p class="warning">Секреты хранятся отдельно по сервисам. Сохранённый API key / OAuth никогда не выводится обратно в текст popup.</p>',
  '      <h2>Ключи и доступы</h2>\n      <p class="warning">Yandex-секреты хранятся отдельно по сервисам. Google Search Console использует Chrome Identity: Google-токены не показываются и не попадают в backup.</p>',
  'html-credentials-heading'
);
const directCardEnd = `      <details id="directCredentials" class="credential-card" data-service="direct">
        <summary><span>Direct</span><strong id="directCredentialState">не настроен</strong></summary>
        <label>OAuth token<input id="directOauthToken" type="password" autocomplete="off" placeholder="Введите новый OAuth или оставьте пустым"></label>
        <label>Client-Login <small>необязательно; нужен для агентского доступа</small><input id="directClientLogin" type="text" autocomplete="off" spellcheck="false" placeholder="Оставьте пустым для обычного аккаунта"></label>
        <div class="actions"><button id="saveDirectCredential" type="button">Save</button><button id="checkDirectCredential" type="button">Check</button></div>
        <p id="directCheckMeta" class="credential-meta">Не проверено.</p>
        <p class="warning">Check делает ровно один read-only Campaigns.get с FieldNames=["Id"] и Limit=1 и расходует Direct Units. Это POST по протоколу Direct; автоматического повтора при неизвестном исходе нет.</p>
      </details>`;
const gscCard = `${directCardEnd}

      <details id="google_search_consoleCredentials" class="credential-card" data-service="google_search_console">
        <summary><span>Google Search Console</span><strong id="googleSearchConsoleCredentialState">OAuth не привязан</strong></summary>
        <p class="muted">Read-only доступ только к Search Console properties, доступным выбранному Google-аккаунту. Авторизация управляется Chrome Identity и не сохраняется в YMB backup.</p>
        <div class="actions"><button id="connectGoogleSearchConsole" type="button">Connect Google</button><button id="checkGoogleSearchConsoleAccess" type="button">Check access</button><button id="disconnectGoogleSearchConsole" type="button">Disconnect</button></div>
        <p id="googleSearchConsoleCheckMeta" class="credential-meta">OAuth client_id ещё не привязан к стабильному ID расширения.</p>
        <p class="warning">Connect — единственное действие, которому разрешён интерактивный Google prompt. Check access делает максимум один read-only listSites без автоповтора.</p>
      </details>`;
html = replaceOnce(html, directCardEnd, gscCard, 'html-gsc-card');
const directPolicy = `    <section>
      <h2>Direct policy</h2>
      <label class="switch-row" for="directManualEnabled"><span><strong>Разрешить Direct в ручном режиме</strong><small>Phase 5 разрешает только read-only методы первого среза.</small></span><input id="directManualEnabled" type="checkbox"></label>
      <div class="grid"><label>Max Direct запросов<input id="directMaxRequestsRun" type="number" min="1" max="20"></label><label>Max page size<input id="directMaxPageSize" type="number" min="1" max="1000"></label><label>Max дней отчёта<input id="directMaxReportDays" type="number" min="1" max="31"></label><label>Max строк отчёта<input id="directMaxReportRows" type="number" min="1" max="1000"></label><label>Стоимость<input id="directCost" type="text" value="0 ₽" readonly></label></div>
      <p class="warning">Autorun Direct в Phase 5 по умолчанию выключен и не включается из production popup. Разрешены только listCampaigns, listAdGroups, listAds, listKeywords и getCampaignPerformance; отчёты — только online.</p>
    </section>`;
const gscPolicy = `${directPolicy}

    <section>
      <h2>Google Search Console policy</h2>
      <label class="switch-row" for="googleSearchConsoleManualEnabled"><span><strong>Разрешить Google Search Console в ручном режиме</strong><small>Только read-only listSites и searchAnalytics.</small></span><input id="googleSearchConsoleManualEnabled" type="checkbox"></label>
      <div class="grid"><label>Max GSC запросов<input id="googleSearchConsoleMaxRequestsRun" type="number" min="1" max="100000"></label><label>Стоимость<input id="googleSearchConsoleCost" type="text" value="0 ₽" readonly></label></div>
      <p class="warning">Autorun Google Search Console выключен и не запускается из production popup. Один Bridge command = максимум один Google provider request; автоматического повтора нет.</p>
    </section>`;
html = replaceOnce(html, directPolicy, gscPolicy, 'html-gsc-policy');
html = html.replace('Webmaster, Metrika и Direct Autorun', 'Webmaster, Metrika, Direct и Google Search Console Autorun');
fs.writeFileSync(htmlPath, html);

const jsPath = 'extension/src/popup.js';
let js = fs.readFileSync(jsPath, 'utf8');
js = replaceOnce(
  js,
  '  const SERVICES = new Set(["wordstat", "search", "webmaster", "metrika", "direct"]);\n  const PRODUCTION_AUTORUN_LOCKED = new Set(["webmaster", "metrika", "direct"]);',
  '  const SERVICES = new Set(["wordstat", "search", "webmaster", "metrika", "direct", "google_search_console"]);\n  const PERSISTENT_CREDENTIAL_SERVICES = new Set(["wordstat", "search", "webmaster", "metrika", "direct"]);\n  const PRODUCTION_AUTORUN_LOCKED = new Set(["webmaster", "metrika", "direct", "google_search_console"]);\n  const GSC_AUTH_PORT = "YMB_GSC_AUTH_V1";',
  'js-service-sets'
);
js = replaceOnce(
  js,
  '    metrika: "METRIKA_API_V1",\n    direct: "DIRECT_API_V1"\n',
  '    metrika: "METRIKA_API_V1",\n    direct: "DIRECT_API_V1",\n    google_search_console: "GOOGLE_SEARCH_CONSOLE_API_V1"\n',
  'js-service-protocol'
);
const runtimeSendEnd = `  function runtimeSend(message) {
    return new Promise((resolve, reject) => {
      try {
        chrome.runtime.sendMessage(message, (response) => {
          const error = chrome.runtime.lastError;
          if (error) reject(new Error(error.message || String(error)));
          else resolve(response);
        });
      } catch (error) { reject(error); }
    });
  }`;
const gscRequest = `${runtimeSendEnd}

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
  }`;
js = replaceOnce(js, runtimeSendEnd, gscRequest, 'js-gsc-port');
const directPolicyFunction = `  function directPolicyFromForm() {
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
  }`;
const gscPolicyFunction = `${directPolicyFunction}

  function googleSearchConsolePolicyFromForm() {
    return {
      autorun_enabled: false,
      manual_enabled: $("googleSearchConsoleManualEnabled").checked,
      allowed_methods: ["listSites", "searchAnalytics"],
      max_requests_per_run: asPositiveInt("googleSearchConsoleMaxRequestsRun", 50),
      max_cost_rub_per_run: 0,
      method_cost_rub: { listSites: 0, searchAnalytics: 0 }
    };
  }`;
js = replaceOnce(js, directPolicyFunction, gscPolicyFunction, 'js-gsc-policy-function');
js = replaceOnce(
  js,
  '    if (service === "direct") return state?.direct_policy || {};\n    return state?.wordstat_policy || {};',
  '    if (service === "direct") return state?.direct_policy || {};\n    if (service === "google_search_console") return state?.google_search_console_policy || {};\n    return state?.wordstat_policy || {};',
  'js-policy-for-service'
);
js = replaceOnce(
  js,
  '    if (state === "MISSING") return "не настроен";\n    if (state === "NOT_CHECKED") return configured ? "сохранён, не проверен" : "не проверен";',
  '    if (state === "UNCONFIGURED") return "OAuth client_id не привязан";\n    if (state === "AUTH_REQUIRED") return "не подключён";\n    if (state === "MISSING") return "не настроен";\n    if (state === "NOT_CHECKED") return configured ? "сохранён, не проверен" : "не проверен";',
  'js-check-state'
);
js = replaceOnce(
  js,
  '    const metrika = credentials.metrika || {};\n    const direct = credentials.direct || {};',
  '    const metrika = credentials.metrika || {};\n    const direct = credentials.direct || {};\n    const googleSearchConsole = state?.google_search_console_auth_status || { configured: false, check_state: "UNCONFIGURED" };',
  'js-gsc-render-status-source'
);
const directRender = `    $("directOauthToken").value = "";
    $("directOauthToken").placeholder = direct.has_oauth_token ? "OAuth сохранён; пусто = не менять" : "Введите OAuth token";
    $("directClientLogin").value = direct.client_login || "";
    $("directCredentialState").textContent = checkStateText(direct, { configured: direct.has_oauth_token });
    $("directCheckMeta").textContent = checkMetaText(direct, "checked_at");`;
const gscRender = `${directRender}

    const gscConfigured = googleSearchConsole.configured === true;
    const gscPresent = googleSearchConsole.check_state === "PRESENT";
    $("googleSearchConsoleCredentialState").textContent = checkStateText(googleSearchConsole, { configured: gscConfigured });
    $("googleSearchConsoleCheckMeta").textContent = gscConfigured
      ? (gscPresent ? "Chrome Identity: подключено. Check access доступен." : "Chrome Identity настроен; нажмите Connect Google.")
      : "OAuth client_id ещё не привязан к стабильному ID расширения.";
    $("connectGoogleSearchConsole").disabled = !gscConfigured || gscPresent;
    $("checkGoogleSearchConsoleAccess").disabled = !gscConfigured || !gscPresent;
    $("disconnectGoogleSearchConsole").disabled = !gscConfigured || !gscPresent;`;
js = replaceOnce(js, directRender, gscRender, 'js-gsc-render-status');
const directPolicyRender = `      const dp = state?.direct_policy || {};
      $("directManualEnabled").checked = dp.manual_enabled !== false;
      $("directMaxRequestsRun").value = String(dp.max_requests_per_run ?? 20);
      $("directMaxPageSize").value = String(dp.max_page_size ?? 1000);
      $("directMaxReportDays").value = String(dp.max_report_days ?? 31);
      $("directMaxReportRows").value = String(dp.max_report_rows ?? 1000);
      $("directCost").value = "0 ₽";`;
const gscPolicyRender = `${directPolicyRender}

      const gp = state?.google_search_console_policy || {};
      $("googleSearchConsoleManualEnabled").checked = gp.manual_enabled !== false;
      $("googleSearchConsoleMaxRequestsRun").value = String(gp.max_requests_per_run ?? 50);
      $("googleSearchConsoleCost").value = "0 ₽";`;
js = replaceOnce(js, directPolicyRender, gscPolicyRender, 'js-gsc-policy-render');
const saveDirectPolicy = `    const direct = await runtimeSend({ type: "YMB_SAVE_DIRECT_POLICY", policy: directPolicyFromForm() });
    if (!direct?.ok) throw new Error(direct?.error || direct?.code || "Не удалось сохранить Direct policy.");`;
const saveGscPolicy = `${saveDirectPolicy}
    const googleSearchConsole = await gscRequest("save_policy", { policy: googleSearchConsolePolicyFromForm() });
    if (!googleSearchConsole?.ok) throw new Error(googleSearchConsole?.error || googleSearchConsole?.code || "Не удалось сохранить Google Search Console policy.");`;
js = replaceOnce(js, saveDirectPolicy, saveGscPolicy, 'js-save-gsc-policy');
js = replaceOnce(
  js,
  '      direct_policy: direct.policy || response.state.direct_policy\n',
  '      direct_policy: direct.policy || response.state.direct_policy,\n      google_search_console_policy: googleSearchConsole.policy || response.state.google_search_console_policy\n',
  'js-render-saved-gsc-policy'
);
js = replaceOnce(js, '  for (const service of SERVICES) {\n    const cap = service[0].toUpperCase() + service.slice(1);', '  for (const service of PERSISTENT_CREDENTIAL_SERVICES) {\n    const cap = service[0].toUpperCase() + service.slice(1);', 'js-persistent-credential-loop');
const persistentLoopEnd = `  }

  $("activeService").addEventListener("change", () => {`;
const gscHandlers = `  }

  $("connectGoogleSearchConsole").addEventListener("click", () => withButton($("connectGoogleSearchConsole"), async () => {
    await gscRequest("connect");
    await refresh();
    showStatus("Google Search Console подключён через Chrome Identity.", "ok");
  }));
  $("checkGoogleSearchConsoleAccess").addEventListener("click", () => withButton($("checkGoogleSearchConsoleAccess"), async () => {
    const result = await gscRequest("check_access");
    await refresh();
    showStatus(`Google Search Console: доступ подтверждён; properties: ${Number(result.site_count || 0)}.`, "ok");
  }));
  $("disconnectGoogleSearchConsole").addEventListener("click", () => withButton($("disconnectGoogleSearchConsole"), async () => {
    await gscRequest("disconnect");
    await refresh();
    showStatus("Google Search Console: cached authorization очищена.", "ok");
  }));

  $("activeService").addEventListener("change", () => {`;
js = replaceOnce(js, persistentLoopEnd, gscHandlers, 'js-gsc-auth-handlers');
js = js.replace('Завершить текущий автоматический режим Yandex?', 'Завершить текущий автоматический режим Bridge?');
js = replaceOnce(
  js,
  '      wordstatPolicyFromForm, searchPolicyFromForm, webmasterPolicyFromForm, metrikaPolicyFromForm, directPolicyFromForm, policyForService,',
  '      wordstatPolicyFromForm, searchPolicyFromForm, webmasterPolicyFromForm, metrikaPolicyFromForm, directPolicyFromForm, googleSearchConsolePolicyFromForm, policyForService, gscRequest,',
  'js-test-api'
);
fs.writeFileSync(jsPath, js);

console.log('PHASE9_GSC_POPUP_PATCH_PASS');
