import csv
import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
S11 = ROOT / 'STEP_11_PHRASE_PAGE_MAP.tsv'
ASSIGN = ROOT / 'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv'
UNITS = ROOT / 'STEP_12_STRUCTURAL_UNITS_V5.tsv'
ACTIONS_V1 = ROOT / 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V1.tsv'
ACTIONS = ROOT / 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv'
FINAL_MAP = ROOT / 'STEP_12_PHRASE_ACTION_MAP_FINAL.tsv'
NEW_EVIDENCE = ROOT / 'STEP_12_NEW_PAGE_EVIDENCE_V2.tsv'
HIERARCHY = ROOT / 'STEP_12_NEW_PAGE_HIERARCHY_PLAN.tsv'
PAIRS = ROOT / 'STEP_12_STEP13_CANDIDATE_PAIRS.tsv'
REVIEW = ROOT / 'STEP_12_QA_REVIEW_LEDGER.tsv'
SM_CASES = ROOT / 'STEP_12_SPLIT_MERGE_REGRESSION_CASES.tsv'
STATE = ROOT / 'STEP_12_CORRECTION_CURRENT_STATE.json'

OUT_CHECKS = ROOT / 'STEP_12_QA_CHECKS.tsv'
OUT_REVIEW = ROOT / 'STEP_12_QA_REVIEW_RESULTS.tsv'
OUT_SM = ROOT / 'STEP_12_SPLIT_MERGE_REGRESSION_RESULTS.tsv'
OUT_FINDINGS = ROOT / 'STEP_12_QA_FINDINGS.tsv'
OUT_JSON = ROOT / 'STEP_12_QA_CANDIDATE.json'

ALLOWED_ORIGINS = {'COMPUTED_FROM_DATA', 'VERIFIED_FROM_PROVENANCE', 'MANUAL_REVIEW_LEDGER'}
CANONICAL_MATURITY = {
    'FINAL_WITHIN_STEP12_EVIDENCE',
    'PROVISIONAL_PENDING_STEP13_CONFLICT_CHECK',
    'DEFERRED_PENDING_MISSING_EVIDENCE',
}
TARGET_REQUIRED_ACTIONS = {
    'KEEP_EXISTING_STRUCTURE',
    'EXPAND_EXISTING_PAGE',
    'ADD_SECTION_OR_FAQ_TO_EXISTING',
    'ROUTE_TO_EXISTING_PAGE_AS_SUBTASK',
    'NEW_COMMERCIAL_PAGE',
    'NEW_INFORMATIONAL_PAGE',
    'INCLUDE_AS_SECTION_IN_PROPOSED_PAGE',
}


def read(path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def b(v):
    return str(v).strip().lower() == 'true'


def norm_page(v):
    v = (v or '').strip()
    if not v:
        return ''
    if v.startswith('PROPOSED_NEW:'):
        return 'https://okno-msk.ru' + v.split(':', 1)[1]
    return v


def split_multi(v):
    return [x.strip() for x in (v or '').split('||') if x.strip()]


def actual_text(v):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (dict, list, tuple, set)):
        return json.dumps(v if not isinstance(v, set) else sorted(v), ensure_ascii=False, sort_keys=True)
    return str(v)


s11 = read(S11)
assign = read(ASSIGN)
units = read(UNITS)
actions_v1 = read(ACTIONS_V1)
actions = read(ACTIONS)
final_map = read(FINAL_MAP)
new_evidence = read(NEW_EVIDENCE)
hierarchy = read(HIERARCHY)
pairs = read(PAIRS)
review = read(REVIEW)
sm_cases = read(SM_CASES)
state = json.loads(STATE.read_text(encoding='utf-8'))

action_v1_by = {r['structural_unit_id']: r for r in actions_v1}
action_by = {r['structural_unit_id']: r for r in actions}
unit_by = {r['structural_unit_id']: r for r in units}
assign_by_phrase = {r['phrase']: r for r in assign}
map_by_phrase = {r['phrase']: r for r in final_map}
member_counts = Counter(r['final_structural_unit_id'] for r in assign if r['final_structural_unit_id'])
search_required = [r for r in assign if not r['final_structural_unit_id']]
assigned = [r for r in assign if r['final_structural_unit_id']]

hierarchy_pages = {norm_page(r['proposed_url']) for r in hierarchy}
new_pages = {norm_page(r['proposed_page']) for r in new_evidence}
new_action_rows = [r for r in actions if r['structural_action'] in {'NEW_COMMERCIAL_PAGE', 'NEW_INFORMATIONAL_PAGE'}]
new_action_pages = {norm_page(r['primary_page_candidate']) for r in new_action_rows}

pair_ids = {r['pair_id'] for r in pairs}
all_referenced_pair_ids = set()
for r in actions:
    all_referenced_pair_ids.update(x for x in r['step13_candidate_pair_ids'].split(';') if x)

findings = []

def finding(kind, subject, observed, expected, source, note):
    findings.append({
        'finding_id': f'F{len(findings)+1:03d}',
        'finding_type': kind,
        'subject': subject,
        'observed': actual_text(observed),
        'expected': actual_text(expected),
        'source_artifacts': source,
        'note': note,
    })

# Specific row-level diagnostic findings.
missing_target_rows = [r for r in actions if r['structural_action'] in TARGET_REQUIRED_ACTIONS and not r['primary_page_candidate']]
for r in missing_target_rows:
    finding(
        'ACTION_REQUIRES_PRIMARY_TARGET_BUT_BLANK', r['structural_unit_id'], r['structural_action'],
        'non-empty primary_page_candidate', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv',
        'An implementation action that keeps/expands/adds/routes/creates content must identify the primary structural destination.'
    )

stale_hierarchy_reason_rows = [
    r for r in actions
    if r['hierarchy_clarity'].startswith('MATERIALIZED_')
    and 'hierarchy is not yet finalized' in r['confidence_downgrade_reason'].lower()
]
for r in stale_hierarchy_reason_rows:
    finding(
        'STALE_HIERARCHY_DOWNGRADE_REASON', r['structural_unit_id'], r['confidence_downgrade_reason'],
        'reason consistent with materialized hierarchy; remaining Search/business/Step13 dependency stated instead',
        'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv | STEP_12_NEW_PAGE_HIERARCHY_PLAN.tsv',
        'The hierarchy itself is materialized; unresolved downstream evidence may remain, but the reason must not claim the hierarchy is still absent.'
    )

# QA checks: every row records exact origin and computation.
checks = []

def add_check(cid, category, actual, expected, passed, origin, sources, method):
    checks.append({
        'check_id': cid,
        'category': category,
        'actual': actual_text(actual),
        'expected': actual_text(expected),
        'pass': 'true' if passed else 'false',
        'evidence_origin': origin,
        'source_artifacts': sources,
        'computation_or_review_method': method,
    })

# Accounting / phrase-level integrity.
add_check('Q001', 'ACCOUNTING', len(s11), 2332, len(s11) == 2332, 'COMPUTED_FROM_DATA', 'STEP_11_PHRASE_PAGE_MAP.tsv', 'Count parsed data rows.')
add_check('Q002', 'ACCOUNTING', len(assign), 2332, len(assign) == 2332, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv', 'Count parsed data rows.')
add_check('Q003', 'ACCOUNTING', len(final_map), 2332, len(final_map) == 2332, 'COMPUTED_FROM_DATA', 'STEP_12_PHRASE_ACTION_MAP_FINAL.tsv', 'Count parsed data rows.')
phrase_input_mismatch = Counter(r['phrase'] for r in s11) != Counter(r['phrase'] for r in assign)
add_check('Q004', 'ACCOUNTING', int(phrase_input_mismatch), 0, not phrase_input_mismatch, 'COMPUTED_FROM_DATA', 'STEP_11_PHRASE_PAGE_MAP.tsv | STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv', 'Compare complete phrase multisets, not row-count only.')
phrase_map_mismatch = Counter(r['phrase'] for r in assign) != Counter(r['phrase'] for r in final_map)
add_check('Q005', 'ACCOUNTING', int(phrase_map_mismatch), 0, not phrase_map_mismatch, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv | STEP_12_PHRASE_ACTION_MAP_FINAL.tsv', 'Compare complete phrase multisets.')
add_check('Q006', 'ACCOUNTING', len(assigned), 2313, len(assigned) == 2313, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv', 'Count rows with non-empty final_structural_unit_id.')
add_check('Q007', 'ACCOUNTING', len(search_required), 19, len(search_required) == 19, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv', 'Count rows with blank final_structural_unit_id.')

# Structural unit / action completeness.
unit_ids = [r['structural_unit_id'] for r in units]
action_ids = [r['structural_unit_id'] for r in actions]
add_check('Q008', 'STRUCTURAL_UNITS', len(units), 160, len(units) == 160, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_UNITS_V5.tsv', 'Count parsed structural units.')
add_check('Q009', 'STRUCTURAL_UNITS', len(actions), 160, len(actions) == 160, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv', 'Count parsed final action rows.')
add_check('Q010', 'STRUCTURAL_UNITS', sum(v > 1 for v in Counter(action_ids).values()), 0, len(action_ids) == len(set(action_ids)), 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv', 'Count duplicate structural_unit_id values.')
unit_action_set_mismatch = set(unit_ids) ^ set(action_ids)
add_check('Q011', 'STRUCTURAL_UNITS', len(unit_action_set_mismatch), 0, not unit_action_set_mismatch, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_UNITS_V5.tsv | STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv', 'Symmetric difference of structural-unit ID sets.')
missing_action_assignments = [r for r in assigned if r['final_structural_unit_id'] not in action_by]
add_check('Q012', 'STRUCTURAL_UNITS', len(missing_action_assignments), 0, not missing_action_assignments, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv | STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv', 'Join every assigned phrase to final action by structural_unit_id.')
phrase_count_mismatch_units = [uid for uid, r in action_by.items() if int(r['phrase_count']) != member_counts.get(uid, 0)]
add_check('Q013', 'STRUCTURAL_UNITS', len(phrase_count_mismatch_units), 0, not phrase_count_mismatch_units, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv | STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv', 'Recompute phrase_count from assignments for each action row.')

# Final phrase map integrity.
assigned_map_bad = 0
for r in assigned:
    m = map_by_phrase.get(r['phrase'])
    a = action_by[r['final_structural_unit_id']]
    if not m or m['final_structural_unit_id'] != r['final_structural_unit_id'] or m['structural_action'] != a['structural_action'] or m['primary_page_candidate'] != a['primary_page_candidate'] or m['recommendation_maturity'] != a['recommendation_maturity']:
        assigned_map_bad += 1
add_check('Q014', 'PHRASE_ACTION_MAP', assigned_map_bad, 0, assigned_map_bad == 0, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv | STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv | STEP_12_PHRASE_ACTION_MAP_FINAL.tsv', 'Independently rejoin each assigned phrase and compare material action fields.')
search_map_bad = 0
for r in search_required:
    m = map_by_phrase.get(r['phrase'])
    if not m or m['final_structural_unit_id'] or m['structural_action'] != 'DEFER_UNRESOLVED' or m['primary_page_candidate'] or m['step13_dependency_required'] != 'false':
        search_map_bad += 1
add_check('Q015', 'PHRASE_ACTION_MAP', search_map_bad, 0, search_map_bad == 0, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv | STEP_12_PHRASE_ACTION_MAP_FINAL.tsv', 'Search-required rows must remain unresolved with no target or Step13 action.')

# Evidence-derived confidence / maturity integrity.
required_dims = ['task_coherence','business_truth','current_page_fit','demand_support','search_boundary_support','hierarchy_clarity','recommendation_maturity','final_confidence','confidence_origin','maturity_origin']
missing_dims = [r['structural_unit_id'] for r in actions if any(not r[k] for k in required_dims)]
add_check('Q016', 'EVIDENCE_DIMENSIONS', len(missing_dims), 0, not missing_dims, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv', 'Count rows with blank required evidence/maturity fields.')
review_action_required = [r for r in actions if r['structural_action'] == 'REVIEW_ACTION_REQUIRED']
add_check('Q017', 'ACTION_COMPLETENESS', len(review_action_required), 0, not review_action_required, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv', 'Count unresolved placeholder actions.')
noncanonical_maturity = [r for r in actions if r['recommendation_maturity'] not in CANONICAL_MATURITY]
add_check('Q018', 'MATURITY', len(noncanonical_maturity), 0, not noncanonical_maturity, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv', 'Validate maturity against the three approved Step-12 states.')
dep_high = [r for r in actions if b(r['step13_dependency_required']) and r['final_confidence'] == 'HIGH']
add_check('Q019', 'MATURITY', len(dep_high), 0, not dep_high, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv', 'Count Step13-dependent rows still marked HIGH.')
dep_final = [r for r in actions if b(r['step13_dependency_required']) and r['recommendation_maturity'] == 'FINAL_WITHIN_STEP12_EVIDENCE']
add_check('Q020', 'MATURITY', len(dep_final), 0, not dep_final, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv', 'Count Step13-dependent rows still marked final.')
dep_without_pairs = [r for r in actions if b(r['step13_dependency_required']) and not r['step13_candidate_pair_ids']]
add_check('Q021', 'MATURITY', len(dep_without_pairs), 0, not dep_without_pairs, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv', 'Every Step13 dependency must expose pair IDs that caused it.')
unknown_pair_refs = sorted(all_referenced_pair_ids - pair_ids)
add_check('Q022', 'PAIR_GRAPH', len(unknown_pair_refs), 0, not unknown_pair_refs, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv | STEP_12_STEP13_CANDIDATE_PAIRS.tsv', 'Compare every referenced pair ID to persisted pair ledger IDs.')

# Target/hierarchy implementation readiness.
add_check('Q023', 'ACTION_TARGETS', len(missing_target_rows), 0, not missing_target_rows, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv', 'Actions that implement on a page must identify primary_page_candidate.')
invalid_new_primary = [r for r in new_action_rows if not r['primary_page_candidate'].startswith('PROPOSED_NEW:') or norm_page(r['primary_page_candidate']) not in new_pages]
add_check('Q024', 'NEW_PAGES', len(invalid_new_primary), 0, not invalid_new_primary, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv | STEP_12_NEW_PAGE_EVIDENCE_V2.tsv', 'NEW_* actions must use canonical proposed-page targets from evidence table.')
add_check('Q025', 'NEW_PAGES', len(new_action_pages), 5, len(new_action_pages) == 5, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv', 'Count unique proposed pages behind NEW_* action rows; multiple units may share a page.')
hierarchy_missing_owner = hierarchy_pages - {norm_page(r['primary_page_candidate']) for r in actions}
add_check('Q026', 'HIERARCHY', len(hierarchy_missing_owner), 0, not hierarchy_missing_owner and len(hierarchy_pages) == 5, 'COMPUTED_FROM_DATA', 'STEP_12_NEW_PAGE_HIERARCHY_PLAN.tsv | STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv', 'Compare unique hierarchy candidate pages to normalized action primary targets.')
add_check('Q027', 'HIERARCHY', len(stale_hierarchy_reason_rows), 0, not stale_hierarchy_reason_rows, 'COMPUTED_FROM_DATA', 'STEP_12_NEW_PAGE_HIERARCHY_PLAN.tsv | STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv', 'Materialized hierarchy must not retain a downgrade reason claiming hierarchy is not yet finalized.')

# Confidence contradictions.
high_with_material_gap = [r for r in actions if r['final_confidence'] == 'HIGH' and (r['search_boundary_support'] == 'MATERIAL_BOUNDARY_GAP' or r['business_truth'].startswith('CONDITIONAL') or r['recommendation_maturity'] != 'FINAL_WITHIN_STEP12_EVIDENCE')]
add_check('Q028', 'CONFIDENCE', len(high_with_material_gap), 0, not high_with_material_gap, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv', 'HIGH cannot coexist with a material Search/business/maturity gap.')
deferred_not_low = [r for r in actions if r['recommendation_maturity'] == 'DEFERRED_PENDING_MISSING_EVIDENCE' and r['final_confidence'] != 'LOW']
add_check('Q029', 'CONFIDENCE', len(deferred_not_low), 0, not deferred_not_low, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv', 'Deferred recommendations must not carry MEDIUM/HIGH confidence.')

# Pair graph is a candidate universe only. Recompute the expected pair-key
# universe independently from V1 routing inputs instead of asserting a historical count.
source_uids = defaultdict(set)
for r in assign:
    uid = r['final_structural_unit_id']
    src = r['original_effective_cluster_id']
    if uid and src:
        source_uids[src].add(uid)

expected_pair_keys = set()
for uid, r in action_v1_by.items():
    a = norm_page(r['primary_page_candidate'])
    bpage = norm_page(r['supporting_page'])
    if a and bpage and a != bpage:
        expected_pair_keys.add(tuple(sorted((a, bpage))))
for src, uids in source_uids.items():
    pages = sorted({norm_page(action_v1_by[uid]['primary_page_candidate']) for uid in uids if uid in action_v1_by and norm_page(action_v1_by[uid]['primary_page_candidate'])})
    expected_pair_keys.update(tuple(sorted(pair)) for pair in combinations(pages, 2))
for h in hierarchy:
    candidate = norm_page(h['proposed_url'])
    for raw in split_multi(h.get('mandatory_inbound_links')) + split_multi(h.get('mandatory_outbound_links')):
        other = norm_page(raw)
        if candidate and other and candidate != other:
            expected_pair_keys.add(tuple(sorted((candidate, other))))

actual_pair_keys = [tuple(sorted((norm_page(r['page_a']), norm_page(r['page_b'])))) for r in pairs]
actual_pair_key_set = set(actual_pair_keys)
missing_expected_pairs = sorted(expected_pair_keys - actual_pair_key_set)
extra_actual_pairs = sorted(actual_pair_key_set - expected_pair_keys)
pair_id_dups = sum(v > 1 for v in Counter(r['pair_id'] for r in pairs).values())
add_check('Q030', 'PAIR_GRAPH', len(pairs), len(expected_pair_keys), len(pairs) == len(expected_pair_keys), 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V1.tsv | STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv | STEP_12_NEW_PAGE_HIERARCHY_PLAN.tsv | STEP_12_STEP13_CANDIDATE_PAIRS.tsv', 'Independently recompute expected pair-key count from V1 primary/supporting edges, shared-source multi-primary routes, and hierarchy edges.')
add_check('Q030M', 'PAIR_GRAPH', len(missing_expected_pairs), 0, not missing_expected_pairs, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V1.tsv | STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv | STEP_12_NEW_PAGE_HIERARCHY_PLAN.tsv | STEP_12_STEP13_CANDIDATE_PAIRS.tsv', 'Set-difference expected pair keys minus persisted pair keys.')
add_check('Q030E', 'PAIR_GRAPH', len(extra_actual_pairs), 0, not extra_actual_pairs, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V1.tsv | STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv | STEP_12_NEW_PAGE_HIERARCHY_PLAN.tsv | STEP_12_STEP13_CANDIDATE_PAIRS.tsv', 'Set-difference persisted pair keys minus independently recomputed expected pair keys.')
add_check('Q031', 'PAIR_GRAPH', pair_id_dups, 0, pair_id_dups == 0, 'COMPUTED_FROM_DATA', 'STEP_12_STEP13_CANDIDATE_PAIRS.tsv', 'Count duplicate pair IDs.')
self_pairs = [r for r in pairs if norm_page(r['page_a']) == norm_page(r['page_b'])]
add_check('Q032', 'PAIR_GRAPH', len(self_pairs), 0, not self_pairs, 'COMPUTED_FROM_DATA', 'STEP_12_STEP13_CANDIDATE_PAIRS.tsv', 'Count self-pairs after URL normalization.')
forbidden_pair_columns = [c for c in (pairs[0].keys() if pairs else []) if 'cannibalization_verdict' in c.lower() or 'harmful_overlap_verdict' in c.lower()]
add_check('Q033', 'STEP_BOUNDARY', len(forbidden_pair_columns), 0, not forbidden_pair_columns, 'COMPUTED_FROM_DATA', 'STEP_12_STEP13_CANDIDATE_PAIRS.tsv', 'Inspect pair-ledger schema for forbidden Step13 verdict columns.')
harm_tokens = ('HARMFUL_CANNIBALIZATION', 'CANNIBALIZES', 'PROVEN_CANNIBALIZATION')
harm_cells = sum(any(tok in (v or '').upper() for tok in harm_tokens) for r in pairs for v in r.values())
add_check('Q034', 'STEP_BOUNDARY', harm_cells, 0, harm_cells == 0, 'COMPUTED_FROM_DATA', 'STEP_12_STEP13_CANDIDATE_PAIRS.tsv', 'Scan all pair-ledger cells for self-declared harmful-cannibalization verdicts.')
step13_files = sorted(p.name for p in ROOT.iterdir() if p.is_file() and p.name.startswith('STEP_13_'))
add_check('Q035', 'STEP_BOUNDARY', len(step13_files), 0, not step13_files, 'VERIFIED_FROM_PROVENANCE', 'GitHub job workspace file inventory', 'Enumerate current-job files whose names start with STEP_13_.')
add_check('Q036', 'STEP_BOUNDARY', state.get('step13_blocked'), True, state.get('step13_blocked') is True, 'VERIFIED_FROM_PROVENANCE', 'STEP_12_CORRECTION_CURRENT_STATE.json', 'Parse structured JSON field, not grep text count.')

# Manual review ledger evaluation.
metrics = {
    'SEARCH_REQUIRED_ROWS': len(search_required),
    'HIERARCHY_CANDIDATE_PAGES': len(hierarchy_pages),
}
review_results = []
for r in review:
    observed = []
    ok = True
    if r['subject_id']:
        a = action_by.get(r['subject_id'])
        if not a:
            ok = False
            observed.append('subject_missing')
        else:
            comparisons = [
                ('structural_action', r['expected_action']),
                ('primary_page_candidate', r['expected_primary']),
                ('supporting_page', r['expected_supporting']),
                ('recommendation_maturity', r['expected_maturity']),
                ('final_confidence', r['expected_confidence']),
            ]
            for key, exp in comparisons:
                if exp:
                    observed.append(f'{key}={a[key]}')
                    ok = ok and a[key] == exp
            if r['require_blank_primary'].lower() == 'true':
                observed.append(f'primary_blank={str(not bool(a["primary_page_candidate"])).lower()}')
                ok = ok and not a['primary_page_candidate']
            if r['expected_step13_dependency']:
                observed.append(f'step13_dependency={a["step13_dependency_required"]}')
                ok = ok and a['step13_dependency_required'] == r['expected_step13_dependency']
    if r['phrase']:
        a = assign_by_phrase.get(r['phrase'])
        if not a:
            ok = False
            observed.append('phrase_missing')
        elif r['expected_phrase_unit']:
            observed.append(f'phrase_unit={a["final_structural_unit_id"]}')
            ok = ok and a['final_structural_unit_id'] == r['expected_phrase_unit']
    if r['expected_metric']:
        val = metrics.get(r['expected_metric'])
        observed.append(f'{r["expected_metric"]}={val}')
        ok = ok and val is not None and str(val) == r['expected_metric_value']
    review_results.append({
        'case_id': r['case_id'],
        'case_class': r['case_class'],
        'pass': 'true' if ok else 'false',
        'observed': '; '.join(observed),
        'expected_summary': '; '.join(x for x in [r['expected_action'], r['expected_primary'], r['expected_maturity'], r['expected_confidence'], r['expected_phrase_unit'], (r['expected_metric'] + '=' + r['expected_metric_value']) if r['expected_metric'] else ''] if x),
        'evidence_origin': r['evidence_origin'],
        'source_artifacts': r['source_artifacts'],
        'review_rationale': r['rationale'],
    })
    if not ok:
        finding('MANUAL_REVIEW_CASE_FAILED', r['case_id'], '; '.join(observed), 'review-led expected state', r['source_artifacts'], r['rationale'])
review_failures = [r for r in review_results if r['pass'] != 'true']
add_check('Q037', 'MANUAL_REVIEW', len(review_results), 10, len(review_results) == 10, 'MANUAL_REVIEW_LEDGER', 'STEP_12_QA_REVIEW_LEDGER.tsv', 'Count explicit review cases.')
add_check('Q038', 'MANUAL_REVIEW', len(review_failures), 0, not review_failures, 'MANUAL_REVIEW_LEDGER', 'STEP_12_QA_REVIEW_LEDGER.tsv + cited source artifacts per row', 'Evaluate every explicit review row against current persisted data.')

# SPLIT/MERGE evaluator and four regression controls.
def split_merge_supported(r):
    if r['action_type'] == 'SPLIT_EXISTING_PAGE':
        return b(r['major_logical_task_boundary']) and b(r['distinct_terminal_task']) and b(r['distinct_page_role_or_search_boundary']) and not b(r['modifier_only']) and bool(r['support_evidence'].strip())
    if r['action_type'] == 'MERGE_STRUCTURALLY_REDUNDANT_PAGES':
        return b(r['same_terminal_task']) and b(r['same_page_role']) and b(r['redundancy_evidence']) and not b(r['merge_reason_only_suspected_cannibalization']) and bool(r['support_evidence'].strip())
    return False

sm_results = []
for r in sm_cases:
    supported = split_merge_supported(r)
    expected = b(r['expected_supported'])
    sm_results.append({
        'case_id': r['case_id'],
        'action_type': r['action_type'],
        'computed_supported': 'true' if supported else 'false',
        'expected_supported': 'true' if expected else 'false',
        'pass': 'true' if supported == expected else 'false',
        'support_evidence': r['support_evidence'],
        'case_purpose': r['case_purpose'],
        'evidence_origin': 'COMPUTED_FROM_DATA',
    })
sm_failures = [r for r in sm_results if r['pass'] != 'true']
add_check('Q039', 'SPLIT_MERGE_REGRESSION', len(sm_results), 4, len(sm_results) == 4, 'COMPUTED_FROM_DATA', 'STEP_12_SPLIT_MERGE_REGRESSION_CASES.tsv', 'Count explicit positive/negative control cases.')
add_check('Q040', 'SPLIT_MERGE_REGRESSION', len(sm_failures), 0, not sm_failures, 'COMPUTED_FROM_DATA', 'STEP_12_SPLIT_MERGE_REGRESSION_CASES.tsv', 'Evaluate SPLIT/MERGE evidence rules; compare computed support to expected control result.')
actual_split_merge = [r for r in actions if r['structural_action'] in {'SPLIT_EXISTING_PAGE', 'MERGE_STRUCTURALLY_REDUNDANT_PAGES'}]
reviewed_actual_sm = {r['subject_id'] for r in review if r['case_class'] == 'ACTUAL_SPLIT_MERGE_ACTION' and r['subject_id']}
unreviewed_actual_sm = [r['structural_unit_id'] for r in actual_split_merge if r['structural_unit_id'] not in reviewed_actual_sm]
add_check('Q041', 'SPLIT_MERGE_ACTUAL', len(unreviewed_actual_sm), 0, not unreviewed_actual_sm, 'MANUAL_REVIEW_LEDGER', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv | STEP_12_QA_REVIEW_LEDGER.tsv', 'Any actual SPLIT/MERGE must have an explicit support-evidence review row; zero actual actions is valid.')
unsupported_split = [r for r in actual_split_merge if r['structural_action'] == 'SPLIT_EXISTING_PAGE' and r['structural_unit_id'] in unreviewed_actual_sm]
unsupported_merge = [r for r in actual_split_merge if r['structural_action'] == 'MERGE_STRUCTURALLY_REDUNDANT_PAGES' and r['structural_unit_id'] in unreviewed_actual_sm]
add_check('Q042', 'SPLIT_MERGE_ACTUAL', len(unsupported_split), 0, not unsupported_split, 'MANUAL_REVIEW_LEDGER', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv | STEP_12_QA_REVIEW_LEDGER.tsv', 'Count only unsupported/unreviewed SPLIT actions, never all SPLIT actions.')
add_check('Q043', 'SPLIT_MERGE_ACTUAL', len(unsupported_merge), 0, not unsupported_merge, 'MANUAL_REVIEW_LEDGER', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv | STEP_12_QA_REVIEW_LEDGER.tsv', 'Count only unsupported/unreviewed MERGE actions, never all MERGE actions.')

# D12-05 self-certification audit of the QA itself.
self_asserted = [r for r in checks if r['evidence_origin'] not in ALLOWED_ORIGINS or not r['source_artifacts'].strip() or not r['computation_or_review_method'].strip() or 'ASSUMED' in r['computation_or_review_method'].upper()]
add_check('Q044', 'QA_META', len(self_asserted), 0, not self_asserted, 'COMPUTED_FROM_DATA', 'STEP_12_QA_CHECKS.tsv construction rules', 'Count checks without an allowed origin, source artifact, explicit method, or using ASSUMED language.')

# Write explicit evidence ledgers before deriving status.
def write(path, rows, fields):
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)

write(OUT_REVIEW, review_results, ['case_id','case_class','pass','observed','expected_summary','evidence_origin','source_artifacts','review_rationale'])
write(OUT_SM, sm_results, ['case_id','action_type','computed_supported','expected_supported','pass','support_evidence','case_purpose','evidence_origin'])
write(OUT_FINDINGS, findings, ['finding_id','finding_type','subject','observed','expected','source_artifacts','note'])
write(OUT_CHECKS, checks, ['check_id','category','actual','expected','pass','evidence_origin','source_artifacts','computation_or_review_method'])

failed = [r['check_id'] for r in checks if r['pass'] != 'true']
status = 'D12_05_CANDIDATE_PASS' if not failed else 'D12_05_DIAGNOSTIC_FAIL'
summary = {
    'date': '2026-08-31',
    'status': status,
    'independent_verifier': 'step12_independent_final_qa.py',
    'verification_principle': 'Recompute from persisted source artifacts; do not trust builder/generator QA fields as proof.',
    'checks_total': len(checks),
    'checks_failed': len(failed),
    'failed_check_ids': failed,
    'findings_rows': len(findings),
    'source_phrase_rows': len(s11),
    'assignment_rows': len(assign),
    'final_phrase_action_rows': len(final_map),
    'assigned_rows': len(assigned),
    'search_required_rows': len(search_required),
    'structural_units': len(units),
    'structural_action_rows': len(actions),
    'candidate_pair_rows': len(pairs),
    'new_page_unique_action_targets': len(new_action_pages),
    'hierarchy_candidate_pages': len(hierarchy_pages),
    'manual_review_cases': len(review_results),
    'manual_review_failures': len(review_failures),
    'split_merge_regression_cases': len(sm_results),
    'split_merge_regression_failures': len(sm_failures),
    'actual_split_rows': sum(r['structural_action'] == 'SPLIT_EXISTING_PAGE' for r in actions),
    'actual_merge_rows': sum(r['structural_action'] == 'MERGE_STRUCTURALLY_REDUNDANT_PAGES' for r in actions),
    'unsupported_split_rows': len(unsupported_split),
    'unsupported_merge_rows': len(unsupported_merge),
    'qa_self_asserted_pass_fields': len(self_asserted),
    'actions_requiring_target_but_blank': len(missing_target_rows),
    'stale_materialized_hierarchy_reason_rows': len(stale_hierarchy_reason_rows),
    'step13_artifact_files': step13_files,
    'step13_executed': False,
    'step12_complete': False,
    'next_step_allowed': False,
    'note': 'Even a candidate PASS does not close Step 12 until D12-05 acceptance updates canonical QA/report/state and GitHub readback passes.'
}
OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))
