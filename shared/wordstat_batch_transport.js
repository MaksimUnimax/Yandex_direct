(() => {
  "use strict";

  function normalizeText(text) {
    return String(text || "").replace(/\u00a0/g, " ");
  }

  function detect(text, registry = globalThis.YMBServiceRegistry) {
    const source = normalizeText(text).trim();
    const BatchProtocol = globalThis.WordstatBatchProtocol;
    if (BatchProtocol?.isCommandText?.(source)) {
      return Object.freeze({
        service: registry?.SERVICES?.WORDSTAT || "wordstat",
        prefix: BatchProtocol.PREFIX,
        batch: true
      });
    }
    const ordinary = registry?.detect?.(source) || null;
    return ordinary ? Object.freeze({ ...ordinary, batch: false }) : null;
  }

  function discover(text, discovery = globalThis.YMBBlockCommandDiscovery, registry = globalThis.YMBServiceRegistry) {
    const source = normalizeText(text);
    const ordinary = (discovery?.discover?.(source, registry) || []).map((item) => Object.freeze({ ...item, batch: false }));
    const BatchProtocol = globalThis.WordstatBatchProtocol;
    const prefix = String(BatchProtocol?.PREFIX || "WORDSTAT_BATCH_API_V1");
    const batch = [];
    let from = 0;
    while (from < source.length) {
      const index = source.indexOf(prefix, from);
      if (index < 0) break;
      const json = discovery?.extractJsonObject?.(source, index + prefix.length)
        || { ok: false, code: "BATCH_DISCOVERY_UNAVAILABLE", message: "Batch discovery helper недоступен.", end: index + prefix.length };
      batch.push(Object.freeze({
        index,
        service: registry?.SERVICES?.WORDSTAT || "wordstat",
        prefix,
        batch: true,
        ...json
      }));
      from = Math.max(index + prefix.length, Number(json?.end || 0), index + 1);
    }
    return Object.freeze([...ordinary, ...batch].sort((a, b) => Number(a.index || 0) - Number(b.index || 0)));
  }

  function protocolForText(text, activeService, ordinaryProtocol) {
    const registry = globalThis.YMBServiceRegistry;
    const wordstat = registry?.SERVICES?.WORDSTAT || "wordstat";
    const BatchProtocol = globalThis.WordstatBatchProtocol;
    if (BatchProtocol?.isCommandText?.(text)) return String(activeService || "") === wordstat ? BatchProtocol : null;
    return ordinaryProtocol || null;
  }

  globalThis.YMBWordstatBatchTransport = Object.freeze({
    detect,
    discover,
    protocolForText
  });
})();
