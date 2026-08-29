# KW-001 / OKNO-MSK — Step 09 `nextN` live chunk validation

Date: 2026-08-29  
Status: **LIVE OPERATIONAL EVIDENCE / CORRECTION AUTHORITY**

## Correction

The live `nextN` chunk sizes were not unknown.

During the actual Step-09 Bridge rollout we explicitly tested the following `count` values live:

```text
4
10
25
31
```

Therefore the correct statement is:

```text
LIVE_NEXT_N_REQUESTED_COUNTS_TESTED = [4, 10, 25, 31]
LIVE_NEXT_N_MAX_REQUESTED_COUNT_TESTED = 31
```

This supersedes any earlier wording that said the exact live tested chunk sizes could not be stated.

## Important accounting distinction

The set of tested `count` values is not, by itself, a partition of the final R2 job total.

`nextN.count` means "attempt at most N sequential items". Actual confirmed provider executions for a call are governed by the returned:

```text
confirmed_provider_executions
provider_execution_count_exact
stopped_early
stop_reason
```

and by remaining work / policy / cost / terminal / UNKNOWN controls.

Therefore:

```text
TESTED_REQUESTED_COUNTS = [4, 10, 25, 31]
!=
A CLAIM THAT 4 + 10 + 25 + 31 IS THE COMPLETE R2 EXECUTION PARTITION
```

The authoritative final R2 job accounting remains:

```text
job_id = kw001-okno-msk-search-step09-20260829-r2
requests_started = 74
succeeded = 74
failed_terminal = 0
outcome_unknown = 0
estimated_cost_rub = 36.112
status = COMPLETED
```

Combined with the earlier legacy single-request canary:

```text
initial tranche provider requests = 75
successful = 75
failed_terminal = 0
outcome_unknown = 0
estimated cumulative cost = 36.600 RUB
```

## What the live test established

The live rollout validated increasing chunk sizes rather than jumping directly to the protocol ceiling:

```text
4 -> small live canary chunk
10 -> larger live chunk
25 -> larger bounded live chunk
31 -> largest explicitly tested live requested count
```

The hard protocol ceiling remains:

```text
1 <= count <= 100
```

But the largest explicitly live-tested requested size in this Step-09 run was:

```text
31
```

The local synthetic `count=100` test remains a different fact: it validates the bound/stop semantics, not a 100-request live Yandex chunk.

## Persistence failure attached to these tests

The exact command/result receipts for every live chunk were not durably written to the repository immediately after each returned chunk. That is the process defect recorded in:

`STEP_09_COLLECTION_METHOD_AND_IMMEDIATE_PERSISTENCE_POSTMORTEM_2026-08-29.md`

Because of that error, the project later had job-level/projection evidence for R2 completion, but not a complete durable command-by-command receipt ledger for every chunk.

This does **not** make the tested sizes unknown; it means their full per-command result receipts were not preserved when they should have been.

Correct future rule:

```text
NEXT_N_RESULT_RECEIVED
-> DURABLE_WRITE_COMMAND_AND_FULL_RESULT
-> READ_BACK_QA
-> ONLY THEN NEXT PAID CHUNK
```

## Canonical operational recommendation boundary

Evidence available from this live run supports:

```text
explicitly live-tested requested counts: 4, 10, 25, 31
largest live-tested requested count: 31
hard protocol ceiling: 100
```

Do not replace this with an invented "optimal" chunk size. Any operational default above 31 requires new live evidence; any default up to 31 must still respect result payload size, project immediate-persistence gating and provider/job policy controls.
