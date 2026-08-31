import csv,json
from pathlib import Path

R=Path(__file__).resolve().parent
ACTIONS=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V5.tsv'
ASSIGN=R/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V6.tsv'
LINKS=R/'STEP_12_INTERNAL_LINK_ACTIONS_V5.tsv'
OUT_UNITS=R/'STEP_12_D12_28_UNIT_REVIEW_PACKET.tsv'
OUT_PHRASES=R/'STEP_12_D12_28_MEMBER_PHRASES_PACKET.tsv'
OUT_LINKS=R/'STEP_12_D12_29_IMPLEMENT_REVIEW_PACKET.tsv'
OUT_QA=R/'STEP_12_D12_28_29_REVIEW_PACKET_QA.json'

def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(p,rows,fields):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n',extrasaction='ignore');w.writeheader();w.writerows(rows)

actions=read(ACTIONS);assign=read(ASSIGN);links=read(LINKS)
quality=[r for r in actions if r.get('gap_type')=='QUALITY_GAP']
quality_ids={r['structural_unit_id'] for r in quality}
assert len(actions)==160
assert len(assign)==2332
assert len(quality)==20,(len(quality),sorted(quality_ids))
impl=[r for r in links if r.get('link_action_state')=='IMPLEMENT']
assert len(impl)==28,len(impl)

unit_fields=['structural_unit_id','phrase_count','user_task','intent_type','primary_page_candidate','supporting_page','structural_action','gap_type','gap_evidence','fresh_site_check_status','current_page_fit','owner_goal_evidence_source','owner_policy_materiality','recommendation_maturity','final_confidence']
write(OUT_UNITS,quality,unit_fields)

phrase_rows=[]
for r in assign:
    uid=(r.get('final_structural_unit_id') or '').strip()
    if uid in quality_ids:
        phrase_rows.append({
            'structural_unit_id':uid,
            'phrase':r.get('phrase',''),
            'original_effective_cluster_id':r.get('original_effective_cluster_id',''),
            'assignment_origin':r.get('assignment_origin',''),
            'correction_reason':r.get('correction_reason',''),
        })
phrase_rows.sort(key=lambda r:(r['structural_unit_id'],r['phrase']))
phrase_fields=['structural_unit_id','phrase','original_effective_cluster_id','assignment_origin','correction_reason']
write(OUT_PHRASES,phrase_rows,phrase_fields)

link_fields=['link_action_id','structural_unit_id','structural_action','link_action_state','source_url','target_url','relation_type','placement_context','anchor_concept','user_journey_purpose','business_handoff','evidence_origin']
write(OUT_LINKS,impl,link_fields)

expected=sum(int(r['phrase_count']) for r in quality)
assert len(phrase_rows)==expected,(len(phrase_rows),expected)
qa={
  'date':'2026-08-31',
  'status':'D12_28_D12_29_REVIEW_PACKET_READY',
  'structural_actions':len(actions),
  'quality_gap_units':len(quality),
  'quality_gap_member_phrases':len(phrase_rows),
  'prior_implement_links':len(impl),
  'active_assignment_rows':len(assign),
  'step13_executed':False,
  'packet_origin':'DIRECT_EXTRACTION_FROM_ACCEPTED_V5_ACTIONS_V6_ASSIGNMENTS_AND_V5_LINKS_WITHOUT_REINTERPRETING_ACTIONS'
}
OUT_QA.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False,indent=2))
