(() => {
  "use strict";

  const ordinary = globalThis.SearchProtocol;
  const transport = globalThis.YMBSearchBatchTransport;
  const batch = globalThis.SearchBatchProtocol;
  const registry = globalThis.YMBServiceRegistry;
  if (!ordinary || !transport || !batch || !registry) return;

  const proxy = Object.freeze({
    ...ordinary,
    isCommandText(text) {
      const selected = transport.protocolForText(text, registry.SERVICES.SEARCH, ordinary);
      return selected === batch || ordinary.isCommandText(text);
    }
  });

  globalThis.SearchProtocol = proxy;
  globalThis.YMBSearchBatchContentBridge = Object.freeze({ ordinaryProtocol: ordinary, protocol: proxy });
})();