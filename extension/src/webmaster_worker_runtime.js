/* Phase 3/4 runtime adapter loaded after the accepted Phase-2/lifecycle worker. */
importScripts(
  "shared/credential_store_model.js",
  "shared/webmaster_protocol.js",
  "shared/metrika_protocol.js",
  "shared/credential_runtime.js",
  "shared/phase3_provider_runtime.js",
  "shared/phase4_provider_runtime.js",
  "shared/settings_backup_v3_runtime.js"
);

(() => {
  "use strict";

  const CredentialRuntime = globalThis.YMBCredentialRuntime;
  const Provider = globalThis.YMBPhase4ProviderRuntime;
  const Backup = globalThis.YMBSettingsBackupV3Runtime;
  const Model = globalThis.YMBCredentialStoreModel;
  const Registry = globalThis.YMBServiceRegistry;
  const CredentialRegistry = globalThis.YMBCredentialRegistry;
  const Webmaster = globalThis.WebmasterProtocol;
  const Metrika = globalThis.MetrikaProtocol;
  if (!CredentialRuntime || !Provider || !Backup || !Model || !Registry || !CredentialRegistry || !Webmaster || !Metrika) throw new Error("Phase 4 runtime prerequisites are unavailable.");

  const originals = Object.freeze({
    getSettings: globalThis.getSettings,
    protocolForService: globalThis.protocolForService,
    getPolicyForService: globalThis.getPolicyForService,
    executeServiceCommand: globalThis.executeServiceCommand,
    commonPublicSettingsFields: globalThis.commonPublicSettingsFields,
    defaultAutoStartTextForService: globalThis.defaultAutoStartTextForService
  });
  CredentialRuntime.configure({ baseSettingsGetter: originals.getSettings });

  async function getSettingsV4() { return CredentialRuntime.settings(); }
  function protocolForServiceV4(service) {
    if (service === Registry.SERVICES.WEBMASTER) return Webmaster;
    if (service === Registry.SERVICES.METRIKA) return Metrika;
    return originals.protocolForService(service);
  }
  async function getPolicyForServiceV4(service) {
    if (service === Registry.SERVICES.WEBMASTER) return Provider.getWebmasterPolicy();
    if (service === Registry.SERVICES.METRIKA) return Provider.getMetrikaPolicy();
    return originals.getPolicyForService(service);
  }
  async function executeServiceCommandV4(service, command, metadata = {}) {
    if ([Registry.SERVICES.WORDSTAT, Registry.SERVICES.SEARCH, Registry.SERVICES.WEBMASTER, Registry.SERVICES.METRIKA].includes(service)) return Provider.execute(service, command, metadata);
    return originals.executeServiceCommand(service, command, metadata);
  }
  async function commonPublicSettingsFieldsV4() {
    const base = await originals.commonPublicSettingsFields();
    const settings = await getSettingsV4();
    const webmasterPolicy = await Provider.getWebmasterPolicy();
    const metrikaPolicy = await Provider.getMetrikaPolicy();
    const publicMetrikaPolicy = typeof globalThis.publicPolicy === "function" ? globalThis.publicPolicy(metrikaPolicy, "metrika") : metrikaPolicy;
    return {
      ...base,
      credential_capabilities: {
        ...(base.credential_capabilities || {}),
        wordstat: CredentialRegistry.capabilityForService("wordstat", settings),
        search: CredentialRegistry.capabilityForService("search", settings),
        webmaster: CredentialRegistry.capabilityForService("webmaster", settings),
        metrika: CredentialRegistry.capabilityForService("metrika", settings)
      },
      credential_status: Model.publicCredentialStatus(settings.credentials),
      webmaster_policy: typeof globalThis.publicPolicy === "function" ? globalThis.publicPolicy(webmasterPolicy, "webmaster") : webmasterPolicy,
      metrika_policy: { ...publicMetrikaPolicy, max_report_days: metrikaPolicy.max_report_days },
      settings_schema_version: Model.SETTINGS_SCHEMA_VERSION
    };
  }
  function defaultAutoStartTextForServiceV4(service) {
    if (service === Registry.SERVICES.WEBMASTER) return "Продолжай текущий сбор Yandex Webmaster по активному плану этого диалога. Команды выводи только как WEBMASTER_API_V1. Используй только read-only методы первого среза. Когда сбор закончен, ответь только: сбор закончен.";
    if (service === Registry.SERVICES.METRIKA) return "Продолжай текущий сбор Yandex Metrika по активному плану этого диалога. Команды выводи только как METRIKA_API_V1. Используй только read-only методы первого среза. Когда сбор закончен, ответь только: сбор закончен.";
    return originals.defaultAutoStartTextForService(service);
  }

  globalThis.getSettings = getSettingsV4;
  globalThis.protocolForService = protocolForServiceV4;
  globalThis.getPolicyForService = getPolicyForServiceV4;
  globalThis.executeServiceCommand = executeServiceCommandV4;
  globalThis.commonPublicSettingsFields = commonPublicSettingsFieldsV4;
  globalThis.exportSettingsBackup = Backup.exportBackup;
  globalThis.validateSettingsBackupEnvelope = Backup.validate;
  globalThis.importSettingsBackup = Backup.importBackup;
  globalThis.defaultAutoStartTextForService = defaultAutoStartTextForServiceV4;

  async function saveServiceCredential(service, rawCredential) {
    const value = String(service || "").trim();
    if (!Model.SERVICES.includes(value)) throw Object.assign(new Error("Неизвестный сервис credentials."), { code: "UNKNOWN_SERVICE" });
    const source = rawCredential && typeof rawCredential === "object" && !Array.isArray(rawCredential) ? rawCredential : {};
    const patch = Object.fromEntries(Object.entries(source).filter(([, current]) => current !== undefined));
    if (!Object.keys(patch).length) return { ok: true, service: value, credential: (await CredentialRuntime.status())[value], changed: false };
    if (value === "webmaster") {
      patch.verified_at = null;
      patch.check_state = "NOT_CHECKED";
      if (Object.hasOwn(patch, "oauth_token")) patch.user_id = "";
    } else {
      patch.checked_at = null;
      patch.check_state = "NOT_CHECKED";
    }
    const saved = await CredentialRuntime.save(value, patch);
    return { ok: true, service: value, credential: Model.publicCredentialStatus({ [value]: saved })[value], changed: true };
  }

  async function checkServiceCredential(message) {
    const service = String(message?.service || "").trim();
    if (service === "webmaster") return Provider.checkWebmaster();
    if (service === "metrika") return Provider.checkMetrika();
    if (service === "wordstat" || service === "search") return Provider.checkCloud(service, { confirmBillable: message?.confirm_billable === true });
    throw Object.assign(new Error("Неизвестный сервис credential Check."), { code: "UNKNOWN_SERVICE", request_executed: false, automatic_retry: false });
  }

  async function handleMessage(message) {
    switch (message?.type) {
      case "YMB_GET_CREDENTIALS": return { ok: true, credentials: await CredentialRuntime.status(), settings_schema_version: Model.SETTINGS_SCHEMA_VERSION };
      case "YMB_SAVE_SERVICE_CREDENTIAL": return saveServiceCredential(message.service, message.credential);
      case "YMB_CHECK_SERVICE_CREDENTIAL": return checkServiceCredential(message);
      case "YMB_CHECK_WEBMASTER_CREDENTIAL": return Provider.checkWebmaster(message.oauth_token);
      case "YMB_CHECK_METRIKA_CREDENTIAL": return Provider.checkMetrika(message.oauth_token);
      case "YMB_GET_WEBMASTER_POLICY": return { ok: true, policy: await Provider.getWebmasterPolicy() };
      case "YMB_SAVE_WEBMASTER_POLICY": return { ok: true, policy: await Provider.saveWebmasterPolicy(message.policy || {}) };
      case "YMB_GET_METRIKA_POLICY": return { ok: true, policy: await Provider.getMetrikaPolicy() };
      case "YMB_SAVE_METRIKA_POLICY": return { ok: true, policy: await Provider.saveMetrikaPolicy(message.policy || {}) };
      default: return null;
    }
  }

  chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
    if (!String(message?.type || "").startsWith("YMB_")) return false;
    Promise.resolve(handleMessage(message))
      .then((result) => sendResponse(result || { ok: false, code: "UNKNOWN_MESSAGE", error: "Неизвестная Phase 3/4 команда." }))
      .catch((error) => sendResponse({ ok: false, code: error?.code || "PHASE4_RUNTIME_ERROR", error: error?.message || String(error), request_executed: error?.request_executed ?? false, automatic_retry: false }));
    return true;
  });

  const api = Object.freeze({
    loadCredentials: CredentialRuntime.load,
    saveServiceCredential,
    getWebmasterPolicy: Provider.getWebmasterPolicy,
    saveWebmasterPolicy: Provider.saveWebmasterPolicy,
    getMetrikaPolicy: Provider.getMetrikaPolicy,
    saveMetrikaPolicy: Provider.saveMetrikaPolicy,
    checkServiceCredential,
    checkWebmasterCredential: Provider.checkWebmaster,
    checkMetrikaCredential: Provider.checkMetrika,
    checkCloudCredential: Provider.checkCloud,
    executeWebmasterCommand: Provider.executeWebmaster,
    executeMetrikaCommand: Provider.executeMetrika,
    executeCloudCommand: Provider.executeCloud,
    exportSettingsBackup: Backup.exportBackup,
    validateSettingsBackupEnvelope: Backup.validate,
    importSettingsBackup: Backup.importBackup
  });
  globalThis.YMBPhase3Runtime = api;
  globalThis.YMBPhase4Runtime = api;
})();
