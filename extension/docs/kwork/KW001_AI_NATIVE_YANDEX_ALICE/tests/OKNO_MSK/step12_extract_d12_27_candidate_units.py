import csv,json,re
from pathlib import Path
R=Path(__file__).resolve().parent
V4=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V4.tsv';O=R/'STEP_12_D12_27_CANDIDATE_UNITS.tsv'
with V4.open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
need=['FRENCH','ALUMIN','HARDWARE','ACCESSOR','INSPIR','DIY','VENT','HANDLE','COMPONENT','DECOR','PRIVATE_HOUSE','BALCON']
out=[]
for r in rows:
    hay=' '.join([r.get('structural_unit_id',''),r.get('user_task',''),r.get('intent_type',''),r.get('primary_page_candidate',''),r.get('supporting_page','')]).upper()
    if any(k in hay for k in need):
        out.append({k:r.get(k,'') for k in ['structural_unit_id','user_task','intent_type','structural_action','primary_page_candidate','supporting_page','business_scope_state','unit_page_role','final_confidence','recommendation_maturity']})
with O.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(out[0].keys()),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(out)
print(json.dumps({'rows':len(out),'ids':[r['structural_unit_id'] for r in out]},ensure_ascii=False))
