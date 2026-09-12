(() => {
  "use strict";

  // ChatGPT conversation ids are UUID-shaped opaque identifiers. Do not impose
  // RFC UUID version/variant semantics: factual owner live evidence contains
  // e.g. 6a82924e-5ed0-83eb-84a2-851ddad40c88.
  const CHAT_ID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  const ALLOWED_ORIGINS = new Set(["https://chatgpt.com", "https://chat.openai.com"]);

  function normalizeOrigin(value) {
    try {
      const u = new URL(String(value || ""));
      return ALLOWED_ORIGINS.has(u.origin) ? u.origin : "";
    } catch { return ""; }
  }

  function conversationIdFromPath(pathname) {
    const match = String(pathname || "").match(/(?:^|\/)c\/([^/?#]+)(?:\/|$)/i);
    return match && CHAT_ID_RE.test(match[1]) ? match[1].toLowerCase() : "";
  }

  function identityFromUrl(value) {
    let url;
    try { url = new URL(String(value || "")); }
    catch { return Object.freeze({ origin: "", conversation_id: "", conversation_key: "", status: "unavailable", source: "url", chat_path: "" }); }
    const origin = normalizeOrigin(url.origin);
    const conversationId = conversationIdFromPath(url.pathname);
    return Object.freeze({
      origin,
      conversation_id: conversationId,
      conversation_key: origin && conversationId ? `${origin}|${conversationId}` : "",
      status: origin && conversationId ? "confirmed" : "unconfirmed",
      source: "path",
      chat_path: conversationId ? `/c/${conversationId}` : url.pathname
    });
  }

  function identityFromCandidates(values) {
    const identities = [];
    for (const value of Array.isArray(values) ? values : [values]) {
      const text = String(value || "").trim();
      if (!text) continue;
      identities.push(identityFromUrl(text));
    }

    const confirmedByKey = new Map();
    for (const current of identities) {
      if (current.status === "confirmed" && current.conversation_key) confirmedByKey.set(current.conversation_key, current);
    }

    if (confirmedByKey.size === 1) return [...confirmedByKey.values()][0];
    if (confirmedByKey.size > 1) {
      return Object.freeze({
        origin: "",
        conversation_id: "",
        conversation_key: "",
        status: "conflict",
        source: "candidates",
        chat_path: ""
      });
    }

    if (identities.length) return identities[0];
    return Object.freeze({ origin: "", conversation_id: "", conversation_key: "", status: "unavailable", source: "candidates", chat_path: "" });
  }

  function normalizeConversationKey(value, { required = false } = {}) {
    const text = String(value || "").trim();
    const idx = text.indexOf("|");
    const origin = idx > 0 ? normalizeOrigin(text.slice(0, idx)) : "";
    const id = idx > 0 ? text.slice(idx + 1).trim().toLowerCase() : "";
    if (origin && CHAT_ID_RE.test(id)) return `${origin}|${id}`;
    if (required) {
      const error = new Error("Не удалось подтвердить текущий ChatGPT-диалог.");
      error.code = "CONVERSATION_KEY_INVALID";
      throw error;
    }
    return "";
  }

  function sameConversation(a, b) {
    return Boolean(normalizeConversationKey(a) && normalizeConversationKey(a) === normalizeConversationKey(b));
  }

  globalThis.BB2ConversationIdentity = Object.freeze({
    CHAT_ID_RE,
    ALLOWED_ORIGINS,
    normalizeOrigin,
    conversationIdFromPath,
    identityFromUrl,
    identityFromCandidates,
    normalizeConversationKey,
    sameConversation
  });
})();
