# KW-001 / OKNO-MSK — STEP 03R S01 CHECKPOINT

Date: 2026-08-29
Seed: `S01`
Phrase: `пластиковые окна`
Job: `kw001-okno-msk-wordstat-pass1-repair-20260829`

## Goal of this provider item

Collect and preserve the complete current Wordstat `getTop` response for the frozen S01 seed before allowing S02.

## Provider truth

```text
status = OK
http_status = 200
request_executed = true
automatic_retry = false
request_id = wordstat-batch-dbe7673d-678b-4491-822f-6f29cf7beb04
method = getTop
phrase = пластиковые окна
region = 213
device = DEVICE_ALL
numPhrases = 200
totalCount = 152131
estimated_cost_rub = 0.02
```

Batch progress after this item:

```text
total = 18
pending = 17
succeeded = 1
failed_terminal = 0
outcome_unknown = 0
requests_started = 1
estimated_cost_rub = 0.02
next_safe_action = CLAIM_NEXT
```

## Preservation verification

Raw provider result preserved in:

`STEP_03R_S01_RAW_PROVIDER_RESULT_2026-08-29.json`

Explicit returned-array accounting:

```text
results_rows_returned = 200
association_rows_returned = 18
total_returned_rows = 218
results_rows_saved = 200
association_rows_saved = 18
total_rows_saved = 218
results_rows_verified = 200
association_rows_verified = 18
total_rows_verified = 218
```

Important:

`totalCount = 152131` is demand/frequency evidence for the root phrase and is NOT a returned-row count.

The complete `results[]` and complete `associations[]` arrays delivered in the provider result were preserved, not representative examples.

## Non-repeat control

Historical Step-03 error was: provider success was accepted while only examples were preserved.

For S01 repair:

```text
provider success only = NOT ENOUGH
complete arrays saved = PASS
saved counts reconciled = PASS
saved result usable = PASS
NON_REPEAT_CONTROL = PASS
```

## Gate

```text
S01_PROJECT_RESULT_COMPLETE = true
S01_NEXT_PROVIDER_ITEM_ALLOWED = true
STEP_03R_COMPLETE = false
STEP_03R_PROGRESS_COMPLETE = 1/18
```
