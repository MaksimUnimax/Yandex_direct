(() => {
  "use strict";

  const Protocol = globalThis.GoogleSearchConsoleProtocol;
  const RuntimeFactory = globalThis.YMBGoogleSearchConsoleRuntime;
  const Registry = globalThis.YMBServiceRegistry;
  const Policy = globalThis.YMBPolicyModel;
  if (!Protocol || !RuntimeFactory || !Registry || !Policy) {
    throw new Error("Google Search Console worker prerequisites are unavailable.");
  }

  const SERVICE = Registry.SERVICES.GOOGLE_SEARCH_CONSOLE || "google_search_console";
  const POLICY_KEY = "ymb_google_search_console_policy";
  const READONLY_SCOPE = "https://www.googleapis.com/auth/webmasters.readonly";
  const PORT_NAME = "YMB_GSC_AUTH_V1";
  const DEFAULT_AUTO_START_TEXT = "Продолжай текущий read-only сбор Google Search Console по активному плану этого диалога. Команды выводи только как GOOGLE_SEARCH_CONSOLE_API_V1. Не запрашивай интерактивную авторизацию из Autorun. Когда сбор закончен, ответь только: сбор закончен.";

  const originals = Object.freeze({
    protocolForService: globalThis.protocolForService,
    getPolicyForService: globalThis.getPolicyForService,
    policyDecisionForService: globalThis.policyDecisionForService,
    executeServiceCommand: globalThis.executeServiceCommand,
    defaultAutoStartTextForService: globalThis.defaultAutoStartTextForService,
    commonPublicSettingsFields: globalThis.commonPublicSettingsFields
  });

  if (typeof originals.protocolForService !== "function"
      || typeof originals.getPolicyForService !== "function"
      || typeof originals.policyDecisionForService !== "function"
      || typeof originals.executeServiceCommand !== "function"
      || typeof originals.defaultAutoStartTextForService !== "function") {
    throw new Error("Google Search Console worker overlay prerequisites are unavailable.");
  }

  let testAdapters = null;

  function fail(code, message, requestExecuted = false) {
    const error = new Error(message || code);
    error.code = code;
    error.request_executed = requestExecuted;
    error.automatic_retry = false;
    return error;
  }

  function tokenValue(value) {
    if (typeof value === "string") return value.trim();
    if (value && typeof value === "object" && typeof value.token === "string") return value.token.trim();
    return "";
  }

  function manifestAuthConfiguration() {
    const runtime = globalThis.chrome?.runtime;
    const manifest = typeof runtime?.getManifest === "function" ? runtime.getManifest() : {};
    const permissions = Array.isArray(manifest?.permissions) ? manifest.permissions.map(String) : [];
    const oauth2 = manifest?.oauth2 && typeof manifest.oauth2 === "object" ? manifest.oauth2 : {};
    const clientId = String(oauth2.client_id || "").trim();
    const scopes = Array.isArray(oauth2.scopes) ? oauth2.scopes.map((item) => String(item).trim()).filter(Boolean) : [];
    const hasIdentityPermission = permissions.includes("identity");
    const hasClientId = /\.apps\.googleusercontent\.com$/i.test(clientId);
    const hasReadonlyScope = scopes.includes(READONLY_SCOPE);
    return Object.freeze({
      configured: hasIdentityPermission && hasClientId && hasReadonlyScope,
      has_identity_permission: hasIdentityPermission,
      has_client_id: hasClientId,
      has_readonly_scope: hasReadonlyScope,
      extension_id: String(runtime?.id || "")
    });
  }

  function assertAuthConfiguration() {
    const config = manifestAuthConfiguration();
    if (!config.configured) {
      throw fail(
        "GSC_AUTH_CONFIG_REQUIRED",
        "Google Search Console OAuth client_id is not bound to this stable extension build yet.",
        false
      );
    }
    return config;
  }

  async function getPolicy() {
    const data = await chrome.storage.local.get(POLICY_KEY);
    return Policy.normalizeGoogleSearchConsolePolicy(data?.[POLICY_KEY] || {});
  }

  async function savePolicy(raw = {}) {
    const normalized = Policy.normalizeGoogleSearchConsolePolicy(raw || {});
    await chrome.storage.local.set({ [POLICY_KEY]: normalized });
    return normalized;
  }

  function protocolForServiceV9(service) {
    if (service === SERVICE) return Protocol;
    return originals.protocolForService(service);
  }

  async function getPolicyForServiceV9(service) {
    if (service === SERVICE) return getPolicy();
    return originals.getPolicyForService(service);
  }

  function policyDecisionForServiceV9(service, args = {}) {
    if (service === SERVICE) {
      return Policy.decisionForService(SERVICE, {
        ...args,
        credentialState: "PRESENT"
      });
    }
    return originals.policyDecisionForService(service, args);
  }

  async function chromeGetAccessToken(interactive) {
    const api = globalThis.chrome?.identity?.getAuthToken;
    if (typeof api !== "function") {
      throw fail(
        "GSC_AUTH_REQUIRED",
        "Google Search Console authorization is unavailable. Connect Google explicitly first.",
        false
      );
    }
    let raw;
    try {
      raw = await api.call(globalThis.chrome.identity, { interactive: interactive === true });
    } catch (cause) {
      const error = fail(
        "GSC_AUTH_REQUIRED",
        interactive === true
          ? "Google Search Console authorization was not completed."
          : "Google Search Console authorization is required before this command can run.",
        false
      );
      error.cause = cause;
      throw error;
    }
    const token = tokenValue(raw);
    if (!token) throw fail("GSC_AUTH_REQUIRED", "Google Search Console authorization is required.", false);
    return token;
  }

  function chromeIdentityAdapter() {
    return Object.freeze({
      async getAccessToken(options = {}) {
        if (options?.interactive === true) {
          throw fail(
            "GSC_INTERACTIVE_AUTH_FORBIDDEN",
            "Interactive Google authorization is not allowed from provider execution.",
            false
          );
        }
        return chromeGetAccessToken(false);
      }
    });
  }

  function defaultFetchAdapter(url, options) {
    if (typeof globalThis.fetch !== "function") {
      throw fail("GSC_FETCH_ADAPTER_REQUIRED", "Fetch adapter is unavailable.", false);
    }
    return globalThis.fetch(url, options);
  }

  function activeAdapters() {
    if (testAdapters) return testAdapters;
    return Object.freeze({ identity: chromeIdentityAdapter(), fetchImpl: defaultFetchAdapter });
  }

  function providerRuntime() {
    const adapters = activeAdapters();
    return RuntimeFactory.create({ identity: adapters.identity, fetchImpl: adapters.fetchImpl });
  }

  async function executeGoogleSearchConsoleCommand(command, metadata = {}) {
    const runtime = providerRuntime();
    const policy = await getPolicy();
    const channel = String(metadata?.channel || metadata?.policy?.channel || "manual");
    return runtime.execute(command, {
      ...metadata,
      channel,
      policy,
      run: metadata?.run || { requests_executed: 0, estimated_cost_rub: 0 }
    });
  }

  async function executeServiceCommandV9(service, command, metadata = {}) {
    if (service === SERVICE) return executeGoogleSearchConsoleCommand(command, metadata);
    return originals.executeServiceCommand(service, command, metadata);
  }

  function defaultAutoStartTextForServiceV9(service) {
    if (service === SERVICE) return DEFAULT_AUTO_START_TEXT;
    return originals.defaultAutoStartTextForService(service);
  }

  async function authStatus() {
    const config = manifestAuthConfiguration();
    if (!config.configured) {
      return Object.freeze({
        ok: true,
        service: SERVICE,
        configured: false,
        check_state: "UNCONFIGURED",
        extension_id: config.extension_id,
        request_executed: false,
        automatic_retry: false
      });
    }
    try {
      await chromeGetAccessToken(false);
      return Object.freeze({
        ok: true,
        service: SERVICE,
        configured: true,
        check_state: "PRESENT",
        extension_id: config.extension_id,
        request_executed: false,
        automatic_retry: false
      });
    } catch (error) {
      if (error?.code !== "GSC_AUTH_REQUIRED") throw error;
      return Object.freeze({
        ok: true,
        service: SERVICE,
        configured: true,
        check_state: "AUTH_REQUIRED",
        extension_id: config.extension_id,
        request_executed: false,
        automatic_retry: false
      });
    }
  }

  async function connect() {
    const config = assertAuthConfiguration();
    await chromeGetAccessToken(true);
    return Object.freeze({
      ok: true,
      service: SERVICE,
      configured: true,
      check_state: "PRESENT",
      extension_id: config.extension_id,
      request_executed: false,
      automatic_retry: false
    });
  }

  async function checkAccess() {
    const config = assertAuthConfiguration();
    const runtime = providerRuntime();
    const policy = Policy.normalizeGoogleSearchConsolePolicy({
      manual_enabled: true,
      autorun_enabled: false,
      allowed_methods: ["listSites"],
      max_requests_per_run: 1
    });
    const result = await runtime.execute(
      { method: "listSites" },
      { channel: "manual", policy, run: { requests_executed: 0, estimated_cost_rub: 0 } }
    );
    if (result?.ok === true) {
      const sites = Array.isArray(result?.report_envelope?.result?.sites) ? result.report_envelope.result.sites : [];
      return Object.freeze({
        ok: true,
        service: SERVICE,
        configured: true,
        check_state: "PRESENT",
        extension_id: config.extension_id,
        site_count: sites.length,
        request_executed: true,
        automatic_retry: false
      });
    }
    const httpStatus = Number(result?.http_status || 0);
    const checkState = httpStatus === 401 ? "INVALID_OR_EXPIRED"
      : httpStatus === 403 ? "NO_ACCESS"
      : httpStatus === 429 ? "QUOTA"
      : "NETWORK_ERROR";
    return Object.freeze({
      ok: false,
      service: SERVICE,
      configured: true,
      check_state: checkState,
      extension_id: config.extension_id,
      http_status: httpStatus,
      request_executed: result?.report_envelope?.request_executed !== false,
      automatic_retry: false
    });
  }

  async function disconnect() {
    const config = assertAuthConfiguration();
    let token = "";
    try {
      token = await chromeGetAccessToken(false);
    } catch (error) {
      if (error?.code !== "GSC_AUTH_REQUIRED") throw error;
    }
    if (token) {
      const remove = globalThis.chrome?.identity?.removeCachedAuthToken;
      if (typeof remove !== "function") {
        throw fail("GSC_IDENTITY_CACHE_API_REQUIRED", "Chrome Identity token cache API is unavailable.", false);
      }
      await remove.call(globalThis.chrome.identity, { token });
    }
    return Object.freeze({
      ok: true,
      service: SERVICE,
      configured: true,
      check_state: "AUTH_REQUIRED",
      extension_id: config.extension_id,
      request_executed: false,
      automatic_retry: false
    });
  }

  async function commonPublicSettingsFieldsV9() {
    const base = typeof originals.commonPublicSettingsFields === "function"
      ? await originals.commonPublicSettingsFields()
      : {};
    return {
      ...base,
      google_search_console_policy: await getPolicy(),
      google_search_console_auth_status: await authStatus()
    };
  }

  async function handleAuthAction(message = {}) {
    const action = String(message?.action || "").trim();
    if (action === "status") return authStatus();
    if (action === "connect") return connect();
    if (action === "check_access") return checkAccess();
    if (action === "disconnect") return disconnect();
    if (action === "save_policy") return { ok: true, service: SERVICE, policy: await savePolicy(message.policy || {}) };
    throw fail("GSC_AUTH_ACTION_UNKNOWN", "Unknown Google Search Console auth action.", false);
  }

  function installAuthPort() {
    const event = globalThis.chrome?.runtime?.onConnect;
    if (!event || typeof event.addListener !== "function") return false;
    event.addListener((port) => {
      if (String(port?.name || "") !== PORT_NAME) return;
      let handled = false;
      port.onMessage?.addListener?.((message) => {
        if (handled) return;
        handled = true;
        Promise.resolve(handleAuthAction(message))
          .then((result) => {
            try { port.postMessage(result); } catch {}
            try { port.disconnect(); } catch {}
          })
          .catch((error) => {
            const response = {
              ok: false,
              service: SERVICE,
              code: error?.code || "GSC_AUTH_RUNTIME_ERROR",
              error: error?.message || String(error),
              request_executed: error?.request_executed ?? false,
              automatic_retry: false
            };
            try { port.postMessage(response); } catch {}
            try { port.disconnect(); } catch {}
          });
      });
    });
    return true;
  }

  function configureForTest(adapters) {
    if (globalThis.__YMB_GSC_TEST__ !== true) {
      throw fail("GSC_TEST_MODE_REQUIRED", "GSC test adapters require explicit worker test mode.", false);
    }
    if (adapters == null) {
      testAdapters = null;
      return null;
    }
    if (!adapters.identity || typeof adapters.identity.getAccessToken !== "function"
        || typeof adapters.fetchImpl !== "function") {
      throw fail("GSC_TEST_ADAPTER_INVALID", "Invalid GSC test adapters.", false);
    }
    testAdapters = Object.freeze({ identity: adapters.identity, fetchImpl: adapters.fetchImpl });
    return true;
  }

  globalThis.protocolForService = protocolForServiceV9;
  globalThis.getPolicyForService = getPolicyForServiceV9;
  globalThis.policyDecisionForService = policyDecisionForServiceV9;
  globalThis.executeServiceCommand = executeServiceCommandV9;
  globalThis.defaultAutoStartTextForService = defaultAutoStartTextForServiceV9;
  if (typeof originals.commonPublicSettingsFields === "function") {
    globalThis.commonPublicSettingsFields = commonPublicSettingsFieldsV9;
  }

  installAuthPort();

  globalThis.YMBGoogleSearchConsoleWorkerRuntime = Object.freeze({
    SERVICE,
    POLICY_KEY,
    READONLY_SCOPE,
    PORT_NAME,
    manifestAuthConfiguration,
    getPolicy,
    savePolicy,
    authStatus,
    connect,
    checkAccess,
    disconnect,
    handleAuthAction,
    executeGoogleSearchConsoleCommand,
    configureForTest
  });
})();
