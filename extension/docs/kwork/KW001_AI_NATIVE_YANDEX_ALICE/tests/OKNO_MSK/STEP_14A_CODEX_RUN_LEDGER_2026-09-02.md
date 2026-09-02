# KW-001 / OKNO_MSK — Step 14A Codex run ledger

Date: 2026-09-02  
Status: **ACTIVE / COMPLETE KNOWN-RUN ACCOUNTING / NO-RUN-SKIP**

## Mandatory rule

No Codex execution attempt for Step 14A may be silently omitted, deleted from history, collapsed into a later success, or rewritten as if it never happened.

Canonical rule:

```text
EVERY_CODEX_RUN_ATTEMPT -> LEDGER ROW / SECTION
FAILED_RUN != DISPOSABLE_HISTORY
SUPERSEDED_IMPLEMENTATION != SUPERSEDED_EVIDENCE_HISTORY
DELETE_BAD_CODE != DELETE_RUN_RECORD
```

If a run contains sub-attempts inside one Codex session, preserve those sub-attempts when they materially changed state or exposed a distinct failure.

The purpose is causal traceability: later work must be able to reconstruct what was tried, what actually happened, what evidence was produced, why the attempt stopped, and what changed before the next run.

---

# Run 0 — original Step-14 semantic execution before mandatory Codex correction

Type: ChatGPT/project execution baseline, included here because it caused the Codex correction.

Result:

```text
59/59 known URLs live
58/58 link-action rows accounted
15 IMPLEMENT recommendations preserved
19 unresolved preserved
0 destructive actions
0 new-page actions
```

Material defect discovered later:

```text
KNOWN_URL_RECHECK != CURRENT_SITE_DISCOVERY
SOURCE_LIVE + TARGET_LIVE + SEMANTIC_FIT != EDGE_IMPLEMENTED
```

Consequence:
Step 14 reopened for independent Codex current-site discovery + literal as-is link verification.

---

# Run 1 — Codex Step-14A initial attempt

Observed result:

```text
LOCAL_BRANCH = roadmap/kwork-productization-2026-08-28
LOCAL_HEAD = bd5766a6498577176aaf8d0210a80c670cde4c39
MANDATORY_STEP14A_FILES_APPEARED_MISSING_LOCALLY = true
PUBLIC_SITE_REQUESTS = 0
REPOSITORY_CHANGES = 0
STEP14A_EXECUTION_STARTED = false
```

Stop reason:
Codex correctly failed closed because its local checkout did not contain required authority/input files.

Later diagnosis:
canonical remote branch had advanced; the local clone was stale/diverged.

Classification:
`BLOCKED_SAFELY_STALE_LOCAL_REPOSITORY_STATE`

---

# Run 2 — repository synchronization attempt

Observed result:

```text
LOCAL_HEAD_BEFORE_SYNC = bd5766a6498577176aaf8d0210a80c670cde4c39
REMOTE_HEAD_AFTER_FETCH = a9f54e2a5c2721c84024ec442f8dafad40ccdd8d
LOCAL_REMOTE_RELATIONSHIP = DIVERGED
LOCAL_BACKUP_REF = codex/backup-step14a-pre-sync-20260902
SYNC_MODE = SAFE_MERGE_ATTEMPT_ABORTED
WORKTREE_AFTER_ABORT = clean
PUBLIC_SITE_REQUESTS = 0
STEP14A_EXECUTION_STARTED = false
```

Conflict:
`STEP_11_CODEX_PAGE_REFRESH_REPORT.md` add/add.

Classification:
`BLOCKED_SAFELY_STEP11_ADD_ADD_EVIDENCE_CONFLICT`

No local commit was lost.

---

# Run 3 — safe evidence-preserving synchronization + first crawler implementation attempt

Repository synchronization result:

```text
REMOTE_HEAD_AFTER_FETCH_RETRY3 = 148780ef5dc88f4d2daca21fdfaa70b64bc33cc2
SYNC_MODE = SAFE_MERGE_WITH_EVIDENCE_PRESERVATION
LOCAL_HEAD_AFTER_SYNC = 4675ccd18fa3ac4b12bcbc8ff8191a7220ee01a6
CONFLICT_COUNT = 1
CONFLICT_CLASSIFICATION = EVIDENCE_PRESERVATION_CONFLICT
UNEXPLAINED_EVIDENCE_LOSS = 0
MANDATORY_FILES_PRESENT_AFTER_SYNC = 16/16
PUSH_STATUS = not pushed
```

Evidence conflict details:
- local and remote Step-11 report variants differed only by a trailing blank line;
- local blob preserved under provenance-bearing filename;
- remote variant retained at canonical path;
- reconciliation note created locally.

Crawler sub-attempt 3A:

```text
CUSTOM_CRAWLER_ADDED_LOCALLY = true
FIRST_RUN = FAILED_BEFORE_FETCH
CAUSE = TLS/opener argument bug
```

Crawler sub-attempt 3B:

```text
TLS/opener bug corrected
isolated diagnostic homepage request = HTTP 200 HTML
```

Crawler sub-attempt 3C:

```text
bounded crawler runs made public requests
no terminal completion stream
no terminal error stream
required Step14A artifacts not updated/finalized
QA valid = false
```

Classification:
`BLOCKED_CRAWLER_PROCESS_TERMINATION_OBSERVABILITY`

Step 15 not executed.

---

# Run 4 — runner checkpoint + latest reliability authority integration

Observed result:

```text
LOCAL_HEAD_RETRY4_START = 4675ccd18fa3ac4b12bcbc8ff8191a7220ee01a6
WORKTREE_RETRY4_START = uncommitted runner + invalid final-named diagnostic artifacts
REMOTE_HEAD_AFTER_FETCH_RETRY4 = dbbc8d1b32aec33a956b9ed8e844885da2b296e5
SYNC_MODE_RETRY4 = checkpoint_then_safe_merge
RUNNER_CHECKPOINT_COMMIT = 7f0abb92f0007180923ce43d74670e32d3adc629
LOCAL_HEAD_AFTER_REMOTE_INTEGRATION = 4dce8e4c1cbc5495e2371b630603718c35a3f62f
CRAWLER_SCRIPT_PATH = extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/step14a_codex_site_discovery.py
```

The checkpoint contained unqualified crawler code only and no claimed valid final Step-14A evidence.

Qualification/full crawl did not start in this run.

Step 15 not executed.

---

# Run 5 — Q1-Q4 qualification authority integration

Observed result:

```text
LOCAL_HEAD_QUALIFICATION_START = 4dce8e4c1cbc5495e2371b630603718c35a3f62f
REMOTE_HEAD_AFTER_FETCH_QUALIFICATION = a3e816dc736e65b25a4c6734827b17d15d1b2aa5
SYNC_MODE_QUALIFICATION = SAFE_MERGE
LOCAL_HEAD_AFTER_SYNC_QUALIFICATION = d73010623467506e67ac6ebe7247efc4bd8377fa
```

State:
- mandatory Q1-Q4 prompt/current Step-14 state read;
- seven stale final-named artifacts remained uncommitted;
- qualification not started;
- no full crawl performed;
- Step 15 not executed.

Classification:
`AUTHORITY_INTEGRATED__NO_SITE_COLLECTION_EXECUTED`

---

# Run 6 — direct custom-crawler execution attempt

Observed result:

```text
DIRECT_CRAWL_AUTHORITY_MERGED = true
INVALID_UNCOMMITTED_FINAL_NAMED_ARTIFACTS_REMOVED_BEFORE_EXECUTION = true
ACTUAL_CUSTOM_RUNNER_STARTED_AGAINST_https://okno-msk.ru/ = true
TERMINAL_OUTPUT = absent
ARTIFACT_FINALIZATION = absent
FULL_CRAWL_EXECUTED = false
STEP15_EXECUTED = false
```

Classification:
`BLOCKED_REPEATED_CUSTOM_CRAWLER_PROCESS_TERMINATION_OBSERVABILITY`

This second process-level failure established that continuing to build/debug a monolithic custom crawler was the wrong tool strategy for the Codex environment.

---

# Run 7 — browser-first correction preparation

Status at ledger creation:

```text
BROWSER_FIRST_RULE_WRITTEN = true
BROWSER_FIRST_SITE_PASS_PROMPT_WRITTEN = true
BROWSER_SITE_PASS_EXECUTED = false
```

This is preparation only, not site evidence.

The next actual Codex execution must:

```text
1. preserve this complete run ledger;
2. remove the obsolete local custom crawler code and its stale diagnostic outputs;
3. use the native Codex browser as the primary site-discovery tool;
4. perform the actual browser site pass;
5. persist browser evidence;
6. normal-push results;
7. not execute Step 15.
```

---

# No-run-skip acceptance control

Before final Step-14 acceptance, verify:

```text
KNOWN_CODEX_RUNS_ACCOUNTED = 100%
FAILED_RUNS_PRESERVED_IN_HISTORY = true
SUPERSEDED_CUSTOM_CRAWLER_CODE_MAY_BE_REMOVED = true
CUSTOM_CRAWLER_RUN_HISTORY_MUST_REMAIN = true
BROWSER_RUNS_ADDED_TO_LEDGER = true
STEP15_EXECUTED_PREMATURELY = false
```

Any later Codex attempt must append itself to this ledger or an explicitly linked continuation before Step 14 may finally close.
