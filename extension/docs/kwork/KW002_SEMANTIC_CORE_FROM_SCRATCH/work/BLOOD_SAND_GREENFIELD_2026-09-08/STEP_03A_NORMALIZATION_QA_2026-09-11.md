# KW-002 Blood & Sand — Step03A normalization QA

Date: 2026-09-11  
Status: **COMPLETE / PASS CANDIDATE / MAIN CHATGPT RETURN QA REQUIRED**

## Source and method

- Input is the complete accepted 79/79 Step03 RAW evidence tree; no Step05 evidence is used.
- All 96 local evidence files were byte-read before transformation: `2136069` bytes; tree digest `6dfb0b600984a1e677c30393e17e1c99b272df06eaf15568672d7a6022d488af`.
- Accepted reconstructed re-query payloads were decoded locally and verified against their frozen byte counts and SHA-256 identities.
- All 79 provider outcomes were parsed; generated `phrase/count` sequences match the corrected 25,979-row occurrence carrier exactly, with 0 sequence mismatches.
- Exact normalization is limited to Unicode NFC, outer trim, internal whitespace collapse and case-folded comparison. Digits, punctuation and hyphens remain meaningful.
- Implicit candidates are detected only by equal alphanumeric token multisets; all three structured numeric groups remain `HOLD_AMBIGUOUS` and are not collapsed.
- Observed counts are retained as lineage values and are never summed as independent demand across duplicate occurrences.

## Mechanical accounting

```text
RAW_OCCURRENCES = 25979
RESULT_OCCURRENCES = 24722
ASSOCIATION_OCCURRENCES = 1257
NORMALIZATION_LEDGER_ROWS = 25979
UNIQUE_OCCURRENCE_IDS = 25979
UNMAPPED_RAW_OCCURRENCES = 0
DUPLICATE_OCCURRENCE_IDS = 0
NORMALIZED_UNIQUE_ROWS = 24576
EXACT_DUPLICATE_GROUPS = 1181
COLLAPSED_EXACT_DUPLICATE_OCCURRENCES = 1403
IMPLICIT_DUPLICATE_GROUPS = 3
IMPLICIT_ACCEPTED_GROUPS = 0
IMPLICIT_HOLD_GROUPS = 3
RAW_LINEAGE_LOSS = 0
NORMALIZED_ACCOUNTING = PASS
```

No provider, Search, GenSearch or AI-search call was executed.
