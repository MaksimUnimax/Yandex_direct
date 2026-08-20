/* global BB2ConversationIdentity, BB2ManualControls, WordstatProtocol, SearchProtocol, BB2ComposerSend, BB2ProvenWritingCapture, YMBProduct, YMBServiceRegistry */
(() => {
  "use strict";

  const VERSION = YMBProduct.VERSION;
  const SURFACE_ID = "ymb-external-action-surface";
  const STATUS_KEYS = Object.freeze({
    OPERATION: "operation-state",
    COMPOSER: "composer-occupied",
    AUTORUN: "autorun-state",
    PICKER: "picker-state"
  });
  const POLL_MS = 450;
  const STATE_SYNC_MS = 1800;

  let identity = BB2ConversationIdentity.identityFromUrl(location.href);
  let manualEnabled = false;
  let activeService = YMBServiceRegistry.SERVICES.WORDSTAT;
  let stateSnapshot = null;
  let surfaceHost = null;
  let shadowRoot = null;
  let actionLayer = null;
  let statusLayer = null;
  let mutationObserver = null;
  let refreshScheduled = false;
  let activeAutoWatch = null;
  let autoScanTimer = null;
  let outboxTimer = null;
  let stateTimer = null;
  let lastLocationHref = location.href;
  let activeButtonPicker = null;

  const actionByBlock = new Map();
  const blockId = new WeakMap();
  const manualInFlight = new Set();
  const autorunSeen = new Set();
  const deliveryState = new Map();

  function cssEscape(value) {
    const text = String(value || "");
    if (globalThis.CSS?.escape) return CSS.escape(text);
    return Array.from(text).map((ch) => /[A-Za-z0-9_-]/.test(ch) ? ch : "_").join("");
  }

  function profileFromElement(element) {
    const el = element?.closest?.('button,[role="button"]') || element;
    if (!el || typeof el.getAttribute !== "function") throw new Error("Выбранный элемент не является кнопкой.");
    const tag = String(el.tagName || "button").toLowerCase();
    const testId = el.getAttribute("data-testid") || "";
    const aria = el.getAttribute("aria-label") || "";
    const name = el.getAttribute("name") || "";
    let selector = "";
    if (testId) selector = `${tag}[data-testid=${cssEscape(testId)}]`;
    else if (el.id) selector = `#${cssEscape(el.id)}`;
    else if (aria) selector = `${tag}[aria-label=${cssEscape(aria)}]`;
    else if (name) selector = `${tag}[name=${cssEscape(name)}]`;
    else throw new Error("У кнопки нет устойчивого идентификатора. Выберите другую кнопку.");
    return { selector, tag, data_testid: testId || null, aria_label: aria || null, name: name || null, source: "picker", captured_at: new Date().toISOString() };
  }

  function stopButtonPicker(message = "") {
    if (!activeButtonPicker) return;
    document.removeEventListener("click", activeButtonPicker.listener, true);
    clearTimeout(activeButtonPicker.timeout);
    activeButtonPicker = null;
    if (message) setStatus(STATUS_KEYS.PICKER, message, "info", 5000);
    else setStatus(STATUS_KEYS.PICKER, "");
  }

  function startButtonPicker(kind) {
    stopButtonPicker();
    const isSend = kind === "send";
    const listener = (event) => {
      event.preventDefault();
      event.stopPropagation();
      event.stopImmediatePropagation();
      let profile;
      try { profile = profileFromElement(event.target); }
      catch (error) { setStatus(STATUS_KEYS.PICKER, `Яндекс: ${error.message || error}`, "error", 7000); return; }
      stopButtonPicker();
      const type = isSend ? "WS_SAVE_SEND_BUTTON_PROFILE" : "WS_SAVE_COPY_BUTTON_PROFILE";
      void sendWorker({ type, profile }).then((response) => {
        if (!response?.ok) throw new Error(response?.error || response?.code || "Настройка кнопки не сохранена.");
        stateSnapshot = response.state || stateSnapshot;
        setStatus(STATUS_KEYS.PICKER, `Яндекс: ${isSend ? "Send" : "Copy"} сохранён.`, "ok", 5000);
      }).catch((error) => setStatus(STATUS_KEYS.PICKER, `Яндекс: ${error.message || error}`, "error", 7000));
    };
    document.addEventListener("click", listener, true);
    const timeout = setTimeout(() => stopButtonPicker("Яндекс: выбор кнопки отменён по таймауту."), 15000);
    activeButtonPicker = { kind, listener, timeout };
    setStatus(STATUS_KEYS.PICKER, `Яндекс: нажмите нужную кнопку ${isSend ? "Send" : "Copy"}. Нажатие будет перехвачено и не выполнится.`, "info");
    return true;
  }

  function protocolForService(service) {
    if (String(service || "") === YMBServiceRegistry.SERVICES.SEARCH) return SearchProtocol;
    if (String(service || "") === YMBServiceRegistry.SERVICES.WORDSTAT) return WordstatProtocol;
    return null;
  }

  function sendWorker(message) {
    return new Promise((resolve, reject) => {
      try {
        chrome.runtime.sendMessage(message, (response) => {
          const error = chrome.runtime.lastError;
          if (error) reject(new Error(error.message || String(error)));
          else resolve(response);
        });
      } catch (error) {
        reject(error);
      }
    });
  }

  function refreshIdentity() {
    if (location.href !== lastLocationHref) {
      lastLocationHref = location.href;
      identity = BB2ConversationIdentity.identityFromUrl(location.href);
      actionByBlock.clear();
      autorunSeen.clear();
    } else {
      identity = BB2ConversationIdentity.identityFromUrl(location.href);
    }
    return identity;
  }

  function currentConversationKey() {
    return refreshIdentity().conversation_key || "";
  }

  function ensureSurface() {
    if (surfaceHost?.isConnected && shadowRoot && actionLayer && statusLayer) return;
    document.getElementById(SURFACE_ID)?.remove();
    surfaceHost = document.createElement("div");
    surfaceHost.id = SURFACE_ID;
    surfaceHost.setAttribute("data-ymb-owned", "true");
    Object.assign(surfaceHost.style, {
      position: "fixed",
      inset: "0",
      width: "0",
      height: "0",
      zIndex: "2147483647",
      pointerEvents: "none"
    });
    shadowRoot = surfaceHost.attachShadow({ mode: "open" });
    const style = document.createElement("style");
    style.textContent = `
      :host { all: initial; }
      #actions { position: fixed; inset: 0; pointer-events: none; z-index: 2147483646; }
      .ymb-action {
        position: fixed; pointer-events: auto; appearance: none; border: 1px solid rgba(112,72,0,.35);
        border-radius: 8px; padding: 5px 9px; min-width: 68px; min-height: 28px;
        background: #ffd84d; color: #151515; font: 600 12px/1.2 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
        cursor: pointer; box-shadow: 0 1px 4px rgba(0,0,0,.16);
      }
      .ymb-action:hover { filter: brightness(.98); }
      .ymb-action:disabled { opacity: .58; cursor: progress; }
      #status {
        position: fixed; right: 18px; top: 18px; width: min(380px, calc(100vw - 36px));
        display: grid; gap: 6px; pointer-events: none; z-index: 2147483647;
      }
      .ymb-status {
        justify-self: end; max-width: 100%; box-sizing: border-box; padding: 7px 10px;
        border-radius: 8px; background: rgba(24,24,27,.94); color: white;
        font: 500 12px/1.35 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
        box-shadow: 0 2px 10px rgba(0,0,0,.22);
      }
      .ymb-status[data-level="error"] { background: rgba(130,24,24,.96); }
      .ymb-status[data-level="ok"] { background: rgba(24,100,54,.96); }
    `;
    actionLayer = document.createElement("div");
    actionLayer.id = "actions";
    statusLayer = document.createElement("div");
    statusLayer.id = "status";
    shadowRoot.append(style, actionLayer, statusLayer);
    (document.documentElement || document.body).appendChild(surfaceHost);
  }

  function setStatus(key, text, level = "info", ttl = 0) {
    ensureSurface();
    const safeKey = String(key || STATUS_KEYS.OPERATION);
    let node = statusLayer.querySelector(`[data-status-key="${CSS.escape(safeKey)}"]`);
    if (!text) {
      node?.remove();
      return;
    }
    if (!node) {
      node = document.createElement("div");
      node.className = "ymb-status";
      node.dataset.statusKey = safeKey;
      statusLayer.appendChild(node);
    }
    node.dataset.level = level;
    node.textContent = String(text);
    if (ttl > 0) {
      const stamp = String(Date.now());
      node.dataset.stamp = stamp;
      setTimeout(() => {
        if (node?.isConnected && node.dataset.stamp === stamp) node.remove();
      }, ttl);
    }
  }

  function stableBlockId(block) {
    let id = blockId.get(block);
    if (!id) {
      id = BB2ManualControls.makeId("block");
      blockId.set(block, id);
    }
    return id;
  }

  function normalizedCandidateBlocks() {
    const candidates = BB2ProvenWritingCapture.candidateBlocks(document).filter((block) => block?.isConnected);
    return candidates.filter((block) => !candidates.some((other) => other !== block && other.contains?.(block)));
  }

  function actionPosition(block) {
    const rect = block.getBoundingClientRect();
    const width = 78;
    const gap = 10;
    const maxLeft = Math.max(8, window.innerWidth - width - 8);
    let left = rect.right + gap;
    if (left > maxLeft) left = Math.max(8, rect.right - width);
    return {
      top: Math.max(8, Math.min(window.innerHeight - 36, rect.top + 6)),
      left: Math.max(8, Math.min(maxLeft, left)),
      visible: rect.bottom > 0 && rect.top < window.innerHeight && rect.right > 0 && rect.left < window.innerWidth
    };
  }

  async function onManualAction(block, button) {
    const key = currentConversationKey();
    if (!key || !manualEnabled || !block?.isConnected) return;
    const id = stableBlockId(block);
    if (manualInFlight.has(id)) return;
    manualInFlight.add(id);
    button.disabled = true;
    const token = BB2ManualControls.makeId("manual-request");
    try {
      const fullBlockText = BB2ProvenWritingCapture.textFromBlock(block);
      setStatus(STATUS_KEYS.OPERATION, `Яндекс: выполняю ${activeService}.`);
      const response = await sendWorker({
        type: "WS_EXECUTE_MANUAL_BLOCK",
        conversation_key: key,
        block_text: fullBlockText,
        manual_request_token: token
      });
      if (!response?.ok || response?.accepted === false) {
        setStatus(STATUS_KEYS.OPERATION, `Яндекс: ${response?.error || response?.code || "команда не принята"}`, "error", 9000);
      } else {
        setStatus(STATUS_KEYS.OPERATION, "Яндекс: результат подготовлен к отправке.", "ok", 4500);
        scheduleOutboxPoll(0);
      }
    } catch (error) {
      setStatus(STATUS_KEYS.OPERATION, `Яндекс: ${error.message || String(error)}`, "error", 9000);
    } finally {
      manualInFlight.delete(id);
      if (button?.isConnected) button.disabled = false;
    }
  }

  function createAction(block) {
    ensureSurface();
    const button = document.createElement("button");
    button.type = "button";
    button.className = "ymb-action";
    button.textContent = BB2ManualControls.ACTION_LABEL;
    button.title = "Выполнить этот блок через Yandex Marketing Bridge";
    button.setAttribute(BB2ManualControls.ACTION_ATTR, "true");
    button.dataset.blockId = stableBlockId(block);
    button.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      void onManualAction(block, button);
    });
    actionLayer.appendChild(button);
    actionByBlock.set(block, button);
    return button;
  }

  function layoutActions() {
    if (!manualEnabled) return;
    for (const [block, button] of actionByBlock) {
      if (!block.isConnected || !button.isConnected) continue;
      const p = actionPosition(block);
      button.style.top = `${Math.round(p.top)}px`;
      button.style.left = `${Math.round(p.left)}px`;
      button.style.display = p.visible ? "" : "none";
    }
  }

  function refreshActions() {
    refreshScheduled = false;
    ensureSurface();
    if (!manualEnabled || !currentConversationKey()) {
      for (const button of actionByBlock.values()) button.remove();
      actionByBlock.clear();
      return;
    }
    const blocks = normalizedCandidateBlocks();
    const live = new Set(blocks);
    for (const [block, button] of [...actionByBlock]) {
      if (!live.has(block) || !block.isConnected) {
        button.remove();
        actionByBlock.delete(block);
      }
    }
    for (const block of blocks) {
      if (!actionByBlock.has(block)) createAction(block);
    }
    layoutActions();
  }

  function scheduleActionRefresh() {
    if (refreshScheduled) return;
    refreshScheduled = true;
    queueMicrotask(refreshActions);
  }

  function setManualState(enabled, service = activeService) {
    manualEnabled = enabled === true;
    activeService = YMBServiceRegistry.isKnownService(service) ? service : YMBServiceRegistry.SERVICES.WORDSTAT;
    if (!manualEnabled) {
      for (const button of actionByBlock.values()) button.remove();
      actionByBlock.clear();
      setStatus(STATUS_KEYS.OPERATION, "");
    } else {
      scheduleActionRefresh();
    }
  }

  function assistantTurnIdFor(block) {
    const container = BB2ProvenWritingCapture.assistantContainerFor(block);
    const explicit = container?.getAttribute?.("data-message-id")
      || container?.getAttribute?.("data-testid")
      || container?.id;
    return String(explicit || stableBlockId(block));
  }

  function scanAutorun() {
    if (!activeAutoWatch || activeAutoWatch.paused || activeAutoWatch.status !== "waiting_command") return;
    const protocol = protocolForService(activeAutoWatch.active_service);
    if (!protocol) return;
    for (const block of normalizedCandidateBlocks()) {
      const text = BB2ProvenWritingCapture.textFromBlock(block).trim();
      if (!protocol.isCommandText(text)) continue;
      const turnId = assistantTurnIdFor(block);
      if (autorunSeen.has(turnId) || activeAutoWatch.assistant_baseline_ids?.has(turnId)) continue;
      autorunSeen.add(turnId);
      setStatus(STATUS_KEYS.AUTORUN, `Яндекс ${activeAutoWatch.active_service}: выполняю команду.`);
      void sendWorker({
        type: "WS_AUTO_COMMAND",
        conversation_key: activeAutoWatch.conversation_key,
        run_id: activeAutoWatch.run_id,
        watch_id: activeAutoWatch.watch_id || null,
        assistant_turn_id: turnId,
        command_text: text
      }).then((response) => {
        if (!response?.accepted) {
          if (response?.paused) activeAutoWatch.paused = true;
          if (response?.busy) autorunSeen.delete(turnId);
          if (!response?.ignored && !response?.duplicate) {
            setStatus(STATUS_KEYS.AUTORUN, `Яндекс: ${response?.error || response?.code || "команда не принята"}`, "error", 9000);
          }
        } else {
          activeAutoWatch.status = "delivering";
          scheduleOutboxPoll(0);
        }
      }).catch((error) => {
        autorunSeen.delete(turnId);
        setStatus(STATUS_KEYS.AUTORUN, `Яндекс: ${error.message || error}`, "error", 9000);
      });
      break;
    }
  }

  function scheduleAutoScan(delay = 350) {
    clearTimeout(autoScanTimer);
    autoScanTimer = setTimeout(() => {
      scanAutorun();
      if (activeAutoWatch && !activeAutoWatch.paused) scheduleAutoScan(700);
    }, delay);
  }

  function startAutoWatch(payload) {
    const key = currentConversationKey();
    if (!key || key !== String(payload?.conversation_key || "")) return;
    setManualState(false, payload.active_service);
    activeAutoWatch = {
      run_id: String(payload.run_id || ""),
      active_service: String(payload.active_service || YMBServiceRegistry.SERVICES.WORDSTAT),
      conversation_key: key,
      watch_id: payload.watch_id || null,
      assistant_baseline_ids: new Set((payload.assistant_baseline_ids || []).map(String)),
      paused: false,
      status: "waiting_command"
    };
    autorunSeen.clear();
    scheduleAutoScan(0);
  }

  function stopAutoWatch() {
    activeAutoWatch = null;
    clearTimeout(autoScanTimer);
    autoScanTimer = null;
    setStatus(STATUS_KEYS.AUTORUN, "");
  }

  function collectAssistantTurnIds() {
    const out = [];
    for (const block of normalizedCandidateBlocks()) {
      const id = assistantTurnIdFor(block);
      if (!out.includes(id)) out.push(id);
    }
    return out;
  }

  function isBusyChat() {
    return Boolean(document.querySelector(
      'button[data-testid="stop-button"], button[aria-label*="Stop" i], button[aria-label*="Останов" i]'
    ));
  }

  function wait(ms) { return new Promise((resolve) => setTimeout(resolve, ms)); }

  async function markCommitted(entry) {
    const response = await sendWorker({
      type: "WS_MARK_DELIVERY_COMMITTED",
      conversation_key: entry.conversation_key,
      delivery_id: entry.delivery_id,
      baseline_user_turn_ids: []
    });
    return response?.ok === true;
  }

  async function completeOutbox(entry) {
    const messageType = entry.type === "manual" ? "WS_MANUAL_DELIVERY_COMPLETE" : "WS_AUTO_DELIVERY_COMPLETE";
    const response = await sendWorker({
      type: messageType,
      conversation_key: entry.conversation_key,
      delivery_id: entry.delivery_id,
      confirmation_basis: "microphone",
      assistant_baseline_ids: collectAssistantTurnIds()
    });
    return response?.ok === true;
  }

  function disarmManualSend(local) {
    const button = local?.manual_send_button || null;
    const handler = local?.manual_send_handler || null;
    if (button && handler) {
      try { button.removeEventListener("click", handler, true); } catch {}
    }
    if (local) {
      local.manual_send_button = null;
      local.manual_send_handler = null;
    }
  }

  function armManualSend(entry, local, sendButton) {
    if (!sendButton || local?.committed) return false;
    if (local.manual_send_button === sendButton && local.manual_send_handler) return true;
    disarmManualSend(local);
    const handler = (event) => {
      event.preventDefault();
      event.stopPropagation();
      event.stopImmediatePropagation();
      if (local.manual_commit_pending || local.committed) return;
      local.manual_commit_pending = true;
      void markCommitted(entry).then((ok) => {
        if (!ok) {
          setStatus(STATUS_KEYS.OPERATION, "Яндекс: отправка не подтверждена; Send заблокирован до безопасной фиксации.", "error", 9000);
          return;
        }
        local.committed = true;
        local.clicked = true;
        local.saw_busy = true;
        disarmManualSend(local);
        sendButton.click();
        setStatus(STATUS_KEYS.OPERATION, "Яндекс: результат отправлен.", "ok", 3500);
      }).catch((error) => {
        setStatus(STATUS_KEYS.OPERATION, `Яндекс: ${error.message || error}`, "error", 9000);
      }).finally(() => {
        local.manual_commit_pending = false;
      });
    };
    sendButton.addEventListener("click", handler, true);
    local.manual_send_button = sendButton;
    local.manual_send_handler = handler;
    return true;
  }

  async function handleClaimedOutbox(entry, local) {
    const composer = BB2ComposerSend.findComposer(document);
    if (!composer) {
      setStatus(STATUS_KEYS.COMPOSER, "Яндекс: поле ввода ChatGPT не найдено.", "error");
      return;
    }
    const currentText = BB2ComposerSend.readComposer(composer);
    if (currentText.trim() && currentText !== entry.report_text) {
      disarmManualSend(local);
      setStatus(STATUS_KEYS.COMPOSER, "Яндекс ждёт: поле ввода занято вашим текстом.");
      return;
    }
    setStatus(STATUS_KEYS.COMPOSER, "");
    if (!local.injected) {
      BB2ComposerSend.setComposerText(composer, entry.report_text);
      local.injected = true;
      await wait(60);
    }
    const autoSend = stateSnapshot?.auto_send !== false;
    if (!autoSend) {
      let manualSendButton = BB2ComposerSend.findSendButton(document, stateSnapshot?.send_button_profile || null);
      for (let i = 0; !manualSendButton && i < 4; i += 1) {
        await wait(80);
        manualSendButton = BB2ComposerSend.findSendButton(document, stateSnapshot?.send_button_profile || null);
      }
      if (manualSendButton) armManualSend(entry, local, manualSendButton);
      setStatus(STATUS_KEYS.OPERATION, "Яндекс: результат помещён в поле ввода. Отправьте его, когда будете готовы.", "ok");
      return;
    }
    disarmManualSend(local);
    let sendButton = BB2ComposerSend.findSendButton(document, stateSnapshot?.send_button_profile || null);
    for (let i = 0; !sendButton && i < 4; i += 1) {
      await wait(80);
      sendButton = BB2ComposerSend.findSendButton(document, stateSnapshot?.send_button_profile || null);
    }
    if (!sendButton) {
      setStatus(STATUS_KEYS.COMPOSER, "Яндекс: кнопка отправки пока недоступна.", "error");
      return;
    }
    if (!local.committed) {
      local.committed = await markCommitted(entry);
      if (!local.committed) {
        setStatus(STATUS_KEYS.OPERATION, "Яндекс: не удалось зафиксировать отправку; повтор заблокирован.", "error", 9000);
        return;
      }
    }
    if (!local.clicked) {
      local.clicked = true;
      sendButton.click();
      local.saw_busy = true;
      setStatus(STATUS_KEYS.OPERATION, "Яндекс: результат отправлен.", "ok", 3500);
    }
  }

  async function handleCommittedOutbox(entry, local) {
    // Committed means the Send boundary has already been crossed. Recovery is watch-only:
    // never refill the composer and never click Send a second time.
    if (isBusyChat()) local.saw_busy = true;
    const ready = BB2ComposerSend.composerReady(document, stateSnapshot?.send_button_profile || null);
    const committedAt = Date.parse(entry.committed_at || "") || 0;
    const aged = committedAt > 0 && Date.now() - committedAt >= 500;
    if (ready && (local.saw_busy || aged || local.clicked)) {
      if (!local.completed) {
        local.completed = true;
        const ok = await completeOutbox(entry);
        if (!ok) local.completed = false;
        else setStatus(STATUS_KEYS.OPERATION, "Яндекс: доставка подтверждена.", "ok", 3000);
      }
    }
  }

  async function pollOutbox() {
    outboxTimer = null;
    const key = currentConversationKey();
    if (!key) return scheduleOutboxPoll(POLL_MS);
    try {
      const response = await sendWorker({ type: "WS_GET_OUTBOX", conversation_key: key });
      const entry = response?.outbox;
      if (entry?.delivery_id) {
        const local = deliveryState.get(entry.delivery_id) || { injected: false, committed: entry.phase === "committed", clicked: false, saw_busy: false, completed: false };
        deliveryState.set(entry.delivery_id, local);
        if (entry.phase === "claimed") await handleClaimedOutbox(entry, local);
        else if (entry.phase === "committed") await handleCommittedOutbox(entry, local);
      }
    } catch (error) {
      setStatus(STATUS_KEYS.OPERATION, `Яндекс: ${error.message || error}`, "error", 5000);
    }
    scheduleOutboxPoll(POLL_MS);
  }

  function scheduleOutboxPoll(delay = POLL_MS) {
    clearTimeout(outboxTimer);
    outboxTimer = setTimeout(pollOutbox, delay);
  }

  async function syncState() {
    const key = currentConversationKey();
    if (!key) {
      setManualState(false);
      stopAutoWatch();
      return;
    }
    try {
      const response = await sendWorker({ type: "WS_GET_STATE", conversation_key: key });
      if (!response?.ok || !response.state) return;
      stateSnapshot = response.state;
      activeService = response.state.service_context?.active_service || activeService;
      const run = response.state.auto_run;
      if (run && run.conversation_key === key && !["stopped", "error"].includes(run.status)) {
        if (!activeAutoWatch || activeAutoWatch.run_id !== run.run_id) {
          startAutoWatch({
            conversation_key: key,
            run_id: run.run_id,
            active_service: run.active_service,
            watch_id: run.watch_id,
            assistant_baseline_ids: run.assistant_baseline_ids || []
          });
        }
        if (activeAutoWatch) {
          activeAutoWatch.status = run.status;
          activeAutoWatch.paused = run.status === "paused";
          if (run.status === "waiting_command") scheduleAutoScan(0);
        }
      } else if (!run || ["stopped", "error"].includes(run.status)) {
        stopAutoWatch();
      }
      if (!run || ["paused", "stopped", "error"].includes(run.status)) {
        setManualState(response.state.manual_mode === true, activeService);
      }
    } catch {
      // Worker can be restarting. Keep local UI state and retry.
    }
  }

  function scheduleStateSync() {
    clearTimeout(stateTimer);
    stateTimer = setTimeout(async () => {
      await syncState();
      scheduleStateSync();
    }, STATE_SYNC_MS);
  }

  function installObserver() {
    mutationObserver?.disconnect();
    mutationObserver = new MutationObserver(() => {
      scheduleActionRefresh();
      if (activeAutoWatch && !activeAutoWatch.paused) scheduleAutoScan(120);
    });
    mutationObserver.observe(document.documentElement || document.body, { childList: true, subtree: true });
  }

  chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
    if (message?.type === "WS_START_SEND_BUTTON_PICKER") {
      startButtonPicker("send");
      sendResponse({ ok: true, started: true });
      return false;
    }
    if (message?.type === "WS_START_COPY_BUTTON_PICKER") {
      startButtonPicker("copy");
      sendResponse({ ok: true, started: true });
      return false;
    }
    if (message?.type === "WS_GET_IDENTITY" || message?.type === "WS_PAGE_CONTEXT") {
      const current = refreshIdentity();
      sendResponse({ ok: Boolean(current.conversation_key), identity: current, conversation_key: current.conversation_key || "" });
      return false;
    }
    if (message?.type === "WS_APPLY_MANUAL_MODE") {
      const key = currentConversationKey();
      const addressed = Boolean(key && String(message.conversation_key || "") === key);
      if (!addressed) {
        setManualState(false);
        sendResponse({ ok: true, applied: false, conversation_key: key, identity });
        return false;
      }
      setManualState(message.enabled === true, message.active_service || activeService);
      sendResponse({ ok: true, applied: true, conversation_key: key, identity });
      return false;
    }
    if (message?.type === "WS_APPLY_SERVICE_CONTEXT") {
      if (String(message.conversation_key || "") === currentConversationKey() && YMBServiceRegistry.isKnownService(message.active_service)) {
        activeService = message.active_service;
        scheduleActionRefresh();
      }
      sendResponse({ ok: true });
      return false;
    }
    if (message?.type === "WS_START_AUTO_WATCH") {
      startAutoWatch(message);
      sendResponse({ ok: true });
      return false;
    }
    if (message?.type === "WS_STOP_AUTO_WATCH") {
      stopAutoWatch();
      sendResponse({ ok: true });
      return false;
    }
    if (message?.type === "WS_REFRESH_STATE") {
      void syncState().then(() => sendResponse({ ok: true })).catch((error) => sendResponse({ ok: false, error: error.message }));
      return true;
    }
    return false;
  });

  window.addEventListener("scroll", layoutActions, { passive: true, capture: true });
  window.addEventListener("resize", layoutActions, { passive: true });

  ensureSurface();
  installObserver();
  scheduleActionRefresh();
  scheduleOutboxPoll(0);
  void syncState().finally(scheduleStateSync);

  if (globalThis.__YMB_TEST__ === true) {
    globalThis.__YMB_CONTENT_TEST_API__ = Object.freeze({
      protocolForService,
      actionPosition,
      normalizedCandidateBlocks,
      setManualState,
      refreshActions,
      startAutoWatch,
      scanAutorun,
      profileFromElement,
      startButtonPicker,
      stopButtonPicker
    });
  }
})();
