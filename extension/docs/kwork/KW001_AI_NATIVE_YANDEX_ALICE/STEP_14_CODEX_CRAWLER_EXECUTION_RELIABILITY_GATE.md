# KW-001 — Step 14 Codex crawler execution reliability gate

Date: 2026-09-02  
Status: **ACTIVE / STEP-14-SPECIFIC / OWNER-REQUIRED**  
Stage: Step 14 / Step 14A deterministic current-site discovery and topology correction

## Why this Step-14 rule exists

Step 14 now correctly requires deterministic current-site discovery and literal HTML topology before a completeness/topology-dependent PASS. That stronger requirement introduced a new execution surface: the crawler itself must be demonstrably executable.

The OKNO_MSK Step-14A retry reached repository synchronization successfully but then exposed a runner reliability defect.

Observed sequence reported by Codex:

```text
SAFE_MERGE_WITH_EVIDENCE_PRESERVATION = complete
MANDATORY_FILES_PRESENT_AFTER_SYNC = 16/16
crawler runner added locally
first runner attempt = failed before fetch because of TLS/opener argument bug
TLS/opener bug corrected
isolated diagnostic request to https://okno-msk.ru/ = HTTP 200 HTML
subsequent bounded runner attempts = no completion and no terminal error stream
required Step-14A output artifacts = not updated
Step-14A acceptance claim = withheld
Step15 = not executed
```

The safe decision to withhold PASS was correct.

The missing method element was an explicit execution-reliability ladder before the full crawl.

---

# 1. The reasoning error this control prevents

The dangerous inference is:

```text
one HTTPS request works
-> site is reachable
-> crawler should work
-> rerun broader crawl
```

Only the first implication is valid.

A crawler contains additional independent failure surfaces:

```text
HTTP client construction;
HTML parser;
href extraction;
URL normalization;
queue expansion;
deduplication;
redirect handling;
sitemap recursion;
per-request retry behaviour;
progress/output writes;
terminal finalization;
QA publication.
```

Therefore:

```text
SITE_HTTP_200
!= RUNNER_TERMINATION_PROOF
!= FULL_CRAWL_COMPLETENESS
```

Step 14 depends on enumeration/topology evidence, so a silent or non-terminating runner cannot satisfy the gate even when the public site is healthy.

---

# 2. Why the first Step-14A retry design was still insufficient

Earlier corrections focused on three real problems:

1. known-page reread was not complete site discovery;
2. endpoint liveness was not literal link proof;
3. stale/diverged Codex repository state could invalidate read-first authority.

Those were necessary corrections, but the execution prompt then moved from "repository is valid" directly to "run the complete crawler".

It did not require the crawler to earn trust in progressively larger finite stages.

That left a gap:

```text
CORRECT CURRENT AUTHORITY
+ CORRECT CRAWLER DESIGN INTENT
!= CRAWLER EXECUTION PROVEN
```

The first TLS/opener construction bug demonstrated this immediately. Correcting that bug and obtaining an isolated 200 then proved only one layer of the stack.

The later silent bounded run showed that some later layer still lacked a demonstrated terminal path.

The permanent lesson is:

```text
A NEW OR MATERIALLY CHANGED EVIDENCE RUNNER MUST PROVE TERMINATION ON A SMALL FINITE CASE BEFORE IT IS TRUSTED AT SITE SCALE.
```

---

# 3. Mandatory Step-14A runner qualification ladder

No full Step-14A crawl may start until each applicable earlier stage passes.

## Q1 — runner construction / deterministic unit smoke

Must validate, at minimum:

```text
runner imports/starts;
HTTP client/opener construction succeeds;
URL normalization/same-site logic terminates on fixed samples;
explicit bounds/config parse successfully;
controlled failure produces a terminal state.
```

The observed TLS/opener argument bug must be guarded by a regression check in the runner/test surface when practical.

Failure:

```text
STEP14A_RUNNER_QUALIFICATION = BLOCKED_Q1
```

## Q2 — exact one-page live fetch+parse+exit

Run against one known public HTML page only, with recursion disabled or `max_pages=1` equivalent.

Required proof:

```text
fetch attempted;
fetch terminal state recorded;
HTTP/content state recorded;
HTML parser returned;
internal href extraction returned;
runner exited within configured bounds;
diagnostic output belongs to the current run.
```

An isolated ad hoc HTTP request outside the runner is useful diagnosis but does not substitute for Q2.

Failure:

```text
STEP14A_RUNNER_QUALIFICATION = BLOCKED_Q2
```

## Q3 — finite mini-crawl

Run a deliberately small explicit bound sufficient to exercise actual queue expansion, for example an implementation-chosen small page bound.

It must demonstrate:

```text
queue adds children;
queue dequeues them;
deduplication works;
relative links normalize;
multiple pages complete;
page/profile data writes;
edge data writes;
progress state updates;
runner reaches normal terminal completion.
```

The precise small page count is implementation-defined; the key is that it is explicitly finite and large enough to exercise recursion.

Failure:

```text
STEP14A_RUNNER_QUALIFICATION = BLOCKED_Q3
```

## Q4 — sitemap probe

Test sitemap discovery/parsing under its own explicit bounds and terminal reporting.

This is separate because sitemap index recursion or URL volume may fail differently from normal HTML crawl.

Failure:

```text
STEP14A_RUNNER_QUALIFICATION = BLOCKED_Q4
```

## Q5 — full Step-14A crawl

Only after Q1-Q4 pass may the full current-site discovery/topology run execute.

---

# 4. Required observability for Step 14A

The runner must produce a current-run diagnostic/checkpoint state with at least equivalent fields:

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
latest_completed_url or equivalent progress cursor
current_output_stage
terminal_state
terminal_reason
finished_at
```

The purpose is to answer:

```text
DID THE PROCESS STOP MAKING PROGRESS?
IF YES, AT WHICH PHASE / COUNTER / URL CLASS?
```

without guessing from the absence of console output.

Canonical Step-14 rule:

```text
NO TERMINAL STATE + NO OBSERVABLE PROGRESS
-> CRAWL RESULT = INVALID / BLOCKED
```

---

# 5. Step-14A output publication discipline

Required final artifacts such as:

```text
STEP_14A_CODEX_SITE_DISCOVERY_URLS.tsv
STEP_14A_CODEX_INTERNAL_LINK_GRAPH.tsv
STEP_14A_CODEX_PAGE_PROFILE_LEDGER.tsv
STEP_14A_CODEX_UPSTREAM_RECONCILIATION.tsv
STEP_14A_CODEX_REQUIRED_EDGE_VERIFICATION.tsv
STEP_14A_CODEX_QA.json
STEP_14A_CODEX_REPORT.md
```

must not be overwritten with incomplete diagnostic data and must not be accepted merely because old versions exist.

Use equivalent separation:

```text
diagnostic/checkpoint/staging outputs
-> terminal success
-> QA
-> publish required final artifact set
```

The final QA/report must identify the `run_id` or equivalent identity of the successful crawl that produced them.

---

# 6. How Codex should diagnose the current OKNO_MSK failure

Because an isolated homepage request returned HTTP 200 HTML, the next run must not begin by repeatedly testing general internet availability.

Instead inspect the local runner already created by Codex and find the smallest execution stage that does not terminate.

Recommended diagnostic sequence:

```text
1. preserve current local runner changes and repository sync merge;
2. inspect runner code and current git diff/status;
3. reproduce Q1;
4. reproduce Q2 through the runner itself, not a separate ad hoc client;
5. reproduce Q3 with a tiny explicit page bound and heartbeat/checkpoint output;
6. test Q4 sitemap path separately;
7. only after all four pass, run Q5 full crawl.
```

If Q2 passes but Q3 stalls, inspect queue/dedup/redirect/parser/output transitions before touching sitemap logic.

If Q3 passes but Q4 stalls, isolate sitemap traversal.

If Q1-Q4 pass but Q5 stalls, the progress/checkpoint state must identify the last completed phase/frontier rather than returning a silent non-result.

Do not change semantic Step-14 ownership/architecture while debugging the runner.

---

# 7. Repository/push policy for the current local Codex state

The reported local synchronized merge is:

```text
LOCAL_HEAD_AFTER_SYNC = 4675ccd18fa3ac4b12bcbc8ff8191a7220ee01a6
SYNC_MODE = SAFE_MERGE_WITH_EVIDENCE_PRESERVATION
MANDATORY_FILES_PRESENT_AFTER_SYNC = 16/16
```

That merge is not yet on canonical remote GitHub.

The runner/fix work also exists only locally unless Codex proves otherwise.

Therefore the next Codex run must:

```text
preserve the synchronized merge and local runner work;
fetch latest remote before any push;
never force-push;
commit durable runner/tests/diagnostics only when coherent;
normal-push the final accepted synchronization + runner + Step14A evidence;
```

If execution remains blocked after a reproducible qualification stage, Codex should still persist a bounded diagnostic report and runner/test improvements and normal-push them if safe, so ChatGPT can inspect the actual code rather than relying only on chat text.

---

# 8. Pass gate added to Step 14

Before `CODEX_RUN_EXECUTED = true` may support Step-14 acceptance:

```text
STEP14A_RUNNER_Q1 = PASS
STEP14A_RUNNER_Q2 = PASS
STEP14A_RUNNER_Q3 = PASS
STEP14A_RUNNER_Q4 = PASS
STEP14A_RUNNER_TERMINAL_STATE_OBSERVABLE = true
STEP14A_CURRENT_RUN_OUTPUT_ATTRIBUTION = true
```

Then and only then:

```text
STEP14A_FULL_CRAWL_ELIGIBLE = true
```

After full crawl:

```text
FULL_RUN_TERMINAL_SUCCESS = true
REQUIRED_ARTIFACTS_PUBLISHED_FROM_CURRENT_RUN = true
DETERMINISTIC_QA = PASS
```

Only then may ChatGPT perform semantic reconciliation and reconsider final Step-14 acceptance.

---

# 9. Non-repeat markers

```text
STEP14_HTTP_200_NOT_EQUAL_RUNNER_RELIABLE = true
STEP14_NEW_CRAWLER_REQUIRES_QUALIFICATION_LADDER = true
STEP14_ONE_PAGE_RUNNER_SMOKE_REQUIRED = true
STEP14_BOUNDED_MINI_CRAWL_REQUIRED = true
STEP14_SITEMAP_PROBE_REQUIRED = true
STEP14_PROGRESS_CHECKPOINT_REQUIRED = true
STEP14_TERMINAL_STATE_REQUIRED = true
STEP14_STALE_OUTPUT_REJECTED = true
STEP14_FULL_CRAWL_BLOCKED_UNTIL_Q1_Q4_PASS = true
```
