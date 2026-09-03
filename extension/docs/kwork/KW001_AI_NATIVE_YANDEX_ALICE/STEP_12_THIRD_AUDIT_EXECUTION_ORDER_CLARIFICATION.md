# KW-001 — Step 12 third-audit execution-order clarification

Date: 2026-08-31  
Updated: 2026-09-03  
Status: **APPROVED / ACTIVE / UNIVERSAL / OWNER-REQUIRED**

## Purpose

Clarify that when Step12 is reopened after a material methodological contradiction, the correction must be executed in a causally valid order. A verifier cannot certify outputs that were generated from stale boundaries, and a local patch cannot substitute for regeneration of the affected dependency graph.

## Failure class and root cause

A prior controlled correction exposed a risk of validating downstream rows before all upstream semantic/boundary changes had been fully materialized.

Root cause:

```text
CORRECTION DISCOVERY
AND
CORRECTED-STATE REGENERATION
AND
INDEPENDENT VERIFICATION
WERE NOT KEPT AS SEPARATE PHASES
```

This can create a false PASS where the verifier checks artifacts that are internally consistent but still depend on pre-correction state.

Concrete job counts, phrase/unit IDs, URLs and regression totals belong in Level-2 evidence.

## Mandatory correction order

When a Step12 third/reopen audit is required:

```text
1. FREEZE CURRENT AUTHORITATIVE INPUTS
2. REGISTER KNOWN DEFECT CLASSES + ROOT CAUSES
3. RUN INDEPENDENT GLOBAL COHERENCE DISCOVERY
4. MATERIALIZE ALL REQUIRED PHRASE/UNIT BOUNDARY CHANGES
5. RECONCILE COMPLETE CURRENT INPUT ACCOUNTING
6. REBUILD AFFECTED PAGE-ROLE / STRUCTURAL ACTION OUTPUTS
7. RE-RUN CURRENT-PAGE CONTENT VALIDATION FOR CONTENT-CHANGING ACTIONS
8. REBUILD AFFECTED INTERNAL-LINK ACTIONS
9. RE-RUN SOURCE-CONTEXT + TARGET-FIT LINK VALIDATION
10. PROPAGATE CHANGES TO ALL AFFECTED DOWNSTREAM ARTIFACTS
11. RUN INDEPENDENT SEMANTIC / EVIDENCE QA ON THE REBUILT STATE
12. RUN REGRESSION / ACCOUNTING QA
13. PERSIST DIAGNOSTICS + OUTPUTS
14. GITHUB READBACK
15. ONLY THEN RESTORE STEP PASS
```

Do not verify an artifact and then later mutate an upstream boundary that determines the artifact.

## Independence rule

The final verifier must receive the rebuilt current evidence state, not an old action as proof of its own correctness.

```text
REBUILT RAW/CURRENT EVIDENCE
-> RECOMPUTED EXPECTED DECISION
-> COMPARE WITH FINAL GENERATED DECISION
```

A verifier that merely checks final schema or that all fields agree is insufficient.

## Global-coherence interaction

`STEP_12_GLOBAL_COHERENCE_REVALIDATION_GATE.md` applies before final rebuild/acceptance when the correction is capable of exposing previously unknown task-boundary conflicts.

The current-job regression proof must be stored in Level-2 artifacts and should demonstrate equivalent properties:

```text
CURRENT_JOB_EXPECTED_ACTIVE_TOTAL reconciles exactly;
all affected units/rows are explicitly enumerated;
known defect classes are corrected;
new conflict classes from independent review are resolved or fail-closed;
affected downstream artifacts are regenerated;
unexpected changes are zero or explicitly reviewed.
```

Do not copy the current job's exact totals into this permanent rule.

## Downstream invalidation rule

When upstream Step12 membership/action changes materially, every downstream artifact whose input dependency intersects the changed set is no longer automatically valid.

```text
CHANGED INPUT
-> CALCULATE IMPACT SET
-> INVALIDATE / REBUILD AFFECTED DOWNSTREAM OUTPUTS
-> DO NOT REUSE OLD PASS BLINDLY
```

Unchanged downstream artifacts may be retained only when the impact trace proves they are outside the changed dependency set.

## Pass gate

```text
KNOWN DEFECT ROOT CAUSES ADDRESSED = true
GLOBAL COHERENCE DISCOVERY COMPLETE = true when applicable
ALL REQUIRED BOUNDARY CHANGES MATERIALIZED = true
CURRENT JOB ACCOUNTING RECONCILES = true
AFFECTED STRUCTURAL ACTIONS REBUILT = true
AFFECTED CONTENT EVIDENCE REVALIDATED = true
AFFECTED LINK ACTIONS REBUILT = true
AFFECTED DOWNSTREAM OUTPUTS REBUILT OR PROVEN UNAFFECTED = true
INDEPENDENT QA = PASS
REGRESSION QA = PASS
UNEXPECTED CHANGES = 0 or explicitly accepted
GITHUB READBACK = PASS
```

## Permanent lesson

```text
PATCHED ROWS != CORRECTED SYSTEM
VERIFIER BEFORE REBUILD != INDEPENDENT FINAL QA
OLD DOWNSTREAM PASS != VALID AFTER UPSTREAM MUTATION
```

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.

## Markers

```text
KW001_STEP12_THIRD_AUDIT_ORDER_ACTIVE = true
KW001_STEP12_DISCOVERY_BEFORE_REBUILD = true
KW001_STEP12_REBUILD_BEFORE_FINAL_VERIFICATION = true
KW001_STEP12_CURRENT_TOTALS_PARAMETERIZED = true
KW001_STEP12_DOWNSTREAM_INVALIDATION_REQUIRED = true
KW001_STEP12_CURRENT_JOB_REGRESSION_PROOF_STAYS_LEVEL2 = true
```
