# FSE Manual/popup patch R3 — changed-line coverage checkpoint

Date: 2026-08-17
Base candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`
Intermediate patched `popup.js` SHA-256: `7ab4543f7c952b9936aa34cba9712dcf96df5d76791ec558e11d07fa941080ce`

Status: **INCOMPLETE COVERAGE — 26/28 changed nonblank production lines executed. No product FAIL inferred from coverage alone.**

Node V8 coverage was collected while executing the exact patched `popup.js` through the popup runtime harness.

```text
changed/new popup.js lines: 32 total, 28 nonblank
executed changed nonblank lines: 26/28
unexecuted: 2
```

The only uncovered production branch is the intermediate implementation's second-order failure path after:

1. worker Manual ON has already been committed;
2. content ON acknowledgement fails;
3. attempted worker rollback to OFF also fails.

Uncovered source statements are the branch that forces the checkbox false and reports that rollback was not confirmed.

This checkpoint is intentionally not declared PASS. Dependency review of the uncovered branch produced a safer transaction-order correction for the patch itself:

- enabling Manual should apply/acknowledge content first while the authoritative worker hard gate remains OFF, then commit worker ON only after `applied:true`;
- disabling Manual should retain the opposite safety order: commit worker OFF first, then remove content-side Manual state;
- if worker ON commit fails after a successful content apply, worker remains OFF and content must be best-effort disarmed;
- this removes the need for a worker ON→OFF rollback after failed content acknowledgement and keeps the irreversible API authorization gate safe throughout.

The patch plan must be amended before implementing this transaction-order refinement. No real/external Yandex request occurred.
