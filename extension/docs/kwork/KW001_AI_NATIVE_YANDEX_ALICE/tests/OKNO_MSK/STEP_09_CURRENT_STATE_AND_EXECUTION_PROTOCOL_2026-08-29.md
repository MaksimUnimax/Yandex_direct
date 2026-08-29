# KW-001 / OKNO-MSK — Step 09 corrected current state and execution protocol

Date: 2026-08-29  
Status: **CURRENT STEP-09 EXECUTION / ANALYSIS AUTHORITY**

For causal history and live evidence, read:

- `STEP_09_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md`
- `STEP_09_LIVE_CANARY_AND_BATCH_EXECUTION_CORRECTION_2026-08-29.md`
- `STEP_09_LIVE_R2_PROJECTION_RECEIPT_2026-08-29.md`
- `STEP_09_SERP_R2_PROJECTION_INDEX.md`
- `STEP_09_COLLECTION_METHOD_AND_IMMEDIATE_PERSISTENCE_POSTMORTEM_2026-08-29.md`
- `STEP_09_NEXTN_LIVE_CHUNK_VALIDATION_2026-08-29.md`

Bridge implementation authority:

- `extension/docs/SEARCH_BATCH_NEXTN100_V0_1_2_CHANGELOG_AND_ACCEPTANCE_2026-08-29.md`

## Current truth

```text
OWNER_AUTHORIZATION_FOR_STEP09 = true
ORDINARY_SEARCH_ONLY = true
GEN_SEARCH_ALLOWED = false
REGION = 213
INITIAL_TRANCHE_PROBES = 75
AUTHORIZED_MAX_REQUESTS = 80
AUTHORIZED_MAX_COST_RUB = 39.04
REVIEW_SEARCH_TOTAL = 944
DIRECT_REVIEW_SEARCH_ROWS_IN_INITIAL_TRANCHE = 45
UNRESOLVED_UNPROBED_REVIEW_SEARCH_ROWS = 899
TRACEABILITY_COMPLETE = true
FULL_SERP_EVIDENCE_COVERAGE = false
PRE_SERP_TRANSFER_ALLOWED = false
INITIAL_TRANCHE_SEMANTIC_QA = PASS_AS_INITIAL_BOUNDED_TRANCHE_ONLY

PROVIDER_ACQUISITION_INITIAL_75 = COMPLETE
PROVIDER_REQUESTS_EXECUTED = 75
PROVIDER_REQUESTS_SUCCEEDED = 75
PROVIDER_FAILED_TERMINAL = 0
PROVIDER_OUTCOME_UNKNOWN = 0
PROVIDER_ESTIMATED_COST_RUB = 36.600
NORMALIZED_DIRECT_SERPS_AVAILABLE = 75
NORMALIZED_RANKED_RESULTS_AVAILABLE = 750

FIRST_CANARY_COMPLETENESS_GATE = PASS
R2_JOB_ID = kw001-okno-msk-search-step09-20260829-r2
R2_JOB_STATUS = COMPLETED
R2_SUCCEEDED = 74
R2_PENDING = 0
R2_OUTCOME_UNKNOWN = 0
R2_PROJECTION_COMPLETE = true

ORIGINAL_JOB_ID = kw001-okno-msk-search-step09-20260829
ORIGINAL_JOB_CURRENT_RUNTIME_STATE = NOT_FOUND
ORIGINAL_JOB_CANCEL_REQUEST_EXECUTED = false
ORIGINAL_JOB_CANCEL_PROVIDER_COST_RUB = 0

REPOSITORY_NORMALIZED_SERP_LEDGER_COMPLETE = true
R2_NORMALIZED_PROJECTION_ROWS_PERSISTED = 740
CANARY_FULL_ROWS_PERSISTED = 10
COMBINED_NORMALIZED_RANKED_ROWS_PERSISTED = 750
R2_RAW_PER_ITEM_PROVIDER_XML_LEDGER_COMPLETE = false
R2_PER_ITEM_PROVIDER_REQUEST_ID_LEDGER_COMPLETE = false

YANDEX_MARKETING_BRIDGE_SOURCE_VERSION = 0.1.2
SEARCH_BATCH_NEXT_N_SUPPORTED = true
SEARCH_BATCH_NEXT_N_MANUAL_ONLY = true
SEARCH_BATCH_NEXT_N_COUNT_MIN = 1
SEARCH_BATCH_NEXT_N_COUNT_MAX = 100
LIVE_NEXT_N_REQUESTED_COUNTS_TESTED = 4,10,25,31
LIVE_NEXT_N_MAX_REQUESTED_COUNT_TESTED = 31

STEP09_COMPLETE = false
STEP10_ALLOWED = false
```

## Important meaning of 75/75

The paid Search acquisition target for the initial bounded tranche is complete.

This does **not** mean Step 09 is analytically accepted and does not mean all 944 `REVIEW_SEARCH` rows have direct SERP evidence.

The 75 probes remain:

```text
REVIEW_STRATIFIED_SAMPLE
= direct diagnostic query only; no automatic transfer to other rows.

NONEXACT_DUPLICATE_VARIANT
= direct pairwise comparison input.

STEP1_BOUNDARY_OR_CORE_ANCHOR
= direct contrast/control query for a declared architecture question.
```

No automatic transfer by:

```text
corrected_reason
source_id
Wordstat seed/provenance
lexical similarity
absence of contradiction
```

## Collection method

Step 09 uses ordinary Yandex Search through the Search Batch service-specific protocol.

Frozen provider/search profile:

```text
protocol = SEARCH_BATCH_API_V1
provider = ordinary Yandex Search
searchType = SEARCH_TYPE_RU
region = 213 / Moscow
page = 0
groupsOnPage = 10
docsInGroup = 1
groupMode = GROUP_MODE_FLAT
sortMode = SORT_MODE_BY_RELEVANCE
sortOrder = SORT_ORDER_DESC
familyMode = FAMILY_MODE_MODERATE
fixTypoMode = FIX_TYPO_MODE_ON
provider response format = FORMAT_XML
normalized evidence = TOP-10 rank/url/domain/title
```

No GenSearch provider call is allowed in Step 09.

## Live acquisition structure and tested quantity

Canary job:

```text
job_id = kw001-okno-msk-search-step09-20260829
successful observed canary = 1
query = аксессуары для пластиковых окон
request_id = search-batch-06923ff5-1455-4ca9-99f3-d8778976c96a
item_id = kw001-okno-msk-search-step09-20260829:ca2ccadf3fb1cddc
http_status = 200
result_count = 10
response_format = FORMAT_XML
estimated cost = 0.488 RUB
```

R2 job on the patched Bridge:

```text
job_id = kw001-okno-msk-search-step09-20260829-r2
queries = 74
status = COMPLETED
requests_started = 74
succeeded = 74
failed_terminal = 0
outcome_unknown = 0
estimated cost = 36.112 RUB
projection total_successful = 74
projection topN = 10
projection next_offset = null
```

Combined:

```text
75 real provider requests
75 successes
0 terminal failures
0 outcome unknown
36.600 RUB estimated cumulative cost
750 normalized ranked results
```

### Actual live `nextN` sizes tested

The live rollout explicitly tested these requested `nextN.count` values:

```text
4
10
25
31
```

Therefore:

```text
LIVE_NEXT_N_REQUESTED_COUNTS_TESTED = [4, 10, 25, 31]
LIVE_NEXT_N_MAX_REQUESTED_COUNT_TESTED = 31
```

This is known live execution history and supersedes the earlier incorrect wording that exact tested chunk sizes were unknown.

Important distinction:

```text
TESTED_REQUESTED_COUNTS = [4,10,25,31]
!=
A CLAIM THAT 4+10+25+31 IS THE COMPLETE R2 EXECUTION PARTITION
```

`nextN.count` is an upper bound for that invocation. Actual per-call executions are defined by `confirmed_provider_executions` and can stop early because of remaining work, policy/cost limits, terminal error or UNKNOWN. The authoritative completed R2 job-level accounting remains 74/74.

### Local hard-bound test

Separately from live provider work:

```text
count = 100
```

was verified locally as a bounded protocol/runtime case. With only three remaining synthetic items, the runtime performed exactly three provider boundaries and stopped at completion.

Therefore:

```text
COUNT_100_LOCAL_BOUNDED_TEST = PASS
COUNT_100_LOCAL_BOUNDED_TEST != 100 LIVE PROVIDER REQUESTS IN ONE CHUNK
LARGEST_EXPLICIT_LIVE_REQUESTED_COUNT_TESTED = 31
HARD_PROTOCOL_CEILING = 100
```

Canonical detail authority:

`STEP_09_NEXTN_LIVE_CHUNK_VALIDATION_2026-08-29.md`

## Critical process error and mandatory correction

During R2 acquisition successful provider work continued while the project relied on Bridge `chrome.storage.local` plus chat/result delivery instead of immediately copying each returned result/chunk into the repository before the next paid chunk.

This was a workflow error.

False assumption:

```text
BRIDGE_INTERNAL_DURABILITY == PROJECT_EVIDENCE_DURABILITY
```

Correct rule:

```text
BRIDGE_INTERNAL_DURABILITY != PROJECT_EVIDENCE_DURABILITY
CHAT_DELIVERY != PROJECT_EVIDENCE_DURABILITY
JOB_COMPLETION != REPOSITORY_EVIDENCE_PERSISTENCE
```

The danger is concrete: extension identity/storage, browser/profile state, job lifecycle, tab/session delivery or connection state can disappear after the provider has already been paid. The original canary job later became `SEARCH_BATCH_JOB_NOT_FOUND` in the current runtime. R2 remained available long enough for recovery through `projection`; that must not be treated as an acceptable primary persistence strategy.

The delayed write also reduced evidence fidelity: R2 normalized TOP-10 rows were recoverable, but the final projection did not expose all original per-item raw XML, provider request IDs, snippets or modtime fields.

Mandatory gate from now on:

```text
PROVIDER_RESULT_OR_NEXT_N_CHUNK_RECEIVED
-> PARSE_AND_ACCOUNT
-> IMMEDIATE_REPOSITORY_WRITE
-> GITHUB_READ_BACK_QA
-> COVERAGE_AND_COST_CHECKPOINT
-> ONLY_THEN_NEXT_PAID_CHUNK
```

If write/read-back QA fails:

```text
NEXT_PAID_CHUNK_ALLOWED = false
```

Non-repeat controls:

```text
PROVIDER_SUCCESS_WITHOUT_PROJECT_WRITE = PROCESS_FAILURE
NEXT_PAID_CHUNK_BEFORE_READBACK_QA = PROHIBITED
RUNTIME_STORAGE_AS_ONLY_EVIDENCE_COPY = PROHIBITED
CHAT_AS_ONLY_EVIDENCE_COPY = PROHIBITED
JOB_COMPLETED_WITHOUT_REPOSITORY_LEDGER = NOT_ACCEPTED
```

Full causal postmortem and corrected procedure:

`STEP_09_COLLECTION_METHOD_AND_IMMEDIATE_PERSISTENCE_POSTMORTEM_2026-08-29.md`

## Correction: do not infer current job existence from last observed state

After the canary, the original job's last observed state had 74 pending items. A later cleanup attempt tried to cancel that job and received:

```text
code = SEARCH_BATCH_JOB_NOT_FOUND
stage = BATCH_RUNTIME
request_executed = false
automatic_retry = false
```

Therefore:

```text
LAST_OBSERVED_JOB_STATE != CURRENT_LIVE_JOB_EXISTENCE
```

The current live runtime does not contain the original job under that ID. Do not infer why it disappeared without additional evidence.

No provider request and no provider cost were caused by the failed cancel.

## Manual / protocol controls

Observed service-specific rule remains:

```text
one Manual block = exactly one SEARCH_BATCH_API_V1 command
```

Do not infer Search-batch Manual admission from the generic multi-command Manual contract.

Current repository protocol/source is synchronized to Bridge `0.1.2` and now includes:

```text
start
next
nextN
status
pause
resume
cancel
projection
overlapPage
```

`nextN` is explicitly Manual-only and accepts integer `count` from 1 through 100.

Canonical control remains:

```text
REPOSITORY_PROTOCOL_SNAPSHOT_MUST_BE_VERIFIED_AGAINST_INSTALLED_RUNTIME_BEFORE_LIVE_USE
```

## Evidence-persistence distinction

The R2 projection supplies normalized reusable TOP-10 rows. Those normalized rows are now durably persisted in four repository TSV parts covering frozen query indexes 2–75. The previously persisted canary covers index 1.

Persistence truth:

```text
PROVIDER_ACQUISITION_COMPLETE = true
NORMALIZED_PROJECTION_COMPLETE = true
REPOSITORY_NORMALIZED_SERP_LEDGER_COMPLETE = true
R2_NORMALIZED_PROJECTION_ROWS_PERSISTED = 740
CANARY_FULL_ROWS_PERSISTED = 10
COMBINED_NORMALIZED_RANKED_ROWS_PERSISTED = 750
```

The R2 recovery projection did not expose complete raw per-item XML or provider request IDs for every R2 request. Those unavailable fields were not invented.

Therefore:

```text
R2_RAW_PER_ITEM_PROVIDER_XML_LEDGER_COMPLETE = false
R2_PER_ITEM_PROVIDER_REQUEST_ID_LEDGER_COMPLETE = false
```

Canonical persistence authority and re-read QA:

```text
STEP_09_SERP_R2_PROJECTION_INDEX.md
STEP_09_SERP_R2_PROJECTION_RAW_PART_01.tsv
STEP_09_SERP_R2_PROJECTION_RAW_PART_02.tsv
STEP_09_SERP_R2_PROJECTION_RAW_PART_03.tsv
STEP_09_SERP_R2_PROJECTION_RAW_PART_04.tsv
STEP_09_SERP_RESULTS.tsv
```

## Step-09 completion remains blocked until

```text
1. normalized SERP persistence for all 75 probes — PASS;
2. attempted-provider accounting is reconciled;
3. available durable per-item identifiers/raw evidence are reconciled without provider replay;
4. eight active nonexact duplicate comparisons are produced from real SERPs;
5. declared boundary/evidence questions are decided;
6. all 944 REVIEW_SEARCH rows remain explicitly accounted for as directly resolved, validly transferred, or unresolved;
7. semantic and provider QA pass;
8. no Step-10 clustering/page-ownership decision is silently performed inside Step 09.
```

Until then:

```text
STEP09_COMPLETE = false
STEP10_ALLOWED = false
```
