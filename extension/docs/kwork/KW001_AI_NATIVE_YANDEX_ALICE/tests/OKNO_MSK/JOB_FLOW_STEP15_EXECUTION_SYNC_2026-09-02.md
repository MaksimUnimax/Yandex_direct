# OKNO_MSK — Job flow sync after corrected Step 15 V2

Date: 2026-09-02  
Authority type: job-specific current-state overlay.

## Roadmap

| Step | Status |
|---|---|
| 0–13 | ✅ COMPLETE |
| 14 / 14A | ✅ FINAL PASS at `16d7f38b7b48369d3d2687553f7a865b86bf133e` |
| 15 pre-step research / owner review | ✅ COMPLETE |
| 15 V1 execution | ⚠️ SUPERSEDED — post-run lineage/control defects |
| 15 V2 correction / exact lineage rebuild | ✅ COMPLETE |
| 15 final corrected selection | ✅ PASS — 25 reviewed / 8 selected / 16 rejected / 1 hold |
| 16 AI-search acquisition | ⛔ NOT STARTED / NOT AUTHORIZED |
| 17–22 | ⬜ NOT STARTED |

## Step15 canonical authorities

```text
../../STEP_15_AI_CASE_SELECTION_METHOD.md
STEP_15_POST_RUN_AUDIT_AND_CORRECTION_2026-09-02.md
STEP_15_CASE_SELECTION_LEDGER_MANIFEST.json
STEP_15_CASE_SELECTION_LEDGER_V2_PART_01.tsv
STEP_15_CASE_SELECTION_LEDGER_V2_PART_02.tsv
STEP_15_CASE_SELECTION_LEDGER_V2_PART_03.tsv
STEP_15_CASE_SELECTION_LEDGER_V2_PART_04.tsv
STEP_15_CASE_SELECTION_LEDGER_V2_PART_05.tsv
STEP_15_SELECTED_CASES_V2.tsv
STEP_15_V2_QA_2026-09-02.json
STEP_15_CURRENT_STATE.json
```

If an older Step15 V1 artifact conflicts with V2, V2 wins.

## Corrected selected Step16 candidate IDs

Diagnostic probes:

`C15-004, C15-006, C15-010, C15-013, C15-019, C15-020`

Stability controls:

`C15-007, C15-018`

Total selected: `8`.

## Exact selected queries

```text
C15-004  панорамные алюминиевые окна
C15-006  алюминиевые окна для веранды
C15-007  панорамное остекление балкона          [STABILITY_CONTROL]
C15-010  установка подоконника на пластиковые окна
C15-013  французские панорамные окна
C15-018  замена окна на пластиковое цена москва [STABILITY_CONTROL]
C15-019  как открыть пластиковое окно
C15-020  лучшие пластиковые окна
```

## Why V1 was superseded

V1 had material candidate-lineage drift caused by manual QF metadata reconstruction. Examples included wrong pair IDs, wrong QF008 task, incorrect QF010 owner framing, an altered QF013 query, and wrong frozen URLs for QF019/QF020.

V2 is rebuilt from exact Step13 QF definitions + conflict diagnosis + Step14A delta joins.

Lineage QA:

```text
STEP13_QF_JOIN = 21/21
PAIR_ID_MISMATCH = 0
REPRESENTATIVE_QUERY_MISMATCH = 0
PRIMARY_OWNER_MISMATCH = 0
SUPPORTING_URL_MISMATCH = 0
UNRESOLVED_LINEAGE_MISMATCH = 0
STEP14A_MATERIAL_DELTA_COVERAGE = 21/21
```

## Evaluation design correction

V1 selected only high-information uncertain cases. V2 keeps six corrected diagnostic probes and adds two stable real-world controls:

- `C15-007 / QF007`: stable specialist-owner control; 9/10 saved SERP results balcony/loggia-specific.
- `C15-018 / QF018`: stable transactional replacement-owner control.

The eight-case set is a `DECISION_DIAGNOSTIC_SET_WITH_STABILITY_CONTROLS`, not a representative sample of all site demand.

## Confirmation handoff

Every selected V2 case has:

`confirmation_required_if_material_delta = true`

A single later `CHANGE` or `CONTROL_BREAK` does not directly rewrite architecture. Exact confirmation logic belongs to Step16/17 method research.

## Provider boundary

```text
STEP15_PROVIDER_CALLS = 0
STEP15_GENSEARCH_CALLS = 0
STEP15_CONSUMER_ALICE_CALLS = 0
STEP16_PROVIDER_CALL_AUTHORIZED = false
STEP16_EXECUTED = false
```

## Next legal action

Step16 pre-step current method/capability research only. It must use the V2 ledger manifest/shards and `STEP_15_SELECTED_CASES_V2.tsv`, research current GenSearch/Alice behavior and temporal/confirmation handling, build source-to-method trace and execution manifest, present owner-facing review, and wait for explicit provider authorization.
