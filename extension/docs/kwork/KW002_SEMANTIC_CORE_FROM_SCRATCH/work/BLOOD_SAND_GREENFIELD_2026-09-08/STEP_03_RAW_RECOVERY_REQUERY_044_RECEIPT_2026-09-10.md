# STEP 03 — RAW RECOVERY REQUERY RECEIPT — RUN 44

Date: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Canonical run order: `44`
Canonical phrase: `знак зодиака Лев`

## Why this request was executed

The historical Step-03 acquisition outcome for run 44 existed, but its full provider payload was trapped inside a corrupted Git carrier and was not losslessly reconstructable from the current repository tree. The owner explicitly authorized re-collection when necessary.

This request is a **new current recovery observation**. It does not overwrite or relabel the historical request ID.

## New provider result

```text
request_id = wordstat-dde33455-ff1a-4b90-9c01-f1ed89c5ff15
service = wordstat
operation = getTop
phrase = знак зодиака Лев
numPhrases = 2000
regions = [225]
devices = [DEVICE_ALL]
http_status = 200
status = OK
elapsed_ms = 2723
results_rows = 1074 / DIRECT REMOTE LINE-POSITION COUNT
associations_rows = 14 / DIRECT REMOTE LINE-POSITION COUNT
totalCount = 108619
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
```

Raw provider-envelope copy:

`STEP_03_WORDSTAT_RAW/RECOVERY_REQUERY__044__wordstat-dde33455-ff1a-4b90-9c01-f1ed89c5ff15.raw.txt`

Raw blob SHA:

`5a068c684df64cf37bfcbfb44f9bcb2ae251c360`

## Historical comparison boundary

The preserved historical manifest for canonical run 44 recorded:

```text
historical phrase = знак зодиака Лев
historical request_id = wordstat-d09d1a74-900c-4107-9770-054cf4c0b592
historical results_rows = 1074
historical associations_rows = 14
historical totalCount = 108619
```

The new current observation independently matches all three structural aggregates. The new request ID remains separate from the historical request identity. This receipt does not claim a complete row-by-row identity comparison between the historical and current result arrays.

## Remote readback / completeness verification

Remote GitHub readback of the persisted raw confirmed:

```text
request_id = wordstat-dde33455-ff1a-4b90-9c01-f1ed89c5ff15
command.phrase = знак зодиака Лев
first result = знак зодиака лев / 108619
last result before associations = гиф знак зодиака лев / 1
results array starts = file line 22
last results row = file line 1095
results_rows = 1095 - 22 + 1 = 1074
associations marker = file line 1097
associations rows = file lines 1098..1111 = 14
totalCount = 108619
request_executed = true
automatic_retry = false
raw_blob_sha = 5a068c684df64cf37bfcbfb44f9bcb2ae251c360
```

This is a direct deterministic line-position count because the recovery raw was intentionally materialized with exactly one result object per file line and one association object per file line.

## Persistence / transition rule

```text
FULL_RAW_RECEIVED = true
FULL_RAW_SAVED = true
REMOTE_RAW_READBACK = PASS
REMOTE_TAIL_READBACK = PASS
RESULTS_COMPLETENESS = PASS / 1074 / DIRECT LINE-POSITION COUNT
ASSOCIATIONS_COMPLETENESS = PASS / 14 / DIRECT LINE-POSITION COUNT
TOTALCOUNT_CHECK = PASS / 108619
RUN_44_DURABLE_FEED_FORWARD = PASS
DURABLE_FEED_FORWARD_USABLE = 75/79
REMAINING = 45..48
RECOVERY_PROVIDER_REQUESTS = 13
RECOVERY_PROVIDER_ESTIMATED_COST_RUB = 0.26
NEXT_PROVIDER_REQUEST_ALLOWED = true
STEP04_ALLOWED = false
```
