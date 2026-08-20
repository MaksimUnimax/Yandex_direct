(() => {
  "use strict";

  const SERVICES = Object.freeze({
    WORDSTAT: "wordstat",
    SEARCH: "search"
  });

  const DEFINITIONS = Object.freeze([
    Object.freeze({ service: SERVICES.WORDSTAT, prefix: "WORDSTAT_API_V1" }),
    Object.freeze({ service: SERVICES.SEARCH, prefix: "SEARCH_API_V1" })
  ]);

  function normalizeText(text) {
    return String(text || "").replace(/\u00a0/g, " ").trim();
  }

  function detect(text) {
    const source = normalizeText(text);
    for (const definition of DEFINITIONS) {
      if (source.startsWith(definition.prefix)) return definition;
    }
    return null;
  }

  function isKnownService(service) {
    const value = String(service || "").trim();
    return DEFINITIONS.some((definition) => definition.service === value);
  }

  function definitionForService(service) {
    const value = String(service || "").trim();
    return DEFINITIONS.find((definition) => definition.service === value) || null;
  }

  globalThis.YMBServiceRegistry = Object.freeze({
    SERVICES,
    DEFINITIONS,
    detect,
    isKnownService,
    definitionForService
  });
})();
