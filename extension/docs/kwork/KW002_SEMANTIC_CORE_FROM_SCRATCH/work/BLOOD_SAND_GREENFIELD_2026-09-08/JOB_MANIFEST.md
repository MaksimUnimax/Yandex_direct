# KW-002 JOB MANIFEST — BLOOD_SAND_GREENFIELD_2026-09-08

Status: **STEP05 COMPLETE / STEP06 PRE-STEP V2 PREPARED / STEP06 ACTUAL EXECUTION NOT STARTED / SEARCH RELEASE NOT ISSUED**

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

Frozen authorities:

- `CLIENT_SUPPLIED_BRIEF.md`
- `CLIENT_SUPPLIED_ASSORTMENT_MANIFEST.md`
- `CLIENT_SUPPLIED_PRODUCT_CATALOG_OZON_76.csv`
- `ALLOWED_INPUTS_AND_SEALED_SOURCES.md`

## 3. Clean-baseline boundary

```text
PRIOR BLOOD_SAND WORDSTAT/SEARCH/ALICE/COMPETITOR/CLUSTER/IA RESEARCH = SEALED / FORBIDDEN EXECUTION INPUT
```

Only explicitly allowed current-job evidence may be used.

## 4. Current accepted upstream state

```text
STEP00 = PASS / Ozon-only
STEP01 = PASS / 76 of 76
STEP02 = V2 PASS
STEP03 = PASS / 79 of 79 durable
STEP03A = PASS / 24576 identities / 25979 RAW occurrences
STEP03B = CORRECTED AUTHORITY ACCEPTED / KEEP 5100 / HOLD 13035 / EXCLUDE 6441
STEP04 = W09 CURRENT AUTHORITY ACCEPTED / 32 families / 29 observed / 13 queue rows
STEP05 = COMPLETE / PASS CURRENT RESEARCH SNAPSHOT
STEP06 = NOT STARTED
```

## 5. Step05 final closure

W10C001 was the sole new Step05 provider candidate and was executed exactly once:

```text
candidate_id = W10C001
phrase = (амулет|оберег|талисман) Аум
request_id = wordstat-b3fbe6dd-121b-4e67-81ca-0b03bdc53358
http_status = 200
provider_status = OK
totalCount = 3
results_rows = 0
association_rows = 0
outcome = SUCCESS_WITH_ZERO_ROWS
raw_remote_readback = PASS
new_union_rows = 0
```

Bounded interpretation remains current-snapshot only. `totalCount=3` is not three returned keyword rows and zero returned rows is not universal zero demand.

Step05 closure authority:

`STEP_05_W10_V3_FINAL_CLOSURE_2026-09-12.md`

## 6. Step06 preparation correction

The first Step06 preparation package was prematurely called PASS before the mandatory owner-facing pre-step report existed and contained additional defects. It remains historical and is superseded for execution.

Correction authority:

`STEP_06_PREPARATION_RULE_VIOLATION_AND_CORRECTION_2026-09-12.md`

Historical V1 files, not execution authority:

- `STEP_06_PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_TRACE_2026-09-12.md`
- `STEP_06_REPRESENTATIVE_QUERY_MANIFEST_V1_2026-09-12.tsv`
- `STEP_06_PREPARATION_GATE_2026-09-12.md`

Corrected V2 preparation package:

- `STEP_06_PRE_STEP_EXTERNAL_RESEARCH_V2_2026-09-12.md`
- `STEP_06_REPRESENTATIVE_QUERY_MANIFEST_V2_2026-09-12.tsv`
- `STEP_06_PRE_EXECUTION_GATE_V2_2026-09-12.md`

## 7. Step06 V2 prepared acquisition design

```text
QUERY_ROWS = 22
COVERAGE_DIRECTIONS = 12
QUERY_SOURCE = accepted Step04 W09 observed representative phrases
SEARCH_MODE = ordinary synchronous Yandex Web Search
SEARCH_TYPE = SEARCH_TYPE_RU
REGION = 225 / Russia
PAGE = 0
GROUPS_ON_PAGE = 20
GROUP_MODE = FLAT
FIX_TYPO = OFF
MAX_NORMALIZED_RESULT_ROWS = 440
DAY_MAX_ESTIMATED_COST = 10.736 RUB
NIGHT_MAX_ESTIMATED_COST = 8.052 RUB
GENSEARCH = 0
WORDSTAT = 0
```

Step06 queries are discovery probes, not final keywords, final intents, final clusters or pages.

## 8. Step06 evidence persistence contract

Existing Level1 permits raw **or durable normalized** Search result references.

For Step06, every returned normalized document row and required provenance must be durably preserved and remotely read back before the next provider request. A summary, domain-only list or representative sample is insufficient.

Current branch Search normalization emits all XML `<doc>` rows as `results[]` with rank/url/domain/title/snippet/modtime and serializes the full normalized envelope.

Original provider Base64/XML is not separately required by the current Step06 method if complete required normalized evidence is preserved.

## 9. Current Bridge blocker

Owner's immediately preceding provider output reported installed Bridge runtime `0.1.4`.

Current repository product source reports `0.1.2`, and no `0.1.4` repository source/commit was found in the current preparation recheck.

Therefore:

```text
INSTALLED_SEARCH_RUNTIME_CONTRACT = UNRECONCILED
SEARCH_PROVIDER_EXECUTION_RELEASE = NOT_ISSUED
SEARCH_CALLS_ALLOWED_NOW = 0
```

Before paid Search execution, reconcile installed runtime/schema through a non-provider handshake or authoritative source sync, then issue a separate Step06 Search execution release.

## 10. Work gate

Current Step06 plan is bounded to at most 440 normalized result rows and does not require sampling or truncation in ordinary chat.

```text
WORK_TRIGGER = NOT_MET
WORK_HANDOFF = NOT_REQUIRED
```

If scale later changes materially, re-evaluate under `LEVEL1/WORK_HANDOFF_RULE.md`.

## 11. Current hard boundary

```text
STEP05 = COMPLETE / PASS CURRENT SNAPSHOT
STEP06_PRE_STEP_V1 = SUPERSEDED_FOR_EXECUTION
STEP06_PRE_STEP_V2 = PREPARED
OWNER_FACING_STEP06_DISCLOSURE = REQUIRED_BEFORE_EXECUTION
STEP06_SEARCH_EXECUTION_RELEASED = false
WORDSTAT_CALLS_ALLOWED_NOW = 0
SEARCH_CALLS_ALLOWED_NOW = 0
GENSEARCH_CALLS_ALLOWED_NOW = 0
AI_SEARCH_CALLS_ALLOWED_NOW = 0
STEP06_ACTUAL_EXECUTION = NOT_STARTED
STEP07_STARTED = false
STEP08_STARTED = false
```

## 12. Next action

Complete the mandatory owner-facing Step06 pre-step disclosure in chat. Then, still without a paid provider request, reconcile the installed Search runtime/schema. Only after that and a live-head/current-provider recheck may a separate first Search execution release be materialized.
