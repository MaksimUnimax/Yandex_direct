# KW-002 JOB FLOW — BLOOD_SAND_GREENFIELD_2026-09-08

Updated: 2026-09-17  
State basis: live remote HEAD `0630d3f6dbd1962290dc8ab77a454e86c604a795` plus local Step07-preparation artifacts pending owner publication/readback  
Current status: **STEP06 DURABLE PASS / STEP07 PREPARATION LOCAL PASS / OWNER PUBLICATION PENDING / STEP07 NOT STARTED**

---

## 1. Current authority order

1. current live Level1 rules;
2. current `LEVEL2/STEP_RULES_INDEX.md` and step-specific Level2 rules;
3. accepted upstream stage manifests/acceptance/readback files;
4. this `JOB_FLOW.md` and the current execution cursor;
5. current job-specific pre-handoff manifests and schema contracts;
6. historical/superseded files only for incident or lineage review.

Current cursor prepared with this package:

`KW002_EXECUTION_CURSOR_2026-09-17.json`

The earlier `KW002_EXECUTION_CURSOR_2026-09-11.json` remains historical and
must not control current Step06/Step07 state.

---

## 2. Accepted project cursor

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
STEP07_PREPARATION_WORK = COMPLETE_LOCALLY
STEP07_PREPARATION_QA = PASS_LOCALLY
STEP07_PREPARATION_OWNER_UPLOAD = PENDING
STEP07_PREPARATION_REMOTE_READBACK = PENDING
STEP07_PREPARATION_MAIN_CHAT_ACCEPTANCE = PENDING
STEP07 = NOT STARTED
STEP08–STEP20 = NOT STARTED
```

Local Work output is not automatic project acceptance. Step07 preparation
becomes durable/accepted only after owner upload, remote readback/identity QA
and Main Chat acceptance.

---

## 3. Accepted upstream state

### Step03A

```text
RAW_OCCURRENCES = 25979
NORMALIZED_IDENTITIES = 24576
```

### Step03B corrected authority

```text
KEEP = 5100
HOLD = 13035
EXCLUDE = 6441
TOTAL = 24576
```

The older `5074 / 12750 / 6752` partition is obsolete.

### Step04 current W09 authority

```text
FAMILY_ROWS = 32
OBSERVED_FAMILIES = 29
ZERO_OR_GAP_FAMILIES = 3
IDENTITY_ROWS = 24576
OCCURRENCE_ROWS = 25979
TARGETED_EXPANSION_QUEUE_ROWS = 13
```

Step04 families remain preliminary and are not final intent, SERP clusters or
pages.

### Step05 current snapshot closure

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

The unrelated orientation values `259600 / 200577 / 2658` are not supported by
current live accepted Step05 authority and are not part of the current cursor.

### Step06 durable pass

```text
REPRESENTATIVE_QUERIES = 22
CLASSIFIED_SERP_ROWS = 440
QUERY_TOP10_PROFILES = 22
PAIRWISE_COMPARISONS = 231
DOMAIN_RECURRENCE_UNIVERSE = 165
CURATED_COMPETITOR_REGISTRY = 32
COLLISION_UNCERTAINTY_LEDGER = 5
FINAL_PAGE_DECISIONS = NONE
```

Current Step06 closure/analysis authorities:

- `KW002_STEP06_FINAL_CLOSURE_2026-09-17.md`;
- `KW002_STEP06_ANALYSIS_HARDENED_2026-09-17.md`;
- `KW002_STEP06_SEMANTIC_CLASSIFICATION_AUDIT.md`;
- `KW002_STEP06_SEARCH_COMPETITOR_REGISTRY_HARDENED.csv`;
- `KW002_STEP06_SERP_URL_EVIDENCE_440_CLASSIFIED.csv`;
- associated accepted hardened ledgers.

Step06 evidence is a bounded SERP snapshot, not proof of permanent rankings or
competitor stability.

---

## 4. Step07 preparation package

Local preparation artifacts:

- `LEVEL2/STEP_07_COMPETITOR_SEMANTIC_EXPANSION.md`;
- `LEVEL2/STEP_RULES_INDEX.md` (Step07 rule backlink added);
- `STEP_07_COMPETITOR_SEMANTIC_EXPANSION_WORK_PROMPT.md`;
- `STEP_07_PREPARATION_EXTERNAL_METHODOLOGY_AUDIT.md`;
- `STEP_07_PRE_HANDOFF_MANIFEST.md`;
- `STEP_07_OUTPUT_SCHEMA_CONTRACT.json`;
- `STEP_07_AUTHORIZED_COMPETITOR_UNIVERSE.csv`;
- `STEP_07_PREPARATION_QA.md`;
- `KW002_EXECUTION_CURSOR_2026-09-17.json`;
- this updated `JOB_FLOW.md`.

Preparation freezes:

```text
AUTHORIZED_STEP07_COMPETITORS = 32
COMPETITOR_SOURCE = STEP06_CURATED_REGISTRY_ONLY
OUTPUT_DATA_FILES_FOR_FUTURE_STEP07 = 4
PROVENANCE_MODEL = CANDIDATE_SUMMARY + URL_LEDGER + OCCURRENCE_LEDGER
FULL_VOLUME_POLICY = BOUNDED_FRONTIER_EXHAUSTION
ARBITRARY_TOP_N_OR_SAMPLE = FORBIDDEN
STEP08_DEMAND_GATE = REQUIRED
```

No production Step07 candidate rows exist yet.

---

## 5. Publication state

```text
LOCAL_ARTIFACT_COMPLETE = true
LOCAL_QA_PASS = true
PUBLICATION_HANDOFF_READY = true
OWNER_UPLOAD_COMPLETE = false
REMOTE_READBACK_PASS = false
MAIN_CHAT_ACCEPTANCE = PENDING
```

Direct Work commit/push/PR/GitHub publication is forbidden. Owner relay is the
transport layer for this multi-file package.

---

## 6. Current provider boundary

```text
WORDSTAT_CALLS_ALLOWED_NOW = 0
YANDEX_SEARCH_CALLS_ALLOWED_NOW = 0
AI_SEARCH_CALLS_ALLOWED_NOW = 0
GENSEARCH_CALLS_ALLOWED_NOW = 0
```

Step07 itself is public competitor-page candidate discovery and performs no
search-demand acquisition. Step08 requires a separate pre-step review and
release.

---

## 7. Exact next action

1. Owner downloads the Step07-preparation handoff ZIP.
2. Owner uploads each contained file to its repository-relative path on branch
   `roadmap/kwork-productization-2026-08-28`.
3. Owner replies `готово`.
4. Main Chat/Work fetches the new live remote HEAD and performs remote readback
   plus file/hash/identity QA.
5. Main Chat accepts or rejects `STEP07_PREPARATION`.
6. Only after acceptance may the owner separately relay
   `STEP_07_COMPETITOR_SEMANTIC_EXPANSION_WORK_PROMPT.md` for actual Step07.

```text
CURRENT_NEXT_ACTION = OWNER_RELAY_OF_STEP07_PREPARATION_PACKAGE
ACTUAL_STEP07_RELEASED = false
STEP07 = NOT_STARTED
```
