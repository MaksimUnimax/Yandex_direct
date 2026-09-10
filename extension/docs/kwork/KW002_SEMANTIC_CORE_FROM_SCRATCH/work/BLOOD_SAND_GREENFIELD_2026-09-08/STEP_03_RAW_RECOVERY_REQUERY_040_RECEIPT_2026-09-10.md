# STEP 03 — RAW RECOVERY REQUERY RECEIPT — RUN 40

Date: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Canonical run order: `40`
Canonical phrase: `знак зодиака Водолей`

## Why this request was executed

The historical Step-03 acquisition outcome for run 40 existed, but its full provider payload was trapped inside a corrupted Git carrier and was not losslessly reconstructable from the current repository tree. The owner explicitly authorized re-collection when necessary.

This request is a **new current recovery observation**. It does not overwrite or relabel the historical request ID.

## New provider result

```text
request_id = wordstat-d465de72-775d-4255-83cb-9ad9b4373925
service = wordstat
operation = getTop
phrase = знак зодиака Водолей
numPhrases = 2000
regions = [225]
devices = [DEVICE_ALL]
http_status = 200
status = OK
elapsed_ms = 2376
results_rows = 569 / DIRECT REMOTE LINE-POSITION COUNT
associations_rows = 19 / DIRECT REMOTE LINE-POSITION COUNT
totalCount = 37900
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
```

Raw provider-envelope copy:

`STEP_03_WORDSTAT_RAW/RECOVERY_REQUERY__040__wordstat-d465de72-775d-4255-83cb-9ad9b4373925.raw.txt`

Raw blob SHA:

`94c1d1f76c2da4c7f52e5dfc48d1e909f699f84d`

## Historical comparison boundary

The preserved historical manifest for canonical run 40 recorded:

```text
historical phrase = знак зодиака Водолей
historical request_id = wordstat-03e9a100-bd5c-450c-b9c6-9c65915ec0f9
historical results_rows = 569
historical associations_rows = 19
historical totalCount = 37900
```

The new current observation independently matches all three structural aggregates. The new request ID remains separate from the historical request identity.

## Remote readback / completeness verification

Remote GitHub readback of the persisted raw confirmed:

```text
request_id = wordstat-d465de72-775d-4255-83cb-9ad9b4373925
command.phrase = знак зодиака Водолей
first result = водолей знак зодиака / 37900
last result before associations = тату знак зодиака водолей телец / 1
results array starts = file line 31
last results row = file line 599
results_rows = 599 - 31 + 1 = 569
associations marker = file line 601
associations rows = file lines 602..620 = 19
totalCount = 37900
request_executed = true
automatic_retry = false
raw_blob_sha = 94c1d1f76c2da4c7f52e5dfc48d1e909f699f84d
```

This is a direct deterministic line-position count because the recovery raw was intentionally materialized with exactly one result object per file line and one association object per file line.

## Persistence / transition rule

```text
FULL_RAW_RECEIVED = true
FULL_RAW_SAVED = true
REMOTE_RAW_READBACK = PASS
REMOTE_TAIL_READBACK = PASS
RESULTS_COMPLETENESS = PASS / 569 / DIRECT LINE-POSITION COUNT
ASSOCIATIONS_COMPLETENESS = PASS / 19 / DIRECT LINE-POSITION COUNT
TOTALCOUNT_CHECK = PASS / 37900
RUN_40_DURABLE_FEED_FORWARD = PASS
DURABLE_FEED_FORWARD_USABLE = 71/79
REMAINING = 41..48
RECOVERY_PROVIDER_REQUESTS = 9
RECOVERY_PROVIDER_ESTIMATED_COST_RUB = 0.18
NEXT_PROVIDER_REQUEST_ALLOWED = true
STEP04_ALLOWED = false
```
