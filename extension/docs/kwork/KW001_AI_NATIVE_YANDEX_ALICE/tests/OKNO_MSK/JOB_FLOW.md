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
```

Historical Step 07B semantic PASS remains superseded because of its default-KEEP defect. Step-07C acceptance authority:

`STEP_07C_SEMANTIC_CORRECTION_ACCEPTANCE_2026-08-29.md`.

### Step 8 — Search-stage semantic freeze
Status: **COMPLETE / PASS / SEARCH-STAGE INPUT FROZEN**

Step 8 preserved accepted Step-07C semantic truth and added an explicit routing layer without executing Search or making downstream cluster/page decisions.

Final routing:

```text
CORE_CANDIDATE = 1388
REVIEW_SEARCH = 228
REVIEW_BUSINESS = 0
REVIEW_SEARCH_AND_BUSINESS = 716
REVIEW_DEFERRED = 174
EXCLUDED_PRESERVED = 334
TOTAL = 2840
```

Reconciliation:

```text
phrase keys written = 2840/2840
REVIEW routed = 1118/1118
unrouted REVIEW = 0
silent drops = 0
Step-07C semantic status rewrites = 0
non-exact duplicate groups preserved = 9/9
non-exact duplicate rows preserved = 18/18
automatic non-exact merges = 0
provider/Search requests executed = 0
provider cost = 0 RUB
```

During manual QA, the first generated duplicate handoff was found to use one hard-coded Search route for every duplicate group. That conflicted with one association-only group whose member rows were `REVIEW_DEFERRED` in the main freeze. The handoff was corrected before acceptance so duplicate-group routing now derives from member disposition.

Final duplicate-group routes:

```text
ORDINARY_SEARCH_BEFORE_ANY_NONEXACT_MERGE = 6
SEARCH_AND_BUSINESS_BEFORE_ANY_NONEXACT_MERGE = 2
DEFER_UNLESS_GROUP_SELECTED_FOR_SEARCH = 1
```

Acceptance authority:

`STEP_08_SEARCH_STAGE_FREEZE_ACCEPTANCE_2026-08-29.md`.

Frozen Search-stage artifacts:

```text
STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv
STEP_08_REVIEW_RESOLUTION_ROUTES.tsv
STEP_08_NONEXACT_DUPLICATE_HANDOFF.tsv
STEP_08_SEARCH_STAGE_FREEZE_RECONCILIATION.md
```

## Current transition — Step 9 pre-step required

The next major analytical stage is **Step 9 — ordinary Yandex Search validation**.

Status: **PRE-STEP METHOD RESEARCH REQUIRED / EXECUTION NOT AUTHORIZED**

Permanent methodology index status:

```text
STEP_09_PERMANENT_METHOD = UNVALIDATED
```

Therefore Step 9 must not start with Search/provider calls yet. The next action must be the full current-method pre-step review required by the universal rules:

```text
read current rule architecture + Step rules index
→ restate whole Kwork goal + full roadmap
→ read accepted Step-8 freeze evidence
→ identify relevant prior errors and causal controls
→ research current ordinary-Yandex/Search/SERP methodology from external sources
→ define exactly which Search evidence is needed and how to bound it
→ embed the YMB per-interaction result-preservation/completeness gate if YMB is used
→ show owner method + sources + risks + pass condition
→ wait for explicit owner authorization
→ only then execute Search
```

Current transition truth:

```text
STEP_08_COMPLETE = true
SEARCH_STAGE_INPUT_FROZEN = true
STEP_09_PRE_STEP_RESEARCH_REQUIRED = true
STEP_09_EXECUTION_ALLOWED = false
```

## Remaining work

1. Research and authorize Step 9 ordinary Yandex Search validation methodology.
2. Execute and preserve bounded ordinary Yandex Search evidence for the material intent/page-boundary questions selected by the Step-9 method.
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

Not complete yet:

```text
FINAL_SEMANTIC_SET_COMPLETE = false
ORDINARY_YANDEX_SEARCH_VALIDATION_COMPLETE = false
USER_TASK_SERP_CLUSTERING_COMPLETE = false
PAGE_OWNERSHIP_COMPLETE = false
STRUCTURAL_ACTIONS_COMPLETE = false
SEARCH_ONLY_ARCHITECTURE_COMPLETE = false
AI_EVIDENCE_COMPLETE = false
CLIENT_DELIVERABLES_COMPLETE = false
FINAL_QA_COMPLETE = false
```

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
| 8. Freeze Search-stage semantic set | Freeze exact Search input and route unresolved phrases | ✅ COMPLETE |
| **9. Ordinary Yandex Search validation** | **Resolve material intent/page-boundary uncertainty with real SERP evidence** | **🟡 CURRENT GATE — PRE-STEP RESEARCH REQUIRED / EXECUTION NOT AUTHORIZED** |
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
KW001_OKNO_MSK_STEP08_COMPLETE = true
KW001_OKNO_MSK_SEARCH_STAGE_INPUT_FROZEN = true
KW001_OKNO_MSK_STEP08_UNROUTED_REVIEW = 0
KW001_OKNO_MSK_STEP08_STATUS_REWRITES = 0
KW001_OKNO_MSK_STEP09_PRE_STEP_RESEARCH_REQUIRED = true
KW001_OKNO_MSK_STEP09_EXECUTION_ALLOWED = false
```
