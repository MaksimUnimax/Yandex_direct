(() => {
  "use strict";

  const Credentials = globalThis.YMBCredentialRuntime;
  const Direct = globalThis.DirectProtocol;
  const Base = globalThis.YMBPhase4ProviderRuntime;
  const Policy = globalThis.YMBPolicyModel;
  const Registry = globalThis.YMBServiceRegistry;
  if (!Credentials || !Direct || !Base || !Policy || !Registry) throw new Error("Phase 5 provider prerequisites are unavailable.");

  const DIRECT_POLICY_KEY = "ymb_direct_policy";
  function trim(value) { return String(value ?? "").trim(); }
  function nowIso() { return new Date().toISOString(); }
  function id(prefix) { return `${prefix}-${crypto.randomUUID()}`; }
  function parseJson(text) { try { return JSON.parse(String(text || "")); } catch { return null; } }
  function elapsed(started) { return Math.max(0, Math.round((performance.now?.() ?? Date.now()) - started)); }
  function executionError(error, requestExecuted) { error.request_executed = requestExecuted; error.automatic_retry = false; return error; }

  async function getDirectPolicy() {
    const raw = (await chrome.storage.local.get(DIRECT_POLICY_KEY))[DIRECT_POLICY_KEY] || {};
    return Policy.normalizeDirectPolicy(raw);
  }

  async function saveDirectPolicy(raw) {
    const normalized = Policy.normalizeDirectPolicy(raw || {});
    await chrome.storage.local.set({ [DIRECT_POLICY_KEY]: normalized });
    return normalized;
  }

  function requestHeaders(oauthToken, clientLogin, { report = false } = {}) {
    const headers = {
      Authorization: `Bearer ${oauthToken}`,
      "Accept-Language": "ru",
      "Content-Type": "application/json; charset=utf-8"
    };
    if (clientLogin) headers["Client-Login"] = clientLogin;
    if (report) {
      headers.processingMode = "online";
      headers.skipReportHeader = "true";
      headers.skipReportSummary = "true";
    }
    return headers;
  }

  function errorReturn({ response, responseText, parsed, requestId, command, started, metadata, providerMetadata, reasonOverride = null }) {
    const payload = Direct.safeErrorPayload(response?.status, responseText, parsed);
    const reason = reasonOverride || payload.code;
    const envelope = Direct.buildResultEnvelope({
      requestId,
      command,
      httpStatus: Number(response?.status || 0),
      elapsedMs: elapsed(started),
      result: { error: { ...payload, ...(reasonOverride ? { code: reasonOverride } : {}) } },
      metadata: {
        ...metadata,
        status: "ERROR",
        reason,
        provider_request_id: providerMetadata?.provider_request_id || payload.provider_request_id || null,
        provider_units: providerMetadata?.provider_units || null,
        request_executed: true,
        automatic_retry: false
      }
    });
    return {
      ok: false,
      http_status: Number(response?.status || 0),
      request_id: requestId,
      report_envelope: envelope,
      report_text: Direct.formatResultEnvelope(envelope)
    };
  }

  async function executeDirect(command, metadata = {}) {
    let normalized;
    try { normalized = Direct.normalizeCommand(command); }
    catch (error) { throw executionError(error, false); }

    const settings = await Credentials.settings();
    const record = settings.credentials.direct || {};
    const oauthToken = trim(record.oauth_token);
    const clientLogin = trim(record.client_login);
    if (!oauthToken) throw Object.assign(new Error("OAuth token Direct не сохранён в расширении."), { code: "DIRECT_OAUTH_MISSING", request_executed: false, automatic_retry: false });

    const requestId = metadata.request_id || id("direct");
    let req;
    try { req = Direct.buildRequest(normalized, { reportName: `YMB-P5-${requestId}` }); }
    catch (error) { throw executionError(error, false); }

    const started = performance.now?.() ?? Date.now();
    let response;
    try {
      response = await fetch(req.url, {
        method: "POST",
        headers: requestHeaders(oauthToken, clientLogin, { report: req.kind === "report" }),
        body: JSON.stringify(req.body)
      });
    } catch (error) {
      throw executionError(Object.assign(new Error("Исход Yandex Direct request неизвестен; автоматический повтор запрещён."), { code: "REQUEST_OUTCOME_UNKNOWN_NO_RETRY", cause: error }), "UNKNOWN");
    }

    let responseText = "";
    try { responseText = await response.text(); } catch { responseText = ""; }
    const parsed = parseJson(responseText);
    const providerMetadata = Direct.responseMetadata(response.headers, parsed);

    if (req.kind === "report" && (Number(response.status) === 201 || Number(response.status) === 202)) {
      return errorReturn({ response, responseText, parsed, requestId, command: normalized, started, metadata, providerMetadata, reasonOverride: "REPORT_ASYNC_NOT_ALLOWED" });
    }

    if (Direct.providerError(parsed) || !response.ok) {
      return errorReturn({ response, responseText, parsed, requestId, command: normalized, started, metadata, providerMetadata });
    }

    let result;
    try {
      result = req.kind === "report"
        ? Direct.normalizeReportResult(normalized, responseText)
        : Direct.normalizeJsonProviderResult(normalized, parsed);
    } catch (error) {
      throw executionError(error, true);
    }

    const envelope = Direct.buildResultEnvelope({
      requestId,
      command: normalized,
      httpStatus: response.status,
      elapsedMs: elapsed(started),
      result,
      metadata: {
        ...metadata,
        status: "OK",
        reason: null,
        provider_request_id: providerMetadata.provider_request_id,
        provider_units: providerMetadata.provider_units,
        request_executed: true,
        automatic_retry: false
      }
    });
    return { ok: true, http_status: response.status, request_id: requestId, report_envelope: envelope, report_text: Direct.formatResultEnvelope(envelope) };
  }

  async function execute(service, command, metadata = {}) {
    if (service === Registry.SERVICES.DIRECT) return executeDirect(command, metadata);
    return Base.execute(service, command, metadata);
  }

  async function checkDirect(oauthToken = "", clientLoginOverride) {
    const current = await Credentials.load();
    const token = trim(oauthToken) || trim(current.direct?.oauth_token);
    const clientLogin = clientLoginOverride === undefined ? trim(current.direct?.client_login) : trim(clientLoginOverride);
    if (!token) throw Object.assign(new Error("Сначала сохраните OAuth token Direct."), { code: "DIRECT_OAUTH_MISSING", request_executed: false, automatic_retry: false });

    const url = `${Direct.BASE_URL}/campaigns`;
    const body = {
      method: "get",
      params: {
        SelectionCriteria: {},
        FieldNames: ["Id"],
        Page: { Limit: 1, Offset: 0 }
      }
    };

    let response;
    try {
      response = await fetch(url, { method: "POST", headers: requestHeaders(token, clientLogin), body: JSON.stringify(body) });
    } catch (error) {
      await Credentials.save("direct", { oauth_token: token, client_login: clientLogin, checked_at: nowIso(), check_state: "NETWORK_ERROR" });
      throw executionError(Object.assign(new Error("Не удалось проверить Direct OAuth: сетевой исход неизвестен."), { code: "DIRECT_CHECK_NETWORK_ERROR", cause: error }), "UNKNOWN");
    }

    let responseText = "";
    try { responseText = await response.text(); } catch { responseText = ""; }
    const parsed = parseJson(responseText);
    const providerMetadata = Direct.responseMetadata(response.headers, parsed);

    if (Direct.providerError(parsed) || !response.ok) {
      const state = Direct.providerError(parsed) ? Direct.checkStateForProviderError(parsed) : "NOT_CHECKED";
      await Credentials.save("direct", { oauth_token: token, client_login: clientLogin, checked_at: nowIso(), check_state: state });
      const payload = Direct.safeErrorPayload(response.status, responseText, parsed);
      return {
        ok: false,
        state,
        http_status: response.status,
        code: payload.code,
        provider_code: payload.provider_code,
        error: payload.message,
        provider_request_id: providerMetadata.provider_request_id || payload.provider_request_id || null,
        provider_units: providerMetadata.provider_units,
        request_executed: true,
        automatic_retry: false
      };
    }

    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed) || !parsed.result || !Array.isArray(parsed.result.Campaigns)) {
      await Credentials.save("direct", { oauth_token: token, client_login: clientLogin, checked_at: nowIso(), check_state: "NOT_CHECKED" });
      throw Object.assign(new Error("Direct Check получил неожиданный JSON-ответ."), { code: "INVALID_DIRECT_RESPONSE", request_executed: true, automatic_retry: false });
    }

    await Credentials.save("direct", { oauth_token: token, client_login: clientLogin, checked_at: nowIso(), check_state: "PRESENT" });
    return {
      ok: true,
      state: "PRESENT",
      http_status: response.status,
      campaigns_seen: parsed.result.Campaigns.length,
      provider_request_id: providerMetadata.provider_request_id,
      provider_units: providerMetadata.provider_units,
      request_executed: true,
      automatic_retry: false
    };
  }

  globalThis.YMBPhase5ProviderRuntime = Object.freeze({
    execute,
    executeDirect,
    checkDirect,
    getDirectPolicy,
    saveDirectPolicy,
    executeMetrika: Base.executeMetrika,
    checkMetrika: Base.checkMetrika,
    getMetrikaPolicy: Base.getMetrikaPolicy,
    saveMetrikaPolicy: Base.saveMetrikaPolicy,
    executeWebmaster: Base.executeWebmaster,
    executeCloud: Base.executeCloud,
    checkCloud: Base.checkCloud,
    checkWebmaster: Base.checkWebmaster,
    getWebmasterPolicy: Base.getWebmasterPolicy,
    saveWebmasterPolicy: Base.saveWebmasterPolicy
  });
})();
