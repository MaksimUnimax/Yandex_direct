# KW-001 / OKNO-MSK — STEP 03R S10 CHECKPOINT

Date: 2026-08-29
Job: `kw001-okno-msk-wordstat-pass1-repair-20260829`
Seed: `S10 остекление веранды`
Status: **COMPLETE / PRESERVED / NORMALIZED / VERIFIED**

## Provider truth

```text
request_id = wordstat-batch-288b38ee-8019-44a1-bbeb-2eca2592b816
status = OK
http_status = 200
request_executed = true
automatic_retry = false
outcome_unknown = 0
region = 213
device = DEVICE_ALL
numPhrases = 200
totalCount = 1373
estimated_item_cost_rub = 0.02
estimated_batch_cost_rub_after_item = 0.20
```

## Complete preservation

```text
results rows returned = 176
association rows returned = 16
provider data rows returned = 192
raw provider data rows saved = 192
normalized TSV data rows saved = 192
rows verified after read-back = 192
```

Artifacts:

```text
STEP_03R_S10_RAW_PROVIDER_RESULT_2026-08-29.json
STEP_03R_S10_RAW_NORMALIZED.tsv
```

Raw JSON read-back verified:
- request/seed/region/device/numPhrases metadata match S10;
- first result is `остекление веранды` / `1373`;
- results array ends with `раздвижное алюминиевое остекление для веранды` / `1`;
- associations array contains 16 rows and ends with `застекленная терраса` / `228`;
- `totalCount = 1373`;
- `request_executed = true`.

TSV read-back verified:
- metadata block matches S10;
- data starts at line 15;
- last result row is line 190, therefore results rows = 190 - 15 + 1 = 176;
- associations start at line 191;
- final association row is line 206, therefore association rows = 16;
- no data exists after line 206;
- normalized rows = 176 + 16 = 192.

## Non-repeat control

The recorded Step-3 failure was treating technical provider success as collection completion. The later Step03R local defect was marking items complete before mandatory TSV creation.

For S10 the required sequence was completed before S11:

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
STEP_03R_COMPLETED_ITEMS = 10/18
STEP_03R_REMAINING_ITEMS = 8/18
STEP_03R_TOTAL_RESULTS_ROWS = 1126
STEP_03R_TOTAL_ASSOCIATION_ROWS = 142
STEP_03R_TOTAL_PROVIDER_ROWS = 1268
STEP_03R_ESTIMATED_PROVIDER_COST_RUB = 0.20
NEXT_PROVIDER_ITEM = S11 `алюминиевые окна`
NEXT_PROVIDER_ITEM_ALLOWED = true
FORWARD_ANALYTICAL_STEP = BLOCKED UNTIL 18/18
```
