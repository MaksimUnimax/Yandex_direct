# KW-002 Blood & Sand — Step05 W10 V2 pre-acquisition QA

Date: 2026-09-12
Handoff: `KW002-BS-W10-V2`
Verdict: **PASS_CANDIDATE**

## Authority and freshness

- `WORK_START_REMOTE_HEAD = 7ceec096dad6703b5dffede3271019f55946d75d`
- `WORK_PRE_PUBLICATION_REMOTE_HEAD = 7ceec096dad6703b5dffede3271019f55946d75d`
- `REMOTE_DRIFT_CLASSIFICATION = NO_REMOTE_DRIFT`
- `REMOTE_CHANGED_PATHS = []`
- Current V2 prompt/release/manifest/research/correction authority: **CONFIRMED**.
- Accepted W09 current authority: **USED AND HASH-VERIFIED**.
- Stale mutable cursor/JOB_FLOW/JOB_MANIFEST overwritten or packaged: **0**.

## Complete-volume accounting

| Gate | Expected | Observed | Result |
|---|---:|---:|---|
| W09 normalized identities read/joined | 24,576 | 24,576 | PASS |
| W09 RAW occurrences read/joined | 25,979 | 25,979 | PASS |
| Step03A normalization ledger | 25,979 | 25,979 | PASS |
| Step03B KEEP | 5,100 | 5100 | PASS |
| Step03B HOLD | 13,035 | 13035 | PASS |
| Step03B EXCLUDE | 6,441 | 6441 | PASS |
| Active+HOLD identities | 18,135 | 18135 | PASS |
| Active+HOLD RAW | 19,086 | 19086 | PASS |
| W09 families read and recounted | 32 | 32 | PASS |
| W09 independent diagnostic rows | 24,576 | 24576 | PASS |
| W09 sanitation feedback rows | 18 | 18 | PASS |
| Step02/Step03 manifest alignment | 79/79 | 79/79 | PASS |
| Step03 RAW-tree files byte-read | 96 | 96 | PASS |

Every identity and occurrence was consumed. Family identity/RAW totals were independently recounted from the W09 ledgers and matched all 32 family rows. The independent-taxonomy family key matched the current signal ledger for every one of 24,576 identities. No sampling or truncation was used.

## Queue reconciliation

```text
CURRENT_QUEUE_ROWS = 13
QUEUE_RECONCILED = 13/13
MISSING_QUEUE_ROWS = 0
DUPLICATE_QUEUE_ROWS = 0
CURRENT_W09_QUEUE_IDENTITY = EXACT
SEARCH_GAP_ROWS_CHALLENGED = PSQ001|PSQ004|PSQ005
PSQ001 = CLOSED_BY_Q001_Q002_Q003
PSQ004 = CLOSED_BY_Q019
PSQ005 = SURVIVES_AS_W10C001_NOT_EXECUTED
OWNER_FACT_ROWS_PROVIDER_CANDIDATES = 0
PSQ006_REPROBE = false
PSQ007_REPROBE = false
PSQ008_REPROBE = false
PSQ010_REPROBE = false
PSQ011_PROVIDER_CANDIDATE = false
```

Q001/Q002/Q003 tested the same three exact names with the product-class OR scope. Their durable results contain no result/association rows. Q001's empty object is deliberately recorded as fields unknown, not rewritten as `totalCount=0`. Q019 tested the same Blood & Sand brand+product scope and returned `totalCount=1` with zero materialized result/association rows. Replaying either question has zero incremental gain.

S053 contributes 476 broad `Аум` occurrences/identities (317 HOLD, 159 EXCLUDE). Q005 contributes 23 occurrences/identities for qualified `Ом` (19 KEEP, 3 HOLD, 1 EXCLUDE). Neither answers the distinct qualified `Аум` question, so only W10C001 survives as an inert future candidate.

## Candidate hard gates

```text
SURVIVING_NEW_PROVIDER_CANDIDATES = 1
FIRST_EXECUTION_CANDIDATE = W10C001
EXECUTION_STATUS = NOT_EXECUTED
LITERAL_DUPLICATE = false
SEMANTIC_DUPLICATE = false
INCREMENTAL_GAIN = true
NEGATIVE_RESULT_VALUE = true
STOP_CONDITION = true
MAX_REQUESTS = 1
ESTIMATED_COST_RUB = 0.02 (recheck immediately before any later execution)
BRIDGE_SCHEMA_COMPATIBILITY = PASS
```

The candidate uses only current local Bridge fields (`getTop`, phrase, `numPhrases=2000`, regions `225`, device `DEVICE_ALL`). This is an inert TSV plan row, not a Bridge command or execution authorization. Official operator meaning, provider semantics, quotas and price remain separated from repository-side envelope validation.

## Durable evidence reuse

- PSQ006: 213 source occurrences / 211 identities from S014+S049; accepted W09 qualified-evidence fixture reused.
- PSQ007: 2,412 source occurrences / 2,409 identities across its five named seeds; accepted W09 collision fixture reused.
- PSQ008: 703 source occurrences / 688 identities across S019+S020+Q015; accepted W09 qualified-evidence fixture reused.
- PSQ010: E013 `!чётки` RAW SHA-256 verified, 2,000 results + 19 associations; replay is false.

Historical evidence remains evidence, not final relevance, intent, inventory or page authority.

## Regression and boundary result

All 17 blocking regression checks pass. Provider calls: Wordstat 0, ordinary Yandex Search 0, GenSearch 0, AI-search 0. Step03A mutations 0, Step03B mutations 0, accepted W09 mutations 0. Step06 started: false. Final intent, SERP clustering, query-to-page ownership and IA: not performed.

`STEP03_RAW_TREE_AGGREGATE_SHA256 = 13533746e2180e76251e33f209249ca1feb9dee6da02765248b17ad79e842a3a`
