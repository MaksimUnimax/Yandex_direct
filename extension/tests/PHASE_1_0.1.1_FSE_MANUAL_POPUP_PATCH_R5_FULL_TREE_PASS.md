# FSE Manual/popup patch R5 — revision-2 complete tree regression

Date: 2026-08-17
Base candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`

Status: **PASS — 321/321**.

The exact-candidate-derived working tree contains the transaction-order revision in `popup.js` and the two focused regression groups in the existing popup test file. No other production file is changed.

```text
321 tests
321 PASS
0 FAIL
0 skipped
0 cancelled
```

This full regression includes popup, worker, content runtime, Manual, Autorun, protocol/transport, policy/cost, persistence/import/export, diagnostics, delivery/recovery, duplicate/concurrency, unknown-outcome/no-retry, DOM/locality, source guards and security/secret-containment suites.

The result therefore confirms that the revised popup transaction/error-boundary logic did not regress the existing worker/content/provider and exactly-once safety contours.

No real/external Yandex request occurred.
