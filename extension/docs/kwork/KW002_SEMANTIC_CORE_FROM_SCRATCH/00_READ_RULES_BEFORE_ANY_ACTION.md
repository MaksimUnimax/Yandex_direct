# KW-002 — 00 MAIN CHAT READ RULES BEFORE ANY ACTION

Status: **ACTIVE / OWNER-LOCKED / FAIL-CLOSED / MAIN-CHAT-ONLY**  
Scope correction: **2026-09-17 — THIS GUARD IS FOR MAIN CHAT / ARCHITECT / REVIEWER / ACCEPTANCE CONTROL, NOT FOR CHATGPT WORK RUNTIME.**

## 1. Scope

This guard exists because Main Chat repeatedly violated explicit project rules when relying on memory, summaries or prior chat state instead of freshly reading the current live authorities.

```text
MAIN CHAT MEMORY != RULE AUTHORITY
MAIN CHAT SUMMARY != RULE READBACK
MAIN CHAT FAMILIARITY != EXECUTION PERMISSION
```

Before Main Chat prepares, researches, releases, reviews, accepts, publishes or advances a major KW-002 step, it must follow:

`LEVEL1/00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE.md`

## 2. Explicit Work exclusion

**THIS FILE IS NOT A RUNTIME CHECKLIST FOR CHATGPT WORK.**

Once Main Chat has completed the project/research/release gates and issued a canonical Work execution prompt:

```text
WORK
= EXECUTE THE FROZEN TASK CONTRACT
!= REPEAT MAIN CHAT GOVERNANCE
```

Do NOT require Work to repeat:

- the full Level1 rule reread;
- fresh external methodology research already completed by Main Chat;
- owner-facing source disclosure;
- owner-facing plain-language report;
- roadmap/release authorization;
- Main Chat failure-ledger review;
- the decision whether the already released step should exist or run.

Work may perform only the **narrow execution-safety preflight explicitly written in its prompt**, normally:

```text
FETCH CURRENT REMOTE HEAD
→ VERIFY RELEASE MARKER / PROMPT IDENTITY
→ VERIFY NAMED INPUTS / MANIFEST / SCHEMA / HASHES
→ IF MATERIAL AUTHORITY DRIFT: STOP AND REPORT AUTHORITY_DRIFT
→ OTHERWISE EXECUTE THE TASK
```

## 3. Main Chat hard stop

```text
MAIN CHAT HAS NOT FRESHLY READ APPLICABLE RULES
→ NO PREPARATION
→ NO RESEARCH RELEASE
→ NO WORK PROMPT AUTHORING / RELAY
→ NO BRIDGE / PROVIDER RELEASE
→ NO QA ACCEPTANCE
→ NO CURSOR / ROADMAP ADVANCE
```

Before every major owner-facing report, Main Chat must also read and obey:

`LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`

The owner-facing chat must contain the required clickable source disclosure and real plain-Russian conclusion when that rule applies.

## 4. Permanent distinction

```text
MAIN CHAT GOVERNANCE GATES
!=
WORK EXECUTION INSTRUCTIONS
```

The canonical Work prompt must contain the task, inputs, outputs, execution boundaries, QA and a bounded drift check — not a duplicate of Main Chat's governance process.
