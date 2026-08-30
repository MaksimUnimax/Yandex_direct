# KW-001 — STEP 10 CLUSTERING GRANULARITY METHOD

Date approved: 2026-08-30  
Last corrected: 2026-08-30  
Status: **APPROVED / ACTIVE / UNIVERSAL / OWNER-LOCKED**

This file defines a reusable Step-10 method for controlling clustering granularity.

`UNIVERSAL` means the reasoning structure is reusable. It does **not** exclude current-domain vocabulary, the actual site, real cluster IDs, local examples, job-specific thresholds, a required number of groups, or other execution constraints.

---

## MEANING OF UNIVERSAL

The executable method is:

```text
UNIVERSAL GRANULARITY CORE
+ CURRENT DOMAIN PROFILE
+ CURRENT CORPUS
+ CURRENT SITE / BUSINESS MODEL
+ CURRENT EVIDENCE
+ CURRENT OWNER / CLIENT / DELIVERABLE CONSTRAINTS
```

Canonical interpretation:

```text
UNIVERSAL != DOMAIN-FREE
UNIVERSAL != NO LOCAL RULES
LOCAL RULE != INVALID RULE
LOCAL RULE MUST BE SCOPED != LOCAL RULE MUST BE REMOVED
```

The current execution may define and use:

```text
REAL CLUSTER IDS AND NAMES
DOMAIN-SPECIFIC OBJECTS AND SERVICES
BRANDS, MODELS, MATERIALS, LOCATIONS AND LOCAL LANGUAGE
SITE-SPECIFIC BOUNDARIES
EXACT PHRASE EXAMPLES AND EXCEPTIONS
JOB-SPECIFIC SPLIT / MERGE THRESHOLDS
A FIXED TARGET CLUSTER COUNT OR RANGE
REQUIRED CATEGORIES OR RESERVED EMPTY CATEGORIES
OWNER-PROVIDED CLASSIFICATION RULES
```

These are part of the executable current method. They are not automatically promoted to every other project.

---

## STEP PURPOSE

Step 10 groups active phrases into the cluster structure required by the current job while controlling two opposite risks:

```text
OVER-SPLITTING -> more groups than the current task, evidence or deliverable requires
UNDER-SPLITTING -> fewer groups than the current task, evidence or deliverable can support
```

Granularity is determined by the combination of:

```text
USER TASKS
EXPECTED RESULTS
CURRENT DOMAIN STRUCTURE
PAGE / RESULT COMPATIBILITY WHEN RELEVANT
DIRECT EVIDENCE
BUSINESS AND SITE SCOPE
DELIVERABLE CONSTRAINTS
OWNER DECISIONS
```

---

## CLUSTER-COUNT MODES

Cluster count has two valid modes.

### Mode A — unconstrained count

When no explicit count or range is required:

```text
CLUSTER COUNT = RESULT OF CURRENT VALIDATED BOUNDARIES
```

In this mode the analyst does not invent a preferred number merely because it looks tidy.

### Mode B — constrained count or range

When the owner, client, tool, campaign, report, site structure or deliverable requires a number or range:

```text
EXPLICIT COUNT / RANGE CONSTRAINT
-> RECORD SOURCE AND PRIORITY
-> APPLY DURING TAXONOMY DESIGN
-> RECORD SEMANTIC TRADE-OFFS IF ANY
-> VERIFY FINAL COMPLIANCE
```

Canonical interpretation:

```text
COUNT CONSTRAINT = REAL PROJECT CONSTRAINT
COUNT CONSTRAINT != SEMANTIC EVIDENCE BY ITSELF
COUNT CONSTRAINT MAY CONTROL OUTPUT WHEN AUTHORIZED
```

If the constraint conflicts with the most natural semantic grouping, the conflict must be visible and resolved according to the current owner or delivery priority. The method must not silently ignore the constraint.

---

## BASELINE GRANULARITY PRINCIPLE

When no contrary current-job rule exists, keep semantically compatible phrases together and split materially different tasks.

Default baseline:

```text
SAME MATERIAL USER TASK -> SAME CLUSTER CANDIDATE
MATERIAL USER-TASK DIFFERENCE -> SPLIT CANDIDATE
UNCLEAR BOUNDARY -> REVIEW / EVIDENCE / CURRENT OWNER RULE
```

The current domain profile may define a token, modifier, brand, product class, location, page type, exact phrase family or other signal as a valid split axis.

---

## MATERIAL SPLIT EVIDENCE

A split may be supported by one or more current-job signals such as:

```text
1. DIFFERENT END USER GOAL / TASK OUTCOME
2. DIFFERENT ACTION OR LIFECYCLE TASK
3. DIFFERENT PRIMARY OBJECT, SERVICE OR COMPONENT
4. DIFFERENT INTENT OR EXPECTED RESULT TYPE
5. DIFFERENT EXECUTION MODE: BUY / HIRE / DIY / LEARN / NAVIGATE / OTHER
6. DIFFERENT PAGE OR RESULT NEED WHEN PAGE COMPATIBILITY IS IN SCOPE
7. DIRECT SERP OR OTHER APPROVED EVIDENCE
8. SITE OR BUSINESS-SCOPE BOUNDARY
9. OWNER / CLIENT / DELIVERABLE REQUIREMENT
10. DOMAIN-SPECIFIC RULE OR TAXONOMY CONTRACT
11. REQUIRED COUNT OR RANGE CONSTRAINT
```

No single signal is sufficient in every project. A signal can nevertheless be decisive in a specific project when the current domain profile or owner decision says so.

For each material split record as applicable:

```text
SPLIT AXIS
CURRENT SCOPE
SUPPORTING EVIDENCE OR CONSTRAINT
PARENT / SIBLING CLUSTERS
EXPECTED RESULT DIFFERENCE
OUTPUT EFFECT
```

---

## SAME-PAGE OR SAME-RESULT COMPATIBILITY

When page or result compatibility is relevant, evaluate whether one coherent result can satisfy both groups.

```text
ONE RESULT CAN SATISFY BOTH -> EVIDENCE TOWARD MERGE
ONE RESULT CANNOT SATISFY BOTH -> EVIDENCE TOWARD SPLIT
UNCLEAR -> REVIEW OR CURRENT EVIDENCE ROUTE
```

This is one possible clustering signal. A current deliverable may cluster for another purpose, such as campaign structure, content inventory, reporting, navigation, product taxonomy or fixed output categories.

Therefore:

```text
SAME-PAGE TEST = OPTIONAL CURRENT-JOB SIGNAL
SAME-PAGE TEST != UNIVERSAL OVERRIDE OF ALL OTHER CONSTRAINTS
```

---

## MODIFIER HANDLING

Common modifiers include:

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

Default in an unconstrained task-first run:

```text
MODIFIER -> ATTRIBUTE INSIDE THE SAME MATERIAL TASK
```

Current-job override:

```text
MODIFIER -> SPLIT AXIS
```

is valid when supported by any current source, such as:

```text
DOMAIN TAXONOMY
SITE STRUCTURE
SERP BEHAVIOUR
BUSINESS MODEL
CLIENT REPORTING NEED
CAMPAIGN DESIGN
OWNER INSTRUCTION
TARGET COUNT / RANGE
TOOL REQUIREMENT
```

Brand, geography, material, size or another modifier may therefore remain absorbed in one project and define separate clusters in another.

---

## TAXONOMY-CONSTRUCTION MODES

The current job may use any of these legitimate starting modes:

```text
FRESH TAXONOMY DISCOVERY
ADAPT AN EXISTING TAXONOMY
USE A CLIENT-PROVIDED CATEGORY SET
USE CURRENT SITE CATEGORIES
USE A FIXED NUMBER OF GROUPS
USE A REQUIRED CATEGORY LIST
USE TOOL-GENERATED CANDIDATES
USE A PRIOR VALIDATED TAXONOMY
```

The chosen mode must be declared before assignment.

Historical clusters may be reused when reuse is allowed. They become comparison-only only when the current task explicitly requests an independent rebuild.

---

## CLUSTER CREATION AND ROW CLASSIFICATION

For large or uncertain corpora, the preferred baseline separates task discovery, taxonomy normalization and assignment:

```text
DISCOVER CURRENT TASKS
-> BUILD OR ADAPT TAXONOMY
-> FREEZE CURRENT VERSION
-> ASSIGN
-> VERIFY
```

The current job may also permit controlled in-pass taxonomy growth when:

```text
THE CORPUS IS SMALL
THE OWNER REQUIRES INTERACTIVE SORTING
DATA ARRIVES INCREMENTALLY
THE TOOL REQUIRES ONLINE CLUSTER CREATION
THE CATEGORY SET IS BEING CO-DESIGNED
```

In that mode every mutation must be logged and its impact rechecked.

Canonical distinction:

```text
UNCONTROLLED TAXONOMY MUTATION = PROCESS RISK
CONTROLLED, DECLARED TAXONOMY MUTATION = VALID EXECUTION MODE
```

---

## CLUSTER JUSTIFICATION RECORD

For every material new or changed cluster, preserve the fields required by the current job. A strong baseline is:

```text
CLUSTER ID / LABEL
SCOPE
PARENT OR NEAREST SIBLING
MEMBER PHRASES OR REQUIRED CATEGORY SOURCE
SPLIT AXIS
USER-TASK OR DELIVERABLE DIFFERENCE
PAGE / RESULT COMPATIBILITY IF RELEVANT
DIRECT EVIDENCE STATE
COUNT-CONSTRAINT EFFECT IF RELEVANT
OWNER DECISION IF RELEVANT
FINAL DECISION
```

An exact phrase, local term, site category or owner instruction is valid support when it is the real basis of the decision.

---

## MICROCLUSTERS, SINGLETONS AND EMPTY CATEGORIES

Cluster size is a current-job parameter.

```text
SMALL CLUSTER MAY BE CORRECT
SINGLETON MAY BE CORRECT
LARGE CLUSTER MAY BE INCORRECT
EMPTY CATEGORY MAY BE REQUIRED
```

A current taxonomy may contain:

```text
ACTIVE EVIDENCE-BACKED CLUSTER
RESERVED EMPTY CATEGORY
REQUIRED CLIENT CATEGORY
FUTURE CATEGORY
REJECTED CANDIDATE
```

They must be reported separately.

Any numerical small/large threshold is allowed when declared for the current job. It is not automatically an industry-wide truth.

---

## UNCERTAINTY MODES

The current job must declare one of the following or an equivalent mode:

```text
UNRESOLVED ROWS ALLOWED
EVERY ROW MUST BE ASSIGNED
OWNER DECISION REQUIRED FOR AMBIGUOUS ROWS
SEARCH / SERP USED FOR AMBIGUITY
DEFAULT / FALLBACK CLUSTER USED
```

All are valid when explicit.

When unresolved states are allowed, possible statuses include:

```text
NEW_CLUSTER_CANDIDATE
SPLIT_UNPROVEN
BOUNDARY_REVIEW
SEARCH_REQUIRED
DEFERRED
```

When all rows must be assigned, preserve lower confidence or fallback reasoning instead of pretending the decision was certain.

---

## CONSISTENCY OF SPLIT AXES

Consistency is judged against the current domain profile, not against a requirement that every family use the same split axis.

For each family ask:

```text
WHAT AXIS IS USED HERE?
WHY IS IT MATERIAL OR REQUIRED HERE?
WHAT CURRENT EVIDENCE OR CONSTRAINT SUPPORTS IT?
HOW ARE SIBLING PHRASES HANDLED?
```

One family may validly split by action, another by brand, another by material and another by geography when the current evidence or deliverable supports those choices.

---

## MERGE CONTROL

A merge may be driven by:

```text
SAME USER TASK
SAME EXPECTED RESULT
SAME PAGE / RESULT COMPATIBILITY
CURRENT COUNT CONSTRAINT
OWNER / CLIENT CATEGORY DESIGN
TOOL OR CAMPAIGN REQUIREMENT
```

If a constraint causes semantically broader clusters, record that fact rather than hiding it.

Likewise, a lower count is not automatically better and a higher count is not automatically worse.

```text
CLUSTER QUALITY = FITNESS FOR CURRENT PURPOSE
```

---

## ITERATION AND CORRECTION

Batch review and consolidated correction are the preferred baseline for large corpora.

Iterative correction is allowed when required by:

```text
OWNER INSTRUCTION
NEW DATA
TOOL LIMITS
MODEL LIMITS
EXPERIMENT DESIGN
A/B COMPARISON
BUDGET OR COST STAGING
INCREMENTAL DELIVERY
```

Each run should declare:

```text
INPUT VERSION
PURPOSE
RULE OR TAXONOMY CHANGE
EXPECTED IMPACT
VALIDATION
OUTPUT VERSION
```

The method prevents hidden, unbounded patching; it does not ban legitimate additional runs.

---

## KNOWN FAILURE MODES AND CORRECT CONTROLS

### Failure A — local nuance becomes accidental universal law

Control:

```text
KEEP LOCAL RULE
LABEL ITS SCOPE
DO NOT SILENTLY PROMOTE IT TO EVERY PROJECT
```

### Failure B — universal method strips away required domain knowledge

Control:

```text
CURRENT DOMAIN PROFILE IS PART OF EXECUTION
LOCAL TERMS / IDS / EXAMPLES / THRESHOLDS ARE ALLOWED
```

### Failure C — count constraint is silently ignored

Control:

```text
DECLARE COUNT MODE
APPLY AUTHORIZED CONSTRAINT
RECORD TRADE-OFFS
```

### Failure D — analyst invents a count where none was requested

Control:

```text
UNCONSTRAINED MODE -> COUNT EMERGES FROM CURRENT BOUNDARIES
```

### Failure E — uncertainty is hidden

Control:

```text
USE THE CURRENT DECLARED UNCERTAINTY MODE
PRESERVE CONFIDENCE AND DECISION BASIS
```

---

## EXTERNAL METHOD SUPPORT

Industry clustering guidance supports shared search intent, page/result compatibility, SERP overlap and manual adjudication as useful clustering signals. These signals remain inputs to the current method rather than universal overrides of owner, business, site or deliverable constraints.

Direct references:

- Ahrefs — Keyword Clustering: https://ahrefs.com/blog/keyword-clustering/
- SE Ranking — Comprehensive Guide to Keyword Clustering: https://seranking.com/blog/keyword-clustering/
- SE Ranking — How to start keyword grouping: https://help.seranking.com/hc/en-us/articles/16332627413148-How-to-start-keyword-grouping
- Rush Analytics — keyword clustering guide: https://www.rush-analytics.ru/faq/klasterizaciya-zaprosov-semanticheskogo-yadra-rukovodstvo
- Keyword Insights — clustering types / centroid vs agglomerative trade-off: https://docs.keywordinsights.ai/learning-center/the-features/keyword-clustering/the-advanced-settings/clustering-types

No external source eliminates the need for a current domain profile and current project constraints.

---

## SOURCE-TO-METHOD TRACE

```text
shared search intent / same-result compatibility
-> useful baseline for unconstrained task clustering

SERP overlap
-> possible boundary evidence where Search evidence is in scope

soft vs hard clustering
-> strictness is a configurable current-job choice

manual review
-> automated grouping benefits from current-domain adjudication

owner / client / deliverable constraint
-> valid current execution constraint that must be recorded and applied

fixed target count or range
-> valid constrained mode; not semantic evidence by itself

site / business taxonomy
-> valid current split or merge axis

local exact rule
-> valid within declared scope
```

---

## PASS GATE TEMPLATE

The current execution must instantiate applicable values:

```text
CURRENT_DOMAIN_PROFILE_DEFINED = true
CURRENT_TAXONOMY_MODE_DECLARED = true
CURRENT_COUNT_MODE_DECLARED = true
CURRENT_UNCERTAINTY_MODE_DECLARED = true
CURRENT_SPLIT_AXES_RECORDED = true
CURRENT_CLUSTER_CONSTRAINTS_APPLIED = true
LOCAL_RULES_SCOPED = true
REQUIRED_ROWS_ACCOUNTED = CURRENT_REQUIRED_TOTAL
REQUIRED_CATEGORIES_ACCOUNTED = true
CURRENT_SEMANTIC_QA = PASS
CURRENT_DELIVERABLE_QA = PASS
```

Optional current-job gates may include:

```text
TARGET_CLUSTER_COUNT_MATCHED
TARGET_CLUSTER_RANGE_MATCHED
RESERVED_EMPTY_CATEGORIES_REPORTED
MICROCLUSTER_THRESHOLD_APPLIED
SERP_BOUNDARY_REVIEW_COMPLETE
OWNER_ACCEPTANCE_RECEIVED
```

---

## PERMANENT MARKERS

```text
KW001_STEP10_GRANULARITY_METHOD_APPROVED = true
KW001_STEP10_UNIVERSAL_MEANS_REUSABLE_CORE = true
KW001_STEP10_DOMAIN_PROFILE_ALLOWED = true
KW001_STEP10_DOMAIN_PROFILE_REQUIRED_WHEN_NEEDED = true
KW001_STEP10_SITE_SPECIFIC_BOUNDARIES_ALLOWED = true
KW001_STEP10_REAL_CLUSTER_IDS_AND_LOCAL_EXAMPLES_ALLOWED = true
KW001_STEP10_JOB_SPECIFIC_THRESHOLDS_ALLOWED = true
KW001_STEP10_EXPLICIT_TARGET_COUNT_OR_RANGE_ALLOWED = true
KW001_STEP10_UNCONSTRAINED_COUNT_MODE_ALLOWED = true
KW001_STEP10_CONSTRAINED_COUNT_MODE_ALLOWED = true
KW001_STEP10_MODIFIER_AS_ATTRIBUTE_OR_SPLIT_AXIS_ALLOWED = true
KW001_STEP10_EXISTING_TAXONOMY_REUSE_ALLOWED = true
KW001_STEP10_CONTROLLED_TAXONOMY_MUTATION_ALLOWED = true
KW001_STEP10_RESERVED_EMPTY_CATEGORIES_ALLOWED = true
KW001_STEP10_ITERATIVE_REFINEMENT_ALLOWED_WHEN_SCOPED = true
KW001_STEP10_LOCAL_RULES_MUST_BE_SCOPED_NOT_REMOVED = true
```

Status: **APPROVED / ACTIVE / UNIVERSAL / OWNER-LOCKED**.
