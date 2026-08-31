import csv,json
from pathlib import Path
R=Path(__file__).resolve().parent
P=R/'STEP_12_THIRD_AUDIT_GAP_REVIEW_PACKET.tsv';O=R/'STEP_12_THIRD_AUDIT_STRONG_FIT_GAP_REVIEW.tsv'
with P.open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
out=[r for r in rows if r['current_page_fit']=='STRONG_EXISTING_PAGE_FIT' and r['structural_action'] in {'EXPAND_EXISTING_PAGE','ADD_SECTION_OR_FAQ_TO_EXISTING'}]
fields=list(out[0].keys()) if out else []
with O.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(out)
print(json.dumps({'rows':len(out),'ids':[r['structural_unit_id'] for r in out]},ensure_ascii=False))
