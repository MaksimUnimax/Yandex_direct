# KW-002 — 00 MANDATORY FULL RULE REREAD / NO-ACTION GATE

Status: **ACTIVE / OWNER-LOCKED / FAIL-CLOSED / READ FIRST**  
Owner lock: 2026-09-17

## 0. Why this rule exists

A recurring assistant failure has been observed across KW-002 execution: the assistant has repeatedly relied on remembered rules, summaries, prior chat state or technical artifacts instead of freshly reading the controlling rules in full. That has caused repeated process violations, including incomplete owner-facing reports, missing clickable source disclosure, missing plain-language conclusions, incorrect Work handoff behavior and premature status/acceptance claims.

Therefore:

```text
ASSISTANT MEMORY != RULE READBACK
PRIOR CHAT SUMMARY != RULE READBACK
PAST COMPLIANCE != CURRENT COMPLIANCE
FAMILIARITY WITH THE PROJECT != AUTHORIZATION TO ACT
```

This is a permanent anti-regression rule. The assistant/executor must be treated as unreliable with respect to rule recall unless the current live rules have been freshly read in full for the current action boundary.

## 1. Absolute no-action gate

Before **ANY material KW-002 action**, including preparation, planning, research, Work prompt drafting, Work execution, Bridge/provider work, analysis, file/rule mutation, QA, acceptance, publication, cursor movement, roadmap movement or owner-facing major report:

```text
STOP
→ FETCH CURRENT LIVE REMOTE BRANCH
→ IDENTIFY CURRENT ACTION / STEP / SUBSTEP
→ IDENTIFY ALL APPLICABLE CROSS-KWORK + LEVEL1 + LEVEL2 + JOB-SPECIFIC AUTHORITIES
→ READ EVERY APPLICABLE RULE IN FULL FROM THE CURRENT LIVE BRANCH
→ READ CURRENT JOB FLOW / CURSOR / ACCEPTED INPUT AUTHORITIES WHEN A CONCRETE JOB IS INVOLVED
→ READ RELEVANT FAILURE LEDGER / ANTI-REGRESSION CONTROLS
→ EXPLICITLY VERIFY OWNER-FACING REPORT REQUIREMENTS
→ ONLY THEN MAY ANY MATERIAL ACTION START
```

Hard prohibition:

```text
IF APPLICABLE RULES HAVE NOT BEEN FRESHLY READ IN FULL
THEN
NO PREPARATION
NO ANALYSIS
NO EXTERNAL RESEARCH EXECUTION
NO WORK PROMPT
NO WORK EXECUTION
NO BRIDGE COMMAND
NO PROVIDER CALL
NO FILE OR RULE MUTATION
NO QA ACCEPTANCE
NO CURSOR UPDATE
NO ROADMAP ADVANCE
NO CLAIM THAT THE STEP IS READY
```

There is no exception for urgency, familiarity, prior work, previous summaries, limited context or confidence.

## 2. "Read in full" means read in full

Forbidden shortcuts:

```text
FILE NAME SEEN != FILE READ
SEARCH SNIPPET != FILE READ
FIRST LINES != FILE READ
SUMMARY != FILE READ
MEMORY != FILE READ
OLD COPY != CURRENT LIVE RULE
RELATED RULE != THE ACTUAL RULE
```

If a rule is long, continue reading until its end. If a remembered filename changed, resolve the current live equivalent through repository tree/search/backlinks before acting.

## 3. Mandatory rule-read ledger in the chat/work record

Before a major step/substep or other material execution unit starts, record at minimum:

```text
LIVE_REMOTE_HEAD
CURRENT_ACTION
RULES_READ_IN_FULL = [exact current paths]
JOB_STATE_READ = [exact current paths] when applicable
FAILURE_LEDGER_READ = true/false
OWNER_REPORT_GATE_READ = true/false
WORK_GATE_READ = true/false when applicable
PROVIDER_GATE_READ = true/false when applicable
GENERALIZATION_GATE_READ = true/false before permanent-method mutation
UNRESOLVED_AUTHORITY_CONFLICTS
EXECUTION_ALLOWED = true/false
```

`EXECUTION_ALLOWED=true` is forbidden unless the full-read gate above is complete.

## 4. Owner-facing report gate is mandatory before execution

For every major roadmap step, preparation pass or materially new execution unit, the assistant must freshly read and obey:

`PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`

The owner-facing pre-step report must include, in a complete equivalent structure:

```text
WHOLE KWORK GOAL
FULL ROADMAP
COMPLETED
REMAINING
CURRENT STEP GOAL
WHAT PROBLEM THE STEP SOLVES
REQUIRED OUTPUT
RELEVANT PRIOR ERRORS
NON-REPEAT CONTROLS
FRESH INTERNET RESEARCH
ИСТОЧНИКИ / МАТЕРИАЛЫ, КОТОРЫЕ Я ИЗУЧИЛ ПЕРЕД ШАГОМ
CLICKABLE SOURCE TITLE + PUBLISHER + URL
WHAT EACH SOURCE SUPPORTS
HOW IT CHANGES / CONFIRMS THE METHOD
LIMITATION / WHAT IT DOES NOT PROVE
SOURCE→METHOD TRACE
METHOD / EXECUTION PLAN
BRIDGE / WORK GATE WHEN APPLICABLE
PASS CONDITIONS
ПРОСТЫМИ СЛОВАМИ
```

The `ПРОСТЫМИ СЛОВАМИ` block must explain in normal Russian:

1. зачем нужен шаг / какую проблему решаем;
2. что конкретно сделали или будем делать;
3. что получим и зачем это нужно дальше;
4. можно ли уже продолжать;
5. если нельзя — что мешает;
6. следующее физическое действие.

For a prepared-but-not-executed step it must explicitly say that preparation is complete while actual data processing has not started.

## 5. Source disclosure cannot be delegated to an artifact

Hard rule:

```text
SOURCE LINKS EXIST IN MD/ZIP/WORK OUTPUT
!= OWNER-FACING SOURCE DISCLOSURE IN CHAT
```

The assistant must show clickable source links and source→method explanation directly in the owner-facing chat before execution when the pre-step rule requires them.

A file path, source name without URL, or statement that "research was done" does not pass.

## 6. Work does not bypass this gate

Before writing or relaying any Work execution unit:

```text
FULL RULE REREAD = REQUIRED
PRE-STEP OWNER REPORT = REQUIRED WHEN APPLICABLE
WORK_HANDOFF_RULE = READ IN FULL
PRE-HANDOFF MANIFEST = FROZEN
```

Work itself must also start by fetching the current branch and reading the current applicable rules in full.

Large-data delegation does not authorize Main Chat to skip the owner-facing pre-step report.

## 7. Bridge/provider work does not bypass this gate

Before any Bridge/provider action, read the current provider/Bridge execution authorities in full in addition to this rule.

```text
PRINTED COMMAND != EXECUTED COMMAND
PAST PROVIDER CONTRACT != CURRENT PROVIDER CONTRACT
```

No provider action may start merely because a command is already known from an earlier turn.

## 8. Permanent method/rule mutation does not bypass this gate

Before creating or changing any permanent Level1/Level2 rule, read in full:

- `ROADMAP_AND_METHOD_GENERALIZATION_RULE.md`;
- `JOB_DATA_SEPARATION_AND_LIFECYCLE.md`;
- relevant failure-ledger authorities;
- the current rule being changed.

Concrete job incidents must remain in `work/<JOB_ID>/`. Level1/Level2 may contain only the generalized mechanism/control that can execute on unrelated sites.

```text
JOB INCIDENT != UNIVERSAL RULE BODY
```

Owner authorization to change a rule does not waive the layer-separation/generalization QA.

## 9. Post-execution / acceptance gate

Before accepting Work/Bridge/manual output or moving the cursor:

```text
REREAD APPLICABLE ACCEPTANCE RULES IN FULL
→ VERIFY ACTUAL REMOTE / PROVIDER RESULT
→ VERIFY COUNTS / JOINS / PROVENANCE / HOLD / ERROR / UNRESOLVED
→ VERIFY OWNER-FACING RESULT REPORT REQUIREMENTS
→ PROVIDE PLAIN-LANGUAGE CONCLUSION
→ ONLY THEN ACCEPT / ADVANCE
```

A technically correct artifact does not excuse a failed owner-facing reporting gate.

## 10. Fail-closed behavior

If full-rule readback cannot be completed or authority is unresolved:

```text
EXECUTION_ALLOWED = false
STATUS = BLOCKED_ON_RULE_AUTHORITY / RULE_READBACK
```

Do not replace rule reading with best-effort memory.

## 11. Anti-regression statement that must remain visible

```text
KNOWN_RECURRING_FAILURE:
The assistant has repeatedly violated explicit KW-002 rules when acting from memory instead of rereading current live rules.

PERMANENT_CONTROL:
Never trust remembered project rules as sufficient authority. Read the current applicable rules in full before every material action and again before acceptance/cursor movement.
```

This statement is intentionally repetitive. Its purpose is to prevent the same failure mode from being rationalized away in later chats.

## 12. Mandatory authorities to include when applicable

At minimum consider and read in full:

```text
applicable cross-Kwork owner-locked rules
LEVEL1/00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE.md
LEVEL1/01_RECURRING_ASSISTANT_RULE_FAILURES_ANTI_REGRESSION_CHECKLIST.md
LEVEL1/COMMON_RULES.md
LEVEL1/INHERITED_KW001_UNIVERSAL_RULES.md
LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md
LEVEL1/RESULT_QUALITY_SCORING_RULE.md
LEVEL1/METHOD_SOURCE_AND_EVIDENCE_RULES.md
LEVEL1/JOB_DATA_SEPARATION_AND_LIFECYCLE.md
LEVEL1/ROADMAP_AND_METHOD_GENERALIZATION_RULE.md before permanent-method mutation
LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md
LEVEL1/WORK_HANDOFF_RULE.md when Work/large-data risk applies
LEVEL1/YANDEX_MARKETING_BRIDGE_EXECUTION_RULE.md when Bridge/provider work applies
../../KWORK_LARGE_ARTIFACT_OWNER_RELAY_AND_PUBLICATION_RULE.md when material artifact handoff/publication applies
current LEVEL2 step rule / gate
current STEP_RULES_INDEX.md
current work/<JOB_ID>/JOB_FLOW.md
current cursor / accepted manifests / evidence authorities
current job-specific failure/incident ledger when one exists
```

This is a floor, not an exhaustive list. The current action may require additional rules.

## 13. Markers

```text
KW002_FULL_RULE_REREAD_BEFORE_ANY_MATERIAL_ACTION_REQUIRED = true
KW002_ASSISTANT_MEMORY_NOT_RULE_AUTHORITY = true
KW002_NO_ACTION_BEFORE_FULL_RULE_READ = true
KW002_NO_WORK_PROMPT_BEFORE_FULL_RULE_READ = true
KW002_NO_WORK_EXECUTION_BEFORE_FULL_RULE_READ = true
KW002_NO_PROVIDER_ACTION_BEFORE_FULL_RULE_READ = true
KW002_NO_FILE_OR_RULE_MUTATION_BEFORE_FULL_RULE_READ = true
KW002_NO_ACCEPTANCE_BEFORE_ACCEPTANCE_RULE_REREAD = true
KW002_NO_CURSOR_ADVANCE_BEFORE_RULE_COMPLIANCE = true
KW002_OWNER_FACING_SOURCE_LINKS_MUST_BE_IN_CHAT = true
KW002_OWNER_FACING_PLAIN_LANGUAGE_SUMMARY_MUST_BE_IN_CHAT = true
KW002_MISSING_OWNER_REPORT_GATE_BLOCKS_EXECUTION = true
KW002_KNOWN_RECURRING_ASSISTANT_RULE_NONCOMPLIANCE_GUARD = true
KW002_PERMANENT_METHOD_GENERALIZATION_GATE_REQUIRED = true
KW002_FAIL_CLOSED_ON_RULE_READBACK = true
```
