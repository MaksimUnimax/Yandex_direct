(() => {
  "use strict";

  const MAX_XML_CHARS = 4_000_000;
  const MAX_SNIPPET_CHARS = 4000;

  function fail(code, message) {
    const error = new Error(message || code);
    error.code = code;
    throw error;
  }

  function decodeEntity(entity) {
    if (entity === "amp") return "&";
    if (entity === "lt") return "<";
    if (entity === "gt") return ">";
    if (entity === "quot") return '"';
    if (entity === "apos") return "'";
    if (/^#\d+$/.test(entity)) {
      const cp = Number(entity.slice(1));
      if (Number.isInteger(cp) && cp >= 0 && cp <= 0x10ffff) return String.fromCodePoint(cp);
    }
    if (/^#x[0-9a-f]+$/i.test(entity)) {
      const cp = Number.parseInt(entity.slice(2), 16);
      if (Number.isInteger(cp) && cp >= 0 && cp <= 0x10ffff) return String.fromCodePoint(cp);
    }
    return `&${entity};`;
  }

  function decodeEntities(text) {
    return String(text || "").replace(/&([^;\s]{1,32});/g, (_match, entity) => decodeEntity(entity));
  }

  function normalizeText(text) {
    const normalized = decodeEntities(text).replace(/\s+/g, " ").trim();
    return normalized || null;
  }

  function decodeBase64Utf8(rawData) {
    const value = String(rawData || "").trim();
    if (!value) fail("SEARCH_RAW_DATA_MISSING", "В ответе Yandex Search отсутствует rawData.");
    if (value.length % 4 !== 0 || !/^[A-Za-z0-9+/]*={0,2}$/.test(value)) {
      fail("INVALID_SEARCH_BASE64", "rawData Yandex Search не является корректной Base64-строкой.");
    }

    let binary;
    try {
      if (typeof globalThis.atob === "function") {
        binary = globalThis.atob(value);
      } else if (globalThis.Buffer && typeof globalThis.Buffer.from === "function") {
        binary = globalThis.Buffer.from(value, "base64").toString("latin1");
      } else {
        fail("BASE64_DECODER_UNAVAILABLE", "В среде выполнения недоступен Base64-декодер.");
      }
    } catch (error) {
      if (error?.code) throw error;
      fail("INVALID_SEARCH_BASE64", `Не удалось декодировать rawData: ${error?.message || error}`);
    }

    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i += 1) bytes[i] = binary.charCodeAt(i) & 0xff;

    let xml;
    try {
      if (typeof globalThis.TextDecoder === "function") {
        xml = new globalThis.TextDecoder("utf-8", { fatal: true }).decode(bytes);
      } else if (globalThis.Buffer && typeof globalThis.Buffer.from === "function") {
        xml = globalThis.Buffer.from(bytes).toString("utf8");
      } else {
        fail("UTF8_DECODER_UNAVAILABLE", "В среде выполнения недоступен UTF-8 декодер.");
      }
    } catch (error) {
      if (error?.code) throw error;
      fail("INVALID_SEARCH_UTF8", `rawData не содержит корректный UTF-8 XML: ${error?.message || error}`);
    }

    if (xml.length > MAX_XML_CHARS) fail("SEARCH_XML_TOO_LARGE", `XML-ответ превышает ${MAX_XML_CHARS} символов.`);
    return xml;
  }

  function localName(name) {
    const value = String(name || "");
    const index = value.indexOf(":");
    return (index >= 0 ? value.slice(index + 1) : value).toLowerCase();
  }

  function parseXml(xmlText) {
    const xml = String(xmlText || "");
    if (!xml.trim()) fail("SEARCH_XML_EMPTY", "Yandex Search вернул пустой XML.");
    if (xml.length > MAX_XML_CHARS) fail("SEARCH_XML_TOO_LARGE", `XML-ответ превышает ${MAX_XML_CHARS} символов.`);

    const root = { name: "#document", children: [] };
    const stack = [root];
    const tokenPattern = /<!--[^]*?-->|<!\[CDATA\[[^]*?\]\]>|<\?[^]*?\?>|<!DOCTYPE[^>]*>|<[^>]+>|[^<]+/g;
    let match;

    while ((match = tokenPattern.exec(xml)) !== null) {
      const token = match[0];
      if (!token) continue;
      if (token.startsWith("<!--") || token.startsWith("<?") || /^<!DOCTYPE/i.test(token)) continue;

      if (token.startsWith("<![CDATA[")) {
        stack[stack.length - 1].children.push(token.slice(9, -3));
        continue;
      }

      if (token[0] !== "<") {
        stack[stack.length - 1].children.push(token);
        continue;
      }

      if (/^<\//.test(token)) {
        const close = token.match(/^<\/\s*([A-Za-z_][\w:.-]*)\s*>$/);
        if (!close) fail("INVALID_SEARCH_XML", "Некорректный закрывающий XML-тег.");
        if (stack.length <= 1) fail("INVALID_SEARCH_XML", "Лишний закрывающий XML-тег.");
        const current = stack.pop();
        if (localName(current.name) !== localName(close[1])) {
          fail("INVALID_SEARCH_XML", `Нарушена вложенность XML: ожидался </${current.name}>, получен </${close[1]}>.`);
        }
        continue;
      }

      const open = token.match(/^<\s*([A-Za-z_][\w:.-]*)(?:\s[^>]*)?\/?\s*>$/);
      if (!open) {
        if (/^<!/.test(token)) continue;
        fail("INVALID_SEARCH_XML", "Некорректный открывающий XML-тег.");
      }
      const node = { name: open[1], children: [] };
      stack[stack.length - 1].children.push(node);
      if (!/\/\s*>$/.test(token)) stack.push(node);
    }

    if (stack.length !== 1) {
      const current = stack[stack.length - 1];
      fail("INVALID_SEARCH_XML", `XML оборван внутри <${current.name}>.`);
    }
    return root;
  }

  function isNode(value) {
    return Boolean(value && typeof value === "object" && typeof value.name === "string" && Array.isArray(value.children));
  }

  function descendants(node, name, out = []) {
    const expected = String(name || "").toLowerCase();
    if (!isNode(node)) return out;
    for (const child of node.children) {
      if (!isNode(child)) continue;
      if (localName(child.name) === expected) out.push(child);
      descendants(child, expected, out);
    }
    return out;
  }

  function firstDescendant(node, name) {
    return descendants(node, name, [])[0] || null;
  }

  function textContent(node) {
    if (!isNode(node)) return String(node || "");
    return node.children.map((child) => (isNode(child) ? textContent(child) : String(child || ""))).join("");
  }

  function firstText(node, name) {
    const match = firstDescendant(node, name);
    return match ? normalizeText(textContent(match)) : null;
  }

  function normalizeModtime(value) {
    const text = String(value || "").trim();
    return /^\d{8}T\d{6}$/.test(text) ? text : null;
  }

  function normalizeXml(xmlText) {
    const tree = parseXml(xmlText);
    const response = firstDescendant(tree, "response");
    if (!response) {
      return Object.freeze({ results: Object.freeze([]), result_count: 0, response_format: "FORMAT_XML" });
    }

    const docs = descendants(response, "doc", []);
    const results = docs.map((doc, index) => {
      const passages = descendants(doc, "passage", [])
        .map((passage) => normalizeText(textContent(passage)))
        .filter(Boolean);
      const snippetText = passages.length ? passages.join(" … ").slice(0, MAX_SNIPPET_CHARS) : null;
      return Object.freeze({
        rank: index + 1,
        url: firstText(doc, "url"),
        domain: firstText(doc, "domain"),
        title: firstText(doc, "title"),
        snippet: snippetText,
        modtime: normalizeModtime(firstText(doc, "modtime"))
      });
    });

    return Object.freeze({
      results: Object.freeze(results),
      result_count: results.length,
      response_format: "FORMAT_XML"
    });
  }

  function normalizeBase64RawData(rawData) {
    return normalizeXml(decodeBase64Utf8(rawData));
  }

  globalThis.YMBSearchXml = Object.freeze({
    MAX_XML_CHARS,
    MAX_SNIPPET_CHARS,
    decodeEntities,
    decodeBase64Utf8,
    parseXml,
    normalizeXml,
    normalizeBase64RawData
  });
})();
