# KW-001 / OKNO-MSK — STEP 03 WORDSTAT PASS #1 — S15 CHECKPOINT

Date: 2026-08-28
Status: **SUCCEEDED / RAW ACQUISITION EVIDENCE PRESERVED**

## Seed

```text
seed_id = S15
phrase = цены на пластиковые окна
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
request_id = wordstat-batch-05d2483d-7bd4-4842-8f85-aff472fed49c
elapsed_ms = 713
estimated_cost_rub = 0.02
root_totalCount = 2023
returned_results = 200
returned_associations = 11
```

Checkpoint after S15:

```text
progress.status = RUNNING
total = 18
pending = 3
succeeded = 15
failed_terminal = 0
outcome_unknown = 0
terminal = 15
requests_started = 15
estimated_cost_rub = 0.30
next_safe_action = CLAIM_NEXT
```

## Acquisition observations only

The raw price-oriented seed exposed several materially different demand branches, including:

- broad price/commercial demand;
- Moscow-local price demand;
- price with installation / turnkey context;
- balcony, dacha, kitchen and veranda applications;
- replacement / retrofit price language;
- size-specific price formulations;
- mosquito-net / accessory / fitting / glazing-unit price tails;
- calculator / calculate-price language;
- marketplace and out-of-region noise.

Examples observed in provider output include `цены на пластиковые окна`, `цена на пластиковые окна с установкой`, `цены на пластиковые окна в москве`, `пластиковые окна на балкон цена`, `замена окна на пластиковые цена`, `цена на пластиковое окно размер`, `калькулятор цен на пластиковые окна`.

This checkpoint does **not** decide that “price” deserves a separate page, nor does it merge accessory/repair tails into the commercial core. Cleanup, clustering and later SERP/page-boundary evidence remain required.

## Step state

```text
STEP_03_COMPLETE = false
next_seed = S16
next_phrase = окна в рассрочку
```
