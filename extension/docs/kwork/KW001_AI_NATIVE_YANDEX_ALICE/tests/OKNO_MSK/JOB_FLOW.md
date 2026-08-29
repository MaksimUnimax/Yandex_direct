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

### Step 3R — repaired first-pass Wordstat acquisition
Status: **COMPLETE / VERIFIED**

```text
provider items = 18/18 complete
first-pass rows = 2415
targeted expansion rows = 550
total source rows entering cleanup = 2965
```

### Step 4 — family-level triage
Status: **COMPLETE AS TRIAGE**

### Step 5 — targeted Wordstat expansion
Status: **COMPLETE**

### Step 6 — demand dynamics
Status: **PRESERVED / REUSABLE**

### Step 6A — acquisition coverage revalidation
Status: **COMPLETE / SUFFICIENT**

### Step 7 — row-level semantic cleanup
Status: **COMPLETE AFTER POST-AUDIT CORRECTION**

```text
exact phrase keys = 2840
KEEP = 1388
REVIEW = 1118
EXCLUDE_SCOPE = 180
EXCLUDE_IRRELEVANT = 120
EXCLUDE_MECHANICAL = 34
```

### Step 8 — Search-stage semantic freeze
Status: **COMPLETE AFTER METHOD CORRECTION / SEARCH-STAGE INPUT FROZEN**

Correct final routing:

```text
CORE_CANDIDATE = 1388
REVIEW_SEARCH = 944
REVIEW_DEFERRED = 174
EXCLUDED_PRESERVED = 334
TOTAL = 2840
```

Removed/forbidden Step-08 routes:

```text
REVIEW_BUSINESS
REVIEW_SEARCH_AND_BUSINESS
```

Corrected freeze:

```text
2840/2840 phrase keys preserved
1118/1118 REVIEW routed
0 silent drops
0 semantic status rewrites
9/9 non-exact duplicate groups preserved
0 automatic merge
0 provider/Search requests
0 RUB cost
```

Canonical error control carried forward:

```text
RESEARCH_COLLECTED != METHOD_VALIDATED
SOURCE_TO_METHOD_TRACEABILITY_REQUIRED = true
```

## Current step — Step 9 ordinary Yandex Search validation

Status: **OWNER AUTHORIZED / INITIAL TRANCHE CORRECTED AFTER SEMANTIC AUDIT / PROVIDER EXECUTION NOT STARTED**

Authorities:

```text
STEP_09_ORDINARY_YANDEX_SEARCH_PRE_STEP_REVIEW_2026-08-29.md
STEP_09_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md
STEP_09_CURRENT_STATE_AND_EXECUTION_PROTOCOL_2026-08-29.md
STEP_09_INITIAL_TRANCHE_SEMANTIC_QA.json
```

Where the original pre-step conflicts with the post-audit correction, the postmortem/current-state authority supersedes it.

Permanent methodology status remains:

```text
STEP_09_PERMANENT_METHOD = UNVALIDATED
```

The current job-specific method is not automatically promoted into universal methodology.

### Step 9 purpose

Collect bounded ordinary Yandex SERP evidence for material intent/result-type/page-boundary questions that block later clustering and page ownership.

### Post-audit causal correction

The first builder made a method error:

```text
corrected_reason -> treated as a surrogate SERP/user-intent family
source_id -> treated as a surrogate semantic subfamily
lexical/source centrality -> treated as authoritative marker selection
accounting assignment -> described as Search evidence coverage
```

This was wrong because those fields describe **our acquisition/cleanup process**, not the user's observed Search task.

```text
CLEANUP_REASON != SEARCH_INTENT_CLUSTER
ACQUISITION_SOURCE != SEARCH_INTENT_CLUSTER
LEXICAL_SIMILARITY != SERP_COMPATIBILITY
TRACEABILITY_COMPLETE != FULL_SERP_EVIDENCE_COVERAGE
```

Why the mistake matters: one direct query can otherwise be allowed to silently stand in for many untested phrases even though their intents/result types may differ. That would repeat the Step-07 failure class `ACCOUNTING_QA != SEMANTIC_QA`.

The full causal explanation, concrete bad examples, external authorities, corrected method and non-repeat controls are recorded in `STEP_09_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md`.

### Corrected initial tranche

The 75 queries are now only:

```text
INITIAL_BOUNDED_SERP_TRANCHE
```

Their roles are:

```text
REVIEW_STRATIFIED_SAMPLE
= direct diagnostic query only; not marker authority for other phrases.

NONEXACT_DUPLICATE_VARIANT
= direct pairwise comparison input.

STEP1_BOUNDARY_OR_CORE_ANCHOR
= explicit direct contrast/control query.
```

Correct current counts:

```text
REVIEW_SEARCH_TOTAL = 944
INITIAL_TRANCHE_PROBES = 75
DIRECT_REVIEW_SEARCH_ROWS_IN_INITIAL_TRANCHE = 45
UNRESOLVED_UNPROBED_REVIEW_SEARCH_ROWS = 899
TRACEABILITY_COMPLETE = true
FULL_SERP_EVIDENCE_COVERAGE = false
PRE_SERP_TRANSFER_ALLOWED = false
PRE_SERP_TRANSFER_LINKS = 0
SEMANTIC_SAMPLE_QA = PASS_AS_INITIAL_BOUNDED_TRANCHE_ONLY
```

`TRACEABILITY_COMPLETE=true` means all 944 rows remain accounted for. It does not mean 944 rows have Search evidence.

### External method basis for the correction

Direct sources are preserved in the postmortem, including:

```text
Yandex query clustering: meaning / user intent
https://yandex.ru/support/webmaster/ru/service/queries-selection

Rush Analytics marker-query method: fully automatic marker selection is not reliable for arbitrary sites
https://www.rush-analytics.ru/faq/kak-nayti-markernye-zaprosy

Ahrefs: intent/SERP clustering differs from term/word clustering
https://ahrefs.com/blog/keyword-clustering/
https://ahrefs.com/blog/keyword-clustering-tools/

Semrush: shared intent and SERP similarity/overlap are page-level clustering evidence
https://www.semrush.com/blog/keyword-clustering/
https://www.semrush.com/blog/keyword-manager-clustering-tool/
```

### Baseline Search evidence unit

```text
ordinary Yandex Search only
searchType = RU
region = 213 Moscow
TOP-10
page = 0
GROUP_MODE_FLAT
docsInGroup = 1
relevance sorting
moderate family filter
typo correction ON
XML response
```

`TOP-10` remains an industry evidence convention used here, not an official Yandex SEO threshold.

### Overlap interpretation rule

```text
exact shared URLs = primary page-boundary evidence
domain overlap = secondary competitive-composition evidence
no automatic universal threshold such as 3 URLs => same page
```

### First provider tranche safety ceiling

```text
MAX_PROVIDER_REQUESTS = 80
INITIAL_TRANCHE_REQUESTS = 75
ESTIMATED_INITIAL_TRANCHE_COST_RUB = 36.6
MAX_PROVIDER_COST_RUB = 39.04
```

This is project-specific budget control, not an SEO sufficiency threshold.

### Corrected YMB interaction gate

The generic batch runtime is serial, but generic persistence is not enough for this project's completeness gate.

Forbidden execution shape for Step 09:

```text
start + next x75 + status in one unattended/manual block
```

Reason:

```text
TRANSPORT_PERSISTED != PROJECT_RESULT_COMPLETE
```

Required loop:

```text
start
-> verify zero provider calls

one next
-> at most one paid Search request
-> known governed outcome
-> complete raw payload preserved
-> normalized ranked rows readable
-> observed result count reconciled
-> request/cost/evidence reference preserved
-> only then another paid next
```

```text
OUTCOME_UNKNOWN => STOP / NO AUTOMATIC REPLAY
```

### Required Step-09 outputs after execution

```text
STEP_09_SEARCH_PROBE_MANIFEST.tsv
STEP_09_REVIEW_SEARCH_COVERAGE.tsv
STEP_09_SERP_RESULTS.tsv
STEP_09_SERP_COMPARISONS.tsv
STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv
STEP_09_SEARCH_RECONCILIATION.md
STEP_09_SEARCH_ACCEPTANCE_2026-08-29.md
```

### Current transition truth

```text
STEP_09_PRE_STEP_RESEARCH_REQUIRED = false
STEP_09_PRE_STEP_REVIEW_COMPLETE = true
STEP_09_SOURCE_TO_METHOD_TRACE_PASS = true
STEP_09_OWNER_AUTHORIZATION_PENDING = false
STEP_09_OWNER_AUTHORIZED = true
STEP_09_INITIAL_TRANCHE_CORRECTED = true
STEP_09_TRACEABILITY_ROWS = 944
STEP_09_FULL_SERP_EVIDENCE_COVERAGE = false
STEP_09_PRE_SERP_TRANSFER_LINKS = 0
STEP_09_EXECUTION_STARTED = false
STEP_09_PROVIDER_REQUESTS = 0
STEP_09_PROVIDER_COST_RUB = 0
STEP_09_COMPLETE = false
STEP_10_ALLOWED = false
```

## Remaining work

1. Execute Step 9 ordinary Search using the interaction-gated one-`next` loop.
2. Preserve/verify every paid result before another paid request.
3. Build Step-09 SERP results, comparisons, evidence decisions and reconciliation.
4. Keep non-probed rows unresolved unless a separate post-SERP evidence-transfer decision is explicitly justified.
5. Step 10 — user-task / SERP clustering.
6. Step 11 — page ownership mapping.
7. Step 12 — structural actions.
8. Step 13 — cannibalization diagnosis.
9. Step 14 — Search-only architecture freeze.
10. Step 15 — AI-case selection.
11. Step 16 — selective AI-search evidence.
12. Step 17 — Search-vs-AI comparison.
13. Step 18 — prioritization.
14. Step 19 — client deliverables.
15. Step 20 — final QA.
16. Step 21 — handoff/revisions.
17. Step 22 — job close.

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
| 8. Freeze Search-stage semantic set | Freeze exact Search input and executable unresolved routes | ✅ COMPLETE AFTER METHOD CORRECTION |
| **9. Ordinary Yandex Search validation** | **Resolve material intent/page-boundary uncertainty with real SERP evidence** | **🟡 CURRENT — OWNER AUTHORIZED / INITIAL TRANCHE CORRECTED / PROVIDER NOT STARTED** |
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

Markers:

```text
KW001_OKNO_MSK_JOB_FLOW_ACTIVE = true
KW001_OKNO_MSK_STEP08_COMPLETE_AFTER_METHOD_CORRECTION = true
KW001_OKNO_MSK_STEP08_REVIEW_SEARCH = 944
KW001_OKNO_MSK_STEP08_REVIEW_DEFERRED = 174
KW001_OKNO_MSK_STEP08_FORBIDDEN_BUSINESS_ROUTE_STATES = 0
KW001_OKNO_MSK_SEARCH_STAGE_INPUT_FROZEN = true
KW001_OKNO_MSK_STEP09_PRE_STEP_REVIEW_COMPLETE = true
KW001_OKNO_MSK_STEP09_SOURCE_TO_METHOD_TRACE_PASS = true
KW001_OKNO_MSK_STEP09_OWNER_AUTHORIZATION_PENDING = false
KW001_OKNO_MSK_STEP09_OWNER_AUTHORIZED = true
KW001_OKNO_MSK_STEP09_INITIAL_TRANCHE_CORRECTED = true
KW001_OKNO_MSK_STEP09_FULL_SERP_EVIDENCE_COVERAGE = false
KW001_OKNO_MSK_STEP09_PRE_SERP_TRANSFER_LINKS = 0
KW001_OKNO_MSK_STEP09_EXECUTION_STARTED = false
KW001_OKNO_MSK_STEP09_PROVIDER_REQUESTS = 0
KW001_OKNO_MSK_STEP09_PROVIDER_COST_RUB = 0
KW001_OKNO_MSK_STEP09_COMPLETE = false
KW001_OKNO_MSK_STEP10_ALLOWED = false
```
