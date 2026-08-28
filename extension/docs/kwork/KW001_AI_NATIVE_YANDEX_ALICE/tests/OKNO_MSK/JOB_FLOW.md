# KW-001 / OKNO-MSK — JOB FLOW

Date created: 2026-08-28  
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

Status: **OWNER AUTHORIZED / MANIFEST FROZEN / READY FOR BATCH START**

Pre-step review authority:

```text
STEP_05_PRE_STEP_REVIEW.md
```

Frozen execution authority:

```text
STEP_05_WORDSTAT_PASS2_MANIFEST.md
```

Frozen manifest:

```text
P2-01 оконная фурнитура
P2-02 панорамные окна
P2-03 остекление балкона с выносом
P2-04 окна для частного дома
```

Frozen provider controls:

```text
job_id = kw001-okno-msk-wordstat-pass2-20260828
method = getTop
regions = ["213"]
devices = ["DEVICE_ALL"]
numPhrases = 200
maxRequests = 4
estimated max provider cost = 0.08 RUB
```

Deferred from provider execution because of redundancy, ambiguity or unresolved business boundary:

```text
остекление террасы
панорамное остекление балкона
монтаж окон
регулировка окон пвх
москитные сетки на пластиковые окна
окна пвх
стеклопакет
оконный завод
```

No Step-5 provider request had been made at manifest freeze. Next action is the owner-operated durable batch start, followed by one `batch.next` per frozen probe and a final `batch.status`.

---

## Later job stages

Later steps will be appended here as this concrete job progresses.

They may include, as authorized by the universal KW-001 workflow:

```text
row-level semantic cleanup/freeze
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
```
