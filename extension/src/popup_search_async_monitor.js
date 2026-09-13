(() => {
  "use strict";

  const DB_NAME = "ymb_search_async_items_v2";
  const MAX_INDEX = Number.MAX_SAFE_INTEGER;
  const REFRESH_MS = 5000;
  const UNKNOWN_CONVERSATION = new Set(["", "не определён"]);

  const number = (value) => Number.isFinite(Number(value)) ? Number(value) : 0;
  const count = (counts, key) => Math.max(0, Math.trunc(number(counts?.[key])));
  const percent = (value, total) => total > 0 ? Math.max(0, Math.min(100, (value / total) * 100)) : 0;
  const formatPercent = (value) => {
    const rounded = Math.round(value * 10) / 10;
    return Number.isInteger(rounded) ? `${rounded}%` : `${rounded.toFixed(1)}%`;
  };
  const formatDuration = (ms) => {
    const totalSeconds = Math.max(0, Math.floor(number(ms) / 1000));
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;
    if (hours > 0) return `${hours}ч ${String(minutes).padStart(2, "0")}м`;
    if (minutes > 0) return `${minutes}м ${String(seconds).padStart(2, "0")}с`;
    return `${seconds}с`;
  };

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
    return {
      total, succeeded, failed, parse_failed: parseFailed, cancelled, unknown, pending, waiting, working,
      terminal, remaining, issues, state,
      processed_percent: percent(terminal, total),
      success_percent: percent(succeeded, total),
      result_row_count: Math.max(0, Math.trunc(number(snapshot?.result_row_count))),
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

  function openExistingDb() {
    return new Promise((resolve, reject) => {
      let missing = false;
      const r = indexedDB.open(DB_NAME);
      r.onupgradeneeded = () => {
        missing = true;
        try { r.transaction?.abort(); } catch {}
      };
      r.onsuccess = () => {
        if (missing) {
          try { r.result?.close(); } catch {}
          reject(Object.assign(new Error("ASYNC_MONITOR_DB_MISSING"), { code: "ASYNC_MONITOR_DB_MISSING" }));
          return;
        }
        resolve(r.result);
      };
      r.onerror = () => reject(Object.assign(r.error || new Error(missing ? "ASYNC_MONITOR_DB_MISSING" : "ASYNC_MONITOR_DB_OPEN_FAILED"), {
        code: missing ? "ASYNC_MONITOR_DB_MISSING" : "ASYNC_MONITOR_DB_OPEN_FAILED"
      }));
      r.onblocked = () => reject(Object.assign(new Error("ASYNC_MONITOR_DB_BLOCKED"), { code: "ASYNC_MONITOR_DB_BLOCKED" }));
    });
  }

  async function readonlyTransaction(db, names, work) {
    return new Promise((resolve, reject) => {
      let result;
      let failure;
      const tx = db.transaction(names, "readonly");
      tx.oncomplete = () => resolve(result);
      tx.onabort = () => reject(failure || tx.error || new Error("ASYNC_MONITOR_IDB_ABORTED"));
      tx.onerror = () => { failure ||= tx.error; };
      Promise.resolve().then(() => work(tx)).then((value) => { result = value; }).catch((error) => {
        failure = error;
        try { tx.abort(); } catch { reject(error); }
      });
    });
  }

  async function latestJobForOwner(tx, owner) {
    const store = tx.objectStore("jobs");
    let selected = null;
    await new Promise((resolve, reject) => {
      const cursor = store.openCursor();
      cursor.onerror = () => reject(cursor.error || new Error("ASYNC_MONITOR_JOB_CURSOR_FAILED"));
      cursor.onsuccess = () => {
        const c = cursor.result;
        if (!c) { resolve(); return; }
        const job = c.value;
        if (job?.owner === owner && (!selected || number(job.updated_at) > number(selected.updated_at))) selected = job;
        c.continue();
      };
    });
    return selected;
  }

  async function snapshotForOwner(owner, now = Date.now()) {
    if (typeof owner !== "string" || !owner.trim()) return null;
    const db = await openExistingDb();
    try {
      if (!["jobs", "items", "results"].every((name) => db.objectStoreNames.contains(name))) return null;
      return await readonlyTransaction(db, ["jobs", "items", "results"], async (tx) => {
        const job = await latestJobForOwner(tx, owner);
        if (!job) return null;
        const jobId = String(job.job_id || "");
        let nextPollAt = 0;
        let dueCount = 0;
        let itemCount = 0;
        const items = tx.objectStore("items");
        const itemCursor = items.openCursor(IDBKeyRange.bound([jobId, 0], [jobId, MAX_INDEX]));
        await new Promise((resolve, reject) => {
          itemCursor.onerror = () => reject(itemCursor.error || new Error("ASYNC_MONITOR_ITEM_CURSOR_FAILED"));
          itemCursor.onsuccess = () => {
            const c = itemCursor.result;
            if (!c) { resolve(); return; }
            const item = c.value;
            itemCount += 1;
            if (item?.state === "WAITING") {
              const at = number(item.next_poll_at);
              if (at > 0 && (!nextPollAt || at < nextPollAt)) nextPollAt = at;
              if (at > 0 && at <= now) dueCount += 1;
            }
            c.continue();
          };
        });

        let resultRowCount = 0;
        let normalizedItems = 0;
        let rawItems = 0;
        const results = tx.objectStore("results");
        const resultCursor = results.openCursor(IDBKeyRange.bound([jobId, 0], [jobId, MAX_INDEX]));
        await new Promise((resolve, reject) => {
          resultCursor.onerror = () => reject(resultCursor.error || new Error("ASYNC_MONITOR_RESULT_CURSOR_FAILED"));
          resultCursor.onsuccess = () => {
            const c = resultCursor.result;
            if (!c) { resolve(); return; }
            const record = c.value;
            if (typeof record?.raw_text === "string") rawItems += 1;
            if (Array.isArray(record?.normalized?.results)) {
              normalizedItems += 1;
              resultRowCount += record.normalized.results.length;
            }
            c.continue();
          };
        });

        return {
          job_id: jobId,
          control: String(job.control || ""),
          total: Math.max(0, Math.trunc(number(job.total))),
          counts: { ...(job.counts || {}) },
          requests_started: Math.max(0, Math.trunc(number(job.requests_started))),
          operations_accepted: Math.max(0, Math.trunc(number(job.operations_accepted))),
          polls_started: Math.max(0, Math.trunc(number(job.polls_started))),
          revision: Math.max(0, Math.trunc(number(job.revision))),
          created_at: Math.max(0, number(job.created_at)),
          updated_at: Math.max(0, number(job.updated_at)),
          next_poll_at: nextPollAt,
          due_count: dueCount,
          item_count: itemCount,
          raw_items: rawItems,
          normalized_items: normalizedItems,
          result_row_count: resultRowCount
        };
      });
    } finally {
      try { db.close(); } catch {}
    }
  }

  function el(tag, text = "", className = "") {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  }

  function addRow(section, label, id) {
    const row = el("div", "", "row");
    row.append(el("span", label));
    const value = el("strong", "—");
    value.id = id;
    row.append(value);
    section.append(row);
  }

  function installSection() {
    if (document.getElementById("searchAsyncMonitorSection")) return document.getElementById("searchAsyncMonitorSection");
    const section = el("section");
    section.id = "searchAsyncMonitorSection";
    section.append(el("h2", "Deferred Search — прогресс"));
    addRow(section, "Job", "searchAsyncJob");
    addRow(section, "Состояние", "searchAsyncState");
    addRow(section, "Обработано", "searchAsyncProcessed");
    addRow(section, "Успешно", "searchAsyncSucceeded");
    addRow(section, "Осталось запросов", "searchAsyncRemaining");
    addRow(section, "Ожидают Яндекс", "searchAsyncWaiting");
    addRow(section, "В очереди / работе", "searchAsyncPendingWorking");
    addRow(section, "Ошибки / неопределено", "searchAsyncIssues");
    addRow(section, "Получено SERP-строк", "searchAsyncRows");
    addRow(section, "Ответов нормализовано", "searchAsyncNormalized");
    addRow(section, "Следующая проверка", "searchAsyncNextPoll");
    addRow(section, "Прошло", "searchAsyncElapsed");
    addRow(section, "Локальная ревизия", "searchAsyncRevision");
    const actions = el("div", "", "actions");
    const refresh = el("button", "Обновить статус");
    refresh.id = "searchAsyncRefresh";
    refresh.type = "button";
    actions.append(refresh);
    section.append(actions);
    section.append(el("p", "Только локальное чтение сохранённого job. Этот блок не делает запросов к Яндексу и не запускает polling.", "warning"));

    const sections = Array.from(document.querySelectorAll("main > section"));
    const runSection = sections.find((node) => node.querySelector("h2")?.textContent?.trim() === "Текущий запуск");
    if (runSection?.parentNode) runSection.parentNode.insertBefore(section, runSection.nextSibling);
    else document.querySelector("main")?.append(section);
    return section;
  }

  function setText(id, value) {
    const node = document.getElementById(id);
    if (node) node.textContent = String(value ?? "—");
  }

  function currentConversationKey() {
    const text = String(document.getElementById("conversationMeta")?.textContent || "").trim();
    return UNKNOWN_CONVERSATION.has(text) ? "" : text;
  }

  let latestSnapshot = null;
  let loading = false;

  function render(snapshot, now = Date.now()) {
    latestSnapshot = snapshot || null;
    if (!snapshot) {
      setText("searchAsyncJob", "—");
      setText("searchAsyncState", "Нет локального deferred Search job");
      for (const id of ["searchAsyncProcessed", "searchAsyncSucceeded", "searchAsyncRemaining", "searchAsyncWaiting", "searchAsyncPendingWorking", "searchAsyncIssues", "searchAsyncRows", "searchAsyncNormalized", "searchAsyncNextPoll", "searchAsyncElapsed", "searchAsyncRevision"]) setText(id, "—");
      return;
    }
    const metrics = computeMetrics(snapshot);
    setText("searchAsyncJob", snapshot.job_id || "—");
    setText("searchAsyncState", metrics.state);
    setText("searchAsyncProcessed", `${metrics.terminal} / ${metrics.total} — ${formatPercent(metrics.processed_percent)}`);
    setText("searchAsyncSucceeded", `${metrics.succeeded} / ${metrics.total} — ${formatPercent(metrics.success_percent)}`);
    setText("searchAsyncRemaining", metrics.remaining);
    setText("searchAsyncWaiting", metrics.waiting);
    setText("searchAsyncPendingWorking", `${metrics.pending} / ${metrics.working}`);
    setText("searchAsyncIssues", `${metrics.failed + metrics.parse_failed} / ${metrics.unknown}`);
    setText("searchAsyncRows", metrics.result_row_count);
    setText("searchAsyncNormalized", `${metrics.normalized_items} / ${metrics.total}`);
    setText("searchAsyncNextPoll", formatNextCheck(snapshot, now));
    setText("searchAsyncElapsed", snapshot.created_at ? formatDuration(now - snapshot.created_at) : "—");
    setText("searchAsyncRevision", snapshot.revision);
  }

  async function refreshSnapshot() {
    if (loading) return latestSnapshot;
    const owner = currentConversationKey();
    if (!owner) { render(null); return null; }
    loading = true;
    const button = document.getElementById("searchAsyncRefresh");
    if (button) button.disabled = true;
    try {
      const snapshot = await snapshotForOwner(owner, Date.now());
      render(snapshot);
      return snapshot;
    } catch (error) {
      if (error?.code === "ASYNC_MONITOR_DB_MISSING") { render(null); return null; }
      setText("searchAsyncState", `Ошибка локального чтения: ${error?.code || error?.message || error}`);
      return null;
    } finally {
      loading = false;
      if (button) button.disabled = false;
    }
  }

  function bootstrap() {
    installSection();
    document.getElementById("searchAsyncRefresh")?.addEventListener("click", () => { void refreshSnapshot(); });
    let previousOwner = "";
    setInterval(() => {
      const owner = currentConversationKey();
      if (owner && owner !== previousOwner) {
        previousOwner = owner;
        void refreshSnapshot();
      }
      if (latestSnapshot) render(latestSnapshot, Date.now());
    }, 1000);
    setInterval(() => { if (currentConversationKey()) void refreshSnapshot(); }, REFRESH_MS);
    void refreshSnapshot();
  }

  if (globalThis.__YMB_ASYNC_MONITOR_TEST__ === true) {
    globalThis.__YMB_ASYNC_MONITOR_TEST_API__ = Object.freeze({ computeMetrics, formatPercent, formatDuration, formatNextCheck });
    return;
  }

  if (typeof document !== "undefined") bootstrap();
})();
