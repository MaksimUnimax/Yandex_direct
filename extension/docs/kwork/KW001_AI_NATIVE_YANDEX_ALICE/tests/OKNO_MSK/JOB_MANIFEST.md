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
current_major_step = STEP_10_PRE_STEP_METHODOLOGY_RESEARCH_AND_REVIEW
next_major_step = STEP_10_USER_TASK_SERP_CLUSTERING_EXECUTION_AFTER_METHOD_GATE
job_work_complete = false
final_handoff_complete = false
revision_rework_open = true
provider_operator_action_pending = false
safe_to_delete = false
```

## Authority

Universal controls:

```text
RULES_ARCHITECTURE.md
STEP_RULES_INDEX.md
SOURCE_TO_METHOD_TRACEABILITY_GATE.md
PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md
```

Current job authorities:

```text
JOB_FLOW.md
TEST_ORDER.md
OPEN_QUESTIONS_FOR_CLIENT.md
STEP_03R_FINAL_RECONCILIATION_2026-08-29.md
STEP_04A_WORDSTAT_COVERAGE_AND_EXPANSION_REVALIDATION_2026-08-29.md
STEP_07C_SEMANTIC_CORRECTION_ACCEPTANCE_2026-08-29.md
STEP_08_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md
STEP_08_SEARCH_STAGE_FREEZE_RECONCILIATION.md
STEP_08_SEARCH_STAGE_FREEZE_ACCEPTANCE_2026-08-29.md
STEP_09_ORDINARY_YANDEX_SEARCH_PRE_STEP_REVIEW_2026-08-29.md
STEP_09_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md
STEP_09_CURRENT_STATE_AND_EXECUTION_PROTOCOL_2026-08-29.md
STEP_09_COLLECTION_METHOD_AND_IMMEDIATE_PERSISTENCE_POSTMORTEM_2026-08-29.md
STEP_09_SEARCH_RECONCILIATION.md
STEP_09_SEARCH_ACCEPTANCE_2026-08-29.md
```

Where older Step-09 planning state conflicts with the final reconciliation/acceptance or later correction authorities, the later authority wins.

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

```text
UNKNOWN INTERNAL PRIORITY != SEARCH-STAGE EVIDENCE ROUTE
```

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

### Step 08 — corrected accepted Search-stage freeze

Status: **COMPLETE / PASS AFTER METHOD CORRECTION**

```text
CORE_CANDIDATE = 1388
REVIEW_SEARCH = 944
REVIEW_DEFERRED = 174
EXCLUDED_PRESERVED = 334
TOTAL = 2840
```

Reconciliation:

```text
phrase keys = 2840/2840
REVIEW routed = 1118/1118
unrouted REVIEW = 0
silent drops = 0
semantic status rewrites = 0
forbidden business-route dispositions = 0
non-exact duplicate groups preserved = 9/9
non-exact duplicate rows preserved = 18/18
automatic non-exact merges = 0
provider/Search requests during Step 08 = 0
provider cost during Step 08 = 0 RUB
```

Frozen hashes:

```text
STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv SHA-256 = 73f52fd48ae925573b9739292b8c8893a8db40014775859c9630367703873d1f
STEP_08_REVIEW_RESOLUTION_ROUTES.tsv SHA-256 = c7439005d8371bb1557f11e43fff60be658d397739d99ab4fdeae77f284836f8
STEP_08_NONEXACT_DUPLICATE_HANDOFF.tsv SHA-256 = f0ed54972eb66a151856df494bb3444c064369497b0e2586893897b86c15ed73
```

## Step 09 — ordinary Yandex Search validation

Status: **COMPLETE AFTER METHOD + EXECUTION + PERSISTENCE CORRECTIONS**

### Method boundary

```text
STEP_09_PERMANENT_METHOD = UNVALIDATED
JOB_SPECIFIC_STEP09_METHOD_REVIEW = COMPLETE
STEP_09_SOURCE_TO_METHOD_TRACE = PASS
STEP_09_OWNER_AUTHORIZATION = RECEIVED
```

The first manifest's unsupported evidence-transfer model was corrected before provider execution:

```text
CLEANUP_REASON != SEARCH_INTENT_CLUSTER
ACQUISITION_SOURCE != SEARCH_INTENT_CLUSTER
LEXICAL_SIMILARITY != SERP_COMPATIBILITY
TRACEABILITY_COMPLETE != FULL_SERP_EVIDENCE_COVERAGE
```

### Initial tranche

```text
INITIAL_TRANCHE_PROBES = 75
REVIEW_SEARCH_TOTAL = 944
DIRECT_REVIEW_SEARCH_ROWS = 45
UNRESOLVED_UNPROBED_REVIEW_SEARCH_ROWS = 899
TRACEABILITY_COMPLETE = true
FULL_SERP_EVIDENCE_COVERAGE = false
PRE_SERP_TRANSFER_LINKS = 0
INITIAL_TRANCHE_SEMANTIC_QA = PASS_AS_INITIAL_BOUNDED_TRANCHE_ONLY
```

Ordered query-list SHA-256:

```text
ce2ca4f1220873416f621047b0256e8a1e3c18e633c11b326823ae7e0de0cecb
```

### Provider execution

```text
service = ordinary Yandex Search
protocol = SEARCH_BATCH_API_V1
region = 213 / Moscow
provider requests = 75
provider succeeded = 75
provider failed terminal = 0
provider outcome unknown = 0
provider estimated cost = 36.600 RUB
authorized max requests = 80
authorized max cost = 39.04 RUB
```

### Evidence persistence

```text
normalized query coverage = 75/75
normalized ranked rows = 750/750
repository normalized SERP ledger complete = true
canary full rows persisted = 10
R2 normalized projection rows persisted = 740
R2 raw per-item provider XML ledger complete = false
R2 per-item provider request-id ledger complete = false
```

The R2 raw-fidelity defect is explicitly accepted only as a recorded process incident. No unavailable fields are invented and no paid replay is performed merely to reconstruct lost bookkeeping.

Mandatory future paid-provider persistence gate:

```text
PROVIDER_RESULT_OR_NEXT_N_CHUNK_RECEIVED
-> PARSE_AND_ACCOUNT
-> IMMEDIATE_REPOSITORY_WRITE
-> GITHUB_READ_BACK_QA
-> COVERAGE_AND_COST_CHECKPOINT
-> ONLY_THEN_NEXT_PAID_CHUNK
```

### Step-09 analytical output

```text
DIRECT_EVIDENCE_DECISIONS = 75/75
ACTIVE_NONEXACT_DUPLICATE_COMPARISONS = 8/8
ACTIVE_DUPLICATE_AUTO_MERGES = 0
UNIVERSAL_NUMERIC_OVERLAP_THRESHOLD_USED = false
REVIEW_SEARCH_ACCOUNTED = 944/944
DIRECT_REVIEW_SEARCH_ROWS = 45
UNRESOLVED_UNPROBED_REVIEW_SEARCH_ROWS = 899
POST_SERP_AUTOMATIC_TRANSFER_ROWS = 0
SILENT_DROPS = 0
```

Duplicate handoff:

```text
7 groups = CLUSTER_TOGETHER_CANDIDATE
1 group = DO_NOT_AUTO_MERGE / REVIEW_SEARCH_JOB_BOUNDARY
```

These are Step-10 inputs, not final cluster decisions.

### Step-09 final state

```text
STEP_09_PRE_STEP_REVIEW_COMPLETE = true
STEP_09_SOURCE_TO_METHOD_TRACE_PASS = true
STEP_09_OWNER_AUTHORIZED = true
STEP_09_PROVIDER_REQUESTS = 75
STEP_09_PROVIDER_COST_RUB = 36.600
STEP_09_NORMALIZED_SERP_PERSISTENCE = PASS
STEP_09_R2_RAW_FIDELITY = KNOWN_INCOMPLETE / INCIDENT RECORDED
STEP_09_DIRECT_EVIDENCE_DECISIONS = 75/75
STEP_09_ACTIVE_DUPLICATE_COMPARISONS = 8/8
STEP_09_REVIEW_SEARCH_ACCOUNTED = 944/944
STEP_09_FULL_SERP_EVIDENCE_COVERAGE = false
STEP_09_COMPLETE = true
```

Final authorities:

```text
STEP_09_SEARCH_RECONCILIATION.md
STEP_09_SEARCH_ACCEPTANCE_2026-08-29.md
```

## Current major step — Step 10 user-task / SERP clustering

Status: **PRE-STEP METHODOLOGY RESEARCH / OWNER REVIEW REQUIRED BEFORE EXECUTION**

Permanent method status from `STEP_RULES_INDEX.md`:

```text
STEP_10_PERMANENT_METHOD = UNVALIDATED
```

Current allowed work:

```text
fresh Step-10 methodology research
source-to-method traceability
explicit decision model for meaning + observed SERP compatibility + public business fit + unresolved evidence
quantitative clustering/reconciliation QA design
PASS gate definition
owner-facing pre-step method review with direct links
```

Forbidden before Step-10 method review is complete:

```text
automatic one-keyword-one-page mapping
universal fixed SERP-overlap threshold treated as truth
silent transfer from 45 direct REVIEW probes to 899 unprobed rows
final page ownership
structural action decisions
cannibalization conclusions
```

Current Step-10 transition truth:

```text
STEP_10_PRE_STEP_RESEARCH_REQUIRED = true
STEP_10_SOURCE_TO_METHOD_TRACE_COMPLETE = false
STEP_10_OWNER_METHOD_REVIEW_COMPLETE = false
STEP_10_EXECUTION_STARTED = false
STEP_10_COMPLETE = false
```

## Remaining roadmap

```text
Step 10 — user-task / SERP clustering
Step 11 — page ownership
Step 12 — structural actions
Step 13 — cannibalization diagnosis
Step 14 — Search-only architecture freeze
Step 15 — AI-case selection
Step 16 — selective AI-search evidence
Step 17 — Search-vs-AI comparison
Step 18 — prioritization
Step 19 — client deliverables
Step 20 — final QA
Step 21 — handoff/revisions
Step 22 — job close
```

Still false:

```text
FINAL_SEMANTIC_SET_COMPLETE = false
USER_TASK_SERP_CLUSTERING_COMPLETE = false
PAGE_OWNERSHIP_COMPLETE = false
STRUCTURAL_ACTIONS_COMPLETE = false
SEARCH_ONLY_ARCHITECTURE_COMPLETE = false
AI_EVIDENCE_COMPLETE = false
CLIENT_DELIVERABLES_COMPLETE = false
FINAL_QA_COMPLETE = false
```

## Close rule

Only after job work, handoff/revisions and pending provider/operator actions are finished:

```text
job_work_complete = true
final_handoff_complete = true
revision_rework_open = false
provider_operator_action_pending = false
safe_to_delete = true
```

then delete the disposable workspace.

## Markers

```text
KW001_OKNO_MSK_STEP08_COMPLETE_AFTER_METHOD_CORRECTION = true
KW001_OKNO_MSK_SEARCH_STAGE_INPUT_FROZEN = true
KW001_OKNO_MSK_STEP09_COMPLETE = true
KW001_OKNO_MSK_STEP09_PROVIDER_REQUESTS = 75
KW001_OKNO_MSK_STEP09_PROVIDER_COST_RUB = 36.600
KW001_OKNO_MSK_STEP09_NORMALIZED_RANKED_ROWS = 750
KW001_OKNO_MSK_STEP09_DIRECT_EVIDENCE_DECISIONS = 75
KW001_OKNO_MSK_STEP09_ACTIVE_DUPLICATE_COMPARISONS = 8
KW001_OKNO_MSK_STEP09_REVIEW_SEARCH_ACCOUNTED = 944
KW001_OKNO_MSK_STEP09_REVIEW_SEARCH_UNRESOLVED = 899
KW001_OKNO_MSK_STEP10_PRE_STEP_RESEARCH_REQUIRED = true
KW001_OKNO_MSK_STEP10_SOURCE_TO_METHOD_TRACE_COMPLETE = false
KW001_OKNO_MSK_STEP10_OWNER_METHOD_REVIEW_COMPLETE = false
KW001_OKNO_MSK_STEP10_EXECUTION_STARTED = false
KW001_OKNO_MSK_STEP10_COMPLETE = false
KW001_OKNO_MSK_SAFE_TO_DELETE = false
```
