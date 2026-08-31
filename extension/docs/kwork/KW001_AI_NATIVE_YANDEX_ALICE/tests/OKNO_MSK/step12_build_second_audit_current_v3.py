import csv, json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from urllib.parse import urlsplit

R=Path(__file__).resolve().parent
V1=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V1.tsv'
OLDV2=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv'
ASSIGN=R/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv'
HIST=R/'STEP_12_STRUCTURAL_ACTIONS.tsv'
CORR=R/'STEP_12_POST_CLOSE_CURRENT_SITE_BUSINESS_CORRECTIONS.tsv'
FRESH=R/'STEP_12_SECOND_AUDIT_FRESHNESS_EVIDENCE.tsv'
OUT=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V3.tsv'
OUT_PAIRS=R/'STEP_12_STEP13_CANDIDATE_PAIRS_V3.tsv'
OUT_DEP=R/'STEP_12_MATURITY_DEPENDENCY_LEDGER_V3.tsv'
OUT_MAP=R/'STEP_12_PHRASE_ACTION_MAP_FINAL_V3.tsv'
OUT_DELTA=R/'STEP_12_SECOND_AUDIT_ACTION_DELTA.tsv'
OUT_CONCEPTS=R/'STEP_12_FORMER_NEW_PAGE_CONCEPTS_SECOND_AUDIT.tsv'
OUT_QA=R/'STEP_12_SECOND_AUDIT_GENERATOR_QA.json'


def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(p,rows,fields=None):
    if fields is None: fields=list(rows[0].keys()) if rows else []
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
def norm(v):
    v=(v or '').strip()
    if not v:return ''
    if v.startswith('PROPOSED_NEW:'):
        x=v.split(':',1)[1].strip(); x=x if x.startswith('/') else '/'+x
        return 'https://okno-msk.ru'+x
    return v if v.startswith('http://') or v.startswith('https://') else ''
def parent_child(a,b):
    pa,pb=urlsplit(a),urlsplit(b)
    if pa.netloc!=pb.netloc:return False
    aa=pa.path.rstrip('/')+'/';bb=pb.path.rstrip('/')+'/'
    return aa!=bb and (aa.startswith(bb) or bb.startswith(aa))
def clusters(v):return [x.strip() for x in (v or '').split(';') if x.strip()]

v1=read(V1);oldv2=read(OLDV2);assign=read(ASSIGN);hist=read(HIST);corr=read(CORR);fresh=read(FRESH)
assert len(v1)==160 and len(oldv2)==160 and len(assign)==2332
cb={r['structural_unit_id']:r for r in corr}
assert len(cb)==14, (len(cb),sorted(cb))
assert len(fresh)==5

# Build a current pre-pair action set. Existing accepted V1 evidence is retained unless
# the second audit has explicit fresh-site/business correction evidence.
pre=[]
for src in v1:
    uid=src['structural_unit_id'];o=dict(src)
    c=cb.get(uid)
    if c:
        o['structural_action']=c['corrected_structural_action']
        o['primary_page_candidate']=c['corrected_primary_page_candidate']
        o['supporting_page']=c['corrected_supporting_page']
        o['final_confidence']=c['corrected_confidence']
        o['recommendation_maturity']='FINAL_WITHIN_STEP12_EVIDENCE'
        o['business_truth']='VERIFIED_OR_CURRENT_FIRST_PARTY_SUPPORTED'
        o['current_page_fit']='STRONG_EXISTING_PAGE_FIT' if o['structural_action']=='KEEP_EXISTING_STRUCTURE' else 'PARTIAL_OR_SUPPORTING_PAGE_FIT'
        o['search_boundary_support']='NOT_REQUIRED_FOR_CURRENT_REUSE_ACTION__STEP13_ONLY_IF_PAIR_DERIVED'
        o['hierarchy_clarity']='CURRENT_EXISTING_STRUCTURE_VERIFIED'
        o['confidence_downgrade_reason']=c['correction_reason']
        goal_state='PUBLIC_BUSINESS_GOAL_INFERRED_FROM_CURRENT_FIRST_PARTY_OFFER_AND_CONTENT_STRATEGY'
        fresh_status=c['fresh_site_check_status']
        reuse=c['existing_content_reuse']
        origin='SECOND_EXTERNAL_AUDIT_D12_16_TO_D12_20_FRESH_CURRENT_SITE_AND_OWNER_GOAL_REVIEW'
        owner_goal=c['owner_primary_goal'];desired=c['desired_user_outcome'];bp=c['business_potential'];role=c['content_role'];counter=c['counterproductive_to_core_offer']
    else:
        fresh_status='PREVIOUS_CURRENT_PAGE_EVIDENCE_RETAINED__FRESH_CREATE_GATE_NOT_APPLICABLE'
        reuse='UNCHANGED_PREVIOUS_EXISTING_PAGE_OR_NO_PAGE_DECISION'
        origin='PREVIOUS_CORRECTED_EVIDENCE_RETAINED__NO_SECOND_AUDIT_MATERIAL_CHANGE'
        action=o['structural_action'];intent=o['intent_type']
        if action=='OUTSIDE_SCOPE_NO_ACTION':
            goal_state='NOT_APPLICABLE_OUTSIDE_SCOPE';owner_goal='NOT_APPLICABLE';desired='NO_ACTION';bp='NOT_APPLICABLE';role='DEPRIORITIZE';counter='NOT_APPLICABLE'
        elif action in {'DEFER_PENDING_EVIDENCE','NO_STANDALONE_PAGE'}:
            goal_state='PREVIOUS_EVIDENCE_OR_POLICY_BOUNDARY_RETAINED';owner_goal='NO_STANDALONE_IMPLEMENTATION_OR_EVIDENCE_PENDING';desired='DO_NOT_CREATE_UNSUPPORTED_PAGE';bp='LOW_OR_UNRESOLVED';role='DEPRIORITIZE_OR_DEFER';counter='NOT_APPLICABLE'
        elif 'COMMERCIAL' in intent or 'SERVICE' in intent or intent=='SHOPPING':
            goal_state='PUBLIC_BUSINESS_GOAL_INFERRED_FROM_EXISTING_COMMERCIAL_SITE_ROLE';owner_goal='LEADS_AND_SALES';desired='MOVE_USER_TO_RELEVANT_CURRENT_COMMERCIAL_OR_SERVICE_PATH';bp='HIGH_OR_MEDIUM_EXISTING_BUSINESS_ROLE';role='SELL_OR_ASSIST_DECISION';counter='NO_MATERIAL_CONFLICT_IDENTIFIED_IN_EXISTING_ROLE'
        else:
            goal_state='PUBLIC_CONTENT_STRATEGY_INFERRED_FROM_EXISTING_PUBLISHED_ROLE';owner_goal='ASSIST_DECISION_AUTHORITY_OR_SAFE_SELF_SERVICE';desired='ANSWER_USER_NEED_AND_CONNECT_TO_RELEVANT_BUSINESS_PATH_WHERE_NATURAL';bp='MEDIUM_EXISTING_CONTENT_ROLE';role='ASSIST_DECISION_OR_AUTHORITY';counter='NO_MATERIAL_CONFLICT_IDENTIFIED_IN_EXISTING_PUBLISHED_ROLE'
    o.update({
      'owner_goal_evidence_state':goal_state,
      'owner_primary_goal':owner_goal,
      'desired_user_outcome':desired,
      'business_potential':bp,
      'content_role':role,
      'counterproductive_to_core_offer':counter,
      'fresh_site_check_status':fresh_status,
      'existing_content_reuse':reuse,
      'second_audit_correction_origin':origin,
    })
    # Old Step13 overlay will be recomputed from the new current routing graph.
    o['recommendation_maturity']='DEFERRED_PENDING_MISSING_EVIDENCE' if o['structural_action']=='DEFER_PENDING_EVIDENCE' else o['recommendation_maturity']
    pre.append(o)

# Hard current-architecture invariants before graph derivation.
assert not [r for r in pre if 'PROPOSED_NEW:' in (r['primary_page_candidate']+' '+r['supporting_page'])]
assert not [r for r in pre if r['structural_action'] in {'NEW_COMMERCIAL_PAGE','NEW_INFORMATIONAL_PAGE'}]
assert all(r['owner_goal_evidence_state'] and r['business_potential'] and r['content_role'] for r in pre)
by={r['structural_unit_id']:r for r in pre}

members=defaultdict(list);source_uids=defaultdict(set)
for a in assign:
    uid=a.get('final_structural_unit_id','').strip()
    if uid:
        members[uid].append(a['phrase'])
        src=a.get('original_effective_cluster_id','').strip()
        if src:source_uids[src].add(uid)
page_uids=defaultdict(set)
for uid,r in by.items():
    p=norm(r['primary_page_candidate'])
    if p:page_uids[p].add(uid)
hist_follow={r['cluster_id']:(r.get('step13_followup_required','').strip().lower()=='true') for r in hist}

pairs={}
def add_pair(a,b,route,units=None,srcs=None):
    a,b=norm(a),norm(b)
    if not a or not b or a==b:return
    k=tuple(sorted((a,b)))
    x=pairs.setdefault(k,{'routes':set(),'units':set(),'clusters':set()})
    x['routes'].add(route);x['units'].update(units or []);x['clusters'].update(srcs or [])
# explicit primary/support relations
for uid,r in by.items():
    a,b=norm(r['primary_page_candidate']),norm(r['supporting_page'])
    if a and b and a!=b:
        add_pair(a,b,'EXPLICIT_PRIMARY_SUPPORTING_EDGE',{uid}|page_uids.get(b,set()),clusters(r['source_effective_clusters']))
# same upstream cluster now routed to multiple current primary pages
for src,uids in source_uids.items():
    pu=defaultdict(set)
    for uid in uids:
        p=norm(by[uid]['primary_page_candidate'])
        if p:pu[p].add(uid)
    for a,b in combinations(sorted(pu),2):add_pair(a,b,'SHARED_SOURCE_CLUSTER_PRIMARY_DESTINATIONS',pu[a]|pu[b],{src})

pair_rows=[]
for i,((a,b),x) in enumerate(sorted(pairs.items()),1):
    reasons=set()
    if any(hist_follow.get(c,False) for c in x['clusters']):reasons.add('HISTORICAL_KNOWN_FOLLOWUP_SIGNAL_PRESERVED')
    for uid in x['units']:
        r=by[uid]
        if r['search_boundary_support']=='MATERIAL_BOUNDARY_GAP':reasons.add('MATERIAL_SEARCH_BOUNDARY_GAP_IN_CONTRIBUTING_UNIT')
        if 'PENDING_SEARCH' in r['recommendation_maturity']:reasons.add('CONTRIBUTING_UNIT_ALREADY_SEARCH_PROVISIONAL')
    if 'SHARED_SOURCE_CLUSTER_PRIMARY_DESTINATIONS' in x['routes'] and not parent_child(a,b):reasons.add('NON_HIERARCHICAL_MULTI_PRIMARY_ROUTE_FROM_SAME_SOURCE_CLUSTER')
    normal=[]
    if parent_child(a,b):normal.append('PARENT_CHILD_RELATION_CAN_BE_NORMAL_WHEN_TASK_BOUNDARIES_ARE_DISTINCT')
    if 'EXPLICIT_PRIMARY_SUPPORTING_EDGE' in x['routes']:normal.append('PRIMARY_SUPPORTING_JOURNEY_RELATION_CAN_BE_NORMAL')
    if 'SHARED_SOURCE_CLUSTER_PRIMARY_DESTINATIONS' in x['routes']:normal.append('SAME_UPSTREAM_FAMILY_CAN_NORMALLY_SPLIT_ACROSS_DISTINCT_USER_TASKS')
    rel=sorted(x['units']); tasks=sorted({by[u]['user_task'] for u in rel})
    ev=[]
    for u in rel:
        ph=sorted(set(members.get(u,[])));ev.append(f"{u}[{len(ph)}]: {' | '.join(ph[:3])}")
    pair_rows.append({
      'pair_id':f'V3P{i:04d}','page_a':a,'page_b':b,'derivation_routes':';'.join(sorted(x['routes'])),'source_effective_clusters':';'.join(sorted(x['clusters'])),'relation_structural_units':';'.join(rel),'member_evidence':' || '.join(ev),'adjacent_task':' || '.join(tasks),'normal_overlap_rationale':';'.join(normal),'later_direct_search_check_needed':'true' if reasons else 'false','search_check_reason':';'.join(sorted(reasons)) if reasons else 'NO_MATERIAL_DIRECT_SEARCH_TRIGGER_DERIVED_AT_STEP12','derivation_origin':'DETERMINISTIC_FROM_SECOND_AUDIT_CURRENT_ROUTING_GRAPH_V3_NO_WITHDRAWN_PROPOSED_PAGES'})

pair_ids=defaultdict(list);pair_reasons=defaultdict(set)
for p in pair_rows:
    if p['later_direct_search_check_needed']!='true':continue
    rs=[x for x in p['search_check_reason'].split(';') if x]
    for uid in [x for x in p['relation_structural_units'].split(';') if x]:
        pair_ids[uid].append(p['pair_id']);pair_reasons[uid].update(rs)

# Final V3 maturity/confidence and explanation from current state.
v3=[];deps=[]
for src in pre:
    r=dict(src);uid=r['structural_unit_id'];dep=bool(pair_ids.get(uid));base=r['recommendation_maturity'];old_conf=r['final_confidence']
    if r['structural_action']=='DEFER_PENDING_EVIDENCE' or base.startswith('DEFERRED'):
        mat='DEFERRED_PENDING_MISSING_EVIDENCE'
    elif dep:
        mat='PROVISIONAL_PENDING_STEP13_CONFLICT_CHECK'
    elif base.startswith('PROVISIONAL'):
        mat='DEFERRED_PENDING_MISSING_EVIDENCE'
    else:
        mat='FINAL_WITHIN_STEP12_EVIDENCE'
    conf='LOW' if mat.startswith('DEFERRED') else ('MEDIUM' if dep and old_conf=='HIGH' else old_conf)
    why=[]
    if uid in cb:why.append(cb[uid]['correction_reason'])
    if r['business_potential'] in {'NEGATIVE_OR_COUNTERPRODUCTIVE_FOR_NEUTRAL_DIY','LOW_OR_UNRESOLVED'}:why.append('Business potential constrains the content/page action.')
    if dep:why.append('Step-13 current-page pair check remains: '+';'.join(sorted(pair_ids[uid])))
    if mat.startswith('DEFERRED'):why.append('A named non-Step13 evidence/policy gap remains.')
    if not why:why.append('Current existing-page/content role retained from previously verified evidence; no second-audit material contradiction found.')
    r['recommendation_maturity']=mat;r['final_confidence']=conf;r['confidence_downgrade_reason']=' '.join(why)
    r['step13_dependency_required']='true' if dep else 'false';r['step13_candidate_pair_ids']=';'.join(sorted(pair_ids.get(uid,[])))
    r['maturity_dependency_detail']=';'.join(sorted(pair_reasons.get(uid,set()))) if dep else 'NONE'
    r['maturity_origin']='DERIVED_FROM_SECOND_AUDIT_CURRENT_ROUTING_GRAPH_V3_AND_EXPLICIT_MISSING_EVIDENCE'
    r['confidence_reason_origin']='REGENERATED_FROM_CURRENT_V3_EVIDENCE_AFTER_FRESHNESS_BUSINESS_AND_PAIR_OVERLAYS'
    v3.append(r)
    deps.append({'structural_unit_id':uid,'structural_action':r['structural_action'],'primary_page_candidate':r['primary_page_candidate'],'corrected_maturity':mat,'corrected_confidence':conf,'step13_dependency_required':r['step13_dependency_required'],'step13_candidate_pair_ids':r['step13_candidate_pair_ids'],'dependency_reason':r['maturity_dependency_detail'],'evidence_origin':'COMPUTED_FROM_SECOND_AUDIT_CURRENT_GRAPH'})

# Phrase-level current map.
v3by={r['structural_unit_id']:r for r in v3}; phrase_rows=[]
for a in assign:
    uid=a.get('final_structural_unit_id','').strip()
    if not uid:
        phrase_rows.append({'phrase':a['phrase'],'final_structural_unit_id':'','user_task':'','structural_action':'DEFER_UNRESOLVED','primary_page_candidate':'','supporting_page':'','owner_primary_goal':'','business_potential':'','content_role':'','recommendation_maturity':'DEFERRED_PENDING_MISSING_EVIDENCE','final_confidence':'LOW','step13_dependency_required':'false','step13_candidate_pair_ids':'','mapping_origin':'STEP12_SECOND_AUDIT_UNRESOLVED_PRESERVED'})
    else:
        r=v3by[uid]
        phrase_rows.append({'phrase':a['phrase'],'final_structural_unit_id':uid,'user_task':r['user_task'],'structural_action':r['structural_action'],'primary_page_candidate':r['primary_page_candidate'],'supporting_page':r['supporting_page'],'owner_primary_goal':r['owner_primary_goal'],'business_potential':r['business_potential'],'content_role':r['content_role'],'recommendation_maturity':r['recommendation_maturity'],'final_confidence':r['final_confidence'],'step13_dependency_required':r['step13_dependency_required'],'step13_candidate_pair_ids':r['step13_candidate_pair_ids'],'mapping_origin':'STEP12_SECOND_AUDIT_CURRENT_V3'})

# Five former proposed-page concepts, now explicitly withdrawn/reused.
concept_rows=[
{'former_concept':'PANORAMIC_WINDOWS_COMMERCIAL','former_proposed_page':'PROPOSED_NEW:/panoramnye-okna/','second_audit_verdict':'WITHDRAW_CREATE_REUSE_EXISTING','current_primary':'https://okno-msk.ru/okna-rehau/panoramnoe-osteklenie/','reason':'Exact current commercial panoramic landing exists.'},
{'former_concept':'WINDOW_HARDWARE_GUIDE','former_proposed_page':'PROPOSED_NEW:/stati/okonnaya-furnitura-vidy-brendy-kak-vybrat/','second_audit_verdict':'WITHDRAW_CREATE_EXPAND_EXISTING','current_primary':'https://okno-msk.ru/stati/kak-vybrat-plastikovye-okna/','reason':'Existing selection article already contains substantive hardware coverage; specialist pages exist.'},
{'former_concept':'PVC_WINDOW_INSTALLATION_DIY_GUIDE','former_proposed_page':'PROPOSED_NEW:/stati/ustanovka-plastikovyh-okon-svoimi-rukami/','second_audit_verdict':'WITHDRAW_NEUTRAL_DIY_CREATE_REUSE_SERVICE','current_primary':'https://okno-msk.ru/uslugi/ustanovka-okon/','reason':'Professional installation is a core paid offer and current site explicitly discourages self-installation.'},
{'former_concept':'PVC_WINDOW_REPAIR_DIY_GUIDE','former_proposed_page':'PROPOSED_NEW:/stati/remont-i-regulirovka-plastikovyh-okon-svoimi-rukami/','second_audit_verdict':'WITHDRAW_BROAD_CREATE_REUSE_SELF_HELP_AND_SERVICE','current_primary':'https://okno-msk.ru/stati/kak-otregulirovat-plastikovye-okna/ || https://okno-msk.ru/uslugi/remont-okon/','reason':'Current site already separates safe self-help from paid complex repair.'},
{'former_concept':'WINDOW_REPLACEMENT_SERVICE','former_proposed_page':'PROPOSED_NEW:/uslugi/zamena-okon/','second_audit_verdict':'WITHDRAW_CREATE_REUSE_EXPAND_EXISTING','current_primary':'https://okno-msk.ru/okna-rehau/po-tipu-doma/zamena-okon-v-kvartire/','reason':'Exact current commercial replacement landing exists.'},
]

# Delta against previously closed V2.
old={r['structural_unit_id']:r for r in oldv2}; delta=[]
for r in v3:
    o=old[r['structural_unit_id']]
    changed=[]
    for k in ['structural_action','primary_page_candidate','supporting_page','recommendation_maturity','final_confidence']:
        if o.get(k,'')!=r.get(k,''):changed.append(k)
    if changed:
        delta.append({'structural_unit_id':r['structural_unit_id'],'changed_fields':';'.join(changed),'old_action':o.get('structural_action',''),'new_action':r['structural_action'],'old_primary':o.get('primary_page_candidate',''),'new_primary':r['primary_page_candidate'],'old_supporting':o.get('supporting_page',''),'new_supporting':r['supporting_page'],'old_maturity':o.get('recommendation_maturity',''),'new_maturity':r['recommendation_maturity'],'old_confidence':o.get('final_confidence',''),'new_confidence':r['final_confidence']})

write(OUT,v3);write(OUT_PAIRS,pair_rows,list(pair_rows[0].keys()) if pair_rows else ['pair_id']);write(OUT_DEP,deps);write(OUT_MAP,phrase_rows);write(OUT_DELTA,delta,list(delta[0].keys()) if delta else ['structural_unit_id']);write(OUT_CONCEPTS,concept_rows)

old_actions=Counter(r['structural_action'] for r in oldv2);new_actions=Counter(r['structural_action'] for r in v3)
qa={
 'status':'STEP12_SECOND_AUDIT_V3_CANDIDATE_READY_FOR_INDEPENDENT_QA',
 'source_action_rows':len(v1),'final_action_rows':len(v3),'assignment_rows':len(assign),'phrase_map_rows':len(phrase_rows),
 'assigned_rows':sum(bool(a.get('final_structural_unit_id','').strip()) for a in assign),'unresolved_rows':sum(not bool(a.get('final_structural_unit_id','').strip()) for a in assign),
 'second_audit_correction_rows':len(corr),'freshness_concepts':len(fresh),'former_new_page_concepts':len(concept_rows),
 'new_commercial_page_rows':sum(r['structural_action']=='NEW_COMMERCIAL_PAGE' for r in v3),'new_informational_page_rows':sum(r['structural_action']=='NEW_INFORMATIONAL_PAGE' for r in v3),
 'proposed_new_reference_rows':sum('PROPOSED_NEW:' in (r['primary_page_candidate']+' '+r['supporting_page']) for r in v3),
 'rows_without_owner_goal_fields':sum(not all(r[k] for k in ['owner_goal_evidence_state','owner_primary_goal','desired_user_outcome','business_potential','content_role','fresh_site_check_status','existing_content_reuse']) for r in v3),
 'candidate_pairs_current':len(pair_rows),'pairs_requiring_future_step13_search':sum(p['later_direct_search_check_needed']=='true' for p in pair_rows),'step13_dependency_units':sum(r['step13_dependency_required']=='true' for r in v3),
 'dependency_high_rows':sum(r['step13_dependency_required']=='true' and r['final_confidence']=='HIGH' for r in v3),'dependency_final_rows':sum(r['step13_dependency_required']=='true' and r['recommendation_maturity']=='FINAL_WITHIN_STEP12_EVIDENCE' for r in v3),
 'changed_structural_units_vs_previous_v2':len(delta),
 'action_changed_units':sum('structural_action' in d['changed_fields'].split(';') for d in delta),
 'primary_target_changed_units':sum('primary_page_candidate' in d['changed_fields'].split(';') for d in delta),
 'supporting_target_changed_units':sum('supporting_page' in d['changed_fields'].split(';') for d in delta),
 'maturity_changed_units':sum('recommendation_maturity' in d['changed_fields'].split(';') for d in delta),
 'confidence_changed_units':sum('final_confidence' in d['changed_fields'].split(';') for d in delta),
 'previous_unique_proposed_pages':5,'current_unique_proposed_pages':0,'previous_candidate_pairs':189,
 'old_action_counts':dict(sorted(old_actions.items())),'new_action_counts':dict(sorted(new_actions.items())),
 'defects_closed_by_generator_alone':[], 'step13_executed':False,
}
if not (len(v3)==160 and len(assign)==len(phrase_rows)==2332 and qa['assigned_rows']==2313 and qa['unresolved_rows']==19 and qa['second_audit_correction_rows']==14 and qa['freshness_concepts']==5 and qa['former_new_page_concepts']==5 and qa['new_commercial_page_rows']==0 and qa['new_informational_page_rows']==0 and qa['proposed_new_reference_rows']==0 and qa['rows_without_owner_goal_fields']==0 and qa['dependency_high_rows']==0 and qa['dependency_final_rows']==0):qa['status']='FAIL'
OUT_QA.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False,indent=2))
