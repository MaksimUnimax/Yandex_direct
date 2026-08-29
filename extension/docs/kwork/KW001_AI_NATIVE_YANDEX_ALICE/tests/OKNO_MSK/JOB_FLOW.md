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

### Step 03R — repaired first-pass Wordstat acquisition
Status: **COMPLETE / FINAL RECONCILIATION PASS**

Final execution truth:

```text
job_id = kw001-okno-msk-wordstat-pass1-repair-20260829
region = 213
device = DEVICE_ALL
numPhrases = 200
execution = Manual
batch status = COMPLETED
provider requests executed = 18
provider outcomes known = 18
succeeded = 18
failed_terminal = 0
outcome_unknown = 0
estimated provider cost = 0.36 RUB
fully preserved + normalized + verified = 18/18
results rows preserved/verified = 2153
association rows preserved/verified = 262
total provider rows preserved/verified = 2415
```

Item accounting:

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
S17 32+17=49 COMPLETE
S18 123+17=140 COMPLETE
TOTAL = 2153 results + 262 associations = 2415 rows
```

Historical Step-03 acceptance remains superseded because it had technical success without complete reusable data preservation. Step 03R is the accepted replacement evidence.

### Wordstat acquisition coverage revalidation
Status: **COMPLETE / PASS / SUFFICIENT FOR ROW-LEVEL CLEANUP**

Purpose: freshly recheck the four previously preserved targeted Wordstat probes against the now-complete repaired first-pass corpus before allowing cleanup.

Inputs:

```text
complete first-pass rows = 2415
first-pass results = 2153
first-pass associations = 262
preserved targeted probes = 4/4
targeted probe results = 483
targeted probe associations = 67
targeted probe rows = 550
new provider calls during revalidation = 0
additional provider cost = 0 RUB
```

Exact normalized phrase overlap against all 2415 first-pass rows:

```text
P2-01 оконная фурнитура: 217 rows; exact base matches=2; no-exact-base-match=215
P2-02 панорамные окна: 216 rows; exact base matches=7; no-exact-base-match=209
P2-03 остекление балкона с выносом: 21 rows; exact base matches=3; no-exact-base-match=18
P2-04 окна для частного дома: 96 rows; exact base matches=5; no-exact-base-match=91
TOTAL probe rows=550
TOTAL exact base matches=17
TOTAL rows with no exact base match=533
```

`533` is an exact-string comparison result only. It is not a claim of 533 new topics or 533 cross-probe-unique final keywords.

Information-gain result:

```text
P2-01 hardware/fittings vocabulary = CONFIRMED
P2-02 broader panoramic applications/jobs = CONFIRMED
P2-03 balcony-extension engineering subfamily = CONFIRMED / NARROW
P2-04 private-house window user-job vocabulary = CONFIRMED
```

Deferred candidate roots such as terrace glazing, panoramic balcony glazing, broad installation, PVC regulation, mosquito screens, generic PVC windows, glass units, window factory and cottage glazing do not justify another Wordstat request **now**. They are either already represented sufficiently for acquisition or are better resolved during cleanup, business-scope review, or ordinary Yandex Search/page-boundary work.

Accepted verdict:

```text
ACQUISITION_COVERAGE_VERDICT = SUFFICIENT
ADDITIONAL_WORDSTAT_REQUESTS_REQUIRED_NOW = 0
ADDITIONAL_PROVIDER_COST_RUB = 0
ROW_LEVEL_CLEANUP_ALLOWED = true
FINAL_SEMANTIC_SET_COMPLETE = false
PAGE_ARCHITECTURE_COMPLETE = false
NON_REPEAT_CONTROLS = PASS
```

Authority:

`STEP_04A_WORDSTAT_COVERAGE_AND_EXPANSION_REVALIDATION_2026-08-29.md`

### Preserved dynamics evidence
Status: **PRESERVED / REUSABLE / DOES NOT ADVANCE WORKFLOW BY ITSELF**

```text
4/4 dynamics provider observations completely preserved
24 monthly rows per root preserved
0 failed provider requests
0 outcome_unknown
estimated provider cost = 0.08 RUB
```

These data remain usable later for prioritization/context, but do not replace semantic cleanup or Search/page-boundary evidence.

## Current next step

Status: **ROW-LEVEL CLEANUP NOT YET STARTED / PRE-STEP GATE REQUIRED**

Next task:

1. Build one accountable working table covering the collected source rows.
2. Deduplicate while preserving where each phrase came from.
3. Review every phrase and assign explicit status/reason such as KEEP, REVIEW, EXCLUDE_IRRELEVANT, EXCLUDE_SCOPE or EXCLUDE_MECHANICAL.
4. Do not exclude a phrase solely because frequency is low.
5. Do not promote associations automatically into final keywords.
6. Keep business/page-boundary uncertainty in REVIEW for later ordinary Yandex Search resolution.
7. Reconcile all row counts before calling cleanup complete.

This next major step requires the mandatory whole-goal/completed/remaining/prior-errors/current-step/method-review block and owner authorization before execution.

## Remaining work

1. Row-level cleanup of the collected Wordstat evidence with exact input/deduped/excluded/review/retained accounting.
2. Freeze the final working semantic set.
3. Validate important query/page boundaries in ordinary Yandex Search.
4. Group by user task and decide page ownership/actions.
5. Select only material uncertain cases for AI-search evidence; use Webmaster Alice visibility if access exists, otherwise a small GenSearch set.
6. Compare ordinary Search and AI evidence.
7. Prioritize actions.
8. Produce client deliverables.
9. Run final QA and revision gate.

## Close

When the job is fully completed and handed off, mark `JOB_MANIFEST safe_to_delete = true`, then delete this whole OKNO_MSK workspace.

Markers:

```text
KW001_OKNO_MSK_JOB_FLOW_ACTIVE = true
KW001_OKNO_MSK_STEP_03_COMPLETE = true
KW001_OKNO_MSK_STEP_03R_PROVIDER_ITEMS_PRESERVED = 18
KW001_OKNO_MSK_STEP_03R_NORMALIZED_ROWS_VERIFIED = 2415
KW001_OKNO_MSK_WORDSTAT_COVERAGE_REVALIDATION_COMPLETE = true
KW001_OKNO_MSK_WORDSTAT_COVERAGE_VERDICT_SUFFICIENT = true
KW001_OKNO_MSK_TARGETED_PROBE_ROWS_RECHECKED = 550
KW001_OKNO_MSK_TARGETED_PROBE_EXACT_BASE_MATCHES = 17
KW001_OKNO_MSK_TARGETED_PROBE_ROWS_NO_EXACT_BASE_MATCH = 533
KW001_OKNO_MSK_ADDITIONAL_WORDSTAT_REQUESTS_REQUIRED_NOW = 0
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_ALLOWED = true
KW001_OKNO_MSK_STEP_05_RAW_PROVIDER_EVIDENCE_PRESERVED = true
KW001_OKNO_MSK_STEP_06_RAW_PROVIDER_EVIDENCE_PRESERVED = true
```