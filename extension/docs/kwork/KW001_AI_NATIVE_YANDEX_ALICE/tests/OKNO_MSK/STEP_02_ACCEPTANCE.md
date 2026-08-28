# KW-001 / OKNO-MSK — STEP 02 ACCEPTANCE

Date: 2026-08-28  
Status: **PASS / PRE-WORDSTAT SEED PLAN FROZEN**

## 1. Canonical Step-02 artifact

```text
STEP_02_SEED_QUERY_PLAN.md
```

This file is the only authority for the first Wordstat seed manifest of the current rehearsal.

The earlier 15-direction draft from the initial 18-page discovery is superseded by the merged Step-01 model and must not be reused.

---

## 2. Coverage result

Merged Step 01 established 16 material business/search-job families (`B01..B16`).

Step 02 covers them through 18 first-pass seeds:

```text
B01 broad PVC purchase                  → S01
B02 REHAU brand/profile                 → S02
B03 application/design                  → S03
B04 windows by house series             → S04
B05 PVC/REHAU doors                     → S05
B06 broad balcony/loggia glazing        → S06
B07 balcony engineering solution        → S07
B08 balcony by house series             → S08
B09 GEO                                 → S09
B10 veranda/outbuilding glazing         → S10
B11 aluminium/cold glazing              → S11
B12 accessories/customisation           → S12
B13 installation + repair/aftercare     → S13 + S14
B14 price/calculation + finance          → S15 + S16
B15 informational selection             → S17
B16 manufacturer/trust intent           → S18
```

No material Step-01 family is silently dropped.

---

## 3. Frozen first-pass acquisition policy

```text
method = Wordstat getTop via accepted durable batch hand
region = Moscow
provider region id = must be verified/resolved before execution
devices = DEVICE_ALL
operators = NONE
numPhrases per seed = 200 provisional
seed count = 18
maximum first-pass requests = 18
theoretical maximum raw rows = 3600 before cross-seed duplicate overlap
```

`200` is explicitly recorded as a test/productization setting, not an industry standard or final commercial promise.

---

## 4. Why the plan is bounded instead of mirroring every current site URL

The merged site contains many known repeated subfamilies: profile models, house series, balcony geometries, GEO pages, accessories, editorial topics and other variants.

Step 02 deliberately does **not** seed every known URL label.

**PURPOSE** — test actual user vocabulary and demand rather than copy the current site architecture into the semantic core, while keeping provider requests and analyst review volume measurable.

**FAILURE IF IGNORED** — the analysis could simply reproduce the site's current taxonomy, inflate request count and make later evidence incapable of challenging existing page boundaries.

Second-pass targeted seeds are allowed only through explicit reason codes defined in the plan.

---

## 5. Second-pass safety/expansion policy frozen

Allowed reason codes:

```text
NEW_VOCABULARY
DISTINCT_USER_JOB
KNOWN_SUBFAMILY_GAP
BUSINESS_CRITICAL_GAP
AMBIGUOUS_MEANING
GEO_REPRESENTATIVE_GAP
SERIES_TEMPLATE_GAP
```

Provisional second-pass cap without formal scope revision:

```text
12 additional seeds
```

Combined provisional Wordstat getTop ceiling:

```text
30 requests
```

This ceiling is a rehearsal control and must be recalibrated from measured test economics.

---

## 6. Geography boundary preserved

Frozen order says primary region = Moscow.

Therefore Step 02 uses one Moscow-district representative for GEO discovery and does not silently expand first-pass acquisition to Moscow-region city/subdomain demand.

The discovered regional subdomain architecture remains factual Step-01 evidence but does not alter the client brief.

---

## 7. Provider truth before freeze

```text
Wordstat requests before Step-02 freeze = 0
ordinary Search requests before Step-02 freeze = 0
GenSearch requests before Step-02 freeze = 0
```

No provider result was used to choose or edit the frozen first-pass seeds.

---

## 8. Exit criteria

```text
merged Step-01 business model used = true
old 15-direction draft rejected = true
all B01..B16 families represented = true
first-pass seed manifest frozen = true
seed purpose recorded = true
region/device/operators policy frozen = true
numPhrases setting explicitly provisional = true
second-pass reason codes frozen = true
expansion/stop rules recorded = true
provider requests before freeze = 0
```

Acceptance marker:

```text
KW001_OKNO_MSK_STEP_02_SEED_PLAN_FROZEN = true
```

---

## 9. Stop gate

Per owner workflow:

```text
ONE STEP
→ COMPLETE
→ STOP
→ REPORT
→ WAIT FOR EXPLICIT CONTINUE
```

Therefore Wordstat pass #1 must not start until the owner explicitly tells ChatGPT to continue.
