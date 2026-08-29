# KW-001 / OKNO-MSK — Step 09 Search probe manifest reconciliation

Date: 2026-08-29

```text
REVIEW_SEARCH_ROWS = 944
REVIEW_SEARCH_REASONS = 23
EVIDENCE_QUESTIONS = 40
ACTIVE_DUPLICATE_GROUPS = 8
PROBE_COUNT = 75
MAX_REQUESTS = 80
UNIT_COST_RUB = 0.488
ESTIMATED_COST_RUB = 36.6
MAX_COST_RUB = 39.04
COVERAGE_COMPLETE = true
REQUEST_CAP_OK = true
BUDGET_CAP_OK = true
PROVIDER_EXECUTION_ALLOWED = true
PROVIDER_REQUESTS_EXECUTED_DURING_BUILD = 0
PROVIDER_COST_RUB_DURING_BUILD = 0
```

Every `REVIEW_SEARCH` row is preserved in `STEP_09_REVIEW_SEARCH_COVERAGE.tsv`.
Rows not directly probed stay explicitly `REPRESENTED_BY_QUESTION_UNRESOLVED`; this manifest does not resolve them by inference.
The broad boundary reason is split by acquisition source so its 575 rows are not collapsed into one query.
All eight active non-exact duplicate groups contribute both observed variants before any merge.
The provider command is emitted only if the 80-request and 39.04-RUB hard gates pass.
