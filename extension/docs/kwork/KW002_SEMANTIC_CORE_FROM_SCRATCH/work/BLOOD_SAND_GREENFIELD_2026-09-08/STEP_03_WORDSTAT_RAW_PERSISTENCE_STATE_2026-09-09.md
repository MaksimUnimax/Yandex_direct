# STEP 03 — WORDSTAT RAW PERSISTENCE STATE

Original date: 2026-09-09
Current correction date: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Status: **FINAL CORRECTED / ACQUISITION COMPLETE / DURABLE RAW 79/79 / PASS**

## Current authority

A Step-04 Work readiness check on 2026-09-09 correctly found that the then-current Git feed-forward corpus was only 60/79 losslessly usable because two historical large carrier bundles were corrupted. That finding remains historical evidence and is not deleted.

The owner then authorized recovery/re-query where lossless source rehydration was insufficient. Recovery is now complete.

```text
CANONICAL_PRIMARY_MANIFEST_ROWS = 79
CANONICAL_PRIMARY_RUN_ORDER = 1..79
CANONICAL_PRIMARY_PROBES_WITH_CURRENT_ACQUISITION_OUTCOME = 79
STEP03_PROVIDER_ACQUISITION = COMPLETE / 79 OF 79
INITIAL_LATE_QA_LOSSLESS_FEED_FORWARD_RAW = 60 OF 79
RECOVERED_AFFECTED_RUN_ORDERS = 32-48,50,51
CURRENT_LOSSLESS_GITHUB_FEED_FORWARD_RAW = 79 OF 79
STEP03_DURABLE_RAW_COMPLETE = true
STEP03_DURABLE_RAW = COMPLETE / PASS
STEP03_REMAINING_RECOVERY = 0
RECOVERY_PROVIDER_REQUESTS = 17
RECOVERY_PROVIDER_ESTIMATED_COST_RUB = 0.34
```

## Replacement-carrier authority

The broken historical bundles remain preserved as provenance evidence and are **not** repaired by pretending their historical bytes now match. For current downstream feed-forward, use the complete replacement carriers recorded in:

`STEP_03_RAW_RECOVERY_PROGRESS_2026-09-09.json`

That progress authority maps every recovered run order to its current durable path/request identity.

For affected runs:

```text
32-48 -> current RECOVERY_REQUERY__<run_order>__<fresh_request_id>.raw.txt carriers
50-51 -> RECOVERED__050/051 durable empty-object outcomes
49 -> independently readable original carrier; no recovery required
```

Fresh request IDs never replace historical request IDs. Historical bundle manifests remain useful as historical structural controls only; their broken binary parts are not a required Step04 input now that complete replacement row-level carriers exist.

## Final verification authorities

- `STEP_03_RAW_RECOVERY_PROGRESS_2026-09-09.json`
- `STEP_03_RAW_RECOVERY_FINAL_RECEIPT_2026-09-10.md`
- `STEP_03_RAW_RECOVERY_REQUERY_048_RECEIPT_2026-09-10.md`
- `STEP_03_RAW_RECOVERY_COMPLETION_STATE_2026-09-10.json`

Final run 48 independently closed the last missing position:

```text
phrase = знак зодиака Телец
fresh_request_id = wordstat-9d96a936-b280-4cfb-abb0-5f4a280acd13
results_rows = 594 / direct remote line-position count
associations_rows = 15 / direct remote line-position count
totalCount = 37962
raw_blob_sha = e7e9e63d666ab5af0603ed582a3720abfcda33c0
remote_readback = PASS
```

## Downstream rule

```text
WORDSTAT_PRIMARY_ACQUISITION_COMPLETE = true
STEP03_DURABLE_RAW_COMPLETE = true
STEP03_DURABLE_FEED_FORWARD = 79/79
STEP03_RAW_RECOVERY = COMPLETE / PASS
ADDITIONAL_RECOVERY_PROVIDER_REQUEST_REQUIRED = false
```

This file no longer blocks Step04 for RAW incompleteness. Step04 authorization is controlled separately by `LEVEL2/STEP04_OWNER_EXECUTION_GATE_2026-09-10.md` and the Work handoff rule.
