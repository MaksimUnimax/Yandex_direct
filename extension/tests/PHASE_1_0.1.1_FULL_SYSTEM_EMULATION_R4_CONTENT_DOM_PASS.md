# FSE R4 — production content-script Chromium DOM/event matrix

Date: 2026-08-17
Candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`
Chromium renderer/V8: 144.0.7559.96

Status: **PASS — 34/34**.

Because managed local Chromium policy blocks unpacked-extension installation, the exact production shared modules plus exact `content_script.js` were executed inside a real Chromium renderer with only two controlled environment substitutions:

1. confirmed ChatGPT conversation identity supplied at the `BB2ConversationIdentity` boundary;
2. `crypto.randomUUID` polyfilled because `about:blank` is not a secure context, while real `https://chatgpt.com` provides this API.

The `chrome.runtime` boundary was recorded and emulated; no Yandex transport was available in this batch.

Matrix covered:

- current writing-block DOM;
- legacy `#code-block-viewer` DOM;
- generic assistant `<pre><code>` under historical section identity;
- generic assistant `<pre><code>` under `[data-message-author-role=assistant]`;
- local toolbar Copy before/after block when both share a local wrapper below the assistant section;
- direct section-level sibling Copy fail-closed because the only common ancestor is the whole assistant section;
- Copy recognition independently through visible text, data-testid containing `copy`, aria-label, title and legacy SVG-use marker;
- nested wrappers;
- role-only assistant container;
- `copy-turn-action-button` / `Copy response` exclusion;
- non-HTMLButton role=button fail-closed;
- missing assistant identity fail-closed;
- section without turn-id and without role fail-closed;
- ambiguous multi-code root fail-closed;
- ambiguous two-Copy root fail-closed;
- no-Copy root;
- non-command and empty-code blocks may be visually armed but double click produces zero execution admission;
- delayed Copy insertion and delayed command-block insertion through real MutationObserver;
- Manual initial OFF;
- valid conversation-scoped Manual push ON decorates existing block;
- push OFF restores native styling;
- different-conversation Manual push fails closed;
- valid command rapid double click preserves native click events twice while producing exactly one execution admission at the runtime boundary;
- generic response Copy rapid double click remains native and produces zero execution admission.

Formal result:

```text
34 cases
34 PASS
0 FAIL
```

Two initial direct-sibling expectations were corrected as TEST ERROR before this formal result: the production locality invariant intentionally rejects a candidate whose only shared ancestor with the code block is the entire assistant section. New wrapper-toolbar cases prove the intended sibling-toolbar contour.

One initial click-admission observation was also TEST ERROR: insecure `about:blank` lacked `crypto.randomUUID`, causing execution to stop before the runtime boundary. Adding only the secure-context UUID API present on real ChatGPT resolved the harness error; no production line was changed.

This R4 PASS does **not** supersede the owner's real-current-Chrome patched-candidate K-02 FAIL. It establishes only the enumerated controlled DOM/event/state contracts. No real/external Yandex request occurred.
