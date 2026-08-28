# KW-001 OKNO_MSK — Step 03 checkpoint S12

Status: ACQUISITION CHECKPOINT / RAW WORDSTAT EVIDENCE

## Batch state after S12

- job_id: `kw001-okno-msk-wordstat-pass1-20260828`
- item: `S12`
- seed: `аксессуары для пластиковых окон`
- method: `getTop`
- region: `213` (Moscow)
- devices: `DEVICE_ALL`
- numPhrases: `200`
- item status: `SUCCEEDED`
- request_executed: `true`
- request_id: `wordstat-batch-f9d7cfe3-4f3a-4864-8a03-75916491479e`
- HTTP: `200`
- elapsed_ms: `1580`
- estimated item cost: `0.02 RUB`

Batch progress:
- succeeded: `12/18`
- pending: `6`
- failed_terminal: `0`
- outcome_unknown: `0`
- requests_started: `12`
- estimated total cost: `0.24 RUB`
- next_safe_action: `CLAIM_NEXT`

## Raw acquisition observations

Provider root `totalCount = 29`.

Direct result examples preserved from the provider response:
- `аксессуары для пластиковых окон` — 29
- `для пластикового окна аксессуары gu` — 13
- `аксессуары для пластиковых окон купить` — 3
- `аксессуары для пластиковых окон и дверей` — 2

Material association observed:
- `оконная фурнитура` — 1458

This association is recorded as a possible `NEW_VOCABULARY` signal for a later justified expansion pass. It is NOT yet a semantic-core inclusion, cluster, page, or architecture decision.

## Discipline

`SEED != FINAL KEYWORD`.

No cleanup, clustering, page mapping, or architecture decision is performed in Step 03. Raw provider evidence is preserved first.
