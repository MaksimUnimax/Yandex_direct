# KW-002 JOB MANIFEST — BLOOD_SAND_GREENFIELD_2026-09-08

Status: **STEP 03 ACQUISITION COMPLETE / RAW RECOVERY 65/79 / STEP 04 BLOCKED**

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

```text
CANONICAL_PRIMARY_PROBES = 79
CURRENT_PROVIDER_ACQUISITION_OUTCOMES = 79/79
STEP03_PROVIDER_ACQUISITION_COMPLETE = true
INITIAL_LATE_QA_LOSSLESS_GITHUB_FEED_FORWARD_RAW = 60/79
STEP03_DURABLE_RAW_COMPLETE = false
STEP03_DURABLE_RAW_STATUS = CORRECTION / RECOVERY IN PROGRESS
```

Current recovery progress:

```text
RUN_50 = RECOVERED WITHOUT PROVIDER REPLAY
RUN_51 = RECOVERED WITHOUT PROVIDER REPLAY
RUN_32 = NEW CURRENT RECOVERY OBSERVATION / SAVED / READBACK PASS
RUN_33 = NEW CURRENT RECOVERY OBSERVATION / SAVED / READBACK PASS
RUN_34 = NEW CURRENT RECOVERY OBSERVATION / SAVED / READBACK PASS
CURRENT_DURABLE_FEED_FORWARD = 65/79
REMAINING_RUN_ORDERS = 35..48
REMAINING_COUNT = 14
RECOVERY_PROVIDER_REQUESTS = 3
RECOVERY_PROVIDER_ESTIMATED_COST_RUB = 0.06
```

Current recovery authority:

`STEP_03_RAW_RECOVERY_PROGRESS_2026-09-09.json`

## 7. Recovery source and replay boundary

Original full Wordstat delivery text for both affected large blocks was located in preserved prior-dialogue File Library uploads. It remains a recovery source, but large results cannot be safely materialized from truncated snippets in the current file interface.

```text
RECOVERY_SOURCE_FOUND = true
SOURCE_REHYDRATION_PRIORITY = FIRST WHEN LOSSLESS ACCESS EXISTS
PROVIDER_REQUERY = AUTHORIZED FALLBACK
ONE RECOVERY PROVIDER RESULT AT A TIME = REQUIRED
FULL GITHUB WRITE + REMOTE READBACK BEFORE NEXT REQUEST = REQUIRED
```

New recovery request identities never replace historical request IDs.

## 8. Current Bridge/runtime boundary

The recovery observations actually received in this dialogue identify:

```text
OBSERVED_RECOVERY_BRIDGE_VERSION = 0.1.4
OBSERVED_RECOVERY_ACTIVE_SERVICE = wordstat
OBSERVED_RECOVERY_CHANNEL = manual
```

This observation is scoped to the returned recovery provider envelopes and is not a claim about every future browser state.

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
STEP_03_DURABLE_FEED_FORWARD = 65/79
STEP_03_REMAINING_RECOVERY = 14
STEP_04_STARTED = false
STEP_04_COMPLETE = false
NEXT_STEP_ALLOWED = false
NEXT_ACTION = RECOVER_OR_REQUERY_RUN_ORDER_35_EGISHYALM
```

Historical provider economics are preserved separately from the current recovery cost; do not overwrite historical request accounting with the three new recovery observations.
