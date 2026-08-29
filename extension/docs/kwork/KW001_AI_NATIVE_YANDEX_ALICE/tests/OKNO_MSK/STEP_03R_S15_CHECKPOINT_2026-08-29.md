# KW-001 / OKNO-MSK — STEP 03R S15 CHECKPOINT

Date: 2026-08-29

## Item

```text
seed_id = S15
seed = цены на пластиковые окна
job_id = kw001-okno-msk-wordstat-pass1-repair-20260829
request_id = wordstat-batch-7f0e990a-7052-43a3-9237-56d0ca8cadd4
method = getTop
region = 213
device = DEVICE_ALL
numPhrases = 200
```

## Provider outcome

```text
status = OK
http_status = 200
request_executed = true
automatic_retry = false
failed_terminal = 0
outcome_unknown = 0
estimated_item_cost_rub = 0.02
estimated_step03r_cost_rub = 0.30
totalCount = 2023
```

`totalCount` is demand/frequency evidence and is not used as a returned-row count.

## Complete result preservation

```text
results rows returned = 200
associations rows returned = 11
provider data rows returned = 211
raw provider rows saved = 211
normalized TSV rows saved = 211
rows verified after read-back = 211
```

Artifacts:

- `STEP_03R_S15_RAW_PROVIDER_RESULT_2026-08-29.json`
- `STEP_03R_S15_RAW_NORMALIZED.tsv`

Read-back checks:

```text
request_id matches = true
seed matches = true
region matches = true
device matches = true
numPhrases matches = true
totalCount matches = true
last result = окно пластиковое цена ростов на дону / 2
first association = сколько стоит застеклить балкон / 443
last association = купить дверь пвх / 604
result-to-association boundary verified = true
raw readable/usable = true
TSV readable/usable = true
returned = saved = normalized = verified = 211
```

No cleanup, exclusion, clustering, or semantic acceptance was performed in this acquisition item.

## Non-repeat control

Relevant historical error: provider technical success was previously treated as collection completion even when complete returned rows were not preserved. A later local defect also closed items before the mandatory normalized TSV existed.

For S15 the required order was respected:

```text
ONE PROVIDER ITEM
→ RECEIVE FULL RESULT
→ SAVE FULL RAW RESULT
→ CREATE FULL TSV
→ REOPEN RAW + TSV
→ RECONCILE ALL ROWS
→ ONLY THEN ALLOW S16
```

```text
NON_REPEAT_CONTROLS = PASS
CURRENT_ITEM = COMPLETE
NEXT_PROVIDER_ITEM = S16 `окна в рассрочку`
NEXT_PROVIDER_ITEM_ALLOWED = true
STEP_03R_COMPLETED_ITEMS = 15/18
STEP_03R_REMAINING_ITEMS = 3/18
STEP_03R_RESULTS_ROWS_VERIFIED = 1930
STEP_03R_ASSOCIATION_ROWS_VERIFIED = 215
STEP_03R_TOTAL_ROWS_VERIFIED = 2145
STEP_03R_ESTIMATED_PROVIDER_COST_RUB = 0.30
STEP_03R_COMPLETE = false
```
