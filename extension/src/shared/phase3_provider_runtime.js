(() => {
  "use strict";

  const Credentials = globalThis.YMBCredentialRuntime;
  const Webmaster = globalThis.WebmasterProtocol;
  const ExportModel = globalThis.YMBWebmasterExportModel;
  const Registry = globalThis.YMBServiceRegistry;
  const Policy = globalThis.YMBPolicyModel;
  const Wordstat = globalThis.WordstatProtocol;
  const Search = globalThis.SearchProtocol;
  if (!Credentials || !Webmaster || !ExportModel || !Registry || !Policy || !Wordstat || !Search) throw new Error("Phase 3 provider prerequisites are unavailable.");

  const WEBMASTER_POLICY_KEY = "ymb_webmaster_policy";
  function trim(value) { return String(value ?? "").trim(); }
  function nowIso() { return new Date().toISOString(); }
  function id(prefix) { return `${prefix}-${crypto.randomUUID()}`; }
  function parseJson(text) { try { return JSON.parse(String(text || "")); } catch { return null; } }
  function elapsed(started) { return Math.max(0, Math.round((performance.now?.() ?? Date.now()) - started)); }
  function executionError(error, requestExecuted) { error.request_executed = requestExecuted; error.automatic_retry = false; return error; }
  function checkStateFromHttp(status) {
    if (Number(status) === 401) return "INVALID_OR_EXPIRED";
    if (Number(status) === 403) return "NO_ACCESS";
    return "NOT_CHECKED";
  }

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
      try {
        result = normalized.method === "genSearch"
          ? Protocol.parseProviderResponseText(normalized, text)
          : Protocol.normalizeProviderResult(parsed);
      }
      catch (error) { throw executionError(error, true); }
    }
    const envelope = Protocol.buildResultEnvelope({ requestId, command: normalized, httpStatus: response.status, elapsedMs: elapsed(started), result, metadata: { ...metadata, status: "OK", reason: null, request_executed: true, automatic_retry: false } });
    return { ok: true, http_status: response.status, request_id: requestId, report_envelope: envelope, report_text: Protocol.formatResultEnvelope(envelope) };
  }

  function webmasterEnvelope({ normalized, requestId, result, metadata = {}, httpStatus = 0, elapsedMs = 0, requestExecuted = false }) {
    const envelope = Webmaster.buildResultEnvelope({
      requestId,
      command: normalized,
      httpStatus,
      elapsedMs,
      result,
      metadata: {
        ...metadata,
        status: "OK",
        reason: null,
        request_executed: requestExecuted,
        automatic_retry: false
      }
    });
    return { ok: true, http_status: httpStatus, request_id: requestId, report_envelope: envelope, report_text: Webmaster.formatResultEnvelope(envelope) };
  }

  async function executeLocalWebmaster(normalized, metadata = {}) {
    const requestId = metadata.request_id || id("webmaster-local");
    let result;
    if (normalized.method === "projectQueryUrlExport") result = { projection: ExportModel.projectExport(normalized) };
    else if (normalized.method === "getQueryUrlExportManifest") result = { manifest: await ExportModel.getManifest(normalized.taskId) };
    else if (normalized.method === "readQueryUrlExportChunk") result = await ExportModel.readChunk(normalized.taskId, normalized.offset, normalized.limit);
    else if (normalized.method === "listQueryUrlExportJobs") result = { jobs: await ExportModel.listJobs({ pendingOnly: normalized.pendingOnly }) };
    else throw Object.assign(new Error(`Локальный Webmaster метод ${normalized.method} не реализован.`), { code: "UNSUPPORTED_LOCAL_METHOD", request_executed: false, automatic_retry: false });
    return webmasterEnvelope({ normalized, requestId, result, metadata, requestExecuted: false });
  }

  async function executeWebmasterDownload(normalized, metadata = {}) {
    const requestId = metadata.request_id || id("webmaster-download");
    const target = await ExportModel.downloadTarget(normalized.taskId);
    if (target.host_id && target.host_id !== normalized.hostId) {
      throw Object.assign(new Error("Export task связан с другим hostId."), { code: "WEBMASTER_EXPORT_HOST_MISMATCH", request_executed: false, automatic_retry: false });
    }
    const started = performance.now?.() ?? Date.now();
    let response;
    try {
      response = await fetch(target.url, { method: "GET", headers: { Accept: "text/csv,text/plain;q=0.9,*/*;q=0.1" }, redirect: "error" });
    } catch (error) {
      throw executionError(Object.assign(new Error("Исход скачивания Webmaster export неизвестен; автоматический повтор запрещён."), { code: "REQUEST_OUTCOME_UNKNOWN_NO_RETRY", cause: error }), "UNKNOWN");
    }
    let rawText = "";
    try { rawText = await response.text(); } catch { rawText = ""; }
    if (!response.ok) {
      const payload = Webmaster.safeErrorPayload(response.status, rawText, null);
      const envelope = Webmaster.buildResultEnvelope({ requestId, command: normalized, httpStatus: response.status, elapsedMs: elapsed(started), result: { error: payload }, metadata: { ...metadata, status: "ERROR", reason: payload.code, request_executed: true, automatic_retry: false } });
      return { ok: false, http_status: response.status, request_id: requestId, report_envelope: envelope, report_text: Webmaster.formatResultEnvelope(envelope) };
    }
    let manifest;
    try { manifest = await ExportModel.recordCollected(normalized.taskId, rawText); }
    catch (error) { throw executionError(error, true); }
    const preview = await ExportModel.readChunk(normalized.taskId, 0, 25);
    return webmasterEnvelope({ normalized, requestId, httpStatus: response.status, elapsedMs: elapsed(started), requestExecuted: true, metadata, result: { manifest, preview } });
  }

  async function executeWebmaster(command, metadata = {}) {
    let normalized;
    try { normalized = Webmaster.normalizeCommand(command); }
    catch (error) { throw executionError(error, false); }

    if (Webmaster.isLocalMethod(normalized.method)) return executeLocalWebmaster(normalized, metadata);
    if (Webmaster.isDownloadMethod(normalized.method)) return executeWebmasterDownload(normalized, metadata);

    const settings = await Credentials.settings();
    const record = settings.credentials.webmaster || {};
    const oauthToken = trim(record.oauth_token);
    const userId = trim(record.user_id);
    if (!oauthToken) throw Object.assign(new Error("OAuth token Webmaster не сохранён в расширении."), { code: "WEBMASTER_OAUTH_MISSING", request_executed: false, automatic_retry: false });
    if (!/^\d+$/.test(userId)) throw Object.assign(new Error("Webmaster user_id не подтверждён. Выполните Check."), { code: "WEBMASTER_USER_ID_MISSING", request_executed: false, automatic_retry: false });

    let req;
    try { req = Webmaster.buildRequest(normalized, userId); }
    catch (error) { throw executionError(error, false); }
    const requestId = metadata.request_id || id("webmaster");
    const started = performance.now?.() ?? Date.now();
    let response;
    const headers = { Accept: "application/json", Authorization: `OAuth ${oauthToken}` };
    if (req.body !== undefined) headers["Content-Type"] = "application/json";
    try {
      response = await fetch(req.url, { method: req.method || "GET", headers, body: req.body === undefined ? undefined : JSON.stringify(req.body) });
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
    try {
      result = Webmaster.normalizeProviderResult(normalized, parsed);
      if (normalized.method === "startQueryUrlExport") {
        const manifest = await ExportModel.recordStart(normalized, result, requestId);
        result = { ...result, manifest };
      } else if (normalized.method === "getQueryUrlExportStatus") {
        const manifest = await ExportModel.recordStatus(normalized, parsed);
        result = { ...result, manifest };
      }
    } catch (error) { throw executionError(error, true); }
    return webmasterEnvelope({ normalized, requestId, httpStatus: response.status, elapsedMs: elapsed(started), requestExecuted: true, metadata, result });
  }

  async function execute(service, command, metadata = {}) {
    if (service === Registry.SERVICES.WEBMASTER) return executeWebmaster(command, metadata);
    if (service === Registry.SERVICES.SEARCH || service === Registry.SERVICES.WORDSTAT) return executeCloud(service, command, metadata);
    throw Object.assign(new Error("Сервис не поддерживается."), { code: "SERVICE_NOT_AVAILABLE" });
  }

  async function checkCloud(service, { confirmBillable = false } = {}) {
    if (![Registry.SERVICES.WORDSTAT, Registry.SERVICES.SEARCH].includes(service)) {
      throw Object.assign(new Error("Cloud credential Check поддерживает только Wordstat/Search."), { code: "UNKNOWN_SERVICE", request_executed: false, automatic_retry: false });
    }
    const settings = await Credentials.settings();
    const record = settings.credentials[service] || {};
    if (!trim(record.api_key)) throw Object.assign(new Error(`Сначала сохраните API key ${service}.`), { code: "API_KEY_MISSING", request_executed: false, automatic_retry: false });
    if (!trim(record.folder_id)) throw Object.assign(new Error(`Сначала сохраните folderId ${service}.`), { code: "FOLDER_ID_MISSING", request_executed: false, automatic_retry: false });
    if (service === Registry.SERVICES.SEARCH && confirmBillable !== true) {
      throw Object.assign(new Error("Search Check требует явного подтверждения одного платного запроса."), { code: "SEARCH_CHECK_CONFIRM_REQUIRED", request_executed: false, automatic_retry: false });
    }

    const command = service === Registry.SERVICES.WORDSTAT
      ? { method: "getRegionsTree" }
      : { method: "search", queryText: "yandex", groupsOnPage: 1 };
    try {
      const result = await executeCloud(service, command, { channel: "credential_check" });
      const state = result.ok ? "PRESENT" : checkStateFromHttp(result.http_status);
      await Credentials.save(service, { checked_at: nowIso(), check_state: state });
      return {
        ok: result.ok, service, state, http_status: result.http_status, request_executed: true, automatic_retry: false,
        billable_request_confirmed: service === Registry.SERVICES.SEARCH
      };
    } catch (error) {
      if (error?.request_executed === "UNKNOWN") await Credentials.save(service, { checked_at: nowIso(), check_state: "NETWORK_ERROR" });
      throw error;
    }
  }

  async function checkWebmaster(oauthToken = "") {
    const current = await Credentials.load();
    const token = trim(oauthToken) || trim(current.webmaster?.oauth_token);
    if (!token) throw Object.assign(new Error("Сначала сохраните OAuth token Webmaster."), { code: "WEBMASTER_OAUTH_MISSING", request_executed: false, automatic_retry: false });
    let response;
    try {
      response = await fetch(`${Webmaster.BASE_URL}/user`, { method: "GET", headers: { Accept: "application/json", Authorization: `OAuth ${token}` } });
    } catch (error) {
      await Credentials.save("webmaster", { oauth_token: token, user_id: "", verified_at: null, check_state: "NETWORK_ERROR" });
      throw executionError(Object.assign(new Error("Не удалось проверить Webmaster OAuth: сетевой исход неизвестен."), { code: "WEBMASTER_CHECK_NETWORK_ERROR", cause: error }), "UNKNOWN");
    }
    let text = "";
    try { text = await response.text(); } catch { text = ""; }
    const parsed = parseJson(text);
    if (!response.ok) {
      const state = response.status === 403 ? "NO_ACCESS" : response.status === 401 ? "INVALID_OR_EXPIRED" : "NOT_CHECKED";
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
    getWebmasterPolicy, saveWebmasterPolicy, execute, executeWebmaster, executeCloud, checkCloud, checkWebmaster
  });
})();
