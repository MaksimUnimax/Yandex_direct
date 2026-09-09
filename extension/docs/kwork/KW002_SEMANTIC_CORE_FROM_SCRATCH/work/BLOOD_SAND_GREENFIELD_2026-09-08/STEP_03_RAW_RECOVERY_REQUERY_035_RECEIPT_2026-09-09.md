# STEP 03 — RAW RECOVERY REQUERY RECEIPT — RUN 35

Date: 2026-09-09
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Canonical run order: `35`
Canonical phrase: `Эгисхьяльм`

## Why this request was executed

The historical Step-03 acquisition outcome for run 35 existed, but its full provider payload was trapped inside a corrupted Git carrier and was not losslessly reconstructable from the current repository tree. The owner explicitly authorized re-collection when necessary.

This request is a **new current recovery observation**. It does not overwrite or relabel the historical request ID.

## New provider result

```text
request_id = wordstat-87fb8c19-4323-495a-b1b9-744a18afba0f
service = wordstat
operation = getTop
phrase = Эгисхьяльм
numPhrases = 2000
regions = [225]
devices = [DEVICE_ALL]
http_status = 200
status = OK
elapsed_ms = 1344
results_rows = 6
associations_rows = 16
totalCount = 104
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
```

Complete provider-envelope content, with transport whitespace normalized only:

`STEP_03_WORDSTAT_RAW/RECOVERY_REQUERY__035__wordstat-87fb8c19-4323-495a-b1b9-744a18afba0f.raw.txt`

## Historical comparison boundary

The old block manifest recorded for canonical run 35:

```text
historical phrase = Эгисхьяльм
historical results_rows = 6
historical associations_rows = 16
historical totalCount = 104
```

The new current observation matches those structural/count facts exactly. This is recovery consistency evidence only; it is not a claim that every row/count is byte-identical to the historical snapshot.

## Persistence / transition rule

```text
FULL_RAW_RECEIVED = true
FULL_RAW_SAVED = true
REMOTE_RAW_READBACK = PENDING UNTIL COMMIT READBACK
RUN_35_DURABLE_FEED_FORWARD = PENDING UNTIL REMOTE READBACK
DURABLE_FEED_FORWARD_USABLE_AFTER_READBACK = 66/79
REMAINING_AFTER_READBACK = 36..48
RECOVERY_PROVIDER_REQUESTS_AFTER_READBACK = 4
RECOVERY_PROVIDER_ESTIMATED_COST_RUB_AFTER_READBACK = 0.08
NEXT_PROVIDER_REQUEST_ALLOWED = false until remote readback passes
STEP04_ALLOWED = false
```
