/* global BB2ConversationIdentity, BB2ComposerSend, YMBChatGPTFileAttachment */
(() => {
  "use strict";

  const RUNTIME_KEY = "__YMB_FILE_DELIVERY_CONTENT_V4__";
  const LEGACY_RUNTIME_KEYS = ["__YMB_FILE_DELIVERY_CONTENT_V3__", "__YMB_FILE_DELIVERY_CONTENT_V2__"];
  const OUTBOX_STORAGE_KEY = "wsmb_outbox";
  const RECOVERY_POLL_MS = 60_000;
  const ATTACH_READY_TIMEOUT_MS = 60_000;
  const COMMITTED_RECONCILE_MS = 30_000;
  const SEND_TARGET_TIMEOUT_MS = 30_000;
  const SEND_RECONCILE_TIMEOUT_MS = 120_000;
  const PRE_SEND_PHASES = new Set(["claimed", "attachment_committed", "attachment_ready"]);
  const TERMINAL_PHASES = new Set(["committed", "attachment_failed"]);
  const LOCAL_STOP_CODES = new Set(["ATTACHMENT_LOCAL_PAUSE", "ATTACHMENT_RUNTIME_STOPPED", "ATTACHMENT_CONVERSATION_CHANGED"]);

  const previous = globalThis[RUNTIME_KEY];
  if (previous?.dispose) { try { previous.dispose(); } catch {} }
  for (const key of LEGACY_RUNTIME_KEYS) {
    const legacy = globalThis[key];
    if (legacy?.dispose) { try { legacy.dispose(); } catch {} }
    try { delete globalThis[key]; } catch {}
  }

  const runtime = {
    disposed: false,
    timer: null,
    timer_due: 0,
    poll_in_flight: false,
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

  function safeAttachmentName(value) {
    return String(value || "").replace(/[\u0000-\u001f\u007f]/g, "").replace(/\s+/g, " ").trim().slice(0, 180);
  }

  function deliveryText(entry) {
    const explicit = String(entry?.delivery_text || "").trim();
    if (explicit) return explicit;
    const names = (entry?.artifact_descriptors || []).map((item) => safeAttachmentName(item?.filename)).filter(Boolean);
    if (names.length === 1) return `Yandex Marketing Bridge: результат прикреплён файлом ${names[0]}.`;
    if (names.length > 1) return `Yandex Marketing Bridge: результаты прикреплены файлами: ${names.join(", ")}.`;
    return "Yandex Marketing Bridge: результат прикреплён файлом.";
  }

  function normalizedDeliveryText(entry) { return BB2ComposerSend.normalize(deliveryText(entry)); }

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
    if (!current() || entry?.conversation_key !== conversationKey() || TERMINAL_PHASES.has(entry.phase) || entry.phase === "attachment_send_committed") { removeDeliveryControl(); return; }
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
        const response = await sendWorker({ type: "WS_SET_ATTACHMENT_PAUSED", conversation_key: entry.conversation_key, delivery_id: entry.delivery_id, paused: !paused });
        if (!response?.ok) throw new Error(response?.code || "Не удалось сохранить остановку");
        if (!current() || entry.conversation_key !== conversationKey()) return;
        runtime.local_pause_id = response.paused ? entry.delivery_id : null;
        status(response.paused ? "Доставка остановлена. Файл, результат и учёт запроса сохранены. Уже отправленное сообщение не отзывается." :
          "Наблюдение продолжено. Повторное прикрепление после зафиксированной попытки запрещено.", "info", 0);
        showDeliveryControl({ ...entry, delivery_paused: response.paused });
        schedulePoll(25);
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
      const response = await sendWorker({ type: "WS_GET_OUTBOX_ARTIFACT_CHUNK", conversation_key: entry.conversation_key, delivery_id: entry.delivery_id, artifact_key: descriptor.artifact_key, chunk_index: index }, entry.delivery_signal);
      assertEntryContext(entry);
      if (!response?.ok) throw Object.assign(new Error(response?.error || response?.code || "Не удалось получить часть файла."), { code: response?.code || "ATTACHMENT_CHUNK_FAILED" });
      const bytes = YMBChatGPTFileAttachment.base64ToBytes(response.chunk_base64 || "");
      if (String(response.artifact_key || "") !== String(descriptor.artifact_key || "") || Number(response.chunk_index) !== index || Number(response.total_byte_length) !== total) throw Object.assign(new Error("Метаданные части файла не совпали."), { code: "ATTACHMENT_CHUNK_METADATA_MISMATCH" });
      if (bytes.byteLength !== Number(expected.byte_length) || bytes.byteLength !== Number(response.byte_length) || offset + bytes.byteLength > full.byteLength) throw Object.assign(new Error("Размер части файла не совпал."), { code: "ATTACHMENT_CHUNK_LENGTH_MISMATCH" });
      const sha = await sha256Hex(bytes);
      assertEntryContext(entry);
      if (sha !== String(expected.sha256 || "").toLowerCase() || sha !== String(response.sha256 || "").toLowerCase()) throw Object.assign(new Error("SHA-256 части файла не совпал."), { code: "ATTACHMENT_CHUNK_SHA256_MISMATCH" });
      full.set(bytes, offset); offset += bytes.byteLength;
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
    const actual = BB2ComposerSend.normalize(BB2ComposerSend.readComposer(composer));
    const expected = normalizedDeliveryText(entry);
    if (actual && actual !== expected) return false;
    return composer;
  }

  function stageMarker(entry) {
    assertEntryContext(entry);
    const composer = composerFreeFor(entry);
    if (!composer) throw Object.assign(new Error(composer === false ? "Поле ввода занято вашим текстом." : "Поле ввода ChatGPT не найдено."), { code: composer === false ? "COMPOSER_CONTAINS_OTHER_TEXT" : "COMPOSER_NOT_FOUND" });
    if (!BB2ComposerSend.normalize(BB2ComposerSend.readComposer(composer))) BB2ComposerSend.setComposerText(composer, deliveryText(entry));
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

  function userTurns() {
    const seen = new Set(); const result = [];
    for (const selector of ['[data-message-author-role="user"]', '[data-testid^="conversation-turn-"] [data-message-author-role="user"]']) {
      for (const node of document.querySelectorAll(selector)) if (!seen.has(node)) { seen.add(node); result.push(node); }
    }
    return result;
  }

  function turnSurfaceText(node) {
    if (!(node instanceof Element)) return "";
    const root = node.closest('[data-testid^="conversation-turn-"], [data-message-id]') || node;
    const parts = [root.textContent || "", root.getAttribute("aria-label") || "", root.getAttribute("title") || ""];
    for (const item of root.querySelectorAll('[aria-label], [title]')) parts.push(item.getAttribute("aria-label") || "", item.getAttribute("title") || "");
    return BB2ComposerSend.normalize(parts.join(" "));
  }

  function turnIdentity(node, index) {
    if (!(node instanceof Element)) return `missing:${index}`;
    const root = node.closest('[data-testid^="conversation-turn-"], [data-message-id]') || node;
    const explicit = root.getAttribute("data-message-id") || root.getAttribute("data-testid") || root.id || node.getAttribute("data-message-id") || node.getAttribute("data-testid") || node.id;
    return explicit ? `id:${explicit}` : `fallback:${index}:${turnSurfaceText(root).slice(0, 1600)}`;
  }

  function captureUserTurnIds() { return userTurns().map((node, index) => turnIdentity(node, index)); }

  function matchingNewUserTurn(entry) {
    const baseline = new Set((entry.baseline_message_ids || []).map(String));
    const marker = BB2ComposerSend.normalize(entry.send_marker || deliveryText(entry));
    const filenames = (entry.expected_attachment_names || entry.artifact_descriptors?.map((item) => item.filename) || []).map(String).filter(Boolean);
    const turns = userTurns();
    for (let index = 0; index < turns.length; index += 1) {
      const node = turns[index]; const id = turnIdentity(node, index);
      if (baseline.has(id)) continue;
      const surface = turnSurfaceText(node);
      if (marker && !surface.includes(marker)) continue;
      if (filenames.some((filename) => !surface.includes(filename))) continue;
      return { node, id };
    }
    return null;
  }

  async function waitForMatchingNewUserTurn(entry, timeoutMs) {
    const deadline = Date.now() + timeoutMs;
    while (entryCurrent(entry) && Date.now() < deadline) {
      const match = matchingNewUserTurn(entry);
      if (match) return match;
      await sleep(250);
    }
    return null;
  }

  function sendDeps(entry, descriptors, profile) {
    return {
      resolveContext: () => BB2ComposerSend.resolveContext(document),
      resolveButton: () => BB2ComposerSend.findSendButton(document, profile),
      candidateButtons: (context) => BB2ComposerSend.sendCandidates(context?.form || document, profile),
      visible: BB2ComposerSend.visible,
      disabled: BB2ComposerSend.disabled,
      readComposerText: BB2ComposerSend.readComposer,
      fingerprint: BB2ComposerSend.targetFingerprint,
      requireAttachmentReady: () => YMBChatGPTFileAttachment.attachmentReady(descriptors, document),
      sendBlockedReason: (button) => {
        const text = `${button?.getAttribute?.("aria-label") || ""} ${button?.getAttribute?.("title") || ""}`;
        return /(?:uploading|processing|preparing|загруз|обработ|подготов)/i.test(text) ? "SEND_BLOCKED_BY_UPLOAD" : "";
      },
      sleep
    };
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
    const ready = await sendWorker({ type: "WS_MARK_ATTACHMENT_READY", conversation_key: currentEntry.conversation_key, delivery_id: currentEntry.delivery_id, attached_filenames: built.descriptors.map((item) => String(item.filename)) }, entry.delivery_signal);
    if (!ready?.ok) throw Object.assign(new Error(ready?.error || ready?.code || "Attachment ready ack failed."), { code: ready?.code || "ATTACHMENT_READY_ACK_FAILED" });
    status("Яндекс: файл прикреплён и готов к отправке.", "success", 3500);
  }

  async function processAttachmentCommitted(entry) {
    const descriptors = Array.isArray(entry.artifact_descriptors) ? entry.artifact_descriptors : [];
    if (!descriptors.length) throw Object.assign(new Error("Metadata вложения потеряна."), { code: "ATTACHMENT_DESCRIPTORS_EMPTY" });
    if (!YMBChatGPTFileAttachment.attachmentReady(descriptors, document)) {
      const committedAt = Date.parse(entry.attachment_committed_at || "") || 0;
      if (committedAt && Date.now() - committedAt > COMMITTED_RECONCILE_MS) {
        throw Object.assign(new Error("Attachment уже committed, но существующее вложение не подтверждено. Автоповтор запрещён."), { code: "ATTACH_OUTCOME_UNKNOWN_NO_RETRY" });
      }
      return;
    }
    stageMarker(entry);
    const ready = await sendWorker({ type: "WS_MARK_ATTACHMENT_READY", conversation_key: entry.conversation_key, delivery_id: entry.delivery_id, attached_filenames: descriptors.map((item) => String(item.filename)) }, entry.delivery_signal);
    if (!ready?.ok) throw Object.assign(new Error(ready?.error || ready?.code || "Attachment ready ack failed."), { code: ready?.code || "ATTACHMENT_READY_ACK_FAILED" });
  }

  async function confirmSend(entry, match) {
    const response = await sendWorker({ type: "WS_CONFIRM_ATTACHMENT_SEND", conversation_key: entry.conversation_key, delivery_id: entry.delivery_id, confirmation_message_id: match?.id || null }, entry.delivery_signal);
    if (!response?.ok) throw Object.assign(new Error(response?.error || response?.code || "Send confirmation failed."), { code: response?.code || "ATTACHMENT_CONFIRM_FAILED" });
    disarmManualSend(); removeDeliveryControl();
    status("Яндекс: сообщение с файлом подтверждено в чате.", "success", 3500);
    return response;
  }

  async function reconcileSendCommitted(entry, waitMs = 0) {
    disarmManualSend(); removeDeliveryControl();
    const match = waitMs > 0 ? await waitForMatchingNewUserTurn(entry, waitMs) : matchingNewUserTurn(entry);
    if (match) { await confirmSend(entry, match); return true; }
    status("Яндекс: попытка Send уже зафиксирована. Подтверждения нового сообщения пока нет; автоматический повтор Send запрещён.", "error", 0);
    return false;
  }

  async function rollbackSendBeforeClick(entry, reason) {
    const response = await sendWorker({ type: "WS_ROLLBACK_ATTACHMENT_SEND", conversation_key: entry.conversation_key, delivery_id: entry.delivery_id, reason: String(reason || "pre_click_validation_failed") }, entry.delivery_signal);
    if (!response?.ok) throw Object.assign(new Error(response?.code || "Send rollback failed."), { code: response?.code || "ATTACHMENT_SEND_ROLLBACK_FAILED" });
    return response;
  }

  async function commitAndClick(entry, profile, stableTarget = null) {
    const deliveryId = String(entry?.delivery_id || "");
    if (!entryCurrent(entry) || !deliveryId || runtime.send_in_flight.has(deliveryId)) return;
    runtime.send_in_flight.add(deliveryId);
    let durableEntry = null;
    let methodCalled = false;
    try {
      const descriptors = Array.isArray(entry.artifact_descriptors) ? entry.artifact_descriptors : [];
      stageMarker(entry);
      const expectedText = deliveryText(entry);
      const deps = sendDeps(entry, descriptors, profile);
      const target = stableTarget || await BB2ComposerSend.waitForValidatedTarget({ expectedText, timeoutMs: SEND_TARGET_TIMEOUT_MS, sampleIntervalMs: 120, requiredStableSamples: 3, deps });
      if (!target) { status("Яндекс: стабильная готовая кнопка Send не подтверждена. Ничего не отправлено.", "error", 5000); return; }
      assertEntryContext(entry);
      const baseline = captureUserTurnIds();
      const commit = await sendWorker({
        type: "WS_COMMIT_ATTACHMENT_SEND",
        conversation_key: entry.conversation_key,
        delivery_id: deliveryId,
        send_marker: expectedText,
        baseline_message_ids: baseline,
        expected_attachment_names: descriptors.map((item) => String(item.filename)),
        send_target_fingerprint: target.snapshot?.button_fingerprint || BB2ComposerSend.targetFingerprint(target.button)
      }, entry.delivery_signal);
      if (!commit?.ok) throw Object.assign(new Error(commit?.error || commit?.code || "Send commit failed."), { code: commit?.code || "ATTACHMENT_SEND_COMMIT_FAILED" });
      durableEntry = { ...(commit.outbox || entry), delivery_signal: entry.delivery_signal };
      disarmManualSend();
      if (commit.already_confirmed) return;
      if (commit.already_committed) { await reconcileSendCommitted(durableEntry, 0); return; }
      assertEntryContext(durableEntry);

      const alreadySent = matchingNewUserTurn(durableEntry);
      if (alreadySent) { await confirmSend(durableEntry, alreadySent); return; }

      const freshContext = deps.resolveContext();
      const freshButton = freshContext ? deps.resolveButton(freshContext) : null;
      const freshTarget = freshContext && freshButton ? { context: freshContext, button: freshButton } : null;
      const finalValidation = BB2ComposerSend.validateTarget(freshTarget, expectedText, deps);
      if (!finalValidation.ok) {
        await rollbackSendBeforeClick(durableEntry, finalValidation.code);
        status(`Яндекс: Send изменился до клика (${finalValidation.code}). Клика не было; разрешена новая безопасная проверка.`, "error", 5000);
        return;
      }
      if (!YMBChatGPTFileAttachment.attachmentReady(descriptors, document)) {
        await rollbackSendBeforeClick(durableEntry, "ATTACHMENT_NOT_READY_PRE_CLICK");
        status("Яндекс: вложение перестало быть готовым до клика. Клика не было.", "error", 0);
        return;
      }
      assertEntryContext(durableEntry);

      let clickResult;
      try {
        clickResult = BB2ComposerSend.clickSynchronously({ target: freshTarget, expectedText, deps });
        methodCalled = clickResult?.method_called === true;
      } catch (error) {
        methodCalled = error?.method_called === true;
        if (!methodCalled) {
          await rollbackSendBeforeClick(durableEntry, error?.code || "PRE_CLICK_FAILURE");
          throw error;
        }
        status("Яндекс: вызов Send уже произошёл, но его исход не подтверждён. Повторный Send запрещён; выполняется только сверка чата.", "error", 0);
      }

      if (methodCalled) {
        const clickAck = await sendWorker({
          type: "WS_MARK_ATTACHMENT_CLICK_DISPATCHED",
          conversation_key: durableEntry.conversation_key,
          delivery_id: durableEntry.delivery_id,
          send_click_trace: clickResult?.trace || null
        }, durableEntry.delivery_signal).catch(() => null);
        if (clickAck?.outbox) durableEntry = { ...clickAck.outbox, delivery_signal: entry.delivery_signal };
      }

      const match = await waitForMatchingNewUserTurn(durableEntry, SEND_RECONCILE_TIMEOUT_MS);
      if (match) await confirmSend(durableEntry, match);
      else status("Яндекс: Send был вызван, но новый user-turn не подтверждён за 120 секунд. Автоматический повтор Send запрещён; состояние сохранено для дальнейшей сверки.", "error", 0);
    } finally {
      runtime.send_in_flight.delete(deliveryId);
    }
  }

  async function processReady(entry) {
    assertEntryContext(entry);
    const descriptors = Array.isArray(entry.artifact_descriptors) ? entry.artifact_descriptors : [];
    if (!YMBChatGPTFileAttachment.attachmentReady(descriptors, document)) {
      throw Object.assign(new Error("Вложение больше не подтверждается в ChatGPT. Автоповтор прикрепления запрещён."), { code: "ATTACHMENT_NOT_READY_NO_RETRY" });
    }
    stageMarker(entry);
    const state = await sendWorker({ type: "WS_GET_STATE", conversation_key: entry.conversation_key }, entry.delivery_signal);
    assertEntryContext(entry);
    const profile = state?.state?.send_button_profile || null;
    const expectedText = deliveryText(entry);
    const deps = sendDeps(entry, descriptors, profile);
    const target = await BB2ComposerSend.waitForValidatedTarget({ expectedText, timeoutMs: SEND_TARGET_TIMEOUT_MS, sampleIntervalMs: 120, requiredStableSamples: 3, deps });
    if (!target) { status("Яндекс: стабильная готовая кнопка Send пока не подтверждена.", "error", 5000); return; }
    assertEntryContext(entry);
    if (state?.state?.auto_send === false) {
      if (runtime.manual_button === target.button && runtime.manual_handler) return;
      disarmManualSend();
      const handler = (event) => {
        event.preventDefault(); event.stopPropagation(); event.stopImmediatePropagation();
        void commitAndClick(entry, profile).catch((error) => status(`Яндекс: ${error.message || error}`, "error", 0));
      };
      target.button.addEventListener("click", handler, true);
      runtime.manual_button = target.button; runtime.manual_handler = handler;
      status("Яндекс: файл готов. Ваш клик Send будет проведён через exactly-once барьер.", "success", 0);
      return;
    }
    await commitAndClick(entry, profile, target);
  }

  async function persistFailurePause(entry, error) {
    if (!PRE_SEND_PHASES.has(entry?.phase)) return { ok: false, skipped: true, code: "ATTACHMENT_FAILURE_AFTER_SEND_BARRIER" };
    const response = await sendWorker({
      type: "WS_SET_ATTACHMENT_PAUSED",
      conversation_key: entry.conversation_key,
      delivery_id: entry.delivery_id,
      paused: true
    });
    if (!response?.ok) return response || { ok: false, code: "ATTACHMENT_FAILURE_PAUSE_EMPTY_RESPONSE" };
    runtime.local_pause_id = entry.delivery_id;
    runtime.controller?.abort();
    disarmManualSend();
    return { ...response, failure_code: String(error?.code || "ATTACHMENT_DELIVERY_FAILED") };
  }

  async function processEntry(entry) {
    const key = String(entry?.delivery_id || "");
    if (!key || runtime.in_flight.has(key) || entry.delivery_paused === true || runtime.local_pause_id === key) return;
    if (runtime.controller_id !== key || !runtime.controller || runtime.controller.signal.aborted) {
      runtime.controller?.abort(); runtime.controller = new AbortController(); runtime.controller_id = key;
    }
    entry = { ...entry, delivery_signal: runtime.controller.signal };
    runtime.in_flight.add(key);
    try {
      if (entry.phase === "claimed") await processClaimed(entry);
      else if (entry.phase === "attachment_committed") await processAttachmentCommitted(entry);
      else if (entry.phase === "attachment_ready") await processReady(entry);
      else if (entry.phase === "attachment_send_committed") await reconcileSendCommitted(entry, 0);
    } catch (error) {
      const code = String(error?.code || "ATTACHMENT_DELIVERY_FAILED");
      if (!LOCAL_STOP_CODES.has(code) && PRE_SEND_PHASES.has(entry.phase)) {
        let pause;
        try { pause = await persistFailurePause(entry, error); }
        catch (pauseError) { pause = { ok: false, code: pauseError?.code || "ATTACHMENT_FAILURE_PAUSE_FAILED", error: pauseError?.message || String(pauseError) }; }
        if (pause?.ok) {
          status(`Яндекс: файловая доставка остановлена и сохранена в паузе — ${error.message || error}. Автоматического повтора не будет.`, "error", 0);
        } else if (pause?.code === "ATTACHMENT_SEND_ALREADY_COMMITTED") {
          disarmManualSend();
          status("Яндекс: Send-barrier уже зафиксирован. Pause/повтор запрещены; выполняется только сверка результата отправки.", "error", 0);
          schedulePoll(25);
        } else {
          runtime.local_pause_id = key;
          runtime.controller?.abort();
          disarmManualSend();
          status(`Яндекс: файловая доставка остановлена локально — ${error.message || error}. Durable pause не подтверждена (${pause?.code || "UNKNOWN"}); автоматический повтор в этой вкладке заблокирован.`, "error", 0);
        }
      } else {
        status(`Яндекс: файловая доставка остановлена безопасно — ${error.message || error}`, "error", 0);
      }
    } finally { runtime.in_flight.delete(key); }
  }

  function schedulePoll(delayMs) {
    if (!current()) return;
    const delay = Math.max(0, Number(delayMs || 0));
    const due = Date.now() + delay;
    if (runtime.timer && runtime.timer_due && runtime.timer_due <= due) return;
    if (runtime.timer) clearTimeout(runtime.timer);
    runtime.timer_due = due;
    runtime.timer = setTimeout(() => {
      runtime.timer = null;
      runtime.timer_due = 0;
      void poll();
    }, delay);
  }

  async function poll() {
    if (!current()) return;
    if (runtime.poll_in_flight) { schedulePoll(100); return; }
    runtime.poll_in_flight = true;
    try {
      const key = conversationKey();
      if (key) {
        const response = await sendWorker({ type: "WS_GET_OUTBOX", conversation_key: key });
        const entry = response?.outbox || null;
        if (entry?.delivery_mode === "attachment_v2" && !TERMINAL_PHASES.has(entry.phase)) {
          showDeliveryControl(entry);
          if (entry.delivery_paused === true) { runtime.local_pause_id = entry.delivery_id; runtime.controller?.abort(); disarmManualSend(); }
          else await processEntry(entry);
        } else {
          disarmManualSend(); removeDeliveryControl(); runtime.local_pause_id = null;
          runtime.controller?.abort(); runtime.controller = null; runtime.controller_id = null;
        }
      } else removeDeliveryControl();
    } catch {
      // Worker/page can be restarting. Recovery reads are event-driven with a bounded fallback.
    } finally {
      runtime.poll_in_flight = false;
      schedulePoll(RECOVERY_POLL_MS);
    }
  }

  function onStorageChanged(changes, areaName) {
    if (areaName === "local" && changes && Object.hasOwn(changes, OUTBOX_STORAGE_KEY)) schedulePoll(25);
  }

  function onComposerInput(event) {
    if (!runtime.control_button) return;
    const composer = BB2ComposerSend.findComposer(document);
    if (!composer) return;
    const target = event?.target;
    if (target === composer || composer.contains?.(target)) schedulePoll(50);
  }

  try { chrome.storage.onChanged.addListener(onStorageChanged); } catch {}
  document.addEventListener("input", onComposerInput, true);

  runtime.dispose = () => {
    if (runtime.disposed) return;
    runtime.disposed = true;
    runtime.controller?.abort(); runtime.controller = null;
    removeDeliveryControl();
    if (runtime.timer) clearTimeout(runtime.timer);
    runtime.timer = null; runtime.timer_due = 0; disarmManualSend();
    try { chrome.storage.onChanged.removeListener(onStorageChanged); } catch {}
    document.removeEventListener("input", onComposerInput, true);
    const node = document.getElementById("ymb-file-delivery-status");
    if (node) node.remove();
    try { if (globalThis[RUNTIME_KEY] === runtime) delete globalThis[RUNTIME_KEY]; } catch {}
  };

  schedulePoll(250);
})();
