# KW-001 — Step 14 Codex repository synchronization gate

Date: 2026-09-02
Status: **ACTIVE / STEP-14-SPECIFIC / OWNER-REQUIRED**
Stage: Step 14 / Step 14A deterministic site-discovery and topology correction

## Purpose

A deterministic Codex run is only useful if it reads the current repository authority. A local clone may have the correct branch name while still pointing at an older commit, may contain unpushed local commits, or may have diverged from the remote branch.

Therefore:

```text
LOCAL_BRANCH_NAME_MATCH != REMOTE_STATE_CURRENT
LOCAL_ORIGIN_TRACKING_REF != CURRENT_REMOTE_AUTHORITY UNTIL FETCHED
FILE_NOT_FOUND_IN_LOCAL_CLONE != FILE_ABSENT_FROM_CANONICAL_BRANCH
```

The Step-14A blocked run on 2026-09-02 exposed this failure directly. Codex reported branch `roadmap/kwork-productization-2026-08-28` at local HEAD `bd5766a6498577176aaf8d0210a80c670cde4c39` and concluded that the Step-14A authority/input files were absent. The canonical GitHub branch, however, had already advanced to `2407b5fca3b969bd0559619e422951b8d276ddfc`, where those files existed.

The failure was not that Codex refused to continue. That fail-closed behavior was correct. The process error was that the prompt allowed Codex to perform the read-first gate against an unrefreshed local clone.

## Root cause

The original prompt said:

```text
Use the existing working branch.
```

This was interpreted as sufficient repository identity. It was not.

The implicit reasoning was:

```text
branch name is correct
-> repository context is correct
-> mandatory files should be visible locally
-> missing locally means missing from required branch
```

The invalid implication is the third-to-fourth transition.

A Git branch name does not guarantee that the local ref equals the current remote ref. A stale clone can truthfully report the right branch name and still be missing newer authority files.

In this incident the local Codex HEAD also contained an unpushed Step-11 commit not addressable by the canonical remote. Therefore a destructive reset would also have been unsafe.

## Correct synchronization method

Before reading Step-14 authority files or declaring any required input absent, Codex must:

1. record `git status --short`, current branch and local HEAD;
2. fetch the exact canonical remote branch;
3. record the refreshed `origin/<branch>` HEAD;
4. compare local and remote ancestry/state;
5. preserve any local-only commits before synchronization;
6. use fast-forward when the local branch is strictly behind and clean;
7. when local and remote diverge, create a safety backup ref/branch before rebasing or otherwise integrating local-only commits;
8. never use `reset --hard`, force-push, or destructive cleanup merely to satisfy this gate;
9. if synchronization cannot be completed safely or produces material conflicts in authority/job files, stop and report both SHAs and conflicts;
10. only after synchronization, perform the mandatory file-existence/read-first gate.

Recommended fail-safe pattern:

```text
git status --short
git branch --show-current
git rev-parse HEAD
git fetch origin roadmap/kwork-productization-2026-08-28
git rev-parse origin/roadmap/kwork-productization-2026-08-28

# Then inspect ancestry/divergence before changing refs.
# If local-only work exists, preserve it first.
# No destructive reset/force action is authorized by this gate.
```

Exact synchronization commands after the fetch may vary according to actual ancestry and local working-tree state. The invariant is preservation + current remote authority + no destructive shortcut.

## Missing-file rule

Codex may report a mandatory Step-14 file as absent only after:

```text
REMOTE_FETCH_COMPLETE = true
LOCAL_VS_REMOTE_STATE_RECORDED = true
SAFE_SYNC_COMPLETE = true
MANDATORY_PATH_CHECKED_AFTER_SYNC = true
```

If the canonical remote file exists but the local stale clone did not contain it, the event must be classified as:

```text
STALE_LOCAL_REPOSITORY_STATE
```

not:

```text
MISSING_PROJECT_AUTHORITY
```

## Why this matters for Step 14

Step 14 explicitly depends on durable authority and machine-readable upstream evidence. Running the correct crawler against stale rules or stale freeze/link inputs can produce a reproducible answer to the wrong version of the project.

Therefore repository synchronization is part of evidence validity, not merely developer convenience.

Canonical rule:

```text
DETERMINISTIC_RUN + STALE_INPUTS != VALID_REPRODUCIBLE_EVIDENCE

CURRENT_REMOTE_AUTHORITY
+ SAFE_LOCAL_SYNC
+ READ-FIRST GATE
+ DETERMINISTIC RUN
= ELIGIBLE STEP14A EVIDENCE
```

## Non-repeat control

Every future Codex prompt for a Step-14 completeness/topology run must contain a repository-synchronization phase before the authority-read phase.

The completion report must include:

```text
LOCAL_HEAD_BEFORE_SYNC
REMOTE_HEAD_AFTER_FETCH
SYNC_MODE
LOCAL_HEAD_AFTER_SYNC
WORKTREE_CLEAN_OR_PRESERVED_STATE
```

A Codex run that omits these fields does not satisfy the Step-14 Codex gate.
