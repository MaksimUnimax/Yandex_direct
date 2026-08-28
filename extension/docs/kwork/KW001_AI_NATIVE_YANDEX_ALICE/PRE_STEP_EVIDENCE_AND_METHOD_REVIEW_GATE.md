# KW-001 — PRE-STEP EVIDENCE AND METHOD REVIEW GATE

Date: 2026-08-28  
Status: **ACTIVE / UNIVERSAL / REQUIRED BEFORE EVERY MAJOR STEP**

This document is the canonical KW-001 gate that must run before every new major analytical or provider step.

## Required sequence

```text
READ OWNER-LOCKED UNIVERSAL RULES
→ READ CURRENT JOB WORKSPACE / JOB FLOW
→ READ PREVIOUS STEP EVIDENCE
→ EXPLAIN NEXT STEP
→ IDENTIFY METHOD
→ TRACE METHOD ORIGIN
→ SEARCH CURRENT EXTERNAL MATERIALS
→ CHALLENGE OWN PRIOR WORK
→ CLASSIFY SUPPORT / DEFECT
→ SHOW OWNER SOURCES + RISKS
→ WAIT FOR EXPLICIT OWNER AUTHORIZATION
→ EXECUTE ONE STEP INSIDE CURRENT JOB
→ STOP + REPORT
```

Execution before this gate is a process failure.

---

## 0. Two-layer check before method review

Read and obey:

```text
JOB_WORKSPACE_LIFECYCLE.md
```

Layer A = permanent universal Kwork rules.  
Layer B = disposable current-job workspace.

Universal rules are **owner-locked**:

```text
ChatGPT must not edit, add, remove or promote universal rules during a concrete job
unless the owner explicitly instructs it to change the universal methodology.
```

A discovered possible universal defect is reported to the owner; it is not silently repaired in Layer A.

Before each major step read at minimum:

```text
DIALOGUE_AND_ANALYTICAL_DISCIPLINE.md
WORKING_RUNBOOK_FOR_CHATGPT.md
PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md
JOB_WORKSPACE_LIFECYCLE.md
STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md  # permanent owner-approved history only
current job JOB_MANIFEST.md
current job JOB_FLOW.md if present
relevant current-job step records
previous step acceptance/evidence
```

If a concrete client's facts are being written into permanent universal files, classify this as `CORRECTION_REQUIRED` for the current job organization.

---

## 1. Explain before doing

Before execution, ChatGPT must tell the owner:

```text
what the step is;
what input evidence it uses;
what exact operations will be performed;
what output/gate is expected;
why this step exists;
what later decisions depend on it;
what will explicitly NOT be decided yet.
```

Do not hide methodology behind generic phrases such as `cleanup`, `cluster`, `validate`, `analyze` or `expand`.

---

## 2. Trace where the method came from

Every material rule used by the step must be classified as one of:

```text
OFFICIAL
= official Yandex/provider/search-engine documentation or another primary authority

INDUSTRY_PRACTICE
= established external practitioner/tool methodology, preferably corroborated by more than one credible source when no official standard exists

PROJECT_TEST_VALIDATED
= supported by controlled project evidence or measured provider behavior

ANALYST_HEURISTIC
= a reasoned ChatGPT/project choice for which no authoritative external standard has yet been established
```

Never silently promote `ANALYST_HEURISTIC` to `INDUSTRY_PRACTICE` or `OFFICIAL`.

A project-authored runbook is workflow authority, not independent evidence of its own correctness.

---

## 3. Search current materials before every major step

Before execution, ChatGPT must search current external materials relevant to that step.

Source priority:

```text
1. official / primary provider documentation;
2. official search-engine guidance relevant to the task;
3. credible external industry methodology;
4. controlled project/provider evidence;
5. analyst heuristic, explicitly labelled.
```

Where no official standard exists:

```text
use multiple credible external methodologies when practical;
identify disagreement instead of forcing false consensus;
state explicitly that the final choice is project-specific if that is the truth.
```

Freshness matters when provider behavior, product interfaces or search guidance can change.

---

## 4. Mandatory adversarial self-audit

The pre-step review must actively try to falsify the current workflow, not merely find supporting citations.

Questions to ask:

```text
Did the previous step assume something not proved?
Did we remove or retain terms for a reason that external methodology would reject?
Did we confuse demand volume with relevance?
Did we confuse relevance with page ownership?
Did we use Wordstat associations as if they were accepted keywords?
Did we let site structure predetermine search demand?
Did we let raw search demand override real business scope?
Did we use one arbitrary numerical threshold as if it were universal?
Did we make a page/cluster decision before SERP evidence required by the workflow?
Did we cite our own runbook as proof instead of tracing the rule to evidence?
Is any provider/search behavior assumed from memory rather than checked?
Did we accidentally place case-specific evidence in permanent methodology files?
Does the current job execution conflict with an owner-locked universal rule?
Does a universal rule appear questionable based on new evidence?
```

If the last question is YES, report the issue to the owner. **Do not modify the universal rule unless the owner explicitly orders the change.**

---

## 5. Required review verdict

Before owner authorization, classify the proposed step/method:

```text
SUPPORTED
= method is well supported by current external and/or measured evidence

PROJECT_SPECIFIC_BUT_REASONED
= no universal standard exists, but the project choice is explicit, bounded and defensible

QUESTIONABLE
= meaningful uncertainty remains; owner must see it before deciding whether to proceed

CORRECTION_REQUIRED
= current job artifact/execution contains a material defect that must be corrected before execution
```

A possible defect in an owner-locked universal rule must be surfaced separately as:

```text
UNIVERSAL_RULE_REVIEW_REQUESTED
```

This does not authorize ChatGPT to edit Layer A.

---

## 6. Mandatory owner-facing pre-step report

Before executing a major step, show:

```text
NEXT STEP
WHAT I WILL DO
WHY
INPUT EVIDENCE
METHOD ORIGIN
EXTERNAL SOURCES
SELF-AUDIT FINDINGS
WHAT IS SUPPORTED
WHAT IS PROJECT-SPECIFIC / HEURISTIC
RISKS / UNCERTAINTIES
POSSIBLE UNIVERSAL-RULE ISSUE, IF ANY
WHAT I WILL NOT DO YET
PROPOSED PASS GATE
```

Then stop and wait for explicit owner authorization.

---

## 7. Execution after authorization

After authorization:

```text
execute only the authorized step;
do not silently broaden scope;
preserve provider/source provenance;
keep all case-specific artifacts inside the current job workspace;
record current-job deviations/failures in current-job workflow/evidence files;
complete the step gate;
DO NOT update universal rules unless the owner explicitly ordered such an update;
STOP;
report result, sources, costs/provider calls, commits and remaining uncertainty;
wait for the next explicit owner continuation.
```

This preserves:

```text
PRE-STEP REVIEW
→ OWNER AUTHORIZATION
→ ONE JOB STEP
→ COMPLETE JOB GATE
→ STOP
→ REPORT
→ WAIT
```

---

## 8. Provider sub-items are not separate major steps

The complete research gate is required before a new batch/method/evidence stage, not before every individual item of an already researched, frozen and owner-authorized durable batch.

Any material change to the manifest, method, region, evidence semantics or retry policy requires a fresh review/authorization.

---

## 9. Job close

Completing the last analytical step does not automatically delete the workspace.

Apply `JOB_WORKSPACE_LIFECYCLE.md`:

```text
job work complete
→ final deliverable/handoff complete
→ revisions/rework closed
→ no provider/operator action pending
→ mark safe_to_delete = true
→ delete the entire current-job workspace
```

There is **no mandatory automatic extraction of lessons into universal docs** at close.

If the owner wants a universal method change, the owner explicitly orders it when desired.

---

## 10. Relationship to other KW-001 rules

This gate complements:

```text
DIALOGUE_AND_ANALYTICAL_DISCIPLINE.md
WORKING_RUNBOOK_FOR_CHATGPT.md
STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md
JOB_WORKSPACE_LIFECYCLE.md
KWORK_RUNBOOK_STANDARD_2026-08-28.md
```

Markers:

```text
KW001_PRE_STEP_REVIEW_GATE_REQUIRED = true
KW001_PRE_STEP_EXTERNAL_RESEARCH_REQUIRED = true
KW001_PRE_STEP_ADVERSARIAL_SELF_AUDIT_REQUIRED = true
KW001_PRE_STEP_OWNER_APPROVAL_REQUIRED = true
KW001_ONE_STEP_STOP_REPORT_WAIT_REQUIRED = true
KW001_PRE_STEP_JOB_WORKSPACE_CHECK_REQUIRED = true
KW001_UNIVERSAL_RULES_OWNER_LOCKED_DURING_JOB = true
KW001_NO_AUTOMATIC_UNIVERSAL_RULE_UPDATE = true
KW001_JOB_CLOSE_DELETE_ONLY_NO_MANDATORY_EXTRACTION = true
```
