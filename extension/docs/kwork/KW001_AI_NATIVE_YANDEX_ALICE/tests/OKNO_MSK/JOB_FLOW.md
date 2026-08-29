# KW-001 / OKNO-MSK — JOB FLOW

Date created: 2026-08-28
Last updated: 2026-08-29
Status: **ACTIVE / JOB-SPECIFIC / DISPOSABLE WITH WORKSPACE**

This file tracks only the execution flow of the current OKNO-MSK rehearsal. It is not a universal KW-001 methodology document and must be deleted with the job workspace after close.

## Whole Kwork goal

Deliver a complete, evidence-backed semantic set and site/page structure recommendation for Yandex human search plus selective Yandex AI-search evidence, with client-ready artifacts and final QA.

## Already genuinely completed

### Step 0 — mock order / scope freeze
Status: **COMPLETE**

### Step 1 — existing-site discovery / merged business-page model
Status: **COMPLETE / PASS AFTER CROSS-CHANNEL REWORK**

### Step 2 — first-pass Wordstat seed/query plan
Status: **COMPLETE / FROZEN**

The frozen 18 seeds remain the required input for the Step-03 repair.

### Step 5 provider evidence — targeted Wordstat expansion pass #2
Status of the four provider observations themselves: **PRESERVED COMPLETELY**

```text
4/4 provider responses preserved
0 failed_terminal
0 outcome_unknown
4 provider requests
0.08 RUB estimated provider cost
```

Complete normalized provider rows are preserved in the Step-05 raw TSV files.

Important limitation: because Step 03 was not completely preserved, the claim that these four probes were sufficient expansion coverage must be rechecked after Step-03 repair.

### Step 6 provider evidence — selective Wordstat dynamics
Status of the four dynamics observations themselves: **PRESERVED COMPLETELY**

```text
4/4 provider responses preserved
24 monthly rows per root preserved
0 failed provider requests
0 outcome_unknown
0.08 RUB estimated provider cost
```

These observations remain usable standalone evidence, but they do not repair the missing Step-03 phrase dataset.

## Work that is NOT complete

### Step 3 — Wordstat pass #1 acquisition
Status: **INCOMPLETE / HISTORICAL ACCEPTANCE SUPERSEDED / REPAIR IN PROGRESS**

Historical technical truth:

```text
18 provider calls executed
18 provider calls reported success
0 failed_terminal
0 outcome_unknown
0.36 RUB estimated provider cost
region = 213
device = DEVICE_ALL
```

Project-completion truth:

```text
complete historical results[] + associations[] preserved for all 18 seeds = false
historical Step 03 complete = false
Step 03R repair required = true
forward analytical work allowed = false
```

Authority:

`STEP_03_COMPLETION_CORRECTION_2026-08-29.md`

The historical `STEP_03_ACCEPTANCE.md` remains in the folder as evidence of the earlier incorrect gate, but its PASS verdict no longer controls current status.

### Step 4 — first post-Wordstat family-level triage
Status: **HISTORICAL PARTIAL ANALYSIS ONLY / NOT A COMPLETE PASS-1 CLEANUP**

The earlier family-level observations may be reused as notes, but the step cannot represent processing of a complete Step-03 dataset because that dataset was not preserved.

## Current step

### Step 3R — repair the original 18-seed Wordstat collection
Status: **IN PROGRESS / 11 OF 18 PROVIDER ITEMS CURRENTLY COMPLETE**

Authority:

```text
STEP_03R_WORDSTAT_REPAIR_MANIFEST_2026-08-29.md
STEP_03R_S01_S09_TSV_REPAIR_AUDIT_2026-08-29.md
STEP_03R_S10_CHECKPOINT_2026-08-29.md
STEP_03R_S11_PRE_PROVIDER_NO_SUPPORTED_COMMAND_2026-08-29.md
STEP_03R_S11_CHECKPOINT_2026-08-29.md
```

Goal:

Collect the exact original 18 Wordstat `getTop` observations again and preserve every returned row before allowing the next request.

Past Step-3 error was reread and reported to the owner before method research/execution. The active non-repeat control is save-and-verify-complete-result-before-next-item.

Required per-provider-item gate:

```text
provider outcome known
exact full raw result saved
all results[] rows saved
all associations[] rows saved
complete normalized TSV created
returned/saved/normalized row counts reconciled
raw + TSV readable and usable
NON_REPEAT_CONTROLS = PASS
```

If any check fails:

```text
current item = INCOMPLETE
next provider request = BLOCKED
next analytical step = BLOCKED
```

Frozen execution:

```text
job_id = kw001-okno-msk-wordstat-pass1-repair-20260829
18 exact Step-02 seeds
region = 213
device = DEVICE_ALL
numPhrases = 200
maxRequests = 18
estimated provider cost = 0.36 RUB
execution = Manual
```

### Current execution point after S11

```text
batch.start = COMPLETE
provider requests in Step 03R = 11
provider outcomes known = 11
failed_terminal = 0
outcome_unknown = 0
estimated provider cost = 0.22 RUB
fully preserved + normalized + verified Step-03R provider items = 11/18
provider items remaining = 7
results rows preserved/verified S01-S11 = 1326
association rows preserved/verified S01-S11 = 158
total provider rows preserved/verified S01-S11 = 1484
next provider item = S12 `аксессуары для пластиковых окон`
next YMB action = one manual batch.next only after pre-item goal/error/mode block
forward analytical work = BLOCKED until Step 03R reaches 18/18 and final reconciliation passes
```

### S01-S09 local correction

The original S01-S09 checkpoints were temporally premature under the frozen manifest because normalized TSV files were not yet present. No provider calls were repeated.

Local repair completed before S10:

```text
S01-S09 raw provider JSON = 9/9 present
S01-S09 normalized TSV = 9/9 present
results rows = 950
association rows = 126
total normalized rows = 1076
raw rows = normalized rows = verified rows = 1076
additional provider calls = 0
additional provider cost = 0 RUB
```

Current correction authority:

`STEP_03R_S01_S09_TSV_REPAIR_AUDIT_2026-08-29.md`

### S10 verified acquisition

```text
S10 = остекление веранды
results rows = 176
association rows = 16
provider rows = 192
raw rows saved = 192
normalized TSV rows = 192
rows verified after read-back = 192
totalCount = 1373
NON_REPEAT_CONTROLS = PASS
```

Authority: `STEP_03R_S10_CHECKPOINT_2026-08-29.md`.

### S11 verified acquisition

A manual command-discovery failure happened immediately before S11, but it had `request_executed=false`, so no provider request was made by that failed interaction and the unchanged S11 item was safely retried.

```text
S11 = алюминиевые окна
results rows = 200
association rows = 16
provider rows = 216
raw rows saved = 216
normalized TSV rows = 216
rows verified after read-back = 216
totalCount = 10354
NON_REPEAT_CONTROLS = PASS
```

Authorities:
- `STEP_03R_S11_PRE_PROVIDER_NO_SUPPORTED_COMMAND_2026-08-29.md`
- `STEP_03R_S11_CHECKPOINT_2026-08-29.md`

## Remaining work after Step 3R succeeds

1. Review the complete first-pass dataset and determine whether any additional important acquisition direction was missed.
2. Clean the complete collected phrase set while preserving ambiguous items for later checking.
3. Freeze the working semantic set.
4. Validate important query/page boundaries in ordinary Yandex Search.
5. Group queries by user task and determine page ownership/actions.
6. Select only material uncertain cases for Yandex AI-search evidence.
7. Compare ordinary Search and AI evidence.
8. Prioritize actions.
9. Produce client deliverables.
10. Run final QA and revision gate.

## Close

When the job is fully completed and handed off:

```text
mark JOB_MANIFEST safe_to_delete = true
then delete the entire OKNO_MSK workspace
```

Markers:

```text
KW001_OKNO_MSK_JOB_FLOW_ACTIVE = true
KW001_OKNO_MSK_STEP_03_COMPLETE = false
KW001_OKNO_MSK_STEP_03_REPAIR_REQUIRED = true
KW001_OKNO_MSK_STEP_03R_OWNER_AUTHORIZED = true
KW001_OKNO_MSK_STEP_03R_MANIFEST_FROZEN = true
KW001_OKNO_MSK_STEP_03R_PROVIDER_ITEMS_PRESERVED = 11
KW001_OKNO_MSK_STEP_03R_NORMALIZED_ROWS_VERIFIED = 1484
KW001_OKNO_MSK_FORWARD_ANALYSIS_BLOCKED = true
KW001_OKNO_MSK_STEP_05_RAW_PROVIDER_EVIDENCE_PRESERVED = true
KW001_OKNO_MSK_STEP_06_RAW_PROVIDER_EVIDENCE_PRESERVED = true
```