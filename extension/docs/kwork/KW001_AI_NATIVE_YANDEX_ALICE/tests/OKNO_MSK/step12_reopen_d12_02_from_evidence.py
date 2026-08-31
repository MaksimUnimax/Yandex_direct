import csv, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
LEDGER=ROOT/'STEP_12_CORRECTION_DEFECT_LEDGER.tsv'
STATE=ROOT/'STEP_12_CORRECTION_CURRENT_STATE.json'
EVID=ROOT/'STEP_12_NEW_PAGE_EVIDENCE.tsv'

# Evidence precondition: direct Search exposed the residual reviews task inside hardware-guide core.
rows=list(csv.DictReader(EVID.open(encoding='utf-8'),delimiter='\t'))
hw=next(r for r in rows if r['candidate_id']=='WINDOW_HARDWARE_GUIDE')
assert 'оконная фурнитура отзывы -> WINDOW_HARDWARE_REVIEWS' in hw['direct_step09_query_evidence']
assert 'INFORMATIONAL_NON_LANDING' in hw['direct_step09_query_evidence']

with LEDGER.open(encoding='utf-8',newline='') as f: defects=list(csv.DictReader(f,delimiter='\t'))
fields=list(defects[0].keys())
for r in defects:
    if r['defect_id']=='D12-02':
        r['status']='REOPENED_AFTER_EVIDENCE_MATRIX'
        r['correction_artifact']='STEP_12_NEW_PAGE_EVIDENCE.tsv | STEP_12_NEW_PAGE_DEMAND_PHRASE_EVIDENCE.tsv'
        r['notes']=(r['notes']+' | ' if r['notes'] else '')+'Reopened because direct Step09 evidence for generic “оконная фурнитура отзывы” shows reviews/forum INFORMATIONAL_NON_LANDING, while V4 still placed that phrase in WINDOW_HARDWARE_SELECTION_GUIDE. Fix the residual row, rebuild units/evidence, then repeat acceptance.'
with LEDGER.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(defects)

state=json.loads(STATE.read_text(encoding='utf-8'))
if 'D12-02' not in state['open_defects']: state['open_defects'].append('D12-02')
if 'D12-02' in state['verified_fixed_defects']: state['verified_fixed_defects'].remove('D12-02')
state['open_defects']=sorted(state['open_defects'])
state['verified_fixed_defects']=sorted(state['verified_fixed_defects'])
state['current_correction_item']='D12-02_REOPENED_FROM_D12-03_EVIDENCE'
state['next_action']='Move generic window-hardware reviews out of WINDOW_HARDWARE_SELECTION_GUIDE, rebuild structural units/new-page evidence, repeat D12-02 semantic acceptance, then continue D12-03/D12-10.'
STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
