# KW-002 Blood & Sand — STEP05 W10 PRE-ACQUISITION EXECUTION RELEASE

Date: 2026-09-12  
Handoff ID: `KW002-BS-W10`  
Status: **RELEASED FOR W10 PRE-ACQUISITION RECONCILIATION ONLY / PROVIDER EXECUTION NOT RELEASED**

## 1. Authority

Repository:

`MaksimUnimax/Yandex_direct`

Branch:

`roadmap/kwork-productization-2026-08-28`

Job root:

`extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08`

Canonical W10 Work prompt:

`STEP_05_W10_PRE_ACQUISITION_WORK_PROMPT_2026-09-12.md`

W10 source/method trace:

`STEP_05_W10_PRE_ACQUISITION_EXTERNAL_RESEARCH_2026-09-12.md`

Current Step05 queue gate:

`STEP_05_W10_CURRENT_AUTHORITY_QUEUE_GATE_2026-09-12.tsv`

Current upstream acceptance:

`STEP_04_W09_MAIN_CHATGPT_REMOTE_READBACK_ACCEPTANCE_2026-09-12.md`

## 2. Exact released scope

Released now:

```text
STEP05_W10_PRE_ACQUISITION_RECONCILIATION = YES
READ_CURRENT_W09_QUEUE = YES
RECONCILE_ALL_13_ROWS = YES
READ_ALL_RELEVANT_DURABLE_STEP02_STEP03_STEP05_EVIDENCE = YES
CLASSIFY_OWNER_FACT_ROWS = YES
CLASSIFY_EXISTING_EVIDENCE_REUSE_ROWS = YES
CLASSIFY_DEFERRED_ROWS = YES
CHALLENGE_PSQ001_PSQ004_PSQ005_FOR_TRUE_INCREMENTAL_GAIN = YES
MATERIALIZE_INERT_PROVIDER_CANDIDATE_MANIFEST = YES
SELECT_AT_MOST_ONE_FUTURE_FIRST_EXECUTION_CANDIDATE = YES
```

Not released:

```text
WORDSTAT_PROVIDER_CALL = NO
ORDINARY_YANDEX_SEARCH_CALL = NO
GENSEARCH_CALL = NO
AI_SEARCH_CALL = NO
STEP03A_MUTATION = NO
STEP03B_MUTATION = NO
STEP04_CURRENT_AUTHORITY_MUTATION = NO
STEP06 = NO
FINAL_INTENT = NO
SERP_CLUSTERING = NO
QUERY_TO_PAGE = NO
SITE_ARCHITECTURE = NO
```

## 3. Starting queue state

The accepted W09 Step04 queue contains 13 rows.

Current W10 gate:

```text
POSSIBLE_SEARCH_GAP_CANDIDATES_TO_CHALLENGE = 3
  PSQ001
  PSQ004
  PSQ005

OWNER_FACT_FIRST_OR_ONLY = 5
  PSQ002
  PSQ003
  PSQ009
  PSQ012
  PSQ013

EXISTING_EVIDENCE_REUSE_NO_REPROBE = 4
  PSQ006
  PSQ007
  PSQ008
  PSQ010

DEFER_TO_LATER_SERP_INTENT = 1
  PSQ011

PROVIDER_READY_NOW = 0
```

This split supersedes the older pre-W09 Step05 provisional split for current execution.

## 4. Historical E013 lock

The durable request:

```text
!чётки
wordstat-132a43ff-7cf9-4544-a6e2-68da666c4813
RAW_BLOB_SHA = 550add6010ddbd10e0d807fd1a11046d2b782a4a
REMOTE_READBACK = PASS
```

is current reusable Step05 evidence.

```text
BLIND_REPLAY_E013 = FORBIDDEN
```

## 5. Provider candidate policy

A later provider execution can exist only if W10 proves a surviving candidate has:

```text
NO_EQUIVALENT_DURABLE_EVIDENCE
NO_LITERAL_DUPLICATE
NO_SEMANTIC_DUPLICATE_WITHOUT_SCOPE_GAIN
EXPLICIT_INCREMENTAL_INFORMATION_GAIN
EXPLICIT_NEGATIVE_RESULT_VALUE
EXPLICIT_STOP_CONDITION
OWNER_FACT_DEPENDENCY_RESOLVED_OR_NONE
CURRENT_BRIDGE_COMMAND_SCHEMA_VALIDATED
CURRENT_PROVIDER_PRICE_RECHECKED_IMMEDIATELY_BEFORE_EXECUTION
```

W10 itself may only write an inert `NOT_EXECUTED` candidate specification.

## 6. Fresh-base and publication gates

Work must fetch the current live branch before execution and record the actual start HEAD.

Immediately before publication/owner relay, Work must fetch again. If the remote branch advanced, changed paths must be classified and governing/current authority reconciled before publishing.

A stale mutable cursor/JOB_FLOW/JOB_MANIFEST must not overwrite newer state.

## 7. Required return

Return the artifacts named in the canonical W10 prompt, including:

- 13-row queue reconciliation;
- existing evidence reuse register;
- provider candidate manifest;
- known-failure regression matrix;
- QA;
- Work return;
- artifact manifest/materializer as applicable.

Then STOP for Main ChatGPT remote readback.

## 8. Release marker

```text
HANDOFF_ID = KW002-BS-W10
STEP05_W10_PRE_ACQUISITION_RECONCILIATION_RELEASED = true
STEP05_PROVIDER_EXECUTION_RELEASED = false
PROVIDER_READY_NOW_AT_RELEASE = 0
STEP06_STARTED = false
```
