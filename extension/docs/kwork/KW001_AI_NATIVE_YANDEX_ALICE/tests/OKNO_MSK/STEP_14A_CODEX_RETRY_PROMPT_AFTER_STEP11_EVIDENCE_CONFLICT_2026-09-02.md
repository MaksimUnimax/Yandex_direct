# Retry prompt — OKNO_MSK Step 14A after Step-11 add/add evidence conflict

Use this prompt as the next Codex instruction. It supersedes only the synchronization/conflict-handling portion of the earlier retry. After repository integration passes, execute the full canonical Step-14A prompt already stored in the synchronized repository.

---

You previously stopped correctly after a safe merge attempt found this add/add conflict:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_11_CODEX_PAGE_REFRESH_REPORT.md`

Previous recorded state:

```text
LOCAL_HEAD_BEFORE_SYNC = bd5766a6498577176aaf8d0210a80c670cde4c39
REMOTE_HEAD_AFTER_FETCH = a9f54e2a5c2721c84024ec442f8dafad40ccdd8d
LOCAL_REMOTE_RELATIONSHIP = DIVERGED
LOCAL_BACKUP_REF = codex/backup-step14a-pre-sync-20260902
SYNC_MODE = SAFE_MERGE_ATTEMPT_ABORTED
LOCAL_HEAD_AFTER_SYNC = bd5766a6498577176aaf8d0210a80c670cde4c39
WORKTREE_STATE_AFTER_SYNC = clean
```

The canonical remote branch has advanced again since that report. Fetch it again; do not assume the previous remote SHA is still current.

Your task remains **ONLY Step 14A**.

Do NOT execute Step 15 or later steps.
Do NOT use paid provider/API calls.
Do NOT use GenSearch/Alice.
Do NOT mutate the public website.
Do NOT use `git reset --hard`.
Do NOT force-push.
Do NOT discard the local-only Step-11 commit or any evidence blob.

# PHASE 0 — refresh authority and preserve local history

1. Confirm branch and clean/preserved state:

```bash
git status --short
git branch --show-current
git rev-parse HEAD
```

Expected branch:

`roadmap/kwork-productization-2026-08-28`

2. Confirm the existing safety ref still points to preserved local history:

```bash
git show-ref --verify refs/heads/codex/backup-step14a-pre-sync-20260902
```

If it does not exist, create a new unique backup ref from current HEAD before any integration.

3. Fetch the actual current remote branch:

```bash
git fetch origin roadmap/kwork-productization-2026-08-28
git rev-parse origin/roadmap/kwork-productization-2026-08-28
```

Record this fresh value as `REMOTE_HEAD_AFTER_FETCH_RETRY3`.

4. Recompute ancestry/divergence. Do not assume it is unchanged.

# PHASE 1 — read the corrected conflict rules from the fetched remote

Before retrying the merge, inspect these files directly from the fetched remote ref if they are not yet in local HEAD:

```bash
git show origin/roadmap/kwork-productization-2026-08-28:extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/STEP_14_CODEX_REPOSITORY_SYNC_GATE.md

git show origin/roadmap/kwork-productization-2026-08-28:extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/RULES_ARCHITECTURE_CODEX_EVIDENCE_CONFLICT_PRESERVATION_ADDENDUM_2026-09-02.md

git show origin/roadmap/kwork-productization-2026-08-28:extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14A_CODEX_BLOCKED_RUN_STEP11_ADD_ADD_CONFLICT_2026-09-02.md
```

Understand these canonical distinctions:

```text
AUTHORITY_CONFLICT != EVIDENCE_PRESERVATION_CONFLICT
MERGE_CONFLICT != EVIDENCE_INVALID
PRESERVE_BOTH != TREAT_BOTH_AS_CANONICAL
FAIL_CLOSED != FORBID_LOSSLESS_PRESERVATION
```

# PHASE 2 — retry safe merge and inspect conflict blobs

Retry a normal non-destructive merge of the refreshed remote branch into the current local working branch.

Do not use a destructive reset.

If the known add/add conflict reappears, do NOT immediately abort and do NOT blindly select ours/theirs.

Let:

```text
P=extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_11_CODEX_PAGE_REFRESH_REPORT.md
```

Extract the two conflict-stage blobs before resolving:

```bash
git show :2:$P > /tmp/step11_local_conflict.md
git show :3:$P > /tmp/step11_remote_conflict.md
sha256sum /tmp/step11_local_conflict.md /tmp/step11_remote_conflict.md
diff -u /tmp/step11_remote_conflict.md /tmp/step11_local_conflict.md || true
```

For this merge direction:

```text
stage 2 / ours = local-only version
stage 3 / theirs = refreshed canonical remote version
```

Also extract and compare the current remote dated report from the same Step-11 acquisition pass:

```bash
git show origin/roadmap/kwork-productization-2026-08-28:extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_11_CODEX_CURRENT_PAGE_REFRESH_REPORT_2026-08-30.md > /tmp/step11_remote_dated.md
sha256sum /tmp/step11_remote_dated.md
diff -u /tmp/step11_remote_dated.md /tmp/step11_local_conflict.md || true
```

Classify the conflict from actual content, not filename.

## Case A — local conflict blob is byte-identical to the remote conflict blob

Classify:

```text
CONFLICT_CLASSIFICATION = BYTE_IDENTICAL_DUPLICATE
```

Keep the refreshed remote file at canonical path `P`.
Do not create a redundant preserved copy.
Record both blob hashes in a reconciliation note.
Resolve the conflict and continue the merge.

## Case B — local conflict blob is byte-identical to the already-present dated remote report

Classify:

```text
CONFLICT_CLASSIFICATION = EVIDENCE_ALREADY_PRESERVED_UNDER_REMOTE_DATED_PATH
```

Keep the refreshed remote version at canonical conflict path `P`.
Do not create a third duplicate file.
Record that the local-only blob is already durably represented by the dated remote path, including all hashes/paths.
Resolve and continue.

## Case C — blobs differ, but the local and remote files are both bounded acquisition/extraction evidence and contain no competing ownership/methodology/acceptance decision

Classify:

```text
CONFLICT_CLASSIFICATION = EVIDENCE_PRESERVATION_CONFLICT
```

Preserve both versions without treating both as canonical.

Required actions:

1. preserve the local stage-2 blob under:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_11_CODEX_PAGE_REFRESH_REPORT_LOCAL_BD5766A_PRESERVED_2026-09-02.md`

If that exact path already exists, use a unique suffix and report it.

2. keep the refreshed remote stage-3 version at the original canonical path `P`;

3. create:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_11_CODEX_PAGE_REFRESH_REPORT_MERGE_RECONCILIATION_2026-09-02.md`

The reconciliation note must contain:

```text
original_conflict_path
LOCAL_HEAD / local provenance
REMOTE_HEAD_AFTER_FETCH_RETRY3
local_blob_sha256
remote_blob_sha256
dated_remote_blob_sha256
whether local equals dated remote
preserved_local_path
canonical_remote_path
summary of material textual differences
canonicality boundary: preserved local evidence is NOT automatically canonical authority
```

4. resolve the conflict and continue the merge.

## Case D — either blob contains materially competing project authority

Examples:

```text
page ownership verdict
methodology authority
accepted structural/destructive action
current acceptance state
scope decision
```

Classify:

```text
CONFLICT_CLASSIFICATION = AUTHORITY_CONFLICT
```

Preserve both blobs and STOP for ChatGPT/owner reconciliation.
Do not proceed to crawl.

For the known Step-11 report, acquisition/extraction evidence is expected, but verify actual content before applying Case C.

# PHASE 3 — handle any additional merge conflicts

Do not assume the known file is the only conflict after the newer remote fetch.

For every additional conflict:

1. list exact path/type;
2. inspect both versions;
3. classify as authority conflict, evidence-preservation conflict, byte-identical duplicate, or non-material mechanical conflict;
4. preserve evidence provenance;
5. do not silently choose one version across all files.

If any unresolved `AUTHORITY_CONFLICT` remains, stop.

Otherwise finish the merge commit.

The merge commit must preserve both histories:

```bash
git merge-base --is-ancestor bd5766a6498577176aaf8d0210a80c670cde4c39 HEAD

git merge-base --is-ancestor "$REMOTE_HEAD_AFTER_FETCH_RETRY3" HEAD
```

Both commands must succeed before Step 14A execution.

Record:

```text
SYNC_MODE = SAFE_MERGE_WITH_EVIDENCE_PRESERVATION
LOCAL_HEAD_AFTER_SYNC = <merge sha>
CONFLICT_COUNT = <integer>
CONFLICT_CLASSIFICATIONS = <list>
PRESERVED_EVIDENCE_VARIANTS = <paths or NONE_EQUIVALENT>
UNEXPLAINED_EVIDENCE_LOSS = 0
```

# PHASE 4 — prove mandatory authorities and inputs exist after merge

Verify the complete mandatory file list from the prior retry prompt plus these newer authorities:

```text
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/RULES_ARCHITECTURE_CODEX_EVIDENCE_CONFLICT_PRESERVATION_ADDENDUM_2026-09-02.md
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/STEP_14_CODEX_REPOSITORY_SYNC_GATE.md
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14A_CODEX_BLOCKED_RUN_STEP11_ADD_ADD_CONFLICT_2026-09-02.md
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14A_CODEX_PROMPT_2026-09-02.md
```

Do not declare authority missing before this merged-state check.

# PHASE 5 — execute the full canonical Step-14A task

Now read and execute completely:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14A_CODEX_PROMPT_2026-09-02.md`

Do not weaken it.

Required Step-14A evidence remains:

```text
deterministic homepage/same-site crawl
public sitemap discovery
URL normalization
current URL universe
page-profile ledger
literal same-site <a href> graph
crawl depth
incoming/outgoing internal links
sitemap membership
crawl reachability
redirect/fetch/error evidence
orphan-candidate classification
broken internal targets
upstream-vs-current reconciliation
all newly discovered URLs surfaced
all 15 planned IMPLEMENT edges checked literally
recommendation_state separate from as_is_topology_state
machine-readable QA
human-readable report
```

Do not make semantic ownership changes yourself.
Do not create/merge/delete target pages.
Do not add redirects/canonicals.
Do not execute Step 15.

# PHASE 6 — commit and push durable evidence

After Step-14A execution and QA, commit all intended merge-resolution evidence, crawler code and required Step-14A artifacts.

Then push normally to:

`origin roadmap/kwork-productization-2026-08-28`

Rules:

```text
NO FORCE PUSH
REMOTE FETCHED BEFORE PUSH IF NEEDED
PUSH MUST BE FAST-FORWARD FROM CURRENT REMOTE AUTHORITY
```

If the remote advances again before push, fetch and integrate safely; do not overwrite remote history.

If Step-14A execution is blocked after synchronization by a material website/fetch limitation, persist a bounded failure report and the completed safe synchronization/reconciliation evidence, commit and normal-push those durable artifacts if possible. Do not fabricate PASS.

# FINAL REPORT

Report all synchronization fields plus the canonical Step-14A result:

```text
LOCAL_HEAD_BEFORE_SYNC
REMOTE_HEAD_AFTER_FETCH_RETRY3
LOCAL_REMOTE_RELATIONSHIP
LOCAL_BACKUP_REF
SYNC_MODE
LOCAL_HEAD_AFTER_SYNC
CONFLICT_COUNT
CONFLICT_CLASSIFICATIONS
LOCAL_CONFLICT_BLOB_SHA256
REMOTE_CONFLICT_BLOB_SHA256
DATED_REMOTE_BLOB_SHA256
LOCAL_EQUALS_REMOTE_CONFLICT_BLOB = true/false
LOCAL_EQUALS_DATED_REMOTE_BLOB = true/false
PRESERVED_EVIDENCE_VARIANTS
UNEXPLAINED_EVIDENCE_LOSS = 0
MANDATORY_FILES_PRESENT_AFTER_SYNC = <n>/<n>

FINAL_COMMIT_SHA
PUSH_STATUS
CRAWLER_SCRIPT_PATH
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

Do NOT claim Step 14 is finally closed. ChatGPT will read the pushed artifacts, perform semantic reconciliation of newly discovered URLs, re-open only affected units when justified, verify the 15 edge classifications, rerun final QA, and decide final Step-14 acceptance.
