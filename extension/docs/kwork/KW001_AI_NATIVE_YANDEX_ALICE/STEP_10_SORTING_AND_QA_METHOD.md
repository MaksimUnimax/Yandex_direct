# Step 10 — Universal Sorting and QA Method

Updated: 2026-09-05  

Status: **APPROVED / ACTIVE / UNIVERSAL / OWNER-LOCKED**

This file defines a reusable execution and QA framework for Step-10 clustering.

`UNIVERSAL` means that the framework can be configured for different subjects and deliverables. It does **not** prohibit the use of the current site, business model, cluster names, cluster IDs, local phrases, domain-specific rules, target counts, thresholds or historical taxonomies.

Canonical companion authorities:

- `STEP_10_CLUSTERING_GRANULARITY_METHOD.md`
- `STEP_10_TASK_FIRST_SORTING_DECISION_METHOD.md`

---

## 0. Executable method composition

```text
EXECUTABLE_STEP10 =
UNIVERSAL EXECUTION FRAMEWORK
+ CURRENT DOMAIN PROFILE
+ CURRENT INPUTS
+ CURRENT TAXONOMY MODE
+ CURRENT COUNT MODE
+ CURRENT EVIDENCE MODE
+ CURRENT UNCERTAINTY MODE
+ CURRENT QA MODE
+ CURRENT OWNER / CLIENT / DELIVERABLE CONSTRAINTS
```

Canonical interpretation:

```text
UNIVERSAL FRAMEWORK != ONE FIXED WORKFLOW FOR EVERY JOB
DOMAIN-SPECIFIC EXECUTION != METHODOLOGY CONTAMINATION
LOCAL RULE != INVALID RULE
CURRENT CONSTRAINT != UNIVERSAL LAW
```

The current job may use:

```text
REAL CLUSTER IDS AND NAMES
EXACT LOCAL PHRASES
SITE-SPECIFIC BUSINESS BOUNDARIES
DOMAIN-SPECIFIC TOKENS / REGEX / DICTIONARIES
EXISTING TAXONOMIES AND HISTORICAL ASSIGNMENTS
FIXED CLUSTER COUNTS OR RANGES
LOCAL THRESHOLDS
RESERVED EMPTY CATEGORIES
OWNER-PROVIDED RULES
```

All such elements must be scoped and recorded, not removed merely because they are local.

---

## 1. Purpose

Step 10 transforms the declared current corpus into the cluster result required by the current job and verifies that result against the current method, evidence and constraints.

The framework controls:

```text
TASK UNDERSTANDING
TAXONOMY CONSTRUCTION OR REUSE
ROW ASSIGNMENT
COUNT / RANGE COMPLIANCE
DOMAIN RULE APPLICATION
EVIDENCE SCOPE
SEMANTIC QA
ACCOUNTING QA
CHANGE CONTROL
OWNER ACCEPTANCE
```

---

## 2. Execution modes

The current job must declare its execution mode before classification.

### 2.1 Fresh independent rebuild

Use when the owner explicitly requires a rebuild that does not inherit previous clustering decisions.

```text
HISTORICAL TAXONOMY / ASSIGNMENTS = COMPARISON-ONLY
FRESH TASK DISCOVERY = REQUIRED
```

### 2.2 Existing-taxonomy assignment

Use when the current taxonomy is an accepted input.

```text
EXISTING CLUSTER IDS / NAMES / CONTRACTS = EXECUTABLE INPUT
```

### 2.3 Taxonomy adaptation

Use when an existing taxonomy is retained but may be split, merged, renamed or extended.

### 2.4 Fixed-category or fixed-count execution

Use when the owner, client, tool, campaign, site or deliverable supplies:

```text
A REQUIRED CATEGORY LIST
A FIXED NUMBER OF CLUSTERS
A TARGET RANGE
A MAXIMUM OR MINIMUM SIZE
A REQUIRED OUTPUT SHAPE
```

These constraints are applied and validated as real current-job requirements.

### 2.5 Incremental or interactive execution

Use when data arrives in stages or the owner wants decisions reviewed during the process.

Controlled iteration is valid when versions and impact are recorded.

---

## 3. Count mode

The current job must declare one of the following or an equivalent mode.

### 3.1 Unconstrained

```text
NO EXPLICIT TARGET COUNT
-> COUNT MAY EMERGE FROM CURRENT BOUNDARIES
```

### 3.2 Exact target

```text
FINAL CLUSTERS MUST EQUAL N
```

### 3.3 Target range

```text
MIN_CLUSTERS <= FINAL CLUSTERS <= MAX_CLUSTERS
```

### 3.4 Required category set

The category set may contain active, reserved or currently empty categories.

A count constraint is not automatically semantic evidence, but it is still an executable project constraint. Any trade-off between semantic purity and required output shape must be recorded and resolved according to the current priority.

---

## 4. Baseline three-pass model

For large corpora and unconstrained fresh rebuilds, the preferred baseline is:

```text
PASS 1 — FULL TASK DISCOVERY
TAXONOMY NORMALIZATION / CONFIGURATION
PASS 2 — FULL ASSIGNMENT
PASS 3 — INDEPENDENT QA
CONSOLIDATED CORRECTION
REGRESSION
IMPACT RECHECK
```

This is a strong default, not a ban on other valid workflows.

The current job may use a different number or structure of passes when required by:

```text
SMALL CORPUS
FIXED CLIENT TAXONOMY
INTERACTIVE OWNER REVIEW
INCREMENTAL DATA
TOOL OR MODEL LIMITS
COST STAGING
A/B TESTING
EXPERIMENT DESIGN
```

The selected pass model must still provide enough separation between decision, review and correction for the current risk level.

---

## 5. Input and context declaration

Before execution, record as applicable:

```text
CANONICAL INPUT FILES
VERSIONS / BLOBS / HASHES
CURRENT DOMAIN PROFILE
CURRENT SITE AND BUSINESS SCOPE
CURRENT TAXONOMY MODE
CURRENT CLUSTER CONTRACTS
CURRENT COUNT MODE
CURRENT EVIDENCE SOURCES
CURRENT UNCERTAINTY MODE
CURRENT QA PLAN
OWNER / CLIENT / DELIVERABLE CONSTRAINTS
HISTORICAL RESULTS AND THEIR ALLOWED USE
```

Historical cluster names, counts, assignments and logic may be reused when the current execution mode allows reuse.

Only an explicitly independent rebuild treats them as comparison-only.

---

## 6. Task discovery

Task discovery identifies the current phrase meaning before or during assignment, depending on the selected execution mode.

Recommended semantic fields:

```text
PRIMARY_OBJECT
OBJECT_SCOPE
ACTION_OR_USER_GOAL
EXPECTED_TERMINAL_RESULT
INTENT
LIFECYCLE_STAGE
EXECUTION_MODE
MATERIAL_MODIFIERS
BUSINESS_FIT
DIRECT_EVIDENCE_STATE
BOUNDARY_UNCERTAINTY
PROVISIONAL_TASK_SIGNATURE
LOCAL_RULE_ID_IF_USED
```

Real domain terms, local examples and exact phrase rules belong in this stage when they improve correctness.

### Fresh-discovery mode

When a fresh independent taxonomy is required, final cluster IDs may be withheld during initial discovery to reduce anchoring.

### Existing-taxonomy mode

When an accepted taxonomy is the input, real cluster IDs and contracts may be used immediately.

---

## 7. Taxonomy construction, reuse or adaptation

Possible current operations:

```text
BUILD FRESH TAXONOMY
USE EXISTING TAXONOMY AS-IS
ADAPT EXISTING TAXONOMY
USE CLIENT-PROVIDED CATEGORIES
USE SITE OR CAMPAIGN STRUCTURE
SATISFY FIXED COUNT / RANGE
PRESERVE RESERVED CATEGORIES
```

For each cluster preserve fields needed by the current job. A strong baseline is:

```text
CLUSTER_ID
CLUSTER_NAME
USER_TASK
PRIMARY_OBJECT
OBJECT_SCOPE
EXPECTED_TERMINAL_RESULT
ALLOWED ACTIONS / INTENTS
INCLUSION RULE
EXCLUSION RULE
MATERIAL BOUNDARIES
NEAREST SIBLING CLUSTERS
ABSORBED MODIFIERS
LOCAL TERMS AND ALIASES
EXACT EXCEPTIONS
EVIDENCE STATE
COUNT-CONSTRAINT ROLE
SPLIT / MERGE JUSTIFICATION
STATUS = ACTIVE | RESERVED | REJECTED | OTHER
```

### Controlled taxonomy mutation

Taxonomy mutation during assignment is allowed when declared by the current mode.

Each mutation should record:

```text
WHEN
WHY
AFFECTED CLUSTERS
AFFECTED ROWS
COUNT EFFECT
VALIDATION SCOPE
```

For large fresh runs, batch review and a frozen assignment version remain the preferred default.

---

## 8. Row assignment

For every phrase:

1. preserve original text and provenance;
2. apply the current domain profile;
3. apply site/business scope;
4. attach evidence whose declared scope includes the row;
5. derive the task signature and expected result;
6. apply current cluster contracts;
7. apply current target count, range or category constraints;
8. apply exact local rules when relevant;
9. assign, defer, search, create/adapt a candidate, or request owner decision according to the current mode;
10. record confidence and decisive reasoning.

Possible states include:

```text
ASSIGNED
BOUNDARY_REVIEW
SEARCH_REQUIRED
NEW_CLUSTER_CANDIDATE
DEFERRED
OWNER_DECISION_REQUIRED
RESERVED_CATEGORY_MATCH
```

A current job may require all rows to be assigned. In that case fallback or low-confidence decisions are allowed when clearly marked.

---

## 9. Exact rules, tokens and automation

Automation may use any technique appropriate to the current task:

```text
TOKENS
REGEX
DICTIONARIES
EMBEDDINGS
LLM CLASSIFICATION
SERP OVERLAP
SITE DATA
EXACT PHRASE TABLES
BRAND / MODEL TABLES
LOCAL CLUSTER IDS
DOMAIN-SPECIFIC PRECEDENCE RULES
OWNER-PROVIDED MAPPINGS
```

A token or regex can be a candidate signal or a decisive rule depending on the current domain contract.

For material automated rules preserve as applicable:

```text
RULE ID
SCOPE
POSITIVE CONDITION
DISQUALIFIERS
EXPECTED OUTPUT
EVIDENCE OR OWNER SOURCE
POSITIVE TESTS
NEGATIVE TESTS
IMPACT SET
```

Exact local rules are valid. Their scope must be explicit.

---

## 10. Evidence use

The current job defines evidence coverage and generalization rules.

Possible modes:

```text
EXACT-ROW-ONLY EVIDENCE
EXPLICIT FAMILY-LEVEL EVIDENCE
DOMAIN-RULE GENERALIZATION
FULL-CORPUS SEARCH VALIDATION
TARGETED BOUNDARY SEARCH
NO SEARCH EVIDENCE
```

Evidence may be transferred beyond an exact row only when its declared scope or an approved generalization rule allows it.

SERP overlap thresholds, similarity thresholds and other numeric settings are allowed when defined for the current project.

No one threshold is assumed automatically for every project.

---

## 11. Independent QA

A strong baseline is independent row-level review against the current cluster contracts.

The reviewer may receive:

```text
PHRASE
ASSIGNED CLUSTER
CURRENT CLUSTER CONTRACT
CURRENT DOMAIN PROFILE EXCERPT
RELEVANT EVIDENCE
CURRENT COUNT / CATEGORY CONSTRAINT
```

Whether prior assignment reasoning is hidden or shown depends on the QA design.

Possible verdicts:

```text
PASS
FAIL
ACCEPTED UNDER CONSTRAINT
OWNER DECISION REQUIRED
```

For failures preserve:

```text
EXPECTED TASK
ERROR CLASS
EXPECTED CLUSTER OR ACTION
TAXONOMY CHANGE NEEDED
COUNT EFFECT
RATIONALE
```

### QA coverage modes

```text
FULL ROW QA
STRATIFIED SAMPLE QA
CLUSTER-LEVEL QA
RISK-BASED QA
OWNER REVIEW
COMBINATION
```

Full row QA is preferred for high-risk or previously unstable corpora. Another mode is valid when explicitly selected and sufficient for the current deliverable.

---

## 12. Correction modes

### Consolidated correction

Preferred for large corpora:

```text
COMPLETE ERROR DISCOVERY
-> ROOT-CAUSE GROUPING
-> ONE CONSOLIDATED CORRECTION
-> REGRESSION
```

### Iterative correction

Allowed when required by owner instruction, incremental data, tool limits, experiments or staged delivery.

Each iteration records:

```text
INPUT VERSION
DISCOVERED ERRORS
RULE / TAXONOMY CHANGE
EXPECTED IMPACT SET
COUNT EFFECT
VALIDATION
OUTPUT VERSION
```

The control objective is to avoid hidden and unbounded patching, not to prohibit legitimate additional runs.

---

## 12A. Atomic correction materialization

A correction that changes a row's canonical task/cluster identity is one semantic transaction, not an identifier-only patch.

```text
CORRECTED CANONICAL ID
-> LOAD TARGET CLUSTER / TASK CONTRACT
-> REBUILD EVERY CONTRACT-DERIVED ROW FIELD
-> PRESERVE INDEPENDENT SOURCE FIELDS
-> RECOMPUTE IMPACTED SUMMARIES / HANDOFFS
-> COMPARE CORRECTED ROW AGAINST TARGET CONTRACT
-> QA + READBACK
```

Equivalent derived fields include, when governed by the current contract:

```text
user task
intent / execution mode
business fit or scope
expected result/page role
canonical owner class
confidence/maturity reason
other cluster-derived metadata
```

Fields proven independent may be retained, but the proof must be explicit. A row containing a new canonical ID together with metadata inherited from the old canonical object fails semantic QA even when counts and IDs reconcile.

Required checks:

```text
CORRECTED_ROWS_WITH_TARGET_CONTRACT_MISMATCH = 0
IDENTIFIER_ONLY_CORRECTIONS = 0
DEPENDENT_SUMMARIES_LEFT_ON_OLD_ASSIGNMENT = 0
UNRESOLVED_TO_RESOLVED_WITHOUT_EVIDENCE_LINEAGE = 0
```
## 13. Accounting and regression

After material changes verify applicable items:

```text
TOTAL ROW PRESERVATION
ACTIVE ROW PRESERVATION
NO SILENT DROPS
STATUS COUNTS
ASSIGNMENT COUNTS
EXPECTED CHANGES
UNEXPECTED CHANGES
DUPLICATE-GROUP HANDLING
EVIDENCE-LINK PRESERVATION
UNRESOLVED-STATE ACCOUNTING
COUNT / RANGE COMPLIANCE
REQUIRED CATEGORY COVERAGE
RESERVED CATEGORY REPORTING
```

Machine regression proves accounting and change control. Semantic correctness still requires the selected semantic QA mode.

---

## 14. Impact-set review

After corrections, review the provable impact set as applicable:

```text
CHANGED ROWS
ROWS IN CHANGED CLUSTERS
ROWS IN MERGED OR SPLIT CLUSTERS
SIBLING CLUSTERS ACROSS CHANGED BOUNDARIES
ROWS AFFECTED BY A CHANGED LOCAL RULE
ROWS AFFECTED BY A COUNT-CONSTRAINT CHANGE
ROWS AFFECTED BY A DOMAIN-PROFILE CHANGE
STATE TRANSITIONS
NEW OR RETIRED CLUSTERS
```

A full-corpus recheck is used when impact cannot be bounded reliably or the current QA plan requires it.

---

## 15. Empty, reserved and retired clusters

The current output may contain:

```text
ACTIVE CLUSTER WITH MEMBERS
REQUIRED RESERVED EMPTY CATEGORY
FUTURE CATEGORY
RETIRED CANDIDATE
REJECTED CANDIDATE
```

All are legitimate states when the current taxonomy mode supports them.

Reporting must distinguish them. An empty reserved category must not be falsely presented as an evidence-backed active cluster unless that is the declared reporting convention.

---

## 16. Step boundary

Step 10 produces the clustering result required by the current job.

Whether Step 10 also includes page ownership, campaign grouping, site architecture or another downstream decision depends on the current roadmap and deliverable.

Default roadmap separation may keep those decisions in later steps, but an explicitly combined job is allowed.

```text
STEP BOUNDARY = CURRENT ROADMAP CONFIGURATION
```

---

## 17. Final acceptance gate template

Instantiate the applicable current values:

```text
INPUTS_DECLARED = true
CURRENT_DOMAIN_PROFILE_DEFINED = true
CURRENT_SITE_AND_BUSINESS_SCOPE_DEFINED = true
CURRENT_EXECUTION_MODE_DECLARED = true
CURRENT_TAXONOMY_MODE_DECLARED = true
CURRENT_COUNT_MODE_DECLARED = true
CURRENT_EVIDENCE_MODE_DECLARED = true
CURRENT_UNCERTAINTY_MODE_DECLARED = true
CURRENT_QA_MODE_DECLARED = true
REQUIRED_ROWS_ACCOUNTED = CURRENT_REQUIRED_TOTAL
CURRENT_CLUSTER_CONSTRAINTS_SATISFIED = true
REQUIRED_CATEGORIES_ACCOUNTED = true
LOCAL_RULES_SCOPED = true
EVIDENCE_SCOPE_PRESERVED = true
CURRENT_SEMANTIC_QA = PASS
CURRENT_ACCOUNTING_QA = PASS
CORRECTED_ROWS_WITH_TARGET_CONTRACT_MISMATCH = 0
IDENTIFIER_ONLY_CORRECTIONS = 0
DEPENDENT_SUMMARIES_LEFT_ON_OLD_ASSIGNMENT = 0
UNRESOLVED_TO_RESOLVED_WITHOUT_EVIDENCE_LINEAGE = 0
UNEXPECTED_ASSIGNMENT_CHANGES = 0
OWNER / CLIENT ACCEPTANCE = CURRENT_REQUIRED_STATE
```

Optional job-specific gates may include:

```text
EXACT_TARGET_CLUSTER_COUNT_MATCHED
TARGET_RANGE_MATCHED
FULL_ROW_QA_COMPLETE
RESERVED_EMPTY_CATEGORIES_PRESERVED
SERP_BOUNDARY_REVIEW_COMPLETE
ALL_ROWS_ASSIGNED
UNRESOLVED_ROWS_EXPLICIT
```

---

## 18. Method origin

The framework combines reusable clustering principles with configurable project controls.

Direct external references may support search-intent compatibility, SERP overlap, soft/hard clustering and human review. They do not eliminate the need to apply the actual subject, site, business, owner and deliverable constraints.

Current references:

- Ahrefs, keyword clustering: https://ahrefs.com/blog/keyword-clustering/
- Pixel Tools, query clustering by search results: https://tools.pixelplus.ru/optimization/seo-raspredelenie-i-klasterizaciya-zaprosov
- Pixel Tools, grouping FAQ: https://tools.pixelplus.ru/faq/gruppirovka
- Rush Analytics, semantic-core clustering: https://www.rush-analytics.ru/land/klasterizaciya-zaprosov-semanticheskogo-yadra-po-yandex-i-google
- Keyword Insights, clustering types: https://docs.keywordinsights.ai/learning-center/the-features/keyword-clustering/the-advanced-settings/clustering-types

---

## 19. Permanent markers

```text
STEP10_SORTING_QA_METHOD_ACTIVE = true
STEP10_UNIVERSAL_FRAMEWORK_IS_CONFIGURABLE = true
STEP10_DOMAIN_PROFILE_ALLOWED = true
STEP10_DOMAIN_PROFILE_REQUIRED_WHEN_NEEDED = true
STEP10_SITE_AND_BUSINESS_DATA_ALLOWED = true
STEP10_REAL_CLUSTER_IDS_AND_NAMES_ALLOWED = true
STEP10_EXACT_LOCAL_RULES_ALLOWED = true
STEP10_JOB_SPECIFIC_THRESHOLDS_ALLOWED = true
STEP10_EXPLICIT_TARGET_COUNT_OR_RANGE_ALLOWED = true
STEP10_EXISTING_TAXONOMY_REUSE_ALLOWED = true
STEP10_FRESH_INDEPENDENT_REBUILD_ALLOWED = true
STEP10_CONTROLLED_TAXONOMY_MUTATION_ALLOWED = true
STEP10_RESERVED_EMPTY_CATEGORIES_ALLOWED = true
STEP10_FULL_ROW_QA_AVAILABLE = true
STEP10_ALTERNATIVE_QA_MODES_ALLOWED_WHEN_DECLARED = true
STEP10_CONSOLIDATED_CORRECTION_PREFERRED_FOR_LARGE_CORPORA = true
STEP10_ITERATIVE_CORRECTION_ALLOWED_WHEN_SCOPED = true
STEP10_CANONICAL_ASSIGNMENT_CORRECTION_IS_ATOMIC = true
STEP10_CORRECTED_ROWS_MUST_MATCH_TARGET_CONTRACT = true
STEP10_IDENTIFIER_ONLY_CORRECTION_FORBIDDEN = true
STEP10_EVIDENCE_GENERALIZATION_ALLOWED_WHEN_DECLARED = true
STEP10_CURRENT_JOB_CONSTRAINTS_ARE_EXECUTABLE_INPUTS = true
```
