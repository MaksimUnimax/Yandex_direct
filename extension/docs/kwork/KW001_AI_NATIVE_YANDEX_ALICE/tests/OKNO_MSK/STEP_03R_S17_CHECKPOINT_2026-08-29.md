# KW-001 / OKNO-MSK — Step 03R S17 checkpoint

Date: 2026-08-29

## Item

```text
seed_id = S17
phrase = как выбрать пластиковые окна
job_id = kw001-okno-msk-wordstat-pass1-repair-20260829
request_id = wordstat-batch-d7f87112-ab6a-460a-9a48-0fed0e621259
method = getTop
region = 213
device = DEVICE_ALL
numPhrases = 200
```

## Provider truth

```text
status = OK
http_status = 200
request_executed = true
automatic_retry = false
outcome_unknown = 0
estimated_item_cost_rub = 0.02
totalCount = 254
results_returned = 32
associations_returned = 17
total_provider_rows = 49
```

`totalCount` is demand/frequency evidence, not a returned-row count.

## Preservation truth

```text
raw provider result saved = true
normalized TSV saved = true
results saved = 32
results verified = 32
associations saved = 17
associations verified = 17
provider rows returned = 49
provider rows saved = 49
provider rows normalized = 49
provider rows verified = 49
raw readable = true
TSV readable = true
```

Artifacts:

```text
STEP_03R_S17_RAW_PROVIDER_RESULT_2026-08-29.json
STEP_03R_S17_RAW_NORMALIZED.tsv
```

## Non-repeat control

The historical Step-03 failure was treating provider technical success as collection completion. S17 was not marked complete until the complete raw result and complete TSV were saved and read back.

```text
NON_REPEAT_CONTROLS = PASS
CURRENT_ITEM = COMPLETE
NEXT_PROVIDER_ITEM = S18 `пластиковые окна от производителя`
NEXT_PROVIDER_ITEM_ALLOWED = true
```

## Step 03R cumulative truth after S17

```text
provider requests executed = 17
provider outcomes known = 17
failed_terminal = 0
outcome_unknown = 0
estimated provider cost = 0.34 RUB
complete items = 17/18
remaining items = 1/18
results rows preserved/verified = 2030
association rows preserved/verified = 245
total provider rows preserved/verified = 2275
STEP_03R_COMPLETE = false
FORWARD_ANALYSIS = BLOCKED
```
