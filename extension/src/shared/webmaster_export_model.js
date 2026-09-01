(() => {
  "use strict";

  const STORE_KEY = "ymb_webmaster_exports_v1";
  const RAW_KEY_PREFIX = "ymb_webmaster_export_raw_v1:";
  const ROWS_KEY_PREFIX = "ymb_webmaster_export_rows_v1:";
  const MAX_CHUNK_SIZE = 500;
  const MAX_EXPORT_PAYLOAD_ITEMS = 100;
  const DOWNLOAD_ORIGIN = "https://storage.mds.yandex.net";
  const DOWNLOAD_PATH_PREFIX = "/get-webmaster-download/";
  const EXPORT_COLUMNS = Object.freeze(["date", "host", "url", "query", "region", "clicks", "impressions", "position"]);
  const HEADER_ALIASES = Object.freeze({
    date: Object.freeze(["date", "дата"]),
    host: Object.freeze(["host", "хост"]),
    url: Object.freeze(["url", "адрес", "страница"]),
    query: Object.freeze(["query", "запрос", "поисковый запрос"]),
    region: Object.freeze(["region", "регион"]),
    clicks: Object.freeze(["clicks", "клики"]),
    impressions: Object.freeze(["impressions", "показы"]),
    position: Object.freeze(["position", "позиция"])
  });

  function fail(code, message) { const error = new Error(message || code); error.code = code; throw error; }
  function nowIso() { return new Date().toISOString(); }
  function clone(value) { return value == null ? value : JSON.parse(JSON.stringify(value)); }
  function trim(value) { return String(value ?? "").trim(); }
  function asTaskId(value) {
    const text = trim(value);
    if (!/^[A-Za-z0-9_-]{8,160}$/.test(text)) fail("INVALID_WEBMASTER_EXPORT_TASK_ID", "taskId имеет некорректный формат.");
    return text;
  }
  function asNonNegativeInt(value, name, fallback = 0) {
    const candidate = value === undefined ? fallback : Number(value);
    if (!Number.isSafeInteger(candidate) || candidate < 0) fail("INVALID_FIELD", `${name} должен быть неотрицательным целым числом.`);
    return candidate;
  }
  function asPositiveInt(value, name, fallback, max) {
    const candidate = value === undefined ? fallback : Number(value);
    if (!Number.isSafeInteger(candidate) || candidate < 1 || candidate > max) fail("INVALID_FIELD", `${name} должен быть целым числом от 1 до ${max}.`);
    return candidate;
  }

  function projectExport(command = {}) {
    const paths = Array.isArray(command.paths) ? command.paths : [];
    const dates = Array.isArray(command.dates) ? command.dates : [];
    if (!paths.length) fail("EMPTY_PATHS", "Для выгрузки нужен хотя бы один path.");
    if (!dates.length) fail("EMPTY_DATES", "Для выгрузки нужна хотя бы одна дата.");
    const payloadItems = paths.length + dates.length;
    const projectedUnits = paths.length * dates.length;
    return Object.freeze({
      paths_count: paths.length,
      dates_count: dates.length,
      payload_items: payloadItems,
      provider_payload_item_limit: MAX_EXPORT_PAYLOAD_ITEMS,
      within_provider_payload_item_limit: payloadItems <= MAX_EXPORT_PAYLOAD_ITEMS,
      projected_quota_units: projectedUnits,
      use_pro_tariff: command.useProTariff === true
    });
  }

  function assertSafeDownloadUrl(value) {
    const text = trim(value);
    let url;
    try { url = new URL(text); }
    catch { fail("UNSAFE_WEBMASTER_DOWNLOAD_URL", "Webmaster export вернул некорректную ссылку скачивания."); }
    if (url.protocol !== "https:" || url.origin !== DOWNLOAD_ORIGIN || !url.pathname.startsWith(DOWNLOAD_PATH_PREFIX)) {
      fail("UNSAFE_WEBMASTER_DOWNLOAD_URL", "Ссылка выгрузки не принадлежит разрешённому Yandex Webmaster storage endpoint.");
    }
    return url.toString();
  }

  function normalizeHeader(value) {
    return trim(value).replace(/^\uFEFF/, "").toLowerCase().replace(/\s+/g, " ");
  }

  function canonicalHeader(value) {
    const normalized = normalizeHeader(value);
    for (const [canonical, aliases] of Object.entries(HEADER_ALIASES)) {
      if (aliases.includes(normalized)) return canonical;
    }
    return null;
  }

  function delimiterScore(line, delimiter) {
    let quoted = false;
    let score = 0;
    for (let i = 0; i < line.length; i += 1) {
      const char = line[i];
      if (char === '"') {
        if (quoted && line[i + 1] === '"') { i += 1; continue; }
        quoted = !quoted;
      } else if (!quoted && char === delimiter) score += 1;
    }
    return score;
  }

  function detectDelimiter(text) {
    const firstLine = String(text || "").replace(/^\uFEFF/, "").split(/\r?\n/, 1)[0] || "";
    const candidates = [",", ";", "\t"];
    let best = ",";
    let bestScore = -1;
    for (const delimiter of candidates) {
      const score = delimiterScore(firstLine, delimiter);
      if (score > bestScore) { best = delimiter; bestScore = score; }
    }
    if (bestScore < 1) fail("INVALID_WEBMASTER_EXPORT_CSV", "Не удалось определить разделитель CSV-выгрузки.");
    return best;
  }

  function parseDelimited(text, delimiter) {
    const source = String(text || "").replace(/^\uFEFF/, "");
    const rows = [];
    let row = [];
    let cell = "";
    let quoted = false;
    for (let i = 0; i < source.length; i += 1) {
      const char = source[i];
      if (quoted) {
        if (char === '"' && source[i + 1] === '"') { cell += '"'; i += 1; continue; }
        if (char === '"') { quoted = false; continue; }
        cell += char;
        continue;
      }
      if (char === '"') { quoted = true; continue; }
      if (char === delimiter) { row.push(cell); cell = ""; continue; }
      if (char === "\n") {
        row.push(cell.replace(/\r$/, ""));
        if (row.some((value) => trim(value) !== "")) rows.push(row);
        row = [];
        cell = "";
        continue;
      }
      cell += char;
    }
    if (quoted) fail("INVALID_WEBMASTER_EXPORT_CSV", "CSV завершился внутри quoted field.");
    if (cell !== "" || row.length) {
      row.push(cell.replace(/\r$/, ""));
      if (row.some((value) => trim(value) !== "")) rows.push(row);
    }
    return rows;
  }

  function parseNumber(value) {
    const text = trim(value);
    if (!text) return null;
    const number = Number(text.replace(/\s+/g, "").replace(",", "."));
    return Number.isFinite(number) ? number : null;
  }

  function parseExportCsv(text) {
    const rawText = String(text ?? "");
    if (!rawText.trim()) fail("EMPTY_WEBMASTER_EXPORT", "Yandex Webmaster вернул пустой export-файл.");
    const delimiter = detectDelimiter(rawText);
    const matrix = parseDelimited(rawText, delimiter);
    if (matrix.length < 1) fail("INVALID_WEBMASTER_EXPORT_CSV", "В CSV отсутствует строка заголовков.");
    const headers = matrix[0].map((value) => trim(value).replace(/^\uFEFF/, ""));
    const indexByCanonical = {};
    headers.forEach((header, index) => {
      const canonical = canonicalHeader(header);
      if (canonical && indexByCanonical[canonical] === undefined) indexByCanonical[canonical] = index;
    });
    const missing = EXPORT_COLUMNS.filter((column) => indexByCanonical[column] === undefined);
    if (missing.length) fail("WEBMASTER_EXPORT_COLUMNS_MISSING", `В export CSV отсутствуют обязательные колонки: ${missing.join(", ")}.`);
    const rows = matrix.slice(1).map((sourceRow) => Object.freeze({
      date: trim(sourceRow[indexByCanonical.date]),
      host: trim(sourceRow[indexByCanonical.host]),
      url: trim(sourceRow[indexByCanonical.url]),
      query: trim(sourceRow[indexByCanonical.query]),
      region: trim(sourceRow[indexByCanonical.region]),
      clicks: parseNumber(sourceRow[indexByCanonical.clicks]),
      impressions: parseNumber(sourceRow[indexByCanonical.impressions]),
      position: parseNumber(sourceRow[indexByCanonical.position])
    }));
    return Object.freeze({ delimiter, headers: Object.freeze(headers), rows: Object.freeze(rows) });
  }

  async function sha256Hex(value) {
    const bytes = new TextEncoder().encode(String(value ?? ""));
    const digest = await crypto.subtle.digest("SHA-256", bytes);
    return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
  }

  async function loadJobs() {
    const data = await chrome.storage.local.get(STORE_KEY);
    const value = data[STORE_KEY];
    return value && typeof value === "object" && !Array.isArray(value) ? value : {};
  }

  async function saveJobs(jobs) { await chrome.storage.local.set({ [STORE_KEY]: jobs }); }
  function rawKey(taskId) { return `${RAW_KEY_PREFIX}${asTaskId(taskId)}`; }
  function rowsKey(taskId) { return `${ROWS_KEY_PREFIX}${asTaskId(taskId)}`; }

  function publicManifest(job) {
    if (!job) return null;
    const out = clone(job);
    delete out.download_url;
    delete out.raw_storage_key;
    delete out.rows_storage_key;
    return out;
  }

  async function recordStart(command, result, requestId = null) {
    const taskId = asTaskId(result?.task_id);
    const jobs = await loadJobs();
    const now = nowIso();
    const projection = projectExport(command);
    const job = {
      task_id: taskId,
      host_id: trim(command.hostId),
      created_at: jobs[taskId]?.created_at || now,
      updated_at: now,
      request_id: requestId || null,
      download_status: "QUEUED",
      paths: clone(command.paths || []),
      dates: clone(command.dates || []),
      region_ids: clone(command.regionIds || []),
      use_pro_tariff: command.useProTariff === true,
      projection,
      quota: {
        free_quota_used: Number(result?.free_quota_used ?? 0),
        pro_quota_used: Number(result?.pro_quota_used ?? 0),
        total_quota_used: Number(result?.total_quota_used ?? 0),
        free_quota_remaining: Number(result?.free_quota_remaining ?? 0),
        pro_quota_remaining: Number(result?.pro_quota_remaining ?? 0)
      },
      download_url: null,
      download_url_observed_at: null,
      collection: null,
      raw_storage_key: rawKey(taskId),
      rows_storage_key: rowsKey(taskId)
    };
    jobs[taskId] = job;
    await saveJobs(jobs);
    return publicManifest(job);
  }

  async function recordStatus(command, providerResult) {
    const taskId = asTaskId(command.taskId);
    const jobs = await loadJobs();
    const current = jobs[taskId] || {
      task_id: taskId,
      host_id: trim(command.hostId),
      created_at: nowIso(),
      paths: [], dates: [], region_ids: [], use_pro_tariff: false,
      projection: null, quota: null, collection: null,
      raw_storage_key: rawKey(taskId), rows_storage_key: rowsKey(taskId)
    };
    if (current.host_id && trim(command.hostId) && current.host_id !== trim(command.hostId)) {
      fail("WEBMASTER_EXPORT_HOST_MISMATCH", "taskId уже связан с другим hostId.");
    }
    const status = trim(providerResult?.download_status || "UNKNOWN");
    current.host_id = trim(command.hostId) || current.host_id;
    current.updated_at = nowIso();
    current.download_status = status;
    current.status_error = status === "FAILED" ? {
      code: trim(providerResult?.error_code || "EXPORT_FAILED"),
      message: trim(providerResult?.error_message || "Yandex Webmaster export failed")
    } : null;
    if (status === "SUCCESS") {
      current.download_url = assertSafeDownloadUrl(providerResult?.url);
      current.download_url_observed_at = nowIso();
    }
    jobs[taskId] = current;
    await saveJobs(jobs);
    return publicManifest(current);
  }

  async function downloadTarget(taskId) {
    const id = asTaskId(taskId);
    const jobs = await loadJobs();
    const job = jobs[id];
    if (!job) fail("WEBMASTER_EXPORT_JOB_NOT_FOUND", "Export job не найден в локальном durable store.");
    if (job.download_status !== "SUCCESS") fail("WEBMASTER_EXPORT_NOT_READY", `Export job ещё не готов: ${job.download_status || "UNKNOWN"}.`);
    return Object.freeze({ task_id: id, url: assertSafeDownloadUrl(job.download_url), host_id: job.host_id || null });
  }

  async function recordCollected(taskId, rawText) {
    const id = asTaskId(taskId);
    const parsed = parseExportCsv(rawText);
    const checksum = await sha256Hex(rawText);
    const jobs = await loadJobs();
    const job = jobs[id];
    if (!job) fail("WEBMASTER_EXPORT_JOB_NOT_FOUND", "Export job не найден в локальном durable store.");
    const collectedAt = nowIso();
    await chrome.storage.local.set({
      [rawKey(id)]: String(rawText),
      [rowsKey(id)]: parsed.rows.map((row) => clone(row))
    });
    job.updated_at = collectedAt;
    job.collection = {
      complete: true,
      collected_at: collectedAt,
      row_count: parsed.rows.length,
      raw_sha256: checksum,
      raw_bytes_utf8: new TextEncoder().encode(String(rawText)).byteLength,
      delimiter: parsed.delimiter === "\t" ? "TAB" : parsed.delimiter,
      headers: [...parsed.headers],
      canonical_columns: [...EXPORT_COLUMNS]
    };
    jobs[id] = job;
    await saveJobs(jobs);
    return publicManifest(job);
  }

  async function getManifest(taskId) {
    const id = asTaskId(taskId);
    const jobs = await loadJobs();
    const job = jobs[id];
    if (!job) fail("WEBMASTER_EXPORT_JOB_NOT_FOUND", "Export job не найден в локальном durable store.");
    return publicManifest(job);
  }

  async function listJobs({ pendingOnly = false } = {}) {
    const jobs = await loadJobs();
    return Object.values(jobs)
      .filter((job) => !pendingOnly || (job?.collection?.complete !== true && job?.download_status !== "FAILED"))
      .sort((a, b) => String(b.updated_at || "").localeCompare(String(a.updated_at || "")))
      .map(publicManifest);
  }

  async function readChunk(taskId, offset = 0, limit = 200) {
    const id = asTaskId(taskId);
    const start = asNonNegativeInt(offset, "offset", 0);
    const pageSize = asPositiveInt(limit, "limit", 200, MAX_CHUNK_SIZE);
    const jobs = await loadJobs();
    const job = jobs[id];
    if (!job) fail("WEBMASTER_EXPORT_JOB_NOT_FOUND", "Export job не найден в локальном durable store.");
    if (job?.collection?.complete !== true) fail("WEBMASTER_EXPORT_NOT_COLLECTED", "Export ещё не скачан и не нормализован.");
    const data = await chrome.storage.local.get(rowsKey(id));
    const rows = Array.isArray(data[rowsKey(id)]) ? data[rowsKey(id)] : [];
    const slice = rows.slice(start, start + pageSize).map(clone);
    return Object.freeze({
      task_id: id,
      offset: start,
      limit: pageSize,
      row_count_total: rows.length,
      rows_returned: slice.length,
      next_offset: start + slice.length < rows.length ? start + slice.length : null,
      complete: start + slice.length >= rows.length,
      rows: Object.freeze(slice)
    });
  }

  globalThis.YMBWebmasterExportModel = Object.freeze({
    STORE_KEY, RAW_KEY_PREFIX, ROWS_KEY_PREFIX, MAX_CHUNK_SIZE, MAX_EXPORT_PAYLOAD_ITEMS,
    DOWNLOAD_ORIGIN, DOWNLOAD_PATH_PREFIX, EXPORT_COLUMNS,
    projectExport, assertSafeDownloadUrl, parseExportCsv, sha256Hex,
    recordStart, recordStatus, downloadTarget, recordCollected, getManifest, listJobs, readChunk,
    publicManifest
  });
})();
