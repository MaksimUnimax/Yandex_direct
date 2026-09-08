# KW-002 JOB MANIFEST — BLOOD_SAND_GREENFIELD_2026-09-08

Status: **CLIENT INPUT MATERIALIZED / NOT STARTED / OWNER ROADMAP REVIEW REQUIRED**

## 1. Job identity

```text
KW_ID = KW-002
JOB_ID = BLOOD_SAND_GREENFIELD_2026-09-08
JOB_TYPE = PRODUCTIZATION_REHEARSAL
EXECUTION_MODE = CLEAN_FROM_SCRATCH
BUSINESS = Blood & Sand / «Кровь и Песок»
SITE_STATE = NEW_SITE / no existing production site is an analytical baseline
REGION = Russia
LANGUAGE = Russian
PRIMARY_SEARCH_ENGINE = Yandex
```

## 2. Frozen simulated client brief

Canonical client-input authorities:

```text
CLIENT_SUPPLIED_BRIEF.md
CLIENT_SUPPLIED_ASSORTMENT_MANIFEST.md
```

The rehearsal imitates a real Kwork buyer who wants the semantic core and future site structure built from scratch and has not supplied prior SEO research.

### Business facts supplied by the client

```text
- Brand: «Кровь и Песок» / Blood & Sand.
- Business: product brand / seller.
- What the client says it sells: амулеты, обереги и талисманы; в ассортименте есть в том числе товары для автомобиля.
- Existing sales channels: Ozon and Wildberries.
- Primary market / SEO geography: Russia.
- Delivery geography stated by client: Russia / nationwide.
- A new owned website is planned.
```

The analyst must not replace the client wording with a narrower invented category before Step 01/02 research.

### Future-site goal supplied by the client

```text
Yandex user should be able to:
1. discover the brand/products;
2. understand what products exist and how they differ;
3. choose an appropriate product;
4. proceed toward purchase.
```

Purchase may later be direct and/or through marketplace links. The exact final direct-vs-marketplace checkout architecture is not fixed by this KW-002 order.

## 3. Exact assortment supplied by the client

The client supplies concrete marketplace listing/product facts rather than an SEO category tree.

### Wildberries

Source checked:

```text
MaksimUnimax/blood_sand
marketing/data/normalized/marketplace/wildberries/20260908__wb__cards-list__fresh-current108-identities.csv
```

Client scope decision for this order:

```text
WB account listing rows observed = 108
WB in-scope listing rows = 88
WB other seller-line rows explicitly out of scope = 20
```

The 88 exact in-scope rows are copied into:

```text
CLIENT_SUPPLIED_PRODUCT_CATALOG.csv
```

The 20 client-declared out-of-scope rows are copied into:

```text
CLIENT_SUPPLIED_OUT_OF_SCOPE_SELLER_LINES.csv
```

### Ozon

Source checked:

```text
MaksimUnimax/blood_sand
marketing/data/raw/marketplace/ozon/20260811T1025Z__ozon__stocks-current__all.json
```

Returned listing/product identities = **76**.

The 76 exact rows are copied into:

```text
CLIENT_SUPPLIED_PRODUCT_CATALOG_OZON_76.csv
```

### Intake accounting

```text
TOTAL IN-SCOPE MARKETPLACE LISTING ROWS ADMITTED BEFORE CROSS-PLATFORM RECONCILIATION = 164
CROSS-PLATFORM UNIQUE PRODUCT COUNT = NOT YET DETERMINED
```

This distinction is mandatory:

```text
MARKETPLACE LISTING ROW != UNIQUE PRODUCT MODEL
SAME/RELATED TITLE ON TWO MARKETPLACES != AUTOMATIC SAME PRODUCT/VARIANT
PRODUCT TITLE != PROVEN SEARCH TERM
PRODUCT EXISTS != SEO PRIORITY
PRODUCT EXISTS != AUTOMATIC SEPARATE PAGE
```

Step 01 must reconcile duplicates, variants, families and actual product boundaries from the client-supplied catalog without importing old Blood & Sand SEO conclusions.

## 4. Client-supplied product examples

The exact catalog rows are the authority. Actual supplied names include, among others:

```text
Печать Велеса
Велес / Знак Велеса
Алатырь (Крест Сварога)
Макошь
Родимич
Хорс
Мара
Стрибог
Семаргл
Всеславец
Сварог
Чур
Чернобог
Боговник
Триглав
Звезда Лады
Ратиборец
Белобог
Даждьбог
Жива
Молвинец
Знич
Перун
Звезда Руси
Вегвизир / Рунический компас
Древо Жизни
Гунгнир
Валькнут
Шлем ужаса / Эгисхьяльм
Инь и Ян
Ом / Аум
Бусидо - Путь Воина
Молитва Иоанна Златоуста
Спаси и Сохрани
Герб России
Русская Община
RSOTM
Soldier Of Fortune
12 знаков зодиака и несколько фактических серий/вариантов
```

Do not turn this example list into the Step-01 catalog; use all admitted rows.

## 5. What the client did NOT supply

```text
existing semantic core = NONE
existing keyword list = NONE
existing SEO page map = NONE
existing final site architecture = NONE
existing target URL list = NONE
existing category structure that must be preserved = NONE
existing SEO competitor list = NONE
existing intent classification = NONE
existing clustering = NONE
existing keyword-to-page mapping = NONE
existing Search/SERP conclusions = NONE
existing Alice/AI-search conclusions = NONE
```

The lack of these inputs is intentional. KW-002 must research them from scratch.

## 6. Competitors supplied by client

```text
CLIENT_SUPPLIED_COMPETITORS = NONE
```

Real organic competitors must be independently discovered from current Yandex results in the relevant Level-2 step.

## 7. Business / truth constraints supplied by the client

```text
- do not invent products or services that are not actually sold;
- use the client-supplied product catalogs as the assortment authority;
- keep the 20 client-declared unrelated WB seller lines outside this website order;
- do not pre-cluster the catalog into SEO categories at intake;
- symbolic/mystical statements must not be presented as proven physical effects;
- do not guarantee Yandex position, traffic, sales or Alice AI inclusion/citation;
- do not invent the final direct-vs-marketplace checkout model inside this order;
- full website copywriting is outside this order;
- web design/development is outside this order.
```

## 8. Requested result of the KW-002 order

Produce a site-ready semantic architecture from scratch:

```text
complete in-scope Yandex demand evidence within the frozen business scope
cleaned semantic core
user-task / intent classification
current-Yandex-SERP-backed clusters
query -> target-page mapping
planned site IA
Page Jobs / role of each planned search page
recommended internal-link relationships
competitor-derived semantic gaps with actual demand validation
Search-vs-AI-search decision evidence where decision-relevant
client-ready deliverables
```

No artificial fixed final-keyword count is a job target.

## 9. What KW-002 must research rather than receive from the client

```text
search vocabulary
search-demand universe
frequency/demand observations
seasonality where material
real organic competitors
competitor-derived missing demand
search intent
SERP result/page-type patterns
cross-marketplace unique product/variant model where needed for search architecture
cluster boundaries
same-page vs separate-page decisions
query-to-page ownership
final site IA
Page Jobs
internal-link model
whether bounded AI-search evidence changes, enriches, de-risks or leaves unchanged the Search-only decisions
```

## 10. Explicit exclusions from this Kwork

```text
client-site economics / CAC / margin modeling
full website text writing
web design
technical website implementation
technical SEO crawler audit
ranking guarantees
Alice citation guarantees
reverse-domain keyword-universe claims without an authorized supporting provider/export
```

## 11. Prior-research contamination rule

Until the new KW-002 result is fully frozen after Step 20:

```text
PRIOR BLOOD_SAND SEO RESEARCH = SEALED / FORBIDDEN EXECUTION INPUT
```

This includes prior Wordstat, Search, Alice, opportunity, competitor, buyer-research conclusions, clustering and page-architecture conclusions.

The current conversation's memory of those conclusions is not evidence and must not be passed to a clean Work/execution context.

## 12. Allowed source authority

Exact whitelist is governed by:

```text
ALLOWED_INPUTS_AND_SEALED_SOURCES.md
```

Current admitted job inputs before fresh KW-002 acquisition:

```text
KW002 Level 1 rules
KW002 Level 2 step rules
CLIENT_SUPPLIED_BRIEF.md
CLIENT_SUPPLIED_ASSORTMENT_MANIFEST.md
CLIENT_SUPPLIED_PRODUCT_CATALOG.csv
CLIENT_SUPPLIED_PRODUCT_CATALOG_OZON_76.csv
CLIENT_SUPPLIED_OUT_OF_SCOPE_SELLER_LINES.csv
JOB_MANIFEST.md / JOB_FLOW.md
the two exact marketplace source artifacts admitted in the source whitelist
current external method sources when authorized for a step
```

All other Blood & Sand analytical sources are denied by default.

## 13. Execution context

Each large-data Work handoff must receive only:

```text
KW002 LEVEL1
KW002 relevant LEVEL2 step
this job workspace allowed sources
current accepted upstream job artifacts
owner canonical Work prompt
```

No unlisted Blood & Sand research files may be opened.

## 14. Acceptance state

```text
DOCUMENTATION_PREPARED = true
CLIENT_SUPPLIED_BRIEF_MATERIALIZED = true
CLIENT_ASSORTMENT_MANIFEST_MATERIALIZED = true
CLIENT_PRODUCT_CATALOG_WB_IN_SCOPE_ROWS = 88
CLIENT_PRODUCT_CATALOG_OZON_ROWS = 76
CLIENT_OTHER_WB_ROWS_EXCLUDED = 20
CLIENT_IN_SCOPE_LISTING_ROWS_BEFORE_RECONCILIATION = 164
CROSS_PLATFORM_UNIQUE_PRODUCT_COUNT = NOT_YET_DETERMINED
CLIENT_SOURCE_BOUNDARY_FROZEN = true
RAW_ASSORTMENT_SOURCE_COUNT = 2
ROADMAP_OWNER_APPROVED = false
STEP_00_STARTED = false
PROVIDER_CALLS_FOR_KW002_JOB = 0
WORK_HANDOFFS_FOR_KW002_JOB = 0
```

Do not begin analysis/provider acquisition until the owner accepts the prepared documentation/roadmap.
