# KW-002 Blood & Sand — execution failure ledger addendum: Step04 independent result audit

Date: 2026-09-11
Status: **ACTIVE JOB-SPECIFIC ANTI-REGRESSION AUTHORITY**

Companion authorities:

- `LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`
- `KW002_EXECUTION_FAILURE_LEDGER_2026-09-11.md`
- `STEP_04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT_MAIN_CHATGPT_REVIEW_2026-09-11.md`

This addendum records three new concrete failure classes discovered only after independent full-volume auditing of the post-sanitation Step04 result. Later Step04/05+ work must read this addendum until its rules are merged into a later consolidated failure ledger.

## Failure 11 — broad game morphology `игр*` captured toys

Observed:

```text
CURRENT_FAMILY = PSF019
TOY_WITHOUT_GAME_IDENTITIES = 8
ROOT_CAUSE = has_token_prefix(..., "игр")
```

The broad prefix intended to detect game morphology also matches `игрушка`, `игрушки` and sibling toy forms.

Permanent lesson:

```text
MORPHOLOGICAL STEM MUST NOT CROSS LEXEME BOUNDARIES
```

A prefix convenience rule is not sufficient when another common lexeme shares the same initial characters.

Required regression gates:

```text
TOY_WITHOUT_EXPLICIT_GAME_SIGNAL_ASSIGNED_PSF019 = 0
BROAD_IGR_PREFIX_USED_AS_GAME_PROOF = false
GAME_SIGNAL_REQUIRES_BOUNDED_EXACT_MORPHOLOGY_OR_NAMED_GAME_CONTEXT = true
```

Representative mandatory tests include at least:

- `игрушка оберег` must not be routed as GAME solely by `игр*`;
- `игрушка талисман` must not be routed as GAME solely by `игр*`;
- `алатырь игрушки` must not be routed as GAME solely by `игр*`;
- explicit `игра`, `играть`, `игровой`, named-game contexts must still be detected as game signals where supported.

## Failure 12 — high-level zodiac branch erased more informative user-task signals

Observed:

```text
CURRENT_FAMILY = PSF014
AFFECTED_UNIQUE_IDENTITIES = 199
MEANING = 156
MEDIA = 38
TOY = 5
```

The Step04 zodiac branch runs early. It checks product/commerce/form, visual, a limited ASTRO_INFO list and stone, then falls through to `PSF014`. General MEANING, MEDIA and TOY signals are not evaluated before the unqualified-zodiac fallback.

Permanent lesson:

```text
BROAD TOPIC CONTEXT MUST NOT ERASE A MORE INFORMATIVE EXPLICIT USER TASK
```

A phrase may be zodiac-related and still clearly ask for meaning, media consumption or a physical object type. Preliminary family routing must preserve the more informative task dimension while retaining zodiac as context.

Required regression gates:

```text
PSF014_ROWS_WITH_EXPLICIT_MEANING_SIGNAL = 0
PSF014_ROWS_WITH_EXPLICIT_MEDIA_SIGNAL = 0
PSF014_ROWS_WITH_EXPLICIT_TOY_SIGNAL = 0
ZODIAC_CONTEXT_MAY_COEXIST_WITH_TASK_MARKER = true
FINAL_INTENT_INFERRED_FROM_TASK_MARKER = false
```

The correction must re-evaluate the complete zodiac blast radius, not only the 199 currently identified rows.

## Failure 13 — generic product fallback flattened explicit DIY/make/craft tasks

Observed:

```text
CURRENT_FAMILY = PSF001
EXPLICIT_DIY_IDENTITIES = 48
```

Examples of task vocabulary include `сделать`, `создать`, `изготовить`, `связать`, `сшить`, `сплести`, `своими руками` and equivalent make/craft formulations.

The current generic KEEP routing contains no DIY boundary before product-word fallback to PSF001.

Permanent lesson:

```text
GENERIC PRODUCT WORD != UNQUALIFIED TASK WHEN EXPLICIT ACTION IS PRESENT
```

Required regression gates:

```text
PSF001_ROWS_WITH_EXPLICIT_DIY_SIGNAL = 0
DIY_PRELIMINARY_TASK_MARKER_OR_FAMILY = PRESENT
DIY_MARKER_DOES_NOT_IMPLY_FINAL_PAGE_OR_FINAL_INTENT = true
```

The full active/HOLD universe must be rerun so sibling DIY rows are found by the rule, not patched from an audit list.

## Failure 14 — expansion queue can remain mechanically valid while duplicating already durable evidence

Independent queue audit found:

```text
CURRENT_QUEUE_ROWS = 13
DUPLICATES_EXISTING_EVIDENCE = 5
VALID_GAP = 2
OWNER_FACT_FIRST = 5
DEFER_TO_LATER_INTENT_OR_SERP = 1
```

Duplicate/partially duplicate queue rows: PSQ005, PSQ006, PSQ007, PSQ008, PSQ010.

Permanent lesson:

```text
COVERAGE_GAP HYPOTHESIS MUST BE RECONCILED AGAINST ALL DURABLE EXISTING EVIDENCE BEFORE PROVIDER AUTHORIZATION
```

Required regression gates:

```text
QUEUE_ROW_WITH_EXISTING_EQUIVALENT_EVIDENCE_MARKED_PROVIDER_READY = 0
HISTORICAL_E013_REPLAY_ALLOWED_WITHOUT_NEW_GAP = false
PROPOSED_PROVIDER_PROBE_HAS_INCREMENTAL_INFORMATION_GAIN = true
```

## Corrective-pass hard rule

The accepted independent audit is a defect oracle and regression authority, not a 255-row patch list.

```text
FIX UNDERLYING RULES
-> RERUN COMPLETE 24,576 NORMALIZED IDENTITIES
-> REMATERIALIZE ALL 25,979 OCCURRENCE LINKS
-> REBUILD FAMILY AUTHORITY / QUEUE / FEEDBACK
-> RUN OLD + NEW REGRESSIONS
-> INDEPENDENT RETURN QA
```

Do not mutate Step03B in this correction. Do not execute Step05 or any provider call.
