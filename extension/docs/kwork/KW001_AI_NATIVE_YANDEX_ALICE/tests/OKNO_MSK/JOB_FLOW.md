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

Job-specific outputs include site inventories, cross-channel discovery crosscheck, merged site inventory, merged business/page model and Step-01 acceptance.

---

### Step 2 — first-pass Wordstat seed/query plan

Status: **COMPLETE / FROZEN**

Job-specific output includes 18 frozen pass-1 seeds, region/device/request controls, second-pass reason-code framework and Step-02 acceptance.

---

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

---

### Step 4 — first post-Wordstat family-level triage

Status: **COMPLETE AFTER RETROSPECTIVE CORRECTION / RE-FROZEN**

Completed: family-level triage, ambiguity preservation, exclusion-class correction and pass-2 probe candidate reclassification.

Still incomplete after this step: full row-level cleanup, final semantic core, clustering, SERP validation and page mapping.

---

### Step 5 — targeted Wordstat expansion pass #2

Status: **COMPLETE / PASS / ACQUISITION FROZEN**

Executed:

```text
P2-01 оконная фурнитура
P2-02 панорамные окна
P2-03 остекление балкона с выносом
P2-04 окна для частного дома
```

Final durable truth:

```text
status = COMPLETED
succeeded = 4
failed_terminal = 0
outcome_unknown = 0
requests_started = 4
estimated_cost_rub = 0.08
next_safe_action = NONE
```

Complete normalized provider rows are preserved in the Step-05 raw TSV files.

---

### Step 6 — selective Wordstat dynamics / seasonality diagnostic

Status: **OWNER AUTHORIZED / MANIFEST FROZEN / READY FOR D1**

Authorities:

```text
STEP_06_PRE_STEP_REVIEW.md
STEP_06_DYNAMICS_MANIFEST.md
```

Frozen common controls:

```text
method = getDynamics
period = PERIOD_MONTHLY
fromDate = 2024-08-01T00:00:00Z
toDate = 2026-07-31T23:59:59Z
regions = ["213"]
devices = ["DEVICE_ALL"]
provider_request_ceiling = 4
estimated total cost = 0.08 RUB
```

Frozen request order:

```text
D1 пластиковые окна
D2 остекление балконов
D3 остекление веранды
D4 окна для частного дома
```

No Step-06 provider request had been made at manifest freeze. The next owner-operated action is D1.

Step 06 is context for later prioritization only. It does not decide semantic relevance, clusters or pages.

---

## Later job stages

Later stages remain blocked until Step 06 is completed and separately accepted. They may include row-level semantic cleanup/freeze, ordinary Yandex Search evidence, SERP clustering/page-boundary analysis, page mapping, selective AI evidence, Search-vs-AI comparison, final architecture/priorities, client deliverables, QA/economics/revision and job close.

---

## Close

When the current job is fully completed and handed off:

```text
mark JOB_MANIFEST safe_to_delete = true
then delete this entire OKNO_MSK workspace, including JOB_FLOW.md itself
```

Markers:

```text
KW001_OKNO_MSK_JOB_FLOW_ACTIVE = true
KW001_OKNO_MSK_STEP_05_COMPLETE = true
KW001_OKNO_MSK_STEP_06_MANIFEST_FROZEN = true
KW001_OKNO_MSK_STEP_06_PROVIDER_EXECUTION_STARTED = false
```
