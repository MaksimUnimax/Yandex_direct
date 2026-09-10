# STEP 03 — RAW RECOVERY REQUERY RECEIPT — RUN 39

Date: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Canonical run order: `39`
Canonical phrase: `знак зодиака Весы`

## Why this request was executed

The historical Step-03 acquisition outcome for run 39 existed, but its full provider payload was trapped inside a corrupted Git carrier and was not losslessly reconstructable from the current repository tree. The owner explicitly authorized re-collection when necessary.

This request is a **new current recovery observation**. It does not overwrite or relabel the historical request ID.

## New provider result

```text
request_id = wordstat-77401772-61c8-4bbd-abb9-447700dd1e37
service = wordstat
operation = getTop
phrase = знак зодиака Весы
numPhrases = 2000
regions = [225]
devices = [DEVICE_ALL]
http_status = 200
status = OK
elapsed_ms = 2250
results_rows = 818 / DIRECT REMOTE LINE-POSITION COUNT
associations_rows = 19 / DIRECT REMOTE LINE-POSITION COUNT
totalCount = 64242
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
```

Raw provider-envelope copy:

`STEP_03_WORDSTAT_RAW/RECOVERY_REQUERY__039__wordstat-77401772-61c8-4bbd-abb9-447700dd1e37.raw.txt`

Raw blob SHA:

`089687e879ed8dc5c9a566f6c6d2c414c5f60c63`

## Historical comparison boundary

The preserved historical manifest for canonical run 39 recorded:

```text
historical phrase = знак зодиака Весы
historical request_id = wordstat-deefb197-f237-4761-93e3-132608bc6124
historical results_rows = 818
historical associations_rows = 19
historical totalCount = 64242
```

The new current observation independently matches all three structural aggregates. The new request ID remains separate from the historical request identity.

## Remote readback / completeness verification

Remote GitHub readback of the persisted raw confirmed:

```text
request_id = wordstat-77401772-61c8-4bbd-abb9-447700dd1e37
command.phrase = знак зодиака Весы
first result = весы знак зодиака / 64242
last result before associations = весы знак зодиака темперамент / 3
results array starts = file line 31
last results row = file line 848
results_rows = 848 - 31 + 1 = 818
associations marker = file line 850
associations rows = file lines 851..869 = 19
totalCount = 64242
request_executed = true
automatic_retry = false
raw_blob_sha = 089687e879ed8dc5c9a566f6c6d2c414c5f60c63
```

This is a direct deterministic line-position count because the recovery raw was intentionally materialized with exactly one result object per file line and one association object per file line.

## Persistence / transition rule

```text
FULL_RAW_RECEIVED = true
FULL_RAW_SAVED = true
REMOTE_RAW_READBACK = PASS
REMOTE_TAIL_READBACK = PASS
RESULTS_COMPLETENESS = PASS / 818 / DIRECT LINE-POSITION COUNT
ASSOCIATIONS_COMPLETENESS = PASS / 19 / DIRECT LINE-POSITION COUNT
TOTALCOUNT_CHECK = PASS / 64242
RUN_39_DURABLE_FEED_FORWARD = PASS
DURABLE_FEED_FORWARD_USABLE = 70/79
REMAINING = 40..48
RECOVERY_PROVIDER_REQUESTS = 8
RECOVERY_PROVIDER_ESTIMATED_COST_RUB = 0.16
NEXT_PROVIDER_REQUEST_ALLOWED = true
STEP04_ALLOWED = false
```
