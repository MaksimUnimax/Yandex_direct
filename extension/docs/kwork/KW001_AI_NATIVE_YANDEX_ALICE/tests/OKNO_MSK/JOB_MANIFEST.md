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
current_major_step = WORDSTAT_COVERAGE_REVALIDATION_COMPLETE
next_major_step = ROW_LEVEL_CLEANUP
job_work_complete = false
final_handoff_complete = false
revision_rework_open = false
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
STEP_03R_S01_S09_TSV_REPAIR_AUDIT_2026-08-29.md
STEP_03R_S10_CHECKPOINT_2026-08-29.md
STEP_03R_S11_PRE_PROVIDER_NO_SUPPORTED_COMMAND_2026-08-29.md
STEP_03R_S11_CHECKPOINT_2026-08-29.md
STEP_03R_S12_CHECKPOINT_2026-08-29.md
STEP_03R_S13_CHECKPOINT_2026-08-29.md
STEP_03R_S14_CHECKPOINT_2026-08-29.md
STEP_03R_S15_CHECKPOINT_2026-08-29.md
STEP_03R_S16_CHECKPOINT_2026-08-29.md
STEP_03R_S17_CHECKPOINT_2026-08-29.md
STEP_03R_S18_CHECKPOINT_2026-08-29.md
STEP_03R_FINAL_RECONCILIATION_2026-08-29.md
STEP_04A_WORDSTAT_COVERAGE_AND_EXPANSION_REVALIDATION_2026-08-29.md
```

## Current truth — repaired first-pass acquisition

Historical Step-03 technical run remains superseded because it did not preserve the complete reusable dataset.

```text
job_id = kw001-okno-msk-wordstat-pass1-repair-20260829
frozen seeds = 18
region = 213
device = DEVICE_ALL
numPhrases = 200
execution = Manual
batch.start = COMPLETE
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
current complete items = 18/18
remaining items = 0/18
next provider item = NONE
Step 03R = COMPLETE
forward semantic analysis blocked by Step 03R = false
```

## Per-item preservation truth

```text
S01 results=200 associations=18 rows=218 COMPLETE
S02 results=200 associations=20 rows=220 COMPLETE
S03 results=129 associations=15 rows=144 COMPLETE
S04 results=12 associations=17 rows=29 COMPLETE
S05 results=200 associations=15 rows=215 COMPLETE
S06 results=200 associations=18 rows=218 COMPLETE
S07 results=6 associations=13 rows=19 COMPLETE
S08 results=0 associations=0 rows=0 COMPLETE; sparse provider response; totalCount=19; arrays absent
S09 results=3 associations=10 rows=13 COMPLETE
S10 results=176 associations=16 rows=192 COMPLETE; totalCount=1373
S11 results=200 associations=16 rows=216 COMPLETE; totalCount=10354
S12 results=4 associations=13 rows=17 COMPLETE; totalCount=29
S13 results=200 associations=16 rows=216 COMPLETE; totalCount=15510
S14 results=200 associations=17 rows=217 COMPLETE; totalCount=4382
S15 results=200 associations=11 rows=211 COMPLETE; totalCount=2023
S16 results=68 associations=13 rows=81 COMPLETE; totalCount=507
S17 results=32 associations=17 rows=49 COMPLETE; totalCount=254
S18 results=123 associations=17 rows=140 COMPLETE; totalCount=1589
TOTAL results=2153
TOTAL associations=262
TOTAL provider rows=2415
```

S01-S09 normalized TSV artifacts were repaired locally from already preserved raw JSON with zero additional provider calls and zero additional provider cost.

A pre-provider `COMMAND_DISCOVERY / NO_SUPPORTED_COMMAND` occurred before S11 with `request_executed=false`; it did not execute a Wordstat request and the unchanged S11 item was safely retried.

## Wordstat coverage revalidation — current accepted result

The complete repaired first-pass corpus was freshly reconciled against all four already preserved targeted Wordstat probes before semantic cleanup.

Probe accounting:

```text
P2-01 оконная фурнитура: results=200 associations=17 rows=217
P2-02 панорамные окна: results=200 associations=16 rows=216
P2-03 остекление балкона с выносом: results=5 associations=16 rows=21
P2-04 окна для частного дома: results=78 associations=18 rows=96
TOTAL targeted probe results=483
TOTAL targeted probe associations=67
TOTAL targeted probe rows=550
```

Exact normalized phrase comparison against the complete 2415-row first pass:

```text
P2-01 exact base matches=2; nonmatching rows=215
P2-02 exact base matches=7; nonmatching rows=209
P2-03 exact base matches=3; nonmatching rows=18
P2-04 exact base matches=5; nonmatching rows=91
TOTAL exact base matches=17
TOTAL probe rows with no exact base match=533
```

`533` means rows that do not exactly match a first-pass phrase. It is not a claim of 533 new semantic topics or 533 cross-probe-unique phrases.

Fresh coverage verdict:

```text
ACQUISITION_COVERAGE_VERDICT = SUFFICIENT
ADDITIONAL_WORDSTAT_REQUESTS_REQUIRED_NOW = 0
ADDITIONAL_PROVIDER_COST_RUB = 0
ROW_LEVEL_CLEANUP_ALLOWED = true
FINAL_SEMANTIC_SET_COMPLETE = false
PAGE_ARCHITECTURE_COMPLETE = false
```

The four probes materially filled/confirmed the intended acquisition directions: window hardware language, broader panoramic applications, the narrow balcony-extension engineering family, and private-house window demand. Deferred broad roots are either already represented sufficiently for acquisition or are better resolved by row-level cleanup, business scope, or ordinary Yandex Search rather than another Wordstat call.

## Preserved dynamics evidence

```text
Step-06 dynamics observations = 4/4 completely preserved
24 monthly rows per root preserved
0 failed provider requests
0 outcome_unknown
estimated provider cost = 0.08 RUB
```

These data remain usable standalone evidence, but they do not replace row-level cleanup or Search/page-boundary validation.

## Current operator action

No provider action is pending.

The next major step is **ROW_LEVEL_CLEANUP**: account for every collected source row, deduplicate where appropriate, and assign explicit KEEP / REVIEW / EXCLUDE_IRRELEVANT / EXCLUDE_SCOPE / EXCLUDE_MECHANICAL decisions/reasons without deleting phrases solely because they are low-frequency.

That next major step requires its own mandatory whole-goal/completed/remaining/prior-errors/current-step/method-review block and owner authorization before execution.

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
KW001_OKNO_MSK_STEP_03_REPAIR_REQUIRED = false
KW001_OKNO_MSK_STEP_03R_COMPLETED_ITEMS = 18
KW001_OKNO_MSK_STEP_03R_NORMALIZED_ROWS_VERIFIED = 2415
KW001_OKNO_MSK_WORDSTAT_COVERAGE_REVALIDATION_COMPLETE = true
KW001_OKNO_MSK_WORDSTAT_COVERAGE_VERDICT_SUFFICIENT = true
KW001_OKNO_MSK_TARGETED_PROBE_ROWS_RECHECKED = 550
KW001_OKNO_MSK_TARGETED_PROBE_EXACT_BASE_MATCHES = 17
KW001_OKNO_MSK_TARGETED_PROBE_ROWS_NO_EXACT_BASE_MATCH = 533
KW001_OKNO_MSK_ADDITIONAL_WORDSTAT_REQUESTS_REQUIRED_NOW = 0
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_ALLOWED = true
KW001_OKNO_MSK_PROVIDER_OPERATOR_ACTION_PENDING = false
KW001_OKNO_MSK_SAFE_TO_DELETE = false
```