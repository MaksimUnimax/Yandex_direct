# KW-001 / OKNO_MSK — Step 5A competitor-page inspection report

Date: 2026-09-08  
Status: **ANALYST QA PASS / OWNER REVIEW PENDING / METHOD NOT PROMOTED**

## 1. Completed scope

This execution completed Step 5A.2 and Step 5A.3 for the frozen competitor universe. It opened only the 44 exact public competitor URLs preserved by the prior Step 9 ranking evidence, recorded one page-evidence row per target, derived concise candidate directions from observed page elements, reconciled every candidate against the completed OKNO_MSK semantic authority and produced an exact Wordstat requirement package for Main ChatGPT.

No Yandex Search, Wordstat, Alice, GenSearch, Webmaster, Metrika or Direct provider call was made. No reverse-domain provider, extra competitor URL or whole-site crawl was used.

## 2. Page accounting

```text
SELECTED_DOMAINS = 9 / 9
AUTHORIZED_URL_TARGETS = 44 / 44
ACCESSIBLE_AT_REQUESTED_URL = 43
REDIRECTED_ACCESSIBLE = 1
INACCESSIBLE = 0
OUT_OF_SCOPE_URLS_OPENED_AS_EVIDENCE_TARGETS = 0
```

The single redirect was `I030`: the requested URL without a trailing slash resolved to the same page with a trailing slash. Requested and final URLs are both preserved.

### Page types

| Page type | Count |
|---|---:|
| `ARTICLE_GUIDE` | 3 |
| `COMMERCIAL_CATEGORY` | 5 |
| `COMMERCIAL_LANDING` | 2 |
| `COMMERCIAL_PRODUCT` | 6 |
| `COMMERCIAL_SERVICE` | 13 |
| `COMPARISON_SELECTION` | 4 |
| `HOME_OR_HUB` | 4 |
| `MIXED_COMMERCIAL_INFORMATIONAL` | 2 |
| `PORTFOLIO_GALLERY` | 1 |
| `PRICE_FINANCE` | 4 |

## 3. Candidate reconciliation

```text
RAW_PAGE_DERIVED_CANDIDATE_OCCURRENCES = 92
DEDUPLICATED_CANDIDATE_DIRECTIONS = 43
DUPLICATE_PAGE_SUPPORT_ROWS = 49
ALREADY_COVERED_EXACT_OR_CLOSE = 22
POTENTIALLY_NEW_WORDSTAT_SEED = 14
OFF_SCOPE_BUSINESS = 3
INSUFFICIENT_PAGE_EVIDENCE = 0
HOLD_REVIEW = 4
```

A repeated topic from another page is retained in the candidate register as lineage but does not create another Wordstat seed. Every one of the 44 pages contributes to at least one candidate lineage.

## 4. Exact Wordstat requirement package

These are acquisition probes, not accepted keywords and not ranking claims.

| Priority | Seed | Axis | Competitors | Pages | Source IDs |
|---:|---|---|---:|---:|---|
| 1 | **остекление балкона П-46** | типовая серия дома | 1 | 1 | I014 |
| 2 | **остекление балкона с выносом по полу** | конструкция выносного остекления | 1 | 1 | I011 |
| 3 | **гидроизоляция открытого балкона** | ремонт открытого балкона | 2 | 3 | I023, I040, I044 |
| 4 | **солнцезащитный стеклопакет** | функция стеклопакета | 2 | 5 | I001, I036, I037, I038, I039 |
| 5 | **многофункциональный стеклопакет** | функция стеклопакета | 2 | 4 | I001, I036, I037, I038 |
| 6 | **ударопрочный стеклопакет** | безопасность стеклопакета | 1 | 3 | I036, I037, I038 |
| 7 | **Provedal C640 или P400** | сравнение алюминиевых систем | 1 | 1 | I027 |
| 8 | **окна для старого фонда** | тип жилого объекта | 1 | 1 | I020 |
| 9 | **окна для квартиры под аренду** | сценарий использования квартиры | 1 | 1 | I020 |
| 10 | **балкон под офис** | функциональный сценарий балкона | 1 | 1 | I020 |
| 11 | **балкон-кладовая** | функциональный сценарий балкона | 1 | 1 | I020 |
| 12 | **фальш-крыша на балкон** | конструкция крыши балкона | 1 | 1 | I042 |
| 13 | **шумоизоляция крыши балкона** | функция крыши балкона | 1 | 1 | I042 |
| 14 | **армирование оконного профиля** | параметр выбора ПВХ-профиля | 1 | 1 | I030 |

All package rows use region `213`, device scope `ALL` and authorization state `RETURN_TO_MAIN_CHATGPT_FOR_BRIDGE_EXECUTION`.

## 5. Rejected and held directions

Off-scope/unverified competitor assortment:

- **деревянные окна из сосны, лиственницы или дуба** — Продажа деревянных окон не подтверждена как бизнес-направление клиента; детализация по породам не оправдывает Wordstat до подтверждения предложения.
- **алюминиевые окна Schuco** — Наблюдение подтверждает ассортимент конкурента, но не наличие Schuco у клиента; конкурентный бренд нельзя передавать в пакет Wordstat как клиентское направление.
- **алюминиевые профили Alutech, Vidnal, Alumil или Krauss** — Перечень профильных брендов принадлежит конкуренту и не является доказательством ассортимента OKNO_MSK.

Held before Wordstat:

- **окосячка для пластиковых окон в деревянном доме** — Страница конкурента наблюдаемо раскрывает окосячку, но сохранённая бизнес-правда клиента не подтверждает эту отдельную работу; сначала требуется подтверждение предложения.
- **Provedal или Slidors** — Provedal относится к существующей семантике, но наличие Slidors в предложении клиента не подтверждено; сравнение нельзя отправлять в Wordstat до бизнес-проверки.
- **укрепление балконной плиты** — Конструктивное усиление плиты требует отдельной бизнес- и технической проверки; конкурентные проекты не доказывают услугу клиента.
- **обогрев крыши балкона кабелем** — Кабельный обогрев наблюдался только у конкурента и не подтверждён как доступная услуга клиента.

## 6. Claim boundary

```text
COMPETITOR PAGE TOPIC
!= ACCEPTED KEYWORD
!= EXACT QUERY RANKING CLAIM
!= FULL COMPETITOR KEYWORD UNIVERSE
```

The persisted page register describes only publicly observed page elements. Competitor claims, brands, prices, product properties and service lists were not transferred into OKNO_MSK business truth.

## 7. Protection and provider accounting

```text
NEW_YANDEX_SEARCH_CALLS = 0
NEW_WORDSTAT_CALLS = 0
NEW_ALICE_CALLS = 0
NEW_GENSEARCH_CALLS = 0
NEW_WEBMASTER_CALLS = 0
NEW_METRIKA_CALLS = 0
NEW_DIRECT_CALLS = 0
NEW_PAID_PROVIDER_COST_RUB = 0
CLIENT_RELEASE_MODIFIED = false
DOCUMENTS_01_02_03_MODIFIED = false
SEMANTIC_CORE_04_MODIFIED = false
LEVEL1_METHOD_PROMOTED = false
PROJECT_TEST_VALIDATED = false
OWNER_REVIEW = pending
```

## 8. Next action

Return the 14-row package to Main ChatGPT for owner/Bridge-controlled Wordstat execution. Do not start any Wordstat or Search acquisition from Work.
