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
current_major_step = STEP_08_SEARCH_STAGE_SEMANTIC_FREEZE_COMPLETE_AFTER_METHOD_CORRECTION
next_major_step = STEP_09_ORDINARY_YANDEX_SEARCH_VALIDATION_PRE_STEP_RESEARCH
job_work_complete = false
final_handoff_complete = false
revision_rework_open = true
provider_operator_action_pending = false
safe_to_delete = false
```

## Authority

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
STEP_08_SEARCH_STAGE_FREEZE_PRE_STEP_REVIEW_2026-08-29.md (CORRECTED METHOD VERSION)
STEP_08_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md
STEP_08_SEARCH_STAGE_FREEZE_RECONCILIATION.md
STEP_08_SEARCH_STAGE_FREEZE_ACCEPTANCE_2026-08-29.md (CORRECTED ACCEPTANCE)
```

## Accepted upstream truth

### Scope

```text
site = https://okno-msk.ru/
primary_region = Moscow
business = manufacture / sale / installation of window and glazing products/services
B2C residential = primary test focus
standalone installation internal priority = UNKNOWN
repair/service internal acquisition priority = UNKNOWN
accessories standalone internal priority = UNKNOWN
finance internal acquisition priority = UNKNOWN
new pages = allowed when justified
merge/reassignment = allowed when justified
Webmaster/Metrika/Direct = unavailable for base rehearsal
```

Important correction:

```text
UNKNOWN INTERNAL PRIORITY != SEARCH-STAGE EVIDENCE ROUTE
```

Public business relevance is evaluated from the known public offer/scope together with query/Search intent. Unknown margin, capacity or strategic preference is a later prioritization/client-constraint limitation, not a Step-8 routing state.

Method sources:
- https://yandex.ru/support/webmaster/ru/recommendations/targeting
- https://yandex.ru/support/webmaster/ru/service/queries-selection
- https://ahrefs.com/blog/keyword-intent/
- https://ahrefs.com/blog/keyword-strategy/

### Wordstat acquisition

```text
Step 03R = COMPLETE
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
```

## Step 08 — corrected accepted Search-stage semantic freeze

Status: **COMPLETE / PASS AFTER METHOD CORRECTION / SEARCH-STAGE INPUT FROZEN**

The original routing taxonomy containing:

```text
REVIEW_BUSINESS
REVIEW_SEARCH_AND_BUSINESS
```

is **SUPERSEDED** and must not be used downstream.

Root cause and correction authority:
`STEP_08_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md`.

Correct final routing:

```text
CORE_CANDIDATE = 1388
REVIEW_SEARCH = 944
REVIEW_DEFERRED = 174
EXCLUDED_PRESERVED = 334
TOTAL = 2840
```

Forbidden/removed states:

```text
REVIEW_BUSINESS = 0 / NOT PART OF CURRENT MODEL
REVIEW_SEARCH_AND_BUSINESS = 0 / NOT PART OF CURRENT MODEL
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
forbidden business-route dispositions = 0
non-exact duplicate candidate groups preserved = 9
non-exact duplicate rows preserved = 18
non-exact duplicate groups auto-merged = 0
provider/Search requests executed = 0
provider cost = 0 RUB
```

Correct non-exact duplicate routes:

```text
ORDINARY_SEARCH_BEFORE_ANY_NONEXACT_MERGE = 8 groups
DEFER_UNLESS_GROUP_SELECTED_FOR_SEARCH = 1 group
```

Correct frozen hashes:

```text
STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv SHA-256 = 73f52fd48ae925573b9739292b8c8893a8db40014775859c9630367703873d1f
STEP_08_REVIEW_RESOLUTION_ROUTES.tsv SHA-256 = c7439005d8371bb1557f11e43fff60be658d397739d99ab4fdeae77f284836f8
STEP_08_NONEXACT_DUPLICATE_HANDOFF.tsv SHA-256 = f0ed54972eb66a151856df494bb3444c064369497b0e2586893897b86c15ed73
```

## Method correction / non-repeat truth

Step 8 exposed a process defect: external methodology was gathered, but invented method elements were not individually traced back to what the sources actually supported.

Canonical current-job control:

```text
RESEARCH_COLLECTED != METHOD_VALIDATED
SOURCE_TO_METHOD_TRACEABILITY_REQUIRED = true
UNSUPPORTED_DECISION_STATE_FORBIDDEN = true
NON_EXECUTABLE_EVIDENCE_ROUTE_FORBIDDEN = true
```

For this correction the direct sources are:

- Yandex user needs/site fit: https://yandex.ru/support/webmaster/ru/recommendations/targeting
- Yandex query selection/potential: https://yandex.ru/support/webmaster/ru/service/queries-selection
- Yandex query/page evidence: https://www.yandex.ru/support/webmaster/ru/service/search-queries
- Ahrefs intent: https://ahrefs.com/blog/keyword-intent/
- Ahrefs strategy/business potential: https://ahrefs.com/blog/keyword-strategy/
- Semrush clustering: https://www.semrush.com/blog/keyword-clustering/
- Semrush mapping: https://www.semrush.com/blog/keyword-mapping/

## Current transition

No provider action is pending.

The next major stage is **Step 09 — ordinary Yandex Search validation**.

Direct Search execution remains blocked until Step 09 receives its own fresh method research, source-to-method traceability, full owner-facing pre-step report and explicit authorization.

```text
STEP_08_COMPLETE = true
STEP_08_COMPLETE_AFTER_METHOD_CORRECTION = true
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
KW001_OKNO_MSK_STEP07C_FINAL_ACCEPTANCE = true
KW001_OKNO_MSK_ROW_LEVEL_CLEANUP_COMPLETE = true
KW001_OKNO_MSK_STEP08_CORE_CANDIDATE = 1388
KW001_OKNO_MSK_STEP08_REVIEW_SEARCH = 944
KW001_OKNO_MSK_STEP08_REVIEW_DEFERRED = 174
KW001_OKNO_MSK_STEP08_EXCLUDED_PRESERVED = 334
KW001_OKNO_MSK_STEP08_FORBIDDEN_BUSINESS_ROUTE_STATES = 0
KW001_OKNO_MSK_STEP08_UNROUTED_REVIEW = 0
KW001_OKNO_MSK_STEP08_STATUS_REWRITES = 0
KW001_OKNO_MSK_STEP08_COMPLETE = true
KW001_OKNO_MSK_STEP08_METHOD_CORRECTION_COMPLETE = true
KW001_OKNO_MSK_SEARCH_STAGE_INPUT_FROZEN = true
KW001_OKNO_MSK_STEP09_PRE_STEP_RESEARCH_REQUIRED = true
KW001_OKNO_MSK_STEP09_EXECUTION_ALLOWED = false
KW001_OKNO_MSK_PROVIDER_OPERATOR_ACTION_PENDING = false
KW001_OKNO_MSK_SAFE_TO_DELETE = false
```