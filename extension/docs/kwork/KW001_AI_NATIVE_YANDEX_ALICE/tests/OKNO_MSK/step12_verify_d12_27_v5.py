import csv,json,subprocess,sys
from collections import Counter
from pathlib import Path

R=Path(__file__).resolve().parent
SRC=R/'step12_verify_third_audit_v4.py'
RES=R/'STEP_12_D12_27_PHRASE_RESOLUTIONS.tsv'
A6=R/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V6.tsv'
V5=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V5.tsv'
PM=R/'STEP_12_PHRASE_ACTION_MAP_FINAL_V5.tsv'
RECHECK=R/'STEP_12_THIRD_AUDIT_STRONG_FIT_PAGE_RECHECK.tsv'
OUT=R/'STEP_12_D12_27_INDEPENDENT_QA.json'
FIND=R/'STEP_12_D12_27_QA_FINDINGS.tsv'


def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))

# Run the previously independent verifier against V5/V6 outputs.
text=SRC.read_text(encoding='utf-8')
repls={
"V4=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V4.tsv'":"V4=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V5.tsv'",
"ASSIGN=R/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv'":"ASSIGN=R/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V6.tsv'",
"LINKS=R/'STEP_12_INTERNAL_LINK_ACTIONS.tsv'":"LINKS=R/'STEP_12_INTERNAL_LINK_ACTIONS_V5.tsv'",
"PAIRS=R/'STEP_12_STEP13_CANDIDATE_PAIRS_V4.tsv'":"PAIRS=R/'STEP_12_STEP13_CANDIDATE_PAIRS_V5.tsv'",
"PMAP=R/'STEP_12_PHRASE_ACTION_MAP_FINAL_V4.tsv'":"PMAP=R/'STEP_12_PHRASE_ACTION_MAP_FINAL_V5.tsv'",
"OUT=R/'STEP_12_THIRD_AUDIT_INDEPENDENT_QA.json'":"OUT=R/'STEP_12_D12_27_BASE_INDEPENDENT_QA.json'",
"FIND=R/'STEP_12_THIRD_AUDIT_QA_FINDINGS.tsv'":"FIND=R/'STEP_12_D12_27_BASE_QA_FINDINGS.tsv'",
"STEP12_THIRD_AUDIT_V4_INDEPENDENT_PASS":"STEP12_D12_27_V5_BASE_INDEPENDENT_PASS",
"STEP12_THIRD_AUDIT_V4_INDEPENDENT_FAIL":"STEP12_D12_27_V5_BASE_INDEPENDENT_FAIL",
}
for old,new in repls.items():
    assert old in text,old
    text=text.replace(old,new)
tmp=R/'_tmp_step12_d12_27_v5_verifier.py';tmp.write_text(text,encoding='utf-8')
try:subprocess.run([sys.executable,str(tmp)],check=True)
finally:
    if tmp.exists():tmp.unlink()
base=json.loads((R/'STEP_12_D12_27_BASE_INDEPENDENT_QA.json').read_text(encoding='utf-8'))
find=read(R/'STEP_12_D12_27_BASE_QA_FINDINGS.tsv')

# D12-27 exact independent acceptance checks.
res=read(RES);a6=read(A6);v5=read(V5);pm=read(PM);recheck=read(RECHECK)
by_phrase={}
for r in a6:
    assert r['phrase'] not in by_phrase,('duplicate assignment phrase',r['phrase'])
    by_phrase[r['phrase']]=r
pm_by={}
for r in pm:
    assert r['phrase'] not in pm_by,('duplicate phrase map phrase',r['phrase'])
    pm_by[r['phrase']]=r
v5by={r['structural_unit_id']:r for r in v5}
extra=[]
def fail(cid,msg):extra.append({'check_id':cid,'finding':msg})
if len(res)!=65:fail('D12-27',f'resolution rows={len(res)}')
reassigned=0
for rr in res:
    ph=rr['phrase'];new=rr['corrected_structural_unit_id'];old=rr['old_structural_unit_id']
    if ph not in by_phrase:fail('D12-27',f'missing assignment {ph}');continue
    if by_phrase[ph].get('final_structural_unit_id')!=new:fail('D12-27',f'assignment mismatch {ph}')
    if ph not in pm_by or pm_by[ph].get('final_structural_unit_id')!=new:fail('D12-27',f'phrase-map mismatch {ph}')
    if new not in v5by:fail('D12-27',f'unknown target unit {new}')
    if new!=old:reassigned+=1
# Known mixed parent units now contain only rows explicitly retained there by the review ledger.
expected_french={r['phrase'] for r in res if r['corrected_structural_unit_id']=='FRENCH_WINDOWS_COMMERCIAL'}
actual_french={r['phrase'] for r in a6 if r.get('final_structural_unit_id')=='FRENCH_WINDOWS_COMMERCIAL'}
if expected_french!=actual_french:fail('D12-27',f'French-core mismatch expected={len(expected_french)} actual={len(actual_french)}')
expected_acc={r['phrase'] for r in res if r['corrected_structural_unit_id']=='WINDOW_ACCESSORIES_GENERAL'}
actual_acc={r['phrase'] for r in a6 if r.get('final_structural_unit_id')=='WINDOW_ACCESSORIES_GENERAL'}
if expected_acc!=actual_acc:fail('D12-27',f'accessory-core mismatch expected={len(expected_acc)} actual={len(actual_acc)}')
# All active structural units remain non-empty and phrase_count/source membership are recomputed from V6.
counts=Counter(r.get('final_structural_unit_id','') for r in a6 if r.get('final_structural_unit_id',''))
zero=sorted(set(v5by)-set(counts))
if zero:fail('D12-27',f'zero-member units={zero}')
for uid,r in v5by.items():
    if int(r['phrase_count'])!=counts[uid]:fail('D12-27',f'{uid} phrase_count {r["phrase_count"]}!={counts[uid]}')
# Six current-page rechecks must be reflected as structural KEEP without pretending performance was audited.
for x in recheck:
    uid=x['structural_unit_id'];r=v5by.get(uid)
    if not r:fail('D12-27',f'missing strong-fit unit {uid}');continue
    if r['structural_action']!='KEEP_EXISTING_STRUCTURE':fail('D12-27',f'{uid} not KEEP')
    if r['gap_type']!='NONE':fail('D12-27',f'{uid} gap={r["gap_type"]}')
    if r['performance_evidence_state']!='NOT_AVAILABLE_IN_BASE_SCOPE_NO_WEBMASTER_METRIKA':fail('D12-27',f'{uid} performance overclaim')
    if 'NOT_ASSESSED' not in r['optimization_readiness']:fail('D12-27',f'{uid} optimization overclaim')

allfind=find+extra
fields=['check_id','finding']
with FIND.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(allfind)
qa=dict(base)
qa.update({
 'status':'STEP12_D12_27_V5_INDEPENDENT_PASS' if not allfind else 'STEP12_D12_27_V5_INDEPENDENT_FAIL',
 'findings':len(allfind),
 'd12_27_reviewed_phrases':len(res),
 'd12_27_reassigned_phrases':reassigned,
 'french_commercial_core_rows':len(actual_french),
 'general_accessory_core_rows':len(actual_acc),
 'zero_member_structural_units':zero,
 'strong_fit_recheck_rows':len(recheck),
 'strong_fit_keep_verified':sum(v5by.get(x['structural_unit_id'],{}).get('structural_action')=='KEEP_EXISTING_STRUCTURE' for x in recheck),
 'verification_origin':'INDEPENDENT_V4_METHOD_RECOMPUTATION_PLUS_EXACT_D12_27_65_PHRASE_AND_STRONG_FIT_ASSERTIONS'
})
OUT.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False,indent=2))
