(() => {
  "use strict";

  const DB_NAME = "ymb_search_async_items_v2";
  const MAX_INDEX = Number.MAX_SAFE_INTEGER;
  const UNKNOWN_CONVERSATION = new Set(["", "не определён"]);
  const ACTION_MESSAGE = "YMB_ASYNC_POPUP_ACTION";
  const JOB_OWNER_PREFIX = "search-folder:";

  const number = (value) => Number.isFinite(Number(value)) ? Number(value) : 0;
  const count = (counts, key) => Math.max(0, Math.trunc(number(counts?.[key])));
  const percent = (value, total) => total > 0 ? Math.max(0, Math.min(100, (value / total) * 100)) : 0;
  const request = (r) => new Promise((resolve, reject) => {
    r.onsuccess = () => resolve(r.result);
    r.onerror = () => reject(r.error || new Error("ASYNC_MONITOR_IDB_REQUEST_FAILED"));
  });

  function durableJobOwner(folderId) {
    const value = String(folderId || "");
    if (!value || value.length > 50 || /[\u0000-\u001f\u007f]/u.test(value)) return "";
    return `${JOB_OWNER_PREFIX}${value}`;
  }

  function formatPercent(value) {
    const rounded = Math.round(value * 10) / 10;
    return Number.isInteger(rounded) ? `${rounded}%` : `${rounded.toFixed(1)}%`;
  }

  function formatDuration(ms) {
    const totalSeconds = Math.max(0, Math.floor(number(ms) / 1000));
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;
    if (hours > 0) return `${hours}ч ${String(minutes).padStart(2, "0")}м`;
    if (minutes > 0) return `${minutes}м ${String(seconds).padStart(2, "0")}с`;
    return `${seconds}с`;
  }

  function computeMetrics(snapshot) {
    const total = Math.max(0, Math.trunc(number(snapshot?.total)));
    const counts = snapshot?.counts || {};
    const succeeded = count(counts, "SUCCEEDED");
    const failed = count(counts, "FAILED");
    const parseFailed = count(counts, "PARSE_FAILED");
    const cancelled = count(counts, "CANCELLED");
    const unknown = count(counts, "UNKNOWN");
    const pending = count(counts, "PENDING");
    const waiting = count(counts, "WAITING");
    const working = count(counts, "SUBMITTING") + count(counts, "COLLECTING") + count(counts, "RESULT_SAVED");
    const terminal = succeeded + failed + parseFailed + cancelled;
    const remaining = Math.max(0, total - terminal);
    const issues = failed + parseFailed + unknown;
    let state = "Нет данных";
    if (total > 0 && terminal === total) state = issues ? "Завершено с ошибками" : "Готово";
    else if (unknown > 0) state = "Требует проверки";
    else if (waiting > 0) state = "Ожидание Яндекса";
    else if (working > 0) state = "В работе";
    else if (pending > 0) state = "В очереди";
    const rowCount = snapshot?.result_row_count;
    return {
      total, succeeded, failed, parse_failed: parseFailed, cancelled, unknown, pending, waiting, working,
      terminal, remaining, issues, state,
      processed_percent: percent(terminal, total),
      success_percent: percent(succeeded, total),
      result_row_count: rowCount === null || rowCount === undefined ? null : Math.max(0, Math.trunc(number(rowCount))),
      normalized_items: Math.max(0, Math.trunc(number(snapshot?.normalized_items))),
      raw_items: Math.max(0, Math.trunc(number(snapshot?.raw_items)))
    };
  }

  function formatNextCheck(snapshot, now = Date.now()) {
    const waiting = count(snapshot?.counts || {}, "WAITING");
    if (!waiting) return "—";
    if (number(snapshot?.due_count) > 0) return "можно сейчас";
    const next = number(snapshot?.next_poll_at);
    if (!next) return "ожидается расписание";
    const delta = next - now;
    return delta <= 0 ? "можно сейчас" : `через ${formatDuration(delta)}`;
  }

  function actionAvailability(snapshot, now = Date.now(), inFlight = false) {
    const metrics = computeMetrics(snapshot);
    const hasJob = Boolean(snapshot?.job_id);
    const dueCount = Math.max(0, Math.trunc(number(snapshot?.due_count)));
    const next = number(snapshot?.next_poll_at);
    const waiting = metrics.waiting;
    const dueNow = dueCount > 0 || (waiting > 0 && next > 0 && next <= now);
    const complete = metrics.total > 0 && metrics.terminal === metrics.total;
    const collectEnabled = hasJob && !inFlight && waiting > 0 && dueNow;
    let collectLabel = "Проверить результат";
    if (inFlight) collectLabel = "Выполняется…";
    else if (hasJob && !waiting) collectLabel = "Нет ожидающих запросов";
    else if (hasJob && !dueNow && next > now) collectLabel = `Проверить можно через ${formatDuration(next - now)}`;
    else if (hasJob && !dueNow) collectLabel = "Проверка пока недоступна";
    return {
      collect_enabled: collectEnabled,
      collect_label: collectLabel,
      export_enabled: hasJob && !inFlight && complete,
      export_label: inFlight ? "Выполняется…" : "Отправить файл в чат",
      complete
    };
  }

  function buildActionMessage(action, snapshot, owner) {
    const conversationKey = String(owner || "").trim();
    const jobId = String(snapshot?.job_id || "").trim();
    if (!conversationKey || !jobId) throw new Error("ASYNC_POPUP_ACTION_CONTEXT_MISSING");
    if (action === "collect_one") return { type: ACTION_MESSAGE, action, conversation_key: conversationKey, job_id: jobId };
    if (action === "export_page") {
      const revision = Math.trunc(number(snapshot?.revision));
      if (!Number.isSafeInteger(revision) || revision < 0) throw new Error("ASYNC_POPUP_ACTION_REVISION_INVALID");
      return { type: ACTION_MESSAGE, action, conversation_key: conversationKey, job_id: jobId, revision };
    }
    throw new Error("ASYNC_POPUP_ACTION_UNSUPPORTED");
  }

  function runtimeSend(message) {
    return new Promise((resolve, reject) => {
      try {
        chrome.runtime.sendMessage(message, (response) => {
          const error = chrome.runtime.lastError;
          if (error) reject(new Error(error.message || String(error)));
          else resolve(response);
        });
      } catch (error) { reject(error); }
    });
  }

  async function readSearchFolderId() {
    const response = await runtimeSend({ type: "WS_GET_GLOBAL_STATE", page_context_error: "ASYNC_MONITOR_LOCAL_READ" });
    if (!response?.ok || !response.state) throw Object.assign(new Error(response?.error || response?.code || "ASYNC_MONITOR_STATE_UNAVAILABLE"), { code: response?.code || "ASYNC_MONITOR_STATE_UNAVAILABLE" });
    const folderId = String(response.state?.credential_status?.search?.folder_id || "");
    return durableJobOwner(folderId) ? folderId : "";
  }

  async function databaseExists() {
    if (typeof indexedDB.databases !== "function") return null;
    try {
      const databases = await indexedDB.databases();
      return Array.isArray(databases) ? databases.some((entry) => entry?.name === DB_NAME) : null;
    } catch { return null; }
  }

  async function openExistingDb() {
    const exists = await databaseExists();
    if (exists === false) throw Object.assign(new Error("ASYNC_MONITOR_DB_MISSING"), { code: "ASYNC_MONITOR_DB_MISSING" });
    return new Promise((resolve, reject) => {
      let missing = false;
      const r = indexedDB.open(DB_NAME);
      r.onupgradeneeded = () => { missing = true; try { r.transaction?.abort(); } catch {} };
      r.onsuccess = () => {
        if (missing) {
          try { r.result?.close(); } catch {}
          reject(Object.assign(new Error("ASYNC_MONITOR_DB_MISSING"), { code: "ASYNC_MONITOR_DB_MISSING" }));
          return;
        }
        r.result.onversionchange = () => r.result.close();
        resolve(r.result);
      };
      r.onerror = () => reject(Object.assign(r.error || new Error(missing ? "ASYNC_MONITOR_DB_MISSING" : "ASYNC_MONITOR_DB_OPEN_FAILED"), { code: missing ? "ASYNC_MONITOR_DB_MISSING" : "ASYNC_MONITOR_DB_OPEN_FAILED" }));
      r.onblocked = () => reject(Object.assign(new Error("ASYNC_MONITOR_DB_BLOCKED"), { code: "ASYNC_MONITOR_DB_BLOCKED" }));
    });
  }

  async function latestJobForFolder(db, folderId) {
    const owner = durableJobOwner(folderId);
    if (!owner) return null;
    return new Promise((resolve, reject) => {
      const tx = db.transaction(["jobs"], "readonly");
      const store = tx.objectStore("jobs");
      let selected = null;
      const cursor = store.openCursor();
      cursor.onerror = () => reject(cursor.error || new Error("ASYNC_MONITOR_JOB_CURSOR_FAILED"));
      cursor.onsuccess = () => {
        const c = cursor.result;
        if (!c) { resolve(selected); return; }
        const job = c.value;
        if (job?.folder_id === folderId && job?.owner === owner && (!selected || number(job.updated_at) > number(selected.updated_at))) selected = job;
        c.continue();
      };
      tx.onabort = () => reject(tx.error || new Error("ASYNC_MONITOR_JOB_TX_ABORTED"));
    });
  }

  async function boundedCounts(db, job, now) {
    const jobId = String(job.job_id || "");
    const tx = db.transaction(["items", "results"], "readonly");
    const items = tx.objectStore("items");
    const results = tx.objectStore("results");
    const due = items.index("due");
    const itemRange = IDBKeyRange.bound([jobId, 0], [jobId, MAX_INDEX]);
    const dueRange = IDBKeyRange.bound([jobId, "WAITING", 1, 0], [jobId, "WAITING", Math.max(1, Math.trunc(now)), MAX_INDEX]);
    const waitingRange = IDBKeyRange.bound([jobId, "WAITING", 1, 0], [jobId, "WAITING", MAX_INDEX, MAX_INDEX]);

    // Memory safety invariant: never materialize raw_text or normalized.results in popup.
    const itemCountReq = items.count(itemRange);
    const dueCountReq = due.count(dueRange);
    const nextReq = due.get(waitingRange);
    const resultCountReq = results.count(itemRange);
    const [itemCount, dueCount, nextWaiting, rawItems] = await Promise.all([
      request(itemCountReq), request(dueCountReq), request(nextReq), request(resultCountReq)
    ]);
    return {
      item_count: Math.max(0, Math.trunc(number(itemCount))),
      due_count: Math.max(0, Math.trunc(number(dueCount))),
      next_poll_at: Math.max(0, number(nextWaiting?.next_poll_at)),
      raw_items: Math.max(0, Math.trunc(number(rawItems))),
      normalized_items: count(job.counts || {}, "SUCCEEDED"),
      result_row_count: null
    };
  }

  async function snapshotForFolder(folderId, now = Date.now()) {
    if (!durableJobOwner(folderId)) return null;
    const db = await openExistingDb();
    try {
      if (!["jobs", "items", "results"].every((name) => db.objectStoreNames.contains(name))) return null;
      const job = await latestJobForFolder(db, folderId);
      if (!job) return null;
      const light = await boundedCounts(db, job, now);
      return {
        job_id: String(job.job_id || ""), control: String(job.control || ""), total: Math.max(0, Math.trunc(number(job.total))),
        counts: { ...(job.counts || {}) }, requests_started: Math.max(0, Math.trunc(number(job.requests_started))),
        operations_accepted: Math.max(0, Math.trunc(number(job.operations_accepted))), polls_started: Math.max(0, Math.trunc(number(job.polls_started))),
        revision: Math.max(0, Math.trunc(number(job.revision))), created_at: Math.max(0, number(job.created_at)), updated_at: Math.max(0, number(job.updated_at)),
        ...light
      };
    } finally { try { db.close(); } catch {} }
  }

  function el(tag, text = "", className = "") { const node = document.createElement(tag); if (className) node.className = className; if (text) node.textContent = text; return node; }
  function addRow(section, label, id) { const row = el("div", "", "row"); row.append(el("span", label)); const value = el("strong", "—"); value.id = id; row.append(value); section.append(row); }

  function installSection() {
    if (document.getElementById("searchAsyncMonitorSection")) return document.getElementById("searchAsyncMonitorSection");
    const section = el("section");
    section.id = "searchAsyncMonitorSection";
    section.append(el("h2", "Deferred Search — прогресс"));
    addRow(section, "Job", "searchAsyncJob"); addRow(section, "Состояние", "searchAsyncState"); addRow(section, "Обработано", "searchAsyncProcessed");
    addRow(section, "Успешно", "searchAsyncSucceeded"); addRow(section, "Осталось запросов", "searchAsyncRemaining"); addRow(section, "Ожидают Яндекс", "searchAsyncWaiting");
    addRow(section, "В очереди / работе", "searchAsyncPendingWorking"); addRow(section, "Ошибки / неопределено", "searchAsyncIssues"); addRow(section, "Получено SERP-строк", "searchAsyncRows");
    addRow(section, "Ответов нормализовано", "searchAsyncNormalized"); addRow(section, "Следующая проверка", "searchAsyncNextPoll"); addRow(section, "Прошло", "searchAsyncElapsed"); addRow(section, "Локальная ревизия", "searchAsyncRevision");
    const actions = el("div", "", "actions");
    const refresh = el("button", "Обновить статус"); refresh.id = "searchAsyncRefresh"; refresh.type = "button";
    const collect = el("button", "Проверить результат"); collect.id = "searchAsyncCollectOne"; collect.type = "button"; collect.disabled = true;
    const exportButton = el("button", "Отправить файл в чат"); exportButton.id = "searchAsyncExport"; exportButton.type = "button"; exportButton.disabled = true;
    actions.append(refresh, collect, exportButton); section.append(actions);
    const actionStatus = el("p", "", "warning"); actionStatus.id = "searchAsyncActionStatus"; actionStatus.hidden = true; section.append(actionStatus);
    section.append(el("p", "Статус обновляется только из локального state/IndexedDB. Popup refresh не делает submit, collect или provider polling.", "warning"));
    const sections = Array.from(document.querySelectorAll("main > section"));
    const runSection = sections.find((node) => node.querySelector("h2")?.textContent?.trim() === "Текущий запуск");
    if (runSection?.parentNode) runSection.parentNode.insertBefore(section, runSection.nextSibling); else document.querySelector("main")?.append(section);
    return section;
  }

  function setText(id, value) { const node = document.getElementById(id); if (node) node.textContent = String(value ?? "—"); }
  function setActionStatus(text = "", isError = false) { const node = document.getElementById("searchAsyncActionStatus"); if (!node) return; node.hidden = !text; node.textContent = String(text || ""); node.dataset.level = isError ? "error" : "info"; }
  function currentConversationKey() { const text = String(document.getElementById("conversationMeta")?.textContent || "").trim(); return UNKNOWN_CONVERSATION.has(text) ? "" : text; }

  function sendActiveTabMessage(message) {
    return new Promise((resolve, reject) => {
      try {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          const queryError = chrome.runtime.lastError;
          if (queryError) { reject(new Error(queryError.message || String(queryError))); return; }
          const tabId = tabs?.[0]?.id;
          if (!Number.isInteger(tabId)) { reject(new Error("ASYNC_POPUP_ACTIVE_TAB_MISSING")); return; }
          chrome.tabs.sendMessage(tabId, message, (response) => {
            const sendError = chrome.runtime.lastError;
            if (sendError) reject(new Error(sendError.message || String(sendError))); else resolve(response);
          });
        });
      } catch (error) { reject(error); }
    });
  }

  let latestSnapshot = null;
  let loading = false;
  let actionInFlight = false;

  function renderActions(now = Date.now()) {
    const availability = actionAvailability(latestSnapshot, now, actionInFlight);
    const hasConversationAuthority = Boolean(currentConversationKey());
    const collect = document.getElementById("searchAsyncCollectOne"); const exportButton = document.getElementById("searchAsyncExport");
    if (collect) { collect.disabled = !availability.collect_enabled || !hasConversationAuthority; collect.textContent = availability.collect_label; }
    if (exportButton) { exportButton.disabled = !availability.export_enabled || !hasConversationAuthority; exportButton.textContent = availability.export_label; }
  }

  function render(snapshot, now = Date.now()) {
    latestSnapshot = snapshot || null;
    if (!snapshot) {
      setText("searchAsyncJob", "—"); setText("searchAsyncState", "Нет локального deferred Search job");
      for (const id of ["searchAsyncProcessed", "searchAsyncSucceeded", "searchAsyncRemaining", "searchAsyncWaiting", "searchAsyncPendingWorking", "searchAsyncIssues", "searchAsyncRows", "searchAsyncNormalized", "searchAsyncNextPoll", "searchAsyncElapsed", "searchAsyncRevision"]) setText(id, "—");
      renderActions(now); return;
    }
    const metrics = computeMetrics(snapshot);
    setText("searchAsyncJob", snapshot.job_id || "—"); setText("searchAsyncState", snapshot.control ? `${snapshot.control} / ${metrics.state}` : metrics.state);
    setText("searchAsyncProcessed", `${metrics.terminal} / ${metrics.total} — ${formatPercent(metrics.processed_percent)}`);
    setText("searchAsyncSucceeded", `${metrics.succeeded} / ${metrics.total} — ${formatPercent(metrics.success_percent)}`);
    setText("searchAsyncRemaining", metrics.remaining); setText("searchAsyncWaiting", metrics.waiting); setText("searchAsyncPendingWorking", `${metrics.pending} / ${metrics.working}`);
    setText("searchAsyncIssues", `${metrics.failed + metrics.parse_failed} / ${metrics.unknown}`);
    setText("searchAsyncRows", metrics.result_row_count === null ? "— (без чтения payload)" : metrics.result_row_count);
    setText("searchAsyncNormalized", `${metrics.normalized_items} / ${metrics.total}`); setText("searchAsyncNextPoll", formatNextCheck(snapshot, now));
    setText("searchAsyncElapsed", snapshot.created_at ? formatDuration(now - snapshot.created_at) : "—"); setText("searchAsyncRevision", snapshot.revision); renderActions(now);
  }

  async function refreshSnapshot() {
    if (loading) return latestSnapshot;
    loading = true; const button = document.getElementById("searchAsyncRefresh"); if (button) button.disabled = true;
    try {
      const folderId = await readSearchFolderId();
      if (!folderId) { render(null); return null; }
      const snapshot = await snapshotForFolder(folderId, Date.now()); render(snapshot); return snapshot;
    } catch (error) {
      if (error?.code === "ASYNC_MONITOR_DB_MISSING") { render(null); return null; }
      setText("searchAsyncState", `Ошибка локального чтения: ${error?.code || error?.message || error}`); return null;
    } finally { loading = false; if (button) button.disabled = false; }
  }

  async function runPopupAction(action) {
    if (actionInFlight) return;
    const now = Date.now(); const availability = actionAvailability(latestSnapshot, now, false);
    const conversationKey = currentConversationKey();
    if (!conversationKey || (action === "collect_one" && !availability.collect_enabled) || (action === "export_page" && !availability.export_enabled)) { renderActions(now); return; }
    actionInFlight = true; renderActions(now); setActionStatus(action === "collect_one" ? "Запрашиваю одну разрешённую проверку…" : "Готовлю экспорт через существующий канал доставки…");
    try {
      const message = buildActionMessage(action, latestSnapshot, conversationKey); const response = await sendActiveTabMessage(message);
      if (!response?.ok || response?.accepted === false) throw Object.assign(new Error(response?.error || response?.code || "ASYNC_POPUP_ACTION_REJECTED"), { code: response?.code || "ASYNC_POPUP_ACTION_REJECTED" });
      setActionStatus(action === "collect_one" ? "Проверка принята существующим Manual-контуром." : "Экспорт принят существующим Manual-контуром."); await refreshSnapshot();
    } catch (error) { setActionStatus(`Действие не выполнено: ${error?.code || error?.message || error}`, true); }
    finally { actionInFlight = false; renderActions(Date.now()); }
  }

  function bootstrap() {
    if (globalThis.__YMB_ASYNC_MONITOR_BOOTSTRAPPED__ === true) return;
    globalThis.__YMB_ASYNC_MONITOR_BOOTSTRAPPED__ = true; installSection();
    document.getElementById("searchAsyncRefresh")?.addEventListener("click", () => { void refreshSnapshot(); });
    document.getElementById("searchAsyncCollectOne")?.addEventListener("click", () => { void runPopupAction("collect_one"); });
    document.getElementById("searchAsyncExport")?.addEventListener("click", () => { void runPopupAction("export_page"); });
    let previousOwner = currentConversationKey();
    const uiTimer = setInterval(() => {
      const owner = currentConversationKey();
      if (owner !== previousOwner) { previousOwner = owner; setActionStatus(""); }
      if (!loading && !actionInFlight) void refreshSnapshot();
      else if (latestSnapshot) render(latestSnapshot, Date.now());
      else renderActions(Date.now());
    }, 1000);
    window.addEventListener("pagehide", () => clearInterval(uiTimer), { once: true });
    void refreshSnapshot();
  }

  if (globalThis.__YMB_ASYNC_MONITOR_TEST__ === true) {
    globalThis.__YMB_ASYNC_MONITOR_TEST_API__ = Object.freeze({
      durableJobOwner, computeMetrics, formatPercent, formatDuration, formatNextCheck, actionAvailability, buildActionMessage,
      readSearchFolderId, latestJobForFolder, snapshotForFolder, refreshSnapshot, render
    });
    return;
  }
  if (typeof document !== "undefined") bootstrap();
})();
