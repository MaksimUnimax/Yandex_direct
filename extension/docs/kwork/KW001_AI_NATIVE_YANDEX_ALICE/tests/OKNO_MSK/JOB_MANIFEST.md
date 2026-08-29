# KW-001 / OKNO-MSK — JOB MANIFEST

Date updated: 2026-08-29
Workspace status: **ACTIVE / DISPOSABLE / JOB-SPECIFIC ONLY / LEGACY PATH**

```text
JOB_ID = OKNO_MSK
KWORK_ID = KW001_AI_NATIVE_YANDEX_ALICE
workspace_path = extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/
canonical_future_workspace_path = extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/work/<JOB_ID>/
workspace_is_disposable = true
workspace_contains_universal_rules = false
legacy_path_allowed_until_close = true
current_major_step = ROW_LEVEL_CLEANUP_CORRECTION_CANDIDATE_READY
next_major_step = BLOCKED_PENDING_OWNER_REVIEW_AND_CORRECTION_ACCEPTANCE
job_work_complete = false
final_handoff_complete = false
revision_rework_open = true
provider_operator_action_pending = false
safe_to_delete = false
```

## Authority

This directory is temporary job memory only. Universal KW-001 rules remain in the parent permanent layer and are owner-locked.

Current execution authorities:

```text
JOB_FLOW.md
STEP_03_COMPLETION_CORRECTION_2026-08-29.md
STEP_03R_WORDSTAT_REPAIR_MANIFEST_2026-08-29.md
STEP_03R_FINAL_RECONCILIATION_2026-08-29.md
STEP_04A_WORDSTAT_COVERAGE_AND_EXPANSION_REVALIDATION_2026-08-29.md
STEP_07B_ROW_LEVEL_CLEANUP_BUILD.py
STEP_07B_ROW_LEVEL_CLEANUP_SUMMARY.json
STEP_07B_ROW_LEVEL_CLEANUP_ACCEPTANCE_2026-08-29.md (HISTORICAL SEMANTIC PASS SUPERSEDED)
STEP_07B_POST_AUDIT_CORRECTION_REQUIRED_2026-08-29.md
STEP_07C_SEMANTIC_CORRECTION_BUILD.py
STEP_07C_SEMANTIC_CORRECTION_RUN.py
STEP_07C_SEMANTIC_CORRECTION_SUMMARY.json
STEP_07C_SEMANTIC_CORRECTION_REVIEW_2026-08-29.md
```

## Repaired first-pass acquisition — accepted truth

Historical Step-03 technical run remains superseded because it did not preserve the complete reusable dataset. Step 03R is the accepted replacement.

```text
job_id = kw001-okno-msk-wordstat-pass1-repair-20260829
frozen seeds = 18
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
raw provider items preserved = 18/18
normalized TSV artifacts present = 18/18
results rows preserved/verified = 2153
association rows preserved/verified = 262
normalized provider rows preserved/verified = 2415
Step 03R = COMPLETE
```

Per-item row totals remain:

```text
S01 218
S02 220
S03 144
S04 29
S05 215
S06 218
S07 19
S08 0
S09 13
S10 192
S11 216
S12 17
S13 216
S14 217
S15 211
S16 81
S17 49
S18 140
TOTAL = 2415
```

S01-S09 normalized TSV artifacts were repaired from already preserved raw JSON with zero additional provider calls/cost. The pre-provider S11 `COMMAND_DISCOVERY / NO_SUPPORTED_COMMAND` incident had `request_executed=false`; unchanged S11 was safely retried.

## Wordstat coverage revalidation — accepted truth

```text
complete first-pass rows = 2415
targeted probe rows = 550
P2-01 rows = 217
P2-02 rows = 216
P2-03 rows = 21
P2-04 rows = 96
probe exact matches to first pass = 17
probe rows with no exact first-pass match = 533
new provider calls during revalidation = 0
additional provider cost = 0 RUB
ACQUISITION_COVERAGE_VERDICT = SUFFICIENT
ADDITIONAL_WORDSTAT_REQUESTS_REQUIRED_NOW = 0
```

`533` remains only an exact-string comparison result; it is not a count of new topics or final keywords.

## Preserved dynamics evidence

```text
Step-06 dynamics observations = 4/4 completely preserved
24 monthly rows per root preserved
0 failed provider requests
0 outcome_unknown
estimated provider cost = 0.08 RUB
```

These data remain later prioritization/context evidence and do not replace Search/page-boundary validation.

## Row-level cleanup — historical accounting valid, historical semantic PASS superseded

The historical Step 07B artifacts remain preserved because their accounting/provenance work is valid and must remain auditable.

Input reconciliation remains valid:

```text
first-pass source rows = 2415
targeted-probe source rows = 550
TOTAL source rows = 2965
result rows = 2636
association rows = 329
```

Exact-string accounting remains valid:

```text
unique exact normalized phrases = 2840
duplicate source occurrences = 125
phrase keys with >1 source occurrence = 101
canonical provenance occurrence sum = 2965
```

Historical classifier output was:

```text
KEEP = 1760
REVIEW = 749
EXCLUDE_SCOPE = 180
EXCLUDE_IRRELEVANT = 120
EXCLUDE_MECHANICAL = 31
STATUS TOTAL = 2840
UNCLASSIFIED = 0
```

Those historical status counts are preserved for comparison only. They are not current accepted semantic truth.

The owner-requested external methodology audit found that historical result phrases could fall through to KEEP merely because no exclusion/review dictionary matched. Therefore KEEP was dependent on dictionary completeness instead of consistently requiring positive semantic relevance/user-intent evidence.

Authority for reopening:

`STEP_07B_POST_AUDIT_CORRECTION_REQUIRED_2026-08-29.md`.

## Step 07C semantic correction candidate — current truth

The same 2965 source occurrences / 2840 exact phrase keys were reprocessed without any new provider acquisition.

Current candidate accounting:

```text
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

Correction controls:

```text
KEEP requires explicit POSITIVE_* evidence tied to accepted Step-01 business/site families
default KEEP fallthrough = false
uncertain but potentially relevant -> REVIEW
low-frequency-only exclusion = false
association auto-KEEP = false
historical REVIEW/EXCLUDE rows promoted upward = 0
non-exact duplicate candidates auto-merged = 0
provider requests during correction = 0
provider cost during correction = 0 RUB
```

Semantic QA truth:

```text
builder QA cases = 21
builder QA failures = 0
expanded semantic QA cases = 72
expanded semantic QA failures = 0
manual semantic saturation passes = 4
```

Non-exact duplicate handling:

```text
candidate groups = 9
candidate rows = 18
automatic merges = 0
```

Current correction artifacts:

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

Verified candidate hashes:

```text
corrected working TSV = 753e2875d0ac4090ae4db6df4e2ecc162d6598948adeecca011b2dbdb8b60bbb
corrected occurrences TSV = 8b89585f479d6c3d42c45fcccdfe2eacebabc54adef18eb59b992628b4dff26e
non-exact duplicate candidates = f68626523ab007b58f71a4c18630547dbffa85043ee2a41c532b16ed6628bb7b
expanded semantic QA = 0fa73aee1508cd14190febdb0b5f4ea7eebfb8469db8d672771058404b20d324
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

The temporary GitHub Actions workflow used to execute/recheck the correction was removed after the final successful run. The correction builder/runner and generated evidence remain for reproducibility.

## Current operator action

No provider action is pending.

Current action is **OWNER REVIEW OF STEP 07C CORRECTION CANDIDATE**. The candidate may be accepted, rejected for another correction pass, or used to revise the next-step method. No automatic forward transition is authorized.

Blocked until owner decision and explicit correction acceptance:

```text
FINAL_WORKING_SEMANTIC_SET_FREEZE
ORDINARY_YANDEX_SEARCH_VALIDATION
PAGE_ARCHITECTURE
AI_EVIDENCE
CLIENT_DELIVERABLES
```

Still false:

```text
ROW_LEVEL_CLEANUP_COMPLETE = false
FINAL_SEMANTIC_SET_COMPLETE = false
ORDINARY_YANDEX_SEARCH_VALIDATION_COMPLETE = false
PAGE_ARCHITECTURE_COMPLETE = false
AI_EVIDENCE_COMPLETE = false
CLIENT_DELIVERABLES_COMPLETE = false
```

## Close rule

When all are true:

```text
job_work_complete = true
final_handoff_complete = true
revision_rework_open = false
provider_operator_action_pending = false
safe_to_delete = true
```

then delete the entire `tests/OKNO_MSK/` directory from the active branch.

Markers:

```text
KW001_OKNO_MSK_WORKSPACE_DISPOSABLE = true
KW001_OKNO_MSK_WORKSPACE_JOB_SPECIFIC_ONLY = true
KW001_OKNO_MSK_STEP_03_COMPLETE = true
KW001_OKNO_MSK_STEP_03R_NORMALIZED_ROWS_VERIFIED = 2415
KW001_OKNO_MSK_WORDSTAT_COVERAGE_REVALIDATION_COMPLETE = true
KW001_OKNO_MSK_WORDSTAT_COVERAGE_VERDICT_SUFFICIENT = true
KW001_OKNO_MSK_TARGETED_PROBE_ROWS_RECHECKED = 550
KW001_OKNO_MSK_ADDITIONAL_WORDSTAT_REQUESTS_REQUIRED_NOW = 0
KW001_OKNO_MSK_ROW_LEVEL_DATA_ACCOUNTING_PASS = true
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_INPUT_ROWS = 2965
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_UNIQUE_EXACT = 2840
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_DUPLICATE_OCCURRENCES = 125
KW001_OKNO_MSK_HISTORICAL_ROW_LEVEL_CLEANUP_KEEP = 1760
KW001_OKNO_MSK_HISTORICAL_ROW_LEVEL_CLEANUP_REVIEW = 749
KW001_OKNO_MSK_HISTORICAL_ROW_LEVEL_CLEANUP_EXCLUDE_SCOPE = 180
KW001_OKNO_MSK_HISTORICAL_ROW_LEVEL_CLEANUP_EXCLUDE_IRRELEVANT = 120
KW001_OKNO_MSK_HISTORICAL_ROW_LEVEL_CLEANUP_EXCLUDE_MECHANICAL = 31
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
KW001_OKNO_MSK_PROVIDER_OPERATOR_ACTION_PENDING = false
KW001_OKNO_MSK_SAFE_TO_DELETE = false
```
