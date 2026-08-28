# KW-001 / OKNO-MSK — STEP 03 WORDSTAT PASS #1 CHECKPOINT 05

Date: 2026-08-28  
Status: **ACTIVE / PROVIDER EXECUTION IN PROGRESS**

This checkpoint supplements `STEP_03_WORDSTAT_PASS1_EXECUTION_LOG.md` and records provider item S05 plus cumulative progress after five live Wordstat requests.

## Provider item S05 — `пластиковые двери`

```text
item_status = SUCCEEDED
phrase = пластиковые двери
region = 213
device = DEVICE_ALL
numPhrases = 200
http_status = 200
request_executed = true
automatic_retry = false
request_id = wordstat-batch-da5f237f-72d0-4d3d-9743-776bd70a35f6
elapsed_ms = 1683
estimated_cost_rub = 0.02
root_totalCount = 27229
returned_results = 200
returned_associations = 15
```

### Acquisition observations only

The broad door family contains materially different raw demand directions, including:

```text
entry doors
balcony doors
private-house / exterior doors
glazed vs non-glazed configurations
sliding doors
purchase / price / Moscow
installation
repair / adjustment
hardware / locks / handles / hinges
used / marketplace demand
```

Examples observed: `пластиковые двери входные`, `пластиковая балконная дверь`, `купить пластиковую дверь`, `пластиковая дверь цена`, `пластиковая дверь в дом`, `раздвижные пластиковые двери`, `установка пластиковой двери`, `ремонт пластиковых дверей`, `регулировка пластиковых дверей`, `пластиковые двери рехау`.

No cluster/page decision is made at Step 3. These remain raw acquisition observations for later cleanup and SERP-boundary analysis.

## Cumulative checkpoint after S05

```text
job_id = kw001-okno-msk-wordstat-pass1-20260828
status = RUNNING
total = 18
requests_started = 5
succeeded = 5
failed_terminal = 0
outcome_unknown = 0
pending = 13
estimated_cost_rub = 0.10
next_safe_action = CLAIM_NEXT
STEP_03_COMPLETE = false
```
