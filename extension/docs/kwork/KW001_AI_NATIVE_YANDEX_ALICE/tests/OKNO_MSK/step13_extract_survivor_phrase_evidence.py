import csv,json
from collections import defaultdict
from pathlib import Path

R=Path(__file__).resolve().parent
EL=R/'STEP_13_PAIR_ELIGIBILITY_MANUAL_RESOLUTIONS.tsv'
PAIR=R/'STEP_13_PAIR_INPUT_NORMALIZED.tsv'
ASSIGN=R/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V7.tsv'
OUT=R/'STEP_13_SURVIVOR_PHRASE_EVIDENCE.tsv'
QA=R/'STEP_13_SURVIVOR_PHRASE_EVIDENCE_QA.json'


def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(p,rows,fields):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)

el=read(EL);pairs=read(PAIR);assign=read(ASSIGN)
assert len(el)==195 and len(pairs)==195 and len(assign)==2332
surv={r['pair_id'] for r in el if r['eligibility_class']=='SURVIVES_TO_QUERY_FAMILY'}
assert len(surv)==27,len(surv)
by_pair={r['pair_id']:r for r in pairs}
phrases=defaultdict(list)
for r in assign:
    uid=(r.get('final_structural_unit_id') or '').strip()
    if uid:phrases[uid].append(r['phrase'])
rows=[]
for pid in sorted(surv):
    p=by_pair[pid]
    units=[x for x in p['relation_structural_units'].split(';') if x]
    seen=set()
    for uid in units:
        for ph in phrases.get(uid,[]):
            k=(uid,ph)
            if k in seen:continue
            seen.add(k)
            rows.append({'pair_id':pid,'page_a':p['page_a'],'page_b':p['page_b'],'structural_unit_id':uid,'phrase':ph})
write(OUT,rows,['pair_id','page_a','page_b','structural_unit_id','phrase'])
qa={'date':'2026-08-31','status':'STEP13_SURVIVOR_PHRASE_EVIDENCE_READY','surviving_pairs':len(surv),'evidence_rows':len(rows),'pairs_with_evidence':len({r['pair_id'] for r in rows}),'provider_calls':0,'step13_search_executed':False}
assert qa['pairs_with_evidence']==27
QA.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False,indent=2))
