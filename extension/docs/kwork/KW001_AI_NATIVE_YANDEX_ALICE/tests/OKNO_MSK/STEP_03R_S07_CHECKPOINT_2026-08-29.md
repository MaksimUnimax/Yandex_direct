# KW-001 OKNO_MSK — Step 3R S07 checkpoint

Seed: `остекление балкона с крышей`
Job: `kw001-okno-msk-wordstat-pass1-repair-20260829`
Request ID: `wordstat-batch-b9697896-4903-4fd7-b306-b7ac721aa63a`
Region: `213`
Devices: `DEVICE_ALL`
numPhrases: `200`

## Provider outcome

- status: `OK`
- HTTP: `200`
- request_executed: `true`
- automatic_retry: `false`
- outcome_unknown: `0`
- item cost: `0.02 RUB`
- batch estimated cost after S07: `0.14 RUB`
- totalCount: `48`

## Preservation reconciliation

- results rows returned: `6`
- results rows saved: `6`
- results rows verified: `6`
- association rows returned: `13`
- association rows saved: `13`
- association rows verified: `13`
- total data rows returned: `19`
- total data rows saved: `19`
- total data rows verified: `19`

Raw file: `STEP_03R_S07_RAW_PROVIDER_RESULT_2026-08-29.json`

## Non-repeat control

Past Step-3 failure was treating provider success as collection completion while preserving only examples. For S07 the complete returned `results[]` and `associations[]` were preserved and the saved file was reopened and verified before allowing S08.

`CURRENT_ITEM_COMPLETE = true`
`NEXT_PROVIDER_ITEM_ALLOWED = true`
`NON_REPEAT_CONTROLS = PASS`
