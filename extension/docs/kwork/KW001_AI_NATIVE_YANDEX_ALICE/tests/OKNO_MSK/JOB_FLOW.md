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

Historical Step-03 acceptance remains superseded because it had technical success without complete reusable data preservation. Step 03R is the accepted replacement evidence.

### Wordstat acquisition coverage revalidation
Status: **COMPLETE / PASS / SUFFICIENT**

```text
complete first-pass rows = 2415
preserved targeted probes = 4/4
targeted probe results = 483
targeted probe associations = 67
targeted probe rows = 550
probe exact matches to first-pass rows = 17
probe rows with no exact first-pass match = 533
new provider calls during revalidation = 0
additional provider cost = 0 RUB
ACQUISITION_COVERAGE_VERDICT = SUFFICIENT
ADDITIONAL_WORDSTAT_REQUESTS_REQUIRED_NOW = 0
```

The four probes confirmed/further covered window hardware language, panoramic applications, balcony-extension engineering and private-house window demand. `533` remains an exact-string comparison count only.

Authority: `STEP_04A_WORDSTAT_COVERAGE_AND_EXPANSION_REVALIDATION_2026-08-29.md`.

### Preserved dynamics evidence
Status: **PRESERVED / REUSABLE / DOES NOT ADVANCE WORKFLOW BY ITSELF**

```text
4/4 dynamics provider observations completely preserved
24 monthly rows per root preserved
0 failed provider requests
0 outcome_unknown
estimated provider cost = 0.08 RUB
```

### Step 07B — full row-level semantic cleanup
Status: **COMPLETE / PASS / FULL ACCOUNTING**

Purpose: transform all completely preserved Wordstat source rows into one accountable exact-deduped working dataset without making downstream SERP/page decisions prematurely.

Input:

```text
repaired first-pass source rows = 2415
targeted-probe source rows = 550
TOTAL source rows = 2965
result rows = 2636
association rows = 329
```

Exact deduplication:

```text
unique exact normalized phrases = 2840
duplicate source occurrences = 125
phrase keys with >1 source occurrence = 101
canonical provenance occurrence sum = 2965
```

Complete row classification:

```text
KEEP = 1760
REVIEW = 749
EXCLUDE_SCOPE = 180
EXCLUDE_IRRELEVANT = 120
EXCLUDE_MECHANICAL = 31
STATUS TOTAL = 2840
UNCLASSIFIED = 0
```

Controls passed:

```text
exact phrase equality only used for dedupe
all 2965 source occurrences preserved in occurrence-level audit table
all canonical rows preserve compact provenance
low frequency alone never used for exclusion
association rows never auto-promoted to KEEP
business/page-boundary uncertainty retained as REVIEW
provider requests executed during cleanup = 0
provider cost during cleanup = 0 RUB
PROVENANCE_RECONCILIATION = PASS
```

Artifacts:

```text
STEP_07B_ROW_LEVEL_CLEANUP_BUILD.py
STEP_07B_ROW_LEVEL_CLEANUP_WORKING.tsv
STEP_07B_ROW_LEVEL_CLEANUP_OCCURRENCES.tsv
STEP_07B_ROW_LEVEL_CLEANUP_SUMMARY.json
STEP_07B_ROW_LEVEL_CLEANUP_ACCEPTANCE_2026-08-29.md
```

Recorded content SHA-256:

```text
WORKING = 929b6439e9ace1f269987a046af19ac0a3bc107d4fa90c8320c968817392bc2d
OCCURRENCES = a5e3fceb5647d1f9fbbd5fa3ace9feebb8665a228173ad14fb8b73d846584d63
```

The temporary branch-scoped GitHub Actions workflow used only to execute the reproducible builder was removed after output verification. The builder remains for audit/reproduction.

Authority: `STEP_07B_ROW_LEVEL_CLEANUP_ACCEPTANCE_2026-08-29.md`.

Important limit: `REVIEW=749` is deliberate unresolved evidence, not missing cleanup. Those rows have explicit decisions/reasons but material business/page boundaries must still be resolved with later evidence rather than guessed here.

## Current next step

Status: **FINAL WORKING SEMANTIC SET FREEZE NOT YET STARTED / PRE-STEP GATE REQUIRED**

Next task:

1. Use the completed cleanup artifacts as the sole semantic-row input.
2. Define and freeze which cleaned rows proceed into the Search-stage working semantic set without silently resolving `REVIEW` cases that require Search evidence.
3. Preserve traceability from the frozen set back to the 2840 canonical cleanup rows and 2965 source occurrences.
4. Do not perform ordinary Yandex Search, SERP clustering, page ownership, final architecture or AI evidence inside the freeze itself unless the next step's approved method explicitly defines a combined boundary.
5. Quantitatively reconcile the frozen Search input against the Step-07B statuses.

Before execution, this new major step requires the mandatory whole-goal/completed/remaining/prior-errors/current-step/method-review block and explicit owner authorization.

## Remaining work

1. Freeze the final working semantic set / Search-stage input from the completed row-level cleanup.
2. Validate important query/page boundaries in ordinary Yandex Search.
3. Group the Search-validated semantic set by user task/SERP compatibility.
4. Map groups to existing pages and decide page ownership/actions.
5. Diagnose real cannibalization where evidence supports it.
6. Freeze Search-only architecture before AI evidence.
7. Select only material uncertain cases for AI-search evidence; use Webmaster Alice visibility if access exists, otherwise a small GenSearch set.
8. Compare ordinary Search and AI evidence.
9. Prioritize actions.
10. Produce client deliverables.
11. Run final QA and revision gate.
12. Close/handoff job and only then delete disposable workspace.

Not complete yet:

```text
FINAL_SEMANTIC_SET_COMPLETE = false
ORDINARY_YANDEX_SEARCH_VALIDATION_COMPLETE = false
SEARCH_ONLY_ARCHITECTURE_COMPLETE = false
AI_EVIDENCE_COMPLETE = false
CLIENT_DELIVERABLES_COMPLETE = false
FINAL_QA_COMPLETE = false
```

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
KW001_OKNO_MSK_ADDITIONAL_WORDSTAT_REQUESTS_REQUIRED_NOW = 0
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_COMPLETE = true
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_INPUT_ROWS = 2965
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_UNIQUE_EXACT = 2840
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_DUPLICATE_OCCURRENCES = 125
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_KEEP = 1760
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_REVIEW = 749
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_EXCLUDE_SCOPE = 180
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_EXCLUDE_IRRELEVANT = 120
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_EXCLUDE_MECHANICAL = 31
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_UNCLASSIFIED = 0
KW001_OKNO_MSK_FINAL_SEMANTIC_SET_COMPLETE = false
KW001_OKNO_MSK_STEP_05_RAW_PROVIDER_EVIDENCE_PRESERVED = true
KW001_OKNO_MSK_STEP_06_RAW_PROVIDER_EVIDENCE_PRESERVED = true
```