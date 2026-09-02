# OKNO_MSK — Step 15 post-run audit and correction

Date: 2026-09-02  
Status: **CORRECTION EXECUTED / V1 SUPERSEDED / V2 CANONICAL / STEP16 NOT STARTED**

## 1. Why Step 15 was reopened

After the first Step-15 PASS, the owner requested an external-method review and instructed that all resulting corrections be written into durable project documentation so future runs do not repeat the same mistakes.

The external review confirmed the core information-gain/diversity/pre-registration idea, but identified a missing stability-control layer. A subsequent repository lineage audit then found a more serious V1 execution defect: multiple candidate rows did not exactly match the authoritative Step-13 query-family data they claimed to represent.

Therefore the original `25 reviewed / 6 SELECT / 18 REJECT / 1 HOLD` result is preserved only as historical V1 evidence. It is **not** the canonical Step-15 handoff to Step16.

Canonical corrected artifacts:

- `../../STEP_15_AI_CASE_SELECTION_METHOD.md`
- `STEP_15_CASE_SELECTION_LEDGER_MANIFEST.json`
- `STEP_15_CASE_SELECTION_LEDGER_V2_PART_01.tsv`
- `STEP_15_CASE_SELECTION_LEDGER_V2_PART_02.tsv`
- `STEP_15_CASE_SELECTION_LEDGER_V2_PART_03.tsv`
- `STEP_15_CASE_SELECTION_LEDGER_V2_PART_04.tsv`
- `STEP_15_CASE_SELECTION_LEDGER_V2_PART_05.tsv`
- `STEP_15_SELECTED_CASES_V2.tsv`
- `STEP_15_STEP14A_DELTA_COVERAGE_V2.tsv`
- `STEP_15_V2_QA_2026-09-02.json`
- corrected `STEP_15_CURRENT_STATE.json`
- corrected `STEP_15_SELECTION_REPORT_2026-09-02.md`

## 2. Defect S15-D01 — authoritative lineage drift

### What failed

The V1 candidate ledger used the right-looking `QFxxx` labels, but some metadata was manually reconstructed from other remembered/inferred relationships rather than joined exactly from the accepted Step-13 authority.

Concrete observed mismatches:

### C15-001 / QF001

V1 declared pair IDs:

`V6P0138;V6P0095;V6P0166`

Authoritative `STEP_13_QUERY_FAMILY_DEFINITIONS.tsv#QF001` pair IDs:

`V6P0009;V6P0033;V6P0036`

### C15-008 / QF008

V1 described the candidate as:

`замена алюминиевого остекления`

Authoritative QF008 is:

`PVC_DOOR_INSTALLATION`

with pair ID `V6P0088`, presearch evidence, primary `https://okno-msk.ru/dveri-rehau`, and supporting generic window-installation service.

This was a materially different user job, not a harmless label variation.

### C15-010 / QF010

V1 described installation service as primary.

Authoritative Step13 says:

- exact query: `установка подоконника на пластиковые окна`;
- primary owner: `https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/podokonniki`;
- supporting context: `https://okno-msk.ru/uslugi/otdelka-otkosov`;
- SERP is mixed professional-installation/DIY, while the windowsill object page remains primary.

### C15-013 / QF013

V1 shortened the tested query to `французские окна`.

Authoritative representative query is:

`французские панорамные окна`

The omitted `панорамные` term is exactly what creates the French-vs-panoramic boundary, so the V1 shortening altered the experiment.

### C15-019 / QF019

V1 frozen-owner description did not match the Step13 authoritative pair.

Authoritative primary/supporting URLs are:

- `/stati/okno-otkrylos-v-dvuh-polozheniyah-chto-delat`
- `/stati/kak-otregulirovat-plastikovye-okna`

and the direct probe `как открыть пластиковое окно` drifted toward emergency/outside opening.

### C15-020 / QF020

V1 used the wrong specific primary URL in the frozen description.

Authoritative primary/supporting pair is:

- `/stati/kakie-okna-samye-luchshie`
- `/stati/kak-vybrat-plastikovye-okna`

### Root cause

The error was not a bad Step13 result. The accepted Step13 files were internally specific. The failure occurred when Step15 manually reassembled candidate metadata instead of requiring an exact keyed join.

```text
AUTHORITATIVE QF ID EXISTED
BUT
STEP15 DID NOT ENFORCE EXACT QF-ID JOIN QA
```

### Correction

V2 is rebuilt from:

1. exact `QF_ID` and `pair_ids` in `STEP_13_QUERY_FAMILY_DEFINITIONS.tsv`;
2. exact representative query/evidence mode/owners/verdict in `STEP_13_CONFLICT_DIAGNOSIS.tsv`;
3. exact Step14A delta joins where `affected_query_families` contains that QF, plus separately declared structural-only overlays.

No V1 candidate text is treated as authority.

Mandatory V2 lineage acceptance:

```text
STEP13_QF_JOINED = 21/21
PAIR_ID_MISMATCH = 0
REPRESENTATIVE_QUERY_MISMATCH = 0
PRIMARY_OWNER_MISMATCH = 0
SUPPORTING_URL_MISMATCH = 0
UNRESOLVED_LINEAGE_MISMATCH = 0
STEP14A_MATERIAL_DELTA_COVERAGE = 21/21
```

## 3. Defect S15-D02 — no stability controls

### What was good in V1

The six V1 diagnostic cases were chosen to maximize decision value and diversity, with pre-registered `CHANGE / DE_RISK / NO_CHANGE / INSUFFICIENT` outcomes. That part remains useful after correcting their exact baselines.

### What was missing

The method's E4 information-gain gate rejected all stable cases by design. That makes sense for a pure acquisition-efficiency task, but the resulting batch is enriched for uncertainty and edge boundaries.

It cannot tell us whether the AI surface also distorts boundaries that ordinary Search resolves clearly.

### External-method basis for correction

General evaluation guidance reviewed after the run:

- NIST AI RMF Core: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- NIST AI trustworthiness/representative conditions: https://airc.nist.gov/airmf-resources/airmf/3-sec-characteristics/
- OpenAI eval practice: https://openai.com/index/evals-drive-next-chapter-of-ai/
- Active-learning survey: https://aclanthology.org/2022.emnlp-main.414/
- Batch active-learning redundancy work: https://arxiv.org/abs/2107.14263

These sources do not prescribe “two SEO controls”. The project-level inference is narrower: a batch composed only of difficult/uncertain examples should not be presented as a broad behavioral sample, and adding stable real-world controls makes later deviations easier to interpret.

### Corrected OKNO_MSK controls

The earlier conversational idea of promoting old V1 `C15-008` is rejected because lineage audit proved that row itself was mis-specified and authoritative QF008 has no fresh direct representative probe.

Correct controls are:

#### C15-007 / QF007 — stable specialist-owner control

Query:

`панорамное остекление балкона`

Authoritative evidence:

- retry succeeded;
- 9/10 saved Search results were balcony/loggia-specific;
- dedicated panoramic-balcony page is primary;
- broad panoramic page was rank 10/supporting.

Control purpose: detect whether generative search spuriously collapses a strongly specific specialist task into a broad panoramic responsibility.

#### C15-018 / QF018 — stable transactional control

Query:

`замена окна на пластиковое цена москва`

Authoritative evidence:

- saved SERP contains multiple replacement-specific commercial pages plus generic installation pages;
- replacement specialist remains primary;
- generic installation is supporting.

Control purpose: detect whether generative search over-generalizes a clear replacement transaction into generic installation/product/informational responsibility.

## 4. Defect S15-D03 — representativeness claim boundary

The corrected eight-case set is intentionally decision-focused:

- 6 diagnostic uncertainty probes;
- 2 stable controls.

It is **not** a representative sample of the 2332 active phrases or of all site demand.

Therefore Step16/17 may use it to answer:

> Which high-value frozen decisions change, de-risk or fail under generative evidence, and do stable control boundaries remain stable?

It may **not** answer:

> What percentage of all queries behave differently in AI search?

A prevalence/generalization claim would require a separate representative-sampling design.

## 5. Defect S15-D04 — single-observation change handling

V1 pre-registered `CHANGE` but did not explicitly hand off a confirmation requirement.

V2 adds:

`confirmation_required_if_material_delta = true`

for all eight selected cases.

This does not define the Step16 confirmation mechanism. Step16 remains unvalidated and must research current Yandex/GenSearch/Alice behavior, temporal variance and exact replay/confirmation strategy before any provider call.

For stability controls specifically:

```text
ONE CONTROL_BREAK
!= AUTOMATIC ARCHITECTURE CHANGE
-> STEP16/17 CONFIRMATION + BATCH VALIDITY REVIEW
```

## 6. Corrected Step15 result

```text
CANDIDATE_UNIVERSE = 25
REVIEWED = 25
DIAGNOSTIC_PROBES_SELECTED = 6
STABILITY_CONTROLS_SELECTED = 2
SELECTED_TOTAL = 8
REJECTED = 16
HOLD = 1
ACCOUNTING = 25/25
SILENT_DROPS = 0
STEP14A_MATERIAL_DELTA_COVERAGE = 21/21
STEP16_PROVIDER_CALL_AUTHORIZED = false
STEP16_GENSEARCH_CALLS = 0
STEP16_EXECUTED = false
```

Selected IDs:

```text
DIAGNOSTIC_PROBE:
C15-004
C15-006
C15-010
C15-013
C15-019
C15-020

STABILITY_CONTROL:
C15-007
C15-018
```

## 7. V1 status

The following V1 artifacts remain in Git for audit history but are superseded as decision authority:

- `STEP_15_CASE_SELECTION_LEDGER_PART_01.tsv` ... `PART_05.tsv`
- `STEP_15_SELECTED_CASES_PART_01.tsv`
- `STEP_15_SELECTED_CASES_PART_02.tsv`

Canonical downstream rule:

```text
IF V1 AND V2 CONFLICT
-> V2 WINS
```

No Step16 execution may read a V1 query/owner/pair mapping as authoritative.

## 8. Non-repeat controls

```text
STEP15_V1_LINEAGE_DEFECT_RECORDED = true
STEP15_EXACT_QF_JOIN_REQUIRED = true
STEP15_PAIR_IDS_FROM_QF_AUTHORITY_ONLY = true
STEP15_REPRESENTATIVE_QUERY_FROM_CONFLICT_AUTHORITY_ONLY = true
STEP15_PRIMARY_OWNER_FROM_CONFLICT_AUTHORITY_OR_EXPLICIT_LATER_DELTA = true
STEP15_DIAGNOSTIC_AND_STABILITY_CONTROL_TRACKS_REQUIRED_WHEN_APPLICABLE = true
STEP15_DIAGNOSTIC_SET_NOT_REPRESENTATIVE_BY_DEFAULT = true
STEP15_CONTROL_WITHOUT_FRESH_ACCEPTED_BASELINE_FORBIDDEN_WHEN_FRESH_ALTERNATIVE_EXISTS = true
STEP15_MATERIAL_AI_CHANGE_REQUIRES_CONFIRMATION_HANDOFF = true
STEP15_LEDGER_MANIFEST_MUST_RESOLVE_TO_EXISTING_PARTS = true
STEP15_PROVIDER_CALLS = 0
```

## 9. Next legal action

Step 15 is closed only after V2 writeback/readback QA, including verification that the ledger manifest resolves to the five actual V2 ledger shards.

After that, the next legal stage is Step16 pre-step method/capability research and owner review only. No GenSearch call is authorized by this correction.
