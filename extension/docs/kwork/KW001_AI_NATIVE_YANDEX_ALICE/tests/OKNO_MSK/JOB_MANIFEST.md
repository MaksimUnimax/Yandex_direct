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
next_major_step = STEP_03R_COMPLETE_REMAINING_S12_S18
job_work_complete = false
final_handoff_complete = false
revision_rework_open = true
provider_operator_action_pending = true
safe_to_delete = false
```

## Authority

This directory is the complete temporary working memory and execution history for the current OKNO-MSK job.

It may contain only material specific to this job: mock/client brief, site facts/URLs, job-specific business/page model, words/phrases, provider evidence, job step plans, job flow/status/checkpoints, job-specific corrections, matrices, page/cluster decisions, deliverables, job economics/QA/revisions.

It must not define permanent universal KW-001 rules. Universal methodology lives only in the parent permanent KW-001 layer and may be changed only on explicit owner instruction.

## Current flow authority

Use `JOB_FLOW.md` for the current job sequence/status.

The Step-03 correction authority is:

```text
STEP_03_COMPLETION_CORRECTION_2026-08-29.md
```

The current repair authorities are:

```text
STEP_03R_WORDSTAT_REPAIR_MANIFEST_2026-08-29.md
STEP_03R_S01_S09_TSV_REPAIR_AUDIT_2026-08-29.md
STEP_03R_S10_CHECKPOINT_2026-08-29.md
STEP_03R_S11_PRE_PROVIDER_NO_SUPPORTED_COMMAND_2026-08-29.md
STEP_03R_S11_CHECKPOINT_2026-08-29.md
```

## Current truth

```text
historical Step-03 provider calls = 18 successful technical executions
complete historical first-pass phrase dataset preserved = false
historical Step 03 project completion = false
Step 03 repair required = true
Step 03R owner authorized = true
Step 03R manifest frozen = true
Step 03R batch.start = complete
Step 03R provider requests executed = 11
Step 03R provider outcomes known = 11
Step 03R failed_terminal = 0
Step 03R outcome_unknown = 0
Step 03R estimated provider cost = 0.22 RUB
Step 03R raw provider items preserved = 11/18
Step 03R normalized TSV artifacts present = 11/18
Step 03R results rows preserved/verified = 1326
Step 03R association rows preserved/verified = 158
Step 03R normalized rows preserved/verified = 1484
Step 03R current complete items = 11/18
Step 03R next item = S12 `аксессуары для пластиковых окон`
forward semantic analysis blocked = true
```

## S01-S09 correction state

The historical S01-S09 item checkpoints marked completion before the frozen manifest's required normalized TSV layer existed. The raw provider JSON was present, but checkpoint completion was temporally premature.

No provider item was repeated. The missing local derivative layer was repaired from the already preserved raw JSON before S10.

```text
S01 results=200 associations=18 rows=218
S02 results=200 associations=20 rows=220
S03 results=129 associations=15 rows=144
S04 results=12 associations=17 rows=29
S05 results=200 associations=15 rows=215
S06 results=200 associations=18 rows=218
S07 results=6 associations=13 rows=19
S08 results=0 associations=0 rows=0; sparse response totalCount=19; arrays absent
S09 results=3 associations=10 rows=13
TOTAL results=950
TOTAL associations=126
TOTAL rows=1076
raw rows = normalized TSV rows = verified rows = 1076
additional provider calls for repair = 0
additional provider cost for repair = 0 RUB
```

Current completion truth after repair:

```text
S01-S09 raw provider results = COMPLETE 9/9
S01-S09 normalized TSV = COMPLETE 9/9
S01-S09 row-count reconciliation = PASS
S01-S09 readable/usable preservation = PASS
S01-S09 current manifest completeness = COMPLETE
```

## S10 completion state

```text
seed = S10 `остекление веранды`
request_id = wordstat-batch-288b38ee-8019-44a1-bbeb-2eca2592b816
results rows = 176
association rows = 16
provider rows = 192
raw provider rows saved = 192
normalized TSV rows saved = 192
rows verified after read-back = 192
totalCount = 1373
estimated item cost = 0.02 RUB
NON_REPEAT_CONTROLS = PASS
S10 current manifest completeness = COMPLETE
```

Authority: `STEP_03R_S10_CHECKPOINT_2026-08-29.md`.

## S11 completion state

A pre-provider `COMMAND_DISCOVERY / NO_SUPPORTED_COMMAND` error occurred before S11. It had `request_executed=false`; therefore it did not execute a Wordstat request, did not change provider cost, and the unchanged S11 item was safe to retry.

```text
seed = S11 `алюминиевые окна`
request_id = wordstat-batch-c5589da6-f985-4acd-913d-20beda432598
results rows = 200
association rows = 16
provider rows = 216
raw provider rows saved = 216
normalized TSV rows saved = 216
rows verified after read-back = 216
totalCount = 10354
estimated item cost = 0.02 RUB
NON_REPEAT_CONTROLS = PASS
S11 current manifest completeness = COMPLETE
```

Authorities:
- `STEP_03R_S11_PRE_PROVIDER_NO_SUPPORTED_COMMAND_2026-08-29.md`
- `STEP_03R_S11_CHECKPOINT_2026-08-29.md`

## Preserved downstream observations

Step-05 provider responses:

```text
4/4 preserved completely
estimated provider cost = 0.08 RUB
```

These observations remain valid, but sufficiency of the four-probe expansion choice must be rechecked after Step-03 repair.

Step-06 dynamics responses:

```text
4/4 preserved completely
24 monthly rows per root preserved
estimated provider cost = 0.08 RUB
```

These remain usable standalone demand-history observations and do not repair Step 03.

## Current required repair

Complete remaining S12-S18 under the frozen Step-03R gate. After every individual provider call, preserve and verify:

```text
complete raw result
all results[] rows
all associations[] rows
complete normalized TSV
returned/saved/normalized row-count reconciliation
readability/usability
```

Mandatory non-repeat rule:

```text
ONE PROVIDER ITEM
→ RECEIVE FULL RESULT
→ SAVE FULL RAW RESULT
→ CREATE FULL TSV
→ COUNT RESULTS[]
→ COUNT ASSOCIATIONS[]
→ VERIFY RAW + TSV COUNTS
→ VERIFY READABLE/USABLE
→ ONLY THEN NEXT PROVIDER ITEM
```

## Current operator action

Next provider item is S12 `аксессуары для пластиковых окон`. Before issuing it, execute the required owner-facing goal/status/prior-error/YMB-mode block. Then issue exactly one Manual Wordstat `batch.next`.

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

There is no mandatory export/extraction of job lessons into permanent rules at close.

Markers:

```text
KW001_OKNO_MSK_WORKSPACE_DISPOSABLE = true
KW001_OKNO_MSK_WORKSPACE_JOB_SPECIFIC_ONLY = true
KW001_OKNO_MSK_STEP_03_COMPLETE = false
KW001_OKNO_MSK_STEP_03_REPAIR_REQUIRED = true
KW001_OKNO_MSK_STEP_03R_OWNER_AUTHORIZED = true
KW001_OKNO_MSK_STEP_03R_MANIFEST_FROZEN = true
KW001_OKNO_MSK_STEP_03R_COMPLETED_ITEMS = 11
KW001_OKNO_MSK_STEP_03R_NORMALIZED_ROWS_VERIFIED = 1484
KW001_OKNO_MSK_FORWARD_ANALYSIS_BLOCKED = true
KW001_OKNO_MSK_PROVIDER_OPERATOR_ACTION_PENDING = true
KW001_OKNO_MSK_SAFE_TO_DELETE = false
```