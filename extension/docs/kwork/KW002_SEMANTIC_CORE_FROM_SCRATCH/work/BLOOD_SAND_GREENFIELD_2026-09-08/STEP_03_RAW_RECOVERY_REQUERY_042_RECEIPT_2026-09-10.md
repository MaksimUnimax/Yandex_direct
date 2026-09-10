# STEP 03 — RAW RECOVERY REQUERY RECEIPT — RUN 42

Date: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Canonical run order: `42`
Canonical phrase: `знак зодиака Козерог`

## Why this request was executed

The historical Step-03 acquisition outcome for run 42 existed, but its full provider payload was trapped inside a corrupted Git carrier and was not losslessly reconstructable from the current repository tree. The owner explicitly authorized re-collection when necessary.

This request is a **new current recovery observation**. It does not overwrite or relabel the historical request ID.

## New provider result

```text
request_id = wordstat-9bf7288d-de00-4dba-a5e6-b254ada7cf84
service = wordstat
operation = getTop
phrase = знак зодиака Козерог
numPhrases = 2000
regions = [225]
devices = [DEVICE_ALL]
http_status = 200
status = OK
elapsed_ms = 1903
results_rows = 548 / DIRECT REMOTE LINE-POSITION COUNT
associations_rows = 16 / DIRECT REMOTE LINE-POSITION COUNT
totalCount = 34189
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
```

Raw provider-envelope copy:

`STEP_03_WORDSTAT_RAW/RECOVERY_REQUERY__042__wordstat-9bf7288d-de00-4dba-a5e6-b254ada7cf84.raw.txt`

Raw blob SHA:

`2073d9873f7c30c2badc51a4baae9e4d9b0c5f0b`

## Historical comparison boundary

The preserved historical manifest for canonical run 42 recorded:

```text
historical phrase = знак зодиака Козерог
historical request_id = wordstat-d39bb2e9-2b97-4c7e-b1af-264d9b86df69
historical results_rows = 548
historical associations_rows = 16
historical totalCount = 34189
```

The new current observation independently matches all three structural aggregates. The new request ID remains separate from the historical request identity.

## Remote readback / completeness verification

Remote GitHub readback of the persisted raw confirmed:

```text
request_id = wordstat-9bf7288d-de00-4dba-a5e6-b254ada7cf84
command.phrase = знак зодиака Козерог
first result = козерог знак зодиака / 34189
last result before associations = алиса гороскоп на завтра знак зодиака козерог / 2
results array starts = file line 22
last results row = file line 569
results_rows = 569 - 22 + 1 = 548
associations marker = file line 571
associations rows = file lines 572..587 = 16
totalCount = 34189
request_executed = true
automatic_retry = false
raw_blob_sha = 2073d9873f7c30c2badc51a4baae9e4d9b0c5f0b
```

This is a direct deterministic line-position count because the recovery raw was intentionally materialized with exactly one result object per file line and one association object per file line.

## Persistence / transition rule

```text
FULL_RAW_RECEIVED = true
FULL_RAW_SAVED = true
REMOTE_RAW_READBACK = PASS
REMOTE_TAIL_READBACK = PASS
RESULTS_COMPLETENESS = PASS / 548 / DIRECT LINE-POSITION COUNT
ASSOCIATIONS_COMPLETENESS = PASS / 16 / DIRECT LINE-POSITION COUNT
TOTALCOUNT_CHECK = PASS / 34189
RUN_42_DURABLE_FEED_FORWARD = PASS
DURABLE_FEED_FORWARD_USABLE = 73/79
REMAINING = 43..48
RECOVERY_PROVIDER_REQUESTS = 11
RECOVERY_PROVIDER_ESTIMATED_COST_RUB = 0.22
NEXT_PROVIDER_REQUEST_ALLOWED = true
STEP04_ALLOWED = false
```
