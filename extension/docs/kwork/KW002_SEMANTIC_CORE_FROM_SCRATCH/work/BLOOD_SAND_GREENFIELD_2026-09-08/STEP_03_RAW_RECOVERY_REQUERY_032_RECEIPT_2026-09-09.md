# STEP 03 — RAW RECOVERY REQUERY RECEIPT — RUN 32

Date: 2026-09-09
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Canonical run order: `32`
Canonical phrase: `Аум`

## Why this request was executed

The historical Step-03 acquisition outcome for run 32 existed, but the GitHub carrier that was supposed to preserve the full provider `results[]` / `associations[]` payload was corrupted and not losslessly reconstructable. The preserved prior-dialogue source was known to exist but could not be exported losslessly through the available File Library interface in this execution session. The owner explicitly authorized re-collection when necessary.

This request is therefore a **new current recovery observation**. It does not overwrite or relabel the historical request ID.

## New provider result

```text
request_id = wordstat-efdd12e7-8d7b-4142-96c7-8ece1d883426
service = wordstat
operation = getTop
phrase = Аум
numPhrases = 2000
regions = [225]
devices = [DEVICE_ALL]
http_status = 200
status = OK
elapsed_ms = 2197
results_rows = 460
associations_rows = 16
totalCount = 15635
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
```

Complete raw transport copy:

`STEP_03_WORDSTAT_RAW/RECOVERY_REQUERY__032__wordstat-efdd12e7-8d7b-4142-96c7-8ece1d883426.raw.txt`

## Historical comparison boundary

The old block manifest recorded for canonical run 32:

```text
historical phrase = Аум
historical results_rows = 460
historical associations_rows = 16
historical totalCount = 15635
```

The new current observation matches those three structural/count facts exactly. This is useful recovery consistency evidence, but it is **not** a claim that every row/count inside the new provider response is byte-identical to the historical snapshot.

## Persistence / transition rule

```text
FULL_RAW_RECEIVED = true
FULL_RAW_SAVED = true
RUN_32_DURABLE_FEED_FORWARD = PASS
DURABLE_FEED_FORWARD_USABLE = 63/79
REMAINING = 33..48
NEXT_PROVIDER_REQUEST_ALLOWED_ONLY_AFTER_REMOTE_READBACK = true
STEP04_ALLOWED = false
```
