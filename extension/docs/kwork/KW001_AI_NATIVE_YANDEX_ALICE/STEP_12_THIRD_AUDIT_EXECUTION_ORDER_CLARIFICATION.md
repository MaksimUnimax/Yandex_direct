# Step 12 — third-audit execution-order clarification

Date: 2026-08-31  
Status: **APPROVED / ACTIVE / CANONICAL COMPANION TO `STEP_12_STRUCTURAL_ACTION_METHOD.md`**

## Purpose

The third external audit added D12-21..D12-26 and the D12-27 phrase-level revalidation lesson to the permanent Step-12 method. One legacy sentence remained in Section 8 of `STEP_12_STRUCTURAL_ACTION_METHOD.md`:

```text
Stage 12 — Define hierarchy/internal links for accepted new/split pages
Only pages that survived Stage 10 receive new-page hierarchy.
```

That wording is incomplete after D12-26. It correctly describes **new-page hierarchy**, but it can be misread as limiting internal-link implementation to new/split pages. The approved third-audit rule is broader: material relationships among existing pages must also become implementation-ready link actions.

This file resolves that wording conflict without changing any other Step-12 boundary.

## Canonical precedence

Where Section 8 Stage 12 of `STEP_12_STRUCTURAL_ACTION_METHOD.md` conflicts with this clarification, this clarification controls.

```text
THIRD_AUDIT_EXECUTION_ORDER
> LEGACY SECOND_AUDIT_STAGE_12_WORDING
```

All other permanent rules, defect history, evidence requirements, pass gates and Step-13 boundaries in `STEP_12_STRUCTURAL_ACTION_METHOD.md` remain in force.

## Replacement execution meaning for Stage 12

After the structural action and evidence-derived maturity/confidence have been selected:

### A. Accepted NEW / SPLIT page actions

Materialize implementation hierarchy, including as applicable:

```text
PARENT URL / SECTION
INBOUND LINK SOURCE(S)
ANCHOR / LINK CONCEPT
OUTBOUND SUPPORT / CHILD LINKS
COMMERCIAL CONVERSION LINK WHEN INFORMATIONAL
BREADCRUMB / NAVIGATION ROLE
```

A new/split page is not implementation-ready if its place in the site graph is unknown.

### B. Material existing-page relationships

For material `ROUTE`, `SECTION`, `EXPAND` and supporting-page relationships, materialize an internal-link implementation row with:

```text
structural_unit_id
source_url
target_url
link_action_state
relation_type
placement_context
anchor_concept
user_journey_purpose
business_handoff
evidence_origin
```

When current evidence does not justify a distinct source/target link, use an explicit state such as:

```text
NOT_APPLICABLE
DEFER_SOURCE_CONTEXT_NOT_MATERIALIZED
```

Do not invent a link, source page, target page, anchor or placement merely to satisfy coverage.

### C. Fail-closed coverage

Before Step 12 can pass:

```text
MATERIAL_ROUTE_WITHOUT_LINK_ACTION_OR_EXPLICIT_NA_DEFER = 0
INTERNAL_LINK_TO_WITHDRAWN_PROPOSED_NEW_PAGE = 0
```

Internal linking is therefore part of implementing the accepted structural graph, not a new-page-only SEO task.

## Third-audit execution order

The canonical order is:

```text
1. OWNER GOAL + EVIDENCE SOURCE
2. FULL PHRASE SET / COHERENT STRUCTURAL UNIT
3. FRESH CURRENT-SITE + CONTENT-REUSE CHECK
4. GAP TYPE DIAGNOSIS
5. STRUCTURAL OWNER FIT
6. PERFORMANCE EVIDENCE STATE
7. REAL DEMAND
8. INTENDED TARGET vs OBSERVED YANDEX RELEVANT URL
9. SERP CONTENT TYPE / FORMAT / ANGLE WHEN MATERIAL
10. KEEP / EXPAND / SECTION / ROUTE / REUSE BEFORE CREATE
11. ACTION + STRUCTURAL-ONLY vs OPTIMIZATION-READY MEANING
12. EVIDENCE-DERIVED CONFIDENCE / MATURITY
13. HIERARCHY FOR NEW/SPLIT + INTERNAL-LINK IMPLEMENTATION FOR MATERIAL EXISTING-PAGE RELATIONS
14. FULL PHRASE MAP
15. DERIVED STEP-13 PAIR UNIVERSE
16. INDEPENDENT QA + OWNER CHALLENGE
17. GITHUB SAVE + STRUCTURED READBACK
18. PLAIN-LANGUAGE OWNER REPORT
```

## D12-27 falsification rule remains mandatory

If later material evidence changes or narrows the understanding of a structural unit:

```text
MATERIAL LATER EVIDENCE CONTRADICTS OR NARROWS A STRUCTURAL UNIT
→ REOPEN ALL MEMBER PHRASES
→ REVIEW EACH PHRASE AGAINST TERMINAL USER TASK / PAGE EXPECTATION
→ REASSIGN TO A VALID UNIT OR EXPLICIT NEW/DEFERRED UNIT
→ RECOMPUTE ACTIONS / PHRASE MAP / INTERNAL LINKS / PAIR GRAPH
→ INDEPENDENT EXACT-PHRASE REGRESSION
```

A previously accepted structural-unit ID is not evidence that its members remain coherent.

## Current-job regression proof

For OKNO-MSK, the accepted third-audit closure demonstrates this rule with:

```text
D12-21..D12-27 = VERIFIED_FIXED
active phrases = 2332/2332 accounted
D12-27 reviewed phrases = 65
D12-27 reassigned phrases = 20
material internal-link units = 66
internal-link rows = 66
independent findings = 0
Step13 executed = false
final GitHub readback = PASS
```

The current-job evidence proves the gate can be implemented; it does not turn OKNO-MSK-specific counts or URLs into universal thresholds.

## Markers

```text
KW001_STEP12_THIRD_AUDIT_EXECUTION_ORDER_CLARIFICATION_ACTIVE = true
KW001_STEP12_EXISTING_PAGE_INTERNAL_LINKS_REQUIRED_WHEN_MATERIAL = true
KW001_STEP12_NEW_PAGE_HIERARCHY_AND_EXISTING_PAGE_LINKING_ARE_DISTINCT = true
KW001_STEP12_NO_INVENTED_INTERNAL_LINKS = true
KW001_STEP12_D12_27_FULL_MEMBER_REOPEN_ON_MATERIAL_CONTRADICTION = true
```
