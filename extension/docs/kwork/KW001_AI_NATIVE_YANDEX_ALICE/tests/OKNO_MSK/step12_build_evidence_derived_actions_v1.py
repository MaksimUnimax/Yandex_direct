import csv,json
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parent
UNITS=ROOT/'STEP_12_STRUCTURAL_UNITS_V5.tsv';ASSIGN=ROOT/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv';HIST=ROOT/'STEP_12_STRUCTURAL_ACTIONS.tsv';STEP08=ROOT/'STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv';STEP09=ROOT/'STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv';NEW=ROOT/'STEP_12_NEW_PAGE_EVIDENCE_V2.tsv';OUT=ROOT/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V1.tsv';OUT_QA=ROOT/'STEP_12_CONFIDENCE_QA_V1.json'

def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(p,rows,fields):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
units=read(UNITS);assign=read(ASSIGN);hist=read(HIST);s08={r['phrase']:r for r in read(STEP08)};s09={r['query']:r for r in read(STEP09)};new={r['candidate_id']:r for r in read(NEW)}
hist_by={r['cluster_id']:r for r in hist}
members=defaultdict(list)
for r in assign:
    if r['final_structural_unit_id']:members[r['final_structural_unit_id']].append(r)

NEW_CORE={
'PANORAMIC_WINDOWS_COMMERCIAL_CORE':('PANORAMIC_WINDOWS_COMMERCIAL','NEW_COMMERCIAL_PAGE'),
'WINDOW_HARDWARE_SELECTION_GUIDE':('WINDOW_HARDWARE_GUIDE','NEW_INFORMATIONAL_PAGE'),
'PVC_WINDOW_INSTALLATION_DIY':('PVC_WINDOW_INSTALLATION_DIY_GUIDE','NEW_INFORMATIONAL_PAGE'),
'PVC_WINDOW_REPAIR_DIY_GENERAL':('PVC_WINDOW_REPAIR_DIY_GUIDE','NEW_INFORMATIONAL_PAGE'),
'PVC_WINDOW_ADJUSTMENT_DIY':('PVC_WINDOW_REPAIR_DIY_GUIDE','NEW_INFORMATIONAL_PAGE'),
'WINDOW_REPLACEMENT_SERVICE':('WINDOW_REPLACEMENT_SERVICE','NEW_COMMERCIAL_PAGE'),
}
NEW_SUPPORT={'WINDOW_COMPONENT_SELECTION_INFO','WINDOW_HARDWARE_STANDARD_INFO','WINDOW_INSTALLATION_MATERIALS_INFO','WINDOW_HARDWARE_MAINTENANCE_INFO'}

def source_hist_actions(rs):
    return [hist_by[c]['structural_action'] for c in sorted({r['original_effective_cluster_id'] for r in rs}) if c in hist_by]

def demand_dim(rs,uid):
    if uid in NEW_CORE:
        return new[NEW_CORE[uid][0]]['wordstat_demand_verdict']
    direct=[]
    for r in rs:
        e=s08.get(r['phrase'])
        if e and int(e.get('result_occurrences') or 0)>0: direct.append(int(e.get('max_result_count') or 0))
    if len(direct)==len(rs) and direct:return 'OBSERVED_DIRECT_FOR_ALL_MEMBER_PHRASES'
    if direct:return 'OBSERVED_DIRECT_FOR_SOME_MEMBER_PHRASES'
    return 'NO_DIRECT_WORDSTAT_IN_PERSISTED_SET'

def search_dim(rs,unit):
    uid=unit['structural_unit_id']
    if uid in NEW_CORE:
        c=new[NEW_CORE[uid][0]]
        return 'DIRECT_CORE_QUERY_SUPPORT' if int(c['direct_step09_core_queries'])>0 else 'MATERIAL_BOUNDARY_GAP'
    direct=[s09[r['phrase']] for r in rs if r['phrase'] in s09]
    if direct:return 'DIRECT_QUERY_EVIDENCE_AVAILABLE'
    if 'PROVISIONAL' in unit['recommendation_maturity'] or 'PENDING_SEARCH' in unit['recommendation_maturity']:
        return 'MATERIAL_BOUNDARY_GAP'
    return 'NOT_REQUIRED_FOR_CURRENT_STEP12_ROLE'

def business_dim(unit,uid):
    st=unit['business_scope_state'];role=unit['unit_page_role']
    if st=='OUTSIDE_SCOPE':return 'VERIFIED_OUTSIDE'
    if 'UNVERIFIED' in st or 'UNVERIFIED' in role or 'PENDING_BUSINESS_TRUTH' in st:return 'UNVERIFIED_OR_CONDITIONAL'
    if uid=='PANORAMIC_WINDOWS_COMMERCIAL_CORE':return 'CONDITIONAL_BROAD_PRODUCT_OFFER'
    if uid=='WINDOW_REPLACEMENT_SERVICE':return 'CONDITIONAL_STANDALONE_SERVICE_ROLE'
    return 'VERIFIED_OR_CURRENT_FIRST_PARTY_SUPPORTED'

def page_fit_dim(unit,uid,hacts):
    role=unit['unit_page_role']
    if uid in NEW_CORE:return 'NONE_NEW_PAGE_CANDIDATE'
    if role.startswith('PRIMARY_EXISTING') or role in {'PRIMARY_EXISTING_HUB','PRIMARY_EXISTING_INFO','PRIMARY_EXISTING_PRODUCT','PRIMARY_EXISTING_SERVICE','PRIMARY_EXISTING_UTILITY','PRIMARY_EXISTING_TRUST_COMMERCIAL'}:return 'STRONG_EXISTING_PAGE_FIT'
    if 'PROVISIONAL' in role or role.startswith('SUPPORTING') or role.startswith('PROVISIONAL'):return 'PARTIAL_OR_SUPPORTING_PAGE_FIT'
    if role.startswith('NO_STANDALONE') or role in {'OUTSIDE','UNSERVABLE_NEUTRAL_REVIEW','DEFERRED'}:return 'NOT_APPLICABLE'
    if 'EXPAND_EXISTING_PAGE' in hacts or 'ADD_SECTION_OR_FAQ_TO_EXISTING' in hacts:return 'PARTIAL_EXISTING_PAGE_FIT'
    if 'KEEP_EXISTING_STRUCTURE' in hacts:return 'STRONG_EXISTING_PAGE_FIT'
    return 'REVIEW_REQUIRED'

def action_for(unit,uid,hacts):
    role=unit['unit_page_role'];st=unit['business_scope_state']
    if st=='OUTSIDE_SCOPE' or role=='OUTSIDE':return 'OUTSIDE_SCOPE_NO_ACTION'
    if st.startswith('DEFERRED') or role=='DEFERRED':return 'DEFER_PENDING_EVIDENCE'
    if st.startswith('NO_STANDALONE') or role.startswith('NO_STANDALONE') or role.startswith('UNSERVABLE'):return 'NO_STANDALONE_PAGE'
    if uid in NEW_CORE:return NEW_CORE[uid][1]
    if uid in NEW_SUPPORT and unit['primary_page_candidate'].startswith('PROPOSED_NEW:'):return 'INCLUDE_AS_SECTION_IN_PROPOSED_PAGE'
    if role.startswith('SUPPORTING') or role.startswith('PROVISIONAL') or role in {'PROVISIONAL_EXISTING_INFO'}:
        return 'ROUTE_TO_EXISTING_PAGE_AS_SUBTASK'
    if 'EXPAND_EXISTING_PAGE' in hacts:return 'EXPAND_EXISTING_PAGE'
    if 'ADD_SECTION_OR_FAQ_TO_EXISTING' in hacts:return 'ADD_SECTION_OR_FAQ_TO_EXISTING'
    if role.startswith('PRIMARY_EXISTING') or 'KEEP_EXISTING_STRUCTURE' in hacts:return 'KEEP_EXISTING_STRUCTURE'
    return 'REVIEW_ACTION_REQUIRED'

def page_targets(unit,uid):
    primary=unit['primary_page_candidate'];supporting=unit['supporting_page']
    if uid not in NEW_CORE:return primary,supporting
    candidate_id=NEW_CORE[uid][0]
    proposed=new[candidate_id]['proposed_page']
    if not proposed.startswith('PROPOSED_NEW:'):
        raise RuntimeError(f'Canonical proposed page missing for {uid}: {proposed}')
    if primary and not primary.startswith('PROPOSED_NEW:') and primary!=proposed and not supporting:
        supporting=primary
    return proposed,supporting

def maturity_for(unit,uid,search):
    st=unit['business_scope_state']
    if st.startswith('DEFERRED') or unit['unit_page_role']=='DEFERRED':return 'DEFERRED_PENDING_MISSING_EVIDENCE'
    if uid in NEW_CORE:return new[NEW_CORE[uid][0]]['candidate_maturity_after_existing_evidence']
    if 'PROVISIONAL' in unit['recommendation_maturity'] or search=='MATERIAL_BOUNDARY_GAP':return unit['recommendation_maturity'] if 'PROVISIONAL' in unit['recommendation_maturity'] else 'PROVISIONAL_PENDING_SEARCH_BOUNDARY'
    return 'FINAL_WITHIN_STEP12_EVIDENCE'

def confidence(task,business,pagefit,demand,search,hierarchy,maturity,action):
    reasons=[]
    if maturity.startswith('DEFERRED'):return 'LOW','Deferred because a named material evidence gap remains.'
    if action=='REVIEW_ACTION_REQUIRED':return 'LOW','Action itself remains unresolved.'
    if business in {'UNVERIFIED_OR_CONDITIONAL','CONDITIONAL_BROAD_PRODUCT_OFFER','CONDITIONAL_STANDALONE_SERVICE_ROLE'}:reasons.append('business truth/standalone role is conditional')
    if search=='MATERIAL_BOUNDARY_GAP':reasons.append('material Search page boundary is not directly probed')
    if hierarchy=='PENDING_FOR_PROPOSED_PAGE':reasons.append('new-page hierarchy is not yet finalized')
    if task!='STRONG':reasons.append('task coherence is not strong')
    if action in {'NEW_COMMERCIAL_PAGE','NEW_INFORMATIONAL_PAGE'}:
        if reasons:return 'MEDIUM','; '.join(reasons)
        return 'HIGH','New-page task, business, demand, Search boundary and hierarchy are all directly supported.'
    if maturity.startswith('PROVISIONAL') or reasons:return 'MEDIUM','; '.join(reasons) or 'Recommendation remains provisional.'
    if pagefit in {'STRONG_EXISTING_PAGE_FIT','NOT_APPLICABLE'} and task=='STRONG':return 'HIGH','Coherent task and current structural role are directly supported; no material unresolved page-boundary dependency.'
    return 'MEDIUM','Page fit/support role is partial even though the task is coherent.'

out=[]
for u in units:
    uid=u['structural_unit_id'];rs=members[uid];hacts=source_hist_actions(rs)
    task='WEAK' if u['business_scope_state'].startswith('DEFERRED') or 'AMBIGUOUS' in uid else 'STRONG'
    business=business_dim(u,uid);pagefit=page_fit_dim(u,uid,hacts);demand=demand_dim(rs,uid);search=search_dim(rs,u)
    primary,supporting=page_targets(u,uid)
    hierarchy='PENDING_FOR_PROPOSED_PAGE' if primary.startswith('PROPOSED_NEW:') else ('NOT_APPLICABLE' if pagefit=='NOT_APPLICABLE' else 'EXISTING_STRUCTURE_KNOWN')
    action=action_for(u,uid,hacts);maturity=maturity_for(u,uid,search);conf,why=confidence(task,business,pagefit,demand,search,hierarchy,maturity,action)
    out.append({'structural_unit_id':uid,'phrase_count':len(rs),'source_effective_clusters':u['source_effective_clusters'],'user_task':u['user_task'],'intent_type':u['intent_type'],'business_scope_state':u['business_scope_state'],'unit_page_role':u['unit_page_role'],'primary_page_candidate':primary,'supporting_page':supporting,'structural_action':action,'task_coherence':task,'business_truth':business,'current_page_fit':pagefit,'demand_support':demand,'search_boundary_support':search,'hierarchy_clarity':hierarchy,'recommendation_maturity':maturity,'final_confidence':conf,'confidence_downgrade_reason':why,'historical_action_mix':';'.join(sorted(set(hacts))),'confidence_origin':'DERIVED_FROM_EXPLICIT_EVIDENCE_DIMENSIONS__NO_DEFAULT'})
write(OUT,out,list(out[0].keys()))
canonical_new_targets={uid:new[cid]['proposed_page'] for uid,(cid,_) in NEW_CORE.items()}
new_action_rows=[r for r in out if r['structural_action'] in {'NEW_COMMERCIAL_PAGE','NEW_INFORMATIONAL_PAGE'}]
new_target_mismatches=[r['structural_unit_id'] for r in new_action_rows if canonical_new_targets.get(r['structural_unit_id'])!=r['primary_page_candidate']]
replacement=next(r for r in out if r['structural_unit_id']=='WINDOW_REPLACEMENT_SERVICE')
qa={'status':'CANDIDATE_CONFIDENCE_V1_READY_FOR_MANUAL_REVIEW','structural_units':len(out),'default_high_confidence_used':False,'rows_without_evidence_dimensions':sum(any(not r[k] for k in ['task_coherence','business_truth','current_page_fit','demand_support','search_boundary_support','hierarchy_clarity','recommendation_maturity','final_confidence']) for r in out),'high_rows':sum(r['final_confidence']=='HIGH' for r in out),'medium_rows':sum(r['final_confidence']=='MEDIUM' for r in out),'low_rows':sum(r['final_confidence']=='LOW' for r in out),'new_page_high_with_material_search_gap':sum(r['structural_action'] in {'NEW_COMMERCIAL_PAGE','NEW_INFORMATIONAL_PAGE'} and r['final_confidence']=='HIGH' and r['search_boundary_support']=='MATERIAL_BOUNDARY_GAP' for r in out),'conditional_business_high_commercial_create':sum(r['structural_action']=='NEW_COMMERCIAL_PAGE' and r['final_confidence']=='HIGH' and r['business_truth'].startswith('CONDITIONAL') for r in out),'review_action_required_rows':sum(r['structural_action']=='REVIEW_ACTION_REQUIRED' for r in out),'new_page_action_rows':len(new_action_rows),'new_page_action_primary_target_mismatches':len(new_target_mismatches),'new_page_action_primary_target_mismatch_units':new_target_mismatches,'replacement_service_primary_target_correct':replacement['primary_page_candidate']=='PROPOSED_NEW:/uslugi/zamena-okon/','replacement_service_existing_installation_preserved_as_supporting':replacement['supporting_page']=='https://okno-msk.ru/uslugi/ustanovka-okon/','defects_closed_by_script_alone':[],'defects_candidate_for_closure_after_manual_review':['D12-13']}
if len(out)!=len(units) or qa['rows_without_evidence_dimensions'] or qa['new_page_high_with_material_search_gap'] or qa['conditional_business_high_commercial_create'] or qa['review_action_required_rows'] or qa['new_page_action_primary_target_mismatches'] or not qa['replacement_service_primary_target_correct'] or not qa['replacement_service_existing_installation_preserved_as_supporting']:qa['status']='FAIL'
OUT_QA.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False))
