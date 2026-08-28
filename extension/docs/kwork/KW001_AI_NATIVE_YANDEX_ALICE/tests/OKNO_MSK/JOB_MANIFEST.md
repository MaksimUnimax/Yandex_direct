# KW-001 / OKNO-MSK — JOB MANIFEST

Date created: 2026-08-28  
Workspace status: **ACTIVE / DISPOSABLE / LEGACY PATH**

```text
JOB_ID = OKNO_MSK
KWORK_ID = KW001_AI_NATIVE_YANDEX_ALICE
workspace_path = extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/
canonical_future_workspace_path = extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/work/<JOB_ID>/
workspace_is_disposable = true
legacy_path_allowed_until_close = true
current_major_step = STEP_04_CORRECTED_AND_REFROZEN
next_major_step = STEP_05_PRE_STEP_REVIEW
close_extraction_complete = false
universal_lessons_promoted_for_final_close = false
final_handoff_complete = false
revision_window_closed = false
safe_to_delete = false
```

## Authority

This directory is the isolated working memory for the current OKNO-MSK rehearsal.

All concrete case-specific material belongs here, including:

```text
site facts / URLs
client/mock-order assumptions
raw and processed keyword evidence
provider evidence
step checkpoints
matrices
page/cluster decisions
deliverables
case errors/incidents
case acceptances
```

Permanent reusable methodology must be promoted to the parent KW-001 universal docs and stripped of concrete case-specific facts.

## Close rule

Do not delete this workspace while any field below remains false:

```text
close_extraction_complete
universal_lessons_promoted_for_final_close
final_handoff_complete
revision_window_closed
safe_to_delete
```

At final close:

```text
1. review STEP_REVIEW_AND_ERRORS_LEDGER.md;
2. extract reusable lessons to permanent KW-001 docs;
3. verify final productization/rehearsal records have been incorporated where needed;
4. confirm no unfinished revision/provider/QA action remains;
5. set close conditions true;
6. delete the complete tests/OKNO_MSK/ directory from the repository.
```

The workspace is not permanent project history after close.

Markers:

```text
KW001_OKNO_MSK_WORKSPACE_DISPOSABLE = true
KW001_OKNO_MSK_SAFE_TO_DELETE = false
```
