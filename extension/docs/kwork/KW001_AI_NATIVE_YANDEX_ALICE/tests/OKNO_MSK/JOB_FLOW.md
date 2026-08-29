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
Status: **INCOMPLETE / HISTORICAL ACCEPTANCE SUPERSEDED / REPAIR REQUIRED**

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
complete results[] + associations[] preserved for all 18 seeds = false
Step 03 complete = false
forward analytical work allowed = false
```

Authority:

`STEP_03_COMPLETION_CORRECTION_2026-08-29.md`

The historical `STEP_03_ACCEPTANCE.md` remains in the folder as evidence of the earlier incorrect gate, but its PASS verdict no longer controls current status.

### Step 4 — first post-Wordstat family-level triage
Status: **HISTORICAL PARTIAL ANALYSIS ONLY / NOT A COMPLETE PASS-1 CLEANUP**

The earlier family-level observations may be reused as notes, but the step cannot represent processing of a complete Step-03 dataset because that dataset was not preserved.

## Current next step

### Step 3R — repair the original 18-seed Wordstat collection
Status: **PRE-STEP METHOD REVIEW IN PROGRESS / PROVIDER EXECUTION NOT STARTED**

Goal:

Collect the exact original 18 Wordstat `getTop` observations again and preserve every returned row before allowing the next request.

Required per-provider-item gate:

```text
provider outcome known
exact full result envelope saved
all results[] rows saved
all associations[] rows saved
returned results count verified
returned associations count verified
saved rows = results.length + associations.length
saved data readable and usable
```

If any check fails:

```text
current item = INCOMPLETE
next provider request = BLOCKED
next analytical step = BLOCKED
```

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
KW001_OKNO_MSK_FORWARD_ANALYSIS_BLOCKED = true
KW001_OKNO_MSK_STEP_05_RAW_PROVIDER_EVIDENCE_PRESERVED = true
KW001_OKNO_MSK_STEP_06_RAW_PROVIDER_EVIDENCE_PRESERVED = true
```
