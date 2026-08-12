# Phase 1 — 0.1.1 repair WIP checkpoint

Date: 2026-08-12
Status: **WIP / NOT A RELEASE CANDIDATE**

This checkpoint exists so the current repair cannot be lost if the development conversation or local workspace disappears.

## Base

Exact withdrawn candidate:

```text
yandex-marketing-bridge-0.1.0-phase1-wordstat-candidate.zip
SHA-256 79c2bca5e2e65aaa1cb7cc38754589a0bf3b0b436c82f36416934cd175cafa2a
```

The current WIP is a repair on top of that candidate.

## Recoverable source delta

The complete current WIP source delta is stored as sequential patch fragments:

```text
extension/tests/wip/phase1-0.1.1-repair/part-000.patch
extension/tests/wip/phase1-0.1.1-repair/part-001.patch
extension/tests/wip/phase1-0.1.1-repair/part-002.patch
extension/tests/wip/phase1-0.1.1-repair/part-003.patch
extension/tests/wip/phase1-0.1.1-repair/part-004.patch
extension/tests/wip/phase1-0.1.1-repair/part-005.patch
```

Concatenate them in numeric order to reconstruct the unified diff.

Original local unified diff evidence:

```text
SHA-256 594d13d01db858ff5a944abbaef5616a33163669b39a13b9ea87ba8ab3416ecb
bytes   104230
lines   1782
```

Machine-readable checkpoint evidence:

```text
extension/tests/PHASE_1_0.1.1_REPAIR_WIP_EVIDENCE.json
```

A base64 source-snapshot transfer was also started under:

```text
extension/tests/wip/phase1-0.1.1-repair/snapshot-base64/
```

Do not treat an incomplete chunk set as authoritative; the six patch fragments above are the recovery authority for the current WIP delta.

## Current changed-file SHA-256

```text
manifest.json                    a91d6bff606a8bd2e440543392e61692b107dabd81978b7323d7c5f9afb61ddb
package.json                     2c2893f009c894858366ce74b89dfb54e68d22dfccc59541eca1bfb2fa08412e
content_script.js                54832342f003ddefd6f029f02ba4d4b17068001dc7d6edcccd0990ae0fe94ac6
popup.html                       af3ae634104a17bc1341e1dfea38eb908ca76f350754c78821defd10948989a4
popup.js                         4e3e99a9da591bd13d4de34e6fc86213764f8990ce323014b7302138dec6f90b
service_worker.js                03172e12228ac0a9ffc683a93b0e4c5c36f7482a9bdde979f2aac11e25cb881a
shared/job_model.js              3581d69c4e17225935bddaa02e62b186d909650b0f2f8d533d89028ca9856010
shared/policy_model.js           7dc6c809b7f81b01d3ffc95ecb558747d50f3512df7dc361955a2cab56532063
shared/product.js                f5257f3dc5512f1f4ebfc9f6ca22a012817afca3f35cafb2f22cf057d3b94c34
shared/wordstat_protocol.js      34cf8e36d513269deabd41c80da9126fc4a6c8fe1e66c3efeae50266caf621bc
```

## Implemented in WIP so far

- remove mandatory `job_id` from extension run/execution/result path;
- remove GitHub/workspace coupling from extension popup/runtime path;
- keep GitHub order workspace as external ChatGPT/development workflow only;
- replace job-level extension budgets with run-level limits;
- add Debug Mode setting: errors are delivered regardless of Debug Mode, while Debug Mode only adds extra redacted logs;
- add always-on `YMB_ERROR_V1` ChatGPT delivery scaffold for Manual/Autorun/runtime/content failures;
- make recoverable Autorun failures return toward `WAITING_COMMAND` instead of terminal `ERROR` when safe;
- preserve no-blind-retry semantics for unknown request outcome;
- add versioned secret settings export/import scaffold with canonical SHA-256 validation and active-run preservation;
- add error-delivery durable claim/commit/reconciliation scaffold;
- bump WIP product/manifest/package/result fallback version to `0.1.1`.

## Current test state

The legacy suite is intentionally not green yet because old assertions still require the rejected 0.1.0 Job/runtime model.

Recorded runs:

```text
first repair run:      277 PASS / 22 FAIL / 299 total
after restore pass:    280 PASS / 19 FAIL / 299 total
```

These failures are **not accepted**. They must be classified into:

1. obsolete assertions that encode removed `job_id`/per-JOB/runtime GitHub behavior;
2. real regressions that must be fixed before packaging.

## Required continuation

Do not start Search.

Continue Phase 1 repair by:

1. classify every remaining failing legacy test;
2. rewrite only assertions that encode the explicitly rejected Job/GitHub runtime model;
3. add dedicated tests for every input/output/error path;
4. emulate `writing block -> capture -> policy -> fetch/no-fetch -> result/error -> composer -> Send -> continuation`;
5. test Debug OFF and Debug ON separately;
6. test all error classes automatically arrive in ChatGPT;
7. test recoverable Autorun errors continue the run;
8. test unknown paid-request outcome never retries automatically;
9. test Export/Import checksum, secrets, merge semantics, legacy `wsmb_*` compatibility and active-run preservation;
10. restore/reference-check all required toast/status UI behavior;
11. run source suite, fresh ZIP suite, source↔ZIP identity, syntax/JSON and Chromium-load smoke;
12. append final documentation and only then produce a new live-test candidate.

No paid Yandex request was executed while producing this checkpoint.
