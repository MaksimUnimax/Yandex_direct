# KW-002 — 00 MAIN CHAT READ RULES BEFORE ANY JOB ACTION

Status: **ACTIVE / OWNER-LOCKED / FAIL-CLOSED / MAIN-CHAT-ONLY**

## Scope

This guard applies when **Main Chat / architect / reviewer / acceptance controller** enters or modifies `work/<JOB_ID>/` state.

It is **not** a runtime instruction for ChatGPT Work merely because Work operates on files under `work/`.

Before Main Chat prepares, releases, reviews, accepts, publishes or advances a concrete job action, read the current Main Chat gate beginning with:

`../LEVEL1/00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE.md`

Then read the applicable Level1/Level2 rules, current job `JOB_FLOW.md`, current cursor, accepted manifests/evidence and job incident/failure records.

```text
MAIN CHAT MEMORY != CURRENT JOB AUTHORITY
```

Hard stop for Main Chat:

```text
NO FRESH APPLICABLE RULE/JOB READ
→ NO JOB PREPARATION
→ NO WORK HANDOFF AUTHORING / RELEASE
→ NO PROVIDER RELEASE
→ NO PUBLICATION ACCEPTANCE
→ NO CURSOR MOVEMENT
```

## Explicit Work exclusion

```text
THIS work/ GUARD
!= WORK RUNTIME GATE
```

Once Main Chat has released a concrete Work prompt, Work executes that prompt and reads only the specific data/method/input files named there as necessary for execution.

Do NOT require Work to repeat:

- the full Level1 rule set;
- Main Chat's owner-facing report gate;
- Main Chat's fresh external research;
- Main Chat's release authorization;
- Main Chat's failure-history review.

Work may perform only a bounded current-HEAD / release / input / manifest / schema drift check if the execution prompt requires it.
