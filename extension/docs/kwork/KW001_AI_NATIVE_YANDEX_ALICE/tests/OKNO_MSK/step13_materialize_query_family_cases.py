import csv,json,re
from collections import defaultdict,Counter
from pathlib import Path
from urllib.parse import urlsplit

R=Path(__file__).resolve().parent
DEF=R/'STEP_13_QUERY_FAMILY_DEFINITIONS.tsv'
EL=R/'STEP_13_PAIR_ELIGIBILITY.tsv'
ASSIGN=R/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V7.tsv'
ACT=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv'
OUT=R/'STEP_13_QUERY_FAMILY_CASES.tsv'
EVID=R/'STEP_13_QUERY_FAMILY_PHRASE_EVIDENCE.tsv'
QA=R/'STEP_13_QUERY_FAMILY_CASES_QA.json'


def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(p,rows,fields):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
def norm_url(v):
    v=(v or '').strip()
    if not v:return ''
    p=urlsplit(v);path=(p.path or '/').rstrip('/') or '/'
    return f'https://{p.netloc.lower().removeprefix("www.")}{path}'

defs=read(DEF);elig=read(EL);assign=read(ASSIGN);acts=read(ACT)
assert len(defs)==21 and len(elig)==195 and len(assign)==2332 and len(acts)==168
surv={r['pair_id'] for r in elig if r['eligibility_class']=='SURVIVES_TO_QUERY_FAMILY'}
assert len(surv)==27
# Each surviving pair must map to exactly one query-family case.
pair_to_case={}
for d in defs:
    for pid in [x for x in d['pair_ids'].split(';') if x]:
        assert pid in surv,(d['case_id'],pid)
        assert pid not in pair_to_case,(pid,pair_to_case[pid],d['case_id'])
        pair_to_case[pid]=d['case_id']
assert set(pair_to_case)==surv,(sorted(surv-set(pair_to_case)),sorted(set(pair_to_case)-surv))

by_pair={r['pair_id']:r for r in elig}
act_by={r['structural_unit_id']:r for r in acts}
phrases=defaultdict(list)
for r in assign:
    uid=(r.get('final_structural_unit_id') or '').strip()
    if uid: phrases[uid].append(r['phrase'])

case_rows=[];evidence_rows=[]
for d in defs:
    pids=[x for x in d['pair_ids'].split(';') if x]
    units=[];urls=[]
    for pid in pids:
        p=by_pair[pid]
        urls.extend([norm_url(p['page_a']),norm_url(p['page_b'])])
        units.extend([x for x in p['relation_structural_units'].split(';') if x])
    units=sorted(set(units));urls=sorted(set(u for u in urls if u))
    pattern=re.compile(d['query_match_regex'],re.I)
    matched=[]
    for uid in units:
        owner=norm_url(act_by.get(uid,{}).get('primary_page_candidate',''))
        for ph in phrases.get(uid,[]):
            if pattern.search(ph):
                row={'case_id':d['case_id'],'query_family':d['query_family'],'pair_ids':';'.join(pids),'structural_unit_id':uid,'unit_owner_url':owner,'phrase':ph}
                matched.append(row);evidence_rows.append(row)
    matched_units=sorted({r['structural_unit_id'] for r in matched})
    owner_urls=sorted({r['unit_owner_url'] for r in matched if r['unit_owner_url']})
    candidate_owner_hits=sorted(set(urls)&set(owner_urls))
    if not matched: state='ZERO_REGEX_MATCH_IN_CONTRIBUTING_UNITS'
    elif len(candidate_owner_hits)>=2: state='MULTI_CANDIDATE_URL_QUERY_FAMILY_MATERIALIZED'
    elif len(candidate_owner_hits)==1: state='SINGLE_CANDIDATE_URL_QUERY_FAMILY_MATERIALIZED'
    elif owner_urls: state='MATCHED_TO_OTHER_CURRENT_OWNER_URLS'
    else: state='MATCHED_BUT_OWNER_UNRESOLVED_OR_NO_PAGE'
    case_rows.append({
      'case_id':d['case_id'],'query_family':d['query_family'],'pair_ids':';'.join(pids),'candidate_urls':';'.join(urls),
      'contributing_structural_units':';'.join(units),'query_match_regex':d['query_match_regex'],'case_rationale':d['case_rationale'],
      'matched_phrase_count':len(matched),'matched_structural_units':';'.join(matched_units),'matched_owner_urls':';'.join(owner_urls),
      'candidate_owner_urls_with_matches':';'.join(candidate_owner_hits),'query_family_materialization_state':state,
      'fresh_search_required':'UNDECIDED_REUSE_PERSISTED_SEARCH_FIRST'})

write(OUT,case_rows,list(case_rows[0].keys()))
write(EVID,evidence_rows,['case_id','query_family','pair_ids','structural_unit_id','unit_owner_url','phrase'])
states=Counter(r['query_family_materialization_state'] for r in case_rows)
qa={
 'date':'2026-08-31','status':'STEP13_QUERY_FAMILY_CASES_MATERIALIZED','input_surviving_pairs':len(surv),'mapped_surviving_pairs':len(pair_to_case),
 'query_family_cases':len(case_rows),'phrase_evidence_rows':len(evidence_rows),'materialization_state_counts':dict(sorted(states.items())),
 'zero_match_cases':sum(r['matched_phrase_count']==0 for r in case_rows),'provider_calls':0,'step13_search_executed':False,
 'semantic_boundary':'REGEX_MATERIALIZATION_IS_EVIDENCE_EXTRACTION_ONLY__FINAL_CASE_ELIGIBILITY_AND_CONFLICT_VERDICT_REMAIN_MANUAL'
}
QA.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False,indent=2))
