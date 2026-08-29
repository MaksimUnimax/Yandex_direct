# KW-001 — PRE-STEP EVIDENCE AND METHOD REVIEW GATE

Date: 2026-08-29  
Status: **ACTIVE / UNIVERSAL / REQUIRED BEFORE EVERY MAJOR STEP**

This document is the canonical KW-001 gate that must run before every new major analytical or provider step.

Mandatory companion rule:

```text
STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md
```

## Required sequence

```text
READ OWNER-LOCKED UNIVERSAL RULES
→ READ CURRENT JOB WORKSPACE / JOB FLOW
→ READ PREVIOUS STEP EVIDENCE
→ RE-READ STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md
→ STATE WHOLE KWORK GOAL IN PLAIN LANGUAGE
→ SHOW COMPLETED WORK LIST FOR WHOLE KWORK/JOB
→ SHOW REMAINING WORK LIST FOR WHOLE KWORK/JOB
→ STATE CURRENT STEP GOAL
→ STATE WHAT THIS STEP SOLVES
→ STATE EXACT REQUIRED OUTPUT
→ STATE RELEVANT PRIOR ERRORS + HOW THEY ARE BLOCKED THIS TIME
→ ONLY THEN IDENTIFY / RESEARCH METHOD
→ TRACE METHOD ORIGIN
→ SEARCH CURRENT EXTERNAL MATERIALS
→ CHALLENGE OWN PRIOR WORK
→ CLASSIFY SUPPORT / DEFECT
→ IF YMB IS USED, EMBED THE YMB RESULT-COMPLETION GATE INSIDE THIS EXACT STEP
→ SHOW OWNER SOURCES + PRACTICAL PLAN + RISKS
→ WAIT FOR EXPLICIT OWNER AUTHORIZATION
→ EXECUTE ONE STEP INSIDE CURRENT JOB
→ VERIFY EACH YMB RESULT IS COMPLETE + SAVED BEFORE ANY NEXT YMB ACTION
→ REPORT AGAINST PREDECLARED STEP GOAL WITH NUMBERS
→ UPDATE COMPLETED WORK LIST
→ UPDATE REMAINING WORK LIST
→ STOP + REPORT
```

Execution or method research before the goal/status/error-review block is a process failure.

---

## 0. Two-layer check before method review

Read and obey:

```text
JOB_WORKSPACE_LIFECYCLE.md
STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md
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
STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md
WORKING_RUNBOOK_FOR_CHATGPT.md
PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md
JOB_WORKSPACE_LIFECYCLE.md
STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md
current job JOB_MANIFEST.md
current job JOB_FLOW.md if present
relevant current-job step records
previous step acceptance/evidence
```

`STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` is not merely part of a background reading list. It must be explicitly re-opened and re-read before **every** new step as part of the same goal-first block that re-establishes the whole Kwork objective and the current step objective.

The owner-facing pre-step message must state which previously recorded errors/corrections are relevant to the current step, what went wrong previously, and what concrete control will prevent recurrence in this step.

If no recorded error is relevant, state that explicitly rather than silently skipping the check.

Required owner-facing wording/concept:

```text
RELEVANT PRIOR ERRORS / CORRECTIONS
= errors or corrections from STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md that apply to this step.

WHAT FAILED BEFORE
= the concrete process or reasoning failure.

NON-REPEAT CONTROL FOR THIS STEP
= the exact check/gate that prevents the same failure now.

NON-REPEAT COMMITMENT
= these recorded errors must not be repeated in the current step; the relevant control will be verified before transition.
```

If this error/correction reread and owner-facing statement are missing:

```text
METHOD_RESEARCH = BLOCKED
STEP_AUTHORIZATION = BLOCKED
EXECUTION = BLOCKED
```

If a concrete client's facts are being written into permanent universal files, classify this as `CORRECTION_REQUIRED` for the current job organization.

---

## 1. Goal, job-status AND prior-error review MUST happen before method research

Before searching external methodology or deciding how to execute a step, ChatGPT must first tell the owner in plain language:

```text
WHOLE KWORK GOAL
= what final client result KW-001 is intended to deliver.

COMPLETED WORK
= full list of work/results across the current Kwork/job that are genuinely complete and verified.

REMAINING WORK
= full ordered list of everything still required before final completion.

CURRENT STEP GOAL
= the single concrete result this step must achieve.

WHAT THIS STEP SOLVES
= the missing evidence, uncertainty, decision or production requirement it closes.

REQUIRED OUTPUT
= exactly what must exist at the end of the step for it to count as complete.

RELEVANT PRIOR ERRORS / CORRECTIONS
= applicable lessons/errors from STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md, freshly re-read for this step.

WHAT FAILED BEFORE
= what was previously done wrong.

NON-REPEAT CONTROL FOR THIS STEP
= what exact check/gate will prevent repetition.
```

Rules:

```text
No item may appear in COMPLETED WORK merely because an API call succeeded, a file exists, or a summary was written.
If later evidence shows an earlier item is incomplete, move it back out of COMPLETED WORK and into REMAINING WORK / CORRECTION REQUIRED.
The lists must be updated after every step.
Past errors/corrections must be re-read from the permanent ledger, not reconstructed from memory.
Relevant past errors must be stated in chat before method research begins.
The current step may not transition until its stated non-repeat controls have been checked.
```

If this block is missing:

```text
METHOD_RESEARCH = BLOCKED
STEP_AUTHORIZATION = BLOCKED
EXECUTION = BLOCKED
```

Only after this block may ChatGPT research the method for the step.

---

## 2. Explain the practical step before doing it

After the goal/status/error-review block and before execution, ChatGPT must tell the owner:

```text
what input evidence the step uses;
what exact operations will be performed;
why this method is appropriate;
what sources support it;
what output/gate is expected;
what later decisions depend on it;
what will explicitly NOT be decided yet.
```

Do not hide methodology behind generic phrases such as `cleanup`, `cluster`, `validate`, `analyze`, `SERP` or `expand` without a plain-language explanation of what it means and why it matters to the client result.

---

## 3. Trace where the method came from

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

## 4. Search current materials before every major step

Only after Sections 1–2 are complete may ChatGPT search current external materials relevant to that step.

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

## 5. Mandatory adversarial self-audit

The pre-step review must actively try to falsify the current workflow, not merely find supporting citations.

Questions to ask:

```text
Does this step actually move the Kwork toward its final client result?
Does the declared required output genuinely satisfy the current step goal?
Is anything currently listed as completed actually incomplete?
Did I freshly re-read STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md for this exact step?
Which recorded errors/corrections apply here?
What exact control prevents each relevant recorded failure from recurring?
Did the previous step assume something not proved?
Did we remove or retain terms for a reason that external methodology would reject?
Did we confuse demand volume with relevance?
Did we confuse relevance with page ownership?
Did we use Wordstat associations as if they were accepted keywords?
Did we let site structure predetermine search demand?
Did we let raw search demand override real business scope?
Did we use one arbitrary numerical threshold as if it were universal?
Did we make a page/cluster decision before required search evidence?
Did we cite our own runbook as proof instead of tracing the rule to evidence?
Is any provider/search behavior assumed from memory rather than checked?
Did we accidentally place case-specific evidence in permanent methodology files?
Does the current job execution conflict with an owner-locked universal rule?
Does a universal rule appear questionable based on new evidence?
If the step uses YMB: what exact usable result must be collected and saved, and how will I prove it is complete before the next YMB action?
```

If a universal-rule question is YES, report the issue to the owner. **Do not modify the universal rule unless the owner explicitly orders the change.**

---

## 6. Required review verdict

Before owner authorization, classify the proposed step/method:

```text
SUPPORTED
PROJECT_SPECIFIC_BUT_REASONED
QUESTIONABLE
CORRECTION_REQUIRED
```

A possible defect in an owner-locked universal rule must be surfaced separately as:

```text
UNIVERSAL_RULE_REVIEW_REQUESTED
```

This does not authorize ChatGPT to edit Layer A.

---

## 7. Mandatory owner-facing pre-step report

Before executing a major step, show, in plain language and in this order:

```text
WHOLE KWORK GOAL
COMPLETED WORK
REMAINING WORK
CURRENT STEP GOAL
WHAT THIS STEP SOLVES
REQUIRED OUTPUT
RELEVANT PRIOR ERRORS / CORRECTIONS
WHAT FAILED BEFORE
NON-REPEAT CONTROL FOR THIS STEP
INPUT EVIDENCE
METHOD ORIGIN
EXTERNAL SOURCES
HOW WE WILL DO IT
SELF-AUDIT FINDINGS
RISKS / UNCERTAINTIES
WHAT WE WILL NOT DO YET
PROPOSED PASS GATE
```

The prior-error section must be based on a fresh read of `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md`, not on memory or the previous chat turn.

If the step contains **any YMB interaction**, the pre-step report and the concrete job-step artifact must also contain the mandatory YMB block defined in Section 9 below.

Then stop and wait for explicit owner authorization.

---

## 8. Execution after authorization

After authorization:

```text
execute only the authorized step;
do not silently broaden scope;
preserve provider/source evidence;
keep all case-specific artifacts inside the current job workspace;
record current-job deviations/failures in current-job workflow/evidence files;
complete the step gate;
DO NOT update universal rules unless the owner explicitly ordered such an update;
STOP;
report result against the predeclared step goal;
report quantitative accounting;
report whether every stated NON-REPEAT CONTROL passed;
update COMPLETED WORK list;
update REMAINING WORK list;
state NEXT_STEP_ALLOWED = true | false;
wait for the next explicit owner continuation.
```

This preserves:

```text
GOAL + STATUS + PRIOR-ERROR REREAD
→ METHOD RESEARCH
→ OWNER AUTHORIZATION
→ ONE JOB STEP
→ VERIFY REQUIRED OUTPUT + NON-REPEAT CONTROLS
→ QUANTITATIVE REPORT
→ UPDATE COMPLETED / REMAINING WORK
→ STOP
→ WAIT
```

---

## 9. Mandatory block INSIDE EVERY step that uses YMB

This is not an optional cross-reference and not a rule that may live only in a universal document.

**Every concrete job step that contains one or more YMB interactions must include this block inside that step's own pre-step/manifest/execution gate.**

Before the first YMB command in that step, the concrete step must state:

```text
YMB STEP OBJECTIVE
= what usable project result this step must actually collect.

YMB REQUIRED MODE
= active service + execution mode + manual/autorun state where relevant.

YMB REQUIRED SAVED RESULT
= exactly what complete data/payload/rows/evidence must be stored in the job workspace after each interaction.

YMB COMPLETENESS CHECK
= how completeness will be verified: returned row count, item count, identifiers, pagination completion, payload fields, or other provider truth appropriate to the command.

YMB STOP CONDITION
= if the complete required result is not saved and verified, STOP immediately; do not issue the next YMB command and do not advance the step.
```

After **every individual YMB interaction** in the step, before any next YMB interaction, ChatGPT must verify:

```text
1. Did the interaction reach the provider or fail before provider execution?
2. Is the provider outcome known, or is it OUTCOME_UNKNOWN?
3. Did we obtain the actual result needed for the project objective, not merely an OK/status response?
4. Was the complete required result saved in the current job workspace?
5. Was saved completeness verified against the response/provider truth?
6. Is the saved result readable and usable for the next action?
```

The next YMB interaction is allowed only when all applicable answers required for success are confirmed.

The following **never** substitute for this check:

```text
HTTP 200
request_executed = true
status = OK
item_status = SUCCEEDED
batch succeeded count
cost recorded
representative examples
summary text
```

If the objective was to collect 200 returned phrases, saving 10 examples means the interaction is **NOT COMPLETE** and the next YMB interaction is **BLOCKED**.

If the objective was to collect all pages of a paginated Search result, saving page 1 alone means the interaction/step is **NOT COMPLETE** unless the concrete step explicitly and correctly defined page 1 as the whole bounded objective.

If the objective was only a status check and no provider payload is expected, the concrete step must state that explicitly; then completeness means the full required status truth was preserved and verified.

### Required concrete-step markers

Every YMB-enabled job step must include:

```text
YMB_INTERACTION_GATE_EMBEDDED = true
YMB_PROJECT_RESULT_DEFINED = true
YMB_REQUIRED_STORAGE_DEFINED = true
YMB_COMPLETENESS_CHECK_DEFINED = true
YMB_STOP_ON_INCOMPLETE_RESULT = true
```

If any marker is missing:

```text
STEP_AUTHORIZATION = BLOCKED
YMB_EXECUTION = BLOCKED
```

This rule applies to Wordstat, Search, GenSearch, Webmaster, Metrika, Direct and every future accepted YMB service.

---

## 10. Provider sub-items are not separate major steps

The complete external research gate is required before a new batch/method/evidence stage, not before every individual item of an already researched, frozen and owner-authorized durable batch.

However, **Section 9 still applies after every individual YMB interaction inside that batch.** Not repeating external research does not waive result preservation/completeness verification.

Any material change to the manifest, method, region, evidence semantics or retry policy requires a fresh review/authorization.

---

## 11. Mandatory end-of-step quantitative report

Every step ends with a report tied to the step goal declared before research/execution.

At minimum report all applicable numbers:

```text
how many items/queries/pages/rows were planned
how many were actually processed
how many provider calls were attempted
how many provider calls actually executed
how many results/rows were returned
how many were saved
how many were verified
how many were deduplicated
how many were excluded
how many were retained
how many remain for review
how many were analyzed
how many artifacts were produced
errors / OUTCOME_UNKNOWN
provider cost
```

Then explicitly show:

```text
NON-REPEAT CONTROLS: PASS | FAIL per applicable prior error/correction
UPDATED COMPLETED WORK
UPDATED REMAINING WORK
NEXT_STEP_ALLOWED = true | false
```

If the required counts cannot be reconciled against the declared output, or any required non-repeat control fails, the step is `INCOMPLETE` and the next step is blocked.

---

## 12. Job close

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

## 13. Relationship to other KW-001 rules

This gate complements:

```text
STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md
DIALOGUE_AND_ANALYTICAL_DISCIPLINE.md
WORKING_RUNBOOK_FOR_CHATGPT.md
STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md
JOB_WORKSPACE_LIFECYCLE.md
KWORK_RUNBOOK_STANDARD_2026-08-28.md
```

Markers:

```text
KW001_PRE_STEP_REVIEW_GATE_REQUIRED = true
KW001_GOAL_STATUS_BLOCK_BEFORE_METHOD_RESEARCH = true
KW001_PRIOR_ERROR_LEDGER_REREAD_REQUIRED_EVERY_STEP = true
KW001_RELEVANT_PRIOR_ERRORS_MUST_BE_STATED_IN_CHAT = true
KW001_NON_REPEAT_CONTROL_REQUIRED_EVERY_STEP = true
KW001_COMPLETED_WORK_LIST_REQUIRED_EVERY_STEP = true
KW001_REMAINING_WORK_LIST_REQUIRED_EVERY_STEP = true
KW001_COMPLETED_REMAINING_LISTS_UPDATED_AFTER_EVERY_STEP = true
KW001_STEP_GOAL_REQUIRED_OUTPUT_BEFORE_RESEARCH = true
KW001_PRE_STEP_EXTERNAL_RESEARCH_REQUIRED = true
KW001_PRE_STEP_ADVERSARIAL_SELF_AUDIT_REQUIRED = true
KW001_PRE_STEP_OWNER_APPROVAL_REQUIRED = true
KW001_ONE_STEP_STOP_REPORT_WAIT_REQUIRED = true
KW001_QUANTITATIVE_STEP_REPORT_REQUIRED = true
KW001_PRE_STEP_JOB_WORKSPACE_CHECK_REQUIRED = true
KW001_UNIVERSAL_RULES_OWNER_LOCKED_DURING_JOB = true
KW001_NO_AUTOMATIC_UNIVERSAL_RULE_UPDATE = true
KW001_JOB_CLOSE_DELETE_ONLY_NO_MANDATORY_EXTRACTION = true
KW001_EVERY_YMB_STEP_MUST_EMBED_INTERACTION_GATE = true
KW001_EVERY_YMB_INTERACTION_MUST_VERIFY_PROJECT_RESULT = true
KW001_NEXT_YMB_INTERACTION_BLOCKED_UNTIL_RESULT_SAVED_AND_VERIFIED = true
```
