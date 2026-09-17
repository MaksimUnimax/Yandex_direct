# BLOOD_SAND_GREENFIELD_2026-09-08 — 00 MAIN CHAT READ RULES BEFORE ANY JOB ACTION

Status: **ACTIVE / OWNER-LOCKED / FAIL-CLOSED / MAIN-CHAT-ONLY**

## Scope

This guard exists because **Main Chat** repeatedly violated explicit KW-002 rules by relying on memory, summaries or prior chat state instead of rereading current live authority.

This guard applies to Main Chat / architect / reviewer / acceptance / repository-control actions for this job.

**IT DOES NOT APPLY AS A RUNTIME CHECKLIST TO CHATGPT WORK.**

Before Main Chat performs any material job action:

```text
1. FETCH CURRENT LIVE REMOTE BRANCH
2. READ THE CURRENT MAIN-CHAT 00 GATE
3. READ applicable current Level1/Level2 authorities
4. READ current JOB_FLOW + cursor + accepted manifests/evidence
5. READ relevant job incident/failure records
6. VERIFY owner-facing report requirements when applicable
7. only then perform Main Chat governance/release/acceptance work
```

Hard stop for Main Chat:

```text
MAIN CHAT RULE/JOB AUTHORITY NOT FRESHLY READ
→ NO PREPARATION
→ NO WORK PROMPT AUTHORING / RELEASE
→ NO BRIDGE / PROVIDER RELEASE
→ NO ACCEPTANCE
→ NO PUBLICATION ACCEPTANCE
→ NO CURSOR / ROADMAP ADVANCE
```

## Work runtime boundary

Once Main Chat has released a concrete Work prompt:

```text
CHATGPT WORK
→ EXECUTES THAT PROMPT
→ DOES NOT REPEAT MAIN CHAT'S GOVERNANCE CYCLE
```

Work does not need to read this guard, the full Level1 set, the Main Chat failure incident, fresh external research or owner-facing reporting rules unless the actual Work task explicitly concerns methodology/rule auditing.

For ordinary Step execution, Work may do only the bounded technical preflight written in the canonical prompt:

```text
CURRENT HEAD
+ RELEASE MARKER
+ INPUT / MANIFEST / SCHEMA IDENTITY
→ MATERIAL DRIFT? STOP
→ OTHERWISE EXECUTE
```

Main Chat retains responsibility for post-Work readback, QA, acceptance, owner-facing explanation and cursor movement.
