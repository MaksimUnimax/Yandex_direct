/* Deferred Search wire adapter. Internal only; admission must persist before fetch. */
(() => {
  "use strict";
  const codeError = code => Object.assign(new Error(code), { code });
  const known = new Set(["ASYNC_ABORTED", "ASYNC_TIMEOUT", "ASYNC_RESPONSE_TOO_LARGE", "ASYNC_BODY_STREAM_REQUIRED", "ASYNC_RESPONSE_REDIRECTED", "ASYNC_INVALID_UTF8"]);
  function create({ fetchImpl, protocol = globalThis.SearchAsyncProtocol, maxResponseBytes, timeoutMs = 20000 } = {}) {
    if (typeof fetchImpl !== "function" || !protocol?.buildSubmitRequest || !protocol?.buildGetRequest || !protocol?.parseOperation) throw codeError("ASYNC_TRANSPORT_DEPENDENCY_MISSING");
    // Required operator/runtime resource budget, NOT a purported provider limit.
    if (!Number.isSafeInteger(maxResponseBytes) || maxResponseBytes < 1 || !Number.isSafeInteger(timeoutMs) || timeoutMs < 1 || timeoutMs > 25000) throw codeError("ASYNC_TRANSPORT_BUDGET_REQUIRED");
    async function execute({ kind, query, parameters, operationId, credential, expectedFolderId, admit, signal } = {}) {
      const publicBase = { kind, automatic_retry: false };
      let request, apiKey;
      try {
        if (!["submit", "collect"].includes(kind)) throw codeError("ASYNC_TRANSPORT_KIND_INVALID");
        if (!credential || typeof credential.api_key !== "string" || !credential.api_key.trim() || /[\r\n\u0000]/u.test(credential.api_key)) throw codeError("ASYNC_SEARCH_KEY_INVALID");
        if (typeof credential.folder_id !== "string" || !credential.folder_id || credential.folder_id !== expectedFolderId) throw codeError("ASYNC_CREDENTIAL_CONTEXT_CHANGED");
        if (typeof admit !== "function") throw codeError("ASYNC_DURABLE_ADMISSION_REQUIRED");
        apiKey = credential.api_key.trim();
        request = kind === "submit" ? protocol.buildSubmitRequest(query, parameters, credential.folder_id) : protocol.buildGetRequest(operationId);
      } catch (error) {
        return { ...publicBase, ok: false, request_executed: false, code: error?.code || "ASYNC_PREFLIGHT_INVALID" };
      }
      if (signal?.aborted) return { ...publicBase, ok: false, request_executed: false, code: "ASYNC_ABORTED" };
      let admitted;
      try { admitted = await admit({ kind, folder_id: expectedFolderId }); }
      catch { return { ...publicBase, ok: false, request_executed: false, code: "ASYNC_ADMISSION_FAILED" }; }
      if (admitted?.allowed !== true) return { ...publicBase, ok: false, request_executed: false, code: "ASYNC_ADMISSION_DENIED" };
      if (signal?.aborted) return { ...publicBase, ok: false, request_executed: false, code: "ASYNC_ABORTED_AFTER_ADMISSION" };

      const controller = new AbortController();
      let reader = null, timer, abortCode = "ASYNC_ABORTED";
      const stop = (code = "ASYNC_ABORTED") => { abortCode = code; controller.abort(); };
      // One detachable listener per pending fetch/read; no shared Promise.race
      // whose unresolved abort branch accumulates reactions for every chunk.
      const wait = start => new Promise((resolve, reject) => {
        const cleanup = () => controller.signal.removeEventListener("abort", onAbort);
        const onAbort = () => { cleanup(); reject(codeError(abortCode)); };
        if (controller.signal.aborted) { reject(codeError(abortCode)); return; }
        controller.signal.addEventListener("abort", onAbort, { once: true });
        Promise.resolve().then(() => {
          if (controller.signal.aborted) throw codeError(abortCode);
          return start();
        }).then(value => { cleanup(); resolve(value); }, error => { cleanup(); reject(error); });
      });
      const outerAbort = () => stop("ASYNC_ABORTED");
      signal?.addEventListener("abort", outerAbort, { once: true });
      timer = setTimeout(() => stop("ASYNC_TIMEOUT"), timeoutMs);
      let httpStatus = null;
      try {
        const init = {
          method: request.method,
          headers: { Authorization: `Api-Key ${apiKey}`, Accept: "application/json", ...(kind === "submit" ? { "Content-Type": "application/json" } : {}) },
          redirect: "error", credentials: "omit", cache: "no-store", referrerPolicy: "no-referrer", signal: controller.signal,
          ...(kind === "submit" ? { body: JSON.stringify(request.body) } : {})
        };
        // Exactly one fetch per admitted invocation. No retries, follow-up GET, fan-out or polling.
        const response = await wait(() => fetchImpl(request.url, init));
        httpStatus = response.status;
        if (response.redirected || (response.url && response.url !== request.url)) throw codeError("ASYNC_RESPONSE_REDIRECTED");
        if (!response.ok) {
          controller.abort();
          try { Promise.resolve(response.body?.cancel?.()).catch(() => null); } catch {}
          return { ...publicBase, ok: false, request_executed: true, http_status: httpStatus, code: `ASYNC_HTTP_${httpStatus}`, outcome: kind === "submit" ? ([400, 401, 403, 404, 405, 413, 415, 422, 429].includes(httpStatus) ? "rejected" : "unknown") : "read_error" };
        }
        if (!response.body?.getReader) throw codeError("ASYNC_BODY_STREAM_REQUIRED");
        // Read decompressed bytes with a hard local budget. Never return truncated success.
        const declared = Number(response.headers?.get?.("content-length"));
        if (Number.isFinite(declared) && declared > maxResponseBytes) throw codeError("ASYNC_RESPONSE_TOO_LARGE");
        reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8", { fatal: true });
        let rawText = "", byteLength = 0;
        for (;;) {
          const { done, value } = await wait(() => reader.read());
          if (done) break;
          if (!(value instanceof Uint8Array)) throw codeError("ASYNC_BODY_STREAM_REQUIRED");
          byteLength += value.byteLength;
          if (byteLength > maxResponseBytes) throw codeError("ASYNC_RESPONSE_TOO_LARGE");
          try { rawText += decoder.decode(value, { stream: true }); }
          catch { throw codeError("ASYNC_INVALID_UTF8"); }
        }
        try { rawText += decoder.decode(); } catch { throw codeError("ASYNC_INVALID_UTF8"); }
        // An upstream error reflecting a credential must not be exported as raw evidence.
        if (rawText.includes(apiKey)) return { ...publicBase, ok: false, request_executed: true, http_status: httpStatus, code: "ASYNC_CREDENTIAL_REFLECTED_IN_RESPONSE", outcome: kind === "submit" ? "unknown" : "read_error" };
        let operation;
        try { operation = protocol.parseOperation(rawText, kind === "collect" ? operationId : null); }
        catch { return { ...publicBase, ok: false, request_executed: true, http_status: httpStatus, code: "ASYNC_OPERATION_RESPONSE_INVALID", outcome: kind === "submit" ? "unknown" : "read_error" }; }
        return { ...publicBase, ok: true, request_executed: true, http_status: httpStatus, operation, raw_text: rawText, byte_length: byteLength };
      } catch (error) {
        const code = controller.signal.aborted ? abortCode : known.has(error?.code) ? error.code : "ASYNC_NETWORK_OUTCOME_UNKNOWN";
        controller.abort();
        return { ...publicBase, ok: false, request_executed: "UNKNOWN", http_status: httpStatus, code, outcome: kind === "submit" ? "unknown" : "read_error" };
      } finally {
        clearTimeout(timer); signal?.removeEventListener("abort", outerAbort);
        if (reader) { try { Promise.resolve(reader.cancel()).catch(() => null); } catch {} try { reader.releaseLock(); } catch {} }
        apiKey = null;
      }
    }
    return Object.freeze({ execute });
  }
  globalThis.YMBSearchAsyncTransport = Object.freeze({ create });
})();
