import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
QA = ROOT / 'STEP_12_QA.json'
STATE = ROOT / 'STEP_12_CORRECTION_CURRENT_STATE.json'
FLOW = ROOT / 'JOB_FLOW.md'
MANIFEST = ROOT / 'JOB_MANIFEST.md'
REPORT = ROOT / 'STEP_12_REPORT.md'
ACCEPTANCE = ROOT / 'STEP_12_FINAL_ACCEPTANCE_2026-08-31.md'


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


qa = read_json(QA)
state = read_json(STATE)
flow = FLOW.read_text(encoding='utf-8')
manifest = MANIFEST.read_text(encoding='utf-8')
report = REPORT.read_text(encoding='utf-8')
acceptance = ACCEPTANCE.read_text(encoding='utf-8')

# Only run after the canonical closure has itself passed and been read back once.
assert qa['status'] == 'PASS_AFTER_EXTERNAL_METHOD_AUDIT_FAIL_CLOSED_CORRECTIONS_AND_INDEPENDENT_QA'
assert qa['step12_complete'] is True
assert qa['checks_total'] == 46 and qa['checks_failed'] == 0
assert qa['all_defects_verified_fixed'] is True
assert state['status'] == 'STEP12_COMPLETE_AFTER_EXTERNAL_METHOD_AUDIT_FAIL_CLOSED_CORRECTION_AND_INDEPENDENT_QA'
assert state['open_defects'] == []
assert state['step13_executed'] is False
assert 'KW001_OKNO_MSK_STEP12_FINAL_GITHUB_READBACK = pending_final_closure_readback' in flow
assert 'current_major_step = STEP_12_COMPLETE_AFTER_EXTERNAL_METHOD_AUDIT_AND_INDEPENDENT_QA' in manifest
assert 'next_major_step = STEP_13_PRE_STEP_METHODOLOGY_RESEARCH_AND_REVIEW' in manifest
assert 'Step 12 — structural actions\nStep 13 — cannibalization diagnosis' in manifest
assert 'Step 12 is complete. Step 13 has not been started.' in report
assert 'ALL_TRACKED_DEFECTS_VERIFIED_FIXED = 15/15' in acceptance

qa['final_github_readback'] = True
qa['canonical_closure_readback_passed'] = True
QA.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

state['final_github_readback'] = True
state['canonical_closure_readback_passed'] = True
STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Keep all Step10/11/12 markers in one valid fenced block and resolve pending marker.
flow = flow.replace(
    'KW001_OKNO_MSK_NEXT_STEP_ALLOWED = true\n```\n\nKW001_OKNO_MSK_STEP12_COMPLETE = true',
    'KW001_OKNO_MSK_NEXT_STEP_ALLOWED = true\nKW001_OKNO_MSK_STEP12_COMPLETE = true',
    1,
)
flow = flow.replace(
    'KW001_OKNO_MSK_STEP12_FINAL_GITHUB_READBACK = pending_final_closure_readback',
    'KW001_OKNO_MSK_STEP12_FINAL_GITHUB_READBACK = true',
    1,
)
if not flow.rstrip().endswith('```'):
    flow = flow.rstrip() + '\n```\n'
FLOW.write_text(flow, encoding='utf-8')

manifest = manifest.replace(
    'STEP_12_COMPLETE = true\nSTEP_13_STATUS = NOT_STARTED_NEXT_ALLOWED',
    'STEP_12_COMPLETE = true\nSTEP_12_FINAL_GITHUB_READBACK = true\nSTEP_13_STATUS = NOT_STARTED_NEXT_ALLOWED',
    1,
)
manifest = manifest.replace(
    'Step 12 — structural actions\nStep 13 — cannibalization diagnosis',
    'Step 13 — cannibalization diagnosis',
    1,
)
MANIFEST.write_text(manifest, encoding='utf-8')

if 'FINAL_CANONICAL_GITHUB_READBACK = true' not in acceptance:
    acceptance = acceptance.replace(
        'STEP13_EXECUTED = false\n```',
        'STEP13_EXECUTED = false\nFINAL_CANONICAL_GITHUB_READBACK = true\n```',
        1,
    )
    acceptance += '\nThe canonical closure commit was read back from GitHub before this final durable-status synchronization. This synchronization itself must also pass a second structured GitHub readback before the job state is reported externally.\n'
ACCEPTANCE.write_text(acceptance, encoding='utf-8')

if '## Final durable closure readback' not in report:
    report += '''

## Final durable closure readback

The canonical Step-12 closure commit passed structured GitHub readback. The final status synchronization records that durable proof in the canonical QA/state/flow/manifest. A second structured readback of the synchronization commit is required before external reporting.

```text
FINAL_CANONICAL_GITHUB_READBACK = true
STEP13_EXECUTED = false
```
'''
REPORT.write_text(report, encoding='utf-8')

print(json.dumps({
    'status': 'STEP12_POST_READBACK_STATUS_READY',
    'final_github_readback': True,
    'remaining_roadmap_starts_with': 'Step 13',
    'step13_executed': False,
}, ensure_ascii=False, indent=2))
