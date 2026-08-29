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
current_major_step = STEP_08_SEARCH_STAGE_SEMANTIC_FREEZE_COMPLETE
next_major_step = STEP_09_ORDINARY_YANDEX_SEARCH_VALIDATION_PRE_STEP_RESEARCH
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
STEP_08_SEARCH_STAGE_FREEZE_RECONCILIATION.md
STEP_08_SEARCH_STAGE_FREEZE_ACCEPTANCE_2026-08-29.md
```

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

### Step 07 — accepted corrected cleanup

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
```

Accepted Step-07 controls remain active:

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

## Step 08 — accepted Search-stage semantic freeze

Status: **COMPLETE / PASS / SEARCH-STAGE INPUT FROZEN**

Purpose achieved:

```text
accepted Step-07C semantic truth was preserved unchanged;
every phrase received an explicit Search-stage disposition;
every REVIEW row received a next-resolution route;
all exclusions remained preserved for audit;
all non-exact duplicate candidates remained unresolved and visible;
no Search/provider request was made;
no clustering/page ownership/architecture decision was made.
```

Final Step-08 routing counts:

```text
CORE_CANDIDATE = 1388
REVIEW_SEARCH = 228
REVIEW_BUSINESS = 0
REVIEW_SEARCH_AND_BUSINESS = 716
REVIEW_DEFERRED = 174
EXCLUDED_PRESERVED = 334
TOTAL = 2840
```

Reconciliation:

```text
Step-07C phrase keys expected = 2840
Step-08 phrase keys written = 2840
Step-07C REVIEW expected = 1118
Step-08 REVIEW routed = 1118
unrouted REVIEW = 0
silent drops = 0
Step-07C semantic status rewrites = 0
non-exact duplicate candidate groups preserved = 9
non-exact duplicate rows preserved = 18
non-exact duplicate groups auto-merged = 0
provider/Search requests executed = 0
provider cost = 0 RUB
```

Non-exact duplicate group routing after manual QA correction:

```text
ORDINARY_SEARCH_BEFORE_ANY_NONEXACT_MERGE = 6 groups
SEARCH_AND_BUSINESS_BEFORE_ANY_NONEXACT_MERGE = 2 groups
DEFER_UNLESS_GROUP_SELECTED_FOR_SEARCH = 1 group
```

Step-08 artifacts:

```text
STEP_08_SEARCH_STAGE_FREEZE_BUILD.py
STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv
STEP_08_REVIEW_RESOLUTION_ROUTES.tsv
STEP_08_NONEXACT_DUPLICATE_HANDOFF.tsv
STEP_08_SEARCH_STAGE_FREEZE_RECONCILIATION.md
STEP_08_SEARCH_STAGE_FREEZE_ACCEPTANCE_2026-08-29.md
```

Frozen hashes:

```text
STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv SHA-256 = e5cd7fb5e3ca118b7b1685d2a661c24797938b811a4d3dc23e1b364b3df05fe7
STEP_08_REVIEW_RESOLUTION_ROUTES.tsv SHA-256 = d9a86120c8ae8ec34ab25c7c2e07c86e8b665a31dc69531477d57b5713d61035
STEP_08_NONEXACT_DUPLICATE_HANDOFF.tsv SHA-256 = a2ba2f81a84ae5d285b6cdb8e303b1715f435b0ad0fe614e92735921f827e09a
```

## Current operator action / transition

No provider action is pending.

The next major stage is **Step 09 — ordinary Yandex Search validation**.

Permanent `STEP_RULES_INDEX.md` currently marks Step 09 `UNVALIDATED`. Therefore direct Search execution is not allowed yet.

Required next transition:

```text
READ RULES / STEP INDEX / CURRENT JOB
→ RESEARCH CURRENT STEP-09 METHOD FROM CURRENT EXTERNAL SOURCES
→ STATE YMB/SEARCH RESULT-PRESERVATION GATE IF YMB IS USED
→ SHOW OWNER SOURCES + PRACTICAL METHOD + RISKS + FULL ROADMAP
→ WAIT FOR EXPLICIT OWNER AUTHORIZATION
→ ONLY THEN EXECUTE ORDINARY SEARCH VALIDATION
```

Current transition truth:

```text
STEP_08_COMPLETE = true
SEARCH_STAGE_INPUT_FROZEN = true
NEXT_STAGE_PRE_STEP_RESEARCH_ALLOWED = true
STEP_09_PRE_STEP_RESEARCH_REQUIRED = true
STEP_09_EXECUTION_ALLOWED = false
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
KW001_OKNO_MSK_STEP07C_FINAL_ACCEPTANCE = true
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_COMPLETE = true
KW001_OKNO_MSK_STEP08_CORE_CANDIDATE = 1388
KW001_OKNO_MSK_STEP08_REVIEW_SEARCH = 228
KW001_OKNO_MSK_STEP08_REVIEW_SEARCH_AND_BUSINESS = 716
KW001_OKNO_MSK_STEP08_REVIEW_DEFERRED = 174
KW001_OKNO_MSK_STEP08_EXCLUDED_PRESERVED = 334
KW001_OKNO_MSK_STEP08_UNROUTED_REVIEW = 0
KW001_OKNO_MSK_STEP08_STATUS_REWRITES = 0
KW001_OKNO_MSK_STEP08_COMPLETE = true
KW001_OKNO_MSK_SEARCH_STAGE_INPUT_FROZEN = true
KW001_OKNO_MSK_STEP09_PRE_STEP_RESEARCH_REQUIRED = true
KW001_OKNO_MSK_STEP09_EXECUTION_ALLOWED = false
KW001_OKNO_MSK_PROVIDER_OPERATOR_ACTION_PENDING = false
KW001_OKNO_MSK_SAFE_TO_DELETE = false
```
