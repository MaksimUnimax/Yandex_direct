# Step 12 — D12-14 implementable action without primary target

Date: 2026-08-31
Status: OPEN / discovered by durable independent D12-05 QA
Discovery run: GitHub Actions `33366415931`
Diagnostic persistence commit: `426f41e1b1aebb69072ad9f037cfd73cb92475f8`

## What independent QA found

Check `Q023` failed because four final structural-action rows describe an implementable on-site action but do not identify the primary page that is supposed to receive that action:

1. `PVC_DOOR_INSTALLATION_SERVICE` — `ADD_SECTION_OR_FAQ_TO_EXISTING` — blank primary target.
2. `PVC_WINDOW_OPERATION_DIY` — `ROUTE_TO_EXISTING_PAGE_AS_SUBTASK` — blank primary target.
3. `REHAU_OTHER_BRAND_COMPARISON_INFO` — `ADD_SECTION_OR_FAQ_TO_EXISTING` — blank primary target.
4. `WINDOW_DEMOLITION_SERVICE` — `ADD_SECTION_OR_FAQ_TO_EXISTING` — blank primary target.

The independent QA intentionally did not guess replacements. It persisted all four findings before failing the pass gate.

## Why this is a real structural defect

An action such as `ADD_SECTION_OR_FAQ_TO_EXISTING`, `ROUTE_TO_EXISTING_PAGE_AS_SUBTASK`, `EXPAND_EXISTING_PAGE`, `KEEP_EXISTING_STRUCTURE`, or `NEW_*_PAGE` is an implementation instruction. Without a primary destination, the client still cannot answer **where** the change is supposed to happen.

A supporting page is not automatically the primary owner, and the closest lexical URL is not evidence. Therefore a blank target cannot be repaired by filling the nearest-looking URL.

## Root cause

The Step-12 action derivation can infer an action from unit role and historical action mix even when the structural-unit row has no `primary_page_candidate`. There was no final action-readiness invariant requiring the destination to be resolved before an implementable action was emitted.

## Corrective method

Each affected unit must be re-evaluated independently:

```text
EXACT MEMBER PHRASES / TERMINAL TASK
→ CURRENT VERIFIED PAGE INVENTORY + STEP-11 OWNERSHIP/PAGE EVIDENCE
→ DOES A TRUTHFUL PRIMARY PAGE EXIST?
   → YES: record that exact primary target and keep supporting pages separate
   → NO: change the structural action to an explicit defer/no-standalone state with the named evidence gap
→ RECOMPUTE MATURITY / CONFIDENCE IF ACTION CHANGED
```

Hard invariant:

```text
IMPLEMENTABLE_PAGE_ACTION
→ NON_EMPTY_VERIFIED_PRIMARY_TARGET
```

Never:

```text
IMPLEMENTABLE_PAGE_ACTION
→ BLANK_TARGET
```

and never:

```text
BLANK_TARGET
→ AUTO_COPY_SUPPORTING_PAGE_WITHOUT_PAGE-FIT_REVIEW
```

## Required verification

D12-14 can close only when:

- `actions_requiring_target_but_blank = 0` under the independent QA definition;
- all four discovered rows have an explicit reviewed resolution;
- any chosen existing target is supported by current site/Page Ownership evidence;
- any row with no suitable target is explicitly deferred/reclassified rather than force-routed;
- final phrase-action map is rebuilt;
- independent D12-05 QA passes the target gate after GitHub persistence/readback.

## Step boundary

This correction does not start Step 13 and does not diagnose cannibalization.
