import csv,json,subprocess,sys
from collections import Counter,defaultdict
from pathlib import Path

R=Path(__file__).resolve().parent
A5=R/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv'
A6=R/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V6.tsv'
RES=R/'STEP_12_D12_27_PHRASE_RESOLUTIONS.tsv'
V3=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V3.tsv'
BASE=R/'STEP_12_D12_27_BASE_ACTIONS.tsv'
RECHECK=R/'STEP_12_THIRD_AUDIT_STRONG_FIT_PAGE_RECHECK.tsv'
SRC=R/'step12_build_third_audit_v4.py'


def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(p,rows,fields=None):
    if fields is None: fields=list(rows[0].keys()) if rows else []
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)

# 1. Apply all 65 exact phrase resolutions to the canonical assignment ledger.
a5=read(A5);res=read(RES)
assert len(a5)==2332 and len(res)==65
by_phrase=defaultdict(list)
for i,r in enumerate(a5):by_phrase[r['phrase']].append(i)
res_by={r['phrase']:r for r in res}
assert len(res_by)==65
changed=0
for phrase,rr in res_by.items():
    idxs=by_phrase.get(phrase,[]);assert len(idxs)==1,(phrase,len(idxs))
    i=idxs[0];row=a5[i]
    assert row.get('final_structural_unit_id','')==rr['old_structural_unit_id'],(phrase,row.get('final_structural_unit_id'),rr['old_structural_unit_id'])
    if rr['corrected_structural_unit_id']!=rr['old_structural_unit_id']:changed+=1
    row['final_structural_unit_id']=rr['corrected_structural_unit_id']
    if 'assignment_origin' in row:
        row['assignment_origin']='D12_27_EXPLICIT_PHRASE_REVIEW' if rr['corrected_structural_unit_id']!=rr['old_structural_unit_id'] else row.get('assignment_origin','')
    if 'correction_reason' in row and rr['corrected_structural_unit_id']!=rr['old_structural_unit_id']:
        row['correction_reason']=rr['decision_reason']
write(A6,a5,list(a5[0].keys()))

# 2. Rebuild action base from V3, using V6 membership and six fresh current-page rechecks.
v3=read(V3);recheck=read(RECHECK)
assert len(v3)==160 and len(recheck)==6
uids={r['structural_unit_id'] for r in v3}
assert all(r['corrected_structural_unit_id'] in uids for r in res)
counts=Counter();sources=defaultdict(set)
for a in a5:
    uid=(a.get('final_structural_unit_id') or '').strip()
    if uid:
        counts[uid]+=1
        src=(a.get('original_effective_cluster_id') or '').strip()
        if src:sources[uid].add(src)
assert sum(counts.values())==2313
zero_units=sorted(uids-set(counts))
assert not zero_units,zero_units
rb={r['structural_unit_id']:r for r in recheck}
assert len(rb)==6
base=[]
for src in v3:
    r=dict(src);uid=r['structural_unit_id']
    r['phrase_count']=str(counts[uid])
    r['source_effective_clusters']=';'.join(sorted(sources[uid]))
    if uid in rb:
        x=rb[uid]
        r['structural_action']=x['corrected_structural_action']
        r['primary_page_candidate']=x['current_url']
        r['current_page_fit']='STRONG_EXISTING_PAGE_FIT'
        r['fresh_site_check_status']='CURRENT_FIRST_PARTY_PAGE_RECHECK_2026_08_31'
        r['second_audit_correction_origin']='THIRD_AUDIT_STRONG_FIT_CURRENT_PAGE_RECHECK'
        r['confidence_downgrade_reason']='Fresh current-page recheck shows the existing owner already visibly serves the accepted structural task. KEEP is structural-only; account performance/content optimization remains unassessed in base scope.'
    base.append(r)
write(BASE,base,list(base[0].keys()))

# 3. Execute the already independently-tested V4 logic with corrected V6/base inputs and V5 outputs.
text=SRC.read_text(encoding='utf-8')
repls={
"V3=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V3.tsv'":"V3=R/'STEP_12_D12_27_BASE_ACTIONS.tsv'",
"ASSIGN=R/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv'":"ASSIGN=R/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V6.tsv'",
"OUT=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V4.tsv'":"OUT=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V5.tsv'",
"OUT_MAP=R/'STEP_12_PHRASE_ACTION_MAP_FINAL_V4.tsv'":"OUT_MAP=R/'STEP_12_PHRASE_ACTION_MAP_FINAL_V5.tsv'",
"OUT_LINKS=R/'STEP_12_INTERNAL_LINK_ACTIONS.tsv'":"OUT_LINKS=R/'STEP_12_INTERNAL_LINK_ACTIONS_V5.tsv'",
"OUT_PAIRS=R/'STEP_12_STEP13_CANDIDATE_PAIRS_V4.tsv'":"OUT_PAIRS=R/'STEP_12_STEP13_CANDIDATE_PAIRS_V5.tsv'",
"OUT_QA=R/'STEP_12_THIRD_AUDIT_GENERATOR_QA.json'":"OUT_QA=R/'STEP_12_D12_27_GENERATOR_QA.json'",
"f'V4P{i:04d}'":"f'V5P{i:04d}'",
"DETERMINISTIC_FROM_THIRD_AUDIT_CURRENT_ROUTING_GRAPH_V4":"DETERMINISTIC_FROM_D12_27_CORRECTED_ROUTING_GRAPH_V5",
"STEP12_THIRD_EXTERNAL_METHOD_AUDIT_V4":"STEP12_D12_27_CORRECTED_V5",
"STEP12_THIRD_AUDIT_V4_CANDIDATE_READY_FOR_INDEPENDENT_QA":"STEP12_D12_27_V5_CANDIDATE_READY_FOR_INDEPENDENT_QA",
}
for old,new in repls.items():
    assert old in text,old
    text=text.replace(old,new)
tmp=R/'_tmp_step12_d12_27_v5_engine.py';tmp.write_text(text,encoding='utf-8')
try:subprocess.run([sys.executable,str(tmp)],cwd=R.parent.parent.parent.parent.parent.parent,check=True)
finally:
    if tmp.exists():tmp.unlink()

# 4. Strengthen the six rechecked rows with direct fresh evidence after the generic engine pass.
v5=read(R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V5.tsv')
v5by={r['structural_unit_id']:r for r in v5}
for uid,x in rb.items():
    r=v5by[uid]
    assert r['structural_action']=='KEEP_EXISTING_STRUCTURE'
    r['gap_type']='NONE'
    r['gap_evidence']=x['current_evidence']+' Structural KEEP does not certify account performance/content optimization because Webmaster/Metrika are outside base scope.'
    r['current_page_fit']='STRONG_EXISTING_PAGE_FIT'
    r['fresh_site_check_status']='CURRENT_FIRST_PARTY_PAGE_RECHECK_2026_08_31'
    r['optimization_readiness']='STRUCTURAL_OWNER_CONFIRMED__CONTENT_PERFORMANCE_NOT_ASSESSED'
write(R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V5.tsv',v5,list(v5[0].keys()))

qa=json.loads((R/'STEP_12_D12_27_GENERATOR_QA.json').read_text(encoding='utf-8'))
qa.update({
 'd12_27_reviewed_phrases':len(res),
 'd12_27_reassigned_phrases':changed,
 'assignment_v6_rows':len(a5),
 'assigned_v6_rows':sum(counts.values()),
 'zero_member_structural_units':zero_units,
 'strong_fit_recheck_rows':len(recheck),
 'strong_fit_keep_rows':sum(v5by[u]['structural_action']=='KEEP_EXISTING_STRUCTURE' for u in rb),
 'build_origin':'V4_PROVEN_LOGIC_PLUS_D12_27_EXACT_PHRASE_RESOLUTIONS_AND_STRONG_FIT_RECHECK'
})
(R/'STEP_12_D12_27_GENERATOR_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False,indent=2))
