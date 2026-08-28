# KW-001 / OKNO-MSK — STEP 03 WORDSTAT PASS #1 — S18 CHECKPOINT

Date: 2026-08-28
Status: **SUCCEEDED / RAW ACQUISITION EVIDENCE PRESERVED**

## Seed

```text
seed_id = S18
phrase = пластиковые окна от производителя
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
request_id = wordstat-batch-4d5df692-28ff-4f09-b3c7-dc1c5908c4e9
elapsed_ms = 801
estimated_cost_rub = 0.02
root_totalCount = 1589
returned_results = 130
returned_associations = 17
```

Checkpoint after S18:

```text
progress.status = COMPLETED
total = 18
pending = 0
succeeded = 18
failed_terminal = 0
outcome_unknown = 0
terminal = 18
requests_started = 18
estimated_cost_rub = 0.36
next_safe_action = NONE
```

## Acquisition observations only

The raw manufacturer-oriented seed exposed commercially relevant demand around:

- direct-from-manufacturer language;
- Moscow-local purchase demand;
- price / inexpensive / buy / order language;
- installation / turnkey combinations;
- REHAU manufacturer combinations;
- official-site / factory / manufacturer vocabulary;
- a long GEO tail across Moscow Region and unrelated out-of-region locations.

Examples observed include `пластиковые окна от производителя`, `недорогие окна пластиковые от производителя`, `пластиковые окна от производителя с установкой`, `пластиковые окна в москве от производителя`, `пластиковые окна от производителя цены`, `купить пластиковые окна от производителя`, `пластиковые окна от производителя под ключ`.

This checkpoint does **not** prove a separate manufacturer/trust landing page or GEO expansion. Cleanup, clustering and later SERP/page-boundary evidence remain required.

## Batch terminal state observed on S18 response

The final `batch.next` response itself reported the batch as fully terminal and successful:

```text
status = COMPLETED
succeeded = 18
failed_terminal = 0
outcome_unknown = 0
pending = 0
requests_started = 18
estimated_cost_rub = 0.36
next_safe_action = NONE
```

A separate non-provider `batch.status` read is still required by the Step-03 completion gate to capture final durable job status independently before closing the step.

## Step state

```text
STEP_03_COMPLETE = false
next_action = batch.status
provider_acquisition_complete = true
```
