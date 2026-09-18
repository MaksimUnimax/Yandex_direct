# KW-002 / BLOOD & SAND — STEP08 PROVIDER EXECUTION PLAN

Date: 2026-09-18
Status: **HISTORICAL / SUPERSEDED BEFORE ANY PROVIDER EXECUTION**
Depends on: `STEP08_PRE_ACQUISITION_MAIN_CHAT_RETURN_QA_2026-09-18.md`

## 1. Accepted provider queue

```text
ANALYTICAL_PROVIDER_SEEDS = 386
CURRENT_DIRECT_COST_ESTIMATE_RUB = 7.72
REGION = 225 / Russia
DEVICE = DEVICE_ALL
WORDSTAT_METHOD = GetTop
```

Provider queue source:

`STEP08_PROVIDER_SEED_MANIFEST.csv`

Transport mapping:

`STEP08_PROVIDER_EXECUTION_BATCH_MANIFEST_2026-09-18.csv`

## 2. Current provider/Bridge authority

Current accepted YMB production authority remains:

```text
branch = hotfix/ymb-file-delivery-p0-2026-09-14
commit = b218afb0187bd26af1d7ada3590b02edc2d4a2de
version = 0.1.9
production_branch_vs_commit = IDENTICAL
```

Wordstat protocol:

```text
WORDSTAT_BATCH_API_V1
-> WORDSTAT_BATCH_RESULT_V1

start = local batch creation / request_executed=false
next = at most one provider GetTop request
automatic_retry = false
```

## 3. Depth-homogeneous batch plan

### D500

```text
job_id = kw002-s08-d500-20260918
seed_count = 22
research_mode = COLLISION_DIAGNOSTIC
numPhrases = 500
maxRequests = 22
expected_direct_cost = 0.44 RUB
maxCostRub = 0.44
```

### D1000

```text
job_id = kw002-s08-d1000-20260918
seed_count = 250
dominant_mode = PRECISION_VALIDATION
numPhrases = 1000
maxRequests = 250
expected_direct_cost = 5.00 RUB
maxCostRub = 5.00
```

### D2000

```text
job_id = kw002-s08-d2000-20260918
seed_count = 114
research_mode = DISCOVERY_RECALL_FIRST
numPhrases = 2000
maxRequests = 114
expected_direct_cost = 2.28 RUB
maxCostRub = 2.28
```

Total planned maximum if no queue shrinkage:

```text
REQUESTS = 386
DIRECT_COST = 7.72 RUB
```

## 4. Execution order

```text
D500 FIRST
-> D500 raw complete
-> D500 normalization/sanitation/reconciliation
-> remaining queue impact QA
-> D1000 only if still justified

D1000
-> raw complete
-> normalization/sanitation/reconciliation
-> remaining queue impact QA
-> D2000 only if still justified
```

This plan intentionally does not preload or execute all three jobs at once.

## 5. Mandatory per-request persistence

After every actual `batch.next` provider response:

```text
receive complete WORDSTAT_BATCH_RESULT_V1
-> preserve complete provider_result/envelope
-> write STEP_08_WORDSTAT_RAW/<sequence>__<seed_id>__<request_id>.txt
-> update STEP08_WORDSTAT_ACQUISITION_RECEIPTS.csv
-> GitHub remote readback
-> reconcile phrase/depth/region/device/result rows/associations/totalCount/error truth
-> ONLY THEN next batch.next may be released
```

If `request_executed = UNKNOWN`:

```text
STOP
BLIND RETRY = FORBIDDEN
```

## 6. Current provider facts

Current official provider documentation was rechecked immediately before this plan:

- GetTop accepts `numPhrases=1..2000`, phrase max 400, up to 100 regions and 3 device types;
- Wordstat quota: 10 statistics requests/sec and 100/hour;
- GetTop: 20 RUB/1000 requests incl. VAT;
- supported grouping operators include `()` and `|`.

The method-specific GetTop contract controls `numPhrases`; the generic Search API 250-result row is not used to override the explicit Wordstat GetTop field contract.

## 7. Current release boundary

Only the D500 **local start** may be released now.

```text
D500_START = RELEASED
D500_NEXT = NOT_RELEASED_UNTIL_ACTUAL_START_RESULT
D1000_START = NOT_RELEASED
D2000_START = NOT_RELEASED
PROVIDER_CALLS_AUTHORIZED_BY_START = 0
```

Printing the start command is not execution.

## 8. Supersession

This execution plan was invalidated before any Bridge command was released after late semantic QA found systematic duplicate acquisition questions in the 386-seed queue.

```text
WORDSTAT_CALLS = 0
D500_START_ACTUALLY_RELEASED_TO_OWNER = false
D500_START_EXECUTED = false
CURRENT_PLAN = SUPERSEDED
```

A corrected provider queue must model parent/broad probes and conditional child probes before execution can be released.
