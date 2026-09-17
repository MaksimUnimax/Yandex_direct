# KW-002 Step06 semantic classification audit

## Scope and result

- Input file: KW002_STEP06_SERP_URL_EVIDENCE_440.csv
- Input SHA-256: b71c2158df9d01fb18bc30e738b1b60d22817f990f18b6bac631d81826e1546f
- Exact input data rows: 440
- Exact classified output data rows: 440
- Exact query count: 22
- Expected grid: 22 queries × 20 ranks = 440 rows
- SERP_FEATURE_COVERAGE = NOT_CAPTURED_BY_CURRENT_SOURCE
- NEW_PROVIDER_CALLS = 0
- STEP07_STARTED = FALSE
- FINAL_PAGE_DECISIONS = NONE

## Hard QA

| Invariant | Result | Detail |
|---|---:|---|
| classified rows = 440 exactly | PASS | input=440, output=440 |
| unique query IDs = 22 exactly | PASS | actual=22 |
| every query has exactly 20 rows | PASS | checked=22 |
| ranks are exactly integers 1..20 for every query | PASS | all queries checked |
| (query_id, rank) is unique | PASS | unique_pairs=440 |
| every original input row exists exactly once | PASS | logical source-column comparison |
| every original source field is logically preserved | PASS | all 11 source fields compared |
| no new URL was introduced | PASS | URL multiset comparison |
| no URL was removed | PASS | URL multiset comparison |
| all required classification columns exist | PASS | required=8 |
| no classification field is blank | PASS | UNKNOWN/UNCERTAIN used where needed |
| all enum values are valid | PASS | all 440 classifications checked |
| query profile rows = 22 exactly | PASS | actual=22 |
| all Top-10 row counts reconcile to 10 per query | PASS | relevance and page-type buckets checked |
| no provider call was made | PASS | local immutable-source processing only |
| no Step07 work was performed | PASS | scope remained Step06 classification |
| no final target-page decisions were made | PASS | no CREATE/KEEP/MERGE or final clustering fields |

OVERALL_QA = PASS

## Per-query rank integrity

| query_id | query | rows | ranks 1..20 exactly once | unique query/rank |
|---|---|---:|---:|---:|
| S06Q001 | амулет | 20 | PASS | PASS |
| S06Q002 | оберег | 20 | PASS | PASS |
| S06Q003 | талисман | 20 | PASS | PASS |
| S06Q004 | аум | 20 | PASS | PASS |
| S06Q005 | буддийский символ | 20 | PASS | PASS |
| S06Q006 | ваджра | 20 | PASS | PASS |
| S06Q007 | лотос | 20 | PASS | PASS |
| S06Q008 | мантра | 20 | PASS | PASS |
| S06Q009 | молот тора | 20 | PASS | PASS |
| S06Q010 | мусульманский амулет | 20 | PASS | PASS |
| S06Q011 | ом | 20 | PASS | PASS |
| S06Q012 | подкова | 20 | PASS | PASS |
| S06Q013 | руна | 20 | PASS | PASS |
| S06Q014 | руна альгиз | 20 | PASS | PASS |
| S06Q015 | руна отал | 20 | PASS | PASS |
| S06Q016 | руна феху | 20 | PASS | PASS |
| S06Q017 | славянский оберег | 20 | PASS | PASS |
| S06Q018 | славянский символ | 20 | PASS | PASS |
| S06Q019 | талисман удачи | 20 | PASS | PASS |
| S06Q020 | улитка | 20 | PASS | PASS |
| S06Q021 | фигурка будды | 20 | PASS | PASS |
| S06Q022 | христианский символ | 20 | PASS | PASS |

## Enum and completeness validation

- rank_bucket enum: PASS
- target_relevance enum: PASS
- page_type enum: PASS
- content_format enum: PASS
- market_surface enum: PASS
- entity_collision enum: PASS
- classification_confidence enum: PASS
- Blank required classification fields: 0

## Classification totals

### target_relevance

| Value | Rows |
|---|---:|
| TARGET | 343 |
| ADJACENT | 31 |
| NON_TARGET | 5 |
| COLLISION | 56 |
| UNCERTAIN | 5 |

### page_type

| Value | Rows |
|---|---:|
| CATEGORY | 19 |
| PRODUCT | 27 |
| MARKETPLACE_CATEGORY | 90 |
| MARKETPLACE_PRODUCT | 5 |
| ARTICLE | 164 |
| ENCYCLOPEDIA | 52 |
| DICTIONARY | 13 |
| VIDEO | 12 |
| SOCIAL | 16 |
| LANDING | 11 |
| HOMEPAGE | 13 |
| OTHER | 16 |
| UNKNOWN | 2 |

### classification_confidence

| Value | Rows |
|---|---:|
| HIGH | 406 |
| MEDIUM | 29 |
| LOW | 5 |

## LOW-confidence rows

| query_id | query | rank | target_relevance | page_type | title | classification_basis |
|---|---|---:|---|---|---|---|
| S06Q003 | талисман | 14 | UNCERTAIN | UNKNOWN | Ссылка на network.talisman-online.ru | The generic link title and empty snippet do not establish what the network.talisman-online.ru page contains. The URL/title/snippet do not establish a supported page type. |
| S06Q009 | молот тора | 6 | UNCERTAIN | MARKETPLACE_CATEGORY | молот тора - Авито \| Объявления во всех регионах: купить вещь... | The Avito search URL matches the query, but the title and empty snippet do not show whether listings are amulets, replicas, or toys. avito.ru and the listing/category URL identify a marketplace category or search-results page. |
| S06Q012 | подкова | 4 | UNCERTAIN | MARKETPLACE_CATEGORY | Подкова настоящая купить на OZON по низкой цене | The Ozon category is “real horseshoe”; the title/snippet do not establish whether the offer is equestrian equipment or a luck souvenir. ozon.ru and the listing/category URL identify a marketplace category or search-results page. |
| S06Q012 | подкова | 5 | UNCERTAIN | MARKETPLACE_CATEGORY | Подкова настоящая - купить в интернет-магазине уникальные... | The Livemaster tag is “real horseshoe”, but the empty snippet does not establish the dominant intended use. livemaster.ru and the listing/category URL identify a marketplace category or search-results page. |
| S06Q013 | руна | 17 | UNCERTAIN | UNKNOWN | Ссылка на my.runa.ru | The generic link title and empty snippet do not establish the content of my.runa.ru. The URL/title/snippet do not establish a supported page type. |

## Collision-heavy queries

These are the queries with a material concentration of clearly different entities/meanings in this 20-result snapshot. This label is an audit summary, not a universal intent threshold.

| query_id | query | Top-10 collisions | all-20 collisions | snapshot finding |
|---|---|---:|---:|---|
| S06Q003 | талисман | 1 | 7 | Dictionary and encyclopedia results dominate the Top-10; one language-school collision remains visible. |
| S06Q006 | ваджра | 9 | 16 | The Top-10 is dominated by Andrey Vajra media/entity results rather than the ritual symbol. |
| S06Q007 | лотос | 3 | 6 | The Top-10 is split between the “ЛОТОС” clinic and botanical/travel meanings; the target symbolic meaning is not represented directly. |
| S06Q020 | улитка | 10 | 20 | All Top-10 results interpret the query biologically as a snail/gastropod rather than as a symbolic motif. |

## Top-10 intent still mixed or uncertain

| query_id | query | intent | confidence | basis |
|---|---|---|---|---|
| S06Q009 | молот тора | HYBRID | MEDIUM | Top-10 relevance: TARGET=7, ADJACENT=1, NON_TARGET=0, COLLISION=1, UNCERTAIN=1. Page types: MARKETPLACE_CATEGORY=6, ARTICLE=3, ENCYCLOPEDIA=1. The Top-10 mixes commerce and reference content, while some commercial results drift into entertainment replicas. |
| S06Q012 | подкова | UNCERTAIN | LOW | Top-10 relevance: TARGET=3, ADJACENT=3, NON_TARGET=1, COLLISION=1, UNCERTAIN=2. Page types: CATEGORY=5, MARKETPLACE_CATEGORY=3, ARTICLE=1, HOMEPAGE=1. The Top-10 mixes luck souvenirs, functional equestrian horseshoes, a business-name collision, and two ambiguous “real horseshoe” listings. |

## Queries with LOW/UNCERTAIN row-level material

- S06Q003 / талисман: LOW=1, UNCERTAIN=1
- S06Q009 / молот тора: LOW=1, UNCERTAIN=1
- S06Q012 / подкова: LOW=2, UNCERTAIN=2
- S06Q013 / руна: LOW=1, UNCERTAIN=1

## Methodological findings and limitations

- The source begins with a UTF-8 BOM attached to the first header. It was preserved; validation normalizes it only when locating query_id internally.
- 86 of 440 rows have an empty snippet. Those rows were classified from the remaining supplied URL/domain/title evidence, with LOW or UNKNOWN/UNCERTAIN used where that evidence was insufficient.
- 40 of 440 rows have an empty modtime. No acquisition-time value was invented.
- The existing source serp_class field was preserved as evidence but was not treated as row-level ground truth.
- top10_other_or_unknown_pages includes LANDING, HOMEPAGE, OTHER, and UNKNOWN so the page-type buckets reconcile to exactly 10.
- Dominant page type is the largest Top-10 page-type count. A count tie is resolved by the tied type appearing at the best rank, then by average rank. The count and share remain explicit.
- SERP_FEATURE_COVERAGE = NOT_CAPTURED_BY_CURRENT_SOURCE. Image packs, PAA, shopping modules, carousels, map packs, rich snippets, and other features were not inferred.
- This is a bounded acquisition snapshot. It demonstrates observed composition only and does not prove long-term SERP stability or permanent domain/intent behavior.
- No final page, CREATE/KEEP/MERGE decision, final SEO cluster, or Step07 artifact was created.
