# KW-001 / OKNO-MSK — Step 09 initial Search tranche reconciliation

Date: 2026-08-29
Status: **CORRECTED AFTER SEMANTIC-MANIFEST AUDIT**

```text
REVIEW_SEARCH_ROWS = 944
REVIEW_SEARCH_REASONS = 23
REVIEW_SAMPLING_STRATA = 40
ACTIVE_DUPLICATE_GROUPS = 8
PROBE_COUNT = 75
DIRECT_REVIEW_SEARCH_ROWS = 45
UNRESOLVED_UNPROBED_REVIEW_SEARCH_ROWS = 899
TRACEABILITY_COMPLETE = true
FULL_SERP_EVIDENCE_COVERAGE = false
PRE_SERP_TRANSFER_LINKS = 0
SEMANTIC_SAMPLE_QA_PASS = true
MAX_REQUESTS = 80
ESTIMATED_COST_RUB = 36.6
MAX_COST_RUB = 39.04
PROVIDER_EXECUTION_ALLOWED = true
PROVIDER_EXECUTION_SCOPE = INITIAL_BOUNDED_TRANCHE_ONLY
PROVIDER_REQUESTS_EXECUTED_DURING_BUILD = 0
PROVIDER_COST_RUB_DURING_BUILD = 0
```

## Corrected interpretation

The previous builder incorrectly treated `corrected_reason` and acquisition source as if they created transferable SERP evidence families. They do not.

The 40 REVIEW_SEARCH selections are now only **stratified direct samples** used to obtain diverse first-tranche evidence. They may resolve the exact queried phrase and help identify further questions, but they do not pre-resolve or represent the other rows in the same cleanup-reason/source stratum.

Every non-probed REVIEW_SEARCH row is explicitly `UNRESOLVED_UNPROBED`. Evidence transfer may occur only after observed SERP evidence and a separate analytical transfer decision.

All eight active non-exact duplicate groups still contribute both variants for direct comparison. Step-01/core anchors remain direct comparison controls.

`traceability_complete=true` means all 944 rows are still present in the ledger. It does **not** mean full Search evidence coverage.
