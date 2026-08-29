# KW-001 / OKNO-MSK — Step 09 corrected current state and execution protocol

Date: 2026-08-29  
Status: **CURRENT STEP-09 EXECUTION / ANALYSIS AUTHORITY**

For causal history and live evidence, read:

- `STEP_09_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md`
- `STEP_09_LIVE_CANARY_AND_BATCH_EXECUTION_CORRECTION_2026-08-29.md`
- `STEP_09_LIVE_R2_PROJECTION_RECEIPT_2026-08-29.md`
- `STEP_09_SERP_R2_PROJECTION_INDEX.md`

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

## Live acquisition structure

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

R2 job:

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
75 requests
75 successes
0 terminal failures
0 outcome unknown
36.600 RUB estimated cumulative cost
750 normalized ranked results visible across canary + R2 projection
```

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

The GitHub branch version of `search_batch_protocol.js` observed earlier still listed only:

```text
start
next
status
pause
resume
cancel
projection
overlapPage
```

However live result envelopes now include fields such as `chunk`; therefore installed live Bridge behavior and branch code must not be assumed identical without verification.

Canonical control:

```text
REPOSITORY_PROTOCOL_SNAPSHOT != AUTOMATICALLY_CURRENT_INSTALLED_RUNTIME
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
