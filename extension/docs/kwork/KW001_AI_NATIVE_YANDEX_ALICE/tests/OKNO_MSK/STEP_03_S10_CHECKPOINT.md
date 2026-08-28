# KW-001 / OKNO-MSK — STEP 03 S10 CHECKPOINT

Date: 2026-08-28
Status: **PROVIDER ITEM SUCCEEDED / STEP 03 STILL ACTIVE**

## Item

```text
seed = остекление веранды
method = getTop
region = 213 (Moscow)
devices = DEVICE_ALL
numPhrases = 200
request_id = wordstat-batch-5579a3b1-a1db-4638-b1f5-7a0c0ad4f773
http_status = 200
elapsed_ms = 700
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
root_totalCount = 1373
```

## Batch checkpoint after S10

```text
total = 18
pending = 8
succeeded = 10
failed_terminal = 0
outcome_unknown = 0
terminal = 10
requests_started = 10
estimated_cost_rub = 0.20
next_safe_action = CLAIM_NEXT
STEP_03_COMPLETE = false
```

## Acquisition observations only

The seed exposes a real veranda/terrace glazing demand family with multiple formulations around:

- veranda / terrace;
- price and turnkey intent;
- aluminium glazing;
- sliding systems;
- cold / warm glazing;
- frameless glazing;
- dacha / private-house use;
- panoramic glazing;
- Moscow Region and other GEO modifiers.

Examples observed in raw provider output include `остекление веранды и террасы`, `остекление веранды цена`, `алюминиевое остекление веранды`, `раздвижное остекление веранды`, `холодное остекление веранды`, `теплое остекление веранды`, `безрамное остекление веранды`, `остекление веранды на даче`, `панорамное остекление веранды`, `остекление веранд под ключ`.

This checkpoint makes no cleanup, clustering, page-boundary, or architecture decision. Out-of-region and noisy formulations remain preserved as raw acquisition evidence for the later cleanup step.
