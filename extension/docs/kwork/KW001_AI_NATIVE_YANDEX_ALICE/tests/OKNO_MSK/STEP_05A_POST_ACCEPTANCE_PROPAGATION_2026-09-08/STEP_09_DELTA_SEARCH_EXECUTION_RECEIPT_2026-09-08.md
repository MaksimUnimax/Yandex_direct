# OKNO_MSK — Step 09 delta Search acquisition receipt

Date: 2026-09-08  
Status: **ACQUIRED / DURABLY MATERIALIZED**

## Scope

Exactly six Step-09 ordinary Yandex Search probes required by the post-acceptance Step-5A propagation impact register were executed.

Job:

`kw001-okno-msk-step09-delta-20260908-r1`

Parameters:

- service: `search`
- search type: `SEARCH_TYPE_RU`
- region: `213`
- TOP: `10`
- max requests: `6`
- max cost: `3 RUB`
- live Bridge runtime: `0.1.4`

## Execution chain

1. `batch.start` — `OK`; `request_executed=false`; six pending items; zero provider requests.
2. Delivery attempt failed with `SEND_BUTTON_NOT_READY`; `request_executed=false`; no provider boundary crossed.
3. Delivery attempt failed with `COMPOSER_NOT_FOUND`; `request_executed=false`; no provider boundary crossed.
4. `batch.nextN count=6` — `OK`; job `COMPLETED`.

Final accounting:

- confirmed provider executions: **6**
- succeeded: **6**
- failed terminal: **0**
- outcome unknown: **0**
- automatic retry: **false**
- duplicate paid calls caused by delivery failures: **0**
- estimated cost: **2.928 RUB**
- next safe action: `NONE`

## Durable evidence

- `STEP_09_DELTA_SEARCH_ACQUISITION_RECEIPT_NORMALIZED_2026-09-08.json`
- `STEP_09_DELTA_SEARCH_TOP10_EVIDENCE_2026-09-08.tsv`

The JSON is a normalized durable projection from the chat-delivered Bridge receipts. It does **not** claim byte identity with browser-storage raw: Markdown URL wrappers and escaped field-name/domain presentation were normalized, and snippets were omitted from this projection. Query text, request IDs, HTTP status, timing, accounting, and TOP10 rank / URL / domain / title / modtime are preserved.

No additional provider call is required to use these six observations downstream.

## Queries

1. `гидроизоляция открытого балкона в частном доме`
2. `лучшая гидроизоляция для открытого балкона`
3. `как сделать гидроизоляцию на открытом балконе`
4. `гидроизоляция открытого деревянного балкона`
5. `гидроизоляция балконной плиты открытого балкона`
6. `шумоизоляция крыши балкона изнутри от дождя`

## Boundary

These observations are exact-query Search evidence. They must not be silently promoted to proof for an entire semantic family. Downstream Step10–18 routing must compare the six exact observations with the existing canonical family / owner / structural authorities and update only the affected seven Step-5A directions.
