(() => {
  "use strict";

  function textFingerprint(value) {
    const text = String(value || "");
    let hash = 2166136261;
    for (let i = 0; i < text.length; i += 1) {
      hash ^= text.charCodeAt(i);
      hash = Math.imul(hash, 16777619);
    }
    return (hash >>> 0).toString(16).padStart(8, "0");
  }

  function extractJsonObject(source, start) {
    let i = start;
    while (i < source.length && /\s/u.test(source[i])) i += 1;
    if (source[i] !== "{") return { ok: false, code: "MISSING_JSON", message: "После маркера ожидается JSON-объект.", end: i };
    const begin = i;
    let depth = 0;
    let inString = false;
    let escape = false;
    for (; i < source.length; i += 1) {
      const ch = source[i];
      if (inString) {
        if (escape) { escape = false; continue; }
        if (ch === "\\") { escape = true; continue; }
        if (ch === '"') inString = false;
        continue;
      }
      if (ch === '"') { inString = true; continue; }
      if (ch === "{") depth += 1;
      else if (ch === "}") {
        depth -= 1;
        if (depth === 0) {
          const jsonText = source.slice(begin, i + 1);
          try {
            const raw = JSON.parse(jsonText);
            if (!raw || typeof raw !== "object" || Array.isArray(raw)) return { ok: false, code: "INVALID_JSON_ROOT", message: "Команда должна быть JSON-объектом.", end: i + 1 };
            return { ok: true, raw, json_text: jsonText, start: begin, end: i + 1 };
          } catch (error) {
            return { ok: false, code: "INVALID_JSON", message: `Некорректный JSON: ${error.message}`, start: begin, end: i + 1 };
          }
        }
      }
    }
    return { ok: false, code: "UNTERMINATED_JSON", message: "JSON-объект команды не закрыт.", start: begin, end: source.length };
  }

  function discover(text, registry = globalThis.YMBServiceRegistry) {
    const source = String(text || "").replace(/\u00a0/g, " ");
    const definitions = Array.isArray(registry?.DEFINITIONS) ? registry.DEFINITIONS : [];
    const markers = [];
    for (const def of definitions) {
      let from = 0;
      while (from < source.length) {
        const idx = source.indexOf(def.prefix, from);
        if (idx < 0) break;
        markers.push({ index: idx, service: def.service, prefix: def.prefix });
        from = idx + def.prefix.length;
      }
    }
    markers.sort((a, b) => a.index - b.index);
    return markers.map((marker) => {
      const json = extractJsonObject(source, marker.index + marker.prefix.length);
      return Object.freeze({ ...marker, ...json });
    });
  }

  globalThis.YMBBlockCommandDiscovery = Object.freeze({ textFingerprint, extractJsonObject, discover });
})();
