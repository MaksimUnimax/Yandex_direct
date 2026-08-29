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

### Step 07B — row-level data accounting / deterministic prefilter
Status: **ACCOUNTING PASS / SEMANTIC PASS SUPERSEDED / CORRECTION IN PROGRESS**

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

Historical classifier output was:

```text
KEEP = 1760
REVIEW = 749
EXCLUDE_SCOPE = 180
EXCLUDE_IRRELEVANT = 120
EXCLUDE_MECHANICAL = 31
STATUS TOTAL = 2840
```

Those counts are preserved for audit/comparison but are no longer accepted as completed semantic cleanup.

Owner-requested fresh external methodology audit found that the historical rule engine used a default-KEEP fallthrough: result phrases not matched by known exclusion or boundary dictionaries became KEEP even when positive semantic relevance/user intent had not been demonstrated.

Concrete false-KEEP / dictionary-dependence evidence included:

```text
1 установка пластиковых окон -> KEEP
6 6 с панорамными окнами -> KEEP
rehau окна 2 -> KEEP
алюминиевые окна 2 -> KEEP
rehau окна анадырский проезд д 47 -> KEEP
rehau микролифт для окна -> KEEP while similar hardware terms were REVIEW
```

Post-audit verdict:

```text
ROW_LEVEL_DATA_ACCOUNTING = PASS
EXACT_DEDUPLICATION_ACCOUNTING = PASS
DETERMINISTIC_PREFILTER = PASS
FULL_SEMANTIC_ROW_REVIEW = CORRECTION_REQUIRED
SEMANTIC_CLEANUP_COMPLETE = false
NEXT_STEP_ALLOWED = false
```

Authority: `STEP_07B_POST_AUDIT_CORRECTION_REQUIRED_2026-08-29.md`.

Historical artifacts remain preserved for comparison:

```text
STEP_07B_ROW_LEVEL_CLEANUP_BUILD.py
STEP_07B_ROW_LEVEL_CLEANUP_WORKING.tsv
STEP_07B_ROW_LEVEL_CLEANUP_OCCURRENCES.tsv
STEP_07B_ROW_LEVEL_CLEANUP_SUMMARY.json
STEP_07B_ROW_LEVEL_CLEANUP_ACCEPTANCE_2026-08-29.md
```

## Current step

Status: **ROW-LEVEL CLEANUP CORRECTION IN PROGRESS / NEXT STEP BLOCKED**

Correction goal:

1. Reuse the same 2965 source occurrences and 2840 exact phrase keys; do not recollect Wordstat.
2. Preserve all existing provenance and arithmetic controls.
3. Replace default KEEP with positive-evidence KEEP: a phrase is KEEP only when its user need is clearly compatible with the known OKNO-MSK business/site model.
4. If a phrase may be relevant but positive KEEP is not established, assign REVIEW rather than silently accepting it.
5. Keep deterministic exclusions only where the mismatch/scope failure is unambiguous.
6. Surface non-obvious duplicate candidates separately; do not silently merge them by lexical normalization alone.
7. Perform post-generation semantic QA on the corrected decision set in addition to machine reconciliation.
8. Create an explicit correction acceptance before allowing the workflow forward.

No provider action is required for this correction.

## Remaining work

1. Complete and audit the Step-07B semantic correction.
2. Freeze the final working semantic set / Search-stage input only after corrected cleanup acceptance.
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
| 7. Row-level semantic cleanup | Produce trustworthy phrase-level decisions | 🔁 CORRECTION IN PROGRESS |
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
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_CORRECTION_REQUIRED = true
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_COMPLETE = false
KW001_OKNO_MSK_NEXT_STEP_ALLOWED = false
KW001_OKNO_MSK_FINAL_SEMANTIC_SET_COMPLETE = false
KW001_OKNO_MSK_STEP_05_RAW_PROVIDER_EVIDENCE_PRESERVED = true
KW001_OKNO_MSK_STEP_06_RAW_PROVIDER_EVIDENCE_PRESERVED = true
```