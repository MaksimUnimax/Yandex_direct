# MK02 — OWNER PRODUCT-GAP CORRECTION — 2026-09-10

Status: **SUBSTANTIVE METHOD DEFECT CONFIRMED / PHASE 7 REOPENED FOR CORRECTIVE REWORK**

## 1. Defect

The accepted Phase-7 package was internally consistent and physically clean, but it under-delivered the core sold value of MK02.

The rehearsal was biased by the fact that OKNO_MSK already has a mature current site with many existing pages already aligned to the semantic demand. The method began ownership analysis from current pages and later turned only current→target differences into implementation work. As a result, the client PDFs visibly emphasized a small change delta instead of the full work the product sells.

Observed product-level failure:

```text
SOLD PRODUCT
= semantic core + phrase/page mapping + target SEO structure + page-level TZ

VISIBLE PHASE-7 PACKAGE
= semantic statistics + current-site audit conclusions + small physical-change delta
```

A technically good current site is a valid analytical result, but it must not make the sold landing-page mapping and target architecture disappear from the client deliverable.

## 2. Root cause

The method conflated four different objects:

```text
A. TARGET LANDING RESPONSIBILITY DERIVED FROM DEMAND
B. CURRENT PUBLIC PAGE / CURRENT OWNER
C. TARGET PAGE SPECIFICATION
D. PHYSICAL CURRENT→TARGET CHANGE TICKET
```

The earlier execution path effectively started from B, then generated D. A and C were present only indirectly and were not materialized as first-class client results.

## 3. Correct causal chain

MK02 must execute this order:

```text
YANDEX DEMAND
→ CLEAN PHRASES
→ TASK / INTENT CLUSTERS
→ INDEPENDENT PHRASE→TARGET LANDING MAP
→ CLUSTER→TARGET LANDING PAGE MAP
→ TARGET PAGE REGISTRY
→ TARGET PAGE HIERARCHY / SEO STRUCTURE
→ RECONCILE TARGET MODEL AGAINST CURRENT PUBLIC SITE
→ CLASSIFY EACH TARGET PAGE: CREATE / OPTIMIZE / KEEP / ROUTE / NO-STANDALONE / RECHECK
→ FULL PAGE-BY-PAGE TARGET SPECIFICATIONS
→ PHYSICAL CURRENT→TARGET CHANGE DELTA
→ CLIENT XLSX + ANALYTICAL PDF + TZ PDF
```

## 4. Required levels of mapping

### 4.1 Phrase level

Every active phrase must resolve to:

```text
phrase
→ task/cluster
→ intended target landing page key
→ target URL/route or explicit unresolved/no-standalone state
```

This full detail belongs in XLSX.

### 4.2 Cluster / landing-page level

Every material cluster/task must resolve to one intended primary landing page with:

```text
cluster/task
primary/representative query
member phrase count
intent
page type
page purpose
target URL/route
parent/section
supporting relationships
current match state
action state
```

### 4.3 Page-spec level

Every material target page must have a page specification even if no site change is needed:

```text
target page / URL
purpose
page type
parent/section
primary task/intent
primary query
semantic scope / cluster
phrase count
what the page should cover
what belongs elsewhere / no-standalone boundaries when material
supporting/child/related pages
current URL match/current state
action = CREATE | OPTIMIZE | KEEP | ROUTE | NO_STANDALONE | RECHECK
real site change = YES | NO | UNRESOLVED
implementation detail if change is real and resolved
acceptance / final expected state
uncertainty / clarification if needed
```

## 5. Rehearsal honesty

Do **not** falsify OKNO_MSK and do not pretend the current site lacks pages or mapping.

Correct rehearsal model:

```text
CURRENT SITE = REAL AS-IS INVENTORY / EVIDENCE
CURRENT PAGE MAPPING = NOT PRE-ACCEPTED AS TARGET ANSWER
TARGET LANDING MODEL = INDEPENDENTLY DERIVED FROM SEMANTICS/TASKS
THEN TARGET MODEL IS RECONCILED WITH CURRENT SITE
```

If many target pages match existing pages, classify them as KEEP / LOCK AS TARGET OWNER and still deliver their full page specifications.

## 6. Correct client package meaning

Physical package remains:

```text
1 XLSX
+ 1 ANALYTICAL PDF
+ 1 TZ PDF
+ SHORT HANDOFF MESSAGE
```

But the content contract changes.

### XLSX

Must visibly contain equivalent client views for:

1. all phrases;
2. clusters/tasks;
3. phrase→target page mapping;
4. cluster→target landing page map;
5. target site structure/page registry;
6. page-by-page target specifications;
7. current→target change delta;
8. unresolved/recheck/clarifications;
9. page relationships where material.

### Analytical PDF

Must show the **target site model**, not mainly counts:

- demand/task directions;
- how clusters become landing pages;
- target page registry or useful summary;
- target hierarchy/tree or hierarchical table;
- examples of landing assignments;
- current-vs-target match summary;
- create/optimize/keep/no-standalone/recheck classes;
- explanation that complete phrase-level mapping is in XLSX.

### TZ PDF

Must be a **page-by-page target specification**, not only a short list of physical changes.

It must let the recipient understand for each material target page what demand lands there, what role it has, where it sits in the structure, whether the current page already exists, what action applies, and what the finished target state is.

The physical change tickets are a subset/delta inside this fuller page-level specification.

## 7. Permanent hard failures

```text
CURRENT-SITE-FIRST MAPPING WITHOUT INDEPENDENT TARGET MODEL = FAIL
DELTA-ONLY CLIENT PACKAGE = FAIL
GOOD CURRENT SITE CAUSING TARGET PAGE SPECS TO DISAPPEAR = FAIL
PHRASE DETAIL ONLY WITHOUT CLUSTER→PAGE / PAGE→STRUCTURE VIEWS = FAIL
THOUSANDS OF PHRASES DUMPED INTO PDF INSTEAD OF PAGE-LEVEL SPEC = FAIL
KEEP / NO_CHANGE OMITTED FROM FULL PAGE SPEC REGISTER = FAIL
NO_STANDALONE TASK WITHOUT NAMED PARENT/OWNER ROUTE = FAIL
SMALL PHYSICAL CHANGE COUNT USED AS PRODUCT-VALUE PROXY = FAIL
```

## 8. Impact set

At minimum affected Level-1 rules:

- `steps/STEP_10_PAGE_OWNERSHIP_MAPPING.md`
- `steps/STEP_11_STRUCTURAL_ACTION_DIAGNOSIS.md`
- `steps/STEP_13_SEARCH_ONLY_ARCHITECTURE_FREEZE.md`
- `steps/STEP_14_IMPLEMENTATION_SPECIFICATION.md`
- `steps/STEP_15_CLIENT_MATERIALIZATION_QA.md`
- `STEP_RULES_INDEX.md`
- `DELIVERABLE_SPEC.md`
- `QA_AND_RELEASE.md`
- `PRODUCT_SCOPE.md`
- `PRODUCT_ROADMAP.md`
- `PRODUCT_PACKAGING.md`
- series cursor/state as needed.

Affected Level-2/client outputs include the OKNO_MSK target map views, target page registry, page specifications, client workbook, analytical PDF, TZ PDF and their QA/readback receipts.

The underlying accepted semantic phrase universe does **not** need to be discarded merely because the presentation/product causal chain was incomplete. Reuse preserved evidence and only reopen analytical authorities that are actually affected by target-first rematerialization.

## 9. Phase boundary

Phase 8 pricing/economics is blocked until this correction is executed and the corrected client package passes recipient QA.

```text
PHASE 7 PREVIOUS PASS = SUPERSEDED BY OWNER PRODUCT-GAP FINDING
CURRENT STATE = PHASE 7 CORRECTIVE REWORK REQUIRED
NEXT = TARGET-FIRST REBUILD / REMATERIALIZATION / QA / REMOTE READBACK
PHASE 8 = BLOCKED UNTIL CORRECTION PASS
```
