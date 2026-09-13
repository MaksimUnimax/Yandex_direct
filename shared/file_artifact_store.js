(() => {
  "use strict";

  const DB_NAME = "ymb_delivery_artifacts_v2";
  const DB_VERSION = 2;
  const META_STORE = "meta";
  const CHUNK_STORE = "chunks";
  const CHUNK_ARTIFACT_INDEX = "artifact_key";
  const DEFAULT_CHUNK_CHARACTERS = 256 * 1024;
  const WRITE_BATCH_CHUNKS = 8;
  const MAX_CHUNK_BYTES = 256 * 1024;
  const ARTIFACT_TTL_MS = 60 * 60 * 1000;

  function fail(code, message) {
    const error = new Error(message || code);
    error.code = code;
    throw error;
  }

  function nowMs() { return Date.now(); }

  function openDb() {
    return new Promise((resolve, reject) => {
      let request;
      try { request = indexedDB.open(DB_NAME, DB_VERSION); }
      catch (error) { reject(error); return; }
      request.onupgradeneeded = () => {
        const db = request.result;
        if (!db.objectStoreNames.contains(META_STORE)) db.createObjectStore(META_STORE, { keyPath: "artifact_key" });
        const chunkStore = db.objectStoreNames.contains(CHUNK_STORE)
          ? request.transaction.objectStore(CHUNK_STORE)
          : db.createObjectStore(CHUNK_STORE, { keyPath: "chunk_key" });
        if (!chunkStore.indexNames.contains(CHUNK_ARTIFACT_INDEX)) chunkStore.createIndex(CHUNK_ARTIFACT_INDEX, "artifact_key", { unique: false });
      };
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error || new Error("IndexedDB open failed."));
      request.onblocked = () => reject(new Error("IndexedDB open blocked."));
    });
  }

  async function transaction(storeNames, mode, work) {
    const db = await openDb();
    try {
      return await new Promise((resolve, reject) => {
        let tx;
        try { tx = db.transaction(storeNames, mode); }
        catch (error) { reject(error); return; }
        let value;
        try { value = work(tx); }
        catch (error) { try { tx.abort(); } catch {} reject(error); return; }
        tx.oncomplete = () => resolve(value);
        tx.onabort = () => reject(tx.error || new Error("IndexedDB transaction aborted."));
        tx.onerror = () => reject(tx.error || new Error("IndexedDB transaction failed."));
      });
    } finally {
      try { db.close(); } catch {}
    }
  }

  function requestResult(request) {
    return new Promise((resolve, reject) => {
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error || new Error("IndexedDB request failed."));
    });
  }

  async function sha256Hex(bytes) {
    const view = bytes instanceof Uint8Array ? bytes : new Uint8Array(bytes || []);
    const digest = await crypto.subtle.digest("SHA-256", view);
    return [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
  }

  function safeTextSliceEnd(text, start, requestedEnd) {
    let end = Math.min(text.length, requestedEnd);
    if (end > start && end < text.length) {
      const previous = text.charCodeAt(end - 1);
      const next = text.charCodeAt(end);
      if (previous >= 0xD800 && previous <= 0xDBFF && next >= 0xDC00 && next <= 0xDFFF) end -= 1;
    }
    return Math.max(start + 1, end);
  }

  async function stageTextArtifact({ artifactKey, deliveryId, filename, text, mimeType = "text/plain;charset=utf-8", chunkCharacters = DEFAULT_CHUNK_CHARACTERS } = {}) {
    const key = String(artifactKey || "").trim();
    const delivery = String(deliveryId || "").trim();
    if (!key || !delivery) fail("ARTIFACT_ID_REQUIRED", "artifactKey и deliveryId обязательны.");
    const source = String(text ?? "");
    const windowChars = Math.max(1024, Math.min(DEFAULT_CHUNK_CHARACTERS, Math.trunc(Number(chunkCharacters) || DEFAULT_CHUNK_CHARACTERS)));
    const encoder = new TextEncoder();
    const manifest = [];
    let totalBytes = 0;
    let charOffset = 0;
    let index = 0;
    let pending = [];
    const created = nowMs();

    try { await deleteArtifact(key); } catch {}

    // Persist staging authority before any chunk. If the worker dies mid-stage,
    // restart/TTL cleanup can still discover and delete the partial artifact.
    await transaction(META_STORE, "readwrite", (tx) => {
      tx.objectStore(META_STORE).put({
        artifact_key: key,
        delivery_id: delivery,
        filename: String(filename || "yandex-bridge-result.txt").slice(0, 180),
        mime_type: String(mimeType || "text/plain;charset=utf-8"),
        byte_length: 0,
        chunk_count: 0,
        chunk_manifest: [],
        status: "staging",
        created_at_ms: created,
        expires_at_ms: created + ARTIFACT_TTL_MS
      });
    });

    async function flush() {
      if (!pending.length) return;
      const batch = pending;
      pending = [];
      await transaction(CHUNK_STORE, "readwrite", (tx) => {
        const store = tx.objectStore(CHUNK_STORE);
        for (const record of batch) store.put(record);
      });
    }

    try {
      while (charOffset < source.length) {
        const end = safeTextSliceEnd(source, charOffset, charOffset + windowChars);
        const segment = source.slice(charOffset, end);
        const scratch = new Uint8Array(MAX_CHUNK_BYTES);
        const encoded = encoder.encodeInto(segment, scratch);
        if (!encoded || encoded.read <= 0) fail("ARTIFACT_ENCODING_STALLED", `TextEncoder did not consume input at chunk ${index}.`);
        const bytes = scratch.slice(0, encoded.written);
        const sha256 = await sha256Hex(bytes);
        const item = { chunk_index: index, byte_length: bytes.byteLength, sha256 };
        manifest.push(item);
        pending.push({
          chunk_key: `${key}:${index}`,
          artifact_key: key,
          delivery_id: delivery,
          chunk_index: index,
          byte_length: bytes.byteLength,
          sha256,
          bytes: bytes.buffer
        });
        totalBytes += bytes.byteLength;
        charOffset += encoded.read;
        index += 1;
        if (pending.length >= WRITE_BATCH_CHUNKS) await flush();
      }

      if (!manifest.length) {
        const bytes = new Uint8Array(0);
        const sha256 = await sha256Hex(bytes);
        manifest.push({ chunk_index: 0, byte_length: 0, sha256 });
        pending.push({ chunk_key: `${key}:0`, artifact_key: key, delivery_id: delivery, chunk_index: 0, byte_length: 0, sha256, bytes: bytes.buffer });
      }
      await flush();

      const meta = {
        artifact_key: key,
        delivery_id: delivery,
        filename: String(filename || "yandex-bridge-result.txt").slice(0, 180),
        mime_type: String(mimeType || "text/plain;charset=utf-8"),
        byte_length: totalBytes,
        chunk_count: manifest.length,
        chunk_manifest: manifest,
        status: "ready",
        created_at_ms: created,
        expires_at_ms: created + ARTIFACT_TTL_MS
      };
      await transaction(META_STORE, "readwrite", (tx) => { tx.objectStore(META_STORE).put(meta); });
      return Object.freeze({ ...meta, chunk_manifest: Object.freeze(meta.chunk_manifest.map((item) => Object.freeze({ ...item }))) });
    } catch (error) {
      try { await deleteArtifact(key); } catch {}
      throw error;
    }
  }

  async function getMeta(artifactKey) {
    const key = String(artifactKey || "");
    const db = await openDb();
    try {
      const tx = db.transaction(META_STORE, "readonly");
      return await requestResult(tx.objectStore(META_STORE).get(key));
    } finally { try { db.close(); } catch {} }
  }

  async function getChunk(artifactKey, chunkIndex) {
    const key = String(artifactKey || "");
    const index = Math.trunc(Number(chunkIndex));
    if (!key || !Number.isSafeInteger(index) || index < 0) fail("ARTIFACT_CHUNK_INDEX_INVALID", "Некорректный индекс части файла.");
    const db = await openDb();
    try {
      const tx = db.transaction(CHUNK_STORE, "readonly");
      const record = await requestResult(tx.objectStore(CHUNK_STORE).get(`${key}:${index}`));
      if (!record) fail("ARTIFACT_CHUNK_MISSING", "Часть файла отсутствует или истекла.");
      const bytes = new Uint8Array(record.bytes || new ArrayBuffer(0));
      return {
        artifact_key: key,
        chunk_index: index,
        byte_length: bytes.byteLength,
        sha256: String(record.sha256 || ""),
        bytes
      };
    } finally { try { db.close(); } catch {} }
  }

  async function deleteArtifact(artifactKey) {
    const key = String(artifactKey || "");
    if (!key) return;
    await transaction([META_STORE, CHUNK_STORE], "readwrite", (tx) => {
      tx.objectStore(META_STORE).delete(key);
      const chunks = tx.objectStore(CHUNK_STORE);
      const request = chunks.index(CHUNK_ARTIFACT_INDEX).openKeyCursor(IDBKeyRange.only(key));
      request.onsuccess = () => {
        const cursor = request.result;
        if (!cursor) return;
        chunks.delete(cursor.primaryKey);
        cursor.continue();
      };
    });
  }

  async function cleanupDescriptors(descriptors = []) {
    for (const descriptor of Array.isArray(descriptors) ? descriptors : []) {
      try { await deleteArtifact(descriptor.artifact_key, descriptor.chunk_count); } catch {}
    }
  }

  async function cleanupExpired() {
    const db = await openDb();
    let metas = [];
    try {
      const tx = db.transaction(META_STORE, "readonly");
      metas = await requestResult(tx.objectStore(META_STORE).getAll());
    } finally { try { db.close(); } catch {} }
    const current = nowMs();
    for (const meta of metas || []) {
      if (Number(meta?.expires_at_ms || 0) > current) continue;
      try { await deleteArtifact(meta.artifact_key, meta.chunk_count); } catch {}
    }
  }

  globalThis.YMBFileArtifactStore = Object.freeze({
    DB_NAME, DB_VERSION, META_STORE, CHUNK_STORE, CHUNK_ARTIFACT_INDEX,
    DEFAULT_CHUNK_CHARACTERS, MAX_CHUNK_BYTES, ARTIFACT_TTL_MS, WRITE_BATCH_CHUNKS,
    stageTextArtifact, getMeta, getChunk, deleteArtifact, cleanupDescriptors, cleanupExpired, sha256Hex
  });
})();
