# KW-001 / OKNO-MSK — STEP 03R S12 CHECKPOINT

Date: 2026-08-29
Job: `kw001-okno-msk-wordstat-pass1-repair-20260829`
Seed: `S12 аксессуары для пластиковых окон`
Status: **COMPLETE / PRESERVED / NORMALIZED / VERIFIED**

## Provider truth

```text
request_id = wordstat-batch-7a613df4-d2b4-402e-90c7-0ef70640141a
status = OK
http_status = 200
request_executed = true
automatic_retry = false
outcome_unknown = 0
region = 213
device = DEVICE_ALL
numPhrases = 200
totalCount = 29
estimated_item_cost_rub = 0.02
estimated_batch_cost_rub_after_item = 0.24
```

## Complete preservation

```text
results rows returned = 4
association rows returned = 13
provider data rows returned = 17
raw provider data rows saved = 17
normalized TSV data rows saved = 17
rows verified after read-back = 17
```

Artifacts:

```text
STEP_03R_S12_RAW_PROVIDER_RESULT_2026-08-29.json
STEP_03R_S12_RAW_NORMALIZED.tsv
```

Read-back verified:
- request/seed/region/device/numPhrases metadata match S12;
- all 4 `results[]` rows are present;
- all 13 `associations[]` rows are present;
- TSV contains 4 `result` rows followed by 13 `association` rows;
- `totalCount = 29`;
- `request_executed = true`.

## Non-repeat control

Recorded Step-3 error: technical provider success was previously treated as collection completion. Later local defect: items were marked complete before mandatory TSV creation.

For S12 the complete required sequence was performed before S13:

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
STEP_03R_COMPLETED_ITEMS = 12/18
STEP_03R_REMAINING_ITEMS = 6/18
STEP_03R_TOTAL_RESULTS_ROWS = 1330
STEP_03R_TOTAL_ASSOCIATION_ROWS = 171
STEP_03R_TOTAL_PROVIDER_ROWS = 1501
STEP_03R_ESTIMATED_PROVIDER_COST_RUB = 0.24
NEXT_PROVIDER_ITEM = S13 `установка пластиковых окон`
NEXT_PROVIDER_ITEM_ALLOWED = true
FORWARD_ANALYTICAL_STEP = BLOCKED UNTIL 18/18
```
