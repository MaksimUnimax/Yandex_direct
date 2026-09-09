# KW-002 JOB MANIFEST — BLOOD_SAND_GREENFIELD_2026-09-08

Status: **STEP 03 ACQUISITION COMPLETE / RAW RECOVERY REQUIRED / STEP 04 BLOCKED**

## 1. Job identity

```text
KW_ID = KW-002
JOB_ID = BLOOD_SAND_GREENFIELD_2026-09-08
JOB_TYPE = PRODUCTIZATION_REHEARSAL
EXECUTION_MODE = CLEAN_FROM_SCRATCH
BUSINESS = Blood & Sand / «Кровь и Песок»
SITE = кровьипесок.рф
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

```text
PRIOR BLOOD_SAND WORDSTAT/SEARCH/ALICE/COMPETITOR/CLUSTER/IA RESEARCH = SEALED / FORBIDDEN EXECUTION INPUT
```

Use only sources allowed by `ALLOWED_INPUTS_AND_SEALED_SOURCES.md`.

## 4. Accepted upstream truth

```text
STEP_00_COMPLETE = true
STEP_01_COMPLETE = true
STEP_01_ASSORTMENT_ROWS = 76/76
STEP_02_V1_STATUS = SUPERSEDED
STEP_02_V1_QUALITY = 65/100
STEP_02_V2_PRIMARY = 79
STEP_02_V2_DEFERRED_CONTROL = 49
STEP_02_V2_QUALITY = 93/100 = 9.3/10
STEP_02_COMPLETE = true
```

Canonical seed authority:

`STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv`

## 5. Step 03 acquisition contract

```text
SERVICE = wordstat
METHOD = getTop
CANONICAL_PRIMARY_ITEMS = 79
REGION = 225 / Russia
DEVICES = DEVICE_ALL
NUM_PHRASES = 2000
```

Historical batch/requery receipts and original request identities remain preserved in Step03 evidence. Do not rewrite an old request ID as a new observation.

## 6. Step 03 current truth

The early `2 requests / MV3 >30s` state is historical and has been superseded by later acquisition work.

Current canonical acquisition coverage:

```text
CANONICAL_PRIMARY_PROBES = 79
CURRENT_PROVIDER_ACQUISITION_OUTCOMES = 79/79
STEP03_PROVIDER_ACQUISITION_COMPLETE = true
```

Late downstream QA then proved that acquisition completeness and durable feed-forward completeness are not the same thing.

```text
LOSSLESS_GITHUB_FEED_FORWARD_RAW = 60/79
AFFECTED_RUN_ORDERS = 32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51
STEP03_DURABLE_RAW_COMPLETE = false
STEP03_DURABLE_RAW_STATUS = CORRECTION / REWORK REQUIRED
```

Correction authorities:

- `STEP_03_RAW_RECOVERY_2026-09-09.md`
- `STEP_03_WORDSTAT_RAW_PERSISTENCE_STATE_2026-09-09.md`
- `STEP_04_WORK_RETURN_RECEIPT_2026-09-09.md`

## 7. Recovery source and replay boundary

Original full Wordstat delivery text for both affected large blocks was located in preserved prior-dialogue File Library uploads. It is a recovery source only until materialized into durable GitHub evidence.

```text
RECOVERY_SOURCE_FOUND = true
SOURCE_REHYDRATION_PRIORITY = FIRST
PROVIDER_REQUERY = FALLBACK_ONLY_IF_SOURCE_RECOVERY_IS_INSUFFICIENT
PROVIDER_REQUESTS_DURING_CURRENT_RECOVERY = 0
PROVIDER_COST_DURING_CURRENT_RECOVERY = 0
```

Owner has authorized re-collection if genuinely needed. If any probe must be re-queried, use new request identity and persist/read back the complete result before the next paid request.

## 8. Current Bridge/runtime boundary

The repository source version and historical browser runtime version are separate facts. The active installed Bridge version/service/mode in the current browser session is not asserted without runtime readback.

```text
CURRENT_INSTALLED_BRIDGE_VERSION = UNKNOWN
CURRENT_ACTIVE_SERVICE = UNKNOWN
CURRENT_MANUAL_AUTORUN_STATE = UNKNOWN
```

No provider action may be claimed from this session unless those runtime facts are actually available.

## 9. Step 04 independent gate

Step04 is not executed.

Current Level2 index remains an owner-review draft unless a later explicit owner decision is reconciled:

```text
LEVEL2_STEP_RULES_INDEX = DRAFT FOR OWNER REVIEW / DO NOT EXECUTE YET
```

Step04 requires both:

```text
STEP03_LOSSLESS_FEED_FORWARD = 79/79
LEVEL2_STEP04_METHOD_AUTHORITY = ACCEPTED
```

## 10. Current execution cursor

```text
DOCUMENTATION_PREPARED = true
ORDER_SCOPE_FROZEN = true
STEP_00_COMPLETE = true
STEP_01_COMPLETE = true
STEP_02_COMPLETE = true
STEP_03_PROVIDER_ACQUISITION_COMPLETE = true
STEP_03_DURABLE_RAW_COMPLETE = false
STEP_03_RAW_RECOVERY_SOURCE_FOUND = true
STEP_04_STARTED = false
STEP_04_COMPLETE = false
NEXT_STEP_ALLOWED = false
NEXT_ACTION = MATERIALIZE_AND_VERIFY_FULL_RAW_FOR_19_AFFECTED_PROBES
```

Do not infer a provider-call total from the obsolete early two-request state. Historical provider economics must be reconciled from the complete acquisition receipts when economics are measured at the later roadmap stage.
