# KW-002 — RECURRING ASSISTANT RULE FAILURES / ANTI-REGRESSION CHECKLIST

Status: **ACTIVE / OWNER-LOCKED / MANDATORY BEFORE EVERY MATERIAL ACTION**  
Owner lock: 2026-09-17

This checklist stores **universal assistant/executor failure mechanisms** that can recur in any KW-002 job. Concrete job incidents, client names, step-specific examples, exact commits and current counts belong in `work/<JOB_ID>/`.

## Known recurring failure pattern

```text
RULE EXISTS
→ ASSISTANT DOES NOT FRESHLY READ IT IN FULL
→ ASSISTANT WORKS FROM MEMORY / SUMMARY
→ ASSISTANT PRODUCES A PLAUSIBLE BUT NON-COMPLIANT RESULT
→ OWNER HAS TO POINT TO THE EXISTING RULE
→ ASSISTANT PATCHES AFTER THE FACT
```

This pattern is itself a named blocking defect.

Before any material action, the executor must prove that it is not repeating this pattern.

## Universal repeated failure classes

### F-RULE-01 — acting from remembered project rules

Failure mechanism: assistant/executor uses memory, summaries, earlier chat state or prior successful execution instead of rereading current live owner-locked rules.

Permanent control:

```text
READ CURRENT LIVE APPLICABLE RULES IN FULL BEFORE ACTION
MEMORY DOES NOT COUNT
```

### F-RULE-02 — incomplete owner-facing pre-step report

Failure mechanism: technical preparation/status is reported without the full mandatory owner-facing structure.

Permanent control:

Read `PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md` in full before drafting the report.

The report must include goal, roadmap, completed/remaining, current-step purpose, prior failures/non-repeat controls, fresh research, source links, source→method trace, method, applicable execution gate, PASS conditions and plain-language conclusion.

### F-RULE-03 — external materials exist in an artifact but are not disclosed in chat

Failure mechanism: source URLs are preserved in a methodology/research artifact, but owner-facing chat omits them.

Permanent control:

```text
ARTIFACT SOURCE LIST != CHAT SOURCE DISCLOSURE
```

The chat itself must contain clickable source links plus what each source supports, how it affects/confirms the method and its limitation.

### F-RULE-04 — status/hash dump substituted for plain-language summary

Failure mechanism: technical statuses, hashes, filenames, request IDs or QA markers are used where normal Russian explanation is mandatory.

Permanent control:

Every major report ends with normal Russian explaining:

```text
WHY
WHAT
RESULT
CAN WE CONTINUE
BLOCKER IF ANY
NEXT PHYSICAL ACTION
```

### F-RULE-05 — Work trigger evaluated for the wrong boundary

Failure mechanism: assistant evaluates whether a later execution step needs Work but fails to evaluate whether the **current execution unit itself** (including preparation, reconciliation, audit or packaging) already meets the large-data trigger.

Permanent control:

Evaluate Work trigger for the current complete execution unit before doing the work.

```text
LARGE DATA → COMPLETE EXECUTION UNIT TO WORK
NO SAMPLING / NO TRUNCATION / NO SUMMARY SUBSTITUTION
```

### F-RULE-06 — owner made responsible for repository routing

Failure mechanism: assistant gives multiple final folders/NEW/REPLACE decisions and asks the owner to sort a multi-file handoff manually.

Permanent control:

```text
ONE HANDOFF
→ ONE OWNER STAGING UPLOAD
→ EXECUTOR DOES FINAL PATH ROUTING
→ EXECUTOR CLEANS STAGING
→ REMOTE READBACK
```

The owner relays bytes; the executor owns final repository placement and acceptance.

### F-RULE-07 — technical artifact PASS treated as sufficient owner-facing completion

Failure mechanism: artifacts/QA/publication are technically correct, but required source disclosure or plain-language owner report is missing, and the assistant still treats the process as fully complete.

Permanent control:

```text
TECHNICAL_ARTIFACT_PASS
!= OWNER_FACING_REPORT_PASS
```

Both gates must pass where required.

### F-RULE-08 — explaining a rule failure before reopening the controlling rule

Failure mechanism: assistant narrates causes/consequences from memory instead of first fetching and applying the live rule the owner says was violated.

Permanent control:

```text
OWNER POINTS TO RULE FAILURE
→ FETCH LIVE RULE
→ READ IN FULL
→ APPLY RULE
→ THEN EXPLAIN CONCISELY
```

### F-RULE-09 — concrete incident contaminates permanent methodology

Failure mechanism: a specific client, step ID, query/family ID, current row count or one concrete incident is copied into Level1/Level2 as if it defines the universal rule.

Permanent control:

```text
JOB INCIDENT
→ IDENTIFY GENERAL MECHANISM
→ UNIVERSAL CONTROL IN LEVEL1/LEVEL2
→ CONCRETE INCIDENT STAYS IN work/<JOB_ID>/
```

Before accepting permanent-rule edits, apply `ROADMAP_AND_METHOD_GENERALIZATION_RULE.md` and `JOB_DATA_SEPARATION_AND_LIFECYCLE.md`.

## Mandatory pre-action checklist

Before every preparation / execution / Work handoff / Bridge action / QA / acceptance / publication / cursor movement:

```text
[ ] current remote HEAD fetched
[ ] 00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE read in full
[ ] COMMON_RULES read in full
[ ] INHERITED_KW001_UNIVERSAL_RULES read in full
[ ] applicable owner-locked Level1 rules read in full
[ ] current Level2 step/gates read in full when a roadmap step is involved
[ ] current JOB_FLOW + cursor read in full when a concrete job is involved
[ ] relevant failure ledger/checklist read in full
[ ] owner-facing report gate read in full
[ ] Work gate read in full if applicable
[ ] provider/Bridge gate read in full if applicable
[ ] generalization/layer-separation gate read in full before permanent-method mutation
[ ] current external-method research requirement evaluated
[ ] clickable source disclosure prepared in chat when required
[ ] plain-language WHY/WHAT/RESULT/BLOCKER/NEXT block prepared
[ ] no unresolved authority conflict
```

If any applicable box is not proven:

```text
EXECUTION_ALLOWED = false
```

## Mandatory post-action checklist

Before acceptance / cursor advance:

```text
[ ] acceptance rules reread in full
[ ] actual output/result fetched
[ ] remote/provider readback completed where required
[ ] counts/joins/provenance checked
[ ] HOLD/ERROR/UNRESOLVED checked
[ ] staging cleanup checked where applicable
[ ] permanent-method contamination audit passed where applicable
[ ] owner-facing result report complete
[ ] plain-language conclusion complete
[ ] next physical action stated
```

## Marker

```text
KW002_RECURRING_ASSISTANT_RULE_FAILURE_PATTERN_RECOGNIZED = true
KW002_RULE_MEMORY_RELIANCE_FORBIDDEN = true
KW002_RULE_REREAD_CHECKLIST_REQUIRED = true
KW002_CHAT_SOURCE_DISCLOSURE_IS_SEPARATE_GATE = true
KW002_PLAIN_LANGUAGE_OWNER_REPORT_IS_SEPARATE_GATE = true
KW002_REPEAT_FAILURE_REQUIRES_RULE_REOPEN_BEFORE_EXPLANATION = true
KW002_WORK_TRIGGER_CURRENT_EXECUTION_UNIT_CHECK_REQUIRED = true
KW002_OWNER_REPOSITORY_ROUTING_FORBIDDEN = true
KW002_JOB_INCIDENT_TO_UNIVERSAL_GENERALIZATION_GATE_REQUIRED = true
```
