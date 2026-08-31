import csv
from collections import defaultdict
from pathlib import Path
R=Path(__file__).resolve().parent
P=R/'STEP_12_D12_28_MEMBER_PHRASES_PACKET.tsv'
U=R/'STEP_12_D12_28_UNIT_REVIEW_PACKET.tsv'
O=R/'STEP_12_D12_28_UNIT_MEMBER_SUMMARY.tsv'
def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
p=read(P);u=read(U);by=defaultdict(list)
for r in p:by[r['structural_unit_id']].append(r['phrase'])
rows=[]
for r in u:
    uid=r['structural_unit_id'];phr=sorted(by[uid]);assert len(phr)==int(r['phrase_count'])
    rows.append({'structural_unit_id':uid,'phrase_count':r['phrase_count'],'old_action':r['structural_action'],'current_url':r['primary_page_candidate'],'user_task':r['user_task'],'member_phrases':' | '.join(phr)})
with O.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
print('D12_28_UNIT_MEMBER_SUMMARY_READY',len(rows),sum(len(by[r['structural_unit_id']]) for r in u))
