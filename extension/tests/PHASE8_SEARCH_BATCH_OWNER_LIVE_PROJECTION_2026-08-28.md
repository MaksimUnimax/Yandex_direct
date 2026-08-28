# Phase 8 Search Batch — owner-live projection evidence — 2026-08-28

Frozen candidate source authority: `0377d6e1f176d4b7ddd8553c0099e02a4f1e8716`

Owner-live job: `p8-owner-live-2026-08-28`

After two successful ordinary Search `next` operations:

- job status: `COMPLETED`
- total: `2`
- succeeded: `2`
- requests_started: `2`
- estimated_cost_rub: `0.976`
- outcome_unknown: `0`
- automatic retries: `0`

Local `status` evidence:

- operation: `batch.status`
- request_executed: `false`
- requests_started remained `2`
- estimated_cost_rub remained `0.976`

Local `projection` command:

`SEARCH_BATCH_API_V1 {"action":"projection","jobId":"p8-owner-live-2026-08-28","offset":0,"limit":10,"topN":10,"targetDomains":["market.yandex.ru","ru.wikipedia.org"]}`

Observed projection:

- operation: `batch.projection`
- request_executed: `false`
- requests_started remained `2`
- estimated_cost_rub remained `0.976`
- total_successful: `2`
- `печать велеса`: `market.yandex.ru` best observed rank = `3`; `ru.wikipedia.org` absent in observed top 10
- `алатырь`: `ru.wikipedia.org` best observed rank = `1`; `market.yandex.ru` absent in observed top 10

Verdict:

`PHASE8_SEARCH_BATCH_OWNER_LIVE_PROJECTION_PASS`

This evidence proves that rank/domain projection is computed from persisted SERP results locally and does not cross the provider boundary.
