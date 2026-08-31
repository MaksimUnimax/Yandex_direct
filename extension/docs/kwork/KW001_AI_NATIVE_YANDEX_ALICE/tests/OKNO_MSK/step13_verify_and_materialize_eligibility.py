import csv,json
from collections import Counter
from pathlib import Path

R=Path(__file__).resolve().parent
PAIR=R/'STEP_13_PAIR_INPUT_NORMALIZED.tsv'
MAN=R/'STEP_13_PAIR_ELIGIBILITY_MANUAL_RESOLUTIONS.tsv'
OUT=R/'STEP_13_PAIR_ELIGIBILITY.tsv'
QA=R/'STEP_13_PAIR_ELIGIBILITY_QA.json'


def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(p,rows,fields):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)

pairs=read(PAIR);man=read(MAN)
assert len(pairs)==195 and len(man)==195
pids=[r['pair_id'] for r in pairs];mids=[r['pair_id'] for r in man]
assert len(set(pids))==195 and len(set(mids))==195
assert set(pids)==set(mids)
allowed={'NORMAL_HIERARCHICAL_OR_SUPPORTING','NORMAL_DISTINCT_OBJECT_OR_TASK','NORMAL_DISTINCT_INTENT','NORMAL_MIXED_INTENT','SURVIVES_TO_QUERY_FAMILY'}
assert not [r for r in man if r['eligibility_class'] not in allowed]
assert not [r for r in man if not r['manual_reason'].strip()]
by={r['pair_id']:r for r in man}
out=[]
for p in pairs:
    m=by[p['pair_id']]
    x=dict(p)
    x.update({
      'eligibility_class':m['eligibility_class'],
      'eligibility_reason':m['manual_reason'],
      'current_page_evidence_state':m['current_page_evidence_state'],
      'fresh_search_required_at_eligibility_stage':'false' if m['eligibility_class']!='SURVIVES_TO_QUERY_FAMILY' else 'UNDECIDED_REUSE_EXISTING_SEARCH_FIRST'
    })
    out.append(x)
fields=list(out[0].keys());write(OUT,out,fields)
counts=Counter(r['eligibility_class'] for r in man)
qa={
 'date':'2026-08-31','status':'STEP13_PAIR_ELIGIBILITY_ACCOUNTING_PASS','input_pairs':len(pairs),'manual_decisions':len(man),
 'materialized_rows':len(out),'unique_input_pair_ids':len(set(pids)),'unique_manual_pair_ids':len(set(mids)),
 'silent_pair_drops':len(set(pids)-set(mids)),'extra_pair_ids':len(set(mids)-set(pids)),
 'class_counts':dict(sorted(counts.items())),'surviving_pairs':counts['SURVIVES_TO_QUERY_FAMILY'],
 'closed_without_fresh_search':len(pairs)-counts['SURVIVES_TO_QUERY_FAMILY'],'provider_calls':0,'step13_search_executed':False,
 'semantic_origin':'MANUAL_PAIR_REVIEW_AGAINST_47_URL_CURRENT_PAGE_ROLE_LEDGER__SCRIPT_CHECKS_ACCOUNTING_ONLY'
}
QA.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False,indent=2))
