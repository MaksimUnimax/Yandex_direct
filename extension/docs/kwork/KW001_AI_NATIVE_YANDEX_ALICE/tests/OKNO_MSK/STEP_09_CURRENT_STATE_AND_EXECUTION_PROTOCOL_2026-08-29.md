# KW-001 / OKNO-MSK — Step 09 corrected current state and execution protocol

Date: 2026-08-29  
Status: **CURRENT STEP-09 EXECUTION AUTHORITY**

This file is the short operational authority after the Step-09 manifest audit and first live ordinary-Search canary. For causal explanations, read:

- `STEP_09_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md`
- `STEP_09_LIVE_CANARY_AND_BATCH_EXECUTION_CORRECTION_2026-08-29.md`

## Current truth

```text
OWNER_AUTHORIZATION_FOR_STEP09 = true
ORDINARY_SEARCH_ONLY = true
GEN_SEARCH_ALLOWED = false
REGION = 213
INITIAL_TRANCHE_PROBES = 75
AUTHORIZED_MAX_REQUESTS = 80
ESTIMATED_INITIAL_TRANCHE_COST_RUB = 36.6
AUTHORIZED_MAX_COST_RUB = 39.04
REVIEW_SEARCH_TOTAL = 944
DIRECT_REVIEW_SEARCH_ROWS_IN_INITIAL_TRANCHE = 45
UNRESOLVED_UNPROBED_REVIEW_SEARCH_ROWS = 899
TRACEABILITY_COMPLETE = true
FULL_SERP_EVIDENCE_COVERAGE = false
PRE_SERP_TRANSFER_ALLOWED = false
PRE_SERP_TRANSFER_LINKS = 0
INITIAL_TRANCHE_SEMANTIC_QA = PASS_AS_INITIAL_BOUNDED_TRANCHE_ONLY
BOUNDED_JOB_CREATED = true
PROVIDER_REQUESTS_EXECUTED = 1
PROVIDER_REQUESTS_SUCCEEDED = 1
PROVIDER_REQUESTS_PENDING = 74
PROVIDER_OUTCOME_UNKNOWN = 0
PROVIDER_COST_INCURRED_RUB = 0.488
COMPLETE_SAVED_SERPS = 1
FIRST_CANARY_COMPLETENESS_GATE = PASS
SEARCH_BATCH_CHUNK_ACTION_AVAILABLE = false
MANUAL_SEARCH_BATCH_SINGLE_COMMAND_REQUIRED = true
STEP09_COMPLETE = false
STEP10_ALLOWED = false
```

## Active authorities

```text
STEP_09_ORDINARY_YANDEX_SEARCH_PRE_STEP_REVIEW_2026-08-29.md
STEP_09_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md
STEP_09_LIVE_CANARY_AND_BATCH_EXECUTION_CORRECTION_2026-08-29.md
STEP_09_INITIAL_TRANCHE_SEMANTIC_QA.json
STEP_09_SEARCH_PROBE_MANIFEST.tsv
STEP_09_REVIEW_SEARCH_COVERAGE.tsv
STEP_09_SEARCH_PROBE_MANIFEST_QA.json
STEP_09_SEARCH_PROBE_MANIFEST_RECONCILIATION.md
STEP_09_SERP_RESULTS.tsv
```

Where the original pre-step conflicts with the post-audit correction or live-canary correction, the newer correction authority supersedes the earlier wording.

## Meaning of the initial 75 probes

The list is **not** a 944-row Search cluster map.

```text
REVIEW_STRATIFIED_SAMPLE
= direct diagnostic query only; no pre-SERP transfer to other rows in the same cleanup/source stratum.

NONEXACT_DUPLICATE_VARIANT
= direct pairwise comparison input.

STEP1_BOUNDARY_OR_CORE_ANCHOR
= direct contrast/control query for a declared architecture question.
```

`corrected_reason`, `source_id`, Wordstat provenance and lexical similarity are sampling/review metadata only. They cannot establish shared intent or same-page compatibility.

## Live execution truth

The frozen bounded job exists:

```text
job_id = kw001-okno-msk-search-step09-20260829
queue = 75
maxRequests = 75
maxCostRub = 39.04
start provider requests = 0
```

The first paid canary has completed successfully:

```text
query = аксессуары для пластиковых окон
request_id = search-batch-06923ff5-1455-4ca9-99f3-d8778976c96a
item_id = kw001-okno-msk-search-step09-20260829:ca2ccadf3fb1cddc
http_status = 200
result_count = 10
response_format = FORMAT_XML
request_executed = true
succeeded = 1
pending = 74
outcome_unknown = 0
estimated cumulative cost = 0.488 RUB
```

The complete observed TOP-10 is persisted in `STEP_09_SERP_RESULTS.tsv`.

Observed dominant pattern for the exact query: transactional/product-category results for window accessories/fittings. No transfer to other phrases is authorized from this single SERP.

## Live Manual admission correction

The installed bridge rejected a Manual block containing `start + next` with:

```text
code = BATCH_SINGLE_COMMAND_REQUIRED
request_executed = false
```

Therefore the current service surface must be treated as:

```text
one Manual block = exactly one SEARCH_BATCH_API_V1 command
```

Do not infer Search-batch Manual admission from the generic multi-command Manual contract.

## Current Search-batch protocol gap

The current Search-batch protocol exposes:

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

There is no validated bounded `nextN` / `runChunk` action.

Therefore the currently installed extension can continue safely only one paid `next` per Manual interaction. That is functionally safe but operationally inefficient for the remaining 74 queries.

The preferred product correction is an explicit bounded chunk action that executes items serially, persists each result before advancing, respects maxRequests/maxCostRub, and stops on OUTCOME_UNKNOWN/terminal failure. Do not work around the limitation by weakening validation and concatenating repeated `next` commands unless that alternative is independently designed and validated.

## Project completeness gate for each observed paid result

Required evidence:

```text
1. governed item outcome is known;
2. request_executed truth is known;
3. provider request_id / item_id / job_id are preserved;
4. complete raw ordinary-Search payload is durably present;
5. normalized ranked result rows are readable;
6. observed_result_count reconciles with saved ranked rows;
7. query text, region and normalized request parameters are preserved;
8. request/cost accounting is updated;
9. no OUTCOME_UNKNOWN exists for the current item;
10. job-specific evidence reference can be reused later without another provider call.
```

Canary #1 passes all ten.

## Failure handling

```text
OUTCOME_UNKNOWN
=> STOP; no automatic replay; no next paid item.

request_executed=false + pre-provider/local validation failure
=> preserve error; understand cause before governed retry.

request_executed=true + terminal provider error
=> record as attempted paid item; do not blindly repeat.

result payload incomplete/unreadable
=> PROJECT_RESULT_INCOMPLETE; STOP even if transport reports SUCCEEDED.
```

## Evidence transfer after Search

A direct SERP may be used beyond the exact query only after a separate explicit transfer decision records why the target phrase shares the same user task and why its modifiers do not materially alter intent/result type.

Until such a record exists:

```text
non-probed REVIEW_SEARCH row = UNRESOLVED_UNPROBED
```

No automatic transfer by:

```text
corrected_reason
source_id
Wordstat seed/provenance
lexical similarity
absence of contradiction
```

## Step-09 completion remains blocked until

```text
all attempted provider items have governed outcomes;
all successful provider results are complete and reusable;
SERP result ledger exists and is complete for attempted probes;
declared duplicate/boundary comparisons are produced;
analytical evidence decisions are produced;
all 944 REVIEW_SEARCH rows are either directly/validly resolved or explicitly unresolved;
provider and semantic QA both pass;
request/cost accounting reconciles;
no Step-10 clustering/page-ownership decision is silently performed inside Step 09.
```
