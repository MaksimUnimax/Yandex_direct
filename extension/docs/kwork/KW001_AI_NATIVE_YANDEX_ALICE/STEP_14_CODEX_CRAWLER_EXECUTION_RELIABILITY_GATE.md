# KW-001 — Step 14 deterministic runner execution reliability gate

Date: 2026-09-02  
Updated: 2026-09-03  
Status: **ACTIVE / STEP-14-SPECIFIC / UNIVERSAL / OWNER-REQUIRED**

This Step-14 gate applies the universal deterministic execution-reliability rules from `RULES_ARCHITECTURE_CODEX_EXECUTION_RELIABILITY_GATE_ADDENDUM_2026-09-02.md` to any current-site discovery/topology runner used as acceptance evidence.

## Why this Step-14 rule exists

Once Step14 requires deterministic current-site discovery or topology evidence, the collector itself becomes part of evidence validity. A runner that starts but cannot demonstrate bounded progress and terminal completion cannot satisfy a completeness/topology gate.

### Failure class

A prior controlled execution proved only isolated source reachability and then attempted a broader runner whose later execution surface had not been qualified.

### Root cause

```text
SOURCE REACHABILITY
+ RUNNER DESIGN INTENT
WAS TREATED AS
RUNNER EXECUTION PROVEN
```

The correct control is staged qualification. Concrete domains, URLs, exact failures, counts, commits and local-run state remain Level-2 incident evidence.

## Mandatory Step14 qualification ladder

No full Step14 deterministic collection run may start until each applicable earlier stage passes.

### Q1 — construction/static smoke

Verify:

```text
runner imports/starts;
client construction succeeds;
normalization/same-site logic terminates on fixed samples;
explicit bounds/config parse;
controlled failure reaches a terminal state.
```

### Q2 — exact one-page live fetch + parse + exit

Run one known public HTML page with recursion disabled or equivalent single-item bound.

Required proof:

```text
fetch attempted;
terminal fetch state recorded;
HTTP/content state recorded;
HTML parser returned;
internal href extraction returned;
runner exited within configured bounds;
output belongs to current run.
```

An isolated ad hoc request outside the runner is diagnostic only and does not substitute for Q2.

### Q3 — finite mini-crawl

Use a deliberately small explicit page bound sufficient to exercise real queue expansion.

Prove:

```text
queue adds/dequeues children;
deduplication works;
URLs normalize;
multiple pages complete;
page/profile data writes;
edge data writes;
progress state updates;
runner reaches normal terminal completion.
```

### Q4 — alternate discovery probe

Test materially different discovery logic such as sitemap parsing separately under explicit bounds.

### Q5 — full current-site run

Only after Q1-Q4 pass may the full current-site discovery/topology run execute.

## Required observability

Preserve equivalent fields:

```text
run_id
phase
started_at
last_progress_at
configured_request_timeout
configured_retry_bound
configured_page_bound_if_any
configured_global_deadline
queued_count
attempted_count
completed_count
failed_or_indeterminate_count
latest_completed_url_or_cursor
current_output_stage
terminal_state
terminal_reason
finished_at
```

```text
NO TERMINAL STATE + NO OBSERVABLE PROGRESS
-> CURRENT RUN RESULT = INVALID / BLOCKED
```

## Output publication discipline

Do not overwrite accepted final artifacts with incomplete diagnostic data.

```text
DIAGNOSTIC/STAGING OUTPUTS
-> TERMINAL SUCCESS
-> DETERMINISTIC QA
-> PUBLISH REQUIRED FINAL ARTIFACTS
```

Every accepted final artifact set must identify the successful `run_id` or equivalent current-run identity that produced it.

## Failure isolation

When a broad run fails, diagnose the smallest failing stage:

```text
construction/network
-> one-page runner execution
-> parse/extraction
-> queue/deduplication
-> mini-crawl
-> alternate discovery source
-> output/checkpoint write
-> finalization/QA
```

Do not replay a full collection merely because one earlier layer works.

## Pass gate

Before a deterministic Step14 run can support acceptance:

```text
STEP14_RUNNER_Q1 = PASS
STEP14_RUNNER_Q2 = PASS
STEP14_RUNNER_Q3 = PASS
STEP14_RUNNER_Q4 = PASS when applicable
STEP14_RUNNER_TERMINAL_STATE_OBSERVABLE = true
STEP14_CURRENT_RUN_OUTPUT_ATTRIBUTION = true
```

After full run:

```text
FULL_RUN_TERMINAL_SUCCESS = true
REQUIRED_ARTIFACTS_PUBLISHED_FROM_CURRENT_RUN = true
DETERMINISTIC_QA = PASS
```

Only then may semantic reconciliation and final Step14 acceptance proceed.

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.

## Markers

```text
STEP14_HTTP_SUCCESS_NOT_EQUAL_RUNNER_RELIABLE = true
STEP14_NEW_OR_CHANGED_RUNNER_REQUIRES_QUALIFICATION_LADDER = true
STEP14_ONE_PAGE_RUNNER_SMOKE_REQUIRED = true
STEP14_BOUNDED_MINI_CRAWL_REQUIRED = true
STEP14_ALTERNATE_DISCOVERY_PROBE_REQUIRED_WHEN_APPLICABLE = true
STEP14_PROGRESS_CHECKPOINT_REQUIRED = true
STEP14_TERMINAL_STATE_REQUIRED = true
STEP14_STALE_OUTPUT_REJECTED = true
STEP14_FULL_RUN_BLOCKED_UNTIL_QUALIFICATION_PASS = true
```
