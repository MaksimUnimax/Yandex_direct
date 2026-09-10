# STEP 03 — RAW RECOVERY REQUERY RECEIPT — RUN 46

Date: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Canonical run order: `46`
Canonical phrase: `знак зодиака Рыбы`

## Why this request was executed

The historical Step-03 acquisition outcome for run 46 existed, but its full provider payload was trapped inside a corrupted Git carrier and was not losslessly reconstructable from the current repository tree. The owner explicitly authorized re-collection when necessary.

This request is a **new current recovery observation**. It does not overwrite or relabel the historical request ID.

## New provider result

```text
request_id = wordstat-bfc1f74c-8137-4795-a00d-47ed8b85d894
service = wordstat
operation = getTop
phrase = знак зодиака Рыбы
numPhrases = 2000
regions = [225]
devices = [DEVICE_ALL]
http_status = 200
status = OK
elapsed_ms = 2466
results_rows = 915 / DIRECT REMOTE LINE-POSITION COUNT
associations_rows = 18 / DIRECT REMOTE LINE-POSITION COUNT
totalCount = 68815
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
```

Raw provider-envelope copy:

`STEP_03_WORDSTAT_RAW/RECOVERY_REQUERY__046__wordstat-bfc1f74c-8137-4795-a00d-47ed8b85d894.raw.txt`

Raw blob SHA:

`eec4fa4fd8026129b619c95f67860e496ba8eaa6`

## Historical comparison boundary

The preserved historical manifest for canonical run 46 recorded:

```text
historical phrase = знак зодиака Рыбы
historical request_id = wordstat-cff4bf6c-1272-43d5-8af8-dad9643796d6
historical results_rows = 915
historical associations_rows = 18
historical totalCount = 68815
```

The new current observation independently matches all three structural aggregates. The new request ID remains separate from the historical request identity. This receipt does not claim a complete row-by-row identity comparison between the historical and current result arrays.

## Remote readback / completeness verification

Remote GitHub readback of the persisted raw confirmed:

```text
request_id = wordstat-bfc1f74c-8137-4795-a00d-47ed8b85d894
command.phrase = знак зодиака Рыбы
first result = рыбы знак зодиака / 68815
last result before associations = девушка рыба знак зодиака измены / 1
results array starts = file line 22
last results row = file line 936
results_rows = 936 - 22 + 1 = 915
associations marker = file line 938
associations rows = file lines 939..956 = 18
totalCount = 68815
request_executed = true
automatic_retry = false
raw_blob_sha = eec4fa4fd8026129b619c95f67860e496ba8eaa6
```

This is a direct deterministic line-position count because the recovery raw was intentionally materialized with exactly one result object per file line and one association object per file line.

## Persistence / transition rule

```text
FULL_RAW_RECEIVED = true
FULL_RAW_SAVED = true
REMOTE_RAW_READBACK = PASS
REMOTE_TAIL_READBACK = PASS
RESULTS_COMPLETENESS = PASS / 915 / DIRECT LINE-POSITION COUNT
ASSOCIATIONS_COMPLETENESS = PASS / 18 / DIRECT LINE-POSITION COUNT
TOTALCOUNT_CHECK = PASS / 68815
RUN_46_DURABLE_FEED_FORWARD = PASS
DURABLE_FEED_FORWARD_USABLE = 77/79
REMAINING = 47..48
RECOVERY_PROVIDER_REQUESTS = 15
RECOVERY_PROVIDER_ESTIMATED_COST_RUB = 0.30
NEXT_PROVIDER_REQUEST_ALLOWED = true
STEP04_ALLOWED = false
```
