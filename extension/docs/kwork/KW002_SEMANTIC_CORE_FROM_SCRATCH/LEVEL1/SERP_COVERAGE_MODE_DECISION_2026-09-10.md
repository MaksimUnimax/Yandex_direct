# KW-002 — SERP COVERAGE MODE DECISION

Date: 2026-09-10
Status: **LEVEL-1 / OWNER-FROZEN / ACTIVE**
Product: greenfield semantic core + clustering + target site architecture.

Portfolio research:

`../../../KWORK_SERP_COVERAGE_MODE_RESEARCH_2026-09-10.md`

Portfolio gate:

`../../../KWORK_SERP_MODE_PRODUCTIZATION_GATE_2026-09-10.md`

## Frozen mode

```text
SERP_COVERAGE_MODE = FULL_SERP_COVERAGE
OWNER_DECISION_DATE = 2026-09-10
PER_CLIENT_MODE_REPROOF = false
```

## Exact scope of FULL

FULL applies to the final cleaned and purchased/frozen Search-stage phrase set.

```text
RAW_WORDSTAT_OCCURRENCES != SEARCH_INPUT
NORMALIZED_BUT_EXCLUDED != SEARCH_INPUT
VALID_RESERVE_OUTSIDE_PURCHASED_SCOPE != SEARCH_INPUT BY DEFAULT
DELIVERY_SELECTED / SEARCH_STAGE_SET = FULL SERP COVERAGE REQUIRED
```

Therefore a large raw acquisition corpus may contain tens of thousands of occurrences while the full Search-covered set remains bounded by the product's final governed/delivery scope.

## Why FULL is frozen for KW-002

KW-002 designs a target architecture from scratch rather than merely checking an established site's existing page structure.

The sold result includes:

```text
clean final semantic core
-> SERP-grounded final clustering
-> query/cluster -> planned page ownership
-> target Search-only site architecture
```

For this product the owner has selected full current SERP coverage of the final Search-stage set to reduce sampling blind spots in page-boundary design.

This does not make SERP overlap automatic truth. Final decisions still require semantic/user-task/business review.

## Required FULL coverage accounting

Before final clustering:

```text
SEARCH_STAGE_SELECTED_ROWS = N
USABLE_DIRECT_OR_VALID_REUSED_SERP_ROWS = N
MISSING_REQUIRED_SERP_ROWS = 0 for full PASS
```

A failed/unretrieved phrase cannot be silently treated as covered. It remains explicit and blocks a full-coverage claim until resolved/degraded by an authorized rule.

## Evidence reuse

Fresh provider calls are not required when an existing preserved observation matches the product's declared reuse contract, including exact query identity, region/search mode, required result depth, freshness and payload/provenance sufficiency.

Reuse must remain explicit.

## Machine vs analyst work

FULL does not mean Work/LLM manually reads every raw Search body.

Allowed architecture:

```text
FULL persisted SERP evidence
-> compact ranked URL/domain projection
-> deterministic URL-overlap/candidate grouping where useful
-> Work/analyst reviews meaning, intent, business scope, mixed clusters and split/merge boundaries
```

No universal URL-overlap threshold is frozen here.

## Provider transport

Current accepted Bridge ordinary Search path is synchronous.

Yandex officially supports cheaper deferred/asynchronous text Search, but current Bridge does not yet implement the async Operation lifecycle.

Research authority:

`../../../YANDEX_SEARCH_ASYNC_DEFERRED_RESEARCH_2026-09-10.md`

Therefore:

```text
KW002_SERP_COVERAGE_METHOD = FULL
KW002_PROVIDER_TRANSPORT_IMPLEMENTATION = CURRENT_ACCEPTED_ROUTE UNTIL ASYNC PATCH IS SEPARATELY VALIDATED
```

Do not treat deferred Search as production capability before the Bridge patch/regression gate passes.

## Re-open trigger

Normal KW-002 client jobs do not debate FULL vs SELECTIVE again.

Re-open only for a material new KW-002 product version, owner-directed scope change, or validated evidence that the product promise/method should change.