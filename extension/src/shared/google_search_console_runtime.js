(() => {
  "use strict";

  const DefaultProtocol = globalThis.GoogleSearchConsoleProtocol;
  const DefaultPolicy = globalThis.YMBPolicyModel;
  const SERVICE = "google_search_console";

  function fail(code, message, requestExecuted = false) {
    const error = new Error(message || code);
    error.code = code;
    error.request_executed = requestExecuted;
    error.automatic_retry = false;
    return error;
  }

  function executionError(error, requestExecuted) {
    error.request_executed = requestExecuted;
    error.automatic_retry = false;
    return error;
  }

  function parseJson(text) {
    try { return JSON.parse(String(text || "")); }
    catch { return null; }
  }

  function tokenValue(value) {
    if (typeof value === "string") return value.trim();
    if (value && typeof value === "object" && typeof value.token === "string") return value.token.trim();
    return "";
  }

  function create({
    protocol = DefaultProtocol,
    policyModel = DefaultPolicy,
    identity,
    fetchImpl,
    now = () => Date.now(),
    uuid = () => globalThis.crypto?.randomUUID?.() || `${Date.now()}-${Math.random()}`
  } = {}) {
    if (!protocol) throw fail("GSC_PROTOCOL_REQUIRED", "Google Search Console protocol is unavailable.");
    if (!policyModel) throw fail("GSC_POLICY_MODEL_REQUIRED", "Policy model is unavailable.");
    if (!identity || typeof identity.getAccessToken !== "function") {
      throw fail("GSC_IDENTITY_ADAPTER_REQUIRED", "Injected Google identity adapter is required.");
    }
    if (typeof fetchImpl !== "function") {
      throw fail("GSC_FETCH_ADAPTER_REQUIRED", "Injected fetch adapter is required.");
    }

    function requestId(metadata) {
      return String(metadata?.request_id || `gsc-${uuid()}`);
    }

    function elapsed(started) {
      return Math.max(0, Number(now()) - Number(started));
    }

    function skipped(normalized, metadata, decision) {
      const id = requestId(metadata);
      const envelope = protocol.buildSkippedEnvelope({
        requestId: id,
        command: normalized,
        reason: decision.reason,
        metadata: {
          ...metadata,
          policy: decision.policy,
          cost_estimate: { estimated_rub: 0 },
          request_executed: false,
          automatic_retry: false
        }
      });
      return {
        ok: false,
        skipped: true,
        http_status: 0,
        request_id: id,
        report_envelope: envelope,
        report_text: protocol.formatResultEnvelope(envelope)
      };
    }

    function admission(normalized, metadata) {
      return policyModel.decisionForService(SERVICE, {
        policy: metadata?.policy || {},
        channel: metadata?.channel || "manual",
        method: normalized.method,
        credentialState: "PRESENT",
        run: metadata?.run || { requests_executed: 0, estimated_cost_rub: 0 }
      });
    }

    async function accessToken() {
      let raw;
      try {
        raw = await identity.getAccessToken({ interactive: false });
      } catch (cause) {
        const error = fail("GSC_AUTH_REQUIRED", "Google Search Console authorization is required before this command can run.", false);
        error.cause = cause;
        throw error;
      }
      const token = tokenValue(raw);
      if (!token) throw fail("GSC_AUTH_REQUIRED", "Google Search Console authorization is required before this command can run.", false);
      return token;
    }

    async function execute(command, metadata = {}) {
      const normalized = protocol.normalizeCommand(command);
      const decision = admission(normalized, metadata);
      if (!decision.allow) return skipped(normalized, metadata, decision);

      const token = await accessToken();
      const req = protocol.buildRequest(normalized);
      const id = requestId(metadata);
      const started = now();
      const headers = {
        Accept: "application/json",
        Authorization: `Bearer ${token}`
      };
      if (req.body !== undefined) headers["Content-Type"] = "application/json";

      const options = {
        method: req.method,
        headers
      };
      if (req.body !== undefined) options.body = JSON.stringify(req.body);

      let response;
      try {
        response = await fetchImpl(req.url, options);
      } catch (cause) {
        const error = fail(
          "REQUEST_OUTCOME_UNKNOWN_NO_RETRY",
          "Исход Google Search Console request неизвестен; автоматический повтор запрещён.",
          "UNKNOWN"
        );
        error.cause = cause;
        throw error;
      }

      let text = "";
      try {
        text = await response.text();
      } catch (cause) {
        const error = fail("INVALID_GOOGLE_SEARCH_CONSOLE_RESPONSE", "Не удалось прочитать ответ Google Search Console.", true);
        error.cause = cause;
        throw error;
      }

      const parsed = parseJson(text);
      if (!response.ok) {
        const payload = protocol.safeErrorPayload(response.status, text, parsed);
        const envelope = protocol.buildResultEnvelope({
          requestId: id,
          command: normalized,
          httpStatus: response.status,
          elapsedMs: elapsed(started),
          result: { error: payload },
          metadata: {
            ...metadata,
            status: "ERROR",
            reason: payload.code,
            policy: decision.policy,
            cost_estimate: { estimated_rub: 0 },
            request_executed: true,
            automatic_retry: false
          }
        });
        return {
          ok: false,
          skipped: false,
          http_status: response.status,
          request_id: id,
          report_envelope: envelope,
          report_text: protocol.formatResultEnvelope(envelope)
        };
      }

      if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
        throw fail("INVALID_GOOGLE_SEARCH_CONSOLE_RESPONSE", "Google Search Console вернул некорректный JSON-ответ.", true);
      }

      let result;
      try {
        result = protocol.normalizeProviderResult(normalized, parsed);
      } catch (error) {
        if (!error.code) error.code = "INVALID_GOOGLE_SEARCH_CONSOLE_RESPONSE";
        throw executionError(error, true);
      }

      const envelope = protocol.buildResultEnvelope({
        requestId: id,
        command: normalized,
        httpStatus: response.status,
        elapsedMs: elapsed(started),
        result,
        metadata: {
          ...metadata,
          status: "OK",
          reason: null,
          policy: decision.policy,
          cost_estimate: { estimated_rub: 0 },
          request_executed: true,
          automatic_retry: false
        }
      });
      return {
        ok: true,
        skipped: false,
        http_status: response.status,
        request_id: id,
        report_envelope: envelope,
        report_text: protocol.formatResultEnvelope(envelope)
      };
    }

    return Object.freeze({ execute });
  }

  globalThis.YMBGoogleSearchConsoleRuntime = Object.freeze({ SERVICE, create });
})();
