import csv
from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv'
out=R/'STEP_12_POST_CLOSE_ALL_PROPOSED_REFS.tsv'
rows=list(csv.DictReader(p.open(encoding='utf-8',newline=''),delimiter='\t'))
hits=[]
for r in rows:
    if 'PROPOSED_NEW:' in (r.get('primary_page_candidate','')+' '+r.get('supporting_page','')):
        hits.append({k:r.get(k,'') for k in ['structural_unit_id','user_task','intent_type','structural_action','primary_page_candidate','supporting_page','recommendation_maturity','final_confidence']})
with out.open('w',encoding='utf-8',newline='') as f:
    fields=list(hits[0].keys()) if hits else ['structural_unit_id']
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(hits)
print({'proposed_ref_rows':len(hits)})
