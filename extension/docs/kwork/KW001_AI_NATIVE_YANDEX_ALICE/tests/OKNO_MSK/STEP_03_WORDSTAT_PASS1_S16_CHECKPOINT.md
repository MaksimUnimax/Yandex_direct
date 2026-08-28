# KW-001 / OKNO-MSK — STEP 03 WORDSTAT PASS #1 — S16 CHECKPOINT

Date: 2026-08-28
Status: **SUCCEEDED / RAW ACQUISITION EVIDENCE PRESERVED**

## Seed

```text
seed_id = S16
phrase = окна в рассрочку
service = wordstat
method = getTop
region = 213 (Moscow)
devices = DEVICE_ALL
numPhrases = 200
```

## Provider result

```text
item_status = SUCCEEDED
http_status = 200
request_executed = true
automatic_retry = false
request_id = wordstat-batch-de8e567d-b18b-43df-8e37-ea752a1c629c
elapsed_ms = 413
estimated_cost_rub = 0.02
root_totalCount = 507
returned_results = 69
returned_associations = 13
```

Checkpoint after S16:

```text
progress.status = RUNNING
total = 18
pending = 2
succeeded = 16
failed_terminal = 0
outcome_unknown = 0
terminal = 16
requests_started = 16
estimated_cost_rub = 0.32
next_safe_action = CLAIM_NEXT
```

## Acquisition observations only

The financing-oriented seed produced a moderate but clearly commercial demand family, including:

- broad installment intent;
- PVC-window installment intent;
- Moscow-local installment demand;
- without-bank / internal-installment language;
- buy/order/install language;
- REHAU-branded installment formulations;
- price / with-installation variants;
- scattered out-of-region GEO noise.

Examples observed in provider output include `окна в рассрочку = 507`, `пластиковые окна в рассрочку = 212`, `окна в рассрочку в москве = 129`, `окна в рассрочку без банка = 38`, `установка окон в рассрочку = 28`, `окна rehau в рассрочку = 26`.

Associations were mostly weak or off-intent and should not be promoted automatically into expansion seeds.

This checkpoint does **not** decide whether installment financing deserves a dedicated finance landing page. Cleanup, clustering and later ordinary-Yandex SERP/page-job evidence remain required.

## Step state

```text
STEP_03_COMPLETE = false
next_seed = S17
next_phrase = как выбрать пластиковые окна
```
