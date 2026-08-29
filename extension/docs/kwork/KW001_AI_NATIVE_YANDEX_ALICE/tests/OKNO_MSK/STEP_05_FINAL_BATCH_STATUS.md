# KW-001 / OKNO-MSK — STEP 05 FINAL BATCH STATUS

Date: 2026-08-29  
Status: **COMPLETED / CONTROL STATUS CAPTURED**

## Batch identity

```text
service = wordstat
operation = batch.status
job_id = kw001-okno-msk-wordstat-pass2-20260828
bridge_version = 0.1.1
```

## Final durable progress

```text
status = COMPLETED
total = 4
input_count = 4
duplicate_count = 0
pending = 0
claimed = 0
requesting = 0
succeeded = 4
failed_terminal = 0
outcome_unknown = 0
skipped = 0
cancelled = 0
terminal = 4
requests_started = 4
estimated_cost_rub = 0.08
active_item_id = null
stop_reason = null
next_safe_action = NONE
```

## Status-call execution truth

```text
request_executed = false
automatic_retry = false
provider_result = null
```

The final `batch.status` itself did not execute a provider request. It only confirmed the already-completed durable batch state.

## Frozen manifest executed

```text
P2-01 оконная фурнитура
P2-02 панорамные окна
P2-03 остекление балкона с выносом
P2-04 окна для частного дома
```

No seed substitution, duplicate input, terminal failure or outcome-unknown state occurred.

Source: owner-supplied `WORDSTAT_BATCH_RESULT_V1` returned by Yandex Marketing Bridge after the fourth provider item completed.
