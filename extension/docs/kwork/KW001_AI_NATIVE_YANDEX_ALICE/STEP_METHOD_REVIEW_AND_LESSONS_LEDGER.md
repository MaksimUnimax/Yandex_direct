# KW-001 — STEP METHOD REVIEW AND LESSONS LEDGER

Updated: 2026-09-05  
Status: **ACTIVE / UNIVERSAL / OWNER-LOCKED**

This file contains permanent owner-approved methodology lessons. It is **not** a current-job log.

Concrete client/test names, domains, URLs, phrases, products, clusters, action IDs, row counts, provider receipts/costs, commit SHAs, job artifact paths and current step results are forbidden here under `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.

## Owner-lock rule

A concrete job may expose a reusable lesson, but permanent promotion requires explicit owner authorization.

```text
JOB INCIDENT
-> MAY PRODUCE PROPOSED LESSON
-> OWNER REVIEW / AUTHORIZATION
-> ONLY THEN PERMANENT METHOD UPDATE
```

Concrete proof remains in Level2/Git history. The permanent lesson keeps the **failure class, root cause, false assumption, corrected control and pass boundary**.

## Mandatory causal-use rule

This ledger is not a checklist to replay mechanically.

Before applying a lesson, explain:

```text
WHAT FAILED
WHY IT FAILED
WHAT FALSE ASSUMPTION / PROCESS GAP CAUSED IT
HOW THE CONTROL BLOCKS THAT CAUSE
WHY THAT CAUSE IS RELEVANT NOW
WHETHER CURRENT EXTERNAL RESEARCH STILL SUPPORTS THE METHOD
```

```text
RULE RECALL WITHOUT CAUSAL UNDERSTANDING != METHOD VALIDATION
```

Detailed step methods listed in `STEP_RULES_INDEX.md` override this summary when more specific.

---

# OWNER-APPROVED PERMANENT LESSONS

## Step 0 — scope freeze

**Purpose:** preserve the client/order goal and boundaries before evidence changes recommendations.

**Failure class:** later evidence can silently redefine the original task.

**Root cause:**

```text
EVOLVING ANALYSIS
WAS ALLOWED TO CHANGE
THE ORIGINAL SUCCESS CRITERION
```

**Control:** freeze initial business, region, scope, exclusions and promised outputs. Later findings may change recommendations but not rewrite what was originally requested.

Status: **APPROVED / ACTIVE**.

---

## Step 1 — existing-site / business discovery

**Purpose:** build the factual current-site/business model before search-demand evidence drives recommendations.

**Failure class:** one successful discovery pass was treated as the whole site.

**Root cause:**

```text
DISCOVERY SUCCESS
WAS CONFUSED WITH
DISCOVERY COMPLETENESS
```

**Control:** for non-trivial sites use sufficiently independent discovery routes when completeness matters, preserve evidence strength/provenance, timestamp current evidence and apply `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`.

Status: **APPROVED / ACTIVE**.

---

## Step 2 — seed / acquisition plan

**Purpose:** create bounded probes that reveal demand vocabulary without pre-deciding the final semantic core.

**Failure class:** seed relevance was confused with final keyword/page relevance.

**Root cause:**

```text
MEASUREMENT INSTRUMENT
WAS TREATED AS
FINAL OBJECT OF SELECTION
```

**Control:** every seed has an explicit uncertainty/information purpose. `SEED != FINAL KEYWORD` and current URL taxonomy must not automatically become the acquisition taxonomy.

Status: **APPROVED / ACTIVE**.

---

## Step 3 — provider acquisition

**Purpose:** preserve a complete reusable acquisition dataset, not merely successful API calls.

**Failure class:** provider requests could succeed technically while only counts/examples or incomplete returned rows were durably saved.

**Root cause:**

```text
TECHNICAL REQUEST SUCCESS
WAS TREATED AS
DATA-COLLECTION GOAL COMPLETION
```

**Control:** per acquisition item:

```text
DEFINE REQUIRED RESULT
-> EXECUTE
-> RECEIVE COMPLETE RESULT
-> IMMEDIATE GITHUB SAVE
-> READBACK / COUNT / FIELD RECONCILIATION
-> ONLY THEN NEXT ITEM
```

`HTTP 200`, `SUCCEEDED`, request count or cost alone do not prove project completeness. `OUTCOME_UNKNOWN` is never blindly replayed.

Status: **APPROVED / ACTIVE**.

---

## Step 3R — recovery of incomplete acquisition

This is a job-specific recovery pattern governed by Step3 durability/accounting rules, not a separate universal analytical method.

Status: **JOB-SPECIFIC RECOVERY PATTERN**.

---

## Step 4 — first post-acquisition triage

**Purpose:** remove obvious noise/scope failures while preserving useful uncertainty for later row-level/Search resolution.

**Failure classes:** family-level triage overstated as full cleanup; low frequency used as irrelevance; association volume over-promoted into semantic acceptance.

**Root causes:**

```text
CATEGORY COVERAGE != ROW-LEVEL ACCOUNTING
LOW FREQUENCY != IRRELEVANCE
ASSOCIATION / VOLUME SIGNAL != SEMANTIC FIT
```

**Control:** distinct KEEP/REVIEW/exclusion reasons, low-frequency non-equivalence, association as probe vocabulary, and no claim of full cleanup without row-level provenance.

Status: **APPROVED / ACTIVE**.

---

## Step 5 — targeted second acquisition

**Purpose:** run a second bounded acquisition only for named information gaps left by pass one.

Permanent partial lesson:

```text
SECOND ACQUISITION
REQUIRES EXPLICIT INFORMATION GAIN
!= RECURSIVE KEYWORD COLLECTION
```

Each probe must state the uncertainty it can resolve and why persisted evidence cannot already answer it.

Status: **PARTIALLY DEFINED / NOT YET UNIVERSALLY VALIDATED**.

---

## Step 6 — demand dynamics / seasonality

No owner-approved reusable method has yet been fully earned.

Status: **UNVALIDATED**.

---

## Step 6A — acquisition coverage revalidation

No owner-approved reusable method has yet been fully earned.

Status: **UNVALIDATED**.

---

## Step 7 — row-level semantic cleanup

**Purpose:** classify every acquired phrase occurrence/unique phrase conservatively without pretending unresolved task/page questions are solved.

### Failure 1 — family triage overstated as row-level cleanup

**Root cause:** category-level decisions were treated as member-level accounting.

**Control:** exact source occurrence + unique phrase reconciliation; every active row receives an explicit state.

### Failure 2 — default KEEP fallthrough

**Root cause:**

```text
NO REJECTION RULE MATCHED
WAS TREATED AS
POSITIVE RELEVANCE EVIDENCE
```

**Control:** KEEP requires positive semantic/business evidence. Ambiguous potentially useful demand goes to REVIEW.

### Failure 3 — arithmetic QA substituted for semantic QA

**Root cause:** no dropped/duplicate rows was treated as proof that the decisions themselves were correct.

**Control:** adversarial semantic QA capable of finding new error classes; fix causes/classes and rerun the whole set.

### Failure 4 — volume/association used as semantic proof

**Control:** low frequency alone never excludes; high count/association alone never promotes.

Status: **APPROVED / ACTIVE AFTER CORRECTION**.

---

## Step 8 — Search-stage semantic freeze

Detailed authority: `STEP_08_SEARCH_STAGE_FREEZE_METHOD.md`.

**Core failure:** evaluation dimensions such as business relevance/internal priority were turned into supposed evidence routes even though no independent source could execute those routes.

**Root cause:**

```text
EVALUATION DIMENSION
WAS CONFUSED WITH
OBSERVABLE EVIDENCE SOURCE
```

**Control:** source-to-method trace; unresolved routes must identify a real independent evidence source and executable action.

```text
EVALUATION_DIMENSION != EVIDENCE_ROUTE
```

Status: **APPROVED / ACTIVE**.

---

## Step 9 — ordinary Search validation

No owner-approved reusable full method has yet been earned. The stage remains unvalidated as a complete permanent method.

Reusable non-repeat boundaries earned without promoting the full method:

```text
EXACT QUERY OBSERVATION != UNPROBED QUERY EVIDENCE
EXACT QUERY OBSERVATION != FAMILY COVERAGE WITHOUT DECLARED GENERALIZATION
NORMALIZED PROJECTION != RAW PROVIDER BODY
RAW FIDELITY LIMITATION MUST CHANGE THE CLAIM THAT MAY BE MADE
ORDINARY SEARCH EVIDENCE MUST REMAIN CLIENT-VISIBLE WHEN MATERIAL
```

**Root cause prevented:** bounded query evidence or a normalized export can be mistaken for broader/raw evidence, and material ordinary-Search reasoning can disappear when a later AI layer is packaged.

**Control:** preserve exact observation scope, declared generalization rule, raw/projection state and client-facing downstream use. These controls do not validate sampling, provider acquisition or the complete Step-9 method.

Status: **UNVALIDATED / NARROW NON-REPEAT CONTROLS ACTIVE**.

---

## Step 10 — user-task / Search clustering

Detailed authorities:

- `STEP_10_CLUSTERING_GRANULARITY_METHOD.md`
- `STEP_10_TASK_FIRST_SORTING_DECISION_METHOD.md`
- `STEP_10_SORTING_AND_QA_METHOD.md`

**Core lesson:** a universal method does not mean domain-free execution or a ban on scoped local rules.

```text
EXECUTABLE METHOD
= REUSABLE TASK-FIRST CORE
+ CURRENT DOMAIN PROFILE
+ CURRENT CONSTRAINTS
```

**Root cause prevented:** stripping all local rules in the name of universality can remove real deliverable/business constraints just as badly as hard-coding one client's vocabulary into the core method.

Additional atomic-correction lesson:

```text
CORRECTED CLUSTER / TASK ID != CORRECTED ROW
```

When canonical assignment changes, every field derived from the target cluster/task contract must be rebuilt and compared with that target contract; checking only that the ID changed is insufficient.

Status: **APPROVED / ACTIVE**.

---

## Step 11 — page ownership / phrase→page mapping

Detailed authority: `STEP_11_PAGE_OWNERSHIP_METHOD.md`.

### Failure 1 — transient acquisition evidence

**Root cause:** request/tool success treated as durable project evidence.

**Control:** save/readback before next provider/browser/code acquisition.

### Failure 2 — cluster ownership treated as complete phrase mapping

**Root cause:** cluster-level completeness substituted for final member-row accounting.

**Control:** one final phrase→page row per active phrase.

### Failure 3 — representative query/cluster label treated as every member's task

**Control:** full member coherence review; explicit correction overlay/split/unresolved state when contradicted.

### Failure 4 — target page conflated with observed Search relevant URL

**Control:** analyst target and observed Search behavior are separate evidence dimensions.

Status: **APPROVED / ACTIVE**.

---

## Step 12 — structural/content-routing actions

Detailed authority: `STEP_12_STRUCTURAL_ACTION_METHOD.md` and companion Step12 gates.

Key permanent causal lessons:

```text
LEXICAL CLUE != PAGE/TASK AUTHORITY
PHRASE VISIBILITY != COHERENCE PROOF
PHRASE COUNT != DEMAND
ACTION LABEL != DIAGNOSIS
ACTION != EVIDENCE FOR ITSELF
NO SINGLE OWNER != CONTENT GAP
OLD INVENTORY ABSENCE != CURRENT SITE ABSENCE
BUSINESS TRUTH != CLIENT/OWNER STRATEGIC GOAL
KEEP STRUCTURAL OWNER != PERFORMANCE GOOD
ROUTING EDGE != IMPLEMENTABLE CURRENT LINK
KNOWN DEFECTS FIXED != GLOBAL COHERENCE PROVEN
HISTORICAL DOWNSTREAM PASS != VALID AFTER MATERIAL UPSTREAM MUTATION
NEW CANONICAL UNIT ID + OLD CANONICAL UNIT METADATA = FAIL
```

**Root pattern:** repeated false PASSes came from substituting representation consistency/previous acceptance for independent current evidence and falsification.

**Control:** current site/content, business goal evidence, real demand, Search boundary when material, alternatives before CREATE, evidence-derived confidence, atomic correction materialization against the canonical target-unit contract, independent global coherence, downstream invalidation/rebuild and GitHub readback.

Status: **APPROVED / ACTIVE**.

---

## Step 13 — competing-page / cannibalization diagnosis

Detailed authority: `STEP_13_COMPETING_PAGE_DIAGNOSIS_METHOD.md`.

### Failure 1 — research source found but not operationalized

**Root cause:** official/evidence source discovery was allowed to remain narrative “ideal evidence” rather than becoming a requirement/mode/access state/claim boundary/QA gate.

```text
SOURCE_DISCOVERED != SOURCE_OPERATIONALIZED
LIMITATION_DISCLOSED != LIMITATION_GOVERNED
```

### Failure 2 — current overlap/history/harm conflated

```text
CURRENT MULTI-URL SIGNAL
!= HISTORICAL COMPETITION
!= PROVEN HARM
```

### Control

Declared base-public vs enhanced/history-required mode; explicit optional/unavailable states; claim boundary mechanically changes with evidence mode; no destructive remediation beyond evidence level.

Status: **APPROVED / ACTIVE**.

---

## Step 14 — Search-only architecture freeze

Detailed authority: `STEP_14_SEARCH_ONLY_ARCHITECTURE_FREEZE_METHOD.md` and companion discovery/reliability/sync rules.

### Failure 1 — closed known URL set treated as complete current site

**Root cause:** anti-speculation was overextended into a ban on independent discovery.

```text
CLOSED LIST CANNOT PROVE ITS OWN COMPLETENESS
```

### Failure 2 — source/target existence treated as current edge

**Root cause:** recommendation and as-is topology were not separate fields.

```text
SOURCE_LIVE + TARGET_LIVE != EDGE_IMPLEMENTED
```

### Failure 3 — deterministic evidence requirement became unnecessary custom infrastructure

**Root cause:** manual-reading limitations were overgeneralized into custom crawler requirement.

**Control:** native-tool capability review before custom code.

### Failure 4 — isolated network success treated as runner reliability

**Control:** staged runner qualification + observability + hard bounds + terminal state.

### Failure 5 — branch identity treated as current authority / conflicts not semantically classified

**Control:** fetch/compare/safe sync and evidence-conflict classification before authority read.

Status: **APPROVED / ACTIVE**.

---

## Step 15 — AI-case selection

Detailed authority: `STEP_15_AI_CASE_SELECTION_METHOD.md`.

### Failure 1 — candidate lineage manually reconstructed

**Root cause:** memory/manual remapping substituted for exact authoritative-ID joins.

**Control:** exact upstream lineage joins; representative query/owner/pair references come from authority.

### Failure 2 — information-gain logic used as the only selection track

**Root cause:** diagnostic probe value was treated as the entire evaluation-design requirement.

**Control:** diagnostic probes and stability controls are separate roles when controls are needed for interpretation.

### Failure 3 — diagnostic set overgeneralized

**Control:** selected set is non-representative unless a separate sampling design proves representativeness.

Status: **APPROVED / ACTIVE**.

---

## Step 16 — AI evidence acquisition

No owner-approved reusable full method has yet been earned.

Narrow evidence-integrity boundaries may be reused without claiming a validated acquisition method:

```text
AI REQUEST EXECUTED != AI-NATIVE ANALYTICAL VALUE
PROVIDER / PROXY SURFACE != CONSUMER SURFACE
NORMALIZED OBSERVATION != VERBATIM RAW EVIDENCE
AI EVIDENCE NOT PERSISTED + READ BACK != DURABLE EVIDENCE
```

These boundaries govern preservation and claims only. They do not validate provider choice, probing design, sampling, repetition cadence or the complete Step-16 method.

Status: **UNVALIDATED / NARROW NON-REPEAT CONTROLS ACTIVE**.

---

## Step 17 — Search-vs-AI comparison

Detailed authority: `STEP_17_SEARCH_VS_AI_COMPARISON_METHOD.md`.

Permanent lessons:

```text
EXACT-QUERY OBSERVATION != USER-JOB-FAMILY GENERALIZATION
SINGLE SNAPSHOT != LONGITUDINAL STABILITY
GENSEARCH/AI PROXY != CONSUMER SURFACE CLAIM
NO ARCHITECTURE CHANGE != NO CONTENT CHANGE
SOURCE URL/TITLE != DIRECT CONTENT EVIDENCE
LIMITATION DISCLOSED BUT NOT BOUNDING CLAIM != VALID LIMITATION GOVERNANCE
```

**Root pattern:** first-pass comparison risked compressing scope/confidence/provenance and content-vs-architecture into one verdict.

**Control:** scope ledger, temporal evidence class, architecture/content verdict separation, direct source provenance and no architecture CHANGE from one bounded AI snapshot alone.

Every material case must also preserve a downstream causal object:

```text
WHY SELECTED BEFORE AI
-> FROZEN SEARCH-ONLY DECISION
-> AI EVIDENCE
-> SEARCH-vs-AI COMPARISON
-> CHANGE | DE_RISK | NO_CHANGE | INSUFFICIENT
-> ARCHITECTURE EFFECT
-> CONTENT EFFECT
-> EXACT DOWNSTREAM ACTION OR EXPLICIT NO-ACTION
-> LIMITATION / RECHECK
```

```text
AI_NATIVE_VALUE != FACT_OF_AI_REQUESTS
SUPPORTED NO_CHANGE / DE_RISK != NO RESULT
```

Status: **APPROVED / ACTIVE**.

---

## Step 18 — prioritization / implementation readiness

Detailed authority: `STEP_18_PRIORITIZATION_AND_IMPLEMENTATION_READINESS_METHOD.md`.

This lesson was promoted after an owner-authorized external method audit.

### Failure 1 — analytical priority overstated as implementation-ready order

**What failed:** evidence-based priority tiers were sound, but the final wording treated them too close to a ready production sequence while real implementation variables remained unknown.

**Root cause:**

```text
ANALYTICAL IMPORTANCE
+ EXPLICIT UNKNOWN IMPLEMENTATION FIELDS
WERE STILL ALLOWED TO PRODUCE
IMPLEMENTATION-READY LANGUAGE
```

**Control:** separate `IDEAL_ANALYTICAL_PRIORITY` from `EXPECTED_IMPLEMENTATION_PRIORITY`; missing real calibration forces `PENDING_CALIBRATION` and blocks implementation-ready wording.

### Failure 2 — “do not guess effort” was mistaken for finishing the effort problem

**Root cause:** the no-fabrication safety rule had no second-stage calibration workflow.

```text
NO GUESS != CALIBRATION COMPLETE
```

**Control:** effort state/value/evidence source; real implementer/client/history evidence required for implementation-ready ordering.

### Failure 3 — execution owner/capacity/timeline missing

**Root cause:** the step was designed as analyst ranking rather than a two-layer analytical-versus-organizational decision.

**Control:** owner, owner confirmation, capacity, delivery window and dependency readiness fields for implementation-ready mode.

### Failure 4 — recheck trigger used as if it were an outcome measurement plan

**Root cause:** uncertainty governance and post-implementation evaluation were conflated.

```text
RECHECK TRIGGER != SUCCESS METRIC
```

**Control:** expected outcome, baseline, success metric, measurement source/window/readiness and post-implementation review trigger.

### Failure 5 — accounting batch masqueraded as executable work item

**Root cause:** accounting convenience substituted for task granularity.

```text
ACCOUNTING BATCH != IMPLEMENTATION WORK PACKAGE
```

**Control:** decompose large batches by real shared execution properties while preserving exact source membership.

### Failure 6 — public business relevance too close to client-confirmed importance

**Root cause:** no-guess policy existed but stronger business-priority wording was not mechanically gated by a client-importance state.

```text
PUBLIC BUSINESS RELEVANCE != CLIENT-CONFIRMED BUSINESS IMPORTANCE
```

**Control:** separate client business importance state/value and allow it to alter expected implementation priority only when real evidence exists.

### Failure 7 — technical detail substituted for owner-facing explanation

**Root cause:** technical completeness was mistaken for owner comprehension.

**Control:** mandatory plain-language `why / what / result` summary before authorization and after execution under `STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md`.

### Failure 8 — analytical action mistaken for implementation specification

**Root cause:** a prioritized analytical row was treated as executable merely because it had an action label, target and priority.

**Control:** `ANALYTICAL ACTION != IMPLEMENTATION SPECIFICATION`. A material action may remain `IMPLEMENTATION_SPEC_STATE = NOT_READY / PENDING_DETAIL` until current state, direct evidence, reason, target state, exact object/location, required topics/relationships, justified example, acceptance criteria, dependencies and do-not-do boundary are materialized where applicable. Missing private owner/effort/capacity/timing remains explicit and is never fabricated.

Status: **APPROVED / ACTIVE AFTER CORRECTION**.

---

## Steps 19–21

Current permanent-method state:

```text
STEP19 = UNVALIDATED / OWNER-DIRECTED CORRECTED METHOD CANDIDATE / ACTIVE NON-REPEAT CONTROL
STEP20 = APPROVED / ACTIVE AFTER OWNER-DIRECTED EXTERNAL METHOD AUDIT + CORRECTION
STEP21 = UNVALIDATED
```

Step19 non-repeat boundary:

```text
ONE CURRENT FINAL SEMANTIC MASTER -> ALL CLIENT SEMANTIC VIEWS
ONE CURRENT CANONICAL ACTION AUTHORITY -> ALL CLIENT ACTION / BUSINESS / PAGE / REPORT VIEWS
POLISHED DERIVATIVE != CURRENT AUTHORITY PROOF
```

Step20 non-repeat boundary:

```text
PHYSICAL / DISTRIBUTION QA
+ SEMANTIC / CANONICAL AUTHORITY QA
+ PRODUCT / DELIVERABLE ACCEPTANCE QA
= GLOBAL RELEASE PASS

CONSISTENT BUGGY DERIVATIVES != INDEPENDENT SEMANTIC VALIDATION
```

Step19 remains unvalidated as a complete permanent method. Step21 still requires fresh method research/review. The specific current Step20 authority supersedes the older grouped status and is recorded in `STEP_20_PERMANENT_LESSONS_LEDGER_AUTHORITY_CORRECTION_2026-09-04.md`.

---

## Step 22 — job close

Partially governed by `JOB_WORKSPACE_LIFECYCLE.md`.

Permanent boundary:

```text
DELIVERABLE PRODUCED != JOB SAFE TO CLOSE
```

Close only after required handoff/revisions and pending provider/operator actions are finished and current job state explicitly allows closure.

Status: **PARTIALLY DEFINED**.

---

## Cross-step authority mutation and uncertainty continuity

**Failure class:** a material authority mutation can update a visible key while dependent fields and downstream consumers retain the old semantic state; output-completeness pressure can also erase unresolved states.

**Root cause:** correction was treated as a local patch and historical PASS as timeless.

**Control:** apply `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`:

```text
MATERIAL AUTHORITY MUTATION
-> IMPACT SET
-> DEPENDENT-FIELD REBUILD
-> MATERIAL-CONSUMER REBUILD
-> CURRENT-AUTHORITY RECONCILIATION
-> INDEPENDENT QA
-> READBACK

OUTPUT COMPLETENESS MUST NOT ERASE TRUTHFUL UNCERTAINTY
```

Status: **ACTIVE / UNIVERSAL CROSS-STEP NON-REPEAT CONTROL**.
# Permanent universality self-check

Before modifying this ledger:

```text
CAUSE PRESERVED = true
CONCRETE JOB IDENTITY COPIED = false
CONCRETE CLIENT DOMAIN/URL COPIED = false
CURRENT JOB COUNTS/IDS/SHAS COPIED = false
CURRENT JOB RESULT/STATUS COPIED = false
DETAILED JOB PROOF REMAINS LEVEL2 = true
```

A permanent lesson should tell the next analyst **why the previous approach failed and what mechanism prevents recurrence**, without teaching the next analyst the vocabulary or numbers of a prior client.
