# KW-001 / OKNO-MSK — Step 03R S18 checkpoint

Date: 2026-08-29
Seed: `S18`
Phrase: `пластиковые окна от производителя`
Job: `kw001-okno-msk-wordstat-pass1-repair-20260829`

## Provider truth

```text
batch status = COMPLETED
batch total = 18
batch succeeded = 18
batch failed_terminal = 0
batch outcome_unknown = 0
batch requests_started = 18
batch estimated_cost_rub = 0.36
next_safe_action = NONE

item status = SUCCEEDED
request_id = wordstat-batch-a6af2f54-cda0-4226-8f4b-1dd5ce3c3a70
request_executed = true
automatic_retry = false
http_status = 200
elapsed_ms = 12004
item estimated_cost_rub = 0.02
method = getTop
region = 213
device = DEVICE_ALL
numPhrases = 200
totalCount = 1589
```

## Complete-result preservation

```text
results returned = 123
results saved raw = 123
results saved normalized = 123
results verified = 123

associations returned = 17
associations saved raw = 17
associations saved normalized = 17
associations verified = 17

total provider rows returned = 140
total provider rows saved raw = 140
total provider rows saved normalized = 140
total provider rows verified = 140
```

Artifacts:

```text
STEP_03R_S18_RAW_PROVIDER_RESULT_2026-08-29.json
STEP_03R_S18_RAW_NORMALIZED.tsv
```

Read-back verification:

- raw provider artifact was re-opened after commit and contains the correct request identity, command parameters, complete `results[]`, complete `associations[]`, `totalCount=1589`, `request_executed=true`, and `automatic_retry=false`;
- normalized TSV was re-opened after commit;
- TSV has 154 total lines: 14 metadata/header lines plus 140 provider-data rows;
- the 123rd `result` is `пластиковые окна в ногинске от производителя цены`;
- the next row is the first `association`, `стеклопакет`;
- 17 associations are present through the final row `изготовление стеклопакетов`.

`totalCount=1589` is demand/frequency metadata and is not a returned-row count.

## Non-repeat control

The historical Step-03 failure was treating successful provider execution as collection completion while complete rows were not preserved. S18 is not accepted on `HTTP 200` / `SUCCEEDED` alone; complete raw + TSV and read-back reconciliation are present.

```text
S18_COMPLETE = true
S18_RESULTS_RETURNED_SAVED_VERIFIED = 123
S18_ASSOCIATIONS_RETURNED_SAVED_VERIFIED = 17
S18_PROVIDER_ROWS_RETURNED_SAVED_VERIFIED = 140
NON_REPEAT_CONTROLS = PASS
NEXT_PROVIDER_ITEM = NONE
BATCH_PROVIDER_EXECUTION_COMPLETE = true
STEP_03R_FINAL_RECONCILIATION_REQUIRED = true
```
