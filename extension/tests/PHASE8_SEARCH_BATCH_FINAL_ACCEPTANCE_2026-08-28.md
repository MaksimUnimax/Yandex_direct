# Phase 8 Search Batch final acceptance — 2026-08-28

Status: `PHASE8_SEARCH_BATCH_FINAL_ACCEPTANCE_PASS`

## Frozen product authority

```text
source = 0377d6e1f176d4b7ddd8553c0099e02a4f1e8716
extension = 446fed6970c5fec627be34c3893800dc4511c6c9
extension/src = bdad1e87a2537d8646e480ca23f8068c3dced17e
freeze run = 33143237276 / SUCCESS
candidate ZIP sha256 = 8f6ba92dbe1f592a62c66cd250ed942e261f56deffbe87117371bd9c481e6332
```

## Owner-live

```text
job = p8-owner-live-2026-08-28
queries = печать велеса | алатырь
start provider requests = 0
next calls = 2
successful provider requests = 2
requests_started = 2
succeeded = 2
outcome_unknown = 0
automatic_retry = false
estimated_cost_rub = 0.976
status provider requests = 0
projection provider requests = 0
overlapPage provider requests = 0
```

Observed target-domain rank evidence:
- `печать велеса`: `market.yandex.ru` best observed TOP-10 rank = 3;
- `алатырь`: `ru.wikipedia.org` best observed TOP-10 rank = 1.

Observed pairwise TOP-10 domain evidence:

```text
left = печать велеса
right = алатырь
left_domain_count = 7
right_domain_count = 8
shared_count = 0
union_count = 15
jaccard = 0
left_containment = 0
right_containment = 0
```

## Production integration

```text
main integration = ebd697e5733a7d40d13401d4c02b82a75711231c
postmerge workflow = 33144396638 / SUCCESS
Node regression = 118/118
controlled installed-extension browser = PASS
product immutability = PASS
real_yandex_requests in controlled browser = 0
```

No sixth service was created. Search batch remains orchestration within `service=search` and uses ordinary Search only.

`PHASE8_SEARCH_BATCH_FINAL_ACCEPTANCE_PASS`
