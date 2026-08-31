import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LEDGER=ROOT/'STEP_12_CORRECTION_DEFECT_LEDGER.tsv'; STATE=ROOT/'STEP_12_CORRECTION_CURRENT_STATE.json'; ACCEPT=ROOT/'STEP_12_NEW_PAGE_EVIDENCE_ACCEPTANCE_2026-08-31.md'; QV5=ROOT/'STEP_12_STRUCTURAL_UNIT_CORRECTION_QA_V5.json'; QE=ROOT/'STEP_12_NEW_PAGE_EVIDENCE_QA_V2.json'; MANIFEST=ROOT/'JOB_MANIFEST.md'; FLOW=ROOT/'JOB_FLOW.md'
accept=ACCEPT.read_text(encoding='utf-8')
for d in ['D12-02','D12-03','D12-10']:
    pos=accept.index(f'### {d} '); assert '**VERIFIED_FIXED' in accept[pos:]
q5=json.loads(QV5.read_text(encoding='utf-8')); qe=json.loads(QE.read_text(encoding='utf-8'))
assert q5['status']=='CANDIDATE_V5_READY_FOR_D12_02_REACCEPTANCE' and q5['residual_hardware_review_rows_corrected']==1
assert qe['status']=='CANDIDATE_V2_READY_FOR_MANUAL_EVIDENCE_ACCEPTANCE' and qe['phrase_counts_not_summed_as_total_unique_demand'] and qe['association_not_counted_as_direct_demand']
with LEDGER.open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f,delimiter='\t'))
fields=list(rows[0].keys());close={'D12-02','D12-03','D12-10'}
artifact='STEP_12_NEW_PAGE_EVIDENCE_ACCEPTANCE_2026-08-31.md | STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv | STEP_12_NEW_PAGE_EVIDENCE_V2.tsv | STEP_12_NEW_PAGE_DEMAND_PHRASE_EVIDENCE_V2.tsv'
for r in rows:
    if r['defect_id'] in close:
        r['status']='VERIFIED_FIXED';r['correction_artifact']=artifact;r['notes']=(r['notes']+' | ' if r['notes'] else '')+'Closed/reclosed only after V5/V2 persisted readback and separate evidence acceptance; candidate page approval remains governed by later confidence/maturity.'
with LEDGER.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
state=json.loads(STATE.read_text(encoding='utf-8'))
for d in close:
    if d in state['open_defects']:state['open_defects'].remove(d)
    if d not in state['verified_fixed_defects']:state['verified_fixed_defects'].append(d)
state['open_defects']=sorted(state['open_defects']);state['verified_fixed_defects']=sorted(state['verified_fixed_defects']);state['current_correction_item']='D12-04';state['next_action']='Derive structural-action confidence from explicit evidence dimensions; no default HIGH. Then continue hierarchy/maturity/pair derivation and independent QA.'
STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest=MANIFEST.read_text(encoding='utf-8').replace('next_major_step = STEP_12_CORRECTION_EXECUTION_D12_03','next_major_step = STEP_12_CORRECTION_EXECUTION_D12_04',1)
for item in ['STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv','STEP_12_STRUCTURAL_UNITS_V5.tsv','STEP_12_NEW_PAGE_EVIDENCE_V2.tsv','STEP_12_NEW_PAGE_DEMAND_PHRASE_EVIDENCE_V2.tsv','STEP_12_NEW_PAGE_EVIDENCE_ACCEPTANCE_2026-08-31.md']:
    if item not in manifest:
        marker='```\n\nWhere older Step-09 planning state';manifest=manifest.replace(marker,item+'\n'+marker,1)
MANIFEST.write_text(manifest,encoding='utf-8')
flow=FLOW.read_text(encoding='utf-8')
# append authoritative current status instead of trusting stale earlier marker order
block='''\n### Accepted correction block — new-page evidence\n\nD12-02 (reopened residual), D12-03 and D12-10 are VERIFIED_FIXED after V5/V2 evidence acceptance. Current open defects: D12-04, D12-05, D12-06, D12-07, D12-11. New pages are not all final: missing direct Search boundaries remain explicit provisional dependencies.\n\n```text\nSTEP12_CURRENT_CORRECTION_ITEM = D12-04\nSTEP12_OPEN_DEFECTS_CURRENT = D12-04,D12-05,D12-06,D12-07,D12-11\n```\n'''
if '### Accepted correction block — new-page evidence' not in flow:flow+=block
FLOW.write_text(flow,encoding='utf-8')
