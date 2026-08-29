# KW-001 / OKNO-MSK — STEP 03R S04 CHECKPOINT

Date: 2026-08-29
Seed: `S04`
Phrase: `окна п 44`
Job: `kw001-okno-msk-wordstat-pass1-repair-20260829`

## Goal of this provider item

Collect and preserve the complete current Wordstat `getTop` response for the frozen S04 seed before allowing S05.

## Provider truth

```text
status = OK
http_status = 200
request_executed = true
automatic_retry = false
request_id = wordstat-batch-4d936c7b-f973-4feb-a283-5e560cd35c98
method = getTop
phrase = окна п 44
region = 213
device = DEVICE_ALL
numPhrases = 200
totalCount = 252
estimated_cost_rub_item = 0.02
estimated_cost_rub_batch = 0.08
```

Batch progress after this item:

```text
total = 18
pending = 14
succeeded = 4
failed_terminal = 0
outcome_unknown = 0
requests_started = 4
estimated_cost_rub = 0.08
next_safe_action = CLAIM_NEXT
```

## Preservation verification

Raw provider result preserved in:

`STEP_03R_S04_RAW_PROVIDER_RESULT_2026-08-29.json`

Explicit returned-array accounting:

```text
results_rows_returned = 12
association_rows_returned = 17
total_returned_rows = 29
results_rows_saved = 12
association_rows_saved = 17
total_rows_saved = 29
results_rows_verified_after_readback = 12
association_rows_verified_after_readback = 17
total_rows_verified_after_readback = 29
```

`numPhrases = 200` is a maximum requested result count, not a promise that Yandex must return 200 rows.

`totalCount = 252` is demand/frequency evidence and is NOT a returned-row count.

## Non-repeat control

Historical Step-03 error was accepting provider success while preserving only examples.

For S04 repair:

```text
provider success only = NOT ENOUGH
complete arrays saved = PASS
saved file reopened = PASS
saved counts reconciled = PASS
saved result usable = PASS
NON_REPEAT_CONTROL = PASS
```

## Gate

```text
S04_PROJECT_RESULT_COMPLETE = true
S04_NEXT_PROVIDER_ITEM_ALLOWED = true
STEP_03R_COMPLETE = false
STEP_03R_PROGRESS_COMPLETE = 4/18
CUMULATIVE_ROWS_SAVED_AND_VERIFIED = 611
```
