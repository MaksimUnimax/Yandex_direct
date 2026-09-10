# STEP 03 — RAW RECOVERY REQUERY RECEIPT — RUN 43

Date: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Canonical run order: `43`
Canonical phrase: `знак зодиака Овен`

## Why this request was executed

The historical Step-03 acquisition outcome for run 43 existed, but its full provider payload was trapped inside a corrupted Git carrier and was not losslessly reconstructable from the current repository tree. The owner explicitly authorized re-collection when necessary.

This request is a **new current recovery observation**. It does not overwrite or relabel the historical request ID.

## New provider result

```text
request_id = wordstat-b9438bf7-323d-4230-b91a-55dfa5474b1b
service = wordstat
operation = getTop
phrase = знак зодиака Овен
numPhrases = 2000
regions = [225]
devices = [DEVICE_ALL]
http_status = 200
status = OK
elapsed_ms = 2450
results_rows = 593 / DIRECT REMOTE LINE-POSITION COUNT
associations_rows = 15 / DIRECT REMOTE LINE-POSITION COUNT
totalCount = 37752
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
```

Raw provider-envelope copy:

`STEP_03_WORDSTAT_RAW/RECOVERY_REQUERY__043__wordstat-b9438bf7-323d-4230-b91a-55dfa5474b1b.raw.txt`

Raw blob SHA:

`4cd21920223058f0636ae670b9a6ebf148e7dbe1`

## Historical comparison boundary

The preserved historical manifest for canonical run 43 recorded:

```text
historical phrase = знак зодиака Овен
historical request_id = wordstat-07c630e8-dd95-4e74-a036-9d01f3a9ecbc
historical results_rows = 593
historical associations_rows = 15
historical totalCount = 37752
```

The new current observation independently matches all three structural aggregates. The new request ID remains separate from the historical request identity.

## Remote readback / completeness verification

Remote GitHub readback of the persisted raw confirmed:

```text
request_id = wordstat-b9438bf7-323d-4230-b91a-55dfa5474b1b
command.phrase = знак зодиака Овен
first result = овен знак зодиака / 37752
last result before associations = что не нравится знаку зодиака овну / 1
results array starts = file line 22
last results row = file line 614
results_rows = 614 - 22 + 1 = 593
associations marker = file line 616
associations rows = file lines 617..631 = 15
totalCount = 37752
request_executed = true
automatic_retry = false
raw_blob_sha = 4cd21920223058f0636ae670b9a6ebf148e7dbe1
```

This is a direct deterministic line-position count because the recovery raw was intentionally materialized with exactly one result object per file line and one association object per file line.

## Persistence / transition rule

```text
FULL_RAW_RECEIVED = true
FULL_RAW_SAVED = true
REMOTE_RAW_READBACK = PASS
REMOTE_TAIL_READBACK = PASS
RESULTS_COMPLETENESS = PASS / 593 / DIRECT LINE-POSITION COUNT
ASSOCIATIONS_COMPLETENESS = PASS / 15 / DIRECT LINE-POSITION COUNT
TOTALCOUNT_CHECK = PASS / 37752
RUN_43_DURABLE_FEED_FORWARD = PASS
DURABLE_FEED_FORWARD_USABLE = 74/79
REMAINING = 44..48
RECOVERY_PROVIDER_REQUESTS = 12
RECOVERY_PROVIDER_ESTIMATED_COST_RUB = 0.24
NEXT_PROVIDER_REQUEST_ALLOWED = true
STEP04_ALLOWED = false
```
