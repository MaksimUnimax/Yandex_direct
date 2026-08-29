# KW-001 / OKNO-MSK — STEP 03R S03 CHECKPOINT

Date: 2026-08-29
Seed: `S03`
Phrase: `французские окна`
Job: `kw001-okno-msk-wordstat-pass1-repair-20260829`

## Goal of this provider item

Collect and preserve the complete current Wordstat `getTop` response for frozen seed S03 before allowing S04.

## Provider truth

```text
status = OK
http_status = 200
request_executed = true
automatic_retry = false
request_id = wordstat-batch-70211b71-7d34-41d9-ba87-dc9be71013b3
method = getTop
phrase = французские окна
region = 213
device = DEVICE_ALL
numPhrases = 200
totalCount = 1453
estimated_cost_rub_item = 0.02
estimated_cost_rub_batch = 0.06
```

Batch progress after S03:

```text
total = 18
pending = 15
succeeded = 3
failed_terminal = 0
outcome_unknown = 0
requests_started = 3
next_safe_action = CLAIM_NEXT
```

## Preservation verification

Raw provider result preserved in:

`STEP_03R_S03_RAW_PROVIDER_RESULT_2026-08-29.json`

Returned-array accounting:

```text
results_rows_returned = 129
association_rows_returned = 15
total_returned_rows = 144
results_rows_saved = 129
association_rows_saved = 15
total_rows_saved = 144
results_rows_verified_after_write = 129
association_rows_verified_after_write = 15
total_rows_verified_after_write = 144
```

`numPhrases = 200` is the request ceiling, not a promise that 200 rows must be returned. S03 returned 129 result rows and all 129 were preserved.

`totalCount = 1453` is demand/frequency evidence and is not a returned-row count.

No semantic cleanup was performed during acquisition. Irrelevant/noisy phrases were intentionally preserved because cleanup is a later step.

## Non-repeat control

Historical Step-03 failure: technical provider success was accepted while only representative examples were preserved.

For S03 repair:

```text
provider success only = NOT ENOUGH
complete results[] saved = PASS
complete associations[] saved = PASS
saved counts reconciled = PASS
saved file re-opened and checked = PASS
NON_REPEAT_CONTROL = PASS
```

## Gate

```text
S03_PROJECT_RESULT_COMPLETE = true
S03_NEXT_PROVIDER_ITEM_ALLOWED = true
STEP_03R_COMPLETE = false
STEP_03R_PROGRESS_COMPLETE = 3/18
CUMULATIVE_ROWS_PRESERVED_S01_TO_S03 = 582
CUMULATIVE_ESTIMATED_COST_RUB = 0.06
```
