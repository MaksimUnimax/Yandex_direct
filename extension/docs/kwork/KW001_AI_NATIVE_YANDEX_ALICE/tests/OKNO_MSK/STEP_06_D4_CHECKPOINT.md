# KW-001 / OKNO-MSK — STEP 06 D4 CHECKPOINT

Date: 2026-08-29  
Status: **D4 SUCCEEDED / DYNAMICS EVIDENCE PRESERVED**

## Request

```text
phrase = окна для частного дома
method = getDynamics
period = PERIOD_MONTHLY
fromDate = 2024-08-01T00:00:00Z
toDate = 2026-07-31T23:59:59Z
region = 213
device = DEVICE_ALL
request_id = wordstat-98c82797-78b7-4a29-8432-56ea549d17ef
```

Provider result:

```text
status = OK
http_status = 200
request_executed = true
automatic_retry = false
elapsed_ms = 1281
estimated_cost_rub = 0.02
monthly_observations = 24
```

Complete monthly rows are preserved in:

`STEP_06_D4_RAW_DYNAMICS.tsv`

## Descriptive diagnostics

```text
24-month median count = 429.5
minimum = 223 (2026-02)
maximum = 803 (2025-08)
max/min ratio ≈ 3.60
first 12-month mean ≈ 482.83
second 12-month mean = 371.00
second-cycle mean vs first-cycle mean ≈ -23.16%
```

Same-month comparison for the second 12-month cycle versus the first:

```text
2025-08 vs 2024-08 = +84.6%
2025-09 vs 2024-09 = -11.1%
2025-10 vs 2024-10 = -26.7%
2025-11 vs 2024-11 = -34.3%
2025-12 vs 2024-12 = -22.6%
2026-01 vs 2025-01 = -39.1%
2026-02 vs 2025-02 = -48.6%
2026-03 vs 2025-03 = -54.2%
2026-04 vs 2025-04 = -49.4%
2026-05 vs 2025-05 = -10.9%
2026-06 vs 2025-06 = -31.1%
2026-07 vs 2025-07 = -13.7%
```

Only one of the twelve same-month comparisons is positive.

## Interpretation

Preliminary classification:

`TREND_OR_STRUCTURAL_CHANGE_POSSIBLE`

The series does not provide strong evidence for a stable recurring annual seasonal pattern across the two observed cycles. The August 2025 peak is followed by a broadly lower level in the subsequent months compared with the corresponding months one year earlier.

This checkpoint does **not** attribute cause. The observed level shift could reflect real demand change, Wordstat measurement/methodology effects, or a combination; the provider series alone cannot distinguish those explanations.

Dynamics is context only. It does not decide semantic relevance, clustering, page ownership, or priority by itself.
