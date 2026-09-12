# KW-002 Blood & Sand — Step06 pre-step external research and source trace

Date: 2026-09-12
Status: **PASS FOR PREPARATION / NO SEARCH PROVIDER CALL / NO STEP06 EXECUTION RELEASE**
Base remote HEAD checked before preparation: `89ba3907196ea4f4f5b19388c0146f0b06d7db48`
Drift from accepted Step05 close: `NO_DRIFT`.

## Step06 purpose boundary

Current Level2 Step06 purpose:

```text
Find pages/domains that actually compete in current ordinary Yandex organic search results
for representative retained demand directions.

BUSINESS RIVAL != SEARCH COMPETITOR
```

This step does not perform competitor semantic expansion (Step07), competitor-derived Wordstat (Step08), final intent classification, SERP clustering, query-to-page ownership, site architecture, or AI/GenSearch analysis.

## Current business/search scope rechecked

Client authority remains:

```text
brand = Blood & Sand / Кровь и Песок
business = product brand / seller
client-stated products = амулеты, обереги, талисманы; including automobile-use goods
market = Russia
search engine = Yandex
new owned site planned
client-supplied SEO competitor list = NONE
```

Source: `CLIENT_SUPPLIED_BRIEF.md`.

## Official Yandex Search API sources rechecked on 2026-09-12

Official sources:

- https://aistudio.yandex.ru/ru/docs/search-api/api-ref/WebSearch/search
- https://aistudio.yandex.ru/ru/docs/search-api/concepts/web-search
- https://aistudio.yandex.ru/ru/docs/search-api/operations/web-search-sync
- https://aistudio.yandex.ru/ru/docs/search-api/concepts/limits
- https://aistudio.yandex.ru/ru/docs/search-api/pricing
- https://aistudio.yandex.ru/ru/docs/search-api/concepts/
- https://yandex.com/support/search/en/query-language/search-context
- https://yandex.com/support/search/en/query-language/qlanguage

Current provider facts used by this preparation:

```text
ORDINARY_WEB_SEARCH_ENDPOINT = POST /v2/web/search
SEARCH_TYPE = SEARCH_TYPE_RU
REGION_225 = Russia
SYNC_RESULT = Base64 rawData containing XML or HTML
XML = search results proper without browser-SERP extras
XML groupsOnPage = 1..100
TOTAL_RESULTS_TECHNICAL_LIMIT = up to 250 per query
QUERY_MAX_LENGTH = 400 characters
QUERY_MAX_WORDS = 40
SYNC_QUOTA = 10 requests/second; 10,000 requests/hour
DAY_SYNC_PRICE = 488 RUB / 1000 = 0.488 RUB/request
NIGHT_SYNC_PRICE = 366 RUB / 1000 = 0.366 RUB/request
NIGHT_WINDOW = 00:00:00–07:59:59 UTC+3
```

The provider documentation explicitly states that Search API proxies Yandex search results and API results may differ from what the same query shows in a browser. Step06 evidence therefore means **current Search API organic evidence under the recorded request parameters**, not a promise of pixel-identical browser SERP composition.

## External SEO-method corroboration

Sources:

- https://ahrefs.com/academy/how-to-use-ahrefs/site-explorer/organic-competitors
- https://ahrefs.com/blog/seo-competitor-analysis/
- https://ahrefs.com/blog/keyword-competitive-analysis/
- https://searchengineland.com/tools/seo-competitor-analysis-tool
- https://searchengineland.com/guide/gap-analysis

Method claims supported by these sources and adopted only where compatible with KW002 rules:

1. Organic/Search competitors are domains competing for the same target search queries; they need not equal direct business competitors.
2. For a new site with no ranking history, competitor discovery can start from target/valuable query sets rather than domain-overlap against the new site itself.
3. Recurrence/overlap across multiple target queries is stronger competitor evidence than one isolated appearance.
4. Marketplaces, publishers, directories or other non-direct businesses can still be SERP competitors, but must be typed separately rather than mislabeled as direct commercial rivals.

No third-party traffic estimate, keyword-volume estimate or proprietary competitor score is imported into KW002 by this source trace.

## Current Bridge repository recheck

Files checked on the current branch:

- `extension/src/shared/product.js`
- `extension/src/shared/search_protocol.js`
- `extension/src/shared/search_batch_protocol.js`
- `extension/src/shared/search_batch_runtime.js`
- `extension/src/shared/search_batch_projection.js`
- `extension/src/shared/search_xml.js`
- `extension/src/search_batch_worker_transport.js`
- `extension/src/service_worker.js`

Repository Search contract observed:

```text
SEARCH_API_V1 ordinary method = search
endpoint = /v2/web/search
responseFormat = FORMAT_XML
region default for SEARCH_TYPE_RU = 225
page default = 0
groupsOnPage = 1..100; repo default single search 10
batch start queries <= 500
batch maxRequests <= 500
batch nextN <= 100
batch persisted to chrome.storage.local key ymb_search_batch_jobs_v1
batch projection exposes rank/url/domain/title and top-domain overlap
OUTCOME_UNKNOWN -> no automatic blind retry
```

## Blocking Bridge authority/persistence findings

### 1. Runtime-source version drift

The successful owner-provided Wordstat execution immediately before Step06 preparation reported:

```text
bridge version = 0.1.4
```

But current branch `extension/src/shared/product.js` reports:

```text
VERSION = 0.1.2
```

Therefore repository source cannot be assumed to be byte-equivalent to the actually installed runtime. A runtime/schema/source reconciliation is mandatory before Step06 provider release.

### 2. Current repository Search path is not lossless RAW feed-forward

Current `executeSearchCommand()` reads the provider response, parses the JSON containing Base64 `rawData`, then calls `SearchProtocol.normalizeProviderResult(parsed)` and puts only the normalized result into the result envelope.

Current `search_xml.js` decodes `rawData` and emits normalized rows:

```text
rank
url
domain
title
snippet
modtime
```

Current batch runtime persists the result envelope as `result_payload`, so under the repository implementation the original provider `rawData` / decoded XML is not retained in the durable batch result.

This violates the KW002 Level1 F03 feed-forward sequence if no other runtime-specific lossless raw-export path exists:

```text
receive complete result
-> persist complete required body
-> persist request/provenance identity
-> remote readback
-> reconcile
-> only then next provider action
```

This is an execution-release blocker, not a reason to discard the Step06 methodology/query plan.

## Preparation verdict

```text
CURRENT_YANDEX_PROVIDER_DOCS = PASS
CURRENT_SEARCH_PRICE = PASS
CURRENT_LIMITS_QUOTAS = PASS
STEP06_METHOD_SOURCE_DISCLOSURE = PASS
STEP06_QUERY_PLAN_MAY_BE_PREPARED = YES
SEARCH_PROVIDER_EXECUTION_RELEASE = HOLD
HOLD_1 = INSTALLED_RUNTIME_0.1.4_NOT_RECONCILED_WITH_REPO_SOURCE_0.1.2
HOLD_2 = LOSSLESS_PROVIDER_RAW_PERSISTENCE_NOT_PROVEN_FOR_SEARCH_RUNTIME
SEARCH_CALLS_EXECUTED = 0
GENSEARCH_CALLS_EXECUTED = 0
WORDSTAT_CALLS_EXECUTED = 0
STEP06_STARTED = false
```

Before release, prove the current installed Search runtime contract and a lossless RAW export/persistence/readback path. Do not solve this by accepting only normalized projection rows as if they were complete provider RAW evidence.
