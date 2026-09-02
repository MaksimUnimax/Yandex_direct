# OKNO_MSK — Step 16 process failures and mandatory non-repeat controls

Date: 2026-09-02
Authority type: **job-specific Step-16 execution rule / owner-requested non-repeat record**
Status: **ACTIVE FOR THE REMAINDER OF STEP 16**

## Purpose

The owner explicitly required Step 16 to record where ChatGPT failed during Step-16 preparation, why those failures occurred, and the exact controls that must prevent recurrence during the remainder of this step.

This file does not modify Layer-A universal rules. It operationalizes the already owner-approved universal rules inside the current Step-16 job execution.

## Failure S16-P01 — method research started before the mandatory owner-facing goal/full-roadmap block

### What ChatGPT did wrong

After Step 16 was requested to be prepared, ChatGPT began reading method/provider material and preparing Step-16 artifacts before first presenting the complete live owner-facing sequence required by `STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md`:

```text
WHOLE KWORK GOAL
-> ONE FULL START-TO-CLOSE ROADMAP
-> COMPLETED WORK
-> REMAINING WORK
-> CURRENT STEP GOAL
-> WHAT THIS STEP SOLVES
-> REQUIRED OUTPUT
-> RELEVANT PRIOR ERRORS / ROOT CAUSE / NON-REPEAT CONTROL
-> ONLY THEN METHOD RESEARCH
```

A short technical status paragraph was incorrectly treated as sufficient.

### Why it happened

ChatGPT prioritized technical gates — source-to-method traceability, provider capability, cost, persistence and authorization — and treated the owner-communication gate as a presentation requirement instead of an execution-order constraint.

Canonical causal error:

```text
TECHNICAL PREPARATION READY
WAS INCORRECTLY TREATED AS
STEP READY FOR METHOD RESEARCH
```

### Consequence

The Step-16 research work remained useful, but the transition was procedurally invalid until the full live owner-facing gate was reissued.

### Non-repeat control

Before any new material Step-16 substage that changes method/scope/evidence type:

```text
GOAL_FIRST_BLOCK_PRESENT = true
FULL_0_22_ROADMAP_PRESENT = true
COMPLETED_REMAINING_PRESENT = true
STEP_GOAL_SOLVES_OUTPUT_PRESENT = true
RELEVANT_ERRORS_AND_CONTROLS_PRESENT = true
```

If any is false:

```text
METHOD_CHANGE = BLOCKED
PROVIDER_EXECUTION = BLOCKED
```

## Failure S16-P02 — the mandatory plain-language summary was present but was not kept as the final explanatory block

### What ChatGPT did wrong

ChatGPT wrote a `ПРОСТЫМИ СЛОВАМИ` pre-step summary, then continued with technical GitHub/readback/status explanation and ended the response in technical language.

The universal rule does not merely require that a simple-language block appear somewhere. It requires the last owner-facing explanation before authorization/transition to be understandable without specialist vocabulary.

### Why it happened

ChatGPT incorrectly treated GitHub persistence/readback communication as being outside the owner-facing explanation and therefore failed to re-run the final response-order check after those technical updates.

Canonical causal error:

```text
PLAIN_LANGUAGE_SUMMARY_EXISTS
WAS INCORRECTLY TREATED AS
PLAIN_LANGUAGE_SUMMARY_IS_FINAL
```

### Consequence

The communication gate was violated again even though the rule had just been reread.

### Non-repeat control — mandatory pre-send response-order gate

Before sending any owner-facing Step-16 pre-step/transition/end-of-step response, check:

```text
1. FULL ROADMAP PRESENT WHEN REQUIRED?
2. COMPLETED + REMAINING PRESENT WHEN REQUIRED?
3. STEP GOAL / SOLVES / OUTPUT PRESENT?
4. PRIOR ERROR + ROOT CAUSE + NON-REPEAT CONTROL PRESENT?
5. METHOD / SOURCES / RISKS / PASS GATE PRESENT WHEN APPLICABLE?
6. PLAIN-LANGUAGE SUMMARY PRESENT?
7. IS THE PLAIN-LANGUAGE SUMMARY THE LAST EXPLANATORY BLOCK?
```

If #7 is false:

```text
RESPONSE = BLOCKED
MOVE OR REPEAT THE PLAIN-LANGUAGE SUMMARY TO THE END
RECHECK
ONLY THEN SEND
```

No technical explanatory tail may follow the final plain-language block. If tool/GitHub work happens after a previously written simple summary, the final user-facing message must end with a fresh plain-language summary again.

## Failure S16-P03 — rules were reread but not fully operationalized as a pre-send control

### What ChatGPT did wrong

ChatGPT correctly reread the relevant universal rule and even identified the simple-language requirement, but still repeated the same communication error in the next prepared response.

### Why it happened

The rule was retained as remembered content/checklist knowledge instead of becoming an enforced response-state condition.

This is the same structural failure class described by `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`:

```text
RULE READ != RULE OPERATIONALIZED
REQUIREMENT KNOWN != EXECUTION CONTROL ACTIVE
```

### Non-repeat control

For the remainder of Step 16, owner-facing communication gates are treated as executable state, not prose guidance.

Required current state flags:

```text
STEP16_GOAL_FIRST_GATE = PASS
STEP16_FULL_ROADMAP_GATE = PASS
STEP16_PLAIN_LANGUAGE_FINAL_POSITION_GATE = PASS
STEP16_PRE_SEND_RESPONSE_ORDER_GATE = PASS
```

Any failed flag blocks transition.

## Failure S16-P04 — risk of conflating provider technical success with project evidence completion

### Prior project failure relevant to Step 16

Earlier provider work showed that `HTTP 200`, `request_executed=true`, `SUCCEEDED` or cost accounting can exist while the complete evidence needed by the project is not durably preserved.

### Why it matters now

GenSearch results are paid and can vary; losing a useful response can force paid replay and can destroy reproducibility.

### Non-repeat control

After every useful Step-16 provider interaction:

```text
PROVIDER RESULT
-> COMPLETE RAW GITHUB WRITE
-> GITHUB READBACK
-> COMPLETENESS / ACCOUNTING QA
-> NORMALIZED OBSERVATION WRITE
-> NORMALIZED READBACK
-> ONLY THEN ANALYSIS / CLASSIFICATION / NEXT PAID ACTION
```

Failure of write/readback blocks the next paid action.

## Failure S16-P05 — Step15 V1 manual lineage drift must not contaminate Step16

### What failed upstream

Step15 V1 manually reconstructed QF metadata and produced wrong pair IDs/query/owner metadata on multiple cases.

### Root cause

```text
MANUAL RECONSTRUCTION / MEMORY
WAS USED INSTEAD OF
EXACT AUTHORITATIVE ID JOIN
```

### Non-repeat control

Step16 execution input is only `STEP_15_SELECTED_CASES_V2.tsv`.

Before every initial/confirmation/retry call:

```text
CASE_ID EXACT MATCH = true
AUTHORITATIVE_QUERY EXACT MATCH = true
V1 INPUT USED = false
```

## Failure S16-P06 — unsupported GenSearch interpretation must not be invented

### Risk

Step15 wording included `used-source hierarchy` for one case, while official GenSearch documents `sources[].used` but does not define array position as source ranking.

### Non-repeat control

```text
sources[].used = provider evidence
sources[] array order = preserved raw only
sources[] array order != rank / importance
GEN_SEARCH_* != CONSUMER_ALICE_*
```

No classification may depend on source-array position.

## Failure S16-P07 — one generative delta must not auto-rewrite architecture

### Risk

A single generated answer may look materially different and tempt immediate architecture change.

### Non-repeat control

```text
INITIAL MATERIAL DIAGNOSTIC RESULT -> CHANGE_CANDIDATE
INITIAL MATERIAL CONTROL RESULT -> CONTROL_BREAK_CANDIDATE
-> REQUIRED SAME-EXACT-QUERY CONFIRMATION
-> ONLY CONFIRMED MATERIAL DIRECTION MAY BE HANDED TO STEP17
```

Step16 never rewrites architecture.

## Mandatory execution-time checklist for every paid Step-16 interaction

Before command:

```text
OWNER AUTHORIZATION COVERS THIS INTERACTION = true
CASE / EXACT QUERY VERIFIED = true
ATTEMPT TYPE STATED = true
EXPECTED INCREMENTAL COST STATED = true
YMB ACTIVE SERVICE STATED = search
YMB EXECUTION MODE STATED = Manual
MANUAL MODE STATE STATED = ON when required
```

After result:

```text
PROVIDER EXECUTION TRUTH KNOWN
OUTCOME KNOWN OR OUTCOME_UNKNOWN
USEFUL EVIDENCE STATE KNOWN
USEFUL RAW RESULT PERSISTED BEFORE ANALYSIS
RAW READBACK PASS
NORMALIZED OBSERVATION PERSISTED
NORMALIZED READBACK PASS
ACCOUNTING RECONCILED
ONLY THEN OUTCOME CLASSIFIED
ONLY THEN NEXT PAID ACTION CONSIDERED
```

## Mandatory end-of-Step-16 communication control

The final Step-16 report must contain detailed evidence/accounting and updated full roadmap, then end with:

```text
ПРОСТЫМИ СЛОВАМИ — ИТОГ

Зачем делали этот шаг
Что фактически сделали
Что получили и что это даёт дальше
```

Nothing technical may follow that final plain-language explanation.

## Additional mandatory method-validation authority

The post-run external audit found **four additional method-validation defects** that are separate from S16-P01..S16-P09 and must be applied before any future Step-16-like execution:

```text
S16-M01 — reproducibility / repeat policy was not defined strongly enough before paid execution
S16-M02 — exact-query evidence was allowed to expand into broader user-job claims
S16-M03 — GenSearch proxy boundary existed but was not fully enforced in result naming/owner-facing claims
S16-M04 — Step 16 crossed into Step 17 Search-vs-AI comparison/decision work
```

Full causes, external source support, blocking gates and the corrected Step-16 execution contract are authoritative in:

`STEP_16_METHOD_VALIDATION_AND_CORRECT_EXECUTION_ADDENDUM_2026-09-02.md`

Mandatory rule:

```text
BEFORE ANY FUTURE STEP16-LIKE PAID EXECUTION
-> READ THIS PARENT RULE
-> READ STEP_16_METHOD_VALIDATION_AND_CORRECT_EXECUTION_ADDENDUM_2026-09-02.md
-> PASS ALL METHOD-VALIDATION PREFLIGHT MARKERS
-> ONLY THEN PROVIDER EXECUTION MAY BE CONSIDERED
```

If the addendum is not read and operationalized:

```text
STEP16_METHOD_VALIDATION = FAILED
PAID_PROVIDER_EXECUTION = BLOCKED
```

## Markers

```text
STEP16_PROCESS_FAILURES_EXPLICITLY_RECORDED = true
STEP16_ROOT_CAUSES_EXPLICITLY_RECORDED = true
STEP16_PRE_SEND_RESPONSE_ORDER_GATE_REQUIRED = true
STEP16_PLAIN_LANGUAGE_SUMMARY_MUST_BE_FINAL_EXPLANATORY_BLOCK = true
STEP16_RULE_READ_NOT_EQUAL_RULE_OPERATIONALIZED = true
STEP16_USEFUL_PROVIDER_RESULT_PERSIST_BEFORE_ANALYSIS = true
STEP16_EXACT_V2_LINEAGE_ONLY = true
STEP16_SOURCE_ORDER_RANK_INFERENCE_FORBIDDEN = true
STEP16_SINGLE_MATERIAL_DELTA_NOT_ARCHITECTURE_CHANGE = true
STEP16_METHOD_VALIDATION_ADDENDUM_REQUIRED = true
STEP16_S16_M01_TO_M04_MUST_BE_REVIEWED_BEFORE_PAID_EXECUTION = true
```
