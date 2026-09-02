# KW-001 — Codex deterministic execution reliability gate addendum

Date: 2026-09-02  
Status: **ACTIVE / UNIVERSAL PROCESS ADDENDUM / OWNER-APPROVED / OWNER-LOCKED**

## Purpose

A deterministic crawler or evidence runner is useful only if the process can be shown to terminate, expose progress, classify failure, and produce outputs attributable to the current run.

A successful isolated network request does not prove that the full crawler is executable.

Canonical non-equivalences:

```text
SINGLE_REQUEST_HTTP_200 != CRAWLER_EXECUTION_RELIABLE
RUNNER_STARTED != RUNNER_COMPLETED
NO_ERROR_STREAM != SUCCESS
PROCESS_STILL_SILENT != PROCESS_HEALTHY
OLD_OUTPUT_FILE_PRESENT != CURRENT_RUN_OUTPUT_PRODUCED
```

This rule was added after the OKNO_MSK Step-14A Codex execution on 2026-09-02. The runner initially failed before fetching because of a TLS/opener argument bug. After that bug was corrected, isolated public HTTPS access to the homepage returned HTTP 200 HTML, but subsequent bounded crawler runs produced neither a completion nor a terminal error stream and did not update the required output artifacts. The correct response was to withhold Step-14A PASS.

The lesson is causal: network reachability had been tested, but crawler termination/reliability had not.

---

# 1. What the failure proved and did not prove

The isolated diagnostic proved only:

```text
PUBLIC_SITE_TLS_HTTP_REACHABILITY = AVAILABLE for the tested request
```

It did not prove:

```text
crawl queue terminates;
URL deduplication terminates;
sitemap traversal terminates;
redirect handling terminates;
HTML parsing terminates;
all per-request timeouts are bounded;
output finalization executes;
required artifacts belong to the current run.
```

Therefore the correct failure classification is an execution-reliability blocker, not a site-unavailable blocker and not a successful crawl.

---

# 2. Mandatory staged execution before a full deterministic crawl

When a new or materially changed Codex crawler/runner is required for acceptance, the following stages are mandatory.

## Stage A — static / construction smoke

Before public requests:

- import/instantiate the runner and HTTP client/opener path;
- exercise URL normalization and same-site classification on fixed examples;
- exercise queue/deduplication termination on a tiny synthetic graph when practical;
- verify CLI/config parsing for explicit bounds;
- verify the runner can produce a terminal state and diagnostics even on controlled failure.

A previously observed construction bug, such as the Step-14A TLS/opener argument failure, must receive a regression check when practical.

## Stage B — one-page live smoke

Fetch exactly one known public HTML page with explicit timeout and no recursive expansion.

Required evidence:

```text
request attempted;
terminal status recorded;
HTTP/fetch state recorded;
content type recorded;
HTML parse completed;
internal href extraction completed;
process exited cleanly within the configured bound.
```

`HTTP 200` without parser/termination evidence is insufficient.

## Stage C — bounded mini-crawl

Run a deliberately small crawl, normally a small fixed `max_pages` / equivalent bound, sufficient to exercise:

```text
queue expansion;
deduplication;
relative/absolute href handling;
redirect/final URL handling;
page ledger write;
link-graph write;
progress/checkpoint emission;
normal terminal completion.
```

The exact page count is implementation-specific, but the bound must be small and explicit.

A full-site crawl is blocked until the mini-crawl reaches a clean terminal state.

## Stage D — sitemap probe

Sitemap discovery/parsing must be tested separately enough to distinguish sitemap problems from normal HTML crawl problems.

A pathological sitemap or sitemap index must not be allowed to create an unbounded run.

## Stage E — full crawl

Only after Stages A-D pass may the full deterministic crawl run.

---

# 3. Observability is part of correctness

A crawler used as acceptance evidence must expose enough state to diagnose a stall without guessing.

At minimum the runner must make observable:

```text
run_id;
start timestamp;
current phase;
URLs queued;
URLs dequeued/attempted;
URLs completed;
URLs failed/indeterminate;
current URL or latest completed URL where safe;
last progress timestamp;
configured page/time bounds;
terminal state;
terminal reason.
```

Progress may be written to stdout/stderr, a dedicated diagnostic/checkpoint file, or both.

Required principle:

```text
SILENT_LONG_RUNNING_PROCESS_WITHOUT_HEARTBEAT
!=
ACCEPTABLE DETERMINISTIC EVIDENCE RUN
```

The exact progress interval may be implementation-specific, but it must be frequent enough to distinguish active progress from a stall.

---

# 4. Hard bounds and termination

Every network request must have an explicit timeout.

The overall run must also have a bounded completion policy so a stalled queue/parser/finalizer cannot wait indefinitely.

At minimum support equivalent controls for:

```text
per-request timeout;
bounded retries;
maximum pages or equivalent discovery safety bound for smoke/diagnostic modes;
overall wall-clock deadline or watchdog;
maximum redirect handling;
finite sitemap traversal / deduplication.
```

If a full production crawl intentionally has no low `max_pages`, it still requires a global safety/termination mechanism and deduplicated finite URL frontier.

A deadline hit must produce an explicit bounded state such as:

```text
TIMEOUT_BLOCKED
```

not a silent disappearance.

---

# 5. Output attribution and stale-output protection

Required acceptance artifacts must not be mistaken for outputs of the current run merely because files already exist.

Each run must make it possible to prove output attribution using equivalent evidence such as:

```text
run_id;
started_at;
finished_at;
input/config identity;
output row counts;
current-run file update/write evidence;
terminal status.
```

Recommended execution discipline:

```text
CURRENT RUN writes temporary/staging outputs
-> current run reaches terminal success
-> deterministic QA passes
-> atomically/prominently publish required final artifacts
```

A failed or incomplete diagnostic run must not overwrite previously accepted required artifacts with partial data.

Canonical rule:

```text
OUTPUT_FILE_EXISTS != CURRENT_RUN_SUCCESS
```

---

# 6. Failure isolation

When a full runner stalls but an isolated page request succeeds, do not immediately blame the site or retry the full run blindly.

Isolate the failing layer in this order or an equivalently diagnostic order:

```text
HTTP client construction/TLS
-> single fetch
-> HTML parse
-> href extraction/normalization
-> queue/deduplication
-> bounded multi-page crawl
-> sitemap parsing
-> output/checkpoint writing
-> finalization/QA
```

The goal is to identify the smallest stage that fails to reach a terminal state.

Do not change multiple unrelated layers at once unless evidence requires it.

---

# 7. Fail-closed policy

A deterministic evidence run cannot be accepted when:

```text
runner has no terminal state;
mini-crawl does not terminate;
progress cannot distinguish work from stall;
required outputs are unchanged/stale;
current-run output attribution is missing;
material timeout/fetch failures are silently dropped;
full crawl is launched before the executable smoke gate passes.
```

Then:

```text
DETERMINISTIC_EXECUTION_RELIABILITY = FAIL_OR_BLOCKED
STEP_ACCEPTANCE = BLOCKED
```

Do not substitute manual evidence and call it equivalent when the step specifically requires deterministic site-scale enumeration/topology.

---

# 8. Separation of concerns

```text
NETWORK_REACHABILITY
!= RUNNER_EXECUTABILITY
!= CRAWL_COMPLETENESS
!= SEMANTIC_CORRECTNESS
```

Each requires its own evidence.

Codex/code owns deterministic execution and mechanical evidence.
ChatGPT owns semantic interpretation and final analytical reconciliation.
The owner controls authorization and scope.

---

# 9. Non-repeat lesson

The OKNO_MSK Step-14A failure chain was:

```text
new runner created
-> first run exposed TLS/opener construction bug
-> bug corrected
-> isolated site request returned HTTP 200 HTML
-> broader bounded runner started
-> no terminal completion/error stream
-> required output artifacts not updated
```

The mistaken shortcut to prevent is:

```text
ISOLATED REQUEST WORKS
-> THEREFORE FULL CRAWLER SHOULD WORK
-> RETRY FULL CRAWL
```

The corrected chain is:

```text
construction/static smoke
-> one-page fetch+parse+exit
-> bounded mini-crawl+outputs+exit
-> sitemap probe
-> full crawl with heartbeat/checkpoints/deadline
-> deterministic QA
-> final artifact publication
```

The purpose is not extra ceremony. Each stage tests a different failure surface and narrows the cause before expensive or opaque site-scale execution.

---

Markers:

```text
KW001_CODEX_EXECUTION_RELIABILITY_GATE_ACTIVE = true
KW001_SINGLE_HTTP_200_NOT_EQUAL_CRAWLER_RELIABLE = true
KW001_NEW_OR_CHANGED_CRAWLER_REQUIRES_STAGED_SMOKE = true
KW001_BOUNDED_MINI_CRAWL_REQUIRED_BEFORE_FULL_RUN = true
KW001_CRAWLER_PROGRESS_HEARTBEAT_REQUIRED = true
KW001_CRAWLER_TERMINAL_STATE_REQUIRED = true
KW001_CRAWLER_GLOBAL_SAFETY_BOUND_REQUIRED = true
KW001_CURRENT_RUN_OUTPUT_ATTRIBUTION_REQUIRED = true
KW001_STALE_OUTPUT_NOT_ACCEPTABLE_AS_CURRENT_EVIDENCE = true
KW001_FAILED_DIAGNOSTIC_MUST_NOT_PUBLISH_PARTIAL_FINAL_ARTIFACTS = true
```
