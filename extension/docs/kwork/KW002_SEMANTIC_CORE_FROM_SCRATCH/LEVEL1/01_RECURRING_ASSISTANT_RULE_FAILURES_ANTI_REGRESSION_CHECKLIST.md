# KW-002 — MAIN CHAT RECURRING RULE FAILURES / ANTI-REGRESSION CHECKLIST

Status: **ACTIVE / OWNER-LOCKED / MAIN-CHAT-ONLY**  
Owner lock: 2026-09-17  
Scope correction: 2026-09-17 — **THIS CHECKLIST CONTROLS MAIN CHAT / ARCHITECT / REVIEW / ACCEPTANCE. IT IS NOT A CHATGPT WORK RUNTIME CHECKLIST.**

## 1. Known recurring Main Chat failure pattern

```text
RULE EXISTS
→ MAIN CHAT DOES NOT FRESHLY READ IT
→ MAIN CHAT WORKS FROM MEMORY / SUMMARY
→ MAIN CHAT PRODUCES A PLAUSIBLE BUT NON-COMPLIANT RESULT
→ OWNER POINTS TO THE EXISTING RULE
→ MAIN CHAT PATCHES AFTER THE FACT
```

This pattern is a blocking Main Chat governance defect.

## 2. Work exclusion

```text
THIS CHECKLIST
= MAIN CHAT ANTI-REGRESSION CONTROL
!= WORK EXECUTION CHECKLIST
```

After Main Chat has frozen and released a Work prompt, Work is not required to reread this checklist, reproduce its history, generate owner-facing reports, rerun external research or decide whether the step should be released.

The Work prompt must contain only the anti-regression controls materially necessary to execute the concrete task.

## 3. Universal Main Chat failure classes

### F-RULE-01 — acting from remembered project rules

Main Chat uses memory/summary instead of current live authority.

Control:

```text
MAIN CHAT READS CURRENT APPLICABLE RULES BEFORE GOVERNANCE / RELEASE / ACCEPTANCE
MEMORY DOES NOT COUNT
```

### F-RULE-02 — incomplete owner-facing report

Main Chat reports technical status without the required owner-facing structure.

Control: Main Chat reads `PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md` before the report.

### F-RULE-03 — sources exist in an artifact but are not disclosed in chat

```text
ARTIFACT SOURCE LIST != OWNER-FACING CHAT DISCLOSURE
```

Main Chat must show clickable sources + supported claim + method effect + limitation when required.

### F-RULE-04 — status/hash dump substituted for plain language

Main Chat must end major reports with normal Russian explaining:

```text
WHY
WHAT
RESULT
CAN WE CONTINUE
BLOCKER IF ANY
NEXT PHYSICAL ACTION
```

### F-RULE-05 — Work trigger evaluated for the wrong execution unit

Main Chat must decide whether the **current complete unit** requires Work.

```text
LARGE DATA → COMPLETE UNIT TO WORK
NO SAMPLING / TRUNCATION FOR CHAT CONVENIENCE
```

### F-RULE-06 — owner made responsible for repository routing

```text
ONE HANDOFF
→ ONE OWNER STAGING UPLOAD
→ MAIN CHAT DOES FINAL ROUTING / CLEANUP / READBACK
```

### F-RULE-07 — technical artifact PASS treated as enough

```text
TECHNICAL_ARTIFACT_PASS != OWNER_FACING_REPORT_PASS
```

### F-RULE-08 — explaining failure before reopening the live rule

```text
OWNER POINTS TO RULE FAILURE
→ MAIN CHAT FETCHES LIVE RULE
→ READS IT
→ APPLIES IT
→ THEN EXPLAINS
```

### F-RULE-09 — concrete incident contaminates permanent methodology

```text
JOB INCIDENT
→ GENERAL MECHANISM
→ UNIVERSAL CONTROL IN LEVEL1/LEVEL2
→ CONCRETE INCIDENT REMAINS IN work/<JOB_ID>/
```

### F-RULE-10 — Main Chat governance duplicated inside Work prompt

Failure mechanism: Main Chat correctly performs rule/research/release gates, then copies the same full governance cycle into Work, forcing the executor to redo Main Chat's job before executing the concrete task.

Why it fails:

- wastes Work context and execution budget;
- blurs architect vs executor roles;
- creates conflicting duplicated authority checks;
- can turn a concrete execution prompt into another planning/release exercise.

Permanent control:

```text
MAIN CHAT DOES GOVERNANCE ONCE
→ RELEASES FROZEN EXECUTION CONTRACT
→ WORK EXECUTES IT
```

Allowed Work startup check:

```text
CURRENT HEAD
+ RELEASE IDENTITY
+ INPUT / MANIFEST / SCHEMA IDENTITY
+ MATERIAL DRIFT STOP
```

Forbidden by default in ordinary Work execution:

```text
FULL LEVEL1 REREAD
OWNER-FACING REPORT GATE
FRESH EXTERNAL RESEARCH REDO
RELEASE AUTHORIZATION REDO
MAIN CHAT FAILURE-HISTORY REVIEW
```

## 4. Mandatory Main Chat pre-action checklist

Before preparation / research / Work handoff / Bridge release / QA / acceptance / publication / cursor movement:

```text
[ ] current remote HEAD fetched
[ ] Main Chat 00 gate read
[ ] COMMON_RULES / inherited applicable authority read
[ ] applicable owner-locked Level1 rules read
[ ] current Level2 step/gates read
[ ] current JOB_FLOW + cursor read
[ ] relevant job incident/failure records read
[ ] owner-facing report gate read when required
[ ] Work handoff rule read when Work is applicable
[ ] provider gate read when provider execution is applicable
[ ] generalization/layer-separation gate read before permanent-method mutation
[ ] current external-method research requirement evaluated
[ ] no unresolved authority conflict
```

If incomplete:

```text
MAIN_CHAT_EXECUTION_ALLOWED = false
```

## 5. Mandatory Main Chat post-action / acceptance checklist

Before acceptance/cursor advance:

```text
[ ] applicable acceptance rules reread
[ ] actual Work/provider/result artifacts fetched
[ ] remote/provider readback completed where required
[ ] counts/joins/provenance checked
[ ] HOLD/ERROR/UNRESOLVED checked
[ ] staging cleanup checked when applicable
[ ] owner-facing result report complete
[ ] plain-language conclusion complete
[ ] next physical action stated
```

## 6. Marker

```text
KW002_RECURRING_MAIN_CHAT_RULE_FAILURE_PATTERN_RECOGNIZED = true
KW002_MAIN_CHAT_RULE_MEMORY_RELIANCE_FORBIDDEN = true
KW002_MAIN_CHAT_REREAD_CHECKLIST_REQUIRED = true
KW002_CHAT_SOURCE_DISCLOSURE_IS_MAIN_CHAT_GATE = true
KW002_PLAIN_LANGUAGE_OWNER_REPORT_IS_MAIN_CHAT_GATE = true
KW002_WORK_TRIGGER_CURRENT_EXECUTION_UNIT_CHECK_REQUIRED = true
KW002_OWNER_REPOSITORY_ROUTING_FORBIDDEN = true
KW002_MAIN_GOVERNANCE_MUST_NOT_BE_DUPLICATED_IN_WORK = true
KW002_WORK_RUNTIME_EXCLUDED_FROM_FULL_RULE_REREAD_CHECKLIST = true
```
