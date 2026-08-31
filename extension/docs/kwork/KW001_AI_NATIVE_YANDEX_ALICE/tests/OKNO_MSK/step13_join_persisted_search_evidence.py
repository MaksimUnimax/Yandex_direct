import csv,json,re
from collections import defaultdict,Counter
from pathlib import Path
from urllib.parse import urlsplit

R=Path(__file__).resolve().parent
CASES=R/'STEP_13_QUERY_FAMILY_CASES.tsv'
PH=R/'STEP_13_QUERY_FAMILY_PHRASE_EVIDENCE.tsv'
DEC=R/'STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv'
RAW=[R/'STEP_09_SERP_RESULTS.tsv']+sorted(R.glob('STEP_09_SERP_R2_PROJECTION_RAW_PART_*.tsv'))
OUT=R/'STEP_13_EXISTING_SEARCH_EVIDENCE.tsv'
SUM=R/'STEP_13_EXISTING_SEARCH_CASE_SUMMARY.tsv'
QA=R/'STEP_13_EXISTING_SEARCH_EVIDENCE_QA.json'


def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(p,rows,fields):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
def qnorm(s):return re.sub(r'\s+',' ',(s or '').strip().lower())
def norm_url(v):
    v=(v or '').strip()
    if not v:return ''
    if not v.startswith(('http://','https://')):return ''
    p=urlsplit(v);path=(p.path or '/').rstrip('/') or '/'
    return f'https://{p.netloc.lower().removeprefix("www.")}{path}'
def is_target(domain,url):
    d=(domain or '').strip().lower().removeprefix('www.')
    if d=='okno-msk.ru' or d.endswith('.okno-msk.ru'):return True
    try:return urlsplit(url).netloc.lower().removeprefix('www.')=='okno-msk.ru'
    except:return False

def get_rank(r):
    for k in ('rank','position','pos'):
        v=(r.get(k) or '').strip()
        if v:return v
    return ''

cases=read(CASES);ph=read(PH);dec=read(DEC)
assert len(cases)==21 and len(dec)==75
case_by={r['case_id']:r for r in cases}
dec_by={qnorm(r['query']):r for r in dec}
raw_by=defaultdict(list)
raw_files=[]
for p in RAW:
    if not p.exists():continue
    raw_files.append(p.name)
    for r in read(p):
        q=qnorm(r.get('query_text') or r.get('query'))
        if q:raw_by[q].append(r)

# unique case/query from exact phrase evidence
cq=set()
for r in ph:
    q=qnorm(r['phrase'])
    if q in dec_by:cq.add((r['case_id'],q))
rows=[]
for cid,q in sorted(cq):
    c=case_by[cid];d=dec_by[q]
    candidate=set(norm_url(x) for x in c['candidate_urls'].split(';') if x)
    hits=[];cand_hits=[]
    for h in raw_by.get(q,[]):
        if is_target(h.get('domain',''),h.get('url','')):
            u=norm_url(h.get('url',''));rank=get_rank(h)
            if not u:continue
            hits.append((u,rank))
            if u in candidate:cand_hits.append((u,rank))
    # dedupe preserving rank/url combos
    hits=sorted(set(hits),key=lambda x:(int(x[1]) if str(x[1]).isdigit() else 9999,x[0]))
    cand_hits=sorted(set(cand_hits),key=lambda x:(int(x[1]) if str(x[1]).isdigit() else 9999,x[0]))
    rows.append({
      'case_id':cid,'query':q,'step09_probe_id':d['probe_id'],'observed_serp_job':d['observed_serp_job'],'dominant_result_type':d['dominant_result_type'],
      'candidate_urls':c['candidate_urls'],'target_domain_hits':';'.join(f'{u}@{rnk}' for u,rnk in hits),'target_domain_hit_count':len(hits),
      'candidate_url_hits':';'.join(f'{u}@{rnk}' for u,rnk in cand_hits),'candidate_url_hit_count':len(cand_hits),
      'multiple_candidate_urls_observed':'true' if len({u for u,_ in cand_hits})>=2 else 'false','evidence_origin':'PERSISTED_STEP09_DIRECT_SEARCH'})
write(OUT,rows,['case_id','query','step09_probe_id','observed_serp_job','dominant_result_type','candidate_urls','target_domain_hits','target_domain_hit_count','candidate_url_hits','candidate_url_hit_count','multiple_candidate_urls_observed','evidence_origin'])

by_case=defaultdict(list)
for r in rows:by_case[r['case_id']].append(r)
summ=[]
for c in cases:
    rr=by_case.get(c['case_id'],[])
    observed=sorted({u.split('@')[0] for r in rr for u in r['candidate_url_hits'].split(';') if u})
    multi=[r['query'] for r in rr if r['multiple_candidate_urls_observed']=='true']
    any_target=sum(int(r['target_domain_hit_count'])>0 for r in rr)
    any_candidate=sum(int(r['candidate_url_hit_count'])>0 for r in rr)
    summ.append({
      'case_id':c['case_id'],'query_family':c['query_family'],'materialization_state':c['query_family_materialization_state'],
      'persisted_direct_queries':len(rr),'queries_with_any_okno_msk_hit':any_target,'queries_with_candidate_url_hit':any_candidate,
      'candidate_urls_observed_in_persisted_search':';'.join(observed),'queries_with_multiple_candidate_urls_observed':';'.join(multi),
      'persisted_search_evidence_state':'DIRECT_STEP09_AVAILABLE' if rr else 'NO_EXACT_STEP09_QUERY_IN_CASE_PHRASES'})
write(SUM,summ,['case_id','query_family','materialization_state','persisted_direct_queries','queries_with_any_okno_msk_hit','queries_with_candidate_url_hit','candidate_urls_observed_in_persisted_search','queries_with_multiple_candidate_urls_observed','persisted_search_evidence_state'])
qa={'date':'2026-08-31','status':'STEP13_PERSISTED_SEARCH_EVIDENCE_JOINED','query_family_cases':len(cases),'case_query_direct_rows':len(rows),'cases_with_persisted_direct_search':sum(bool(by_case.get(c['case_id'])) for c in cases),'cases_without_persisted_direct_search':sum(not bool(by_case.get(c['case_id'])) for c in cases),'raw_files_used':raw_files,'provider_calls':0,'fresh_search_executed':False,'queries_with_multiple_candidate_urls_observed':sum(r['multiple_candidate_urls_observed']=='true' for r in rows)}
QA.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False,indent=2))
