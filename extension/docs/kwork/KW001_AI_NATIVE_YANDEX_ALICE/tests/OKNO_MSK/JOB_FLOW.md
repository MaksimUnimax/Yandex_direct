# KW-001 / OKNO-MSK — JOB FLOW

Date created: 2026-08-28
Last updated: 2026-08-30
Status: **ACTIVE / JOB-SPECIFIC / DISPOSABLE WITH WORKSPACE**

## Whole Kwork goal

Deliver a complete, evidence-backed semantic set and site/page structure recommendation for Yandex ordinary Search plus selective Yandex AI-search evidence, with client-ready artifacts and final QA.

## Binding process controls

Universal authorities:

```text
RULES_ARCHITECTURE.md
STEP_RULES_INDEX.md
SOURCE_TO_METHOD_TRACEABILITY_GATE.md
PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md
```

Canonical controls carried forward:

```text
ROADMAP_STAGE_EXISTS != METHODOLOGY_VALIDATED
RESEARCH_COLLECTED != METHOD_VALIDATED
ACCOUNTING_QA != SEMANTIC_QA
REQUEST_SUCCEEDED != PROJECT_RESULT_COMPLETE
TRACEABILITY_COMPLETE != FULL_SERP_EVIDENCE_COVERAGE
BRIDGE_INTERNAL_DURABILITY != PROJECT_EVIDENCE_DURABILITY
UNIVERSAL_METHOD = REUSABLE_CORE + CURRENT_JOB_PROFILE + CURRENT_CONSTRAINTS
LOCAL_RULE_MUST_BE_SCOPED != LOCAL_RULE_MUST_BE_REMOVED
```

Every major step must satisfy its own methodology status and gate. A completed job-specific rehearsal does not silently promote an `UNVALIDATED` permanent method to `APPROVED`.

A universal method does not exclude domain-specific execution. The current site, business, vocabulary, real IDs, exact phrases, thresholds and owner constraints are legitimate method inputs when their scope is declared.

## Accepted completed work

### Step 0 — scope freeze
Status: **✅ COMPLETE**

### Step 1 — existing-site discovery / business-page model
Status: **✅ COMPLETE / PASS AFTER CROSS-CHANNEL REWORK**

### Step 2 — Wordstat acquisition plan
Status: **✅ COMPLETE / FROZEN**

### Step 3 — historical first Wordstat pass
Status: **🔁 SUPERSEDED**

### Step 3R — repaired first-pass Wordstat acquisition
Status: **✅ COMPLETE / VERIFIED**

```text
provider items = 18/18 complete
first-pass rows = 2415
targeted expansion rows = 550
total source rows entering cleanup = 2965
```

### Step 4 — family-level triage
Status: **✅ COMPLETE AS TRIAGE**

### Step 5 — targeted Wordstat expansion
Status: **✅ COMPLETE**

### Step 6 — demand dynamics
Status: **✅ PRESERVED / REUSABLE**

### Step 6A — acquisition coverage revalidation
Status: **✅ COMPLETE / SUFFICIENT**

### Step 7 — row-level semantic cleanup
Status: **✅ COMPLETE AFTER POST-AUDIT CORRECTION**

```text
exact phrase keys = 2840
KEEP = 1388
REVIEW = 1118
EXCLUDE_SCOPE = 180
EXCLUDE_IRRELEVANT = 120
EXCLUDE_MECHANICAL = 34
```

### Step 8 — Search-stage semantic freeze
Status: **✅ COMPLETE AFTER METHOD CORRECTION / SEARCH-STAGE INPUT FROZEN**

```text
CORE_CANDIDATE = 1388
REVIEW_SEARCH = 944
REVIEW_DEFERRED = 174
EXCLUDED_PRESERVED = 334
TOTAL = 2840
```

Step-08 reconciliation:

```text
2840/2840 phrase keys preserved
1118/1118 REVIEW routed
0 silent drops
0 semantic status rewrites
9/9 non-exact duplicate groups preserved
0 automatic merge
0 provider/Search requests
0 RUB cost
```

## Step 9 — ordinary Yandex Search validation

Status: **✅ COMPLETE AFTER METHOD + EXECUTION + PERSISTENCE CORRECTIONS**

Primary final authorities:

```text
STEP_09_SEARCH_RECONCILIATION.md
STEP_09_SEARCH_ACCEPTANCE_2026-08-29.md
STEP_09_CURRENT_STATE_AND_EXECUTION_PROTOCOL_2026-08-29.md
STEP_09_COLLECTION_METHOD_AND_IMMEDIATE_PERSISTENCE_POSTMORTEM_2026-08-29.md
STEP_09_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md
```

### Accepted job-specific method boundary

The original manifest grouping assumption was corrected before provider execution:

```text
CLEANUP_REASON != SEARCH_INTENT_CLUSTER
ACQUISITION_SOURCE != SEARCH_INTENT_CLUSTER
LEXICAL_SIMILARITY != SERP_COMPATIBILITY
TRACEABILITY_COMPLETE != FULL_SERP_EVIDENCE_COVERAGE
```

The frozen 75-query list remained valid only as:

```text
INITIAL_BOUNDED_SERP_TRANCHE
```

Permanent methodology status remains:

```text
STEP_09_PERMANENT_METHOD = UNVALIDATED
```

This job-specific completion does not change the permanent methodology index.

### Provider execution truth

```text
ordinary Yandex Search only = true
region = 213 / Moscow
initial tranche probes = 75
authorized max requests = 80
authorized max cost = 39.04 RUB
provider requests = 75
provider succeeded = 75
provider failed terminal = 0
provider outcome unknown = 0
provider estimated cost = 36.600 RUB
normalized queries = 75/75
normalized ranked rows = 750/750
```

### Live Bridge execution history

```text
YANDEX_MARKETING_BRIDGE_SOURCE_VERSION = 0.1.2
SEARCH_BATCH_NEXT_N_SUPPORTED = true
SEARCH_BATCH_NEXT_N_MANUAL_ONLY = true
LIVE_NEXT_N_REQUESTED_COUNTS_TESTED = 4,10,25,31
LIVE_NEXT_N_MAX_REQUESTED_COUNT_TESTED = 31
HARD_PROTOCOL_CEILING = 100
```

`count=100` was a local bounded-runtime test, not 100 live provider requests.

### Evidence persistence truth

```text
REPOSITORY_NORMALIZED_SERP_LEDGER_COMPLETE = true
CANARY_FULL_ROWS_PERSISTED = 10
R2_NORMALIZED_PROJECTION_ROWS_PERSISTED = 740
COMBINED_NORMALIZED_RANKED_ROWS_PERSISTED = 750
R2_RAW_PER_ITEM_PROVIDER_XML_LEDGER_COMPLETE = false
R2_PER_ITEM_PROVIDER_REQUEST_ID_LEDGER_COMPLETE = false
```

The R2 raw-fidelity limitation is a recorded process incident. It is not falsely marked as a full-raw PASS and did not trigger paid replay.

Mandatory non-repeat rule:

```text
PROVIDER_RESULT_OR_NEXT_N_CHUNK_RECEIVED
-> PARSE_AND_ACCOUNT
-> IMMEDIATE_REPOSITORY_WRITE
-> GITHUB_READ_BACK_QA
-> COVERAGE_AND_COST_CHECKPOINT
-> ONLY_THEN_NEXT_PAID_CHUNK
```

### Direct SERP analysis truth

```text
DIRECT_EVIDENCE_DECISIONS = 75/75
ACTIVE_NONEXACT_DUPLICATE_COMPARISONS = 8/8
ACTIVE_DUPLICATE_AUTO_MERGES_IN_STEP09 = 0
UNIVERSAL_NUMERIC_OVERLAP_THRESHOLD_USED = false
```

Duplicate comparison handoff:

```text
7 groups = CLUSTER_TOGETHER_CANDIDATE
1 group = DO_NOT_AUTO_MERGE / REVIEW_SEARCH_JOB_BOUNDARY
```

These remained Step-10 candidates, not Step-09 final clusters.

### REVIEW_SEARCH accounting truth

```text
REVIEW_SEARCH_TOTAL = 944
DIRECT_REVIEW_SEARCH_ROWS = 45
UNRESOLVED_UNPROBED_REVIEW_SEARCH_ROWS = 899
POST_SERP_AUTOMATIC_TRANSFER_ROWS = 0
TOTAL_ACCOUNTED = 944
SILENT_DROPS = 0
FULL_SERP_EVIDENCE_COVERAGE = false
```

`FULL_SERP_EVIDENCE_COVERAGE=false` is intentional and truthful. The bounded tranche was never authorized to stand in for all 944 rows.

### Step-09 close truth

```text
STEP09_METHOD_RESEARCH_AND_TRACE = PASS
STEP09_OWNER_AUTHORIZATION = RECEIVED
STEP09_INITIAL_TRANCHE_SEMANTIC_QA = PASS_AS_INITIAL_BOUNDED_TRANCHE_ONLY
STEP09_PROVIDER_ACCOUNTING = PASS
STEP09_NORMALIZED_SERP_PERSISTENCE = PASS
STEP09_R2_RAW_FIDELITY = KNOWN_INCOMPLETE / INCIDENT RECORDED
STEP09_DIRECT_EVIDENCE_DECISIONS = 75/75
STEP09_ACTIVE_DUPLICATE_COMPARISONS = 8/8
STEP09_REVIEW_SEARCH_ACCOUNTING = 944/944
STEP09_PREMATURE_FINAL_CLUSTERING = 0
STEP09_PREMATURE_PAGE_OWNERSHIP = 0
STEP09_COMPLETE = true
```

## Step 10 — user-task / SERP clustering

Status: **✅ COMPLETE / FRESH R1 FINAL VERIFIED / UNIVERSALITY RULE CORRECTED**

Canonical universal method authorities:

```text
STEP_10_CLUSTERING_GRANULARITY_METHOD.md
STEP_10_TASK_FIRST_SORTING_DECISION_METHOD.md
STEP_10_SORTING_AND_QA_METHOD.md
```

Corrected universal interpretation:

```text
UNIVERSAL METHOD != DOMAIN-FREE EXECUTION
EXECUTABLE METHOD = REUSABLE CORE + CURRENT JOB DOMAIN PROFILE + CURRENT CONSTRAINTS
LOCAL RULE MUST BE SCOPED != LOCAL RULE MUST BE REMOVED
```

Primary final job artifacts:

```text
STEP_10_FRESH_R1_TAXONOMY_FINAL.tsv
STEP_10_FRESH_R1_ASSIGNMENTS_FINAL.tsv
STEP_10_FRESH_R1_CLUSTER_SUMMARY_FINAL.tsv
STEP_10_FRESH_R1_PASS3_FULL_QA_LEDGER.tsv
STEP_10_FRESH_R1_PASS3_ERROR_LEDGER.tsv
STEP_10_FRESH_R1_PASS3_CONSOLIDATED_CORRECTIONS.tsv
STEP_10_FRESH_R1_PASS3_IMPACT_RECHECK.tsv
STEP_10_FRESH_R1_FINAL_QA.json
STEP_10_FRESH_R1_PASS3_REPORT.md
STEP_10_FRESH_R1_PASS3_V5_VERIFIED.marker.json
```

### Current-job clustering configuration

```text
DOMAIN_PROFILE = OKNO_MSK WINDOW / DOOR / GLAZING SUBJECT
ACTUAL_SITE_AND_BUSINESS_SCOPE_USED = true
REAL_CLUSTER_IDS_AND_NAMES_USED = true
DOMAIN-SPECIFIC VOCABULARY_USED = true
EXACT_LOCAL_PHRASES_AND_RULES_USED = true
LOCAL REGRESSION EXAMPLES USED = true
EXISTING EXACT STEP09 EVIDENCE USED = true
COUNT_MODE = UNCONSTRAINED_FOR_THIS_RUN
EXPLICIT_TARGET_CLUSTER_COUNT_USED = false
```

The absence of a target count is a fact about this run only. It is not a universal prohibition. A future job may require an exact number or range, and the corrected Step-10 rules now allow and require applying that declared constraint.

### Accepted current-run clustering boundary

```text
CURRENT PRIMARY UNIT = MATERIAL USER TASK
CURRENT BASELINE = TASK-FIRST
CURRENT DOMAIN PROFILE MAY OVERRIDE GENERIC SIGNAL PRECEDENCE
CURRENT EXACT LOCAL RULES ARE VALID WITHIN THEIR DECLARED SCOPE
CURRENT COUNT MODE = UNCONSTRAINED
```

The final sorting method resolved the complete task signature and expected terminal result, then applied the actual window/glazing vocabulary, site/business scope, real cluster IDs, exact local rules, local regression phrases and available Search evidence.

These domain details are legitimate and necessary execution inputs. Their scope is job-specific; their presence is not a defect in a universal method.

### Full-corpus execution truth

```text
SOURCE_ROWS = 2840
ACTIVE_ROWS = 2332
PASS3_INDEPENDENTLY_REVIEWED = 2332/2332
PASS3_ERROR_LEDGER_ROWS = 927
CONSOLIDATED_CORRECTION_ROWS = 927
CORRECTION_BATCHES_APPLIED = 1
FINAL_ASSIGNED_ACTIVE_ROWS = 2319
FINAL_SEARCH_REQUIRED_ACTIVE_ROWS = 13
FINAL_ACTIVE_ACCOUNTED_ROWS = 2332/2332
PRESERVED_DEFERRED_ROWS = 174
PRESERVED_EXCLUDED_ROWS = 334
```

### Taxonomy truth

```text
INPUT_FROZEN_TAXONOMY_CANDIDATES = 62
FINAL_ACTIVE_CLUSTERS_WITH_MEMBER_EVIDENCE = 59
FINAL_ZERO_MEMBER_ACTIVE_CLUSTERS = 0
RETIRED_ZERO-MEMBER_INPUT_CANDIDATES = 3
RETIRED_IDS = WINDOW_CARE_INFO, WINDOW_MEASUREMENT_INFO, OUTSIDE_USED_MARKET
TARGET_CLUSTER_COUNT_USED = false
TARGET_CLUSTER_COUNT_USED_IS_CURRENT_RUN_FACT = true
```

The three retired IDs remain preserved only as input-history candidates. They are not counted as final clusters because no final active phrase supplied member evidence in this run.

The corrected universal method nevertheless allows required reserved empty categories in a future job when the current taxonomy or deliverable calls for them.

### Final QA truth

```text
DIRECT_EVIDENCE_EXACT_ROWS_SEEN = 66
DIRECT_EVIDENCE_TRANSFER_TO_NEIGHBOURS = 0
IMPACT_ROWS_RECHECKED = 927
IMPACT_RECHECK_FAILURES = 0
SEMANTIC_INVARIANT_VIOLATIONS = 0
SEMANTIC_REGRESSION_CASES = 47
SEMANTIC_REGRESSION_FAILURES = 0
FULL_LEDGER_SEMANTIC_SCAN_FAILURES = 0
OLD_STEP10_INPUT_USED = false
BLIND84_INPUT_USED = false
```

### Bridge use and cost

```text
STEP10_BRIDGE_CLASSIFICATION = BRIDGE_CONDITIONAL
NEW_STEP10_PROVIDER_REQUESTS = 0
NEW_STEP10_PROVIDER_COST_RUB = 0
EXISTING_EXACT_STEP09_SERP_EVIDENCE_REUSED = true
```

No paid Search call was added merely to force assignment. Thirteen genuinely unresolved active phrases remain explicit for later boundary/search handling.

### Step-10 close truth

```text
STEP10_PASS1_COMPLETE = true
STEP10_PASS2_COMPLETE = true
STEP10_PASS3_COMPLETE = true
STEP10_COMPLETE_ERROR_LEDGER_FROZEN_BEFORE_CORRECTION = true
STEP10_ONE_CONSOLIDATED_CORRECTION_BATCH = true
STEP10_FULL_ACCOUNTING_REGRESSION = PASS
STEP10_IMPACT_SET_SEMANTIC_RECHECK = PASS
STEP10_ACTIVE_TAXONOMY_MEMBER_EVIDENCE = PASS
STEP10_UNIVERSALITY_CORRECTION_APPLIED = true
STEP10_FINAL_STATUS = COMPLETE
NEXT_STEP_ALLOWED = true
```

## Current step — Step 11 page ownership

Status: **🔄 PRE-STEP METHODOLOGY RESEARCH REQUIRED / EXECUTION NOT STARTED**

`STEP_RULES_INDEX.md` status:

```text
STEP_11_PERMANENT_METHOD = UNVALIDATED
```

Current allowed work is limited to the Step-11 pre-step gate:

```text
1. restate the whole Kwork goal and complete roadmap;
2. read prior page-mapping failure lessons;
3. research current page-ownership methodology;
4. define the evidence needed to map a task cluster to an existing URL;
5. distinguish page ownership from lexical URL-name matching;
6. define how existing-site evidence, ordinary SERP evidence and unresolved rows combine;
7. create source-to-method trace and owner-facing method review;
8. wait for explicit owner authorization before execution.
```

Step-11 execution is blocked until that gate is complete:

```text
STEP11_PRE_STEP_RESEARCH_REQUIRED = true
STEP11_SOURCE_TO_METHOD_TRACE_COMPLETE = false
STEP11_OWNER_METHOD_REVIEW_COMPLETE = false
STEP11_EXECUTION_STARTED = false
STEP11_COMPLETE = false
```

## Full roadmap status

| Major step | Meaning | Status |
|---|---|---|
| 0. Scope freeze | Freeze business/region/order boundaries | ✅ COMPLETE |
| 1. Existing-site discovery | Build cross-checked site/business/page model | ✅ COMPLETE |
| 2. Wordstat acquisition plan | Freeze first-pass demand probes | ✅ COMPLETE |
| 3. Historical first pass | Original provider-success-only acceptance | 🔁 SUPERSEDED |
| 3R. Repaired first pass | Preserve complete reusable Wordstat data | ✅ COMPLETE |
| 4. Family-level triage | Identify families/noise/ambiguity/probe candidates | ✅ COMPLETE AS TRIAGE |
| 5. Targeted Wordstat expansion | Fill/confirm material acquisition directions | ✅ COMPLETE |
| 6. Demand dynamics | Preserve seasonality context | ✅ PRESERVED |
| 6A. Acquisition coverage revalidation | Decide whether more Wordstat is needed | ✅ COMPLETE |
| 7. Row-level semantic cleanup | Produce trustworthy phrase-level decisions | ✅ COMPLETE AFTER CORRECTION |
| 8. Freeze Search-stage semantic set | Freeze exact Search input and executable unresolved routes | ✅ COMPLETE AFTER METHOD CORRECTION |
| 9. Ordinary Yandex Search validation | Bounded real SERP evidence and direct boundary decisions | ✅ COMPLETE AFTER CORRECTIONS |
| 10. User-task / SERP clustering | Group compatible search jobs | ✅ COMPLETE / FRESH R1 FINAL VERIFIED |
| **11. Page ownership** | **Map clusters to best existing URLs** | **🔄 CURRENT — PRE-STEP METHOD RESEARCH REQUIRED** |
| 12. Structural actions | Keep/expand/split/merge/create decisions | ⬜ NOT STARTED |
| 13. Cannibalization diagnosis | Confirm real competing-page conflicts | ⬜ NOT STARTED |
| 14. Search-only architecture freeze | Freeze architecture before AI | ⬜ NOT STARTED |
| 15. AI-case selection | Select high-information uncertain cases | ⬜ NOT STARTED |
| 16. AI-search evidence | Gather selected Alice/GenSearch evidence | ⬜ NOT STARTED |
| 17. Search-vs-AI comparison | Compare classic Search and AI evidence | ⬜ NOT STARTED |
| 18. Prioritization | Rank recommended actions | ⬜ NOT STARTED |
| 19. Client deliverables | Produce client-ready workbooks/maps/matrices | ⬜ NOT STARTED |
| 20. Final QA | Reconcile evidence, numbers and recommendations | ⬜ NOT STARTED |
| 21. Handoff/revisions | Deliver and process allowed revisions | ⬜ NOT STARTED |
| 22. Job close | Mark safe-to-delete and remove disposable workspace | ⬜ NOT STARTED |

## Current markers

```text
KW001_OKNO_MSK_JOB_FLOW_ACTIVE = true
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
KW001_OKNO_MSK_STEP10_COMPLETE = true
KW001_OKNO_MSK_STEP10_ACTIVE_ROWS = 2332
KW001_OKNO_MSK_STEP10_FINAL_ASSIGNED = 2319
KW001_OKNO_MSK_STEP10_FINAL_SEARCH_REQUIRED = 13
KW001_OKNO_MSK_STEP10_INPUT_TAXONOMY_CANDIDATES = 62
KW001_OKNO_MSK_STEP10_FINAL_ACTIVE_CLUSTERS = 59
KW001_OKNO_MSK_STEP10_ZERO_MEMBER_ACTIVE_CLUSTERS = 0
KW001_OKNO_MSK_STEP10_ERROR_LEDGER_ROWS = 927
KW001_OKNO_MSK_STEP10_CORRECTION_BATCHES = 1
KW001_OKNO_MSK_STEP10_SEMANTIC_REGRESSION_FAILURES = 0
KW001_OKNO_MSK_STEP10_COUNT_MODE = UNCONSTRAINED_FOR_THIS_RUN
KW001_OKNO_MSK_STEP10_DOMAIN_PROFILE_USED = true
KW001_OKNO_MSK_STEP10_REAL_CLUSTER_IDS_USED = true
KW001_OKNO_MSK_STEP10_EXACT_LOCAL_RULES_USED = true
KW001_OKNO_MSK_STEP10_UNIVERSALITY_CORRECTION_APPLIED = true
KW001_OKNO_MSK_STEP11_PRE_STEP_RESEARCH_REQUIRED = true
KW001_OKNO_MSK_STEP11_SOURCE_TO_METHOD_TRACE_COMPLETE = false
KW001_OKNO_MSK_STEP11_OWNER_METHOD_REVIEW_COMPLETE = false
KW001_OKNO_MSK_STEP11_EXECUTION_STARTED = false
KW001_OKNO_MSK_STEP11_COMPLETE = false
```