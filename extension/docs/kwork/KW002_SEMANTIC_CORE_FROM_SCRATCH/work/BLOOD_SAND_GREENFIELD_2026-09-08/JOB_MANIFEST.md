# KW-002 JOB MANIFEST — BLOOD_SAND_GREENFIELD_2026-09-08

Status: **STEP 03 BLOCKED / BRIDGE MV3 LONG WORDSTAT FETCH REPAIR REQUIRED**

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
OZON PRODUCT/LISTING ROWS = 76
WB PRODUCT/LISTING ROWS ACTIVE = 0
```

## 3. Clean-baseline rule

Until Step 20 final freeze:

```text
PRIOR BLOOD_SAND SEO RESEARCH = SEALED / FORBIDDEN EXECUTION INPUT
```

## 4. Universal rules active

```text
LEVEL1/RESULT_QUALITY_SCORING_RULE.md
LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md
```

```text
EACH QUALITY CRITERION = 0–10
QUALITY_TOTAL = 0–100
QUALITY_SCORE = 0–10
PASS = >=90/100 AND >=9.0/10 AND ALL HARD GATES AND NO OPEN CRITICAL DEFECT
```

Fresh internet research + clickable owner-facing source disclosure is mandatory before each major step.

## 5. Accepted upstream truth

```text
STEP_00_COMPLETE = true
STEP_01_COMPLETE = true
STEP_01_MAIN_RETURN_QA = PASS
STEP_02_V1_QUALITY_TOTAL = 65/100
STEP_02_V1_QUALITY_SCORE = 6.5/10
STEP_02_V1_STATUS = SUPERSEDED
STEP_02_V2_PRIMARY = 79
STEP_02_V2_DEFERRED_CONTROL = 49
STEP_02_V2_QUALITY_TOTAL = 93/100
STEP_02_V2_QUALITY_SCORE = 9.3/10
STEP_02_V2_QA = PASS
STEP_02_COMPLETE = true
```

Current upstream seed authority:

`STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv`

## 6. Step 03 provider plan

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

Pre-step authorities:

```text
STEP_03_PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_2026-09-09.md
STEP_03_PRE_STEP_PROVIDER_GATE_2026-09-09.md
STEP_03_WORDSTAT_EXECUTION_MANIFEST_V1.csv
```

## 7. Batch start accepted truth

```text
BRIDGE_RUNTIME_VERSION = 0.1.4
batch.start = OK
total = 79
input_count = 79
duplicate_count = 0
pending = 79
requests_started = 0
estimated_cost_rub = 0
request_executed = false
```

## 8. Executed item 1 — Q001

```text
seed_id = Q001
phrase = (амулет|оберег|талисман) RSOTM
request_id = wordstat-batch-9292c032-e48e-443e-8576-a51ad4b2c8cc
HTTP = 200
item status = SUCCEEDED
elapsed_ms = 1884
provider result = {}
request_executed = true
cost = 0.02 RUB
raw readback = PASS
```

Raw authority:

`STEP_03_WORDSTAT_RAW/001__Q001__wordstat-batch-9292c032-e48e-443e-8576-a51ad4b2c8cc.txt`

Q001 interpretation:

```text
OR operator accepted end-to-end = true
raw provider JSON = {}
empty response compatible with zero/default ProtoJSON fields = true
zero-result serialization explicitly documented by Yandex = false
raw evidence rewritten with synthetic fields = false
```

## 9. Executed item 2 — S001

```text
seed_id = S001
phrase = амулет
request_id = wordstat-batch-93be1f25-c5ff-4b43-a992-b286101d5c2a
item status = OUTCOME_UNKNOWN
reason = REQUEST_OUTCOME_UNKNOWN_NO_RETRY
result_ref = null
request_started_at = 2026-09-09T02:02:05.072Z
completed_at = 2026-09-09T02:02:35.728Z
observed duration = 30.656 s
cost ledger = +0.02 RUB
raw readback = PASS
```

Raw authority:

`STEP_03_WORDSTAT_RAW/002__S001__OUTCOME_UNKNOWN__wordstat-batch-93be1f25-c5ff-4b43-a992-b286101d5c2a.txt`

## 10. Confirmed blocker

Official Chrome documentation states that an MV3 extension service worker is terminated if a `fetch()` response takes more than 30 seconds to arrive:

https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/lifecycle

The current v0.1.4 source family performs Wordstat provider execution through direct `await fetch(...)` in the extension service worker and maps a thrown fetch to `REQUEST_OUTCOME_UNKNOWN_NO_RETRY`.

A repository v0.1.4 authority was identified:

```text
branch = bridge/webmaster-readiness-gzip-v0.1.4
commit = 8bb1365a9905df8a6d7e09917e81444a9b7f1024
```

Exact installed artifact identity is not asserted because the runtime result did not expose its artifact SHA.

Root cause:

```text
ROOT_CAUSE_CONFIDENCE = HIGH
SLOW SYNCHRONOUS WORDSTAT GETTOP (>30s)
+
DIRECT MV3 SERVICE-WORKER FETCH
→ CHROME 30S FETCH-RESPONSE LIMIT
→ OUTCOME_UNKNOWN
```

Current Yandex GetTop documentation reviewed does not specify a matching 30-second provider timeout.

Incident authority:

`STEP_03_BRIDGE_MV3_30S_FETCH_BLOCKER_2026-09-09.md`

Engineering repair handoff:

`extension/docs/WORDSTAT_MV3_LONG_FETCH_REPAIR_HANDOFF_2026-09-09.md`

## 11. Current batch/accounting truth

```text
STEP_03_BATCH_TOTAL = 79
STEP_03_BATCH_PENDING = 77
STEP_03_BATCH_SUCCEEDED = 1
STEP_03_BATCH_OUTCOME_UNKNOWN = 1
STEP_03_BATCH_TERMINAL = 2
STEP_03_PROVIDER_REQUESTS_STARTED = 2
STEP_03_ESTIMATED_COST_RUB = 0.04
STEP_03_STOP_REASON = OUTCOME_UNKNOWN_REQUIRES_RECONCILIATION
STEP_03_NEXT_SAFE_ACTION = RECONCILE_UNKNOWN
STEP_03_THIRD_PROVIDER_REQUEST_ALLOWED = false
STEP_03_AUTO_RETRY_S001_ALLOWED = false
```

Receipt authority:

`STEP_03_WORDSTAT_ACQUISITION_RECEIPTS.csv`

## 12. Current execution state

```text
DOCUMENTATION_PREPARED = true
ROADMAP_OWNER_APPROVED = true
ORDER_SCOPE_FROZEN = true
STEP_00_COMPLETE = true
STEP_01_COMPLETE = true
STEP_02_COMPLETE = true
STEP_03_STARTED = true
STEP_03_PRE_STEP_EXTERNAL_RESEARCH = PASS
STEP_03_PRE_STEP_PROVIDER_GATE = COMPLETE
STEP_03_BATCH_STARTED = true
STEP_03_RUNTIME_BRIDGE_VERSION_OBSERVED = 0.1.4
STEP_03_PROVIDER_REQUESTS_STARTED = 2
STEP_03_Q001_RAW_READBACK = PASS
STEP_03_S001_RAW_READBACK = PASS
STEP_03_BLOCKER = BRIDGE_MV3_WORDSTAT_FETCH_GT_30S
STEP_03_PROVIDER_PROGRESSION = BLOCKED
STEP_03_COMPLETE = false
NEXT_STEP_ALLOWED = false
NEXT_ACTION = REPAIR_AND_ACCEPT_LONG_WORDSTAT_TRANSPORT_BEFORE_NEW_ACQUISITION_REVISION
PROVIDER_CALLS_FOR_KW002_JOB = 2
WORK_HANDOFFS_EXECUTED = 1
```

Do not replay the historical S001 request automatically. After Bridge repair, preserve this blocked batch as history and begin a new Step-03 acquisition revision with explicit new request lineage.
