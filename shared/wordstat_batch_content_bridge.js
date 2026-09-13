(() => {
  "use strict";

  const ordinary = globalThis.WordstatProtocol;
  const transport = globalThis.YMBWordstatBatchTransport;
  const batch = globalThis.WordstatBatchProtocol;
  const registry = globalThis.YMBServiceRegistry;
  if (!ordinary || !transport || !batch || !registry) return;

  const proxy = Object.freeze({
    ...ordinary,
    isCommandText(text) {
      const selected = transport.protocolForText(text, registry.SERVICES.WORDSTAT, ordinary);
      return selected === batch || ordinary.isCommandText(text);
    }
  });

  globalThis.WordstatProtocol = proxy;
  globalThis.YMBWordstatBatchContentBridge = Object.freeze({ ordinaryProtocol: ordinary, protocol: proxy });
})();
