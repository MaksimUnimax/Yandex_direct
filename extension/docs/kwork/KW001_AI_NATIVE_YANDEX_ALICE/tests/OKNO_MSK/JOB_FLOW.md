# KW-001 / OKNO-MSK — JOB FLOW

Date created: 2026-08-28
Last updated: 2026-08-29
Status: **ACTIVE / JOB-SPECIFIC / DISPOSABLE WITH WORKSPACE**

## Whole Kwork goal

Deliver a complete, evidence-backed semantic set and site/page structure recommendation for Yandex human search plus selective Yandex AI-search evidence, with client-ready artifacts and final QA.

## Genuinely complete

### Step 0 — mock order / scope freeze
Status: **COMPLETE**

### Step 1 — existing-site discovery / merged business-page model
Status: **COMPLETE / PASS AFTER CROSS-CHANNEL REWORK**

### Step 2 — first-pass Wordstat seed/query plan
Status: **COMPLETE / FROZEN**

Frozen input remains the original 18 seeds.

### Step 03R — repaired first-pass Wordstat acquisition
Status: **COMPLETE / FINAL RECONCILIATION PASS**

```text
job_id = kw001-okno-msk-wordstat-pass1-repair-20260829
region = 213
device = DEVICE_ALL
numPhrases = 200
execution = Manual
batch status = COMPLETED
provider requests executed = 18
provider outcomes known = 18
succeeded = 18
failed_terminal = 0
outcome_unknown = 0
estimated provider cost = 0.36 RUB
fully preserved + normalized + verified = 18/18
results rows preserved/verified = 2153
association rows preserved/verified = 262
total provider rows preserved/verified = 2415
```

Historical Step-03 acceptance remains superseded because it had technical success without complete reusable data preservation. Step 03R is the accepted replacement evidence.

### Wordstat acquisition coverage revalidation
Status: **COMPLETE / PASS / SUFFICIENT**

```text
complete first-pass rows = 2415
preserved targeted probes = 4/4
targeted probe results = 483
targeted probe associations = 67
targeted probe rows = 550
probe exact matches to first-pass rows = 17
probe rows with no exact first-pass match = 533
new provider calls during revalidation = 0
additional provider cost = 0 RUB
ACQUISITION_COVERAGE_VERDICT = SUFFICIENT
ADDITIONAL_WORDSTAT_REQUESTS_REQUIRED_NOW = 0
```

The four probes confirmed/further covered window hardware language, panoramic applications, balcony-extension engineering and private-house window demand. `533` remains an exact-string comparison count only.

Authority: `STEP_04A_WORDSTAT_COVERAGE_AND_EXPANSION_REVALIDATION_2026-08-29.md`.

### Preserved dynamics evidence
Status: **PRESERVED / REUSABLE / DOES NOT ADVANCE WORKFLOW BY ITSELF**

```text
4/4 dynamics provider observations completely preserved
24 monthly rows per root preserved
0 failed provider requests
0 outcome_unknown
estimated provider cost = 0.08 RUB
```

### Step 07B — historical row-level accounting / deterministic prefilter
Status: **ACCOUNTING PASS / HISTORICAL SEMANTIC PASS SUPERSEDED**

The historical Step 07B run correctly accounted for all preserved source data:

```text
repaired first-pass source rows = 2415
targeted-probe source rows = 550
TOTAL source rows = 2965
result rows = 2636
association rows = 329
unique exact normalized phrases = 2840
duplicate source occurrences = 125
phrase keys with >1 source occurrence = 101
canonical provenance occurrence sum = 2965
UNCLASSIFIED = 0
```

Historical classifier output:

```text
KEEP = 1760
REVIEW = 749
EXCLUDE_SCOPE = 180
EXCLUDE_IRRELEVANT = 120
EXCLUDE_MECHANICAL = 31
STATUS TOTAL = 2840
```

The owner-requested fresh external methodology audit found a material default-KEEP defect: result phrases could become KEEP merely because no known exclusion/review dictionary matched. The historical semantic PASS is therefore superseded while its complete accounting/provenance evidence remains valid.

Authority: `STEP_07B_POST_AUDIT_CORRECTION_REQUIRED_2026-08-29.md`.

## Current step — Step 07C semantic correction candidate

Status: **CORRECTION CANDIDATE READY / OWNER REVIEW PENDING / NEXT STEP BLOCKED**

The correction reuses the same complete corpus. No new Wordstat/provider acquisition occurred.

Corrected candidate:

```text
source occurrences = 2965
exact phrase keys = 2840
KEEP = 1388
REVIEW = 1118
EXCLUDE_SCOPE = 180
EXCLUDE_IRRELEVANT = 120
EXCLUDE_MECHANICAL = 34
STATUS TOTAL = 2840
```

Historical-to-candidate transitions:

```text
KEEP -> KEEP = 1388
KEEP -> REVIEW = 369
KEEP -> EXCLUDE_MECHANICAL = 3
REVIEW -> REVIEW = 749
EXCLUDE_SCOPE -> EXCLUDE_SCOPE = 180
EXCLUDE_IRRELEVANT -> EXCLUDE_IRRELEVANT = 120
EXCLUDE_MECHANICAL -> EXCLUDE_MECHANICAL = 31
historical non-KEEP -> KEEP = 0
```

Correction contract:

```text
KEEP requires explicit POSITIVE_* evidence tied to accepted Step-01 business/site families
default KEEP fallthrough = false
uncertain but potentially relevant phrase -> REVIEW
low frequency alone never excludes
associations are never automatically promoted to KEEP
historical REVIEW/EXCLUDE rows are not promoted upward
non-exact duplicate candidates are surfaced, not auto-merged
```

Post-generation QA:

```text
builder QA cases = 21
builder QA failures = 0
expanded semantic QA cases = 72
expanded semantic QA failures = 0
manual semantic saturation passes = 4
```

The semantic QA was allowed to fail during correction. Those failures exposed and caused fixes for real defects such as Russian `окон`/`окн` morphology and reordered state fragments such as `окно пластиковое закрыто`.

Non-exact duplicate candidates:

```text
candidate groups = 9
candidate rows = 18
automatic merges = 0
```

Examples corrected/demoted from historical unsafe KEEP include navigational REHAU queries, REHAU diagnostics, component/hardware intent, DIY/technical intent, incomplete fragments, panoramic real-estate/inspiration queries, uncertain demolition service intent and malformed repair phrases.

Artifacts:

```text
STEP_07C_SEMANTIC_CORRECTION_BUILD.py
STEP_07C_SEMANTIC_CORRECTION_RUN.py
STEP_07C_SEMANTIC_CORRECTION_WORKING.tsv
STEP_07C_SEMANTIC_CORRECTION_OCCURRENCES.tsv
STEP_07C_NONEXACT_DUPLICATE_CANDIDATES.tsv
STEP_07C_SEMANTIC_QA_CASES.tsv
STEP_07C_SEMANTIC_QA_CASES_V2.tsv
STEP_07C_SEMANTIC_CORRECTION_SUMMARY.json
STEP_07C_SEMANTIC_CORRECTION_REVIEW_2026-08-29.md
```

Current candidate verdict:

```text
ROW_LEVEL_DATA_ACCOUNTING = PASS
PROVENANCE_RECONCILIATION = PASS
DEFAULT_KEEP_DEFECT = CORRECTED
KEEP_POSITIVE_EVIDENCE_GATE = PASS
SEMANTIC_QA = PASS_AS_CANDIDATE
CORRECTION_CANDIDATE_READY = true
OWNER_REVIEW_PENDING = true
ROW_LEVEL_CLEANUP_FINAL_ACCEPTANCE = false
ROW_LEVEL_CLEANUP_COMPLETE = false
NEXT_STEP_ALLOWED = false
```

This is intentionally not a self-acceptance. The owner and assistant now review the corrected result and decide whether to accept it or run another correction pass.

## Remaining work

1. Review the Step-07C correction candidate and either accept it or reopen another cleanup correction.
2. Only after correction acceptance, freeze the final working semantic set / Search-stage input.
3. Validate important query/page boundaries in ordinary Yandex Search.
4. Group the Search-validated semantic set by user task/SERP compatibility.
5. Map groups to existing pages and decide page ownership/actions.
6. Diagnose real cannibalization where evidence supports it.
7. Freeze Search-only architecture before AI evidence.
8. Select only material uncertain cases for AI-search evidence; use Webmaster Alice visibility if access exists, otherwise a small GenSearch set.
9. Compare ordinary Search and AI evidence.
10. Prioritize actions.
11. Produce client deliverables.
12. Run final QA and revision gate.
13. Close/handoff job and only then delete disposable workspace.

Not complete yet:

```text
ROW_LEVEL_CLEANUP_COMPLETE = false
FINAL_SEMANTIC_SET_COMPLETE = false
ORDINARY_YANDEX_SEARCH_VALIDATION_COMPLETE = false
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
| **7. Row-level semantic cleanup** | **Produce trustworthy phrase-level decisions** | **🟡 CORRECTION CANDIDATE READY / OWNER REVIEW PENDING** |
| 8. Freeze Search-stage semantic set | Freeze corrected rows allowed into Search | ⛔ BLOCKED |
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

When the job is fully completed and handed off, mark `JOB_MANIFEST safe_to_delete = true`, then delete this whole OKNO_MSK workspace.

Markers:

```text
KW001_OKNO_MSK_JOB_FLOW_ACTIVE = true
KW001_OKNO_MSK_STEP_03_COMPLETE = true
KW001_OKNO_MSK_STEP_03R_PROVIDER_ITEMS_PRESERVED = 18
KW001_OKNO_MSK_STEP_03R_NORMALIZED_ROWS_VERIFIED = 2415
KW001_OKNO_MSK_WORDSTAT_COVERAGE_REVALIDATION_COMPLETE = true
KW001_OKNO_MSK_WORDSTAT_COVERAGE_VERDICT_SUFFICIENT = true
KW001_OKNO_MSK_TARGETED_PROBE_ROWS_RECHECKED = 550
KW001_OKNO_MSK_ADDITIONAL_WORDSTAT_REQUESTS_REQUIRED_NOW = 0
KW001_OKNO_MSK_ROW_LEVEL_DATA_ACCOUNTING_PASS = true
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_INPUT_ROWS = 2965
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_UNIQUE_EXACT = 2840
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_DUPLICATE_OCCURRENCES = 125
KW001_OKNO_MSK_STEP07C_KEEP = 1388
KW001_OKNO_MSK_STEP07C_REVIEW = 1118
KW001_OKNO_MSK_STEP07C_EXCLUDE_SCOPE = 180
KW001_OKNO_MSK_STEP07C_EXCLUDE_IRRELEVANT = 120
KW001_OKNO_MSK_STEP07C_EXCLUDE_MECHANICAL = 34
KW001_OKNO_MSK_STEP07C_SEMANTIC_QA_FAILURES = 0
KW001_OKNO_MSK_STEP07C_CORRECTION_CANDIDATE_READY = true
KW001_OKNO_MSK_STEP07C_OWNER_REVIEW_PENDING = true
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_COMPLETE = false
KW001_OKNO_MSK_NEXT_STEP_ALLOWED = false
KW001_OKNO_MSK_FINAL_SEMANTIC_SET_COMPLETE = false
KW001_OKNO_MSK_STEP_05_RAW_PROVIDER_EVIDENCE_PRESERVED = true
KW001_OKNO_MSK_STEP_06_RAW_PROVIDER_EVIDENCE_PRESERVED = true
```