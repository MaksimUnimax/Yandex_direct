# KW-002 — LEVEL 1 CHATGPT WORK HANDOFF RULE

Status: **ACTIVE / OWNER-LOCKED**  
Owner instruction: 2026-09-08

## 1. Purpose

Large-data work must not be degraded merely to fit an ordinary chat context.

```text
LARGE DATA
!= SAMPLE IT
!= TRUNCATE IT
!= SUMMARIZE BEFORE ANALYSIS

LARGE DATA
→ HAND OFF THE COMPLETE EXECUTION UNIT TO CHATGPT WORK
```

## 2. Trigger

Use ChatGPT Work when one or more are true:

```text
- complete analysis of a large table or several large files is required;
- row-level joins/deduplication/reconciliation cannot be verified reliably in ordinary chat;
- full provider evidence would otherwise be sampled or omitted;
- pairwise/cluster analysis creates a large intermediate universe;
- a final workbook/report must be generated from large structured inputs;
- ordinary-context limits materially risk skipped rows, lost provenance, partial QA or repeated reconstruction.
```

This is a quality trigger, not an arbitrary row-count threshold.

## 3. Canonical Work prompt authority

The MAIN CHATGPT WORKFLOW prepares the exact Work prompt for the current step. The owner/user only relays that prompt to ChatGPT Work.

```text
MAIN CHATGPT = PROMPT AUTHOR
OWNER / USER = PROMPT RELAY
CHATGPT WORK = EXECUTION ENVIRONMENT
```

Mandatory sequence:

```text
CURRENT STEP PRE-STEP REVIEW
→ WORK TRIGGER CONFIRMED
→ PRE-HANDOFF MANIFEST FROZEN
→ MAIN CHATGPT WRITES COMPLETE CANONICAL WORK PROMPT
→ OWNER RELAYS PROMPT TO WORK WITHOUT NEEDING TO DESIGN IT
→ WORK EXECUTES
→ OWNER RETURNS WORK RESULT/ARTIFACTS
→ MAIN CHATGPT RUNS RETURN QA
```

The owner is not responsible for inventing, completing or correcting the Work prompt.

Main ChatGPT must include all current step/job constraints in the prompt and must not ask the owner to supply a methodology prompt that the project already knows how to construct.

If the owner edits the prompt intentionally, the latest explicit owner instruction has authority. Otherwise the generated prompt is the canonical handoff contract for that execution.

## 4. Required pre-handoff manifest

Before writing the Work prompt, freeze:

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

For clean tests, the source whitelist is mandatory.

## 5. Work is execution environment, not authority

```text
WORK OUTPUT != AUTOMATICALLY ACCEPTED TRUTH
```

Work must obey the same Level 1 and Level 2 rules as ordinary execution and may not:

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

## 7. No ordinary-chat fallback by quality reduction

If a Work-triggered step cannot be run in Work, do not silently switch to representative samples, first-N rows, manual examples or summary-only processing.

Record `WORK_EXECUTION_REQUIRED / BLOCKED`, or split into complete independently valid units only when the Level 2 method explicitly permits it without loss of global coherence.

## 8. Relation to Bridge

```text
BRIDGE = PROVIDER EVIDENCE ACQUISITION / PERSISTENCE
WORK = LARGE-DATA ANALYSIS / TRANSFORMATION / ARTIFACT EXECUTION
MAIN CHATGPT = METHOD CONTROL / WORK PROMPT AUTHOR / DECISIONS / RETURN QA / OWNER COMMUNICATION
OWNER = AUTHORIZATION / PROMPT RELAY / RESULT RETURN
```

## 9. Markers

```text
KW002_WORK_HANDOFF_RULE_ACTIVE = true
KW002_MAIN_CHATGPT_WRITES_WORK_PROMPT = true
KW002_OWNER_RELAYS_WORK_PROMPT = true
KW002_OWNER_DOES_NOT_HAVE_TO_DESIGN_WORK_PROMPT = true
KW002_LARGE_DATA_MUST_NOT_BE_SAMPLED_FOR_CONTEXT_CONVENIENCE = true
KW002_WORK_OUTPUT_REQUIRES_RETURN_QA = true
```