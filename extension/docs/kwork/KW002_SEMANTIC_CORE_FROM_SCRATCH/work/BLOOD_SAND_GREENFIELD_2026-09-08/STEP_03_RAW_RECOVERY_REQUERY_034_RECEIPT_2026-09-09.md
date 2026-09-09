# STEP 03 — RAW RECOVERY REQUERY RECEIPT — RUN 34

Date: 2026-09-09
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Canonical run order: `34`
Canonical phrase: `Шлем ужаса`

## Why this request was executed

The historical Step-03 acquisition outcome for run 34 existed, but its full provider payload was trapped inside a corrupted Git carrier and was not losslessly reconstructable from the current repository tree. The owner explicitly authorized re-collection when necessary.

This request is a **new current recovery observation**. It does not overwrite or relabel the historical request ID.

## New provider result

```text
request_id = wordstat-a256259e-581c-4389-92a1-9779e75b5253
service = wordstat
operation = getTop
phrase = Шлем ужаса
numPhrases = 2000
regions = [225]
devices = [DEVICE_ALL]
http_status = 200
status = OK
elapsed_ms = 2204
results_rows = 177
associations_rows = 15
totalCount = 5599
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
```

Complete raw transport copy:

`STEP_03_WORDSTAT_RAW/RECOVERY_REQUERY__034__wordstat-a256259e-581c-4389-92a1-9779e75b5253.raw.txt`

## Historical comparison boundary

The old block manifest recorded for canonical run 34:

```text
historical phrase = Шлем ужаса
historical results_rows = 177
historical associations_rows = 15
historical totalCount = 5599
```

The new current observation matches those structural/count facts exactly. This is recovery consistency evidence only; it is not a claim that every row/count is byte-identical to the historical snapshot.

## Persistence / transition rule

```text
FULL_RAW_RECEIVED = true
FULL_RAW_SAVED = true
RUN_34_DURABLE_FEED_FORWARD = PASS_PENDING_REMOTE_READBACK
DURABLE_FEED_FORWARD_USABLE = 65/79
REMAINING = 35..48
RECOVERY_PROVIDER_REQUESTS = 3
RECOVERY_PROVIDER_ESTIMATED_COST_RUB = 0.06
NEXT_PROVIDER_REQUEST_ALLOWED_ONLY_AFTER_REMOTE_READBACK = true
STEP04_ALLOWED = false
```
