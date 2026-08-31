import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGETS = [
    'PVC_DOOR_INSTALLATION_SERVICE',
    'PVC_WINDOW_OPERATION_DIY',
    'REHAU_OTHER_BRAND_COMPARISON_INFO',
    'WINDOW_DEMOLITION_SERVICE',
]


def read(name):
    with (ROOT / name).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))

assign = read('STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv')
units = {r['structural_unit_id']: r for r in read('STEP_12_STRUCTURAL_UNITS_V5.tsv')}
actions = {r['structural_unit_id']: r for r in read('STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv')}
s11 = {r['phrase']: r for r in read('STEP_11_PHRASE_PAGE_MAP.tsv')}
s09 = {r['query']: r for r in read('STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv')}
hist = {r['phrase']: r for r in read('STEP_12_PHRASE_ACTION_MAP.tsv')}

members = defaultdict(list)
for r in assign:
    if r['final_structural_unit_id'] in TARGETS:
        members[r['final_structural_unit_id']].append(r)

rows = []
summary = []
for uid in TARGETS:
    if uid not in units or uid not in actions:
        raise RuntimeError(f'Missing target unit/action {uid}')
    rs = members[uid]
    if not rs:
        raise RuntimeError(f'No members for {uid}')
    u = units[uid]
    a = actions[uid]
    step11_targets = Counter()
    step11_states = Counter()
    direct_search = 0
    hist_targets = Counter()
    for r in rs:
        p = r['phrase']
        e11 = s11[p]
        if e11['target_url']:
            step11_targets[e11['target_url']] += 1
        step11_states[e11['ownership_state']] += 1
        e09 = s09.get(p)
        if e09:
            direct_search += 1
        h = hist.get(p, {})
        ht = h.get('target_or_new_page', '')
        if ht:
            hist_targets[ht] += 1
        rows.append({
            'structural_unit_id': uid,
            'phrase': p,
            'final_unit_task': r['final_unit_task'],
            'assignment_origin': r['assignment_origin'],
            'assignment_correction_reason': r['correction_reason'],
            'step11_ownership_state': e11['ownership_state'],
            'step11_target_url': e11['target_url'],
            'step11_mapping_reason': e11['mapping_reason'],
            'step11_evidence_provenance': e11['evidence_provenance'],
            'step09_direct_evidence_present': 'true' if e09 else 'false',
            'step09_job_type': e09.get('job_type','') if e09 else '',
            'step09_result_type': e09.get('result_type','') if e09 else '',
            'step09_decision': e09.get('decision','') if e09 else '',
            'historical_step12_action': h.get('structural_action',''),
            'historical_step12_target': ht,
        })
    summary.append({
        'structural_unit_id': uid,
        'phrase_count': len(rs),
        'user_task': u['user_task'],
        'intent_type': u['intent_type'],
        'business_scope_state': u['business_scope_state'],
        'unit_page_role': u['unit_page_role'],
        'v5_primary_page_candidate': u['primary_page_candidate'],
        'v5_supporting_page': u['supporting_page'],
        'v2_structural_action': a['structural_action'],
        'v2_primary_page_candidate': a['primary_page_candidate'],
        'v2_supporting_page': a['supporting_page'],
        'v2_search_boundary_support': a['search_boundary_support'],
        'v2_recommendation_maturity': a['recommendation_maturity'],
        'v2_final_confidence': a['final_confidence'],
        'step11_target_distribution': json.dumps(dict(step11_targets), ensure_ascii=False, sort_keys=True),
        'step11_ownership_state_distribution': json.dumps(dict(step11_states), ensure_ascii=False, sort_keys=True),
        'step09_direct_member_queries': direct_search,
        'historical_step12_target_distribution': json.dumps(dict(hist_targets), ensure_ascii=False, sort_keys=True),
        'unit_reason': u['unit_reason'],
    })

with (ROOT / 'STEP_12_D12_14_REVIEW_PACKET.tsv').open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter='\t', lineterminator='\n')
    w.writeheader(); w.writerows(rows)
with (ROOT / 'STEP_12_D12_14_REVIEW_SUMMARY.tsv').open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(summary[0].keys()), delimiter='\t', lineterminator='\n')
    w.writeheader(); w.writerows(summary)

md = ['# Step 12 — D12-14 evidence review packet', '', 'This packet is diagnostic only. It does not choose targets automatically.', '']
for s in summary:
    md += [
        f"## {s['structural_unit_id']}",
        '',
        f"- phrase count: {s['phrase_count']}",
        f"- user task: {s['user_task']}",
        f"- intent: {s['intent_type']}",
        f"- business scope: {s['business_scope_state']}",
        f"- unit page role: {s['unit_page_role']}",
        f"- V5 primary/supporting: `{s['v5_primary_page_candidate']}` / `{s['v5_supporting_page']}`",
        f"- V2 action: `{s['v2_structural_action']}`",
        f"- V2 primary/supporting: `{s['v2_primary_page_candidate']}` / `{s['v2_supporting_page']}`",
        f"- Step11 target distribution: `{s['step11_target_distribution']}`",
        f"- Step11 ownership distribution: `{s['step11_ownership_state_distribution']}`",
        f"- direct Step09 member queries: {s['step09_direct_member_queries']}",
        f"- historical Step12 target distribution: `{s['historical_step12_target_distribution']}`",
        f"- unit reason: {s['unit_reason']}",
        '',
        'Member phrases and per-phrase evidence are in `STEP_12_D12_14_REVIEW_PACKET.tsv`.',
        '',
    ]
(ROOT / 'STEP_12_D12_14_REVIEW_PACKET.md').write_text('\n'.join(md) + '\n', encoding='utf-8')

print(json.dumps({'status':'D12_14_REVIEW_PACKET_READY','units':len(summary),'phrase_rows':len(rows)}, ensure_ascii=False))
