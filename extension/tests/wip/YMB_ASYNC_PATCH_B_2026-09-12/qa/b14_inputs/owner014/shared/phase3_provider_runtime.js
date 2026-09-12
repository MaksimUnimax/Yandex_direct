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
  const WEBMASTER_EXPORT_JOBS_KEY = "ymb_webmaster_query_url_exports_v1";
  const SAFE_DOWNLOAD_HOST = "storage.mds.yandex.net";
  const SAFE_DOWNLOAD_PATH_PREFIX = "/get-webmaster-download/";

  function trim(value) { return String(value ?? "").trim(); }
  function nowIso() { return new Date().toISOString(); }
  function id(prefix) { return `${prefix}-${crypto.randomUUID()}`; }
  function clone(value) { return value == null ? value : JSON.parse(JSON.stringify(value)); }
  function parseJson(text) { try { return JSON.parse(String(text || "")); } catch { return null; } }
  function elapsed(started) { return Math.max(0, Math.round((performance.now?.() ?? Date.now()) - started)); }
  function executionError(error, requestExecuted) { error.request_executed = requestExecuted; error.automatic_retry = false; return error; }
  function checkStateFromHttp(status) { if (Number(status) === 401) return "INVALID_OR_EXPIRED"; if (Number(status) === 403) return "NO_ACCESS"; return "NOT_CHECKED"; }

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
      response = await fetch(req.url, { method: isSearch ? "POST" : (req.method || "POST"), headers: { "Content-Type": "application/json", Authorization: `Api-Key ${apiKey}` }, body: isSearch ? JSON.stringify(req.body) : (req.body == null ? undefined : JSON.stringify(req.body)) });
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
      return { ok: false, http_status: response.status, request_id: requestId, request_executed: true, automatic_retry: false, report_envelope: envelope, report_text: Protocol.formatResultEnvelope(envelope) };
    }
    let result = parsed;
    if (isSearch) {
      try { result = normalized.method === "genSearch" ? Protocol.parseProviderResponseText(normalized, text) : Protocol.normalizeProviderResult(parsed); }
      catch (error) { throw executionError(error, true); }
    }
    const envelope = Protocol.buildResultEnvelope({ requestId, command: normalized, httpStatus: response.status, elapsedMs: elapsed(started), result, metadata: { ...metadata, status: "OK", reason: null, request_executed: true, automatic_retry: false } });
    return { ok: true, http_status: response.status, request_id: requestId, request_executed: true, automatic_retry: false, report_envelope: envelope, report_text: Protocol.formatResultEnvelope(envelope) };
  }

  async function loadExportJobs() {
    const raw = (await chrome.storage.local.get(WEBMASTER_EXPORT_JOBS_KEY))[WEBMASTER_EXPORT_JOBS_KEY];
    return raw && typeof raw === "object" && !Array.isArray(raw) ? clone(raw) : {};
  }

  async function saveExportJobs(map) {
    await chrome.storage.local.set({ [WEBMASTER_EXPORT_JOBS_KEY]: clone(map) });
    return map;
  }

  async function loadExportJob(taskId, { required = true } = {}) {
    const map = await loadExportJobs();
    const job = map[String(taskId || "")] || null;
    if (!job && required) throw Object.assign(new Error(`Webmaster export task не найден в локальном durable storage: ${taskId}`), { code: "WEBMASTER_EXPORT_JOB_NOT_FOUND", request_executed: false, automatic_retry: false });
    return { map, job: clone(job) };
  }

  async function persistExportJob(map, job) {
    map[job.task_id] = clone(job);
    await saveExportJobs(map);
    return clone(job);
  }

  function publicExportManifest(job) {
    if (!job) return null;
    const csvSha256 = job.csv_sha256 || job.raw_sha256 || null;
    const csvBytes = Number(job.csv_bytes ?? job.raw_bytes ?? 0);
    return {
      task_id: job.task_id,
      host_id: job.host_id,
      download_status: job.download_status || "SUBMITTED",
      created_at: job.created_at || null,
      updated_at: job.updated_at || null,
      collected_at: job.collected_at || null,
      projection: clone(job.projection || null),
      quota: clone(job.quota || null),
      row_count: Number(job.row_count || 0),
      columns: Array.isArray(job.columns) ? [...job.columns] : [],
      downloaded_sha256: job.downloaded_sha256 || null,
      downloaded_bytes: Number(job.downloaded_bytes || 0),
      compression: job.compression || null,
      csv_sha256: csvSha256,
      csv_bytes: csvBytes,
      raw_sha256: csvSha256,
      raw_bytes: csvBytes,
      parse_warning: job.parse_warning || null,
      download_url_available: Boolean(job.download_url)
    };
  }

  function safeDownloadUrl(value) {
    let url;
    try { url = new URL(String(value || "")); }
    catch { throw Object.assign(new Error("Webmaster export status вернул некорректный download URL."), { code: "WEBMASTER_EXPORT_UNSAFE_DOWNLOAD_URL", request_executed: true, automatic_retry: false }); }
    if (url.protocol !== "https:" || url.hostname !== SAFE_DOWNLOAD_HOST || !url.pathname.startsWith(SAFE_DOWNLOAD_PATH_PREFIX) || url.username || url.password) {
      throw Object.assign(new Error("Webmaster export download URL не прошёл allowlist storage.mds.yandex.net."), { code: "WEBMASTER_EXPORT_UNSAFE_DOWNLOAD_URL", request_executed: true, automatic_retry: false });
    }
    return url.href;
  }

  async function sha256Bytes(bytes) {
    const source = bytes instanceof Uint8Array ? bytes : new Uint8Array(bytes || 0);
    const digest = await crypto.subtle.digest("SHA-256", source);
    return Array.from(new Uint8Array(digest)).map((item) => item.toString(16).padStart(2, "0")).join("");
  }

  function isGzipBytes(bytes) {
    return bytes instanceof Uint8Array && bytes.length >= 2 && bytes[0] === 0x1f && bytes[1] === 0x8b;
  }

  async function readResponseBytes(response) {
    if (typeof response?.arrayBuffer === "function") return new Uint8Array(await response.arrayBuffer());
    let text = "";
    try { text = await response.text(); } catch { text = ""; }
    return new TextEncoder().encode(text);
  }

  function decodeUtf8(bytes, { fatal = true } = {}) {
    try { return new TextDecoder("utf-8", { fatal }).decode(bytes); }
    catch (error) {
      throw executionError(Object.assign(new Error("Webmaster export содержит некорректный UTF-8 после распаковки."), { code: "WEBMASTER_EXPORT_INVALID_UTF8", cause: error }), true);
    }
  }

  async function gunzipBytes(bytes) {
    if (typeof globalThis.DecompressionStream !== "function" || typeof globalThis.Response !== "function") {
      throw executionError(Object.assign(new Error("Среда расширения не поддерживает безопасную локальную gzip-распаковку Webmaster export."), { code: "WEBMASTER_EXPORT_GZIP_DECOMPRESSION_FAILED" }), true);
    }
    try {
      const source = new globalThis.Response(bytes);
      if (!source.body) throw new Error("gzip source stream is unavailable");
      const stream = source.body.pipeThrough(new globalThis.DecompressionStream("gzip"));
      const buffer = await new globalThis.Response(stream).arrayBuffer();
      return new Uint8Array(buffer);
    } catch (error) {
      if (error?.code === "WEBMASTER_EXPORT_GZIP_DECOMPRESSION_FAILED") throw error;
      throw executionError(Object.assign(new Error("Не удалось распаковать gzip Webmaster export."), { code: "WEBMASTER_EXPORT_GZIP_DECOMPRESSION_FAILED", cause: error }), true);
    }
  }

  function delimiterScore(text, delimiter) {
    let score = 0; let quoted = false;
    for (let index = 0; index < text.length; index += 1) {
      const ch = text[index];
      if (ch === '"') {
        if (quoted && text[index + 1] === '"') { index += 1; continue; }
        quoted = !quoted; continue;
      }
      if (!quoted && (ch === "\n" || ch === "\r")) break;
      if (!quoted && ch === delimiter) score += 1;
    }
    return score;
  }

  function detectCsvDelimiter(text) {
    const candidates = [",", ";", "\t"];
    return candidates.map((delimiter) => ({ delimiter, score: delimiterScore(text, delimiter) })).sort((a, b) => b.score - a.score)[0]?.delimiter || ",";
  }

  function parseCsv(text, delimiter) {
    const rows = []; let row = []; let cell = ""; let quoted = false;
    const source = String(text || "").replace(/^\uFEFF/, "");
    for (let index = 0; index < source.length; index += 1) {
      const ch = source[index];
      if (quoted) {
        if (ch === '"' && source[index + 1] === '"') { cell += '"'; index += 1; }
        else if (ch === '"') quoted = false;
        else cell += ch;
        continue;
      }
      if (ch === '"') { quoted = true; continue; }
      if (ch === delimiter) { row.push(cell); cell = ""; continue; }
      if (ch === "\r") { if (source[index + 1] === "\n") index += 1; row.push(cell); rows.push(row); row = []; cell = ""; continue; }
      if (ch === "\n") { row.push(cell); rows.push(row); row = []; cell = ""; continue; }
      cell += ch;
    }
    if (quoted) throw Object.assign(new Error("CSV выгрузки содержит незакрытое quoted field."), { code: "WEBMASTER_EXPORT_INVALID_CSV", request_executed: true, automatic_retry: false });
    if (cell.length || row.length) { row.push(cell); rows.push(row); }
    return rows.filter((cells) => cells.some((value) => String(value).length));
  }

  function canonicalHeader(value) {
    return String(value || "").replace(/^\uFEFF/, "").trim().toLowerCase().replace(/[\s_\-]+/g, " ");
  }

  const HEADER_ALIASES = Object.freeze({
    date: new Set(["date", "дата"]),
    host: new Set(["host", "хост"]),
    url: new Set(["url", "адрес", "страница", "url страницы"]),
    query: new Set(["query", "запрос", "поисковый запрос"]),
    region: new Set(["region", "регион"]),
    clicks: new Set(["clicks", "клики"]),
    impressions: new Set(["impressions", "shows", "показы"]),
    position: new Set(["position", "позиция"])
  });

  function columnMap(headers) {
    const map = {};
    headers.forEach((header, index) => {
      const value = canonicalHeader(header);
      for (const [field, aliases] of Object.entries(HEADER_ALIASES)) if (aliases.has(value) && map[field] === undefined) map[field] = index;
    });
    return map;
  }

  function numberOrNull(value) {
    const text = String(value ?? "").trim();
    if (!text) return null;
    const normalized = /^-?\d+,\d+$/.test(text) ? text.replace(",", ".") : text;
    const number = Number(normalized);
    return Number.isFinite(number) ? number : null;
  }

  function normalizeExportCsv(text) {
    const delimiter = detectCsvDelimiter(text);
    const table = parseCsv(text, delimiter);
    if (!table.length) return { columns: [], rows: [], delimiter, warning: "EMPTY_REPORT" };
    const columns = table[0].map((value) => String(value || "").trim());
    const mapping = columnMap(columns);
    const required = ["date", "host", "url", "query", "region", "clicks", "impressions", "position"];
    const missing = required.filter((field) => mapping[field] === undefined);
    if (missing.length) return { columns, rows: [], delimiter, warning: `UNRECOGNIZED_HEADER_MISSING:${missing.join(",")}` };
    const rows = table.slice(1).map((cells) => ({
      date: String(cells[mapping.date] ?? ""),
      host: String(cells[mapping.host] ?? ""),
      url: String(cells[mapping.url] ?? ""),
      query: String(cells[mapping.query] ?? ""),
      region: String(cells[mapping.region] ?? ""),
      clicks: numberOrNull(cells[mapping.clicks]),
      impressions: numberOrNull(cells[mapping.impressions]),
      position: numberOrNull(cells[mapping.position])
    }));
    return { columns, rows, delimiter, warning: null };
  }

  function buildWebmasterReturn({ normalized, metadata, requestId, httpStatus = 0, started, result, ok = true, status = null, reason = null, requestExecuted = false }) {
    const envelope = Webmaster.buildResultEnvelope({ requestId, command: normalized, httpStatus, elapsedMs: started == null ? 0 : elapsed(started), result, metadata: { ...metadata, status: status || (ok ? "OK" : "ERROR"), reason, request_executed: requestExecuted, automatic_retry: false } });
    return { ok, http_status: httpStatus, request_id: requestId, request_executed: requestExecuted, automatic_retry: false, report_envelope: envelope, report_text: Webmaster.formatResultEnvelope(envelope) };
  }

  async function executeLocalExportCommand(normalized, metadata = {}) {
    const requestId = metadata.request_id || id("webmaster-local");
    const { job } = await loadExportJob(normalized.taskId);
    if (!Array.isArray(job.rows)) throw Object.assign(new Error("Webmaster export ещё не собран локально. Сначала выполните collectQueryUrlExport."), { code: "WEBMASTER_EXPORT_NOT_COLLECTED", request_executed: false, automatic_retry: false });
    const rows = job.rows.slice(normalized.offset, normalized.offset + normalized.limit);
    return buildWebmasterReturn({ normalized, metadata, requestId, result: { manifest: publicExportManifest(job), chunk: { offset: normalized.offset, limit: normalized.limit, returned: rows.length, total: job.rows.length, has_more: normalized.offset + rows.length < job.rows.length, rows } }, requestExecuted: false });
  }

  async function executeExportDownload(normalized, metadata = {}) {
    const requestId = metadata.request_id || id("webmaster-download");
    const loaded = await loadExportJob(normalized.taskId);
    const map = loaded.map; const job = loaded.job;
    if (String(job.host_id || "") !== normalized.hostId) throw Object.assign(new Error("hostId не совпадает с durable export job."), { code: "WEBMASTER_EXPORT_HOST_MISMATCH", request_executed: false, automatic_retry: false });
    if (job.download_status !== "SUCCESS" || !job.download_url) {
      return buildWebmasterReturn({ normalized, metadata, requestId, result: { manifest: publicExportManifest(job), skipped: true }, ok: true, status: "SKIPPED", reason: "WEBMASTER_EXPORT_NOT_READY", requestExecuted: false });
    }
    const downloadUrl = safeDownloadUrl(job.download_url);
    const started = performance.now?.() ?? Date.now();
    let response;
    try { response = await fetch(downloadUrl, { method: "GET", headers: { Accept: "text/csv,application/gzip,application/octet-stream;q=0.9,text/plain;q=0.8,*/*;q=0.1" } }); }
    catch (error) { throw executionError(Object.assign(new Error("Исход скачивания Webmaster export неизвестен; автоматический повтор запрещён."), { code: "REQUEST_OUTCOME_UNKNOWN_NO_RETRY", cause: error }), "UNKNOWN"); }
    const finalUrl = String(response?.url || downloadUrl);
    safeDownloadUrl(finalUrl);
    let downloadedBytes;
    try { downloadedBytes = await readResponseBytes(response); }
    catch (error) { throw executionError(Object.assign(new Error("Не удалось прочитать байты Webmaster export."), { code: "WEBMASTER_EXPORT_DOWNLOAD_READ_FAILED", cause: error }), true); }
    if (!response.ok) {
      let text = "";
      try { text = decodeUtf8(downloadedBytes, { fatal: false }); } catch { text = ""; }
      const payload = Webmaster.safeErrorPayload(response.status, text, parseJson(text));
      return buildWebmasterReturn({ normalized, metadata, requestId, httpStatus: response.status, started, result: { error: payload, manifest: publicExportManifest(job) }, ok: false, reason: payload.code, requestExecuted: true });
    }

    const downloadedSha256 = await sha256Bytes(downloadedBytes);
    const compression = isGzipBytes(downloadedBytes) ? "GZIP" : "NONE";
    const csvBytes = compression === "GZIP" ? await gunzipBytes(downloadedBytes) : downloadedBytes;
    const text = decodeUtf8(csvBytes, { fatal: true });
    const parsed = normalizeExportCsv(text);
    const csvSha256 = await sha256Bytes(csvBytes);
    const next = {
      ...job,
      downloaded_sha256: downloadedSha256,
      downloaded_bytes: downloadedBytes.byteLength,
      compression,
      csv_sha256: csvSha256,
      csv_bytes: csvBytes.byteLength,
      raw_csv: text,
      rows: parsed.rows,
      columns: parsed.columns,
      delimiter: parsed.delimiter === "\t" ? "TAB" : parsed.delimiter,
      parse_warning: parsed.warning,
      row_count: parsed.rows.length,
      raw_sha256: csvSha256,
      raw_bytes: csvBytes.byteLength,
      collected_at: nowIso(),
      updated_at: nowIso()
    };
    await persistExportJob(map, next);
    const preview = parsed.rows.slice(0, normalized.previewLimit);
    return buildWebmasterReturn({ normalized, metadata, requestId, httpStatus: response.status, started, result: { manifest: publicExportManifest(next), preview: { returned: preview.length, limit: normalized.previewLimit, rows: preview } }, requestExecuted: true });
  }

  async function executeWebmaster(command, metadata = {}) {
    let normalized;
    try { normalized = Webmaster.normalizeCommand(command); } catch (error) { throw executionError(error, false); }
    if (Webmaster.isLocalMethod(normalized.method)) return executeLocalExportCommand(normalized, metadata);
    if (Webmaster.isDownloadMethod(normalized.method)) return executeExportDownload(normalized, metadata);

    const settings = await Credentials.settings();
    const record = settings.credentials.webmaster || {};
    const oauthToken = trim(record.oauth_token);
    const userId = trim(record.user_id);
    if (!oauthToken) throw Object.assign(new Error("OAuth token Webmaster не сохранён в расширении."), { code: "WEBMASTER_OAUTH_MISSING", request_executed: false, automatic_retry: false });
    if (!/^\d+$/.test(userId)) throw Object.assign(new Error("Webmaster user_id не подтверждён. Выполните Check."), { code: "WEBMASTER_USER_ID_MISSING", request_executed: false, automatic_retry: false });
    let req;
    try { req = Webmaster.buildRequest(normalized, userId); } catch (error) { throw executionError(error, false); }
    const requestId = metadata.request_id || id("webmaster");
    const started = performance.now?.() ?? Date.now();
    const headers = { Accept: "application/json", Authorization: `OAuth ${oauthToken}` };
    if (req.method === "POST") headers["Content-Type"] = "application/json";
    let response;
    try { response = await fetch(req.url, { method: req.method || "GET", headers, body: req.body == null ? undefined : JSON.stringify(req.body) }); }
    catch (error) { throw executionError(Object.assign(new Error("Исход Yandex Webmaster request неизвестен; автоматический повтор запрещён."), { code: "REQUEST_OUTCOME_UNKNOWN_NO_RETRY", cause: error }), "UNKNOWN"); }
    let text = "";
    try { text = await response.text(); } catch { text = ""; }
    const parsed = parseJson(text);
    if (!response.ok) {
      const payload = Webmaster.safeErrorPayload(response.status, text, parsed);
      return buildWebmasterReturn({ normalized, metadata, requestId, httpStatus: response.status, started, result: { error: payload }, ok: false, reason: payload.code, requestExecuted: true });
    }
    let result;
    try { result = Webmaster.normalizeProviderResult(normalized, parsed); } catch (error) { throw executionError(error, true); }

    if (normalized.method === "startQueryUrlExport") {
      const jobs = await loadExportJobs();
      const job = {
        task_id: result.task_id,
        host_id: normalized.hostId,
        start_manifest: clone(normalized),
        projection: clone(result.projection || Webmaster.projectQueryUrlExport(normalized)),
        quota: { free_quota_used: result.free_quota_used, pro_quota_used: result.pro_quota_used, total_quota_used: result.total_quota_used, free_quota_remaining: result.free_quota_remaining, pro_quota_remaining: result.pro_quota_remaining },
        download_status: "SUBMITTED",
        download_url: null,
        created_at: nowIso(),
        updated_at: nowIso(),
        collected_at: null,
        rows: null,
        columns: [],
        downloaded_sha256: null,
        downloaded_bytes: 0,
        compression: null,
        csv_sha256: null,
        csv_bytes: 0,
        raw_csv: null,
        raw_sha256: null,
        raw_bytes: 0,
        row_count: 0,
        parse_warning: null
      };
      await persistExportJob(jobs, job);
      result = { ...result, durable_export: publicExportManifest(job) };
    } else if (normalized.method === "getQueryUrlExportStatus") {
      const loaded = await loadExportJob(normalized.taskId, { required: false });
      const jobs = loaded.map;
      const existing = loaded.job || { task_id: normalized.taskId, host_id: normalized.hostId, created_at: null, projection: null, quota: null, rows: null, columns: [], downloaded_sha256: null, downloaded_bytes: 0, compression: null, csv_sha256: null, csv_bytes: 0, raw_csv: null, raw_sha256: null, raw_bytes: 0, row_count: 0, parse_warning: null };
      if (existing.host_id && existing.host_id !== normalized.hostId) throw Object.assign(new Error("hostId не совпадает с durable export job."), { code: "WEBMASTER_EXPORT_HOST_MISMATCH", request_executed: true, automatic_retry: false });
      const next = { ...existing, host_id: normalized.hostId, download_status: result.download_status, updated_at: nowIso() };
      if (result.download_status === "SUCCESS") next.download_url = safeDownloadUrl(result.url);
      if (result.download_status === "FAILED") { next.error_code = result.error_code || null; next.error_message = result.error_message || null; next.download_url = null; }
      await persistExportJob(jobs, next);
      result = { ...result, url: undefined, durable_export: publicExportManifest(next) };
      delete result.url;
    }

    return buildWebmasterReturn({ normalized, metadata, requestId, httpStatus: response.status, started, result, requestExecuted: true });
  }

  async function execute(service, command, metadata = {}) {
    if (service === Registry.SERVICES.WEBMASTER) return executeWebmaster(command, metadata);
    if (service === Registry.SERVICES.SEARCH || service === Registry.SERVICES.WORDSTAT) return executeCloud(service, command, metadata);
    throw Object.assign(new Error("Сервис не поддерживается."), { code: "SERVICE_NOT_AVAILABLE" });
  }

  async function checkCloud(service, { confirmBillable = false } = {}) {
    if (![Registry.SERVICES.WORDSTAT, Registry.SERVICES.SEARCH].includes(service)) throw Object.assign(new Error("Cloud credential Check поддерживает только Wordstat/Search."), { code: "UNKNOWN_SERVICE", request_executed: false, automatic_retry: false });
    const settings = await Credentials.settings();
    const record = settings.credentials[service] || {};
    if (!trim(record.api_key)) throw Object.assign(new Error(`Сначала сохраните API key ${service}.`), { code: "API_KEY_MISSING", request_executed: false, automatic_retry: false });
    if (!trim(record.folder_id)) throw Object.assign(new Error(`Сначала сохраните folderId ${service}.`), { code: "FOLDER_ID_MISSING", request_executed: false, automatic_retry: false });
    if (service === Registry.SERVICES.SEARCH && confirmBillable !== true) throw Object.assign(new Error("Search Check требует явного подтверждения одного платного запроса."), { code: "SEARCH_CHECK_CONFIRM_REQUIRED", request_executed: false, automatic_retry: false });
    const command = service === Registry.SERVICES.WORDSTAT ? { method: "getRegionsTree" } : { method: "search", queryText: "yandex", groupsOnPage: 1 };
    try {
      const result = await executeCloud(service, command, { channel: "credential_check" });
      const state = result.ok ? "PRESENT" : checkStateFromHttp(result.http_status);
      await Credentials.save(service, { checked_at: nowIso(), check_state: state });
      return { ok: result.ok, service, state, http_status: result.http_status, request_executed: true, automatic_retry: false, billable_request_confirmed: service === Registry.SERVICES.SEARCH };
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
    try { response = await fetch(`${Webmaster.BASE_URL}/user`, { method: "GET", headers: { Accept: "application/json", Authorization: `OAuth ${token}` } }); }
    catch (error) {
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
    WEBMASTER_EXPORT_JOBS_KEY,
    getWebmasterPolicy,
    saveWebmasterPolicy,
    execute,
    executeWebmaster,
    executeCloud,
    checkCloud,
    checkWebmaster,
    loadExportJobs,
    publicExportManifest
  });
})();