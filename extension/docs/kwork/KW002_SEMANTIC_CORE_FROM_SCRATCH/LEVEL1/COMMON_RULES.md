# KW-002 — LEVEL 1 COMMON RULES INDEX

Status: **ACTIVE / OWNER-AUTHORIZED / OWNER-LOCKED**

Owner clarification: 2026-09-11 — owner-facing `ПРОСТЫМИ СЛОВАМИ` is mandatory real plain Russian and must never be replaced by hashes, IDs, status markers or machine-style dumps.

Owner fail-closed rule-read lock: 2026-09-17 — remembered rules are not authority; current applicable rules must be freshly read in full before Main Chat governance/release/acceptance actions.

Owner role-boundary correction: 2026-09-17 — **THE FULL RULE-REREAD / FRESH-RESEARCH / OWNER-REPORT / RELEASE GATES ARE MAIN CHAT RESPONSIBILITIES. THEY MUST NOT BE DUPLICATED INSIDE ORDINARY CHATGPT WORK RUNTIME.**

## 00. Mandatory role boundary

```text
MAIN CHATGPT
= RULE REREAD
+ METHOD / FRESH RESEARCH
+ OWNER-FACING SOURCE DISCLOSURE / PLAIN-LANGUAGE REPORT
+ WORK TRIGGER / PROMPT AUTHORING / RELEASE
+ RETURN QA / REMOTE ACCEPTANCE / CURSOR

CHATGPT WORK
= EXECUTE THE RELEASED FULL-VOLUME CONTRACT
+ TASK QA
+ ARTIFACT MATERIALIZATION
+ HANDOFF PACKAGE
```

For ordinary Work execution:

```text
FULL LEVEL1 REREAD = NOT A WORK RUNTIME REQUIREMENT
FRESH EXTERNAL METHOD RESEARCH REDO = NOT A WORK RUNTIME REQUIREMENT
OWNER-FACING PRE-STEP REPORT = NOT A WORK RUNTIME REQUIREMENT
RELEASE AUTHORIZATION REDO = NOT A WORK RUNTIME REQUIREMENT
```

Work may perform the narrow technical preflight explicitly contained in the released prompt:

```text
CURRENT REMOTE HEAD
+ RELEASE / PROMPT IDENTITY
+ NAMED INPUT / MANIFEST / SCHEMA / HASH IDENTITY
→ MATERIAL DRIFT? STOP
→ OTHERWISE EXECUTE
```

Canonical Main Chat fail-closed gate:

`00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE.md`

Canonical recurring Main Chat failure checklist:

`01_RECURRING_ASSISTANT_RULE_FAILURES_ANTI_REGRESSION_CHECKLIST.md`

Canonical Work role/handoff boundary:

`WORK_HANDOFF_RULE.md`

---

## 1. Mandatory Main Chat Level-1 authorities

Before every major KW-002 preparation/release/acceptance action, **Main Chat** reads in full from the current live branch, as applicable:

```text
0. 00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE.md
1. 01_RECURRING_ASSISTANT_RULE_FAILURES_ANTI_REGRESSION_CHECKLIST.md
2. applicable cross-Kwork owner-locked authorities
3. INHERITED_KW001_UNIVERSAL_RULES.md
4. PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md
5. RESULT_QUALITY_SCORING_RULE.md
6. METHOD_SOURCE_AND_EVIDENCE_RULES.md
7. CLIENT_INTAKE_AND_SCOPE_RULE.md when scope/client facts are material
8. JOB_DATA_SEPARATION_AND_LIFECYCLE.md
9. ROADMAP_AND_METHOD_GENERALIZATION_RULE.md before permanent Level1/Level2 mutation
10. EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md
11. WORK_HANDOFF_RULE.md when Work/large-data risk exists
12. YANDEX_MARKETING_BRIDGE_EXECUTION_RULE.md when provider work is possible
13. current Level2 step method/gates
14. current work/<JOB_ID>/ flow/cursor/manifests/evidence/incidents
```

A filename, snippet, summary or remembered old copy is not a Main Chat full read.

This list is **not** an instruction to Work to reread all of these files. Main Chat must translate applicable controls into the canonical Work execution prompt.

---

## 2. Product identity

KW-002 builds a semantic core and planned site architecture from scratch for modern Yandex.

```text
FROM SCRATCH
= no existing semantic core required
= no existing final site structure required
= client guesses do not become search truth
```

The method uses ordinary Yandex Search and later bounded Yandex generative/Alice evidence where decision-relevant.

```text
AI-SEARCH EVIDENCE != ASKING AN ASSISTANT HOW TO DO SEO
```

---

## 3. Data volume / delivery scope

```text
RAW CANDIDATES
!= NORMALIZED POOL
!= SANITIZED CANDIDATES
!= VALID RESERVE
!= DELIVERY SELECTED SET
!= FINAL DELIVERED CORE
```

Never sample/truncate legitimate large data merely for ordinary-chat convenience. When complete processing is unsafe in ordinary chat, Main Chat delegates the complete unit to Work under `WORK_HANDOFF_RULE.md`.

---

## 4. Evidence classes remain separate

Distinguish:

```text
CLIENT FACT
PROVIDER OBSERVATION
CURRENT SEARCH OBSERVATION
PUBLIC COMPETITOR-PAGE OBSERVATION
AI-SEARCH OBSERVATION
PROJECT DERIVATION / ANALYST JUDGMENT
UNKNOWN / HOLD
```

Examples:

```text
COMPETITOR PAGE TOPIC != PROVEN DEMAND
WORDSTAT PHRASE != BUSINESS RELEVANCE
SERP OVERLAP != AUTOMATIC SAME-PAGE DECISION
AI ANSWER TOPIC != AUTOMATIC NEW SEO PAGE
```

---

## 5. Owner-facing reporting — Main Chat responsibility

Every major owner-facing pre-step/status/result/QA report from **Main Chat** must explain in normal Russian:

```text
WHY
WHAT
RESULT
CAN WE CONTINUE
BLOCKER IF ANY
NEXT PHYSICAL ACTION
```

Technical hashes/IDs/status dumps do not replace that explanation.

For external method research, Main Chat shows clickable links plus what each source supports and how it affects the method.

```text
SOURCE LINKS IN ARTIFACT != OWNER-FACING DISCLOSURE
```

These owner-report obligations are not Work runtime tasks.

---

## 6. Work execution / handoff

Canonical authority:

`WORK_HANDOFF_RULE.md`

```text
MAIN CHAT GOVERNANCE / RELEASE
→ OWNER RELAYS CANONICAL PROMPT
→ WORK EXECUTES COMPLETE TASK
→ WORK LOCAL QA
→ DIRECT FILE LINKS + ONE TRANSPORT ZIP
→ OWNER UPLOADS ALL FILES TO ONE STAGING TARGET
→ OWNER RETURNS "ГОТОВО"
→ MAIN CHAT FINAL PLACEMENT / READBACK / ACCEPTANCE
```

The owner does not sort files into final repository paths.

Work does not redo Main Chat's rule/research/report/release gates.

---

## 7. Fail-closed truthfulness

If a material decision lacks evidence:

```text
DO NOT GUESS
→ HOLD / REVIEW / SEARCH_REQUIRED / EVIDENCE_REQUIRED / DEFERRED
```

Output completeness must not erase truthful uncertainty.

---

## 8. Result quality scoring

After every major step/rework/deliverable, the applicable QA uses the ten criteria from `RESULT_QUALITY_SCORING_RULE.md`, each independently scored 0–10, with total `/100` and average `/10`.

PASS requires score threshold plus all hard gates; score never overrides a hard failure.

Work may calculate task-level QA/quality when the prompt explicitly requires it. Main Chat still owns final acceptance.

---

## 9. Permanent markers

```text
KW002_MAIN_CHAT_FULL_RULE_REREAD_REQUIRED = true
KW002_MAIN_CHAT_FRESH_EXTERNAL_RESEARCH_REQUIRED = true
KW002_MAIN_CHAT_OWNER_FACING_REPORT_REQUIRED = true
KW002_MAIN_CHAT_WORK_RELEASE_AND_ACCEPTANCE_CONTROL = true
KW002_WORK_EXECUTES_RELEASED_CONTRACT = true
KW002_WORK_FULL_LEVEL1_REREAD_FORBIDDEN_BY_DEFAULT = true
KW002_WORK_FRESH_RESEARCH_REDO_FORBIDDEN_BY_DEFAULT = true
KW002_WORK_OWNER_REPORT_GATE_FORBIDDEN_BY_DEFAULT = true
KW002_WORK_RELEASE_REAUTHORIZATION_FORBIDDEN_BY_DEFAULT = true
KW002_WORK_NARROW_DRIFT_PREFLIGHT_ALLOWED = true
KW002_LARGE_DATA_NO_SAMPLING = true
KW002_OWNER_RELAY_SINGLE_STAGING_REQUIRED = true
KW002_OWNER_MUST_NOT_ROUTE_FINAL_PATHS = true
KW002_REMOTE_READBACK_AND_MAIN_ACCEPTANCE_REQUIRED = true
KW002_LEVEL1_OWNER_LOCKED = true
```
