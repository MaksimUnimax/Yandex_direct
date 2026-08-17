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

- historical current writing-block and legacy `#code-block-viewer` remain working;
- generic assistant `<pre><code>` works with both assistant container families;
- zero/multiple-code and non-assistant roots fail closed;
- inside-block and sibling-toolbar Copy locality work; ambiguous Copy fails closed;
- generic assistant response Copy excluded; non-command remains native-only; native Copy never prevented; duplicate click fence retained;
- initial reverse scan, dynamic pre/code, late Copy and wrapper MutationObserver discovery work;
- Manual OFF restores and ON rescans; conversation mismatch remains fail closed;
- `generic_pre_code_v1` profile accepted; old IDs preserved; unknown IDs rejected; profile limits unchanged;
- every changed production line must execute or be exact-source asserted;
- full source and fresh-ZIP suites; syntax/JSON; 42-file package; byte identity; only two authorized production files differ; zero live Yandex requests.

## Execution results

### R1 — focused touched-dependency VM emulation — PASS

```text
node --test tests/content_runtime_exhaustive.test.mjs tests/shared_every_function.test.mjs
32/32 PASS; fail 0; skipped 0; cancelled 0
```

Covers generic/current/legacy binding, locality, ambiguity, response-Copy exclusion, native/non-command/double-click behavior, initial + MutationObserver discovery, Manual ON/OFF and adapter-profile dependency. `WS_EXECUTE_COMMAND` is mocked; Yandex network 0.

### R2 — real local Chromium baseline-versus-patch DOM comparison — PASS

| Tree | DOM | Decoration | 2 native clicks | Bridge admissions | prevented? |
|---|---|---|---:|---:|---|
| consolidated | generic `<pre><code>` | no | 2 | 0 | no |
| patched | generic `<pre><code>` | yellow | 2 | 1 | no |
| consolidated | legacy | yellow | 2 | 1 | no |
| patched | legacy | yellow | 2 | 1 | no |
| consolidated | historical writing-block | yellow | 2 | 1 | no |
| patched | historical writing-block | yellow | 2 | 1 | no |

Accepted Chromium run had page/runtime errors 0. Sandbox navigation and insecure-context preliminary harness attempts were infrastructure TEST ERROR before accepted production execution. Yandex network 0.

### R3 — Chromium CDP precise changed-line coverage — PASS

```text
content_script.js changed/new lines:       31/31 EXECUTED
shared/manual_controls.js changed lines:    3/3 EXECUTED
TOTAL changed production lines:            34/34 EXECUTED
unexecuted changed production lines:        0
browser/page errors:                         0
live Yandex requests:                        0
```

Full production files were measured without source extraction/wrapping while exercising initial generic/legacy/writing roots, non-assistant/ambiguous roots, dynamic pre/code, wrapper insertion, late button, Manual OFF/ON rescan and new profile normalization. An earlier wrapper-offset Node coverage dump was rejected as attribution evidence; R3 uses direct full-source CDP offsets.

### R4 — complete patched source suite — FAIL (provenance invariant only)

```text
npm test
319 tests
317 PASS
2 FAIL
0 skipped
0 cancelled
```

Both failures are the same intentionally affected dependency assertion:

- test 162 `four proven shared modules remain byte-identical to the audited reference hashes`;
- test 242 `manual-controls module is byte-identical to supplied Business Bridge 2 v2.0.0.22 reference`.

Expected old `shared/manual_controls.js` SHA-256:
`81f302487da7b5ff7c1b746298353438b2cfec100a5bb8f7fa2c80d1e033c81e`

Actual intentionally patched SHA-256:
`241f07a4aeb0882a424ea7e312278ed40a8a67732ca7ee05ab651a6715276bc2`

No runtime/behavior test failed. This is a real regression-suite FAIL because the old provenance contract says four common modules must remain byte-identical, while the owner-authorized K-02 dependency closure deliberately changes `manual_controls.js`. It must not be silenced by merely replacing the expected hash. Required test correction: retain exact reference byte-identity for the other three common modules and replace the obsolete `manual_controls.js` byte-identity assertion with an audited-delta assertion proving the only semantic source delta is addition of `GENERIC_PRE_CODE: "generic_pre_code_v1"` and builtin adapter count `2 → 3`; locality/normalization code must remain byte-equivalent after normalizing those two authorized lines.

This R4 FAIL is recorded before altering the provenance tests. No additional production-code scope is created. Live Yandex requests remain 0.

Next: update only the affected provenance test expectations/audit logic, rerun those tests, record result, then rerun complete source suite.

## Acceptance boundary

Controlled/static PASS does not make K-02 live PASS. Final patched ZIP must still be installed in real current Chrome and visibly decorate the supported Copy. Other K gates retain their governed state.