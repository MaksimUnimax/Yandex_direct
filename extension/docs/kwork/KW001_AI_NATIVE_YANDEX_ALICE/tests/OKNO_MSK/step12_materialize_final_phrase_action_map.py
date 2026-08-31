import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSIGN = ROOT / 'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv'
ACTIONS = ROOT / 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv'
OUT = ROOT / 'STEP_12_PHRASE_ACTION_MAP_FINAL.tsv'


def read(path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def write(path, rows, fields):
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


assignments = read(ASSIGN)
actions = read(ACTIONS)
if len(assignments) != 2332:
    raise RuntimeError(f'Expected 2332 assignment rows, got {len(assignments)}')
if len(actions) != 160:
    raise RuntimeError(f'Expected 160 structural action rows, got {len(actions)}')

ids = [r['structural_unit_id'] for r in actions]
dups = [k for k, v in Counter(ids).items() if v > 1]
if dups:
    raise RuntimeError(f'Duplicate structural action unit ids: {dups[:10]}')
action_by = {r['structural_unit_id']: r for r in actions}

out = []
for a in assignments:
    uid = a['final_structural_unit_id']
    if uid:
        if uid not in action_by:
            raise RuntimeError(f'Assigned structural unit missing action: {uid} / {a["phrase"]}')
        x = action_by[uid]
        out.append({
            'phrase': a['phrase'],
            'original_effective_cluster_id': a['original_effective_cluster_id'],
            'final_structural_unit_id': uid,
            'final_unit_task': a['final_unit_task'],
            'intent_type': a['intent_type'],
            'business_scope_state': a['business_scope_state'],
            'unit_page_role': a['unit_page_role'],
            'structural_action': x['structural_action'],
            'primary_page_candidate': x['primary_page_candidate'],
            'supporting_page': x['supporting_page'],
            'recommendation_maturity': x['recommendation_maturity'],
            'final_confidence': x['final_confidence'],
            'step13_dependency_required': x['step13_dependency_required'],
            'step13_candidate_pair_ids': x['step13_candidate_pair_ids'],
            'assignment_origin': a['assignment_origin'],
            'correction_reason': a['correction_reason'],
            'action_origin': 'JOINED_FROM_STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2',
        })
    else:
        out.append({
            'phrase': a['phrase'],
            'original_effective_cluster_id': a['original_effective_cluster_id'],
            'final_structural_unit_id': '',
            'final_unit_task': '',
            'intent_type': a['intent_type'],
            'business_scope_state': a['business_scope_state'],
            'unit_page_role': '',
            'structural_action': 'DEFER_UNRESOLVED',
            'primary_page_candidate': '',
            'supporting_page': '',
            'recommendation_maturity': 'DEFERRED_PENDING_MISSING_EVIDENCE',
            'final_confidence': 'LOW',
            'step13_dependency_required': 'false',
            'step13_candidate_pair_ids': '',
            'assignment_origin': a['assignment_origin'],
            'correction_reason': a['correction_reason'],
            'action_origin': 'SEARCH_REQUIRED_NO_STRUCTURAL_ACTION',
        })

write(OUT, out, list(out[0].keys()))
print({
    'rows': len(out),
    'assigned_rows': sum(bool(r['final_structural_unit_id']) for r in out),
    'search_required_rows': sum(not r['final_structural_unit_id'] for r in out),
})
