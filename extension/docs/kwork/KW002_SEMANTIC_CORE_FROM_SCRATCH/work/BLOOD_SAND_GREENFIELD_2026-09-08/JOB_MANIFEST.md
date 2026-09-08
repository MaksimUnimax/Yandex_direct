# KW-002 JOB MANIFEST — BLOOD_SAND_GREENFIELD_2026-09-08

Status: **STEP 02 REWORK_REQUIRED AFTER EXTERNAL METHOD AUDIT / STEP 03 BLOCKED**

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
Assortment authority for this KW-002 test = Ozon only
Primary market/search geography = Russia
New owned website planned = YES
```

## 3. Current authoritative assortment input

```text
CLIENT_SUPPLIED_BRIEF.md
CLIENT_SUPPLIED_ASSORTMENT_MANIFEST.md
CLIENT_SUPPLIED_PRODUCT_CATALOG_OZON_76.csv
ALLOWED_INPUTS_AND_SEALED_SOURCES.md
```

Accounting:

```text
OZON PRODUCT/LISTING ROWS = 76
WB PRODUCT/LISTING ROWS ACTIVE = 0
CROSS_PLATFORM RECONCILIATION = NOT APPLICABLE
```

## 4. Clean-baseline rule

Until Step 20 final freeze:

```text
PRIOR BLOOD_SAND SEO RESEARCH = SEALED / FORBIDDEN EXECUTION INPUT
DEFAULT BLOOD_SAND PROJECT MATERIAL = DENY
EXCEPTIONS = exact sources whitelisted in ALLOWED_INPUTS_AND_SEALED_SOURCES.md
```

## 5. Step 01 accepted truth

```text
STEP_01_INPUT_ROWS_ACCOUNTED = 76
STEP_01_SILENT_DROPS = 0
STEP_01_WB_ROWS_USED = 0
STEP_01_NEUTRAL_CONCEPTS = 4
STEP_01_AMBIGUITY_ISSUES = 10
STEP_01_REMOTE_GITHUB_READBACK = PASS
STEP_01_MAIN_RETURN_QA = PASS
STEP_01_COMPLETE = true
```

## 6. Step 02 historical materialization

Historical files remain authoritative for what version 1 contained:

```text
STEP_02_PRE_STEP_REVIEW_2026-09-08.md
STEP_02_SEED_MAP.csv
STEP_02_COVERAGE_MATRIX.csv
STEP_02_DEFERRED_OR_TARGETED_PROBES.csv
STEP_02_REPORT.md
STEP_02_QA_REPORT.md
```

Version-1 accounting remains:

```text
STEP_02_V1_SEED_ROWS_TOTAL = 97
STEP_02_V1_PRIMARY_SEEDS = 67
STEP_02_V1_DEFERRED_TARGETED_SEEDS = 30
STEP_02_V1_DUPLICATE_NORMALIZED_SEEDS = 0
STEP_02_V1_COVERAGE_ROWS = 76
STEP_02_V1_WORDSTAT_CALLS = 0
STEP_02_V1_REMOTE_READBACK = PASS
```

## 7. Step 02 external method audit

Superseding authority:

```text
STEP_02_EXTERNAL_METHOD_AUDIT_2026-09-08.md
```

External materials used include current official Yandex Webmaster, Yandex Direct, Wordstat GetTop/operators/pricing documentation and Ahrefs/Semrush seed-keyword/ecommerce guidance.

Audit verdict:

```text
STEP_02_PREVIOUS_PASS = INVALIDATED
STEP_02_STATUS = REWORK_REQUIRED
STEP_03_ALLOWED = false
```

Main defects:

```text
1. catalog-route coverage was treated as if it proved search-probe quality;
2. high-noise bare-name seeds were PRIMARY without mandatory qualified/refinement route;
3. automobile use-context synonyms/variants were not systematically covered;
4. primary set is too dependent on exact seller names;
5. expected_information_gain rationale is boilerplate for many exact-name seeds;
6. PRIMARY/DEFERRED rationale must not be driven by trivial direct Yandex API cost.
```

## 8. Required Step 02 correction

Before Step 03:

```text
- rebuild primary/deferred seed priorities;
- add probe-quality coverage gate, not only card-lineage coverage;
- require qualified/refinement route for high-noise bare seeds;
- add bounded synonym/use-context coverage for car-related demand;
- rebalance broad/qualified/exact-name/alternate-writing/brand probes;
- replace generic information-gain text with discriminating rationale;
- rerun adversarial QA;
- perform remote GitHub readback.
```

## 9. Current execution state

```text
DOCUMENTATION_PREPARED = true
ROADMAP_OWNER_APPROVED = true
ORDER_SCOPE_FROZEN = true
STEP_00_COMPLETE = true
STEP_01_COMPLETE = true
STEP_01_MAIN_RETURN_QA = PASS
STEP_02_STARTED = true
STEP_02_V1_MATERIALIZED = true
STEP_02_EXTERNAL_METHOD_AUDIT = COMPLETE
STEP_02_EXTERNAL_METHOD_VERDICT = FAIL
STEP_02_COMPLETE = false
STEP_02_STATUS = REWORK_REQUIRED
STEP_03_STARTED = false
NEXT_STEP_ALLOWED = false
NEXT_STEP = STEP_02_REWORK
PROVIDER_CALLS_FOR_KW002_JOB = 0
WORK_HANDOFFS_EXECUTED = 1
```