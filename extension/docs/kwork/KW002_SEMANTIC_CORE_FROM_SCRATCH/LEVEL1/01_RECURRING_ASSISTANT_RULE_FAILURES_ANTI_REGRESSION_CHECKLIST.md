# KW-002 — RECURRING ASSISTANT RULE FAILURES / ANTI-REGRESSION CHECKLIST

Status: **ACTIVE / OWNER-LOCKED / MANDATORY BEFORE EVERY MATERIAL ACTION**  
Owner lock: 2026-09-17

This checklist exists because the same class of assistant failure has repeated after rules already existed.

## Known recurring failure pattern

```text
RULE EXISTS
→ ASSISTANT DOES NOT FRESHLY READ IT IN FULL
→ ASSISTANT WORKS FROM MEMORY / SUMMARY
→ ASSISTANT PRODUCES A PLAUSIBLE BUT NON-COMPLIANT RESULT
→ OWNER HAS TO POINT TO THE EXISTING RULE
→ ASSISTANT PATCHES AFTER THE FACT
```

This pattern is itself now a named blocking defect.

Before any material action, the executor must prove that it is not repeating this pattern.

## Repeated failures already observed

### F-RULE-01 — acting from remembered project rules

Observed behavior: assistant used memory/summary instead of rereading the current live owner-locked rules.

Permanent control:

```text
READ CURRENT LIVE APPLICABLE RULES IN FULL BEFORE ACTION
MEMORY DOES NOT COUNT
```

### F-RULE-02 — incomplete owner-facing pre-step report

Observed behavior: technical preparation/status was reported without the full mandatory owner-facing structure.

Permanent control:

Read `PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md` in full before drafting the report.

The report must include goal, roadmap, completed/remaining, current-step purpose, prior failures/non-repeat controls, fresh research, source links, source→method trace, method, gate, PASS conditions and plain-language conclusion.

### F-RULE-03 — external materials existed in artifact but were not shown in chat

Observed behavior: source URLs were preserved inside a methodology-audit artifact, but the owner-facing chat omitted them.

Permanent control:

```text
ARTIFACT SOURCE LIST != CHAT SOURCE DISCLOSURE
```

The chat itself must contain clickable source links plus what each source supports, how it affects the method and its limitation.

### F-RULE-04 — status/hash dump substituted for plain-language summary

Observed behavior: technical statuses, hashes, filenames and QA markers were used where normal Russian explanation was mandatory.

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

### F-RULE-05 — wrong Work boundary

Observed behavior: assistant initially treated actual Step07 as the Work unit while failing to recognize that Step07 preparation itself met the LARGE DATA trigger.

Permanent control:

Evaluate Work trigger for the **current execution unit itself**, including preparation/reconciliation work.

```text
LARGE DATA → COMPLETE UNIT TO WORK
NO SAMPLING / NO TRUNCATION
```

### F-RULE-06 — owner asked to route handoff files manually

Observed behavior: assistant initially gave multiple GitHub target folders and expected owner to sort files.

Permanent control:

```text
ONE HANDOFF
→ ONE OWNER STAGING UPLOAD
→ EXECUTOR DOES FINAL PATH ROUTING
→ EXECUTOR CLEANS STAGING
→ REMOTE READBACK
```

Owner does not route NEW/REPLACE files among Level1/Level2/job directories.

### F-RULE-07 — preparation acceptance reported before full owner-facing disclosure

Observed behavior: technical preparation QA and remote publication were correct, but the required owner-facing source disclosure/plain-language report was incomplete.

Permanent control:

Technical artifact PASS and chat-report PASS are separate gates. A technically valid package does not waive owner-facing reporting requirements.

### F-RULE-08 — explaining the failure instead of immediately applying the controlling rule

Observed behavior: assistant narrated consequences/causes instead of first reopening the actual live rule and executing the required correction.

Permanent control:

```text
OWNER POINTS TO RULE FAILURE
→ FETCH LIVE RULE
→ READ IN FULL
→ APPLY RULE
→ THEN EXPLAIN CONCISELY
```

## Mandatory pre-action checklist

Before every preparation / execution / Work handoff / Bridge action / QA / acceptance / cursor movement:

```text
[ ] current remote HEAD fetched
[ ] 00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE read in full
[ ] COMMON_RULES read in full
[ ] applicable owner-locked Level1 rules read in full
[ ] current Level2 step/gates read in full
[ ] current JOB_FLOW + cursor read in full
[ ] relevant failure ledger/checklist read in full
[ ] owner-facing report gate read in full
[ ] Work gate read in full if applicable
[ ] provider/Bridge gate read in full if applicable
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
```
