# Phase 1 0.1.1 — K-02 generic ChatGPT code-block DOM patch plan

Date: 2026-08-17
Status: PATCH IN CONTROLLED VERIFICATION — LIVE K-02 STILL PENDING.
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
- **R2 PASS:** Chromium baseline reproduces generic DOM defect (no decoration/0 admission); patch on identical DOM is yellow and 2 native clicks → exactly 1 admission, neither prevented; legacy/current-writing contours remain green; accepted browser errors 0. Preliminary harness navigation/secure-context attempts were infrastructure TEST ERROR.
- **R3 PASS:** Chromium CDP precise coverage executes `content_script.js` changed lines 31/31 and `shared/manual_controls.js` 3/3 = **34/34**, uncovered 0; network 0.
- **R4 FAIL:** first full source run 317/319; only two obsolete byte-identity provenance assertions for intentionally changed `manual_controls.js`; no runtime/behavior failure. Old SHA `81f302487da7b5ff7c1b746298353438b2cfec100a5bb8f7fa2c80d1e033c81e`; patched SHA `241f07a4aeb0882a424ea7e312278ed40a8a67732ca7ee05ab651a6715276bc2`.
- **R5 PASS:** provenance dependency rerun 35/35. Three untouched common modules retain exact reference hashes; patched manual-controls exact hash required; removing only new adapter line and count 3→2 must reproduce old reference hash, so any unrelated third change fails audit.
- **R6 PASS:** complete patched source suite **319/319**, fail/skipped/cancelled 0.
- **R7 PASS — production surface/syntax audit:**

```text
JS/MJS syntax:                    37/37 PASS
manifest/package JSON:              2/2 PASS
base file paths:                     42
patched file paths:                  42
same path set:                     PASS
changed files total:                  6
changed production files:             2
live Yandex requests:                  0
```

Exact production delta is only:

- `content_script.js`: base SHA `148c8205bc360ba0e08a07945c3f283c5ca83eab81332c92ab8606e16d6b4f01` → patch SHA `a5677a45fd1e94fa82ef6fa3e368d23a27767c834fcc67fb53e138517878b57f`;
- `shared/manual_controls.js`: base SHA `81f302487da7b5ff7c1b746298353438b2cfec100a5bb8f7fa2c80d1e033c81e` → patch SHA `241f07a4aeb0882a424ea7e312278ed40a8a67732ca7ee05ab651a6715276bc2`.

Four changed test files are the generic-DOM regression, shared-function adapter regression, core provenance audit and provenance-specific audit. `manifest.json`, `service_worker.js`, `popup.js`, `shared/wordstat_protocol.js` are byte-identical to the consolidated base. Extension permissions remain `storage`, `tabs`, `unlimitedStorage`; host permissions remain ChatGPT/chat.openai.com plus fixed Yandex Search API host. No permission/host expansion.

Next: deterministic ZIP → fresh extraction → full 319-test rerun → 42/42 byte identity → fresh syntax/JSON → Chromium pack check. Result must be recorded before final GitHub artifact/evidence checkpoint.

## Acceptance boundary

Controlled/static PASS does not make K-02 live PASS. The final patched ZIP must still be installed in real current Chrome and visibly decorate the supported Copy. Other K gates retain their governed state.