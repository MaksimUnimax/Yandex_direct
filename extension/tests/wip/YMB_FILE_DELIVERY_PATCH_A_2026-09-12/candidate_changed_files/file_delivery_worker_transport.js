/* global YMBFileArtifactStore */
(() => {
  "use strict";

  const basePutOutbox = putOutbox;
  const baseClearOutbox = clearOutbox;
  const baseHandleMessage = handleMessage;
  const baseExecuteManualBlock = executeManualBlock;
  const baseHandleAutoCommand = handleAutoCommand;
  const CHATGPT_FILE_TEXT_THRESHOLD = 1_048_000;
  const DELIVERY_MODE = "attachment_v2";

  function unicodeLengthExceeds(value, limit) {
    let count = 0;
    for (const _character of String(value ?? "")) {
      count += 1;
      if (count > limit) return true;
    }
    return false;
  }

  function safeFilename(value, fallback = "yandex-bridge-result.txt") {
    const raw = String(value || "").replace(/[\u0000-\u001f\u007f]/g, "").replace(/[\\/]/g, "_").trim();
    const clean = raw.replace(/^\.+/, "").replace(/\.{2,}/g, ".").slice(0, 180);
    return clean && clean !== "." && clean !== ".." ? clean : fallback;
  }

  function bytesToBase64(bytes) {
    const source = bytes instanceof Uint8Array ? bytes : new Uint8Array(bytes || []);
    let binary = "";
    const step = 0x8000;
    for (let offset = 0; offset < source.length; offset += step) {
      binary += String.fromCharCode(...source.subarray(offset, Math.min(source.length, offset + step)));
    }
    return btoa(binary);
  }

  async function prepareEntry(entry) {
    let next = { ...(entry || {}) };
    const deliveryId = String(next.delivery_id || uid("delivery"));
    next.delivery_id = deliveryId;
    if (Array.isArray(next.artifact_descriptors) && next.artifact_descriptors.length) return next;
    if (!unicodeLengthExceeds(next.report_text || "", CHATGPT_FILE_TEXT_THRESHOLD)) return next;

    const text = String(next.report_text || "");
    const filename = safeFilename(`yandex-bridge-${String(next.type || "result")}-${deliveryId}.txt`);
    const descriptor = await YMBFileArtifactStore.stageTextArtifact({
      artifactKey: `delivery:${deliveryId}:0`,
      deliveryId,
      filename,
      mimeType: "text/plain;charset=utf-8",
      text
    });
    return {
      ...next,
      delivery_mode: DELIVERY_MODE,
      artifact_descriptors: [descriptor],
      report_text: `Yandex Marketing Bridge: полный результат прикреплён файлом ${filename}.`
    };
  }

  putOutbox = async function fileAwarePutOutbox(conversationKey, entry) {
    const key = normalizeConversationKey(conversationKey);
    const previous = await getConversationOutbox(key);
    const entryHadArtifacts = Array.isArray(entry?.artifact_descriptors) && entry.artifact_descriptors.length > 0;
    const prepared = await prepareEntry(entry);
    const stagedHere = !entryHadArtifacts && prepared.delivery_mode === DELIVERY_MODE ? (prepared.artifact_descriptors || []) : [];
    let stored;
    try {
      stored = await basePutOutbox(key, prepared);
    } catch (error) {
      if (stagedHere.length) await YMBFileArtifactStore.cleanupDescriptors(stagedHere).catch(() => null);
      throw error;
    }
    if (previous?.delivery_mode === DELIVERY_MODE && previous.delivery_id !== stored?.delivery_id) {
      await YMBFileArtifactStore.cleanupDescriptors(previous.artifact_descriptors || []).catch(() => null);
    }
    return stored;
  };

  clearOutbox = async function fileAwareClearOutbox(conversationKey, deliveryId = null) {
    const key = normalizeConversationKey(conversationKey);
    const previous = await getConversationOutbox(key);
    await baseClearOutbox(key, deliveryId);
    if (previous?.delivery_mode === DELIVERY_MODE && (!deliveryId || previous.delivery_id === deliveryId)) {
      await YMBFileArtifactStore.cleanupDescriptors(previous.artifact_descriptors || []).catch(() => null);
    }
  };

  function compactLargeCommandResult(value) {
    if (!value || typeof value !== "object" || Array.isArray(value)) return value;
    const text = typeof value.report_text === "string" ? value.report_text : "";
    if (!unicodeLengthExceeds(text, CHATGPT_FILE_TEXT_THRESHOLD)) return value;
    const out = {};
    for (const field of [
      "ok", "accepted", "duplicate", "busy", "ignored", "paused", "skipped", "error_delivery",
      "code", "error", "reason", "request_id", "operation_id", "delivery_id", "request_executed",
      "confirmed_provider_executions", "provider_executions"
    ]) if (Object.hasOwn(value, field)) out[field] = value[field];
    out.report_text = "Yandex Marketing Bridge: большой результат сохранён для файловой доставки; полный payload не возвращается через runtime message.";
    if (value.result && typeof value.result === "object") {
      out.result = {};
      for (const field of ["ok", "request_id", "http_status", "request_executed", "automatic_retry"]) {
        if (Object.hasOwn(value.result, field)) out.result[field] = value.result[field];
      }
    }
    if (value.run && typeof value.run === "object") {
      out.run = {
        run_id: value.run.run_id || null,
        status: value.run.status || null,
        active_service: value.run.active_service || null,
        sequence: value.run.sequence ?? null
      };
    }
    return out;
  }

  executeManualBlock = async function fileAwareExecuteManualBlock(...args) {
    return compactLargeCommandResult(await baseExecuteManualBlock(...args));
  };

  handleAutoCommand = async function fileAwareHandleAutoCommand(...args) {
    return compactLargeCommandResult(await baseHandleAutoCommand(...args));
  };

  async function ownedAttachment(message, sender) {
    const key = normalizeConversationKey(message.conversation_key);
    const outbox = await getOutbox();
    const entry = outbox[key] || null;
    if (!entry || entry.delivery_id !== String(message.delivery_id || "")) return { key, entry: null, error: { ok: false, code: "DELIVERY_NOT_FOUND" } };
    const ownerFence = await outboxOwnerFence(entry, key, sender);
    if (ownerFence) return { key, entry, error: ownerFence };
    if (entry.delivery_mode !== DELIVERY_MODE) return { key, entry, error: { ok: false, code: "ATTACHMENT_MODE_REQUIRED" } };
    return { key, entry, error: null };
  }

  async function attachmentChunk(message, sender) {
    const owned = await ownedAttachment(message, sender);
    if (owned.error) return owned.error;
    const descriptor = (owned.entry.artifact_descriptors || []).find((item) => String(item.artifact_key) === String(message.artifact_key || ""));
    if (!descriptor) return { ok: false, code: "OUTBOX_ARTIFACT_NOT_DECLARED" };
    const index = Number(message.chunk_index);
    const expected = (descriptor.chunk_manifest || []).find((item) => Number(item.chunk_index) === index);
    if (!expected) return { ok: false, code: "OUTBOX_ARTIFACT_CHUNK_NOT_DECLARED" };
    const chunk = await YMBFileArtifactStore.getChunk(descriptor.artifact_key, index);
    if (chunk.byte_length !== Number(expected.byte_length) || chunk.sha256 !== String(expected.sha256 || "")) {
      return { ok: false, code: "OUTBOX_ARTIFACT_CHUNK_INTEGRITY_MISMATCH" };
    }
    return {
      ok: true,
      artifact_key: descriptor.artifact_key,
      chunk_index: index,
      byte_length: chunk.byte_length,
      sha256: chunk.sha256,
      total_byte_length: Number(descriptor.byte_length || 0),
      chunk_base64: bytesToBase64(chunk.bytes)
    };
  }

  async function markAttachmentCommitted(message, sender) {
    const owned = await ownedAttachment(message, sender);
    if (owned.error) return owned.error;
    if (["attachment_committed", "attachment_ready", "committed"].includes(owned.entry.phase)) {
      return { ok: true, already_committed: true, outbox: owned.entry };
    }
    if (owned.entry.phase !== "claimed") return { ok: false, code: "ATTACHMENT_PHASE_INVALID" };
    const next = await putOutbox(owned.key, { ...owned.entry, phase: "attachment_committed", attachment_committed_at: nowIso() });
    return { ok: true, outbox: next };
  }

  async function markAttachmentReady(message, sender) {
    const owned = await ownedAttachment(message, sender);
    if (owned.error) return owned.error;
    if (owned.entry.phase === "attachment_ready") return { ok: true, already_ready: true, outbox: owned.entry };
    if (owned.entry.phase !== "attachment_committed") return { ok: false, code: "ATTACHMENT_PHASE_INVALID" };
    const expected = (owned.entry.artifact_descriptors || []).map((item) => String(item.filename));
    const actual = Array.isArray(message.attached_filenames) ? message.attached_filenames.map(String) : [];
    if (JSON.stringify(expected) !== JSON.stringify(actual)) return { ok: false, code: "ATTACHMENT_FILESET_MISMATCH" };
    const next = await putOutbox(owned.key, {
      ...owned.entry,
      phase: "attachment_ready",
      attached_filenames: actual,
      attachment_ready_at: nowIso()
    });
    return { ok: true, outbox: next };
  }

  async function commitAttachmentSend(message, sender) {
    const owned = await ownedAttachment(message, sender);
    if (owned.error) return owned.error;
    if (owned.entry.phase === "committed") return { ok: true, already_committed: true };
    if (owned.entry.phase !== "attachment_ready") return { ok: false, code: "ATTACHMENT_NOT_READY" };
    await putOutbox(owned.key, { ...owned.entry, phase: "committed", committed_at: nowIso() });
    return { ok: true };
  }

  handleMessage = async function fileAwareHandleMessage(message, sender) {
    switch (message?.type) {
      case "WS_GET_OUTBOX_ARTIFACT_CHUNK": return attachmentChunk(message, sender);
      case "WS_MARK_ATTACHMENT_COMMITTED": return markAttachmentCommitted(message, sender);
      case "WS_MARK_ATTACHMENT_READY": return markAttachmentReady(message, sender);
      case "WS_COMMIT_ATTACHMENT_SEND": return commitAttachmentSend(message, sender);
      default: return baseHandleMessage(message, sender);
    }
  };

  void YMBFileArtifactStore.cleanupExpired().catch(() => null);

  globalThis.YMBFileDeliveryWorkerTransport = Object.freeze({
    DELIVERY_MODE,
    CHATGPT_FILE_TEXT_THRESHOLD,
    compactLargeCommandResult
  });
})();
