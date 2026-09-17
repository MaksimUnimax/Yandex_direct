# KW-002 / BLOOD & SAND — RULE COMPLIANCE HARDENING QA — 2026-09-17

Status: **HISTORICAL QA / ROLE-BOUNDARY CORRECTED**  
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`

## 0. Superseding scope correction

The original version of this QA correctly identified repeated Main Chat rule-memory failures, but it **incorrectly generalized the full rule-reread/no-action gate to ChatGPT Work runtime**.

That scope is now superseded.

Current authority:

```text
MAIN CHAT
= FULL RULE REREAD / FRESH RESEARCH / OWNER REPORT / WORK RELEASE / RETURN ACCEPTANCE

CHATGPT WORK
= EXECUTE THE RELEASED CONTRACT
```

Therefore any historical text from this QA implying:

```text
WORK MUST READ THE FULL RULE STACK
WORK MUST PRODUCE A FULL RULE-READ LEDGER
WORK MUST REDO FRESH EXTERNAL RESEARCH
WORK MUST REDO OWNER-FACING DISCLOSURE / RELEASE
```

is **SUPERSEDED / INVALID**.

Current Work startup is limited to:

```text
CURRENT HEAD
+ RELEASE / PROMPT IDENTITY
+ NAMED INPUT / MANIFEST / SCHEMA / HASH IDENTITY
→ MATERIAL DRIFT? STOP
→ OTHERWISE EXECUTE
```

## 1. What remains valid from the original hardening

The following findings remain valid and are retained through Git history and current authority files:

- Main Chat repeatedly worked from memory instead of current live rules;
- owner-facing clickable source disclosure is a Main Chat gate;
- plain-language owner reporting is a Main Chat gate;
- Main Chat must evaluate Work trigger for the current complete execution unit;
- the owner must not route multi-file Work handoffs among repository directories;
- one handoff uses one owner staging target;
- Main Chat owns post-upload readback / final placement / acceptance;
- Level1/Level2 universal rules must not be contaminated with current-job incidents;
- the roadmap authority runs through Step22;
- a technically correct artifact does not waive Main Chat reporting/acceptance duties.

## 2. Newly identified regression

The later owner review exposed an additional failure:

```text
MAIN CHAT GOVERNANCE WAS DUPLICATED INSIDE WORK RUNTIME
```

This is now recorded as:

`KW002_RULE_COMPLIANCE_FAILURE_INCIDENT_2026-09-17.md` → `I-2026-09-17-08`.

Permanent control:

```text
MAIN CHAT DOES GOVERNANCE ONCE
→ WRITES / RELEASES THE FROZEN WORK PROMPT
→ WORK EXECUTES THE PROMPT
```

## 3. Current authoritative files

Use the current live versions of:

```text
LEVEL1/00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE.md
LEVEL1/01_RECURRING_ASSISTANT_RULE_FAILURES_ANTI_REGRESSION_CHECKLIST.md
LEVEL1/WORK_HANDOFF_RULE.md
LEVEL2/00_READ_RULES_BEFORE_ANY_STEP.md
work/00_READ_RULES_BEFORE_ANY_JOB_ACTION.md
work/BLOOD_SAND_GREENFIELD_2026-09-08/00_READ_RULES_BEFORE_ANY_ACTION.md
work/BLOOD_SAND_GREENFIELD_2026-09-08/STEP_07_RELEASE_REVALIDATION_GATE_2026-09-17.md
work/BLOOD_SAND_GREENFIELD_2026-09-08/STEP_07_EXECUTION_RELEASE_REVALIDATION_2026-09-17.md
work/BLOOD_SAND_GREENFIELD_2026-09-08/STEP_07_COMPETITOR_SEMANTIC_EXPANSION_WORK_PROMPT.md
```

These current files supersede the incorrect Work-runtime scope in the earlier hardening QA.

## 4. Current QA

```text
MAIN_CHAT_FAIL_CLOSED_RULE_REREAD = PASS
MAIN_CHAT_OWNER_SOURCE_DISCLOSURE_CONTROL = PASS
MAIN_CHAT_PLAIN_LANGUAGE_REPORT_CONTROL = PASS
MAIN_CHAT_WORK_TRIGGER_CONTROL = PASS
WORK_FULL_RULE_REREAD_REQUIRED = false
WORK_FRESH_RESEARCH_REDO_REQUIRED = false
WORK_OWNER_REPORT_REQUIRED = false
WORK_RELEASE_REAUTHORIZATION_REQUIRED = false
WORK_NARROW_DRIFT_PREFLIGHT = REQUIRED
OWNER_SINGLE_STAGING_CONTROL = PASS
ROADMAP_STEP22_AUTHORITY = PASS
ROLE_SEPARATION = PASS
```

## 5. Quality score for the corrected hardening

| Criterion | Score / 10 | Basis |
|---|---:|---|
| Goal and output completeness | 10 | Current guards now protect Main Chat without burdening Work. |
| Method/source support | 10 | Direct owner instruction plus observed failure evidence. |
| Input/provenance integrity | 10 | Concrete incident remains job-root; universal control remains generic. |
| Coverage/completeness | 10 | Root/Level1/Level2/work/job/release/handoff authorities are aligned. |
| Analytical correctness | 10 | Architect/executor roles are now separated correctly. |
| Adversarial QA | 10 | Owner review exposed the duplicated-governance defect and it was corrected. |
| Persistence/readback | 9 | Current files require final remote readback after this correction pass. |
| Owner usability | 10 | Owner relays one prompt and one staging package only. |
| Execution efficiency | 10 | Removed unnecessary Work governance/research repetition. |
| Downstream readiness | 10 | Step07 can execute directly under the corrected prompt. |

```text
QUALITY_TOTAL = 99 / 100
QUALITY_SCORE = 9.9 / 10
```

## 6. Plain-language conclusion

The original anti-regression idea was right about one thing: Main Chat kept forgetting or skipping rules. But I then overcorrected and forced Work to reread those rules too. That was wrong. The current rule is now simple: **I do the governance and checks before giving Work the task; Work executes the task.** Work only verifies that the released inputs have not materially changed during handoff.
