# KW-002 JOB MANIFEST — BLOOD_SAND_GREENFIELD_2026-09-08

Status: **STEP 03 CURRENT / PRE-STEP PROVIDER GATE COMPLETE / BATCH START READY**

## 1. Job identity

```text
KW_ID = KW-002
JOB_ID = BLOOD_SAND_GREENFIELD_2026-09-08
JOB_TYPE = PRODUCTIZATION_REHEARSAL
EXECUTION_MODE = CLEAN_FROM_SCRATCH
BUSINESS = Blood & Sand / «Кровь и Песок»
SITE_STATE = NEW_SITE
REGION = Russia
LANGUAGE = Russian
PRIMARY_SEARCH_ENGINE = Yandex
```

## 2. Frozen client truth

```text
Brand = «Кровь и Песок» / Blood & Sand
Business = product brand / seller
Client wording = амулеты, обереги и талисманы; в ассортименте есть в том числе товары для автомобиля
Sales channels = Ozon + Wildberries
Assortment authority = Ozon only
Primary market/search geography = Russia
New owned website planned = YES
```

## 3. Current authoritative assortment input

```text
CLIENT_SUPPLIED_BRIEF.md
CLIENT_SUPPLIED_ASSORTMENT_MANIFEST.md
CLIENT_SUPPLIED_PRODUCT_CATALOG_OZON_76.csv
ALLOWED_INPUTS_AND_SEALED_SOURCES.md
OZON PRODUCT/LISTING ROWS = 76
WB PRODUCT/LISTING ROWS ACTIVE = 0
```

## 4. Clean-baseline rule

Until Step 20 final freeze:

```text
PRIOR BLOOD_SAND SEO RESEARCH = SEALED / FORBIDDEN EXECUTION INPUT
DEFAULT BLOOD_SAND PROJECT MATERIAL = DENY
EXCEPTIONS = exact sources whitelisted in ALLOWED_INPUTS_AND_SEALED_SOURCES.md
```

## 5. Universal quality rule

Current Level-1 authority:

`LEVEL1/RESULT_QUALITY_SCORING_RULE.md`

```text
EACH CRITERION = 0–10
DEFAULT CRITERIA = 10
QUALITY_TOTAL = 0–100
QUALITY_SCORE = QUALITY_TOTAL / 10
PASS = >=90/100 AND >=9.0/10 AND ALL HARD GATES AND NO OPEN CRITICAL DEFECT
```

## 6. Accepted upstream truth

### Step 01

```text
STEP_01_INPUT_ROWS_ACCOUNTED = 76
STEP_01_SILENT_DROPS = 0
STEP_01_WB_ROWS_USED = 0
STEP_01_MAIN_RETURN_QA = PASS
STEP_01_COMPLETE = true
```

### Step 02 V1 historical

```text
STEP_02_V1_SEEDS = 97
STEP_02_V1_PRIMARY = 67
STEP_02_V1_DEFERRED = 30
STEP_02_V1_QUALITY_TOTAL = 65/100
STEP_02_V1_QUALITY_SCORE = 6.5/10
STEP_02_V1_STATUS = SUPERSEDED / REWORK_REQUIRED
```

### Step 02 V2 current authority

```text
STEP_02_V2_PRIMARY = 79
STEP_02_V2_DEFERRED_CONTROL = 49
STEP_02_V2_SEARCH_QUALITY_GROUPS_PASS = 26/26
STEP_02_V2_QUALITY_TOTAL = 93/100
STEP_02_V2_QUALITY_SCORE = 9.3/10
STEP_02_V2_QA = PASS
STEP_02_COMPLETE = true
```

Current upstream seed authority:

`STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv`

## 7. Step 03 provider contract

Canonical current files:

```text
STEP_03_PRE_STEP_PROVIDER_GATE_2026-09-09.md
STEP_03_WORDSTAT_EXECUTION_MANIFEST_V1.csv
STEP_03_WORDSTAT_BATCH_START_COMMAND_2026-09-09.txt
STEP_03_WORDSTAT_ACQUISITION_RECEIPTS.csv
```

Step-03 acquisition parameters:

```text
ACTIVE_SERVICE = wordstat
PROTOCOL = WORDSTAT_BATCH_API_V1
BATCH_JOB_ID = BLOOD_SAND_GREENFIELD_2026-09-08__STEP03_PRIMARY_V1
METHOD = getTop
PRIMARY_ITEMS = 79
REGION = 225 / Russia
DEVICES = DEVICE_ALL
NUM_PHRASES = 2000
MAX_REQUESTS = 79
EXPECTED_DIRECT_YANDEX_COST_RUB = 1.58
MAX_COST_RUB = 2.00
```

Bridge production contract:

```text
batch.start/status/pause/resume/cancel = zero provider requests
one batch.next = at most one provider request
no automatic retry after uncertain outcome
complete returned provider payload must be preserved
```

## 8. OR capability gate

Nineteen current V2 primary probes use grouped Wordstat OR syntax.

Official Yandex documentation supports operators in `phrase`, and Bridge accepts phrase strings up to 400 chars, but this exact grouped form has not yet been observed end-to-end in this job.

Therefore Step-03 execution order is intentionally changed while preserving the same 79 seeds:

```text
ITEM 1 = Q001 = (амулет|оберег|талисман) RSOTM
```

After `batch.start`, only one `batch.next` is authorised until Q001 result is persisted/read back and OR behavior is accepted.

If grouped OR fails for syntax/provider reasons:

```text
cancel current batch without further provider calls
→ replace each grouped Q parent with three child probes
→ preserve Q-parent lineage
→ revised request count = 117 total primary items
→ recompute cost/budget before restart
```

## 9. Persistence contract

Every executed provider item must be durably saved before the next provider call:

```text
STEP_03_WORDSTAT_RAW/<batch_order>__<seed_id>.*
```

and reconciled into:

`STEP_03_WORDSTAT_ACQUISITION_RECEIPTS.csv`

Preserve:

```text
command / seed / region / devices / numPhrases
batch item identity / state
request_id
http/provider outcome
complete results[]
complete associations[]
totalCount
cost/request truth
raw file locator
remote readback truth
```

After all terminal items, create complete occurrence authority. If the occurrence universe is large, use ChatGPT Work for full union/transformation/QA; sampling is forbidden.

## 10. Current execution state

```text
DOCUMENTATION_PREPARED = true
ROADMAP_OWNER_APPROVED = true
ORDER_SCOPE_FROZEN = true
STEP_00_COMPLETE = true
STEP_01_COMPLETE = true
STEP_02_COMPLETE = true
STEP_02_V2_QUALITY_TOTAL = 93/100
STEP_02_V2_QUALITY_SCORE = 9.3/10
STEP_03_STARTED = true
STEP_03_PRE_STEP_PROVIDER_GATE = COMPLETE
STEP_03_EXECUTION_MANIFEST_ROWS = 79
STEP_03_BATCH_START_COMMAND = READY
STEP_03_BATCH_STARTED = false
STEP_03_PROVIDER_REQUESTS_STARTED = 0
STEP_03_FIRST_ITEM = Q001_OR_CAPABILITY
STEP_03_COMPLETE = false
NEXT_STEP_ALLOWED = false
NEXT_ACTION = EXECUTE_WORDSTAT_BATCH_START_COMMAND
PROVIDER_CALLS_FOR_KW002_JOB = 0
WORK_HANDOFFS_EXECUTED = 1
```
