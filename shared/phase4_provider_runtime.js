(() => {
  "use strict";

  const Credentials = globalThis.YMBCredentialRuntime;
  const Metrika = globalThis.MetrikaProtocol;
  const Base = globalThis.YMBPhase3ProviderRuntime;
  const Policy = globalThis.YMBPolicyModel;
  const Registry = globalThis.YMBServiceRegistry;
  if (!Credentials || !Metrika || !Base || !Policy || !Registry) throw new Error("Phase 4 provider prerequisites are unavailable.");

  const METRIKA_POLICY_KEY = "ymb_metrika_policy";
  function trim(value) { return String(value ?? "").trim(); }
  function nowIso() { return new Date().toISOString(); }
  function id(prefix) { return `${prefix}-${crypto.randomUUID()}`; }
  function parseJson(text) { try { return JSON.parse(String(text || "")); } catch { return null; } }
  function elapsed(started) { return Math.max(0, Math.round((performance.now?.() ?? Date.now()) - started)); }
  function executionError(error, requestExecuted) { error.request_executed = requestExecuted; error.automatic_retry = false; return error; }

  async function getMetrikaPolicy() {
    const raw = (await chrome.storage.local.get(METRIKA_POLICY_KEY))[METRIKA_POLICY_KEY] || {};
    return Policy.normalizeMetrikaPolicy(raw);
  }

  async function saveMetrikaPolicy(raw) {
    const normalized = Policy.normalizeMetrikaPolicy(raw || {});
    await chrome.storage.local.set({ [METRIKA_POLICY_KEY]: normalized });
    return normalized;
  }

  async function executeMetrika(command, metadata = {}) {
    let normalized;
    try { normalized = Metrika.normalizeCommand(command); }
    catch (error) { throw executionError(error, false); }
    const settings = await Credentials.settings();
    const record = settings.credentials.metrika || {};
    const oauthToken = trim(record.oauth_token);
    if (!oauthToken) throw Object.assign(new Error("OAuth token Metrika не сохранён в расширении."), { code: "METRIKA_OAUTH_MISSING", request_executed: false, automatic_retry: false });
    let req;
    try { req = Metrika.buildRequest(normalized); }
    catch (error) { throw executionError(error, false); }
    const requestId = metadata.request_id || id("metrika");
    const started = performance.now?.() ?? Date.now();
    let response;
    try {
      response = await fetch(req.url, { method: "GET", headers: { Accept: "application/json", Authorization: `OAuth ${oauthToken}` } });
    } catch (error) {
      throw executionError(Object.assign(new Error("Исход Yandex Metrika request неизвестен; автоматический повтор запрещён."), { code: "REQUEST_OUTCOME_UNKNOWN_NO_RETRY", cause: error }), "UNKNOWN");
    }
    let responseText = "";
    try { responseText = await response.text(); } catch { responseText = ""; }
    const parsed = parseJson(responseText);
    if (!response.ok) {
      const payload = Metrika.safeErrorPayload(response.status, responseText, parsed);
      const envelope = Metrika.buildResultEnvelope({
        requestId, command: normalized, httpStatus: response.status, elapsedMs: elapsed(started), result: { error: payload },
        metadata: { ...metadata, status: "ERROR", reason: payload.code, request_executed: true, automatic_retry: false }
      });
      return { ok: false, http_status: response.status, request_id: requestId, report_envelope: envelope, report_text: Metrika.formatResultEnvelope(envelope) };
    }
    let result;
    try { result = Metrika.normalizeProviderResult(normalized, parsed); }
    catch (error) { throw executionError(error, true); }
    const envelope = Metrika.buildResultEnvelope({
      requestId, command: normalized, httpStatus: response.status, elapsedMs: elapsed(started), result,
      metadata: { ...metadata, status: "OK", reason: null, request_executed: true, automatic_retry: false }
    });
    return { ok: true, http_status: response.status, request_id: requestId, report_envelope: envelope, report_text: Metrika.formatResultEnvelope(envelope) };
  }

  async function execute(service, command, metadata = {}) {
    if (service === Registry.SERVICES.METRIKA) return executeMetrika(command, metadata);
    return Base.execute(service, command, metadata);
  }

  function checkStateFromHttp(status) {
    if (Number(status) === 401) return "INVALID_OR_EXPIRED";
    if (Number(status) === 403) return "NO_ACCESS";
    if (Number(status) === 420 || Number(status) === 429) return "QUOTA";
    return "NOT_CHECKED";
  }

  async function checkMetrika(oauthToken = "") {
    const current = await Credentials.load();
    const token = trim(oauthToken) || trim(current.metrika?.oauth_token);
    if (!token) throw Object.assign(new Error("Сначала сохраните OAuth token Metrika."), { code: "METRIKA_OAUTH_MISSING", request_executed: false, automatic_retry: false });
    let response;
    try {
      response = await fetch(`${Metrika.MANAGEMENT_BASE_URL}/counters?per_page=1`, { method: "GET", headers: { Accept: "application/json", Authorization: `OAuth ${token}` } });
    } catch (error) {
      await Credentials.save("metrika", { oauth_token: token, checked_at: nowIso(), check_state: "NETWORK_ERROR" });
      throw executionError(Object.assign(new Error("Не удалось проверить Metrika OAuth: сетевой исход неизвестен."), { code: "METRIKA_CHECK_NETWORK_ERROR", cause: error }), "UNKNOWN");
    }
    let responseText = "";
    try { responseText = await response.text(); } catch { responseText = ""; }
    const parsed = parseJson(responseText);
    if (!response.ok) {
      const state = checkStateFromHttp(response.status);
      await Credentials.save("metrika", { oauth_token: token, checked_at: nowIso(), check_state: state });
      const payload = Metrika.safeErrorPayload(response.status, responseText, parsed);
      return { ok: false, state, http_status: response.status, code: payload.code, error: payload.message, request_executed: true, automatic_retry: false };
    }
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed) || !Array.isArray(parsed.counters)) {
      await Credentials.save("metrika", { oauth_token: token, checked_at: nowIso(), check_state: "NOT_CHECKED" });
      throw Object.assign(new Error("Metrika Check получил неожиданный JSON-ответ."), { code: "INVALID_METRIKA_RESPONSE", request_executed: true, automatic_retry: false });
    }
    await Credentials.save("metrika", { oauth_token: token, checked_at: nowIso(), check_state: "PRESENT" });
    return { ok: true, state: "PRESENT", http_status: response.status, counters_seen: parsed.counters.length, request_executed: true, automatic_retry: false };
  }

  globalThis.YMBPhase4ProviderRuntime = Object.freeze({
    execute,
    executeMetrika,
    checkMetrika,
    getMetrikaPolicy,
    saveMetrikaPolicy,
    executeWebmaster: Base.executeWebmaster,
    executeCloud: Base.executeCloud,
    checkCloud: Base.checkCloud,
    checkWebmaster: Base.checkWebmaster,
    getWebmasterPolicy: Base.getWebmasterPolicy,
    saveWebmasterPolicy: Base.saveWebmasterPolicy
  });
})();
