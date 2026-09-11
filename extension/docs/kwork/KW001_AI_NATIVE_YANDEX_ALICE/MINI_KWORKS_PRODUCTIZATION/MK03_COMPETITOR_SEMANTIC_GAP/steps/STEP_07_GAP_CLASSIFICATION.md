# MK03 STEP 07 — CLIENT COVERAGE COMPARISON AND GAP CLASSIFICATION

## Purpose
Decide whether each material competitor-derived direction is genuinely missing, already covered, outside scope or still unresolved.

## Why this step exists
Demand and competitor visibility do not themselves establish a client gap.

## Inputs
Sanitized candidates; material Search confirmation; current client coverage baseline/current page evidence.

## Required evidence
Demand/provenance; client business fit; current-site coverage sufficient for the decision; Search evidence where exact visibility/intent is material.

## Method
For each material candidate reconcile:
- competitor source lineage;
- normalized phrase/direction;
- Wordstat demand state;
- client business/scope fit;
- tested Search state where applicable;
- current client page/topic coverage;
- uncertainty.

Route to exactly one state:

```text
CONFIRMED_GAP
ALREADY_COVERED
REJECT_OFF_SCOPE
HOLD_EVIDENCE
```

Preserve reason and evidence meaning, not only locator.

## Outputs
`COMPETITOR_GAP_DECISION_REGISTER` and complete accounting.

## Source authority
Parent Step5A 5A.7; current-site freshness authorities; local GENERAL_RULES.

## Known failures / root causes
- competitor signal accepted automatically;
- old inventory used to claim absence;
- Search absence used to claim site absence;
- already-covered rows silently dropped because they are “not gaps”.

## Non-repeat controls
All states are client-value states; `ALREADY_COVERED` remains visible where material.

## Claim boundary
`CONFIRMED_GAP` means a supported missed demand/topic opportunity under MK03 evidence, not automatic new-page architecture or implementation readiness.

## Unknown behavior
Insufficient current-site/business/Search evidence yields HOLD_EVIDENCE with the exact missing fact/check.

## PASS gate
Every material candidate accounted; silent drops = 0; gap reasons are independently reconstructable from evidence.

## Client-facing meaning
“We separate what is truly missing from what your site already covers, what does not belong to your business and what still needs evidence.”
