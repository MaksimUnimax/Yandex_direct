# KW-001 — Codex deterministic execution reliability gate addendum

Date: 2026-09-02  
Updated: 2026-09-03  
Status: **ACTIVE / UNIVERSAL PROCESS ADDENDUM / OWNER-APPROVED / OWNER-LOCKED**

## Purpose

A deterministic crawler or evidence runner is useful only if the process can be shown to terminate, expose progress, classify failure, and produce outputs attributable to the current run.

A successful isolated network request does not prove that the full runner is executable.

Canonical non-equivalences:

```text
SINGLE_REQUEST_HTTP_200 != RUNNER_EXECUTION_RELIABLE
RUNNER_STARTED != RUNNER_COMPLETED
NO_ERROR_STREAM != SUCCESS
PROCESS_STILL_SILENT != PROCESS_HEALTHY
OLD_OUTPUT_FILE_PRESENT != CURRENT_RUN_OUTPUT_PRODUCED
```

## Why this rule exists

A prior controlled execution exposed the following reusable failure class: an evidence runner first failed during client construction, later passed an isolated live request, but a broader bounded run did not reach a terminal state or update the required outputs. Withholding analytical PASS was correct.

### Root cause

```text
NETWORK REACHABILITY
WAS TREATED AS A PROXY FOR
FULL RUNNER TERMINATION / RELIABILITY
```

The missing control was a staged qualification ladder that proves each independent execution surface before site-scale or corpus-scale work.

Concrete domains, timestamps, commit IDs, URLs and run results belong in Level-2 incident evidence and are not part of this universal rule.

---

## 1. What an isolated successful request proves

It may prove only the bounded network/fetch fact that was actually tested.

It does not prove:

```text
queue termination;
URL/item deduplication termination;
recursive discovery termination;
redirect handling termination;
parser termination;
per-request bounds;
output finalization;
required artifacts belong to the current run.
```

Therefore a broader non-terminating execution is an execution-reliability blocker, not proof that the source is unavailable and not a successful collection.

---

## 2. Mandatory staged qualification before a full deterministic run

When a new or materially changed deterministic runner is required for acceptance, qualify applicable stages in order.

### Q1 — construction/static smoke

Before production requests:

```text
runner imports/starts;
client/opener construction succeeds;
normalization/scope classification terminates on fixed examples;
explicit bounds/config parse successfully;
controlled failure produces an observable terminal state.
```

Known implementation bugs should receive regression checks when practical.

### Q2 — one-item live fetch/parse/exit

Run exactly one known bounded item with recursion disabled or equivalent one-item configuration.

Required evidence:

```text
attempt recorded;
terminal fetch state recorded;
content/protocol state recorded;
parser returned;
extraction returned;
runner exited within configured bounds;
diagnostic output belongs to current run.
```

An ad hoc request outside the runner does not substitute for Q2.

### Q3 — finite mini-run

Run a deliberately small explicit bound sufficient to exercise real iteration/queue expansion.

It must demonstrate, where applicable:

```text
queue/input expansion;
deduplication;
normalization;
multiple item completion;
profile/data writes;
edge/relation writes;
progress/checkpoint updates;
normal terminal completion.
```

The exact item count is implementation-defined. It must be finite and large enough to exercise the recursion/iteration path.

### Q4 — alternate discovery/source probe

If the full runner has a materially different acquisition path such as sitemap recursion, archive traversal, pagination or secondary indexes, test that path separately under explicit bounds.

### Q5 — full run

Only after Q1-Q4 pass may the full deterministic evidence run execute.

---

## 3. Observability is part of correctness

A runner used as acceptance evidence must expose enough state to diagnose a stall without guessing.

At minimum preserve equivalent fields:

```text
run_id
phase
started_at
last_progress_at
configured_request_timeout
configured_retry_bound
configured_item_bound_if_any
configured_global_deadline
queued_or_planned_count
attempted_count
completed_count
failed_or_indeterminate_count
latest_completed_item_or_cursor
current_output_stage
terminal_state
terminal_reason
finished_at
```

Canonical rule:

```text
NO TERMINAL STATE + NO OBSERVABLE PROGRESS
-> RESULT = INVALID / BLOCKED
```

---

## 4. Hard bounds and termination

Every external request must have an explicit timeout.

The overall run must have a bounded completion policy so a stalled queue/parser/finalizer cannot wait indefinitely.

Use equivalent controls for applicable surfaces:

```text
per-request timeout;
bounded retries;
maximum items/pages for diagnostic modes;
overall deadline/watchdog;
maximum redirects;
finite recursion/deduplicated frontier.
```

A deadline hit must produce a terminal bounded state such as `TIMEOUT_BLOCKED`, not silence.

---

## 5. Output attribution and stale-output protection

Required artifacts cannot be accepted merely because files already exist.

Each run must make output attribution possible through equivalent evidence such as:

```text
run_id
started_at
finished_at
input/config identity
output counts
current-run write/update evidence
terminal status
```

Preferred discipline:

```text
CURRENT RUN -> STAGING OUTPUTS
-> TERMINAL SUCCESS
-> DETERMINISTIC QA
-> PUBLISH FINAL REQUIRED ARTIFACTS
```

A failed diagnostic run must not overwrite previously accepted final artifacts with partial data.

```text
OUTPUT_FILE_EXISTS != CURRENT_RUN_SUCCESS
```

---

## 6. Failure isolation

When a broad run stalls but a bounded request succeeds, identify the smallest failing layer instead of blindly replaying the full run.

Example diagnostic order:

```text
client construction/network
-> one fetch
-> parse
-> extraction/normalization
-> queue/deduplication
-> bounded multi-item execution
-> alternate discovery source
-> output/checkpoint write
-> finalization/QA
```

Do not change multiple unrelated layers at once unless evidence requires it.

---

## 7. Fail-closed policy

A deterministic evidence run cannot be accepted when:

```text
runner has no terminal state;
mini-run does not terminate;
progress cannot distinguish work from stall;
required outputs are unchanged/stale;
current-run attribution is missing;
material timeout/fetch failures are silently dropped;
full run started before applicable qualification stages passed.
```

Then:

```text
DETERMINISTIC_EXECUTION_RELIABILITY = FAIL_OR_BLOCKED
STEP_ACCEPTANCE = BLOCKED
```

Do not substitute a weaker manual collection method and claim equivalent completeness when the step explicitly requires deterministic enumeration.

---

## 8. Separation of concerns

```text
NETWORK_REACHABILITY
!= RUNNER_EXECUTABILITY
!= COLLECTION_COMPLETENESS
!= SEMANTIC_CORRECTNESS
```

Each requires its own evidence.

---

## 9. Permanent non-repeat chain

The shortcut to prevent is:

```text
ISOLATED REQUEST WORKS
-> ASSUME FULL RUNNER WORKS
-> REPLAY BROAD RUN
```

The corrected chain is:

```text
construction/static smoke
-> one-item fetch+parse+exit
-> bounded mini-run+outputs+exit
-> alternate-source probe when applicable
-> full run with heartbeat/checkpoints/deadline
-> deterministic QA
-> final artifact publication
```

Each stage tests a different failure surface and narrows the cause before expensive/opaque execution.

This rule follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.

## Markers

```text
KW001_CODEX_EXECUTION_RELIABILITY_GATE_ACTIVE = true
KW001_SINGLE_HTTP_200_NOT_EQUAL_RUNNER_RELIABLE = true
KW001_NEW_OR_CHANGED_RUNNER_REQUIRES_STAGED_SMOKE = true
KW001_BOUNDED_MINI_RUN_REQUIRED_BEFORE_FULL_RUN = true
KW001_RUNNER_PROGRESS_HEARTBEAT_REQUIRED = true
KW001_RUNNER_TERMINAL_STATE_REQUIRED = true
KW001_RUNNER_GLOBAL_SAFETY_BOUND_REQUIRED = true
KW001_CURRENT_RUN_OUTPUT_ATTRIBUTION_REQUIRED = true
KW001_STALE_OUTPUT_NOT_ACCEPTABLE_AS_CURRENT_EVIDENCE = true
KW001_FAILED_DIAGNOSTIC_MUST_NOT_PUBLISH_PARTIAL_FINAL_ARTIFACTS = true
```
