# STEP 03 — RAW RECOVERY REQUERY RECEIPT — RUN 36

Date: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Canonical run order: `36`
Canonical phrase: `знак зодиака`

## Why this request was executed

The historical Step-03 acquisition outcome for run 36 existed, but its full provider payload was trapped inside a corrupted Git carrier and was not losslessly reconstructable from the current repository tree. The owner explicitly authorized re-collection when necessary.

This request is a **new current recovery observation**. It does not overwrite or relabel the historical request ID.

## New provider result

```text
request_id = wordstat-e142a328-7497-495b-83ee-ef069dbae0d0
service = wordstat
operation = getTop
phrase = знак зодиака
numPhrases = 2000
regions = [225]
devices = [DEVICE_ALL]
http_status = 200
status = OK
elapsed_ms = 2830
expected_results_rows_from_provider_limit_and_historical_control = 2000
expected_associations_rows_from_received_tail_and_historical_control = 15
totalCount = 3512863
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
```

Raw provider-envelope copy:

`STEP_03_WORDSTAT_RAW/RECOVERY_REQUERY__036__wordstat-e142a328-7497-495b-83ee-ef069dbae0d0.raw.txt`

Raw blob SHA:

`e0b895235d957352a264a1020c882dfbfde3a00d`

## Historical comparison boundary

The old block manifest recorded for canonical run 36:

```text
historical phrase = знак зодиака
historical results_rows = 2000
historical associations_rows = 15
historical totalCount = 3512863
```

The new current observation has the same `totalCount` and was returned with `numPhrases=2000`; exact current array row counts must be verified from the persisted remote raw before PASS is granted.

## Persistence / transition rule

```text
FULL_RAW_RECEIVED = true
RAW_BLOB_CREATED = true
REMOTE_RAW_READBACK = PENDING
RUN_36_DURABLE_FEED_FORWARD = PENDING
DURABLE_FEED_FORWARD_CURRENT = 66/79
RECOVERY_PROVIDER_REQUESTS = 5
RECOVERY_PROVIDER_ESTIMATED_COST_RUB = 0.10
NEXT_PROVIDER_REQUEST_ALLOWED = false until remote readback and row-count check pass
STEP04_ALLOWED = false
```
