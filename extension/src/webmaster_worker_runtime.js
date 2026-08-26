/* Phase 3 runtime adapter loaded after the accepted Phase-2/lifecycle worker. */
importScripts(
  "shared/credential_store_model.js",
  "shared/webmaster_protocol.js",
  "shared/credential_runtime.js",
  "shared/phase3_provider_runtime.js",
  "shared/settings_backup_v3_runtime.js"
);

(() => {
  "use strict";

  const CredentialRuntime = globalThis.YMBCredentialRuntime;
  const Provider = globalThis.YMBPhase3ProviderRuntime;
  const Backup = globalThis.YMBSettingsBackupV3Runtime;
  const Model = globalThis.YMBCredentialStoreModel;
  const Registry = globalThis.YMBServiceRegistry;
  const CredentialRegistry = globalThis.YMBCredentialRegistry;
  const Webmaster = globalThis.WebmasterProtocol;
  if (!CredentialRuntime || !Provider || !Backup || !Model || !Registry || !CredentialRegistry || !Webmaster) throw new Error("Phase 3 runtime prerequisites are unavailable.");

  const originals = Object.freeze({
    getSettings: globalThis.getSettings,
    protocolForService: globalThis.protocolForService,
    getPolicyForService: globalThis.getPolicyForService,
    executeServiceCommand: globalThis.executeServiceCommand,
    commonPublicSettingsFields: globalThis.commonPublicSettingsFields,
    defaultAutoStartTextForService: globalThis.defaultAutoStartTextForService
  });
  CredentialRuntime.configure({ baseSettingsGetter: originals.getSettings });

  async function getSettingsV3() { return CredentialRuntime.settings(); }
  function protocolForServiceV3(service) {
    if (service === Registry.SERVICES.WEBMASTER) return Webmaster;
    return originals.protocolForService(service);
  }
  async function getPolicyForServiceV3(service) {
    if (service === Registry.SERVICES.WEBMASTER) return Provider.getWebmasterPolicy();
    return originals.getPolicyForService(service);
  }
  async function executeServiceCommandV3(service, command, metadata = {}) {
    if ([Registry.SERVICES.WORDSTAT, Registry.SERVICES.SEARCH, Registry.SERVICES.WEBMASTER].includes(service)) return Provider.execute(service, command, metadata);
    return originals.executeServiceCommand(service, command, metadata);
  }
  async function commonPublicSettingsFieldsV3() {
    const base = await originals.commonPublicSettingsFields();
    const settings = await getSettingsV3();
    const webmasterPolicy = await Provider.getWebmasterPolicy();
    return {
      ...base,
      credential_capabilities: {
        ...(base.credential_capabilities || {}),
        wordstat: CredentialRegistry.capabilityForService("wordstat", settings),
        search: CredentialRegistry.capabilityForService("search", settings),
        webmaster: CredentialRegistry.capabilityForService("webmaster", settings)
      },
      credential_status: Model.publicCredentialStatus(settings.credentials),
      webmaster_policy: typeof globalThis.publicPolicy === "function" ? globalThis.publicPolicy(webmasterPolicy, "webmaster") : webmasterPolicy,
      settings_schema_version: Model.SETTINGS_SCHEMA_VERSION
    };
  }
  function defaultAutoStartTextForServiceV3(service) {
    if (service === Registry.SERVICES.WEBMASTER) return "Продолжай текущий сбор Yandex Webmaster по активному плану этого диалога. Команды выводи только как WEBMASTER_API_V1. Используй только read-only методы первого среза. Когда сбор закончен, ответь только: сбор закончен.";
    return originals.defaultAutoStartTextForService(service);
  }

  globalThis.getSettings = getSettingsV3;
  globalThis.protocolForService = protocolForServiceV3;
  globalThis.getPolicyForService = getPolicyForServiceV3;
  globalThis.executeServiceCommand = executeServiceCommandV3;
  globalThis.commonPublicSettingsFields = commonPublicSettingsFieldsV3;
  globalThis.exportSettingsBackup = Backup.exportBackup;
  globalThis.validateSettingsBackupEnvelope = Backup.validate;
  globalThis.importSettingsBackup = Backup.importBackup;
  globalThis.defaultAutoStartTextForService = defaultAutoStartTextForServiceV3;

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
    if (service === "wordstat" || service === "search") return Provider.checkCloud(service, { confirmBillable: message?.confirm_billable === true });
    throw Object.assign(new Error("Неизвестный сервис credential Check."), { code: "UNKNOWN_SERVICE", request_executed: false, automatic_retry: false });
  }

  async function handleMessage(message) {
    switch (message?.type) {
      case "YMB_GET_CREDENTIALS": return { ok: true, credentials: await CredentialRuntime.status(), settings_schema_version: Model.SETTINGS_SCHEMA_VERSION };
      case "YMB_SAVE_SERVICE_CREDENTIAL": return saveServiceCredential(message.service, message.credential);
      case "YMB_CHECK_SERVICE_CREDENTIAL": return checkServiceCredential(message);
      case "YMB_CHECK_WEBMASTER_CREDENTIAL": return Provider.checkWebmaster(message.oauth_token);
      case "YMB_GET_WEBMASTER_POLICY": return { ok: true, policy: await Provider.getWebmasterPolicy() };
      case "YMB_SAVE_WEBMASTER_POLICY": return { ok: true, policy: await Provider.saveWebmasterPolicy(message.policy || {}) };
      default: return null;
    }
  }

  chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
    if (!String(message?.type || "").startsWith("YMB_")) return false;
    Promise.resolve(handleMessage(message))
      .then((result) => sendResponse(result || { ok: false, code: "UNKNOWN_MESSAGE", error: "Неизвестная Phase 3 команда." }))
      .catch((error) => sendResponse({ ok: false, code: error?.code || "PHASE3_RUNTIME_ERROR", error: error?.message || String(error), request_executed: error?.request_executed ?? false, automatic_retry: false }));
    return true;
  });

  globalThis.YMBPhase3Runtime = Object.freeze({
    loadCredentials: CredentialRuntime.load,
    saveServiceCredential,
    getWebmasterPolicy: Provider.getWebmasterPolicy,
    saveWebmasterPolicy: Provider.saveWebmasterPolicy,
    checkServiceCredential,
    checkWebmasterCredential: Provider.checkWebmaster,
    checkCloudCredential: Provider.checkCloud,
    executeWebmasterCommand: Provider.executeWebmaster,
    executeCloudCommand: Provider.executeCloud,
    exportSettingsBackup: Backup.exportBackup,
    validateSettingsBackupEnvelope: Backup.validate,
    importSettingsBackup: Backup.importBackup
  });
})();
