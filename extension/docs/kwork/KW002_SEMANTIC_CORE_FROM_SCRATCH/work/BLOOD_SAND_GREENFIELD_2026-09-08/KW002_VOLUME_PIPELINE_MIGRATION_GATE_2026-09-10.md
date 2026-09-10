# BLOOD & SAND — KW-002 VOLUME-PIPELINE MIGRATION GATE

Date: 2026-09-10
Status: **STEP05 REMAINS PAUSED / METHODOLOGY MIGRATION REQUIRED AFTER STEP04 LIMITED-REWORK PUBLICATION**

This is a job-specific migration gate created because the universal KW-002 methodology was revised after the Blood & Sand rehearsal had already completed Step03 and original Step04.

## Current preserved truth

```text
STEP03 RAW = COMPLETE / 79 of 79 primary probes
RESULT OCCURRENCES = 24722
ASSOCIATION OCCURRENCES = 1257
TOTAL RAW OCCURRENCES = 25979
STEP04 ORIGINAL = audited at 87/100
STEP04 LIMITED REWORK = computed locally / publication recovery in progress separately
STEP05 = one historical E013 provider observation exists, then paused
```

## What changes

The 25,979 Step03 occurrences remain the lossless evidence layer. They are NOT invalidated and must not be reacquired solely because methodology changed.

They also must no longer be treated as 25,979 equal semantic-analysis units.

Before Step05 resumes, this job must backfill the new universal gates:

```text
Step03 RAW 25,979 occurrences
-> Step03A NORMALIZED_UNIQUE_POOL
-> Step03B SANITIZED_CANDIDATE_POOL / HOLD / AUTO_EXCLUDED
-> reconcile corrected Step04 family state against sanitized candidates
-> materialize candidate-count funnel
-> establish DELIVERY_KEYWORD_CAP for this rehearsal/productization test
-> freeze pre-Step05 migration baseline
```

## Historical Step05 E013 boundary

The already executed `!чётки` E013 result remains valid historical Step05 evidence.

It must NOT be used to rewrite the historical end-of-Step04 baseline or the limited Step04 correction.

After the migration baseline is frozen, E013 may be passed through the same normalization/sanitation rules as any other Step05 acquisition before union with the current candidate pool.

## No provider calls for migration

```text
WORDSTAT_REPLAY_REQUIRED = false
SEARCH_REQUIRED = false
GENSEARCH_REQUIRED = false
AI_SEARCH_REQUIRED = false
```

The migration is a deterministic transformation/reconciliation of already preserved evidence.

## Required migration outputs

At minimum:

```text
STEP_03A_NORMALIZED_UNIQUE_POOL_*.tsv
STEP_03A_NORMALIZATION_QA_*.md
STEP_03B_SANITIZED_CANDIDATE_POOL_*.tsv
STEP_03B_EXCLUDED_HOLD_REGISTER_*.tsv
STEP_03B_SANITATION_QA_*.md
STEP_04_POST_SANITATION_RECONCILIATION_*.md
KW002_DATA_FUNNEL_*.json
```

The funnel must report:

```text
raw_occurrence_rows = 25979
normalized_unique_rows = N
implicit_duplicate_groups = N
collapsed_duplicate_rows = N
auto_excluded_rows = N
hold_ambiguous_rows = N
sanitized_candidate_rows = N
valid_reserve_rows = N when available
delivery_cap = N once frozen
```

## Resume gate

Step05 cannot resume until Main ChatGPT/owner accepts the migration outputs and confirms that the working candidate set is appropriately compact and traceable.
