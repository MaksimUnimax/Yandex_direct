# KW-002 / BLOOD & SAND — STEP08 PREPARATION METHOD + EXECUTION GATE

Date: 2026-09-18
Status: **PREPARATION PASS / FULL-VOLUME WORK RECONCILIATION REQUIRED / PROVIDER NOT RELEASED**

## 1. Whole Kwork goal

Build from scratch a client-ready semantic core and planned site architecture for modern Yandex with complete evidence lineage from business facts through demand, current Search/SERP, clustering, page ownership, AI-search reconciliation and final deliverables.

## 2. Current roadmap

```text
00 Scope/source/delivery freeze                         COMPLETE
01 Business + assortment model                         COMPLETE
02 Seed/acquisition design                             COMPLETE
03 Primary Wordstat                                    COMPLETE
03A Normalization                                      COMPLETE
03B Conservative sanitation                            COMPLETE
04 Preliminary family/topic/task triage                ACCEPTED
05 Targeted coverage expansion                         PASS
06 Current Yandex organic competitors                  DURABLE PASS
07 Competitor semantic expansion                       PASS_ACCEPTED_WITH_EXTERNAL_SOURCE_LIMITATION
08 Competitor-derived Wordstat validation              PREPARATION / CURRENT
09 Candidate semantic master + reserve freeze          NOT STARTED
10 Relevance / task / intent / priority                NOT STARTED
11 Delivery scope + Search freeze                      NOT STARTED
12 Current Yandex Search evidence                      NOT STARTED
13 SERP + task-first clustering                        NOT STARTED
14 Query->page ownership + Search IA                   NOT STARTED
15 AI-search diagnostic selection                      NOT STARTED
16 AI-search evidence                                  NOT STARTED
17 Search vs AI reconciliation                         NOT STARTED
18 Final core + IA + Page Jobs + links                 NOT STARTED
19 Client deliverables                                 NOT STARTED
20 Final QA / recipient acceptance                     NOT STARTED
21 Productization measurement                          NOT STARTED
22 Job close                                           NOT STARTED
```

## 3. Current accepted input

Current state authority:

`CURRENT_STATE_POINTER_2026-09-18_R10.json`

Accepted Step07 handoff:

```text
CANDIDATE_IDENTITIES = 2172
STEP08_ELIGIBLE = 794
NEW_CANDIDATE = 787
POSSIBLE_VARIANT = 7
PAGE_PROVENANCE_ROWS = 3948
RANKING_QUERY_OBSERVATIONS = 0
KNOWN_RECALL_LIMITATION = ACTIVE
```

The ranking-query limitation does not block Step08 and must remain visible downstream.

## 4. Step08 goal

For every one of the 794 eligible Step07 candidates:

1. define the exact unresolved demand question;
2. reconcile it against all current durable KW-002 Wordstat/normalized/sanitized evidence;
3. prove whether existing evidence answers the same question;
4. if not answered, decide whether a new Wordstat seed has incremental information gain;
5. design the smallest complete provider seed set;
6. define query/operator/depth/outcome/persistence/reopen contracts before any provider call.

Step08 preparation MUST NOT equate:

```text
794 ELIGIBLE CANDIDATES = 794 PROVIDER REQUESTS
```

## 5. Why full-volume Work is required now

The preparation requires a complete join and semantic reconciliation across:

- 794 Step07 eligible candidates;
- 3,948 Step07 page provenance rows;
- the accepted Step03A normalized universe;
- corrected Step03B KEEP/HOLD/EXCLUDE authorities;
- existing Step03 Wordstat acquisition lineage/raw receipts;
- accepted Step05 reuse/acquisition evidence.

These are large structured authorities. Sampling or first-N analysis would violate the active Level1 Work/data-volume rules.

Therefore:

```text
CURRENT_EXECUTION_UNIT = FULL 794-ROW PRE-ACQUISITION RECONCILIATION
WORK_TRIGGER = TRUE
SAMPLE = FORBIDDEN
PROVIDER_CALLS_IN_WORK = 0
```

## 6. Method

### Stage A — full-volume existing-evidence reconciliation in Work

Process 794/794.

For each candidate:

```text
STEP07 CANDIDATE
-> EXACT/NORMALIZED IDENTITY CHECK
-> EXISTING PROVIDER-EVIDENCE SCOPE CHECK
-> DOES OLD EVIDENCE ANSWER THIS EXACT QUALIFIED QUESTION?
   YES -> REUSE / NO NEW CALL
   NO  -> INFORMATION-GAIN REVIEW
-> IF NEW EVIDENCE NEEDED:
   DESIGN BOUNDED SEED / RESEARCH MODE / OPERATORS / DEPTH / OUTCOME CONTRACT
```

Do not close a narrower question from merely related broad evidence.

Do not create one provider request per product name/heading by default.

A single acquisition seed may cover several candidates only when one explicit information question legitimately covers those candidate identities without collapsing distinct referents.

### Stage B — Main Chat return QA

After Work returns:

- verify 794/794 accounting;
- verify evidence locators and scope matches;
- challenge provider seeds for duplication and unnecessary calls;
- recheck depth/operator contracts;
- calculate final request count/cost/quota plan;
- publish/accept preparation artifacts.

### Stage C — provider execution release later

Only after Stage B passes may Main Chat separately release Wordstat execution.

No Wordstat command is emitted by this preparation gate.

## 7. Current provider facts

Frozen job region:

```text
REGION = RUSSIA
YANDEX_REGION_ID = 225
LANGUAGE = RUSSIAN
```

Current intended device mode:

`DEVICE_ALL`

Current provider:

`Wordstat GetTop`

Current official capabilities verified 2026-09-18:

```text
numPhrases = 1..2000
phrase max = 400 chars
regions max = 100
devices max = 3
results[] + associations[] + totalCount
Wordstat quota = 10 requests/sec; 100 requests/hour
GetTop price = 20 RUB / 1000 requests incl. VAT
```

Current YMB batch capability:

```text
max phrases/job = 500
start = local only / request_executed=false
next = at most one provider item
automatic_retry=false
```

## 8. Depth policy

Do not hard-code a magic universal depth merely because 2000 is available.

Preparation must classify each provider seed by information purpose.

For a recall-first discovery seed, 2000 is normally the leading candidate because:

- GetTop supports it;
- billing is per request, not per returned phrase;
- smaller limits can discard observable vocabulary without saving provider calls.

But the provider manifest must still state why the selected depth answers the specific question.

```text
RETURNED_RESULTS_ROWS == REQUESTED_DEPTH
!= SEMANTIC_UNIVERSE_COMPLETE
```

## 9. Operator policy

Classify every provider seed as one of:

```text
DISCOVERY_RECALL_FIRST
PRECISION_VALIDATION
EXACT_FORM_TEST
COLLISION_DIAGNOSTIC
```

Then justify the operator shape.

No automatic morphology fixation.
No automatic quoting.
No automatic grouped-OR use merely to reduce request count.

## 10. Provider outcome contract

Every future provider seed must predefine:

| Outcome | Meaning |
|---|---|
| `SUCCESS_WITH_ROWS` | bounded positive provider evidence; persist/readback then normalize/sanitize |
| `SUCCESS_WITH_ZERO_ROWS` | valid bounded zero for this query/operator/region/device/snapshot only |
| `SUCCESS_BUT_EVIDENCE_INCOMPLETE` | unresolved; no semantic closure |
| `VALIDATION_FAILURE` | request contract failed; no semantic conclusion |
| `PROVIDER_FAILURE` | no semantic answer |
| `OUTCOME_UNKNOWN` | duplicate-execution risk; blind retry forbidden |

```text
NO_RETRY != NEGATIVE_EVIDENCE
ZERO_ROWS != UNIVERSAL_ZERO_DEMAND
```

## 11. RAW / downstream contract

After any later executed Wordstat request:

```text
ACTUAL BRIDGE RESULT
-> COMPLETE RAW ENVELOPE + RESULTS + ASSOCIATIONS + ERROR TRUTH
-> DURABLE STORAGE
-> REMOTE READBACK
-> REQUEST/ROW/FIELD RECONCILIATION
-> STEP03A-COMPATIBLE NORMALIZATION
-> STEP03B-COMPATIBLE SANITATION
-> STEP08 RECONCILIATION
```

No next provider request is allowed before the current RAW persistence/readback gate passes.

## 12. Relevant prior failures / non-repeat controls

```text
F03 / provider success != durable completion
F03A / destructive normalization forbidden
F03B / lexical shortcuts and ambiguity destruction forbidden
F05-1 / duplicate provider acquisition forbidden
F05-8 / operator choice must be justified
F05-9 / broad evidence cannot close narrower qualified question
F05-10 / temporal evidence != permanent truth
F05-12 / stale provider schema/limits/pricing forbidden
F05-13 / provider RAW != accepted semantic output
F05-14 / next call before RAW readback forbidden
F05-15 / provider probe without information-gain contract forbidden
F05-16 / zero-result overclaim forbidden
F05-17 / Work only when large-data trigger exists
F07-2 / missing ranking-query reverse-index remains an explicit recall limitation
```

## 13. Step08 preparation required outputs

Work must return:

1. `STEP08_CANDIDATE_PRE_ACQUISITION_RECONCILIATION.csv` — exactly 794 rows;
2. `STEP08_EXISTING_EVIDENCE_REUSE_REGISTER.csv`;
3. `STEP08_PROVIDER_SEED_MANIFEST.csv`;
4. `STEP08_PRE_ACQUISITION_KNOWN_FAILURE_REGRESSION_MATRIX.csv`;
5. `STEP08_PRE_ACQUISITION_QA.md`;
6. `STEP08_PREPARATION_HANDOFF_MANIFEST.json`.

Schema authority:

`STEP_08_PREPARATION_OUTPUT_SCHEMA_CONTRACT_2026-09-18.json`

## 14. Preparation PASS gates

```text
LIVE_AUTHORITY = PASS
MAIN_CHAT_FULL_RULE_REREAD = PASS
FRESH_EXTERNAL_RESEARCH = PASS
CURRENT_BRIDGE_RECHECK = PASS
STEP08_ELIGIBLE_ROWS = 794
WORK_TRIGGER = TRUE
WORK_FULL_VOLUME = 794/794
REUSE_FIRST_REQUIRED = true
PROVIDER_CALLS_DURING_PREPARATION = 0
WORDSTAT_EXECUTION_RELEASED = false
SEARCH_CALLS = 0
AI_SEARCH_CALLS = 0
GENSEARCH_CALLS = 0
```

Preparation is not Step08 final PASS.

It only releases the full-volume pre-acquisition reconciliation into Work.

## 15. Plain-language meaning

Step07 gave us 794 competitor-derived candidates worth checking. We do not send all 794 blindly to Yandex. First, Work compares all 794 against the large Wordstat evidence we already bought and saved. Existing evidence is reused wherever it really answers the same question. Only the remaining genuinely unanswered directions become a new Wordstat queue. No provider request is made during this preparation.
