# KW-001 — Step 14 Codex repository synchronization gate

Date: 2026-09-02  
Updated: 2026-09-03  
Status: **ACTIVE / STEP-14-SPECIFIC / UNIVERSAL / OWNER-REQUIRED**

## Purpose

A deterministic run is valid only when it reads the current repository authority and preserves local-only evidence safely.

Canonical rules:

```text
LOCAL_BRANCH_NAME_MATCH != REMOTE_STATE_CURRENT
LOCAL_TRACKING_REF != CURRENT_REMOTE_AUTHORITY UNTIL FETCHED
FILE_NOT_FOUND_IN_LOCAL_CLONE != FILE_ABSENT_FROM CANONICAL BRANCH
SAFE_SYNC != DESTRUCTIVE HISTORY REPLACEMENT
EVIDENCE_CONFLICT != AUTHORIZATION TO DROP ONE VERSION
```

## Failure history and root causes

Prior controlled executions exposed two reusable synchronization failures.

### S14-SYNC-01 — branch-name identity mistaken for current repository state

A local checkout had the expected branch name but was behind/diverged from the canonical remote. Required authority files were therefore missing locally and could have been misclassified as absent from the project.

Root cause:

```text
CORRECT BRANCH NAME
WAS TREATED AS
PROOF OF CURRENT REMOTE CONTENT
```

Correction: fetch and compare local/remote state before the read-first/file-existence gate.

### S14-SYNC-02 — all material conflicts treated as one class

A non-destructive synchronization can produce a conflict between independently created evidence artifacts. The original rule correctly failed closed but did not distinguish factual evidence-preservation conflicts from competing semantic/project-authority conflicts.

Root cause:

```text
CONFLICT SEVERITY
WAS NOT SEPARATED FROM
CONFLICT MEANING
```

Correction: classify conflicts and preserve both versions losslessly when they are compatible evidence rather than competing authority.

Concrete branches, commits, hashes, paths and incident files remain job-specific evidence.

## Correct synchronization method

Before reading Step-14 authority files or declaring required inputs absent, Codex must:

1. record `git status --short`, current branch and local HEAD or equivalent state;
2. fetch the exact canonical remote branch;
3. record refreshed remote HEAD;
4. compare local and remote ancestry/state;
5. preserve local-only commits/work before synchronization;
6. fast-forward only when safe and applicable;
7. when local and remote diverge, create a safety backup ref/branch before integration;
8. never use destructive reset, force-push or cleanup merely to satisfy this gate;
9. attempt safe non-destructive integration;
10. classify conflicts before deciding whether they can be preserved mechanically or require analyst/owner reconciliation;
11. only after clean/safely preserved synchronization, perform the mandatory authority/file read.

## Conflict classification

Use `RULES_ARCHITECTURE_CODEX_EVIDENCE_CONFLICT_PRESERVATION_ADDENDUM_2026-09-02.md`.

Minimum classes:

```text
AUTHORITY_CONFLICT
EVIDENCE_PRESERVATION_CONFLICT
BYTE_IDENTICAL_DUPLICATE
NON_MATERIAL_MECHANICAL_CONFLICT
```

### Authority conflict

Competing versions alter methodology, ownership, scope, acceptance, destructive actions or other project truth.

```text
PRESERVE BOTH
-> STOP
-> ANALYST / OWNER RECONCILIATION
```

### Evidence-preservation conflict

Two factual evidence variants can coexist without declaring either false.

```text
COMPARE BLOBS
-> KEEP CURRENT CANONICAL REMOTE VERSION AT CANONICAL PATH
-> PRESERVE LOCAL-ONLY VARIANT UNDER PROVENANCE PATH WHEN NEEDED
-> RECORD RECONCILIATION NOTE
-> CONTINUE SAFE INTEGRATION
```

### Byte-identical duplicate

Record equivalence; do not create redundant evidence copies.

## Missing-file rule

A mandatory file may be reported absent only after:

```text
REMOTE_FETCH_COMPLETE = true
LOCAL_VS_REMOTE_STATE_RECORDED = true
SAFE_SYNC_COMPLETE = true
MANDATORY_PATH_CHECKED_AFTER_SYNC = true
```

If the canonical remote contains the file but the stale local checkout did not, classify the incident as stale-local repository state, not missing project authority.

## Why this matters

A reproducible algorithm run against stale rules or stale inputs gives a reproducible answer to the wrong project state.

Likewise, a deterministic run after silent evidence loss is not valid evidence.

```text
CURRENT_REMOTE_AUTHORITY
+ SAFE_LOCAL_SYNC
+ LOSSLESS_EVIDENCE_CONFLICT_HANDLING
+ READ-FIRST GATE
+ DETERMINISTIC RUN
= ELIGIBLE STEP14 EVIDENCE
```

## Required completion report

Preserve equivalent fields:

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

## Pass gate

```text
REMOTE_FETCH_COMPLETE = true
LOCAL_REMOTE_RELATIONSHIP_CLASSIFIED = true
LOCAL_ONLY_WORK_PRESERVED = true when applicable
NO_DESTRUCTIVE_RESET_OR_FORCE = true
CONFLICTS_CLASSIFIED = true when applicable
AUTHORITY_CONFLICTS_UNRESOLVED = 0
EVIDENCE_VARIANTS_PRESERVED_OR_PROVEN_DUPLICATE = true when applicable
MANDATORY_AUTHORITY_READ_AFTER_SYNC = true
```

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.

## Markers

```text
KW001_STEP14_REMOTE_FETCH_BEFORE_AUTHORITY_READ = true
KW001_STEP14_BRANCH_NAME_NOT_EQUAL_CURRENT_REMOTE = true
KW001_STEP14_LOCAL_ONLY_WORK_PRESERVATION_REQUIRED = true
KW001_STEP14_EVIDENCE_CONFLICT_CLASSIFICATION_REQUIRED = true
KW001_STEP14_DESTRUCTIVE_SYNC_SHORTCUT_FORBIDDEN = true
```
