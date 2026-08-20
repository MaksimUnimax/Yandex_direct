(() => {
  "use strict";

  function findComposer(doc = document) {
    const selectors = [
      '#prompt-textarea',
      'div[contenteditable="true"][data-lexical-editor="true"]',
      'div[contenteditable="true"][role="textbox"]',
      'textarea'
    ];
    for (const selector of selectors) {
      const el = doc.querySelector(selector);
      if (el) return el;
    }
    return null;
  }

  function readComposer(el) {
    if (!el) return "";
    if ("value" in el && typeof el.value === "string") return el.value;
    return String(el.innerText ?? el.textContent ?? "");
  }

  function setComposerText(el, text) {
    if (!el) return false;
    const value = String(text || "");
    el.focus?.();
    if ("value" in el && typeof el.value === "string") {
      const setter = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(el), "value")?.set;
      if (setter) setter.call(el, value); else el.value = value;
      el.dispatchEvent(new Event("input", { bubbles: true }));
      return true;
    }
    el.textContent = value;
    el.dispatchEvent(new InputEvent("input", { bubbles: true, inputType: "insertText", data: value }));
    return true;
  }

  function findSendButton(doc = document) {
    const selectors = [
      'button[data-testid="send-button"]',
      'button[aria-label*="Send" i]',
      'button[aria-label*="Отправ" i]'
    ];
    for (const selector of selectors) {
      const el = doc.querySelector(selector);
      if (el && !el.disabled) return el;
    }
    return null;
  }

  function composerReady(doc = document) {
    const mic = doc.querySelector('button[aria-label*="voice" i], button[aria-label*="microphone" i], button[aria-label*="голос" i], button[aria-label*="микроф" i]');
    return Boolean(mic) && !findSendButton(doc) && !readComposer(findComposer(doc)).trim();
  }

  globalThis.BB2ComposerSend = Object.freeze({ findComposer, readComposer, setComposerText, findSendButton, composerReady });
})();
