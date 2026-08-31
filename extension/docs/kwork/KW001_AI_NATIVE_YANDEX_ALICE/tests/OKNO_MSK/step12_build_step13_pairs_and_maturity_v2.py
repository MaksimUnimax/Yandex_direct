import csv
import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
ACTIONS_V1 = ROOT / 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V1.tsv'
ASSIGNMENTS = ROOT / 'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv'
HISTORICAL = ROOT / 'STEP_12_STRUCTURAL_ACTIONS.tsv'
HIERARCHY = ROOT / 'STEP_12_NEW_PAGE_HIERARCHY_PLAN.tsv'
OUT_ACTIONS = ROOT / 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv'
OUT_PAIRS = ROOT / 'STEP_12_STEP13_CANDIDATE_PAIRS.tsv'
OUT_DEP = ROOT / 'STEP_12_MATURITY_DEPENDENCY_LEDGER.tsv'
OUT_QA = ROOT / 'STEP_12_D12_11_D12_06_GENERATOR_QA.json'


def read_tsv(path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def write_tsv(path, rows, fields):
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def norm_page(raw):
    raw = (raw or '').strip()
    if not raw:
        return ''
    if raw.startswith('PROPOSED_NEW:'):
        suffix = raw.split(':', 1)[1].strip()
        if not suffix.startswith('/'):
            suffix = '/' + suffix
        return 'https://okno-msk.ru' + suffix
    if raw.startswith('http://') or raw.startswith('https://'):
        return raw
    return ''


def split_multi(value):
    return [x.strip() for x in (value or '').split('||') if x.strip()]


def split_clusters(value):
    return [x.strip() for x in (value or '').split(';') if x.strip()]


def is_parent_child(a, b):
    pa, pb = urlsplit(a), urlsplit(b)
    if pa.netloc != pb.netloc:
        return False
    xa = pa.path.rstrip('/') + '/'
    xb = pb.path.rstrip('/') + '/'
    if xa == xb:
        return False
    return xa.startswith(xb) or xb.startswith(xa)


def dedupe(items):
    return list(dict.fromkeys(x for x in items if x))


def regenerate_confidence_reason(row, hierarchy_clarity, new_maturity, dependency, new_conf):
    old_reason = (row.get('confidence_downgrade_reason') or '').strip()
    reasons = []

    # Explicit deferred resolutions can contain a carefully reviewed concrete reason
    # (for example D12-14). Preserve that evidence wording if it is not stale.
    if new_maturity == 'DEFERRED_PENDING_MISSING_EVIDENCE':
        if old_reason and 'hierarchy is not yet finalized' not in old_reason.lower():
            reasons.append(old_reason)
        else:
            reasons.append('Deferred because a named material evidence gap remains.')
        if dependency:
            reasons.append('Adjacent page-role overlap also remains queued for Step 13 conflict verification.')
        return '; '.join(dedupe(reasons))

    business = row.get('business_truth', '')
    if business in {
        'UNVERIFIED_OR_CONDITIONAL',
        'CONDITIONAL_BROAD_PRODUCT_OFFER',
        'CONDITIONAL_STANDALONE_SERVICE_ROLE',
    }:
        reasons.append('Business truth or standalone page role remains conditional.')

    if row.get('search_boundary_support') == 'MATERIAL_BOUNDARY_GAP':
        reasons.append('Material Search page boundary is not directly probed.')

    if hierarchy_clarity == 'PENDING_FOR_PROPOSED_PAGE':
        reasons.append('New-page hierarchy is not yet finalized.')

    if row.get('task_coherence') != 'STRONG':
        reasons.append('Task coherence is not strong.')

    page_fit = row.get('current_page_fit', '')
    if page_fit in {'PARTIAL_OR_SUPPORTING_PAGE_FIT', 'PARTIAL_EXISTING_PAGE_FIT', 'REVIEW_REQUIRED'}:
        reasons.append('Current page fit is partial or supporting rather than a fully verified primary fit.')

    if dependency:
        reasons.append('Material adjacent page-role overlap remains for Step 13 conflict verification.')

    reasons = dedupe(reasons)
    if reasons:
        return '; '.join(reasons)
    if new_conf == 'HIGH':
        return 'Coherent task and current structural role are directly supported; no material unresolved Step-12 evidence dependency remains.'
    if new_conf == 'MEDIUM':
        return 'Recommendation remains medium-confidence because current page fit or evidence strength is partial.'
    return 'Recommendation remains low-confidence because a material unresolved evidence dependency remains.'


actions = read_tsv(ACTIONS_V1)
assignments = read_tsv(ASSIGNMENTS)
historical = read_tsv(HISTORICAL)
hierarchy = read_tsv(HIERARCHY)

if len(actions) != 160:
    raise RuntimeError(f'Expected 160 structural actions, got {len(actions)}')
if len(assignments) != 2332:
    raise RuntimeError(f'Expected 2332 phrase assignments, got {len(assignments)}')
if len(hierarchy) != 5:
    raise RuntimeError(f'Expected 5 hierarchy rows, got {len(hierarchy)}')

action_by_uid = {r['structural_unit_id']: r for r in actions}
if len(action_by_uid) != len(actions):
    raise RuntimeError('Duplicate structural_unit_id in actions V1')

hist_followup = {
    r['cluster_id']: (r.get('step13_followup_required', '').strip().lower() == 'true')
    for r in historical
}

members = defaultdict(list)
source_to_uids = defaultdict(set)
for row in assignments:
    uid = row.get('final_structural_unit_id', '').strip()
    if not uid:
        continue
    if uid not in action_by_uid:
        raise RuntimeError(f'Assignment references unknown structural unit: {uid}')
    members[uid].append(row['phrase'])
    src = row.get('original_effective_cluster_id', '').strip()
    if src:
        source_to_uids[src].add(uid)

page_to_uids = defaultdict(set)
for uid, row in action_by_uid.items():
    page = norm_page(row.get('primary_page_candidate'))
    if page:
        page_to_uids[page].add(uid)

pairs = {}


def add_pair(a, b, route, units=None, clusters=None, hierarchy_search_gap=False):
    a, b = norm_page(a), norm_page(b)
    if not a or not b or a == b:
        return
    key = tuple(sorted((a, b)))
    rec = pairs.setdefault(key, {
        'routes': set(),
        'units': set(),
        'clusters': set(),
        'hierarchy_search_gap': False,
    })
    rec['routes'].add(route)
    rec['units'].update(units or [])
    rec['clusters'].update(clusters or [])
    rec['hierarchy_search_gap'] = rec['hierarchy_search_gap'] or hierarchy_search_gap


# 1) Explicit primary/supporting edges materialized by the corrected structural units.
for uid, row in action_by_uid.items():
    primary = norm_page(row.get('primary_page_candidate'))
    supporting = norm_page(row.get('supporting_page'))
    if primary and supporting and primary != supporting:
        related = {uid} | page_to_uids.get(supporting, set())
        add_pair(
            primary,
            supporting,
            'EXPLICIT_PRIMARY_SUPPORTING_EDGE',
            units=related,
            clusters=split_clusters(row.get('source_effective_clusters')),
        )

# 2) If one upstream semantic source is now routed to multiple primary pages, every
# pair of those destinations belongs to the deterministic Step-13 candidate universe.
for source_cluster, uids in sorted(source_to_uids.items()):
    page_units = defaultdict(set)
    for uid in sorted(uids):
        page = norm_page(action_by_uid[uid].get('primary_page_candidate'))
        if page:
            page_units[page].add(uid)
    for a, b in combinations(sorted(page_units), 2):
        add_pair(
            a,
            b,
            'SHARED_SOURCE_CLUSTER_PRIMARY_DESTINATIONS',
            units=page_units[a] | page_units[b],
            clusters={source_cluster},
        )

# 3) New-page hierarchy is part of the final routing graph. It creates adjacency
# candidates but does not itself imply harmful competition.
hierarchy_by_page = {}
for row in hierarchy:
    candidate = norm_page(row['proposed_url'])
    hierarchy_by_page[candidate] = row
    material_gap = 'MATERIAL' in row.get('search_boundary_status', '')
    for link in split_multi(row.get('mandatory_inbound_links')):
        other = norm_page(link)
        related = page_to_uids.get(candidate, set()) | page_to_uids.get(other, set())
        clusters = set()
        for uid in related:
            clusters.update(split_clusters(action_by_uid[uid].get('source_effective_clusters')))
        add_pair(candidate, other, 'NEW_PAGE_HIERARCHY_INBOUND_EDGE', related, clusters, material_gap)
    for link in split_multi(row.get('mandatory_outbound_links')):
        other = norm_page(link)
        related = page_to_uids.get(candidate, set()) | page_to_uids.get(other, set())
        clusters = set()
        for uid in related:
            clusters.update(split_clusters(action_by_uid[uid].get('source_effective_clusters')))
        add_pair(candidate, other, 'NEW_PAGE_HIERARCHY_OUTBOUND_EDGE', related, clusters, material_gap)


def member_evidence(uids):
    chunks = []
    for uid in sorted(uids):
        phrases = sorted(set(members.get(uid, [])))
        sample = ' | '.join(phrases[:3])
        chunks.append(f'{uid}[{len(phrases)}]: {sample}')
    return ' || '.join(chunks)


pair_rows = []
for idx, ((page_a, page_b), rec) in enumerate(sorted(pairs.items()), 1):
    reasons = set()
    if any(hist_followup.get(c, False) for c in rec['clusters']):
        reasons.add('HISTORICAL_KNOWN_FOLLOWUP_SIGNAL_PRESERVED')
    for uid in rec['units']:
        row = action_by_uid[uid]
        if row.get('search_boundary_support') == 'MATERIAL_BOUNDARY_GAP':
            reasons.add('MATERIAL_SEARCH_BOUNDARY_GAP_IN_CONTRIBUTING_UNIT')
        if 'PENDING_SEARCH' in row.get('recommendation_maturity', ''):
            reasons.add('CONTRIBUTING_UNIT_ALREADY_SEARCH_PROVISIONAL')
    if rec['hierarchy_search_gap']:
        reasons.add('PROPOSED_PAGE_HIERARCHY_HAS_UNRESOLVED_SEARCH_BOUNDARY')
    if (
        'SHARED_SOURCE_CLUSTER_PRIMARY_DESTINATIONS' in rec['routes']
        and not is_parent_child(page_a, page_b)
    ):
        reasons.add('NON_HIERARCHICAL_MULTI_PRIMARY_ROUTE_FROM_SAME_SOURCE_CLUSTER')

    normal = set()
    if is_parent_child(page_a, page_b):
        normal.add('PARENT_CHILD_RELATION_CAN_BE_NORMAL_WHEN_TASK_BOUNDARIES_ARE_DISTINCT')
    if 'EXPLICIT_PRIMARY_SUPPORTING_EDGE' in rec['routes']:
        normal.add('PRIMARY_SUPPORTING_JOURNEY_RELATION_CAN_BE_NORMAL')
    if any(x.startswith('NEW_PAGE_HIERARCHY_') for x in rec['routes']):
        normal.add('PLANNED_INTERNAL_LINK_RELATION_DOES_NOT_PROVE_CONFLICT')
    if 'SHARED_SOURCE_CLUSTER_PRIMARY_DESTINATIONS' in rec['routes']:
        normal.add('SAME_UPSTREAM_FAMILY_CAN_NORMALLY_SPLIT_ACROSS_DISTINCT_USER_TASKS')

    tasks = sorted({action_by_uid[u]['user_task'] for u in rec['units'] if u in action_by_uid})
    a_units = sorted(page_to_uids.get(page_a, set()))
    b_units = sorted(page_to_uids.get(page_b, set()))
    a_phrases = {p for uid in a_units for p in members.get(uid, [])}
    b_phrases = {p for uid in b_units for p in members.get(uid, [])}
    pair_rows.append({
        'pair_id': f'P{idx:04d}',
        'page_a': page_a,
        'page_b': page_b,
        'derivation_routes': ';'.join(sorted(rec['routes'])),
        'source_effective_clusters': ';'.join(sorted(rec['clusters'])),
        'page_a_structural_units': ';'.join(a_units),
        'page_b_structural_units': ';'.join(b_units),
        'relation_structural_units': ';'.join(sorted(rec['units'])),
        'page_a_phrase_count': len(a_phrases),
        'page_b_phrase_count': len(b_phrases),
        'member_evidence': member_evidence(rec['units']),
        'adjacent_task': ' || '.join(tasks),
        'normal_overlap_rationale': ';'.join(sorted(normal)),
        'later_direct_search_check_needed': 'true' if reasons else 'false',
        'search_check_reason': ';'.join(sorted(reasons)) if reasons else 'NO_MATERIAL_DIRECT_SEARCH_TRIGGER_DERIVED_AT_STEP12',
        'derivation_origin': 'DETERMINISTIC_FROM_FINAL_STRUCTURAL_ROUTING_GRAPH_V5_ACTIONS_V1_HIERARCHY',
    })

pair_ids_by_uid = defaultdict(list)
search_reasons_by_uid = defaultdict(set)
for row in pair_rows:
    if row['later_direct_search_check_needed'] != 'true':
        continue
    units = [x for x in row['relation_structural_units'].split(';') if x]
    reasons = [x for x in row['search_check_reason'].split(';') if x]
    for uid in units:
        pair_ids_by_uid[uid].append(row['pair_id'])
        search_reasons_by_uid[uid].update(reasons)

# Materialize hierarchy clarity from the already accepted D12-07 plan.
for page, hrow in hierarchy_by_page.items():
    if page not in page_to_uids:
        raise RuntimeError(f'Hierarchy candidate page has no structural action owner: {page}')

v2 = []
dep_rows = []
for row in actions:
    uid = row['structural_unit_id']
    out = dict(row)
    primary = norm_page(row.get('primary_page_candidate'))
    old_maturity = row['recommendation_maturity']
    dependency = bool(pair_ids_by_uid.get(uid))

    if primary in hierarchy_by_page:
        hstatus = hierarchy_by_page[primary]['hierarchy_status']
        out['hierarchy_clarity'] = (
            'MATERIALIZED_SUPPORTED_HIERARCHY'
            if hstatus.startswith('EVIDENCE_SUPPORTED')
            else 'MATERIALIZED_PROVISIONAL_HIERARCHY'
        )

    if old_maturity.startswith('DEFERRED') or row['structural_action'] == 'DEFER_PENDING_EVIDENCE':
        new_maturity = 'DEFERRED_PENDING_MISSING_EVIDENCE'
    elif dependency:
        new_maturity = 'PROVISIONAL_PENDING_STEP13_CONFLICT_CHECK'
    elif old_maturity.startswith('PROVISIONAL'):
        new_maturity = 'DEFERRED_PENDING_MISSING_EVIDENCE'
    else:
        new_maturity = 'FINAL_WITHIN_STEP12_EVIDENCE'

    reasons = []
    if old_maturity != new_maturity:
        reasons.append(f'PREVIOUS_MATURITY={old_maturity}')
    if dependency:
        reasons.append('STEP13_PAIRS=' + ';'.join(sorted(pair_ids_by_uid[uid])))
        reasons.extend(sorted(search_reasons_by_uid[uid]))
    if new_maturity == 'DEFERRED_PENDING_MISSING_EVIDENCE' and not dependency:
        reasons.append('MATERIAL_NON_STEP13_EVIDENCE_DEPENDENCY_REMAINS')

    old_conf = row['final_confidence']
    if new_maturity == 'DEFERRED_PENDING_MISSING_EVIDENCE':
        new_conf = 'LOW'
    elif new_maturity == 'PROVISIONAL_PENDING_STEP13_CONFLICT_CHECK' and old_conf == 'HIGH':
        new_conf = 'MEDIUM'
    else:
        new_conf = old_conf

    why = regenerate_confidence_reason(
        row,
        out['hierarchy_clarity'],
        new_maturity,
        dependency,
        new_conf,
    )

    out['recommendation_maturity'] = new_maturity
    out['final_confidence'] = new_conf
    out['confidence_downgrade_reason'] = why
    out['confidence_reason_origin'] = 'REGENERATED_FROM_CURRENT_V2_EVIDENCE_AFTER_HIERARCHY_AND_DEPENDENCY_OVERLAY'
    out['step13_dependency_required'] = 'true' if dependency else 'false'
    out['step13_candidate_pair_ids'] = ';'.join(sorted(pair_ids_by_uid.get(uid, [])))
    out['maturity_dependency_detail'] = ';'.join(dict.fromkeys(reasons)) if reasons else 'NONE'
    out['maturity_origin'] = 'DERIVED_FROM_DETERMINISTIC_STEP13_PAIR_GRAPH_AND_EXPLICIT_MISSING_EVIDENCE'
    v2.append(out)

    dep_rows.append({
        'structural_unit_id': uid,
        'structural_action': row['structural_action'],
        'primary_page_candidate': row['primary_page_candidate'],
        'previous_maturity': old_maturity,
        'corrected_maturity': new_maturity,
        'previous_confidence': old_conf,
        'corrected_confidence': new_conf,
        'step13_dependency_required': 'true' if dependency else 'false',
        'step13_candidate_pair_ids': ';'.join(sorted(pair_ids_by_uid.get(uid, []))),
        'dependency_reason': ';'.join(dict.fromkeys(reasons)) if reasons else 'NONE',
        'evidence_origin': 'COMPUTED_FROM_DATA',
    })

canonical_maturity = {
    'FINAL_WITHIN_STEP12_EVIDENCE',
    'PROVISIONAL_PENDING_STEP13_CONFLICT_CHECK',
    'DEFERRED_PENDING_MISSING_EVIDENCE',
}
stale_hierarchy_reason_rows = [
    r for r in v2
    if r['hierarchy_clarity'].startswith('MATERIALIZED_')
    and 'hierarchy is not yet finalized' in r['confidence_downgrade_reason'].lower()
]
reason_regenerated_rows = [
    r for r in v2
    if r.get('confidence_reason_origin') == 'REGENERATED_FROM_CURRENT_V2_EVIDENCE_AFTER_HIERARCHY_AND_DEPENDENCY_OVERLAY'
]
qa = {
    'status': 'CANDIDATE_D12_11_D12_06_READY_FOR_INDEPENDENT_VERIFICATION',
    'source_action_rows': len(actions),
    'source_assignment_rows': len(assignments),
    'candidate_pairs': len(pair_rows),
    'pairs_requiring_direct_step13_search_check': sum(r['later_direct_search_check_needed'] == 'true' for r in pair_rows),
    'dependency_action_rows': sum(r['step13_dependency_required'] == 'true' for r in v2),
    'dependency_high_rows': sum(r['step13_dependency_required'] == 'true' and r['final_confidence'] == 'HIGH' for r in v2),
    'dependency_without_explicit_provisional_or_deferred_maturity': sum(
        r['step13_dependency_required'] == 'true'
        and r['recommendation_maturity'] not in {'PROVISIONAL_PENDING_STEP13_CONFLICT_CHECK', 'DEFERRED_PENDING_MISSING_EVIDENCE'}
        for r in v2
    ),
    'noncanonical_maturity_rows': sum(r['recommendation_maturity'] not in canonical_maturity for r in v2),
    'new_page_hierarchy_rows_expected': len(hierarchy),
    'new_page_hierarchy_owner_action_rows': sum(
        norm_page(r['primary_page_candidate']) in hierarchy_by_page
        and r['hierarchy_clarity'].startswith('MATERIALIZED_')
        for r in v2
    ),
    'new_page_hierarchy_rows_materialized_in_actions': len({
        norm_page(r['primary_page_candidate'])
        for r in v2
        if norm_page(r['primary_page_candidate']) in hierarchy_by_page
        and r['hierarchy_clarity'].startswith('MATERIALIZED_')
    }),
    'd12_15_reason_regenerated_rows': len(reason_regenerated_rows),
    'd12_15_stale_materialized_hierarchy_reason_rows': len(stale_hierarchy_reason_rows),
    'historical_manual_followup_true_clusters': sum(hist_followup.values()),
    'historical_manual_followup_used_as_pair_universe_source': False,
    'pair_universe_derivation_routes': sorted({route for p in pair_rows for route in p['derivation_routes'].split(';')}),
    'defects_closed_by_generator_alone': [],
    'defects_candidate_for_closure_after_independent_verification': ['D12-15', 'D12-11', 'D12-06'],
}
if (
    qa['dependency_high_rows']
    or qa['dependency_without_explicit_provisional_or_deferred_maturity']
    or qa['noncanonical_maturity_rows']
    or qa['new_page_hierarchy_rows_materialized_in_actions'] != qa['new_page_hierarchy_rows_expected']
    or qa['d12_15_reason_regenerated_rows'] != len(v2)
    or qa['d12_15_stale_materialized_hierarchy_reason_rows']
):
    qa['status'] = 'FAIL'

write_tsv(OUT_PAIRS, pair_rows, list(pair_rows[0].keys()))
write_tsv(OUT_ACTIONS, v2, list(v2[0].keys()))
write_tsv(OUT_DEP, dep_rows, list(dep_rows[0].keys()))
OUT_QA.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(qa, ensure_ascii=False, indent=2))
