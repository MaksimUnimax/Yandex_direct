import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
QA = ROOT / 'STEP_12_QA_CANDIDATE.json'
FINDINGS = ROOT / 'STEP_12_QA_FINDINGS.tsv'
LEDGER = ROOT / 'STEP_12_CORRECTION_DEFECT_LEDGER.tsv'
STATE = ROOT / 'STEP_12_CORRECTION_CURRENT_STATE.json'

qa = json.loads(QA.read_text(encoding='utf-8'))
assert qa['status'] == 'D12_05_DIAGNOSTIC_FAIL'
assert qa['failed_check_ids'] == ['Q023', 'Q027']
assert qa['actions_requiring_target_but_blank'] == 4
assert qa['stale_materialized_hierarchy_reason_rows'] == 10

with FINDINGS.open(encoding='utf-8', newline='') as f:
    findings = list(csv.DictReader(f, delimiter='\t'))
missing = [r for r in findings if r['finding_type'] == 'ACTION_REQUIRES_PRIMARY_TARGET_BUT_BLANK']
stale = [r for r in findings if r['finding_type'] == 'STALE_HIERARCHY_DOWNGRADE_REASON']
assert len(missing) == 4
assert len(stale) == 10
assert {r['subject'] for r in missing} == {
    'PVC_DOOR_INSTALLATION_SERVICE',
    'PVC_WINDOW_OPERATION_DIY',
    'REHAU_OTHER_BRAND_COMPARISON_INFO',
    'WINDOW_DEMOLITION_SERVICE',
}

with LEDGER.open(encoding='utf-8', newline='') as f:
    rows = list(csv.DictReader(f, delimiter='\t'))
fields = list(rows[0].keys())
ids = {r['defect_id'] for r in rows}
if 'D12-14' in ids or 'D12-15' in ids:
    raise RuntimeError('D12-14/D12-15 already registered; refuse duplicate append')

rows.append({
    'defect_id':'D12-14',
    'short_name':'IMPLEMENTABLE_ACTION_WITHOUT_PRIMARY_TARGET',
    'first_run_behavior':'Independent D12-05 QA found four final implementable actions with blank primary_page_candidate: PVC_DOOR_INSTALLATION_SERVICE, PVC_WINDOW_OPERATION_DIY, REHAU_OTHER_BRAND_COMPARISON_INFO and WINDOW_DEMOLITION_SERVICE.',
    'why_it_seemed_reasonable':'The action type could be inferred from the unit role/historical action mix and some rows had a supporting or conceptually adjacent page, so the missing primary destination was easy to overlook.',
    'why_it_is_insufficient_or_wrong':'An implementation instruction such as ADD_SECTION_OR_FAQ_TO_EXISTING or ROUTE_TO_EXISTING_PAGE_AS_SUBTASK is incomplete without the exact page that receives the change; a supporting page is not automatically the owner.',
    'root_cause':'Action derivation allowed implementable actions even when primary_page_candidate was blank; there was no final action-readiness invariant requiring a verified primary destination.',
    'corrective_action':'Re-evaluate all four units against exact phrases, Step-11 ownership and verified site/page evidence. If a truthful current primary page exists, record it; otherwise change the action to explicit defer/no-standalone rather than guessing a URL. Enforce IMPLEMENTABLE_PAGE_ACTION -> NON_EMPTY_VERIFIED_PRIMARY_TARGET.',
    'verification_required':'Independent QA actions_requiring_target_but_blank=0; all four cases have explicit reviewed resolutions; any selected target is evidence-backed; final phrase map rebuilt; GitHub readback passes.',
    'status':'OPEN',
    'correction_artifact':'STEP_12_D12_14_IMPLEMENTABLE_ACTION_WITHOUT_PRIMARY_TARGET_2026-08-31.md | STEP_12_QA_FINDINGS.tsv | STEP_12_QA_CANDIDATE.json',
    'notes':'Discovered by durable independent D12-05 workflow run 33366415931 after diagnostics were committed first. Do not auto-copy a supporting page into primary without page-fit review.'
})
rows.append({
    'defect_id':'D12-15',
    'short_name':'STALE_CONFIDENCE_REASON_AFTER_HIERARCHY_MATERIALIZATION',
    'first_run_behavior':'Independent D12-05 QA found ten rows with hierarchy_clarity=MATERIALIZED_* while confidence_downgrade_reason still claimed the new-page hierarchy was not yet finalized.',
    'why_it_seemed_reasonable':'V2 correctly overlaid materialized hierarchy and Step-13 dependency on V1 rows, while carrying forward the prior confidence text as a convenient explanation.',
    'why_it_is_insufficient_or_wrong':'The structured state and human-readable reason contradict each other; the remaining uncertainty is Search/business/Step13 dependency, not missing hierarchy.',
    'root_cause':'V2 updated hierarchy_clarity/recommendation_maturity but did not regenerate confidence_downgrade_reason from the current evidence dimensions.',
    'corrective_action':'Regenerate confidence_downgrade_reason after hierarchy and dependency overlays from current business_truth, search_boundary_support, hierarchy_clarity and recommendation_maturity. Resolved dimensions must disappear from downgrade reasons.',
    'verification_required':'Independent QA stale_materialized_hierarchy_reason_rows=0; all ten discovered rows corrected by regeneration; real Search/business/Step13 uncertainty remains; no confidence/maturity is strengthened merely by wording cleanup; GitHub readback passes.',
    'status':'OPEN',
    'correction_artifact':'STEP_12_D12_15_STALE_HIERARCHY_CONFIDENCE_REASON_2026-08-31.md | STEP_12_QA_FINDINGS.tsv | STEP_12_QA_CANDIDATE.json',
    'notes':'Discovered by durable independent D12-05 workflow run 33366415931. This is explanation consistency, not evidence resolution.'
})

with LEDGER.open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
    w.writeheader(); w.writerows(rows)

state = json.loads(STATE.read_text(encoding='utf-8'))
assert state['open_defects'] == ['D12-05']
state['open_defects'] = ['D12-14', 'D12-15', 'D12-05']
state['current_correction_item'] = 'D12-14'
order = state['correction_order']
assert 'D12-14' not in order and 'D12-15' not in order
idx = order.index('D12-05')
state['correction_order'] = order[:idx] + ['D12-14', 'D12-15'] + order[idx:]
state['next_action'] = 'D12-14: resolve four implementable actions with blank primary targets from evidence, then D12-15 regenerate stale hierarchy confidence reasons, then rerun the same durable independent D12-05 QA. Step13 remains blocked and unexecuted.'
STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

print(json.dumps({
    'status':'D12_14_15_REGISTRATION_READY',
    'open_defects':state['open_defects'],
    'missing_target_findings':len(missing),
    'stale_reason_findings':len(stale),
}, ensure_ascii=False))
