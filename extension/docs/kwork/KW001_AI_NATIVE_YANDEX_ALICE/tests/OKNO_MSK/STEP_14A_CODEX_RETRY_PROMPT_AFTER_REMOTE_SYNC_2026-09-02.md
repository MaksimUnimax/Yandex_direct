# Retry prompt — OKNO_MSK Step 14A after stale-local block

Use this prompt as the next Codex instruction. It supersedes only the repository-start/synchronization portion of the earlier Step-14A prompt. After synchronization, Codex must execute the full canonical prompt already stored in the repository.

---

You previously stopped correctly because your local checkout did not contain the mandatory Step-14A authorities/inputs. That local conclusion was caused by **stale/diverged local repository state**, not by missing canonical project files.

The canonical GitHub branch is:

`roadmap/kwork-productization-2026-08-28`

Your previous local HEAD was:

`bd5766a6498577176aaf8d0210a80c670cde4c39`

At diagnosis, the canonical remote branch had already advanced beyond that local state and contained the missing Step-14A files. The remote may have advanced further again by the time you run this retry.

Execute the following phases in order.

## Phase 0 — preserve local work and synchronize repository authority

Do NOT start website crawling before this phase passes.
Do NOT use `git reset --hard`.
Do NOT force-push.
Do NOT discard the previous local-only Step-11 commit or any other local-only work.

### 0.1 Record local state

Run and preserve in your final report:

```bash
git status --short
git branch --show-current
git rev-parse HEAD
```

The branch must be:

`roadmap/kwork-productization-2026-08-28`

If there are uncommitted changes, do not overwrite them. Determine whether they are expected prior work. If safe synchronization cannot be performed without risking them, stop and report exact paths/status.

### 0.2 Create a local safety ref before synchronization

Before integrating the remote branch, create a local backup branch/ref pointing to the current local HEAD, for example:

```bash
git branch codex/backup-step14a-pre-sync-20260902 HEAD
```

If that name already exists, use a unique suffix. This backup is local safety state; do not delete it during this run.

### 0.3 Fetch the canonical remote branch

Run:

```bash
git fetch origin roadmap/kwork-productization-2026-08-28
```

Then record:

```bash
git rev-parse origin/roadmap/kwork-productization-2026-08-28
```

This refreshed remote SHA, not the pre-fetch tracking ref, is the canonical repository authority for this run.

### 0.4 Determine local/remote relationship

Inspect ancestry/divergence explicitly, for example with:

```bash
git merge-base --is-ancestor HEAD origin/roadmap/kwork-productization-2026-08-28; echo "local_is_ancestor=$?"
git merge-base --is-ancestor origin/roadmap/kwork-productization-2026-08-28 HEAD; echo "remote_is_ancestor=$?"
git log --left-right --cherry-pick --oneline HEAD...origin/roadmap/kwork-productization-2026-08-28
```

Use the result:

- If local HEAD is strictly behind the refreshed remote and the worktree is safe, fast-forward only.
- If local HEAD already contains the refreshed remote, keep local HEAD and continue.
- If local and remote diverged, preserve the backup ref created above and integrate the refreshed remote **without discarding local-only commits**. Prefer a normal merge of the refreshed remote into the local working branch if it is conflict-free. Do not rewrite or drop local-only history merely for convenience.
- If conflicts occur in project authority, Step-11 evidence, Step-14 evidence, or other material files and cannot be resolved conservatively from repository evidence, abort the integration and stop with the exact conflict list. Do not guess.

A safe conflict-free merge is allowed. A destructive reset is not.

### 0.5 Prove synchronization before reading Step-14A authority

After synchronization/integration, record:

```bash
git rev-parse HEAD
git status --short
```

Then verify that the local checkout contains these files:

```text
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/RULES_ARCHITECTURE_CODEX_SITE_DISCOVERY_GATE_ADDENDUM_2026-09-02.md
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/STEP_14_SEARCH_ONLY_ARCHITECTURE_FREEZE_METHOD.md
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/STEP_14_CODEX_REPOSITORY_SYNC_GATE.md
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14_CURRENT_STATE.json
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14_SEARCH_ONLY_ARCHITECTURE_FREEZE.tsv
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14_INTERNAL_LINK_ARCHITECTURE.tsv
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14_CURRENT_URL_RECHECK.tsv
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14_UNRESOLVED_AND_BOUNDARY_LEDGER.tsv
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14A_CODEX_PROMPT_2026-09-02.md
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14A_CODEX_BLOCKED_RUN_STALE_LOCAL_STATE_2026-09-02.md
```

Canonical rule:

```text
LOCAL_BRANCH_NAME_MATCH != REMOTE_STATE_CURRENT
FILE_NOT_FOUND_IN_STALE_LOCAL_CLONE != FILE_ABSENT_FROM_CANONICAL_BRANCH
```

Do not repeat the previous missing-file conclusion unless the files are still absent **after refreshed remote fetch and safe synchronization**.

## Phase 1 — read the synchronization lesson

Read completely:

1. `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/STEP_14_CODEX_REPOSITORY_SYNC_GATE.md`
2. `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/RULES_ARCHITECTURE_CODEX_SITE_DISCOVERY_GATE_ADDENDUM_2026-09-02.md`
3. `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14A_CODEX_BLOCKED_RUN_STALE_LOCAL_STATE_2026-09-02.md`

Understand why the previous run was classified as `STALE_LOCAL_REPOSITORY_STATE` rather than `MISSING_PROJECT_AUTHORITY`.

## Phase 2 — execute the full canonical Step-14A prompt

Now read and execute **the full prompt from the synchronized repository**:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14A_CODEX_PROMPT_2026-09-02.md`

Follow it completely. Do not shorten its discovery, sitemap, literal `<a href>` graph, reconciliation, 15-edge verification, QA, output, or analytical-boundary requirements.

Do not execute Step 15 or later steps.
Do not make paid provider calls.
Do not use GenSearch/Alice.
Do not mutate the public site.

## Additional final-report requirements for this retry

In addition to every field required by the canonical Step-14A prompt, include:

```text
LOCAL_HEAD_BEFORE_SYNC = <sha>
REMOTE_HEAD_AFTER_FETCH = <sha>
LOCAL_REMOTE_RELATIONSHIP = <behind|ahead|diverged|equal + details>
SYNC_MODE = <fast-forward|already-contained|merge|other-safe-mode>
LOCAL_HEAD_AFTER_SYNC = <sha>
LOCAL_BACKUP_REF = <name>
WORKTREE_STATE_AFTER_SYNC = <clean/preserved + details>
MANDATORY_FILES_PRESENT_AFTER_SYNC = <count>/<count>
```

Then report the Step-14A crawl/topology results and final commit SHA exactly as required by the canonical prompt.

Do not claim final Step-14 closure. ChatGPT will read back the committed outputs, perform semantic reconciliation, and decide final acceptance afterward.
