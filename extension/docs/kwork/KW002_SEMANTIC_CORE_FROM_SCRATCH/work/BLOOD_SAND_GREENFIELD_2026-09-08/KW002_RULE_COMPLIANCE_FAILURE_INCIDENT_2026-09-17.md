# KW-002 / BLOOD & SAND — RULE COMPLIANCE FAILURE INCIDENT — 2026-09-17

Status: **ACTIVE INCIDENT RECORD / ANTI-REGRESSION EVIDENCE**  
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`  
Date: 2026-09-17

This file records concrete job-specific Main Chat failures. Universal mechanisms belong in Level1.

## 1. Repeated root pattern

```text
RULE ALREADY EXISTED
→ MAIN CHAT DID NOT APPLY THE CURRENT RULE CORRECTLY
→ MAIN CHAT PRODUCED A PLAUSIBLE BUT NON-COMPLIANT PROCESS RESPONSE
→ OWNER POINTED TO THE DEFECT
→ MAIN CHAT CORRECTED AFTER THE FACT
```

The root problem was Main Chat governance, not Work execution.

## 2. Concrete incidents

### I-2026-09-17-01 — wrong Work boundary for Step07 preparation

Main Chat initially treated actual Step07 as the Work unit while Step07 preparation itself already met the large-data trigger.

Correction: complete preparation was delegated to Work.

### I-2026-09-17-02 — owner was asked to route files manually

Main Chat initially gave several GitHub target directories and expected the owner to sort files.

Correction:

```text
ONE HANDOFF
→ ONE OWNER STAGING TARGET
→ MAIN CHAT DOES FINAL PATH ROUTING / CLEANUP / READBACK
```

### I-2026-09-17-03 — mandatory clickable materials omitted from owner-facing chat

The methodology artifact contained source URLs, but Main Chat did not initially disclose them in chat with supported claims and method impact.

Correction:

```text
SOURCE LINKS IN ARTIFACT != OWNER-FACING SOURCE DISCLOSURE
```

### I-2026-09-17-04 — plain-language summary omitted

Main Chat substituted statuses/hashes/files for the mandatory normal-Russian WHY / WHAT / RESULT / BLOCKER / NEXT ACTION explanation.

### I-2026-09-17-05 — technical preparation PASS treated as enough

Technical artifacts/publication were treated as sufficient before owner-facing reporting compliance was checked.

Correction:

```text
TECHNICAL_ARTIFACT_PASS != OWNER_FACING_REPORT_PASS
```

### I-2026-09-17-06 — explanation before reopening the exact live rule

Main Chat initially explained from memory instead of fetching/applying the controlling rule first.

Correction:

```text
OWNER POINTS TO RULE FAILURE
→ MAIN CHAT FETCHES LIVE RULE
→ APPLIES IT
→ THEN EXPLAINS
```

### I-2026-09-17-07 — concrete incident briefly contaminated Level1

A Step07-specific incident was initially written into a universal Level1 checklist.

Correction: universal mechanism stays Level1; concrete incident stays here in job-root.

### I-2026-09-17-08 — Main Chat governance gates were wrongly pushed into Work runtime

Observed:

After Main Chat had already performed full rule reread, fresh external research, owner-facing source disclosure and Step07 release authorization, Main Chat copied those same governance gates into the actual Step07 Work prompt and required Work to repeat them before executing.

Why this is wrong:

```text
MAIN CHAT = ARCHITECT / GOVERNANCE / RELEASE / ACCEPTANCE
WORK = EXECUTOR OF THE RELEASED CONTRACT
```

Duplicating Main Chat governance inside Work:

- wastes Work context and execution budget;
- blurs architect/executor roles;
- creates duplicated and potentially conflicting release authority;
- turns a concrete execution task back into another planning/research/release task.

Permanent correction:

```text
MAIN CHAT DOES RULE / RESEARCH / REPORT / RELEASE GATES
→ MAIN CHAT ISSUES FROZEN EXECUTION PROMPT
→ WORK EXECUTES THAT PROMPT
```

Work startup is limited to a narrow technical safety check:

```text
CURRENT REMOTE HEAD
+ RELEASE RECORD IDENTITY
+ PROMPT IDENTITY
+ INPUT / MANIFEST / SCHEMA / HASH IDENTITY
→ MATERIAL DRIFT? STOP
→ OTHERWISE EXECUTE
```

Work does NOT repeat by default:

```text
FULL LEVEL1 REREAD
FRESH EXTERNAL METHODOLOGY RESEARCH
OWNER-FACING SOURCE DISCLOSURE
OWNER-FACING PLAIN-LANGUAGE REPORT
RELEASE AUTHORIZATION
MAIN CHAT FAILURE-HISTORY REVIEW
```

## 3. Correct permanent architecture

```text
MAIN CHAT
= READ RULES / RESEARCH / METHOD / OWNER REPORT / WORK PROMPT / RELEASE / RETURN QA / ACCEPTANCE / CURSOR

WORK
= FULL-VOLUME EXECUTION / ARTIFACT MATERIALIZATION / TASK QA / HANDOFF PACKAGE

OWNER
= AUTHORIZATION / PROMPT RELAY / SINGLE-STAGING BYTE RELAY
```

## 4. Main Chat fail-closed rule

The fresh full-rule reread/no-action controls created after these incidents apply to Main Chat governance, not Work runtime.

```text
MAIN CHAT NO FRESH APPLICABLE RULE REREAD
→ NO MAIN CHAT MATERIAL GOVERNANCE ACTION
```

This includes Main Chat preparation, research release, Work prompt authoring/release, provider release, acceptance, publication control and cursor/roadmap movement.

## 5. Work runtime rule

```text
RELEASED CANONICAL WORK PROMPT EXISTS
→ WORK EXECUTES IT
```

Work does not inherit the Main Chat governance checklist merely because its task touches project files.

The Work prompt itself must contain all execution-relevant constraints.

## 6. Current Step07 boundary

At the time of this scope correction:

```text
STEP06 = DURABLE PASS
STEP07_PREPARATION = ACCEPTED
STEP07_RELEASE = AUTHORIZED BY MAIN CHAT
STEP07 = NOT YET EXECUTED
STEP08 = NOT STARTED
```

The actual Step07 Work prompt must be the corrected execution-only version, without duplicated Main Chat gates.

## 7. Plain-language incident conclusion

The latest mistake was that Main Chat finally did its own checks, but then forced Work to do the same checks all over again. That is the wrong architecture. The permanent correction is now explicit in the repository: Main Chat does the project governance once; Work receives the finished task and executes it. Work only checks that the released inputs have not materially changed while the task was being handed over.
