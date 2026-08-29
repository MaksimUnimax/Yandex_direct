# KW-001 / OKNO-MSK — STEP 03R S14 CHECKPOINT

Date: 2026-08-29
Job: `kw001-okno-msk-wordstat-pass1-repair-20260829`
Seed: `S14 ремонт пластиковых окон`
Status: **COMPLETE / PRESERVED / NORMALIZED / VERIFIED**

## Provider truth

```text
request_id = wordstat-batch-0ea6d1b6-ab45-4fea-a091-56e2def2dc39
status = OK
http_status = 200
request_executed = true
automatic_retry = false
outcome_unknown = 0
region = 213
device = DEVICE_ALL
numPhrases = 200
totalCount = 4382
estimated_item_cost_rub = 0.02
estimated_batch_cost_rub_after_item = 0.28
```

## Complete preservation

```text
results rows returned = 200
association rows returned = 17
provider data rows returned = 217
raw provider data rows saved = 217
normalized TSV data rows saved = 217
rows verified after read-back = 217
```

Artifacts:

```text
STEP_03R_S14_RAW_PROVIDER_RESULT_2026-08-29.json
STEP_03R_S14_RAW_NORMALIZED.tsv
```

Read-back verified:
- request/seed/region/device/numPhrases metadata match S14;
- TSV starts with the correct S14 metadata and first result;
- the 200th result is `клей для ремонта пластиковых окон`;
- the next row starts associations with `пластика окон`;
- all 17 associations are present through `как починить окно`;
- `totalCount = 4382` is frequency evidence and is not treated as row count;
- raw provider artifact was saved from the same parsed complete 200 + 17 provider rows and reopened successfully.

## Non-repeat control

Recorded Step-3 error: technical provider success was previously treated as collection completion. Later local defect: items were marked complete before mandatory TSV creation.

For S14 the required sequence was performed before S15:

```text
ONE PROVIDER ITEM
→ COUNT COMPLETE PROVIDER ARRAYS
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
STEP_03R_COMPLETED_ITEMS = 14/18
STEP_03R_REMAINING_ITEMS = 4/18
STEP_03R_TOTAL_RESULTS_ROWS = 1730
STEP_03R_TOTAL_ASSOCIATION_ROWS = 204
STEP_03R_TOTAL_PROVIDER_ROWS = 1934
STEP_03R_ESTIMATED_PROVIDER_COST_RUB = 0.28
NEXT_PROVIDER_ITEM = S15 `цены на пластиковые окна`
NEXT_PROVIDER_ITEM_ALLOWED = true
FORWARD_ANALYTICAL_STEP = BLOCKED UNTIL 18/18
```