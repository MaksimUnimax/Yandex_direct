# KW-001 / OKNO-MSK — Step 09 live R2 projection receipt

Date: 2026-08-29  
Status: **LIVE PROVIDER EXECUTION RECEIPT / STEP 09 NOT YET ACCEPTED**

## Source event

Observed live bridge result:

```text
service = search
operation = batch.projection
job_id = kw001-okno-msk-search-step09-20260829-r2
status = OK
projection.offset = 0
projection.limit = 74
projection.topN = 10
projection.total_successful = 74
projection.next_offset = null
```

The projection command itself is non-billable:

```text
request_executed = false
automatic_retry = false
```

## R2 execution accounting

The completed R2 job reports:

```text
job status = COMPLETED
total = 74
pending = 0
succeeded = 74
failed_terminal = 0
outcome_unknown = 0
terminal = 74
requests_started = 74
estimated_cost_rub = 36.11199999999997
next_safe_action = NONE
max_requests = 74
max_cost_rub = 38.552
```

This is consistent with the configured 0.488 RUB/request unit estimate:

```text
74 * 0.488 = 36.112 RUB
```

## Combined initial-tranche acquisition accounting

The first canary in the original job already established:

```text
query = аксессуары для пластиковых окон
requests_started = 1
succeeded = 1
outcome_unknown = 0
estimated_cost_rub = 0.488
```

Combining the canary with R2:

```text
initial tranche probes = 75
provider requests started = 75
provider requests succeeded = 75
failed_terminal = 0
outcome_unknown = 0
estimated cumulative cost = 36.600 RUB
authorized ceiling = 39.040 RUB
provider acquisition target for the initial 75 probes = COMPLETE
```

The R2 projection exposes a normalized TOP-10 for all 74 R2 items. Together with the already persisted canary TOP-10, the initial tranche has 75 direct SERP observations available for analysis.

## Important evidence-persistence distinction

Do **not** equate provider acquisition completion with Step-09 acceptance.

The projection is a normalized reusable view containing, per item:

```text
item_id
query_text
region
search_type
requested_groups
observed_result_count
ranked_results(rank,url,domain,title)
top_domains
```

However this projection envelope does not itself expose the per-item provider request IDs or complete raw XML payloads for the 74 R2 items.

Therefore the correct current distinction is:

```text
PROVIDER_ACQUISITION_INITIAL_75 = COMPLETE
R2_NORMALIZED_PROJECTION_AVAILABLE = true
R2_PROVIDER_REQUEST_ACCOUNTING = COMPLETE_AT_JOB_LEVEL
R2_RAW_PER_ITEM_EVIDENCE_PROVEN_BY_THIS_PROJECTION_ALONE = false
REPOSITORY_SERP_LEDGER_COMPLETE = false
STEP09_ACCEPTED = false
STEP10_ALLOWED = false
```

The existing `STEP_09_SERP_RESULTS.tsv` currently persists only the first canary TOP-10. It must be expanded/reconciled before Step-09 acceptance.

## Stale original-job hazard

The original canary job was created with all 75 probes and, after canary #1, had 74 pending items:

```text
job_id = kw001-okno-msk-search-step09-20260829
succeeded = 1
pending = 74
```

R2 is a separate job:

```text
job_id = kw001-okno-msk-search-step09-20260829-r2
succeeded = 74
pending = 0
status = COMPLETED
```

Therefore the original job's remaining queue is now stale duplicate work. It must not receive another paid `next`.

Required operational cleanup:

```text
cancel kw001-okno-msk-search-step09-20260829
```

This is a non-provider control action and exists solely to eliminate accidental duplicate paid acquisition.

## Immediate analytical implications visible in the R2 projection

These are Step-09 evidence observations only, not Step-10 clusters or Step-11 page-ownership decisions.

Strong boundary examples observed directly:

```text
алюминиевые окна fapim
=> fittings/components commerce, not aluminium-window installation service.

дом с панорамными окнами
=> house-project/construction SERP, not a window-product SERP.

панорамные окна лес
=> property/rental/lifestyle SERP, not window purchase/installation.

как выбрать шторы на пластиковые окна
шторы на пластиковые окна фото цены
=> curtain/blind informational/commerce SERPs, not window product/service intent.

пластиковые двери видео
=> video / DIY installation intent.

пластиковые двери старый
=> used-door marketplace intent.

пошаговая установка пластиковых окон
установка пластиковых окон пошагово
=> informational DIY installation intent.

установка пластиковых окон москва
=> commercial installation-service intent.
```

Strong direct service/result-type examples:

```text
остекление балкона с выносом
остекление балкона с выносом подоконника
=> dedicated commercial glazing-with-extension result type.

остекление балкона с крышей
остекление балкона с крышей цена
=> dedicated commercial glazing-with-roof result type.

теплое остекление балкона
холодное остекление балкона
=> distinct modifier-led commercial landing patterns.

остекление балкона п 46
=> highly specific house-series landing-page pattern.

пластиковые окна митино
=> geo-specific local landing/contact pattern.

ремонт пластиковых окон в одинцове
ремонт пластиковых окон в одинцово
=> strongly local repair/service SERPs including local service aggregators/maps.
```

The active nonexact duplicate pairs now have direct SERP evidence for both variants; their overlap must be calculated explicitly in `STEP_09_SERP_COMPARISONS.tsv` rather than inferred lexically.

## Next Step-09 work after stale-job cleanup

```text
1. preserve/reconcile all 75 observed normalized SERPs in the repository;
2. reconcile per-item raw/result identifiers from durable bridge state or prior live result envelopes where available;
3. calculate the eight active duplicate-pair overlaps;
4. produce evidence-question decisions without performing Step-10 clustering;
5. update REVIEW_SEARCH coverage ledger;
6. produce Step-09 reconciliation and acceptance QA;
7. keep Step 10 blocked pending explicit owner authorization.
```
