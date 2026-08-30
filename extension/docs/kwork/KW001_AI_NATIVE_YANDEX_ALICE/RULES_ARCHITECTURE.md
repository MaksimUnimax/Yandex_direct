# KW-001 — RULES ARCHITECTURE

Date: 2026-08-29  
Last corrected: 2026-08-30  
Status: **ACTIVE / UNIVERSAL / OWNER-APPROVED / OWNER-LOCKED**

This document defines where KW-001 rules live, what each layer is responsible for, and how ChatGPT must use them before executing any major step.

The purpose is to prevent three failures:

```text
1. rules scattered across documents so an important control is missed;
2. rules treated as a mechanical checklist without understanding why they exist;
3. external research collected correctly but then ignored while unsupported method elements are invented.
```

The system separates **universal process rules**, **step-specific methodology/lessons**, and **job-specific execution evidence**.

This separation defines authority, storage and scope. It does **not** prohibit an executable method from using current-domain data.

Canonical meaning of universality:

```text
EXECUTABLE METHOD = UNIVERSAL CORE + CURRENT JOB PROFILE + CURRENT CONSTRAINTS
UNIVERSAL != DOMAIN-FREE EXECUTION
LOCAL RULE MUST BE SCOPED != LOCAL RULE MUST BE REMOVED
LAYER SEPARATION != BAN ON CROSS-LAYER USE
```

A universal or step-specific method may:

```text
reference domain examples;
define a domain-profile schema;
require the actual site and business model;
use real cluster IDs and names;
use exact local phrases and exceptions;
use job-specific thresholds or target counts;
incorporate owner/client/deliverable constraints.
```

The requirement is that scope and authority remain explicit. A current-job rule is not automatically a rule for every job, but it remains fully valid for the current job.

---

# 1. Rule hierarchy

## Layer A — universal process rules

These rules apply to every KW-001 job and every major step.

Canonical files:

```text
DIALOGUE_AND_ANALYTICAL_DISCIPLINE.md
STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md
PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md
SOURCE_TO_METHOD_TRACEABILITY_GATE.md
JOB_WORKSPACE_LIFECYCLE.md
RULES_ARCHITECTURE.md
```

They define HOW ChatGPT must think, research, communicate, authorize, execute, verify and report a step.

Layer-A files normally do not serve as the authoritative storage for one client's row-level results. They may still refer to domain examples or require current-job inputs. Most importantly, Layer A never blocks the executable method from loading and applying Layer-B and Layer-C data.

### Mandatory dialogue-start Yandex Marketing Bridge capability alignment

Canonical Yandex Marketing Bridge GitHub source for this project:

https://github.com/MaksimUnimax/Yandex_direct/tree/roadmap/kwork-productization-2026-08-28/extension

At the beginning of every new dialogue/session for KW-001, before executing or continuing any roadmap step, ChatGPT must perform the following gate **once per dialogue**:

```text
1. read the current Yandex Marketing Bridge implementation from the canonical GitHub extension/ tree at the current branch/HEAD; do not rely on memory or an old dialogue summary;
2. identify the current extension version, accepted service surfaces, execution/batch/recovery capabilities and material limitations from current source, canonical docs and accepted test evidence;
3. report to the owner in chat a practical functional inventory of the current Bridge and provide the canonical GitHub link to the extension;
4. read the current KW-001 roadmap/implementation plan and map EVERY roadmap step to one of:
   BRIDGE_REQUIRED
   BRIDGE_CONDITIONAL
   NO_BRIDGE;
5. for every BRIDGE_REQUIRED or BRIDGE_CONDITIONAL step, name the exact Bridge surface that can be used, such as Wordstat, ordinary Search/SERP, Webmaster, Metrika, Direct, GenSearch, provider-batch/recovery, cost ledger or workspace/lifecycle controls;
6. distinguish provider evidence acquisition performed by Bridge from analytical judgment owned by ChatGPT and authorization owned by the human owner;
7. do not treat this capability map as authorization to make provider calls or execute a roadmap step;
8. if the extension or roadmap materially changes during the dialogue, refresh the affected part of the mapping before the affected step is executed.
```

This startup review must happen before the normal current-step pre-step process. It is not repeated mechanically before every step in the same dialogue unless the extension/roadmap materially changes or the owner explicitly asks for a refresh.

Canonical startup markers:

```text
DIALOGUE_START_BRIDGE_REVIEW_REQUIRED = true
DIALOGUE_START_BRIDGE_REVIEW_ONCE_PER_DIALOGUE = true
DIALOGUE_START_BRIDGE_REVIEW_COMPLETE = true before step execution
ROADMAP_TO_BRIDGE_MAP_COMPLETE = true before step execution
BRIDGE_CAPABILITY_MAP_IS_NOT_EXECUTION_AUTHORIZATION = true
```

If the dialogue-start Bridge inventory or roadmap-to-Bridge mapping has not been completed:

```text
STEP_EXECUTION = BLOCKED
```

### Universal requirements before every major step

Before execution ChatGPT must:

```text
1. reconstruct the whole Kwork goal and current job state;
2. identify the exact current-step goal and required output;
3. check STEP_RULES_INDEX.md for the current methodology status and canonical step-method file(s);
4. read the step-specific methodology/lessons entry/file when one exists;
5. load and apply the current job profile, domain vocabulary, site/business data, real IDs and current constraints required by that method;
6. explain relevant previous mistakes, their root cause, and the non-repeat control;
7. search the current internet for materials specifically relevant to the step when current external research is required;
8. provide direct sources/links and distinguish official evidence, industry practice, project evidence and analyst heuristic;
9. use the external research adversarially — search for evidence that the planned method is wrong or incomplete, not only confirming evidence;
10. apply SOURCE_TO_METHOD_TRACEABILITY_GATE.md to EVERY material state, route, threshold, filter and decision rule;
11. retain necessary current-job rules and label their scope; remove only rules that are unsupported for the declared current purpose;
12. explain the practical configured method and why it solves the step goal;
13. state what the step will NOT decide yet unless the current roadmap combines those decisions;
14. define the pass gate before execution;
15. wait for explicit owner authorization when the current gate requires it;
16. execute only the authorized step/configuration;
17. verify actual output, preservation and non-repeat controls;
18. report quantitative reconciliation and update the whole roadmap;
19. stop before the next major step unless the owner authorized continuation.
```

### Internet research is mandatory when the current gate requires it

For every new major analytical/provider step whose method or external behaviour may have changed:

```text
CURRENT_EXTERNAL_METHOD_RESEARCH_REQUIRED = true
DIRECT_SOURCES_REQUIRED = true
ADVERSARIAL_SOURCE_REVIEW_REQUIRED = true
SOURCE_TO_METHOD_TRACEABILITY_REQUIRED = true
```

The research must be **specific to the current step**. Reusing sources from an earlier step without checking whether they answer the current methodological question is not sufficient.

Preferred source order:

```text
1. official / primary source;
2. official search-engine/provider guidance;
3. credible current industry methodology;
4. controlled project/provider evidence;
5. explicitly labelled analyst heuristic;
6. explicit owner/client/deliverable constraint.
```

If no authoritative industry rule exists, say so. A documented project requirement remains a legitimate executable constraint.

### Research is not validated until it constrains the method

Canonical rule:

```text
RESEARCH_COLLECTED != METHOD_VALIDATED
```

Every material method element must show:

```text
METHOD ELEMENT
→ DIRECT SOURCE / PROJECT EVIDENCE / OWNER OR DELIVERABLE REQUIREMENT
→ EXACT CLAIM OR CONSTRAINT SUPPORTED
→ SCOPE: UNIVERSAL / DOMAIN / JOB / ROW / OTHER
→ REAL EXECUTABLE NEXT ACTION / OUTPUT
```

If this trace is missing for a material invented element:

```text
METHOD_ELEMENT = UNSUPPORTED
STEP_AUTHORIZATION = BLOCKED
EXECUTION = BLOCKED
```

A local method element is not unsupported merely because it is local. Its support may be the current site, corpus, owner instruction, client requirement, deliverable or controlled project evidence.

Authority: `SOURCE_TO_METHOD_TRACEABILITY_GATE.md`.

---

# 2. Layer B — step-specific methodology and lessons

Canonical files:

```text
STEP_RULES_INDEX.md
STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md
STEP_<N>_*_METHOD.md when a dedicated permanent step file is registered by STEP_RULES_INDEX.md
```

`STEP_RULES_INDEX.md` answers:

```text
Does this roadmap stage actually have a validated permanent method yet?
Where is the canonical detailed method for this step?
```

`STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` contains permanent cross-step/step lessons and causal error memory.

A dedicated permanent step-method file may be used when the step requires substantial detail. It becomes canonical only when `STEP_RULES_INDEX.md` explicitly registers it.

Every validated step method must preserve:

```text
STEP PURPOSE
APPROVED METHOD
WHY THIS METHOD
METHOD ORIGIN / DIRECT SOURCES
SOURCE-TO-METHOD TRACE
KNOWN ERRORS
ROOT CAUSE
CORRECTED METHOD
NON-REPEAT CONTROLS
PASS GATE
STATUS
```

### Domain configuration inside a universal step method

A Step-B method may directly contain or require:

```text
DOMAIN-SPECIFIC EXAMPLES
REAL CLUSTER / ROUTE / STATE IDS
LOCAL TERMINOLOGY
EXACT PHRASE RULES
SITE-SPECIFIC BOUNDARIES
JOB-SPECIFIC THRESHOLDS
TARGET COUNTS OR RANGES
OWNER DECISIONS
```

These details are valid when their scope is explicit. They may be stored inline, in a companion profile, or in Layer C.

The reusable core and the current profile must be distinguishable, but they are executed together.

A step is not validated merely because a roadmap row exists or a job once completed it.

```text
ROADMAP_STAGE_EXISTS != METHODOLOGY_VALIDATED
JOB_EXECUTION_SUCCESS != PERMANENT_METHOD_VALIDATION
```

## Mechanical repetition is controlled, not confused with legitimate reuse

Before applying a recorded rule, ChatGPT must reconstruct:

```text
WHAT FAILED?
WHY DID IT FAIL?
WHAT FALSE ASSUMPTION OR PROCESS GAP CAUSED IT?
HOW DOES THE RECORDED CONTROL BLOCK THAT CAUSE?
DOES THE SAME CAUSE ACTUALLY APPLY TO THE CURRENT JOB/STEP?
HAS CURRENT EXTERNAL RESEARCH CHANGED THE METHOD?
DO THE CURRENT SOURCES OR REQUIREMENTS SUPPORT EACH MATERIAL METHOD ELEMENT?
IS THIS RULE UNIVERSAL, DOMAIN-SPECIFIC, JOB-SPECIFIC OR ROW-SPECIFIC?
```

A domain/job rule may be reused inside its declared scope without being generalized to all projects.

Canonical rules:

```text
RULE_RECALL_WITHOUT_CAUSAL_UNDERSTANDING != METHOD_VALIDATION
SOURCE_COLLECTION_WITHOUT_METHOD_TRACEABILITY != METHOD_VALIDATION
SCOPED_LOCAL_RULE != MECHANICAL UNIVERSAL REPLAY
```

---

# 3. Layer C — job-specific execution rules and evidence

Location:

```text
work/<JOB_ID>/
```

or an explicitly accepted legacy job workspace such as:

```text
tests/<JOB_ID>/
```

Typical files:

```text
JOB_MANIFEST.md
JOB_FLOW.md
STEP_<N>_PRE_STEP_REVIEW*.md
STEP_<N>_*_MANIFEST*.md
STEP_<N>_*_RESULT*.md / .tsv / .json
STEP_<N>_*_ACCEPTANCE*.md
STEP_<N>_*_CORRECTION*.md
STEP_<N>_*_METHOD_POSTMORTEM*.md
```

This layer contains:

```text
client/site facts;
provider request identities;
rows and counts;
concrete query/page decisions;
real cluster IDs and assignments;
local phrases, terms and exceptions;
job-specific thresholds and count constraints;
job-specific deviations;
step execution evidence;
reconciliation and acceptance truth;
causal postmortems for errors found in this job.
```

Layer-C data is an executable input to the configured method. It is not second-class or optional when the current task needs it.

Job-specific evidence may reveal a reusable lesson, but it does not automatically mutate Layer A or Layer B. Permanent promotion still requires explicit owner instruction.

---

# 4. Required read order before every major step

Canonical order:

```text
A0. ONCE PER DIALOGUE: COMPLETE YANDEX MARKETING BRIDGE CAPABILITY INVENTORY + ROADMAP-TO-BRIDGE MAP
A. READ RULES_ARCHITECTURE.md
B. READ UNIVERSAL PROCESS RULES
C. READ SOURCE_TO_METHOD_TRACEABILITY_GATE.md
D. READ STEP_RULES_INDEX.md FOR CURRENT STEP STATUS + CANONICAL METHOD FILE
E. READ CURRENT STEP METHOD / LESSONS
F. READ CURRENT JOB MANIFEST / FLOW / EVIDENCE / POSTMORTEM
G. LOAD THE CURRENT DOMAIN PROFILE, SITE/BUSINESS DATA, REAL IDS, LOCAL RULES AND CURRENT CONSTRAINTS
H. CONFIGURE THE UNIVERSAL CORE FOR THE CURRENT JOB
I. READ PREVIOUS STEP EVIDENCE AND CURRENT STEP PRE-STEP / POSTMORTEM ARTIFACTS
J. RECONSTRUCT WHY THE CURRENT STEP EXISTS
K. RECONSTRUCT RELEVANT PREVIOUS ERRORS + ROOT CAUSES
L. SEARCH CURRENT EXTERNAL MATERIALS FOR THIS STEP WHEN REQUIRED
M. BUILD SOURCE-TO-METHOD TRACE FOR EVERY MATERIAL METHOD ELEMENT
N. CHALLENGE / SIMPLIFY THE PLANNED METHOD WITHOUT REMOVING NECESSARY LOCAL RULES
O. EXPLAIN CONFIGURED METHOD + DIRECT SOURCES + PROJECT CONSTRAINTS + NON-REPEAT CONTROLS TO OWNER
P. WAIT FOR OWNER AUTHORIZATION WHEN REQUIRED
Q. EXECUTE
R. VERIFY
S. REPORT / UPDATE ROADMAP / STOP OR CONTINUE AS AUTHORIZED
```

If the step-specific method is missing or does not cover a material operation:

```text
STEP_METHOD_STATUS = UNVALIDATED
METHOD_RESEARCH_REQUIRED = true
EXECUTION = BLOCKED until pre-step review is complete
```

If a material invented state/rule has no source, project evidence or current requirement:

```text
SOURCE_TO_METHOD_TRACEABILITY = FAIL
EXECUTION = BLOCKED
```

---

# 5. Precedence and conflict handling

If documents appear to conflict:

```text
1. explicit latest owner instruction;
2. explicit current client/deliverable constraint authorized by owner;
3. owner-approved universal process rule;
4. owner-approved step-specific lesson/method rule;
5. current job's frozen scope/manifest/domain profile;
6. current job execution artifact;
7. analyst convenience or old historical artifact.
```

A universal default may be overridden by a more specific authorized current-job rule when the universal method declares that configuration point.

A historical PASS does not override later evidence that the method was defective.

A script does not prove its own correctness.

A successful API/workflow run does not prove the analytical goal was achieved.

A list of good external sources does not prove that the method built afterward is supported by those sources.

A local rule does not need to become universal in order to be correct and binding for its current scope.

---

# 6. How a new error must be recorded

When a material error is discovered, first record it in the current job with:

```text
WHAT WAS DONE WRONG
OBSERVED CONSEQUENCE
ROOT CAUSE
WHY THE OLD METHOD WAS INVALID OR INSUFFICIENT
DIRECT SOURCES / PROJECT EVIDENCE / OWNER REQUIREMENT USED TO RECHECK IT
WHAT EACH SOURCE OR REQUIREMENT ACTUALLY SUPPORTS
SCOPE OF THE CORRECTED RULE
HOW IT WAS CORRECTED
WHAT QA EXPOSED THE PROBLEM
CURRENT LIMITS
```

If the lesson is reusable across jobs, ChatGPT may propose promotion under owner authorization.

A permanent lesson must preserve the causal explanation and source-to-method trace, not only the final instruction.

A job-specific correction remains valid even when it is not promoted.

---

# 7. Minimum owner-facing explanation before authorization

Every step explanation must make these questions answerable:

```text
What are we trying to achieve?
Why is this step necessary?
What did we previously get wrong in this step, if anything?
Why did that error happen?
What current sources did we check?
What EXACT claim does each source support?
Which method element uses that claim?
Which current site/business/owner/deliverable constraints apply?
Which method elements are universal, domain-specific, job-specific or row-specific?
Why is each project-specific element necessary?
What real action/output does each route/state produce?
Can any state/rule be removed without losing necessary evidence or constraints?
How exactly will we perform the configured step now?
What checks will catch a repeat of the known errors?
What output must exist before we call the step complete?
```

At the end of the detailed explanation, apply the mandatory non-specialist summary from `STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md`.

---

# 8. Structural summary

```text
DIALOGUE START
    ↓ once per dialogue: read current Bridge + report capabilities + map all roadmap steps to Bridge/no-Bridge
UNIVERSAL PROCESS RULES
    ↓ reusable core and process controls
SOURCE_TO_METHOD_TRACEABILITY_GATE
    ↓ requires support from sources, project evidence or explicit current requirements
STEP_RULES_INDEX
    ↓ tells us whether the step has a validated method and where it lives
STEP-SPECIFIC METHOD / LESSONS
    ↓ reusable method plus allowed configuration points
CURRENT JOB MANIFEST / FLOW / DOMAIN PROFILE / EVIDENCE / POSTMORTEM
    ↓ actual site, business, IDs, phrases, constraints and decisions
CONFIGURED EXECUTABLE METHOD
    ↓ universal core + current job profile + current constraints
CURRENT INTERNET RESEARCH WHEN REQUIRED
    ↓ rechecks freshness and challenges the method
SOURCE / REQUIREMENT → METHOD TRACE
    ↓ blocks unsupported invented elements without deleting necessary local rules
OWNER AUTHORIZATION WHEN REQUIRED
    ↓
EXECUTION + VERIFICATION
    ↓
JOB RESULT / LESSON PROMOTION ONLY IF OWNER APPROVES
```

Markers:

```text
KW001_RULES_ARCHITECTURE_ACTIVE = true
KW001_UNIVERSAL_PROCESS_LAYER_REQUIRED = true
KW001_UNIVERSAL_MEANS_REUSABLE_CORE_PLUS_CURRENT_PROFILE = true
KW001_LAYER_SEPARATION_IS_SCOPE_NOT_LOCAL_DATA_BAN = true
KW001_DOMAIN_SPECIFIC_EXECUTION_ALLOWED = true
KW001_LOCAL_RULES_MUST_BE_SCOPED_NOT_REMOVED = true
KW001_REAL_IDS_EXACT_PHRASES_AND_LOCAL_THRESHOLDS_ALLOWED = true
KW001_EXPLICIT_TARGET_COUNTS_OR_RANGES_ALLOWED = true
KW001_DIALOGUE_START_BRIDGE_REVIEW_REQUIRED = true
KW001_DIALOGUE_START_BRIDGE_REVIEW_ONCE_PER_DIALOGUE = true
KW001_ROADMAP_TO_BRIDGE_MAP_REQUIRED = true
KW001_SOURCE_TO_METHOD_TRACEABILITY_GATE_REQUIRED = true
KW001_STEP_RULES_INDEX_REQUIRED = true
KW001_PER_STEP_METHOD_LAYER_REQUIRED = true
KW001_JOB_SPECIFIC_EVIDENCE_LAYER_REQUIRED = true
KW001_CURRENT_JOB_PROFILE_IS_EXECUTABLE_INPUT = true
KW001_CURRENT_EXTERNAL_RESEARCH_WHEN_REQUIRED = true
KW001_DIRECT_SOURCES_WHEN_REQUIRED = true
KW001_RESEARCH_COLLECTED_NOT_EQUAL_METHOD_VALIDATED = true
KW001_UNSUPPORTED_INVENTED_METHOD_ELEMENT_BLOCKS_EXECUTION = true
KW001_NON_EXECUTABLE_EVIDENCE_ROUTE_BLOCKS_EXECUTION = true
KW001_CAUSAL_RULE_UNDERSTANDING_REQUIRED = true
KW001_SCOPED_LOCAL_RULE_REUSE_ALLOWED = true
KW001_UNVALIDATED_STEP_BLOCKS_EXECUTION = true
```