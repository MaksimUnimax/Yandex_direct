import csv,json,re
from collections import defaultdict,Counter
from itertools import combinations
from pathlib import Path
from urllib.parse import urlsplit

R=Path(__file__).resolve().parent
V4=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V4.tsv';ASSIGN=R/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv';DEC=R/'STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv';LINKS=R/'STEP_12_INTERNAL_LINK_ACTIONS.tsv';PAIRS=R/'STEP_12_STEP13_CANDIDATE_PAIRS_V4.tsv';PMAP=R/'STEP_12_PHRASE_ACTION_MAP_FINAL_V4.tsv';OUT=R/'STEP_12_THIRD_AUDIT_INDEPENDENT_QA.json';FIND=R/'STEP_12_THIRD_AUDIT_QA_FINDINGS.tsv'

def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def qnorm(s):return re.sub(r'\s+',' ',(s or '').strip().lower())
def norm_url(v):
    v=(v or '').strip()
    if not v:return ''
    if not v.startswith(('http://','https://')):return ''
    p=urlsplit(v); path=(p.path or '/').rstrip('/') or '/'
    return f'https://{p.netloc.lower().removeprefix("www.")}{path}'
def target_domain(d):
    d=(d or '').strip().lower().removeprefix('www.');return d=='okno-msk.ru' or d.endswith('.okno-msk.ru')
def parent_child(a,b):
    pa,pb=urlsplit(a),urlsplit(b)
    if pa.netloc.lower().removeprefix('www.')!=pb.netloc.lower().removeprefix('www.'):return False
    aa=pa.path.rstrip('/')+'/';bb=pb.path.rstrip('/')+'/'
    return aa!=bb and (aa.startswith(bb) or bb.startswith(aa))

v4=read(V4);assign=read(ASSIGN);dec=read(DEC);links=read(LINKS);pairs=read(PAIRS);pmap=read(PMAP)
find=[]
def f(cid,msg):find.append({'check_id':cid,'finding':msg})
if len(v4)!=160:f('Q001',f'v4 rows={len(v4)}')
if len(assign)!=2332 or len(pmap)!=2332:f('Q002',f'accounting assign={len(assign)} pmap={len(pmap)}')
by={r['structural_unit_id']:r for r in v4}
if len(by)!=len(v4):f('Q003','duplicate structural_unit_id')

# Independent member mapping.
members=defaultdict(list);source_uids=defaultdict(set)
for a in assign:
    uid=(a.get('final_structural_unit_id') or '').strip()
    if uid:
        members[uid].append(a['phrase'])
        s=(a.get('original_effective_cluster_id') or '').strip()
        if s:source_uids[s].add(uid)

# D12-21: gap type is recomputed solely from action semantics.
for r in v4:
    a=r['structural_action']
    exp='QUALITY_GAP' if a in {'EXPAND_EXISTING_PAGE','ADD_SECTION_OR_FAQ_TO_EXISTING'} else ('EVIDENCE_INSUFFICIENT' if a=='DEFER_PENDING_EVIDENCE' else 'NONE')
    if r['gap_type']!=exp:f('D12-21',f"{r['structural_unit_id']} gap={r['gap_type']} expected={exp}")
    if not r['gap_evidence']:f('D12-21',f"{r['structural_unit_id']} blank gap evidence")
    if a in {'NEW_COMMERCIAL_PAGE','NEW_INFORMATIONAL_PAGE'} and r['gap_type']!='TOPIC_GAP':f('D12-21',f"{r['structural_unit_id']} CREATE without TOPIC_GAP")

# D12-22: no performance fabrication, especially KEEP.
for r in v4:
    if r['performance_evidence_state']!='NOT_AVAILABLE_IN_BASE_SCOPE_NO_WEBMASTER_METRIKA':f('D12-22',f"{r['structural_unit_id']} unexpected performance state")
    if r['structural_action']=='KEEP_EXISTING_STRUCTURE' and 'NOT_ASSESSED' not in r['optimization_readiness']:f('D12-22',f"{r['structural_unit_id']} KEEP overstates optimization readiness")

# Rebuild persisted Step9 query/hit evidence independently.
dec_by={qnorm(r['query']):r for r in dec};raw_by=defaultdict(list)
for p in [R/'STEP_09_SERP_RESULTS.tsv']+sorted(R.glob('STEP_09_SERP_R2_PROJECTION_RAW_PART_*.tsv')):
    if not p.exists():continue
    for x in read(p):
        q=qnorm(x.get('query_text') or x.get('query'))
        if q:raw_by[q].append(x)
for r in v4:
    uid=r['structural_unit_id'];dqs=[];obs=set();types=set();jobs=set()
    for ph in members.get(uid,[]):
        q=qnorm(ph)
        if q not in dec_by:continue
        dqs.append(ph);d=dec_by[q]
        if d.get('dominant_result_type'):types.add(d['dominant_result_type'].strip())
        if d.get('observed_serp_job'):jobs.add(d['observed_serp_job'].strip())
        for hit in raw_by.get(q,[]):
            if target_domain(hit.get('domain','')):
                u=norm_url(hit.get('url',''))
                if u:obs.add(u)
    intended=norm_url(r.get('primary_page_candidate'))
    if not intended:exp='NOT_APPLICABLE_NO_INTENDED_TARGET'
    elif not dqs:exp='NOT_DIRECTLY_CHECKED'
    elif not obs:exp='SITE_NOT_OBSERVED'
    elif intended in obs:exp='MATCH'
    else:exp='MISMATCH'
    if r['relevant_url_match_state']!=exp:f('D12-23',f"{uid} match={r['relevant_url_match_state']} expected={exp}")
    if set(filter(None,r['current_yandex_relevant_url'].split(';')))!=obs:f('D12-23',f'{uid} observed URL set mismatch')
    if set(filter(None,r['direct_serp_queries'].split(';')))!=set(dqs):f('D12-23',f'{uid} direct query set mismatch')
    # D12-24: preserve source-derived type; format/angle may remain explicitly unobserved.
    if dqs:
        if not r['serp_format_evidence_state'].startswith('DIRECT_STEP09_QUERY_EVIDENCE'):f('D12-24',f'{uid} direct evidence state missing')
        if set(filter(None,r['serp_expected_content_type'].split(';')))!=types:f('D12-24',f'{uid} content type mismatch')
        if r['serp_expected_format']!='NOT_SEPARATELY_OBSERVED_IN_PERSISTED_STEP09':f('D12-24',f'{uid} fabricated/invalid format state')
        if r['serp_expected_angle']!='NOT_SEPARATELY_OBSERVED_IN_PERSISTED_STEP09':f('D12-24',f'{uid} fabricated/invalid angle state')
    else:
        if r['serp_format_evidence_state']!='NOT_DIRECTLY_CHECKED':f('D12-24',f'{uid} unprobed format state not explicit')

# D12-25: source labels and policy-sensitive uncertainty.
allowed={'CLIENT_STATED','ANALYTICS_OBSERVED','SALES_SUPPORT_EVIDENCE','PUBLIC_SITE_EXPLICIT','PUBLIC_SITE_INFERRED','UNKNOWN','NOT_APPLICABLE'}
for r in v4:
    if r['owner_goal_evidence_source'] not in allowed:f('D12-25',f"{r['structural_unit_id']} bad owner source")
    if r['owner_goal_evidence_source']=='CLIENT_STATED':f('D12-25',f"{r['structural_unit_id']} falsely labelled client-stated in base public-site scope")
    if r['owner_goal_evidence_source']=='UNKNOWN' and r['owner_policy_materiality']=='HIGH' and r['recommendation_maturity']=='FINAL_WITHIN_STEP12_EVIDENCE':f('D12-25',f"{r['structural_unit_id']} high policy uncertainty marked final")

# D12-26: every material existing-page action has exactly one implementation-state row.
material={'ROUTE_TO_EXISTING_PAGE_AS_SUBTASK','ADD_SECTION_OR_FAQ_TO_EXISTING','EXPAND_EXISTING_PAGE'}
link_by=defaultdict(list)
for x in links:link_by[x['structural_unit_id']].append(x)
for r in v4:
    uid=r['structural_unit_id']
    if r['structural_action'] in material:
        if len(link_by[uid])!=1:f('D12-26',f'{uid} link rows={len(link_by[uid])}')
        else:
            x=link_by[uid]
            x=x[0]
            if x['link_action_state']=='IMPLEMENT':
                if not x['source_url'] or not x['target_url'] or norm_url(x['source_url'])==norm_url(x['target_url']):f('D12-26',f'{uid} invalid implement link')
            elif not x['link_action_state'].startswith(('NOT_APPLICABLE','DEFER')):f('D12-26',f'{uid} invalid explicit non-implement state')
            if 'PROPOSED_NEW:' in (x['source_url']+' '+x['target_url']):f('D12-26',f'{uid} withdrawn proposed link')
    elif link_by.get(uid):f('D12-26',f'{uid} unexpected link row for non-material action')

# Recompute expected pair-key universe from V4 routing + target/relevant mismatch.
page_uids=defaultdict(set)
for uid,r in by.items():
    p=norm_url(r.get('primary_page_candidate'))
    if p:page_uids[p].add(uid)
expected=set()
def add(a,b):
    a,b=norm_url(a),norm_url(b)
    if a and b and a!=b:expected.add(tuple(sorted((a,b))))
for uid,r in by.items():
    add(r.get('primary_page_candidate'),r.get('supporting_page'))
    if r['relevant_url_match_state']=='MISMATCH':
        for u in filter(None,r['current_yandex_relevant_url'].split(';')):add(r.get('primary_page_candidate'),u)
for src,uids in source_uids.items():
    pages=sorted({norm_url(by[u].get('primary_page_candidate')) for u in uids if norm_url(by[u].get('primary_page_candidate'))})
    for a,b in combinations(pages,2):add(a,b)
actual=[tuple(sorted((norm_url(r['page_a']),norm_url(r['page_b'])))) for r in pairs]
actset=set(actual)
missing=expected-actset;extra=actset-expected;dups=len(actual)-len(actset)
if missing:f('QPAIR',f'missing pairs={len(missing)}')
if extra:f('QPAIR',f'extra pairs={len(extra)}')
if dups:f('QPAIR',f'duplicate pairs={dups}')

# Phrase map exact accounting.
if Counter(r['phrase'] for r in pmap)!=Counter(a['phrase'] for a in assign):f('QMAP','phrase multiset mismatch')
if any('PROPOSED_NEW:' in ((r.get('primary_page_candidate') or '')+(r.get('supporting_page') or '')) for r in v4):f('QCREATE','withdrawn proposed refs remain')
if any(r['structural_action'] in {'NEW_COMMERCIAL_PAGE','NEW_INFORMATIONAL_PAGE'} for r in v4):f('QCREATE','new page action remains')
step13_files=[p.name for p in R.iterdir() if p.is_file() and p.name.startswith('STEP_13_')]
if step13_files:f('QBOUNDARY','Step13 artifacts exist: '+','.join(step13_files))

fields=['check_id','finding']
with FIND.open('w',encoding='utf-8',newline='') as fp:
    w=csv.DictWriter(fp,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(find)
qa={
 'date':'2026-08-31','status':'STEP12_THIRD_AUDIT_V4_INDEPENDENT_PASS' if not find else 'STEP12_THIRD_AUDIT_V4_INDEPENDENT_FAIL','findings':len(find),
 'structural_units':len(v4),'assignments':len(assign),'phrase_map_rows':len(pmap),'gap_type_missing':sum(not r['gap_type'] for r in v4),
 'performance_state_missing':sum(not r['performance_evidence_state'] for r in v4),'keep_rows':sum(r['structural_action']=='KEEP_EXISTING_STRUCTURE' for r in v4),
 'keep_overstated_optimization':sum(r['structural_action']=='KEEP_EXISTING_STRUCTURE' and 'NOT_ASSESSED' not in r['optimization_readiness'] for r in v4),
 'relevant_match_counts':dict(Counter(r['relevant_url_match_state'] for r in v4)),'direct_serp_units':sum(bool(r['direct_serp_queries']) for r in v4),
 'owner_goal_source_counts':dict(Counter(r['owner_goal_evidence_source'] for r in v4)),'material_link_units':sum(r['structural_action'] in material for r in v4),'internal_link_rows':len(links),
 'internal_link_implement':sum(r['link_action_state']=='IMPLEMENT' for r in links),'expected_pair_keys':len(expected),'actual_pair_rows':len(pairs),'pair_missing':len(missing),'pair_extra':len(extra),'pair_duplicates':dups,
 'new_page_actions':sum(r['structural_action'] in {'NEW_COMMERCIAL_PAGE','NEW_INFORMATIONAL_PAGE'} for r in v4),'proposed_new_refs':sum('PROPOSED_NEW:' in ((r.get('primary_page_candidate') or '')+(r.get('supporting_page') or '')) for r in v4),
 'step13_files':step13_files,'step13_executed':False,'verification_origin':'INDEPENDENT_RECOMPUTATION_FROM_V4_ASSIGNMENTS_PERSISTED_STEP09_RAW_AND_DECISIONS'}
OUT.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False,indent=2))
