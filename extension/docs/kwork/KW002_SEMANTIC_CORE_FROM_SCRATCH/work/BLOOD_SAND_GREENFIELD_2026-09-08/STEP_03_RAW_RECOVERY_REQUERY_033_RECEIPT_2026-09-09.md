# STEP 03 — RAW RECOVERY REQUERY RECEIPT — RUN 33

Date: 2026-09-09
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Canonical run order: `33`
Canonical phrase: `Крест Сварога`

## Why this request was executed

The historical Step-03 acquisition outcome for run 33 existed, but its full provider payload was trapped inside a corrupted Git carrier and was not losslessly reconstructable from the current repository tree. The owner explicitly authorized re-collection when necessary.

This request is a **new current recovery observation**. It does not overwrite or relabel the historical request ID.

## New provider result

```text
request_id = wordstat-41388da3-fc8c-4c8d-bb8d-2ed3055d877d
service = wordstat
operation = getTop
phrase = Крест Сварога
numPhrases = 2000
regions = [225]
devices = [DEVICE_ALL]
http_status = 200
status = OK
elapsed_ms = 1636
results_rows = 11
associations_rows = 18
totalCount = 366
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
```

Complete raw transport copy:

`STEP_03_WORDSTAT_RAW/RECOVERY_REQUERY__033__wordstat-41388da3-fc8c-4c8d-bb8d-2ed3055d877d.raw.txt`

## Historical comparison boundary

The old block manifest recorded for canonical run 33:

```text
historical phrase = Крест Сварога
historical results_rows = 11
historical associations_rows = 18
historical totalCount = 366
```

The new current observation matches those structural/count facts exactly. This is recovery consistency evidence only; it is not a claim that every row/count is byte-identical to the historical snapshot.

## Persistence / transition rule

```text
FULL_RAW_RECEIVED = true
FULL_RAW_SAVED = true
RUN_33_DURABLE_FEED_FORWARD = PASS
DURABLE_FEED_FORWARD_USABLE = 64/79
REMAINING = 34..48
RECOVERY_PROVIDER_REQUESTS = 2
RECOVERY_PROVIDER_ESTIMATED_COST_RUB = 0.04
NEXT_PROVIDER_REQUEST_ALLOWED_ONLY_AFTER_REMOTE_READBACK = true
STEP04_ALLOWED = false
```
