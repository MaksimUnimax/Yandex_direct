import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parent
ASSIGN=ROOT/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv'
UNITS=ROOT/'STEP_12_STRUCTURAL_UNITS_V5.tsv'
A2=ROOT/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv'
OUT=ROOT/'STEP_12_POST_CLOSE_NEW_PAGE_REVIEW_PACKET.tsv'

TARGET_UNITS={
'PANORAMIC_WINDOWS_COMMERCIAL_CORE',
'PANORAMIC_WINDOW_TECH_SELECTION_INFO',
'PANORAMIC_OUTDOOR_GLAZING',
'WINDOW_HARDWARE_SELECTION_GUIDE',
'WINDOW_COMPONENT_SELECTION_INFO',
'WINDOW_HARDWARE_STANDARD_INFO',
'PVC_WINDOW_INSTALLATION_DIY',
'WINDOW_INSTALLATION_MATERIALS_INFO',
'PVC_WINDOW_REPAIR_DIY_GENERAL',
'PVC_WINDOW_ADJUSTMENT_DIY',
'WINDOW_HARDWARE_MAINTENANCE_INFO',
'WINDOW_REPLACEMENT_SERVICE',
}

def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))

a=read(ASSIGN); units={r['structural_unit_id']:r for r in read(UNITS)}; actions={r['structural_unit_id']:r for r in read(A2)}
rows=[]
for r in a:
    uid=r.get('final_structural_unit_id','')
    if uid not in TARGET_UNITS: continue
    u=units[uid]; ac=actions[uid]
    rows.append({
      'structural_unit_id':uid,
      'phrase':r['phrase'],
      'user_task':u.get('user_task',''),
      'intent_type':u.get('intent_type',''),
      'business_scope_state':u.get('business_scope_state',''),
      'unit_page_role':u.get('unit_page_role',''),
      'current_structural_action':ac.get('structural_action',''),
      'current_primary_page_candidate':ac.get('primary_page_candidate',''),
      'current_supporting_page':ac.get('supporting_page',''),
      'current_maturity':ac.get('recommendation_maturity',''),
      'current_confidence':ac.get('final_confidence',''),
      'source_effective_clusters':ac.get('source_effective_clusters',''),
      'assignment_origin':r.get('assignment_origin',''),
      'assignment_correction_reason':r.get('assignment_correction_reason',''),
    })
fields=list(rows[0].keys())
with OUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
print({'rows':len(rows),'units':len({r['structural_unit_id'] for r in rows})})
