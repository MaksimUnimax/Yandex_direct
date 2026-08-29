# KW-001 / OKNO-MSK — STEP 07B ROW-LEVEL CLEANUP ACCEPTANCE

Date: 2026-08-29  
Status: **COMPLETE / PASS / JOB-SPECIFIC**

## 1. Step goal

Transform the completely preserved Wordstat acquisition evidence into one accountable row-level working dataset in which every exact normalized phrase is explicitly classified while preserving all source occurrences and without making downstream Search/page-architecture decisions prematurely.

This step is semantic cleanup only. It does not freeze the final semantic set, perform Yandex SERP clustering, assign page ownership, make final merge/create-page decisions, or use AI-search evidence.

## 2. Authoritative input

The accepted input is the union of:

```text
repaired first-pass Wordstat rows = 2415
preserved targeted-probe rows = 550
TOTAL source rows = 2965
```

Section accounting:

```text
result rows = 2636
association rows = 329
TOTAL = 2965
```

No new provider call was made for this cleanup step.

```text
provider requests executed = 0
provider cost = 0 RUB
```

## 3. Cleanup method applied

The working dataset was built reproducibly from the stored normalized TSV evidence using `STEP_07B_ROW_LEVEL_CLEANUP_BUILD.py`.

Controls:

```text
exact phrase equality only for deduplication
all duplicate source occurrences preserved in provenance
low frequency alone never triggers exclusion
associations are never automatically promoted to KEEP
business/page-boundary uncertainty remains REVIEW
explicit out-of-region queries are separated as EXCLUDE_SCOPE
unrelated meanings are separated as EXCLUDE_IRRELEVANT
malformed/truncated mechanical rows are separated as EXCLUDE_MECHANICAL
```

The five accepted row-level statuses are:

```text
KEEP
REVIEW
EXCLUDE_SCOPE
EXCLUDE_IRRELEVANT
EXCLUDE_MECHANICAL
```

`REVIEW` is a valid cleanup decision, not an unprocessed row. It intentionally preserves phrases whose business or page boundary requires later ordinary Yandex Search and/or existing-site evidence.

## 4. Exact deduplication accounting

```text
source rows = 2965
unique exact normalized phrases = 2840
duplicate source occurrences collapsed into existing phrase keys = 125
phrase keys with more than one source occurrence = 101
```

No source occurrence is discarded from audit history. The occurrence-level table retains all 2965 original normalized rows, while the canonical working table stores all source provenance for each of the 2840 exact phrase keys.

## 5. Complete classification accounting

```text
KEEP = 1760
REVIEW = 749
EXCLUDE_SCOPE = 180
EXCLUDE_IRRELEVANT = 120
EXCLUDE_MECHANICAL = 31
--------------------------------
STATUS TOTAL = 2840
```

Reconciliation:

```text
status total = unique exact phrases = 2840
canonical provenance occurrence sum = original source rows = 2965
unclassified phrases = 0
```

Therefore every unique phrase and every original source occurrence is accountable.

## 6. Preserved artifacts

```text
STEP_07B_ROW_LEVEL_CLEANUP_BUILD.py
STEP_07B_ROW_LEVEL_CLEANUP_WORKING.tsv
STEP_07B_ROW_LEVEL_CLEANUP_OCCURRENCES.tsv
STEP_07B_ROW_LEVEL_CLEANUP_SUMMARY.json
```

Content SHA-256 recorded by the verified builder:

```text
STEP_07B_ROW_LEVEL_CLEANUP_WORKING.tsv
929b6439e9ace1f269987a046af19ac0a3bc107d4fa90c8320c968817392bc2d

STEP_07B_ROW_LEVEL_CLEANUP_OCCURRENCES.tsv
a5e3fceb5647d1f9fbbd5fa3ace9feebb8665a228173ad14fb8b73d846584d63
```

The generated working TSV contains one header plus 2840 canonical phrase rows. The occurrence TSV contains one header plus 2965 source-occurrence rows.

The temporary GitHub Actions workflow used only to execute the reproducible builder on the branch was removed after the generated artifacts were verified. The builder itself remains as an audit/reproduction artifact.

## 7. Important interpretation limits

The following claims are **not** made by this acceptance:

```text
KEEP does not mean a separate landing page is required
REVIEW does not mean a phrase is low quality or should be excluded
EXCLUDE_* does not mean the underlying topic can never matter in another business scope
2840 unique phrases are not 2840 semantic clusters
1760 KEEP phrases are not yet the final Search-only semantic set
page architecture is not complete
ordinary Yandex Search validation has not yet been performed for the unresolved boundaries
AI-search evidence has not been used in this step
```

## 8. Non-repeat controls

This step specifically prevents recurrence of the earlier OKNO-MSK failures:

```text
technical success is not accepted without complete reusable data
family-level triage is not mislabeled as row-level cleanup
all 2965 input occurrences are quantitatively reconciled
all 2840 unique phrases receive an explicit status/reason
association count is not treated as final-keyword authority
low frequency alone is not used as an exclusion rule
ambiguous commercial boundaries are retained rather than silently deleted
```

## 9. Verdict

```text
ROW_LEVEL_CLEANUP_VERDICT = COMPLETE
INPUT_ROWS_VERIFIED = 2965
UNIQUE_EXACT_PHRASES = 2840
DUPLICATE_OCCURRENCES = 125
KEEP = 1760
REVIEW = 749
EXCLUDE_SCOPE = 180
EXCLUDE_IRRELEVANT = 120
EXCLUDE_MECHANICAL = 31
UNCLASSIFIED = 0
PROVENANCE_RECONCILIATION = PASS
PROVIDER_REQUESTS_EXECUTED = 0
PROVIDER_COST_RUB = 0
FINAL_SEMANTIC_SET_COMPLETE = false
PAGE_ARCHITECTURE_COMPLETE = false
NEXT_STEP_ALLOWED = true
```

Next major step: freeze the cleaned working semantic set that is allowed to proceed into ordinary Yandex Search validation, without prematurely resolving the retained `REVIEW` boundaries.
