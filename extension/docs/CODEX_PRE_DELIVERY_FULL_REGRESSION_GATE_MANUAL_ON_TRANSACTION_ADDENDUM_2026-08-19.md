# Mandatory gate addendum — Manual ON cross-layer transaction regression

Status: **MANDATORY / IMMEDIATE / PART OF THE PRE-DELIVERY FULL REGRESSION GATE**  
Date: 2026-08-19  
Applies in the current conversation and every future/resumed conversation until merged into the parent living gate.

This addendum is mandatory together with `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md`. A Codex campaign that does not execute the assertions below cannot return PASS.

## 1. Owner-live incident that exposed the missing regression

The exact previously full-gate-passed artifact:

```text
yandex-marketing-bridge-0.1.1-phase1-external-ui-manual-delivery-candidate.zip
SHA-256 31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
```

failed in the owner's real Chrome before any Yandex command could be executed.

Observed diagnostic sequence on the same confirmed conversation/tab:

```text
MANUAL_BLOCK_DECORATED external_action:true separate_action:true
MANUAL_SURFACE_SCAN reason:manual_on manual_enabled:true decorated_button_count:1
MANUAL_MODE_APPLIED manual_enabled:true decorated_button_count:1
MANUAL_SURFACE_SCAN reason:manual_off manual_enabled:false decorated_button_count:0
MANUAL_MODE_APPLIED manual_enabled:false decorated_button_count:0
```

The ON→OFF collapse repeated. The visible result was that the expected external `Яндекс` action was absent by the time the owner tried to use it.

Classification: **PRODUCT FAIL + TEST-DESIGN FAIL**. The earlier Codex PASS was valid only for the assertions that were actually implemented; it did not prove the missing cross-layer transaction invariant below.

## 2. Exact root cause

The regression was introduced by combining two individually tested behaviors whose ordering contract was not revalidated as one transaction:

1. existing `popup.js` Manual-ON flow sent `WS_APPLY_MANUAL_MODE(enabled:true)` to content first and committed worker state through `WS_SET_MANUAL_MODE(enabled:true)` only afterward;
2. the later `content_script.js` patch changed the `WS_APPLY_MANUAL_MODE(enabled:true)` handler so it immediately calls `syncManualState()` and reads authoritative worker Manual state before returning.

Therefore, during the popup ON transition, content temporarily enabled Manual, immediately queried a worker that was still OFF, applied OFF to itself, removed the Bridge-owned Yandex action, and then returned an acknowledgement that did not truthfully represent the final content state. The popup subsequently committed worker ON, but did not perform another successful content ON synchronization.

## 3. Why the previous automated/Codex gate missed it

This is a permanent QA-engineering lesson.

### A. Popup test double was too weak

The popup harness mocked `WS_APPLY_MANUAL_MODE` by directly assigning a synthetic `contentManualMode = enabled` and returning `applied:true`. It did not execute or faithfully model the real content handler's worker re-sync. Thus the popup test could not expose the ordering race.

### B. Content test asserted the acknowledgement, not final state

The content runtime test invoked `WS_APPLY_MANUAL_MODE(enabled:true)` while its default mocked `WS_GET_MANUAL_STATE` returned `enabled:false`, but asserted only that the response said `applied:true`. It did not assert that Manual remained enabled or that a Yandex action remained present after the internal `syncManualState()` completed. The test therefore exercised the buggy sequence without failing on it.

### C. External-button lifecycle test bypassed the real transaction

The external-Yandex lifecycle regression directly called internal `applyManualMode(true)` / test-ready helpers. It proved the action survived native Copy lifecycle after being armed, but it did not prove that the actual popup→worker→content transaction could arm and keep it armed.

### D. PD-05 and PD-06 were tested as adjacent surfaces, not as one cross-layer transaction

Popup behavior and Manual DOM/action behavior both had coverage, but the installed-extension transition from initial worker OFF + content OFF through a real popup Manual-ON action was not a mandatory end-to-end assertion. This gap is what allowed a full gate PASS despite the owner-visible failure.

## 4. Permanent product invariant

For Manual ON:

1. the worker authoritative Manual gate must be committed ON before content is asked to acknowledge/activate ON;
2. the content ON handler must re-read authoritative worker state and may report `applied:true` only if final authoritative state is ON and the addressed content runtime remains ON;
3. if content ON cannot be confirmed after worker commit, popup must roll worker state back to OFF and best-effort disarm content; it must not display successful ON;
4. no transient local ON followed by worker-derived OFF may be reported as successful ON;
5. after successful popup ON, a follow-up worker state read, content state sync, popup reopen and ordinary DOM mutation must leave the external Yandex action armed while Manual remains ON.

For Manual OFF, the existing safety ordering remains: worker OFF first, then content disarm; failure to disarm content cannot reopen the worker gate.

## 5. Mandatory executable regression coverage

### PD-01 / deterministic source suite

The complete source and packaged suites must include assertions equivalent to all of the following:

- worker initially OFF + content initially OFF + `WS_APPLY_MANUAL_MODE(enabled:true)` without worker commit → content must return `applied:false`, remain OFF and expose no armed Yandex action;
- worker ON first + content apply ON → content returns `applied:true`, remains ON and has an armed Yandex action;
- popup Manual ON call ordering is `WS_SET_MANUAL_MODE(true)` **before** `WS_APPLY_MANUAL_MODE(true)`;
- content-apply failure after worker ON causes worker rollback OFF and no successful ON UI state;
- the regression test must fail against the exact old `31cc5f…` production bytes and pass against the repaired bytes.

### PD-04 / PD-05 / PD-06 — qualified CfT + Puppeteer installed-extension scenario

This cross-layer scenario is browser-mandatory and may not be replaced by independent popup and independent DOM tests:

1. install the exact package/source under test in the qualified QA profile;
2. start with the bound controlled ChatGPT conversation at worker Manual OFF and content Manual OFF;
3. render at least one eligible current factual PRE/readonly-CodeMirror block;
4. use the **real extension popup control** to turn Manual ON once — do not call internal `applyManualMode`, do not preseed content ON, and do not bypass popup messaging;
5. require worker authoritative state ON after the transition;
6. require content to remain ON after its worker re-sync completes;
7. require exactly one Bridge-owned external `Яндекс` action to remain connected and ready on the eligible block;
8. wait through at least one ordinary content resync/mutation interval and re-check that it did not self-revert to OFF;
9. close/reopen the popup and require it still reflects worker ON while the Yandex action remains present;
10. turn Manual OFF through the real popup and require worker OFF plus Bridge action removal;
11. repeat ON once more and require the action to remain armed again;
12. execute zero real Yandex requests in this scenario.

Any ON→OFF self-reversion, `applied:true` while final content is OFF, worker/content disagreement, or missing Yandex action after successful popup ON is `FAIL_PRODUCT`.

## 6. Handoff rule

The owner is not to retest this repair before Codex. Product bytes changed, so the previous `31cc5f…` full-gate PASS no longer authorizes handoff. A new exact candidate must pass the complete living `PD-00…PD-17` campaign **plus this addendum** before owner real-profile acceptance resumes.
