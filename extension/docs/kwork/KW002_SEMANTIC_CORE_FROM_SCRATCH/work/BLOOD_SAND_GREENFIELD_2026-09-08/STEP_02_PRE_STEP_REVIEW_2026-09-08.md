# KW-002 Blood & Sand — STEP 02 PRE-STEP REVIEW

Date: 2026-09-08  
Status: **PRE-STEP REVIEW COMPLETE / AWAITING OWNER AUTHORIZATION / EXECUTION NOT STARTED**  
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`

## 1. Whole Kwork goal

Build from scratch a client-ready semantic core and planned site architecture for modern Yandex from the frozen client business facts/catalog plus fresh KW-002 evidence.

```text
business + exact assortment
→ seed/acquisition probes
→ Wordstat demand
→ coverage control
→ real Yandex competitors
→ competitor-derived expansion
→ candidate semantic master
→ row-level cleanup / user task / intent
→ ordinary Yandex Search evidence
→ task/SERP clustering
→ query→page ownership + Search-only IA
→ bounded generative-Yandex/Alice evidence
→ Search-vs-AI reconciliation
→ final core + IA + Page Jobs + internal links
→ client deliverables + QA
```

## 2. Full roadmap / progress

| Step | What it does | Status |
|---|---|---|
| 00 | Freeze order/client/source boundary | ✅ COMPLETE / Ozon-only correction applied |
| 01 | Build factual business + complete 76-card Ozon assortment model | ✅ COMPLETE / PASS / main return QA PASS |
| 02 | Build seed/acquisition probe map | 🟡 CURRENT / PRE-STEP REVIEW COMPLETE / EXECUTION NOT STARTED |
| 03 | Collect primary Wordstat demand | ⬜ NOT STARTED |
| 04 | First family-level triage | ⬜ NOT STARTED |
| 05 | Targeted second acquisition for named gaps | ⬜ NOT STARTED |
| 06 | Discover real current organic competitors in Yandex | ⬜ NOT STARTED |
| 07 | Extract missed candidate topics from competitor pages | ⬜ NOT STARTED |
| 08 | Test competitor-derived topics in Wordstat | ⬜ NOT STARTED |
| 09 | Freeze candidate semantic master | ⬜ NOT STARTED |
| 10 | Row-level relevance / task / intent cleanup | ⬜ NOT STARTED |
| 11 | Freeze retained semantic set before structural Search decisions | ⬜ NOT STARTED |
| 12 | Collect ordinary Yandex Search/TOP evidence | ⬜ NOT STARTED |
| 13 | Cluster by task + intent + current SERP evidence | ⬜ NOT STARTED |
| 14 | Build query→page map + Search-only IA | ⬜ NOT STARTED |
| 15 | Select bounded AI-search diagnostic/control cases | ⬜ NOT STARTED |
| 16 | Collect Yandex generative/Alice evidence | ⬜ NOT STARTED |
| 17 | Compare Search-only decisions with AI evidence | ⬜ NOT STARTED |
| 18 | Freeze final core + IA + Page Jobs + internal links | ⬜ NOT STARTED |
| 19 | Produce client deliverables | ⬜ NOT STARTED |
| 20 | Data/workbook/recipient QA | ⬜ NOT STARTED |
| 21 | Revision rehearsal + Kwork execution/cost measurement | ⬜ NOT STARTED |
| 22 | Final handoff / close | ⬜ NOT STARTED |

## 3. Completed work

```text
Step 00 frozen order/source boundary = PASS
Step 01 Ozon-only input = 76/76 rows processed
Step 01 silent drops = 0
Step 01 WB rows used = 0
Step 01 old-research contamination = 0
Step 01 neutral accounting model = 4 directions / membership 76
Step 01 ambiguity ledger = 10 governed uncertainty issues
Step 01 Work return QA = PASS
Step 01 main-workflow return QA = PASS
```

## 4. Current Step 02 goal

Create a reproducible set of demand-discovery probes for Wordstat that covers the factual business and assortment without pretending those probes are already accepted keywords, clusters or pages.

```text
SEED = MEASUREMENT / DISCOVERY INPUT
SEED != FINAL KEYWORD
SEED != FINAL CLUSTER
SEED != FUTURE PAGE
```

## 5. What Step 02 solves

The client catalog contains product names and limited form/use words, but users may search with:

- broader product words;
- synonyms;
- use-case wording;
- exact symbol/product names;
- alternative spellings visible in client titles;
- more specific or more general wording unknown to the client.

Step 02 designs probes so Step 03 can ask Wordstat what people actually search for instead of treating catalog wording as search truth.

## 6. Required Step-02 inputs

Primary accepted authorities:

```text
CLIENT_SUPPLIED_BRIEF.md
CLIENT_SUPPLIED_PRODUCT_CATALOG_OZON_76.csv
STEP_01_OZON_LISTING_MODEL.csv
STEP_01_ASSORTMENT_CONCEPT_MODEL.csv
STEP_01_BUSINESS_AND_ASSORTMENT_MODEL.md
STEP_01_UNKNOWN_OR_AMBIGUITY_LEDGER.csv
STEP_01_QA_REPORT.md
STEP_01_MAIN_CHATGPT_RETURN_QA_2026-09-08.md
```

Old Blood & Sand Wordstat/Search/Alice/competitor/cluster/IA research remains prohibited.

## 7. Relevant prior errors / non-repeat controls

### Error A — analyst-created vocabulary became business/search truth too early

Control:

```text
SEED SOURCE AND PURPOSE MUST BE EXPLICIT
ANALYST-COMPOSED PROBE MUST BE LABELLED AS COMPOSED
COMPOSED PROBE != CLIENT WORDING
```

Verify: no analyst-composed phrase is represented as a client-supplied term.

### Error B — client title treated as proven search term

Control:

```text
CLIENT TITLE / PRODUCT NAME -> POSSIBLE PROBE
NOT -> ACCEPTED KEYWORD
```

Verify: every seed output has `seed_role = DISCOVERY_PROBE`, not KEEP/final status.

### Error C — Step-01 accounting buckets could be promoted to SEO categories

Control:

`NAC-04` and all Step-01 neutral buckets are evidence summaries only.

Verify: no seed family is justified merely because `neutral_assortment_concept_id` exists.

### Error D — uncertain product facts could be used to build over-specific probes

Control:

Step-01 ambiguity ledger governs whether a dimension may be used.

Verify: missing form/material/size/use is not invented inside a seed.

### Error E — too few seeds create coverage blindness; too many arbitrary combinations create noise/cost

Control:

Each seed must state a specific discovery purpose and expected information gain. No magic target count.

Verify: seeds without named purpose = 0; redundant probes require explicit reason.

## 8. Current external method sources

### OFFICIAL_YANDEX — Wordstat overview

https://yandex.ru/support2/wordstat/ru/

Supports: Wordstat shows query statistics, top queries containing selected words and other queries searched on the same topic.

### OFFICIAL_YANDEX — Wordstat API structure

https://yandex.ru/support2/wordstat/en/content/api-structure

Supports: `/v1/topRequests` returns recent popular queries containing the supplied phrase and similar queries. Therefore a supplied phrase can act as an acquisition probe rather than a final keyword decision.

### OFFICIAL_YANDEX — Webmaster targeting guidance

https://yandex.ru/support/webmaster/en/recommendations/targeting

Supports: start with words/phrases that describe the product/service and inspect containing plus related queries to understand how users formulate needs.

### OFFICIAL_YANDEX — Wordstat operators

https://yandex.ru/support2/wordstat/ru/content/operators

Supports: operators may deliberately constrain word count/order/forms. They are measurement tools and must not be confused with broad unquoted demand.

### INDUSTRY_PRACTICE — Ahrefs seed keyword guidance

https://ahrefs.com/seo/glossary/seed-keywords/

Supports: multiple relevant seed terms around the core offer are starting points for discovering keyword ideas and subtopics; generated ideas still require later evaluation.

## 9. Source-to-method trace

| Method element | Source class | Supported claim | Project-specific application | Executable output |
|---|---|---|---|---|
| Seed is an acquisition probe | OFFICIAL_YANDEX + inherited KW001 | Wordstat expands a supplied phrase into containing/similar real queries | preserve seed purpose/lineage separately from later keyword decisions | seed map row |
| Use actual product/service wording as starting vocabulary | OFFICIAL_YANDEX | query research can start from words describing product/service | use client business wording + explicit Ozon title vocabulary | factual seed class |
| Use multiple relevant seeds, not one generic head term | INDUSTRY_PRACTICE | broader seed coverage reveals more subtopics | cover broad class/use/name/alias dimensions without arbitrary combinations | coverage matrix |
| Operators are scoped measurements, not default seeds | OFFICIAL_YANDEX | operators change matching semantics | only add operator probe when exact measurement question is named | operator_mode field |
| No fixed seed count | PROJECT_SPECIFIC / information-gain rule | external sources do not define one universal correct number | stop when all factual dimensions have probes and additional seed adds no distinct discovery purpose | stop rationale |

## 10. Proposed seed classes

The execution should consider these classes independently; not every class must produce the same number of seeds.

### A. CLIENT_HEAD_CLASS

Direct client business words:

```text
амулет
оберег
талисман
```

Purpose: discover broad vocabulary and related demand around the business classes the client explicitly supplied.

### B. EXPLICIT_USE_OR_FORM

Only factual title/use language from Step 01, for example:

```text
чётки
талисман в машину
```

Purpose: discover whether form/use language maps to material Yandex demand.

### C. ANALYST_COMPOSED_USE_DIAGNOSTIC

A limited set of combinations made only from separately frozen client facts, for example combining a client class word with the confirmed fact that the assortment includes car products.

These must be explicitly labelled:

```text
source_type = ANALYST_COMPOSED_DIAGNOSTIC
```

Purpose: test vocabulary formulations the client did not literally provide without pretending they are client wording.

### D. EXACT_NAMED_PRODUCT_OR_SYMBOL

Use explicit product/symbol names from the 76-card catalog as independent discovery probes where materially distinct.

Purpose: test whether each named offer direction has actual search vocabulary/demand around it.

### E. EXPLICIT_ALIAS_OR_ALTERNATE_WRITING

Examples visible in client titles:

```text
Рунический компас
Gungner
Копьё Одина
Valknut
Узел павших
ॐ
Аум
Крест Сварога
```

Purpose: discover whether alternate title wording reveals materially different or additional query vocabulary.

Do not claim the aliases are historically/linguistically equivalent simply because the client title places them together.

### F. ZODIAC_FAMILY

Use the explicit client wording `знак зодиака` as a family probe.

Individual signs and composed variants may be planned only with a named purpose so that broad astrology noise does not explode without information gain.

### G. VARIANT_MARKER_DIAGNOSTIC

`Античность`, `Античность 2`, `Символы`, `Логотип` are NOT standalone primary seeds by default.

They may only be used in a scoped combination where the exact question is whether users search that supplied variant wording.

### H. BRAND

Blood & Sand / «Кровь и Песок» may be preserved as a separate brand probe class, but brand ambiguity must be explicit and it must not substitute for non-brand demand acquisition.

## 11. Required seed-map fields

At minimum:

```text
seed_id
seed_phrase
seed_class
seed_source_type
source_product_ids_or_business_fact
source_exact_terms
seed_purpose
question_to_resolve
expected_information_gain
region
planned_wordstat_mode
operator_mode
priority_for_primary_acquisition
known_noise_risk
claim_boundary
status
```

Allowed `seed_source_type` examples:

```text
CLIENT_BUSINESS_WORDING
EXPLICIT_OZON_TITLE_TERM
EXPLICIT_OZON_ALIAS
ANALYST_COMPOSED_DIAGNOSTIC
BRAND_FACT
```

All Step-02 rows remain:

```text
DISCOVERY_PROBE
```

No `KEEP`, final intent, cluster or page result is allowed in Step 02.

## 12. Proposed execution sequence

```text
1. enumerate complete factual vocabulary from Step 01;
2. separate broad classes / forms / use context / exact names / aliases / variants / brand;
3. normalize exact duplicate probes without destroying source lineage;
4. create only information-gaining composed probes;
5. identify likely noise/ambiguity risk per seed;
6. decide primary Wordstat vs deferred/targeted probe;
7. verify every material factual assortment direction has at least one acquisition route;
8. adversarially check for missing names and arbitrary combinations;
9. freeze Step-03 Wordstat acquisition manifest separately after Step 02 passes.
```

## 13. Work / Bridge decision

```text
CHATGPT_WORK_REQUIRED = false for Step 02 under current input
BRIDGE_REQUIRED = false
WORDSTAT_CALLS_ALLOWED_IN_STEP02 = 0
SEARCH_CALLS_ALLOWED_IN_STEP02 = 0
AI_SEARCH_CALLS_ALLOWED_IN_STEP02 = 0
PROVIDER_COST_EXPECTED = 0 RUB
```

Reason: Step 02 is methodical probe design over a 76-row already-normalized catalog, not a large pairwise/join operation. If execution proves otherwise, stop and trigger Work rather than sampling.

## 14. Required outputs

Proposed durable outputs:

```text
STEP_02_SEED_MAP.csv
STEP_02_COVERAGE_MATRIX.csv
STEP_02_DEFERRED_OR_TARGETED_PROBES.csv
STEP_02_REPORT.md
STEP_02_QA_REPORT.md
```

After QA only:

```text
JOB_MANIFEST.md
JOB_FLOW.md
```

## 15. Step-02 PASS gate

```text
ALL_SEEDS_HAVE_SOURCE_LINEAGE = true
ALL_SEEDS_HAVE_EXPLICIT_PURPOSE = true
ALL_SEEDS_STATUS = DISCOVERY_PROBE
CLIENT_TERMS_NOT_RELABELLED_AS_DEMAND = true
ANALYST_COMPOSED_SEEDS_EXPLICITLY_LABELLED = true
STEP01_NAC_BUCKETS_USED_AS_SEO_TAXONOMY = 0
UNSUPPORTED_PRODUCT_FACTS_USED = 0
MATERIAL_CLIENT_ASSORTMENT_DIRECTIONS_WITHOUT_PROBE_ROUTE = 0
REDUNDANT_SEEDS_WITHOUT_INFORMATION_GAIN_REASON = 0
STANDALONE_INTERNAL_VARIANT_MARKER_SEEDS_WITHOUT_JUSTIFICATION = 0
WORDSTAT_CALLS = 0
SEARCH_CALLS = 0
AI_SEARCH_CALLS = 0
OLD_RESEARCH_CONTAMINATION = 0
QA = PASS
REMOTE_GITHUB_READBACK = PASS
```

Then:

```text
STEP_02 = COMPLETE / PASS
NEXT_STEP_ALLOWED = true
NEXT_STEP = STEP_03_PRIMARY_WORDSTAT_ACQUISITION
```

## 16. What Step 02 explicitly does NOT decide

```text
a phrase has search demand
a phrase belongs in the final semantic core
frequency
intent
cluster
page
site category
SEO priority
competitor visibility
Alice/AI behavior
```

## ПРОСТЫМИ СЛОВАМИ

### Зачем нужен этот шаг

Чтобы перед Wordstat не бросать туда случайный набор слов и не пропустить часть реального ассортимента.

### Что конкретно будем делать

Возьмём все реальные названия и немногочисленные подтверждённые товарные слова из Ozon-каталога, разложим их по типам и для каждого стартового запроса запишем, какую именно часть спроса он должен помочь обнаружить. Где мы сами составляем новую комбинацию слов, это будет прямо отмечено как наша диагностическая гипотеза.

### Что получим в конце

Получим проверенный список стартовых запросов для Wordstat и карту покрытия ассортимента. Это ещё не семантическое ядро: на следующем шаге Wordstat покажет, как люди на самом деле формулируют спрос.

## Authorization state

```text
STEP_02_PRE_STEP_REVIEW = COMPLETE
STEP_02_EXECUTION = NOT_STARTED
OWNER_AUTHORIZATION_REQUIRED = true
NEXT_STEP_ALLOWED = false until owner authorizes Step 02 execution
```
