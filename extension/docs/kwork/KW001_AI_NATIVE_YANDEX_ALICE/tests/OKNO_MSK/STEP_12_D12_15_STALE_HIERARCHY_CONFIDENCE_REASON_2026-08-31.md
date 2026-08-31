# Step 12 — D12-15 stale confidence reason after hierarchy materialization

Date: 2026-08-31
Status: OPEN / discovered by durable independent D12-05 QA
Discovery run: GitHub Actions `33366415931`
Diagnostic persistence commit: `426f41e1b1aebb69072ad9f037cfd73cb92475f8`

## What independent QA found

Check `Q027` found **10** action rows whose `hierarchy_clarity` is already `MATERIALIZED_*`, while `confidence_downgrade_reason` still says `new-page hierarchy is not yet finalized`.

Affected structural units persisted in `STEP_12_QA_FINDINGS.tsv`:

- `PANORAMIC_WINDOWS_COMMERCIAL_CORE`
- `PVC_WINDOW_ADJUSTMENT_DIY`
- `PVC_WINDOW_INSTALLATION_DIY`
- `PVC_WINDOW_REPAIR_DIY_GENERAL`
- `WINDOW_COMPONENT_SELECTION_INFO`
- `WINDOW_HARDWARE_MAINTENANCE_INFO`
- `WINDOW_HARDWARE_SELECTION_GUIDE`
- `WINDOW_HARDWARE_STANDARD_INFO`
- `WINDOW_INSTALLATION_MATERIALS_INFO`
- `WINDOW_REPLACEMENT_SERVICE`

## Why this matters

The structural state and the explanation disagree. A client or downstream analyst reading the row could believe hierarchy still needs to be designed even though D12-07 already materialized the parent/inbound/outbound role.

The remaining uncertainty is real, but it comes from other dimensions: Search page boundary, business truth, or the deterministic Step-13 conflict dependency. The reason field must name the actual unresolved evidence rather than a condition that has already been resolved.

## Root cause

`STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv` overlays materialized hierarchy and Step-13 dependency onto V1 actions, but it carries forward the V1 `confidence_downgrade_reason` text. The hierarchy dimension was updated; its human-readable explanation was not recomputed from the updated dimensions.

## Corrective method

After hierarchy and dependency overlays, confidence explanation must be regenerated from the current evidence state:

```text
CURRENT business_truth
+ CURRENT search_boundary_support
+ CURRENT hierarchy_clarity
+ CURRENT recommendation_maturity / Step13 dependency
→ CURRENT confidence_downgrade_reason
```

Resolved evidence dimensions must not remain as downgrade reasons.

Hard invariant:

```text
HIERARCHY_CLARITY = MATERIALIZED_*
→ CONFIDENCE_REASON MUST NOT CLAIM HIERARCHY IS NOT FINALIZED
```

## Required verification

D12-15 can close only when:

- `stale_materialized_hierarchy_reason_rows = 0`;
- all 10 discovered rows are corrected by regeneration, not hand-edited one by one;
- real Search/business/Step13 uncertainty remains visible where applicable;
- confidence/maturity values do not become stronger merely because stale wording was removed;
- independent D12-05 QA passes after durable GitHub persistence/readback.

## Step boundary

This is an explanation-consistency repair. It does not resolve Search gaps or execute Step 13.
