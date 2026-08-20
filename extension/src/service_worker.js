/* global BB2ConversationIdentity, BB2ManualControls, WordstatProtocol, SearchProtocol, YMBSearchXml, WordstatAutorunModel, YMBProduct, YMBServiceRegistry, YMBBlockCommandDiscovery, YMBRunContextModel, YMBCredentialRegistry, YMBPolicyModel, YMBCostLedgerModel */
importScripts(
  "shared/product.js",
  "shared/conversation_identity.js",
  "shared/manual_controls.js",
  "shared/service_registry.js",
  "shared/block_command_discovery.js",
  "shared/run_context_model.js",
  "shared/credential_registry.js",
  "shared/policy_model.js",
  "shared/cost_ledger_model.js",
  "shared/wordstat_protocol.js",
  "shared/search_xml.js",
  "shared/search_protocol.js",
  "shared/autorun_model.js"
);

"use strict";

const VERSION = YMBProduct.VERSION;
const SETTINGS_SCHEMA_VERSION = 2;
const KEYS = Object.freeze({
  API_KEY: "wsmb_api_key", FOLDER_ID: "wsmb_folder_id", AUTO_SEND: "wsmb_auto_send",
  CONVERSATION_BINDINGS: "wsmb_conversation_bindings", MANUAL_MODES: "wsmb_manual_modes",
  MANUAL_OPERATIONS: "wsmb_manual_operations", REPORT_PREFIXES: "wsmb_report_prefixes",
  AUTO_START_PROMPTS: "wsmb_auto_start_prompts", AUTO_RUNS: "wsmb_auto_runs", OUTBOX: "wsmb_outbox",
  SERVICE_CONTEXTS: "ymb_service_contexts", WORDSTAT_POLICY: "ymb_wordstat_policy", SEARCH_POLICY: "ymb_search_policy",
  DEBUG_MODE: "ymb_debug_mode", SETTINGS_SCHEMA: "ymb_settings_schema_version", LAST_STATUS: "wsmb_last_status",
  DIAGNOSTICS: "ymb_diagnostics"
});
const DEFAULT_FOLDER_ID = String(WordstatProtocol.DEFAULT_FOLDER_ID || "");
const DEFAULT_AUTO_START_TEXT = "Продолжай текущий сбор Wordstat по активному плану этого диалога. Команды выводи только как WORDSTAT_API_V1. Когда сбор закончен, ответь только: сбор закончен.";
const SEARCH_DEFAULT_AUTO_START_TEXT = "Продолжай текущий сбор Yandex Search по активному плану этого диалога. Команды выводи только как SEARCH_API_V1. Один блок = один Search API request. Не повторяй запрос автоматически при неизвестном исходе. Когда сбор закончен, ответь только: сбор закончен.";
const TERMINAL_MANUAL_STATUSES = new Set(["completed", "error", "cancelled"]);

function nowIso() { return new Date().toISOString(); }
function uid(prefix = "ymb") { return `${prefix}-${crypto.randomUUID()}`; }
function clone(v) { return v == null ? v : JSON.parse(JSON.stringify(v)); }
function normalizeConversationKey(value) { return BB2ConversationIdentity.normalizeConversationKey(value, { required: true }); }
function defaultAutoStartTextForService(service) { return String(service || "") === YMBServiceRegistry.SERVICES.SEARCH ? SEARCH_DEFAULT_AUTO_START_TEXT : DEFAULT_AUTO_START_TEXT; }
function storageGet(keys) { return chrome.storage.local.get(keys); }
function storageSet(values) { return chrome.storage.local.set(values); }
function storageRemove(keys) { return chrome.storage.local.remove(keys); }

async function diagnostic(code, detail = {}, { level = "info" } = {}) {
  const data = await storageGet(KEYS.DEBUG_MODE);
  if (data[KEYS.DEBUG_MODE] !== true) return;
  const current = (await storageGet(KEYS.DIAGNOSTICS))[KEYS.DIAGNOSTICS] || [];
  const safe = JSON.parse(JSON.stringify(detail, (key, value) => /api.?key|authorization|token|secret/i.test(key) ? "[REDACTED]" : value));
  current.push({ ts: nowIso(), level, code, detail: safe });
  await storageSet({ [KEYS.DIAGNOSTICS]: current.slice(-200) });
}
async function setStatus(status) { await storageSet({ [KEYS.LAST_STATUS]: { ...status, updated_at: nowIso() } }); }
function normalizeApiKey(value, { required = false } = {}) {
  const text = String(value || "").trim();
  if (required && !text) throw Object.assign(new Error("API key не сохранён в расширении."), { code: "API_KEY_MISSING" });
  return text;
}
function normalizeFolderId(value, { required = false } = {}) {
  const text = String(value || "").trim();
  if (required && !text) throw Object.assign(new Error("Folder ID не сохранён в расширении."), { code: "FOLDER_ID_MISSING" });
  return text;
}

async function getSettings() {
  const d = await storageGet([KEYS.API_KEY, KEYS.FOLDER_ID, KEYS.AUTO_SEND, KEYS.DEBUG_MODE]);
  return { apiKey: String(d[KEYS.API_KEY] || ""), folderId: String(d[KEYS.FOLDER_ID] || DEFAULT_FOLDER_ID), autoSend: d[KEYS.AUTO_SEND] !== false, debugMode: d[KEYS.DEBUG_MODE] === true };
}
async function getWordstatPolicy() { return YMBPolicyModel.normalizeWordstatPolicy((await storageGet(KEYS.WORDSTAT_POLICY))[KEYS.WORDSTAT_POLICY] || {}); }
async function saveWordstatPolicy(raw) { const v = YMBPolicyModel.normalizeWordstatPolicy(raw || {}); await storageSet({ [KEYS.WORDSTAT_POLICY]: v }); return v; }
async function getSearchPolicy() { return YMBPolicyModel.normalizeSearchPolicy((await storageGet(KEYS.SEARCH_POLICY))[KEYS.SEARCH_POLICY] || {}); }
async function saveSearchPolicy(raw) { const v = YMBPolicyModel.normalizeSearchPolicy(raw || {}); await storageSet({ [KEYS.SEARCH_POLICY]: v }); return v; }
async function getPolicyForService(service) {
  if (service === YMBServiceRegistry.SERVICES.SEARCH) return getSearchPolicy();
  if (service === YMBServiceRegistry.SERVICES.WORDSTAT) return getWordstatPolicy();
  throw Object.assign(new Error("Сервис не поддерживается."), { code: "SERVICE_NOT_AVAILABLE" });
}
function publicPolicy(policy, service = YMBServiceRegistry.SERVICES.WORDSTAT) {
  const n = YMBPolicyModel.normalizePolicyForService(service, policy || {});
  return { autorun_enabled: n.autorun_enabled, manual_enabled: n.manual_enabled, allowed_methods: [...n.allowed_methods], max_requests_per_run: n.max_requests_per_run, max_cost_rub_per_run: n.max_cost_rub_per_run, method_cost_rub: { ...n.method_cost_rub }, tariff_checked_at: n.tariff_checked_at, tariff_source: n.tariff_source };
}
function publicCapability(settings, service = YMBServiceRegistry.SERVICES.WORDSTAT) { return YMBCredentialRegistry.capabilityForService(service, settings || {}); }
function protocolForService(service) {
  if (service === YMBServiceRegistry.SERVICES.SEARCH) return SearchProtocol;
  if (service === YMBServiceRegistry.SERVICES.WORDSTAT) return WordstatProtocol;
  return null;
}
function assertProtocolForService(service) { const p = protocolForService(service); if (!p) throw Object.assign(new Error("Сервис не поддерживается."), { code: "SERVICE_NOT_AVAILABLE" }); return p; }
function policyDecisionForService(service, args = {}) { return YMBPolicyModel.decisionForService(service, args); }
function serviceExecutionAdmission(service, { settings = {}, policy = {}, channel = "autorun", command = {}, run = {} } = {}) {
  const protocol = assertProtocolForService(service);
  const normalizedCommand = protocol.normalizeCommand(command);
  const capability = publicCapability(settings, service);
  const decision = policyDecisionForService(service, { policy, channel, method: normalizedCommand.method, credentialState: capability.state, run });
  const reservedTotals = decision.allow ? YMBCostLedgerModel.noteExecuted(run || {}, decision.estimated_cost_rub) : YMBCostLedgerModel.normalizeTotals(run || {});
  return Object.freeze({ service, command: normalizedCommand, capability, allow: decision.allow, reason: decision.reason, estimated_cost_rub: decision.estimated_cost_rub, policy: decision.policy, reserved_totals: reservedTotals });
}

async function getBinding(conversationKey) { const key = normalizeConversationKey(conversationKey); return ((await storageGet(KEYS.CONVERSATION_BINDINGS))[KEYS.CONVERSATION_BINDINGS] || {})[key] || null; }
async function saveBinding(identity) {
  const key = normalizeConversationKey(identity.conversation_key);
  const data = await storageGet(KEYS.CONVERSATION_BINDINGS); const map = { ...(data[KEYS.CONVERSATION_BINDINGS] || {}) }; const old = map[key];
  map[key] = { binding_id: old?.binding_id || uid("binding"), revision: Number(old?.revision || 0) + 1, origin: identity.origin, conversation_id: identity.conversation_id, conversation_key: key, bound_at: old?.bound_at || nowIso(), updated_at: nowIso() };
  await storageSet({ [KEYS.CONVERSATION_BINDINGS]: map }); return map[key];
}
async function getManualMode(conversationKey) { const key = normalizeConversationKey(conversationKey); const data = await storageGet(KEYS.MANUAL_MODES); return data[KEYS.MANUAL_MODES]?.[key] === true; }
async function setManualMode(conversationKey, enabled) { const key = normalizeConversationKey(conversationKey); const data = await storageGet(KEYS.MANUAL_MODES); const map = { ...(data[KEYS.MANUAL_MODES] || {}) }; map[key] = enabled === true; await storageSet({ [KEYS.MANUAL_MODES]: map }); return map[key]; }
async function getServiceContext(conversationKey) {
  const key = normalizeConversationKey(conversationKey); const map = (await storageGet(KEYS.SERVICE_CONTEXTS))[KEYS.SERVICE_CONTEXTS] || {};
  const raw = map[key] || {}; let service = String(raw.active_service || YMBServiceRegistry.SERVICES.WORDSTAT);
  if (!YMBServiceRegistry.isKnownService(service)) service = YMBServiceRegistry.SERVICES.WORDSTAT;
  return { active_service: service, updated_at: raw.updated_at || null };
}
async function saveServiceContext(conversationKey, raw) {
  const key = normalizeConversationKey(conversationKey); const service = YMBRunContextModel.normalizeActiveService(raw?.active_service, YMBServiceRegistry, { required: true });
  const map = { ...((await storageGet(KEYS.SERVICE_CONTEXTS))[KEYS.SERVICE_CONTEXTS] || {}) }; map[key] = { active_service: service, updated_at: nowIso() }; await storageSet({ [KEYS.SERVICE_CONTEXTS]: map }); return map[key];
}
async function getAutoRun(conversationKey) { const key = normalizeConversationKey(conversationKey); return ((await storageGet(KEYS.AUTO_RUNS))[KEYS.AUTO_RUNS] || {})[key] || null; }
async function saveAutoRun(conversationKey, run) { const key = normalizeConversationKey(conversationKey); const map = { ...((await storageGet(KEYS.AUTO_RUNS))[KEYS.AUTO_RUNS] || {}) }; map[key] = run; await storageSet({ [KEYS.AUTO_RUNS]: map }); return run; }
async function patchAutoRun(conversationKey, fn) { const old = await getAutoRun(conversationKey); if (!old) return null; return saveAutoRun(conversationKey, fn(clone(old))); }
function publicRun(run) { if (!run) return null; const { request_worker_session_id, ...safe } = clone(run); return safe; }

function sendTabMessage(tabId, message) {
  return new Promise((resolve, reject) => {
    try {
      chrome.tabs.sendMessage(tabId, message, (response) => {
        const err = chrome.runtime.lastError;
        if (err) reject(new Error(err.message || String(err)));
        else resolve(response);
      });
    } catch (error) { reject(error); }
  });
}
async function identityForTab(tabId) {
  const response = await sendTabMessage(tabId, { type: "WS_GET_IDENTITY" });
  const raw = response?.identity || response || {};
  const derivedKey = raw.conversation_key
    || response?.conversation_key
    || (raw.origin && raw.conversation_id ? `${raw.origin}|${String(raw.conversation_id).toLowerCase()}` : "");
  const conversationKey = normalizeConversationKey(derivedKey);
  if (!conversationKey) throw Object.assign(new Error("Не удалось подтвердить ChatGPT-диалог во вкладке."), { code: "CONVERSATION_UNCONFIRMED" });
  return { ...raw, conversation_key: conversationKey };
}
async function assertTabConversation(tabId, conversationKey, expectedConversationId = null) {
  const key = normalizeConversationKey(conversationKey);
  const identity = await identityForTab(tabId);
  if (normalizeConversationKey(identity.conversation_key) !== key) throw Object.assign(new Error("Вкладка больше не принадлежит связанному диалогу."), { code: "CONVERSATION_MISMATCH" });
  if (expectedConversationId && String(identity.conversation_id || "").toLowerCase() !== String(expectedConversationId).toLowerCase()) throw Object.assign(new Error("Conversation ID изменился."), { code: "CONVERSATION_MISMATCH" });
  return identity;
}

function parseJsonMaybe(text) { try { return JSON.parse(String(text || "")); } catch { return null; } }
function annotateExecutionError(error, requestExecuted) { error.request_executed = requestExecuted; error.automatic_retry = false; return error; }

async function executeSearchCommand(command, metadata = {}) {
  const normalized = SearchProtocol.normalizeCommand(command);
  const settings = await getSettings();
  const apiKey = normalizeApiKey(settings.apiKey, { required: true });
  const folderId = normalizeFolderId(settings.folderId, { required: true });
  const request = SearchProtocol.buildRequest(normalized, folderId);
  const requestId = metadata.request_id || uid("search");
  const started = performance.now?.() ?? Date.now();
  await diagnostic("SEARCH_PROVIDER_INITIATED", { request_id: requestId, method: normalized.method, queryText: normalized.queryText, run_id: metadata.run_id || null });
  let response;
  try {
    response = await fetch(request.url, { method: "POST", headers: { "Content-Type": "application/json", Authorization: `Api-Key ${apiKey}` }, body: JSON.stringify(request.body) });
  } catch (error) {
    await diagnostic("SEARCH_PROVIDER_OUTCOME_UNKNOWN", { request_id: requestId, code: error?.name || "NETWORK_ERROR", message: error?.message || String(error) }, { level: "error" });
    throw annotateExecutionError(Object.assign(new Error("Исход Yandex Search request неизвестен; автоматический повтор запрещён."), { code: "REQUEST_OUTCOME_UNKNOWN_NO_RETRY", cause: error }), "UNKNOWN");
  }
  const elapsedMs = Math.max(0, Math.round((performance.now?.() ?? Date.now()) - started));
  let text = ""; try { text = await response.text(); } catch { text = ""; }
  const parsed = parseJsonMaybe(text);
  if (!response.ok) {
    const payload = SearchProtocol.safeErrorPayload(response.status, text, parsed);
    const envelope = SearchProtocol.buildResultEnvelope({ requestId, command: normalized, httpStatus: response.status, elapsedMs, result: { error: payload }, metadata: { ...metadata, status: "ERROR", reason: payload.code, request_executed: true, automatic_retry: false } });
    return { ok: false, http_status: response.status, request_id: requestId, report_envelope: envelope, report_text: SearchProtocol.formatResultEnvelope(envelope) };
  }
  let result;
  try { result = SearchProtocol.normalizeProviderResult(parsed); }
  catch (error) { throw annotateExecutionError(error, true); }
  const envelope = SearchProtocol.buildResultEnvelope({ requestId, command: normalized, httpStatus: response.status, elapsedMs, result, metadata: { ...metadata, status: "OK", reason: null, request_executed: true, automatic_retry: false } });
  await setStatus({ ok: true, code: "CONNECTED", service: "search", http_status: response.status });
  return { ok: true, http_status: response.status, request_id: requestId, report_envelope: envelope, report_text: SearchProtocol.formatResultEnvelope(envelope) };
}

async function executeWordstatCommand(command, metadata = {}) {
  const normalized = WordstatProtocol.normalizeCommand(command);
  const settings = await getSettings(); const apiKey = normalizeApiKey(settings.apiKey, { required: true }); const folderId = normalizeFolderId(settings.folderId, { required: true });
  const req = WordstatProtocol.buildRequest(normalized, folderId); const requestId = metadata.request_id || uid("wordstat"); const started = performance.now?.() ?? Date.now();
  let response;
  try { response = await fetch(req.url, { method: req.method || "POST", headers: { "Content-Type": "application/json", Authorization: `Api-Key ${apiKey}` }, body: req.body == null ? undefined : JSON.stringify(req.body) }); }
  catch (error) { throw annotateExecutionError(Object.assign(new Error("Исход Wordstat request неизвестен; автоматический повтор запрещён."), { code: "REQUEST_OUTCOME_UNKNOWN_NO_RETRY", cause: error }), "UNKNOWN"); }
  const elapsedMs = Math.max(0, Math.round((performance.now?.() ?? Date.now()) - started)); const text = await response.text(); const parsed = parseJsonMaybe(text);
  if (!response.ok) {
    const payload = WordstatProtocol.safeErrorPayload(response.status, text, parsed);
    const envelope = WordstatProtocol.buildResultEnvelope({ requestId, command: normalized, httpStatus: response.status, elapsedMs, result: { error: payload }, metadata: { ...metadata, status: "ERROR", reason: payload.code, request_executed: true, automatic_retry: false } });
    return { ok: false, http_status: response.status, request_id: requestId, report_envelope: envelope, report_text: WordstatProtocol.formatResultEnvelope(envelope) };
  }
  const envelope = WordstatProtocol.buildResultEnvelope({ requestId, command: normalized, httpStatus: response.status, elapsedMs, result: parsed, metadata: { ...metadata, status: "OK", reason: null, request_executed: true, automatic_retry: false } });
  return { ok: true, http_status: response.status, request_id: requestId, report_envelope: envelope, report_text: WordstatProtocol.formatResultEnvelope(envelope) };
}
async function executeServiceCommand(service, command, metadata = {}) {
  if (service === YMBServiceRegistry.SERVICES.SEARCH) return executeSearchCommand(command, metadata);
  if (service === YMBServiceRegistry.SERVICES.WORDSTAT) return executeWordstatCommand(command, metadata);
  throw Object.assign(new Error("Сервис не поддерживается."), { code: "SERVICE_NOT_AVAILABLE" });
}
async function executeServiceCore(service, commandText, metadata = {}) { const protocol = assertProtocolForService(service); return executeServiceCommand(service, protocol.parseCommand(commandText), metadata); }
async function executeSearchCore(commandText, metadata = {}) { return executeServiceCore(YMBServiceRegistry.SERVICES.SEARCH, commandText, metadata); }
async function executeWordstatCore(commandText, metadata = {}) { return executeServiceCore(YMBServiceRegistry.SERVICES.WORDSTAT, commandText, metadata); }

function formatBridgeError({ code, message, stage = "BRIDGE", requestExecuted = false, service = null, runId = null, operationId = null }) {
  return ["YMB_ERROR_V1", JSON.stringify({ bridge: YMBProduct.BRIDGE_ID, version: VERSION, status: "ERROR", code, message, stage, service, run_id: runId, operation_id: operationId, request_executed: requestExecuted, automatic_retry: false }, null, 2)].join("\n");
}
async function commonPublicSettingsFields() {
  const settings = await getSettings(); const [wordstatPolicy, searchPolicy] = await Promise.all([getWordstatPolicy(), getSearchPolicy()]);
  return { product_name: YMBProduct.NAME, product_version: VERSION, has_api_key: Boolean(settings.apiKey), folder_id: settings.folderId, credential_capability: publicCapability(settings), credential_capabilities: { wordstat: publicCapability(settings, "wordstat"), search: publicCapability(settings, "search") }, wordstat_policy: publicPolicy(wordstatPolicy, "wordstat"), search_policy: publicPolicy(searchPolicy, "search"), auto_send: settings.autoSend, debug_mode: settings.debugMode };
}
async function getAutoStartPrompt(conversationKey, { service = null } = {}) {
  const key = normalizeConversationKey(conversationKey); const resolved = service || (await getServiceContext(key)).active_service; const map = (await storageGet(KEYS.AUTO_START_PROMPTS))[KEYS.AUTO_START_PROMPTS] || {}; const rec = map[key];
  return rec?.text && rec.is_default !== true ? { ...rec, service: resolved } : { text: defaultAutoStartTextForService(resolved), is_default: true, service: resolved, updated_at: rec?.updated_at || null };
}
async function saveAutoStartPrompt(conversationKey, text, { service = null } = {}) {
  const key = normalizeConversationKey(conversationKey); const resolved = service || (await getServiceContext(key)).active_service; const value = String(text || "").trim(); if (!value) throw Object.assign(new Error("Стартовый текст пуст."), { code: "AUTO_START_PROMPT_EMPTY" });
  const map = { ...((await storageGet(KEYS.AUTO_START_PROMPTS))[KEYS.AUTO_START_PROMPTS] || {}) }; map[key] = { text: value, is_default: value === defaultAutoStartTextForService(resolved), service: resolved, updated_at: nowIso() }; await storageSet({ [KEYS.AUTO_START_PROMPTS]: map }); return map[key];
}
async function resetAutoStartPrompt(conversationKey, { service = null } = {}) { const key = normalizeConversationKey(conversationKey); const resolved = service || (await getServiceContext(key)).active_service; return saveAutoStartPrompt(key, defaultAutoStartTextForService(resolved), { service: resolved }); }

async function publicSettingsState(conversationKey) {
  const key = normalizeConversationKey(conversationKey); const [common, binding, manualMode, serviceContext, run, startPrompt] = await Promise.all([commonPublicSettingsFields(), getBinding(key), getManualMode(key), getServiceContext(key), getAutoRun(key), getAutoStartPrompt(key)]);
  const opsData = await storageGet(KEYS.MANUAL_OPERATIONS); const op = opsData[KEYS.MANUAL_OPERATIONS]?.[key] || null;
  return { ...common, conversation_key: key, binding, manual_mode: manualMode, service_context: serviceContext, auto_run: publicRun(run), auto_start_prompt: startPrompt, manual_operation: op ? { operation_id: op.operation_id, status: op.status, active_service: op.active_service, delivery_id: op.delivery_id || null } : null };
}
async function publicGlobalSettingsState(pageContextError = null) { return { ...(await commonPublicSettingsFields()), page_context_error: pageContextError, binding: null, manual_mode: false, service_context: { active_service: "wordstat" }, auto_run: null, auto_start_prompt: { text: DEFAULT_AUTO_START_TEXT, is_default: true, service: "wordstat" } }; }
async function patchToggleSettings(message = {}) {
  const values = {}; if (Object.hasOwn(message, "auto_send")) values[KEYS.AUTO_SEND] = message.auto_send === true; if (Object.hasOwn(message, "debug_mode")) values[KEYS.DEBUG_MODE] = message.debug_mode === true; if (Object.keys(values).length) await storageSet(values);
  if (Object.hasOwn(message, "wordstat_autorun_enabled")) { const p = await getWordstatPolicy(); await saveWordstatPolicy({ ...p, autorun_enabled: message.wordstat_autorun_enabled === true }); }
  if (Object.hasOwn(message, "search_autorun_enabled")) { const p = await getSearchPolicy(); await saveSearchPolicy({ ...p, autorun_enabled: message.search_autorun_enabled === true }); }
  if (message.conversation_key && Object.hasOwn(message, "manual_mode")) await setManualMode(message.conversation_key, message.manual_mode === true);
  return message.conversation_key ? publicSettingsState(message.conversation_key) : publicGlobalSettingsState();
}

function exportedSettingsKeys() { return [KEYS.API_KEY, KEYS.FOLDER_ID, KEYS.AUTO_SEND, KEYS.CONVERSATION_BINDINGS, KEYS.MANUAL_MODES, KEYS.REPORT_PREFIXES, KEYS.AUTO_START_PROMPTS, KEYS.SERVICE_CONTEXTS, KEYS.WORDSTAT_POLICY, KEYS.SEARCH_POLICY, KEYS.DEBUG_MODE]; }
async function exportSettingsBackup() {
  const data = await storageGet(exportedSettingsKeys()); const settings = await getSettings();
  return { schema: "YMB_SETTINGS_BACKUP_V2", version: VERSION, exported_at: nowIso(), settings: { wordstat: { api_key: settings.apiKey, folder_id: settings.folderId }, auto_send: data[KEYS.AUTO_SEND] !== false, conversation_bindings: data[KEYS.CONVERSATION_BINDINGS] || {}, manual_modes: data[KEYS.MANUAL_MODES] || {}, report_prefixes: data[KEYS.REPORT_PREFIXES] || {}, auto_start_prompts: data[KEYS.AUTO_START_PROMPTS] || {}, service_contexts: data[KEYS.SERVICE_CONTEXTS] || {}, wordstat_policy: publicPolicy(data[KEYS.WORDSTAT_POLICY] || {}, "wordstat"), search_policy: publicPolicy(data[KEYS.SEARCH_POLICY] || {}, "search"), debug_mode: data[KEYS.DEBUG_MODE] === true } };
}
async function importSettingsBackup(backup) {
  const incoming = backup?.settings; if (!incoming || typeof incoming !== "object") throw Object.assign(new Error("Некорректный backup."), { code: "INVALID_BACKUP" });
  const runs = (await storageGet(KEYS.AUTO_RUNS))[KEYS.AUTO_RUNS] || {}; if (Object.values(runs).some((r) => r && !WordstatAutorunModel.isTerminalStatus(r.status))) throw Object.assign(new Error("Нельзя импортировать настройки во время активного Autorun."), { code: "IMPORT_ACTIVE_RUN" });
  const ops = (await storageGet(KEYS.MANUAL_OPERATIONS))[KEYS.MANUAL_OPERATIONS] || {}; if (Object.values(ops).some((op) => op && !TERMINAL_MANUAL_STATUSES.has(op.status))) throw Object.assign(new Error("Нельзя импортировать настройки во время активной Manual-операции."), { code: "IMPORT_ACTIVE_MANUAL" });
  const wordstat = incoming.wordstat || {}; const apiKey = String(wordstat.api_key || "").trim(); const folderId = String(wordstat.folder_id || DEFAULT_FOLDER_ID).trim();
  await storageSet({ [KEYS.API_KEY]: apiKey, [KEYS.FOLDER_ID]: folderId, [KEYS.AUTO_SEND]: incoming.auto_send !== false, [KEYS.CONVERSATION_BINDINGS]: clone(incoming.conversation_bindings || {}), [KEYS.MANUAL_MODES]: clone(incoming.manual_modes || {}), [KEYS.REPORT_PREFIXES]: clone(incoming.report_prefixes || {}), [KEYS.AUTO_START_PROMPTS]: clone(incoming.auto_start_prompts || {}), [KEYS.SERVICE_CONTEXTS]: clone(incoming.service_contexts || {}), [KEYS.WORDSTAT_POLICY]: YMBPolicyModel.normalizeWordstatPolicy(incoming.wordstat_policy || {}), [KEYS.SEARCH_POLICY]: YMBPolicyModel.normalizeSearchPolicy(incoming.search_policy || {}), [KEYS.DEBUG_MODE]: incoming.debug_mode === true, [KEYS.SETTINGS_SCHEMA]: SETTINGS_SCHEMA_VERSION });
  return { imported: true };
}

function discoverManualBlockItems(blockText) {
  const discovered = YMBBlockCommandDiscovery.discover(blockText, YMBServiceRegistry); const items = [];
  for (const d of discovered) {
    const base = { service: d.service, prefix: d.prefix, marker_index: d.index, request_executed: false, automatic_retry: false, status: "pending" };
    if (!d.ok) { items.push({ ...base, status: "error", stage: "COMMAND_DISCOVERY", code: d.code, message: d.message }); continue; }
    try { const protocol = assertProtocolForService(d.service); const command = protocol.normalizeCommand(d.raw); items.push({ ...base, stage: "VALIDATED", operation: command.method, command }); }
    catch (error) { items.push({ ...base, status: "error", stage: "COMMAND_VALIDATION", code: error.code || "INVALID_COMMAND", message: error.message || String(error) }); }
  }
  return { items, marker_count: discovered.length };
}
async function getOutbox() { const data = await storageGet(KEYS.OUTBOX); return data[KEYS.OUTBOX] && typeof data[KEYS.OUTBOX] === "object" ? data[KEYS.OUTBOX] : {}; }
async function putOutbox(conversationKey, entry) { const key = normalizeConversationKey(conversationKey); const outbox = { ...(await getOutbox()) }; outbox[key] = { ...entry, conversation_key: key, updated_at: nowIso() }; await storageSet({ [KEYS.OUTBOX]: outbox }); return outbox[key]; }
async function clearOutbox(conversationKey, deliveryId = null) { const key = normalizeConversationKey(conversationKey); const outbox = { ...(await getOutbox()) }; if (!deliveryId || outbox[key]?.delivery_id === deliveryId) delete outbox[key]; await storageSet({ [KEYS.OUTBOX]: outbox }); }

async function executeManualBlock(blockText, conversationKey, sender, manualRequestToken = "") {
  const key = normalizeConversationKey(conversationKey); const senderTabId = Number(sender?.tab?.id);
  if (!Number.isInteger(senderTabId)) return { ok: false, accepted: false, code: "MANUAL_SENDER_TAB_REQUIRED", error: "Manual action должна исходить из вкладки ChatGPT." };
  let liveIdentity; try { liveIdentity = await assertTabConversation(senderTabId, key); } catch (error) { return { ok: false, accepted: false, code: error.code, error: error.message }; }
  const binding = await getBinding(key); if (!binding || binding.conversation_id !== liveIdentity.conversation_id) return { ok: false, accepted: false, code: "CONVERSATION_NOT_BOUND", error: "Сначала привяжите этот диалог в popup." };
  if (!(await getManualMode(key))) return { ok: false, accepted: false, code: "MANUAL_MODE_DISABLED", error: "Ручной режим выключен." };
  const source = String(blockText || ""); const serviceContext = await getServiceContext(key); const preflight = discoverManualBlockItems(source);
  const mismatch = preflight.items.find((item) => item.service && item.service !== serviceContext.active_service);
  if (mismatch) return { ok: false, accepted: false, code: "SERVICE_NOT_ACTIVE", error: `Активный сервис ${serviceContext.active_service}; команда ${mismatch.prefix} относится к ${mismatch.service}.`, request_executed: false };
  const currentRun = await getAutoRun(key); if (currentRun && !WordstatAutorunModel.isTerminalStatus(currentRun.status) && currentRun.status !== WordstatAutorunModel.RUN_STATUSES.PAUSED) return { ok: false, accepted: false, code: "AUTORUN_NOT_PAUSED", error: "Для Manual активный Autorun должен быть поставлен на паузу." };
  if (currentRun?.status === WordstatAutorunModel.RUN_STATUSES.PAUSED) { try { YMBRunContextModel.assertServiceMatch(currentRun.active_service, serviceContext.active_service); } catch (error) { return { ok: false, accepted: false, code: error.code, error: error.message }; } }
  const data = await storageGet(KEYS.MANUAL_OPERATIONS); const map = { ...(data[KEYS.MANUAL_OPERATIONS] || {}) }; const existing = map[key];
  if (existing && !TERMINAL_MANUAL_STATUSES.has(existing.status)) return { ok: false, accepted: false, code: "MANUAL_OPERATION_ACTIVE", error: "Предыдущая ручная операция ещё не завершена." };
  const requestToken = String(manualRequestToken || uid("manual-request")); if (existing?.request_token === requestToken) return { ok: true, accepted: false, duplicate: true, operation_id: existing.operation_id };
  const operation = { operation_id: uid("manual"), request_token: requestToken, conversation_key: key, tab_id: senderTabId, active_service: serviceContext.active_service, run_id: currentRun?.status === WordstatAutorunModel.RUN_STATUSES.PAUSED ? currentRun.run_id : null, status: "requesting", block_fingerprint: YMBBlockCommandDiscovery.textFingerprint(source), created_at: nowIso(), request_executed: false };
  map[key] = operation; await storageSet({ [KEYS.MANUAL_OPERATIONS]: map });
  let reportText = ""; let providerExecutions = 0;
  if (!preflight.items.length) reportText = formatBridgeError({ code: "NO_SUPPORTED_COMMAND", message: "В выбранном блоке нет поддерживаемой команды Yandex Marketing Bridge.", stage: "COMMAND_DISCOVERY", requestExecuted: false, service: serviceContext.active_service, operationId: operation.operation_id });
  else {
    const reports = [];
    for (const item of preflight.items) {
      if (item.status === "error") { reports.push(formatBridgeError({ code: item.code, message: item.message, stage: item.stage, requestExecuted: false, service: item.service, operationId: operation.operation_id })); continue; }
      const settings = await getSettings(); const policy = await getPolicyForService(item.service); const budgetRun = operation.run_id ? await getAutoRun(key) : {};
      const decision = policyDecisionForService(item.service, { policy, channel: "manual", method: item.command.method, credentialState: publicCapability(settings, item.service).state, run: budgetRun || {} });
      if (!decision.allow) { const protocol = assertProtocolForService(item.service); reports.push(protocol.formatSkippedReport({ requestId: uid("skip"), command: item.command, reason: decision.reason, metadata: { run_id: operation.run_id || null, cost_estimate: { estimated_rub: decision.estimated_cost_rub, tariff_checked_at: decision.policy.tariff_checked_at, tariff_source: decision.policy.tariff_source }, policy: { channel: "manual", active_service: item.service }, request_executed: false, automatic_retry: false } })); continue; }
      if (operation.run_id) await patchAutoRun(key, (run) => ({ ...run, requests_attempted: Number(run.requests_attempted || 0) + 1, requests_executed: Number(run.requests_executed || 0) + 1, estimated_cost_rub: Number((Number(run.estimated_cost_rub || 0) + Number(decision.estimated_cost_rub || 0)).toFixed(6)) }));
      try { const result = await executeServiceCommand(item.service, item.command, { conversation_key: key, run_id: operation.run_id || null, cost_estimate: { estimated_rub: decision.estimated_cost_rub, tariff_checked_at: decision.policy.tariff_checked_at, tariff_source: decision.policy.tariff_source }, policy: { channel: "manual", active_service: item.service } }); providerExecutions += 1; reports.push(result.report_text); }
      catch (error) { reports.push(formatBridgeError({ code: error.code || "PROVIDER_ERROR", message: error.message || String(error), stage: "PROVIDER", requestExecuted: error.request_executed ?? "UNKNOWN", service: item.service, runId: operation.run_id, operationId: operation.operation_id })); }
    }
    reportText = reports.join("\n\n---\n\n");
  }
  const deliveryId = uid("delivery"); await putOutbox(key, { delivery_id: deliveryId, operation_id: operation.operation_id, type: "manual", tab_id: senderTabId, report_text: reportText, phase: "claimed", provider_executions: providerExecutions, created_at: nowIso() });
  map[key] = { ...operation, status: "delivering", delivery_id: deliveryId, request_executed: providerExecutions > 0, report_ready_at: nowIso() }; await storageSet({ [KEYS.MANUAL_OPERATIONS]: map });
  return { ok: true, accepted: true, operation_id: operation.operation_id, delivery_id: deliveryId, report_text: reportText, request_executed: providerExecutions > 0 };
}

async function startAutoRun(conversationKey, tabId) {
  const key = normalizeConversationKey(conversationKey); const tab = Number(tabId); if (!Number.isInteger(tab)) throw Object.assign(new Error("Не определена вкладка-owner."), { code: "OWNER_TAB_REQUIRED" });
  const liveIdentity = await assertTabConversation(tab, key); const binding = await getBinding(key); if (!binding) throw Object.assign(new Error("Сначала привяжите диалог."), { code: "CONVERSATION_NOT_BOUND" }); if (await getManualMode(key)) throw Object.assign(new Error("Сначала отключите ручной режим."), { code: "MANUAL_MODE_ACTIVE" });
  const service = (await getServiceContext(key)).active_service; const policy = await getPolicyForService(service); if (!policy.autorun_enabled) throw Object.assign(new Error("Autorun выключен для выбранного сервиса."), { code: "AUTORUN_DISABLED" });
  const existing = await getAutoRun(key); if (existing && !WordstatAutorunModel.isTerminalStatus(existing.status)) throw Object.assign(new Error("Для этого диалога уже существует активный Autorun."), { code: "AUTO_RUN_ALREADY_ACTIVE" });
  const startPrompt = await getAutoStartPrompt(key, { service }); const run = { run_id: uid("ymbrun"), active_service: service, permission_profile: service.toUpperCase(), requests_attempted: 0, requests_executed: 0, requests_skipped: 0, estimated_cost_rub: 0, conversation_key: key, origin: liveIdentity.origin, conversation_id: liveIdentity.conversation_id, binding_snapshot: clone(binding), tab_id: tab, status: WordstatAutorunModel.RUN_STATUSES.STARTING, sequence: 0, pause_requested: false, finish_requested: false, assistant_baseline_ids: [], watch_id: null, start_delivery: { phase: "none", message_text: startPrompt.text }, delivery: null, created_at: nowIso() };
  await saveAutoRun(key, run); await putOutbox(key, { delivery_id: uid("start"), type: "autorun_start", run_id: run.run_id, tab_id: tab, report_text: startPrompt.text, phase: "claimed", created_at: nowIso() }); return run;
}
async function handleAutoCommand(message, sender) {
  const key = normalizeConversationKey(message?.conversation_key); const runId = String(message?.run_id || ""); const commandText = String(message?.command_text || ""); const assistantTurnId = String(message?.assistant_turn_id || ""); const senderTabId = Number(sender?.tab?.id); const currentRun = await getAutoRun(key);
  if (!currentRun || currentRun.run_id !== runId) return { ok: false, accepted: false, code: "AUTO_RUN_NOT_FOUND", error: "Autorun не найден." };
  if (!Number.isInteger(senderTabId) || senderTabId !== Number(currentRun.tab_id)) return { ok: false, accepted: false, code: "AUTO_NON_OWNER_TAB", error: "Команда появилась не во вкладке-owner активного Autorun." };
  try { await assertTabConversation(senderTabId, key, currentRun.conversation_id); } catch (error) { return { ok: false, accepted: false, code: error.code || "CONVERSATION_MISMATCH", error: error.message }; }
  if (await getManualMode(key)) return { ok: false, paused: true, code: "MANUAL_MODE_ACTIVE", error: "Ручной режим включён; Autorun не выполняет команду." };
  if (![WordstatAutorunModel.RUN_STATUSES.WAITING_COMMAND, WordstatAutorunModel.RUN_STATUSES.DELIVERING].includes(currentRun.status)) return { ok: true, accepted: false, ignored: true, status: currentRun.status };
  if (assistantTurnId && currentRun.last_assistant_turn_id === assistantTurnId) return { ok: true, accepted: false, ignored: true, duplicate: true, status: currentRun.status };
  const detected = YMBServiceRegistry.detect(commandText); if (!detected) return { ok: false, accepted: false, code: "UNKNOWN_SERVICE_PROTOCOL", error: "Блок не относится ни к одному зарегистрированному сервису." };
  try { YMBRunContextModel.assertServiceMatch(currentRun.active_service, detected.service); } catch (error) { return { ok: false, accepted: false, skipped: true, code: error.code || "SERVICE_NOT_ACTIVE", error: error.message }; }
  const protocol = protocolForService(detected.service); let parsed; try { parsed = protocol.parseCommand(commandText); } catch (error) { return { ok: false, accepted: false, code: error.code || "INVALID_COMMAND", error: error.message }; }
  const fingerprint = protocol.commandFingerprint(parsed); if (currentRun.last_error?.request_executed === "UNKNOWN" && currentRun.last_command_fingerprint === fingerprint) return { ok: false, accepted: false, code: "REQUEST_OUTCOME_UNKNOWN_NO_RETRY", error: "Предыдущий такой же запрос имеет неизвестный исход. Автоматический повтор запрещён." };
  let run = await patchAutoRun(key, (r) => ({ ...r, last_assistant_turn_id: assistantTurnId, last_command_fingerprint: fingerprint, last_method: parsed.method, last_phrase: parsed.phrase || parsed.queryText || null, requests_attempted: Number(r.requests_attempted || 0) + 1, last_error: null }));
  const [settings, policy] = await Promise.all([getSettings(), getPolicyForService(run.active_service)]); const decision = policyDecisionForService(run.active_service, { policy, channel: "autorun", method: parsed.method, credentialState: publicCapability(settings, run.active_service).state, run });
  if (!decision.allow) { const reportText = protocol.formatSkippedReport({ requestId: uid("skip"), command: parsed, reason: decision.reason, metadata: { run_id: run.run_id, cost_estimate: { estimated_rub: decision.estimated_cost_rub, tariff_checked_at: decision.policy.tariff_checked_at, tariff_source: decision.policy.tariff_source }, policy: { channel: "autorun", active_service: run.active_service }, request_executed: false, automatic_retry: false } }); run = await patchAutoRun(key, (r) => ({ ...r, requests_skipped: Number(r.requests_skipped || 0) + 1, status: WordstatAutorunModel.RUN_STATUSES.DELIVERING, delivery: { delivery_id: uid("delivery"), phase: "claimed", report_text: reportText } })); await putOutbox(key, { delivery_id: run.delivery.delivery_id, type: "autorun", run_id: run.run_id, tab_id: senderTabId, report_text: reportText, phase: "claimed", created_at: nowIso() }); return { ok: true, accepted: true, skipped: true, report_text: reportText, reason: decision.reason }; }
  run = await patchAutoRun(key, (r) => ({ ...r, status: WordstatAutorunModel.RUN_STATUSES.REQUESTING, requests_executed: Number(r.requests_executed || 0) + 1, estimated_cost_rub: Number((Number(r.estimated_cost_rub || 0) + Number(decision.estimated_cost_rub || 0)).toFixed(6)), request_worker_session_id: "current" }));
  let result; try { result = await executeServiceCore(run.active_service, commandText, { conversation_key: key, run_id: run.run_id, cost_estimate: { estimated_rub: decision.estimated_cost_rub, tariff_checked_at: decision.policy.tariff_checked_at, tariff_source: decision.policy.tariff_source }, policy: { channel: "autorun", active_service: run.active_service } }); } catch (error) { await patchAutoRun(key, (r) => ({ ...r, status: WordstatAutorunModel.RUN_STATUSES.ERROR, last_error: { code: error.code || "PROVIDER_ERROR", message: error.message, request_executed: error.request_executed ?? "UNKNOWN", automatic_retry: false } })); throw error; }
  const deliveryId = uid("delivery"); await putOutbox(key, { delivery_id: deliveryId, type: "autorun", run_id: run.run_id, tab_id: senderTabId, report_text: result.report_text, phase: "claimed", created_at: nowIso() }); await patchAutoRun(key, (r) => ({ ...r, status: WordstatAutorunModel.RUN_STATUSES.DELIVERING, delivery: { delivery_id: deliveryId, phase: "claimed", request_id: result.request_id, outgoing_text: result.report_text } })); return { ok: true, accepted: true, report_text: result.report_text, result };
}
async function completeDelivery(message) {
  const key = normalizeConversationKey(message.conversation_key); const deliveryId = String(message.delivery_id || ""); const outbox = await getOutbox(); const entry = outbox[key]; if (!entry || (deliveryId && entry.delivery_id !== deliveryId)) return { ok: false, code: "DELIVERY_NOT_FOUND" };
  await clearOutbox(key, entry.delivery_id);
  if (entry.type === "manual") { const data = await storageGet(KEYS.MANUAL_OPERATIONS); const map = { ...(data[KEYS.MANUAL_OPERATIONS] || {}) }; if (map[key]?.delivery_id === entry.delivery_id) { map[key] = { ...map[key], status: "completed", delivery_confirmed: true, confirmation_basis: message.confirmation_basis || "microphone", completed_at: nowIso() }; await storageSet({ [KEYS.MANUAL_OPERATIONS]: map }); } }
  else if (entry.type === "autorun_start") await patchAutoRun(key, (run) => WordstatAutorunModel.afterConfirmedStart({ ...run, start_delivery: { ...(run.start_delivery || {}), phase: "committed" } }, message.assistant_baseline_ids || []));
  else if (entry.type === "autorun") await patchAutoRun(key, (run) => WordstatAutorunModel.afterConfirmedDelivery({ ...run, delivery: { ...(run.delivery || {}), phase: "confirmed" } }));
  return { ok: true };
}
async function bindConversationFromTab(tabId) { const identity = await identityForTab(Number(tabId)); const binding = await saveBinding(identity); return { binding, conversation_key: identity.conversation_key }; }

async function handleMessage(message, sender) {
  switch (message?.type) {
    case "WS_GET_GLOBAL_STATE": return { ok: true, state: await publicGlobalSettingsState(message.page_context_error || null) };
    case "WS_GET_STATE": return { ok: true, state: await publicSettingsState(message.conversation_key) };
    case "WS_BIND_CONVERSATION": return { ok: true, ...(await bindConversationFromTab(message.tab_id || sender?.tab?.id)) };
    case "WS_PATCH_TOGGLES": return { ok: true, state: await patchToggleSettings(message) };
    case "WS_SET_MANUAL_MODE": return { ok: true, enabled: await setManualMode(message.conversation_key, message.enabled === true), state: await publicSettingsState(message.conversation_key) };
    case "WS_SAVE_SETTINGS": {
      const values = {}; if (typeof message.api_key === "string" && message.api_key.trim()) values[KEYS.API_KEY] = normalizeApiKey(message.api_key, { required: true }); if (typeof message.folder_id === "string") values[KEYS.FOLDER_ID] = normalizeFolderId(message.folder_id, { required: true }); if (Object.hasOwn(message, "auto_send")) values[KEYS.AUTO_SEND] = message.auto_send === true; if (Object.hasOwn(message, "debug_mode")) values[KEYS.DEBUG_MODE] = message.debug_mode === true; if (Object.keys(values).length) await storageSet(values); if (message.wordstat_policy) await saveWordstatPolicy(message.wordstat_policy); if (message.search_policy) await saveSearchPolicy(message.search_policy); if (message.conversation_key && message.active_service) await saveServiceContext(message.conversation_key, { active_service: message.active_service }); return { ok: true, state: message.conversation_key ? await publicSettingsState(message.conversation_key) : await publicGlobalSettingsState() };
    }
    case "WS_SAVE_SERVICE_CONTEXT": return { ok: true, service_context: await saveServiceContext(message.conversation_key, { active_service: message.active_service }) };
    case "WS_SAVE_AUTO_START_PROMPT": return { ok: true, auto_start_prompt: await saveAutoStartPrompt(message.conversation_key, message.text, { service: message.active_service || null }) };
    case "WS_RESET_AUTO_START_PROMPT": return { ok: true, auto_start_prompt: await resetAutoStartPrompt(message.conversation_key, { service: message.active_service || null }) };
    case "WS_START_AUTORUN": return { ok: true, run: publicRun(await startAutoRun(message.conversation_key, message.tab_id || sender?.tab?.id)) };
    case "WS_PAUSE_AUTORUN": return { ok: true, run: publicRun(await patchAutoRun(message.conversation_key, (r) => ({ ...r, status: WordstatAutorunModel.RUN_STATUSES.PAUSED }))) };
    case "WS_RESUME_AUTORUN": return { ok: true, run: publicRun(await patchAutoRun(message.conversation_key, (r) => ({ ...r, status: WordstatAutorunModel.RUN_STATUSES.WAITING_COMMAND }))) };
    case "WS_FINISH_AUTORUN": return { ok: true, run: publicRun(await patchAutoRun(message.conversation_key, (r) => ({ ...r, status: WordstatAutorunModel.RUN_STATUSES.STOPPED, finish_requested: false }))) };
    case "WS_AUTO_COMMAND": return handleAutoCommand(message, sender);
    case "WS_EXECUTE_MANUAL_BLOCK": return executeManualBlock(message.block_text, message.conversation_key, sender, message.manual_request_token);
    case "WS_GET_OUTBOX": { const key = normalizeConversationKey(message.conversation_key); const outbox = await getOutbox(); return { ok: true, outbox: outbox[key] || null }; }
    case "WS_MARK_DELIVERY_COMMITTED": { const key = normalizeConversationKey(message.conversation_key); const outbox = await getOutbox(); const entry = outbox[key]; if (!entry || entry.delivery_id !== message.delivery_id) return { ok: false, code: "DELIVERY_NOT_FOUND" }; await putOutbox(key, { ...entry, phase: "committed", committed_at: nowIso() }); return { ok: true }; }
    case "WS_MANUAL_DELIVERY_COMPLETE": case "WS_AUTO_DELIVERY_COMPLETE": return completeDelivery(message);
    case "WS_EXPORT_BACKUP": return { ok: true, backup: await exportSettingsBackup() };
    case "WS_IMPORT_BACKUP": return { ok: true, result: await importSettingsBackup(message.backup), state: await publicGlobalSettingsState() };
    default: return { ok: false, code: "UNKNOWN_MESSAGE", error: "Неизвестная команда расширения." };
  }
}
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => { Promise.resolve(handleMessage(message, sender)).then(sendResponse).catch((error) => sendResponse({ ok: false, code: error.code || "WORKER_ERROR", error: error.message || String(error), request_executed: error.request_executed ?? false, automatic_retry: false })); return true; });
