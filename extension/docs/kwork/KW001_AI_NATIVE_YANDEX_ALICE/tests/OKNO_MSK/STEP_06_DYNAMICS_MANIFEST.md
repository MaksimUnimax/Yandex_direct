# KW-001 / OKNO-MSK — STEP 06 DYNAMICS MANIFEST

Date: 2026-08-29  
Status: **FROZEN / OWNER AUTHORIZED / READY FOR PROVIDER EXECUTION**

This file is job-specific and disposable with the OKNO-MSK workspace.

## Purpose

Run a bounded Wordstat `getDynamics` diagnostic on four representative roots to qualify whether the late-August `GetTop` snapshot is seasonally atypical before later prioritization.

This is not keyword expansion, semantic cleanup, clustering, page mapping or SERP validation.

## Frozen provider contract

Current YMB contract authority:

`extension/src/shared/wordstat_protocol.js`

Required command prefix:

`WORDSTAT_API_V1`

Method:

`getDynamics`

Frozen common controls:

```text
period = PERIOD_MONTHLY
fromDate = 2024-08-01T00:00:00Z
toDate = 2026-07-31T23:59:59Z
regions = ["213"]
devices = ["DEVICE_ALL"]
```

The range intentionally contains 24 complete calendar months and excludes the incomplete current August 2026.

## Frozen request order

```text
D1 пластиковые окна
D2 остекление балконов
D3 остекление веранды
D4 окна для частного дома
```

No phrase, order, date range, region, device or period may be changed during execution without a new owner-facing review.

## Request ceiling and economics

```text
provider_request_ceiling = 4
estimated_cost_per_request_rub = 0.02
estimated_step_cost_rub = 0.08
```

Each accepted `WORDSTAT_API_V1 getDynamics` command may initiate at most one provider request.

## Execution safety

```text
one command <= one provider request
preserve raw monthly response before interpretation
request_executed=false pre-provider failure may be repaired/replayed after cause is understood
OUTCOME_UNKNOWN / uncertain irreversible outcome => STOP / NO BLIND REPLAY
no semantic or page decision from dynamics alone
```

## Interpretation boundary

After raw data is preserved, descriptive diagnostics may include monthly series, median, min/max, same-month year-over-year comparison, peak/trough months and whether a recurring annual pattern is visible.

Do not invent a universal numeric threshold for seasonality.

## Explicitly deferred roots

```text
панорамные окна — mixed intent; clean first
оконная фурнитура — standalone commercial priority unresolved
ремонт пластиковых окон — acquisition priority unresolved
narrow house-series / engineering roots — poor representative dynamics sample
```

## Gate

Step 06 closes only when all four frozen requests have terminal known outcomes, raw monthly provider rows are preserved in the job workspace, request count/cost are recorded, and the resulting seasonal interpretation remains descriptive and does not make semantic/page decisions.

Markers:

```text
KW001_OKNO_MSK_STEP_06_MANIFEST_FROZEN = true
KW001_OKNO_MSK_STEP_06_REQUEST_COUNT = 4
KW001_OKNO_MSK_STEP_06_PROVIDER_EXECUTION_STARTED = false
KW001_OKNO_MSK_STEP_06_COMPLETE = false
```
