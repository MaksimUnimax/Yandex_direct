# KW-002 Blood & Sand — post-sanitation Step04 reconciliation preparation

Date: 2026-09-11  
Status: **RECONCILIATION-READY SUMMARY / CORRECTED STEP04 NOT REWRITTEN**

## Boundary

Step03A/03B sanitation was completed independently from corrected Step04 family assignments. This document is the first downstream join. It maps the immutable corrected Step04 occurrence IDs to the independently assigned Step03B states; it does not change any corrected Step04 artifact and does not advance Step05.

## Summary

```text
NORMALIZED_UNIQUE_ROWS = 24576
SANITIZED_CANDIDATE_ROWS = 5074
HOLD_ROWS_NEEDING_FAMILY_CONTEXT = 12750
CORRECTED_STEP04_OCCURRENCES_MAPPING_TO_AUTO_EXCLUDED = 7243
CORRECTED_STEP04_OCCURRENCES_REMAINING_ACTIVE_CANDIDATES = 5236
CORRECTED_STEP04_OCCURRENCES_MAPPING_TO_HOLD = 13500
CORRECTED_STEP04_OCCURRENCES_RECONCILED = 25979
CORRECTED_STEP04_FAMILY_ROWS_TOTAL = 31
CORRECTED_STEP04_OBSERVED_FAMILY_ROWS = 25
CORRECTED_STEP04_FAMILY_ROWS_AFFECTED_BY_SANITATION = 24
DEDICATED_POST_SANITATION_STEP04_WORK_PASS_REQUIRED = YES
```

Why a dedicated pass is required: corrected Step04 was built over RAW occurrence families. The independently sanitized candidate universe now separates retained candidates, explicit exclusions and unresolved HOLD identities. Main ChatGPT must accept the migration outputs before a future Work pass may reconcile family scope; this summary does not perform that rewrite.

## Corrected family occurrence mapping

| family_id | source occurrences | KEEP | HOLD | AUTO_EXCLUDED |
|---|---:|---:|---:|---:|
| F001 | 3 | 3 | 0 | 0 |
| F002 | 70 | 64 | 1 | 5 |
| F003 | 146 | 140 | 5 | 1 |
| F004 | 691 | 667 | 14 | 10 |
| F005 | 200 | 195 | 1 | 4 |
| F006 | 106 | 2 | 103 | 1 |
| F007 | 249 | 0 | 232 | 17 |
| F008 | 2042 | 52 | 1890 | 100 |
| F009 | 506 | 358 | 137 | 11 |
| F010 | 1263 | 408 | 834 | 21 |
| F011 | 244 | 188 | 48 | 8 |
| F012 | 5022 | 0 | 4825 | 197 |
| F013 | 1094 | 97 | 951 | 46 |
| F014 | 1314 | 4 | 102 | 1208 |
| F015 | 489 | 0 | 1 | 488 |
| F016 | 234 | 0 | 70 | 164 |
| F017 | 1680 | 0 | 208 | 1472 |
| F018 | 809 | 1 | 424 | 384 |
| F019 | 127 | 0 | 59 | 68 |
| F020 | 143 | 0 | 50 | 93 |
| F021 | 5673 | 0 | 3053 | 2620 |
| F022 | 104 | 0 | 0 | 104 |
| F023 | 294 | 0 | 227 | 67 |
| F024 | 116 | 5 | 111 | 0 |
| F025 | 3360 | 3052 | 154 | 154 |
| F026 | 0 | 0 | 0 | 0 |
| F027 | 0 | 0 | 0 | 0 |
| F028 | 0 | 0 | 0 | 0 |
| F029 | 0 | 0 | 0 | 0 |
| F030 | 0 | 0 | 0 | 0 |
| F031 | 0 | 0 | 0 | 0 |

Zero-occurrence coverage-gap families remain recorded and are not converted into observed candidates.
