# Phase 1 0.1.1 — K-02 generic ChatGPT code-block DOM patch plan

Date: 2026-08-17
Status: PATCH IN CONTROLLED VERIFICATION — LIVE K-02 STILL PENDING.
Authority: owner explicitly interrupted the K campaign and ordered an immediate patch after the governed K-02/C-01 real-current-Chrome FAIL in the authoritative ledger section 8.4.

## Root cause

The consolidated Yandex candidate inherited the Wordstat 1.1.5 DOM adapter: special writing-block families plus legacy `<pre>` only when `#code-block-viewer` exists. Current ordinary assistant `<pre><code>...</code></pre>` therefore has no binding and is omitted from initial/manual MutationObserver discovery. Ozon Bridge v0.1.11 independently records/corrects the same live failure class.

## Authorized production scope

1. `content_script.js`: support historical assistant sections plus `[data-message-author-role="assistant"]`; add fail-closed generic assistant `<pre><code>` binding; preserve legacy precedence; include generic roots in initial/MutationObserver discovery; use existing locality algorithm for sibling Copy; preserve native Copy, generic response Copy exclusion, conversation scoping and duplicate fences.
2. `shared/manual_controls.js`: register `generic_pre_code_v1` so copy-profile fallback/picker supports the new binding family; keep locality and normalization rules unchanged.

No worker, popup, provider, pricing, request/result, delivery, credential, permission or Autorun execution semantics are authorized.

## Mandatory regression matrix defined before execution

Historical current/legacy/generic DOM families; assistant-container variants; zero/multiple-code/non-assistant fail-closed cases; local/sibling/ambiguous Copy locality; response-Copy exclusion; native/non-command/double-click safety; initial and MutationObserver discovery; Manual OFF/ON; profile adapter compatibility; changed-line execution; full source/fresh-ZIP suites; syntax/JSON; 42-file identity; only two authorized production-file deltas; zero live Yandex requests.

## Execution results

### R1 — focused touched-dependency VM emulation — PASS

`32/32 PASS`; content and manual-controls dependency contours; provider/Yandex network 0.

### R2 — real local Chromium baseline-versus-patch DOM comparison — PASS

- consolidated + generic `<pre><code>`: no yellow decoration, 0 bridge admissions;
- patch + identical generic DOM: yellow decoration, two native clicks → exactly 1 admission, neither click prevented;
- legacy and historical writing-block: yellow + exactly 1 admission on both consolidated and patch;
- accepted browser run errors 0; Yandex network 0.

Preliminary sandbox-navigation/insecure-context harness attempts were infrastructure TEST ERROR before the accepted run.

### R3 — Chromium CDP precise changed-line coverage — PASS

```text
content_script.js changed/new lines:       31/31 EXECUTED
shared/manual_controls.js changed lines:    3/3 EXECUTED
TOTAL changed production lines:            34/34 EXECUTED
unexecuted changed production lines:        0
browser/page errors:                         0
live Yandex requests:                        0
```

Full production files were measured directly, without source extraction/wrapping. An ambiguous wrapper-offset Node coverage dump was rejected and not used as evidence.

### R4 — first complete patched source suite — FAIL (provenance invariant only)

```text
npm test
319 tests; 317 PASS; 2 FAIL; 0 skipped/cancelled
```

Only failures: old assertions that `shared/manual_controls.js` must remain byte-identical to Business Bridge reference SHA `81f302487da7b5ff7c1b746298353438b2cfec100a5bb8f7fa2c80d1e033c81e`. Actual intentionally patched SHA is `241f07a4aeb0882a424ea7e312278ed40a8a67732ca7ee05ab651a6715276bc2`. No runtime/behavior test failed. Result was recorded before test correction.

Required correction was deliberately not a new expected-hash substitution: keep exact byte identity for the other three proven shared modules and prove `manual_controls.js` differs from its old reference by only the authorized K-02 adapter delta.

### R5 — affected provenance dependency correction/rerun — PASS

```text
node --test tests/phase1_unified_core.test.mjs tests/reference_provenance.test.mjs
35/35 PASS
fail: 0
skipped: 0
cancelled: 0
```

The corrected provenance tests now enforce all of the following:

- `composer_send.js`, `conversation_identity.js`, and `proven_writing_block_capture.js` retain their exact original reference hashes;
- current `manual_controls.js` must have exact patched SHA-256 `241f07a4aeb0882a424ea7e312278ed40a8a67732ca7ee05ab651a6715276bc2`;
- `GENERIC_PRE_CODE: "generic_pre_code_v1"` occurs exactly once;
- builtin adapter count `3` occurs exactly once;
- after mechanically removing only the new adapter line and normalizing count `3 → 2`, the complete module must hash exactly to the old reference SHA-256 `81f302487da7b5ff7c1b746298353438b2cfec100a5bb8f7fa2c80d1e033c81e`.

Therefore any third/unrelated change in `manual_controls.js` fails the provenance audit instead of being hidden by an updated expected hash. No production code was changed by R5. Yandex network remains 0.

Next: rerun the complete patched source suite. If green, record it before syntax/JSON/surface checks.

## Acceptance boundary

Controlled/static PASS does not make K-02 live PASS. Final patched ZIP must still be installed in real current Chrome and visibly decorate the supported Copy. Other K gates retain their governed state.