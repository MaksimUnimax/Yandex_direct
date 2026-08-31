import csv, json, re
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from urllib.parse import urlsplit

R=Path(__file__).resolve().parent
V3=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V3.tsv'
ASSIGN=R/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv'
HIST=R/'STEP_12_STRUCTURAL_ACTIONS.tsv'
DEC=R/'STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv'
CORR=R/'STEP_12_POST_CLOSE_CURRENT_SITE_BUSINESS_CORRECTIONS.tsv'
OUT=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V4.tsv'
OUT_MAP=R/'STEP_12_PHRASE_ACTION_MAP_FINAL_V4.tsv'
OUT_LINKS=R/'STEP_12_INTERNAL_LINK_ACTIONS.tsv'
OUT_PAIRS=R/'STEP_12_STEP13_CANDIDATE_PAIRS_V4.tsv'
OUT_QA=R/'STEP_12_THIRD_AUDIT_GENERATOR_QA.json'


def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(p,rows,fields=None):
    if fields is None: fields=list(rows[0].keys()) if rows else []
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
def qnorm(s):return re.sub(r'\s+',' ',(s or '').strip().lower())
def norm_url(v):
    v=(v or '').strip()
    if not v:return ''
    if v.startswith('PROPOSED_NEW:'):
        x=v.split(':',1)[1].strip();x=x if x.startswith('/') else '/'+x
        v='https://okno-msk.ru'+x
    if not v.startswith(('http://','https://')):return ''
    p=urlsplit(v); path=p.path or '/'; path=path.rstrip('/') or '/'
    return f'https://{p.netloc.lower().removeprefix("www.")}{path}'
def target_domain(domain):
    d=(domain or '').strip().lower().removeprefix('www.')
    return d=='okno-msk.ru' or d.endswith('.okno-msk.ru')
def clusters(v):return [x.strip() for x in (v or '').split(';') if x.strip()]
def parent_child(a,b):
    pa,pb=urlsplit(a),urlsplit(b)
    if pa.netloc.lower().removeprefix('www.')!=pb.netloc.lower().removeprefix('www.'):return False
    aa=pa.path.rstrip('/')+'/';bb=pb.path.rstrip('/')+'/'
    return aa!=bb and (aa.startswith(bb) or bb.startswith(aa))

v3=read(V3);assign=read(ASSIGN);hist=read(HIST);dec=read(DEC);corr=read(CORR)
assert len(v3)==160 and len(assign)==2332 and len(dec)==75
corr_by={r['structural_unit_id']:r for r in corr}

members=defaultdict(list);source_uids=defaultdict(set)
for a in assign:
    uid=(a.get('final_structural_unit_id') or '').strip()
    if uid:
        members[uid].append(a['phrase'])
        src=(a.get('original_effective_cluster_id') or '').strip()
        if src:source_uids[src].add(uid)

dec_by={qnorm(r['query']):r for r in dec}
# Materialize every persisted Step-9 result row. The first tranche is in STEP_09_SERP_RESULTS.tsv;
# the remaining projection is split across R2 raw parts.
raw_by=defaultdict(list)
raw_files=[R/'STEP_09_SERP_RESULTS.tsv']+sorted(R.glob('STEP_09_SERP_R2_PROJECTION_RAW_PART_*.tsv'))
for p in raw_files:
    if not p.exists():continue
    for r in read(p):
        q=qnorm(r.get('query_text') or r.get('query'))
        if q:raw_by[q].append(r)

# Third-audit evidence overlay.
v4=[]
for src in v3:
    r=dict(src);uid=r['structural_unit_id'];action=r['structural_action']
    # D12-21: diagnose gap before prescribing action.
    if action in {'EXPAND_EXISTING_PAGE','ADD_SECTION_OR_FAQ_TO_EXISTING'}:
        gap='QUALITY_GAP';gap_ev='Current owner/path is retained but the accepted structural action requires materially fuller same-task coverage on that current page.'
    elif action=='DEFER_PENDING_EVIDENCE':
        gap='EVIDENCE_INSUFFICIENT';gap_ev='A material evidence or owner-policy boundary remains unresolved; no content/page gap is asserted beyond the evidence.'
    else:
        gap='NONE'
        if action=='ROUTE_TO_EXISTING_PAGE_AS_SUBTASK':gap_ev='A current specialist/owner page exists; the task is routing/relationship implementation rather than a missing-content topic gap.'
        elif action=='KEEP_EXISTING_STRUCTURE':gap_ev='The current URL remains the structural owner; this does not assert that page performance/content optimization is complete.'
        elif action=='NO_STANDALONE_PAGE':gap_ev='No separate URL is justified for this structural unit under current evidence.'
        elif action=='OUTSIDE_SCOPE_NO_ACTION':gap_ev='The unit is outside the implementation scope; no first-party content gap is asserted.'
        else:gap_ev='No standalone content-gap diagnosis is required by the current structural action.'
    r['gap_type']=gap;r['gap_evidence']=gap_ev

    # D12-22: structural ownership is not a page-performance verdict.
    r['performance_evidence_state']='NOT_AVAILABLE_IN_BASE_SCOPE_NO_WEBMASTER_METRIKA'
    if action=='KEEP_EXISTING_STRUCTURE':opt='STRUCTURAL_OWNER_CONFIRMED__CONTENT_PERFORMANCE_NOT_ASSESSED'
    elif action in {'EXPAND_EXISTING_PAGE','ADD_SECTION_OR_FAQ_TO_EXISTING'}:opt='CONTENT_GAP_ACTION_READY__ACCOUNT_PERFORMANCE_NOT_ASSESSED'
    elif action=='ROUTE_TO_EXISTING_PAGE_AS_SUBTASK':opt='STRUCTURAL_ROUTING_READY__TARGET_PERFORMANCE_NOT_ASSESSED'
    elif action=='DEFER_PENDING_EVIDENCE':opt='DEFERRED_PENDING_MISSING_EVIDENCE'
    else:opt='NOT_APPLICABLE_TO_PAGE_PERFORMANCE_DECISION'
    r['optimization_readiness']=opt

    # D12-23/24: join only persisted direct Search evidence.
    dqs=[];observed_urls=set();types=set();jobs=set()
    for ph in members.get(uid,[]):
        q=qnorm(ph)
        if q not in dec_by:continue
        dqs.append(ph)
        d=dec_by[q]
        if d.get('dominant_result_type'):types.add(d['dominant_result_type'].strip())
        if d.get('observed_serp_job'):jobs.add(d['observed_serp_job'].strip())
        for hit in raw_by.get(q,[]):
            if target_domain(hit.get('domain','')):
                u=norm_url(hit.get('url',''))
                if u:observed_urls.add(u)
    intended=norm_url(r.get('primary_page_candidate',''))
    if not intended:
        match='NOT_APPLICABLE_NO_INTENDED_TARGET'
    elif not dqs:
        match='NOT_DIRECTLY_CHECKED'
    elif not observed_urls:
        match='SITE_NOT_OBSERVED'
    elif intended in observed_urls:
        match='MATCH'
    else:
        match='MISMATCH'
    r['intended_target_url']=intended
    r['current_yandex_relevant_url']=';'.join(sorted(observed_urls))
    r['relevant_url_match_state']=match
    r['direct_serp_queries']=';'.join(sorted(set(dqs)))
    r['serp_observed_user_job']=';'.join(sorted(jobs)) if jobs else ('NOT_DIRECTLY_CHECKED' if not dqs else 'NOT_SEPARATELY_OBSERVED')
    r['serp_expected_content_type']=';'.join(sorted(types)) if types else ('NOT_DIRECTLY_CHECKED' if not dqs else 'NOT_SEPARATELY_OBSERVED_IN_PERSISTED_EVIDENCE')
    r['serp_expected_format']='NOT_DIRECTLY_CHECKED' if not dqs else 'NOT_SEPARATELY_OBSERVED_IN_PERSISTED_STEP09'
    r['serp_expected_angle']='NOT_DIRECTLY_CHECKED' if not dqs else 'NOT_SEPARATELY_OBSERVED_IN_PERSISTED_STEP09'
    r['serp_format_evidence_state']='NOT_DIRECTLY_CHECKED' if not dqs else 'DIRECT_STEP09_QUERY_EVIDENCE__FORMAT_AND_ANGLE_NOT_SEPARATELY_RECORDED'

    # D12-25: label evidence source and policy materiality; do not present inference as client instruction.
    if action=='OUTSIDE_SCOPE_NO_ACTION':source='NOT_APPLICABLE'
    elif uid in corr_by:source='PUBLIC_SITE_EXPLICIT'
    elif (r.get('owner_goal_evidence_state') or '').startswith('PUBLIC_'):source='PUBLIC_SITE_INFERRED'
    else:source='UNKNOWN'
    counter=(r.get('counterproductive_to_core_offer') or '').upper();bp=(r.get('business_potential') or '').upper();intent=(r.get('intent_type') or '').upper()
    if action in {'OUTSIDE_SCOPE_NO_ACTION','NO_STANDALONE_PAGE'}:materiality='NOT_APPLICABLE'
    elif 'YES' in counter or 'NEGATIVE' in bp:materiality='HIGH'
    elif 'INFO' in intent or 'DIY' in intent:materiality='MEDIUM'
    else:materiality='LOW'
    r['owner_goal_evidence_source']=source
    r['owner_policy_materiality']=materiality
    r['owner_goal_evidence_note']='Client/internal analytics/sales-support evidence is not available in the base public-site scope; public-site inference/explicit evidence is labelled accordingly.'
    v4.append(r)

by={r['structural_unit_id']:r for r in v4}
# No third-audit CREATE survives without TOPIC_GAP; current job has no CREATE.
assert not [r for r in v4 if r['structural_action'] in {'NEW_COMMERCIAL_PAGE','NEW_INFORMATIONAL_PAGE'}]
assert not [r for r in v4 if 'PROPOSED_NEW:' in ((r.get('primary_page_candidate') or '')+' '+(r.get('supporting_page') or ''))]

# D12-26: materialize existing-page internal-link implementation or explicit NA/defer.
link_rows=[];material_actions={'ROUTE_TO_EXISTING_PAGE_AS_SUBTASK','ADD_SECTION_OR_FAQ_TO_EXISTING','EXPAND_EXISTING_PAGE'}
for r in v4:
    if r['structural_action'] not in material_actions:continue
    uid=r['structural_unit_id'];primary=norm_url(r.get('primary_page_candidate'));support=norm_url(r.get('supporting_page'))
    if r['structural_action']=='ROUTE_TO_EXISTING_PAGE_AS_SUBTASK':
        if support and primary and support!=primary:
            state='IMPLEMENT';source=support;target=primary;rel='SUPPORTING_CONTEXT_TO_EXACT_OWNER';purpose='Move the user from broader/supporting context to the exact current owner for this task.'
        else:
            state='NOT_APPLICABLE_NO_DISTINCT_SOURCE_CONTEXT';source='';target=primary;rel='ROUTING_TARGET_ONLY';purpose='The target owner is explicit, but no distinct current source page is evidenced for an additional internal-link instruction.'
    else:
        if primary and support and primary!=support:
            state='IMPLEMENT';source=primary;target=support;rel='PRIMARY_TO_SUPPORTING_SPECIALIST_OR_HANDOFF';purpose='Connect the expanded/section content to the relevant specialist, product or service handoff.'
        else:
            state='NOT_APPLICABLE_NO_DISTINCT_TARGET';source=primary;target='';rel='ON_PAGE_CONTENT_ACTION_ONLY';purpose='The action is implemented on the current primary page and no distinct supporting target is evidenced.'
    link_rows.append({
      'link_action_id':f'IL{len(link_rows)+1:04d}','structural_unit_id':uid,'structural_action':r['structural_action'],'link_action_state':state,
      'source_url':source,'target_url':target,'relation_type':rel,'placement_context':f"Contextual implementation around: {r['user_task']}",
      'anchor_concept':r['user_task'],'user_journey_purpose':purpose,'business_handoff':r.get('desired_user_outcome',''),
      'evidence_origin':'STEP12_V4_PRIMARY_SUPPORTING_RELATION_AND_CURRENT_ACTION__NO_LITERAL_ANCHOR_TEXT_PRESCRIBED'})

# Rebuild current pair universe, adding intended-vs-observed mismatch edges if any.
page_uids=defaultdict(set)
for uid,r in by.items():
    p=norm_url(r.get('primary_page_candidate'))
    if p:page_uids[p].add(uid)
hist_follow={r['cluster_id']:(r.get('step13_followup_required','').strip().lower()=='true') for r in hist}
pairs={}
def add_pair(a,b,route,units=None,srcs=None):
    a,b=norm_url(a),norm_url(b)
    if not a or not b or a==b:return
    k=tuple(sorted((a,b)));x=pairs.setdefault(k,{'routes':set(),'units':set(),'clusters':set()})
    x['routes'].add(route);x['units'].update(units or []);x['clusters'].update(srcs or [])
for uid,r in by.items():
    a,b=norm_url(r.get('primary_page_candidate')),norm_url(r.get('supporting_page'))
    if a and b and a!=b:add_pair(a,b,'EXPLICIT_PRIMARY_SUPPORTING_EDGE',{uid}|page_uids.get(b,set()),clusters(r.get('source_effective_clusters')))
    if r['relevant_url_match_state']=='MISMATCH':
        for obs in [x for x in r['current_yandex_relevant_url'].split(';') if x]:add_pair(a,obs,'TARGET_VS_OBSERVED_YANDEX_RELEVANT_MISMATCH',{uid},clusters(r.get('source_effective_clusters')))
for src,uids in source_uids.items():
    pu=defaultdict(set)
    for uid in uids:
        p=norm_url(by[uid].get('primary_page_candidate'))
        if p:pu[p].add(uid)
    for a,b in combinations(sorted(pu),2):add_pair(a,b,'SHARED_SOURCE_CLUSTER_PRIMARY_DESTINATIONS',pu[a]|pu[b],{src})

pair_rows=[]
for i,((a,b),x) in enumerate(sorted(pairs.items()),1):
    reasons=set()
    if 'TARGET_VS_OBSERVED_YANDEX_RELEVANT_MISMATCH' in x['routes']:reasons.add('OBSERVED_TARGET_RELEVANT_URL_MISMATCH')
    if any(hist_follow.get(c,False) for c in x['clusters']):reasons.add('HISTORICAL_KNOWN_FOLLOWUP_SIGNAL_PRESERVED')
    for uid in x['units']:
        r=by[uid]
        if r.get('search_boundary_support')=='MATERIAL_BOUNDARY_GAP':reasons.add('MATERIAL_SEARCH_BOUNDARY_GAP_IN_CONTRIBUTING_UNIT')
        # Prior recommendation maturity is downstream state, not independent evidence; do not use it to trigger Step-13 search.
    if 'SHARED_SOURCE_CLUSTER_PRIMARY_DESTINATIONS' in x['routes'] and not parent_child(a,b):reasons.add('NON_HIERARCHICAL_MULTI_PRIMARY_ROUTE_FROM_SAME_SOURCE_CLUSTER')
    rel=sorted(x['units']);tasks=sorted({by[u]['user_task'] for u in rel})
    ev=[]
    for u in rel:
        ph=sorted(set(members.get(u,[])));ev.append(f"{u}[{len(ph)}]: {' | '.join(ph[:3])}")
    normal=[]
    if parent_child(a,b):normal.append('PARENT_CHILD_RELATION_CAN_BE_NORMAL_WHEN_TASK_BOUNDARIES_ARE_DISTINCT')
    if 'EXPLICIT_PRIMARY_SUPPORTING_EDGE' in x['routes']:normal.append('PRIMARY_SUPPORTING_JOURNEY_RELATION_CAN_BE_NORMAL')
    if 'SHARED_SOURCE_CLUSTER_PRIMARY_DESTINATIONS' in x['routes']:normal.append('SAME_UPSTREAM_FAMILY_CAN_NORMALLY_SPLIT_ACROSS_DISTINCT_USER_TASKS')
    pair_rows.append({'pair_id':f'V4P{i:04d}','page_a':a,'page_b':b,'derivation_routes':';'.join(sorted(x['routes'])),'source_effective_clusters':';'.join(sorted(x['clusters'])),'relation_structural_units':';'.join(rel),'member_evidence':' || '.join(ev),'adjacent_task':' || '.join(tasks),'normal_overlap_rationale':';'.join(normal),'later_direct_search_check_needed':'true' if reasons else 'false','search_check_reason':';'.join(sorted(reasons)) if reasons else 'NO_MATERIAL_DIRECT_SEARCH_TRIGGER_DERIVED_AT_STEP12','derivation_origin':'DETERMINISTIC_FROM_THIRD_AUDIT_CURRENT_ROUTING_GRAPH_V4'})

pair_ids=defaultdict(list);pair_reasons=defaultdict(set)
for p in pair_rows:
    if p['later_direct_search_check_needed']!='true':continue
    for uid in [x for x in p['relation_structural_units'].split(';') if x]:
        pair_ids[uid].append(p['pair_id']);pair_reasons[uid].update([x for x in p['search_check_reason'].split(';') if x])

# Recompute maturity only where the new evidence introduces a real material dependency.
for r in v4:
    uid=r['structural_unit_id'];action=r['structural_action'];dep=bool(pair_ids.get(uid))
    if action=='DEFER_PENDING_EVIDENCE':
        mat='DEFERRED_PENDING_MISSING_EVIDENCE';conf='LOW'
    elif r['owner_goal_evidence_source']=='UNKNOWN' and r['owner_policy_materiality']=='HIGH':
        mat='DEFERRED_PENDING_MISSING_EVIDENCE';conf='LOW'
    elif dep:
        mat='PROVISIONAL_PENDING_STEP13_CONFLICT_CHECK';conf='MEDIUM' if r['final_confidence']=='HIGH' else r['final_confidence']
    else:
        mat=r['recommendation_maturity'];conf=r['final_confidence']
    r['recommendation_maturity']=mat;r['final_confidence']=conf
    r['step13_dependency_required']='true' if dep else 'false';r['step13_candidate_pair_ids']=';'.join(sorted(pair_ids.get(uid,[])))
    extra=[]
    if dep:extra.append('Step-13 current-page pair check remains: '+';'.join(sorted(pair_ids[uid])))
    if r['relevant_url_match_state']=='MISMATCH':extra.append('Observed Yandex relevant URL differs from intended target.')
    if action=='KEEP_EXISTING_STRUCTURE':extra.append('KEEP is structural-only; account performance/content optimization was not assessed in base scope.')
    r['third_audit_evidence_note']=' '.join(extra) if extra else 'Third-audit evidence fields materialized; no additional structural downgrade introduced.'

# Final phrase-level V4 map.
v4by={r['structural_unit_id']:r for r in v4};phrase_rows=[]
for a in assign:
    uid=(a.get('final_structural_unit_id') or '').strip()
    if not uid:
        phrase_rows.append({'phrase':a['phrase'],'final_structural_unit_id':'','structural_action':'DEFER_UNRESOLVED','primary_page_candidate':'','gap_type':'EVIDENCE_INSUFFICIENT','optimization_readiness':'DEFERRED_PENDING_MISSING_EVIDENCE','relevant_url_match_state':'NOT_APPLICABLE_NO_INTENDED_TARGET','owner_goal_evidence_source':'UNKNOWN','recommendation_maturity':'DEFERRED_PENDING_MISSING_EVIDENCE','final_confidence':'LOW','mapping_origin':'STEP12_THIRD_AUDIT_UNRESOLVED_PRESERVED'})
    else:
        r=v4by[uid]
        phrase_rows.append({'phrase':a['phrase'],'final_structural_unit_id':uid,'structural_action':r['structural_action'],'primary_page_candidate':r['primary_page_candidate'],'gap_type':r['gap_type'],'optimization_readiness':r['optimization_readiness'],'relevant_url_match_state':r['relevant_url_match_state'],'owner_goal_evidence_source':r['owner_goal_evidence_source'],'recommendation_maturity':r['recommendation_maturity'],'final_confidence':r['final_confidence'],'mapping_origin':'STEP12_THIRD_EXTERNAL_METHOD_AUDIT_V4'})

write(OUT,v4);write(OUT_MAP,phrase_rows);write(OUT_LINKS,link_rows);write(OUT_PAIRS,pair_rows)

qa={
 'date':'2026-08-31','status':'STEP12_THIRD_AUDIT_V4_CANDIDATE_READY_FOR_INDEPENDENT_QA','structural_units':len(v4),'assignment_rows':len(assign),'phrase_map_rows':len(phrase_rows),
 'gap_type_missing':sum(not r['gap_type'] for r in v4),'gap_type_counts':dict(Counter(r['gap_type'] for r in v4)),'create_rows':sum(r['structural_action'] in {'NEW_COMMERCIAL_PAGE','NEW_INFORMATIONAL_PAGE'} for r in v4),
 'performance_state_missing':sum(not r['performance_evidence_state'] for r in v4),'keep_rows':sum(r['structural_action']=='KEEP_EXISTING_STRUCTURE' for r in v4),'keep_claiming_no_optimization_needed':sum(r['structural_action']=='KEEP_EXISTING_STRUCTURE' and 'NOT_ASSESSED' not in r['optimization_readiness'] for r in v4),
 'relevant_match_state_missing':sum(not r['relevant_url_match_state'] for r in v4),'relevant_match_counts':dict(Counter(r['relevant_url_match_state'] for r in v4)),'direct_serp_units':sum(bool(r['direct_serp_queries']) for r in v4),
 'serp_format_state_missing':sum(not r['serp_format_evidence_state'] for r in v4),'owner_goal_source_missing':sum(not r['owner_goal_evidence_source'] for r in v4),'owner_goal_source_counts':dict(Counter(r['owner_goal_evidence_source'] for r in v4)),
 'policy_sensitive_unknown_final':sum(r['owner_goal_evidence_source']=='UNKNOWN' and r['owner_policy_materiality']=='HIGH' and r['recommendation_maturity']=='FINAL_WITHIN_STEP12_EVIDENCE' for r in v4),
 'material_link_units':sum(r['structural_action'] in material_actions for r in v4),'internal_link_rows':len(link_rows),'internal_link_implement':sum(r['link_action_state']=='IMPLEMENT' for r in link_rows),'internal_link_explicit_na_or_defer':sum(r['link_action_state']!='IMPLEMENT' for r in link_rows),'internal_link_proposed_refs':sum('PROPOSED_NEW:' in (r['source_url']+' '+r['target_url']) for r in link_rows),
 'candidate_pairs':len(pair_rows),'pairs_requiring_step13':sum(r['later_direct_search_check_needed']=='true' for r in pair_rows),'step13_dependency_units':sum(r['step13_dependency_required']=='true' for r in v4),
 'new_bridge_requests':0,'new_bridge_cost_rub':0.0,'step13_executed':False,'defects_closed_by_generator_alone':[]}
OUT_QA.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False,indent=2))
