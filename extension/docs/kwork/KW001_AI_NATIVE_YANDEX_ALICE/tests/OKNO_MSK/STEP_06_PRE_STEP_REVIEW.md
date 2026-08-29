# KW-001 / OKNO-MSK — STEP 06 PRE-STEP REVIEW

Date: 2026-08-29  
Status: **PRE-STEP REVIEW COMPLETE / WAITING OWNER AUTHORIZATION / NO PROVIDER EXECUTION**

This file is job-specific and disposable with the OKNO-MSK workspace.

## 1. Candidate next major step

Selective Yandex Wordstat demand dynamics / seasonality check.

Purpose:

```text
verify whether last-30-day demand levels used in Steps 3 and 5 are seasonally atypical
for a small number of representative major search families
before later priority interpretation and semantic freeze
```

This is not another keyword-expansion pass.

This step must not create new semantic families merely because dynamics exists for a phrase.

---

## 2. Why this step exists

The current acquisition evidence from `GetTop` represents the last 30 days. That is suitable for current vocabulary discovery, but one observation window can mislead later prioritization if the category is seasonal.

The universal KW-001 runbook currently says:

```text
STEP 7 — Demand dynamics / seasonality where material
Use dynamics only on representative major roots where seasonality can materially change interpretation.
PURPOSE — avoid presenting one observation month as timeless demand truth.
```

Official Yandex sources confirm:

- Wordstat Dynamics shows how query frequency changes over time.
- The interface defaults to the last 2 years with monthly detail.
- Monthly/weekly history can be requested for periods extending back to 2018.
- Region and device filters are supported.
- `GetDynamics` is a dedicated Wordstat method.

Official sources:

- https://yandex.ru/support2/wordstat/ru/interface/new
- https://yandex.ru/support2/wordstat/en/content/api-structure
- https://aistudio.yandex.ru/docs/en/search-api/api-ref/Wordstat/getDynamics.html
- https://aistudio.yandex.ru/docs/ru/search-api/pricing.html

External methodology corroboration:

- https://ahrefs.com/blog/search-demand-lifecycle/

The external source supports the general need to distinguish recurring seasonality from current-point demand, but it does not prescribe which Yandex phrases or how many phrases must be checked.

---

## 3. Method-origin classification

```text
GetDynamics semantics = OFFICIAL
Use history to detect seasonality / avoid single-month overinterpretation = OFFICIAL + INDUSTRY_PRACTICE
Use only representative roots rather than every keyword = owner-approved universal workflow + ANALYST_HEURISTIC
24 complete monthly observations = ANALYST_HEURISTIC, aligned with Yandex UI default two-year view
Exact representative phrase set = ANALYST_HEURISTIC / project-specific
region 213 = frozen job scope
DEVICE_ALL = frozen job scope
```

No source establishes a universal rule that all semantic families require dynamics.

---

## 4. Adversarial review: is dynamics actually necessary here?

Possible argument to skip Step 06:

```text
The Kwork is primarily semantic + page architecture.
Seasonality does not determine semantic relevance or SERP page ownership.
Therefore dynamics should not become ritual overhead.
```

That objection is valid.

Reason not to skip entirely in this rehearsal:

```text
Steps 3 and 5 collected all demand from one late-August observation window.
Later H/A/C/O priority and client recommendations may refer to relative demand magnitude.
A few representative dynamics checks can tell us whether this snapshot is near peak/trough/normal.
```

Therefore the method is justified only as a **small diagnostic sample**, not as a full-core dynamics sweep.

Verdict:

```text
DO NOT run dynamics for every retained keyword/family.
DO run a small representative set where a seasonal distortion could materially affect interpretation.
```

---

## 5. Proposed representative roots

### D1 — `пластиковые окна`

Reason:

```text
umbrella commercial root
central baseline for the entire order
broadest reference family from pass #1
```

Question answered:

```text
Is the current broad-window demand snapshot seasonally high, low, or roughly normal?
```

Status: `DYNAMICS_READY / CORE_BASELINE`.

### D2 — `остекление балконов`

Reason:

```text
large independent service family
material page/job family in the site model
installation/outdoor work may have a seasonal pattern different from generic window purchase
```

Question answered:

```text
Does balcony-glazing demand have a materially different seasonal curve from the broad PVC baseline?
```

Status: `DYNAMICS_READY / MAJOR_SERVICE_FAMILY`.

### D3 — `остекление веранды`

Reason:

```text
separate object/use-case family
veranda/terrace demand may be more exposed to construction/outdoor seasonality
current Step-3 observation is a single 30-day window
```

The seasonality expectation itself is not treated as fact; the dynamics request is used to test it.

Question answered:

```text
Is this object's current demand strongly seasonal enough that one-month counts should be qualified in client prioritization?
```

Status: `DYNAMICS_READY / SEASONALITY_DIAGNOSTIC`.

### D4 — `окна для частного дома`

Reason:

```text
Step 5 validated a distinct private-house user job
later prioritization could over- or under-weight this family based on one month
```

Question answered:

```text
Does private-house window demand have a materially different seasonal profile from the umbrella PVC root?
```

Status: `DYNAMICS_READY / DISTINCT_USER_JOB`.

---

## 6. Important roots deliberately NOT selected

### `панорамные окна`

Do not use for dynamics now.

Reason:

Step 5 showed substantial mixed intent: window purchase, architecture/design, apartments/real estate, hotels/rental, heating/convector topics and other adjacency. A dynamics curve for the broad root would measure this mixed universe and could be falsely interpreted as client-commercial seasonality.

Status: `DEFER_UNTIL_CLEANUP / MIXED_INTENT`.

### `оконная фурнитура`

Do not use for dynamics now.

Reason:

Standalone fittings/accessories commercial priority remains unresolved. Seasonal analysis is lower information value before business-scope resolution.

Status: `DEFER / BUSINESS_PRIORITY_UNKNOWN`.

### `ремонт пластиковых окон`

Do not use for dynamics now.

Reason:

Repair acquisition priority is still unresolved in the mock client facts. A seasonal curve would not resolve whether this service belongs in the commercial acquisition scope.

Status: `DEFER / BUSINESS_PRIORITY_UNKNOWN`.

### `окна п 44`, `остекление балкона п 46`, roofed-balcony and other narrow roots

Do not use for dynamics now.

Reason:

They are too narrow to justify representative seasonality calls before later SERP/page-boundary analysis. Low frequency does not make them irrelevant; it makes them poor choices for this particular diagnostic sample.

---

## 7. Proposed provider controls after owner approval

Use complete calendar months to avoid a partial current month.

Proposed period:

```text
period = MONTHLY
fromDate = 2024-08-01
toDate = 2026-07-31
```

This gives 24 complete monthly observations.

Proposed scope:

```text
regions = ["213"]
devices = ["DEVICE_ALL"]
phrase_count = 4
```

Proposed phrases:

```text
D1 пластиковые окна
D2 остекление балконов
D3 остекление веранды
D4 окна для частного дома
```

Official current pricing lists `GetDynamics` at 20 RUB per 1,000 requests, i.e. 0.02 RUB/request in the RUB tariff.

Estimated provider cost for four calls:

```text
4 × 0.02 RUB = 0.08 RUB
```

The exact YMB command syntax must be re-read from the current extension/provider protocol before execution; do not construct it from memory.

---

## 8. What will be calculated from each dynamics response

The raw monthly data must be preserved first.

Then derive descriptive diagnostics only, for example:

```text
24-month monthly series
latest complete month count
24-month median
24-month min/max
same-month year-over-year comparison where available
peak month(s)
trough month(s)
peak/trough ratio
whether a recurring seasonal pattern is visible across both annual cycles
```

Do not invent a universal numerical threshold such as `seasonal if ratio > X` unless separately justified.

Classification should remain descriptive:

```text
STABLE_OR_WEAK_SEASONALITY
RECURRING_SEASONAL_PATTERN
TREND_OR_STRUCTURAL_CHANGE_POSSIBLE
INSUFFICIENT_OR_MIXED
```

These labels are project-specific analyst mechanics, not Yandex classifications.

---

## 9. What Step 06 will NOT decide

```text
no keyword exclusion solely because demand is seasonal
no new page solely because demand peaks seasonally
no cluster/page ownership decision
no semantic relevance decision from dynamics alone
no final H/A/C/O score
no third Wordstat expansion pass
no SERP call
no GenSearch call
```

Seasonality is context for later prioritization, not semantic truth.

---

## 10. Self-audit of Step 05 handoff

Step 05 is safe to hand into this step because:

```text
4/4 probes succeeded
0 failed_terminal
0 outcome_unknown
complete Step-5 phrase rows were preserved before acceptance
final batch.status was captured
no third recursive expansion was authorized
```

No Step-05 correction is required before dynamics.

One limitation remains from earlier work:

Step 03 provider evidence was acquired successfully, but the workspace does not contain one single normalized raw table for all ~pass-1 phrase rows. This does not block four representative dynamics calls, but it remains relevant before final row-level semantic freeze and must not be forgotten.

---

## 11. Proposed Step-06 gate

After owner authorization, Step 06 passes only if:

```text
exact representative roots frozen before provider execution
exact full-month date range frozen
region 213 used on every call
DEVICE_ALL used on every call
raw monthly provider data preserved in the job workspace
request count and estimated cost recorded
no blind retry after uncertain outcome
seasonality conclusions remain descriptive and traceable to monthly values
no semantic/page decision is made from dynamics alone
```

---

## 12. Pre-step verdict

```text
STEP_06_METHOD_VERDICT = SUPPORTED_WITH_PROJECT_SPECIFIC_REPRESENTATIVE_SAMPLE
STEP_06_DYNAMICS_CALLS_PROPOSED = 4
STEP_06_ESTIMATED_PROVIDER_COST_RUB = 0.08
STEP_06_PROVIDER_EXECUTION = NOT STARTED
STEP_06_OWNER_AUTHORIZATION_REQUIRED = true
```

No universal KW-001 rule was modified during this review.
