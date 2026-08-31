import csv,json
from collections import Counter,defaultdict
from itertools import combinations
from pathlib import Path
from urllib.parse import urlsplit
R=Path(__file__).resolve().parent
V1=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V1.tsv';V3=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V3.tsv';ASSIGN=R/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv';HIST=R/'STEP_12_STRUCTURAL_ACTIONS.tsv';CORR=R/'STEP_12_POST_CLOSE_CURRENT_SITE_BUSINESS_CORRECTIONS.tsv';FRESH=R/'STEP_12_SECOND_AUDIT_FRESHNESS_EVIDENCE.tsv';PAIRS=R/'STEP_12_STEP13_CANDIDATE_PAIRS_V3.tsv';MAP=R/'STEP_12_PHRASE_ACTION_MAP_FINAL_V3.tsv';CONCEPTS=R/'STEP_12_FORMER_NEW_PAGE_CONCEPTS_SECOND_AUDIT.tsv';STATE=R/'STEP_12_CORRECTION_CURRENT_STATE.json';OUT=R/'STEP_12_SECOND_AUDIT_INDEPENDENT_QA.json';FIND=R/'STEP_12_SECOND_AUDIT_QA_FINDINGS.tsv'

def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def norm(v):
    v=(v or '').strip()
    if v.startswith('PROPOSED_NEW:'):
        x=v.split(':',1)[1].strip();x=x if x.startswith('/') else '/'+x;return 'https://okno-msk.ru'+x
    return v if v.startswith('http://') or v.startswith('https://') else ''
def pc(a,b):
    pa,pb=urlsplit(a),urlsplit(b)
    if pa.netloc!=pb.netloc:return False
    aa=pa.path.rstrip('/')+'/';bb=pb.path.rstrip('/')+'/'
    return aa!=bb and (aa.startswith(bb) or bb.startswith(aa))

def fail(findings,kind,subject,observed,expected,note):findings.append({'finding_id':f'F{len(findings)+1:03d}','finding_type':kind,'subject':subject,'observed':str(observed),'expected':str(expected),'note':note})

v1=read(V1);v3=read(V3);a=read(ASSIGN);hist=read(HIST);corr=read(CORR);fresh=read(FRESH);pairs=read(PAIRS);pm=read(MAP);concepts=read(CONCEPTS);state=json.loads(STATE.read_text(encoding='utf-8'))
findings=[];by={r['structural_unit_id']:r for r in v3};v1by={r['structural_unit_id']:r for r in v1};cb={r['structural_unit_id']:r for r in corr}
# basic accounting
if len(v3)!=160:fail(findings,'ACTION_ROW_COUNT','V3',len(v3),160,'Final structural actions must cover all units.')
if len(a)!=2332:fail(findings,'ASSIGNMENT_COUNT','assignments',len(a),2332,'Frozen phrase assignments must be preserved.')
if len(pm)!=2332:fail(findings,'PHRASE_MAP_COUNT','phrase map',len(pm),2332,'Every phrase must be materialized.')
if Counter(r['phrase'] for r in a)!=Counter(r['phrase'] for r in pm):fail(findings,'PHRASE_MULTISET_MISMATCH','phrase map','mismatch','exact same multiset','No silent phrase loss/duplication.')
assigned=[r for r in a if r.get('final_structural_unit_id','').strip()];unres=[r for r in a if not r.get('final_structural_unit_id','').strip()]
if len(assigned)!=2313 or len(unres)!=19:fail(findings,'ASSIGNMENT_ACCOUNTING','assigned/unresolved',f'{len(assigned)}/{len(unres)}','2313/19','Preserve corrected Step11 handoff.')
# Current proposed/create invariants
proposed=[r['structural_unit_id'] for r in v3 if 'PROPOSED_NEW:' in (r['primary_page_candidate']+' '+r['supporting_page'])]
new=[r['structural_unit_id'] for r in v3 if r['structural_action'] in {'NEW_COMMERCIAL_PAGE','NEW_INFORMATIONAL_PAGE'}]
if proposed:fail(findings,'WITHDRAWN_PROPOSED_REF_SURVIVED',';'.join(proposed),len(proposed),0,'All five former page concepts were withdrawn under current-site/business audit.')
if new:fail(findings,'NEW_ACTION_SURVIVED_SECOND_AUDIT',';'.join(new),len(new),0,'No current new page survived the second audit.')
# business/freshness fields
req=['owner_goal_evidence_state','owner_primary_goal','desired_user_outcome','business_potential','content_role','counterproductive_to_core_offer','fresh_site_check_status','existing_content_reuse']
miss=[r['structural_unit_id'] for r in v3 if any(not r.get(k,'').strip() for k in req)]
if miss:fail(findings,'BUSINESS_FRESHNESS_FIELDS_MISSING',';'.join(miss),len(miss),0,'Every unit needs explicit business/freshness interpretation.')
if len(corr)!=14 or any(r['fresh_site_check_status']!='CURRENT_VERIFIED' for r in corr):fail(findings,'SECOND_AUDIT_CORRECTION_COVERAGE','correction overlay',len(corr),'14 CURRENT_VERIFIED','All old proposed references must be explicitly re-routed.')
if len(fresh)!=5 or any(r['page_opened_read']!='true' for r in fresh):fail(findings,'FRESHNESS_CONCEPT_COVERAGE','former concepts',len(fresh),'5 opened/read','All former page concepts need timestamped current evidence.')
if len(concepts)!=5 or any(not r['second_audit_verdict'].startswith('WITHDRAW') for r in concepts):fail(findings,'FORMER_NEW_PAGE_STATUS','former concepts',len(concepts),'5 withdrawn','Former concepts must be explicitly superseded.')
# Known owner-challenge regressions
known={
'PANORAMIC_WINDOWS_COMMERCIAL_CORE':('KEEP_EXISTING_STRUCTURE','https://okno-msk.ru/okna-rehau/panoramnoe-osteklenie/'),
'WINDOW_REPLACEMENT_SERVICE':('EXPAND_EXISTING_PAGE','https://okno-msk.ru/okna-rehau/po-tipu-doma/zamena-okon-v-kvartire/'),
'PVC_WINDOW_INSTALLATION_DIY':('ADD_SECTION_OR_FAQ_TO_EXISTING','https://okno-msk.ru/uslugi/ustanovka-okon/'),
'PVC_WINDOW_ADJUSTMENT_DIY':('KEEP_EXISTING_STRUCTURE','https://okno-msk.ru/stati/kak-otregulirovat-plastikovye-okna/'),
'WINDOW_HARDWARE_SELECTION_GUIDE':('EXPAND_EXISTING_PAGE','https://okno-msk.ru/stati/kak-vybrat-plastikovye-okna/'),
'PVC_WINDOW_OPERATION_DIY':('ROUTE_TO_EXISTING_PAGE_AS_SUBTASK','https://okno-msk.ru/stati/okno-otkrylos-v-dvuh-polozheniyah-chto-delat/'),
}
for uid,(act,url) in known.items():
    r=by[uid]
    if (r['structural_action'],r['primary_page_candidate'])!=(act,url):fail(findings,'OWNER_CHALLENGE_REGRESSION',uid,f"{r['structural_action']} -> {r['primary_page_candidate']}",f'{act} -> {url}','Fresh current-page/business correction must persist.')
# phrase map independently joins V3
pmb={r['phrase']:r for r in pm};bad=0
for r in assigned:
    m=pmb.get(r['phrase']);x=by[r['final_structural_unit_id']]
    if not m or m['final_structural_unit_id']!=r['final_structural_unit_id'] or m['structural_action']!=x['structural_action'] or m['primary_page_candidate']!=x['primary_page_candidate'] or m['recommendation_maturity']!=x['recommendation_maturity']:bad+=1
if bad:fail(findings,'PHRASE_ACTION_JOIN_MISMATCH','assigned phrase map',bad,0,'Recompute final phrase route from assignment + V3 action.')
bad_un=0
for r in unres:
    m=pmb.get(r['phrase'])
    if not m or m['final_structural_unit_id'] or m['structural_action']!='DEFER_UNRESOLVED' or m['primary_page_candidate']:bad_un+=1
if bad_un:fail(findings,'UNRESOLVED_ROUTE_MISMATCH','unresolved phrase map',bad_un,0,'19 unresolved rows must remain unresolved/no target.')
# Independently derive expected current pair-key universe: primary/support + multi-primary shared source. No old proposed hierarchy.
source=defaultdict(set);pageuids=defaultdict(set)
for r in a:
    uid=r.get('final_structural_unit_id','').strip();src=r.get('original_effective_cluster_id','').strip()
    if uid and src:source[src].add(uid)
for uid,r in by.items():
    p=norm(r['primary_page_candidate'])
    if p:pageuids[p].add(uid)
exp={}
def add(a,b,route,units,srcs):
    a,b=norm(a),norm(b)
    if not a or not b or a==b:return
    k=tuple(sorted((a,b)));x=exp.setdefault(k,{'routes':set(),'units':set(),'clusters':set()});x['routes'].add(route);x['units'].update(units);x['clusters'].update(srcs)
for uid,r in by.items():
    p,s=norm(r['primary_page_candidate']),norm(r['supporting_page'])
    if p and s and p!=s:add(p,s,'EXPLICIT_PRIMARY_SUPPORTING_EDGE',{uid}|pageuids.get(s,set()),set(x for x in r['source_effective_clusters'].split(';') if x))
for src,uids in source.items():
    ps=defaultdict(set)
    for uid in uids:
        p=norm(by[uid]['primary_page_candidate'])
        if p:ps[p].add(uid)
    for x,y in combinations(sorted(ps),2):add(x,y,'SHARED_SOURCE_CLUSTER_PRIMARY_DESTINATIONS',ps[x]|ps[y],{src})
actualkeys=[tuple(sorted((r['page_a'],r['page_b']))) for r in pairs];actual=set(actualkeys);expected=set(exp)
if expected-actual:fail(findings,'PAIR_KEYS_MISSING','pair graph',len(expected-actual),0,'Independent current-routing graph has missing persisted pairs.')
if actual-expected:fail(findings,'PAIR_KEYS_EXTRA','pair graph',len(actual-expected),0,'Persisted graph contains non-current/old proposed edges.')
if len(actualkeys)!=len(actual):fail(findings,'PAIR_DUPLICATES','pair graph',len(actualkeys)-len(actual),0,'No duplicate current pair rows.')
# Recompute expected search flags using historical signal + current V1/overlay pre-pair evidence + nonhier multi-primary.
hfollow={r['cluster_id']:(r.get('step13_followup_required','').strip().lower()=='true') for r in hist}
actual_by={tuple(sorted((r['page_a'],r['page_b']))):r for r in pairs};flagmis=[];dep_expected=set()
for k,x in exp.items():
    reasons=set()
    if any(hfollow.get(c,False) for c in x['clusters']):reasons.add('HIST')
    for uid in x['units']:
        if uid in cb:pre_search='NOT_REQUIRED_FOR_CURRENT_REUSE_ACTION__STEP13_ONLY_IF_PAIR_DERIVED';pre_mat='FINAL_WITHIN_STEP12_EVIDENCE'
        else:pre_search=v1by[uid]['search_boundary_support'];pre_mat=v1by[uid]['recommendation_maturity']
        if pre_search=='MATERIAL_BOUNDARY_GAP':reasons.add('SEARCH_GAP')
        if 'PENDING_SEARCH' in pre_mat:reasons.add('PENDING_SEARCH')
    if 'SHARED_SOURCE_CLUSTER_PRIMARY_DESTINATIONS' in x['routes'] and not pc(*k):reasons.add('NON_HIER_MULTI_PRIMARY')
    expected_true=bool(reasons);actual_true=actual_by[k]['later_direct_search_check_needed']=='true'
    if expected_true!=actual_true:flagmis.append(k)
    if expected_true:dep_expected.update(x['units'])
if flagmis:fail(findings,'PAIR_SEARCH_FLAG_MISMATCH','pair graph',len(flagmis),0,'Search-check flags must be independently derivable.')
dep_actual={r['structural_unit_id'] for r in v3 if r['step13_dependency_required']=='true'}
if dep_expected!=dep_actual:fail(findings,'DEPENDENCY_UNIT_MISMATCH','V3 dependency flags',f'missing={len(dep_expected-dep_actual)}, extra={len(dep_actual-dep_expected)}','0/0','Step13 dependency must follow current pair flags.')
dh=[r['structural_unit_id'] for r in v3 if r['step13_dependency_required']=='true' and r['final_confidence']=='HIGH'];df=[r['structural_unit_id'] for r in v3 if r['step13_dependency_required']=='true' and r['recommendation_maturity']=='FINAL_WITHIN_STEP12_EVIDENCE']
if dh:fail(findings,'DEPENDENCY_HIGH','V3',len(dh),0,'Step13-dependent recommendations cannot be HIGH.')
if df:fail(findings,'DEPENDENCY_FINAL','V3',len(df),0,'Step13-dependent recommendations cannot look final.')
# Step boundary / state
step13_files=sorted(p.name for p in R.glob('STEP_13_*'))
if step13_files:fail(findings,'PREMATURE_STEP13_FILES','workspace',step13_files,[],'Step13 must remain unexecuted while Step12 reopened.')
needed={'D12-16','D12-17','D12-18','D12-19','D12-20'}
if not needed.issubset(set(state.get('open_defects',[]))) or not state.get('step13_blocked') or state.get('step12_complete'):fail(findings,'PRE_CLOSURE_STATE_INVALID','current state',state.get('open_defects'),sorted(needed),'Defects remain open until this QA is persisted/read back and closure runs.')

# Persist findings and QA without self-certifying closure.
fields=['finding_id','finding_type','subject','observed','expected','note']
with FIND.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(findings)
qa={
 'date':'2026-08-31','status':'STEP12_SECOND_AUDIT_V3_INDEPENDENT_PASS' if not findings else 'STEP12_SECOND_AUDIT_V3_DIAGNOSTIC_FAIL','findings':len(findings),
 'source_actions':len(v1),'final_actions_v3':len(v3),'assignments':len(a),'phrase_map_rows':len(pm),'assigned':len(assigned),'unresolved':len(unres),
 'current_new_actions':len(new),'current_proposed_refs':len(proposed),'freshness_concepts':len(fresh),'former_new_concepts':len(concepts),'business_freshness_missing_rows':len(miss),
 'expected_current_pair_keys':len(expected),'actual_current_pair_rows':len(pairs),'missing_pair_keys':len(expected-actual),'extra_pair_keys':len(actual-expected),'duplicate_pair_rows':len(actualkeys)-len(actual),'search_flag_mismatches':len(flagmis),'expected_dependency_units':len(dep_expected),'actual_dependency_units':len(dep_actual),'dependency_high_rows':len(dh),'dependency_final_rows':len(df),
 'owner_challenge_regression_cases':len(known),'step13_files':step13_files,'step13_executed':False,'step12_complete':False,'next_step_allowed':False,
 'verification_origin':'INDEPENDENT_RECOMPUTATION_FROM_PERSISTED_V1_ASSIGNMENTS_CURRENT_V3_FRESHNESS_AND_CORRECTION_EVIDENCE','defects_closed_by_verifier_alone':[]}
OUT.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False,indent=2))
