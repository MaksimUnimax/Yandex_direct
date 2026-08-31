import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent.parent


def read_json(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))


def read_tsv(name):
    with (ROOT / name).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


# Re-read canonical final output, not finalizer stdout.
qa = read_json('STEP_12_QA.json')
state = read_json('STEP_12_CORRECTION_CURRENT_STATE.json')
ledger = read_tsv('STEP_12_CORRECTION_DEFECT_LEDGER.tsv')
checks = read_tsv('STEP_12_QA_CHECKS.tsv')
findings = read_tsv('STEP_12_QA_FINDINGS.tsv')
final_map = read_tsv('STEP_12_PHRASE_ACTION_MAP_FINAL.tsv')
actions = read_tsv('STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv')
pairs = read_tsv('STEP_12_STEP13_CANDIDATE_PAIRS.tsv')
hierarchy = read_tsv('STEP_12_NEW_PAGE_HIERARCHY_PLAN.tsv')
review = read_tsv('STEP_12_QA_REVIEW_RESULTS.tsv')
sm = read_tsv('STEP_12_SPLIT_MERGE_REGRESSION_RESULTS.tsv')

assert qa['status'] == 'PASS_AFTER_EXTERNAL_METHOD_AUDIT_FAIL_CLOSED_CORRECTIONS_AND_INDEPENDENT_QA'
assert qa['step12_complete'] is True
assert qa['next_step_allowed'] is True
assert qa['next_step'] == 'STEP_13_PRE_STEP_METHODOLOGY_RESEARCH_AND_REVIEW'
assert qa['step13_status'] == 'NOT_STARTED_NEXT_ALLOWED'
assert qa['step13_executed'] is False
assert qa['step14_executed'] is False
assert qa['historical_first_pass_qa_superseded'] is True
assert qa['checks_total'] == 46
assert qa['checks_failed'] == 0
assert qa['findings_rows'] == 0
assert qa['source_phrase_rows'] == 2332
assert qa['final_phrase_action_rows'] == 2332 == len(final_map)
assert qa['assigned_rows'] == 2313
assert qa['search_required_rows'] == 19
assert qa['structural_units'] == 160
assert qa['structural_action_rows'] == 160 == len(actions)
assert qa['manual_review_cases'] == 10 == len(review)
assert qa['manual_review_failures'] == 0
assert qa['split_merge_regression_cases'] == 4 == len(sm)
assert qa['split_merge_regression_failures'] == 0
assert qa['unsupported_split_rows'] == 0
assert qa['unsupported_merge_rows'] == 0
assert qa['qa_self_asserted_pass_fields'] == 0
assert qa['actions_requiring_target_but_blank'] == 0
assert qa['stale_materialized_hierarchy_reason_rows'] == 0
assert qa['all_defects_verified_fixed'] is True
assert qa['defect_count'] == 15
assert qa['open_defects'] == []
assert qa['candidate_pair_rows_current_derived'] == len(pairs)
assert qa['new_page_unique_action_targets'] == 5
assert qa['hierarchy_candidate_pages'] == 5 == len(hierarchy)
assert qa['step13_dependency_units'] == sum(r['step13_dependency_required'] == 'true' for r in actions)
assert findings == []
assert len(checks) == 46 and all(r['pass'] == 'true' for r in checks)
assert all(r['evidence_origin'] in {'COMPUTED_FROM_DATA','VERIFIED_FROM_PROVENANCE','MANUAL_REVIEW_LEDGER'} for r in checks)

assert state['status'] == 'STEP12_COMPLETE_AFTER_EXTERNAL_METHOD_AUDIT_FAIL_CLOSED_CORRECTION_AND_INDEPENDENT_QA'
assert state['step12_complete'] is True
assert state['next_step_allowed'] is True
assert state['open_defects'] == []
assert state['verified_fixed_defects'] == [f'D12-{i:02d}' for i in range(1,16)]
assert state['current_correction_item'] is None
assert state['step13_blocked'] is False
assert state['step13_executed'] is False
assert state['step13_status'] == 'NOT_STARTED_NEXT_ALLOWED'
assert state['next_major_step'] == 'STEP_13_PRE_STEP_METHODOLOGY_RESEARCH_AND_REVIEW'

assert len(ledger) == 15
assert {r['defect_id'] for r in ledger} == {f'D12-{i:02d}' for i in range(1,16)}
assert all(r['status'] == 'VERIFIED_FIXED' for r in ledger)
for d in ('D12-05','D12-14','D12-15'):
    row = next(r for r in ledger if r['defect_id'] == d)
    assert row['correction_artifact']
    assert 'STEP_12_FINAL_ACCEPTANCE_2026-08-31.md' in row['correction_artifact']

report = (ROOT / 'STEP_12_REPORT.md').read_text(encoding='utf-8')
acceptance = (ROOT / 'STEP_12_FINAL_ACCEPTANCE_2026-08-31.md').read_text(encoding='utf-8')
method = (BASE / 'STEP_12_STRUCTURAL_ACTION_METHOD.md').read_text(encoding='utf-8')
rules = (BASE / 'STEP_RULES_INDEX.md').read_text(encoding='utf-8')
flow = (ROOT / 'JOB_FLOW.md').read_text(encoding='utf-8')
manifest = (ROOT / 'JOB_MANIFEST.md').read_text(encoding='utf-8')

assert 'PASS AFTER EXTERNAL METHOD AUDIT + FAIL-CLOSED CORRECTIONS + INDEPENDENT QA' in report
assert 'INDEPENDENT_QA_CHECKS = 46/46 PASS' in report
assert 'QA_SELF_ASSERTED_PASS_FIELDS = 0' in report
assert 'Step 13 is **NOT STARTED**' in report
assert 'Step 12 is complete. Step 13 has not been started.' in report
assert 'ALL_TRACKED_DEFECTS_VERIFIED_FIXED = 15/15' in acceptance
assert 'STEP13_EXECUTED = false' in acceptance

assert 'Status: **APPROVED / ACTIVE AFTER EXTERNAL METHOD AUDIT + FAIL-CLOSED CORRECTIONS + INDEPENDENT QA**' in method
assert 'KW001_STEP12_FINAL_ACCEPTANCE_PENDING_CORRECTION = false' in method
assert 'KW001_STEP12_METHOD_APPROVED_AFTER_INDEPENDENT_QA = true' in method
assert 'KW001_STEP12_DIAGNOSTICS_PERSIST_BEFORE_FINAL_GATE = true' in method
assert 'KW001_STEP12_DYNAMIC_PAIR_UNIVERSE_QA_REQUIRED = true' in method
assert 'KW001_STEP12_IMPLEMENTABLE_ACTION_REQUIRES_PRIMARY_TARGET = true' in method
assert 'KW001_STEP12_CONFIDENCE_REASON_MUST_MATCH_CURRENT_STATE = true' in method
assert '# 12. Post-audit defects discovered by fail-closed correction' in method

assert '| **Step 12** | **Structural actions (keep/expand/split/merge/create)** | **APPROVED / ACTIVE AFTER EXTERNAL METHOD AUDIT + FAIL-CLOSED CORRECTIONS + INDEPENDENT QA** |' in rules
assert '| Step 13 | Cannibalization diagnosis | **UNVALIDATED** |' in rules
assert 'KW001_STEP12_METHOD_APPROVED_AFTER_INDEPENDENT_QA = true' in rules

assert '## Completed step — Step 12 structural actions' in flow
assert 'Status: **✅ COMPLETE AFTER EXTERNAL METHOD AUDIT + FAIL-CLOSED CORRECTIONS + INDEPENDENT QA**' in flow
assert '| **12. Structural actions** | **Decide what to keep, strengthen, add, create or deliberately not create** | **✅ COMPLETE AFTER EXTERNAL METHOD AUDIT + INDEPENDENT QA** |' in flow
assert '| 13. Cannibalization diagnosis | Confirm real competing-page conflicts | ⬜ NOT STARTED / NEXT ALLOWED |' in flow
assert 'KW001_OKNO_MSK_STEP12_COMPLETE = true' in flow
assert 'KW001_OKNO_MSK_STEP12_ALL_DEFECTS_FIXED = true' in flow
assert 'KW001_OKNO_MSK_STEP13_STATUS = NOT_STARTED_NEXT_ALLOWED' in flow
assert 'KW001_OKNO_MSK_STEP13_EXECUTED = false' in flow
assert 'STEP12_OPEN_DEFECTS_CURRENT =' not in flow
assert 'STEP12_CORRECTED_ACCEPTANCE = pending' not in flow

assert 'current_major_step = STEP_12_COMPLETE_AFTER_EXTERNAL_METHOD_AUDIT_AND_INDEPENDENT_QA' in manifest
assert 'next_major_step = STEP_13_PRE_STEP_METHODOLOGY_RESEARCH_AND_REVIEW' in manifest
assert 'revision_rework_open = false' in manifest
assert 'STRUCTURAL_ACTIONS_COMPLETE = true' in manifest
assert 'STEP_12_COMPLETE = true' in manifest
assert 'STEP_13_STATUS = NOT_STARTED_NEXT_ALLOWED' in manifest
assert 'STEP_13_EXECUTED = false' in manifest
assert 'Step 12 has **not** started.' not in manifest

# No Step-13 execution artifact was created by closure.
step13_files = sorted(p.name for p in ROOT.iterdir() if p.is_file() and p.name.startswith('STEP_13_'))
assert step13_files == []

print(json.dumps({
    'status': 'STEP12_CANONICAL_CLOSURE_VERIFY_PASS',
    'defects_fixed': len(ledger),
    'checks': len(checks),
    'final_phrase_rows': len(final_map),
    'structural_actions': len(actions),
    'pair_rows_current_derived': len(pairs),
    'step13_files': step13_files,
    'step13_executed': False,
}, ensure_ascii=False, indent=2))
