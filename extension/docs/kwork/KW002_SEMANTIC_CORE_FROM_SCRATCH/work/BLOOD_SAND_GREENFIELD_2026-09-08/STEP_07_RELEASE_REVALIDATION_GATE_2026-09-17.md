# KW-002 / BLOOD & SAND — STEP07 RELEASE REVALIDATION GATE

Status: **ACTIVE / REQUIRED BEFORE ACTUAL STEP07 WORK RELAY**  
Date: 2026-09-17

## 1. Why this gate exists

`STEP07_PREPARATION` was technically accepted before the new owner-locked full-rule reread / no-action authority was added.

The preparation artifacts remain valid frozen preparation evidence, but the actual Step07 Work prompt was prepared against an older remote authority state. Current Level1 rules now include stronger process gates for full rule reread, recurring assistant-rule failure control, owner-facing source disclosure and rule-mutation discipline.

Per `WORK_BASE_FRESHNESS_AND_AUTHORITY_DRIFT_RULE.md`:

```text
NEWER METHOD / EXECUTION AUTHORITY
>
OLDER PREPARED WORK CONTRACT
```

Therefore the existing Step07 Work prompt MUST NOT be relayed/executed as-is without current-authority reconciliation.

## 2. Hard entry gate before actual Step07

Before Main Chat may relay `STEP_07_COMPETITOR_SEMANTIC_EXPANSION_WORK_PROMPT.md`:

```text
1. FETCH CURRENT LIVE REMOTE HEAD
2. READ IN FULL LEVEL1/00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE.md
3. READ IN FULL LEVEL1/01_RECURRING_ASSISTANT_RULE_FAILURES_ANTI_REGRESSION_CHECKLIST.md
4. READ IN FULL all applicable current cross-Kwork + Level1 rules
5. READ IN FULL current STEP_RULES_INDEX + STEP_07_COMPETITOR_SEMANTIC_EXPANSION.md
6. READ IN FULL current JOB_FLOW + execution cursor
7. READ IN FULL KW002_RULE_COMPLIANCE_FAILURE_INCIDENT_2026-09-17.md
8. READ IN FULL current Step07 preparation manifest/schema/prompt/QA
9. classify remote authority drift since the preparation base
10. reconcile or amend the Step07 Work prompt if current rules require changes
11. perform fresh Step07 pre-step external research/freshness check required by PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md
12. show the complete owner-facing pre-step report in chat
13. show clickable source links + what each supports + source→method trace directly in chat
14. end with real plain-Russian WHY / WHAT / RESULT / BLOCKER / NEXT ACTION
15. only after all gates pass may Main Chat mark STEP07_EXECUTION_ALLOWED=true and give the owner the current canonical Work prompt to relay
```

## 3. Mandatory rule-read ledger

The Step07 release record must explicitly show:

```text
LIVE_REMOTE_HEAD
CURRENT_ACTION = ACTUAL_STEP07_RELEASE_REVALIDATION
RULES_READ_IN_FULL
JOB_STATE_READ
FAILURE_LEDGER_READ = true
OWNER_REPORT_GATE_READ = true
WORK_GATE_READ = true
WORK_BASE_FRESHNESS_RULE_READ = true
PROVIDER_GATE_READ = NOT_APPLICABLE_FOR_STEP07
UNRESOLVED_AUTHORITY_CONFLICTS
WORK_PROMPT_RECONCILED_TO_CURRENT_AUTHORITY = true|false
FRESH_EXTERNAL_RESEARCH = PASS|FAIL
SOURCE_DISCLOSURE_IN_CHAT = PASS|FAIL
PLAIN_LANGUAGE_SUMMARY = PASS|FAIL
STEP07_EXECUTION_ALLOWED = true|false
```

## 4. Owner-facing report is a hard gate

Before actual Step07 Work execution, the chat itself must contain:

```text
WHOLE KWORK GOAL
FULL ROADMAP
COMPLETED
REMAINING
CURRENT STEP GOAL
WHAT PROBLEM STEP07 SOLVES
REQUIRED OUTPUT
RELEVANT PRIOR ERRORS
NON-REPEAT CONTROLS
FRESH INTERNET RESEARCH
CLICKABLE SOURCE LIST
WHAT EACH SOURCE SUPPORTS
HOW EACH SOURCE AFFECTS / CONFIRMS THE STEP07 METHOD
SOURCE LIMITATIONS
SOURCE→METHOD TRACE
EXECUTION PLAN
WORK GATE
PASS CONDITIONS
ПРОСТЫМИ СЛОВАМИ
```

Artifact-only source links do not satisfy this gate.

## 5. Step07 remains unexecuted

This release gate does not perform competitor extraction.

```text
STEP07_PREPARATION = ACCEPTED
STEP07_RELEASE_REVALIDATION = REQUIRED
STEP07 = NOT_STARTED
STEP08 = NOT_STARTED
```

## 6. PASS

Actual Step07 may be released only if:

```text
CURRENT_RULE_AUTHORITY = PASS
FULL_RULE_REREAD = PASS
RECURRENT_FAILURE_CONTROLS = PASS
WORK_PROMPT_CURRENT_AUTHORITY_RECONCILIATION = PASS
FRESH_EXTERNAL_RESEARCH = PASS
SOURCE_DISCLOSURE_IN_CHAT = PASS
PLAIN_LANGUAGE_SUMMARY = PASS
UNRESOLVED_AUTHORITY_CONFLICTS = 0
STEP07_EXECUTION_ALLOWED = true
```

Until then:

```text
DO NOT RELAY ACTUAL STEP07 WORK PROMPT
DO NOT START STEP07 CRAWL / EXTRACTION
```
