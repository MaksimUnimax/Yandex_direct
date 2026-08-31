import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / 'STEP_12_CORRECTION_DEFECT_LEDGER.tsv'
STATE = ROOT / 'STEP_12_CORRECTION_CURRENT_STATE.json'
GEN_QA = ROOT / 'STEP_12_D12_11_D12_06_GENERATOR_QA.json'
IND_QA = ROOT / 'STEP_12_D12_11_D12_06_QA.json'
CONF_QA = ROOT / 'STEP_12_CONFIDENCE_QA_V1.json'
REPORT = ROOT / 'STEP_12_D12_13_11_06_ACCEPTANCE_2026-08-31.md'


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


g = read_json(GEN_QA)
q = read_json(IND_QA)
c = read_json(CONF_QA)

# D12-13 canonical new-page target integrity.
assert c['status'] == 'CANDIDATE_CONFIDENCE_V1_READY_FOR_MANUAL_REVIEW'
assert c['new_page_action_rows'] == 6
assert c['new_page_action_primary_target_mismatches'] == 0
assert c['replacement_service_primary_target_correct'] is True
assert c['replacement_service_existing_installation_preserved_as_supporting'] is True
assert g['new_page_hierarchy_rows_expected'] == 5
assert g['new_page_hierarchy_rows_materialized_in_actions'] == 5

# D12-11 maturity is derived from complete downstream dependency graph.
assert g['dependency_action_rows'] == 104
assert g['dependency_high_rows'] == 0
assert g['dependency_without_explicit_provisional_or_deferred_maturity'] == 0
assert q['dependency_high_rows'] == 0
assert q['dependency_final_maturity_rows'] == 0
assert q['noncanonical_maturity_rows'] == 0

# D12-06 pair universe is deterministic and independently recomputed.
assert g['candidate_pairs'] == 189
assert g['pairs_requiring_direct_step13_search_check'] == 171
assert g['historical_manual_followup_used_as_pair_universe_source'] is False
assert q['status'] == 'STEP12_D12_11_D12_06_INDEPENDENT_PASS'
assert q['expected_pair_keys'] == 189
assert q['actual_pair_rows'] == 189
assert q['missing_pair_keys'] == 0
assert q['extra_pair_keys'] == 0
assert q['duplicate_pair_rows'] == 0
assert q['search_flag_mismatch_rows'] == 0
assert q['expected_dependency_units'] == 104
assert q['actual_dependency_units'] == 104
assert q['missing_dependency_units'] == 0
assert q['extra_dependency_units'] == 0
assert q['hierarchy_candidate_pages'] == 5
assert q['hierarchy_not_materialized_in_v2'] == 0
assert q['historical_true_clusters_without_any_derived_pair'] == 0
assert q['forbidden_step13_verdict_columns'] == 0
assert q['self_declared_harm_verdict_cells'] == 0
assert q['step13_executed'] is False
assert q['verification_origin'] == 'INDEPENDENT_RECOMPUTATION_FROM_SOURCE_ARTIFACTS_NOT_GENERATOR_QA'

# Update defect ledger only after all persisted evidence passes.
with LEDGER.open(encoding='utf-8', newline='') as f:
    rows = list(csv.DictReader(f, delimiter='\t'))
fields = list(rows[0].keys())
by_id = {r['defect_id']: r for r in rows}
for defect in ('D12-13', 'D12-11', 'D12-06'):
    assert by_id[defect]['status'] == 'OPEN'

by_id['D12-13']['status'] = 'VERIFIED_FIXED'
by_id['D12-13']['correction_artifact'] = 'STEP_12_D12_13_NEW_PAGE_ACTION_TARGET_DISCONNECT_2026-08-31.md | STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V1.tsv | STEP_12_CONFIDENCE_QA_V1.json | STEP_12_D12_11_D12_06_GENERATOR_QA.json | STEP_12_D12_11_D12_06_QA.json | STEP_12_D12_13_11_06_ACCEPTANCE_2026-08-31.md'
by_id['D12-13']['notes'] += ' | Closed only after all six NEW_* action rows had zero canonical-target mismatches, replacement service pointed to PROPOSED_NEW:/uslugi/zamena-okon/ with installation kept as supporting context, and the downstream graph proved all 5 hierarchy candidate pages had structural-action owners.'

by_id['D12-11']['status'] = 'VERIFIED_FIXED'
by_id['D12-11']['correction_artifact'] = 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv | STEP_12_MATURITY_DEPENDENCY_LEDGER.tsv | STEP_12_D12_11_D12_06_GENERATOR_QA.json | STEP_12_D12_11_D12_06_QA.json | STEP_12_D12_13_11_06_ACCEPTANCE_2026-08-31.md'
by_id['D12-11']['notes'] += ' | Closed after 104/104 derived dependency units were explicit, dependency HIGH rows=0, dependency FINAL maturity rows=0, and independent recomputation passed.'

by_id['D12-06']['status'] = 'VERIFIED_FIXED'
by_id['D12-06']['correction_artifact'] = 'STEP_12_STEP13_CANDIDATE_PAIRS.tsv | STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv | STEP_12_MATURITY_DEPENDENCY_LEDGER.tsv | STEP_12_D12_11_D12_06_GENERATOR_QA.json | STEP_12_D12_11_D12_06_QA.json | STEP_12_D12_13_11_06_ACCEPTANCE_2026-08-31.md'
by_id['D12-06']['notes'] += ' | Closed after deterministic graph produced 189 unique candidate pairs, independent recomputation matched 189/189 with zero missing/extra/duplicate pairs, all 9 historical manual follow-up families were covered without using the manual list as the universe source, and Step13 remained unexecuted.'

with LEDGER.open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
    w.writeheader()
    w.writerows(rows)

state = read_json(STATE)
assert state['open_defects'] == ['D12-13', 'D12-11', 'D12-06', 'D12-05']
state['open_defects'] = ['D12-05']
for defect in ('D12-13', 'D12-11', 'D12-06'):
    if defect not in state['verified_fixed_defects']:
        state['verified_fixed_defects'].append(defect)
state['verified_fixed_defects'] = sorted(state['verified_fixed_defects'], key=lambda x: int(x.split('-')[1]))
state['current_correction_item'] = 'D12-05'
state['next_action'] = 'D12-05 only: build independent final Step12 QA with explicit evidence-origin ledger and validate SPLIT/MERGE by attached support evidence rather than blanket failure. Step13 remains blocked and unexecuted.'
STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

REPORT.write_text(f'''# Step 12 — D12-13 / D12-11 / D12-06 acceptance

Date: 2026-08-31
Verdict: **VERIFIED_FIXED** for D12-13, D12-11 and D12-06. Step 12 is still not complete because D12-05 remains open. Step 13 is blocked and was not executed.

## D12-13 — new-page action target disconnect

The fail-closed graph run exposed that `WINDOW_REPLACEMENT_SERVICE` said `NEW_COMMERCIAL_PAGE` while still naming the current installation page as primary. The action builder was corrected so every NEW_* action gets its primary target from canonical new-page evidence.

Persisted verification:
- NEW_* structural-action rows: {c['new_page_action_rows']};
- primary-target mismatches: {c['new_page_action_primary_target_mismatches']};
- replacement-service proposed target correct: {str(c['replacement_service_primary_target_correct']).lower()};
- current installation page preserved only as supporting context: {str(c['replacement_service_existing_installation_preserved_as_supporting']).lower()};
- hierarchy candidate pages expected/materialized: {g['new_page_hierarchy_rows_expected']}/{g['new_page_hierarchy_rows_materialized_in_actions']} unique pages;
- hierarchy owner action rows: {g['new_page_hierarchy_owner_action_rows']} (multiple structural units may legitimately share one proposed page).

## D12-11 — provisional dependencies hidden by final action

The final Step-12 action maturity is now derived from the deterministic downstream page-pair graph rather than a manually selected boolean.

Persisted verification:
- structural units with material Step-13 dependency: {g['dependency_action_rows']};
- dependent rows still HIGH: {q['dependency_high_rows']};
- dependent rows still FINAL_WITHIN_STEP12_EVIDENCE: {q['dependency_final_maturity_rows']};
- noncanonical maturity rows: {q['noncanonical_maturity_rows']}.

A dependency therefore changes the recommendation statement itself to `PROVISIONAL_PENDING_STEP13_CONFLICT_CHECK` (or remains deferred for a separate missing-evidence reason), rather than hiding uncertainty behind a side flag.

## D12-06 — deterministic Step-13 candidate universe

The handoff is now generated from actual corrected routing relationships, not analyst memory.

Persisted verification:
- candidate page pairs: {q['actual_pair_rows']};
- pairs requiring direct Step-13 Search review: {q['pairs_requiring_direct_step13_search_check']};
- missing / extra / duplicate pair rows: {q['missing_pair_keys']} / {q['extra_pair_keys']} / {q['duplicate_pair_rows']};
- expected / actual dependency units: {q['expected_dependency_units']} / {q['actual_dependency_units']};
- historical manual follow-up families: {q['historical_manual_followup_true_clusters']};
- historical families without a derived pair: {q['historical_true_clusters_without_any_derived_pair']};
- forbidden Step-13 verdict columns: {q['forbidden_step13_verdict_columns']};
- self-declared harmful-cannibalization verdict cells: {q['self_declared_harm_verdict_cells']};
- Step 13 executed: {str(q['step13_executed']).lower()}.

Independent verification origin: `{q['verification_origin']}`.

## QA lesson discovered during closure

A prior fail-closed attempt revealed that the generator counted **10 action rows** against **5 hierarchy pages**. That was the wrong unit of measurement because a proposed page can legitimately have more than one structural-unit owner. The QA was corrected to retain both metrics:
- owner action rows = {g['new_page_hierarchy_owner_action_rows']};
- unique hierarchy pages materialized = {g['new_page_hierarchy_rows_materialized_in_actions']}.

This is carried into D12-05: QA must verify the exact property it claims, at the correct unit of analysis.

## Boundary

This acceptance does **not** diagnose cannibalization and does not start Step 13. The 189 pairs are only the complete candidate universe for later proof/rejection of harmful overlap.
''', encoding='utf-8')

print(json.dumps({
    'status': 'D12_13_11_06_CLOSURE_READY',
    'open_defects_after': state['open_defects'],
    'pair_rows': q['actual_pair_rows'],
    'dependency_units': q['actual_dependency_units'],
    'hierarchy_pages_materialized': g['new_page_hierarchy_rows_materialized_in_actions'],
    'step13_executed': q['step13_executed'],
}, ensure_ascii=False))
