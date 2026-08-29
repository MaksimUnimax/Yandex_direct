# KW-001 — RULES ARCHITECTURE

Date: 2026-08-29  
Status: **ACTIVE / UNIVERSAL / OWNER-APPROVED / OWNER-LOCKED**

This document defines where KW-001 rules live, what each layer is responsible for, and how ChatGPT must use them before executing any major step.

The purpose is to prevent two opposite failures:

```text
1. rules scattered across documents so an important control is missed;
2. rules treated as a mechanical checklist without understanding why they exist.
```

The system therefore separates **universal process rules**, **step-specific methodology/lessons**, and **job-specific execution evidence**.

---

# 1. Rule hierarchy

## Layer A — universal process rules

These rules apply to every KW-001 job and every major step.

Canonical files:

```text
DIALOGUE_AND_ANALYTICAL_DISCIPLINE.md
STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md
PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md
JOB_WORKSPACE_LIFECYCLE.md
RULES_ARCHITECTURE.md
```

They define HOW ChatGPT must think, research, communicate, authorize, execute, verify and report a step.

They do **not** contain client-specific facts or row-level job results.

### Universal requirements before every major step

Before execution ChatGPT must:

```text
1. reconstruct the whole Kwork goal and current job state;
2. identify the exact current-step goal and required output;
3. read the step-specific methodology/lessons entry;
4. explain relevant previous mistakes, their root cause, and the non-repeat control;
5. search the current internet for materials specifically relevant to the step;
6. provide direct sources/links and distinguish official evidence, industry practice, project evidence and analyst heuristic;
7. use the external research adversarially — search for evidence that the planned method is wrong or incomplete, not only confirming evidence;
8. explain the practical method and why it solves the step goal;
9. state what the step will NOT decide yet;
10. define the pass gate before execution;
11. wait for explicit owner authorization;
12. execute only the authorized step;
13. verify actual output, preservation and non-repeat controls;
14. report quantitative reconciliation and update the whole roadmap;
15. stop before the next major step.
```

### Internet research is mandatory, not optional

For every new major analytical/provider step:

```text
CURRENT_EXTERNAL_METHOD_RESEARCH_REQUIRED = true
DIRECT_SOURCES_REQUIRED = true
ADVERSARIAL_SOURCE_REVIEW_REQUIRED = true
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

---

# 2. Layer B — step-specific methodology and lessons

Canonical file:

```text
STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md
```

This is the permanent step playbook and error memory.

There must be a separate section for each major methodology step that has been researched or executed.

A step section is not allowed to contain only instructions such as `dedupe`, `cluster`, `clean`, `validate` or `run Search`. It must preserve the reasoning behind those instructions.

## Mandatory per-step section schema

Every validated step entry must answer:

```text
STEP PURPOSE
= what the step is trying to prove/produce for the client task.

METHOD
= how the step should be performed.

WHY THIS METHOD
= why these operations are appropriate for the step goal.

METHOD ORIGIN / SOURCES
= official/current external sources + project evidence + clearly labelled heuristics.

KNOWN ERRORS
= mistakes already observed in this step across rehearsals/jobs.

ROOT CAUSE
= why the mistake happened, not merely what bad output was seen.

CORRECTED METHOD
= what changed after understanding the cause.

NON-REPEAT CONTROLS
= concrete gates that detect/prevent recurrence.

PASS GATE
= what must be true before the step may be declared complete.

STATUS
= APPROVED / ACTIVE, UNVALIDATED, QUESTIONABLE, CORRECTION_REQUIRED, etc.
```

If a future step has never been methodologically validated, it must be marked `UNVALIDATED`; ChatGPT must research it before execution rather than infer a procedure from neighbouring steps.

## Mechanical repetition is prohibited

The purpose of the lessons ledger is **not** to make ChatGPT replay old actions blindly.

Before applying a recorded rule, ChatGPT must reconstruct:

```text
WHAT FAILED?
WHY DID IT FAIL?
WHAT FALSE ASSUMPTION OR PROCESS GAP CAUSED IT?
HOW DOES THE RECORDED CONTROL BLOCK THAT CAUSE?
DOES THE SAME CAUSE ACTUALLY APPLY TO THE CURRENT JOB/STEP?
HAS CURRENT EXTERNAL RESEARCH CHANGED THE METHOD?
```

If ChatGPT cannot explain this causal chain, the step is not ready for authorization.

Canonical rule:

```text
RULE_RECALL_WITHOUT_CAUSAL_UNDERSTANDING != METHOD_VALIDATION
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
```

This layer contains:

```text
client/site facts;
provider request identities;
rows and counts;
concrete query/page decisions;
job-specific deviations;
step execution evidence;
reconciliation and acceptance truth.
```

Job-specific evidence may reveal a reusable lesson, but it does not automatically mutate Layer A or Layer B. Permanent rule changes require explicit owner instruction.

---

# 4. Required read order before every major step

Canonical order:

```text
A. READ RULES_ARCHITECTURE.md
B. READ UNIVERSAL PROCESS RULES
C. READ CURRENT STEP SECTION IN STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md
D. READ CURRENT JOB MANIFEST / FLOW
E. READ PREVIOUS STEP EVIDENCE AND CURRENT STEP PRE-STEP ARTIFACTS
F. RECONSTRUCT WHY THE CURRENT STEP EXISTS
G. RECONSTRUCT RELEVANT PREVIOUS ERRORS + ROOT CAUSES
H. SEARCH CURRENT EXTERNAL MATERIALS FOR THIS STEP
I. CHALLENGE THE PLANNED METHOD
J. EXPLAIN METHOD + SOURCES + NON-REPEAT CONTROLS TO OWNER
K. WAIT FOR OWNER AUTHORIZATION
L. EXECUTE
M. VERIFY
N. REPORT / UPDATE ROADMAP / STOP
```

If the step-specific ledger section is missing or does not cover a material operation:

```text
STEP_METHOD_STATUS = UNVALIDATED
METHOD_RESEARCH_REQUIRED = true
EXECUTION = BLOCKED until pre-step review is complete
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

---

# 6. How a new error must be recorded

When a material error is discovered, first record it in the current job with:

```text
WHAT WAS DONE WRONG
OBSERVED CONSEQUENCE
ROOT CAUSE
WHY THE OLD METHOD WAS INVALID OR INSUFFICIENT
HOW IT WAS CORRECTED
WHAT QA EXPOSED THE PROBLEM
CURRENT LIMITS
```

If the lesson is reusable across jobs, ChatGPT must propose promotion into `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md`.

Only after explicit owner approval may the universal/per-step permanent ledger be changed.

A permanent lesson must preserve the causal explanation, not only the final instruction.

---

# 7. Minimum owner-facing explanation before authorization

The universal gates define the full required report. In methodology terms, every step explanation must make these questions answerable:

```text
What are we trying to achieve?
Why is this step necessary?
What did we previously get wrong in this step, if anything?
Why did that error happen?
What current sources did we check?
What do those sources actually support?
What is still a project-specific choice?
How exactly will we perform the step now?
Why should this procedure solve the goal?
What checks will catch a repeat of the known errors?
What output must exist before we call the step complete?
```

At the end of the detailed explanation, apply the mandatory non-specialist summary from `STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md`.

---

# 8. Structural summary

```text
UNIVERSAL PROCESS RULES
    ↓ tell us how every step must be approached
STEP-SPECIFIC METHOD + LESSONS LEDGER
    ↓ tells us how this exact kind of step works and what has failed before
CURRENT JOB MANIFEST / FLOW / EVIDENCE
    ↓ tells us what happened in this exact client job
PRE-STEP CURRENT INTERNET RESEARCH
    ↓ checks that the recorded method is still defensible and relevant
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
KW001_PER_STEP_METHOD_LAYER_REQUIRED = true
KW001_JOB_SPECIFIC_EVIDENCE_LAYER_REQUIRED = true
KW001_CURRENT_EXTERNAL_RESEARCH_EVERY_MAJOR_STEP = true
KW001_DIRECT_SOURCES_EVERY_MAJOR_STEP = true
KW001_MECHANICAL_RULE_REPLAY_PROHIBITED = true
KW001_CAUSAL_ERROR_UNDERSTANDING_REQUIRED = true
KW001_UNVALIDATED_STEP_BLOCKS_EXECUTION = true
```
