# KW-001 / OKNO-MSK — STEP 06 D1 CHECKPOINT

Date: 2026-08-29  
Status: **D1 SUCCEEDED / RAW PRESERVED / DESCRIPTIVE DIAGNOSTIC ONLY**

## Request

```text
phrase = пластиковые окна
method = getDynamics
period = PERIOD_MONTHLY
fromDate = 2024-08-01T00:00:00Z
toDate = 2026-07-31T23:59:59Z
regions = ["213"]
devices = ["DEVICE_ALL"]
request_id = wordstat-c2786f94-e5d7-45e0-b852-883c94dad9b3
http_status = 200
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
```

Complete raw monthly rows are preserved in:

```text
STEP_06_D1_RAW_DYNAMICS.tsv
```

## Descriptive diagnostics

```text
observations = 24
median_count = 186615
minimum = 83031 at 2026-02
maximum = 362237 at 2025-07
max_min_ratio = 4.36x
```

Selected same-month year-over-year changes:

```text
2025-08 vs 2024-08 = +97.7%
2025-09 vs 2024-09 = -22.4%
2025-10 vs 2024-10 = -38.5%
2025-11 vs 2024-11 = -57.6%
2025-12 vs 2024-12 = -73.0%
2026-01 vs 2025-01 = -74.7%
2026-02 vs 2025-02 = -58.1%
2026-03 vs 2025-03 = -50.0%
2026-04 vs 2025-04 = -55.8%
2026-05 vs 2025-05 = -37.9%
2026-06 vs 2025-06 = -39.4%
2026-07 vs 2025-07 = -60.8%
```

## Interpretation

Do **not** classify this series as a clean recurring seasonal pattern yet.

The observed series contains both within-year variation and a strong level shift across comparable months. The evidence is consistent with one or more of:

```text
seasonality
trend / changing demand level
structural/provider/market regime change
other time-varying effects not identifiable from this single series
```

Current descriptive classification:

```text
TREND_OR_STRUCTURAL_CHANGE_POSSIBLE
```

This label is an analyst description, not a Yandex classification.

## Boundary

D1 does not decide semantic relevance, page ownership, cluster boundaries, or client commercial priority. It only warns against treating the current 30-day GetTop count as timeless baseline demand.

Markers:

```text
KW001_OKNO_MSK_STEP_06_D1_COMPLETE = true
KW001_OKNO_MSK_STEP_06_D1_RAW_PRESERVED = true
KW001_OKNO_MSK_STEP_06_D1_CLASSIFICATION = TREND_OR_STRUCTURAL_CHANGE_POSSIBLE
```
