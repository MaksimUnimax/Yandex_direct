(() => {
  "use strict";

  function assistantContainerFor(node) {
    return node?.closest?.('[data-message-author-role="assistant"], article, [data-testid^="conversation-turn-"]') || null;
  }

  function isWholeResponseCopy(button) {
    if (!button) return false;
    const label = String(button.getAttribute?.("aria-label") || button.title || button.textContent || "").toLowerCase();
    const block = button.closest?.('pre, [data-testid="code-block"], .code-block, #code-block-viewer');
    return !block && /copy|копир/u.test(label);
  }

  function blockForCopy(button) {
    if (!button || isWholeResponseCopy(button)) return null;
    const direct = button.closest?.('pre, [data-testid="code-block"], .code-block, #code-block-viewer');
    if (direct) return direct;
    const parent = button.parentElement;
    if (!parent) return null;
    const candidates = parent.querySelectorAll?.('pre, [data-testid="code-block"], .code-block, #code-block-viewer') || [];
    return candidates.length === 1 ? candidates[0] : null;
  }

  function textFromBlock(block) {
    if (!block) return "";
    const cm = block.querySelector?.('.cm-content, [contenteditable="false"].cm-content');
    if (cm) return String(cm.innerText || cm.textContent || "").replace(/\r\n?/g, "\n");
    const code = block.querySelector?.('code');
    return String((code || block).innerText || (code || block).textContent || "").replace(/\r\n?/g, "\n");
  }

  function candidateBlocks(doc = document) {
    const out = [];
    const seen = new Set();
    for (const block of doc.querySelectorAll('pre, [data-testid="code-block"], .code-block, #code-block-viewer')) {
      if (seen.has(block) || !assistantContainerFor(block)) continue;
      seen.add(block); out.push(block);
    }
    return out;
  }

  globalThis.BB2ProvenWritingCapture = Object.freeze({ assistantContainerFor, isWholeResponseCopy, blockForCopy, textFromBlock, candidateBlocks });
})();
