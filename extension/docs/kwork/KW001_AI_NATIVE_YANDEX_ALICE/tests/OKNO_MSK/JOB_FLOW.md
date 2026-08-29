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

Status: **PRE-STEP METHOD REVIEW COMPLETE / OWNER AUTHORIZATION PENDING / EXECUTION NOT STARTED**

Authority:

`STEP_09_ORDINARY_YANDEX_SEARCH_PRE_STEP_REVIEW_2026-08-29.md`

Permanent methodology status remains:

```text
STEP_09_PERMANENT_METHOD = UNVALIDATED
```

The current job-specific method is therefore not automatically promoted into permanent methodology.

### Step 9 purpose

Collect bounded ordinary Yandex SERP evidence for the material intent/result-type/page-boundary questions that block later clustering and page ownership.

### Why not Search every active phrase

There is no authoritative method saying that each active keyword must receive its own paid SERP request before clustering. Industry practice compares TOP result sets and marker/contrast queries; therefore this job will probe the **decisions that need evidence**, while keeping all 944 `REVIEW_SEARCH` rows mapped to an evidence question or explicitly unresolved.

Method sources are recorded directly in the pre-step, including:

```text
Yandex Webmaster relevance/query-page evidence
Yandex Search API request and region semantics
Yandex Search API pricing
Rush Analytics TOP-10 overlap methodology
Topvisor TOP-10 soft/middle/hard methodology
Ahrefs SERP comparison / search intent
Semrush SERP overlap / clustering practice
```

### Mandatory coverage before paid execution can pass

```text
material Step-01 page-boundary questions represented
all 8 active Search-routed non-exact duplicate groups directly compared
every distinct REVIEW_SEARCH corrected_reason represented
base commercial/page directions represented as core anchors
all 944 REVIEW_SEARCH rows mapped to an evidence_question_id or explicit UNRESOLVED state
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

`TOP-10` is an industry evidence convention used here, not an official Yandex SEO threshold.

### Overlap interpretation rule

```text
exact shared URLs = primary page-boundary evidence
domain overlap = secondary competitive-composition evidence
no automatic universal threshold such as 3 URLs => same page
```

Different industry methods use different overlap rules, so a single hard cutoff is not promoted into a universal truth.

### First provider tranche safety ceiling

```text
MAX_PROVIDER_REQUESTS = 80
MAX_PROVIDER_COST_RUB = 39.04
```

This is project-specific budget control based on current ordinary synchronous Search pricing `0.488 RUB/request`, not an SEO sufficiency threshold.

If the frozen manifest exceeds 80 required direct probes, no provider call is allowed until the owner explicitly authorizes a larger tranche.

### YMB interaction gate

```text
service = search
SEARCH_BATCH_API_V1
ordinary Search only
no GenSearch
freeze manifest before paid execution
one explicit next <= one provider request
save + verify complete current result before another paid next
OUTCOME_UNKNOWN => no automatic replay
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
STEP_09_OWNER_AUTHORIZATION_PENDING = true
STEP_09_EXECUTION_STARTED = false
STEP_09_PROVIDER_REQUESTS = 0
STEP_09_PROVIDER_COST_RUB = 0
STEP_09_COMPLETE = false
STEP_10_ALLOWED = false
```

## Remaining work

1. Execute Step 9 bounded ordinary-Yandex Search evidence after owner authorization.
2. Step 10 — user-task / SERP clustering.
3. Step 11 — page ownership mapping.
4. Step 12 — structural actions.
5. Step 13 — cannibalization diagnosis.
6. Step 14 — Search-only architecture freeze.
7. Step 15 — AI-case selection.
8. Step 16 — selective AI-search evidence.
9. Step 17 — Search-vs-AI comparison.
10. Step 18 — prioritization.
11. Step 19 — client deliverables.
12. Step 20 — final QA.
13. Step 21 — handoff/revisions.
14. Step 22 — job close.

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
| **9. Ordinary Yandex Search validation** | **Resolve material intent/page-boundary uncertainty with real SERP evidence** | **🟡 CURRENT — PRE-STEP COMPLETE / AUTHORIZATION PENDING** |
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
KW001_OKNO_MSK_STEP09_OWNER_AUTHORIZATION_PENDING = true
KW001_OKNO_MSK_STEP09_EXECUTION_STARTED = false
KW001_OKNO_MSK_STEP09_PROVIDER_REQUESTS = 0
KW001_OKNO_MSK_STEP09_PROVIDER_COST_RUB = 0
KW001_OKNO_MSK_STEP09_COMPLETE = false
KW001_OKNO_MSK_STEP10_ALLOWED = false
```