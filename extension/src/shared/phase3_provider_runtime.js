(() => {
  "use strict";

  const Credentials = globalThis.YMBCredentialRuntime;
  const Webmaster = globalThis.WebmasterProtocol;
  const Registry = globalThis.YMBServiceRegistry;
  const Policy = globalThis.YMBPolicyModel;
  const Wordstat = globalThis.WordstatProtocol;
  const Search = globalThis.SearchProtocol;
  if (!Credentials || !Webmaster || !Registry || !Policy || !Wordstat || !Search) throw new Error("Phase 3 provider prerequisites are unavailable.");

  const WEBMASTER_POLICY_KEY = "ymb_webmaster_policy";
  function trim(value) { return String(value ?? "").trim(); }
  function nowIso() { return new Date().toISOString(); }
  function id(prefix) { return `${prefix}-${crypto.randomUUID()}`; }
  function parseJson(text) { try { return JSON.parse(String(text || "")); } catch { return null; } }
  function elapsed(started) { return Math.max(0, Math.round((performance.now?.() ?? Date.now()) - started)); }
  function executionError(error, requestExecuted) { error.request_executed = requestExecuted; error.automatic_retry = false; return error; }

  async function getWebmasterPolicy() {
    const raw = (await chrome.storage.local.get(WEBMASTER_POLICY_KEY))[WEBMASTER_POLICY_KEY] || {};
    return Policy.normalizeWebmasterPolicy(raw);
  }

  async function saveWebmasterPolicy(raw) {
    const normalized = Policy.normalizeWebmasterPolicy(raw || {});
    await chrome.storage.local.set({ [WEBMASTER_POLICY_KEY]: normalized });
    return normalized;
  }

  async function executeCloud(service, command, metadata = {}) {
    const isSearch = service === Registry.SERVICES.SEARCH;
    const Protocol = isSearch ? Search : Wordstat;
    const normalized = Protocol.normalizeCommand(command);
    const settings = await Credentials.settings();
    const record = settings.credentials[service] || {};
    const apiKey = trim(record.api_key);
    const folderId = trim(record.folder_id);
    if (!apiKey) throw Object.assign(new Error(`API key ${service} не сохранён в расширении.`), { code: "API_KEY_MISSING", request_executed: false, automatic_retry: false });
    if (!folderId) throw Object.assign(new Error(`Folder ID ${service} не сохранён в расширении.`), { code: "FOLDER_ID_MISSING", request_executed: false, automatic_retry: false });
    const req = Protocol.buildRequest(normalized, folderId);
    const requestId = metadata.request_id || id(service);
    const started = performance.now?.() ?? Date.now();
    let response;
    try {
      response = await fetch(req.url, {
        method: isSearch ? "POST" : (req.method || "POST"),
        headers: { "Content-Type": "application/json", Authorization: `Api-Key ${apiKey}` },
        body: isSearch ? JSON.stringify(req.body) : (req.body == null ? undefined : JSON.stringify(req.body))
      });
    } catch (error) {
      const name = isSearch ? "Yandex Search" : "Wordstat";
      throw executionError(Object.assign(new Error(`Исход ${name} request неизвестен; автоматический повтор запрещён.`), { code: "REQUEST_OUTCOME_UNKNOWN_NO_RETRY", cause: error }), "UNKNOWN");
    }
    let text = "";
    try { text = await response.text(); } catch { text = ""; }
    const parsed = parseJson(text);
    if (!response.ok) {
      const payload = Protocol.safeErrorPayload(response.status, text, parsed);
      const envelope = Protocol.buildResultEnvelope({ requestId, command: normalized, httpStatus: response.status, elapsedMs: elapsed(started), result: { error: payload }, metadata: { ...metadata, status: "ERROR", reason: payload.code, request_executed: true, automatic_retry: false } });
      return { ok: false, http_status: response.status, request_id: requestId, report_envelope: envelope, report_text: Protocol.formatResultEnvelope(envelope) };
    }
    let result = parsed;
    if (isSearch) {
      try { result = Protocol.normalizeProviderResult(parsed); }
      catch (error) { throw executionError(error, true); }
    }
    const envelope = Protocol.buildResultEnvelope({ requestId, command: normalized, httpStatus: response.status, elapsedMs: elapsed(started), result, metadata: { ...metadata, status: "OK", reason: null, request_executed: true, automatic_retry: false } });
    return { ok: true, http_status: response.status, request_id: requestId, report_envelope: envelope, report_text: Protocol.formatResultEnvelope(envelope) };
  }

  async function executeWebmaster(command, metadata = {}) {
    const normalized = Webmaster.normalizeCommand(command);
    const settings = await Credentials.settings();
    const record = settings.credentials.webmaster || {};
    const oauthToken = trim(record.oauth_token);
    const userId = trim(record.user_id);
    if (!oauthToken) throw Object.assign(new Error("OAuth token Webmaster не сохранён в расширении."), { code: "WEBMASTER_OAUTH_MISSING", request_executed: false, automatic_retry: false });
    if (!/^\d+$/.test(userId)) throw Object.assign(new Error("Webmaster user_id не подтверждён. Выполните Check."), { code: "WEBMASTER_USER_ID_MISSING", request_executed: false, automatic_retry: false });
    const req = Webmaster.buildRequest(normalized, userId);
    const requestId = metadata.request_id || id("webmaster");
    const started = performance.now?.() ?? Date.now();
    let response;
    try {
      response = await fetch(req.url, { method: "GET", headers: { Accept: "application/json", Authorization: `OAuth ${oauthToken}` } });
    } catch (error) {
      throw executionError(Object.assign(new Error("Исход Yandex Webmaster request неизвестен; автоматический повтор запрещён."), { code: "REQUEST_OUTCOME_UNKNOWN_NO_RETRY", cause: error }), "UNKNOWN");
    }
    let text = "";
    try { text = await response.text(); } catch { text = ""; }
    const parsed = parseJson(text);
    if (!response.ok) {
      const payload = Webmaster.safeErrorPayload(response.status, text, parsed);
      const envelope = Webmaster.buildResultEnvelope({ requestId, command: normalized, httpStatus: response.status, elapsedMs: elapsed(started), result: { error: payload }, metadata: { ...metadata, status: "ERROR", reason: payload.code, request_executed: true, automatic_retry: false } });
      return { ok: false, http_status: response.status, request_id: requestId, report_envelope: envelope, report_text: Webmaster.formatResultEnvelope(envelope) };
    }
    let result;
    try { result = Webmaster.normalizeProviderResult(normalized, parsed); }
    catch (error) { throw executionError(error, true); }
    const envelope = Webmaster.buildResultEnvelope({ requestId, command: normalized, httpStatus: response.status, elapsedMs: elapsed(started), result, metadata: { ...metadata, status: "OK", reason: null, request_executed: true, automatic_retry: false } });
    return { ok: true, http_status: response.status, request_id: requestId, report_envelope: envelope, report_text: Webmaster.formatResultEnvelope(envelope) };
  }

  async function execute(service, command, metadata = {}) {
    if (service === Registry.SERVICES.WEBMASTER) return executeWebmaster(command, metadata);
    if (service === Registry.SERVICES.SEARCH || service === Registry.SERVICES.WORDSTAT) return executeCloud(service, command, metadata);
    throw Object.assign(new Error("Сервис не поддерживается."), { code: "SERVICE_NOT_AVAILABLE" });
  }

  async function checkWebmaster(oauthToken) {
    const token = trim(oauthToken);
    if (!token) throw Object.assign(new Error("OAuth token Webmaster пуст."), { code: "WEBMASTER_OAUTH_MISSING", request_executed: false, automatic_retry: false });
    let response;
    try {
      response = await fetch(`${Webmaster.BASE_URL}/user`, { method: "GET", headers: { Accept: "application/json", Authorization: `OAuth ${token}` } });
    } catch (error) {
      const current = await Credentials.load();
      await Credentials.save("webmaster", { ...current.webmaster, oauth_token: token, user_id: "", verified_at: null, check_state: "NETWORK_ERROR" });
      throw executionError(Object.assign(new Error("Не удалось проверить Webmaster OAuth: сетевой исход неизвестен."), { code: "WEBMASTER_CHECK_NETWORK_ERROR", cause: error }), "UNKNOWN");
    }
    let text = "";
    try { text = await response.text(); } catch { text = ""; }
    const parsed = parseJson(text);
    if (!response.ok) {
      const state = response.status === 403 ? "NO_ACCESS" : "INVALID_OR_EXPIRED";
      await Credentials.save("webmaster", { oauth_token: token, user_id: "", verified_at: nowIso(), check_state: state });
      const payload = Webmaster.safeErrorPayload(response.status, text, parsed);
      return { ok: false, state, http_status: response.status, code: payload.code, error: payload.message, request_executed: true, automatic_retry: false };
    }
    const userId = trim(parsed?.user_id ?? parsed?.userId);
    if (!/^\d+$/.test(userId)) {
      await Credentials.save("webmaster", { oauth_token: token, user_id: "", verified_at: nowIso(), check_state: "INVALID_OR_EXPIRED" });
      throw Object.assign(new Error("Webmaster /v4/user не вернул корректный user_id."), { code: "WEBMASTER_USER_ID_INVALID", request_executed: true, automatic_retry: false });
    }
    const record = await Credentials.save("webmaster", { oauth_token: token, user_id: userId, verified_at: nowIso(), check_state: "PRESENT" });
    return { ok: true, state: "PRESENT", user_id: record.user_id, http_status: response.status, request_executed: true, automatic_retry: false };
  }

  globalThis.YMBPhase3ProviderRuntime = Object.freeze({
    getWebmasterPolicy,
    saveWebmasterPolicy,
    execute,
    executeWebmaster,
    executeCloud,
    checkWebmaster
  });
})();
