(() => {
  "use strict";

  function normalizeText(text) {
    return String(text || "").replace(/\u00a0/g, " ");
  }

  function detect(text, registry = globalThis.YMBServiceRegistry) {
    const source = normalizeText(text).trim();
    const BatchProtocol = globalThis.SearchBatchProtocol;
    if (BatchProtocol?.isCommandText?.(source)) {
      return Object.freeze({
        service: registry?.SERVICES?.SEARCH || "search",
        prefix: BatchProtocol.PREFIX,
        batch: true,
        batch_kind: "search",
        search_batch: true
      });
    }
    const wordstatTransport = globalThis.YMBWordstatBatchTransport;
    if (wordstatTransport?.detect) return wordstatTransport.detect(source, registry);
    const ordinary = registry?.detect?.(source) || null;
    return ordinary ? Object.freeze({ ...ordinary, batch: false, search_batch: false }) : null;
  }

  function discover(text, discovery = globalThis.YMBBlockCommandDiscovery, registry = globalThis.YMBServiceRegistry) {
    const source = normalizeText(text);
    const wordstatTransport = globalThis.YMBWordstatBatchTransport;
    const base = wordstatTransport?.discover
      ? [...wordstatTransport.discover(source, discovery, registry)]
      : (discovery?.discover?.(source, registry) || []).map((item) => Object.freeze({ ...item, batch: false, search_batch: false }));

    const BatchProtocol = globalThis.SearchBatchProtocol;
    const prefix = String(BatchProtocol?.PREFIX || "SEARCH_BATCH_API_V1");
    const batch = [];
    let from = 0;
    while (from < source.length) {
      const index = source.indexOf(prefix, from);
      if (index < 0) break;
      const json = discovery?.extractJsonObject?.(source, index + prefix.length)
        || { ok: false, code: "SEARCH_BATCH_DISCOVERY_UNAVAILABLE", message: "Search batch discovery helper недоступен.", end: index + prefix.length };
      batch.push(Object.freeze({
        index,
        service: registry?.SERVICES?.SEARCH || "search",
        prefix,
        batch: true,
        batch_kind: "search",
        search_batch: true,
        ...json
      }));
      from = Math.max(index + prefix.length, Number(json?.end || 0), index + 1);
    }

    return Object.freeze([...base, ...batch].sort((a, b) => Number(a.index || 0) - Number(b.index || 0)));
  }

  function protocolForText(text, activeService, ordinaryProtocol) {
    const registry = globalThis.YMBServiceRegistry;
    const search = registry?.SERVICES?.SEARCH || "search";
    const BatchProtocol = globalThis.SearchBatchProtocol;
    if (BatchProtocol?.isCommandText?.(text)) return String(activeService || "") === search ? BatchProtocol : null;
    return ordinaryProtocol || null;
  }

  globalThis.YMBSearchBatchTransport = Object.freeze({
    detect,
    discover,
    protocolForText
  });
})();