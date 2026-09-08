# KW-001 / OKNO_MSK — Step 5A first execution report

Date: 2026-09-08  
Status: **ANALYST QA PASS / OWNER REVIEW PENDING / METHOD NOT PROMOTED**

## 1. What this execution completed

This isolated execution processed the complete preserved ordinary-Yandex dataset: 75 queries and 750 ranked TOP-10 rows for region 213. It reconstructed one deterministic ledger, measured recurring domains, separated recurrence from business comparability, traced every query as far as completed downstream evidence allows and selected a bounded set of real search competitors for the next Step 5A subphase.

No new Yandex Search, Wordstat, Alice, GenSearch, Webmaster, Metrika or Direct call was made. No public competitor page was opened. Client deliverables and historical Step 0–20 authorities were not modified.

## 2. Source accounting

```text
SOURCE_QUERIES = 75
SOURCE_RANKED_ROWS = 750
ACCOUNTED_QUERIES = 75
ACCOUNTED_RANKED_ROWS = 750
SILENT_ROW_DROPS = 0
DUPLICATE_ROW_INFLATION = 0
NORMALIZED_DOMAINS = 237
REGION = 213
RANKS_PER_QUERY = 1..10
```

The canary row source and four R2 projection parts were combined only through their common supported fields. Unavailable R2 snippets, request IDs, HTTP fields and raw XML were not invented.

## 3. Domain recurrence and classification

All 237 normalized domains were assigned one routing class. Where the preserved hostname/title/URL fields were insufficient, the class remains `UNKNOWN` (77 domains) rather than being guessed.

| Class | Domains |
|---|---:|
| `AGGREGATOR_DIRECTORY` | 4 |
| `DIRECT_BUSINESS_COMPETITOR` | 78 |
| `INFORMATIONAL_PUBLISHER` | 15 |
| `MANUFACTURER_OR_BRAND_SOURCE` | 9 |
| `MARKETPLACE` | 9 |
| `ORGANIC_COMPETITOR_OTHER_MODEL` | 39 |
| `OTHER_REVIEW` | 2 |
| `UNKNOWN` | 77 |
| `YANDEX_PLATFORM` | 4 |

Top recurring direct-business competitors from the preserved ledger:

| Domain | TOP-10 appearances | Distinct queries | TOP-3 | Best rank |
|---|---:|---:|---:|---:|
| mosokna.ru | 80 | 22 | 22 | 2 |
| i-okna.ru | 19 | 14 | 7 | 1 |
| msk.okna-servise.com | 19 | 13 | 10 | 1 |
| okna-moskva.ru | 16 | 13 | 6 | 1 |
| oknafactoria.ru | 13 | 10 | 3 | 1 |
| okna-germany.ru | 9 | 9 | 1 | 1 |
| fabrikaokon.ru | 8 | 8 | 3 | 2 |
| svetokna.ru | 7 | 7 | 3 | 1 |
| oknastreet.ru | 6 | 6 | 1 | 3 |
| ramokna.ru | 6 | 6 | 3 | 1 |
| al-solution.ru | 6 | 5 | 1 | 3 |
| aluminarium.ru | 6 | 5 | 4 | 1 |
| okno.ru | 6 | 5 | 2 | 2 |
| elit-balkon.ru | 6 | 4 | 3 | 1 |
| mosbalkon.ru | 6 | 4 | 0 | 5 |

Recurrence was not treated as business equivalence. High-frequency non-direct surfaces such as the REHAU online shop, Avito, Ozon and Yandex services remain manufacturer, marketplace or platform observations.

## 4. What ordinary Yandex Search changed or confirmed

Every Step 9 query has one impact row with an exact-query claim boundary:

| Impact class | Queries | Meaning in this execution |
|---|---:|---|
| `CHANGED_DECISION` | 26 | Direct evidence resolved a review-state phrase into a preserved task/cluster. |
| `DE_RISKED_DECISION` | 20 | Evidence supported a boundary, hold, outside-scope or no-standalone-page route. |
| `CONFIRMED_EXISTING_DECISION` | 19 | Evidence confirmed a task/cluster already carried as a core candidate. |
| `NO_MATERIAL_DOWNSTREAM_EFFECT` | 0 | Observation existed without a material traceable downstream effect. |
| `UNRESOLVED_TRACE` | 10 | No exact completed downstream join or the preserved row remained unresolved. |

There are 66 exact Step 10 / Step 11 phrase / final-master joins. Ten queries remain unresolved rather than receiving family-level causal attribution:

- Q39 / SP09-039: цены материала на пластиковые окна
- Q57 / SP09-057: rehau thermo окна
- Q60 / SP09-060: какой профиль rehau выбрать
- Q62 / SP09-062: остекление балкона п 46
- Q65 / SP09-065: остекление балконов москва
- Q66 / SP09-066: остекление беседки
- Q68 / SP09-068: остекление террасы
- Q70 / SP09-070: пластиковые окна митино
- Q73 / SP09-073: теплое остекление балкона
- Q74 / SP09-074: установка пластиковых окон москва

These impact classes describe the role explicitly traceable in preserved evidence. They do not claim that Search alone caused every later structural decision.

## 5. Bounded competitor selection for the next Step 5A subphase

Nine competitors were selected from an eleven-domain shortlist. Selection combines recurrence, direct/partial business comparability and task diversity; it is not a market-share ranking.

| # | Domain | Queries | TOP-3 | Best | Why retained |
|---:|---|---:|---:|---:|---|
| 1 | mosokna.ru | 22 | 22 | 2 | Highest recurrence in the preserved set and broad coverage of PVC/Rehau, price, finance, product and balcony tasks through multiple ranking URLs. |
| 2 | i-okna.ru | 14 | 7 | 1 | Frequent Rehau-focused transactional visibility plus preserved repair, price and finance pages provides a concentrated brand-family comparison source. |
| 3 | msk.okna-servise.com | 13 | 10 | 1 | Strong TOP-3 recurrence across balcony subtypes, house-series, installation, price and cold/warm glazing tasks. |
| 4 | okna-moskva.ru | 13 | 6 | 1 | Broad product visibility combined with Rehau, instalment, balcony-roof and veranda pages adds cross-task comparison value. |
| 5 | oknafactoria.ru | 10 | 3 | 1 | Preserved results bridge service pages and editorial pages across open balcony, porch, repair, Provedal, selection and cold glazing. |
| 6 | okna-germany.ru | 9 | 1 | 1 | A content-led set of preserved Rehau comparison/selection/repair and Provedal URLs is useful for testing missed informational directions. |
| 7 | fabrikaokon.ru | 8 | 3 | 2 | Preserved rankings cover timber-aluminium windows, wooden balcony glazing, warm/cold subtypes and installation information/service. |
| 8 | aluminarium.ru | 5 | 4 | 1 | Repeated high positions in aluminium windows and outdoor-structure glazing provide a specialist contrast to broad PVC/window competitors. |
| 9 | elit-balkon.ru | 4 | 3 | 1 | Focused preserved visibility for open-balcony finishing, demolition and roof glazing supplies a specialist balcony-service comparison. |

Not selected in the bounded set:

- **al-solution.ru** — Not selected in the bounded set because its preserved aluminium/terrace/Provedal coverage is substantially represented by selected specialist and content candidates.
- **svetokna.ru** — Not selected in the bounded set because its mixed wood/aluminium/veranda/balcony coverage overlaps selected Fabrika Okon and Aluminarium evidence.

### Exact preserved ranking URLs to inspect next

These URLs are evidence-bearing inspection targets only. Their page topics were not inspected in this execution and no candidate seed was inferred from the URL alone.

- **mosokna.ru**
  - Q17/R2: https://www.mosokna.ru/plastikovye-okna
  - Q30/R2: https://www.mosokna.ru/plastikovye-okna/vidy-okon/dvuhstvorchatoe-okno
  - Q44/R2: https://www.mosokna.ru/ceny/rassrochka
  - Q48/R2: https://www.mosokna.ru/
  - Q61/R3: https://www.mosokna.ru/plastikovye-okna-rehau
- **i-okna.ru**
  - Q14/R1: https://i-okna.ru/
  - Q33/R2: https://i-okna.ru/uslugi/remont_okon
  - Q48/R6: https://i-okna.ru/price
  - Q45/R7: https://i-okna.ru/uslugi/kredit
  - Q14/R4: https://i-okna.ru/uslugi
- **msk.okna-servise.com**
  - Q19/R1: https://www.msk.okna-servise.com/osteklenie-balkonov/s-vynosom/
  - Q36/R1: https://www.msk.okna-servise.com/plastikovye-okna/okna-v-derevyannom-dome/
  - Q39/R1: https://www.msk.okna-servise.com/
  - Q62/R1: https://www.msk.okna-servise.com/osteklenie-balkonov/dom/p-46/
  - Q74/R1: https://www.msk.okna-servise.com/pod-klyuch/
- **okna-moskva.ru**
  - Q48/R1: https://www.okna-moskva.ru/plastikovye-okna-rehau/blitz-60/
  - Q64/R1: https://www.okna-moskva.ru/osteklenie-balkonov/osteklenie-s-kryshey/
  - Q71/R1: https://www.okna-moskva.ru/series/
  - Q67/R3: https://www.okna-moskva.ru/okna-dlja-dachi/osteklenie-verandy/
  - Q72/R5: https://www.okna-moskva.ru/
- **oknafactoria.ru**
  - Q11/R1: https://oknafactoria.ru/krylco/
  - Q15/R1: https://oknafactoria.ru/articles/regulirovka-plastikovyh-okon-rehau-prostye-instrukczii-na-vse-sluchai/
  - Q3/R3: https://oknafactoria.ru/articles/kak-preobrazit-otkrytyj-balkon-bez-ostekleniya-praktichnyj-putevoditel-po-remontu-i-komfortnoj-zhizni-na-svezhem-vozduhe/
  - Q42/R5: https://oknafactoria.ru/okna-provedal/
  - Q60/R5: https://oknafactoria.ru/articles/obzor-vseh-vidov-profilya-rehau-sravnivaem-harakteristiki-i-vybiraem-luchshij/
- **okna-germany.ru**
  - Q60/R1: https://okna-germany.ru/blog/sravnenie-profilej-dlya-okon-rehau
  - Q53/R4: https://okna-germany.ru/blog/vidy-preimushchestva-sistemy-provedal
  - Q57/R5: https://okna-germany.ru/okna-rehau/rehau-thermo
  - Q15/R7: https://okna-germany.ru/blog/regulirovka-plastikovyih-okon-rehau
  - Q59/R7: https://okna-germany.ru/blog/kakie-vybrat-plastikovye-okna-dlya-kvartiry
- **fabrikaokon.ru**
  - Q6/R2: https://www.fabrikaokon.ru/derevo-alyuminievyie-okna.html
  - Q73/R2: https://www.fabrikaokon.ru/tyoploe-osteklenie.html
  - Q21/R3: https://www.fabrikaokon.ru/balkon-derevyannye-okna.html
  - Q22/R5: https://www.fabrikaokon.ru/balkon.html
  - Q75/R6: https://www.fabrikaokon.ru/xolodnoe-osteklenie.html
- **aluminarium.ru**
  - Q58/R1: https://aluminarium.ru/alyuminievye-okna/schuco/
  - Q67/R1: https://aluminarium.ru/osteklenie-verandy-i-terrasy/
  - Q66/R2: https://aluminarium.ru/alyuminievoe-osteklenie-besedki/
  - Q58/R5: https://aluminarium.ru/alyuminievye-okna/
- **elit-balkon.ru**
  - Q3/R1: https://www.elit-balkon.ru/remont-balkonov/balkon-bez-ostekleniya
  - Q20/R1: https://www.elit-balkon.ru/tseny/osteklenie-balkonov-s-kryshej
  - Q64/R3: https://www.elit-balkon.ru/krisha-na-balkon
  - Q5/R4: https://www.elit-balkon.ru/remont-balkonov/demontazh
  - Q3/R6: https://www.elit-balkon.ru/galereya/balkon-bez-ostekleniya

## 6. Method-validation result

```text
REAL_SEARCH_COMPETITOR_DISCOVERY = PASS
PRESERVED_QUERY_TO_COMPETITOR_VISIBILITY = PASS
RECURRENCE_VS_BUSINESS_COMPARABILITY_BOUNDARY = PASS
QUERY_IMPACT_TRACE = PASS_WITH_10_EXPLICIT_UNRESOLVED_ROWS
COMPETITOR_PAGE_TO_SEED_LINEAGE = NOT_EXECUTED
WORDSTAT_COMPETITOR_EXPANSION = NOT_EXECUTED
NEW_CANDIDATE_SEARCH_RECHECK = NOT_EXECUTED
WEBSITE_TEXT_AS_RANKING_OVERCLAIM = 0
FULL_COMPETITOR_KEYWORD_UNIVERSE_OVERCLAIM = 0
PROJECT_TEST_VALIDATED = false
OWNER_REVIEW = PENDING
```

This execution validates the preserved-SERP discovery, classification, impact-trace and bounded-selection operations. It does not satisfy the full permanent promotion gate because competitor-page inspection, page→seed lineage, Wordstat expansion, candidate filtering, Search recheck and merge reconciliation were intentionally not executed.

## 7. Exact next evidence boundary

Next authorized work must first inspect only the exact selected ranking URLs recorded in `STEP_05A_COMPETITOR_CANDIDATE_SELECTION.tsv` and persist page-level provenance. Only then can exact candidate seeds be named.

```text
EXACT_NEW_WORDSTAT_SEEDS_REQUIRED_NOW = NONE__NOT_YET_EVIDENCED
EXACT_NEW_SEARCH_QUERIES_REQUIRED_NOW = NONE__PENDING_PAGE_INSPECTION_AND_WORDSTAT_RESULTS
NEXT_EVIDENCE_PRODUCING_STEP = OWNER_AUTHORIZED_SELECTED_COMPETITOR_PAGE_INSPECTION
```

The absence of exact seeds at this boundary is intentional: inventing them from domain names or URL slugs would violate `COMPETITOR PAGE TOPIC != EXACT QUERY RANKING` and the lineage requirement.

## 8. Durable artifact set

- `CHECKPOINT_00_BASELINE_AND_REUSE_INVENTORY.md`
- `STEP_05A_SERP_COMBINED_750.tsv`
- `STEP_05A_DOMAIN_FREQUENCY.tsv`
- `STEP_05A_QUERY_IMPACT_TRACE.tsv`
- `STEP_05A_COMPETITOR_CANDIDATE_SELECTION.tsv`
- `STEP_05A_FIRST_EXECUTION_QA.json`
- `STEP_05A_FIRST_EXECUTION_REPORT.md`
- `EXECUTION_LOG.md`
- `build_step05a_first_execution.py`
- `validate_step05a_first_execution.py`

Optional page-evidence and derived-seed files were not created because no competitor page was inspected.
