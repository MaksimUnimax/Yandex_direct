# STEP 03 — RAW RECOVERY REQUERY RECEIPT — RUN 47

Date: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Canonical run order: `47`
Canonical phrase: `знак зодиака Скорпион`

## Why this request was executed

The historical Step-03 acquisition outcome for run 47 existed, but its full provider payload was trapped inside a corrupted Git carrier and was not losslessly reconstructable from the current repository tree. The owner explicitly authorized re-collection when necessary.

This request is a **new current recovery observation**. It does not overwrite or relabel the historical request ID.

## New provider result

```text
request_id = wordstat-0088ece9-d252-428d-927f-0acdf0a03a84
service = wordstat
operation = getTop
phrase = знак зодиака Скорпион
numPhrases = 2000
regions = [225]
devices = [DEVICE_ALL]
http_status = 200
status = OK
elapsed_ms = 2719
results_rows = 809 / DIRECT REMOTE LINE-POSITION COUNT
associations_rows = 17 / DIRECT REMOTE LINE-POSITION COUNT
totalCount = 57861
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
```

Raw provider-envelope copy:

`STEP_03_WORDSTAT_RAW/RECOVERY_REQUERY__047__wordstat-0088ece9-d252-428d-927f-0acdf0a03a84.raw.txt`

Raw blob SHA:

`1da07c996b06157b6eaae20613c25bd11136fb03`

## Historical comparison boundary

The preserved historical manifest for canonical run 47 recorded:

```text
historical phrase = знак зодиака Скорпион
historical request_id = wordstat-57268c34-c203-4ea9-9f28-0cef4284d00d
historical results_rows = 809
historical associations_rows = 17
historical totalCount = 57861
```

The new current observation independently matches all three structural aggregates. The new request ID remains separate from the historical request identity. This receipt does not claim a complete row-by-row identity comparison between the historical and current result arrays.

## Remote readback / completeness verification

Remote GitHub readback of the persisted raw confirmed:

```text
request_id = wordstat-0088ece9-d252-428d-927f-0acdf0a03a84
command.phrase = знак зодиака Скорпион
first result = скорпион знак зодиака / 57861
last result before associations = скорпион знак зодиака мужчина рисунок / 1
results array starts = file line 22
last results row = file line 830
results_rows = 830 - 22 + 1 = 809
associations marker = file line 832
associations rows = file lines 833..849 = 17
totalCount = 57861
request_executed = true
automatic_retry = false
raw_blob_sha = 1da07c996b06157b6eaae20613c25bd11136fb03
```

This is a direct deterministic line-position count because the recovery raw was intentionally materialized with exactly one result object per file line and one association object per file line.

## Persistence / transition rule

```text
FULL_RAW_RECEIVED = true
FULL_RAW_SAVED = true
REMOTE_RAW_READBACK = PASS
REMOTE_TAIL_READBACK = PASS
RESULTS_COMPLETENESS = PASS / 809 / DIRECT LINE-POSITION COUNT
ASSOCIATIONS_COMPLETENESS = PASS / 17 / DIRECT LINE-POSITION COUNT
TOTALCOUNT_CHECK = PASS / 57861
RUN_47_DURABLE_FEED_FORWARD = PASS
DURABLE_FEED_FORWARD_USABLE = 78/79
REMAINING = 48
RECOVERY_PROVIDER_REQUESTS = 16
RECOVERY_PROVIDER_ESTIMATED_COST_RUB = 0.32
NEXT_PROVIDER_REQUEST_ALLOWED = true
STEP04_ALLOWED = false
```
