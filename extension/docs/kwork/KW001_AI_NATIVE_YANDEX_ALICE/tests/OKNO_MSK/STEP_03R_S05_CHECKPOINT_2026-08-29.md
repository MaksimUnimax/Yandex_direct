# KW-001 / OKNO-MSK — STEP 03R S05 CHECKPOINT

Date: 2026-08-29
Seed: `S05`
Phrase: `пластиковые двери`
Job: `kw001-okno-msk-wordstat-pass1-repair-20260829`

## Goal

Collect and preserve the complete current Wordstat `getTop` response for S05 before allowing S06.

## Provider result

```text
status = OK
http_status = 200
request_executed = true
automatic_retry = false
request_id = wordstat-batch-d5768da9-c98f-4205-b507-6db78420606b
method = getTop
phrase = пластиковые двери
region = 213
device = DEVICE_ALL
numPhrases = 200
totalCount = 27229
estimated_cost_rub_item = 0.02
estimated_cost_rub_batch = 0.10
```

Batch progress after S05:

```text
total = 18
pending = 13
succeeded = 5
failed_terminal = 0
outcome_unknown = 0
requests_started = 5
next_safe_action = CLAIM_NEXT
```

## Preservation verification

Raw provider result:

`STEP_03R_S05_RAW_PROVIDER_RESULT_2026-08-29.json`

```text
results_rows_returned = 200
associations_rows_returned = 15
total_rows_returned = 215
results_rows_saved = 200
associations_rows_saved = 15
total_rows_saved = 215
results_rows_verified_after_save = 200
associations_rows_verified_after_save = 15
total_rows_verified_after_save = 215
```

`totalCount = 27229` is phrase demand evidence and is not a returned-row count.

No semantic cleanup or exclusion was performed during acquisition.

## Non-repeat control

Historical Step-03 failure: successful provider execution was previously accepted although complete rows were not preserved.

```text
provider_success_only = NOT_ENOUGH
complete_arrays_saved = PASS
saved_file_reopened = PASS
saved_counts_reconciled = PASS
NON_REPEAT_CONTROL = PASS
```

## Gate

```text
S05_PROJECT_RESULT_COMPLETE = true
S06_PROVIDER_REQUEST_ALLOWED = true
STEP_03R_COMPLETE = false
STEP_03R_PROGRESS_COMPLETE = 5/18
```
