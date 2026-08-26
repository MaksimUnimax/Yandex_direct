(() => {
  "use strict";

  const Model = globalThis.YMBCredentialStoreModel;
  if (!Model) throw new Error("Credential store model is unavailable.");

  const STORAGE_KEY = Model.STORAGE_KEY;
  const SETTINGS_SCHEMA_KEY = "ymb_settings_schema_version";
  const LEGACY_API_KEY = "wsmb_api_key";
  const LEGACY_FOLDER_ID = "wsmb_folder_id";
  let getBaseSettings = async () => ({});

  function clone(value) { return value == null ? value : JSON.parse(JSON.stringify(value)); }
  function storageGet(keys) { return chrome.storage.local.get(keys); }
  function storageSet(values) { return chrome.storage.local.set(values); }

  function configure({ baseSettingsGetter } = {}) {
    if (typeof baseSettingsGetter === "function") getBaseSettings = baseSettingsGetter;
  }

  async function load({ persistMigration = true } = {}) {
    const data = await storageGet([STORAGE_KEY, LEGACY_API_KEY, LEGACY_FOLDER_ID, SETTINGS_SCHEMA_KEY]);
    const migrated = Model.migrateStorageRecord(data[STORAGE_KEY], data[LEGACY_API_KEY], data[LEGACY_FOLDER_ID]);
    if (persistMigration && (migrated.changed || Number(data[SETTINGS_SCHEMA_KEY] || 0) < Model.SETTINGS_SCHEMA_VERSION)) {
      await storageSet({
        [STORAGE_KEY]: clone(migrated.credentials),
        [SETTINGS_SCHEMA_KEY]: Model.SETTINGS_SCHEMA_VERSION
      });
    }
    return clone(migrated.credentials);
  }

  async function settings() {
    const base = await getBaseSettings();
    return { ...(base || {}), credentials: await load() };
  }

  async function save(service, rawRecord) {
    const current = await load();
    const next = Model.withServiceCredential(current, service, rawRecord);
    await storageSet({
      [STORAGE_KEY]: clone(next),
      [SETTINGS_SCHEMA_KEY]: Model.SETTINGS_SCHEMA_VERSION
    });
    return clone(next[String(service)]);
  }

  async function status() {
    return Model.publicCredentialStatus(await load());
  }

  globalThis.YMBCredentialRuntime = Object.freeze({
    configure,
    load,
    settings,
    save,
    status,
    STORAGE_KEY,
    SETTINGS_SCHEMA_KEY,
    LEGACY_API_KEY,
    LEGACY_FOLDER_ID
  });
})();
