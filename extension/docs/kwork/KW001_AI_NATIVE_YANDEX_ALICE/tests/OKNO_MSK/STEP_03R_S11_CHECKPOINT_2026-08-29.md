# KW-001 / OKNO-MSK — STEP 03R S11 CHECKPOINT

Date: 2026-08-29
Job: `kw001-okno-msk-wordstat-pass1-repair-20260829`
Seed: `S11 алюминиевые окна`
Status: **COMPLETE / PRESERVED / NORMALIZED / VERIFIED**

## Provider truth

```text
request_id = wordstat-batch-c5589da6-f985-4acd-913d-20beda432598
status = OK
http_status = 200
request_executed = true
automatic_retry = false
outcome_unknown = 0
region = 213
device = DEVICE_ALL
numPhrases = 200
totalCount = 10354
estimated_item_cost_rub = 0.02
estimated_batch_cost_rub_after_item = 0.22
```

A prior manual `COMMAND_DISCOVERY / NO_SUPPORTED_COMMAND` failure occurred before S11 provider execution. It had `request_executed=false`, so it did not reach Wordstat, did not consume provider cost, did not advance the batch item, and was safely retried unchanged. Authority: `STEP_03R_S11_PRE_PROVIDER_NO_SUPPORTED_COMMAND_2026-08-29.md`.

## Complete preservation

```text
results rows returned = 200
association rows returned = 16
provider data rows returned = 216
raw provider data rows saved = 216
normalized TSV data rows saved = 216
rows verified after read-back = 216
```

Artifacts:

```text
STEP_03R_S11_RAW_PROVIDER_RESULT_2026-08-29.json
STEP_03R_S11_RAW_NORMALIZED.tsv
```

Raw JSON read-back verified:
- request/seed/region/device/numPhrases metadata match S11;
- first result is `алюминиевые окна` / `10354`;
- results array ends with `жалюзи горизонтальные алюминиевые на пластиковые окна` / `26`;
- associations array contains 16 rows and ends with `оконная створка` / `537`;
- `totalCount = 10354`;
- `request_executed = true`.

TSV read-back verified:
- metadata block matches S11;
- data starts at line 15;
- last result row is line 214, therefore results rows = 214 - 15 + 1 = 200;
- associations start at line 215;
- final association row is line 230, therefore association rows = 16;
- no data exists after line 230;
- normalized rows = 200 + 16 = 216.

## Non-repeat control

The recorded Step-3 failure was treating technical provider success as collection completion. The later Step03R local defect was marking items complete before mandatory TSV creation.

For S11 the required sequence was completed before S12:

```text
ONE PROVIDER ITEM
→ SAVE COMPLETE RAW PROVIDER RESULT
→ COUNT COMPLETE RESULTS[] + ASSOCIATIONS[]
→ CREATE COMPLETE NORMALIZED TSV
→ REOPEN RAW
→ REOPEN TSV
→ RECONCILE RETURNED = SAVED = NORMALIZED = VERIFIED
→ ONLY THEN MARK ITEM COMPLETE
```

```text
NON_REPEAT_CONTROLS = PASS
CURRENT_ITEM = COMPLETE
STEP_03R_COMPLETED_ITEMS = 11/18
STEP_03R_REMAINING_ITEMS = 7/18
STEP_03R_TOTAL_RESULTS_ROWS = 1326
STEP_03R_TOTAL_ASSOCIATION_ROWS = 158
STEP_03R_TOTAL_PROVIDER_ROWS = 1484
STEP_03R_ESTIMATED_PROVIDER_COST_RUB = 0.22
NEXT_PROVIDER_ITEM = S12 `аксессуары для пластиковых окон`
NEXT_PROVIDER_ITEM_ALLOWED = true
FORWARD_ANALYTICAL_STEP = BLOCKED UNTIL 18/18
```