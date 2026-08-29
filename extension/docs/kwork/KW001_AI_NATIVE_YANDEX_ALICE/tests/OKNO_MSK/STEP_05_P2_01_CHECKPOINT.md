# KW-001 / OKNO-MSK — STEP 05 P2-01 CHECKPOINT

Date: 2026-08-29  
Status: **P2-01 SUCCEEDED / ACQUISITION EVIDENCE ONLY**

## Probe

```text
job_id = kw001-okno-msk-wordstat-pass2-20260828
probe_id = P2-01
phrase = оконная фурнитура
method = getTop
region = 213
devices = DEVICE_ALL
numPhrases = 200
reason = NEW_VOCABULARY
```

## Provider result

```text
status = SUCCEEDED
http_status = 200
request_executed = true
automatic_retry = false
request_id = wordstat-batch-211dce0d-f4c6-4ab1-b074-fec49f38fc9a
elapsed_ms = 2037
estimated_cost_rub = 0.02
root_totalCount = 1459
```

Batch checkpoint after P2-01:

```text
status = RUNNING
total = 4
pending = 3
succeeded = 1
failed_terminal = 0
outcome_unknown = 0
terminal = 1
requests_started = 1
estimated_cost_rub = 0.02
next_safe_action = CLAIM_NEXT
```

## Acquisition observations

This probe materially expanded the vocabulary compared with the pass-1 literal seed `аксессуары для пластиковых окон`.

Observed result families include:

```text
commercial purchase/shop/Moscow vocabulary
brand vocabulary: Vorne, Roto, Maco, Siegenia, GU, Internika and others
selection/review/rating vocabulary
repair/regulation/replacement vocabulary
parts/mechanisms vocabulary: reducer, kit, hinge, trunnion, scissors and related components
maintenance/lubrication vocabulary
PVC-specific fittings vocabulary
```

Examples with measured counts include:

```text
оконная фурнитура = 1459
оконная фурнитура для окон = 193
оконная фурнитура для пластиковых = 170
оконная фурнитура для пластиковых окон = 163
оконная фурнитура отзывы = 78
оконная фурнитура vorne = 64
лучшая оконная фурнитура = 52
оконная фурнитура roto = 52
купить оконную фурнитуру = 51
магазин оконной фурнитуры = 45
оконная фурнитура москва = 39
регулировка оконной фурнитуры = 38
ремонт оконной фурнитуры = 37
```

Associations also contain substantial unrelated/noisy meanings; they remain raw provider evidence only.

## Interpretation boundary

This checkpoint does **not** decide:

```text
whether accessories/fittings are a standalone commercial priority
which phrases enter the final semantic core
whether a separate page is justified
whether repair/regulation belongs to the same page/job
cluster/page mapping
```

P2-01 therefore validates the acquisition rationale `NEW_VOCABULARY` without promoting the returned phrases to final semantics.
