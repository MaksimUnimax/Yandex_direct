# Retry prompt — OKNO_MSK Step 14A crawler execution reliability

Use this as the next Codex instruction. It supersedes only the execution/reliability portion of the previous retry. Repository/evidence preservation rules remain active. The task is still ONLY Step 14A.

---

You are continuing the OKNO_MSK Step-14A correction in repository:

`MaksimUnimax/Yandex_direct`

Branch:

`roadmap/kwork-productization-2026-08-28`

Your last reported synchronized local state was:

```text
LOCAL_HEAD_BEFORE_SYNC = bd5766a6498577176aaf8d0210a80c670cde4c39
REMOTE_HEAD_AFTER_FETCH_RETRY3 = 148780ef5dc88f4d2daca21fdfaa70b64bc33cc2
LOCAL_REMOTE_RELATIONSHIP = DIVERGED
LOCAL_BACKUP_REF = codex/backup-step14a-pre-sync-20260902
SYNC_MODE = SAFE_MERGE_WITH_EVIDENCE_PRESERVATION
LOCAL_HEAD_AFTER_SYNC = 4675ccd18fa3ac4b12bcbc8ff8191a7220ee01a6
CONFLICT_COUNT = 1
CONFLICT_CLASSIFICATIONS = EVIDENCE_PRESERVATION_CONFLICT
UNEXPLAINED_EVIDENCE_LOSS = 0
MANDATORY_FILES_PRESENT_AFTER_SYNC = 16/16
```

The Step-11 conflict was resolved correctly and losslessly.

You then created a Step-14A crawler/runner locally.

Reported execution history:

```text
first runner attempt -> failed before fetch because of TLS/opener argument bug
bug corrected
isolated request to https://okno-msk.ru/ -> HTTP 200 HTML
subsequent bounded runner attempts -> public requests occurred but no terminal completion/error stream and no required Step-14A artifacts were updated
FINAL_COMMIT_SHA = 4675ccd18fa3ac4b12bcbc8ff8191a7220ee01a6  # synchronization merge only
PUSH_STATUS = not pushed
QA_STATUS = not valid / no Step-14A acceptance claim
STEP15_EXECUTED = false
```

The canonical remote has advanced since your last fetch. Do not assume any earlier remote SHA is current.

Your job now is:

```text
1. preserve and safely integrate your current local synchronized history + crawler work with the latest remote rules;
2. qualify/debug the crawler through staged finite execution;
3. only after qualification passes, execute the full Step-14A crawl;
4. commit and NORMAL-PUSH durable code/evidence;
5. do NOT execute Step 15.
```

Do NOT use paid provider/API calls.
Do NOT use GenSearch/Alice.
Do NOT mutate the public website.
Do NOT use `git reset --hard`.
Do NOT force-push.
Do NOT discard the local Step-11 preserved evidence or current crawler work.
Do NOT publish partial diagnostic data under the required final Step-14A filenames.

# PHASE 0 — preserve local runner work before integrating newer remote authority

Run:

```bash
git status --short
git branch --show-current
git rev-parse HEAD
```

Record:

```text
LOCAL_HEAD_RETRY4_START
WORKTREE_RETRY4_START
```

Expected branch:

`roadmap/kwork-productization-2026-08-28`

Confirm the safety ref still exists:

```bash
git show-ref --verify refs/heads/codex/backup-step14a-pre-sync-20260902
```

Inspect all local tracked/untracked changes created after merge `4675ccd18fa3ac4b12bcbc8ff8191a7220ee01a6`.

Your previous report says a crawler/runner was added and modified locally. Preserve it.

If the runner/fix changes are uncommitted, create a local checkpoint commit BEFORE merging new remote authority, provided you can do so without including partial/invalid final Step-14A output artifacts.

A checkpoint commit may contain:

```text
runner code;
runner tests;
diagnostic helpers;
notes explaining that the runner is not yet qualified.
```

It must NOT claim Step-14A success.

Do not include partial files under these required final names unless they are valid final outputs from a terminal-success run:

```text
STEP_14A_CODEX_SITE_DISCOVERY_URLS.tsv
STEP_14A_CODEX_INTERNAL_LINK_GRAPH.tsv
STEP_14A_CODEX_PAGE_PROFILE_LEDGER.tsv
STEP_14A_CODEX_UPSTREAM_RECONCILIATION.tsv
STEP_14A_CODEX_REQUIRED_EDGE_VERIFICATION.tsv
STEP_14A_CODEX_QA.json
STEP_14A_CODEX_REPORT.md
```

If such partial files exist locally, move/remove them from final-output paths only after preserving any useful diagnostic information under clearly diagnostic/staging names.

# PHASE 1 — fetch and safely integrate latest remote authority

Run:

```bash
git fetch origin roadmap/kwork-productization-2026-08-28
git rev-parse origin/roadmap/kwork-productization-2026-08-28
```

Record:

```text
REMOTE_HEAD_AFTER_FETCH_RETRY4
```

Recompute local-vs-remote ancestry/divergence.

Integrate non-destructively.

The existing preservation rules remain mandatory:

```text
AUTHORITY_CONFLICT != EVIDENCE_PRESERVATION_CONFLICT
PRESERVE_BOTH != TREAT_BOTH_AS_CANONICAL
NO UNEXPLAINED EVIDENCE LOSS
```

If a genuine unresolved authority conflict appears, preserve both and stop.

If only normal non-conflicting new rules/docs arrive, merge them and continue.

After integration prove both histories are preserved as applicable.

# PHASE 2 — read the new execution reliability authorities

Read completely:

```text
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/RULES_ARCHITECTURE_CODEX_EXECUTION_RELIABILITY_GATE_ADDENDUM_2026-09-02.md

extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/STEP_14_CODEX_CRAWLER_EXECUTION_RELIABILITY_GATE.md

extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14A_CODEX_BLOCKED_RUN_CRAWLER_EXECUTION_RELIABILITY_2026-09-02.md
```

Also reread the existing Step-14A authorities/prompt required by the prior retries.

Understand these required distinctions:

```text
SINGLE_REQUEST_HTTP_200 != CRAWLER_EXECUTION_RELIABLE
RUNNER_STARTED != RUNNER_COMPLETED
NO_ERROR_STREAM != SUCCESS
NETWORK_REACHABILITY != RUNNER_EXECUTABILITY != CRAWL_COMPLETENESS
OUTPUT_FILE_EXISTS != CURRENT_RUN_SUCCESS
```

# PHASE 3 — inspect the current local crawler before changing it

Before another execution, inspect the runner code and report:

```text
CRAWLER_SCRIPT_PATH
CRAWLER_CURRENT_DIFF_SUMMARY
CURRENT_HTTP_CLIENT_PATH
CURRENT_REQUEST_TIMEOUT_POLICY
CURRENT_RETRY_POLICY
CURRENT_QUEUE_STRUCTURE
CURRENT_DEDUPLICATION_KEY
CURRENT_REDIRECT_POLICY
CURRENT_SITEMAP_TRAVERSAL_POLICY
CURRENT_PROGRESS_REPORTING
CURRENT_GLOBAL_TERMINATION_POLICY
CURRENT_OUTPUT_PUBLICATION_POLICY
```

Do not guess the stall cause from the old symptom.

Identify which of the required observability/termination controls are missing.

The runner must have equivalent support for:

```text
unique run_id;
current phase;
started_at;
last_progress_at;
explicit per-request timeout;
bounded retries;
finite mini-crawl page bound;
global deadline/watchdog;
queued/attempted/completed/failed counters;
latest completed URL or equivalent cursor;
terminal_state;
terminal_reason;
finished_at;
staging/diagnostic output separate from final required artifacts.
```

If these are missing, implement them before proceeding.

The exact CLI/options are your implementation choice, but the behavior is mandatory.

Add a regression check for the observed TLS/opener construction bug when practical.

# PHASE 4 — Q1 construction/static qualification

Run a finite static/construction qualification.

At minimum verify:

```text
runner imports/starts;
HTTP opener/client construction succeeds;
URL normalization terminates on fixed cases;
same-site/external classification is deterministic;
explicit bound/deadline options parse;
controlled failure produces a terminal diagnostic state;
TLS/opener regression check passes.
```

Record:

```text
Q1_STATUS = PASS|FAIL
Q1_COMMANDS
Q1_TERMINAL_STATE
Q1_FAILURE_REASON
```

If Q1 fails:

- do NOT launch Q2-Q5;
- persist a diagnostic report and runner/tests;
- commit and normal-push the diagnostic work if repository integration is safe;
- stop with Step14A blocked.

# PHASE 5 — Q2 one-page live runner qualification

This MUST use the actual crawler runner path, not a separate ad hoc urllib/curl diagnostic.

Run exactly one known HTML page with recursion/full discovery disabled or an equivalent explicit `max_pages=1` bound.

Use explicit request timeout and global deadline.

The run must prove:

```text
request attempted;
fetch terminal state recorded;
HTTP/content state recorded;
HTML parse returned;
internal href extraction returned;
progress/checkpoint updated;
runner exited cleanly;
diagnostic output is attributed to this run_id.
```

Record:

```text
Q2_STATUS = PASS|FAIL
Q2_RUN_ID
Q2_START
Q2_FINISH
Q2_HTTP_STATUS
Q2_EXTRACTED_INTERNAL_HREF_COUNT
Q2_TERMINAL_STATE
Q2_TERMINAL_REASON
```

`HTTP 200` alone does NOT pass Q2.

If Q2 fails or hits its deadline:

- do NOT run Q3-Q5;
- preserve current diagnostics/code;
- commit and normal-push a bounded failure report if safe;
- stop.

# PHASE 6 — Q3 finite recursive mini-crawl

Run the actual crawler with a deliberately small explicit finite page bound sufficient to exercise recursion/queue expansion.

Choose a small bound appropriate to the implementation and report it exactly as:

```text
Q3_MAX_PAGES
Q3_GLOBAL_DEADLINE
```

The mini-crawl must exercise and prove:

```text
homepage/source parsed;
child internal URLs enqueued;
multiple URLs dequeued;
deduplication prevents repeat frontier growth;
relative href normalization works;
redirect/final URL path terminates;
profile/page staging data written;
link-edge staging data written;
heartbeat/checkpoint advances;
runner reaches a clean terminal state before its explicit bound/deadline.
```

Record:

```text
Q3_STATUS
Q3_RUN_ID
Q3_MAX_PAGES
Q3_ATTEMPTED
Q3_COMPLETED
Q3_FAILED_OR_INDETERMINATE
Q3_QUEUED_FINAL
Q3_EDGE_COUNT
Q3_TERMINAL_STATE
Q3_TERMINAL_REASON
```

If Q2 passes but Q3 stalls/fails, diagnose queue/dedup/redirect/parser/output transitions before touching the full-site crawl.

Do NOT run Q5 until Q3 passes.

# PHASE 7 — Q4 sitemap qualification, isolated from full crawl

Test sitemap discovery/parsing separately under explicit finite bounds.

The goal is to prove sitemap logic terminates independently of normal HTML recursion.

Record at minimum:

```text
Q4_STATUS
Q4_RUN_ID
Q4_SITEMAP_LOCATIONS_ATTEMPTED
Q4_SITEMAPS_PARSED
Q4_URLS_DISCOVERED_WITHIN_PROBE_BOUND
Q4_TERMINAL_STATE
Q4_TERMINAL_REASON
```

Prevent recursive sitemap/index traversal from being unbounded.

If Q4 fails, do not run full Q5. Persist/push bounded diagnostics and stop.

# PHASE 8 — publish a runner qualification artifact

After Q1-Q4 pass, create:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14A_CODEX_RUNNER_QUALIFICATION_2026-09-02.json`

It must contain machine-readable values for Q1-Q4 and at minimum:

```text
runner_path
runner_code_commit_or_worktree_identity
Q1_STATUS
Q2_STATUS
Q3_STATUS
Q4_STATUS
REQUEST_TIMEOUT_CONFIGURED = true
RETRY_BOUND_CONFIGURED = true
GLOBAL_DEADLINE_CONFIGURED = true
PROGRESS_HEARTBEAT_CONFIGURED = true
TERMINAL_STATE_CONFIGURED = true
STAGING_SEPARATE_FROM_FINAL = true
FULL_CRAWL_ELIGIBLE = true
```

If any Q is not PASS:

```text
FULL_CRAWL_ELIGIBLE = false
```

# PHASE 9 — only now execute full canonical Step-14A crawl

Only if Q1=Q2=Q3=Q4=PASS:

read and execute completely:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14A_CODEX_PROMPT_2026-09-02.md`

The full run must itself use:

```text
run_id;
per-request timeout;
bounded retries;
global safety deadline/watchdog;
progress heartbeat/checkpoint;
finite deduplicated frontier;
explicit terminal state;
staging outputs before final publication.
```

If the execution environment stops returning a console stream, inspect the checkpoint/progress artifact rather than assuming success or rerunning blindly.

If progress has stopped and the runner reaches its own deadline, classify the exact terminal state and persist it.

Do not publish/overwrite the required final Step-14A artifacts until the current full run reaches terminal success and deterministic QA passes.

Required final outputs remain:

```text
STEP_14A_CODEX_SITE_DISCOVERY_URLS.tsv
STEP_14A_CODEX_INTERNAL_LINK_GRAPH.tsv
STEP_14A_CODEX_PAGE_PROFILE_LEDGER.tsv
STEP_14A_CODEX_UPSTREAM_RECONCILIATION.tsv
STEP_14A_CODEX_REQUIRED_EDGE_VERIFICATION.tsv
STEP_14A_CODEX_QA.json
STEP_14A_CODEX_REPORT.md
```

All must be attributable to the successful full run_id.

All 15 planned IMPLEMENT edges must still be classified exactly once:

```text
AS_IS_PRESENT
AS_IS_ABSENT_PLANNED
BLOCKED_OR_UNVERIFIED
NOT_APPLICABLE
```

Recommendation state remains separate from as-is topology state.

Do not make semantic page-ownership decisions yourself.
Do not execute Step 15.

# PHASE 10 — commit and NORMAL-push, even for a bounded qualification failure when useful

The previous run left important code only in the local checkout. That prevents ChatGPT from inspecting the actual runner.

Therefore:

### If Q1-Q4 or full crawl FAILS/BLOCKS

If repository integration is safe and you have coherent diagnostic code/evidence:

- commit the runner/tests/diagnostic artifact(s);
- clearly mark them BLOCKED/NOT ACCEPTED;
- do NOT publish fake final Step-14A evidence;
- fetch remote again before push;
- integrate any new remote change safely;
- NORMAL-push the diagnostic commit(s).

This lets ChatGPT inspect the actual code and failure evidence on GitHub.

### If full crawl PASSES

Commit:

```text
runner code/tests;
qualification artifact;
full current-run Step-14A outputs;
QA/report;
merge/reconciliation evidence not already committed.
```

Then fetch remote again if needed, integrate safely, and normal-push.

Rules:

```text
NO FORCE PUSH
NO RESET --HARD
NO UNEXPLAINED EVIDENCE LOSS
NO STEP15
```

# FINAL REPORT

Always report synchronization + qualification status.

At minimum:

```text
LOCAL_HEAD_RETRY4_START
WORKTREE_RETRY4_START
REMOTE_HEAD_AFTER_FETCH_RETRY4
SYNC_MODE_RETRY4
LOCAL_HEAD_AFTER_REMOTE_INTEGRATION
CRAWLER_SCRIPT_PATH
CRAWLER_CURRENT_DIFF_SUMMARY

Q1_STATUS
Q2_STATUS
Q2_RUN_ID
Q2_HTTP_STATUS
Q2_EXTRACTED_INTERNAL_HREF_COUNT
Q3_STATUS
Q3_RUN_ID
Q3_MAX_PAGES
Q3_ATTEMPTED
Q3_COMPLETED
Q3_FAILED_OR_INDETERMINATE
Q3_EDGE_COUNT
Q4_STATUS
Q4_RUN_ID
Q4_SITEMAPS_PARSED
Q4_URLS_DISCOVERED_WITHIN_PROBE_BOUND
FULL_CRAWL_ELIGIBLE

FINAL_COMMIT_SHA
PUSH_STATUS
```

If full crawl ran successfully, also report:

```text
FULL_RUN_ID
TOTAL_NORMALIZED_CURRENT_URLS
CRAWL_DISCOVERED_URLS
SITEMAP_DISCOVERED_URLS
CURRENT_URLS_NOT_IN_UPSTREAM
FETCH_FAILED_OR_INDETERMINATE
BROKEN_INTERNAL_TARGETS
ORPHAN_CANDIDATES

PLANNED_IMPLEMENT_EDGE_BASELINE = 15
AS_IS_PRESENT
AS_IS_ABSENT_PLANNED
BLOCKED_OR_UNVERIFIED
NOT_APPLICABLE
EDGE_ACCOUNTING = 15/15

QA_STATUS
BLOCKERS_OR_LIMITATIONS
STEP15_EXECUTED = false
```

If any qualification/full-run stage blocks, report its smallest proven failing stage and push the bounded diagnostic evidence/code if safe.

Do NOT claim final Step-14 closure. ChatGPT will read back the pushed code/artifacts, verify the qualification and crawl evidence, perform semantic reconciliation, and decide final Step-14 acceptance.
