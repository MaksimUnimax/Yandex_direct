# STEP 03 — RAW RECOVERY REQUERY RECEIPT — RUN 37

Date: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Canonical run order: `37`
Canonical phrase: `знак зодиака Стрелец`

## Why this request was executed

The historical Step-03 acquisition outcome for run 37 existed, but its full provider payload was trapped inside a corrupted Git carrier and was not losslessly reconstructable from the current repository tree. The owner explicitly authorized re-collection when necessary.

This request is a **new current recovery observation**. It does not overwrite or relabel the historical request ID.

## New provider result

```text
request_id = wordstat-93645021-729a-492b-9ba7-4e607f0c440f
service = wordstat
operation = getTop
phrase = знак зодиака Стрелец
numPhrases = 2000
regions = [225]
devices = [DEVICE_ALL]
http_status = 200
status = OK
elapsed_ms = 2441
results_rows = 595 / RECONCILED
associations_rows = 13
totalCount = 39531
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
```

Raw provider-envelope copy:

`STEP_03_WORDSTAT_RAW/RECOVERY_REQUERY__037__wordstat-93645021-729a-492b-9ba7-4e607f0c440f.raw.txt`

Raw blob SHA:

`611f9fbcbb5442779bb5780a4244c427e027701c`

## Historical comparison boundary

The preserved historical control for canonical run 37 recorded:

```text
historical phrase = знак зодиака Стрелец
historical results_rows = 595
historical associations_rows = 13
historical totalCount = 39531
```

The new current observation has the same `totalCount=39531` and the remote raw reaches the last result row, complete associations block, and final response flags.

## Remote readback / completeness verification

Remote GitHub readback of the persisted raw confirmed:

```text
request_id = wordstat-93645021-729a-492b-9ba7-4e607f0c440f
command.phrase = знак зодиака Стрелец
first result = стрелец знак зодиака / 39531
last result before associations = знак зодиака стрелец мужчина сегодня гороскоп / 4
associations block present = true
associations_rows = 13 / COMPLETE REMOTE TAIL READBACK
totalCount = 39531
request_executed = true
automatic_retry = false
raw_blob_sha = 611f9fbcbb5442779bb5780a4244c427e027701c
```

`results_rows=595` is marked **RECONCILED**, not independently parser-counted in this execution environment. Basis: the persisted remote raw reaches the final result row and complete response tail without truncation; the historical control records 595 rows for the same canonical probe; and `totalCount` matches exactly. No stronger verification is claimed.

## Persistence / transition rule

```text
FULL_RAW_RECEIVED = true
FULL_RAW_SAVED = true
REMOTE_RAW_READBACK = PASS
REMOTE_TAIL_READBACK = PASS
ASSOCIATIONS_COMPLETENESS = PASS / 13
RESULTS_ROW_COUNT = 595 / RECONCILED
TOTALCOUNT_CHECK = PASS / 39531
RUN_37_DURABLE_FEED_FORWARD = PASS
DURABLE_FEED_FORWARD_USABLE = 68/79
REMAINING = 38..48
RECOVERY_PROVIDER_REQUESTS = 6
RECOVERY_PROVIDER_ESTIMATED_COST_RUB = 0.12
NEXT_PROVIDER_REQUEST_ALLOWED = true
STEP04_ALLOWED = false
```
