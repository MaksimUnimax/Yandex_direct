# KW-001 / OKNO-MSK — JOB FLOW

Date created: 2026-08-28  
Last updated: 2026-08-29  
Status: **ACTIVE / JOB-SPECIFIC / DISPOSABLE WITH WORKSPACE**

This file tracks only the execution flow of the current OKNO-MSK rehearsal.

It is not a universal KW-001 methodology document and must be deleted together with the entire job workspace after job close.

---

## Current job sequence

### Step 0 — mock order / scope freeze

Status: **COMPLETE**

Job-specific outputs include the frozen test order and client/open-question assumptions.

---

### Step 1 — existing-site discovery / merged business-page model

Status: **COMPLETE / PASS AFTER CROSS-CHANNEL REWORK**

Job-specific outputs include:

```text
site inventories
cross-channel discovery crosscheck
merged site inventory
merged business/page model
Step-01 acceptance
```

---

### Step 2 — first-pass Wordstat seed/query plan

Status: **COMPLETE / FROZEN**

Job-specific output:

```text
18 frozen pass-1 seeds
region/device/request controls
second-pass reason-code framework
Step-02 acceptance
```

---

### Step 3 — Wordstat pass #1 acquisition

Status: **COMPLETE / PASS**

Final job facts:

```text
18/18 succeeded
0 failed_terminal
0 outcome_unknown
18 provider requests
0.36 RUB estimated provider cost
region = 213
DEVICE_ALL
```

Job-specific raw/checkpoint/provider evidence remains inside this workspace.

---

### Step 4 — first post-Wordstat family-level triage

Status: **COMPLETE AFTER RETROSPECTIVE CORRECTION / RE-FROZEN**

What this job actually completed:

```text
family-level triage across the 18 pass-1 result families
review/ambiguity preservation
exclusion-class correction
pass-2 probe candidate reclassification
```

What remains incomplete:

```text
full row-level cleanup
final semantic core
clustering
SERP validation
page mapping
```

Current authoritative job files:

```text
STEP_04_PROGRESSIVE_CLEANUP_1.md
STEP_04_METHOD_REVIEW_CORRECTION.md
STEP_04_ACCEPTANCE.md
```

---

### Step 5 — targeted Wordstat expansion pass #2

Status: **COMPLETE / PASS / ACQUISITION FROZEN**

Pre-step and manifest authority:

```text
STEP_05_PRE_STEP_REVIEW.md
STEP_05_WORDSTAT_PASS2_MANIFEST.md
```

Executed manifest:

```text
P2-01 оконная фурнитура
P2-02 панорамные окна
P2-03 остекление балкона с выносом
P2-04 окна для частного дома
```

Frozen provider controls actually used:

```text
job_id = kw001-okno-msk-wordstat-pass2-20260828
method = getTop
regions = ["213"]
devices = ["DEVICE_ALL"]
numPhrases = 200
maxRequests = 4
```

Final durable batch truth:

```text
status = COMPLETED
total = 4
succeeded = 4
failed_terminal = 0
outcome_unknown = 0
requests_started = 4
estimated_cost_rub = 0.08
next_safe_action = NONE
```

Complete normalized provider rows are preserved inside the job workspace:

```text
STEP_05_P2_01_RAW_NORMALIZED.tsv
STEP_05_P2_02_RAW_NORMALIZED.tsv
STEP_05_P2_03_RAW_NORMALIZED.tsv
STEP_05_P2_04_RAW_NORMALIZED.tsv
```

Execution/control authority:

```text
STEP_05_P2_01_CHECKPOINT.md
STEP_05_P2_02_CHECKPOINT.md
STEP_05_P2_03_CHECKPOINT.md
STEP_05_P2_04_CHECKPOINT.md
STEP_05_FINAL_BATCH_STATUS.md
STEP_05_ACCEPTANCE.md
```

Step-05 acquisition findings remain evidence only. Final row-level semantic decisions, clustering, page mapping and SERP validation are still not complete.

No third recursive Wordstat pass is authorized by Step 05.

---

## Next major step

Status: **NOT STARTED / PRE-STEP REVIEW REQUIRED**

The next major job step is not automatically authorized by Step-05 acceptance.

Before execution:

```text
read current job evidence
explain the proposed next step
check current external/official methodology where relevant
adversarially review Step-05 handoff
show owner sources/risks
wait for explicit owner authorization
```

No provider/operator action is currently pending.

---

## Later job stages

Later stages may include, subject to their own pre-step review and owner authorization:

```text
row-level semantic cleanup/freeze
selective demand/dynamics checks if independently justified
ordinary Yandex Search evidence
SERP clustering/page-boundary analysis
page mapping
selective AI evidence
Search-vs-AI comparison
final architecture/priorities
client deliverables
QA/economics/revision
job close
```

The exact current-job sequence may be refined during authorized pre-step reviews, but any such refinement belongs only to this job unless the owner explicitly changes universal KW-001 methodology.

---

## Close

When the current job is fully completed and handed off:

```text
mark JOB_MANIFEST safe_to_delete = true
then delete this entire OKNO_MSK workspace, including JOB_FLOW.md itself
```

Marker:

```text
KW001_OKNO_MSK_JOB_FLOW_ACTIVE = true
KW001_OKNO_MSK_STEP_05_COMPLETE = true
KW001_OKNO_MSK_NEXT_STEP_NOT_STARTED = true
```
