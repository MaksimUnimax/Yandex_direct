import csv,json
from collections import defaultdict
from pathlib import Path
R=Path(__file__).resolve().parent
V4=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V4.tsv';A=R/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv';OUT=R/'STEP_12_THIRD_AUDIT_GAP_REVIEW_PACKET.tsv';Q=R/'STEP_12_THIRD_AUDIT_GAP_REVIEW_PACKET_QA.json'
def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(p,rows,fields):
    with p.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
v4=read(V4);ass=read(A);members=defaultdict(list)
for a in ass:
    u=(a.get('final_structural_unit_id') or '').strip()
    if u:members[u].append(a['phrase'])
review_actions={'EXPAND_EXISTING_PAGE','ADD_SECTION_OR_FAQ_TO_EXISTING','DEFER_PENDING_EVIDENCE'}
rows=[]
for r in v4:
    if r['structural_action'] not in review_actions:continue
    ph=sorted(set(members[r['structural_unit_id']]))
    rows.append({
      'structural_unit_id':r['structural_unit_id'],'structural_action':r['structural_action'],'user_task':r['user_task'],'intent_type':r['intent_type'],'member_count':len(ph),'member_phrase_examples':' | '.join(ph[:8]),
      'primary_page_candidate':r['primary_page_candidate'],'supporting_page':r['supporting_page'],'current_page_fit':r['current_page_fit'],'existing_content_reuse':r['existing_content_reuse'],'fresh_site_check_status':r['fresh_site_check_status'],'business_truth':r['business_truth'],'owner_primary_goal':r['owner_primary_goal'],'owner_goal_evidence_source':r['owner_goal_evidence_source'],'business_potential':r['business_potential'],'search_boundary_support':r['search_boundary_support'],'previous_gap_type_candidate':r['gap_type'],'previous_gap_evidence_candidate':r['gap_evidence'],'confidence_downgrade_reason':r['confidence_downgrade_reason'],'second_audit_correction_origin':r['second_audit_correction_origin']})
fields=list(rows[0].keys());write(OUT,rows,fields)
qa={'rows':len(rows),'expand':sum(r['structural_action']=='EXPAND_EXISTING_PAGE' for r in rows),'section':sum(r['structural_action']=='ADD_SECTION_OR_FAQ_TO_EXISTING' for r in rows),'defer':sum(r['structural_action']=='DEFER_PENDING_EVIDENCE' for r in rows),'all_have_phrases':all(int(r['member_count'])>0 for r in rows)}
Q.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False))
