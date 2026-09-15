# KW-002 Step06 — S06Q001 REACQUISITION R1 RESULT CLOSURE

Date: 2026-09-15
Status: **S06Q001 CURRENT EVIDENCE CLOSED / SUCCESS_WITH_RESULTS / FULL RAW+NORMALIZED EXPORT PERSISTED**

## 1. Evidence identity

```text
QUERY_ID = S06Q001
QUERY_TEXT = амулет
COVERAGE_DIRECTION = GENERIC_PRODUCT
SOURCE_FAMILY_ID = PSF001
ATTEMPT = CONTROLLED_REACQUISITION_R1
JOB_ID = kw002-s06q001-r1-20260915
OPERATION_ID = spr9hlddpfp9al2grrfl
CURRENT_OUTCOME = SUCCESS_WITH_RESULTS
```

The original failed lifecycle (`kw002-s06q001-20260914` / `spr2q2fbfldmt6poichd`) remains preserved as historical provenance and is not rewritten by this closure.

## 2. Exact durable export authority

Bridge-delivered source file:

`search-kw002-s06q001-r1-20260915-r5-0-0.json`

Persisted unchanged at the job root under the same filename.

Local exact-file checks before publication:

```text
UTF8_BYTES = 62141
SHA256 = a585a21ec19a952227ca7eb0b531bd566c0bba5cb54c5bc28158b687910fc375
JSON_PARSE = PASS
SCHEMA = YMB_SEARCH_ASYNC_EXPORT_PAGE_V1
REVISION = 5
TOTAL_ITEMS = 1
ALL_JOB_ITEMS_IN_THIS_FILE = true
HAS_MORE = false
```

The file preserves both:
- provider `raw_text` including the Operation response and Base64 Search XML;
- the complete normalized result object and all normalized Search rows.

## 3. Provider/runtime reconciliation

```text
ITEM_STATE = SUCCEEDED
REQUESTS_STARTED = 1
OPERATIONS_ACCEPTED = 1
POLLS_STARTED = 1
UNRESOLVED = 0
ALL_SUCCESSFUL = true
RESULT_COUNT = 20
NORMALIZED_DOCUMENT_COUNT = 20
RESULT_ROWS_IN_EXPORT_PAGE = 20
RAW_ITEM_COUNT = 1
NORMALIZED_ITEM_COUNT = 1
PARSE_ERROR = null
RESPONSE_FORMAT = FORMAT_XML
USABLE_FOR_URL_COMPARISON = true
MISSING_URL_RANKS = []
UNSAFE_URL_RANKS = []
```

Provider timestamps preserved in the export:

```text
OPERATION_CREATED_AT = 2026-09-15T02:20:34Z
OPERATION_MODIFIED_AT = 2026-09-15T02:20:35Z
BRIDGE_SUBMITTED_AT = 2026-09-15T02:20:31.690Z
RESULT_SAVED_AT = 2026-09-15T02:30:45.441Z
NORMALIZED_AT = 2026-09-15T02:30:45.482Z
```

Budget/runtime envelope:

```text
MAX_REQUESTS = 1
MAX_COST_MICRORUB = 30500
RESERVED_MICRORUB = 30500
REACQUISITION_PROVIDER_SUBMIT_CALLS = 1
REACQUISITION_PROVIDER_COLLECT_CALLS = 1
AUTOMATIC_RETRY = false
```

## 4. Row/accounting QA

Machine reconciliation over the exact exported JSON:

```text
EXPECTED_RANKS = 1..20
OBSERVED_RANKS = 1..20
MISSING_RANKS = 0
DUPLICATE_RANKS = 0
URL_ROWS = 20
UNIQUE_URLS = 20
UNIQUE_DOMAINS = 15
ROWS_WITH_MODTIME = 20
ROWS_WITH_NON_NULL_SNIPPET = 15
ROWS_WITH_NULL_SNIPPET = 5
```

Null snippet is allowed because the Step06 evidence contract requires snippet only when supplied by the provider. No returned row was dropped because a snippet was absent.

Domain multiplicity in this single SERP snapshot:

```text
market.yandex.ru = 5 rows
www.livemaster.ru = 2 rows
all other observed domains = 1 row each
```

This within-query multiplicity is recorded as observation only. It does not by itself assign a final cross-query recurrence tier.

## 5. Bounded result-type classification

The result-type label below describes the observed URL/page role in this SERP. It is not final competitor inclusion, final intent, clustering or page-architecture evidence.

| Rank | Domain | Result type | URL |
|---:|---|---|---|
| 1 | `happywitch.ru` | `SPECIALTY_SELLER_OR_BRAND` | https://happywitch.ru/catalog/products/amulety_i_talismany/ |
| 2 | `www.ozon.ru` | `MARKETPLACE` | https://www.ozon.ru/category/amulety-i-oberegi/ |
| 3 | `leonardo.ru` | `OTHER` | https://leonardo.ru/ishop/tree_9538925124/ |
| 4 | `www.livemaster.ru` | `MARKETPLACE` | https://www.livemaster.ru/itemlist/amuletioberegitalismani |
| 5 | `slavyanskieoberegi.ru` | `SPECIALTY_SELLER_OR_BRAND` | https://slavyanskieoberegi.ru/ |
| 6 | `www.wildberries.ru` | `MARKETPLACE` | https://www.wildberries.ru/catalog/tags/amulet-i-obereg |
| 7 | `ru.wikipedia.org` | `INFORMATIONAL_PUBLISHER` | https://ru.wikipedia.org/wiki/%D0%90%D0%BC%D1%83%D0%BB%D0%B5%D1%82 |
| 8 | `aliexpress.ru` | `MARKETPLACE` | https://aliexpress.ru/popular/%D0%B0%D0%BC%D1%83%D0%BB%D0%B5%D1%82%D1%8B-%D0%B8-%D1%82%D0%B0%D0%BB%D0%B8%D1%81%D0%BC%D0%B0%D0%BD%D1%8B |
| 9 | `www.giftman.ru` | `OTHER` | https://www.giftman.ru/blog/amulety-dlya-chego-nuzhny-i-kak-vybrat-svoy/ |
| 10 | `natilash-amulets.ru` | `SPECIALTY_SELLER_OR_BRAND` | https://natilash-amulets.ru/ |
| 11 | `market.yandex.ru` | `MARKETPLACE` | https://market.yandex.ru/category/amulety-i-oberegi |
| 12 | `znanierussia.ru` | `INFORMATIONAL_PUBLISHER` | https://znanierussia.ru/articles/%D0%90%D0%BC%D1%83%D0%BB%D0%B5%D1%82 |
| 13 | `market.yandex.ru` | `MARKETPLACE` | https://market.yandex.ru/category/oberegi-i-talismany |
| 14 | `www.joom.ru` | `MARKETPLACE` | https://www.joom.ru/ru/best/oberegi-i-amulety |
| 15 | `ru.wikiquote.org` | `INFORMATIONAL_PUBLISHER` | https://ru.wikiquote.org/wiki/%D0%90%D0%BC%D1%83%D0%BB%D0%B5%D1%82 |
| 16 | `www.livemaster.ru` | `INFORMATIONAL_PUBLISHER` | https://www.livemaster.ru/topic/89553-article-amulety-talismany-oberegi-v-chem-raznitsa |
| 17 | `market.yandex.ru` | `MARKETPLACE` | https://market.yandex.ru/category/oberegi |
| 18 | `market.yandex.ru` | `MARKETPLACE` | https://market.yandex.ru/category/amulety-yuvelirnyye |
| 19 | `market.yandex.ru` | `MARKETPLACE` | https://market.yandex.ru/search?text=%D0%B0%D0%BC%D1%83%D0%BB%D0%B5%D1%82%D1%8B%20%D0%B8%20%D1%82%D0%B0%D0%BB%D0%B8%D1%81%D0%BC%D0%B0%D0%BD%D1%8B%20%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D0%BD%D0%B5%D1%82%20%D0%BC%D0%B0%D0%B3%D0%B0%D0%B7%D0%B8%D0%BD |
| 20 | `tr-page.yandex.ru` | `OTHER` | https://tr-page.yandex.ru/translate?lang=en-ru&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FAmulet |

Type counts:

```text
MARKETPLACE = 10
INFORMATIONAL_PUBLISHER = 4
SPECIALTY_SELLER_OR_BRAND = 3
OTHER = 3
TOTAL = 20
```

`OTHER` is intentionally used for pages whose observed role does not fit the allowed Step06 type labels cleanly enough to force a narrower class.

## 6. Bounded analytical interpretation

The generic query `амулет` produced a mixed commercial + informational top-20 snapshot:
- product/category and marketplace pages occupy a large share of the observed ranks;
- specialist sellers/brands are also present;
- encyclopedic/explanatory pages remain materially represented;
- the same marketplace domain can occupy several distinct result slots.

This supports continuing competitor discovery across the remaining representative queries. It does **not** prove:
- a final competitor set;
- a final keyword intent;
- final clustering;
- query-to-page ownership;
- a site architecture decision;
- full SERP coverage for Step12.

## 7. Closure verdict and next gate

```text
S06Q001_CURRENT_PROVIDER_OUTCOME = SUCCESS_WITH_RESULTS
S06Q001_FULL_RESULT_PERSISTED = true
S06Q001_RAW_PRESERVED = true
S06Q001_NORMALIZED_ROWS_PRESERVED = 20
S06Q001_ROW_ACCOUNTING = PASS
S06Q001_URL_VALIDATION = PASS
S06Q001_REMOTE_READBACK = PENDING_AT_FILE_CREATION
S06Q002_RELEASED_BY_THIS_FILE = false
STEP07_STARTED = false
```

After remote readback of the exact export, this closure and the updated execution cursor, S06Q001 may be accepted as durably closed and a separate bounded release may authorize the next manifest row `S06Q002 / оберег`.
