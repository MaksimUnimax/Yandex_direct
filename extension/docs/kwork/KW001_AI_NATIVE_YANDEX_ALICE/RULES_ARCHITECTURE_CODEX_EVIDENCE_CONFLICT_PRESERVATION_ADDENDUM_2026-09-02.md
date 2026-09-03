# KW-001 — Codex evidence-conflict preservation addendum

Date: 2026-09-02  
Updated: 2026-09-03  
Status: **ACTIVE / UNIVERSAL PROCESS ADDENDUM / OWNER-REQUIRED**

## Purpose

A Codex/code run may need to synchronize a local repository that contains unpushed evidence with a canonical remote branch that contains independently produced evidence. Git can report an add/add or content conflict even when neither evidence version should be discarded.

This addendum prevents synchronization from changing project truth by silently deleting, overwriting, or arbitrarily choosing one evidence version.

Canonical rules:

```text
MERGE_CONFLICT != EVIDENCE_INVALID
EVIDENCE_CONFLICT != AUTHORIZATION_TO_PICK_ONE
PRESERVE_BOTH != TREAT_BOTH_AS_CANONICAL
FAIL_CLOSED != FORBID_LOSSLESS_PRESERVATION
```

## Why this rule exists

A prior controlled repository-synchronization incident produced an add/add conflict between independently created evidence artifacts at the same path. The execution correctly stopped instead of arbitrarily choosing one version, but the synchronization rule treated every material conflict as one undifferentiated class.

### Root cause

```text
ALL MATERIAL CONFLICTS
WERE TREATED AS
SEMANTIC / AUTHORITY CONFLICTS
```

That was too coarse. Some conflicts contain competing project truth and require analyst/owner resolution; others contain factual acquisition evidence that can be preserved losslessly with explicit provenance.

The reusable lesson is the classification and preservation logic below. The concrete repository path, commits, hashes and evidence versions remain job-specific history and must not be copied into this permanent rule.

## Required classification

Before resolving a conflict in a project evidence path, classify it as one of:

```text
AUTHORITY_CONFLICT
EVIDENCE_PRESERVATION_CONFLICT
BYTE_IDENTICAL_DUPLICATE
NON_MATERIAL_MECHANICAL_CONFLICT
```

### AUTHORITY_CONFLICT

The versions make incompatible methodology, ownership, acceptance, destructive-action, scope, or other project-truth decisions.

Action:

```text
PRESERVE BOTH
STOP
ANALYST / OWNER RECONCILIATION REQUIRED
```

### EVIDENCE_PRESERVATION_CONFLICT

Both versions are factual acquisition/extraction/run evidence and can coexist without deciding that one is false.

Action:

```text
COMPARE BOTH BLOBS
KEEP CURRENT CANONICAL REMOTE VERSION AT CANONICAL PATH
PRESERVE LOCAL-ONLY VERSION UNDER A PROVENANCE-BEARING PATH IF IT IS NOT ALREADY PRESENT ELSEWHERE
CREATE RECONCILIATION NOTE
CONTINUE SAFE INTEGRATION
```

### BYTE_IDENTICAL_DUPLICATE

Both blobs are identical, or the local blob is byte-identical to another already-present canonical remote artifact.

Action:

```text
DO NOT CREATE REDUNDANT COPY
RECORD HASH / PATH EQUIVALENCE
KEEP CANONICAL REMOTE PATH
CONTINUE
```

### NON_MATERIAL_MECHANICAL_CONFLICT

The conflict is mechanical and contains no competing evidence or project truth. Resolve only after confirming that no evidence/provenance is lost.

## Mandatory blob inspection

Do not resolve evidence conflicts from filenames alone.

For a normal merge, inspect the conflict stages or equivalent immutable blob content:

```text
OURS / LOCAL BLOB
THEIRS / REMOTE BLOB
HASHES
DIFF
RELATED CANONICAL ARTIFACTS
```

Where available, compare a local-only evidence blob against other remote artifacts from the same run before creating another preserved copy. If identical evidence already exists under a different durable canonical path, record the equivalence instead of duplicating bytes.

## Provenance requirements

When a local-only evidence version is preserved under a new path, the preserved artifact or its reconciliation note must record:

```text
original_conflict_path
local_head
remote_head_after_fetch
local_blob_hash
remote_blob_hash
preserved_local_path
canonical_remote_path
material_difference_summary
canonicality_boundary
```

The canonicality boundary must state:

```text
PRESERVED LOCAL EVIDENCE != AUTOMATIC CANONICAL AUTHORITY
```

## No destructive shortcuts

The following are forbidden as conflict-resolution shortcuts unless explicitly authorized for a different purpose:

```text
git reset --hard
force push
silent checkout --ours for all conflicts
silent checkout --theirs for all conflicts
deleting local-only evidence to obtain a clean merge
rewriting accepted remote evidence without analytical reconciliation
```

## Completion gate

A Codex synchronization involving evidence conflicts may continue only when:

```text
ALL_CONFLICTS_CLASSIFIED = true
NO_UNEXPLAINED_EVIDENCE_LOSS = true
AUTHORITY_CONFLICTS = 0
OR authority conflicts explicitly reconciled by analyst/owner
LOCAL_ONLY_EVIDENCE_PRESERVED_OR_PROVEN_DUPLICATE = true
CANONICAL_PATHS_PRESERVED = true
RECONCILIATION_NOTE_WRITTEN = true when material preservation occurred
```

## Permanent lesson

Repository synchronization is part of evidence validity. A deterministic calculation performed after silent evidence loss is not reproducible project evidence.

```text
DETERMINISTIC_EXECUTION
+ CURRENT_INPUTS
+ LOSSLESS_EVIDENCE_PROVENANCE
= ELIGIBLE REPRODUCIBLE EVIDENCE
```

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`: concrete incident identity and values belong only in Level-2 evidence or Git history.
