# KW-001 / OKNO-MSK — STEP 10 FRESH R1 PASS 3 REPORT

Date: 2026-08-30  
Status: **COMPLETE — FULL INDEPENDENT QA / ONE CONSOLIDATED CORRECTION BATCH / REGRESSION PASS**

## Coverage

```text
SOURCE_ROWS = 2840
ACTIVE_ROWS = 2332
PASS3_INDEPENDENTLY_REVIEWED = 2332/2332
FULL_QA_LEDGER_ROWS = 2332
PASS3_SILENT_DROPS = 0
```

Every active row received an independent task-first decision. Preserved deferred and excluded rows were retained without mutation.

## Frozen error ledger and consolidated correction

```text
PASS3_ERROR_LEDGER_ROWS = 876
CONSOLIDATED_CORRECTION_ROWS = 876
CORRECTION_BATCHES_APPLIED = 1
```

The complete error ledger was written before the final assignment artifact. No row-by-row iterative mutation was used.

## Final accounting

```text
FINAL_ASSIGNED_ACTIVE_ROWS = 2319
FINAL_SEARCH_REQUIRED_ACTIVE_ROWS = 13
FINAL_ACTIVE_ACCOUNTED_ROWS = 2332/2332
PRESERVED_DEFERRED_ROWS = 174/174
PRESERVED_EXCLUDED_ROWS = 334/334
UNKNOWN_CLUSTER_IDS = 0
FROZEN_TAXONOMY_CLUSTER_IDS = 62
USED_CLUSTER_IDS = 59
```

## Impact-set recheck

```text
IMPACT_ROWS_RECHECKED = 876/876
REPEAT_DECISION_INSTABILITY = 0
SEMANTIC_INVARIANT_VIOLATIONS = 0
IMPACT_SET_RECHECK = PASS
```

The recheck explicitly guards against known failure modes: branded components attracted into a core Rehau product cluster, technical intent attracted into commercial clusters, photo/design intent placed into selection, aluminium products placed into generic windows, DIY intent placed into professional services, open-balcony intent placed into glazing, and permission intent placed into a commercial service.

## Isolation controls

```text
OLD_STEP10_INPUT_USED = false
BLIND84_INPUT_USED = false
TARGET_CLUSTER_COUNT_USED = false
DIRECT_SERP_TRANSFER_TO_UNPROBED_ROWS = false
```

Step-09 evidence was used only when the exact phrase existed in the direct evidence file.

## Artifact hashes

```text
STEP_10_FRESH_R1_PASS3_FULL_QA_LEDGER.tsv  4b786b1eb7d2a8cd3764184e0ad1792d916032cf6b1d3767cde6f6bfbcb72468
STEP_10_FRESH_R1_PASS3_ERROR_LEDGER.tsv  027f07389809f0e3c12b034e06d322c096b22bce7c0876f46b1121f7f37bc997
STEP_10_FRESH_R1_PASS3_CONSOLIDATED_CORRECTIONS.tsv  8bc20cbae3f1b8602b10d68cf3edb5422918085cbc956aa1a5feb06324576a38
STEP_10_FRESH_R1_ASSIGNMENTS_FINAL.tsv  ea2cc5760e71c1564bc189692be218f7af95cd35995334d523c4b985bdeacb68
STEP_10_FRESH_R1_CLUSTER_SUMMARY_FINAL.tsv  83535756c151bee301b4d99c38719c239318c54471c974eecb42a63955f0d91a
STEP_10_FRESH_R1_PASS3_IMPACT_RECHECK.tsv  24dad85eb869544fea32a6b9c6bf68a36670d8c205f027ae39a90b8c6dd86a6e
STEP_10_FRESH_R1_FINAL_QA.json  07cab0d9a0a99e7753c67c47e164ffafdc47825e50fe1387f147531f3f3191d9
```

## Verdict

```text
STEP10_FRESH_R1_PASS1 = COMPLETE
STEP10_FRESH_R1_PASS2 = COMPLETE
STEP10_FRESH_R1_PASS3 = COMPLETE
STEP10_FRESH_R1_COMPLETE_ERROR_LEDGER = FROZEN
STEP10_FRESH_R1_CONSOLIDATED_CORRECTION_BATCH = PASS_ONE_BATCH
STEP10_FRESH_R1_FULL_ACCOUNTING_REGRESSION = PASS
STEP10_FRESH_R1_IMPACT_SET_SEMANTIC_RECHECK = PASS
STEP10_FRESH_R1_FINAL_STATUS = COMPLETE
```
