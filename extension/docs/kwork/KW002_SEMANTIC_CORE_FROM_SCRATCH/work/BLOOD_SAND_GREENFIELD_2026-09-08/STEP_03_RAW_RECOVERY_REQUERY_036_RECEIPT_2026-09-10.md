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
results_rows = 2000 (RECONCILED; see verification method below)
associations_rows = 15
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

The new current observation has the same `totalCount=3512863` and was returned with `numPhrases=2000`.

## Remote readback / completeness verification

Remote GitHub readback of the persisted raw confirmed:

```text
request_id = wordstat-e142a328-7497-495b-83ee-ef069dbae0d0
command.phrase = знак зодиака
numPhrases = 2000
first result = знаки зодиака / 3512863
last result before associations = знак зодиака козерог скорпион / 789
associations block present = true
associations_rows visible in complete tail = 15
totalCount = 3512863
request_executed = true
automatic_retry = false
raw_blob_sha = e0b895235d957352a264a1020c882dfbfde3a00d
```

`results_rows=2000` is marked **RECONCILED**, not independently parser-counted in this execution environment. Basis: current request explicitly requested `numPhrases=2000`; the persisted remote raw reaches the final result row and complete response tail without truncation; the historical manifest independently records 2000 rows for the same canonical probe; and `totalCount` matches exactly. An independent local Python download/parser was not available because this execution container could not resolve/download the GitHub raw URL. No stronger verification is claimed.

## Persistence / transition rule

```text
FULL_RAW_RECEIVED = true
RAW_BLOB_CREATED = true
REMOTE_RAW_READBACK = PASS
REMOTE_TAIL_READBACK = PASS
ASSOCIATIONS_COMPLETENESS = PASS / 15
RESULTS_ROW_COUNT = 2000 / RECONCILED
TOTALCOUNT_CHECK = PASS / 3512863
RUN_36_DURABLE_FEED_FORWARD = PASS
DURABLE_FEED_FORWARD_USABLE = 67/79
REMAINING = 37..48
RECOVERY_PROVIDER_REQUESTS = 5
RECOVERY_PROVIDER_ESTIMATED_COST_RUB = 0.10
NEXT_PROVIDER_REQUEST_ALLOWED = true
STEP04_ALLOWED = false
```
