# OKNO_MSK — KW-001 VOLUME-SCALING RETROACTIVE IMPACT NOTE

Date: 2026-09-10  
Status: **NO AUTOMATIC REBUILD REQUIRED / HISTORICAL RESULT PRESERVED**

This note records the effect of the 2026-09-10 KW-001 universal data-volume/scalability correction on the existing OKNO_MSK rehearsal/release.

## Current accepted size reference

The corrected release manifest records:

```text
all_unique_phrases = 2840
active_phrases = 2332
canonical_clusters = 168
search_required_phrases = 19
```

These counts are historical/current job facts only. They are not promoted into universal KW-001 method limits.

## Decision

The universal addition of Step3A normalization and Step3B early sanitation does **not** by itself invalidate the current OKNO_MSK semantic core.

```text
2332 ACTIVE PHRASES != AUTOMATIC OVERSIZE DEFECT
KW002 1500 DELIVERY CEILING != KW001 LIMIT
```

No phrase is to be deleted merely to force the existing KW-001 result below 1500 or another arbitrary number.

## When backfill would become required

A normalization/sanitation backfill for OKNO_MSK is required only if one of the following occurs:

```text
Step2/3/4/5/5A/7 is materially reopened
new large acquisition is added
an independent duplicate/noise/scalability defect is demonstrated
owner explicitly orders retrospective migration
```

Otherwise the existing release remains governed by its accepted historical authorities and current post-release correction gates.

## Future job rule

All new KW-001 jobs, including larger catalog sites, must use:

`DATA_VOLUME_NORMALIZATION_AND_SANITATION_GATE.md`

before Step4 and after every material acquisition expansion.

This note prevents the universal scalability fix from being misread as an order to rewrite an already accepted client result solely because its active core contains more than 1500 phrases.