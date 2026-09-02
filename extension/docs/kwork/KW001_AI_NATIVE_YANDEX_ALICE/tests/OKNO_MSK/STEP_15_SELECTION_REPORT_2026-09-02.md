# OKNO_MSK — Step 15 AI-case selection — corrected V2

Date: 2026-09-02  
Status: **FINAL PASS AFTER POST-RUN CORRECTION**  
Result: `25 REVIEWED / 8 SELECTED / 16 REJECTED / 1 HOLD / STEP16 NOT STARTED`

## 1. Canonical authority

Permanent method:

`../../STEP_15_AI_CASE_SELECTION_METHOD.md`

Post-run correction record:

`STEP_15_POST_RUN_AUDIT_AND_CORRECTION_2026-09-02.md`

Canonical V2 evidence:

- `STEP_15_CASE_SELECTION_LEDGER_MANIFEST.json`
- `STEP_15_CASE_SELECTION_LEDGER_V2_PART_01.tsv`
- `STEP_15_CASE_SELECTION_LEDGER_V2_PART_02.tsv`
- `STEP_15_CASE_SELECTION_LEDGER_V2_PART_03.tsv`
- `STEP_15_CASE_SELECTION_LEDGER_V2_PART_04.tsv`
- `STEP_15_CASE_SELECTION_LEDGER_V2_PART_05.tsv`
- `STEP_15_SELECTED_CASES_V2.tsv`
- `STEP_15_STEP14A_DELTA_COVERAGE_V2.tsv`
- `STEP_15_V2_QA_2026-09-02.json`
- `STEP_15_CURRENT_STATE.json`

The earlier V1 ledger shards and V1 selected-case shards remain in repository history but are superseded for Step16 decision authority.

## 2. What was corrected

### 2.1 Candidate lineage

V1 contained manual QF metadata drift. V2 is rebuilt from exact authoritative joins:

```text
STEP_13_QUERY_FAMILY_DEFINITIONS.tsv
+ exact QF_ID join
STEP_13_CONFLICT_DIAGNOSIS.tsv
+ exact Step14A affected_query_families joins / declared structural overlays
```

V2 QA:

```text
STEP13_QF_JOINED = 21/21
PAIR_ID_MISMATCH = 0
REPRESENTATIVE_QUERY_MISMATCH = 0
PRIMARY_OWNER_MISMATCH = 0
SUPPORTING_URL_MISMATCH = 0
UNRESOLVED_LINEAGE_MISMATCH = 0
STEP14A_MATERIAL_DELTA_COVERAGE = 21/21
```

### 2.2 Stability controls

The first method over-optimized for uncertain/high-information diagnostic cases. V2 keeps the six corrected diagnostic probes and adds two stable controls.

```text
DIAGNOSTIC_PROBES = 6
STABILITY_CONTROLS = 2
SELECTED_TOTAL = 8
```

This remains inside the job-scoped normal `3–10` range.

## 3. Corrected selected set

### Diagnostic probes

| Case | Exact authoritative query | Frozen Search responsibility | Why selected |
|---|---|---|---|
| C15-004 / QF004 | `панорамные алюминиевые окна` | aluminium commercial owner primary; panoramic information supporting | commercial/product vs explanatory synthesis |
| C15-006 / QF006 | `алюминиевые окна для веранды` | veranda use-case hub primary; aluminium/material support | hub vs material/mechanism specialists |
| C15-010 / QF010 | `установка подоконника на пластиковые окна` | windowsill object page primary; finishing service support; mixed service/DIY SERP | object/product vs service/DIY interpretation |
| C15-013 / QF013 | `французские панорамные окна` | French specialist primary; general panoramic support | explicit taxonomy intersection |
| C15-019 / QF019 | `как открыть пластиковое окно` | narrow troubleshooting pair preserved; probe drifts to emergency/outside opening | direct intent-drift discrimination |
| C15-020 / QF020 | `лучшие пластиковые окна` | best-windows article specific primary; broad choose-windows guide supporting | overlapping selection/comparison-page differentiation |

### Stability controls

| Case | Exact authoritative query | Stable baseline | Control role |
|---|---|---|---|
| C15-007 / QF007 | `панорамное остекление балкона` | 9/10 saved SERP results balcony/loggia-specific; broad panoramic result rank 10 | stable specialist-owner control |
| C15-018 / QF018 | `замена окна на пластиковое цена москва` | replacement-specific commercial results plus generic installation support | stable transactional replacement control |

The previously discussed V1 `C15-008` is **not** a control. Authoritative QF008 is PVC-door installation with presearch evidence, so it does not meet the corrected fresh-stable-control requirement.

## 4. Selected-case preregistration

Every V2 selected case contains before Step16:

```text
exact QF ID
exact representative query
exact Search evidence mode
exact primary owner
exact supporting URL(s)
exact upstream verdict
Step14A related deltas
case_role = DIAGNOSTIC_PROBE | STABILITY_CONTROL
pre-AI baseline
evaluation purpose
expected observable fields
CHANGE or CONTROL_BREAK condition
DE_RISK condition
NO_CHANGE condition
INSUFFICIENT condition
confirmation_required_if_material_delta = true
step16_provider_call_authorized = false
```

## 5. Control interpretation

Controls do not exist to force agreement.

Expected normal control outcome is `NO_CHANGE` or `DE_RISK`, but observed evidence must be recorded as returned.

Canonical rule:

```text
SINGLE CONTROL_BREAK
!= ARCHITECTURE CHANGE
-> CONFIRMATION / BATCH-VALIDITY REVIEW IN STEP16/17
```

## 6. HOLD

`C15-023` remains HOLD.

The glass-unit commercial hub / informational article / custom-manufacturing boundary is architecturally useful and AI-observable, but it still lacks a fresh direct ordinary-Search baseline. It cannot be promoted into Step16 just to increase coverage.

## 7. Claim boundary

This eight-case set is:

`DECISION_DIAGNOSTIC_SET_WITH_STABILITY_CONTROLS`

It is **not** a representative sample of all 2332 active phrases/site demand.

Therefore the later AI comparison may support conclusions about these selected architecture decisions and the behavior of the two stable controls. It may not support a prevalence statement such as “AI differs from Search in X% of site demand”.

## 8. Accounting

```text
CANDIDATE_UNIVERSE = 25
REVIEWED = 25
SELECTED = 8
  DIAGNOSTIC = 6
  CONTROLS = 2
REJECTED = 16
HOLD = 1
TOTAL = 25
SILENT_DROPS = 0
STEP14A_MATERIAL_DELTA_COVERAGE = 21/21
```

## 9. Provider boundary

```text
STEP15_PROVIDER_CALLS = 0
STEP15_GENSEARCH_CALLS = 0
STEP15_CONSUMER_ALICE_CALLS = 0
STEP16_PROVIDER_CALL_AUTHORIZED = false
STEP16_EXECUTED = false
```

Step15 correction does not authorize Step16.

## 10. Final gate

```text
FINAL_GATE = PASS_STEP15_V2_CORRECTED_SELECTION__8_SELECTED__STEP16_NOT_STARTED
```

Next legal work: Step16 pre-step current-method/capability research, exact acquisition/confirmation design, source-to-method trace, execution manifest, owner-facing review, then explicit provider authorization before any AI request.
