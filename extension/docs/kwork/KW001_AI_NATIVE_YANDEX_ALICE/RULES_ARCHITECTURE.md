# KW-001 — RULES ARCHITECTURE

Date: 2026-08-29  
Status: **ACTIVE / UNIVERSAL / OWNER-APPROVED / OWNER-LOCKED**

This document defines where KW-001 rules live, what each layer is responsible for, and how ChatGPT must use them before executing any major step.

The purpose is to prevent three failures:

```text
1. rules scattered across documents so an important control is missed;
2. rules treated as a mechanical checklist without understanding why they exist;
3. external research collected correctly but then ignored while unsupported method elements are invented.
```

The system separates **universal process rules**, **step-specific methodology/lessons**, and **job-specific execution evidence**.

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

They do **not** contain client-specific facts or row-level job results.

### Mandatory dialogue-start Yandex Marketing Bridge capability alignment

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
5. explain relevant previous mistakes, their root cause, and the non-repeat control;
6. search the current internet for materials specifically relevant to the step;
7. provide direct sources/links and distinguish official evidence, industry practice, project evidence and analyst heuristic;
8. use the external research adversarially — search for evidence that the planned method is wrong or incomplete, not only confirming evidence;
9. apply SOURCE_TO_METHOD_TRACEABILITY_GATE.md to EVERY material state, route, threshold, filter and decision rule;
10. remove any unsupported or non-executable method element before authorization;
11. explain the practical method and why it solves the step goal;
12. state what the step will NOT decide yet;
13. define the pass gate before execution;
14. wait for explicit owner authorization;
15. execute only the authorized step;
16. verify actual output, preservation and non-repeat controls;
17. report quantitative reconciliation and update the whole roadmap;
18. stop before the next major step.
```

### Internet research is mandatory, not optional

For every new major analytical/provider step:

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
5. explicitly labelled analyst heuristic.
```

If no authoritative rule exists, say so. Do not invent an industry standard.

### Research is not validated until it constrains the method

Canonical rule:

```text
RESEARCH_COLLECTED != METHOD_VALIDATED
```

Every material method element must show:

```text
METHOD ELEMENT
→ DIRECT SOURCE / PROJECT EVIDENCE
→ EXACT CLAIM SUPPORTED
→ PROJECT-SPECIFIC PART, IF ANY
→ REAL EXECUTABLE NEXT ACTION / OUTPUT
```

If this trace is missing:

```text
METHOD_ELEMENT = UNSUPPORTED
STEP_AUTHORIZATION = BLOCKED
EXECUTION = BLOCKED
```

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

A step is not validated merely because a roadmap row exists or a job once completed it.

```text
ROADMAP_STAGE_EXISTS != METHODOLOGY_VALIDATED
JOB_EXECUTION_SUCCESS != PERMANENT_METHOD_VALIDATION
```

## Mechanical repetition is prohibited

Before applying a recorded rule, ChatGPT must reconstruct:

```text
WHAT FAILED?
WHY DID IT FAIL?
WHAT FALSE ASSUMPTION OR PROCESS GAP CAUSED IT?
HOW DOES THE RECORDED CONTROL BLOCK THAT CAUSE?
DOES THE SAME CAUSE ACTUALLY APPLY TO THE CURRENT JOB/STEP?
HAS CURRENT EXTERNAL RESEARCH CHANGED THE METHOD?
DO THE CURRENT SOURCES ACTUALLY SUPPORT EACH MATERIAL METHOD ELEMENT?
```

If ChatGPT cannot explain this causal and source chain, the step is not ready for authorization.

Canonical rules:

```text
RULE_RECALL_WITHOUT_CAUSAL_UNDERSTANDING != METHOD_VALIDATION
SOURCE_COLLECTION_WITHOUT_METHOD_TRACEABILITY != METHOD_VALIDATION
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
job-specific deviations;
step execution evidence;
reconciliation and acceptance truth;
causal postmortems for errors found in this job.
```

Job-specific evidence may reveal a reusable lesson, but it does not automatically mutate Layer A or Layer B. Permanent rule changes require explicit owner instruction.

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
F. READ CURRENT JOB MANIFEST / FLOW
G. READ PREVIOUS STEP EVIDENCE AND CURRENT STEP PRE-STEP / POSTMORTEM ARTIFACTS
H. RECONSTRUCT WHY THE CURRENT STEP EXISTS
I. RECONSTRUCT RELEVANT PREVIOUS ERRORS + ROOT CAUSES
J. SEARCH CURRENT EXTERNAL MATERIALS FOR THIS STEP
K. BUILD SOURCE-TO-METHOD TRACE FOR EVERY MATERIAL METHOD ELEMENT
L. CHALLENGE / SIMPLIFY THE PLANNED METHOD; REMOVE UNSUPPORTED STATES/ROUTES
M. EXPLAIN METHOD + DIRECT SOURCES + NON-REPEAT CONTROLS TO OWNER
N. WAIT FOR OWNER AUTHORIZATION
O. EXECUTE
P. VERIFY
Q. REPORT / UPDATE ROADMAP / STOP
```

If the step-specific method is missing or does not cover a material operation:

```text
STEP_METHOD_STATUS = UNVALIDATED
METHOD_RESEARCH_REQUIRED = true
EXECUTION = BLOCKED until pre-step review is complete
```

If a material state/rule has no trace:

```text
SOURCE_TO_METHOD_TRACEABILITY = FAIL
EXECUTION = BLOCKED
```

---

# 5. Precedence and conflict handling

If documents appear to conflict:

```text
1. explicit latest owner instruction;
2. owner-approved universal process rule;
3. owner-approved step-specific lesson/method rule;
4. current job's frozen scope/manifest;
5. current job execution artifact;
6. analyst convenience or old historical artifact.
```

A historical PASS does not override later evidence that the method was defective.

A script does not prove its own correctness.

A successful API/workflow run does not prove the analytical goal was achieved.

A list of good external sources does not prove that the method built afterward is supported by those sources.

---

# 6. How a new error must be recorded

When a material error is discovered, first record it in the current job with:

```text
WHAT WAS DONE WRONG
OBSERVED CONSEQUENCE
ROOT CAUSE
WHY THE OLD METHOD WAS INVALID OR INSUFFICIENT
DIRECT SOURCES USED TO RECHECK IT
WHAT EACH SOURCE ACTUALLY SUPPORTS
HOW IT WAS CORRECTED
WHAT QA EXPOSED THE PROBLEM
CURRENT LIMITS
```

If the lesson is reusable across jobs, ChatGPT must propose/persist it only under owner authorization.

A permanent lesson must preserve the causal explanation and source-to-method trace, not only the final instruction.

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
What is still project-specific?
Why is the project-specific element necessary?
What real action/output does each route/state produce?
Can any state/rule be removed without losing necessary evidence?
How exactly will we perform the step now?
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
    ↓ how every step must be approached
SOURCE_TO_METHOD_TRACEABILITY_GATE
    ↓ forces each invented rule/state/route to be justified by sources or proven project need
STEP_RULES_INDEX
    ↓ tells us whether the step has a validated method and where it lives
STEP-SPECIFIC METHOD / LESSONS
    ↓ how this exact step works + prior failures + direct sources
CURRENT JOB MANIFEST / FLOW / EVIDENCE / POSTMORTEM
    ↓ what happened in this exact job
CURRENT INTERNET RESEARCH
    ↓ rechecks freshness and challenges the method
SOURCE→METHOD TRACE
    ↓ blocks unsupported/non-executable method elements
OWNER AUTHORIZATION
    ↓
EXECUTION + VERIFICATION
    ↓
JOB RESULT / LESSON PROMOTION ONLY IF OWNER APPROVES
```

Markers:

```text
KW001_RULES_ARCHITECTURE_ACTIVE = true
KW001_UNIVERSAL_PROCESS_LAYER_REQUIRED = true
KW001_DIALOGUE_START_BRIDGE_REVIEW_REQUIRED = true
KW001_DIALOGUE_START_BRIDGE_REVIEW_ONCE_PER_DIALOGUE = true
KW001_ROADMAP_TO_BRIDGE_MAP_REQUIRED = true
KW001_SOURCE_TO_METHOD_TRACEABILITY_GATE_REQUIRED = true
KW001_STEP_RULES_INDEX_REQUIRED = true
KW001_PER_STEP_METHOD_LAYER_REQUIRED = true
KW001_JOB_SPECIFIC_EVIDENCE_LAYER_REQUIRED = true
KW001_CURRENT_EXTERNAL_RESEARCH_EVERY_MAJOR_STEP = true
KW001_DIRECT_SOURCES_EVERY_MAJOR_STEP = true
KW001_RESEARCH_COLLECTED_NOT_EQUAL_METHOD_VALIDATED = true
KW001_UNSUPPORTED_METHOD_ELEMENT_BLOCKS_EXECUTION = true
KW001_NON_EXECUTABLE_EVIDENCE_ROUTE_BLOCKS_EXECUTION = true
KW001_MECHANICAL_RULE_REPLAY_PROHIBITED = true
KW001_CAUSAL_ERROR_UNDERSTANDING_REQUIRED = true
KW001_UNVALIDATED_STEP_BLOCKS_EXECUTION = true
```