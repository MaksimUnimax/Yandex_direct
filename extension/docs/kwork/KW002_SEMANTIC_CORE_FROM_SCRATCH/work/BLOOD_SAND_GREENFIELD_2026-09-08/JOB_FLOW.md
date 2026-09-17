# KW-002 JOB FLOW — BLOOD_SAND_GREENFIELD_2026-09-08

Updated: 2026-09-17  
Preparation base: `0630d3f6dbd1962290dc8ab77a454e86c604a795`  
Preparation canonical placement/readback: `3c141c0a4f2dbfdc51a563fd7c76e40958bfee33`  
Step07 release-revalidation start HEAD: `cb7545462a4386dcad24b46ec7d99ec788f6e44d`  
Step07 prompt reconciliation commit: `360d4c2c1ed54fa42075dcced156fe867b7b1b23`  
Step07 release record commit: `8eef4d17512f75235daf5745373daa10c46e056f`  
Current status: **STEP06 DURABLE PASS / STEP07 PREPARATION ACCEPTED / STEP07 RELEASE REVALIDATION PASS / ACTUAL STEP07 RELEASED TO WORK / STEP07 NOT YET EXECUTED**

---

## 0. Mandatory no-action rule-read gate

Before every material action, including the Work run and later acceptance, the executor must freshly read the applicable current live rules in full beginning with:

- `../../LEVEL1/00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE.md`;
- `../../LEVEL1/01_RECURRING_ASSISTANT_RULE_FAILURES_ANTI_REGRESSION_CHECKLIST.md`;
- `00_READ_RULES_BEFORE_ANY_ACTION.md`;
- `KW002_RULE_COMPLIANCE_FAILURE_INCIDENT_2026-09-17.md`.

```text
ASSISTANT MEMORY != RULE READBACK
NO FRESH FULL RULE REREAD -> NO MATERIAL ACTION
```

Actual Step07 Work must independently fetch the current branch and materialize `STEP07_EXECUTION_RULE_READ_LEDGER.md` before extraction.

---

## 1. Current authority order

1. current live cross-Kwork owner-locked authorities;
2. current Level1 `00` / `01` fail-closed authorities;
3. all other applicable current Level1 rules;
4. current `LEVEL2/STEP_RULES_INDEX.md` and `LEVEL2/STEP_07_COMPETITOR_SEMANTIC_EXPANSION.md`;
5. accepted upstream manifests/acceptances/evidence;
6. this `JOB_FLOW.md` and current execution cursor;
7. current Step07 preparation manifest/schema/authorized-universe files;
8. `STEP_07_EXECUTION_RELEASE_REVALIDATION_2026-09-17.md`;
9. current `STEP_07_COMPETITOR_SEMANTIC_EXPANSION_WORK_PROMPT.md`;
10. job-specific failure/incident records;
11. historical/superseded files only for lineage/review.

Canonical roadmap authority is `LEVEL2/STEP_RULES_INDEX.md` and currently runs through **STEP22 — job close**.

---

## 2. Current project cursor

```text
STEP00 = COMPLETE
STEP01 = COMPLETE
STEP02 = COMPLETE
STEP03 = COMPLETE
STEP03A = COMPLETE
STEP03B = COMPLETE
STEP04 = ACCEPTED
STEP05 = COMPLETE / PASS
STEP06 = DURABLE PASS

STEP07_PREPARATION_WORK = COMPLETE
STEP07_PREPARATION_QA = PASS
STEP07_PREPARATION_OWNER_UPLOAD = COMPLETE
STEP07_PREPARATION_REMOTE_READBACK = PASS
STEP07_PREPARATION_MAIN_CHAT_ACCEPTANCE = ACCEPTED

STEP07_RELEASE_RULE_REVALIDATION = PASS
STEP07_OWNER_FACING_PRE_STEP_REPORT = PASS
STEP07_WORK_PROMPT_LIVE_AUTHORITY_RECONCILIATION = PASS
STEP07_EXECUTION_ALLOWED = true
STEP07_RELEASED_FOR_WORK_RELAY = true
STEP07 = NOT STARTED / RELEASED TO WORK

STEP08 = NOT STARTED
STEP09 = NOT STARTED
STEP10 = NOT STARTED
STEP11 = NOT STARTED
STEP12 = NOT STARTED
STEP13 = NOT STARTED
STEP14 = NOT STARTED
STEP15 = NOT STARTED
STEP16 = NOT STARTED
STEP17 = NOT STARTED
STEP18 = NOT STARTED
STEP19 = NOT STARTED
STEP20 = NOT STARTED
STEP21 = NOT STARTED
STEP22 = NOT STARTED
```

`STEP07 = NOT STARTED / RELEASED TO WORK` means Main Chat has authorized the actual full-volume Step07 execution unit, but no competitor-page production extraction has yet been returned by Work.

---

## 3. Accepted upstream state

### Step03A

```text
RAW_OCCURRENCES = 25,979
NORMALIZED_IDENTITIES = 24,576
```

### Step03B corrected authority

```text
KEEP = 5,100
HOLD = 13,035
EXCLUDE = 6,441
TOTAL = 24,576
```

The older `5,074 / 12,750 / 6,752` partition is obsolete.

### Step04 current authority

```text
FAMILY_ROWS = 32
IDENTITY_ROWS = 24,576
OCCURRENCE_ROWS = 25,979
TARGETED_EXPANSION_QUEUE_ROWS = 13
```

Step04 remains preliminary family/task context, not final intent, SERP clusters or pages.

### Step05 current accepted closure

```text
QUEUE_ROWS_RECONCILED = 13/13
NEW_PROVIDER_CANDIDATES = 1
EXECUTED_PROVIDER_CANDIDATES = 1
W10C001_OUTCOME = SUCCESS_WITH_ZERO_ROWS
TOTALCOUNT_AGGREGATE = 3
RETURNED_RESULT_ROWS = 0
RETURNED_ASSOCIATION_ROWS = 0
NEW_UNION_ROWS = 0
```

The old orientation values `259600 / 200577 / 2658` are not supported by current accepted Step05 authority and remain excluded.

### Step06 durable pass

```text
REPRESENTATIVE_QUERIES = 22
CLASSIFIED_SERP_ROWS = 440
QUERY_TOP10_PROFILES = 22
PAIRWISE_COMPARISONS = 231
DOMAIN_RECURRENCE_UNIVERSE = 165
CURATED_COMPETITOR_REGISTRY = 32
COLLISION_UNCERTAINTY_LEDGER = 5
```

Only the accepted 32-row curated registry may authorize Step07 competitors.

---

## 4. Step07 preparation and release authorities

Accepted preparation package includes:

### Level2
- `LEVEL2/STEP_07_COMPETITOR_SEMANTIC_EXPANSION.md`;
- `LEVEL2/STEP_RULES_INDEX.md`.

### Job root
- `STEP_07_PRE_HANDOFF_MANIFEST.md`;
- `STEP_07_OUTPUT_SCHEMA_CONTRACT.json`;
- `STEP_07_AUTHORIZED_COMPETITOR_UNIVERSE.csv`;
- `STEP_07_PREPARATION_EXTERNAL_METHODOLOGY_AUDIT.md`;
- `STEP_07_PREPARATION_QA.md`;
- `STEP_07_COMPETITOR_SEMANTIC_EXPANSION_WORK_PROMPT.md`.

Current release controls additionally include:

- `STEP_07_RELEASE_REVALIDATION_GATE_2026-09-17.md`;
- `STEP_07_EXECUTION_RELEASE_REVALIDATION_2026-09-17.md`;
- `KW002_RULE_COMPLIANCE_FAILURE_INCIDENT_2026-09-17.md`;
- Level1 `00`/`01` fail-closed rules.

Release revalidation confirmed:

```text
FULL_RULE_REREAD = PASS
FRESH_EXTERNAL_RESEARCH = PASS
SOURCE_DISCLOSURE_IN_CHAT = PASS
PLAIN_LANGUAGE_SUMMARY = PASS
WORK_PROMPT_CURRENT_AUTHORITY_RECONCILIATION = PASS
UNRESOLVED_AUTHORITY_CONFLICTS = 0
```

The current Work prompt now reflects Step22 roadmap authority, clean source boundaries, current fail-closed rules, universal quality scoring and single-staging owner relay.

---

## 5. Actual Step07 execution contract

```text
AUTHORIZED_STEP07_COMPETITORS = 32
AUTHORITY_IDS = S07A001..S07A032
COMPETITOR_SOURCE = STEP06_CURATED_REGISTRY_ONLY
FULL_VOLUME_POLICY = BOUNDED_FRONTIER_EXHAUSTION_NO_SAMPLE
STEP08_DEMAND_GATE = REQUIRED
```

Step07 must create:

```text
COMPETITOR_GAP_CANDIDATES.csv
STEP07_COMPETITOR_COVERAGE_LEDGER.csv
STEP07_SOURCE_URL_LEDGER.csv
STEP07_CANDIDATE_PROVENANCE_LEDGER.csv
STEP07_EXECUTION_QA.md
STEP07_EXECUTION_RULE_READ_LEDGER.md
STEP07_EXECUTION_HANDOFF_MANIFEST.json
```

Hard boundaries:

```text
COMPETITOR PAGE TOPIC != PROVEN SEARCH DEMAND
COMPETITOR-DERIVED CANDIDATE != PRODUCTION KEYWORD
WORDSTAT_CALLS_IN_STEP07 = 0
YANDEX_SEARCH_CALLS_IN_STEP07 = 0
AI_SEARCH_OR_GENSEARCH_CALLS_IN_STEP07 = 0
FINAL_INTENT_DECISIONS = 0
FINAL_CLUSTER_DECISIONS = 0
FINAL_PAGE_DECISIONS = 0
```

---

## 6. Work handoff / publication boundary

Actual Step07 executes in ChatGPT Work because this is a complete full-volume large-data unit.

Work must not commit/push/PR.

After Work completes local QA:

```text
WORK OUTPUT
→ DIRECT FILE LINKS + ONE TRANSPORT ZIP
→ OWNER EXTRACTS ZIP
→ OWNER UPLOADS ALL HANDOFF FILES TO ONE STAGING TARGET
→ OWNER RETURNS "ГОТОВО"
→ MAIN CHAT VERIFIES STAGING
→ MAIN CHAT PERFORMS FINAL PLACEMENT IF NEEDED
→ REMOTE READBACK / IDENTITY QA
→ MAIN CHAT ACCEPTANCE
```

Frozen staging target:

```text
repository = MaksimUnimax/Yandex_direct
branch = roadmap/kwork-productization-2026-08-28
directory = extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08
upload URL = https://github.com/MaksimUnimax/Yandex_direct/upload/roadmap/kwork-productization-2026-08-28/extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08
```

Owner does not route NEW/REPLACE files among repository directories. ZIP is transport-only and is not committed.

Work must not include stale mutable `JOB_FLOW.md`/cursor copies in its output package. Main Chat updates mutable state after remote readback.

---

## 7. Exact next action

Actual Step07 is released now.

```text
CURRENT_NEXT_ACTION = OWNER_RELAY_CURRENT_STEP_07_COMPETITOR_SEMANTIC_EXPANSION_WORK_PROMPT_TO_CHATGPT_WORK
STEP07_EXECUTION_ALLOWED = true
STEP07_RELEASED_FOR_WORK_RELAY = true
STEP07 = NOT_STARTED_RELEASED_TO_WORK
STEP08 = NOT_STARTED
```

The owner should relay the current complete contents of `STEP_07_COMPETITOR_SEMANTIC_EXPANSION_WORK_PROMPT.md` to ChatGPT Work. Main Chat must not perform a sampled substitute for the Work execution.
