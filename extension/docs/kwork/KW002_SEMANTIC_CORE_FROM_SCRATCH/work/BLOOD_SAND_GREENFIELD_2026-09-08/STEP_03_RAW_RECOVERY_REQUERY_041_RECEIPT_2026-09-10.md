# STEP 03 — RAW RECOVERY REQUERY RECEIPT — RUN 41

Date: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Canonical run order: `41`
Canonical phrase: `знак зодиака Дева`

## Why this request was executed

The historical Step-03 acquisition outcome for run 41 existed, but its full provider payload was trapped inside a corrupted Git carrier and was not losslessly reconstructable from the current repository tree. The owner explicitly authorized re-collection when necessary.

This request is a **new current recovery observation**. It does not overwrite or relabel the historical request ID.

## New provider result

```text
request_id = wordstat-459de9aa-c5e2-42e6-9ce1-a160bbafd8e0
service = wordstat
operation = getTop
phrase = знак зодиака Дева
numPhrases = 2000
regions = [225]
devices = [DEVICE_ALL]
http_status = 200
status = OK
elapsed_ms = 2545
results_rows = 952 / DIRECT REMOTE LINE-POSITION COUNT
associations_rows = 18 / DIRECT REMOTE LINE-POSITION COUNT
totalCount = 101545
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
```

Raw provider-envelope copy:

`STEP_03_WORDSTAT_RAW/RECOVERY_REQUERY__041__wordstat-459de9aa-c5e2-42e6-9ce1-a160bbafd8e0.raw.txt`

Raw blob SHA:

`c6d56339e7fe919f506a9703e5f4d30e5d5bf2d4`

## Historical comparison boundary

The preserved historical manifest for canonical run 41 recorded:

```text
historical phrase = знак зодиака Дева
historical request_id = wordstat-73422929-ec25-4b7d-8ed0-eca43ab784a4
historical results_rows = 952
historical associations_rows = 18
historical totalCount = 101545
```

The new current observation independently matches all three structural aggregates. The new request ID remains separate from the historical request identity.

## Remote readback / completeness verification

Remote GitHub readback of the persisted raw confirmed:

```text
request_id = wordstat-459de9aa-c5e2-42e6-9ce1-a160bbafd8e0
command.phrase = знак зодиака Дева
first result = дева знак зодиака / 101545
last result before associations = дева знак зодиака на турецком / 3
results array starts = file line 31
last results row = file line 982
results_rows = 982 - 31 + 1 = 952
associations marker = file line 984
associations rows = file lines 985..1002 = 18
totalCount = 101545
request_executed = true
automatic_retry = false
raw_blob_sha = c6d56339e7fe919f506a9703e5f4d30e5d5bf2d4
```

This is a direct deterministic line-position count because the recovery raw was intentionally materialized with exactly one result object per file line and one association object per file line.

## Persistence / transition rule

```text
FULL_RAW_RECEIVED = true
FULL_RAW_SAVED = true
REMOTE_RAW_READBACK = PASS
REMOTE_TAIL_READBACK = PASS
RESULTS_COMPLETENESS = PASS / 952 / DIRECT LINE-POSITION COUNT
ASSOCIATIONS_COMPLETENESS = PASS / 18 / DIRECT LINE-POSITION COUNT
TOTALCOUNT_CHECK = PASS / 101545
RUN_41_DURABLE_FEED_FORWARD = PASS
DURABLE_FEED_FORWARD_USABLE = 72/79
REMAINING = 42..48
RECOVERY_PROVIDER_REQUESTS = 10
RECOVERY_PROVIDER_ESTIMATED_COST_RUB = 0.20
NEXT_PROVIDER_REQUEST_ALLOWED = true
STEP04_ALLOWED = false
```
