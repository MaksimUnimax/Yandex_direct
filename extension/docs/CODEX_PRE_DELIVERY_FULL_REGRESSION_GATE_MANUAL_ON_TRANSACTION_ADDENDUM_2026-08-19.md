# Mandatory gate addendum — Manual ON cross-layer transaction regression

Status: **MANDATORY / CURRENT CONTRACT RECONCILED 2026-08-25**  
Originally adopted: 2026-08-19  
Current contract correction: 2026-08-25  
Scope: applies together with `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` to every candidate that touches Manual/runtime/content/popup lifecycle behavior.

## 1. Historical incident

This addendum was originally created after an owner-visible Manual ON regression where the visible `Яндекс` action armed and then disappeared because content synchronized against worker state during the ON transition.

That historical incident remains evidence, but its original proposed ordering (`worker ON -> content ON`) is **not** the current accepted transaction contract. Later Phase-1/Phase-2 repair established the opposite safety invariant now implemented in the accepted product.

## 2. Current accepted Manual ON invariant

The accepted contract is:

```text
content/page ON acknowledgement
-> worker Manual hard-gate ON commit
```

Reason: the worker must not authorize executable Manual requests until the addressed ChatGPT page has positively acknowledged that the correct bound conversation can arm the Bridge-owned Manual surface.

Required behavior:

1. popup resolves the current concrete ChatGPT tab/conversation;
2. popup sends `WS_APPLY_MANUAL_MODE(enabled:true)` to the addressed content runtime first;
3. content may return `applied:true` only for the addressed confirmed conversation and must leave its local Manual surface armed;
4. only after that acknowledgement does popup send `WS_SET_MANUAL_MODE(enabled:true)` to worker;
5. if worker commit fails, popup best-effort sends content `enabled:false` and reports failure; it must not leave a successful ON UI state;
6. after successful worker commit, later state synchronization must keep content Manual ON and the external `Яндекс` action present;
7. there must be no window in which the worker hard gate is ON while the addressed page has not acknowledged Manual ON.

Manual OFF remains safety-first:

```text
worker Manual hard-gate OFF commit
-> content/page cleanup acknowledgement
```

If page cleanup fails, worker stays OFF.

## 3. Mandatory deterministic regression coverage

The source and packaged suites must assert equivalent behavior:

- popup Manual ON ordering is content `WS_APPLY_MANUAL_MODE(true)` **before** worker `WS_SET_MANUAL_MODE(true)`;
- failed content ON acknowledgement never authorizes worker Manual mode;
- failed worker ON commit after successful content acknowledgement best-effort disarms content and does not report successful ON;
- successful ON followed by worker/content resynchronization keeps Manual ON and preserves exactly one Bridge-owned `Яндекс` action on each eligible uniquely bound block;
- Manual OFF ordering is worker OFF before content cleanup;
- no native Copy lifecycle is allowed to own or gate the Bridge action;
- all scenarios execute zero real Yandex requests unless a separate explicitly authorized live-provider boundary requires otherwise.

## 4. Mandatory installed-extension browser regression

For candidates affecting these layers, the qualified browser scenario must use the real extension popup and real installed content/worker code:

1. start with bound controlled ChatGPT conversation, worker Manual OFF, content Manual OFF;
2. render at least one eligible current writing/code block;
3. turn Manual ON once through the real popup control;
4. require content acknowledgement to occur before worker hard-gate authorization;
5. require final worker Manual state ON;
6. require content to remain ON after ordinary state-sync/mutation intervals;
7. require exactly one connected ready Bridge-owned `Яндекс` action on the eligible block;
8. close/reopen popup and require it still reflects worker ON while the action remains present;
9. turn Manual OFF through the real popup and require worker OFF before Bridge action removal;
10. repeat ON once and require the action to remain armed;
11. execute zero real Yandex requests in this scenario.

Any worker authorization before page acknowledgement, ON->OFF self-reversion, worker/content disagreement, missing action after successful ON, or successful UI state after a failed transaction is `FAIL_PRODUCT`.

## 5. Current lifecycle-button patch interaction

The 2026-08-25 owner functional run exposed an additional UI invariant for the next governed patch:

```text
MANUAL_OPERATION_ACTIVE or DELIVERY_IN_PROGRESS
-> existing Bridge-owned Yandex action remains present but disabled/non-clickable
-> backend admission guards remain fail-closed
-> after positively observed lifecycle completion, action becomes clickable again
```

This availability gating must not reset worker timers, delivery state, Manual mode, conversation binding, or Autorun state. Regression coverage must prove `blocked -> click impossible -> lifecycle clears -> clickable again`.

## 6. Handoff rule

Any candidate that changes production bytes in these layers requires a new exact candidate and the complete applicable governed gate before owner handoff. Historical PASS evidence on earlier product bytes cannot authorize the changed candidate.