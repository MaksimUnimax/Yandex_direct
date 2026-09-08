# KW-002 JOB MANIFEST — BLOOD_SAND_GREENFIELD_2026-09-08

Status: **STEP 02 V2 COMPLETE / PASS 93/100 = 9.3/10 / STEP 03 NEXT ALLOWED**

## 1. Job identity

```text
KW_ID = KW-002
JOB_ID = BLOOD_SAND_GREENFIELD_2026-09-08
JOB_TYPE = PRODUCTIZATION_REHEARSAL
EXECUTION_MODE = CLEAN_FROM_SCRATCH
BUSINESS = Blood & Sand / «Кровь и Песок»
SITE_STATE = NEW_SITE
REGION = Russia
LANGUAGE = Russian
PRIMARY_SEARCH_ENGINE = Yandex
```

## 2. Frozen client truth

```text
Brand = «Кровь и Песок» / Blood & Sand
Business = product brand / seller
Client wording = амулеты, обереги и талисманы; в ассортименте есть в том числе товары для автомобиля
Sales channels = Ozon + Wildberries
Assortment authority = Ozon only
Primary market/search geography = Russia
New owned website planned = YES
```

## 3. Current authoritative assortment input

```text
CLIENT_SUPPLIED_BRIEF.md
CLIENT_SUPPLIED_ASSORTMENT_MANIFEST.md
CLIENT_SUPPLIED_PRODUCT_CATALOG_OZON_76.csv
ALLOWED_INPUTS_AND_SEALED_SOURCES.md
```

```text
OZON PRODUCT/LISTING ROWS = 76
WB PRODUCT/LISTING ROWS ACTIVE = 0
CROSS_PLATFORM RECONCILIATION = NOT APPLICABLE
```

## 4. Clean-baseline rule

Until Step 20 final freeze:

```text
PRIOR BLOOD_SAND SEO RESEARCH = SEALED / FORBIDDEN EXECUTION INPUT
DEFAULT BLOOD_SAND PROJECT MATERIAL = DENY
EXCEPTIONS = exact sources whitelisted in ALLOWED_INPUTS_AND_SEALED_SOURCES.md
```

## 5. Step 01 accepted truth

```text
STEP_01_INPUT_ROWS_ACCOUNTED = 76
STEP_01_SILENT_DROPS = 0
STEP_01_WB_ROWS_USED = 0
STEP_01_NEUTRAL_CONCEPTS = 4
STEP_01_AMBIGUITY_ISSUES = 10
STEP_01_REMOTE_GITHUB_READBACK = PASS
STEP_01_MAIN_RETURN_QA = PASS
STEP_01_COMPLETE = true
```

## 6. Universal quality rule

Current Level-1 authority:

```text
LEVEL1/RESULT_QUALITY_SCORING_RULE.md
```

Every major step/rework/deliverable must now be scored as follows:

```text
EACH CRITERION = 0–10
DEFAULT CRITERIA = 10
QUALITY_TOTAL = 0–100
QUALITY_SCORE = QUALITY_TOTAL / 10 = 0–10
```

Forbidden:

```text
1.0/1.0 per criterion
0.9/1.0 per criterion
10 criteria treated as 10 one-point components
```

PASS requires:

```text
QUALITY_TOTAL >= 90/100
AND QUALITY_SCORE >= 9.0/10
AND all hard gates PASS
AND no open critical defect
```

## 7. Step 02 V1 historical result

Historical V1 remains preserved:

```text
STEP_02_V1_SEEDS = 97
STEP_02_V1_PRIMARY = 67
STEP_02_V1_DEFERRED = 30
STEP_02_V1_REMOTE_READBACK = PASS
STEP_02_V1_EXTERNAL_AUDIT = FAIL
STEP_02_V1_QUALITY_TOTAL = 65/100
STEP_02_V1_QUALITY_SCORE = 6.5/10
STEP_02_V1_STATUS = SUPERSEDED / REWORK_REQUIRED
```

Authorities:

```text
STEP_02_EXTERNAL_METHOD_AUDIT_2026-09-08.md
STEP_02_V1_QUALITY_SCORE_2026-09-08.md
```

## 8. Permanent Step-02 correction

Current Level-2 authority:

```text
LEVEL2/STEP_02_SEED_ACQUISITION_QUALITY_GATE.md
```

Permanent corrected rules include:

```text
CATALOG_LINEAGE_COVERAGE != SEARCH_PROBE_QUALITY_COVERAGE
HIGH-noise bare primary requires refinement/control governance
material use context requires bounded synonym/formulation plan
seller name != automatic PRIMARY
information gain must discriminate now/later/control/redundant
cost alone cannot justify deferral
current primary set must be deterministic
Step 02 quality score must satisfy the universal Level-1 0–10-per-criterion rule
```

## 9. Step 02 V2 current authority

Current artifacts:

```text
STEP_02_V2_DECISION_OVERLAY.csv
STEP_02_V2_ADDITIONAL_PROBES.csv
STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv
STEP_02_DEFERRED_CONTROL_MANIFEST_V2.csv
STEP_02_SEARCH_PROBE_QUALITY_COVERAGE_V2.csv
STEP_02_V2_INFORMATION_GAIN_POLICY.csv
STEP_02_REWORK_REPORT_V2_2026-09-08.md
STEP_02_QA_REPORT_V2_2026-09-08.md
```

Accepted truth:

```text
V1_RETAINED_PRIMARY = 48
V1_BARE_PROBES_DEMOTED = 19
V2_QUALIFIED_REFINEMENT_PROBES = 19
V2_USE_SYNONYM_PROBES = 12
V2_NEW_PROBES_TOTAL = 31
V2_PRIMARY_MANIFEST_ROWS = 79
V2_DEFERRED_CONTROL_ROWS = 49
V2_SEARCH_QUALITY_COVERAGE_GROUPS = 26
V2_SEARCH_QUALITY_COVERAGE_PASS = 26
V2_QUALITY_TOTAL = 93/100
V2_QUALITY_SCORE = 9.3/10
V2_QA = PASS
V2_REMOTE_READBACK = PASS
STEP_02_COMPLETE = true
```

Current Step-03 seed authority is only:

```text
STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv
```

Do not reconstruct current execution from the old V1 97-row seed map.

## 10. Step 03 handoff boundary

Step 03 may start only after its own provider gate.

19 V2 qualified probes use grouped Wordstat OR syntax.

```text
OR_OPERATOR_DOCUMENTED_BY_YANDEX = true
BRIDGE_OR_OPERATOR_EXECUTION_VERIFIED = false
```

Step 03 must verify actual Bridge/provider behavior before mass execution.

Fallback if grouped OR is unsupported:

```text
parent Q probe
→ split into three child probes with амулет / оберег / талисман
→ preserve parent lineage
→ do not silently drop the acquisition branch
```

## 11. Current execution state

```text
DOCUMENTATION_PREPARED = true
ROADMAP_OWNER_APPROVED = true
ORDER_SCOPE_FROZEN = true
STEP_00_COMPLETE = true
STEP_01_COMPLETE = true
STEP_01_MAIN_RETURN_QA = PASS
STEP_02_STARTED = true
STEP_02_V1_MATERIALIZED = true
STEP_02_V1_QUALITY_TOTAL = 65/100
STEP_02_V1_QUALITY_SCORE = 6.5/10
STEP_02_V1_STATUS = SUPERSEDED
STEP_02_V2_REWORK = COMPLETE
STEP_02_V2_QA = PASS
STEP_02_V2_QUALITY_TOTAL = 93/100
STEP_02_V2_QUALITY_SCORE = 9.3/10
STEP_02_COMPLETE = true
STEP_03_STARTED = false
NEXT_STEP_ALLOWED = true
NEXT_STEP = STEP_03_PRIMARY_WORDSTAT_ACQUISITION
PROVIDER_CALLS_FOR_KW002_JOB = 0
WORK_HANDOFFS_EXECUTED = 1
```