# KW-002 — 00 READ RULES BEFORE ANY ACTION

Status: **ACTIVE / OWNER-LOCKED / FAIL-CLOSED / READ FIRST**

**DO NOT START OR CONTINUE ANY MATERIAL KW-002 ACTION BEFORE READING THE CURRENT LIVE RULES IN FULL.**

Canonical hard gate:

`LEVEL1/00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE.md`

Known recurring failure that this guard exists to prevent:

```text
The assistant has repeatedly violated explicit project rules when relying on memory, summaries or prior chat state instead of freshly reading the current live rules in full.
```

Therefore:

```text
MEMORY != AUTHORITY
SUMMARY != RULE READBACK
FAMILIARITY != EXECUTION PERMISSION

NO FULL RULE REREAD
→ NO PREPARATION
→ NO WORK PROMPT
→ NO WORK EXECUTION
→ NO BRIDGE / PROVIDER ACTION
→ NO ANALYSIS
→ NO FILE MUTATION
→ NO QA ACCEPTANCE
→ NO CURSOR / ROADMAP ADVANCE
```

Before every major owner-facing report, also read in full:

`LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`

The chat report must include clickable studied-source links with what each supports, source→method trace, and a real plain-Russian `ПРОСТЫМИ СЛОВАМИ` conclusion. Having those links only inside an artifact does not satisfy the chat-disclosure gate.

If this guard has not been satisfied, stop and set `EXECUTION_ALLOWED = false`.
