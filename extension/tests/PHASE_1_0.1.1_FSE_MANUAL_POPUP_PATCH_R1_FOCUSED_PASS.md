# FSE Manual/popup patch R1 — focused regression

Date: 2026-08-17
Base candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`

Status: **PASS — 13/13** on the exact-candidate-derived patched working tree.

Authorized production delta at this point:

```text
popup.js
base SHA-256:    f668ec90c8519d89d0c1b3d3b011e5908ac1a5d7335519091d22119d838ddde4
patched SHA-256: 7ab4543f7c952b9936aa34cba9712dcf96df5d76791ec558e11d07fa941080ce
```

No other production file is changed in the working tree.

Focused popup suite:

```text
13 tests
13 PASS
0 FAIL
```

The 11 existing popup-runtime regressions remain green. Two new focused groups also pass:

1. Manual acknowledgement/reconciliation matrix:
   - ON + confirmed content apply → worker/content/popup ON;
   - OFF + confirmed content apply → worker/content/popup OFF;
   - ON + apply transport failure → worker rolled back OFF, popup OFF, error status;
   - ON + `{ok:true, applied:false}` → worker rolled back OFF, popup OFF, error status;
   - OFF + transport failure → worker remains hard-safe OFF, popup OFF, explicit reconciliation error instead of false observer/listener-removal success;
   - OFF + `applied:false` → same safe/truthful behavior.
2. Common popup async error boundary:
   - Send picker;
   - Copy picker;
   - Pause;
   - Resume;
   - Finish;
   - Clear Send;
   - Clear Copy;
   - Export;
   - Import;
   - Clear diagnostics;
   - clipboard Copy diagnostics;
   all complete without escaping rejected async event callbacks and expose controlled status text on their injected negative path.

Implementation behavior under test:

- `busy()` now catches otherwise-uncaught action exceptions, renders error status, returns `null`, and still restores button/render state in `finally`;
- Manual success is accepted only when the content acknowledgement has both `ok:true` and `applied:true`;
- failed Manual ON acknowledgement performs safe worker rollback to OFF plus best-effort content OFF;
- failed Manual OFF acknowledgement retains authoritative worker OFF and reports incomplete content reconciliation rather than claiming observer/listener/decor removal.

No worker/content/provider/request/permission production change was made. No real/external Yandex request occurred.
