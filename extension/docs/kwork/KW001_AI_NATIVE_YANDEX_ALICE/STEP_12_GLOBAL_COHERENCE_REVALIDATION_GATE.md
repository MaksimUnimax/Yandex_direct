# KW-001 — Step 12 global coherence revalidation gate

Date: 2026-08-31  
Updated: 2026-09-05  
Status: **APPROVED / ACTIVE / UNIVERSAL / OWNER-REQUIRED**

## Purpose

A local correction to one structural unit or phrase family can expose a broader failure in the underlying semantic partition. Step12 must therefore revalidate global coherence after material boundary corrections instead of assuming that fixing the originally reported row/class is sufficient.

## Failure class

A prior correction successfully repaired several locally identified assignments/actions, but phrase-level review showed that adjacent structural units still mixed materially different terminal user tasks.

Generic conflict examples include:

```text
A service/bundle unit that also contains a standalone product task;
a broad technical-information unit that also contains a repair/replacement task;
a commercial unit that contains a DIY/how-to subtask;
an accessory/product unit that contains a professional service task;
a broad object unit that hides a more specific object/lifecycle boundary.
```

### Root cause

```text
KNOWN FAILURE SET
WAS TREATED AS
COMPLETE FAILURE UNIVERSE
```

and:

```text
LOCAL PATCH SUCCESS
WAS TREATED AS
GLOBAL SEMANTIC COHERENCE PROOF
```

The correct control is an independent global phrase-level coherence pass after material structural corrections.

Concrete domains, phrase families, unit IDs, counts and correction batches remain Level-2 evidence.

## Mandatory global review

After any Step12 correction that changes structural-unit membership, boundaries, owner roles, content actions or route states materially, review the complete affected semantic universe with enough independence to detect **new conflict classes**, not only regress the known edits.

For every active phrase/unit derive or re-check as applicable:

```text
PRIMARY_OBJECT
OBJECT_SCOPE
USER_ACTION_OR_GOAL
EXPECTED_TERMINAL_RESULT
INTENT_MODE
LIFECYCLE_STAGE
EXECUTION_MODE
BUSINESS_SCOPE_STATE
CURRENT_STRUCTURAL_UNIT
CURRENT_PAGE_ROLE / OWNER STATE
```

Then test whether every structural unit is coherent under its accepted contract.

## Mandatory contradiction patterns

Flag a unit when phrases inside it materially disagree on one or more of:

```text
terminal result;
whole object vs component;
product vs hired service;
hired service vs DIY/how-to;
buy vs repair vs replace vs maintain;
commercial transaction vs neutral information;
current business scope;
page-role compatibility;
current owner truth.
```

A modifier difference alone does not require a split unless the current domain/profile/evidence makes it material.

## Correction procedure

For each newly discovered coherence defect:

```text
1. record the defect class;
2. identify all affected phrases/units, not only the trigger phrase;
3. define the corrected task/structural boundary;
4. reassign/mutate units according to current accepted method;
5. recompute affected owner/action/link evidence;
6. revalidate current page/content evidence where a material action changes;
7. preserve old-to-new provenance;
8. rerun global accounting;
9. rerun global coherence review until no material new conflict class is discovered.
```

Do not stop merely because the originally reported examples now pass.

## Correction atomicity gate

For each changed canonical phrase/unit identity, load the target unit contract and rebuild every field governed by that contract before downstream propagation.

```text
NEW UNIT ID + OLD UNIT-DERIVED TASK / INTENT / SCOPE / PAGE ROLE / OWNER / MATURITY
=> FAIL
```

QA must compare the corrected row to the canonical target contract, not only to the correction overlay or old row. Independently sourced fields may remain only when their lineage proves they do not depend on the changed unit.

If any declared downstream materializer consumes a base assignment plus selected overlays, its precedence/join logic must be tested against the complete correction universe.
## Accounting gate

The current job must instantiate its own expected totals. Do not hard-code rehearsal numbers into this permanent method.

Required pattern:

```text
GLOBAL_ACCOUNTING_AFTER_REASSIGNMENT
= CURRENT_JOB_ACTUAL_ACCOUNTED_TOTAL / CURRENT_JOB_EXPECTED_ACTIVE_TOTAL
```

Pass requires equality and zero silent drops.

Where exact occurrence and unique-phrase universes both matter, reconcile both separately.

## Impact propagation

If phrase/unit membership changes, downstream artifacts that depend on the changed boundary must be invalidated or regenerated as applicable:

```text
page ownership
structural action
content-gap state
internal-link recommendation
competing-page diagnosis inputs
architecture freeze
later AI-case selection
priority records
```

The exact downstream set is determined by the current roadmap and dependency trace.

## Independent QA

A valid global-coherence verifier must be capable of discovering an error not present in the original defect list.

```text
VERIFIER ONLY CHECKS KNOWN CORRECTIONS
!= GLOBAL COHERENCE QA
```

Preferred outputs include:

```text
units reviewed
phrases/rows reviewed
new conflict classes found
new affected rows
reassignments
splits/merges if authorized
unresolved boundary rows
accounting result
unexpected changes
```

## Pass gate

```text
CURRENT_JOB_ACTIVE_TOTAL_ACCOUNTED = true
SILENT_DROPS = 0
UNEXPECTED_DUPLICATION = 0
ALL MATERIAL CHANGED UNITS REVALIDATED = true
CORRECTED_ROWS_MATCH_CANONICAL_TARGET_CONTRACT = true
IDENTIFIER_ONLY_CORRECTIONS = 0
GLOBAL COHERENCE REVIEW COMPLETE = true
NEW MATERIAL CONFLICT CLASS IN FINAL PASS = 0
AFFECTED DOWNSTREAM OUTPUTS REBUILT = true
COMPLETE_CORRECTION_UNIVERSE_RECONCILED_THROUGH_DECLARED_CONSUMERS = true
CURRENT PAGE/EVIDENCE GATES RE-RUN WHERE ACTION CHANGED = true
FINAL INDEPENDENT QA = PASS
GITHUB READBACK = PASS
```

A pass with unresolved newly discovered boundary conflicts is forbidden.

## Permanent lesson

```text
LOCAL CORRECTION != GLOBAL CORRECTNESS
KNOWN DEFECTS FIXED != FAILURE UNIVERSE EXHAUSTED
ARITHMETIC ACCOUNTING != SEMANTIC COHERENCE
CORRECTED ID != CORRECTED SEMANTIC STATE
```

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.

## Markers

```text
KW001_STEP12_GLOBAL_COHERENCE_GATE_ACTIVE = true
KW001_STEP12_LOCAL_PATCH_NOT_EQUAL_GLOBAL_PASS = true
KW001_STEP12_GLOBAL_PHRASE_OR_UNIT_REVIEW_REQUIRED_AFTER_MATERIAL_BOUNDARY_CHANGE = true
KW001_STEP12_CURRENT_JOB_TOTALS_MUST_BE_PARAMETERIZED = true
KW001_STEP12_DOWNSTREAM_IMPACT_PROPAGATION_REQUIRED = true
KW001_STEP12_CORRECTED_ROW_TARGET_CONTRACT_QA_REQUIRED = true
KW001_STEP12_IDENTIFIER_ONLY_CORRECTION_IS_FAIL = true
KW001_STEP12_COMPLETE_CORRECTION_UNIVERSE_FORWARD_AUDIT_REQUIRED = true
KW001_STEP12_GLOBAL_QA_MUST_DISCOVER_NEW_CLASSES = true
```
