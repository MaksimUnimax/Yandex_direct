# KW-001 / OKNO-MSK — STEP 03R S13 CHECKPOINT

Date: 2026-08-29
Job: `kw001-okno-msk-wordstat-pass1-repair-20260829`
Seed: `S13 установка пластиковых окон`
Status: **COMPLETE / PRESERVED / NORMALIZED / VERIFIED**

## Provider truth

```text
request_id = wordstat-batch-027f5a42-a471-4452-8a24-49a0e25faa23
status = OK
http_status = 200
request_executed = true
automatic_retry = false
outcome_unknown = 0
region = 213
device = DEVICE_ALL
numPhrases = 200
totalCount = 15510
estimated_item_cost_rub = 0.02
estimated_batch_cost_rub_after_item = 0.26
```

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
STEP_03R_S13_RAW_PROVIDER_RESULT_2026-08-29.json
STEP_03R_S13_RAW_NORMALIZED.tsv
```

Read-back verified:
- request/seed/region/device/numPhrases metadata match S13;
- all 200 `results[]` rows are preserved;
- the final result is `пластиковые окна наружной установки` / `31`;
- all 16 `associations[]` rows are preserved;
- the final association is `монтаж окон пвх` / `492`;
- `totalCount = 15510`;
- `request_executed = true`.

TSV boundary verification:

```text
data start line = 15
last result line = 214
results rows = 214 - 15 + 1 = 200
first association line = 215
last association line = 230
association rows = 230 - 215 + 1 = 16
total normalized rows = 216
```

## Non-repeat control

Recorded Step-3 failure: technical provider success was previously treated as collection completion. Later Step03R defect: items were marked complete before mandatory TSV creation.

For S13 the required sequence was completed before S14:

```text
ONE PROVIDER ITEM
→ SAVE COMPLETE RAW RESULT
→ CREATE COMPLETE TSV
→ REOPEN RAW
→ REOPEN TSV
→ RECONCILE RETURNED = SAVED = NORMALIZED = VERIFIED
→ ONLY THEN MARK COMPLETE
```

```text
NON_REPEAT_CONTROLS = PASS
CURRENT_ITEM = COMPLETE
STEP_03R_COMPLETED_ITEMS = 13/18
STEP_03R_REMAINING_ITEMS = 5/18
STEP_03R_TOTAL_RESULTS_ROWS = 1530
STEP_03R_TOTAL_ASSOCIATION_ROWS = 187
STEP_03R_TOTAL_PROVIDER_ROWS = 1717
STEP_03R_ESTIMATED_PROVIDER_COST_RUB = 0.26
NEXT_PROVIDER_ITEM = S14 `ремонт пластиковых окон`
NEXT_PROVIDER_ITEM_ALLOWED = true
FORWARD_ANALYTICAL_STEP = BLOCKED UNTIL 18/18
```