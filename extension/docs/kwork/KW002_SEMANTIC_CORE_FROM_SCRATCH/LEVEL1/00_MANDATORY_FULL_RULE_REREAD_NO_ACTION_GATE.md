# KW-002 — 00 MANDATORY MAIN-CHAT FULL RULE REREAD / NO-ACTION GATE

Status: **ACTIVE / OWNER-LOCKED / FAIL-CLOSED / MAIN-CHAT-ONLY**  
Owner lock: 2026-09-17  
Scope correction: 2026-09-17 — **THIS GATE CONTROLS MAIN CHAT / ARCHITECT / REVIEW / ACCEPTANCE. IT IS NOT A CHATGPT WORK RUNTIME GATE.**

## 0. Why this rule exists

A recurring Main Chat failure has been observed across KW-002: Main Chat repeatedly relied on remembered rules, summaries, prior chat state or technical artifacts instead of freshly reading the controlling live rules in full. This caused incomplete owner-facing reports, missing source disclosure, incorrect Work handoff behavior and premature acceptance/status claims.

Therefore:

```text
MAIN CHAT MEMORY != RULE READBACK
PRIOR CHAT SUMMARY != RULE READBACK
PAST COMPLIANCE != CURRENT COMPLIANCE
FAMILIARITY != AUTHORIZATION TO ACT
```

## 1. Exact scope

This gate applies to **Main Chat / architect / reviewer / repository-control / acceptance-control actions**, including:

- step preparation and methodology work;
- fresh external research;
- owner-facing pre-step/result reports;
- Work-trigger decision;
- canonical Work-prompt authoring;
- Work release/relay authorization;
- Bridge/provider release where applicable;
- Main Chat analysis;
- permanent rule/method mutation;
- Work-return review and acceptance;
- publication/final placement/readback;
- cursor and roadmap movement.

Before those actions, Main Chat must:

```text
FETCH CURRENT LIVE REMOTE BRANCH
→ IDENTIFY CURRENT MAIN-CHAT ACTION
→ IDENTIFY APPLICABLE CROSS-KWORK + LEVEL1 + LEVEL2 + JOB AUTHORITIES
→ READ THEM IN FULL FROM CURRENT LIVE AUTHORITY
→ READ CURRENT JOB FLOW / CURSOR / ACCEPTED INPUT AUTHORITIES
→ READ RELEVANT FAILURE / ANTI-REGRESSION RECORDS
→ VERIFY OWNER-FACING REPORT REQUIREMENTS
→ ONLY THEN ACT
```

If not complete:

```text
MAIN_CHAT_EXECUTION_ALLOWED = false
```

## 2. Critical explicit exclusion — ChatGPT Work

**DO NOT APPLY THIS FULL-RULE-REREAD GATE TO CHATGPT WORK RUNTIME.**

Main Chat is responsible for converting the governing project rules into a complete frozen execution prompt before Work starts.

```text
MAIN CHAT
= GOVERNANCE / METHOD / RESEARCH / RELEASE / ACCEPTANCE

CHATGPT WORK
= EXECUTION OF THE RELEASED CONTRACT
```

Work MUST NOT be instructed to redo Main Chat's process by default.

Specifically, Work does **not** need to repeat:

```text
FULL LEVEL1 REREAD
OWNER-FACING SOURCE DISCLOSURE
FRESH EXTERNAL METHODOLOGY AUDIT ALREADY COMPLETED BY MAIN CHAT
PLAIN-LANGUAGE OWNER REPORT
RELEASE-REVALIDATION DECISION
MAIN CHAT FAILURE-LEDGER REVIEW
ROADMAP AUTHORIZATION
```

unless the owner explicitly creates a special Work task whose actual purpose is rule/method auditing.

For ordinary execution Work, the only required startup safety check is the one written in the released prompt, normally:

```text
FETCH CURRENT REMOTE HEAD
→ VERIFY RELEASE / PROMPT IDENTITY
→ VERIFY NAMED INPUT FILES / HASHES / MANIFEST / SCHEMA
→ MATERIAL DRIFT? STOP + REPORT AUTHORITY_DRIFT
→ NO MATERIAL DRIFT? EXECUTE
```

This bounded drift check is **not** a second governance/research/release cycle.

## 3. “Read in full” applies to Main Chat

For Main Chat, forbidden shortcuts remain:

```text
FILE NAME SEEN != FILE READ
SEARCH SNIPPET != FILE READ
FIRST LINES != FILE READ
SUMMARY != FILE READ
MEMORY != FILE READ
OLD COPY != CURRENT LIVE RULE
```

## 4. Main Chat rule-read ledger

Before a major Main Chat release/acceptance action, record at minimum:

```text
LIVE_REMOTE_HEAD
CURRENT_MAIN_CHAT_ACTION
RULES_READ_IN_FULL
JOB_STATE_READ
FAILURE_LEDGER_READ
OWNER_REPORT_GATE_READ
WORK_HANDOFF_RULE_READ when applicable
PROVIDER_GATE_READ when applicable
GENERALIZATION_GATE_READ before permanent-method mutation
UNRESOLVED_AUTHORITY_CONFLICTS
MAIN_CHAT_EXECUTION_ALLOWED = true|false
```

This ledger is a **Main Chat control record**. Do not require Work to materialize an equivalent full-rule ledger.

## 5. Owner-facing report gate

For every major roadmap step/preparation/release, Main Chat must freshly obey:

`PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`

The chat itself must contain the required roadmap/status/source disclosure/source→method explanation and real plain-Russian `ПРОСТЫМИ СЛОВАМИ` conclusion.

```text
SOURCE LINKS IN ARTIFACT
!=
OWNER-FACING SOURCE DISCLOSURE IN CHAT
```

Again: **this owner-facing reporting gate belongs to Main Chat, not Work.**

## 6. Work handoff boundary

Before Main Chat relays a Work execution unit:

```text
MAIN CHAT FULL RULE REREAD = PASS
MAIN CHAT PRE-STEP RESEARCH / DISCLOSURE = PASS where required
WORK TRIGGER = CONFIRMED
PRE-HANDOFF MANIFEST = FROZEN
CANONICAL EXECUTION PROMPT = COMPLETE
RELEASE = AUTHORIZED
```

Then Work executes the prompt.

```text
RELEASED WORK PROMPT
!= INVITATION FOR WORK TO REDO MAIN CHAT GOVERNANCE
```

## 7. Permanent method mutation

Before Main Chat changes Level1/Level2 methodology, it must read in full:

- `ROADMAP_AND_METHOD_GENERALIZATION_RULE.md`;
- `JOB_DATA_SEPARATION_AND_LIFECYCLE.md`;
- relevant failure-ledger authorities;
- the current rule being changed.

Concrete job incidents remain in `work/<JOB_ID>/`.

## 8. Post-Work acceptance

After Work returns, Main Chat — not Work — performs the governing acceptance cycle:

```text
REREAD APPLICABLE ACCEPTANCE RULES
→ VERIFY RETURNED / PUBLISHED ARTIFACTS
→ VERIFY COUNTS / JOINS / PROVENANCE / HOLD / ERROR / UNRESOLVED
→ VERIFY OWNER-FACING RESULT REPORT
→ REMOTE READBACK / IDENTITY QA
→ ONLY THEN ACCEPT / ADVANCE
```

## 9. Anti-regression statement

```text
KNOWN_RECURRING_FAILURE:
Main Chat has repeatedly violated explicit KW-002 rules when acting from memory.

PERMANENT_CONTROL:
Main Chat rereads current applicable rules before governance/release/acceptance actions.

WORK_RUNTIME_CONTROL:
Do not burden ChatGPT Work with Main Chat's full governance cycle. Work executes the released prompt and performs only the bounded freshness/input-drift checks explicitly required there.
```

## 10. Markers

```text
KW002_MAIN_CHAT_FULL_RULE_REREAD_REQUIRED = true
KW002_MAIN_CHAT_MEMORY_NOT_AUTHORITY = true
KW002_MAIN_CHAT_NO_RELEASE_BEFORE_FULL_RULE_READ = true
KW002_MAIN_CHAT_OWNER_SOURCE_DISCLOSURE_REQUIRED = true
KW002_MAIN_CHAT_ACCEPTANCE_REREAD_REQUIRED = true
KW002_FULL_RULE_REREAD_GATE_DOES_NOT_APPLY_TO_WORK_RUNTIME = true
KW002_WORK_FULL_LEVEL1_REREAD_FORBIDDEN_BY_DEFAULT = true
KW002_WORK_OWNER_REPORT_GATE_FORBIDDEN_BY_DEFAULT = true
KW002_WORK_RESEARCH_REVALIDATION_FORBIDDEN_BY_DEFAULT = true
KW002_WORK_NARROW_DRIFT_PREFLIGHT_ALLOWED = true
KW002_MAIN_GOVERNANCE_AND_WORK_EXECUTION_SEPARATED = true
```
