# KW-001 / OKNO-MSK — STEP 06 DYNAMICS SYNTHESIS

Date: 2026-08-29  
Status: **FOUR-ROOT DIAGNOSTIC COMPLETE / DESCRIPTIVE INTERPRETATION ONLY**

## Scope

Four frozen representative roots were checked with Yandex Wordstat `getDynamics` using the same controls:

```text
period = PERIOD_MONTHLY
fromDate = 2024-08-01T00:00:00Z
toDate = 2026-07-31T23:59:59Z
region = 213
device = DEVICE_ALL
```

Roots:

```text
D1 пластиковые окна
D2 остекление балконов
D3 остекление веранды
D4 окна для частного дома
```

All four provider calls returned HTTP 200 and complete 24-month series.

## Comparative diagnostics

| ID | Phrase | Median | Min | Max | Max/Min | Mean cycle 2 vs cycle 1 | Positive same-month comparisons |
|---|---|---:|---:|---:|---:|---:|---:|
| D1 | пластиковые окна | 186615 | 83031 | 362237 | 4.36× | -45.41% | 1/12 |
| D2 | остекление балконов | 17893 | 5771 | 115887 | 20.08× | -30.99% | 2/12 |
| D3 | остекление веранды | 1699 | 562 | 5347 | 9.51× | -59.28% | 1/12 |
| D4 | окна для частного дома | 429.5 | 223 | 803 | 3.60× | -23.16% | 1/12 |

`cycle 1` = 2024-08 through 2025-07.  
`cycle 2` = 2025-08 through 2026-07.

## Main finding

The four independent roots do **not** show a clean stable repeated annual cycle that would justify labeling the observed variation as ordinary seasonality alone.

Instead, all four series show a material level shift around/after summer 2025:

```text
D1: second 12-month mean ≈ 45% below first
D2: second 12-month mean ≈ 31% below first
D3: second 12-month mean ≈ 59% below first
D4: second 12-month mean ≈ 23% below first
```

The direction is broadly synchronized across unrelated-but-adjacent window/glazing roots. August 2025 is unusually high in all four compared with August 2024, followed by predominantly lower same-month comparisons thereafter.

## Interpretation boundary

Allowed conclusion:

`TREND_OR_STRUCTURAL_CHANGE_POSSIBLE`

for D1–D4.

Not allowed from these series alone:

```text
claim that the shift is caused by real market demand decline
claim that Wordstat changed methodology or measurement
claim that August 2025 is definitely an external event
claim a universal seasonal peak/trough calendar
use one peak month as a reason to create/delete a page
use a low month as proof of semantic irrelevance
```

The synchronized shift may reflect real demand change, measurement/methodology effects, or a combination. Step 06 does not establish cause.

## Consequence for later work

Later priority interpretation must not treat the current 30-day `GetTop` counts as timeless average monthly demand.

Where demand magnitude is used, later work should preserve the distinction between:

```text
current snapshot
historical range
possible level/trend shift
semantic relevance
SERP intent/page ownership
```

Dynamics is context for prioritization, not a semantic-cleaning or page-mapping rule.

## Provider execution truth

```text
successful provider calls = 4
failed provider calls = 0
outcome_unknown = 0
estimated provider cost = 0.08 RUB
```

One recoverable delivery-stage incident occurred before D2:

```text
code = SEND_BUTTON_NOT_READY
request_executed = false
automatic_retry = false
```

It consumed no provider request. The unchanged D2 command was safely replayed and then succeeded.

## Evidence files

```text
STEP_06_D1_RAW_DYNAMICS.tsv
STEP_06_D1_CHECKPOINT.md
STEP_06_D2_PRE_PROVIDER_INCIDENT.md
STEP_06_D2_RAW_DYNAMICS.tsv
STEP_06_D2_CHECKPOINT.md
STEP_06_D3_RAW_DYNAMICS.tsv
STEP_06_D3_CHECKPOINT.md
STEP_06_D4_RAW_DYNAMICS.tsv
STEP_06_D4_CHECKPOINT.md
```

No universal KW-001 methodology was modified by this synthesis.
