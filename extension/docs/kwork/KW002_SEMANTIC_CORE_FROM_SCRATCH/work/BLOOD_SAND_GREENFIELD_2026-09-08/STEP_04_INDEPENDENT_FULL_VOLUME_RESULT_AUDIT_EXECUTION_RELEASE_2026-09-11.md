# KW-002 Blood & Sand — Step04 independent full-volume result audit execution release

Date: 2026-09-11
Status: RELEASED TO CHATGPT WORK / AUDIT ONLY

Canonical prompt:
`STEP_04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT_WORK_PROMPT_2026-09-11.md`

Main ChatGPT external method review:
`STEP_04_EXTERNAL_METHODOLOGY_REVIEW_MAIN_CHATGPT_2026-09-11.md`

Execution purpose:
independently audit the actual full-volume Step04 family-triage result after external methodology review identified a material need to test hidden family heterogeneity and deterministic lexicon/rule-order bias.

Hard boundaries:

```text
PROVIDER_CALLS_ALLOWED = 0
WORDSTAT = 0
ORDINARY_SEARCH = 0
GENSEARCH = 0
AI_SEARCH = 0
STEP05_ADVANCEMENT = false
STEP06_ADVANCEMENT = false
STEP04_CORRECTION_IN_THIS_PASS = false
SEALED_PRIOR_BLOOD_SAND_RESEARCH = forbidden
```

Required audit volume:

```text
NORMALIZED_IDENTITIES = 24576
ACTIVE_PLUS_HOLD_IDENTITIES = 18135
EXCLUDED_IDENTITIES_HISTORY = 6441
RAW_OCCURRENCES = 25979
FAMILIES = 26
EXPANSION_QUEUE_ROWS = 13
SANITATION_FEEDBACK_ROWS = 10
```

The Work result must be adversarial and independent. Previous `97.20/100` self-score is not an audit prior and must not be reused.

Final Work verdict must be one of:

```text
STEP04_RESULT_AUDIT = PASS
STEP04_RESULT_AUDIT = PASS_WITH_NONBLOCKING_FINDINGS
STEP04_RESULT_AUDIT = REWORK_REQUIRED
```

After publication/owner relay, STOP for Main ChatGPT return QA.
