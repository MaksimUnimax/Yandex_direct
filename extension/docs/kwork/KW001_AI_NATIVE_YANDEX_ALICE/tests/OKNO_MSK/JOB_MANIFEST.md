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
current_major_step = STEP_09_INITIAL_SEARCH_TRANCHE_CORRECTED_READY_FOR_INTERACTION_GATED_EXECUTION
next_major_step = STEP_09_INTERACTION_GATED_PROVIDER_EXECUTION
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
STEP_07C_SEMANTIC_CORRECTION_ACCEPTANCE_2026-08-29.md
STEP_08_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md
STEP_08_SEARCH_STAGE_FREEZE_RECONCILIATION.md
STEP_08_SEARCH_STAGE_FREEZE_ACCEPTANCE_2026-08-29.md
STEP_09_ORDINARY_YANDEX_SEARCH_PRE_STEP_REVIEW_2026-08-29.md
STEP_09_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md
STEP_09_CURRENT_STATE_AND_EXECUTION_PROTOCOL_2026-08-29.md
STEP_09_INITIAL_TRANCHE_SEMANTIC_QA.json
```

Where the original Step-09 pre-step wording conflicts with the post-audit correction, the postmortem and current-state protocol supersede it.

Universal current controls include:

```text
SOURCE_TO_METHOD_TRACEABILITY_GATE.md
PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md
STEP_RULES_INDEX.md
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

Forbidden/removed states:

```text
REVIEW_BUSINESS
REVIEW_SEARCH_AND_BUSINESS
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

Correct frozen hashes:

```text
STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv SHA-256 = 73f52fd48ae925573b9739292b8c8893a8db40014775859c9630367703873d1f
STEP_08_REVIEW_RESOLUTION_ROUTES.tsv SHA-256 = c7439005d8371bb1557f11e43fff60be658d397739d99ab4fdeae77f284836f8
STEP_08_NONEXACT_DUPLICATE_HANDOFF.tsv SHA-256 = f0ed54972eb66a151856df494bb3444c064369497b0e2586893897b86c15ed73
```

## Step 09 — ordinary Yandex Search validation

Status: **OWNER AUTHORIZED / INITIAL TRANCHE CORRECTED AFTER SEMANTIC AUDIT / PROVIDER EXECUTION NOT STARTED**

Authorities:

```text
STEP_09_ORDINARY_YANDEX_SEARCH_PRE_STEP_REVIEW_2026-08-29.md
STEP_09_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md
STEP_09_CURRENT_STATE_AND_EXECUTION_PROTOCOL_2026-08-29.md
STEP_09_INITIAL_TRANCHE_SEMANTIC_QA.json
```

Step goal:

```text
collect bounded real ordinary-Yandex SERP evidence for material intent/result-type/page-boundary questions
without prematurely performing final clustering/page ownership
```

### Post-audit causal correction

The first Step-09 manifest model incorrectly promoted process metadata into Search evidence authority:

```text
corrected_reason -> wrongly treated as if it were a SERP/user-intent family
source_id -> wrongly treated as if it were a semantic subfamily
lexical centrality -> wrongly treated as authoritative marker selection
row-to-group accounting -> wrongly described as Search coverage
```

Why this was wrong:

```text
corrected_reason explains why Step 07 remained uncertain;
source_id explains acquisition provenance;
lexical overlap explains word similarity;
none independently proves shared user intent, shared SERP, same-page compatibility or evidence transferability.
```

Canonical controls:

```text
CLEANUP_REASON != SEARCH_INTENT_CLUSTER
ACQUISITION_SOURCE != SEARCH_INTENT_CLUSTER
LEXICAL_SIMILARITY != SERP_COMPATIBILITY
TRACEABILITY_COMPLETE != FULL_SERP_EVIDENCE_COVERAGE
TRANSPORT_PERSISTED != PROJECT_RESULT_COMPLETE
```

Full causal explanation is preserved in `STEP_09_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md`, including external method authorities from Yandex, Rush Analytics, Ahrefs and Semrush.

### Corrected initial tranche truth

```text
INITIAL_TRANCHE_PROBES = 75
REVIEW_SEARCH_TOTAL = 944
DIRECT_REVIEW_SEARCH_ROWS_IN_INITIAL_TRANCHE = 45
UNRESOLVED_UNPROBED_REVIEW_SEARCH_ROWS = 899
TRACEABILITY_COMPLETE = true
FULL_SERP_EVIDENCE_COVERAGE = false
PRE_SERP_TRANSFER_ALLOWED = false
PRE_SERP_TRANSFER_LINKS = 0
INITIAL_TRANCHE_SEMANTIC_QA = PASS_AS_INITIAL_BOUNDED_TRANCHE_ONLY
```

The 75-query list is an `INITIAL_BOUNDED_SERP_TRANCHE`, not a 944-row Search cluster map.

`corrected_reason`, `source_id`, Wordstat provenance and lexical similarity may help sampling/review, but they cannot establish shared intent or same-page compatibility.

Before observed Search evidence, REVIEW_SEARCH rows are only:

```text
DIRECT_PROBE
UNRESOLVED_UNPROBED
```

No pre-SERP evidence transfer is allowed merely because two rows share a cleanup reason, acquisition source, seed, provenance or lexical pattern.

### Provider safety ceiling

```text
MAX_PROVIDER_REQUESTS = 80
INITIAL_TRANCHE_REQUESTS = 75
UNIT_COST_RUB = 0.488
ESTIMATED_INITIAL_TRANCHE_COST_RUB = 36.6
MAX_PROVIDER_COST_RUB = 39.04
```

This is project-specific budget/scope control, not an SEO threshold.

### Baseline Search parameters

```text
service = search
protocol = SEARCH_BATCH_API_V1
searchType = SEARCH_TYPE_RU
region = 213
page = 0
groupsOnPage = 10
docsInGroup = 1
groupMode = GROUP_MODE_FLAT
sortMode = SORT_MODE_BY_RELEVANCE
familyMode = FAMILY_MODE_MODERATE
fixTypoMode = FIX_TYPO_MODE_ON
responseFormat = FORMAT_XML
```

### Corrected YMB execution rule

The previously prepared one-block concept:

```text
start + next x75 + status
```

is rejected for Step 09.

Generic serial transport persistence is necessary but not sufficient. The Step-09 project gate requires:

```text
start
-> verify zero provider requests

one next
-> at most one ordinary Search provider request
-> verify governed outcome
-> verify request_executed truth
-> verify complete raw payload
-> verify normalized ranked rows
-> reconcile observed count
-> preserve reusable job evidence
-> only then allow another next
```

```text
OUTCOME_UNKNOWN => STOP / NO BLIND REPLAY
TRANSPORT_PERSISTED != PROJECT_RESULT_COMPLETE
```

### Current Step-09 state

```text
STEP_09_PRE_STEP_RESEARCH_REQUIRED = false
STEP_09_PRE_STEP_REVIEW_COMPLETE = true
STEP_09_SOURCE_TO_METHOD_TRACE_PASS = true
STEP_09_OWNER_AUTHORIZATION_PENDING = false
STEP_09_OWNER_AUTHORIZED = true
STEP_09_INITIAL_TRANCHE_CORRECTED = true
STEP_09_INITIAL_TRANCHE_SEMANTIC_QA = PASS_AS_INITIAL_BOUNDED_TRANCHE_ONLY
STEP_09_TRACEABILITY_ROWS = 944
STEP_09_TRACEABILITY_COMPLETE = true
STEP_09_FULL_SERP_EVIDENCE_COVERAGE = false
STEP_09_PRE_SERP_TRANSFER_ALLOWED = false
STEP_09_PRE_SERP_TRANSFER_LINKS = 0
STEP_09_PROVIDER_EXECUTION_SCOPE = INITIAL_BOUNDED_TRANCHE_ONLY
STEP_09_EXECUTION_STARTED = false
STEP_09_PROVIDER_REQUESTS = 0
STEP_09_PROVIDER_COST_RUB = 0
STEP_09_COMPLETE = false
STEP_10_ALLOWED = false
```

## Remaining work

```text
Step 09 interaction-gated ordinary Search execution
Step 09 preserve and verify every paid result before the next paid request
Step 09 build SERP results/comparisons/evidence decisions and reconciliation
Step 09 leave non-probed/unresolved rows explicit unless evidence transfer is separately justified
Step 10 user-task / SERP clustering
Step 11 page ownership
Step 12 structural actions
Step 13 cannibalization diagnosis
Step 14 Search-only architecture freeze
Step 15 AI-case selection
Step 16 selective AI-search evidence
Step 17 Search-vs-AI comparison
Step 18 prioritization
Step 19 client deliverables
Step 20 final QA
Step 21 handoff/revisions
Step 22 job close
```

Still false:

```text
FINAL_SEMANTIC_SET_COMPLETE = false
ORDINARY_YANDEX_SEARCH_VALIDATION_COMPLETE = false
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

Markers:

```text
KW001_OKNO_MSK_STEP08_COMPLETE_AFTER_METHOD_CORRECTION = true
KW001_OKNO_MSK_STEP08_REVIEW_SEARCH = 944
KW001_OKNO_MSK_STEP08_REVIEW_DEFERRED = 174
KW001_OKNO_MSK_STEP08_FORBIDDEN_BUSINESS_ROUTE_STATES = 0
KW001_OKNO_MSK_SEARCH_STAGE_INPUT_FROZEN = true
KW001_OKNO_MSK_STEP09_PRE_STEP_REVIEW_COMPLETE = true
KW001_OKNO_MSK_STEP09_SOURCE_TO_METHOD_TRACE_PASS = true
KW001_OKNO_MSK_STEP09_OWNER_AUTHORIZATION_PENDING = false
KW001_OKNO_MSK_STEP09_OWNER_AUTHORIZED = true
KW001_OKNO_MSK_STEP09_INITIAL_TRANCHE_CORRECTED = true
KW001_OKNO_MSK_STEP09_FULL_SERP_EVIDENCE_COVERAGE = false
KW001_OKNO_MSK_STEP09_PRE_SERP_TRANSFER_LINKS = 0
KW001_OKNO_MSK_STEP09_EXECUTION_STARTED = false
KW001_OKNO_MSK_STEP09_PROVIDER_REQUESTS = 0
KW001_OKNO_MSK_STEP09_PROVIDER_COST_RUB = 0
KW001_OKNO_MSK_STEP09_COMPLETE = false
KW001_OKNO_MSK_STEP10_ALLOWED = false
KW001_OKNO_MSK_SAFE_TO_DELETE = false
```
