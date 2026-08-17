# FSE Manual/popup patch R2 — complete patched-tree suite

Date: 2026-08-17
Base candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`
Patched `popup.js` SHA-256: `7ab4543f7c952b9936aa34cba9712dcf96df5d76791ec558e11d07fa941080ce`

Status: **PASS — 321/321**.

```text
321 tests
321 PASS
0 FAIL
0 skipped
0 cancelled
```

The complete package test corpus was executed from the patched working tree. The prior 319 tests remain present and two new focused popup regression groups are added in the existing popup exhaustive test file.

The full suite includes worker/content/transport/protocol/policy/security/export-import/Autorun/recovery/concurrency/source-guard regressions; therefore the popup-only production change did not regress those previously proven contours.

No real/external Yandex request occurred.
