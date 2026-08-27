(() => {
  "use strict";

  const baseProtocolForService = globalThis.protocolForService;
  if (typeof baseProtocolForService !== "function") return;

  globalThis.protocolForService = function batchAwareProtocolForService(service) {
    const ordinary = baseProtocolForService(service);
    if (String(service || "") !== String(globalThis.YMBWordstatBatchTransport?.BATCH_SERVICE || "wordstat")) return ordinary;
    if (!ordinary) return ordinary;
    return Object.freeze({
      ...ordinary,
      isCommandText(text) {
        const selected = globalThis.YMBWordstatBatchTransport.protocolForText(text, service, ordinary);
        return Boolean(selected && typeof selected.isCommandText === "function" && selected.isCommandText(text));
      }
    });
  };
})();
