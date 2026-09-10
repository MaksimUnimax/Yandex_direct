# STEP 03 — RAW RECOVERY REQUERY RECEIPT — RUN 38

Date: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Canonical run order: `38`
Canonical phrase: `знак зодиака Близнецы`

## Why this request was executed

The historical Step-03 acquisition outcome for run 38 existed, but its full provider payload was trapped inside a corrupted Git carrier and was not losslessly reconstructable from the current repository tree. The owner explicitly authorized re-collection when necessary.

This request is a **new current recovery observation**. It does not overwrite or relabel the historical request ID.

## New provider result

```text
request_id = wordstat-547013bc-6ce5-48de-981e-411f71b7d247
service = wordstat
operation = getTop
phrase = знак зодиака Близнецы
numPhrases = 2000
regions = [225]
devices = [DEVICE_ALL]
http_status = 200
status = OK
elapsed_ms = 1976
results_rows = 783 / DIRECT REMOTE LINE-POSITION COUNT
associations_rows = 15 / DIRECT REMOTE LINE-POSITION COUNT
totalCount = 47689
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
```

Raw provider-envelope copy:

`STEP_03_WORDSTAT_RAW/RECOVERY_REQUERY__038__wordstat-547013bc-6ce5-48de-981e-411f71b7d247.raw.txt`

Raw blob SHA:

`eac14976a280a50ade7ac47d454a1404f33daa83`

## Historical comparison boundary

The preserved historical manifest for canonical run 38 recorded:

```text
historical phrase = знак зодиака Близнецы
historical request_id = wordstat-cef67c2a-34a9-4724-bc07-41f11796dd43
historical results_rows = 783
historical associations_rows = 15
historical totalCount = 47689
```

The new current observation independently matches all three structural aggregates. The new request ID remains separate from the historical request identity.

## Remote readback / completeness verification

Remote GitHub readback of the persisted raw confirmed:

```text
request_id = wordstat-547013bc-6ce5-48de-981e-411f71b7d247
command.phrase = знак зодиака Близнецы
first result = близнецы знак зодиака / 47689
last result before associations = тайны близнецов все знаки зодиака / 1
results array starts = file line 31
last results row = file line 813
results_rows = 813 - 31 + 1 = 783
associations marker = file line 815
associations rows = file lines 816..830 = 15
totalCount = 47689
request_executed = true
automatic_retry = false
raw_blob_sha = eac14976a280a50ade7ac47d454a1404f33daa83
```

This is a direct deterministic line-position count because the recovery raw was intentionally materialized with exactly one result object per file line and one association object per file line.

## Persistence / transition rule

```text
FULL_RAW_RECEIVED = true
FULL_RAW_SAVED = true
REMOTE_RAW_READBACK = PASS
REMOTE_TAIL_READBACK = PASS
RESULTS_COMPLETENESS = PASS / 783 / DIRECT LINE-POSITION COUNT
ASSOCIATIONS_COMPLETENESS = PASS / 15 / DIRECT LINE-POSITION COUNT
TOTALCOUNT_CHECK = PASS / 47689
RUN_38_DURABLE_FEED_FORWARD = PASS
DURABLE_FEED_FORWARD_USABLE = 69/79
REMAINING = 39..48
RECOVERY_PROVIDER_REQUESTS = 7
RECOVERY_PROVIDER_ESTIMATED_COST_RUB = 0.14
NEXT_PROVIDER_REQUEST_ALLOWED = true
STEP04_ALLOWED = false
```
