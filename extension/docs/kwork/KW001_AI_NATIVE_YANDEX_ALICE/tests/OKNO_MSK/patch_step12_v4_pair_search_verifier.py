from pathlib import Path

R=Path(__file__).resolve().parent
builder=R/'step12_build_third_audit_v4.py'
bs=builder.read_text(encoding='utf-8')
old="        if 'PENDING_STEP13' in (r.get('recommendation_maturity') or ''):reasons.add('CONTRIBUTING_UNIT_ALREADY_SEARCH_PROVISIONAL')\n"
fixed="        # Prior recommendation maturity is downstream state, not independent evidence; do not use it to trigger Step-13 search.\n"
if old in bs:
    bs=bs.replace(old,fixed,1)
elif fixed not in bs:
    raise RuntimeError('builder pair-trigger pattern missing')
builder.write_text(bs,encoding='utf-8')

p=R/'step12_verify_third_audit_v4.py'
s=p.read_text(encoding='utf-8')
old_decl="V4=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V4.tsv';ASSIGN=R/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv';DEC=R/'STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv';LINKS=R/'STEP_12_INTERNAL_LINK_ACTIONS.tsv';PAIRS=R/'STEP_12_STEP13_CANDIDATE_PAIRS_V4.tsv';PMAP=R/'STEP_12_PHRASE_ACTION_MAP_FINAL_V4.tsv';OUT=R/'STEP_12_THIRD_AUDIT_INDEPENDENT_QA.json';FIND=R/'STEP_12_THIRD_AUDIT_QA_FINDINGS.tsv'"
new_decl="V4=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V4.tsv';ASSIGN=R/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv';DEC=R/'STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv';HIST=R/'STEP_12_STRUCTURAL_ACTIONS.tsv';LINKS=R/'STEP_12_INTERNAL_LINK_ACTIONS.tsv';PAIRS=R/'STEP_12_STEP13_CANDIDATE_PAIRS_V4.tsv';PMAP=R/'STEP_12_PHRASE_ACTION_MAP_FINAL_V4.tsv';OUT=R/'STEP_12_THIRD_AUDIT_INDEPENDENT_QA.json';FIND=R/'STEP_12_THIRD_AUDIT_QA_FINDINGS.tsv'"
if old_decl in s:s=s.replace(old_decl,new_decl,1)
elif new_decl not in s:raise RuntimeError('verifier declaration pattern missing')
old_load="v4=read(V4);assign=read(ASSIGN);dec=read(DEC);links=read(LINKS);pairs=read(PAIRS);pmap=read(PMAP)"
new_load="v4=read(V4);assign=read(ASSIGN);dec=read(DEC);hist=read(HIST);links=read(LINKS);pairs=read(PAIRS);pmap=read(PMAP)"
if old_load in s:s=s.replace(old_load,new_load,1)
elif new_load not in s:raise RuntimeError('verifier load pattern missing')
start=s.index('# Recompute expected pair-key universe from V4 routing + target/relevant mismatch.')
end=s.index('# Phrase map exact accounting.',start)
new_block=r'''# Recompute expected pair universe AND Step-13 search trigger/reasons from primary evidence only.
page_uids=defaultdict(set)
for uid,r in by.items():
    p=norm_url(r.get('primary_page_candidate'))
    if p:page_uids[p].add(uid)
hist_follow={r['cluster_id']:(r.get('step13_followup_required','').strip().lower()=='true') for r in hist}
expected_meta={}
def add_pair(a,b,route,units=None,srcs=None):
    a,b=norm_url(a),norm_url(b)
    if not a or not b or a==b:return
    k=tuple(sorted((a,b)))
    x=expected_meta.setdefault(k,{'routes':set(),'units':set(),'clusters':set()})
    x['routes'].add(route);x['units'].update(units or []);x['clusters'].update(srcs or [])
for uid,r in by.items():
    a,b=norm_url(r.get('primary_page_candidate')),norm_url(r.get('supporting_page'))
    if a and b and a!=b:
        add_pair(a,b,'EXPLICIT_PRIMARY_SUPPORTING_EDGE',{uid}|page_uids.get(b,set()),[x.strip() for x in (r.get('source_effective_clusters') or '').split(';') if x.strip()])
    if r['relevant_url_match_state']=='MISMATCH':
        for u in filter(None,r['current_yandex_relevant_url'].split(';')):
            add_pair(a,u,'TARGET_VS_OBSERVED_YANDEX_RELEVANT_MISMATCH',{uid},[x.strip() for x in (r.get('source_effective_clusters') or '').split(';') if x.strip()])
for src,uids in source_uids.items():
    pu=defaultdict(set)
    for uid in uids:
        pp=norm_url(by[uid].get('primary_page_candidate'))
        if pp:pu[pp].add(uid)
    for a,b in combinations(sorted(pu),2):
        add_pair(a,b,'SHARED_SOURCE_CLUSTER_PRIMARY_DESTINATIONS',pu[a]|pu[b],{src})

expected_search={}; expected_reason_sets={}; expected_dep_units=set()
for k,x in expected_meta.items():
    reasons=set()
    if 'TARGET_VS_OBSERVED_YANDEX_RELEVANT_MISMATCH' in x['routes']:
        reasons.add('OBSERVED_TARGET_RELEVANT_URL_MISMATCH')
    if any(hist_follow.get(c,False) for c in x['clusters']):
        reasons.add('HISTORICAL_KNOWN_FOLLOWUP_SIGNAL_PRESERVED')
    for uid in x['units']:
        if by[uid].get('search_boundary_support')=='MATERIAL_BOUNDARY_GAP':
            reasons.add('MATERIAL_SEARCH_BOUNDARY_GAP_IN_CONTRIBUTING_UNIT')
    if 'SHARED_SOURCE_CLUSTER_PRIMARY_DESTINATIONS' in x['routes'] and not parent_child(*k):
        reasons.add('NON_HIERARCHICAL_MULTI_PRIMARY_ROUTE_FROM_SAME_SOURCE_CLUSTER')
    expected_search[k]=bool(reasons); expected_reason_sets[k]=reasons
    if reasons:expected_dep_units.update(x['units'])

actual_keys=[]; actual_by={}
for row in pairs:
    k=tuple(sorted((norm_url(row['page_a']),norm_url(row['page_b']))))
    actual_keys.append(k);actual_by[k]=row
expected=set(expected_meta);actset=set(actual_keys)
missing=expected-actset;extra=actset-expected;dups=len(actual_keys)-len(actset)
if missing:f('QPAIR',f'missing pairs={len(missing)}')
if extra:f('QPAIR',f'extra pairs={len(extra)}')
if dups:f('QPAIR',f'duplicate pairs={dups}')
flag_mismatches=0;reason_mismatches=0;route_mismatches=0;unit_mismatches=0
for k in sorted(expected & actset):
    row=actual_by[k];x=expected_meta[k]
    act_flag=row['later_direct_search_check_needed']=='true'
    if act_flag!=expected_search[k]:
        flag_mismatches+=1;f('QPAIR_SEARCH_FLAG',f'{k} actual={act_flag} expected={expected_search[k]}')
    act_reasons={z for z in row['search_check_reason'].split(';') if z and z!='NO_MATERIAL_DIRECT_SEARCH_TRIGGER_DERIVED_AT_STEP12'}
    if act_reasons!=expected_reason_sets[k]:
        reason_mismatches+=1;f('QPAIR_SEARCH_REASON',f'{k} actual={sorted(act_reasons)} expected={sorted(expected_reason_sets[k])}')
    act_routes={z for z in row['derivation_routes'].split(';') if z}
    if act_routes!=x['routes']:
        route_mismatches+=1;f('QPAIR_ROUTE',f'{k} routes mismatch')
    act_units={z for z in row['relation_structural_units'].split(';') if z}
    if act_units!=x['units']:
        unit_mismatches+=1;f('QPAIR_UNITS',f'{k} units mismatch')
actual_dep_units={r['structural_unit_id'] for r in v4 if r.get('step13_dependency_required')=='true'}
if actual_dep_units!=expected_dep_units:
    f('QPAIR_DEP_UNITS',f'actual dependency units={len(actual_dep_units)} expected={len(expected_dep_units)}')
expected_search_pair_count=sum(expected_search.values())
actual_search_pair_count=sum(r['later_direct_search_check_needed']=='true' for r in pairs)
'''
s=s[:start]+new_block+'\n'+s[end:]
old_qa=" 'internal_link_implement':sum(r['link_action_state']=='IMPLEMENT' for r in links),'expected_pair_keys':len(expected),'actual_pair_rows':len(pairs),'pair_missing':len(missing),'pair_extra':len(extra),'pair_duplicates':dups,"
new_qa=" 'internal_link_implement':sum(r['link_action_state']=='IMPLEMENT' for r in links),'expected_pair_keys':len(expected),'actual_pair_rows':len(pairs),'pair_missing':len(missing),'pair_extra':len(extra),'pair_duplicates':dups,\n 'expected_pairs_requiring_step13':expected_search_pair_count,'actual_pairs_requiring_step13':actual_search_pair_count,'pair_search_flag_mismatches':flag_mismatches,'pair_search_reason_mismatches':reason_mismatches,'pair_route_mismatches':route_mismatches,'pair_unit_mismatches':unit_mismatches,'expected_dependency_units':len(expected_dep_units),'actual_dependency_units':len(actual_dep_units),"
if old_qa not in s:raise RuntimeError('QA insertion pattern missing')
s=s.replace(old_qa,new_qa,1)
p.write_text(s,encoding='utf-8')
print('STEP12_V4_PAIR_SEARCH_VERIFIER_PATCHED')
