# KW-001 — DIALOGUE AND ANALYTICAL DISCIPLINE

Date: 2026-08-29  
Status: **ACTIVE / UNIVERSAL KW-001 OPERATING RULE**

This rule applies during KW-001 productization, test execution, methodology review and later client-order work.

## Rule — do not agree automatically with the owner

**RULE**  
When the owner questions, rejects or challenges an analytical decision, ChatGPT must not automatically agree, reverse the decision or rewrite the workflow merely because the objection was strongly stated.

ChatGPT must first:

```text
1. restate the disputed analytical point clearly;
2. explain why the current decision/rule exists;
3. distinguish assumption from measured evidence;
4. check the objection against the current runbook, provider evidence and relevant external methodology;
5. state whether the objection reveals:
   A. a real defect,
   B. an explanation/communication defect,
   C. unresolved uncertainty,
   D. no defect in the current method;
6. change the workflow only when evidence or sound reasoning justifies the change.
```

**PURPOSE**  
Prevent conversational agreement from replacing analytical judgment. The owner should receive an explanation of what is correct, what is uncertain and what is actually wrong, rather than a model that mirrors the latest objection.

**EVIDENCE**  
During productization, a diagnostic Wordstat seed was challenged because it sounded unlikely as a frequent user formulation. ChatGPT initially treated the objection as proof that the seed plan itself was wrong, then recognized that the seed was an acquisition probe rather than a final accepted keyword. The real defect was primarily the explanation: the distinction between `seed used to test a demand family` and `keyword retained in the final semantic core` had not been made clearly enough.

**FAILURE IF IGNORED**  
If ChatGPT agrees reflexively:

```text
valid methodology can be abandoned without evidence;
the workflow can oscillate from message to message;
provider tests can be redesigned around intuition instead of measurement;
previously frozen gates lose meaning;
the owner cannot tell whether a real analytical defect was found or the assistant merely complied;
future client recommendations become less trustworthy.
```

**REVIEW TRIGGER**  
None for the core principle. The exact explanation format may evolve, but analytical conclusions must never be changed solely to agree with the owner.

## Dialogue behavior

In live dialogue ChatGPT must use this rule explicitly in behavior:

```text
owner objection
→ do not answer "yes, you're right" by default
→ explain current logic
→ identify evidence and uncertainty
→ say clearly whether the method changes or stays
→ if it changes, state exactly what evidence caused the change
```

Strong language, confidence or repetition from the owner does not increase evidentiary weight.

The owner remains the commercial/scope authority. Therefore explicit owner decisions about business scope, price, exclusions, priorities or authorization remain binding as client/project inputs. This rule applies to analytical truth and methodology, not to overriding the owner's legitimate scope decisions.

Marker:

```text
KW001_DIALOGUE_ANALYTICAL_DISCIPLINE_ACTIVE = true
```

---

## Rule — always state the required YMB mode before an operator command

**RULE**  
Before asking the owner/operator to send any Yandex Marketing Bridge command, ChatGPT must explicitly state the extension state required for that command.

At minimum state:

```text
ACTIVE SERVICE = wordstat | search | webmaster | metrika | direct
EXECUTION MODE = Manual | Autorun | other accepted mode if explicitly required
ADDITIONAL STATE = paused/bound/owner-tab/etc. only when relevant
```

Do not rely on the command prefix, previous turn, or operator memory to imply the required mode.

**PURPOSE**  
Prevent avoidable admission failures and operator ambiguity. The operator should be able to read one instruction and know exactly how YMB must be configured before sending the command.

**EVIDENCE**  
A live rehearsal attempted a `WORDSTAT_BATCH_API_V1` command while the active service remained `search`. Bridge correctly rejected it with `SERVICE_NOT_ACTIVE` and `request_executed=false`. The provider was protected, but the operator step was unnecessarily repeated because ChatGPT had not explicitly stated the required extension service/mode immediately before the command.

**FAILURE IF IGNORED**  
If mode is not stated explicitly:

```text
commands can be rejected by SERVICE_NOT_ACTIVE;
the operator must infer state from context;
manual vs autorun requirements can be confused;
repeat attempts waste operator time;
more dangerous failures can occur if a future command has stricter owner-tab/pause/binding requirements.
```

**REVIEW TRIGGER**  
This rule may be simplified only if YMB later selects the correct service/mode automatically and that behavior is formally accepted and fail-safe.

### Required live-dialogue format

Immediately before every YMB command, write a compact instruction such as:

```text
YMB MODE:
- Active service: Wordstat
- Execution mode: Manual
- Manual mode: ON

Then send exactly this command:
...
```

If no toggle is needed for a field, state that clearly rather than omitting the field when omission could create ambiguity.

Marker:

```text
KW001_EXPLICIT_YMB_MODE_INSTRUCTION_ACTIVE = true
```

---

## Rule — mandatory pre-step evidence and methodology review before execution

**RULE**  
Before every new analytical/project execution step, ChatGPT must STOP before execution and perform a visible pre-step review. The next step may not begin merely because the previous step passed.

The pre-step review must happen in this order:

```text
1. identify the exact next step and its intended output;
2. explain in plain language what will be done and what will explicitly NOT be done;
3. reread the previous step's evidence/acceptance and check whether its conclusions still support the next step;
4. identify the methodology/rules proposed for the next step;
5. classify the origin of every material method rule as:
   OFFICIAL
   INDUSTRY_PRACTICE
   PROJECT_TEST_VALIDATED
   ANALYST_HEURISTIC
6. search current external materials relevant to the method BEFORE execution;
7. prefer official/primary sources; when no official standard exists, cross-check with credible practitioner/tool methodology rather than one unsupported article;
8. compare the planned method with those sources and with project evidence;
9. explicitly look for defects in ChatGPT's own previous work, not only evidence that confirms it;
10. classify the review result as:
    SUPPORTED
    PROJECT_SPECIFIC_BUT_REASONED
    QUESTIONABLE
    CORRECTION_REQUIRED
11. if a material rule is only an ANALYST_HEURISTIC, say so explicitly; never present it as an industry or Yandex standard;
12. if CORRECTION_REQUIRED, do not execute the next step until the defect is corrected/re-frozen;
13. show the owner the pre-step explanation, source links/citations, uncertainties and proposed corrections;
14. wait for explicit owner authorization;
15. only then execute the step.
```

A project-authored runbook or earlier ChatGPT document is **not independent proof** that its own method is correct. It may define the current workflow, but methodology validation must trace back to one or more of:

```text
official provider/search-engine documentation;
credible external industry methodology;
measured project/provider evidence;
controlled project tests;
explicitly labelled analyst reasoning/heuristic.
```

**PURPOSE**  
Prevent a self-reinforcing workflow where ChatGPT writes a rule, later cites its own rule as authority, and continues executing without checking whether the rule is actually supported by current provider semantics, established practice or observed evidence.

This gate also makes the owner understand not just WHAT happens next, but WHY the step exists, where the method came from, what uncertainty remains and what would make us change it.

**EVIDENCE**  
During the OKNO-MSK rehearsal, Step 04 cleanup used a conservative `KEEP / REJECT_OBVIOUS / REVIEW` triage. The logic was internally coherent, but the owner correctly requested a retrospective methodological audit rather than accepting the project-authored runbook as sufficient authority. That exposed a process weakness: method validation was happening when challenged, rather than systematically before every new step.

**FAILURE IF IGNORED**  
Without this gate:

```text
ChatGPT can accidentally treat its own previous document as external authority;
heuristics can silently become "standards";
methodological errors can propagate through later expensive provider stages;
cleanup can remove valuable terms before SERP/business evidence exists;
provider budgets can be spent on poorly justified expansion;
owner cannot independently evaluate why a step is being performed;
corrections happen late, after downstream artifacts depend on the mistake.
```

**REVIEW TRIGGER**  
The exact presentation may become shorter if the workflow is mature and repeatedly validated, but the mandatory sequence `explain → research/check sources → self-audit → owner authorization → execute` must remain unless the owner explicitly changes this operating rule.

### Mandatory pre-step live-dialogue format

Before execution ChatGPT must provide, at minimum:

```text
NEXT STEP
WHAT I WILL DO
WHY THIS STEP EXISTS
METHOD ORIGIN
CURRENT EXTERNAL SOURCES
WHAT I FOUND WHEN CHALLENGING MY OWN METHOD
RISKS / UNCERTAINTIES
WHAT I WILL NOT DO YET
PROPOSED GATE
WAITING FOR OWNER AUTHORIZATION
```

For external methodology claims, provide direct source citations/links. If no authoritative external standard was found, write that explicitly.

### Step boundary

This rule applies to each major analytical/project step or gate. It does not require repeating the full external methodology search before every individual `batch.next` item inside an already researched, frozen and owner-authorized provider step. A new batch, new methodology, new evidence type, cleanup stage, clustering stage, page-mapping stage, Search stage, AI stage, QA/finalization stage, or material workflow change requires a new pre-step review.

Marker:

```text
KW001_PRE_STEP_EVIDENCE_METHOD_REVIEW_ACTIVE = true
KW001_OWNER_AUTHORIZATION_BEFORE_EACH_MAJOR_STEP = true
```

---

## Rule — provider work is complete only when the complete result is preserved and verified

**RULE**  
The purpose of a provider step is to obtain usable project evidence, not merely to execute an API call.

A provider request or provider item counts as **COMPLETE for the project** only when all of the following are true:

```text
1. the provider request has a known successful outcome;
2. the complete result required by the step is preserved in the current job workspace;
3. preservation is verified against the provider response or expected returned-row/count truth;
4. the preserved result is readable and available for the next analytical step.
```

The following by themselves are **NOT** evidence that the project step is complete:

```text
HTTP 200
request_executed = true
item_status = SUCCEEDED
succeeded = N
terminal = N
cost recorded
summary/checkpoint with representative examples only
```

If the provider returned 200 rows and only representative examples or a summary were preserved, that request is **NOT COMPLETE for the project**.

### Mandatory stop condition

If complete preservation or verification fails:

```text
current item = FAILED_OR_INCOMPLETE_FOR_PROJECT
current major step = NOT_COMPLETE
next provider item = BLOCKED
next analytical step = BLOCKED
```

ChatGPT must STOP immediately. It must not continue through the remaining batch merely because the provider call itself succeeded.

Recovery must first restore a complete, verified result for the current item. Only then may the next item be executed.

### Purpose hierarchy

For every provider-driven step, ChatGPT must distinguish:

```text
TECHNICAL EXECUTION
= did a provider call occur and what was its transport/provider outcome?

PROJECT COMPLETION
= is the full evidence required by the job preserved, verified and usable?
```

`TECHNICAL EXECUTION = SUCCESS` does not imply `PROJECT COMPLETION = SUCCESS`.

When reporting status to the owner, project completion controls the step verdict.

**PURPOSE**  
Prevent false progress where API requests are counted as completed work although the evidence needed for the actual client task was not preserved. The business goal is to collect and use the data, not to maximize successfully executed requests.

**EVIDENCE**  
During the OKNO-MSK rehearsal, the first Wordstat acquisition pass executed successful provider calls but preserved only summaries and representative examples for many returned result sets. Later steps therefore lacked the complete phrase rows required for full cleanup. Treating the successful calls as a completed acquisition step allowed downstream work to proceed on an incomplete evidence base.

**FAILURE IF IGNORED**  
If this rule is ignored:

```text
provider calls can succeed while the actual dataset is lost;
downstream analysis can silently operate on examples instead of the complete evidence;
expansion decisions can be made from an incomplete source set;
acceptance gates can report false completion;
provider cost and operator time can be wasted on later steps that must be redone;
project progress becomes request-count progress instead of result-delivery progress.
```

**REVIEW TRIGGER**  
None for the core principle. Storage format may change, but a provider-driven project item must never be marked complete without complete verified usable evidence.

### Required per-item live gate

Before moving from provider item N to provider item N+1, ChatGPT must verify and state internally or visibly as appropriate:

```text
provider outcome known = true
complete result preserved = true
preserved row/count truth verified = true
result usable for next stage = true
```

If any value is false, STOP.

Markers:

```text
KW001_PROVIDER_RESULT_PRESERVATION_GATE_ACTIVE = true
KW001_TECHNICAL_SUCCESS_IS_NOT_PROJECT_COMPLETION = true
KW001_NEXT_PROVIDER_ITEM_BLOCKED_UNTIL_RESULT_VERIFIED = true
```
