# Phase 1 0.1.1 — K-02 generic ChatGPT code-block DOM patch plan

Date: 2026-08-17
Status: CONTROLLED/PACKAGED PASS — REAL CURRENT-CHROME K-02 RERUN PENDING.
Authority: owner explicitly interrupted the K campaign and ordered an immediate patch after the governed K-02/C-01 real-current-Chrome FAIL in authoritative ledger section 8.4.

## Root cause and authorized production scope

The consolidated candidate inherited the Wordstat 1.1.5 DOM adapter, which does not bind current generic assistant `<pre><code>...</code></pre>`. Ozon Bridge v0.1.11 independently records/corrects the same live failure class.

Authorized production changes are limited to:
1. `content_script.js`: current assistant-container resolution, fail-closed generic pre/code binding, initial/MutationObserver discovery and existing locality integration while preserving legacy/current writing-block, native Copy, generic response Copy exclusion, conversation scoping and duplicate fences.
2. `shared/manual_controls.js`: add `generic_pre_code_v1` to supported copy-profile adapters and change builtin adapter count 2→3; locality/normalization logic otherwise unchanged.

No worker, popup, provider, pricing, request/result, delivery, credential, permission or Autorun execution semantics are authorized.

Mandatory regressions were defined before execution: old/new DOM families, ambiguity/non-assistant failures, Copy locality/native/duplicate safety, discovery lifecycle, Manual OFF/ON, profile compatibility, changed-line execution, full source/fresh-ZIP suites, syntax/JSON, package identity, exact production-delta scope and zero live Yandex requests.

## Execution results

- **R1 PASS:** focused dependency VM 32/32; network 0.
- **R2 PASS:** Chromium baseline reproduces generic DOM defect (no decoration/0 admission); patch on identical DOM becomes yellow and two native clicks yield exactly one admission, neither prevented; legacy/current-writing contours remain green; accepted browser errors 0. Preliminary harness navigation/secure-context attempts were infrastructure TEST ERROR.
- **R3 PASS:** Chromium CDP precise coverage executes `content_script.js` 31/31 changed/new lines and `shared/manual_controls.js` 3/3 = **34/34**, uncovered 0; network 0.
- **R4 FAIL:** first full source run 317/319; only two obsolete byte-identity provenance assertions for intentionally changed `manual_controls.js`; no runtime/behavior failure. Old SHA `81f302487da7b5ff7c1b746298353438b2cfec100a5bb8f7fa2c80d1e033c81e`; patched SHA `241f07a4aeb0882a424ea7e312278ed40a8a67732ca7ee05ab651a6715276bc2`.
- **R5 PASS:** provenance dependency rerun 35/35. Three untouched common modules retain exact reference hashes; patched manual-controls exact hash required; removing only new adapter line and count 3→2 must reproduce old reference hash, so unrelated changes fail audit.
- **R6 PASS:** complete patched source suite **319/319**, fail/skipped/cancelled 0.
- **R7 PASS:** JS/MJS syntax 37/37; JSON 2/2; exact same 42-file path set; changed files total 6 (2 production + 4 regression tests); production delta only `content_script.js` and `shared/manual_controls.js`; manifest/worker/popup/protocol byte-identical; permissions/hosts unchanged; network 0.
- **R8 PASS — deterministic package and fresh extraction:**

```text
candidate: yandex-marketing-bridge-0.1.1-phase1-k02-generic-dom-patch-candidate.zip
SHA-256: 46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c
bytes: 178143
files: 42

deterministic rebuild: byte-identical PASS
source ↔ fresh ZIP: 42/42 byte-identical PASS
fresh ZIP full suite: 319/319 PASS
fresh JS/MJS syntax: 37/37 PASS
fresh manifest/package JSON: 2/2 PASS
Chromium --pack-extension: exit 0 PASS
live Yandex requests during patch/verification: 0
```

Exact production hashes:
- `content_script.js`: base `148c8205bc360ba0e08a07945c3f283c5ca83eab81332c92ab8606e16d6b4f01` → patch `a5677a45fd1e94fa82ef6fa3e368d23a27767c834fcc67fb53e138517878b57f`;
- `shared/manual_controls.js`: base `81f302487da7b5ff7c1b746298353438b2cfec100a5bb8f7fa2c80d1e033c81e` → patch `241f07a4aeb0882a424ea7e312278ed40a8a67732ca7ee05ab651a6715276bc2`.

Next: create reproducible patch artifact + machine-readable evidence, commit them, then record the patch checkpoint in the authoritative live ledger. Only after that may the final ZIP be installed for real-current-Chrome K-02 rerun.

## Acceptance boundary

Controlled/static/package PASS does not make K-02 live PASS. The final patched ZIP must still be installed in real current Chrome and visibly decorate the supported Copy. Other K gates retain their governed state.