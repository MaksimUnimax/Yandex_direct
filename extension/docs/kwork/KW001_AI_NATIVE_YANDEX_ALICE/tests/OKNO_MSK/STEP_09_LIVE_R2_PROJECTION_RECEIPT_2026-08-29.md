# KW-001 / OKNO-MSK — Step 09 live R2 projection receipt

Date: 2026-08-29  
Status: **LIVE PROVIDER EXECUTION RECEIPT / STEP 09 NOT YET ACCEPTED**

## R2 projection event

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
request_executed = false
automatic_retry = false
```

The projection command itself was non-billable.

## R2 accounting

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

At the configured estimate:

```text
74 * 0.488 = 36.112 RUB
```

## Combined initial-tranche acquisition accounting

The first canary in the original job already established one successful request at 0.488 RUB.

Combined truth:

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

The R2 projection exposes a normalized TOP-10 for all 74 R2 items. Together with the already persisted canary TOP-10, 75 direct SERP observations are available for Step-09 analysis.

## Evidence-persistence distinction

Provider acquisition completion is not Step-09 acceptance.

The R2 projection contains, per item:

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

It does not by itself expose the complete per-item provider request IDs or raw XML payloads for all 74 R2 items.

Therefore:

```text
PROVIDER_ACQUISITION_INITIAL_75 = COMPLETE
R2_NORMALIZED_PROJECTION_AVAILABLE = true
R2_PROVIDER_REQUEST_ACCOUNTING = COMPLETE_AT_JOB_LEVEL
R2_RAW_PER_ITEM_EVIDENCE_PROVEN_BY_PROJECTION_ALONE = false
REPOSITORY_SERP_LEDGER_COMPLETE = false
STEP09_ACCEPTED = false
STEP10_ALLOWED = false
```

`STEP_09_SERP_RESULTS.tsv` still needs to be expanded/reconciled beyond the first canary before Step-09 acceptance.

## Correction: original-job stale-queue inference was not live-confirmed

An earlier revision inferred that the original canary job still had 74 actionable pending items because its last observed state after canary #1 was `pending=74`.

A live non-provider cleanup attempt then executed:

```text
operation = batch.cancel
job_id = kw001-okno-msk-search-step09-20260829
```

Observed result:

```text
status = ERROR
stage = BATCH_RUNTIME
code = SEARCH_BATCH_JOB_NOT_FOUND
recoverable = true
request_executed = false
automatic_retry = false
autorun_continues = false
```

Correct interpretation:

```text
THE ORIGINAL JOB IS NOT PRESENT IN THE CURRENT LIVE BATCH RUNTIME UNDER THAT JOB ID.
```

The event does **not** prove why it is absent (purged, replaced, storage reset, lifecycle cleanup, or another cause). It only proves that no live `cancel` or paid `next` can currently target that job ID through this runtime state.

Therefore the prior statement "the original job's remaining queue is now stale duplicate work and must be cancelled" is superseded.

Accounting for the failed cancel:

```text
provider requests = 0
provider cost = 0 RUB
```

Non-repeat control:

```text
LAST_OBSERVED_JOB_STATE != CURRENT_LIVE_JOB_EXISTENCE
```

Before issuing a cleanup/control command against an old job, current runtime existence must be verified when the action itself could otherwise be misleading.

## Direct Step-09 observations visible in the R2 projection

These remain evidence observations only, not Step-10 clusters or Step-11 page ownership.

Examples of strong boundaries:

```text
алюминиевые окна fapim => fittings/components commerce
дом с панорамными окнами => house-project/construction SERP
панорамные окна лес => property/rental/lifestyle SERP
как выбрать шторы на пластиковые окна => curtain/blind informational intent
шторы на пластиковые окна фото цены => curtain/blind commerce intent
пластиковые двери видео => video / DIY installation intent
пластиковые двери старый => used-door marketplace intent
пошаговая установка пластиковых окон => informational DIY installation intent
установка пластиковых окон пошагово => informational DIY installation intent
установка пластиковых окон москва => commercial installation-service intent
```

Examples of strong commercial result types:

```text
остекление балкона с выносом
остекление балкона с выносом подоконника
=> commercial glazing-with-extension landing pattern

остекление балкона с крышей
остекление балкона с крышей цена
=> commercial glazing-with-roof landing pattern

теплое остекление балкона
холодное остекление балкона
=> modifier-led commercial landing patterns

остекление балкона п 46
=> highly specific house-series landing pattern

пластиковые окна митино
=> geo-specific local landing pattern

ремонт пластиковых окон в одинцове
ремонт пластиковых окон в одинцово
=> local repair/service SERPs with local aggregators/maps
```

The eight active nonexact duplicate pairs now have direct SERP evidence for both variants. Their overlap must be calculated explicitly rather than inferred lexically.

## Next Step-09 work

```text
1. preserve/reconcile all 75 observed normalized SERPs in the repository;
2. reconcile per-item raw/result identifiers from durable bridge state or prior live envelopes where available;
3. calculate the eight active duplicate-pair overlaps;
4. produce evidence-question decisions without performing Step-10 clustering;
5. update REVIEW_SEARCH coverage ledger;
6. produce Step-09 reconciliation and acceptance QA;
7. keep Step 10 blocked pending explicit owner authorization.
```
