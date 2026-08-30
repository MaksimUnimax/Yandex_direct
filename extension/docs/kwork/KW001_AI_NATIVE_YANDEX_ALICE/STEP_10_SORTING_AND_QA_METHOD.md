# Step 10 — Universal Sorting and QA Method

Status: **APPROVED / ACTIVE / UNIVERSAL / OWNER-LOCKED**

This file defines the universal execution method for Step 10 user-task / SERP clustering.

It is deliberately job-independent. It must not contain client-specific phrases, sites, current cluster counts, cluster IDs, or job history.

Canonical companion authority:

`STEP_10_CLUSTERING_GRANULARITY_METHOD.md`

---

## 1. Purpose

Step 10 must transform a frozen pre-clustering semantic corpus and available direct Search/SERP evidence into a defensible set of user-task clusters without:

- inventing a target number of clusters;
- creating taxonomy while classifying one row;
- allowing modifiers or lexical variation to create clusters by default;
- silently transferring direct SERP evidence to unprobed phrases;
- accepting the classifier's own assignments without independent row-level review;
- repeatedly correcting the first discovered error and restarting the whole corpus.

The execution baseline is:

```text
3 FULL SEMANTIC PASSES + CONDITIONAL IMPACT RECHECK
```

The three full passes have different purposes and must not be collapsed into one self-confirming operation.

---

## 2. Governing equations

```text
TASK_DISCOVERY != FINAL_CLUSTER_CREATION
CLUSTER_CREATION != PHRASE_CLASSIFICATION
ASSIGNMENT != INDEPENDENT_QA
SAMPLE_QA != FULL_ROW_SEMANTIC_QA
ACCOUNTING_QA != SEMANTIC_QA
MACHINE_REGRESSION != SEMANTIC_CORRECTNESS
DISCOVERY != CORRECTION
UNCERTAINTY != NEW_CLUSTER
MODIFIER_PRESENT != NEW_CLUSTER
TARGET_CLUSTER_COUNT = FORBIDDEN
NO_NEW_CLUSTER_WITHOUT_MATERIAL_SPLIT_EVIDENCE
```

The granularity rules in `STEP_10_CLUSTERING_GRANULARITY_METHOD.md` remain binding throughout this method.

---

## 3. Input freeze and contamination control

Before Pass 1:

1. identify the canonical outputs of the immediately preceding semantic/search stages;
2. record their exact repository paths, versions/blob identifiers and, where available, frozen content hashes;
3. freeze an input manifest;
4. record all historical Step-10 results as comparison-only baselines;
5. do not read historical cluster dictionaries, assignments, classifier logic or cluster-level QA before the fresh candidate taxonomy is frozen when an independent rebuild is required.

Required principle:

```text
HISTORICAL_RESULT_FOR_COMPARISON != INPUT_TO_INDEPENDENT_REBUILD
```

A fresh rebuild must not inherit cluster names, counts, boundaries or row assignments merely because they already exist.

---

## 4. Pass 1 — 100% task discovery

### 4.1 Objective

Review every active phrase to identify the user's task before final cluster IDs exist.

Pass 1 is not an assignment pass.

### 4.2 Required row-level semantic fields

Each row should preserve, when applicable:

```text
PRIMARY_OBJECT
ACTION_OR_USER_GOAL
INTENT
LIFECYCLE_STAGE
EXPECTED_RESULT_TYPE
MATERIAL_MODIFIERS
BUSINESS_FIT
BOUNDARY_UNCERTAINTY
PROVISIONAL_TASK_SIGNATURE
```

These are analytical descriptors, not final taxonomy.

### 4.3 Prohibitions

During Pass 1:

```text
FINAL_CLUSTER_ID_CREATION = FORBIDDEN
TARGET_CLUSTER_COUNT = FORBIDDEN
HISTORICAL_CLUSTER_MATCHING = FORBIDDEN_IN_INDEPENDENT_REBUILD
```

Encountering a new lexical form, brand, model, location, price qualifier, dimension, color, material, series, source, frequency or similar modifier does not by itself establish a new user task.

### 4.4 Pass gate

```text
ACTIVE_ROWS_REVIEWED = ACTIVE_ROWS_TOTAL
UNREVIEWED = 0
FINAL_CLUSTER_IDS_CREATED_DURING_PASS1 = 0
```

---

## 5. Taxonomy normalization — between Pass 1 and Pass 2

This is a consolidated taxonomy operation over completed Pass-1 task signatures. It is not another row-by-row discovery pass.

### 5.1 Build candidate task families

Normalize semantically equivalent task signatures and separate materially different tasks.

Default behaviour:

```text
SAME_MATERIAL_USER_TASK -> SAME_CANDIDATE_CLUSTER
MODIFIER_ONLY_DIFFERENCE -> ATTRIBUTE_BY_DEFAULT
UNCLEAR_BOUNDARY -> BOUNDARY_REVIEW_OR_SEARCH_REQUIRED
POSSIBLE_NOVEL_TASK -> NEW_CLUSTER_CANDIDATE
```

### 5.2 Material split gate

Every proposed new cluster must satisfy `STEP_10_CLUSTERING_GRANULARITY_METHOD.md`.

A split must be justified by a material difference such as:

- a different user action or desired outcome;
- a materially different object of demand;
- a different lifecycle stage where that changes the task;
- a different expected result/content type;
- strong direct SERP evidence that the same-page hypothesis is false.

Lexical or modifier difference alone is insufficient.

### 5.3 Same-page test

For a proposed split, ask:

> Can one coherent page satisfy both query groups without changing its primary user task, expected result type or core page purpose?

If yes, split is rejected by default.

If clearly no, the split may pass semantic review.

If unclear, preserve the boundary as unresolved and use available direct SERP evidence or targeted Search review rather than inventing taxonomy.

### 5.4 Batch candidate review

All `NEW_CLUSTER_CANDIDATE` items must be reviewed together.

Do not create clusters opportunistically while handling one phrase.

For every accepted cluster preserve at least:

```text
CLUSTER_ID
USER_TASK
PRIMARY_OBJECT
ALLOWED_ACTION_OR_INTENT
INCLUSION_RULE
EXCLUSION_RULE
MATERIAL_BOUNDARIES
NEAREST_SIBLING_CLUSTERS
SERP_EVIDENCE_STATE
SPLIT_JUSTIFICATION
```

### 5.5 Microcluster review

A very small cluster is a QA trigger, not an automatic error and not an automatic merge.

Every microcluster must explicitly justify why it represents a material task boundary rather than a modifier or lexical variant.

### 5.6 Taxonomy freeze gate

Before Pass 2:

```text
CANDIDATE_TAXONOMY_NORMALIZED = true
NEW_CLUSTER_CANDIDATES_BATCH_REVIEWED = true
TARGET_CLUSTER_COUNT_USED = false
UNJUSTIFIED_NEW_CLUSTERS = 0
CLUSTER_DICTIONARY_FROZEN = true
```

---

## 6. Pass 2 — 100% assignment against frozen taxonomy

### 6.1 Objective

For every active phrase, determine whether it fits an already frozen cluster contract.

Allowed states:

```text
ASSIGN_TO_EXISTING_CLUSTER
BOUNDARY_REVIEW
SEARCH_REQUIRED
NEW_CLUSTER_CANDIDATE
```

### 6.2 Prohibitions during Pass 2

```text
CREATE_NEW_CLUSTER = FORBIDDEN
RENAME_CLUSTER = FORBIDDEN
CHANGE_CLUSTER_DEFINITION = FORBIDDEN
TARGET_CLUSTER_COUNT_OPTIMIZATION = FORBIDDEN
```

A row that does not fit the frozen dictionary must not mutate the dictionary in place.

### 6.3 Candidate accumulation

All new-task suspicions discovered in Pass 2 are accumulated to completion and reviewed in one consolidated batch only after every row has been classified.

If the batch changes taxonomy, affected rows must be reassigned under the changed frozen dictionary before independent QA begins.

### 6.4 Pass gate

```text
ACTIVE_ROWS_CLASSIFIED = ACTIVE_ROWS_TOTAL
UNCLASSIFIED = 0
IN_PASS_TAXONOMY_MUTATIONS = 0
NEW_CLUSTER_CANDIDATES_ACCOUNTED = ALL
```

---

## 7. Pass 3 — 100% independent row QA

### 7.1 Objective

Independently test every assignment rather than asking the assignment classifier to approve itself.

For each row, the reviewer receives only the information needed to adjudicate the assignment, normally:

```text
PHRASE
ASSIGNED_CLUSTER
CLUSTER_DEFINITION
RELEVANT_DIRECT_EVIDENCE_IF_ANY
```

The reviewer must not be shown Pass-2 reasoning when avoidable.

### 7.2 Required verdict

Every active row receives:

```text
PASS
or
FAIL
```

For FAIL preserve:

```text
EXPECTED_TASK
ERROR_CLASS
NEAREST_CORRECT_CLUSTER_IF_ANY
NEW_CLUSTER_REQUIRED = NO | CANDIDATE
RATIONALE
```

### 7.3 No correction during discovery

Do not repair the first error and restart.

Required sequence:

```text
FREEZE_CANDIDATE
-> FULL_QA_DISCOVERY_TO_COMPLETION
-> COLLECT_ALL_FAILURES_WITHOUT_CORRECTION
-> FREEZE_COMPLETE_ERROR_LEDGER
```

### 7.4 Full-row requirement

Sampled cluster QA can supplement Pass 3 but cannot replace it.

```text
SAMPLE_QA_PASS != FULL_ROW_QA_PASS
```

### 7.5 Pass gate

```text
QA_ROWS = ACTIVE_ROWS_TOTAL
UNREVIEWED = 0
ERROR_LEDGER_FROZEN = true
CORRECTIONS_DURING_PASS3 = 0
```

---

## 8. Consolidated correction

After the complete Pass-3 error ledger is frozen:

1. group failures by semantic root cause;
2. distinguish row-assignment errors from taxonomy-boundary errors;
3. resolve all supported corrections in one consolidated batch;
4. send any newly suspected cluster through the material split gate and batch candidate review;
5. do not create a cluster merely to make an individual failing row fit somewhere.

Required pattern:

```text
FULL_ERROR_LEDGER
-> ROOT_CAUSE_GROUPING
-> ONE_CONSOLIDATED_CORRECTION_BATCH
```

---

## 9. Full N/N machine regression

After every consolidated correction, reconcile the entire corpus mechanically.

At minimum verify:

```text
TOTAL_ROW_PRESERVATION
ACTIVE_ROW_PRESERVATION
NO_SILENT_DROPS
EXPECTED_STATUS_COUNTS
EXPECTED_ASSIGNMENT_CHANGES
UNEXPECTED_ASSIGNMENT_CHANGES
DUPLICATE_GROUP_PRESERVATION
DIRECT_EVIDENCE_LINK_PRESERVATION
UNRESOLVED_STATE_ACCOUNTING
```

Machine regression proves accounting and change control. It does not prove semantic correctness.

```text
MACHINE_REGRESSION_PASS != SEMANTIC_QA_PASS
```

---

## 10. Conditional impact-set semantic recheck

A successful full machine regression does not require another full semantic pass by default.

Re-review the complete semantic impact set, including:

1. every row whose assignment changed;
2. every row in a cluster whose definition changed;
3. every row in merged or split clusters;
4. relevant sibling clusters across a changed boundary;
5. every `SEARCH_REQUIRED -> assigned` transition;
6. every `assigned -> SEARCH_REQUIRED` transition;
7. every new-cluster candidate or accepted new cluster;
8. every row potentially affected by a changed classification rule.

Required principle:

```text
SEMANTIC_RECHECK_SCOPE = PROVABLE_IMPACT_SET
```

A new full-corpus semantic pass is required when the correction is structural enough that the provable impact set approaches the whole corpus or when change propagation cannot be bounded reliably.

---

## 11. Residual correction cycle

If the impact recheck finds residual failures:

```text
COLLECT_ALL_RESIDUAL_FAILURES_WITHOUT_CORRECTION
-> FREEZE_RESIDUAL_LEDGER
-> ONE_CONSOLIDATED_RESIDUAL_CORRECTION
-> FULL_N/N_MACHINE_REGRESSION
-> IMPACT_SET_RECHECK
```

Repeat until the acceptance gate is met.

Never return to:

```text
FIND_FIRST_ERROR
-> FIX_IMMEDIATELY
-> RERUN_ALL
-> REPEAT
```

---

## 12. Search/SERP evidence use

Direct SERP evidence is primarily a boundary adjudication signal, not a requirement to probe every phrase.

Prioritize Search review for states such as:

```text
SPLIT_UNPROVEN
MERGE_UNPROVEN
NEW_CLUSTER_CANDIDATE
MICROCLUSTER_WITH_WEAK_JUSTIFICATION
SAME_PAGE_TEST_UNCLEAR
SEMANTIC_TASK_VS_DIRECT_SERP_CONFLICT
```

Direct evidence may be applied only to the phrase/query or explicitly supported comparison for which it exists. Do not silently transfer evidence to unprobed rows merely because they share a cleanup reason, lexical feature, acquisition source or candidate cluster.

No universal fixed SERP-overlap number is treated as truth across all projects.

---

## 13. Final acceptance gate

A Step-10 result may be accepted only when all applicable conditions are true:

```text
INPUT_MANIFEST_FROZEN = true
PASS1_ACTIVE_ROWS_REVIEWED = ACTIVE_ROWS_TOTAL
PASS1_UNREVIEWED = 0
TAXONOMY_NORMALIZED_AND_FROZEN = true
UNJUSTIFIED_NEW_CLUSTERS = 0
PASS2_ACTIVE_ROWS_CLASSIFIED = ACTIVE_ROWS_TOTAL
PASS2_UNCLASSIFIED = 0
PASS2_IN_PASS_TAXONOMY_MUTATIONS = 0
PASS3_QA_ROWS = ACTIVE_ROWS_TOTAL
PASS3_UNREVIEWED = 0
PASS3_CORRECTIONS_DURING_DISCOVERY = 0
COMPLETE_ERROR_LEDGER_FROZEN = true
CONSOLIDATED_CORRECTION_COMPLETE = true
FULL_MACHINE_REGRESSION = PASS
UNEXPECTED_ASSIGNMENT_CHANGES = 0
SILENT_DROPS = 0
IMPACT_SET_REVIEW_COMPLETE = true
RESIDUAL_SEMANTIC_FAIL = 0
DIRECT_SERP_CONTRADICTIONS_UNRESOLVED = 0
TARGET_CLUSTER_COUNT_USED = false
STEP11_DECISIONS_MADE_PREMATURELY = 0
```

Unresolved evidence may remain explicit when the method permits it; it must not be hidden by creating a speculative cluster.

---

## 14. Step boundary

Step 10 decides defensible user-task / SERP-compatible clustering.

Step 10 does **not** by itself decide:

- final existing-page ownership;
- whether a new page must be created;
- structural keep/expand/split/merge/create action;
- cannibalization diagnosis;
- final Search-only site architecture.

Those belong to later governed steps.

```text
STEP10_CLUSTER != AUTOMATIC_FINAL_PAGE
```

---

## 15. Method origin / direct sources

The universal execution design combines direct industry clustering principles with project-level QA controls.

Direct external references used for the clustering boundary model include:

- Ahrefs, keyword clustering: https://ahrefs.com/blog/keyword-clustering/
- Pixel Tools, query clustering by search results: https://tools.pixelplus.ru/optimization/seo-raspredelenie-i-klasterizaciya-zaprosov
- Pixel Tools, grouping FAQ: https://tools.pixelplus.ru/faq/gruppirovka
- Rush Analytics, semantic-core clustering: https://www.rush-analytics.ru/land/klasterizaciya-zaprosov-semanticheskogo-yadra-po-yandex-i-google
- Keyword Insights, clustering types: https://docs.keywordinsights.ai/learning-center/the-features/keyword-clustering/the-advanced-settings/clustering-types

Reusable methodological conclusions:

```text
SEARCH_INTENT_COMPATIBILITY_MATTERS = true
SERP_OVERLAP_CAN_BE_BOUNDARY_EVIDENCE = true
SOFT_VS_HARD_STRICTNESS_CHANGES_GRANULARITY = true
AUTOMATIC_CLUSTERING_REQUIRES_HUMAN_ADJUDICATION = true
NO_INDUSTRY_STANDARD_CLUSTER_COUNT_QUOTA = true
```

---

## 16. Permanent markers

```text
STEP10_SORTING_QA_METHOD_ACTIVE = true
STEP10_BASELINE_FULL_SEMANTIC_PASSES = 3
STEP10_PASS1_TASK_DISCOVERY_ONLY = true
STEP10_TAXONOMY_FREEZE_BEFORE_ASSIGNMENT = true
STEP10_PASS2_FROZEN_DICTIONARY_ASSIGNMENT = true
STEP10_PASS2_TAXONOMY_MUTATION_FORBIDDEN = true
STEP10_PASS3_FULL_INDEPENDENT_ROW_QA = true
STEP10_DISCOVERY_CORRECTION_SEPARATION_REQUIRED = true
STEP10_COMPLETE_ERROR_LEDGER_REQUIRED = true
STEP10_CONSOLIDATED_CORRECTION_REQUIRED = true
STEP10_FULL_MACHINE_REGRESSION_REQUIRED = true
STEP10_CONDITIONAL_IMPACT_RECHECK_ACTIVE = true
STEP10_TARGET_CLUSTER_COUNT_FORBIDDEN = true
STEP10_NEW_CLUSTER_REQUIRES_MATERIAL_SPLIT_EVIDENCE = true
```
