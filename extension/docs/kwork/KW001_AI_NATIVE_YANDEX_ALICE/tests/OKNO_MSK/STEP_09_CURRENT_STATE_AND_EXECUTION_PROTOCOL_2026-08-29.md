# KW-001 / OKNO-MSK — Step 09 corrected current state and execution protocol

Date: 2026-08-29  
Status: **CURRENT STEP-09 EXECUTION AUTHORITY**

This file is the short operational authority after the Step-09 manifest audit. For the causal explanation, read `STEP_09_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md`.

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
PROVIDER_REQUESTS_EXECUTED = 0
PROVIDER_COST_INCURRED_RUB = 0
STEP09_COMPLETE = false
STEP10_ALLOWED = false
```

## Active authorities

```text
STEP_09_ORDINARY_YANDEX_SEARCH_PRE_STEP_REVIEW_2026-08-29.md
STEP_09_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md
STEP_09_INITIAL_TRANCHE_SEMANTIC_QA.json
STEP_09_SEARCH_PROBE_MANIFEST.tsv
STEP_09_REVIEW_SEARCH_COVERAGE.tsv
STEP_09_SEARCH_PROBE_MANIFEST_QA.json
STEP_09_SEARCH_PROBE_MANIFEST_RECONCILIATION.md
```

Where the original pre-step conflicts with the post-audit correction, the postmortem and this file supersede the earlier wording.

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

## Provider interaction protocol

### Start

Run the frozen `SEARCH_BATCH_API_V1 start` from `STEP_09_SEARCH_BATCH_START_COMMAND.txt`.

Expected truth:

```text
request_executed = false
provider_requests_started = 0
job exists with frozen 75-query queue and bounded maxRequests/maxCostRub
```

If start performs or reports a provider request, STOP.

### Paid iteration

Issue exactly **one**:

```text
SEARCH_BATCH_API_V1
{"action":"next","jobId":"kw001-okno-msk-search-step09-20260829"}
```

Then STOP issuing paid commands until the current item passes the project completeness gate.

### Project completeness gate after each `next`

Required before another paid `next`:

```text
1. governed item outcome is known;
2. request_executed truth is known;
3. provider request_id / item_id / job_id are preserved;
4. complete raw ordinary-Search payload is durably present;
5. normalized ranked result rows are readable;
6. observed_result_count reconciles with saved ranked rows;
7. query text, region and normalized request parameters are preserved;
8. estimated/actual request accounting is updated;
9. no OUTCOME_UNKNOWN exists for the current item;
10. job-specific evidence reference can be reused later without another provider call.
```

Only after all ten are true may the next paid `next` be issued.

### Failure handling

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

## Explicitly forbidden execution shape

For Step 09, do not execute one Manual block containing:

```text
start
next x75
status
```

Reason: generic serial transport persistence does not perform the Step-09 project completeness verification required between paid calls.

Canonical distinction:

```text
TRANSPORT_PERSISTED != PROJECT_RESULT_COMPLETE
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
SERP result ledger exists;
declared duplicate/boundary comparisons are produced;
analytical evidence decisions are produced;
all 944 REVIEW_SEARCH rows are either directly/validly resolved or explicitly unresolved;
provider and semantic QA both pass;
request/cost accounting reconciles;
no Step-10 clustering/page-ownership decision is silently performed inside Step 09.
```
