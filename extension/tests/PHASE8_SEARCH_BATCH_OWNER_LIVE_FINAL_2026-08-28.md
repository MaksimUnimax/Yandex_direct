# Phase 8 Search Batch owner-live final — 2026-08-28

Status: `PHASE8_SEARCH_BATCH_OWNER_LIVE_PASS`

Frozen install candidate authority:
- source SHA: `0377d6e1f176d4b7ddd8553c0099e02a4f1e8716`
- extension/src tree: `bdad1e87a2537d8646e480ca23f8068c3dced17e`
- candidate ZIP SHA-256: `8f6ba92dbe1f592a62c66cd250ed942e261f56deffbe87117371bd9c481e6332`
- freeze workflow run: `33143237276` = SUCCESS

Owner-live job:
- `job_id = p8-owner-live-2026-08-28`
- queries: `печать велеса`, `алатырь`
- region: `225`
- Search type: `SEARCH_TYPE_RU`
- groupsOnPage: `10`
- maxRequests: `2`
- maxCostRub: `1`

Observed sequence:

1. `start`
- status: `OK`
- job status: `RUNNING`
- total: `2`
- pending: `2`
- requests_started: `0`
- estimated_cost_rub: `0`
- request_executed: `false`
- automatic_retry: `false`

2. first `next` — `печать велеса`
- status: `SUCCEEDED`
- request_id: `search-batch-b9a5a44e-c103-4ab1-a5b5-75e5b10e9288`
- HTTP 200
- elapsed_ms: `952`
- result_count: `10`
- requests_started after call: `1`
- estimated_cost_rub after call: `0.488`
- request_executed: `true`
- automatic_retry: `false`

3. second `next` — `алатырь`
- status: `SUCCEEDED`
- request_id: `search-batch-930f9199-c558-4c34-a90b-b7b96552ce4c`
- HTTP 200
- elapsed_ms: `1049`
- result_count: `10`
- final job status: `COMPLETED`
- succeeded: `2`
- requests_started: `2`
- outcome_unknown: `0`
- estimated_cost_rub: `0.976`
- request_executed: `true`
- automatic_retry: `false`

4. local `status`
- request_executed: `false`
- requests_started remained `2`
- estimated_cost_rub remained `0.976`

5. local `projection`, topN=10
- request_executed: `false`
- requests_started remained `2`
- `печать велеса`: `market.yandex.ru` best observed rank = `3`; `ru.wikipedia.org` absent
- `алатырь`: `ru.wikipedia.org` best observed rank = `1`; `market.yandex.ru` absent

6. local `overlapPage`, topN=10
- request_executed: `false`
- requests_started remained `2`
- total_pairs: `1`
- `печать велеса` unique observed domains: `7`
- `алатырь` unique observed domains: `8`
- shared_domains: `[]`
- shared_count: `0`
- union_count: `15`
- jaccard: `0`
- left_containment: `0`
- right_containment: `0`

Owner-live verdict:
- exactly two ordinary Search provider crossings for two queries;
- zero automatic retries;
- `start`, `status`, `projection`, and `overlapPage` remained local-only;
- durable ranked SERP evidence survived across commands;
- sampled target-domain rank and pairwise TOP-domain overlap worked on real provider results;
- no outcome-unknown event occurred;
- owner-live estimated total = `0.976 RUB`.

`PHASE8_SEARCH_BATCH_OWNER_LIVE_PASS`
