/* global BB2ConversationIdentity, BB2ComposerSend, YMBChatGPTFileAttachment */
(() => {
  "use strict";

  const RUNTIME_KEY = "__YMB_FILE_DELIVERY_CONTENT_V2__";
  const POLL_MS = 900;
  const ATTACH_READY_TIMEOUT_MS = 60_000;
  const COMMITTED_RECONCILE_MS = 30_000;
  const previous = globalThis[RUNTIME_KEY];
  if (previous?.dispose) { try { previous.dispose(); } catch {} }

  const runtime = {
    disposed: false,
    timer: null,
    in_flight: new Set(),
    send_in_flight: new Set(),
    manual_button: null,
    manual_handler: null,
    local_pause_id: null,
    controller: null,
    controller_id: null,
    control_button: null,
    control_busy: false,
    dispose: null
  };
  globalThis[RUNTIME_KEY] = runtime;

  function current() { return !runtime.disposed && globalThis[RUNTIME_KEY] === runtime; }
  function sleep(ms) { return new Promise((resolve) => setTimeout(resolve, ms)); }
  function canonicalConversationUrl() { return String(document.querySelector('link[rel="canonical"]')?.href || "").trim(); }
  function identity() { return BB2ConversationIdentity.identityFromCandidates([location.href, canonicalConversationUrl()]); }
  function conversationKey() { const value = identity(); return value?.status === "confirmed" ? value.conversation_key : ""; }

  // A SPA can keep the same file input and Send button while changing chat.
  // Worker admission happened earlier; recheck the page owner after every await
  // and immediately before any DOM/file/send side effect. Never replay on failure.
  function entryCurrent(entry) {
    return current() && !entry?.delivery_signal?.aborted &&
      runtime.local_pause_id !== entry?.delivery_id && entry?.delivery_paused !== true &&
      Boolean(entry?.conversation_key) && entry.conversation_key === conversationKey();
  }
  function assertEntryContext(entry) {
    if (!entryCurrent(entry)) throw Object.assign(new Error("Диалог изменился; доставка остановлена без повторной отправки."), { code: "ATTACHMENT_CONVERSATION_CHANGED" });
  }


  function sendWorker(message, signal = null) {
    return new Promise((resolve, reject) => {
      let finished = false;
      const end = (error, response) => {
        if (finished) return;
        finished = true;
        signal?.removeEventListener("abort", abort);
        if (error) reject(error); else resolve(response);
      };
      const abort = () => end(Object.assign(new Error("Подготовка файла остановлена локально."), { code: "ATTACHMENT_LOCAL_PAUSE" }));
      if (signal?.aborted) { abort(); return; }
      signal?.addEventListener("abort", abort, { once: true });
      try {
        chrome.runtime.sendMessage(message, (response) => {
          const error = chrome.runtime.lastError;
          end(error ? new Error(error.message || String(error)) : null, response);
        });
      } catch (error) { end(error); }
    });
  }

  function removeDeliveryControl() {
    if (runtime.control_button) { runtime.control_button.onclick = null; runtime.control_button.remove(); }
    runtime.control_button = null;
  }

  function showDeliveryControl(entry) {
    if (!current() || entry?.conversation_key !== conversationKey() || entry.phase === "committed") { removeDeliveryControl(); return; }
    let button = runtime.control_button;
    if (!button?.isConnected) {
      button = document.createElement("button");
      button.id = "ymb-file-delivery-control";
      button.type = "button";
      Object.assign(button.style, { position: "fixed", right: "18px", top: "140px", zIndex: "2147483647", padding: "8px 12px" });
      document.documentElement.appendChild(button); runtime.control_button = button;
    }
    const paused = entry.delivery_paused === true;
    button.textContent = paused ? (entry.phase === "claimed" ? "Продолжить подготовку файла" : "Продолжить наблюдение за вложением") : "Остановить подготовку / отправку";
    button.title = "Не отменяет запрос Яндекса, не удаляет файл и не отзывает уже отправленное сообщение.";
    button.disabled = runtime.control_busy;
    button.onclick = async () => {
      if (runtime.control_busy || !current() || entry.conversation_key !== conversationKey()) return;
      runtime.control_busy = true; button.disabled = true;
      if (!paused) {
        runtime.local_pause_id = entry.delivery_id;
        runtime.controller?.abort();
        disarmManualSend();
      }
      try {
        const response = await sendWorker({ type: "WS_SET_ATTACHMENT_PAUSED", conversation_key: entry.conversation_key,
          delivery_id: entry.delivery_id, paused: !paused });
        if (!response?.ok) throw new Error(response?.code || "Не удалось сохранить остановку");
        if (!current() || entry.conversation_key !== conversationKey()) return;
        runtime.local_pause_id = response.paused ? entry.delivery_id : null;
        status(response.paused ? "Доставка остановлена. Файл, результат и учёт запроса сохранены. Уже отправленное сообщение не отзывается." :
          "Наблюдение продолжено. Повторное прикрепление после зафиксированной попытки запрещено.", "info", 0);
        showDeliveryControl({ ...entry, delivery_paused: response.paused });
      } catch (error) {
        if (current()) status(`Локальная подготовка остановлена, но изменение состояния не подтверждено: ${error.message}. Не считайте это отменой запроса.`, "error", 0);
      } finally {
        runtime.control_busy = false;
        if (current() && runtime.control_button) runtime.control_button.disabled = false;
      }
    };
  }

  function status(message, tone = "info", timeout = 6000) {
    let node = document.getElementById("ymb-file-delivery-status");
    if (!(node instanceof HTMLElement)) {
      node = document.createElement("div");
      node.id = "ymb-file-delivery-status";
      Object.assign(node.style, {
        position: "fixed", right: "18px", top: "82px", zIndex: "2147483646", maxWidth: "460px",
        whiteSpace: "pre-wrap", padding: "10px 12px", borderRadius: "10px", font: "13px/1.4 system-ui, sans-serif",
        boxShadow: "0 8px 24px rgba(15,23,42,.18)", pointerEvents: "none"
      });
      document.documentElement.appendChild(node);
    }
    node.textContent = String(message || "");
    node.style.background = tone === "error" ? "#fee2e2" : tone === "success" ? "#dcfce7" : "#e0f2fe";
    node.style.color = tone === "error" ? "#7f1d1d" : "#0f172a";
    if (timeout > 0) setTimeout(() => { if (node?.isConnected && node.textContent === String(message || "")) node.remove(); }, timeout);
  }

  function disarmManualSend() {
    if (runtime.manual_button && runtime.manual_handler) {
      try { runtime.manual_button.removeEventListener("click", runtime.manual_handler, true); } catch {}
    }
    runtime.manual_button = null;
    runtime.manual_handler = null;
  }

  async function sha256Hex(bytes) { return YMBChatGPTFileAttachment.sha256Hex(bytes); }

  async function fetchArtifact(entry, descriptor) {
    assertEntryContext(entry);
    const total = Number(descriptor?.byte_length || 0);
    const manifest = Array.isArray(descriptor?.chunk_manifest) ? descriptor.chunk_manifest : [];
    if (!Number.isSafeInteger(total) || total < 0 || !manifest.length) throw Object.assign(new Error("Некорректные метаданные файла."), { code: "ATTACHMENT_METADATA_INVALID" });
    const full = new Uint8Array(total);
    let offset = 0;
    for (const expected of manifest) {
      if (!current()) throw Object.assign(new Error("File delivery runtime остановлен."), { code: "ATTACHMENT_RUNTIME_STOPPED" });
      assertEntryContext(entry);
      const index = Number(expected.chunk_index);
      const response = await sendWorker({
        type: "WS_GET_OUTBOX_ARTIFACT_CHUNK",
        conversation_key: entry.conversation_key,
        delivery_id: entry.delivery_id,
        artifact_key: descriptor.artifact_key,
        chunk_index: index
      }, entry.delivery_signal);
      assertEntryContext(entry);
      if (!response?.ok) throw Object.assign(new Error(response?.error || response?.code || "Не удалось получить часть файла."), { code: response?.code || "ATTACHMENT_CHUNK_FAILED" });
      const bytes = YMBChatGPTFileAttachment.base64ToBytes(response.chunk_base64 || "");
      if (String(response.artifact_key || "") !== String(descriptor.artifact_key || "") || Number(response.chunk_index) !== index || Number(response.total_byte_length) !== total) {
        throw Object.assign(new Error("Метаданные части файла не совпали."), { code: "ATTACHMENT_CHUNK_METADATA_MISMATCH" });
      }
      if (bytes.byteLength !== Number(expected.byte_length) || bytes.byteLength !== Number(response.byte_length) || offset + bytes.byteLength > full.byteLength) {
        throw Object.assign(new Error("Размер части файла не совпал."), { code: "ATTACHMENT_CHUNK_LENGTH_MISMATCH" });
      }
      const sha = await sha256Hex(bytes);
      assertEntryContext(entry);
      if (sha !== String(expected.sha256 || "").toLowerCase() || sha !== String(response.sha256 || "").toLowerCase()) {
        throw Object.assign(new Error("SHA-256 части файла не совпал."), { code: "ATTACHMENT_CHUNK_SHA256_MISMATCH" });
      }
      full.set(bytes, offset);
      offset += bytes.byteLength;
    }
    if (offset !== total) throw Object.assign(new Error("Размер восстановленного файла не совпал."), { code: "ATTACHMENT_LENGTH_MISMATCH" });
    return full;
  }

  async function buildFiles(entry) {
    const descriptors = Array.isArray(entry.artifact_descriptors) ? entry.artifact_descriptors : [];
    if (!descriptors.length) throw Object.assign(new Error("Нет файлов для доставки."), { code: "ATTACHMENT_DESCRIPTORS_EMPTY" });
    const files = [];
    for (const descriptor of descriptors) files.push(YMBChatGPTFileAttachment.createFile(await fetchArtifact(entry, descriptor), descriptor));
    return { descriptors, files };
  }

  function composerFreeFor(entry) {
    const composer = BB2ComposerSend.findComposer(document);
    if (!composer) return null;
    const text = BB2ComposerSend.readComposer(composer);
    if (text.trim() && text !== entry.report_text) return false;
    return composer;
  }

  function stageMarker(entry) {
    assertEntryContext(entry);
    const composer = composerFreeFor(entry);
    if (!composer) throw Object.assign(new Error(composer === false ? "Поле ввода занято вашим текстом." : "Поле ввода ChatGPT не найдено."), { code: composer === false ? "COMPOSER_CONTAINS_OTHER_TEXT" : "COMPOSER_NOT_FOUND" });
    if (!BB2ComposerSend.readComposer(composer).trim()) BB2ComposerSend.setComposerText(composer, entry.report_text || "Yandex Marketing Bridge: результат прикреплён файлом.");
    return composer;
  }

  async function waitAttachmentReady(descriptors, timeoutMs, entry) {
    const deadline = Date.now() + timeoutMs;
    while (entryCurrent(entry) && Date.now() < deadline) {
      if (YMBChatGPTFileAttachment.attachmentReady(descriptors, document)) return true;
      await sleep(250);
    }
    return false;
  }

  async function processClaimed(entry) {
    assertEntryContext(entry);
    const free = composerFreeFor(entry);
    if (free === false) { status("Яндекс ждёт: поле ввода занято вашим текстом.", "info", 0); return; }
    if (!free) { status("Яндекс: поле ввода ChatGPT не найдено.", "error", 5000); return; }
    const input = YMBChatGPTFileAttachment.fileInput(document);
    if (!input) { status("Яндекс: поле прикрепления файлов ChatGPT пока недоступно.", "error", 5000); return; }

    const commit = await sendWorker({ type: "WS_MARK_ATTACHMENT_COMMITTED", conversation_key: entry.conversation_key, delivery_id: entry.delivery_id }, entry.delivery_signal);
    assertEntryContext(entry);
    if (!commit?.ok) throw Object.assign(new Error(commit?.error || commit?.code || "Attachment commit failed."), { code: commit?.code || "ATTACHMENT_COMMIT_FAILED" });
    if (commit.already_committed && commit.outbox?.phase !== "attachment_committed") return;
    const currentEntry = { ...(commit.outbox || entry), delivery_signal: entry.delivery_signal };
    const built = await buildFiles(currentEntry);
    assertEntryContext(currentEntry);
    if (YMBChatGPTFileAttachment.fileInput(document) !== input) throw Object.assign(new Error("Поле прикрепления изменилось; автоповтор запрещён."), { code: "ATTACHMENT_TARGET_CHANGED" });
    if (!input.isConnected) throw Object.assign(new Error("File input исчез после commit; автоматический повтор запрещён."), { code: "ATTACH_OUTCOME_UNKNOWN_NO_RETRY" });
    YMBChatGPTFileAttachment.setInputFiles(input, built.files);
    if (!(await waitAttachmentReady(built.descriptors, ATTACH_READY_TIMEOUT_MS, currentEntry))) throw Object.assign(new Error("ChatGPT не подтвердил готовность вложения; автоматический повтор запрещён."), { code: "ATTACH_OUTCOME_UNKNOWN_NO_RETRY" });
    stageMarker(currentEntry);
    const ready = await sendWorker({
      type: "WS_MARK_ATTACHMENT_READY",
      conversation_key: currentEntry.conversation_key,
      delivery_id: currentEntry.delivery_id,
      attached_filenames: built.descriptors.map((item) => String(item.filename))
    }, entry.delivery_signal);
    if (!ready?.ok) throw Object.assign(new Error(ready?.error || ready?.code || "Attachment ready ack failed."), { code: ready?.code || "ATTACHMENT_READY_ACK_FAILED" });
    status("Яндекс: файл прикреплён и готов к отправке.", "success", 3500);
  }

  async function processAttachmentCommitted(entry) {
    const descriptors = Array.isArray(entry.artifact_descriptors) ? entry.artifact_descriptors : [];
    if (!descriptors.length) throw Object.assign(new Error("Metadata вложения потеряна."), { code: "ATTACHMENT_DESCRIPTORS_EMPTY" });
    if (!YMBChatGPTFileAttachment.attachmentReady(descriptors, document)) {
      const committedAt = Date.parse(entry.attachment_committed_at || "") || 0;
      if (committedAt && Date.now() - committedAt > COMMITTED_RECONCILE_MS) status("Яндекс: attachment уже committed, но существующее вложение не подтверждено. Автоповтор запрещён.", "error", 0);
      return;
    }
    stageMarker(entry);
    const ready = await sendWorker({
      type: "WS_MARK_ATTACHMENT_READY",
      conversation_key: entry.conversation_key,
      delivery_id: entry.delivery_id,
      attached_filenames: descriptors.map((item) => String(item.filename))
    }, entry.delivery_signal);
    if (!ready?.ok) throw Object.assign(new Error(ready?.error || ready?.code || "Attachment ready ack failed."), { code: ready?.code || "ATTACHMENT_READY_ACK_FAILED" });
  }

  async function commitAndClick(entry, button) {
    const deliveryId = String(entry?.delivery_id || "");
    if (!entryCurrent(entry) || !deliveryId || runtime.send_in_flight.has(deliveryId)) return;
    runtime.send_in_flight.add(deliveryId);
    try {
      const response = await sendWorker({ type: "WS_COMMIT_ATTACHMENT_SEND", conversation_key: entry.conversation_key, delivery_id: deliveryId }, entry.delivery_signal);
      if (!response?.ok) throw Object.assign(new Error(response?.error || response?.code || "Send commit failed."), { code: response?.code || "ATTACHMENT_SEND_COMMIT_FAILED" });
      disarmManualSend();
      // An acknowledgement of an earlier commit is not a new permission to click.
      // A replaced/disposed page must leave the committed outbox to its watcher.
      if (response.already_committed || !entryCurrent(entry) || !button?.isConnected) return;
      button.click();
      status("Яндекс: сообщение с файлом отправлено.", "success", 3500);
    } finally {
      runtime.send_in_flight.delete(deliveryId);
    }
  }

  async function processReady(entry) {
    assertEntryContext(entry);
    const descriptors = Array.isArray(entry.artifact_descriptors) ? entry.artifact_descriptors : [];
    if (!YMBChatGPTFileAttachment.attachmentReady(descriptors, document)) {
      status("Яндекс: вложение больше не подтверждается в ChatGPT. Send заблокирован; автоповтор прикрепления запрещён.", "error", 0);
      return;
    }
    stageMarker(entry);
    const state = await sendWorker({ type: "WS_GET_STATE", conversation_key: entry.conversation_key }, entry.delivery_signal);
    const profile = state?.state?.send_button_profile || null;
    let button = BB2ComposerSend.findSendButton(document, profile);
    for (let i = 0; !button && i < 4; i += 1) { await sleep(80); button = BB2ComposerSend.findSendButton(document, profile); }
    if (!button) { status("Яндекс: кнопка Send пока недоступна.", "error", 5000); return; }
    assertEntryContext(entry);
    if (state?.state?.auto_send === false) {
      if (runtime.manual_button === button && runtime.manual_handler) return;
      disarmManualSend();
      const handler = (event) => {
        event.preventDefault(); event.stopPropagation(); event.stopImmediatePropagation();
        void commitAndClick(entry, button).catch((error) => status(`Яндекс: ${error.message || error}`, "error", 0));
      };
      button.addEventListener("click", handler, true);
      runtime.manual_button = button;
      runtime.manual_handler = handler;
      status("Яндекс: файл прикреплён. Отправьте сообщение, когда будете готовы.", "success", 0);
      return;
    }
    await commitAndClick(entry, button);
  }

  async function processEntry(entry) {
    const key = String(entry?.delivery_id || "");
    if (!key || runtime.in_flight.has(key) || entry.delivery_paused === true || runtime.local_pause_id === key) return;
    if (runtime.controller_id !== key || !runtime.controller || runtime.controller.signal.aborted) {
      runtime.controller?.abort();
      runtime.controller = new AbortController(); runtime.controller_id = key;
    }
    entry = { ...entry, delivery_signal: runtime.controller.signal };
    runtime.in_flight.add(key);
    try {
      if (entry.phase === "claimed") await processClaimed(entry);
      else if (entry.phase === "attachment_committed") await processAttachmentCommitted(entry);
      else if (entry.phase === "attachment_ready") await processReady(entry);
    } catch (error) {
      status(`Яндекс: файловая доставка остановлена безопасно — ${error.message || error}`, "error", 0);
    } finally {
      runtime.in_flight.delete(key);
    }
  }

  async function poll() {
    runtime.timer = null;
    if (!current()) return;
    try {
      const key = conversationKey();
      if (key) {
        const response = await sendWorker({ type: "WS_GET_OUTBOX", conversation_key: key });
        const entry = response?.outbox || null;
        if (entry?.delivery_mode === "attachment_v2" && entry.phase !== "committed") {
          showDeliveryControl(entry);
          if (entry.delivery_paused === true) { runtime.local_pause_id = entry.delivery_id; runtime.controller?.abort(); disarmManualSend(); }
          else await processEntry(entry);
        } else { disarmManualSend(); removeDeliveryControl(); runtime.local_pause_id = null;
          runtime.controller?.abort(); runtime.controller = null; runtime.controller_id = null;
        }
      } else removeDeliveryControl();
    } catch (error) {
      // Worker/page can be restarting; bounded polling will retry without provider work.
    }
    if (current()) runtime.timer = setTimeout(poll, POLL_MS);
  }

  runtime.dispose = () => {
    if (runtime.disposed) return;
    runtime.disposed = true;
    runtime.controller?.abort(); runtime.controller = null;
    removeDeliveryControl();
    if (runtime.timer) clearTimeout(runtime.timer);
    runtime.timer = null;
    disarmManualSend();
    const node = document.getElementById("ymb-file-delivery-status");
    if (node) node.remove();
    try { if (globalThis[RUNTIME_KEY] === runtime) delete globalThis[RUNTIME_KEY]; } catch {}
  };

  runtime.timer = setTimeout(poll, 250);
})();
