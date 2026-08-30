# Step 10 — Universal Task-First Sorting Decision Method

Status: **APPROVED / ACTIVE / UNIVERSAL / OWNER-LOCKED**

This file defines how Step 10 must decide what a phrase is about and how it is assigned to a user-task cluster.

It is deliberately domain-independent. It must not contain client-specific phrases, sites, products, cluster IDs, target counts, or current-job history.

Canonical companion authorities:

- `STEP_10_CLUSTERING_GRANULARITY_METHOD.md`
- `STEP_10_SORTING_AND_QA_METHOD.md`

---

## 1. Purpose

The method exists to prevent three recurrent failures:

1. guessing a cluster from one visible word;
2. treating modifiers as separate user tasks;
3. discovering one error, adding one narrow rule, rerunning, and repeating an unbounded patch chain.

The required baseline is:

```text
UNDERSTAND THE REQUESTED RESULT
-> EXPRESS A COMPLETE TASK SIGNATURE
-> MATCH THAT SIGNATURE TO A FROZEN CLUSTER CONTRACT
-> PRESERVE UNCERTAINTY WHEN NO CONTRACT FITS
```

A phrase is not clustered by its most conspicuous token. It is clustered by the result the user is trying to obtain.

---

## 2. Governing equations

```text
LEXICAL_MATCH != USER_TASK
OBJECT_WORD != COMPLETE_INTENT
MODIFIER_PRESENT != NEW_CLUSTER
ACTION_WORD_ALONE != FINAL_TASK
REGEX_MATCH != SEMANTIC_DECISION
PRODUCT_WITH_INCLUDED_SERVICE != SERVICE_ONLY_REQUEST
COMPONENT_TASK != WHOLE_OBJECT_TASK
DIY_RESULT != HIRED_SERVICE_RESULT
INFORMATION_RESULT != TRANSACTIONAL_RESULT
UNCERTAINTY != NEW_CLUSTER
ZERO_ASSIGNMENT_CLUSTER != PROVEN_CLUSTER
PASS != VERSIONED_RETRY
```

The unit of clustering is a materially distinct user task, not a keyword shape.

---

## 3. Required task signature

Before assigning a phrase, derive the following semantic signature when the phrase supports it:

```text
PRIMARY_OBJECT
OBJECT_SCOPE = WHOLE_OBJECT | COMPONENT | BUNDLE | UNSPECIFIED
USER_ACTION_OR_GOAL
EXPECTED_TERMINAL_RESULT
INTENT_MODE
LIFECYCLE_STAGE
EXECUTION_MODE = BUY | HIRE | DIY | LEARN | NAVIGATE | INSPIRE | OTHER
BUSINESS_SCOPE_STATE
MATERIAL_MODIFIERS
DIRECT_EVIDENCE_STATE
BOUNDARY_UNCERTAINTY
```

The normalized task signature is:

```text
TASK_SIGNATURE =
PRIMARY_OBJECT
+ OBJECT_SCOPE
+ USER_ACTION_OR_GOAL
+ EXPECTED_TERMINAL_RESULT
+ INTENT_MODE
+ LIFECYCLE_STAGE
+ EXECUTION_MODE
+ BUSINESS_SCOPE_STATE
```

Modifiers are recorded separately. They do not enter the task signature unless evidence shows that they materially change the requested result.

---

## 4. Universal decision order

Every phrase must be resolved in this order. A later signal must not silently override a stronger earlier task signal.

### 4.1 Literal request and negation

Read the complete phrase, including:

- negation;
- prepositions and grammatical relations;
- whether an action applies to a product, component, service, or information request;
- whether one item is included with another;
- whether the user requests the work itself or information about the work.

Do not infer omitted words merely to force the phrase into a known cluster.

```text
NEGATED_ACTION != REQUESTED_ACTION
INCLUDED_ACTION != PRIMARY_ACTION_BY_DEFAULT
```

### 4.2 Exact direct evidence

If direct Search/SERP or other approved evidence exists for the exact phrase, use it to adjudicate the task boundary.

Exact evidence may confirm, refine, or contradict the semantic reading. A contradiction must remain explicit and be reviewed; it must not be hidden.

```text
EXACT_EVIDENCE_FOR_ROW -> MAY_ADJUDICATE_ROW
EVIDENCE_FOR_NEIGHBOUR -> MUST_NOT_BE_INHERITED
```

### 4.3 Explicit scope and navigation

Resolve clear outside-scope, navigational, and destination-seeking tasks before broad product/service attraction.

A phrase requesting a destination, official source, marketplace, unrelated profession, or excluded business result must not be pulled into a core cluster merely because it contains a core object word.

### 4.4 Expected terminal result

Identify what the user expects to possess, receive, perform, understand, compare, view, or reach when the task is complete.

The expected terminal result is normally the strongest semantic head.

Examples of universal result classes:

```text
OBTAIN A PRODUCT
ORDER A COMPLETE BUNDLE
HIRE A PROFESSIONAL ACTION
REPAIR OR RESTORE
REPLACE A WHOLE OBJECT
BUY OR REPLACE A COMPONENT
LEARN TO DO THE ACTION
CHOOSE BETWEEN OPTIONS
COMPARE OPTIONS
READ REVIEWS OR REPUTATION
UNDERSTAND TECHNOLOGY OR FACTS
FIND DIMENSIONS OR SPECIFICATIONS
REACH AN OFFICIAL DESTINATION
VIEW IDEAS OR EXAMPLES
UNDERSTAND RULES OR PERMISSIONS
```

### 4.5 Lifecycle action

Separate materially different lifecycle tasks when they change the requested result:

```text
DISCOVER / CHOOSE
BUY / ORDER
MEASURE / PLAN
INSTALL / CONFIGURE
USE / MAINTAIN
REPAIR / RESTORE
REPLACE
DISMANTLE / REMOVE
REVIEW / COMPARE
```

A shared object does not merge different lifecycle results automatically.

### 4.6 Intent and execution mode

Distinguish at minimum:

```text
TRANSACTIONAL PRODUCT
TRANSACTIONAL BUNDLE
HIRED PROFESSIONAL SERVICE
DIY / HOW-TO
SELECTION
COMPARISON
REVIEWS / REPUTATION
TECHNICAL / DEFINITIONAL INFORMATION
FACTUAL SPECIFICATION
NAVIGATIONAL
INSPIRATION / EXAMPLES
LEGAL / PERMISSION
OUTSIDE SCOPE
```

### 4.7 Material object boundary

Only after action, expected result, and intent are understood should the object or subtype be used to choose between sibling clusters.

A different object may justify a split when it materially changes the content, procedure, answer, commercial result, or same-page compatibility.

A different label, brand, model, material, size, colour, location, or price wording does not justify a split by itself.

---

## 5. Mandatory multi-signal contrast rules

### 5.1 Product or bundle with an included service vs service-only request

When the primary result is acquiring a product or complete bundle and a service is included, keep the phrase with the product/bundle task unless direct evidence proves a different dominant result.

When the primary result is hiring an action for an already selected, supplied, or existing object, use the service task.

Universal contrast:

```text
BUY PRODUCT WITH INSTALLATION INCLUDED
-> PRODUCT OR BUNDLE TASK

INSTALL THE PRODUCT
-> INSTALLATION SERVICE TASK
```

The mere presence of an installation word must not convert a product purchase into a service-only cluster.

### 5.2 Whole object vs component

Determine whether the user acts on the complete object or on a part, accessory, consumable, tool, or subsystem.

```text
BUY / REPLACE / REPAIR WHOLE OBJECT
!=
BUY / REPLACE / REPAIR COMPONENT
```

A component word must not be attracted into a broad whole-object commercial cluster solely because both mention the parent object.

### 5.3 Product vs consumable or tool used for a service

A product, consumable, or tool used during an action is not the hired action itself.

```text
BUY MATERIAL OR TOOL FOR ACTION
-> PRODUCT / COMPONENT TASK

HIRE ACTION
-> SERVICE TASK
```

### 5.4 Hired service vs DIY or technical instruction

A phrase asking how to perform, diagnose, assemble, configure, repair, or install something seeks an informational result unless it also clearly requests a provider.

```text
HOW TO PERFORM ACTION
-> DIY / INFORMATION TASK

ORDER PROFESSIONAL ACTION
-> HIRED SERVICE TASK
```

### 5.5 Transaction vs selection, comparison, reviews, and technical information

Commercial words do not automatically dominate a clearly informational task.

Separate:

```text
BUY / ORDER
CHOOSE
COMPARE
READ REVIEWS OR RATINGS
UNDERSTAND TECHNOLOGY
FIND DIMENSIONS OR SPECIFICATIONS
VIEW EXAMPLES OR DESIGN IDEAS
```

Each is a different expected result when the distinction is material and supported by the corpus or direct evidence.

### 5.6 Multi-object phrases

For phrases mentioning multiple objects:

1. determine whether one object is the primary target and the others are context/components;
2. determine whether the user requests a true combined bundle;
3. use a combined-task cluster only when the expected result materially includes all objects;
4. do not create a combined cluster from mere co-occurrence.

### 5.7 Mixed lifecycle phrases

When several lifecycle words appear, choose the terminal requested result rather than the first matched verb.

Examples of abstract resolution:

```text
REPAIR OR REPLACE?
-> use the explicitly requested final state;
-> if genuinely unresolved, preserve boundary uncertainty.

BUY FOR LATER INSTALLATION
-> buying task, not installation service.

REVIEWS OF SERVICE PROVIDERS
-> reviews/reputation task, not immediate service order.
```

---

## 6. Modifier handling

The following are attributes by default:

```text
GEO
PRICE OR DISCOUNT WORDING
FINANCING
BRAND
MODEL OR SERIES
MANUFACTURER OR SELLER SOURCE
MATERIAL
COLOUR
SIZE OR DIMENSION
YEAR
BUILDING / USER / APPLICATION CONTEXT
STYLE
QUALITY OR PREMIUM WORDING
MORPHOLOGY
WORD ORDER
ACQUISITION SOURCE
FREQUENCY
```

A modifier becomes part of a cluster boundary only when one of the following is demonstrated:

1. it changes the primary object materially;
2. it changes the expected terminal result;
3. it changes the lifecycle action or execution mode;
4. one coherent result/page cannot satisfy both groups;
5. exact direct evidence supports a stable separate intent.

Every exception must be explicit in the cluster contract and split justification.

```text
DEFAULT = ABSORB MODIFIER
EXCEPTION = MATERIAL BOUNDARY PROVEN
```

---

## 7. Frozen cluster contracts

Every accepted cluster must have a contract that is strong enough to classify without guessing:

```text
CLUSTER_ID
USER_TASK
PRIMARY_OBJECT
OBJECT_SCOPE
EXPECTED_TERMINAL_RESULT
ALLOWED_ACTIONS
INTENT_MODE
LIFECYCLE_STAGE
EXECUTION_MODE
INCLUSION_RULE
EXCLUSION_RULE
NEAREST_SIBLING_CLUSTERS
ABSORBED_MODIFIERS
MATERIAL_BOUNDARIES
DIRECT_EVIDENCE_STATE
POSITIVE_EXAMPLES
NEGATIVE_EXAMPLES
```

Assignment is contract matching, not name similarity.

For each row ask:

1. Does the complete task signature satisfy the inclusion rule?
2. Does any exclusion rule apply?
3. Is a sibling contract more specific to the terminal result?
4. Would this assignment violate the cluster's object scope, lifecycle, or intent mode?
5. Is the phrase still ambiguous after reading the full wording and exact evidence?

Assign only when one contract is the strongest compatible contract.

---

## 8. Taxonomy construction without guessing

Taxonomy construction must happen after full task discovery, not while classifying the first matching phrase.

Required sequence:

```text
FULL CORPUS TASK SIGNATURES
-> NORMALIZE EQUIVALENT TASKS
-> REVIEW MATERIAL DIFFERENCES
-> APPLY SAME-PAGE / RESULT-COMPATIBILITY TEST
-> BATCH-REVIEW ALL NEW-CLUSTER CANDIDATES
-> FREEZE CLUSTER CONTRACTS
-> ASSIGN ALL ROWS
```

A new cluster is allowed only when a material user-task boundary is demonstrated.

A new cluster is forbidden when the only difference is a modifier, lexical form, isolated token, or one classifier exception.

---

## 9. One-pass assignment procedure

For every active phrase in Pass 2:

1. preserve the original phrase and provenance;
2. derive the complete task signature;
3. attach exact direct evidence only when it belongs to that exact phrase;
4. identify the expected terminal result;
5. identify object scope, lifecycle, intent, execution mode, and business scope;
6. record modifiers separately;
7. compare the signature against all plausible sibling contracts;
8. assign the strongest compatible existing cluster;
9. otherwise use `BOUNDARY_REVIEW`, `SEARCH_REQUIRED`, or `NEW_CLUSTER_CANDIDATE` without mutating taxonomy;
10. preserve confidence and a semantic rationale that names the decisive contrast.

Required row output:

```text
PHRASE
TASK_SIGNATURE
ASSIGNMENT_STATUS
CLUSTER_ID_IF_ASSIGNED
DECISIVE_SEMANTIC_CONTRAST
CONFIDENCE
DIRECT_EVIDENCE_EXACT
MODIFIERS
BOUNDARY_UNCERTAINTY
```

---

## 10. Automation boundary

Automation may help retrieve candidate phrases, detect signals, apply a frozen decision table, preserve accounting, and run invariants.

Automation must not redefine the method.

```text
TOKEN OR REGEX HIT -> CANDIDATE SIGNAL ONLY
TASK SIGNATURE + CLUSTER CONTRACT -> SEMANTIC DECISION
```

Any automated rule promoted after QA must:

1. express a universal semantic contrast rather than a client-specific phrase;
2. state its positive condition;
3. state disqualifying conditions;
4. include positive and negative regression examples;
5. be tested against all rows in its provable impact set;
6. avoid changing unrelated sibling tasks.

A list of exact phrases may be used only for genuinely opaque unresolved rows or exact direct-evidence identity, never as the general clustering method.

---

## 11. Uncertainty and Search routing

Use uncertainty states when the phrase does not expose a stable terminal result or when plausible sibling contracts remain materially incompatible.

```text
NO STABLE TASK HEAD -> SEARCH_REQUIRED OR BOUNDARY_REVIEW
POSSIBLE UNSEEN TASK -> NEW_CLUSTER_CANDIDATE
AMBIGUITY -> MUST NOT CREATE CLUSTER
```

Search/SERP is used to adjudicate material boundaries, not to manufacture confidence for every row.

No evidence may be propagated from one probed phrase to an unprobed neighbour without explicit support.

---

## 12. Empty clusters, microclusters, and member evidence

```text
ZERO_ASSIGNMENT_CLUSTER != PROVEN_CLUSTER
SMALL_CLUSTER != AUTOMATIC_ERROR
LARGE_CLUSTER != AUTOMATICALLY COHERENT
```

Before final acceptance:

- every zero-assignment cluster must be removed from the active taxonomy or explicitly marked as a non-counted reserved candidate with evidence and rationale;
- every microcluster must demonstrate a material boundary;
- every large cluster must pass internal-coherence review;
- cluster quality must be judged from member tasks and sibling boundaries, not from the attractiveness of the cluster name.

A final active cluster must have member evidence in the frozen corpus.

---

## 13. No patch-chain execution

The three semantic passes are planned roles inside one governed execution. They are not permission to create an unlimited series of versioned reruns.

Required execution model:

```text
ONE PLANNED EXECUTION
=
FULL TASK DISCOVERY
+ ONE TAXONOMY FREEZE
+ ONE FULL ASSIGNMENT
+ ONE FULL INDEPENDENT QA DISCOVERY
+ ONE FROZEN ERROR LEDGER
+ ONE CONSOLIDATED CORRECTION BATCH
+ ONE FULL MACHINE REGRESSION
+ ONE PROVABLE IMPACT-SET RECHECK
```

Forbidden model:

```text
FIND ONE ERROR
-> ADD ONE NARROW RULE
-> CREATE NEW VERSION
-> RERUN
-> REPEAT
```

A residual correction cycle is allowed only when the consolidated impact recheck finds a real remaining failure. All residual failures must again be collected before one consolidated residual correction.

---

## 14. Required semantic QA

The final result must pass all of the following:

### 14.1 Row correctness

Every active row has an independent verdict against its assigned cluster contract.

### 14.2 Cluster cohesion

Every cluster's members share the same material user task and expected result.

### 14.3 Sibling separation

Nearest sibling clusters have explicit, testable boundaries.

### 14.4 Modifier absorption

Modifier-only variations remain together unless a documented exception passes the material split gate.

### 14.5 Contrast regression

At minimum test both sides of each material contrast:

```text
PRODUCT OR BUNDLE vs SERVICE ONLY
WHOLE OBJECT vs COMPONENT
BUY vs HIRE vs DIY
TRANSACTION vs SELECTION vs COMPARISON vs REVIEWS vs TECHNICAL INFO
PRIMARY OBJECT vs CONTEXT OBJECT
IN-SCOPE vs OUTSIDE-SCOPE
ASSIGNED vs SEARCH_REQUIRED
```

### 14.6 Taxonomy evidence

Every final active cluster has at least one member and a valid split justification.

---

## 15. Acceptance gate

```text
TASK_SIGNATURE_FIELDS_DEFINED = true
ACTIVE_ROWS_HAVE_TASK_DECISIONS = ACTIVE_ROWS_TOTAL
TERMINAL_RESULT_RESOLVED_OR_UNCERTAINTY_PRESERVED = ALL
MODIFIERS_STORED_SEPARATELY = true
CLUSTER_CONTRACTS_FROZEN_BEFORE_ASSIGNMENT = true
IN_PASS_TAXONOMY_MUTATIONS = 0
EXACT_EVIDENCE_TRANSFER_TO_NEIGHBOURS = 0
ZERO_ASSIGNMENT_ACTIVE_CLUSTERS = 0
UNJUSTIFIED_MICROCLUSTERS = 0
FULL_ROW_INDEPENDENT_QA = PASS
COMPLETE_ERROR_LEDGER_FROZEN = true
CONSOLIDATED_CORRECTION_BATCHES = 1
FULL_MACHINE_REGRESSION = PASS
IMPACT_SET_RECHECK = PASS
RESIDUAL_SEMANTIC_FAILURES = 0
TARGET_CLUSTER_COUNT_USED = false
```

Explicit unresolved rows are allowed. Hidden ambiguity and speculative taxonomy are not.

---

## 16. Method origin and scope

This method formalizes reusable lessons from comparing independently produced clustering candidates and from full-corpus semantic QA:

- a more coherent task axis can outperform a larger or more detailed taxonomy;
- taxonomy quality and row-assignment quality are separate questions;
- token-first classifiers repeatedly confuse included services, components, lifecycle actions, and information modes;
- full error discovery before correction prevents endless local patch chains;
- cluster counts are outputs, never optimization targets.

The method is universal. Domain-specific vocabulary belongs only in the current job's evidence and implementation layer, never in this rule file.

---

## 17. Permanent markers

```text
STEP10_TASK_FIRST_SORTING_METHOD_ACTIVE = true
STEP10_TASK_SIGNATURE_REQUIRED = true
STEP10_EXPECTED_TERMINAL_RESULT_REQUIRED = true
STEP10_LITERAL_NEGATION_AND_RELATION_REVIEW_REQUIRED = true
STEP10_PRODUCT_BUNDLE_VS_SERVICE_CONTRAST_REQUIRED = true
STEP10_WHOLE_OBJECT_VS_COMPONENT_CONTRAST_REQUIRED = true
STEP10_HIRED_SERVICE_VS_DIY_CONTRAST_REQUIRED = true
STEP10_INFORMATION_MODE_SEPARATION_REQUIRED = true
STEP10_MODIFIERS_ABSORBED_BY_DEFAULT = true
STEP10_CLUSTER_CONTRACT_MATCHING_REQUIRED = true
STEP10_REGEX_IS_SIGNAL_NOT_SEMANTIC_TRUTH = true
STEP10_ZERO_ASSIGNMENT_ACTIVE_CLUSTER_FORBIDDEN = true
STEP10_ONE_PLANNED_EXECUTION_MODEL_ACTIVE = true
STEP10_ERROR_BY_ERROR_VERSION_CHAIN_FORBIDDEN = true
STEP10_RULES_MUST_BE_DOMAIN_INDEPENDENT = true
```
