# KW-002 Blood & Sand — Step04 post-audit corrective rework execution release

Date: 2026-09-11
Status: **RELEASED TO WORK / FULL-VOLUME CORRECTION ONLY / STEP05 BLOCKED**

## Accepted basis

Main ChatGPT accepted the independent W07 audit published at:

`212a6fa7be66360317b3026541896669b8b019c6`

Main review authority:

`STEP_04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT_MAIN_CHATGPT_REVIEW_2026-09-11.md`

Current semantic verdict:

```text
STEP04_CURRENT_RESULT = REWORK_REQUIRED
MATERIAL_DEFECT_IDENTITIES = 255
RULE_ORDER_DEFECT_IDENTITIES = 207
FAMILY_TOO_BROAD_IDENTITIES = 48
STEP05_ALLOWED = false
STEP06_ALLOWED = false
```

Accepted blocking defect classes:

1. PSF019 broad `игр*` prefix captures 8 toy/non-game identities.
2. PSF014 early zodiac route hides 199 explicit-task identities: 156 meaning, 38 media, 5 toy.
3. PSF001 generic fallback hides 48 explicit DIY/make/craft identities.
4. Step05 queue contains 5 rows duplicating durable current/historical evidence and must be corrected before any provider authorization.

## Correction authority

Execute exactly:

`STEP_04_POST_AUDIT_CORRECTIVE_REWORK_WORK_PROMPT_2026-09-11.md`

Mandatory failure authorities:

- `LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`
- `KW002_EXECUTION_FAILURE_LEDGER_2026-09-11.md`
- `KW002_EXECUTION_FAILURE_LEDGER_ADDENDUM_STEP04_RESULT_AUDIT_2026-09-11.md`

## Execution boundaries

```text
WORDSTAT_CALLS_ALLOWED = 0
ORDINARY_SEARCH_CALLS_ALLOWED = 0
GENSEARCH_CALLS_ALLOWED = 0
AI_SEARCH_CALLS_ALLOWED = 0
STEP03A_MUTATION_ALLOWED = false
STEP03B_MUTATION_ALLOWED = false
STEP05_ADVANCEMENT_ALLOWED = false
STEP06_ADVANCEMENT_ALLOWED = false
ROW_PATCH_ONLY_ALLOWED = false
FULL_VOLUME_RERUN_REQUIRED = true
```

The correction must fix underlying rule logic and rerun all 24,576 normalized identities plus all 25,979 RAW occurrence links. The 255 audit findings are mandatory regression evidence, not the only rows that may be affected.

## Acceptance target

The Work return is only a PASS_CANDIDATE until Main ChatGPT independently verifies it.

Required hard gates include:

```text
RAW_LINEAGE_LOSS = 0
STEP03B_STATE_MUTATIONS = 0
TOY_WITHOUT_GAME_ASSIGNED_BY_IGR_PREFIX = 0
PSF014_EXPLICIT_MEANING_LEAKAGE = 0
PSF014_EXPLICIT_MEDIA_LEAKAGE = 0
PSF014_EXPLICIT_TOY_LEAKAGE = 0
GENERIC_UNQUALIFIED_EXPLICIT_DIY = 0
ALL_PRIOR_BLOCKING_REGRESSIONS = PASS
QUEUE_PROVIDER_READY_DUPLICATE_EVIDENCE = 0
PROVIDER_CALLS = 0
STEP05_ADVANCEMENT = false
STEP06_ADVANCEMENT = false
```

## Stop

Stop after corrected Step04 artifacts, full-volume QA, publication/owner-relay preparation and Work return.

Do not resume Step05 in the same Work execution.
