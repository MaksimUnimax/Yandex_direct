# Phase 1 0.1.1 — K-02 generic ChatGPT code-block DOM patch plan

Date: 2026-08-17
Status: PATCH IN CONTROLLED VERIFICATION — LIVE K-02 STILL PENDING.
Authority: owner explicitly interrupted the K campaign and ordered an immediate patch after the governed K-02/C-01 real-current-Chrome FAIL recorded in `PHASE_1_0.1.1_LIVE_TEST_PLAN_AND_RESULTS.md` section 8.4.

## Root cause already established before patch

The consolidated Yandex candidate inherited the Wordstat 1.1.5 DOM adapter. It accepts the special writing-block families and legacy `<pre>` only when `#code-block-viewer` exists. A current ordinary assistant `<pre><code>...</code></pre>` therefore has no binding and is omitted from initial/manual MutationObserver discovery. Ozon Bridge v0.1.11 independently records and corrects the same live failure class: Manual READY while the visible local Copy remains native/gray because generic assistant `<pre><code>` is not a supported root.

## Authorized implementation scope

Production changes are limited to the dependency closure required by this K-02 FAIL:

1. `content_script.js`
   - resolve assistant containers from both the historical `section[data-turn="assistant"][data-turn-id]` family and current `[data-message-author-role="assistant"]` family;
   - add a fail-closed generic assistant `<pre><code>` binding only when one unambiguous `code` body exists;
   - preserve legacy `#code-block-viewer` precedence;
   - include generic pre/code roots in initial reverse scan and MutationObserver candidate discovery;
   - make late-added sibling Copy controls re-resolve through the existing locality algorithm;
   - preserve native Copy, generic assistant Copy exclusion, Manual conversation scoping, duplicate fences, and zero provider execution before an actual local Copy click.
2. `shared/manual_controls.js`
   - register the generic adapter id so custom Copy profile normalization/picker fallback remains compatible with the new binding family;
   - do not change locality ranking or any run/policy/provider behavior.

No worker, popup, provider, pricing, request, result, delivery, credential, permission, or Autorun execution semantics are authorized by this patch.

## Mandatory pre/post regression matrix

### DOM families

- historical current writing-block family remains decorated and executes one Manual admission;
- legacy `<pre>#code-block-viewer</pre>` remains decorated and executes one Manual admission;
- current generic assistant `<pre><code>WORDSTAT_API_V1...</code></pre>` becomes decorated and executes one Manual admission;
- generic assistant container may be `[data-message-author-role="assistant"]` without requiring `section[data-turn]`;
- generic pre with zero `code` children is rejected;
- generic pre with multiple `code` descendants is rejected as ambiguous;
- non-assistant `<pre><code>` is rejected.

### Copy locality / safety

- local Copy inside the block works;
- local Copy in a sibling toolbar resolves to the correct single block;
- two equally local Copy candidates remain fail-closed/no decoration;
- generic assistant-level `copy-turn-action-button` remains excluded;
- non-command code block may keep native Copy but must not submit a Yandex command;
- native Copy event is never prevented;
- rapid duplicate clicks preserve the existing in-flight/dedup contour.

### Discovery lifecycle

- initial reverse scan finds generic pre/code roots;
- MutationObserver discovers a newly added generic block;
- MutationObserver discovers a Copy button added after the generic block and re-evaluates locality;
- Manual OFF removes decoration and click handler;
- Manual ON re-scan decorates existing supported blocks;
- conversation mismatch/resync behavior remains fail-closed.

### Adapter profile dependency

- `generic_pre_code_v1` is accepted by copy-profile normalization;
- profile signature matches only the same adapter family;
- existing legacy/current profile IDs remain accepted unchanged;
- unknown adapter IDs remain rejected;
- existing profile count/dedup limits remain unchanged.

### Whole-system regression / packaging

- execute every changed/new production function branch reachable in the controlled DOM harness;
- map every added production line to runtime execution or exact-source assertion;
- full existing source suite must remain green;
- repeat full suite against a fresh extraction of the final ZIP;
- all production JS/MJS syntax checks pass;
- manifest/package JSON parse pass;
- production file count remains 42;
- source ↔ fresh ZIP is byte-identical for all 42 files;
- only the two authorized production files may differ from the consolidated base candidate;
- no live Yandex request is permitted during patch/emulation.

## Execution results

### R1 — focused touched-dependency / VM DOM emulation — PASS

```text
node --test tests/content_runtime_exhaustive.test.mjs tests/shared_every_function.test.mjs
32/32 PASS
fail: 0
skipped: 0
cancelled: 0
```

The focused run executes the actual patched production source used by those harnesses and covers the direct dependency closure introduced by this patch: generic assistant `<pre><code>` binding, historical writing-block binding, legacy `#code-block-viewer` precedence, sibling-toolbar locality, ambiguity fail-closed behavior, generic assistant-level Copy exclusion, native Copy preservation, non-command behavior, rapid duplicate admission fence, initial/manual root discovery, MutationObserver discovery including a late-added Copy button, Manual ON decoration/OFF restoration, and the `generic_pre_code_v1` adapter-profile dependency in `shared/manual_controls.js` while retaining existing adapter IDs and limits.

No live Yandex request was issued. `WS_EXECUTE_COMMAND` in this focused run is a mocked content→worker boundary inside the controlled VM harness; provider/network execution is absent.

### R2 — real local Chromium baseline-versus-patch DOM comparison — PASS

The exact consolidated candidate production scripts and the patched production scripts were executed in Chromium against the same controlled DOM families. Network/provider execution was mocked out completely.

| Production tree | DOM family | Copy decoration | Two immediate native clicks | `WS_EXECUTE_COMMAND` admissions | Native click prevented? |
|---|---|---|---:|---:|---|
| consolidated baseline | generic assistant `<pre><code>` | ordinary / no yellow style | 2 | 0 | no |
| patched | generic assistant `<pre><code>` | yellow Wordstat style | 2 | exactly 1 | no |
| consolidated baseline | legacy `#code-block-viewer` | yellow | 2 | exactly 1 | no |
| patched | legacy `#code-block-viewer` | yellow | 2 | exactly 1 | no |
| consolidated baseline | historical writing-block | yellow | 2 | exactly 1 | no |
| patched | historical writing-block | yellow | 2 | exactly 1 | no |

This directly reproduces the field defect on unchanged consolidated bytes and proves the patch changes the missing generic DOM contour without regressing the two previously supported contours. Harness navigation/secure-context preliminary failures are classified as infrastructure TEST ERROR; the accepted run had no page/runtime error and supplied only confirmed conversation identity plus `crypto.randomUUID`, capabilities available on production `https://chatgpt.com`.

No live Yandex request was issued.

### R3 — Chromium CDP precise changed-line coverage — PASS

The complete patched production files were injected without source extraction/wrapping and measured with Chromium `Profiler.startPreciseCoverage`. The controlled page exercised the initial generic/legacy/writing families plus non-assistant and ambiguous code roots, direct dynamic `<pre>`, dynamic `<code>`, wrapper insertion containing descendant `pre`/button, late sibling-button insertion, Manual OFF/ON restoration/rescan, native click behavior and new copy-profile normalization.

```text
content_script.js changed/new lines:       31/31 EXECUTED
shared/manual_controls.js changed lines:    3/3 EXECUTED
TOTAL changed production lines:            34/34 EXECUTED
unexecuted changed production lines:        0
browser/page errors:                         0
live Yandex requests:                        0
```

This is execution evidence, not merely a textual assertion: every new or replacement production line identified by an exact consolidated-base → patched-tree diff had a positive precise-coverage count. Representative counts include `assistantContainerFromNode` 58 executions, `genericCodeBodyFromPre` 39 executions, generic/legacy binding lines up to 48 executions, MutationObserver candidate additions 5 executions, reverse-scan generic pre/code branches 53/42 executions, and all three `manual_controls.js` adapter/count changes executed at module initialization.

The earlier Node coverage dump that did not attribute some content-script lines was rejected as evidence because one VM harness used shifted wrapper offsets. R3 deliberately replaces that ambiguous attribution with full-source Chromium CDP offsets.

No live Yandex request was issued.

Next governed verification step: complete source regression suite on the patched tree, then syntax/JSON and production-surface diff checks.

## Acceptance boundary

Passing this amendment closes only the controlled/static implementation side of the current K-02 DOM defect. K-02 remains live-pending until the final patched ZIP is installed in real current Chrome and the visible supported Copy is confirmed decorated there. K-01/K-03/K-04/K-05/K-06/K-08 retain their governed status.