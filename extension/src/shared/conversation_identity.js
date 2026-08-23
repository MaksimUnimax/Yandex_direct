(() => {
  "use strict";

  const CHAT_ID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  const ALLOWED_ORIGINS = new Set(["https://chatgpt.com", "https://chat.openai.com"]);

  function normalizeOrigin(value) {
    try {
      const u = new URL(String(value || ""));
      return ALLOWED_ORIGINS.has(u.origin) ? u.origin : "";
    } catch { return ""; }
  }

  function identityFromUrl(value) {
    let url;
    try { url = new URL(String(value || "")); }
    catch { return Object.freeze({ origin: "", conversation_id: "", conversation_key: "", status: "unavailable", source: "url" }); }
    const origin = normalizeOrigin(url.origin);
    const m = url.pathname.match(/^\/c\/([^/?#]+)/i);
    const conversationId = m && CHAT_ID_RE.test(m[1]) ? m[1].toLowerCase() : "";
    return Object.freeze({
      origin,
      conversation_id: conversationId,
      conversation_key: origin && conversationId ? `${origin}|${conversationId}` : "",
      status: origin && conversationId ? "confirmed" : "unconfirmed",
      source: "path",
      chat_path: conversationId ? `/c/${conversationId}` : url.pathname
    });
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
    identityFromUrl,
    normalizeConversationKey,
    sameConversation
  });
})();
