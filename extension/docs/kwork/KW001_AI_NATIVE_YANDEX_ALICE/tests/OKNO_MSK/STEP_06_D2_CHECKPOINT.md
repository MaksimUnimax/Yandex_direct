# KW-001 / OKNO-MSK — STEP 06 D2 CHECKPOINT

Date: 2026-08-29  
Status: **D2 SUCCEEDED / DYNAMICS EVIDENCE ONLY**

## Request

```text
phrase = остекление балконов
method = getDynamics
period = PERIOD_MONTHLY
fromDate = 2024-08-01T00:00:00Z
toDate = 2026-07-31T23:59:59Z
regions = ["213"]
devices = ["DEVICE_ALL"]
request_id = wordstat-dde1f9a7-23be-4408-ab7e-053c3f0908dd
http_status = 200
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
```

A prior local delivery attempt failed with `SEND_BUTTON_NOT_READY`, `recoverable=true`, `request_executed=false`. It was preserved separately and did not reach the provider.

## Preserved raw data

Complete 24-month `date/count/share` rows are stored in:

```text
STEP_06_D2_RAW_DYNAMICS.tsv
```

## Descriptive diagnostics

```text
observation_count = 24
median_count = 17893
min_count = 5771 (2025-12)
max_count = 115887 (2025-08)
max_min_ratio = 20.0809
```

Same-month comparisons show a non-repeating level shift rather than a clean annual seasonal cycle. Examples:

```text
2025-08 vs 2024-08: +509.8%
2025-09 vs 2024-09: +78.0%
2025-10 vs 2024-10: -26.3%
2025-11 vs 2024-11: -59.3%
2025-12 vs 2024-12: -83.3%
2026-01 vs 2025-01: -80.6%
2026-02 vs 2025-02: -70.2%
2026-03 vs 2025-03: -50.0%
2026-04 vs 2025-04: -60.1%
2026-05 vs 2025-05: -51.9%
2026-06 vs 2025-06: -67.8%
2026-07 vs 2025-07: -83.8%
```

August 2025 is exceptionally high relative to the rest of this two-year window, but this checkpoint does not assert why.

## Interpretation

Project-specific descriptive classification:

```text
TREND_OR_STRUCTURAL_CHANGE_POSSIBLE
```

Reason: the series contains a very large 2025-08 peak followed by a sustained lower level, and same-month year-over-year comparisons do not show a stable repeating annual pattern across the two cycles.

Do **not** label this series `RECURRING_SEASONAL_PATTERN` from the available evidence.

## Boundary

This checkpoint does not change semantic relevance, page ownership, commercial scope or priority. Dynamics is contextual evidence only.
