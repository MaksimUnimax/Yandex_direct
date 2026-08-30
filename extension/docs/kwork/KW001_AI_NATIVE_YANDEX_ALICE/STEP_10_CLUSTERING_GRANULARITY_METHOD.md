# KW-001 — STEP 10 CLUSTERING GRANULARITY METHOD

Date approved: 2026-08-30  
Status: **APPROVED / ACTIVE / UNIVERSAL / OWNER-LOCKED**

This file defines the permanent universal Step-10 rule for controlling clustering granularity.

It is methodology only. It must not contain client-specific phrases, sites, cluster counts, cluster IDs, job histories or job-specific thresholds.

---

## STEP PURPOSE

Step 10 groups active search phrases into defensible user-task / search-intent clusters without either:

```text
OVER-SPLITTING -> inventing a new cluster for every modifier, wording nuance or individual correction
UNDER-SPLITTING -> merging materially different user tasks merely because the object or wording is similar
```

The number of clusters is an output of evidence-backed boundaries. It is never a target, quota or quality metric by itself.

Canonical rule:

```text
TARGET_CLUSTER_COUNT = FORBIDDEN
CLUSTER_COUNT = RESULT_OF_VALIDATED_BOUNDARIES
```

---

## CORE GRANULARITY PRINCIPLE

The default state is to keep a phrase inside an existing compatible task cluster.

A new cluster is an exception that must earn the right to exist.

Canonical rules:

```text
DEFAULT = KEEP_IN_EXISTING_COMPATIBLE_CLUSTER
NO_NEW_CLUSTER_WITHOUT_MATERIAL_SPLIT_EVIDENCE
NO_MERGE_IF_MATERIAL_USER_TASK_DIFFERS
UNCERTAINTY != NEW_CLUSTER
```

A phrase must not create a new cluster merely because it contains a new token, modifier, formulation or previously unseen combination.

---

## MATERIAL SPLIT EVIDENCE

A new cluster may be created only when at least one material boundary is established and the parent cluster can no longer truthfully represent the task.

Valid split evidence may include:

```text
1. DIFFERENT END USER GOAL / TASK OUTCOME
2. DIFFERENT ACTION OR LIFECYCLE TASK
3. DIFFERENT PRIMARY OBJECT/SERVICE WHERE THE REQUIRED ANSWER OR OFFER CHANGES MATERIALLY
4. DIFFERENT INTENT / RESULT TYPE THAT CANNOT BE SATISFIED BY THE SAME PRIMARY RESPONSE
5. DIFFERENT PAGE-TYPE NEED / SAME-PAGE INCOMPATIBILITY
6. DIRECT SERP EVIDENCE SHOWING A STABLE MATERIAL BOUNDARY
```

No one signal is universally sufficient in every domain. The analyst must explain the causal reason the split is material.

Required question:

```text
WHAT DIFFERENT USER TASK DOES THE NEW CLUSTER SOLVE THAT THE PARENT CLUSTER CANNOT REPRESENT?
```

If that cannot be answered concretely, the split is not approved.

---

## SAME-PAGE COMPATIBILITY TEST

Before creating a new cluster, evaluate whether both phrase sets can be satisfied by one normal primary page/task response without changing its central intent, page type or principal user outcome.

```text
SAME_PRIMARY_PAGE_CAN_SATISFY_BOTH = strong evidence against split
SAME_PRIMARY_PAGE_CANNOT_SATISFY_BOTH = split candidate
UNCLEAR = preserve uncertainty / inspect SERP
```

This is an intent/granularity test. It is not final page ownership and does not authorize Step-11 architecture decisions.

Canonical separation:

```text
STEP10_SAME_PAGE_COMPATIBILITY_TEST != STEP11_PAGE_OWNERSHIP
```

---

## MODIFIER NON-TRIGGER RULE

The following are attributes/modifiers by default and must not create a new cluster automatically:

```text
GEO
BRAND
MODEL
COLOR
SIZE / DIMENSION
PRICE WORDING
YEAR
MATERIAL
HOUSE / SERIES / TYPE LABEL
NUMBER OF COMPONENTS / LEAVES / UNITS
CHEAP / PREMIUM / DISCOUNT WORDING
MANUFACTURER WORDING
TURNKEY WORDING
LEXICAL FORM / WORD ORDER / MORPHOLOGY
FREQUENCY / VOLUME
ACQUISITION SOURCE / SEED / PROVENANCE
```

A modifier may support a split only after material task/page/SERP evidence demonstrates that it changes the search task rather than merely refining the same task.

Canonical rule:

```text
MODIFIER_PRESENT != NEW_CLUSTER
```

---

## CLUSTER CREATION MUST BE SEPARATE FROM ROW CLASSIFICATION

Phrase assignment and taxonomy creation are separate analytical operations.

Forbidden pattern:

```text
READ ONE PHRASE
-> IT DOES NOT FIT PERFECTLY
-> CREATE NEW CLUSTER IMMEDIATELY
-> CONTINUE
```

Required pattern:

```text
DISCOVER / CLASSIFY FULL DECLARED CORPUS
-> COLLECT ALL NEW_CLUSTER_CANDIDATE ITEMS
-> REVIEW ALL CANDIDATES TOGETHER
-> APPLY MATERIAL SPLIT GATE
-> NORMALIZE TAXONOMY
-> FREEZE CLUSTER DICTIONARY
-> REASSIGN / VERIFY FULL CORPUS
```

Canonical rules:

```text
CLUSTER_CREATION != PHRASE_CLASSIFICATION
ROW_ERROR_CORRECTION_CANNOT_AUTO_CREATE_CLUSTER = true
NEW_CLUSTER_CANDIDATES_ARE_BATCH_REVIEWED = true
```

---

## NEW CLUSTER JUSTIFICATION LEDGER

Every new cluster created after an existing candidate taxonomy has been formed must have an auditable justification record.

At minimum record:

```text
candidate cluster ID / label
parent or nearest existing cluster
phrase set requesting the split
material user-task difference
same-page compatibility result
SERP evidence state if used
reason parent cluster is insufficient
review decision: CONFIRMED / REJECTED / SEARCH_REQUIRED
```

No justification record -> no new cluster.

Canonical rule:

```text
NEW_CLUSTER_WITHOUT_JUSTIFICATION_LEDGER = FAIL
```

---

## MICROCLUSTER / SINGLETON CONTROL

Small clusters and singleton clusters are not automatically wrong and must not be auto-merged solely by size.

However, they receive mandatory granularity review because they are high-risk for accidental over-splitting.

```text
SMALL_CLUSTER != BAD_CLUSTER
SINGLETON != AUTOMATIC_ERROR
SMALL_CLUSTER -> MANDATORY_SPLIT_JUSTIFICATION_REVIEW
```

Any numerical definition of `small` used for QA triggering is an internal workflow parameter, not an industry truth and must not become an automatic merge rule.

---

## UNCERTAINTY CONTROL

When a potential split is plausible but not proven:

```text
DO NOT CREATE A NEW CLUSTER TO REMOVE UNCERTAINTY
```

Use an explicit unresolved state such as:

```text
NEW_CLUSTER_CANDIDATE
SPLIT_UNPROVEN
BOUNDARY_REVIEW
SEARCH_REQUIRED
```

Exact status names may vary by implementation. The invariant is that uncertainty remains visible rather than being converted into taxonomy growth.

Canonical rule:

```text
UNCERTAINTY_PRESERVATION > FALSE_TAXONOMY_PRECISION
```

---

## CONSISTENCY-OF-SPLIT-AXIS CONTROL

A taxonomy must not split one family by action, another by modifier, another by brand, and another by geography without evidence explaining why those axes are material in each case.

For every split family ask:

```text
WHAT AXIS IS CAUSING THE SPLIT?
IS THAT AXIS MATERIAL TO USER TASK / PAGE COMPATIBILITY / SERP?
IS THE SAME AXIS HANDLED CONSISTENTLY ACROSS SIBLING PHRASES?
```

Inconsistent handling of the same modifier or boundary is a QA failure unless explicit evidence explains the difference.

---

## MERGE CONTROL

The anti-fragmentation rule must not become a forced-merge rule.

Do not merge phrases merely to reduce cluster count when they materially differ by user task, required result type, commercial/informational purpose, lifecycle action, primary object or validated SERP boundary.

Canonical rule:

```text
LOWER_CLUSTER_COUNT != BETTER_CLUSTERING
MERGE_REQUIRES_TASK_COMPATIBILITY
```

---

## KNOWN FAILURE MODES PREVENTED

### Failure A — endless taxonomy growth

Cause:

```text
new nuance / modifier / discovered error -> immediate new cluster
```

Control:

```text
batch candidate review + material split gate + justification ledger
```

### Failure B — broad bucket swallowing distinct tasks

Cause:

```text
same object / lexical similarity treated as sufficient merge proof
```

Control:

```text
user-task distinction + same-page compatibility + SERP review where materially uncertain
```

### Failure C — cluster count used as target

Cause:

```text
analyst attempts to reach a preferred number of clusters
```

Control:

```text
no target count; count is the consequence of validated boundaries
```

### Failure D — uncertainty converted into false precision

Cause:

```text
ambiguous phrase gets a new cluster because no existing cluster feels perfect
```

Control:

```text
preserve unresolved state instead of inventing taxonomy
```

---

## EXTERNAL METHOD SUPPORT

The permanent rule is supported by current industry clustering guidance that clusters are fundamentally about shared search intent / page compatibility, with SERP overlap used as evidence and with known trade-offs between broader and stricter clustering.

Direct methodology references:

- Ahrefs — Keyword Clustering: https://ahrefs.com/blog/keyword-clustering/
- SE Ranking — Comprehensive Guide to Keyword Clustering: https://seranking.com/blog/keyword-clustering/
- SE Ranking — How to start keyword grouping: https://help.seranking.com/hc/en-us/articles/16332627413148-How-to-start-keyword-grouping
- Rush Analytics — keyword clustering guide: https://www.rush-analytics.ru/faq/klasterizaciya-zaprosov-semanticheskogo-yadra-rukovodstvo
- Keyword Insights — clustering types / centroid vs agglomerative trade-off: https://docs.keywordinsights.ai/learning-center/the-features/keyword-clustering/the-advanced-settings/clustering-types

These sources do not prescribe one universal cluster count. The exact internal states, ledgers and pass-gate mechanics above are project controls derived from the supported principles and owner-approved to prevent repeatable over-splitting and under-splitting failures.

---

## SOURCE-TO-METHOD TRACE

```text
shared / similar search intent
-> task compatibility is the primary clustering unit

same or materially overlapping SERP / same ranking-page pattern
-> evidence for same-page compatibility or boundary review

soft vs hard / centroid vs stricter pairwise clustering trade-off
-> no universal correct cluster count; strictness changes granularity

manual review after automated grouping
-> machine grouping cannot self-accept semantic boundaries

project-observed over-splitting risk
-> new-cluster burden of proof + justification ledger

project-observed under-splitting risk
-> no forced merge merely to reduce count
```

---

## PASS GATE

Step-10 taxonomy cannot pass unless all of the following are true:

```text
TARGET_CLUSTER_COUNT_USED = false
NEW_CLUSTER_WITHOUT_MATERIAL_JUSTIFICATION = 0
NEW_CLUSTER_CREATED_DURING_SINGLE_ROW_PATCH = 0
UNREVIEWED_NEW_CLUSTER_CANDIDATES = 0
MODIFIER_ONLY_SPLITS_WITHOUT_EVIDENCE = 0
UNEXPLAINED_SPLIT_AXIS_INCONSISTENCIES = 0
FORCED_MERGES_ACROSS_MATERIAL_USER_TASKS = 0
UNRESOLVED_BOUNDARIES_HIDDEN_AS_CONFIRMED_CLUSTERS = 0
MICROCLUSTERS_REVIEWED_FOR_SPLIT_JUSTIFICATION = true
FULL_DECLARED_CORPUS_ACCOUNTED = true
SEMANTIC_BOUNDARY_QA = PASS
```

Machine/accounting success alone is insufficient.

---

## PERMANENT MARKERS

```text
KW001_STEP10_GRANULARITY_METHOD_APPROVED = true
KW001_STEP10_TARGET_CLUSTER_COUNT_FORBIDDEN = true
KW001_STEP10_NO_NEW_CLUSTER_WITHOUT_MATERIAL_SPLIT_EVIDENCE = true
KW001_STEP10_MODIFIER_NOT_CLUSTER_TRIGGER = true
KW001_STEP10_CLUSTER_CREATION_SEPARATE_FROM_ROW_CLASSIFICATION = true
KW001_STEP10_NEW_CLUSTER_JUSTIFICATION_LEDGER_REQUIRED = true
KW001_STEP10_MICROCLUSTER_REVIEW_REQUIRED = true
KW001_STEP10_UNCERTAINTY_CANNOT_CREATE_CLUSTER = true
KW001_STEP10_NO_FORCED_MERGE_FOR_COUNT_REDUCTION = true
KW001_STEP10_SPLIT_AXIS_CONSISTENCY_REQUIRED = true
```

Status: **APPROVED / ACTIVE / UNIVERSAL / OWNER-LOCKED**.
