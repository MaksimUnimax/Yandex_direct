(() => {
  "use strict";

  const Model = globalThis.YMBCredentialStoreModel;
  if (!Model) throw new Error("Credential store model is unavailable.");

  const STORAGE_KEY = Model.STORAGE_KEY;
  const SETTINGS_SCHEMA_KEY = "ymb_settings_schema_version";
  const LEGACY_API_KEY = "wsmb_api_key";
  const LEGACY_FOLDER_ID = "wsmb_folder_id";
  let getBaseSettings = async () => ({});
  let mutationTail = Promise.resolve();

  function clone(value) { return value == null ? value : JSON.parse(JSON.stringify(value)); }
  function storageGet(keys) { return chrome.storage.local.get(keys); }
  function storageSet(values) { return chrome.storage.local.set(values); }

  function configure({ baseSettingsGetter } = {}) {
    if (typeof baseSettingsGetter === "function") getBaseSettings = baseSettingsGetter;
  }

  function withExclusiveMutation(task) {
    if (typeof task !== "function") {
      const error = new Error("Credential mutation task must be a function.");
      error.code = "INVALID_CREDENTIAL_MUTATION_TASK";
      return Promise.reject(error);
    }
    const run = mutationTail.then(() => task(), () => task());
    mutationTail = run.then(() => undefined, () => undefined);
    return run;
  }

  async function readSnapshot() {
    const data = await storageGet([STORAGE_KEY, LEGACY_API_KEY, LEGACY_FOLDER_ID, SETTINGS_SCHEMA_KEY]);
    const migrated = Model.migrateStorageRecord(data[STORAGE_KEY], data[LEGACY_API_KEY], data[LEGACY_FOLDER_ID]);
    const needsPersistence = migrated.changed || Number(data[SETTINGS_SCHEMA_KEY] || 0) < Model.SETTINGS_SCHEMA_VERSION;
    return { data, migrated, needsPersistence };
  }

  async function persistLatestMigration() {
    const latest = await readSnapshot();
    if (latest.needsPersistence) {
      await storageSet({
        [STORAGE_KEY]: clone(latest.migrated.credentials),
        [SETTINGS_SCHEMA_KEY]: Model.SETTINGS_SCHEMA_VERSION
      });
    }
    return clone(latest.migrated.credentials);
  }

  async function load({ persistMigration = true } = {}) {
    const snapshot = await readSnapshot();
    if (!persistMigration || !snapshot.needsPersistence) return clone(snapshot.migrated.credentials);
    // A migration write is a mutation. Re-read inside the shared mutation queue so
    // an older startup snapshot can never overwrite a credential saved meanwhile.
    return withExclusiveMutation(persistLatestMigration);
  }

  async function settings() {
    const base = await getBaseSettings();
    return { ...(base || {}), credentials: await load() };
  }

  async function save(service, rawRecord = {}) {
    const value = String(service || "").trim();
    if (!Model.SERVICES.includes(value)) {
      const error = new Error(`Неизвестный сервис: ${service || "unknown"}`);
      error.code = "UNKNOWN_SERVICE";
      throw error;
    }
    const patch = rawRecord && typeof rawRecord === "object" && !Array.isArray(rawRecord) ? clone(rawRecord) : {};
    return withExclusiveMutation(async () => {
      // Read inside the mutation queue. This preserves every independently stored
      // service record when multiple credential saves overlap.
      const latest = await readSnapshot();
      const current = latest.migrated.credentials;
      const merged = { ...current[value], ...patch };
      const next = Model.withServiceCredential(current, value, merged);
      await storageSet({
        [STORAGE_KEY]: clone(next),
        [SETTINGS_SCHEMA_KEY]: Model.SETTINGS_SCHEMA_VERSION
      });
      return clone(next[value]);
    });
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
    withExclusiveMutation,
    STORAGE_KEY,
    SETTINGS_SCHEMA_KEY,
    LEGACY_API_KEY,
    LEGACY_FOLDER_ID
  });
})();
