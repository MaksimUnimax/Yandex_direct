# KW-001 / OKNO-MSK — JOB FLOW

Date created: 2026-08-28
Last updated: 2026-08-29
Status: **ACTIVE / JOB-SPECIFIC / DISPOSABLE WITH WORKSPACE**

## Whole Kwork goal

Deliver a complete, evidence-backed semantic set and site/page structure recommendation for Yandex ordinary Search plus selective Yandex AI-search evidence, with client-ready artifacts and final QA.

## Accepted completed work

### Step 0 — scope freeze
Status: **COMPLETE**

### Step 1 — existing-site discovery / business-page model
Status: **COMPLETE / PASS AFTER CROSS-CHANNEL REWORK**

### Step 2 — Wordstat acquisition plan
Status: **COMPLETE / FROZEN**

### Step 3 — historical first Wordstat pass
Status: **SUPERSEDED**

Technical request success was incorrectly accepted before complete reusable returned data had been preserved.

### Step 3R — repaired first-pass Wordstat acquisition
Status: **COMPLETE / VERIFIED**

```text
provider items = 18/18 complete
results rows = 2153
association rows = 262
total first-pass rows = 2415
estimated provider cost = 0.36 RUB
```

### Step 4 — family-level triage
Status: **COMPLETE AS TRIAGE / NOT TREATED AS ROW-LEVEL CLEANUP**

### Step 5 — targeted Wordstat expansion
Status: **COMPLETE**

```text
targeted probe rows = 550
additional acquisition currently required = 0
```

### Step 6 — demand dynamics
Status: **PRESERVED / REUSABLE**

### Step 6A — acquisition coverage revalidation
Status: **COMPLETE / SUFFICIENT**

### Step 7 — row-level semantic cleanup
Status: **COMPLETE AFTER POST-AUDIT CORRECTION**

Historical Step 07B accounting was valid but its semantic PASS was superseded because of default-KEEP fallthrough.

Accepted corrected Step 07C:

```text
source occurrences = 2965
exact phrase keys = 2840
KEEP = 1388
REVIEW = 1118
EXCLUDE_SCOPE = 180
EXCLUDE_IRRELEVANT = 120
EXCLUDE_MECHANICAL = 34
TOTAL = 2840
builder QA failures = 0
expanded semantic QA failures = 0
manual semantic saturation passes = 4
```

Owner acceptance authority:

`STEP_07C_SEMANTIC_CORRECTION_ACCEPTANCE_2026-08-29.md`.

Permanent Step-7 lesson now requires positive-evidence KEEP, separate accounting/semantic QA, explicit REVIEW uncertainty and cause-level correction rather than mechanical phrase exceptions.

## Current step — Step 8 Search-stage semantic freeze

Status: **PRE-STEP METHOD REVIEW COMPLETE / WAITING OWNER AUTHORIZATION / EXECUTION NOT STARTED**

Permanent methodology index status before this review:

```text
STEP_08_PERMANENT_METHOD = UNVALIDATED
```

Therefore fresh external research was performed before execution.

Authority:

`STEP_08_SEARCH_STAGE_FREEZE_PRE_STEP_REVIEW_2026-08-29.md`.

### Step 8 purpose

Create an immutable, auditable handoff from accepted Step-07C phrase decisions into ordinary Yandex Search validation without prematurely making final clustering, page ownership or architecture decisions.

### Proposed Step-8 accounting contract

```text
Step-07C exact phrase keys = 2840
KEEP carried as CORE_CANDIDATE = 1388
REVIEW rows requiring one explicit next-resolution route = 1118
EXCLUDE_* rows preserved for audit = 334
TOTAL = 2840
non-exact duplicate candidate groups carried = 9
Search/provider calls during Step 8 = 0
```

Step 08 will preserve Step-07C semantic status and add only Search-stage disposition / next-resolution routing.

REVIEW must not be silently discarded. Depending on why a phrase is unresolved, routing may point to ordinary Search, business-scope evidence, both, or a deferred evidence queue.

### What Step 8 explicitly does not do

```text
no new Wordstat
no ordinary Search requests
no final clustering
no page ownership
no structural action
no cannibalization verdict
no AI evidence
no frequency-only deletion
no silent non-exact duplicate merging
no silent resolution of UNKNOWN business priorities
```

### Current transition state

```text
STEP_08_PRE_STEP_REVIEW_COMPLETE = true
STEP_08_OWNER_AUTHORIZATION_PENDING = true
STEP_08_EXECUTION_STARTED = false
STEP_08_COMPLETE = false
NEXT_STEP_09_ALLOWED = false
```

## Remaining work

1. Execute and verify Step 8 Search-stage semantic freeze after owner authorization.
2. Validate material query/intent/page boundaries in ordinary Yandex Search.
3. Group Search-validated semantics by user task and SERP compatibility.
4. Map groups to existing pages and decide page ownership.
5. Determine structural actions: keep / expand / split / merge / reassign / new page.
6. Diagnose actual cannibalization where evidence supports it.
7. Freeze Search-only architecture before AI evidence.
8. Select only material uncertain cases for AI-search evidence.
9. Obtain selective AI-search evidence.
10. Compare ordinary Search and AI evidence.
11. Prioritize actions.
12. Produce client-facing deliverables.
13. Run final QA.
14. Handoff and process allowed revisions.
15. Close and delete disposable workspace only when safe.

## Full roadmap status

| Major step | Meaning | Status |
|---|---|---|
| 0. Scope freeze | Freeze business/region/order boundaries | ✅ COMPLETE |
| 1. Existing-site discovery | Build cross-checked site/business/page model | ✅ COMPLETE |
| 2. Wordstat acquisition plan | Freeze first-pass demand probes | ✅ COMPLETE |
| 3. Historical first pass | Original provider-success-only acceptance | 🔁 SUPERSEDED |
| 3R. Repaired first pass | Preserve complete reusable Wordstat data | ✅ COMPLETE |
| 4. Family-level triage | Identify families/noise/ambiguity/probe candidates | ✅ COMPLETE AS TRIAGE |
| 5. Targeted Wordstat expansion | Fill/confirm material acquisition directions | ✅ COMPLETE |
| 6. Demand dynamics | Preserve seasonality context | ✅ PRESERVED |
| 6A. Acquisition coverage revalidation | Decide whether more Wordstat is needed | ✅ COMPLETE |
| 7. Row-level semantic cleanup | Produce trustworthy phrase-level decisions | ✅ COMPLETE AFTER CORRECTION |
| **8. Freeze Search-stage semantic set** | **Freeze the exact Search-stage handoff and route unresolved phrases** | **🟡 CURRENT — PRE-STEP REVIEW COMPLETE / AUTHORIZATION PENDING** |
| 9. Ordinary Yandex Search validation | Resolve intent/page boundaries with real SERP | ⬜ NOT STARTED |
| 10. User-task / SERP clustering | Group compatible search jobs | ⬜ NOT STARTED |
| 11. Page ownership | Map clusters to best existing URLs | ⬜ NOT STARTED |
| 12. Structural actions | Keep/expand/split/merge/create decisions | ⬜ NOT STARTED |
| 13. Cannibalization diagnosis | Confirm real competing-page conflicts | ⬜ NOT STARTED |
| 14. Search-only architecture freeze | Freeze architecture before AI | ⬜ NOT STARTED |
| 15. AI-case selection | Select high-information uncertain cases | ⬜ NOT STARTED |
| 16. AI-search evidence | Gather selected Alice/GenSearch evidence | ⬜ NOT STARTED |
| 17. Search-vs-AI comparison | Compare classic Search and AI evidence | ⬜ NOT STARTED |
| 18. Prioritization | Rank recommended actions | ⬜ NOT STARTED |
| 19. Client deliverables | Produce client-ready workbooks/maps/matrices | ⬜ NOT STARTED |
| 20. Final QA | Reconcile evidence, numbers and recommendations | ⬜ NOT STARTED |
| 21. Handoff/revisions | Deliver and process allowed revisions | ⬜ NOT STARTED |
| 22. Job close | Mark safe-to-delete and remove disposable workspace | ⬜ NOT STARTED |

## Close

When the job is fully completed and handed off, mark `JOB_MANIFEST safe_to_delete = true`, then delete the whole disposable OKNO_MSK workspace.

Markers:

```text
KW001_OKNO_MSK_JOB_FLOW_ACTIVE = true
KW001_OKNO_MSK_STEP07C_FINAL_ACCEPTANCE = true
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_COMPLETE = true
KW001_OKNO_MSK_STEP08_PRE_STEP_REVIEW_COMPLETE = true
KW001_OKNO_MSK_STEP08_OWNER_AUTHORIZATION_PENDING = true
KW001_OKNO_MSK_STEP08_EXECUTION_STARTED = false
KW001_OKNO_MSK_STEP08_COMPLETE = false
KW001_OKNO_MSK_NEXT_STEP_09_ALLOWED = false
```
