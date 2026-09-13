(() => {
  "use strict";
  const ACTION_ATTR = "data-ymb-manual-action";
  const BLOCK_ATTR = "data-ymb-block-id";
  const ACTION_LABEL = "Яндекс";
  function makeId(prefix = "ymb") {
    return `${prefix}-${globalThis.crypto?.randomUUID?.() || Math.random().toString(36).slice(2)}`;
  }
  globalThis.BB2ManualControls = Object.freeze({ ACTION_ATTR, BLOCK_ATTR, ACTION_LABEL, makeId });
})();
