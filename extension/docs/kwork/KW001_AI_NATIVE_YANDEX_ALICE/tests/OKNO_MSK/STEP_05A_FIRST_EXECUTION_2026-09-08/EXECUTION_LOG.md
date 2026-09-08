# KW-001 / OKNO_MSK — Step 5A first execution log

Date: 2026-09-08

## Durable blocks

| Block | Result | Remote commit / readback |
|---|---|---|
| 0. Baseline / reuse inventory | PASS | `925a00b528a48f6e2825cb892fa4c445f010ac90` / PASS |
| A. Combined 75-query / 750-row ledger | PASS | `ca3178fff1630ebd3ef8dddf4aa1cd2c512ca941` / PASS |
| B. Domain frequency / classification | PASS | `918c414822760f6b9ab0f317f2922f10f5fc27ad` / PASS |
| C. Query impact trace | PASS | `31c9ecb0ca43d2da901ce3dc22203bb0059e7003` / PASS |
| D. Candidate selection / report / final QA | PASS | `9376000ef969ce335da99df1846a0674e3295260` / PASS |

Finalization readback confirmed the remote branch HEAD, all ten isolated execution files, the `751 / 238 / 76 / 12` physical line counts for combined/domain/impact/candidate TSV files, the final QA payload and exact remote/local tree equality.

## Acquisition boundary

```text
NEW_YANDEX_SEARCH_CALLS = 0
NEW_WORDSTAT_CALLS = 0
NEW_ALICE_CALLS = 0
NEW_GENSEARCH_CALLS = 0
NEW_WEBMASTER_CALLS = 0
NEW_METRIKA_CALLS = 0
NEW_DIRECT_CALLS = 0
NEW_PAID_PROVIDER_COST_RUB = 0
PUBLIC_COMPETITOR_PAGE_INSPECTION = false
```

## Scope protection

All task changes remain under `STEP_05A_FIRST_EXECUTION_2026-09-08/`. The corrected client release, Documents 01–03, semantic-core XLSX and historical Step 0–20 outputs were not modified.

## Final routing

```text
PROJECT_TEST_VALIDATED = false
OWNER_REVIEW = PENDING
NEXT_ACTION = OWNER_REVIEW_STEP_05A_FIRST_EXECUTION__THEN_AUTHORIZE_SELECTED_COMPETITOR_PAGE_INSPECTION_IF_ACCEPTED
```
