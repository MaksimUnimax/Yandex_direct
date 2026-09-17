# KW-002 — 00 MAIN CHAT READ RULES BEFORE AUTHORIZING ANY LEVEL2 STEP

Status: **ACTIVE / OWNER-LOCKED / FAIL-CLOSED / MAIN-CHAT-ONLY**

## Scope

This file is a **Main Chat / architect pre-entry guard** for Level2 work.

```text
THIS GUARD = MAIN CHAT GOVERNANCE
THIS GUARD != CHATGPT WORK RUNTIME INSTRUCTION
```

Before Main Chat prepares, releases, changes, reviews or accepts a Level2 roadmap step, it must first read the current Main Chat gate:

`../LEVEL1/00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE.md`

and the applicable current Level1/Level2/job authorities.

Known recurring failure:

```text
MAIN CHAT ACTS FROM MEMORY
→ MISSES AN EXISTING RULE
→ OWNER HAS TO CORRECT IT
```

Hard stop for Main Chat:

```text
APPLICABLE RULES NOT FRESHLY READ
→ NO STEP PREPARATION
→ NO WORK PROMPT AUTHORING / RELEASE
→ NO PROVIDER RELEASE
→ NO STEP ACCEPTANCE
→ NO CURSOR ADVANCE
```

## Explicit Work exclusion

After Main Chat has already authorized a step and produced its canonical Work prompt, **ChatGPT Work does not reread this guard or repeat the Main Chat Level1/Level2 governance cycle.**

Work executes the released prompt.

The Work prompt may require a bounded technical preflight only:

```text
FETCH CURRENT HEAD
→ VERIFY RELEASE / INPUT / SCHEMA IDENTITY
→ MATERIAL DRIFT? STOP
→ OTHERWISE EXECUTE
```

Do not put fresh external research, owner-facing source disclosure, plain-language report or release authorization back onto Work unless the Work task itself is explicitly a methodology/review task.
