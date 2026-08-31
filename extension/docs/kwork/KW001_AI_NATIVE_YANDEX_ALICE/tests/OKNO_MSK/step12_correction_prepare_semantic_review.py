import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PHRASE_MAP = ROOT / 'STEP_11_PHRASE_PAGE_MAP.tsv'
HIST = ROOT / 'STEP_12_PHRASE_ACTION_MAP.tsv'
OUT_UNITS = ROOT / 'STEP_12_CORRECTION_OVERRIDE_UNIT_AUDIT.tsv'
OUT_REVIEW = ROOT / 'STEP_12_CORRECTION_SEMANTIC_REVIEW_INPUT.md'
OUT_QA = ROOT / 'STEP_12_CORRECTION_PREP_QA.json'

MANDATORY_MIXED = {
    'WINDOW_INSTALLATION_DIY_INFO',
    'PANORAMIC_WINDOWS_COMMERCIAL',
    'GLAZING_PERMISSION_INFO',
    'WOOD_WINDOWS_COMMERCIAL',
    'WINDOW_HARDWARE_INFO',
    'WINDOW_REPAIR_DIY_INFO',
    'WINDOW_HARDWARE_SHOPPING',
    'WINDOW_ACCESSORIES_SHOPPING',
}
NO_PAGE_OR_OUTSIDE_ACTIONS = {'NO_STANDALONE_PAGE', 'OUTSIDE_SCOPE_NO_ACTION'}


def read_tsv(path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def write_tsv(path, rows, fields):
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


phrase_rows = read_tsv(PHRASE_MAP)
hist_rows = read_tsv(HIST)
if len(phrase_rows) != 2332 or len(hist_rows) != 2332:
    raise RuntimeError(f'expected 2332 rows; step11={len(phrase_rows)} hist={len(hist_rows)}')
if len({r['phrase'] for r in phrase_rows}) != len(phrase_rows):
    raise RuntimeError('STEP_11 phrase keys are not unique')

overrides = [r for r in hist_rows if r['routing_override'] == 'true']
groups = defaultdict(list)
for r in overrides:
    key = (r['structural_unit_id'], r['target_or_new_page'], r['routing_reason'], r['routing_source'], r['phrase_structural_action'])
    groups[key].append(r)

unit_rows = []
covered = set()
for key, rows in sorted(groups.items(), key=lambda kv: kv[0][0]):
    unit_id, target, reason, source, phrase_action = key
    phrases = sorted(r['phrase'] for r in rows)
    covered.update(phrases)
    source_clusters = sorted({r['effective_cluster_id'] for r in rows if r['effective_cluster_id']})
    unit_rows.append({
        'historical_structural_unit_id': unit_id,
        'historical_phrase_count': len(rows),
        'source_effective_clusters': ';'.join(source_clusters),
        'historical_target_url': target,
        'historical_phrase_action': phrase_action,
        'historical_reason': reason,
        'historical_source': source,
        'review_status': 'REVIEW_REQUIRED_BEFORE_FINAL_UNIT',
        'primary_or_supporting_role': 'UNRESOLVED_IN_FIRST_PASS',
        'final_unit_id': '',
        'final_user_task': '',
        'final_target_or_support_page': '',
        'final_role': '',
        'final_confidence': '',
        'member_phrases': ' || '.join(phrases),
    })

fields = ['historical_structural_unit_id','historical_phrase_count','source_effective_clusters','historical_target_url','historical_phrase_action','historical_reason','historical_source','review_status','primary_or_supporting_role','final_unit_id','final_user_task','final_target_or_support_page','final_role','final_confidence','member_phrases']
write_tsv(OUT_UNITS, unit_rows, fields)
if len(overrides) != 191 or len(covered) != 191:
    raise RuntimeError(f'override accounting mismatch rows={len(overrides)} unique={len(covered)}')

cluster_members = defaultdict(list)
for r in phrase_rows:
    if r['effective_cluster_id']:
        cluster_members[r['effective_cluster_id']].append(r)

historical_cluster_action = {}
for r in hist_rows:
    cid = r['effective_cluster_id']
    if cid and cid not in historical_cluster_action and r['cluster_structural_action']:
        historical_cluster_action[cid] = r['cluster_structural_action']

review_clusters = set(MANDATORY_MIXED)
for cid, action in historical_cluster_action.items():
    if action in NO_PAGE_OR_OUTSIDE_ACTIONS:
        review_clusters.add(cid)

lines = [
    '# Step 12 correction — semantic review input','',
    'Purpose: review every known mixed unit plus every historical NO_STANDALONE/OUTSIDE unit for salvageable in-scope phrases before rebuilding structural actions.','',
    f'Historical lexical override phrases materialized separately: **{len(overrides)}** in `{OUT_UNITS.name}`.',
    f'Clusters in this review packet: **{len(review_clusters)}**.',''
]
for cid in sorted(review_clusters):
    rows = cluster_members.get(cid, [])
    lines += [f'## {cid}', f'- phrase count: **{len(rows)}**', f'- historical cluster action: `{historical_cluster_action.get(cid, "N/A")}`', f'- mandatory mixed review: `{str(cid in MANDATORY_MIXED).lower()}`', '- phrases:']
    for r in sorted(rows, key=lambda x: x['phrase']):
        lines.append(f"  - {r['phrase']}")
    lines.append('')
OUT_REVIEW.write_text('\n'.join(lines) + '\n', encoding='utf-8')

qa = {
    'status': 'PREPARED_FOR_SEMANTIC_CORRECTION_REVIEW',
    'step11_phrase_rows': len(phrase_rows),
    'historical_step12_phrase_rows': len(hist_rows),
    'historical_override_phrases': len(overrides),
    'historical_override_unique_phrases': len(covered),
    'historical_override_candidate_units': len(unit_rows),
    'mandatory_mixed_clusters': len(MANDATORY_MIXED),
    'no_page_or_outside_clusters_in_review': sum(1 for cid in review_clusters if historical_cluster_action.get(cid) in NO_PAGE_OR_OUTSIDE_ACTIONS),
    'total_clusters_in_semantic_review_packet': len(review_clusters),
    'defects_closed_by_this_preparation': [],
    'defects_still_open': ['D12-01','D12-02','D12-08','D12-09'],
}
OUT_QA.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(qa, ensure_ascii=False))
