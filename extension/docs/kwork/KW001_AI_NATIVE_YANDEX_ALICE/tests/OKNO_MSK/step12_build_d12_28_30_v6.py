import csv,json,itertools
from collections import defaultdict
from pathlib import Path

R=Path(__file__).resolve().parent
P_ASSIGN=R/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V6.tsv'
P_ACTION=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V5.tsv'
P_MAP=R/'STEP_12_PHRASE_ACTION_MAP_FINAL_V5.tsv'
P_LINK=R/'STEP_12_INTERNAL_LINK_ACTIONS_V5.tsv'
P_CONTENT=R/'STEP_12_D12_28_CURRENT_CONTENT_REVALIDATION.tsv'
P_RES=R/'STEP_12_D12_30_PHRASE_RESOLUTIONS.tsv'
P_NEW=R/'STEP_12_D12_30_NEW_UNIT_DEFINITIONS.tsv'
P_LVAL=R/'STEP_12_D12_29_CURRENT_LINK_VALIDATION.tsv'

O_ASSIGN=R/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V7.tsv'
O_ACTION=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv'
O_MAP=R/'STEP_12_PHRASE_ACTION_MAP_FINAL_V6.tsv'
O_LINK=R/'STEP_12_INTERNAL_LINK_ACTIONS_V6.tsv'
O_PAIR=R/'STEP_12_STEP13_CANDIDATE_PAIRS_V6.tsv'
O_QA=R/'STEP_12_D12_28_30_BUILD_QA.json'

def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def header(p):
    with p.open(encoding='utf-8',newline='') as f:return next(csv.reader(f,delimiter='\t'))
def write(p,rows,fields):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n',extrasaction='ignore');w.writeheader();w.writerows(rows)
def norm(u):
    u=(u or '').strip()
    if u and u!='https://okno-msk.ru/':u=u.rstrip('/')
    return u

def bools(v):return str(v).strip().lower()=='true'

assign=read(P_ASSIGN); actions=read(P_ACTION); oldmap=read(P_MAP); oldlinks=read(P_LINK)
content=read(P_CONTENT); resolutions=read(P_RES); newdefs=read(P_NEW); lvals=read(P_LVAL)
assert len(assign)==2332
assert len(actions)==160
assert len(content)==20
assert len(resolutions)==49
assert len(lvals)==28

# Apply exact phrase resolutions. Action is never used as evidence for a move.
by_phrase=defaultdict(list)
for i,r in enumerate(assign):by_phrase[r.get('phrase','')].append(i)
seen=[]
for rr in resolutions:
    hits=[i for i in by_phrase[rr['phrase']] if assign[i].get('final_structural_unit_id','')==rr['old_structural_unit_id']]
    assert len(hits)==1,(rr,hits)
    i=hits[0]
    assign[i]['final_structural_unit_id']=rr['corrected_structural_unit_id']
    assign[i]['assignment_origin']='D12_30_FULL_MEMBER_REVALIDATION'
    assign[i]['correction_reason']=rr['decision_reason']
    seen.append(rr['phrase'])
assert len(set(seen))==49

# Final membership accounting.
members=defaultdict(list); source_clusters=defaultdict(set)
for r in assign:
    uid=(r.get('final_structural_unit_id') or '').strip()
    if uid:
        members[uid].append(r['phrase'])
        c=(r.get('original_effective_cluster_id') or '').strip()
        if c:source_clusters[uid].add(c)
assert sum(len(v) for v in members.values())==2313
assert len({r['phrase'] for r in assign})==2332

old_actions={r['structural_unit_id']:dict(r) for r in actions}
afields=header(P_ACTION)
extra_fields=['structural_gap_state','content_enhancement_state','current_content_read_date','current_content_evidence','explicit_missing_needs','coherence_verdict','structural_owner_decision','d12_28_30_origin']
for f in extra_fields:
    if f not in afields:afields.append(f)

# Backfill separated gap states for unaffected historical rows without strengthening them.
for r in old_actions.values():
    g=r.get('gap_type','NONE')
    if g=='TOPIC_GAP':sg,cg='TOPIC_GAP','NONE'
    elif g=='INTENT_GAP':sg,cg='INTENT_GAP','NONE'
    elif g=='QUALITY_GAP':sg,cg='NONE','QUALITY_GAP'
    elif g=='ORIGINALITY_GAP':sg,cg='NONE','ORIGINALITY_GAP'
    elif g=='MIXED_GAP':sg,cg='MIXED_STRUCTURAL_GAP','CONTENT_EVIDENCE_INSUFFICIENT'
    elif g=='EVIDENCE_INSUFFICIENT':sg,cg='STRUCTURAL_EVIDENCE_INSUFFICIENT','CONTENT_EVIDENCE_INSUFFICIENT'
    else:sg,cg='NONE','NONE'
    r['structural_gap_state']=sg;r['content_enhancement_state']=cg
    r['current_content_read_date']='';r['current_content_evidence']='';r['explicit_missing_needs']=''
    r['coherence_verdict']='PREVIOUSLY_ACCEPTED_UNAFFECTED'
    r['structural_owner_decision']='KEEP_STRUCTURAL_OWNER' if r.get('structural_action')=='KEEP_EXISTING_STRUCTURE' else r.get('structural_action','')
    r['d12_28_30_origin']='LEGACY_V5_UNAFFECTED_BY_POST_PASS_CLASS'

content_by={r['structural_unit_id']:r for r in content}
map_action={'KEEP_STRUCTURAL_OWNER':'KEEP_EXISTING_STRUCTURE','ADD_SECTION_OR_FAQ_TO_EXISTING':'ADD_SECTION_OR_FAQ_TO_EXISTING','EXPAND_EXISTING_PAGE':'EXPAND_EXISTING_PAGE','NO_STANDALONE_PAGE':'NO_STANDALONE_PAGE','DEFER_PENDING_EVIDENCE':'DEFER_PENDING_EVIDENCE'}
removed=set()
for uid,c in content_by.items():
    assert uid in old_actions
    if c['content_action_resolution']=='SUPERSEDED_ZERO_MEMBER_AFTER_RECLASSIFICATION':
        assert len(members.get(uid,[]))==0,(uid,len(members.get(uid,[])))
        removed.add(uid);continue
    r=old_actions[uid]
    act=map_action[c['content_action_resolution']]
    r['structural_action']=act
    r['structural_owner_decision']=c['structural_owner_decision']
    r['structural_gap_state']=c['structural_gap_state']
    r['content_enhancement_state']=c['content_enhancement_state']
    r['current_content_read_date']=c['current_page_read_date']
    r['current_content_evidence']=c['current_page_evidence']
    r['explicit_missing_needs']=c['explicit_missing_needs']
    r['coherence_verdict']=c['coherence_verdict']
    r['d12_28_30_origin']='D12_28_CURRENT_CONTENT_PLUS_D12_30_FULL_MEMBER_REVIEW'
    if c['content_enhancement_state']=='QUALITY_GAP':legacy_gap='QUALITY_GAP'
    elif 'INSUFFICIENT' in c['structural_gap_state'] or 'INSUFFICIENT' in c['content_enhancement_state']:legacy_gap='EVIDENCE_INSUFFICIENT'
    elif c['structural_gap_state']=='INTENT_GAP':legacy_gap='INTENT_GAP'
    elif c['structural_gap_state']=='TOPIC_GAP':legacy_gap='TOPIC_GAP'
    elif c['structural_gap_state']=='MIXED_STRUCTURAL_GAP':legacy_gap='MIXED_GAP'
    else:legacy_gap='NONE'
    r['gap_type']=legacy_gap
    miss=c['explicit_missing_needs'].strip()
    r['gap_evidence']=(('Current-page read 2026-08-31 independently observed missing need(s): '+miss) if miss else c['resolution_rationale'])
    r['fresh_site_check_status']='CURRENT_FIRST_PARTY_PAGE_RECHECK_2026_08_31'
    r['current_page_fit']='STRONG_EXISTING_PAGE_FIT' if act=='KEEP_EXISTING_STRUCTURE' else ('PARTIAL_EXISTING_PAGE_FIT' if act in {'EXPAND_EXISTING_PAGE','ADD_SECTION_OR_FAQ_TO_EXISTING'} else 'NOT_APPLICABLE')
    if act=='KEEP_EXISTING_STRUCTURE':r['optimization_readiness']='STRUCTURAL_OWNER_CONFIRMED__CONTENT_PERFORMANCE_NOT_ASSESSED'
    elif act in {'EXPAND_EXISTING_PAGE','ADD_SECTION_OR_FAQ_TO_EXISTING'}:r['optimization_readiness']='CONTENT_GAP_ACTION_READY__ACCOUNT_PERFORMANCE_NOT_ASSESSED'
    elif act=='DEFER_PENDING_EVIDENCE':r['optimization_readiness']='DEFERRED_PENDING_MISSING_EVIDENCE'
    else:r['optimization_readiness']='NOT_APPLICABLE_TO_PAGE_PERFORMANCE_DECISION'
    if act=='DEFER_PENDING_EVIDENCE':
        r['recommendation_maturity']='DEFERRED_PENDING_MISSING_EVIDENCE';r['final_confidence']='LOW'
    elif c['content_enhancement_state']=='QUALITY_GAP':
        r['recommendation_maturity']='FINAL_WITHIN_STEP12_EVIDENCE';r['final_confidence']='MEDIUM'
    else:
        r['recommendation_maturity']='FINAL_WITHIN_STEP12_EVIDENCE';r['final_confidence']='HIGH' if c['coherence_verdict']=='STRONG' else 'MEDIUM'
    r['confidence_downgrade_reason']=c['resolution_rationale'] if r['final_confidence']!='HIGH' else 'Current first-party content independently supports the structural owner; account performance remains outside base scope.'
    r['confidence_origin']='D12_28_D12_30_INDEPENDENT_CURRENT_CONTENT'
    r['maturity_origin']='D12_28_D12_30_INDEPENDENT_CURRENT_CONTENT'
    r['confidence_reason_origin']='D12_28_D12_30_INDEPENDENT_CURRENT_CONTENT'
    r['second_audit_correction_origin']='D12_28_D12_30_POST_PASS_REVALIDATION'
    r['third_audit_evidence_note']='Post-PASS revalidated from current page content without using old action as evidence.'

for uid in removed:old_actions.pop(uid,None)

# Materialize explicit new units produced by full-member review.
for d in newdefs:
    uid=d['structural_unit_id'];assert uid not in old_actions
    r={f:'' for f in afields}
    for k,v in d.items():
        if k in r:r[k]=v
    r['structural_unit_id']=uid
    r['historical_action_mix']='D12_30_NEW_EXPLICIT_UNIT'
    r['confidence_origin']='D12_30_FULL_MEMBER_REVALIDATION'
    r['owner_goal_evidence_state']=d.get('owner_goal_evidence_source','UNKNOWN')
    r['second_audit_correction_origin']='D12_30_FULL_MEMBER_REVALIDATION'
    r['maturity_origin']='D12_30_FULL_MEMBER_REVALIDATION'
    r['confidence_reason_origin']='D12_30_FULL_MEMBER_REVALIDATION'
    r['structural_owner_decision']='KEEP_STRUCTURAL_OWNER' if d['structural_action']=='KEEP_EXISTING_STRUCTURE' else d['structural_action']
    r['current_content_read_date']='2026-08-31' if 'CURRENT_FIRST_PARTY' in d.get('fresh_site_check_status','') else ''
    r['current_content_evidence']=d['gap_evidence']
    r['explicit_missing_needs']=''
    r['coherence_verdict']='STRONG' if d['task_coherence']=='STRONG' else d['task_coherence']
    r['d12_28_30_origin']='D12_30_NEW_UNIT_FROM_FULL_MEMBER_REVIEW'
    r['intended_target_url']=norm(d.get('primary_page_candidate',''))
    r['current_yandex_relevant_url']=''
    r['relevant_url_match_state']='NOT_DIRECTLY_CHECKED' if r['intended_target_url'] else 'NOT_APPLICABLE_NO_INTENDED_TARGET'
    r['direct_serp_queries']='';r['serp_observed_user_job']='NOT_DIRECTLY_CHECKED';r['serp_expected_content_type']='NOT_DIRECTLY_CHECKED';r['serp_expected_format']='NOT_DIRECTLY_CHECKED';r['serp_expected_angle']='NOT_DIRECTLY_CHECKED';r['serp_format_evidence_state']='NOT_DIRECTLY_CHECKED'
    r['owner_goal_evidence_note']='Current public evidence only; missing owner/business evidence remains explicit where material.'
    r['third_audit_evidence_note']='Created only after D12-30 exact member-phrase revalidation; no new URL is implied.'
    old_actions[uid]=r

# Update counts and cluster provenance from final assignment ledger; forbid orphan/zero active actions.
for uid,r in old_actions.items():
    r['phrase_count']=str(len(members.get(uid,[])))
    r['source_effective_clusters']=';'.join(sorted(source_clusters.get(uid,set())))
zero=[uid for uid,r in old_actions.items() if int(r['phrase_count'])==0]
assert not zero,zero
missing_actions=sorted(set(members)-set(old_actions))
assert not missing_actions,missing_actions

# Build pair universe independently from current final routing graph (candidate universe, no harm verdict).
pairdata={}
def addpair(a,b,route,cluster='',units=()):
    a,b=norm(a),norm(b)
    if not a or not b or a==b:return
    key=tuple(sorted((a,b)))
    p=pairdata.setdefault(key,{'routes':set(),'clusters':set(),'units':set()})
    p['routes'].add(route)
    if cluster:p['clusters'].add(cluster)
    p['units'].update(u for u in units if u)

for uid,r in old_actions.items():
    p,s=norm(r.get('primary_page_candidate','')),norm(r.get('supporting_page',''))
    if p and s and p!=s:addpair(p,s,'EXPLICIT_PRIMARY_SUPPORTING_EDGE',units=(uid,))
clusters=defaultdict(lambda:defaultdict(set))
for ar in assign:
    uid=ar.get('final_structural_unit_id','');c=ar.get('original_effective_cluster_id','')
    if uid and c and uid in old_actions:
        p=norm(old_actions[uid].get('primary_page_candidate',''))
        if p:clusters[c][p].add(uid)
for c,pages in clusters.items():
    if len(pages)>1:
        for a,b in itertools.combinations(sorted(pages),2):addpair(a,b,'SHARED_SOURCE_CLUSTER_PRIMARY_DESTINATIONS',cluster=c,units=pages[a]|pages[b])

oldpair_by_key={}
try:
    for p in read(R/'STEP_12_STEP13_CANDIDATE_PAIRS_V5.tsv'):
        oldpair_by_key[tuple(sorted((norm(p['page_a']),norm(p['page_b']))))]=p
except FileNotFoundError:pass

pair_rows=[]
for n,(key,p) in enumerate(sorted(pairdata.items()),1):
    a,b=key;units=sorted(p['units']);routes=sorted(p['routes']);cl=sorted(p['clusters'])
    evidence=[];tasks=[]
    for uid in units:
        ph=sorted(members.get(uid,[])); evidence.append(f"{uid}[{len(ph)}]: {' | '.join(ph[:3])}")
        t=old_actions[uid].get('user_task','')
        if t:tasks.append(t)
    parent_child=a.startswith(b.rstrip('/')+'/') or b.startswith(a.rstrip('/')+'/')
    normal=[]
    if parent_child:normal.append('PARENT_CHILD_RELATION_CAN_BE_NORMAL_WHEN_TASK_BOUNDARIES_ARE_DISTINCT')
    if 'EXPLICIT_PRIMARY_SUPPORTING_EDGE' in routes:normal.append('PRIMARY_SUPPORTING_JOURNEY_RELATION_CAN_BE_NORMAL')
    if 'SHARED_SOURCE_CLUSTER_PRIMARY_DESTINATIONS' in routes:normal.append('SAME_UPSTREAM_FAMILY_CAN_NORMALLY_SPLIT_ACROSS_DISTINCT_USER_TASKS')
    old=oldpair_by_key.get(key,{})
    need=('SHARED_SOURCE_CLUSTER_PRIMARY_DESTINATIONS' in routes) or old.get('later_direct_search_check_needed','').lower()=='true'
    reasons=[]
    if old.get('later_direct_search_check_needed','').lower()=='true':reasons.append('HISTORICAL_KNOWN_FOLLOWUP_SIGNAL_PRESERVED')
    if 'SHARED_SOURCE_CLUSTER_PRIMARY_DESTINATIONS' in routes:reasons.append('NON_HIERARCHICAL_MULTI_PRIMARY_ROUTE_FROM_SAME_SOURCE_CLUSTER')
    if not reasons:reasons.append('NO_MATERIAL_DIRECT_SEARCH_TRIGGER_DERIVED_AT_STEP12')
    pair_rows.append({'pair_id':f'V6P{n:04d}','page_a':a,'page_b':b,'derivation_routes':';'.join(routes),'source_effective_clusters':';'.join(cl),'relation_structural_units':';'.join(units),'member_evidence':' || '.join(evidence),'adjacent_task':' || '.join(sorted(set(tasks))),'normal_overlap_rationale':';'.join(normal),'later_direct_search_check_needed':str(need).lower(),'search_check_reason':';'.join(reasons),'derivation_origin':'D12_28_D12_30_CORRECTED_ROUTING_GRAPH_V6'})

# Pair dependency overlay after pair derivation.
unit_pairs=defaultdict(list);unit_required=defaultdict(list)
for p in pair_rows:
    for uid in p['relation_structural_units'].split(';') if p['relation_structural_units'] else []:
        unit_pairs[uid].append(p['pair_id'])
        if p['later_direct_search_check_needed']=='true':unit_required[uid].append(p['pair_id'])
for uid,r in old_actions.items():
    r['step13_candidate_pair_ids']=';'.join(unit_pairs.get(uid,[]))
    dep=bool(unit_required.get(uid))
    r['step13_dependency_required']=str(dep).lower()
    if dep and r['structural_action']!='DEFER_PENDING_EVIDENCE':
        r['recommendation_maturity']='PROVISIONAL_PENDING_STEP13_CONFLICT_CHECK'
        if r.get('final_confidence')=='HIGH':r['final_confidence']='MEDIUM'
        r['maturity_dependency_detail']='Step-13 current-page pair check remains: '+';'.join(unit_required[uid])
    elif r['structural_action']=='DEFER_PENDING_EVIDENCE':
        r['maturity_dependency_detail']='NON_STEP13_EVIDENCE_OR_POLICY_GAP_REMAINS'
    else:r['maturity_dependency_detail']='NONE'

# Build phrase map from final assignments/actions; preserve 19 unresolved rows exactly as unresolved.
old_map={r['phrase']:r for r in oldmap}
map_fields=header(P_MAP)
map_rows=[]
for ar in assign:
    ph=ar['phrase'];uid=ar.get('final_structural_unit_id','')
    if not uid:
        r=dict(old_map[ph]);r['mapping_origin']='STEP12_D12_28_30_UNRESOLVED_PRESERVED';map_rows.append(r);continue
    ac=old_actions[uid]
    map_rows.append({'phrase':ph,'final_structural_unit_id':uid,'structural_action':ac['structural_action'],'primary_page_candidate':ac.get('primary_page_candidate',''),'gap_type':ac.get('gap_type','NONE'),'optimization_readiness':ac.get('optimization_readiness',''),'relevant_url_match_state':ac.get('relevant_url_match_state',''),'owner_goal_evidence_source':ac.get('owner_goal_evidence_source',''),'recommendation_maturity':ac.get('recommendation_maturity',''),'final_confidence':ac.get('final_confidence',''),'mapping_origin':'STEP12_D12_28_D12_30_EVIDENCE_INDEPENDENT_V6'})
assert len(map_rows)==2332

# Rebuild internal-link ledger. Every old IMPLEMENT row is replaced only by its explicit D12-29 current validation.
lval={r['link_action_id']:r for r in lvals}
assert len(lval)==28
link_fields=header(P_LINK)
final_links=[]
affected=set(content_by)
for l in oldlinks:
    uid=l['structural_unit_id']
    if l['link_action_state']=='IMPLEMENT':
        v=lval[l['link_action_id']]
        cuid=v['corrected_structural_unit_id']
        assert cuid in old_actions,(l['link_action_id'],cuid)
        nl=dict(l);nl['structural_unit_id']=cuid;nl['structural_action']=old_actions[cuid]['structural_action'];nl['link_action_state']=v['corrected_link_action_state'];nl['relation_type']=v['corrected_relation_type'];nl['placement_context']=v['corrected_placement_context'];nl['anchor_concept']=v['corrected_anchor_concept'];nl['user_journey_purpose']=v['validation_rationale'];nl['business_handoff']='CURRENT_USER_NEXT_STEP_HELPFUL' if bools(v['user_next_step_helpful']) else 'DEFER_UNTIL_CURRENT_CONTEXT_OR_TARGET_FIT_EXISTS';nl['evidence_origin']='D12_29_CURRENT_SOURCE_TARGET_VALIDATION';final_links.append(nl)
    elif uid in affected or uid in removed:
        continue
    elif uid in old_actions:
        nl=dict(l);nl['structural_action']=old_actions[uid]['structural_action'];final_links.append(nl)

# Explicit on-page states for surviving affected content-changing actions; no invented link.
existing_link_units={r['structural_unit_id'] for r in final_links}
seq=1
for uid,c in sorted(content_by.items()):
    if uid not in old_actions:continue
    act=old_actions[uid]['structural_action']
    if act in {'EXPAND_EXISTING_PAGE','ADD_SECTION_OR_FAQ_TO_EXISTING'} and uid not in existing_link_units:
        final_links.append({'link_action_id':f'ILR28{seq:03d}','structural_unit_id':uid,'structural_action':act,'link_action_state':'NOT_APPLICABLE_NO_DISTINCT_TARGET','source_url':old_actions[uid].get('primary_page_candidate',''),'target_url':'','relation_type':'ON_PAGE_CONTENT_ACTION_ONLY','placement_context':'Implement only the explicit missing need(s) recorded by D12-28 current-content evidence.','anchor_concept':c['explicit_missing_needs'],'user_journey_purpose':'Close the independently observed current-page content deficit without inventing a separate URL/link.','business_handoff':'ANSWER_USER_NEED_ON_CURRENT_OWNER','evidence_origin':'D12_28_CURRENT_CONTENT_REVALIDATION'});seq+=1
# Remove stale links to action rows that no longer exist.
final_links=[l for l in final_links if l['structural_unit_id'] in old_actions]
assert len({l['link_action_id'] for l in final_links})==len(final_links)

# Final row order and files.
action_rows=[old_actions[k] for k in sorted(old_actions)]
write(O_ASSIGN,assign,header(P_ASSIGN))
write(O_ACTION,action_rows,afields)
write(O_MAP,map_rows,map_fields)
write(O_LINK,sorted(final_links,key=lambda r:r['link_action_id']),link_fields)
pair_fields=['pair_id','page_a','page_b','derivation_routes','source_effective_clusters','relation_structural_units','member_evidence','adjacent_task','normal_overlap_rationale','later_direct_search_check_needed','search_check_reason','derivation_origin']
write(O_PAIR,pair_rows,pair_fields)

quality=[r for r in action_rows if r.get('content_enhancement_state')=='QUALITY_GAP']
qa={'date':'2026-08-31','status':'D12_28_D12_29_D12_30_V6_CANDIDATE_READY_FOR_INDEPENDENT_QA','source_assignment_rows':2332,'final_assignment_rows':len(assign),'assigned_rows':sum(bool(r.get('final_structural_unit_id')) for r in assign),'exact_phrase_resolutions':len(resolutions),'affected_source_units':len(content),'affected_source_member_phrases':sum(int(r['source_phrase_count']) for r in content),'removed_zero_member_units':sorted(removed),'new_explicit_units':len(newdefs),'final_structural_units':len(action_rows),'quality_gap_units_after_revalidation':len(quality),'quality_gap_without_explicit_missing_need':sum(not r.get('explicit_missing_needs','').strip() for r in quality),'final_phrase_map_rows':len(map_rows),'prior_implement_links_reviewed':len(lvals),'final_link_rows':len(final_links),'final_implement_links':sum(r['link_action_state']=='IMPLEMENT' for r in final_links),'candidate_pairs':len(pair_rows),'pairs_requiring_step13':sum(r['later_direct_search_check_needed']=='true' for r in pair_rows),'new_page_actions':sum(r['structural_action'] in {'NEW_COMMERCIAL_PAGE','NEW_INFORMATIONAL_PAGE'} for r in action_rows),'step13_executed':False,'build_origin':'EXPLICIT_D12_28_CURRENT_CONTENT_EVIDENCE_PLUS_D12_30_EXACT_PHRASE_RESOLUTIONS_PLUS_D12_29_CURRENT_LINK_VALIDATION'}
O_QA.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False,indent=2))
