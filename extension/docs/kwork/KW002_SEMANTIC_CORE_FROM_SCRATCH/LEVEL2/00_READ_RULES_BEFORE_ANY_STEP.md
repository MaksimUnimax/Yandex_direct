# KW-002 — 00 READ THIS FIRST BEFORE ANY LEVEL2 STEP

Status: **ACTIVE / OWNER-LOCKED / FAIL-CLOSED**

Before reading or executing ANY Level2 step, first read in full:

`../LEVEL1/00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE.md`

Then read all applicable current live Level1 rules, the current Level2 step rule/gates, current job flow/cursor/evidence, and relevant failure ledger.

Known recurring assistant failure:

```text
The assistant has repeatedly violated explicit KW-002 rules by acting from remembered rules instead of rereading the current live authorities in full.
```

Hard stop:

```text
RULES NOT FRESHLY READ IN FULL
→ EXECUTION_ALLOWED = false
→ NO STEP PREPARATION
→ NO STEP EXECUTION
→ NO WORK PROMPT / WORK EXECUTION
→ NO PROVIDER ACTION
→ NO ACCEPTANCE / CURSOR ADVANCE
```

Before a major owner-facing pre-step report also read `../LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md` in full and show clickable external source links + what each supports + source→method trace + a real plain-Russian `ПРОСТЫМИ СЛОВАМИ` block in chat.
