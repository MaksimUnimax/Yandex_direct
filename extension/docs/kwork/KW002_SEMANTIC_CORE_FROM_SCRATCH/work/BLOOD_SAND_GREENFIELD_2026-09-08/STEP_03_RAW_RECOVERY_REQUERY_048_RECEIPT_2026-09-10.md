# STEP 03 — RAW RECOVERY REQUERY RECEIPT — RUN 48

Date: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Canonical run order: `48`
Canonical phrase: `знак зодиака Телец`

## Why this request was executed

The historical Step-03 acquisition outcome for run 48 existed, but its complete provider payload was trapped in the corrupted large Git carrier and was not losslessly reconstructable from the current repository tree. The owner explicitly authorized re-collection when preserved-source recovery is insufficient.

This request is a **new current recovery observation**. It does not overwrite, rename, or relabel the historical request identity.

## New provider result

```text
request_id = wordstat-9d96a936-b280-4cfb-abb0-5f4a280acd13
service = wordstat
operation = getTop
phrase = знак зодиака Телец
numPhrases = 2000
regions = [225]
devices = [DEVICE_ALL]
http_status = 200
status = OK
elapsed_ms = 2512
results_rows = 594 / DIRECT REMOTE LINE-POSITION COUNT
associations_rows = 15 / DIRECT REMOTE LINE-POSITION COUNT
totalCount = 37962
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
```

Raw provider-envelope copy:

`STEP_03_WORDSTAT_RAW/RECOVERY_REQUERY__048__wordstat-9d96a936-b280-4cfb-abb0-5f4a280acd13.raw.txt`

Raw blob SHA:

`e7e9e63d666ab5af0603ed582a3720abfcda33c0`

## Historical comparison boundary

The preserved historical manifest for canonical run 48 records:

```text
historical phrase = знак зодиака Телец
historical request_id = wordstat-24ddaafc-4e79-4bec-9130-f97e7c0e1175
historical results_rows = 594
historical associations_rows = 15
historical totalCount = 37962
```

The new current observation independently matches all three structural aggregates. The new request ID remains separate from the historical request identity. This receipt does not claim complete historical-vs-current row-by-row identity because such a comparison was not required for the recovery gate.

## Remote readback / completeness verification

The recovery raw was materialized with exactly one result object per file line and one association object per file line. Remote GitHub readback proves:

```text
request_id = wordstat-9d96a936-b280-4cfb-abb0-5f4a280acd13
command.phrase = знак зодиака Телец
first result = телец знак зодиака / 37962
last result before associations = тату знак зодиака водолей телец / 1
results array first row = file line 22
results array last row = file line 615
results_rows = 615 - 22 + 1 = 594
associations marker = file line 617
associations rows = file lines 618..632 = 15
totalCount = file line 634 = 37962
request_executed = true
automatic_retry = false
raw_blob_sha = e7e9e63d666ab5af0603ed582a3720abfcda33c0
```

## Run-48 verdict

```text
FULL_RAW_RECEIVED = true
FULL_RAW_SAVED = true
REMOTE_RAW_READBACK = PASS
REMOTE_TAIL_READBACK = PASS
RESULTS_COMPLETENESS = PASS / 594 / DIRECT LINE-POSITION COUNT
ASSOCIATIONS_COMPLETENESS = PASS / 15 / DIRECT LINE-POSITION COUNT
TOTALCOUNT_CHECK = PASS / 37962
HISTORICAL_STRUCTURAL_CONTROL = PASS / 594 / 15 / 37962
RUN_48_DURABLE_FEED_FORWARD = PASS
DURABLE_FEED_FORWARD_USABLE = 79/79
REMAINING_RECOVERY = 0
RECOVERY_PROVIDER_REQUESTS = 17
RECOVERY_PROVIDER_ESTIMATED_COST_RUB = 0.34
NEXT_PROVIDER_REQUEST_ALLOWED = false / RECOVERY COMPLETE
STEP04_ALLOWED = false / INDEPENDENT LEVEL2 OWNER GATE STILL OPEN
```
