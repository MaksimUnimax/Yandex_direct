# KW-002 JOB FLOW — BLOOD_SAND_GREENFIELD_2026-09-08

Updated: 2026-09-17  
Preparation base: `0630d3f6dbd1962290dc8ab77a454e86c604a795`  
Owner upload HEAD: `b868a85a5b0ffd2a95740a351ba8bb3d2586d326`  
Canonical placement / preparation remote-readback HEAD: `3c141c0a4f2dbfdc51a563fd7c76e40958bfee33`  
Current status: **STEP06 DURABLE PASS / STEP07 PREPARATION ACCEPTED / STEP07 RELEASE REVALIDATION REQUIRED / STEP07 NOT STARTED**

---

## 0. Mandatory no-action rule-read gate

Before any further material job action, the executor MUST first read in full the current live authorities, beginning with:

- `../../LEVEL1/00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE.md`;
- `../../LEVEL1/01_RECURRING_ASSISTANT_RULE_FAILURES_ANTI_REGRESSION_CHECKLIST.md`;
- `00_READ_RULES_BEFORE_ANY_ACTION.md`;
- `KW002_RULE_COMPLIANCE_FAILURE_INCIDENT_2026-09-17.md`.

Known recurring failure: Main Chat has repeatedly violated explicit project rules when working from memory/summary instead of freshly reading current live authorities in full.

```text
NO FRESH FULL RULE REREAD
→ NO MATERIAL ACTION
```

This includes preparation, Work prompt relay/execution, analysis, provider work, publication acceptance and cursor/roadmap movement.

---

## 1. Current authority order

1. current live cross-Kwork owner-locked authorities where applicable;
2. current `LEVEL1/00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE.md`;
3. current `LEVEL1/01_RECURRING_ASSISTANT_RULE_FAILURES_ANTI_REGRESSION_CHECKLIST.md`;
4. all other applicable current Level1 rules, including owner-facing report/source disclosure and Work freshness/handoff authorities;
5. current `LEVEL2/STEP_RULES_INDEX.md` and step-specific Level2 rules;
6. accepted upstream stage manifests/acceptance/readback files;
7. this `JOB_FLOW.md` and current execution cursor;
8. current job-specific pre-handoff manifests/schema contracts/release gates;
9. current job-specific failure/incident records;
10. historical/superseded files only for incident or lineage review.

Current cursor:

`KW002_EXECUTION_CURSOR_2026-09-17.json`

The earlier `KW002_EXECUTION_CURSOR_2026-09-11.json` is historical and must not control current Step06/Step07 state.

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
STEP07_PREPARATION_WORK = COMPLETE
STEP07_PREPARATION_QA = PASS
STEP07_PREPARATION_OWNER_UPLOAD = COMPLETE
STEP07_PREPARATION_REMOTE_READBACK = PASS
STEP07_PREPARATION_MAIN_CHAT_ACCEPTANCE = ACCEPTED
STEP07_RELEASE_RULE_REVALIDATION = REQUIRED
STEP07_OWNER_FACING_PRE_STEP_REPORT = REQUIRED
STEP07_WORK_PROMPT_LIVE_AUTHORITY_RECONCILIATION = REQUIRED
STEP07 = NOT STARTED
STEP08–STEP20 = NOT STARTED
```

`STEP07_PREPARATION` remains accepted as the frozen preparation package. However, the live Level1 authority changed after that preparation was accepted. Under `WORK_BASE_FRESHNESS_AND_AUTHORITY_DRIFT_RULE.md`, the older prepared Work contract may not be executed as current authority until release revalidation passes.

The release gate is:

`STEP_07_RELEASE_REVALIDATION_GATE_2026-09-17.md`

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

Step04 families remain preliminary and are not final intent, SERP clusters or pages.

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

The orientation values `259600 / 200577 / 2658` are not supported by the current live accepted Step05 W10 V2/V3 authority and are not part of the current cursor.

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

Current Step06 closure/analysis authorities include:

- `KW002_STEP06_FINAL_CLOSURE_2026-09-17.md`;
- `KW002_STEP06_ANALYSIS_HARDENED_2026-09-17.md`;
- `KW002_STEP06_SEMANTIC_CLASSIFICATION_AUDIT.md`;
- `KW002_STEP06_SEARCH_COMPETITOR_REGISTRY_HARDENED.csv`;
- `KW002_STEP06_SERP_URL_EVIDENCE_440_CLASSIFIED.csv`;
- associated accepted hardened ledgers.

Step06 evidence is a bounded SERP snapshot, not proof of permanent rankings or competitor stability.

---

## 4. Accepted Step07 preparation package

Canonical final preparation files:

### Level2

- `LEVEL2/STEP_07_COMPETITOR_SEMANTIC_EXPANSION.md`;
- `LEVEL2/STEP_RULES_INDEX.md`.

### Job root

- `STEP_07_COMPETITOR_SEMANTIC_EXPANSION_WORK_PROMPT.md`;
- `STEP_07_PREPARATION_EXTERNAL_METHODOLOGY_AUDIT.md`;
- `STEP_07_PRE_HANDOFF_MANIFEST.md`;
- `STEP_07_OUTPUT_SCHEMA_CONTRACT.json`;
- `STEP_07_AUTHORIZED_COMPETITOR_UNIVERSE.csv`;
- `STEP_07_PREPARATION_QA.md`;
- `KW002_EXECUTION_CURSOR_2026-09-17.json`;
- this `JOB_FLOW.md`.

Post-preparation rule-compliance controls now additionally include:

- `00_READ_RULES_BEFORE_ANY_ACTION.md`;
- `KW002_RULE_COMPLIANCE_FAILURE_INCIDENT_2026-09-17.md`;
- `STEP_07_RELEASE_REVALIDATION_GATE_2026-09-17.md`.

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

Step07 preparation Work QA:

```text
PROGRAMMATIC_CHECKS = 60
PROGRAMMATIC_PASS = 60
PROGRAMMATIC_FAIL = 0
NEW_PROVIDER_CALLS = 0
```

Return QA confirmed:

```text
CANONICAL_HANDOFF_FILES = 10/10
LEVEL2_STAGING_BLOB_IDENTITY = PASS
STAGING_ONLY_COPIES_REMAINING = 0
AUTHORIZED_COMPETITOR_UNIVERSE = 32
ACTUAL_STEP07_PRODUCTION_OUTPUTS_PRESENT = 0
REMOTE_READBACK = PASS
MAIN_CHAT_ACCEPTANCE = ACCEPTED
```

No production Step07 candidate rows exist yet.

---

## 5. Owner-relay publication state

The active publication rule is single-staging owner relay:

```text
ONE HANDOFF UNIT
→ ONE OWNER UPLOAD TARGET
→ EXECUTOR FINAL PLACEMENT
→ STAGING CLEANUP
→ REMOTE READBACK
→ ACCEPTANCE
```

For the Step07 preparation package:

```text
LOCAL_ARTIFACT_COMPLETE = true
LOCAL_QA_PASS = true
PUBLICATION_HANDOFF_READY = true
OWNER_UPLOAD_COMPLETE = true
CANONICAL_PLACEMENT_COMPLETE = true
STAGING_CLEANUP_COMPLETE = true
REMOTE_READBACK_PASS = true
REMOTE_PUBLICATION_COMPLETE = true
MAIN_CHAT_ACCEPTANCE = ACCEPTED
```

The owner was not required to route files among Level2/job-root paths. Two staging-only Level2 artifacts were placed by Main Chat using exact existing blob identities and their staging copies were removed.

---

## 6. Current provider boundary

```text
WORDSTAT_CALLS_ALLOWED_NOW = 0
YANDEX_SEARCH_CALLS_ALLOWED_NOW = 0
AI_SEARCH_CALLS_ALLOWED_NOW = 0
GENSEARCH_CALLS_ALLOWED_NOW = 0
```

Actual Step07 is public competitor-page candidate discovery and performs no search-demand acquisition. Step08 requires a separate pre-step review and release.

---

## 7. Exact next action

The preparation package is accepted, but actual Step07 is **not released yet** because current rule authority changed after preparation.

Before the existing Step07 Work prompt can be relayed, Main Chat MUST execute:

`STEP_07_RELEASE_REVALIDATION_GATE_2026-09-17.md`

That requires, in order:

```text
FETCH CURRENT LIVE REMOTE HEAD
→ READ ALL APPLICABLE RULES IN FULL
→ READ CURRENT FAILURE/INCIDENT LEDGERS
→ RECONCILE THE PREPARED STEP07 WORK PROMPT AGAINST CURRENT LIVE AUTHORITY
→ PERFORM THE FRESH STEP07 EXTERNAL-RESEARCH / FRESHNESS CHECK REQUIRED BY THE PRE-STEP RULE
→ SHOW THE COMPLETE OWNER-FACING PRE-STEP REPORT IN CHAT
→ SHOW CLICKABLE SOURCES + WHAT EACH SUPPORTS + SOURCE→METHOD TRACE
→ END WITH A REAL PLAIN-RUSSIAN WHY / WHAT / RESULT / BLOCKER / NEXT ACTION SUMMARY
→ ONLY THEN STEP07_EXECUTION_ALLOWED MAY BECOME true
→ ONLY THEN RELAY THE CURRENT CANONICAL WORK PROMPT
```

```text
CURRENT_NEXT_ACTION = STEP07_RELEASE_REVALIDATION_BEFORE_WORK_HANDOFF
STEP07_PREPARATION = ACCEPTED
STEP07_RELEASE_REVALIDATION = REQUIRED
ACTUAL_STEP07_RELEASED = false
STEP07 = NOT_STARTED
STEP08 = NOT_STARTED
```
