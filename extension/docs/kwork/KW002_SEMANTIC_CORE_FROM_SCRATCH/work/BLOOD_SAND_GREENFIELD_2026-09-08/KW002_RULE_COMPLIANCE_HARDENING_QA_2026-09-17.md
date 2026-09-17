# KW-002 / BLOOD & SAND — RULE COMPLIANCE HARDENING QA — 2026-09-17

Status: **QA CANDIDATE / REMOTE READBACK REQUIRED AFTER WRITE**  
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`  
Action: repository-wide KW-002 rule-read / anti-regression hardening  
QA base remote HEAD before this QA write: `cc741f78e8c3d884ae07c19c1fb7578aec61bf47`

## 1. Goal

Prevent a recurring process failure in which Main Chat / another executor remembers or summarizes project rules instead of freshly reading the current live controlling authorities in full before acting.

Required owner control:

```text
NO FRESH FULL APPLICABLE RULE REREAD
→ NO MATERIAL KW-002 ACTION
```

The control must be visible at the project, Level1, Level2, work and current-job entry layers and must block preparation, Work, Bridge/provider actions, analysis, mutation, QA acceptance and cursor/roadmap advancement.

## 2. Rule-read ledger used for this hardening pass

The following current authorities were read in full during the hardening action before final acceptance work:

```text
LEVEL1/00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE.md
LEVEL1/01_RECURRING_ASSISTANT_RULE_FAILURES_ANTI_REGRESSION_CHECKLIST.md
LEVEL1/COMMON_RULES.md
LEVEL1/INHERITED_KW001_UNIVERSAL_RULES.md
LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md
LEVEL1/RESULT_QUALITY_SCORING_RULE.md
LEVEL1/METHOD_SOURCE_AND_EVIDENCE_RULES.md
LEVEL1/JOB_DATA_SEPARATION_AND_LIFECYCLE.md
LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md
LEVEL1/WORK_HANDOFF_RULE.md
LEVEL1/ROADMAP_AND_METHOD_GENERALIZATION_RULE.md
LEVEL1/WORK_BASE_FRESHNESS_AND_AUTHORITY_DRIFT_RULE.md
../../KWORK_LARGE_ARTIFACT_OWNER_RELAY_AND_PUBLICATION_RULE.md
LEVEL2/STEP_RULES_INDEX.md through EOF
LEVEL2/STEP_07_COMPETITOR_SEMANTIC_EXPANSION.md through EOF
work/BLOOD_SAND_GREENFIELD_2026-09-08/JOB_FLOW.md
work/BLOOD_SAND_GREENFIELD_2026-09-08/KW002_EXECUTION_CURSOR_2026-09-17.json
work/BLOOD_SAND_GREENFIELD_2026-09-08/STEP_07_COMPETITOR_SEMANTIC_EXPANSION_WORK_PROMPT.md through EOF
work/BLOOD_SAND_GREENFIELD_2026-09-08/KW002_RULE_COMPLIANCE_FAILURE_INCIDENT_2026-09-17.md
work/BLOOD_SAND_GREENFIELD_2026-09-08/STEP_07_RELEASE_REVALIDATION_GATE_2026-09-17.md
```

`COMMON_RULES.md` was modified during this pass and then freshly read back in full again before this QA file was written.

No Web/SEO methodology research was required for this rule-hardening action itself because this action changes owner-mandated process controls, not a Search/SEO/provider methodology claim. The controlling source classes for this correction are:

```text
OWNER_SCOPE_RULE
PROJECT_TEST_VALIDATED incident evidence
CURRENT PROJECT RULE AUTHORITY
```

Fresh external research remains mandatory before the actual Step07 execution release under the existing pre-step rule and the new Step07 release-revalidation gate.

## 3. Files created

Universal / project-layer guards:

```text
KW002_SEMANTIC_CORE_FROM_SCRATCH/00_READ_RULES_BEFORE_ANY_ACTION.md
LEVEL1/00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE.md
LEVEL1/01_RECURRING_ASSISTANT_RULE_FAILURES_ANTI_REGRESSION_CHECKLIST.md
LEVEL2/00_READ_RULES_BEFORE_ANY_STEP.md
work/00_READ_RULES_BEFORE_ANY_JOB_ACTION.md
```

Current-job guards / evidence:

```text
work/BLOOD_SAND_GREENFIELD_2026-09-08/00_READ_RULES_BEFORE_ANY_ACTION.md
work/BLOOD_SAND_GREENFIELD_2026-09-08/KW002_RULE_COMPLIANCE_FAILURE_INCIDENT_2026-09-17.md
work/BLOOD_SAND_GREENFIELD_2026-09-08/STEP_07_RELEASE_REVALIDATION_GATE_2026-09-17.md
this QA file
```

## 4. Files materially updated

```text
LEVEL1/COMMON_RULES.md
work/BLOOD_SAND_GREENFIELD_2026-09-08/JOB_FLOW.md
work/BLOOD_SAND_GREENFIELD_2026-09-08/KW002_EXECUTION_CURSOR_2026-09-17.json
```

`COMMON_RULES.md` no longer falsely presents itself as the first Level1 read. It now explicitly states that the new `00` and `01` authorities are mandatory pre-entry gates.

The job state now explicitly blocks actual Step07 until current-authority release revalidation, owner-facing source disclosure and Work-prompt reconciliation pass.

## 5. Universal-vs-job separation QA

An initial version of the recurring-failure checklist briefly contained a concrete Step07-specific incident in Level1. Fresh reread of `ROADMAP_AND_METHOD_GENERALIZATION_RULE.md` caught the contamination.

Correction performed:

```text
LEVEL1/01_RECURRING_ASSISTANT_RULE_FAILURES_ANTI_REGRESSION_CHECKLIST.md
= universal failure mechanisms only

work/BLOOD_SAND_GREENFIELD_2026-09-08/KW002_RULE_COMPLIANCE_FAILURE_INCIDENT_2026-09-17.md
= concrete Step07/job incident history
```

QA:

```text
JOB_SPECIFIC_CLIENT_NAMES_USED_TO_DEFINE_UNIVERSAL_CONTROL = 0
JOB_SPECIFIC_STEP07_COUNTS_USED_AS_UNIVERSAL_THRESHOLDS = 0
CURRENT_JOB_STATUS_EMBEDDED_IN_UNIVERSAL_FAILURE_RULE = 0
UNIVERSAL_FAILURE_MECHANISM_EXPLICIT = true
JOB_INCIDENT_PRESERVED_SEPARATELY = true
LAYER_SEPARATION = PASS
```

## 6. Hard controls now present

The repository now explicitly states:

```text
ASSISTANT MEMORY != RULE READBACK
PRIOR CHAT SUMMARY != RULE READBACK
PAST COMPLIANCE != CURRENT COMPLIANCE
FAMILIARITY != EXECUTION PERMISSION
```

And blocks:

```text
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
```

until the current applicable live authorities have been read in full.

The rule also requires an explicit rule-read ledger before a major execution unit.

## 7. Owner-facing report hardening

The new gate explicitly prevents the prior failure where sources existed only inside an artifact.

```text
SOURCE LINKS EXIST IN MD/ZIP/WORK OUTPUT
!= OWNER-FACING SOURCE DISCLOSURE IN CHAT
```

Before a major step, owner-facing chat must itself show:

- fresh research where required;
- clickable source title / publisher / URL;
- what each source supports;
- how it changes/confirms the method;
- source limitations;
- source→method trace;
- a real normal-Russian `ПРОСТЫМИ СЛОВАМИ` conclusion explaining WHY / WHAT / RESULT / BLOCKER / NEXT ACTION.

## 8. Work / owner-relay hardening

The active control remains:

```text
ONE HANDOFF UNIT
→ ONE OWNER STAGING TARGET
→ OWNER RELAYS ALL FILES TOGETHER
→ EXECUTOR DOES FINAL NEW/REPLACE PATH ROUTING
→ EXECUTOR CLEANS STAGING
→ FINAL-PATH REMOTE READBACK
→ ACCEPTANCE
```

The owner is not responsible for sorting handoff files across Level1 / Level2 / job-root directories.

## 9. Authority drift discovered by the full reread

The fresh full read caught an additional stale-roadmap assumption:

```text
CURRENT STEP_RULES_INDEX FINAL STEP = STEP22
OLDER CURSOR / PROMPT ASSUMPTION = TERMINAL AT STEP20
```

The current cursor and JOB_FLOW were corrected to include Step21 and Step22.

The prepared actual-Step07 Work prompt remains a frozen preparation artifact but is now explicitly blocked from relay/execution until `STEP_07_RELEASE_REVALIDATION_GATE_2026-09-17.md` reconciles it to the live rule authority.

This is an intended fail-closed state, not an execution failure.

## 10. Current semantic boundary after hardening

No semantic/provider work was performed by this hardening action.

```text
NEW_WORDSTAT_CALLS = 0
NEW_YANDEX_SEARCH_CALLS = 0
NEW_AI_SEARCH_OR_GENSEARCH_CALLS = 0
STEP07_PRODUCTION_EXTRACTION = 0
STEP07 = NOT_STARTED
STEP08 = NOT_STARTED
```

The accepted Step07 preparation data package remains accepted. Only release of the **future actual Step07 execution** is blocked pending current-authority revalidation.

## 11. Hard-gate QA

```text
ROOT_READ_FIRST_GUARD_PRESENT = PASS
LEVEL1_FAIL_CLOSED_GATE_PRESENT = PASS
LEVEL1_RECURRING_FAILURE_CHECKLIST_PRESENT = PASS
COMMON_RULES_PREENTRY_ORDER_CORRECTED = PASS
LEVEL2_READ_FIRST_GUARD_PRESENT = PASS
WORK_ROOT_READ_FIRST_GUARD_PRESENT = PASS
CURRENT_JOB_READ_FIRST_GUARD_PRESENT = PASS
CONCRETE_INCIDENT_PRESERVED_IN_JOB_ROOT = PASS
UNIVERSAL_GENERALIZATION_CONTAMINATION = 0
OWNER_CHAT_SOURCE_DISCLOSURE_CONTROL = PASS
PLAIN_LANGUAGE_REPORT_CONTROL = PASS
WORK_CURRENT_EXECUTION_UNIT_TRIGGER_CONTROL = PASS
OWNER_SINGLE_STAGING_CONTROL = PASS
STEP07_RELEASE_FAIL_CLOSED = PASS
STEP07_EXECUTION_ALLOWED = false
ROADMAP_STEP22_AUTHORITY_RECONCILED_IN_CURRENT_STATE = PASS
PROVIDER_CALLS_FROM_THIS_ACTION = 0
```

Post-write requirement for this QA artifact:

```text
FETCH FINAL REMOTE HEAD
READ BACK THIS QA FILE
READ BACK CURRENT JOB_FLOW / CURSOR
VERIFY ALL GUARD FILES STILL PRESENT
ONLY THEN REPORT THIS HARDENING PASS AS REMOTELY VERIFIED
```

## 12. Quality score

Each criterion is scored independently out of 10 as required by `RESULT_QUALITY_SCORING_RULE.md`.

| Criterion | Score / 10 | Basis / lost points |
|---|---:|---|
| Goal and output completeness | 10 | The requested fail-closed rule-read control, visible guards, incident history and blocked next release are materialized. |
| Method and source support | 10 | Derived directly from owner instructions plus current owner-locked project rules and observed repeated failures; no unsupported external-method claim was introduced. |
| Input evidence and provenance integrity | 10 | Concrete incident remains job-specific; universal controls are separated and linked to current rule authorities. |
| Coverage and completeness | 9 | Guards exist at project/Level1/Level2/work/job entry layers and Common Rules; not every historical file was rewritten because duplicate rule bodies would create drift. One point retained as caution against claiming literal every-file duplication. |
| Analytical correctness and claim boundaries | 10 | Distinguishes memory from authority, technical PASS from owner-report PASS, preparation from execution and universal rule from job incident. |
| Adversarial QA quality | 10 | Fresh reread caught and corrected both Level1 contamination and the stale Step20 terminal-roadmap assumption. |
| Persistence, readback and reproducibility | 9 | All material controls except this just-written QA file were remotely read back before QA creation; this QA requires one final post-write readback by Main Chat. |
| Owner/client usability and plain language | 9 | Hard requirements are explicit and operational, but final owner-facing chat summary still must be produced after this QA readback. |
| Information gain / cost / execution efficiency | 8 | The correction required several sequential commits and one initial Level1 contamination correction; this is preserved rather than hidden. |
| Downstream readiness | 9 | Future execution is safely fail-closed, but Step07 cannot yet run until its required release revalidation and fresh owner-facing pre-step disclosure are completed. |

```text
QUALITY_TOTAL = 94 / 100
QUALITY_SCORE = 9.4 / 10
HARD_GATE_FAILURES = 0 for this rule-hardening result
PASS_CANDIDATE = true
REMOTE_QA_ARTIFACT_READBACK = required after this write
```

## 13. ПРОСТЫМИ СЛОВАМИ

Проблема была не в том, что правил не существовало. Правила уже были, но Main Chat несколько раз работал по памяти и поэтому снова нарушал то, что уже было записано. Теперь это перестало быть просто замечанием в переписке: в репозитории появились отдельные файлы, которые прямо запрещают начинать любую существенную работу, пока актуальные правила не прочитаны полностью заново.

Запрет поставлен на входе в проект, Level1, Level2, рабочую область и текущий заказ. Кроме этого, конкретные сегодняшние ошибки сохранены отдельно в истории этого заказа, а универсальная методика содержит только общий механизм ошибки.

Во время полной перечитки нашлась ещё одна польза этого контроля: старые документы считали Step20 концом roadmap, хотя живой roadmap уже идёт до Step22. Текущий статус исправлен. Сам Step07 при этом не запускался.

Продолжать непосредственно Step07 сейчас нельзя автоматически. Сначала Main Chat должен ещё раз пройти release revalidation уже по новым правилам, показать в чате свежие материалы со ссылками и нормальное объяснение простыми словами, сверить подготовленный Work prompt с текущей authority. Только после этого можно будет отдать актуальный prompt в Work.
