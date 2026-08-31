import csv
import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
A1 = ROOT / 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V1.tsv'
A2 = ROOT / 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv'
ASSIGN = ROOT / 'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv'
HIST = ROOT / 'STEP_12_STRUCTURAL_ACTIONS.tsv'
HIER = ROOT / 'STEP_12_NEW_PAGE_HIERARCHY_PLAN.tsv'
PAIRS = ROOT / 'STEP_12_STEP13_CANDIDATE_PAIRS.tsv'
OUT = ROOT / 'STEP_12_D12_11_D12_06_QA.json'


def read(path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def norm(raw):
    raw = (raw or '').strip()
    if raw.startswith('PROPOSED_NEW:'):
        p = raw.split(':', 1)[1].strip()
        if not p.startswith('/'):
            p = '/' + p
        return 'https://okno-msk.ru' + p
    return raw if raw.startswith('http://') or raw.startswith('https://') else ''


def multi(v):
    return [x.strip() for x in (v or '').split('||') if x.strip()]


def clusters(v):
    return [x.strip() for x in (v or '').split(';') if x.strip()]


def parent_child(a, b):
    pa, pb = urlsplit(a), urlsplit(b)
    if pa.netloc != pb.netloc:
        return False
    xa, xb = pa.path.rstrip('/') + '/', pb.path.rstrip('/') + '/'
    return xa != xb and (xa.startswith(xb) or xb.startswith(xa))


a1 = read(A1)
a2 = read(A2)
assign = read(ASSIGN)
hist = read(HIST)
hier = read(HIER)
pairs = read(PAIRS)

by1 = {r['structural_unit_id']: r for r in a1}
by2 = {r['structural_unit_id']: r for r in a2}
page_uids = defaultdict(set)
for uid, row in by1.items():
    p = norm(row['primary_page_candidate'])
    if p:
        page_uids[p].add(uid)

source_uids = defaultdict(set)
for row in assign:
    uid = row.get('final_structural_unit_id', '').strip()
    src = row.get('original_effective_cluster_id', '').strip()
    if uid and src:
        source_uids[src].add(uid)

hist_true = {r['cluster_id'] for r in hist if r.get('step13_followup_required', '').strip().lower() == 'true'}

# Independently recompute only the expected pair-key universe from source artifacts.
expected = set()
for uid, row in by1.items():
    a, b = norm(row['primary_page_candidate']), norm(row['supporting_page'])
    if a and b and a != b:
        expected.add(tuple(sorted((a, b))))
for src, uids in source_uids.items():
    pages = sorted({norm(by1[u]['primary_page_candidate']) for u in uids if norm(by1[u]['primary_page_candidate'])})
    expected.update(tuple(sorted(x)) for x in combinations(pages, 2))
for h in hier:
    candidate = norm(h['proposed_url'])
    for other in multi(h.get('mandatory_inbound_links')) + multi(h.get('mandatory_outbound_links')):
        other = norm(other)
        if candidate and other and candidate != other:
            expected.add(tuple(sorted((candidate, other))))

actual_keys = [tuple(sorted((r['page_a'], r['page_b']))) for r in pairs]
actual = set(actual_keys)
missing_pairs = sorted(expected - actual)
extra_pairs = sorted(actual - expected)
duplicate_pair_rows = len(actual_keys) - len(actual)

# Independently recompute whether each emitted pair has a material direct-search trigger.
search_flag_mismatches = []
expected_dependency_uids = set()
covered_hist_true = set()
for row in pairs:
    rel_uids = {x for x in row['relation_structural_units'].split(';') if x}
    srcs = {x for x in row['source_effective_clusters'].split(';') if x}
    reasons = set()
    if srcs & hist_true:
        reasons.add('HIST')
        covered_hist_true.update(srcs & hist_true)
    for uid in rel_uids:
        src = by1[uid]
        if src.get('search_boundary_support') == 'MATERIAL_BOUNDARY_GAP':
            reasons.add('SEARCH_GAP')
        if 'PENDING_SEARCH' in src.get('recommendation_maturity', ''):
            reasons.add('SEARCH_PROVISIONAL')
    if 'SHARED_SOURCE_CLUSTER_PRIMARY_DESTINATIONS' in row['derivation_routes'] and not parent_child(row['page_a'], row['page_b']):
        reasons.add('NON_HIERARCHICAL_MULTI_PRIMARY')
    for h in hier:
        cand = norm(h['proposed_url'])
        if cand in {row['page_a'], row['page_b']} and 'MATERIAL' in h.get('search_boundary_status', ''):
            other = row['page_b'] if cand == row['page_a'] else row['page_a']
            hlinks = {norm(x) for x in multi(h.get('mandatory_inbound_links')) + multi(h.get('mandatory_outbound_links'))}
            if other in hlinks:
                reasons.add('HIERARCHY_SEARCH_GAP')
    expected_true = bool(reasons)
    actual_true = row['later_direct_search_check_needed'] == 'true'
    if expected_true != actual_true:
        search_flag_mismatches.append(row['pair_id'])
    if expected_true:
        expected_dependency_uids.update(rel_uids)

actual_dependency_uids = {r['structural_unit_id'] for r in a2 if r['step13_dependency_required'] == 'true'}
missing_dependency_uids = sorted(expected_dependency_uids - actual_dependency_uids)
extra_dependency_uids = sorted(actual_dependency_uids - expected_dependency_uids)

dep_high = [r['structural_unit_id'] for r in a2 if r['step13_dependency_required'] == 'true' and r['final_confidence'] == 'HIGH']
dep_final = [r['structural_unit_id'] for r in a2 if r['step13_dependency_required'] == 'true' and r['recommendation_maturity'] == 'FINAL_WITHIN_STEP12_EVIDENCE']
canonical = {'FINAL_WITHIN_STEP12_EVIDENCE', 'PROVISIONAL_PENDING_STEP13_CONFLICT_CHECK', 'DEFERRED_PENDING_MISSING_EVIDENCE'}
noncanonical = [r['structural_unit_id'] for r in a2 if r['recommendation_maturity'] not in canonical]

hier_pages = {norm(h['proposed_url']) for h in hier}
hierarchy_not_materialized = [
    r['structural_unit_id'] for r in a2
    if norm(r['primary_page_candidate']) in hier_pages and not r['hierarchy_clarity'].startswith('MATERIALIZED_')
]

forbidden_headers = [h for h in (pairs[0].keys() if pairs else []) if h.lower() in {'cannibalization_verdict', 'harmful_competition_verdict', 'final_conflict_verdict'}]
self_declared_verdict_cells = []
for row in pairs:
    for k, v in row.items():
        low = (v or '').lower()
        if 'confirmed_harmful' in low or 'confirmed_cannibal' in low:
            self_declared_verdict_cells.append(f"{row['pair_id']}:{k}")

hist_true_without_derived_pair = sorted(hist_true - covered_hist_true)

qa = {
    'status': 'STEP12_D12_11_D12_06_INDEPENDENT_PASS',
    'source_action_rows_v1': len(a1),
    'corrected_action_rows_v2': len(a2),
    'assignment_rows': len(assign),
    'expected_pair_keys': len(expected),
    'actual_pair_rows': len(pairs),
    'missing_pair_keys': len(missing_pairs),
    'extra_pair_keys': len(extra_pairs),
    'duplicate_pair_rows': duplicate_pair_rows,
    'search_flag_mismatch_rows': len(search_flag_mismatches),
    'pairs_requiring_direct_step13_search_check': sum(r['later_direct_search_check_needed'] == 'true' for r in pairs),
    'expected_dependency_units': len(expected_dependency_uids),
    'actual_dependency_units': len(actual_dependency_uids),
    'missing_dependency_units': len(missing_dependency_uids),
    'extra_dependency_units': len(extra_dependency_uids),
    'dependency_high_rows': len(dep_high),
    'dependency_final_maturity_rows': len(dep_final),
    'noncanonical_maturity_rows': len(noncanonical),
    'hierarchy_candidate_pages': len(hier_pages),
    'hierarchy_not_materialized_in_v2': len(hierarchy_not_materialized),
    'historical_manual_followup_true_clusters': len(hist_true),
    'historical_true_clusters_without_any_derived_pair': len(hist_true_without_derived_pair),
    'forbidden_step13_verdict_columns': len(forbidden_headers),
    'self_declared_harm_verdict_cells': len(self_declared_verdict_cells),
    'step13_executed': False,
    'details': {
        'missing_pair_keys': missing_pairs[:20],
        'extra_pair_keys': extra_pairs[:20],
        'search_flag_mismatch_pair_ids': search_flag_mismatches[:20],
        'missing_dependency_units': missing_dependency_uids[:20],
        'extra_dependency_units': extra_dependency_uids[:20],
        'dependency_high_units': dep_high[:20],
        'dependency_final_units': dep_final[:20],
        'noncanonical_maturity_units': noncanonical[:20],
        'hierarchy_not_materialized_units': hierarchy_not_materialized[:20],
        'historical_true_clusters_without_pair': hist_true_without_derived_pair[:20],
    },
    'verification_origin': 'INDEPENDENT_RECOMPUTATION_FROM_SOURCE_ARTIFACTS_NOT_GENERATOR_QA',
}

fail_keys = [
    'missing_pair_keys', 'extra_pair_keys', 'duplicate_pair_rows', 'search_flag_mismatch_rows',
    'missing_dependency_units', 'extra_dependency_units', 'dependency_high_rows',
    'dependency_final_maturity_rows', 'noncanonical_maturity_rows',
    'hierarchy_not_materialized_in_v2', 'historical_true_clusters_without_any_derived_pair',
    'forbidden_step13_verdict_columns', 'self_declared_harm_verdict_cells',
]
if any(qa[k] for k in fail_keys):
    qa['status'] = 'FAIL'

OUT.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(qa, ensure_ascii=False, indent=2))
