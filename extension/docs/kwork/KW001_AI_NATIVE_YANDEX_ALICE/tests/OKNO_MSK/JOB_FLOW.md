# KW-001 / OKNO-MSK — JOB FLOW

Date created: 2026-08-28  
Last updated: 2026-08-29  
Status: **ACTIVE / JOB-SPECIFIC / DISPOSABLE WITH WORKSPACE**

This file tracks only the execution flow of the current OKNO-MSK rehearsal. It is not a universal KW-001 methodology document and must be deleted with the job workspace after close.

---

## Current job sequence

### Step 0 — mock order / scope freeze

Status: **COMPLETE**

### Step 1 — existing-site discovery / merged business-page model

Status: **COMPLETE / PASS AFTER CROSS-CHANNEL REWORK**

### Step 2 — first-pass Wordstat seed/query plan

Status: **COMPLETE / FROZEN**

### Step 3 — Wordstat pass #1 acquisition

Status: **COMPLETE / PASS**

```text
18/18 succeeded
0 failed_terminal
0 outcome_unknown
18 provider requests
0.36 RUB estimated provider cost
region = 213
DEVICE_ALL
```

### Step 4 — first post-Wordstat family-level triage

Status: **COMPLETE AFTER RETROSPECTIVE CORRECTION / RE-FROZEN**

Completed: family-level triage, ambiguity preservation, exclusion-class correction and pass-2 probe candidate reclassification.

Still incomplete after this step: full row-level cleanup, final semantic core, clustering, SERP validation and page mapping.

### Step 5 — targeted Wordstat expansion pass #2

Status: **COMPLETE / PASS / ACQUISITION FROZEN**

```text
4/4 succeeded
0 failed_terminal
0 outcome_unknown
4 provider requests
0.08 RUB estimated provider cost
```

Complete normalized provider rows are preserved in the Step-05 raw TSV files.

### Step 6 — selective Wordstat dynamics / historical-demand diagnostic

Status: **COMPLETE / PASS / DYNAMICS EVIDENCE FROZEN**

Authorities:

```text
STEP_06_PRE_STEP_REVIEW.md
STEP_06_DYNAMICS_MANIFEST.md
STEP_06_DYNAMICS_SYNTHESIS.md
STEP_06_ACCEPTANCE.md
```

Executed roots:

```text
D1 пластиковые окна
D2 остекление балконов
D3 остекление веранды
D4 окна для частного дома
```

Frozen controls actually used:

```text
method = getDynamics
period = PERIOD_MONTHLY
fromDate = 2024-08-01T00:00:00Z
toDate = 2026-07-31T23:59:59Z
regions = ["213"]
devices = ["DEVICE_ALL"]
```

Provider truth:

```text
successful provider requests = 4
failed provider requests = 0
outcome_unknown = 0
estimated provider cost = 0.08 RUB
```

One recoverable local delivery incident occurred before D2:

```text
SEND_BUTTON_NOT_READY
request_executed = false
```

The unchanged D2 command was safely replayed and then succeeded.

All four 24-month series are preserved in raw TSV files. Comparative evidence does not support treating variation as stable seasonality alone; all four roots are currently classified descriptively as `TREND_OR_STRUCTURAL_CHANGE_POSSIBLE`. Cause is unresolved and must not be invented.

Step 06 changes only later demand-magnitude interpretation. It does not decide semantic relevance, clustering or pages.

---

## Next major step

Status: **NOT STARTED / PRE-STEP REVIEW REQUIRED**

Before any next analytical or provider stage:

```text
read current job evidence
explain proposed next step and why it is needed
check current external/official methodology where relevant
adversarially review the handoff
show sources, risks and what will not be done
wait for explicit owner authorization
```

No provider/operator action is currently pending.

Candidate later work includes full row-level semantic cleanup/freeze, ordinary Yandex Search evidence, SERP clustering/page-boundary analysis, page mapping, selective AI evidence, Search-vs-AI comparison, architecture/priorities, client deliverables and QA.

---

## Close

When the job is fully completed and handed off:

```text
mark JOB_MANIFEST safe_to_delete = true
then delete the entire OKNO_MSK workspace
```

Markers:

```text
KW001_OKNO_MSK_JOB_FLOW_ACTIVE = true
KW001_OKNO_MSK_STEP_05_COMPLETE = true
KW001_OKNO_MSK_STEP_06_COMPLETE = true
KW001_OKNO_MSK_NEXT_STEP_NOT_STARTED = true
```
