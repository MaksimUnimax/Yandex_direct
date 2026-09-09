# KW-002 Blood & Sand — STEP 03 WORDSTAT BATCH START ACCEPTANCE

Date: 2026-09-09

Status: **PASS / DURABLE QUEUE CREATED / ZERO PROVIDER REQUESTS / Q001 NEXT ONLY**

## Observed runtime result

Source: owner-relayed `WORDSTAT_BATCH_RESULT_V1` from the actual Yandex Marketing Bridge runtime.

Observed runtime provenance:

```text
bridge = yandex-marketing-bridge
runtime_version = 0.1.4
service = wordstat
operation = batch.start
job_id = BLOOD_SAND_GREENFIELD_2026-09-08__STEP03_PRIMARY_V1
status = OK
```

Note: current repository documentation previously described extension version 0.1.2. The actual runtime returned 0.1.4. This version difference is preserved as provenance and is not silently rewritten. It is not a blocker for this start acceptance because the observed protocol/result shape and all execution controls match the expected Step-03 contract.

## Queue accounting

```text
total = 79
input_count = 79
duplicate_count = 0
pending = 79
claimed = 0
requesting = 0
succeeded = 0
failed_terminal = 0
outcome_unknown = 0
skipped = 0
cancelled = 0
terminal = 0
requests_started = 0
estimated_cost_rub = 0
active_item_id = null
stop_reason = null
next_safe_action = CLAIM_NEXT
```

## Policy/accounting

```text
numPhrases = 2000
regions = ["225"]
devices = ["DEVICE_ALL"]
maxRequests = 79
maxCostRub = 2
request_executed = false
automatic_retry = false
provider_result = null
```

## Acceptance checks

```text
EXPECTED_INPUT_ITEMS = 79
OBSERVED_INPUT_ITEMS = 79
DUPLICATE_INPUT_ITEMS = 0
PROVIDER_REQUESTS_EXPECTED_FOR_START = 0
PROVIDER_REQUESTS_OBSERVED = 0
BILLABLE_COST_EXPECTED_FOR_START = 0
BILLABLE_COST_OBSERVED = 0
JOB_STATUS = RUNNING
NEXT_SAFE_ACTION = CLAIM_NEXT
BATCH_START = PASS
```

## Durable evidence

Exact result envelope persisted at:

`STEP_03_WORDSTAT_BATCH_START_RESULT_2026-09-09.txt`

No row has yet been added to `STEP_03_WORDSTAT_ACQUISITION_RECEIPTS.csv` because that ledger is per provider item and `batch.start` executes no provider item.

## Next authorised action

Exactly one provider item is authorised next:

```text
batch.next
→ item 1
→ Q001
→ (амулет|оберег|талисман) RSOTM
```

After Q001 returns:

```text
persist complete raw envelope/provider_result
→ remote readback
→ reconcile results/associations/totalCount/request_id/cost
→ accept or reject grouped-OR path
→ only then decide whether another batch.next is allowed
```

`NEXT_STEP_ALLOWED = false` remains in force because Step 03 is still in progress.
