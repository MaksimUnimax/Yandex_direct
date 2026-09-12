/* B4: strict envelope/structure guard around the UNCHANGED Search XML normalizer.
 * This accepts the documented unnamespaced XML 1.0 Yandex dialect, not arbitrary XML.
 * DTDs, entities beyond XML predefined/numeric references and namespaces fail closed.
 * Raw evidence is owned by the caller; errors never authorize another provider call.
 */
(() => {
  "use strict";
  const fail = code => { throw Object.assign(new Error(code), { code }); };
  const NAME = /^[A-Za-z_][A-Za-z0-9_.-]*/;
  const SPACE = /^[\x20\t\r\n]*$/;
  const validCodePoint = n => n === 9 || n === 10 || n === 13 ||
    (n >= 0x20 && n <= 0xD7FF) || (n >= 0xE000 && n <= 0xFFFD) || (n >= 0x10000 && n <= 0x10FFFF);
  function entities(text) {
    if (/[\u0000-\u0008\u000b\u000c\u000e-\u001f\ufffe\uffff]/u.test(text)) fail("ASYNC_XML_CHARACTER_INVALID");
    let pos = text.indexOf("&");
    while (pos !== -1) {
      const end = text.indexOf(";", pos + 1);
      if (end === -1 || end - pos > 32) fail("ASYNC_XML_ENTITY_INVALID");
      const entity = text.slice(pos + 1, end);
      if (!["amp", "lt", "gt", "quot", "apos"].includes(entity)) {
        let cp;
        if (/^#[0-9]+$/.test(entity)) cp = Number(entity.slice(1));
        else if (/^#x[0-9a-fA-F]+$/.test(entity)) cp = Number.parseInt(entity.slice(2), 16);
        else fail("ASYNC_XML_ENTITY_INVALID");
        if (!Number.isSafeInteger(cp) || !validCodePoint(cp)) fail("ASYNC_XML_ENTITY_INVALID");
      }
      pos = text.indexOf("&", end + 1);
    }
  }
  function tagBody(body) {
    const first = body.match(NAME);
    if (!first) fail("ASYNC_XML_TAG_INVALID");
    const name = first[0];
    let offset = name.length;
    const attributes = Object.create(null);
    while (offset < body.length) {
      const gap = body.slice(offset).match(/^[\x20\t\r\n]+/);
      if (!gap) fail("ASYNC_XML_ATTRIBUTE_INVALID");
      offset += gap[0].length;
      if (offset === body.length) break;
      const a = body.slice(offset).match(NAME);
      if (!a) fail("ASYNC_XML_ATTRIBUTE_INVALID");
      const key = a[0];
      if (key === "xmlns" || Object.hasOwn(attributes, key)) fail("ASYNC_XML_ATTRIBUTE_INVALID");
      offset += key.length;
      const equals = body.slice(offset).match(/^[\x20\t\r\n]*=[\x20\t\r\n]*(["'])/);
      if (!equals) fail("ASYNC_XML_ATTRIBUTE_INVALID");
      offset += equals[0].length;
      const end = body.indexOf(equals[1], offset);
      if (end === -1) fail("ASYNC_XML_ATTRIBUTE_INVALID");
      const value = body.slice(offset, end);
      if (value.includes("<")) fail("ASYNC_XML_ATTRIBUTE_INVALID");
      if (value.includes(">")) fail("ASYNC_XML_ATTRIBUTE_UNSUPPORTED");
      entities(value);
      attributes[key] = value;
      if (Object.keys(attributes).length > 64) fail("ASYNC_XML_ATTRIBUTE_LIMIT");
      offset = end + 1;
    }
    return { name, attributes };
  }
  function inspect(xml, { maxDepth, maxNodes, maxResults }) {
    let p = xml.charCodeAt(0) === 0xFEFF ? 1 : 0;
    const start = p, stack = [];
    let rootCount = 0, responses = 0, nodes = 0, docs = 0, rootClosed = false;
    let errorCode = null, errors = 0, responseFound = null;
    const finish = node => {
      if (node.name === "found" && node.parent === "response") {
        if (/^[\x20\t\r\n]*[0-9]+[\x20\t\r\n]*$/.test(node.text)) {
          const value = node.text.trim().replace(/^0+(?=\d)/, "");
          // Multiple priorities may have different positive totals. Only zero consensus is proof.
          responseFound = responseFound === null ? value : (responseFound === "0" && value === "0" ? "0" : "positive-or-mixed");
        } else fail("ASYNC_XML_FOUND_INVALID");
      }
    };
    const append = (text, cdata = false) => {
      if (!cdata) { entities(text); if (text.includes("]]>")) fail("ASYNC_XML_TEXT_INVALID"); }
      if (!stack.length) { if (!SPACE.test(text)) fail("ASYNC_XML_OUTSIDE_ROOT"); return; }
      const current = stack[stack.length - 1];
      if (current.name === "found" && current.parent === "response") {
        if (current.text.length + text.length > 100) fail("ASYNC_XML_FOUND_INVALID");
        current.text += text;
      }
    };
    while (p < xml.length) {
      if (xml[p] !== "<") {
        const next = xml.indexOf("<", p), end = next === -1 ? xml.length : next;
        append(xml.slice(p, end)); p = end; continue;
      }
      if (xml.startsWith("<!--", p)) {
        const end = xml.indexOf("-->", p + 4);
        if (end < 0 || xml.slice(p + 4, end).includes("--") || xml[end - 1] === "-") fail("ASYNC_XML_COMMENT_INVALID");
        p = end + 3; continue;
      }
      if (xml.startsWith("<![CDATA[", p)) {
        if (!stack.length) fail("ASYNC_XML_OUTSIDE_ROOT");
        const end = xml.indexOf("]]>", p + 9);
        if (end < 0) fail("ASYNC_XML_CDATA_INVALID");
        append(xml.slice(p + 9, end), true); p = end + 3; continue;
      }
      if (xml.startsWith("<?", p)) {
        const end = xml.indexOf("?>", p + 2);
        if (end < 0) fail("ASYNC_XML_DECLARATION_INVALID");
        const decl = xml.slice(p + 2, end);
        if (p !== start || !/^xml[\x20\t\r\n]/.test(decl)) fail("ASYNC_XML_DECLARATION_UNSUPPORTED");
        const a = tagBody(decl).attributes;
        const keys = Object.keys(a);
        if (keys[0] !== "version" || a.version !== "1.0" ||
          keys.some(k => !["version", "encoding", "standalone"].includes(k)) ||
          (a.encoding && !/^UTF-8$/i.test(a.encoding)) ||
          (a.standalone && !["yes", "no"].includes(a.standalone))) fail("ASYNC_XML_DECLARATION_UNSUPPORTED");
        p = end + 2; continue;
      }
      if (xml.startsWith("<!", p)) fail("ASYNC_XML_DTD_UNSUPPORTED");
      // Locate the end without treating a quoted '>' as the end of a tag.
      let end = p + 1, quote = null;
      for (; end < xml.length; end++) {
        const ch = xml[end];
        if (quote) { if (ch === quote) quote = null; }
        else if (ch === '"' || ch === "'") quote = ch;
        else if (ch === ">") break;
        else if (ch === "<") fail("ASYNC_XML_TAG_INVALID");
      }
      if (end === xml.length || quote) fail("ASYNC_XML_TRUNCATED");
      const body = xml.slice(p + 1, end); p = end + 1;
      if (body.startsWith("/")) {
        const close = body.slice(1).match(/^([A-Za-z_][A-Za-z0-9_.-]*)[\x20\t\r\n]*$/);
        const node = stack.pop();
        if (!close || !node || node.name !== close[1]) fail("ASYNC_XML_NESTING_INVALID");
        finish(node); if (!stack.length) rootClosed = true; continue;
      }
      const selfClosing = body.endsWith("/");
      const node = tagBody(selfClosing ? body.slice(0, -1) : body);
      node.parent = stack.length ? stack[stack.length - 1].name : null;
      node.inResponse = node.name === "response" || Boolean(stack[stack.length - 1]?.inResponse);
      node.text = "";
      if (++nodes > maxNodes || stack.length + 1 > maxDepth) fail("ASYNC_XML_COMPLEXITY_LIMIT");
      if (!stack.length) {
        if (rootClosed || ++rootCount !== 1 || node.name !== "yandexsearch") fail("ASYNC_XML_ROOT_INVALID");
      }
      if (node.name === "response") {
        if (node.parent !== "yandexsearch" || ++responses > 1) fail("ASYNC_XML_RESPONSE_INVALID");
      }
      if (node.name === "error") {
        if (node.parent !== "response" || ++errors > 1 || !/^[0-9]{1,9}$/.test(node.attributes.code || "")) fail("ASYNC_XML_ERROR_INVALID");
        errorCode = Number(node.attributes.code);
      }
      if (node.name === "doc") {
        if (!node.inResponse || node.parent !== "group" || ++docs > maxResults) fail("ASYNC_XML_DOC_STRUCTURE_INVALID");
      }
      if (selfClosing) { finish(node); if (!stack.length) rootClosed = true; }
      else stack.push(node);
    }
    if (stack.length || !rootClosed || rootCount !== 1 || responses !== 1) fail("ASYNC_XML_RESPONSE_INVALID");
    if (errors && docs) fail("ASYNC_XML_AMBIGUOUS_RESULT");
    if (errorCode === 15 && responseFound !== null && responseFound !== "0") fail("ASYNC_XML_AMBIGUOUS_RESULT");
    if (docs && responseFound === "0") fail("ASYNC_XML_AMBIGUOUS_RESULT");
    if (errors && errorCode !== 15) fail("ASYNC_XML_PROVIDER_ERROR");
    const emptyProven = !docs && (errorCode === 15 || responseFound === "0");
    if (!docs && !emptyProven) fail("ASYNC_XML_EMPTY_UNPROVEN");
    return { docs, emptyProven, errorCode, nodes };
  }
  function create({ xmlNormalizer = globalThis.YMBSearchXml, maxRawBytes,
    maxDepth = 48, maxNodes = 40000, maxResults = 300 } = {}) {
    if (!xmlNormalizer?.normalizeXml || !Number.isSafeInteger(xmlNormalizer.MAX_XML_CHARS)) fail("ASYNC_XML_BASELINE_MISSING");
    for (const value of [maxRawBytes, maxDepth, maxNodes, maxResults]) if (!Number.isSafeInteger(value) || value < 1) fail("ASYNC_XML_BUDGET_REQUIRED");
    if (maxDepth > 48 || maxNodes > 40000 || maxResults > 300 || maxRawBytes > xmlNormalizer.MAX_XML_CHARS * 4) fail("ASYNC_XML_BUDGET_INVALID");
    return function normalizeRaw({ rawData } = {}) {
      if (typeof rawData !== "string" || !rawData.length) fail("ASYNC_BASE64_INVALID");
      if (rawData.length > 4 * Math.ceil(maxRawBytes / 3)) fail("ASYNC_XML_BYTE_BUDGET");
      if (rawData.length % 4 || !/^[A-Za-z0-9+/]*={0,2}$/.test(rawData)) fail("ASYNC_BASE64_INVALID");
      const padding = rawData.endsWith("==") ? 2 : rawData.endsWith("=") ? 1 : 0;
      const expected = rawData.length / 4 * 3 - padding;
      if (expected > maxRawBytes) fail("ASYNC_XML_BYTE_BUDGET");
      // RFC 4648 canonical pad bits. No full re-encode/copy of the payload.
      const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
      if ((padding === 2 && (alphabet.indexOf(rawData.at(-3)) & 15)) ||
        (padding === 1 && (alphabet.indexOf(rawData.at(-2)) & 3))) fail("ASYNC_BASE64_INVALID");
      let binary;
      try { binary = atob(rawData); } catch { fail("ASYNC_BASE64_INVALID"); }
      if (binary.length !== expected) fail("ASYNC_BASE64_INVALID");
      let bytes = new Uint8Array(expected);
      for (let i = 0; i < expected; i++) bytes[i] = binary.charCodeAt(i);
      binary = null;
      let xml;
      try { xml = new TextDecoder("utf-8", { fatal: true }).decode(bytes); } catch { fail("ASYNC_XML_UTF8_INVALID"); }
      bytes = null;
      if (xml.length > xmlNormalizer.MAX_XML_CHARS) fail("ASYNC_XML_CHAR_BUDGET");
      if (/[\u0000-\u0008\u000b\u000c\u000e-\u001f\ufffe\uffff]/u.test(xml)) fail("ASYNC_XML_CHARACTER_INVALID");
      const checked = inspect(xml, { maxDepth, maxNodes, maxResults });
      // Preserve the accepted sync mapper's rank/url/domain/title/snippet semantics.
      const normalized = xmlNormalizer.normalizeXml(xml);
      if (normalized.results.length !== checked.docs) fail("ASYNC_XML_MAPPER_COUNT_MISMATCH");
      const missingUrlRanks = [], unsafeUrlRanks = [];
      for (const row of normalized.results) {
        if (!row.url) missingUrlRanks.push(row.rank);
        else { try { const u = new URL(row.url); if (!["https:", "http:"].includes(u.protocol) || u.username || u.password) unsafeUrlRanks.push(row.rank); } catch { unsafeUrlRanks.push(row.rank); } }
      }
      return Object.freeze({ ...normalized, validation: Object.freeze({
        schema: "YMB_ASYNC_XML_GUARD_V1", document_count: checked.docs,
        empty_proven: checked.emptyProven, xml_error_code: checked.errorCode,
        usable_for_url_comparison: checked.docs > 0 && !missingUrlRanks.length && !unsafeUrlRanks.length,
        missing_url_ranks: Object.freeze(missingUrlRanks), unsafe_url_ranks: Object.freeze(unsafeUrlRanks)
      }) });
    };
  }
  globalThis.YMBSearchAsyncNormalizer = Object.freeze({ create });
})();
