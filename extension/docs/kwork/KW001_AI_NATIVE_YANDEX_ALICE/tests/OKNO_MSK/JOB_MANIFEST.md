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
current_major_step = STEP_03R_MANUAL_YMB_EXECUTION_IN_PROGRESS
next_major_step = STEP_03R_COMPLETE_REMAINING_S17_S18
job_work_complete = false
final_handoff_complete = false
revision_rework_open = true
provider_operator_action_pending = true
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
```

## Current truth

Historical Step-03 technical run remains superseded because it did not preserve the complete reusable dataset.

Current Step-03R repair truth:

```text
job_id = kw001-okno-msk-wordstat-pass1-repair-20260829
frozen seeds = 18
region = 213
device = DEVICE_ALL
numPhrases = 200
execution = Manual
batch.start = COMPLETE
provider requests executed = 16
provider outcomes known = 16
failed_terminal = 0
outcome_unknown = 0
estimated provider cost = 0.32 RUB
raw provider items preserved = 16/18
normalized TSV artifacts present = 16/18
results rows preserved/verified = 1998
association rows preserved/verified = 228
normalized provider rows preserved/verified = 2226
current complete items = 16/18
remaining items = 2/18
next item = S17 `как выбрать пластиковые окна`
forward semantic analysis blocked = true
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
TOTAL results=1998
TOTAL associations=228
TOTAL provider rows=2226
```

S01-S09 normalized TSV artifacts were repaired locally from already preserved raw JSON with zero additional provider calls and zero additional provider cost.

A pre-provider `COMMAND_DISCOVERY / NO_SUPPORTED_COMMAND` occurred before S11 with `request_executed=false`; it did not execute a Wordstat request and the unchanged S11 item was safely retried.

## Mandatory non-repeat gate

```text
ONE PROVIDER ITEM
→ RECEIVE FULL RESULT
→ SAVE COMPLETE RAW RESULT
→ CREATE COMPLETE TSV
→ COUNT results[]
→ COUNT associations[]
→ VERIFY RAW + TSV COUNTS
→ VERIFY READABLE/USABLE
→ ONLY THEN NEXT PROVIDER ITEM
```

If any current item fails this gate:

```text
CURRENT_ITEM = INCOMPLETE
NEXT_PROVIDER_ITEM = BLOCKED
FORWARD_ANALYSIS = BLOCKED
```

## Preserved downstream observations

```text
Step-05 targeted Wordstat probes = 4/4 completely preserved; estimated cost 0.08 RUB
Step-06 dynamics observations = 4/4 completely preserved; 24 monthly rows per root; estimated cost 0.08 RUB
```

Their provider data remain usable, but their analytical sufficiency must be rechecked after Step 03R reaches 18/18.

## Current operator action

Next provider item is S17 `как выбрать пластиковые окна`. Before issuing it, execute the required owner-facing whole-goal/status/prior-error/current-step/YMB-mode block. Then issue exactly one Manual Wordstat `batch.next`.

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
KW001_OKNO_MSK_STEP_03_COMPLETE = false
KW001_OKNO_MSK_STEP_03_REPAIR_REQUIRED = true
KW001_OKNO_MSK_STEP_03R_OWNER_AUTHORIZED = true
KW001_OKNO_MSK_STEP_03R_MANIFEST_FROZEN = true
KW001_OKNO_MSK_STEP_03R_COMPLETED_ITEMS = 16
KW001_OKNO_MSK_STEP_03R_NORMALIZED_ROWS_VERIFIED = 2226
KW001_OKNO_MSK_FORWARD_ANALYSIS_BLOCKED = true
KW001_OKNO_MSK_PROVIDER_OPERATOR_ACTION_PENDING = true
KW001_OKNO_MSK_SAFE_TO_DELETE = false
```