# KW-001 — Step 14 Codex repository synchronization gate

Date: 2026-09-02
Status: **ACTIVE / STEP-14-SPECIFIC / OWNER-REQUIRED / UPDATED AFTER ADD-ADD EVIDENCE CONFLICT**
Stage: Step 14 / Step 14A deterministic site-discovery and topology correction

## Purpose

A deterministic Codex run is only useful if it reads the current repository authority. A local clone may have the correct branch name while still pointing at an older commit, may contain unpushed local commits, or may have diverged from the remote branch.

Therefore:

```text
LOCAL_BRANCH_NAME_MATCH != REMOTE_STATE_CURRENT
LOCAL_ORIGIN_TRACKING_REF != CURRENT_REMOTE_AUTHORITY UNTIL FETCHED
FILE_NOT_FOUND_IN_LOCAL_CLONE != FILE_ABSENT_FROM_CANONICAL_BRANCH
SAFE_SYNC != DESTRUCTIVE_HISTORY_REPLACEMENT
EVIDENCE_CONFLICT != AUTHORIZATION_TO_DROP_ONE_EVIDENCE_VERSION
```

The first Step-14A blocked run on 2026-09-02 exposed a stale-local-state failure. Codex reported branch `roadmap/kwork-productization-2026-08-28` at local HEAD `bd5766a6498577176aaf8d0210a80c670cde4c39` and concluded that the Step-14A authority/input files were absent. The canonical GitHub branch had already advanced and contained those files.

The second Step-14A retry correctly fetched current remote state and proved divergence, but a non-destructive merge then produced an add/add conflict in:

`tests/OKNO_MSK/STEP_11_CODEX_PAGE_REFRESH_REPORT.md`

Codex again stopped correctly instead of choosing one evidence version. That second stop exposed a different process gap: the synchronization rule said to stop on material conflicts, but did not yet define how to preserve two independently created evidence artifacts when both are legitimate and use the same path.

The failure was not that Codex refused to continue. Both fail-closed stops were correct. The process errors were:

1. the first prompt allowed the read-first gate against an unrefreshed local clone;
2. the second sync rule did not distinguish `semantic authority conflict` from `same-path evidence preservation conflict`.

---

## Root cause 1 — branch-name identity was mistaken for current repository state

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

---

## Root cause 2 — material conflict was treated as one undifferentiated class

The first synchronization correction correctly required:

```text
if material conflicts occur -> stop instead of guessing
```

That is necessary but incomplete.

A conflict can mean different things:

```text
A. AUTHORITY / SEMANTIC DECISION CONFLICT
   two versions make competing project decisions or rules;
   automatic resolution may change project truth;
   analyst/owner reconciliation is required.

B. SAME-PATH EVIDENCE PRESERVATION CONFLICT
   two independently created evidence artifacts occupy the same path;
   both can be preserved without deciding that one evidence version is false;
   the merge can continue if provenance is explicit and downstream authority is not silently changed.
```

The Step-11 add/add conflict is class B unless content inspection proves otherwise.

Why stopping forever would also be wrong:

```text
FAIL_CLOSED is a protection against unsupported decisions.
FAIL_CLOSED is not a rule that forbids lossless preservation.
```

If two evidence blobs can both be retained, the correct control is preservation plus provenance, not arbitrary selection and not permanent blockage.

Canonical rule:

```text
EVIDENCE_VERSION_A + EVIDENCE_VERSION_B
-> COMPARE BOTH BLOBS
-> IF IDENTICAL: RECORD EQUIVALENCE, KEEP CANONICAL PATH
-> IF DIFFERENT BUT BOTH ARE EVIDENCE: PRESERVE BOTH WITH DISTINCT PROVENANCE
-> DO NOT PROMOTE THE RENAMED LOCAL COPY TO CANONICAL AUTHORITY AUTOMATICALLY
-> RECORD RECONCILIATION NOTE
-> CONTINUE SAFE MERGE
```

---

## Correct synchronization method

Before reading Step-14 authority files or declaring any required input absent, Codex must:

1. record `git status --short`, current branch and local HEAD;
2. fetch the exact canonical remote branch;
3. record the refreshed `origin/<branch>` HEAD;
4. compare local and remote ancestry/state;
5. preserve any local-only commits before synchronization;
6. use fast-forward when the local branch is strictly behind and clean;
7. when local and remote diverge, create a safety backup ref/branch before integrating local-only commits;
8. never use `reset --hard`, force-push, or destructive cleanup merely to satisfy this gate;
9. attempt safe non-destructive integration;
10. classify conflicts before deciding whether they require an analyst stop or can be losslessly preserved;
11. only after synchronization, perform the mandatory file-existence/read-first gate.

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

---

## Add/add evidence-conflict resolution method

When a safe merge produces an add/add conflict in an evidence/report artifact, Codex must not immediately choose `ours` or `theirs`.

First inspect both conflict stages.

For a path `P` in a normal merge where current local branch is `ours` and fetched remote is `theirs`, use an equivalent of:

```bash
git show :2:P > /tmp/local-evidence

git show :3:P > /tmp/remote-evidence

sha256sum /tmp/local-evidence /tmp/remote-evidence

diff -u /tmp/remote-evidence /tmp/local-evidence || true
```

Also inspect metadata/provenance around both versions when available.

### Case 1 — byte-identical evidence

If the two blobs are byte-identical:

```text
EVIDENCE_CONTENT_EQUIVALENT = true
```

Then:

- keep the canonical remote path at `P`;
- do not create a redundant second file merely to preserve identical bytes;
- record both blob/hash provenance in the merge reconciliation note;
- continue the merge.

### Case 2 — content differs, but both are acquisition/extraction evidence

If the blobs differ but neither is a competing owner/rule/acceptance decision:

- keep the current canonical remote version at the original canonical path `P`;
- preserve the local-only version under a distinct provenance-bearing filename in the same job workspace;
- the renamed local file must clearly state that it is a preserved local-only evidence variant and is NOT automatically canonical;
- create a reconciliation note containing original path, local HEAD, remote HEAD, both hashes, summary of material differences, preservation path, and downstream authority boundary;
- continue the merge.

Recommended preserved name pattern for this incident:

`STEP_11_CODEX_PAGE_REFRESH_REPORT_LOCAL_BD5766A_PRESERVED_2026-09-02.md`

The exact suffix may vary if a collision exists, but provenance may not be lost.

### Case 3 — content differs and contains competing semantic/project authority

If one or both conflict blobs contain competing accepted decisions, methodology authority, ownership decisions, destructive actions, acceptance state, or other project truth rather than mere acquisition evidence:

```text
AUTHORITY_CONFLICT = true
-> STOP
-> PRESERVE BOTH BLOBS
-> REPORT EXACT DIFFERENCE
-> ANALYST / OWNER RECONCILIATION REQUIRED
```

Do not resolve such a conflict mechanically.

### Critical invariant

```text
PRESERVE_BOTH != TREAT_BOTH_AS_CANONICAL
```

The canonical path remains current remote authority unless a later explicit analytical/owner decision changes it. The preserved local copy is durable evidence with provenance, not silent authority promotion.

---

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

---

## Why this matters for Step 14

Step 14 explicitly depends on durable authority and machine-readable upstream evidence. Running the correct crawler against stale rules or stale freeze/link inputs can produce a reproducible answer to the wrong version of the project.

Likewise, destroying or silently selecting between upstream evidence during synchronization can change the factual basis before Step 14A even runs.

Therefore repository synchronization and evidence preservation are part of evidence validity, not merely developer convenience.

Canonical rule:

```text
DETERMINISTIC_RUN + STALE_INPUTS != VALID_REPRODUCIBLE_EVIDENCE
DETERMINISTIC_RUN + SILENT_EVIDENCE_LOSS != VALID_REPRODUCIBLE_EVIDENCE

CURRENT_REMOTE_AUTHORITY
+ SAFE_LOCAL_SYNC
+ LOSSLESS_EVIDENCE_CONFLICT_HANDLING
+ READ-FIRST GATE
+ DETERMINISTIC RUN
= ELIGIBLE STEP14A EVIDENCE
```

---

## Non-repeat controls

Every future Codex prompt for a Step-14 completeness/topology run must contain a repository-synchronization phase before the authority-read phase.

If local and remote diverge, the prompt must require:

```text
LOCAL_BACKUP_REF_CREATED = true
REMOTE_FETCH_COMPLETE = true
LOCAL_REMOTE_RELATIONSHIP_CLASSIFIED = true
NO_DESTRUCTIVE_RESET = true
CONFLICTS_CLASSIFIED = true when conflicts occur
EVIDENCE_VARIANTS_PRESERVED = true when lossless preservation applies
```

The completion report must include:

```text
LOCAL_HEAD_BEFORE_SYNC
REMOTE_HEAD_AFTER_FETCH
LOCAL_REMOTE_RELATIONSHIP
SYNC_MODE
LOCAL_HEAD_AFTER_SYNC
WORKTREE_CLEAN_OR_PRESERVED_STATE
CONFLICT_COUNT
CONFLICT_CLASSIFICATION
PRESERVED_EVIDENCE_VARIANTS
```

A Codex run that omits these fields does not satisfy the Step-14 Codex gate.

---

## Incident-specific lesson — 2026-09-02 Step-11 add/add conflict

Observed:

```text
LOCAL_HEAD_BEFORE_SYNC = bd5766a6498577176aaf8d0210a80c670cde4c39
REMOTE_HEAD_AFTER_FETCH = a9f54e2a5c2721c84024ec442f8dafad40ccdd8d
LOCAL_REMOTE_RELATIONSHIP = DIVERGED
LOCAL_BACKUP_REF = codex/backup-step14a-pre-sync-20260902
SYNC_MODE = SAFE_MERGE_ATTEMPT_ABORTED
WORKTREE_STATE_AFTER_SYNC = clean
CONFLICT_PATH = tests/OKNO_MSK/STEP_11_CODEX_PAGE_REFRESH_REPORT.md
CONFLICT_TYPE = add/add
```

What Codex did correctly:

```text
aborted merge;
kept local HEAD unchanged;
preserved backup ref;
did not choose evidence version;
did not begin website crawl;
did not execute Step 14A against unresolved repository state.
```

What the method lacked:

```text
no rule distinguished a preserve-both evidence conflict from a semantic authority conflict.
```

Corrected control:

```text
retry safe merge
-> inspect stage-2 and stage-3 blobs
-> compare hashes/diff
-> identical: keep canonical path + record equivalence
-> different acquisition evidence: keep remote canonical path + preserve local variant under provenance filename + reconciliation note
-> competing authority: stop for analyst reconciliation
-> only after clean merge proceed to Step 14A read-first gate and crawl
```
