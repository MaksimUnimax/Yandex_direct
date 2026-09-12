# KW-002 Blood & Sand — STEP05 W10 PRE-ACQUISITION EXECUTION RELEASE V2

Date: 2026-09-12
Handoff ID: `KW002-BS-W10-V2`
Status: **CORRECTED RELEASE FOR PRE-ACQUISITION RECONCILIATION ONLY / PROVIDER EXECUTION NOT RELEASED**

## 1. Authority package

Current handoff consists of:

- `STEP_05_W10_PREPARATION_RULE_VIOLATION_AND_CORRECTION_2026-09-12.md`
- `STEP_05_W10_PRE_ACQUISITION_EXTERNAL_RESEARCH_V2_2026-09-12.md`
- `STEP_05_W10_PRE_HANDOFF_MANIFEST_V2_2026-09-12.md`
- `STEP_05_W10_PRE_ACQUISITION_WORK_PROMPT_V2_2026-09-12.md`
- this release.

The V1 W10 prompt/release/research package is historical and superseded for execution.

## 2. Required owner-facing gate before execution

Work execution is NOT authorized merely by this file existing.

Before the owner relays the V2 prompt, Main ChatGPT must provide the mandatory owner-facing pre-step disclosure required by `LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`, including:

```text
WHOLE KWORK GOAL
FULL ROADMAP
COMPLETED
REMAINING
CURRENT STEP GOAL
WHAT PROBLEM THE STEP SOLVES
REQUIRED OUTPUT
RELEVANT PRIOR ERRORS
NON-REPEAT CONTROLS
FRESH INTERNET RESEARCH
CLICKABLE SOURCE LIST + WHAT EACH SOURCE SUPPORTS
SOURCE→METHOD TRACE
METHOD / EXECUTION PLAN
BRIDGE/WORK GATE
PASS CONDITIONS
ПРОСТЫМИ СЛОВАМИ: WHY / WHAT / RESULT / BLOCKER / NEXT ACTION
```

Until that disclosure is visible in chat:

```text
WORK_EXECUTION_ALLOWED = false
```

After the disclosure is visible and the owner relays the exact V2 handoff:

```text
WORK_EXECUTION_ALLOWED = true
PROVIDER_EXECUTION_ALLOWED = false
```

## 3. Released scope

Released:

```text
READ_CURRENT_LIVE_BRANCH = YES
READ_CURRENT_W09_STEP04_AUTHORITY = YES
RECONCILE_ALL_13_QUEUE_ROWS = YES
RECONCILE_ALL_RELEVANT_DURABLE_STEP02_STEP03_STEP05_EVIDENCE = YES
CLASSIFY_OWNER_FACT_ROWS = YES
CLASSIFY_EXISTING_EVIDENCE_REUSE_ROWS = YES
CLASSIFY_DEFERRED_ROW = YES
CHALLENGE_PSQ001_PSQ004_PSQ005_FOR_REAL_INCREMENTAL_GAIN = YES
MATERIALIZE_INERT_PROVIDER_CANDIDATE_MANIFEST = YES
SELECT_AT_MOST_ONE_FUTURE_FIRST_EXECUTION_CANDIDATE = YES
```

Not released:

```text
WORDSTAT_CALL = NO
ORDINARY_YANDEX_SEARCH_CALL = NO
GENSEARCH_CALL = NO
AI_SEARCH_CALL = NO
STEP03A_MUTATION = NO
STEP03B_MUTATION = NO
W09_STEP04_ANALYTICAL_MUTATION = NO
STEP06 = NO
FINAL_INTENT = NO
SERP_CLUSTERING = NO
QUERY_TO_PAGE = NO
SITE_ARCHITECTURE = NO
```

## 4. Current queue gate

```text
SEARCH_GAP_CANDIDATES_TO_CHALLENGE = 3
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

DEFERRED = 1
PSQ011

PROVIDER_READY_NOW = 0
```

## 5. Historical evidence lock

Historical E013:

```text
phrase = !чётки
request_id = wordstat-132a43ff-7cf9-4544-a6e2-68da666c4813
results = 2000
associations = 19
remote_readback = PASS
blind_replay = FORBIDDEN
```

## 6. Current-state warning

`JOB_FLOW.md` and `JOB_MANIFEST.md` contain stale W08-era status summaries. They are not current execution authority for this V2 handoff.

Use current live cursor + W09 acceptance + accepted W09 analytical artifacts + this corrected V2 package.

Do not publish stale mutable state files from Work.

## 7. Freshness gates

At Work start:

```text
FETCH_CURRENT_REMOTE = required
WORK_START_REMOTE_HEAD = actual live head
CURRENT_V2_PROMPT_PRESENT = required
CURRENT_V2_RELEASE_PRESENT = required
CURRENT_PRE_HANDOFF_MANIFEST_PRESENT = required
```

Immediately before publication/owner relay:

```text
REMOTE_HEAD_RECHECK = required
CHANGED_PATHS_CLASSIFIED = required if remote advanced
GOVERNING_AUTHORITY_RECONCILED = required if changed
STALE_BASE_MUTABLE_STATE_FILE_OVERWRITE = 0
```

## 8. Return gate

Work must return the exact V2 artifacts named in the pre-handoff manifest and canonical V2 prompt, then STOP.

Main ChatGPT must perform return QA and remote readback before any later provider command can be released.

## 9. Release markers

```text
HANDOFF_ID = KW002-BS-W10-V2
PRE_HANDOFF_MANIFEST_FROZEN = true
FRESH_EXTERNAL_RESEARCH_V2 = complete
OWNER_FACING_PRE_STEP_DISCLOSURE_REQUIRED = true
STEP05_PRE_ACQUISITION_RECONCILIATION_RELEASED_AFTER_DISCLOSURE = true
STEP05_PROVIDER_EXECUTION_RELEASED = false
PROVIDER_READY_NOW_AT_RELEASE = 0
STEP06_STARTED = false
```
