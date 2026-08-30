# Step 10 — Universal Task-First Sorting Decision Method

Status: **APPROVED / ACTIVE / UNIVERSAL / OWNER-LOCKED**

This file defines a reusable decision method for Step-10 phrase clustering.

`UNIVERSAL` means that the decision structure can be instantiated for different subjects, businesses, sites and deliverables. It does **not** mean that execution must be stripped of domain-specific data.

Canonical companion authorities:

- `STEP_10_CLUSTERING_GRANULARITY_METHOD.md`
- `STEP_10_SORTING_AND_QA_METHOD.md`

---

## 0. Meaning of universal

The executable method is always the combination of a reusable core and the current job context:

```text
EXECUTABLE_STEP10_METHOD =
UNIVERSAL_DECISION_CORE
+ CURRENT_JOB_DOMAIN_PROFILE
+ CURRENT_SITE_AND_BUSINESS_SCOPE
+ CURRENT_CLUSTER_CONTRACTS
+ CURRENT_EVIDENCE
+ CURRENT_DELIVERABLE_CONSTRAINTS
```

Canonical interpretation:

```text
UNIVERSAL_METHOD != DOMAIN-FREE_EXECUTION
UNIVERSAL_METHOD != BAN_ON_LOCAL_RULES
LOCAL_DETAIL != UNIVERSAL_LAW
LOCAL_RULE_MUST_BE_SCOPED != LOCAL_RULE_MUST_BE_REMOVED
```

The current execution may use, and when needed must use:

```text
DOMAIN OBJECTS AND SERVICES
THE ACTUAL SITE AND BUSINESS MODEL
REAL CLUSTER IDS AND CLUSTER NAMES
CURRENT LANGUAGE AND QUERY FORMS
BRANDS, MODELS, MATERIALS AND LOCAL TERMINOLOGY
EXACT PHRASES AND DISAMBIGUATION EXCEPTIONS
SITE-SPECIFIC OR BUSINESS-SPECIFIC BOUNDARIES
JOB-SPECIFIC THRESHOLDS
AN EXPLICIT TARGET CLUSTER COUNT OR RANGE
CURRENT OWNER OR CLIENT CONSTRAINTS
```

These details may live in this file, a companion domain profile, a job method file, executable configuration, regression fixtures, or a combination of them.

The only universal separation is scope:

```text
CURRENT-JOB RULE -> APPLIES TO THE DECLARED JOB / DOMAIN
REUSABLE RULE -> MAY BE PROMOTED ONLY AFTER ITS REUSABILITY IS ESTABLISHED
```

A local rule is not weakened or removed merely because it is local. It is labelled and applied at the correct scope.

---

## 1. Purpose

The method determines what result the user is seeking and then maps that result to the most appropriate current cluster contract.

The baseline is:

```text
READ THE COMPLETE REQUEST
-> APPLY THE CURRENT DOMAIN PROFILE
-> IDENTIFY THE EXPECTED RESULT
-> BUILD A TASK SIGNATURE
-> MATCH IT TO CURRENT CLUSTER CONTRACTS
-> USE CURRENT EVIDENCE AND CONSTRAINTS
-> PRESERVE OR RESOLVE UNCERTAINTY AS THE JOB REQUIRES
```

A visible token may be decisive when the current domain profile proves that it is decisive. Otherwise it is one signal among several.

---

## 2. Current-job domain profile

Before classification, the execution must define or load the current domain profile.

At minimum it may contain:

```text
BUSINESS AND SITE SCOPE
TARGET REGION / LANGUAGE
OBJECT AND SERVICE VOCABULARY
OBJECT-PART RELATIONS
LIFECYCLE ACTIONS
INTENT AND RESULT TYPES
REAL CLUSTER IDS AND CONTRACTS
KNOWN BRANDS / MODELS / SERIES / MATERIALS
LOCAL SYNONYMS, ABBREVIATIONS AND MISSPELLINGS
EXACT PHRASE OVERRIDES WHERE NEEDED
OUTSIDE-SCOPE FAMILIES
DIRECT EVIDENCE OVERRIDES
JOB-SPECIFIC THRESHOLDS
COUNT / RANGE / FORMAT CONSTRAINTS
OWNER DECISIONS
```

The domain profile is part of the method, not contamination of it.

A profile can be replaced for a new subject while the decision sequence remains reusable.

---

## 3. Required task signature

For each phrase derive, when supported by the wording and evidence:

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

Normalized representation:

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

The current domain profile determines which fields and modifiers are material for the subject being processed.

---

## 4. Decision order

The following order is the reusable baseline. The domain profile may add, remove or reorder checks when the current subject requires it, provided the resulting precedence is explicit and tested.

### 4.1 Complete literal request

Read the whole phrase, including:

- negation;
- grammatical relations;
- which action applies to which object;
- whether a service is the requested result or part of a bundle;
- whether the user wants the action, information about the action, or a related product;
- local abbreviations and domain language.

A current domain rule may resolve omitted or elliptical wording when the evidence for that interpretation is documented.

### 4.2 Current exact evidence

Exact Search/SERP evidence, site evidence, owner decisions, or another approved source may resolve a row directly.

Evidence reuse follows the scope declared by the evidence record:

```text
EXACT-ROW EVIDENCE -> EXACT ROW
EXPLICIT FAMILY EVIDENCE -> DECLARED FAMILY
DOMAIN RULE -> DECLARED DOMAIN SCOPE
```

Evidence may be generalized when the current method explicitly supports that generalization; it must not be generalized silently.

### 4.3 Business and site scope

Apply the actual business model, site content, region, supported products/services and deliverable scope.

A phrase can be inside the semantic subject but outside the current business, site or delivery scope. That distinction is job-specific and must use the real current data.

### 4.4 Expected terminal result

Identify what the user expects to possess, receive, perform, understand, compare, view or reach when the task is complete.

Typical result classes include:

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
REACH A DESTINATION
VIEW IDEAS OR EXAMPLES
UNDERSTAND RULES OR PERMISSIONS
```

The domain profile may define additional result classes or combine these when the current deliverable requires it.

### 4.5 Lifecycle action

Possible lifecycle distinctions include:

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

They become separate clusters only when the current taxonomy or evidence treats them as materially distinct tasks.

### 4.6 Intent and execution mode

Possible modes include:

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
OUTSIDE CURRENT SCOPE
```

The current job may use a different or more detailed set.

### 4.7 Material object boundary

After action and expected result are understood, use the current object hierarchy to distinguish:

```text
WHOLE OBJECT
COMPONENT OR SUBSYSTEM
ACCESSORY
CONSUMABLE OR TOOL
BUNDLE
CONTEXT OBJECT
```

The domain profile decides which object differences are material and which are modifiers.

---

## 5. Reusable contrast patterns

These are baseline contrasts, not bans on alternative domain logic.

### 5.1 Product or bundle with included service vs service-only request

```text
ACQUIRE PRODUCT / BUNDLE WITH SERVICE INCLUDED
-> PRODUCT OR BUNDLE TASK BY DEFAULT

HIRE ACTION FOR AN EXISTING OR SEPARATELY SUPPLIED OBJECT
-> SERVICE TASK BY DEFAULT
```

A current domain rule or direct evidence may establish another interpretation.

### 5.2 Whole object vs component

```text
BUY / REPLACE / REPAIR WHOLE OBJECT
MAY DIFFER FROM
BUY / REPLACE / REPAIR COMPONENT
```

Whether they become separate clusters depends on the current taxonomy and result compatibility.

### 5.3 Product, consumable or tool used for an action vs hired action

```text
OBTAIN MATERIAL / TOOL / PART FOR ACTION
MAY MAP TO PRODUCT OR COMPONENT TASK

ORDER THE ACTION ITSELF
MAY MAP TO SERVICE TASK
```

### 5.4 Hired service vs DIY or technical instruction

```text
LEARN HOW TO PERFORM ACTION
MAY MAP TO DIY / INFORMATION

ORDER PROFESSIONAL ACTION
MAY MAP TO SERVICE
```

### 5.5 Transaction vs information modes

The current taxonomy may distinguish or combine:

```text
BUY / ORDER
CHOOSE
COMPARE
READ REVIEWS OR RATINGS
UNDERSTAND TECHNOLOGY
FIND DIMENSIONS OR SPECIFICATIONS
VIEW EXAMPLES OR DESIGN IDEAS
```

The choice is governed by the current job's cluster contracts, evidence and delivery requirements.

### 5.6 Multi-object phrases

For phrases mentioning multiple objects:

1. identify the primary requested result;
2. determine whether other objects are context, parts or true bundle members;
3. use a combined cluster when the current taxonomy defines a combined result;
4. use a single-object cluster when the other terms are contextual;
5. preserve a local exception when the current domain requires one.

### 5.7 Mixed lifecycle phrases

When several lifecycle signals appear, choose the result according to the current precedence rules and evidence.

Examples:

```text
BUY FOR LATER INSTALLATION
-> OFTEN A BUYING TASK

REVIEWS OF SERVICE PROVIDERS
-> OFTEN A REVIEWS / SELECTION TASK

REPAIR OR REPLACE
-> RESOLVE FROM WORDING, DOMAIN PRACTICE OR EVIDENCE
```

`OFTEN` is intentional: the current domain profile may define a different outcome.

---

## 6. Modifier handling

Possible modifiers include:

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

Default mode when no contrary current evidence exists:

```text
MODIFIER -> ATTRIBUTE INSIDE THE SAME MATERIAL TASK
```

A current job may promote a modifier to a cluster boundary when:

1. it changes the primary object materially;
2. it changes the expected terminal result;
3. it changes lifecycle or execution mode;
4. it changes page/result compatibility;
5. direct evidence supports a separate intent;
6. the owner, client or deliverable explicitly requires the split.

Brand, geography, material, size or any other modifier may therefore be either an attribute or a valid split axis. The decision is current-job-specific and must be recorded.

---

## 7. Target count and other output constraints

A fixed cluster count or range is allowed when it is an explicit current-job requirement.

```text
NO EXPLICIT COUNT CONSTRAINT
-> COUNT MAY EMERGE FROM CURRENT TASK BOUNDARIES

EXPLICIT OWNER / CLIENT / DELIVERABLE COUNT OR RANGE
-> RECORD IT
-> APPLY IT
-> RECORD ANY SEMANTIC TRADE-OFF
```

A count constraint is a real project constraint even though it is not, by itself, semantic evidence.

If the required count conflicts with the most natural semantic grouping, the method must not silently ignore either side. It records the conflict and applies the authorized priority or owner decision.

The same rule applies to:

```text
MAXIMUM CLUSTER SIZE
MINIMUM CLUSTER SIZE
REQUIRED CATEGORY LIST
REQUIRED OUTPUT FORMAT
REQUIRED PAGE OR CAMPAIGN LIMIT
TOOL-SPECIFIC THRESHOLDS
```

---

## 8. Current cluster contracts

Each executable cluster contract should contain the fields needed for the current subject. A strong baseline is:

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
NEAREST SIBLING CLUSTERS
ABSORBED MODIFIERS
MATERIAL BOUNDARIES
DIRECT EVIDENCE STATE
POSITIVE EXAMPLES
NEGATIVE EXAMPLES
LOCAL EXCEPTIONS
```

Real IDs, names, examples and exact phrases are expected here.

Assignment is matching the complete current task representation to the current contract set.

---

## 9. Taxonomy construction

Reusable sequence:

```text
REVIEW CURRENT CORPUS
-> BUILD CURRENT TASK SIGNATURES
-> NORMALIZE EQUIVALENT TASKS
-> APPLY CURRENT DOMAIN AND DELIVERABLE CONSTRAINTS
-> REVIEW MATERIAL DIFFERENCES
-> BUILD OR ADAPT CURRENT CLUSTER CONTRACTS
-> FREEZE THE CURRENT ASSIGNMENT VERSION
-> ASSIGN AND VERIFY
```

The current job may start from:

```text
A FRESH TAXONOMY
AN EXISTING TAXONOMY
A CLIENT-PROVIDED CATEGORY SET
A FIXED NUMBER OF GROUPS
A SITE STRUCTURE
AN AD-CAMPAIGN STRUCTURE
A TOOL-GENERATED CANDIDATE SET
```

Historical names, counts and assignments may be reused when reuse is allowed by the current task. They are comparison-only only when an independent rebuild is explicitly required.

---

## 10. Assignment procedure

For every active phrase:

1. preserve the original phrase and provenance;
2. apply the current domain profile;
3. attach all evidence whose declared scope includes the phrase;
4. derive the task signature;
5. identify the expected result and object scope;
6. apply current count, format and business constraints;
7. compare the phrase against plausible current cluster contracts;
8. assign, defer, search, create a candidate, or use a current exact rule as the method permits;
9. record confidence, decisive reason and evidence scope.

Suggested row output:

```text
PHRASE
TASK_SIGNATURE
ASSIGNMENT_STATUS
CLUSTER_ID_IF_ASSIGNED
DECISIVE_REASON
CONFIDENCE
EVIDENCE_SCOPE
MODIFIERS
BOUNDARY_UNCERTAINTY
LOCAL_RULE_ID_IF_USED
```

---

## 11. Automation and exact rules

Automation may use:

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
CURRENT CLUSTER IDS
DOMAIN-SPECIFIC PRECEDENCE RULES
OWNER-PROVIDED RULES
```

No implementation technique is excluded merely because it is domain-specific.

A reusable core rule should be broadly stated. A local implementation rule may be narrow and exact when that is what correctness requires.

For every material automated rule, preserve as applicable:

```text
SCOPE
POSITIVE CONDITION
DISQUALIFYING CONDITION
EXPECTED OUTPUT
EVIDENCE OR OWNER SOURCE
POSITIVE REGRESSION CASES
NEGATIVE REGRESSION CASES
IMPACT SET
```

Exact phrase mappings and hard-coded IDs are valid implementation tools. Their limitation is scope, not legitimacy.

---

## 12. Uncertainty and Search routing

The current job defines how uncertainty is handled.

Possible states:

```text
ASSIGNED
BOUNDARY_REVIEW
SEARCH_REQUIRED
NEW_CLUSTER_CANDIDATE
DEFERRED
OWNER_DECISION_REQUIRED
```

A job may require every phrase to be assigned; another may allow unresolved rows. Both modes are valid when explicitly declared.

Search/SERP may be used for every phrase, only for uncertain boundaries, or not at all, depending on scope, budget and authorization.

---

## 13. Empty clusters, reserved clusters and microclusters

A zero-member cluster may be valid when the current deliverable requires a predeclared, reserved or future category.

Required distinction:

```text
ACTIVE EVIDENCE-BACKED CLUSTER
RESERVED / EMPTY DECLARED CATEGORY
REJECTED CANDIDATE
```

Do not conflate them in reporting.

Small and singleton clusters may be correct. Large clusters may be incoherent. Size is a review signal whose thresholds are job-specific.

---

## 14. Iteration model

Batch discovery and consolidated correction are the preferred default for large corpora because they reduce uncontrolled local patching.

Iterative refinement is also allowed when required by:

```text
OWNER INSTRUCTION
TOOL LIMITS
CORPUS SIZE
INCREMENTAL DATA ARRIVAL
COST CONTROLS
MODEL OR PROVIDER LIMITS
A/B COMPARISON
EXPERIMENT DESIGN
```

Each iteration should declare:

```text
PURPOSE
INPUT VERSION
CHANGED RULES
EXPECTED IMPACT SET
VALIDATION
OUTPUT VERSION
```

The method therefore controls hidden or unbounded patching without banning legitimate reruns.

---

## 15. Semantic QA

Applicable QA may include:

```text
ROW CORRECTNESS
CLUSTER COHESION
SIBLING SEPARATION
MODIFIER CONSISTENCY
COUNT-CONSTRAINT COMPLIANCE
DOMAIN-PROFILE COVERAGE
EXACT-RULE COVERAGE
CONTRAST REGRESSION
ACCOUNTING
IMPACT-SET REVIEW
OWNER ACCEPTANCE
```

The QA plan is configured for the current job rather than assumed identical for every corpus.

---

## 16. Acceptance gate template

The current job must instantiate the applicable values:

```text
CURRENT_DOMAIN_PROFILE_DEFINED = true
CURRENT_SITE_AND_BUSINESS_SCOPE_DEFINED = true
CURRENT_CLUSTER_CONTRACTS_DEFINED = true
CURRENT_COUNT_MODE_DECLARED = true
CURRENT_UNCERTAINTY_MODE_DECLARED = true
ACTIVE_ROWS_ACCOUNTED = CURRENT_REQUIRED_TOTAL
CURRENT_REQUIRED_QA = PASS
CURRENT_CONSTRAINTS_SATISFIED_OR_EXPLICITLY_WAIVED = true
LOCAL_RULES_SCOPED = true
EVIDENCE_SCOPE_PRESERVED = true
UNEXPECTED_ASSIGNMENT_CHANGES = 0
```

Additional gates may be added by the current job.

---

## 17. Method origin and scope

This method formalizes a reusable task-first decision structure while explicitly supporting subject-specific execution.

Domain-specific vocabulary, sites, cluster IDs, exact phrases, examples, thresholds, target counts and local precedence rules may appear in:

```text
THIS METHOD FILE
A COMPANION DOMAIN PROFILE
A JOB-SPECIFIC METHOD
EXECUTABLE CONFIGURATION
REGRESSION TESTS
OWNER DECISION RECORDS
```

Their presence does not make the method non-universal. Universality is provided by the ability to replace the profile and reuse the decision architecture.

---

## 18. Permanent markers

```text
STEP10_TASK_FIRST_SORTING_METHOD_ACTIVE = true
STEP10_UNIVERSAL_METHOD_MEANS_REUSABLE_STRUCTURE = true
STEP10_DOMAIN_PROFILE_ALLOWED = true
STEP10_DOMAIN_PROFILE_REQUIRED_WHEN_NEEDED = true
STEP10_SITE_SPECIFIC_DATA_ALLOWED = true
STEP10_REAL_CLUSTER_IDS_AND_NAMES_ALLOWED = true
STEP10_EXACT_LOCAL_PHRASES_AND_RULES_ALLOWED = true
STEP10_JOB_SPECIFIC_THRESHOLDS_ALLOWED = true
STEP10_EXPLICIT_TARGET_COUNT_OR_RANGE_ALLOWED = true
STEP10_LOCAL_RULES_MUST_BE_SCOPED_NOT_REMOVED = true
STEP10_HISTORICAL_TAXONOMY_REUSE_ALLOWED_WHEN_AUTHORIZED = true
STEP10_RESERVED_EMPTY_CLUSTERS_ALLOWED_WHEN_DECLARED = true
STEP10_ITERATIVE_REFINEMENT_ALLOWED_WHEN_SCOPED_AND_VERIFIED = true
STEP10_TASK_SIGNATURE_BASELINE_ACTIVE = true
STEP10_EXPECTED_TERMINAL_RESULT_BASELINE_ACTIVE = true
STEP10_CURRENT_JOB_CONSTRAINTS_ARE_PART_OF_EXECUTION = true
```
