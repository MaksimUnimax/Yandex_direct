# KW-001 / OKNO-MSK — JOB FLOW

Date created: 2026-08-28
Last updated: 2026-08-29
Status: **ACTIVE / JOB-SPECIFIC / DISPOSABLE WITH WORKSPACE**

## Whole Kwork goal

Deliver a complete, evidence-backed semantic set and site/page structure recommendation for Yandex human search plus selective Yandex AI-search evidence, with client-ready artifacts and final QA.

## Genuinely complete

### Step 0 — mock order / scope freeze
Status: **COMPLETE**

### Step 1 — existing-site discovery / merged business-page model
Status: **COMPLETE / PASS AFTER CROSS-CHANNEL REWORK**

### Step 2 — first-pass Wordstat seed/query plan
Status: **COMPLETE / FROZEN**

Frozen input remains the original 18 seeds.

### Preserved Step-05 evidence

```text
4/4 targeted Wordstat provider responses completely preserved
0 failed_terminal
0 outcome_unknown
estimated provider cost = 0.08 RUB
```

Sufficiency of those four probes must be rechecked after the repaired first-pass dataset is complete.

### Preserved Step-06 evidence

```text
4/4 dynamics provider observations completely preserved
24 monthly rows per root preserved
0 failed provider requests
0 outcome_unknown
estimated provider cost = 0.08 RUB
```

These data remain usable standalone evidence but do not substitute for Step 03R.

## Historical Step 3

Status: **INCOMPLETE / HISTORICAL ACCEPTANCE SUPERSEDED**

Historical technical truth:

```text
18 provider calls executed
18 provider calls reported success
0 failed_terminal
0 outcome_unknown
estimated provider cost = 0.36 RUB
```

Project truth:

```text
complete historical results[] + associations[] preserved for all 18 seeds = false
historical Step 03 project completion = false
Step 03R repair required = true
```

Authority: `STEP_03_COMPLETION_CORRECTION_2026-08-29.md`.

## Current step — Step 03R

Status: **IN PROGRESS / 16 OF 18 PROVIDER ITEMS COMPLETE**

Goal: recollect the exact original 18 Wordstat `getTop` observations and preserve every required row before the next provider request.

Authorities:

```text
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

Frozen execution:

```text
job_id = kw001-okno-msk-wordstat-pass1-repair-20260829
region = 213
device = DEVICE_ALL
numPhrases = 200
maxRequests = 18
max estimated provider cost = 0.36 RUB
execution = Manual
```

Mandatory per-item gate:

```text
provider outcome known
complete raw provider result saved
all results[] saved
all associations[] saved when present
complete normalized TSV created
returned = saved = normalized = verified rows
raw + TSV readable/usable
NON_REPEAT_CONTROLS = PASS
```

### Current execution point after S16

```text
provider requests executed = 16
provider outcomes known = 16
failed_terminal = 0
outcome_unknown = 0
estimated provider cost = 0.32 RUB
fully preserved + normalized + verified = 16/18
remaining = 2/18
results rows preserved/verified = 1998
association rows preserved/verified = 228
total provider rows preserved/verified = 2226
next provider item = S17 `как выбрать пластиковые окна`
forward analytical work = BLOCKED until 18/18 and final reconciliation PASS
```

### Item accounting

```text
S01 200+18=218 COMPLETE
S02 200+20=220 COMPLETE
S03 129+15=144 COMPLETE
S04 12+17=29 COMPLETE
S05 200+15=215 COMPLETE
S06 200+18=218 COMPLETE
S07 6+13=19 COMPLETE
S08 0+0=0 COMPLETE; sparse response, totalCount=19, arrays absent
S09 3+10=13 COMPLETE
S10 176+16=192 COMPLETE
S11 200+16=216 COMPLETE
S12 4+13=17 COMPLETE
S13 200+16=216 COMPLETE
S14 200+17=217 COMPLETE
S15 200+11=211 COMPLETE
S16 68+13=81 COMPLETE
TOTAL = 1998 results + 228 associations = 2226 rows
```

S01-S09 missing TSV artifacts were repaired locally from already preserved raw JSON before S10, with zero new provider calls and zero additional cost.

Before S11 a `COMMAND_DISCOVERY / NO_SUPPORTED_COMMAND` happened with `request_executed=false`; therefore no Wordstat request was executed by that failed interaction and S11 was safely retried unchanged.

## Remaining work after Step 03R succeeds

1. Reconcile all 18 first-pass datasets and the four already preserved targeted expansion datasets; identify any materially missing acquisition direction.
2. Clean every collected phrase with explicit counts for duplicates, irrelevant, out-of-scope, uncertain and retained rows.
3. Freeze the final working semantic set.
4. Validate important query/page boundaries in ordinary Yandex Search.
5. Group by user task and decide page ownership/actions.
6. Select only material uncertain cases for AI-search evidence; use Webmaster Alice visibility if access exists, otherwise a small GenSearch set.
7. Compare ordinary Search and AI evidence.
8. Prioritize actions.
9. Produce client deliverables.
10. Run final QA and revision gate.

## Close

When the job is fully completed and handed off, mark `JOB_MANIFEST safe_to_delete = true`, then delete this whole OKNO_MSK workspace.

Markers:

```text
KW001_OKNO_MSK_JOB_FLOW_ACTIVE = true
KW001_OKNO_MSK_STEP_03_COMPLETE = false
KW001_OKNO_MSK_STEP_03_REPAIR_REQUIRED = true
KW001_OKNO_MSK_STEP_03R_OWNER_AUTHORIZED = true
KW001_OKNO_MSK_STEP_03R_MANIFEST_FROZEN = true
KW001_OKNO_MSK_STEP_03R_PROVIDER_ITEMS_PRESERVED = 16
KW001_OKNO_MSK_STEP_03R_NORMALIZED_ROWS_VERIFIED = 2226
KW001_OKNO_MSK_FORWARD_ANALYSIS_BLOCKED = true
KW001_OKNO_MSK_STEP_05_RAW_PROVIDER_EVIDENCE_PRESERVED = true
KW001_OKNO_MSK_STEP_06_RAW_PROVIDER_EVIDENCE_PRESERVED = true
```