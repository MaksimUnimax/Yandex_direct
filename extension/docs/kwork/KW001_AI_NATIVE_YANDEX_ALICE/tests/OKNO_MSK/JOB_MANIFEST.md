# KW-001 / OKNO-MSK — JOB MANIFEST

Date updated: 2026-08-29
Workspace status: **ACTIVE / DISPOSABLE / JOB-SPECIFIC ONLY / LEGACY PATH**

```text
JOB_ID = OKNO_MSK
KWORK_ID = KW001_AI_NATIVE_YANDEX_ALICE
workspace_path = extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/
canonical_future_workspace_path = extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/work/<JOB_ID>/
workspace_is_disposable = true
workspace_contains_universal_rules = false
legacy_path_allowed_until_close = true
current_major_step = STEP_08_SEARCH_STAGE_SEMANTIC_FREEZE_PRE_STEP_REVIEW
next_major_step = STEP_08_SEARCH_STAGE_SEMANTIC_FREEZE_EXECUTION_AFTER_OWNER_AUTHORIZATION
job_work_complete = false
final_handoff_complete = false
revision_rework_open = true
provider_operator_action_pending = false
safe_to_delete = false
```

## Authority

This directory is temporary job memory only. Universal KW-001 rules remain in the parent permanent layer and are owner-locked.

Current execution authorities:

```text
JOB_FLOW.md
TEST_ORDER.md
OPEN_QUESTIONS_FOR_CLIENT.md
STEP_03R_FINAL_RECONCILIATION_2026-08-29.md
STEP_04A_WORDSTAT_COVERAGE_AND_EXPANSION_REVALIDATION_2026-08-29.md
STEP_07B_POST_AUDIT_CORRECTION_REQUIRED_2026-08-29.md
STEP_07C_SEMANTIC_CORRECTION_REVIEW_2026-08-29.md
STEP_07C_METHOD_POSTMORTEM_AND_CORRECT_EXECUTION_2026-08-29.md
STEP_07C_SEMANTIC_CORRECTION_ACCEPTANCE_2026-08-29.md
STEP_08_SEARCH_STAGE_FREEZE_PRE_STEP_REVIEW_2026-08-29.md
```

For Step 08, the permanent `STEP_RULES_INDEX.md` currently marks this stage `UNVALIDATED`; therefore the job-specific fresh pre-step method research is mandatory authority and Step-08 execution may not begin until the owner authorizes the researched plan.

## Accepted upstream truth

### Scope

```text
site = https://okno-msk.ru/
primary_region = Moscow
business = manufacture / sale / installation of window and glazing products/services
B2C residential = primary test focus
standalone installation priority = UNKNOWN
repair/service acquisition priority = UNKNOWN
accessories standalone priority = UNKNOWN
finance acquisition priority = UNKNOWN
new pages = allowed when justified
merge/reassignment = allowed when justified
Webmaster/Metrika/Direct = unavailable for base rehearsal
```

### Wordstat acquisition

```text
Step 03R = COMPLETE
first-pass provider items = 18/18 complete
first-pass normalized rows = 2415
targeted probe rows = 550
total source rows entering cleanup = 2965
additional Wordstat required now = 0
```

### Step 07 accepted corrected cleanup

Historical Step 07B semantic PASS is superseded, but its accounting/provenance remains valid.

Owner accepted Step 07C for workflow progression on 2026-08-29.

```text
source occurrences = 2965
exact phrase keys = 2840
KEEP = 1388
REVIEW = 1118
EXCLUDE_SCOPE = 180
EXCLUDE_IRRELEVANT = 120
EXCLUDE_MECHANICAL = 34
TOTAL = 2840
builder QA failures = 0
expanded semantic QA failures = 0
manual semantic saturation passes = 4
provider requests during correction = 0
provider cost during correction = 0 RUB
```

Accepted Step-07 controls:

```text
KEEP requires positive evidence
default KEEP fallthrough = false
ACCOUNTING PASS != SEMANTIC PASS
low frequency alone does not exclude
association-only evidence does not auto-promote to KEEP
uncertainty remains REVIEW
non-exact duplicate candidates are surfaced, not silently merged
semantic QA tests both MUST_KEEP and MUST_NOT_KEEP
```

Acceptance authority:

`STEP_07C_SEMANTIC_CORRECTION_ACCEPTANCE_2026-08-29.md`.

## Current Step 08 state

Step 08 purpose:

```text
freeze one immutable Search-stage semantic handoff from accepted Step 07C
without doing Search, final clustering, page ownership or architecture decisions
```

Fresh external method research and adversarial pre-step review are complete in:

`STEP_08_SEARCH_STAGE_FREEZE_PRE_STEP_REVIEW_2026-08-29.md`.

Proposed Step-08 input arithmetic:

```text
Step-07C exact phrase keys = 2840
accepted KEEP / core candidates = 1388
accepted REVIEW requiring explicit next-resolution routing = 1118
accepted EXCLUDE_* preserved for audit = 334
1388 + 1118 + 334 = 2840
non-exact duplicate candidate groups to carry forward = 9
```

Step 08 execution has **not** started.

```text
STEP_08_PRE_STEP_REVIEW_COMPLETE = true
STEP_08_OWNER_AUTHORIZATION_PENDING = true
STEP_08_EXECUTION_STARTED = false
STEP_08_COMPLETE = false
NEXT_STEP_09_ALLOWED = false
```

No provider/Search action is pending or authorized by the current manifest.

## Blocked downstream work

Until Step 08 execution and verification pass:

```text
ORDINARY_YANDEX_SEARCH_VALIDATION = BLOCKED
USER_TASK_SERP_CLUSTERING = BLOCKED
PAGE_OWNERSHIP = BLOCKED
STRUCTURAL_ACTIONS = BLOCKED
CANNIBALIZATION_DIAGNOSIS = BLOCKED
SEARCH_ONLY_ARCHITECTURE_FREEZE = BLOCKED
AI_EVIDENCE = BLOCKED
CLIENT_DELIVERABLES = BLOCKED
```

Still false:

```text
FINAL_SEMANTIC_SET_COMPLETE = false
ORDINARY_YANDEX_SEARCH_VALIDATION_COMPLETE = false
SEARCH_ONLY_ARCHITECTURE_COMPLETE = false
AI_EVIDENCE_COMPLETE = false
CLIENT_DELIVERABLES_COMPLETE = false
FINAL_QA_COMPLETE = false
```

## Close rule

Only when all work, handoff/revisions and pending operator/provider actions are finished:

```text
job_work_complete = true
final_handoff_complete = true
revision_rework_open = false
provider_operator_action_pending = false
safe_to_delete = true
```

then delete the disposable current-job workspace.

Markers:

```text
KW001_OKNO_MSK_WORKSPACE_DISPOSABLE = true
KW001_OKNO_MSK_STEP_03R_NORMALIZED_ROWS_VERIFIED = 2415
KW001_OKNO_MSK_WORDSTAT_COVERAGE_VERDICT_SUFFICIENT = true
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_INPUT_ROWS = 2965
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_UNIQUE_EXACT = 2840
KW001_OKNO_MSK_STEP07C_KEEP = 1388
KW001_OKNO_MSK_STEP07C_REVIEW = 1118
KW001_OKNO_MSK_STEP07C_EXCLUDE_TOTAL = 334
KW001_OKNO_MSK_STEP07C_FINAL_ACCEPTANCE = true
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_COMPLETE = true
KW001_OKNO_MSK_STEP08_PRE_STEP_REVIEW_COMPLETE = true
KW001_OKNO_MSK_STEP08_OWNER_AUTHORIZATION_PENDING = true
KW001_OKNO_MSK_STEP08_EXECUTION_STARTED = false
KW001_OKNO_MSK_STEP08_COMPLETE = false
KW001_OKNO_MSK_NEXT_STEP_09_ALLOWED = false
KW001_OKNO_MSK_PROVIDER_OPERATOR_ACTION_PENDING = false
KW001_OKNO_MSK_SAFE_TO_DELETE = false
```
