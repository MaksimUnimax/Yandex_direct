# KW-002 / BLOOD & SAND — STEP07 MAIN CHAT RELEASE REVALIDATION GATE

Status: **ACTIVE / MAIN-CHAT-ONLY / REQUIRED BEFORE ACTUAL STEP07 WORK RELAY**  
Date: 2026-09-17  
Scope correction: **THIS GATE IS FOR MAIN CHAT. CHATGPT WORK MUST NOT REPEAT IT.**

## 1. Purpose

This gate exists so **Main Chat** verifies that a prepared Step07 execution contract is still current before giving it to Work.

```text
NEWER METHOD / EXECUTION AUTHORITY
>
OLDER PREPARED WORK CONTRACT
```

Main Chat owns the reconciliation.

## 2. Main Chat hard gate before relay

Before Main Chat may relay the actual Step07 Work prompt, Main Chat must:

```text
1. FETCH CURRENT LIVE REMOTE HEAD
2. READ current applicable Main Chat governance/rule authorities
3. READ current STEP_RULES_INDEX + Step07 Level2 method
4. READ current JOB_FLOW + cursor + job incident records
5. READ current Step07 preparation manifest/schema/prompt/QA
6. classify authority drift since preparation
7. reconcile/amend the Work prompt if required
8. perform the fresh external-method research/freshness check required for Step07
9. show the required owner-facing pre-step report in chat
10. show clickable sources + supported claims + source→method trace
11. give the real plain-Russian WHY / WHAT / RESULT / BLOCKER / NEXT ACTION conclusion
12. only then mark STEP07_EXECUTION_ALLOWED=true
13. relay the canonical prompt to Work
```

## 3. Explicit Work exclusion

```text
THIS RELEASE GATE
= MAIN CHAT PRE-RELAY CONTROL
!= WORK RUNTIME TASK
```

Once this gate has PASS and the canonical prompt is released, Work MUST NOT:

- rerun this release gate;
- reread the full project rule stack for governance purposes;
- rerun fresh external research already completed here;
- repeat owner-facing source disclosure;
- repeat the owner-facing plain-language report;
- decide again whether Main Chat was allowed to release Step07.

Work performs only the bounded technical startup check contained in the released prompt:

```text
FETCH CURRENT HEAD
→ VERIFY RELEASE RECORD / PROMPT IDENTITY
→ VERIFY NAMED INPUT / MANIFEST / SCHEMA / HASHES
→ MATERIAL DRIFT? STOP + REPORT AUTHORITY_DRIFT
→ OTHERWISE EXECUTE STEP07
```

## 4. Main Chat release record

The release record must show at minimum:

```text
LIVE_REMOTE_HEAD
CURRENT_ACTION = ACTUAL_STEP07_RELEASE_REVALIDATION
MAIN_CHAT_RULES_READ
JOB_STATE_READ
FAILURE_LEDGER_READ
OWNER_REPORT_GATE_READ
WORK_HANDOFF_RULE_READ
UNRESOLVED_AUTHORITY_CONFLICTS
WORK_PROMPT_RECONCILED_TO_CURRENT_AUTHORITY
FRESH_EXTERNAL_RESEARCH
SOURCE_DISCLOSURE_IN_CHAT
PLAIN_LANGUAGE_SUMMARY
STEP07_EXECUTION_ALLOWED
```

This is a **Main Chat release record**, not a file Work must recreate.

## 5. PASS

Actual Step07 may be relayed only if Main Chat establishes:

```text
CURRENT_RULE_AUTHORITY = PASS
MAIN_CHAT_FULL_RULE_REREAD = PASS
RECURRENT_MAIN_CHAT_FAILURE_CONTROLS = PASS
WORK_PROMPT_CURRENT_AUTHORITY_RECONCILIATION = PASS
FRESH_EXTERNAL_RESEARCH = PASS
SOURCE_DISCLOSURE_IN_CHAT = PASS
PLAIN_LANGUAGE_SUMMARY = PASS
UNRESOLVED_AUTHORITY_CONFLICTS = 0
STEP07_EXECUTION_ALLOWED = true
```

After PASS:

```text
MAIN CHAT RELEASES PROMPT
→ WORK EXECUTES PROMPT
```

Do not insert this release gate back into the Work prompt.
