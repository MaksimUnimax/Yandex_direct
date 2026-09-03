# KW-001 — DIALOGUE AND ANALYTICAL DISCIPLINE

Updated: 2026-09-03  
Status: **ACTIVE / UNIVERSAL KW-001 OPERATING RULE**

This rule applies during productization, test execution, methodology review and client-order work. Concrete rehearsal/client identities and current-job facts belong in Level2.

---

## Rule 1 — do not agree automatically with the owner

When the owner questions, rejects or challenges an analytical decision, ChatGPT must not automatically agree, reverse the decision or rewrite the workflow merely because the objection was strongly stated.

Required sequence:

```text
1. restate the disputed analytical point;
2. explain why the current decision/rule exists;
3. distinguish assumption from measured evidence;
4. check the objection against current rules, evidence and relevant external methodology;
5. classify the objection as:
   A. real defect,
   B. explanation/communication defect,
   C. unresolved uncertainty,
   D. no defect in current method;
6. change the workflow only when evidence or sound reasoning justifies it.
```

### Failure history and root cause

A prior controlled execution showed that an owner objection to a diagnostic acquisition seed was initially treated as proof that the seed plan itself was wrong, even though the seed's role was to probe a demand family rather than become a final accepted keyword.

Root cause:

```text
OWNER OBJECTION / STRONG WORDING
WAS ALLOWED TO SUBSTITUTE FOR
ANALYTICAL RE-VALIDATION
```

The actual issue in that incident was primarily communication: the distinction between a probe and a final retained item had not been explained clearly enough.

### Control

```text
OWNER OBJECTION
→ DO NOT REFLEXIVELY AGREE
→ EXPLAIN CURRENT LOGIC
→ IDENTIFY EVIDENCE AND UNCERTAINTY
→ DETERMINE WHETHER THE METHOD CHANGES
→ IF IT CHANGES, STATE THE EVIDENCE / CAUSE
```

Strong language, confidence or repetition from the owner does not increase evidentiary weight. Explicit owner decisions about commercial scope, authorization, price, exclusions or actual client priorities remain binding inputs.

Marker:

```text
KW001_DIALOGUE_ANALYTICAL_DISCIPLINE_ACTIVE = true
```

---

## Rule 2 — state the required Yandex Marketing Bridge mode before an operator command

Before asking the owner/operator to send any Bridge command, ChatGPT must explicitly state the extension state required for that command.

At minimum:

```text
ACTIVE SERVICE = wordstat | search | webmaster | metrika | direct
EXECUTION MODE = Manual | Autorun | other accepted mode
ADDITIONAL STATE = paused/bound/owner-tab/etc. only when relevant
```

Do not rely on command prefix, previous turn or operator memory to imply state.

### Failure history and root cause

A controlled execution sent a command while a different service remained active. Bridge correctly rejected it before provider execution, but the operator step had to be repeated.

Root cause:

```text
REQUIRED OPERATOR STATE
WAS LEFT IMPLICIT IN DIALOGUE CONTEXT
```

### Control

Immediately before every operator command, state the required service/mode and any material toggle explicitly. If a field requires no change, say so when omission could create ambiguity.

Marker:

```text
KW001_EXPLICIT_YMB_MODE_INSTRUCTION_ACTIVE = true
```

---

## Rule 3 — mandatory pre-step evidence and methodology review

Before every new major analytical/project execution step, ChatGPT must stop before execution and perform a visible pre-step review.

Required order:

```text
1. identify exact next step and intended output;
2. explain plainly what will and will not be done;
3. reread prior accepted evidence/limitations relevant to the next step;
4. identify proposed methodology/rules;
5. classify material method origin:
   OFFICIAL
   INDUSTRY_PRACTICE
   PROJECT_TEST_VALIDATED
   ANALYST_HEURISTIC
6. research current external method sources before execution where required;
7. prefer official/primary sources and corroborate where no official standard exists;
8. compare planned method with sources and project evidence;
9. deliberately challenge the assistant's own previous work;
10. classify review result:
    SUPPORTED
    PROJECT_SPECIFIC_BUT_REASONED
    QUESTIONABLE
    CORRECTION_REQUIRED
11. label heuristics honestly;
12. if correction is required, repair/re-freeze before execution;
13. show owner method, sources, uncertainty and corrections;
14. give the mandatory plain-language why/how/result summary;
15. obtain explicit owner authorization when the major-step gate requires it;
16. only then execute.
```

### Failure history and root cause

A prior controlled execution used an internally coherent cleanup method, but an owner-requested retrospective audit exposed that methodology validation was occurring only when challenged. Project-authored rules were too close to becoming their own authority.

Root cause:

```text
PROJECT METHOD DOCUMENT
WAS ALLOWED TO FUNCTION AS
INDEPENDENT PROOF OF ITS OWN METHOD
```

### Control

A project runbook defines current process but does not independently validate it. Material method claims must trace to official/provider documentation, credible external industry practice, measured project evidence, controlled project tests, or explicitly labelled analyst reasoning.

Canonical sequence:

```text
EXPLAIN
→ RESEARCH / CHECK SOURCES
→ SELF-AUDIT
→ OWNER AUTHORIZATION WHEN REQUIRED
→ EXECUTE
```

This applies to each major analytical/project step or material method/evidence-type change; it does not require rerunning the entire external methodology review before every item inside an already researched/authorized acquisition batch.

Markers:

```text
KW001_PRE_STEP_EVIDENCE_METHOD_REVIEW_ACTIVE = true
KW001_OWNER_AUTHORIZATION_BEFORE_EACH_MAJOR_STEP = true
```

---

## Rule 4 — provider work is complete only when the complete result is preserved and verified

A provider step exists to obtain usable project evidence, not merely to execute an API call.

A provider request/item is complete for the project only when:

```text
1. provider outcome is known and usable;
2. the complete result required by the step is preserved in the job workspace;
3. preservation is verified against response/count/field truth;
4. persisted result is readable and usable for the next stage.
```

The following alone never prove project completion:

```text
HTTP 200
request_executed = true
item_status = SUCCEEDED
succeeded = N
terminal = N
cost recorded
summary/checkpoint containing only examples
```

### Failure history and root cause

A controlled acquisition execution produced technically successful provider calls but preserved only summaries/representative examples for some larger result sets. Later analysis therefore lacked the complete row universe it needed.

Root cause:

```text
TECHNICAL REQUEST SUCCESS
WAS TREATED AS
PROJECT EVIDENCE COMPLETION
```

### Control

If complete preservation/verification fails:

```text
CURRENT ITEM = INCOMPLETE FOR PROJECT
CURRENT MAJOR STEP = NOT COMPLETE
NEXT PROVIDER ITEM = BLOCKED
NEXT ANALYTICAL STEP = BLOCKED
```

Recovery first restores the complete verified current result. Only then may acquisition continue.

Before provider item N+1:

```text
provider outcome known = true
complete result preserved = true
preserved row/count truth verified = true
result usable for next stage = true
```

If any is false, stop.

Markers:

```text
KW001_PROVIDER_RESULT_PRESERVATION_GATE_ACTIVE = true
KW001_TECHNICAL_SUCCESS_IS_NOT_PROJECT_COMPLETION = true
KW001_NEXT_PROVIDER_ITEM_BLOCKED_UNTIL_RESULT_VERIFIED = true
```

---

## Permanent universality boundary

This file stores failure classes, root causes and controls. Concrete case names, domains, queries, provider receipts/counts and current job status remain Level2 evidence under `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.
