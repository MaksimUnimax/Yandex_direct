# KW-002 — WORK BASE FRESHNESS AND AUTHORITY DRIFT RULE

Status: **OWNER-MANDATED / UNIVERSAL / ACTIVE**
Decision date: 2026-09-11
Applies to: every KW-002 Work execution, owner-relay publication and any long-running execution that can outlive repository changes.

## 1. Root cause

A Work run can start from a locally cached or previously fetched branch state while Main ChatGPT or the owner subsequently changes methodology, execution release, current state or upstream authority on the remote branch.

If Work continues from that stale snapshot, two different failures become possible:

1. the analytical result is produced under superseded rules;
2. later owner-relay publication overwrites newer mutable state files with older copies even when the analytical artifacts themselves are internally consistent.

This is an authority-versioning failure, not a niche-specific semantic failure.

## 2. Why it fails

A full-volume result can pass all local row/count tests and still answer an obsolete execution contract.

```text
LOCAL INTERNAL CONSISTENCY
!=
CURRENT AUTHORITY CONSISTENCY
```

Likewise:

```text
OWNER UPLOAD SUCCEEDED
!=
STALE STATE FILES ARE SAFE TO OVERWRITE CURRENT REMOTE STATE
```

## 3. Universal rule

Before any Work execution:

```text
FETCH CURRENT REMOTE BRANCH
→ RECORD ACTUAL LIVE HEAD
→ VERIFY ALL MANDATORY LEVEL1/LEVEL2/JOB AUTHORITIES EXIST
→ VERIFY THE CURRENT PROMPT/RELEASE IS THE ONE BEING EXECUTED
→ ONLY THEN PROCESS DATA
```

Before publication or owner-relay packaging:

```text
FETCH / CHECK REMOTE HEAD AGAIN
→ IF REMOTE DID NOT ADVANCE: publish normally
→ IF REMOTE ADVANCED: classify changed paths
→ reconcile every mutable state/method file against current authority
→ re-run affected QA if any governing authority changed
→ only then package/publish
```

Do not solve authority drift by force-pushing, blind overwrite or treating the local checkout as current truth.

## 4. Mandatory separation of artifact types

### Immutable/frozen analytical payload

Examples:

- full-volume ledgers;
- frozen QA tables;
- generated reports tied to a recorded base;
- historical audit evidence.

These may remain valid historical artifacts even if the branch later advances.

### Mutable current-state / authority files

Examples:

- execution cursor;
- JOB_FLOW / JOB_MANIFEST current status;
- current Work handoff state;
- active prompt/release pointers;
- universal methodology files.

These MUST NOT be published from a stale base without reconciliation.

## 5. Mandatory start-of-run gates

```text
REMOTE_FETCH_PERFORMED = true
WORK_LIVE_BASE_HEAD = REMOTE_BRANCH_HEAD_AT_START
MANDATORY_AUTHORITY_FILES_PRESENT = true
MANDATORY_AUTHORITY_VERSIONS_MATCH_CURRENT_RELEASE = true
SUPERSEDED_PROMPT_EXECUTED_AS_CURRENT = false
SUPERSEDED_RELEASE_EXECUTED_AS_CURRENT = false
```

If any fails:

```text
WORK_EXECUTION_ALLOWED = false
```

## 6. Mandatory pre-publication gates

Immediately before native push or owner-relay packaging:

```text
REMOTE_HEAD_RECHECKED = true
```

If the remote branch advanced after Work start:

```text
REMOTE_ADVANCED_AFTER_START = true
→ CHANGED_PATHS_CLASSIFIED
→ GOVERNING_AUTHORITY_CHANGE = true|false
→ MUTABLE_STATE_FILES_RECONCILED = true
```

If governing method/prompt/release changed:

```text
ANALYTICAL_RESULT_REVALIDATED_AGAINST_NEW_AUTHORITY = true
```

or the result remains historical/not accepted and must be rerun.

Hard gate:

```text
STALE_BASE_MUTABLE_STATE_FILE_OVERWRITE = 0
```

## 7. Owner-relay special rule

An owner-relay ZIP may contain generated analytical payload, but Work must not blindly include mutable current-state files copied from its stale workspace.

When owner relay is needed:

```text
freeze payload
→ recheck remote branch
→ refresh/reconcile mutable status documents
→ build final relay package from current authority state
```

If that cannot be done safely, exclude mutable status files from the relay and let Main ChatGPT update them after remote payload readback.

## 8. Relation to methodology changes

If Level1/Level2 methodology changes while Work is executing, the change is material when it alters:

- the required method;
- input authority;
- output schema;
- pass/fail gates;
- semantic claim boundary;
- mandatory independent QA.

A material method change revokes the old run as current PASS candidate until it is explicitly reconciled or rerun.

```text
NEWER METHOD AUTHORITY
>
OLDER LOCAL WORK CONTRACT
```

## 9. Regression matrix requirements

Every Work return must include, where applicable:

```text
WORK_START_REMOTE_HEAD
WORK_PRE_PUBLICATION_REMOTE_HEAD
REMOTE_ADVANCED_AFTER_START
CURRENT_PROMPT_FILE
CURRENT_RELEASE_FILE
MANDATORY_AUTHORITY_VERSION_CHECK
MUTABLE_STATE_RECONCILIATION
STALE_BASE_OVERWRITE_COUNT
```

## 10. PASS

A Work result may be accepted as current authority only when:

```text
START_BASE_FRESHNESS = PASS
CURRENT_METHOD_AUTHORITY = PASS
PRE_PUBLICATION_REMOTE_RECHECK = PASS
MUTABLE_STATE_RECONCILIATION = PASS
STALE_BASE_MUTABLE_STATE_FILE_OVERWRITE = 0
AND all step-specific analytical gates pass
```

Concrete incidents, commit SHAs, file names and affected job counts remain in the relevant `work/<JOB_ID>/` audit/review, not in this universal rule.
