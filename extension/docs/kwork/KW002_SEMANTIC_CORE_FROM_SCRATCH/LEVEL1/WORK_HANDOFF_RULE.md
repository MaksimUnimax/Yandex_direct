# KW-002 — LEVEL 1 CHATGPT WORK HANDOFF RULE

Status: **ACTIVE / OWNER-LOCKED**  
Owner instruction: 2026-09-08

## 1. Purpose

Large-data work must not be degraded merely to fit an ordinary chat context.

Canonical rule:

```text
LARGE DATA
!= SAMPLE IT
!= TRUNCATE IT
!= SUMMARIZE BEFORE ANALYSIS

LARGE DATA
→ HAND OFF THE COMPLETE EXECUTION UNIT TO CHATGPT WORK
```

The Work handoff exists to preserve completeness, joins, row-level QA, traceability and artifact generation when an ordinary conversation is not a reliable execution environment for the whole dataset.

## 2. Trigger

Use ChatGPT Work when one or more are true:

```text
- the step requires complete analysis of a large table or several large files;
- row-level joins/deduplication/reconciliation cannot be verified reliably in ordinary chat;
- the full provider evidence would otherwise be sampled or omitted;
- pairwise/cluster analysis creates a large intermediate universe;
- a final workbook/report must be generated from large structured inputs;
- ordinary-context limits create a material risk of skipped rows, lost provenance, partial QA or repeated restart/reconstruction.
```

This is a quality trigger, not an arbitrary row-count threshold.

## 3. Owner-supplied prompt authority

The canonical Work prompt is supplied by the owner.

```text
OWNER WORK PROMPT = AUTHORITATIVE HANDOFF TEMPLATE
```

Once supplied:

- use that prompt;
- fill only the current step/job variables it explicitly allows;
- do not silently rewrite its execution contract;
- do not invent a replacement prompt because another wording seems convenient.

Before the owner supplies the canonical prompt, the project may prepare the handoff manifest but must not pretend a different generic prompt is the approved Work contract.

## 4. Required pre-handoff manifest

Before Work receives a large-data task, freeze:

```text
JOB_ID
STEP_ID
WHY_WORK_REQUIRED
ALLOWED_INPUT_FILES / SOURCES
PROHIBITED_INPUT_FILES / SOURCES
CURRENT AUTHORITATIVE UPSTREAM ARTIFACTS
EXACT EXECUTION GOAL
REQUIRED OUTPUT FILES / TABLES
MANDATORY FIELDS
ROW / COUNT / JOIN EXPECTATIONS where known
CLAIM BOUNDARIES
QA / ACCEPTANCE CHECKS
STOP CONDITIONS
```

For clean tests, the source whitelist is mandatory. Work may not browse/open sealed prior-research artifacts merely because they exist in the repository.

## 5. Work is execution environment, not authority

```text
WORK OUTPUT != AUTOMATICALLY ACCEPTED TRUTH
```

Work must obey the same Level 1 and Level 2 rules as ordinary execution.

Work is not allowed to:

- create new permanent methodology;
- override client scope;
- silently drop rows;
- replace missing evidence with assumptions;
- change evidence classes;
- treat partial processing as complete;
- use prohibited prior-research sources;
- silently make provider calls outside the authorized step.

## 6. Post-Work return gate

After Work finishes:

```text
1. receive produced artifacts/results;
2. verify source manifest;
3. verify row/count/join truth;
4. verify required fields and provenance;
5. inspect HOLD/ERROR/UNRESOLVED rows;
6. compare output to Level 2 acceptance contract;
7. persist accepted artifacts in work/<JOB_ID>/;
8. read back from GitHub/storage;
9. only then mark the step complete and continue.
```

If verification fails, the step remains incomplete.

## 7. No ordinary-chat fallback by quality reduction

If a Work-triggered step cannot currently be run in Work, do not silently switch to:

```text
representative sample only
first N rows
manual examples
summary without full processing
```

Instead record `WORK_EXECUTION_REQUIRED / BLOCKED` or split the work into complete, independently valid execution units only when the Level 2 step method permits such partitioning without loss of global coherence.

## 8. Relation to Bridge

Yandex Marketing Bridge remains the governed provider-acquisition hand.

ChatGPT Work may analyze preserved provider evidence and create artifacts, but it does not automatically become authorized to perform provider calls.

Canonical separation:

```text
BRIDGE = PROVIDER EVIDENCE ACQUISITION / PERSISTENCE
WORK = LARGE-DATA ANALYSIS / TRANSFORMATION / ARTIFACT EXECUTION
CHATGPT MAIN WORKFLOW = METHOD CONTROL / DECISIONS / QA / OWNER COMMUNICATION
OWNER = AUTHORIZATION / CANONICAL WORK PROMPT
```

## 9. Marker

```text
KW002_WORK_HANDOFF_RULE_ACTIVE = true
KW002_OWNER_SUPPLIED_WORK_PROMPT_REQUIRED = true
KW002_LARGE_DATA_MUST_NOT_BE_SAMPLED_FOR_CONTEXT_CONVENIENCE = true
KW002_WORK_OUTPUT_REQUIRES_RETURN_QA = true
```
