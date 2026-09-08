# KW-002 «Кровь и Песок» — STEP 02 V2 QA

Дата: 2026-09-08

Статус: **PASS / REMOTE READBACK PASS**

## 1. Проверяемые V2 артефакты

```text
STEP_02_V2_DECISION_OVERLAY.csv
STEP_02_V2_ADDITIONAL_PROBES.csv
STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv
STEP_02_DEFERRED_CONTROL_MANIFEST_V2.csv
STEP_02_SEARCH_PROBE_QUALITY_COVERAGE_V2.csv
STEP_02_V2_INFORMATION_GAIN_POLICY.csv
STEP_02_REWORK_REPORT_V2_2026-09-08.md
```

V1 артефакты сохранены как история и не являются текущим Step-03 execution authority.

## 2. Количественный QA

```text
V1_RETAINED_PRIMARY = 48
V1_BARE_PROBES_DEMOTED = 19
V2_QUALIFIED_REFINEMENT_PROBES = 19
V2_USE_SYNONYM_PROBES = 12
V2_NEW_PROBES_TOTAL = 31
V2_PRIMARY_MANIFEST_ROWS = 79
V2_DEFERRED_CONTROL_ROWS = 49
V2_DECISION_OVERLAY_ROWS = 24
V2_SEARCH_QUALITY_COVERAGE_ROWS = 26
```

Remote terminal-row checks:

```text
PRIMARY_MANIFEST_LAST_RUN_ORDER = 79
PRIMARY_MANIFEST_LAST_SEED = U012
DEFERRED_MANIFEST_LAST_ROW = S097
ADDITIONAL_PROBES_LAST_ROW = U012
DECISION_OVERLAY_LAST_ROW = S096
SEARCH_QUALITY_COVERAGE_LAST_ROW = QC026
```

Remote blob SHA:

```text
PRIMARY_MANIFEST_SHA = 9087d272444727bd03f342b4fae1c989ba55a307
DEFERRED_MANIFEST_SHA = 9e9b4d38dcf98bc233f26d651645d7721bfcf66e
ADDITIONAL_PROBES_SHA = ab14a5be575cea598cd3c3701c4ed6b2769a6bdc
DECISION_OVERLAY_SHA = 4688f393d8fb97dae9167c88f49f9882289d2124
SEARCH_QUALITY_COVERAGE_SHA = 4353d0e23f2b944bcf1427e59883654e31fe8716
INFORMATION_GAIN_POLICY_SHA = 4f090df99b93d4df61e9281c2541c0a7b67cb1c0
```

## 3. External-audit defect closure

### Defect 1 — catalog coverage was mistaken for search-quality coverage

```text
CLOSED = true
```

Now preserved separately:

```text
CATALOG_LINEAGE_COVERAGE = inherited 76/76
SEARCH_PROBE_QUALITY_COVERAGE = 26/26 material quality groups PASS
```

### Defect 2 — high-noise bare primary without refinement

```text
CLOSED = true
```

19 ambiguous/high-noise bare probes were demoted to control/deferred and replaced by 19 qualified primary routes.

Broad roots (`амулет`, `оберег`, `талисман`, `чётки`, `знак зодиака`) remain deliberate broad controls but have explicit scoped/qualified companion routes.

```text
HIGH_NOISE_PRIMARY_WITHOUT_REFINEMENT_OR_CONTROL_JUSTIFICATION = 0
```

### Defect 3 — unsystematic vehicle wording coverage

```text
CLOSED = true
```

Bounded synonym axis added:

```text
для машины
для автомобиля
для авто
```

across four frozen roots:

```text
талисман
амулет
оберег
чётки
```

Existing `в машину` routes are preserved.

```text
MATERIAL_USE_CONTEXT_WITHOUT_BOUNDED_SYNONYM_PLAN = 0
```

### Defect 4 — exact seller names were over-promoted by default

```text
CLOSED = true
```

19 ambiguous bare names were demoted. Distinct low-noise names remain primary only after explicit ambiguity/noise screening.

```text
SELLER_NAMES_PROMOTED_TO_PRIMARY_BY_DEFAULT = 0
```

### Defect 5 — boilerplate information-gain rationale

```text
CLOSED = true
```

Current priority is governed by explicit discriminating classes in `STEP_02_V2_INFORMATION_GAIN_POLICY.csv`:

```text
BROAD_VOCABULARY_DISCOVERY
CONFIRMED_USE_CONTEXT
USE_CONTEXT_COMBINATION
UNIQUE_DISCOVERY_BRANCH
ALTERNATE_WORDING_BRANCH
SCOPED_FAMILY_COVERAGE
NOISE_REFINEMENT
SYNONYM_USE_CONTEXT_COVERAGE
```

### Defect 6 — provider cost could over-influence deferral

```text
CLOSED = true
```

V2 primary/deferred decisions are based on information gain/noise/redundancy. Request cost is secondary and is not used as a standalone deferral reason.

## 4. Claim-boundary QA

```text
SEED_AS_FINAL_KEYWORD_CLAIMS = 0
SEO_CLUSTER_DECISIONS = 0
PAGE_OWNERSHIP_DECISIONS = 0
SITE_IA_DECISIONS = 0
SEARCH_DEMAND_CLAIMS = 0
FINAL_INTENT_DECISIONS = 0
ANALYST_COMPOSED_PROBES_UNLABELLED = 0
OLD_RESEARCH_CONTAMINATION = 0
WB_ROWS_USED = 0
WORDSTAT_CALLS_DURING_REWORK = 0
SEARCH_CALLS_DURING_REWORK = 0
AI_SEARCH_CALLS_DURING_REWORK = 0
```

Qualified OR probes are diagnostic only and do not prove the named product belongs to any one of the business classes.

## 5. Step-03 operator handoff boundary

19 qualified probes use Wordstat OR syntax around client business classes.

```text
OR_OPERATOR_DOCUMENTED_BY_YANDEX = true
BRIDGE_OR_OPERATOR_EXECUTION_VERIFIED = false
```

This is not a Step-02 blocker because the semantic acquisition intent is deterministic.

Step 03 must perform a capability/behavior check before mass execution.

Fallback if the Bridge/provider route does not accept the grouped OR probe:

```text
ONE Q-PROBE
→ split deterministically into 3 class-qualified probes:
   амулет + name
   оберег + name
   талисман + name
→ preserve parent Q seed lineage
→ do not silently drop the branch
```

## 6. 10-point quality score

Governed by `LEVEL1/RESULT_QUALITY_SCORING_RULE.md`.

| Dimension | Score | Evidence |
|---|---:|---|
| Goal/output completeness | 1.0/1.0 | Corrected primary/deferred manifests and quality coverage exist. |
| Method/source support | 1.0/1.0 | V2 directly operationalizes Yandex + industry audit findings. |
| Input evidence/provenance integrity | 1.0/1.0 | V1 lineage retained; every new probe points to client/V1 source. |
| Coverage/completeness | 1.0/1.0 | Catalog lineage retained and separate quality-coverage matrix passes 26/26 groups. |
| Analytical correctness/claim boundaries | 0.9/1.0 | Qualified diagnostics are explicit; slight residual heuristic judgment remains in low-vs-ambiguous screening. |
| Adversarial QA quality | 0.9/1.0 | All six audit defects explicitly retested; final provider behavior still belongs to Step 03. |
| Persistence/readback/reproducibility | 1.0/1.0 | All V2 manifests read back remotely with terminal rows/SHA verified. |
| Owner/client usability/plain language | 0.9/1.0 | Rework report explains changes clearly; internal manifests remain technical by necessity. |
| Information gain/cost/execution efficiency | 0.9/1.0 | Priority is now reason-class driven; no cost-only deferrals. |
| Downstream readiness | 0.7/1.0 | Step-03 primary set is deterministic, but grouped OR behavior still needs Bridge/provider verification. |
| **TOTAL** | **9.3/10** | **PASS** |

### За что сняты баллы

```text
- часть ambiguity/noise screening остаётся аналитической эвристикой до реального Wordstat evidence;
- OR-operator behavior through the actual Bridge path ещё не проверен;
- итоговая полезность отдельных probes всё равно будет подтверждаться Step 03/04 реальными данными.
```

Это не блокирует Step 02, потому что hard gates шага выполнены, а fallback для OR-route определён.

## 7. Final PASS gate

```text
CATALOG_LINEAGE_COVERAGE = PASS
SEARCH_PROBE_QUALITY_COVERAGE = PASS
HIGH_NOISE_PRIMARY_WITHOUT_GOVERNED_ROUTE = 0
USE_CONTEXT_SYNONYM_PLAN = PASS
INFO_GAIN_RATIONALE = PASS
PRIMARY_ACQUISITION_MANIFEST = MATERIALIZED / 79 ROWS
DEFERRED_CONTROL_MANIFEST = MATERIALIZED / 49 ROWS
STEP02_QUALITY_SCORE = 9.3 / 10
ALL_HARD_GATES = PASS
REMOTE_READBACK = PASS
```

Final verdict:

```text
STEP_02 = COMPLETE / PASS AFTER V2 REWORK
NEXT_STEP_ALLOWED = true
NEXT_STEP = STEP_03_PRIMARY_WORDSTAT_ACQUISITION
```
