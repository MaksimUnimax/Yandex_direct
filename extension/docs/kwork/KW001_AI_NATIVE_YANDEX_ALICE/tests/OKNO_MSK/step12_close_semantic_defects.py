import csv, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
LEDGER=ROOT/'STEP_12_CORRECTION_DEFECT_LEDGER.tsv'
STATE=ROOT/'STEP_12_CORRECTION_CURRENT_STATE.json'
QA=ROOT/'STEP_12_STRUCTURAL_UNIT_CORRECTION_QA_V4.json'
ACCEPT=ROOT/'STEP_12_SEMANTIC_CORRECTION_ACCEPTANCE_2026-08-31.md'
FLOW=ROOT/'JOB_FLOW.md'
MANIFEST=ROOT/'JOB_MANIFEST.md'

q=json.loads(QA.read_text(encoding='utf-8'))
assert q['status']=='CANDIDATE_V4_READY_FOR_MANUAL_SEMANTIC_ACCEPTANCE'
assert q['source_rows']==2332 and q['search_required_rows']==19
assert q['historical_override_rows']==191 and q['historical_override_rows_with_explicit_final_unit']==191
assert q['hidden_runtime_override_rules_in_v4_output']==0
assert q['unit_metadata_inconsistency_rows']==0
assert q['mandatory_mixed_original_units_still_final']==[]
accept=ACCEPT.read_text(encoding='utf-8')
for d in ['D12-01','D12-02','D12-08','D12-09','D12-12']:
    assert f'### {d} ' in accept and '**VERIFIED_FIXED' in accept[accept.index(f'### {d} '):]

with LEDGER.open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f,delimiter='\t'))
fields=list(rows[0].keys())
close={'D12-01','D12-02','D12-08','D12-09','D12-12'}
artifact='STEP_12_SEMANTIC_CORRECTION_ACCEPTANCE_2026-08-31.md | STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V4.tsv | STEP_12_STRUCTURAL_UNITS_V4.tsv | STEP_12_STRUCTURAL_UNIT_CORRECTIONS_V4.tsv | STEP_12_NO_PAGE_OUTSIDE_SALVAGE_REVIEW_V4.tsv | STEP_12_SEMANTIC_CORRECTION_REGRESSION_ACTUAL.tsv'
for r in rows:
    if r['defect_id'] in close:
        r['status']='VERIFIED_FIXED'
        r['correction_artifact']=artifact
        r['notes']=(r['notes']+' | ' if r['notes'] else '')+'Closed only after V4 persistence/readback plus separate semantic acceptance; this does not imply Step12 final completion.'
with LEDGER.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)

state=json.loads(STATE.read_text(encoding='utf-8'))
for d in sorted(close):
    if d in state['open_defects']: state['open_defects'].remove(d)
    if d not in state['verified_fixed_defects']: state['verified_fixed_defects'].append(d)
state['verified_fixed_defects']=sorted(state['verified_fixed_defects'])
state['current_correction_item']='D12-03'
state['next_action']='Build demand/Search evidence matrix for corrected standalone-page candidates using persisted evidence first; D12-03 and D12-10 remain open.'
STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

manifest=MANIFEST.read_text(encoding='utf-8')
manifest=manifest.replace('next_major_step = STEP_12_CORRECTION_EXECUTION_D12_01','next_major_step = STEP_12_CORRECTION_EXECUTION_D12_03',1)
for item in ['STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V4.tsv','STEP_12_STRUCTURAL_UNITS_V4.tsv','STEP_12_STRUCTURAL_UNIT_CORRECTIONS_V4.tsv','STEP_12_NO_PAGE_OUTSIDE_SALVAGE_REVIEW_V4.tsv','STEP_12_SEMANTIC_CORRECTION_ACCEPTANCE_2026-08-31.md']:
    if item not in manifest:
        marker='```\n\nWhere older Step-09 planning state'
        if marker not in manifest: raise RuntimeError('manifest authority anchor missing')
        manifest=manifest.replace(marker,item+'\n'+marker,1)
MANIFEST.write_text(manifest,encoding='utf-8')

flow=FLOW.read_text(encoding='utf-8')
flow=flow.replace('STEP12_OPEN_DEFECTS = D12-01,D12-02,D12-03,D12-04,D12-05,D12-06,D12-07,D12-08,D12-09,D12-10,D12-11','STEP12_OPEN_DEFECTS = D12-03,D12-04,D12-05,D12-06,D12-07,D12-10,D12-11',1)
# D12-12 may have been appended after original block was written; enforce current marker separately.
flow=flow.replace('STEP12_CURRENT_CORRECTION_ITEM = D12-01','STEP12_CURRENT_CORRECTION_ITEM = D12-03',1)
if 'STEP12_VERIFIED_FIXED_DEFECTS = D12-01,D12-02,D12-08,D12-09,D12-12' not in flow:
    marker='STEP12_CURRENT_CORRECTION_ITEM = D12-03\n'
    flow=flow.replace(marker,marker+'STEP12_VERIFIED_FIXED_DEFECTS = D12-01,D12-02,D12-08,D12-09,D12-12\n',1)
summary='''\n### Accepted correction block — semantic units / salvage\n\nThe semantic foundation correction has passed separate readback/acceptance for D12-01, D12-02, D12-08, D12-09 and D12-12 only. Accepted V4 keeps 2332/2332 phrases, 19 unresolved, materializes 191/191 old hidden overrides into explicit units, removes known mixed original units, and reviews all 481 historical NO_STANDALONE/OUTSIDE phrases. Step 12 remains incomplete because new-page evidence, confidence, hierarchy, Step-13 pair derivation and independent final QA are still open.\n'''
if '### Accepted correction block — semantic units / salvage' not in flow:
    marker='A defect is not closed because a new file exists. It is closed only after its corrective artifact is produced, its defect-specific verification passes, and GitHub readback confirms the saved result.\n'
    flow=flow.replace(marker,marker+summary,1)
FLOW.write_text(flow,encoding='utf-8')
