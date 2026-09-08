# Step 5A.6 — Search item 05 unknown-outcome reconciliation decision

Job: `kw001-okno-msk-step05a-search-recheck-20260908`

Query: `окна для старого фонда`

Request ID: `search-batch-02843120-5147-4169-aa11-366b3228221e`

Observed terminal item state: `OUTCOME_UNKNOWN`

Bridge reason: `REQUEST_OUTCOME_UNKNOWN_NO_RETRY`

Batch stop reason: `OUTCOME_UNKNOWN_REQUIRES_RECONCILIATION`

Batch next safe action: `RECONCILE_UNKNOWN`

## Evidence decision

The request crossed the durable `REQUEST_STARTED` boundary. The batch therefore reserved/accumulated the configured estimated Search cost of `0.488 RUB` for this item, but the provider outcome and actual returned Search evidence are unknown. No SERP result may be inferred or fabricated.

The query is preserved as unresolved evidence state:

`HOLD_EVIDENCE__SEARCH_REQUEST_OUTCOME_UNKNOWN`

This is not a negative Search result, not an empty SERP, and not proof that the request was not billed.

## Retry decision

`DO_NOT_RETRY_UNKNOWN_QUERY`

Automatic retry is prohibited by the Bridge contract. Main ChatGPT will not issue another Search request for `окна для старого фонда` during this Step 5A execution.

## Batch reconciliation procedure

The Search batch protocol exposes no `reconcile` action. The provider batch model intentionally blocks all later `claimNext` operations while an `OUTCOME_UNKNOWN` item remains in the same job.

Therefore the owner-side reconciliation is:

1. preserve item 05 as `HOLD_EVIDENCE__SEARCH_REQUEST_OUTCOME_UNKNOWN`;
2. cancel the current job, which preserves the terminal unknown item and cancels only its still-pending items;
3. create a new bounded Search batch containing only the four untouched pending requirements:
   - `балконы под офис`
   - `кладовая на балконе`
   - `шумоизоляция на крышу балкона`
   - `армирование оконного профиля`
4. do not include or replay `окна для старого фонда` in the replacement batch;
5. carry the unresolved item into final Step 5A.7 decisioning as HOLD unless independent preserved evidence legally resolves it without another provider call.

This procedure does not reinterpret unknown as success/failure, does not fabricate SERP evidence, and does not create a second paid boundary for the unknown query.
