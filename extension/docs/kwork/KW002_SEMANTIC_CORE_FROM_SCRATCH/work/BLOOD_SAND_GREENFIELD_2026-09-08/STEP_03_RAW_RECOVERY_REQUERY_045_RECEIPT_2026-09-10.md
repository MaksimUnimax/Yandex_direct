# STEP 03 — RAW RECOVERY REQUERY RECEIPT — RUN 45

Date: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Canonical run order: `45`
Canonical phrase: `знак зодиака Рак`

## Why this request was executed

The historical Step-03 acquisition outcome for run 45 existed, but its full provider payload was trapped inside a corrupted Git carrier and was not losslessly reconstructable from the current repository tree. The owner explicitly authorized re-collection when necessary.

This request is a **new current recovery observation**. It does not overwrite or relabel the historical request ID.

## New provider result

```text
request_id = wordstat-22d64620-4342-4d7b-8ad0-9d4c3e54c34a
service = wordstat
operation = getTop
phrase = знак зодиака Рак
numPhrases = 2000
regions = [225]
devices = [DEVICE_ALL]
http_status = 200
status = OK
elapsed_ms = 2627
results_rows = 987 / DIRECT REMOTE LINE-POSITION COUNT
associations_rows = 14 / DIRECT REMOTE LINE-POSITION COUNT
totalCount = 67198
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
```

Raw provider-envelope copy:

`STEP_03_WORDSTAT_RAW/RECOVERY_REQUERY__045__wordstat-22d64620-4342-4d7b-8ad0-9d4c3e54c34a.raw.txt`

Raw blob SHA:

`9b0200e1e0ea434474974dc9f9bd0cf16f50526b`

## Historical comparison boundary

The preserved historical manifest for canonical run 45 recorded:

```text
historical phrase = знак зодиака Рак
historical request_id = wordstat-bd7fb281-180a-4973-a05c-103b4d7b96a4
historical results_rows = 987
historical associations_rows = 14
historical totalCount = 67198
```

The new current observation independently matches all three structural aggregates. The new request ID remains separate from the historical request identity. This receipt does not claim a complete row-by-row identity comparison between the historical and current result arrays.

## Remote readback / completeness verification

Remote GitHub readback of the persisted raw confirmed:

```text
request_id = wordstat-22d64620-4342-4d7b-8ad0-9d4c3e54c34a
command.phrase = знак зодиака Рак
first result = рак знак зодиака / 67198
last result before associations = сходятся ли знаки зодиака лев и рак / 2
results array starts = file line 22
last results row = file line 1008
results_rows = 1008 - 22 + 1 = 987
associations marker = file line 1010
associations rows = file lines 1011..1024 = 14
totalCount = 67198
request_executed = true
automatic_retry = false
raw_blob_sha = 9b0200e1e0ea434474974dc9f9bd0cf16f50526b
```

This is a direct deterministic line-position count because the recovery raw was intentionally materialized with exactly one result object per file line and one association object per file line.

## Persistence / transition rule

```text
FULL_RAW_RECEIVED = true
FULL_RAW_SAVED = true
REMOTE_RAW_READBACK = PASS
REMOTE_TAIL_READBACK = PASS
RESULTS_COMPLETENESS = PASS / 987 / DIRECT LINE-POSITION COUNT
ASSOCIATIONS_COMPLETENESS = PASS / 14 / DIRECT LINE-POSITION COUNT
TOTALCOUNT_CHECK = PASS / 67198
RUN_45_DURABLE_FEED_FORWARD = PASS
DURABLE_FEED_FORWARD_USABLE = 76/79
REMAINING = 46..48
RECOVERY_PROVIDER_REQUESTS = 14
RECOVERY_PROVIDER_ESTIMATED_COST_RUB = 0.28
NEXT_PROVIDER_REQUEST_ALLOWED = true
STEP04_ALLOWED = false
```
