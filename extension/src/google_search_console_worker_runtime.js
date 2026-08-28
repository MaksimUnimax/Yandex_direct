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
  const DEFAULT_AUTO_START_TEXT = "Продолжай текущий read-only сбор Google Search Console по активному плану этого диалога. Команды выводи только как GOOGLE_SEARCH_CONSOLE_API_V1. Не запрашивай интерактивную авторизацию из Autorun. Когда сбор закончен, ответь только: сбор закончен.";

  const originals = Object.freeze({
    protocolForService: globalThis.protocolForService,
    getPolicyForService: globalThis.getPolicyForService,
    policyDecisionForService: globalThis.policyDecisionForService,
    executeServiceCommand: globalThis.executeServiceCommand,
    defaultAutoStartTextForService: globalThis.defaultAutoStartTextForService
  });

  if (typeof originals.protocolForService !== "function"
      || typeof originals.getPolicyForService !== "function"
      || typeof originals.policyDecisionForService !== "function"
      || typeof originals.executeServiceCommand !== "function"
      || typeof originals.defaultAutoStartTextForService !== "function") {
    throw new Error("Google Search Console worker overlay prerequisites are unavailable.");
  }

  let testAdapters = null;

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

  function chromeIdentityAdapter() {
    return Object.freeze({
      async getAccessToken(options = {}) {
        if (options?.interactive === true) {
          const error = new Error("Interactive Google authorization is not allowed from provider execution.");
          error.code = "GSC_INTERACTIVE_AUTH_FORBIDDEN";
          throw error;
        }
        const api = globalThis.chrome?.identity?.getAuthToken;
        if (typeof api !== "function") {
          const error = new Error("Google Search Console authorization is unavailable. Connect Google explicitly first.");
          error.code = "GSC_AUTH_REQUIRED";
          throw error;
        }
        return api.call(globalThis.chrome.identity, { interactive: false });
      }
    });
  }

  function defaultFetchAdapter(url, options) {
    if (typeof globalThis.fetch !== "function") {
      const error = new Error("Fetch adapter is unavailable.");
      error.code = "GSC_FETCH_ADAPTER_REQUIRED";
      throw error;
    }
    return globalThis.fetch(url, options);
  }

  function activeAdapters() {
    if (testAdapters) return testAdapters;
    return Object.freeze({ identity: chromeIdentityAdapter(), fetchImpl: defaultFetchAdapter });
  }

  async function executeGoogleSearchConsoleCommand(command, metadata = {}) {
    const adapters = activeAdapters();
    const runtime = RuntimeFactory.create({
      identity: adapters.identity,
      fetchImpl: adapters.fetchImpl
    });
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

  function configureForTest(adapters) {
    if (globalThis.__YMB_GSC_TEST__ !== true) {
      const error = new Error("GSC test adapters require explicit worker test mode.");
      error.code = "GSC_TEST_MODE_REQUIRED";
      throw error;
    }
    if (adapters == null) {
      testAdapters = null;
      return null;
    }
    if (!adapters.identity || typeof adapters.identity.getAccessToken !== "function"
        || typeof adapters.fetchImpl !== "function") {
      const error = new Error("Invalid GSC test adapters.");
      error.code = "GSC_TEST_ADAPTER_INVALID";
      throw error;
    }
    testAdapters = Object.freeze({ identity: adapters.identity, fetchImpl: adapters.fetchImpl });
    return true;
  }

  globalThis.protocolForService = protocolForServiceV9;
  globalThis.getPolicyForService = getPolicyForServiceV9;
  globalThis.policyDecisionForService = policyDecisionForServiceV9;
  globalThis.executeServiceCommand = executeServiceCommandV9;
  globalThis.defaultAutoStartTextForService = defaultAutoStartTextForServiceV9;

  globalThis.YMBGoogleSearchConsoleWorkerRuntime = Object.freeze({
    SERVICE,
    POLICY_KEY,
    getPolicy,
    savePolicy,
    executeGoogleSearchConsoleCommand,
    configureForTest
  });
})();
