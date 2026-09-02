# Codex prompt — OKNO_MSK Step 14A Q1-Q4 crawler qualification

Execute ONLY the Step-14A crawler qualification and, only if all qualification gates pass, continue into the already-authorized canonical Step-14A full crawl.

Repository:
`MaksimUnimax/Yandex_direct`

Branch:
`roadmap/kwork-productization-2026-08-28`

Reported local state before this instruction:

```text
LOCAL_HEAD_AFTER_REMOTE_INTEGRATION = 4dce8e4c1cbc5495e2371b630603718c35a3f62f
RUNNER_CHECKPOINT_COMMIT = 7f0abb92f0007180923ce43d74670e32d3adc629
CRAWLER_SCRIPT_PATH = extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/step14a_codex_site_discovery.py
STEP15_EXECUTED = false
```

The remote branch has advanced since the last fetch. Fetch current authority again before qualification.

## Phase 0 — preserve local state and integrate latest remote rules

1. Record:

```bash
git status --short
git rev-parse HEAD
git branch --show-current
```

2. Preserve current runner/checkpoint history. Do not reset, force-push or discard it.

3. Fetch:

```bash
git fetch origin roadmap/kwork-productization-2026-08-28
git rev-parse origin/roadmap/kwork-productization-2026-08-28
```

4. Safely integrate the latest remote authority. Existing conflict-preservation rules remain active.

5. Read completely after integration:

```text
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/RULES_ARCHITECTURE_CODEX_EXECUTION_RELIABILITY_GATE_ADDENDUM_2026-09-02.md
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/STEP_14_CODEX_CRAWLER_EXECUTION_RELIABILITY_GATE.md
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14A_CODEX_RETRY4_CHECKPOINT_AND_QUALIFICATION_READY_2026-09-02.md
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14A_CODEX_PROMPT_2026-09-02.md
```

## Phase 1 — quarantine misleading old final-named artifacts

Before any Q1-Q4 test, inspect the worktree for the seven required final Step-14A artifact names:

```text
STEP_14A_CODEX_SITE_DISCOVERY_URLS.tsv
STEP_14A_CODEX_INTERNAL_LINK_GRAPH.tsv
STEP_14A_CODEX_PAGE_PROFILE_LEDGER.tsv
STEP_14A_CODEX_UPSTREAM_RECONCILIATION.tsv
STEP_14A_CODEX_REQUIRED_EDGE_VERIFICATION.tsv
STEP_14A_CODEX_QA.json
STEP_14A_CODEX_REPORT.md
```

If any exist from the previous unqualified run:

- do NOT commit them under final names;
- if they contain unique useful diagnostic information, move/rename them under explicit `DIAGNOSTIC_` or `STAGING_` provenance-bearing names;
- otherwise remove them from the worktree;
- record exact disposition;
- verify the final required names are clean/absent before qualification publication.

Record:

```text
STALE_FINAL_NAMED_ARTIFACTS_FOUND
STALE_FINAL_NAMED_ARTIFACT_DISPOSITION
FINAL_NAMES_CLEAN_BEFORE_QUALIFICATION = true/false
```

## Phase 2 — inspect runner before execution

Inspect the actual runner code. Do not assume the earlier TLS fix made it reliable.

Verify or implement explicit bounded controls for:

```text
run_id
phase
started_at
last_progress_at
per_request_timeout
bounded_retry_count
global_deadline/watchdog
max_pages for mini-crawl
max_sitemap_documents / max_sitemap_urls for sitemap probe
queue_count
attempted_count
completed_count
failed_or_indeterminate_count
latest_completed_url
terminal_state
terminal_reason
finished_at
```

Required invariant:

```text
EVERY RUN MUST TERMINATE AS SUCCESS OR BOUNDED FAILURE
SILENT INDEFINITE EXECUTION IS NOT ALLOWED
```

Diagnostic/Q1-Q4 outputs must not use final Step-14A filenames.

## Q1 — construction/static qualification

Without a full crawl:

1. compile/import runner successfully;
2. exercise argument parsing/configuration needed by Q2-Q4;
3. validate URL normalization on representative cases;
4. validate queue/dedupe primitives with finite in-memory cases;
5. validate terminal-state/output-finalization path using a no-network or mocked finite case if practical;
6. verify global deadline/max-page controls can be invoked.

Q1 PASS requires zero unhandled exception in these checks and proof that bounded controls are wired into the execution path.

Record:

```text
Q1_STATUS
Q1_TESTS_RUN
Q1_FAILURES
```

If Q1 FAIL: stop before network crawl, create diagnostic report, commit/push runner + tests + report.

## Q2 — one-page end-to-end qualification

Use the runner itself, not a separate ad-hoc HTTP snippet.

Target:
`https://okno-msk.ru/`

Bound it to exactly one fetched HTML page and a short global deadline.

It must demonstrate:

```text
request issued
response received or bounded failure recorded
HTTP/final URL recorded
HTML parsed
same-site literal <a href> values extracted
normalization executed
no recursive queue expansion beyond the one-page bound
terminal_state reached
process exits
```

Persist only diagnostic output.

Record:

```text
Q2_STATUS
Q2_RUN_ID
Q2_HTTP_STATUS
Q2_FINAL_URL
Q2_EXTRACTED_INTERNAL_HREF_COUNT
Q2_DURATION
Q2_TERMINAL_STATE
Q2_TERMINAL_REASON
```

If Q2 FAIL: stop, commit/push runner + diagnostics.

## Q3 — finite recursive mini-crawl

Run the actual recursive crawler from the homepage with an explicit small finite `max_pages` bound. Use 5 pages unless the current runner already has another documented bounded smoke-test value between 3 and 10.

Also enforce a short global deadline independent of per-request timeout.

Q3 must exercise:

```text
queue expansion
same-site filtering
normalization
deduplication
multiple fetches
href graph extraction
progress checkpoints
max_pages stop condition
terminal finalization
```

Q3 PASS requires:

```text
attempted <= configured max_pages
completed + failed_or_indeterminate = attempted
process exits
terminal_state is explicit
no infinite queue growth
no stale final-named artifacts published
```

Record:

```text
Q3_STATUS
Q3_RUN_ID
Q3_MAX_PAGES
Q3_ATTEMPTED
Q3_COMPLETED
Q3_FAILED_OR_INDETERMINATE
Q3_UNIQUE_URLS_SEEN
Q3_EDGE_COUNT
Q3_DURATION
Q3_TERMINAL_STATE
Q3_TERMINAL_REASON
```

If Q3 FAIL: stop, commit/push runner + diagnostics.

## Q4 — separately bounded sitemap probe

Do not combine this first proof with the full crawl.

Use the runner's sitemap logic with explicit bounds:

```text
max_sitemap_documents
max_sitemap_urls
global_deadline
```

Test conventional sitemap discovery and any sitemap index recursion only within those bounds.

Q4 PASS requires:

```text
probe terminates
parsed sitemap count recorded
URL count recorded
recursive/index behavior bounded
parse/fetch failures explicit
process exits
```

Record:

```text
Q4_STATUS
Q4_RUN_ID
Q4_SITEMAPS_ATTEMPTED
Q4_SITEMAPS_PARSED
Q4_URLS_DISCOVERED_WITHIN_PROBE_BOUND
Q4_FAILED_OR_INDETERMINATE
Q4_DURATION
Q4_TERMINAL_STATE
Q4_TERMINAL_REASON
```

If Q4 FAIL: stop, commit/push runner + diagnostics.

## Qualification decision

Only if:

```text
Q1_STATUS = PASS
Q2_STATUS = PASS
Q3_STATUS = PASS
Q4_STATUS = PASS
FINAL_NAMES_CLEAN_BEFORE_QUALIFICATION = true
```

set:

```text
FULL_CRAWL_ELIGIBLE = true
```

Otherwise:

```text
FULL_CRAWL_ELIGIBLE = false
```

Do not run the full crawl if false.

## If qualification FAILS

Create:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14A_CODEX_Q1_Q4_QUALIFICATION_REPORT_2026-09-02.md`

and a machine-readable diagnostic JSON with the same Q1-Q4 fields under a diagnostic filename.

Commit:
- runner code;
- tests/helpers;
- diagnostic Q1-Q4 outputs;
- qualification report;
- any preserved stale diagnostic artifacts under non-final provenance names.

Fetch latest remote, integrate safely, and NORMAL-PUSH.

No force push.

Then stop and report the pushed SHA.

## If qualification PASSES

First create the same qualification report/JSON showing PASS.

Then read and execute completely:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14A_CODEX_PROMPT_2026-09-02.md`

The full run must use a new `run_id` and must publish the seven final Step-14A files only after terminal success + QA.

After full execution, commit and NORMAL-PUSH all intended runner, qualification and final evidence.

Do not execute Step 15.

## Final response fields

Always report:

```text
LOCAL_HEAD_QUALIFICATION_START
REMOTE_HEAD_AFTER_FETCH_QUALIFICATION
SYNC_MODE_QUALIFICATION
LOCAL_HEAD_AFTER_SYNC_QUALIFICATION
CRAWLER_SCRIPT_PATH
STALE_FINAL_NAMED_ARTIFACTS_FOUND
STALE_FINAL_NAMED_ARTIFACT_DISPOSITION
FINAL_NAMES_CLEAN_BEFORE_QUALIFICATION

Q1_STATUS
Q1_TESTS_RUN
Q1_FAILURES

Q2_STATUS
Q2_RUN_ID
Q2_HTTP_STATUS
Q2_FINAL_URL
Q2_EXTRACTED_INTERNAL_HREF_COUNT
Q2_DURATION
Q2_TERMINAL_STATE
Q2_TERMINAL_REASON

Q3_STATUS
Q3_RUN_ID
Q3_MAX_PAGES
Q3_ATTEMPTED
Q3_COMPLETED
Q3_FAILED_OR_INDETERMINATE
Q3_UNIQUE_URLS_SEEN
Q3_EDGE_COUNT
Q3_DURATION
Q3_TERMINAL_STATE
Q3_TERMINAL_REASON

Q4_STATUS
Q4_RUN_ID
Q4_SITEMAPS_ATTEMPTED
Q4_SITEMAPS_PARSED
Q4_URLS_DISCOVERED_WITHIN_PROBE_BOUND
Q4_FAILED_OR_INDETERMINATE
Q4_DURATION
Q4_TERMINAL_STATE
Q4_TERMINAL_REASON

FULL_CRAWL_ELIGIBLE
QUALIFICATION_COMMIT_SHA
```

Also report:

```text
FINAL_COMMIT_SHA
PUSH_STATUS
STEP15_EXECUTED = false
```

If the full crawl runs, additionally report the canonical Step-14A counts and 15-edge accounting required by `STEP_14A_CODEX_PROMPT_2026-09-02.md`.

Do not claim final Step-14 acceptance. ChatGPT performs readback and semantic reconciliation after the push.
