# KW-001 / OKNO-MSK — Step 11 Search raw capture gap and recovery

Date: 2026-08-30
Job: `kw001-okno-msk-step11-page-ownership-20260830`

## Current durable state

The Search batch is complete and provider accounting is durable:

```text
BATCH_TOTAL = 68
BATCH_SUCCEEDED = 68
BATCH_FAILED_TERMINAL = 0
BATCH_OUTCOME_UNKNOWN = 0
BATCH_PENDING = 0
BATCH_ESTIMATED_COST_RUB = 33.184
CANARY_REQUESTS = 1
TOTAL_FRESH_SEARCH_REQUESTS = 69
TOTAL_FRESH_SEARCH_COST_RUB = 33.672
```

Existing chunk checkpoints preserve query text, request IDs, result counts, execution accounting and short analytical signals. They do **not** preserve every ranked result row (`rank/url/domain/title/snippet/modtime`) from every `nextN` response.

Therefore:

```text
SEARCH_EXECUTION_ACCOUNTING_DURABLE = true
FULL_RAW_PROVIDER_SERP_CORPUS_DURABLE = false
FULL_RANK_URL_DOMAIN_TITLE_RECOVERABLE_FROM_BATCH_LEDGER = true
FULL_SNIPPET_MODTIME_RECOVERABLE_FROM_PROJECTION = false
```

## Required recovery before ownership synthesis

Use the local Search Batch `projection` action. This reads already persisted batch results; it does not execute a new Yandex Search provider request.

The protocol permits:

- `offset`: 0+
- `limit`: 1..100
- `topN`: 1..100
- optional `targetDomains`

Projection returns each successful item with query metadata and provider-ranked `rank/url/domain/title` rows in observed rank order.

To reduce chat/output truncation risk, recover in four pages and persist each response immediately before running the next:

```text
SEARCH_BATCH_API_V1
{"action":"projection","jobId":"kw001-okno-msk-step11-page-ownership-20260830","offset":0,"limit":20,"topN":10,"targetDomains":["okno-msk.ru"]}
```

```text
SEARCH_BATCH_API_V1
{"action":"projection","jobId":"kw001-okno-msk-step11-page-ownership-20260830","offset":20,"limit":20,"topN":10,"targetDomains":["okno-msk.ru"]}
```

```text
SEARCH_BATCH_API_V1
{"action":"projection","jobId":"kw001-okno-msk-step11-page-ownership-20260830","offset":40,"limit":20,"topN":10,"targetDomains":["okno-msk.ru"]}
```

```text
SEARCH_BATCH_API_V1
{"action":"projection","jobId":"kw001-okno-msk-step11-page-ownership-20260830","offset":60,"limit":8,"topN":10,"targetDomains":["okno-msk.ru"]}
```

Expected recovered ranked rows:

```text
68 successful queries × TOP-10 = up to 680 ranked rows
```

## Persistence rule

For every returned projection page:

1. preserve the response immediately in a raw, unsorted Step-11 artifact;
2. preserve provider rank order exactly;
3. do not cluster, sort, filter or make ownership decisions before the raw artifact exists and is read back;
4. only after all four pages reconcile to `68/68` may derived Search evidence tables be built.

## Evidence boundary

`projection` is a recovery/readout of already executed batch results. It is not a substitute for the original full provider envelope because projection intentionally exposes only ranked `rank/url/domain/title` fields and omits `snippet/modtime`.

Any original `nextN` provider envelope still present in conversation/operator logs should be preserved separately as raw provider evidence when available.