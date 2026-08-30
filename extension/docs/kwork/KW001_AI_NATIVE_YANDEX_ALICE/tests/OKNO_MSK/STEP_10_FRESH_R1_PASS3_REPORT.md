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
PASS3_ERROR_LEDGER_ROWS = 927
CONSOLIDATED_CORRECTION_ROWS = 927
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
IMPACT_ROWS_RECHECKED = 927/927
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
STEP_10_FRESH_R1_PASS3_FULL_QA_LEDGER.tsv  9640f97eb3d5a981ee76ad4467dc07653c143f9ba13fabecd9cc25e812aefaf4
STEP_10_FRESH_R1_PASS3_ERROR_LEDGER.tsv  e1cd59943d73fd401456da659894716ebd2b667f65939e9da82ab17cefdff44e
STEP_10_FRESH_R1_PASS3_CONSOLIDATED_CORRECTIONS.tsv  fe40fbc98193cc1f2041004ae0dd973516084f7469ff518734ccd20941fcabe0
STEP_10_FRESH_R1_ASSIGNMENTS_FINAL.tsv  ad97b8873b4dee78a1c9453cc6fe9ec8efb1cf1b9d18c436bd0475dd088b15c7
STEP_10_FRESH_R1_CLUSTER_SUMMARY_FINAL.tsv  5216f1345fcb190e0e016b67725ba2e42ad4725e59acd5c4c3155f8097ae172e
STEP_10_FRESH_R1_PASS3_IMPACT_RECHECK.tsv  6ddd40142b83e66b64cc166da937d47e62c3d9b39c17f050b1ecd2e07e347a9c
STEP_10_FRESH_R1_FINAL_QA.json  f727e5b55fdcf741ea45341a3e2e67b089d63d4ca8bfcf94a71cd83e355da990
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
