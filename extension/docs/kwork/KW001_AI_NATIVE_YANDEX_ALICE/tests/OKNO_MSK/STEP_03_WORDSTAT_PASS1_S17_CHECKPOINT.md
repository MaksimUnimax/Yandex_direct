# KW-001 / OKNO-MSK — STEP 03 WORDSTAT PASS #1 — S17 CHECKPOINT

Date: 2026-08-28
Status: **SUCCEEDED / RAW ACQUISITION EVIDENCE PRESERVED**

## Seed

```text
seed_id = S17
phrase = как выбрать пластиковые окна
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
request_id = wordstat-batch-7e1949b4-fcec-4369-a403-bf5e58b2b80c
elapsed_ms = 1786
estimated_cost_rub = 0.02
root_totalCount = 254
returned_results = 32
returned_associations = 17
```

Checkpoint after S17:

```text
progress.status = RUNNING
total = 18
pending = 1
succeeded = 17
failed_terminal = 0
outcome_unknown = 0
terminal = 17
requests_started = 17
estimated_cost_rub = 0.34
next_safe_action = CLAIM_NEXT
```

## Acquisition observations only

The seed confirms a measurable informational/selection demand family. Relevant raw branches include:

- how to choose plastic windows;
- correct/good/quality window selection;
- apartment vs private-house selection;
- profile selection;
- glazing-unit selection;
- size selection;
- recommendation/expert-selection language.

Examples observed in provider output include `как выбрать пластиковые окна = 254`, `как правильно выбрать пластиковые окна = 85`, `как выбрать пластиковые окна для квартиры = 22`, `как выбрать окна пластиковые для частного дома = 13`, `как выбрать профиль для пластиковых окон правильно = 12`, `как выбрать стеклопакет для пластиковых окон = 7`.

The raw list also contains accessory-oriented tails such as curtains, seals and mosquito nets, while associations are heavily contaminated by broad unrelated vocabulary. These are preserved as acquisition evidence and are not cleaned here.

This checkpoint does **not** decide whether the family deserves a standalone guide/supporting-content page. Cleanup, clustering and later SERP/page-boundary evidence remain required.

## Step state

```text
STEP_03_COMPLETE = false
next_seed = S18
next_phrase = пластиковые окна от производителя
```
