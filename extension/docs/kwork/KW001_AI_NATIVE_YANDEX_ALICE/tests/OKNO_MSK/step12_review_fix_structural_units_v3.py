import csv, json
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent
V2=ROOT/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V2.tsv'
HIST=ROOT/'STEP_12_PHRASE_ACTION_MAP.tsv'
STEP11=ROOT/'STEP_11_PHRASE_PAGE_MAP.tsv'
OUT_ASSIGN=ROOT/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V3.tsv'
OUT_CORR=ROOT/'STEP_12_STRUCTURAL_UNIT_CORRECTIONS_V3.tsv'
OUT_UNITS=ROOT/'STEP_12_STRUCTURAL_UNITS_V3.tsv'
OUT_SALVAGE=ROOT/'STEP_12_NO_PAGE_OUTSIDE_SALVAGE_REVIEW_V3.tsv'
OUT_QA=ROOT/'STEP_12_STRUCTURAL_UNIT_CORRECTION_QA_V3.json'


def read(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(path,rows,fields):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)

assign=read(V2);hist=read(HIST);step11=read(STEP11)
hist_by={r['phrase']:r for r in hist}; step11_by={r['phrase']:r for r in step11}
cluster_action={}
for r in hist:
    cid=r['effective_cluster_id']
    if cid and r['cluster_structural_action'] and cid not in cluster_action: cluster_action[cid]=r['cluster_structural_action']

UNVERIFIED_SERVICE={'OPEN_BALCONY_FINISHING','PVC_DOOR_REPAIR_SERVICE','PVC_DOOR_REPLACEMENT_SERVICE','MOSQUITO_NET_REPAIR_SERVICE','WINDOWSILL_REPAIR_SERVICE'}
UNVERIFIED_PRODUCT={'ROOF_WINDOWS_COMMERCIAL','SOFT_WINDOWS_COMMERCIAL','TIMBER_ALUMINIUM_WINDOWS_COMMERCIAL','WOOD_WINDOWS_COMMERCIAL'}

fixed=[]
for r in assign:
    phrase=r['phrase']; cid=r['original_effective_cluster_id']; act=cluster_action.get(cid,'')
    if not cid: continue
    if r['assignment_origin']=='UNCHANGED_BASE_UNIT' and act=='OUTSIDE_SCOPE_NO_ACTION':
        r['business_scope_state']='OUTSIDE_SCOPE'; r['unit_page_role']='OUTSIDE'; r['primary_page_candidate']='';r['supporting_page']='';r['recommendation_maturity']='FINAL_WITHIN_STEP12_EVIDENCE';r['assignment_origin']='OUTSIDE_PRESERVED_AFTER_READBACK_FIX';r['correction_reason']='No explicit phrase-level salvage evidence was found; preserve the historical outside-scope state rather than converting it to IN_SCOPE by default.';fixed.append(phrase)
    elif r['assignment_origin']=='UNCHANGED_BASE_UNIT' and act=='NO_STANDALONE_PAGE':
        if cid in UNVERIFIED_SERVICE:
            state='NO_STANDALONE_UNVERIFIED_BUSINESS'; role='NO_STANDALONE_UNVERIFIED_SERVICE'; reason='No explicit salvage rule applies and the service is not verified as a current standalone offer; preserve no-page state.'
        elif cid in UNVERIFIED_PRODUCT:
            state='NO_STANDALONE_UNVERIFIED_BUSINESS'; role='NO_STANDALONE_UNVERIFIED_PRODUCT'; reason='No explicit salvage rule applies and the product family is not verified as a current offer; preserve no-page state.'
        else:
            state='NO_STANDALONE_FIRST_PARTY'; role='NO_STANDALONE_PRESERVED'; reason='No explicit salvage evidence applies; preserve historical no-standalone state pending any separately materialized subtask correction.'
        r['business_scope_state']=state;r['unit_page_role']=role;r['primary_page_candidate']='';r['supporting_page']='';r['recommendation_maturity']='FINAL_WITHIN_STEP12_EVIDENCE';r['assignment_origin']='NO_PAGE_PRESERVED_AFTER_READBACK_FIX';r['correction_reason']=reason;fixed.append(phrase)

# Rebuild corrections against historical/upstream truth.
corr=[]
for r in assign:
    phrase=r['phrase']; cid=r['original_effective_cluster_id']; h=hist_by[phrase]
    if not cid: continue
    changed=(r['final_structural_unit_id']!=cid or h['routing_override']=='true' or r['assignment_origin'] not in {'UNCHANGED_BASE_UNIT'})
    if changed:
        corr.append({
            'phrase':phrase,'original_effective_cluster_id':cid,'historical_step12_structural_unit_id':h['structural_unit_id'],'historical_step12_target':h['target_or_new_page'],'corrected_structural_unit_id':r['final_structural_unit_id'],'corrected_unit_task':r['final_unit_task'],'corrected_primary_page_candidate':r['primary_page_candidate'],'corrected_supporting_page':r['supporting_page'],'corrected_page_role':r['unit_page_role'],'corrected_business_scope_state':r['business_scope_state'],'correction_reason':r['correction_reason'],'correction_origin':r['assignment_origin'],'review_status':'CANDIDATE_V3_PENDING_FULL_READBACK_REVIEW'
        })

# Rebuild unit summary from explicit phrase assignments.
groups=defaultdict(list)
for r in assign:
    if r['final_structural_unit_id']:groups[r['final_structural_unit_id']].append(r)
units=[]
for uid,rows in sorted(groups.items()):
    first=rows[0]
    vals=lambda k: sorted({x[k] for x in rows if x[k]})
    tasks=vals('final_unit_task');roles=vals('unit_page_role');prim=vals('primary_page_candidate');supp=vals('supporting_page');matur=vals('recommendation_maturity');states=vals('business_scope_state');intents=vals('intent_type')
    inconsistent=sum(len(x)>1 for x in [tasks,roles,prim,supp,matur,states,intents])
    units.append({
        'structural_unit_id':uid,'phrase_count':len(rows),'source_effective_clusters':';'.join(sorted({x['original_effective_cluster_id'] for x in rows})),'user_task':' || '.join(tasks),'intent_type':' || '.join(intents),'business_scope_state':' || '.join(states),'unit_page_role':' || '.join(roles),'primary_page_candidate':' || '.join(prim),'supporting_page':' || '.join(supp),'recommendation_maturity':' || '.join(matur),'confidence':'PENDING_EVIDENCE_DERIVATION','assignment_origin_mix':';'.join(f'{k}:{v}' for k,v in sorted(Counter(x['assignment_origin'] for x in rows).items())),'unit_reason':' || '.join(vals('correction_reason')),'inconsistent_unit_metadata_fields':inconsistent
    })

# Rebuild no-page/outside review with correct disposition semantics.
salvage=[]
for r in assign:
    cid=r['original_effective_cluster_id'];
    if not cid: continue
    act=cluster_action.get(cid,'')
    if act not in {'NO_STANDALONE_PAGE','OUTSIDE_SCOPE_NO_ACTION'}:continue
    state=r['business_scope_state']
    if state=='OUTSIDE_SCOPE': disp='OUTSIDE_CONFIRMED'
    elif state.startswith('NO_STANDALONE'): disp='NO_STANDALONE_CONFIRMED'
    elif state.startswith('DEFERRED'): disp='EXPLICITLY_DEFERRED'
    else: disp='SALVAGED_TO_IN_SCOPE_UNIT'
    salvage.append({
        'phrase':r['phrase'],'historical_cluster_id':cid,'historical_cluster_action':act,'final_structural_unit_id':r['final_structural_unit_id'],'final_business_scope_state':state,'final_page_role':r['unit_page_role'],'primary_page_candidate':r['primary_page_candidate'],'supporting_page':r['supporting_page'],'review_disposition':disp,'review_reason':r['correction_reason'],'review_status':'CANDIDATE_V3_PENDING_FULL_READBACK_REVIEW'
    })

write(OUT_ASSIGN,assign,list(assign[0].keys()));write(OUT_CORR,corr,list(corr[0].keys()));write(OUT_UNITS,units,list(units[0].keys()));write(OUT_SALVAGE,salvage,list(salvage[0].keys()))

# Readback-fix QA: no old OUTSIDE/NO_PAGE row may silently become in-scope through unchanged fallback.
outside_bad=[];nopage_bad=[]
for r in assign:
    cid=r['original_effective_cluster_id']; act=cluster_action.get(cid,'')
    if act=='OUTSIDE_SCOPE_NO_ACTION' and r['business_scope_state']!='OUTSIDE_SCOPE' and r['assignment_origin'] not in {'OUTSIDE_NO_PAGE_SALVAGE_REVIEW','MIXED_UNIT_CORRECTION'}:
        outside_bad.append(r['phrase'])
    if act=='NO_STANDALONE_PAGE' and r['assignment_origin']=='UNCHANGED_BASE_UNIT':
        nopage_bad.append(r['phrase'])

qa={
    'status':'CANDIDATE_V3_READBACK_FIX_READY_FOR_SEMANTIC_REVIEW',
    'source_rows':len(assign),'search_required_rows':sum(not r['final_structural_unit_id'] for r in assign),'structural_units':len(units),'correction_rows':len(corr),'readback_fallback_rows_fixed':len(fixed),'historical_no_page_or_outside_review_rows':len(salvage),'salvaged_to_in_scope_units':sum(r['review_disposition']=='SALVAGED_TO_IN_SCOPE_UNIT' for r in salvage),'explicitly_deferred_rows':sum(r['review_disposition']=='EXPLICITLY_DEFERRED' for r in salvage),'outside_confirmed_rows':sum(r['review_disposition']=='OUTSIDE_CONFIRMED' for r in salvage),'no_standalone_confirmed_rows':sum(r['review_disposition']=='NO_STANDALONE_CONFIRMED' for r in salvage),'historical_outside_rows_silently_in_scope_without_explicit_salvage':len(outside_bad),'historical_no_page_rows_left_as_unchanged_in_scope_base':len(nopage_bad),'unit_metadata_inconsistency_rows':sum(u['inconsistent_unit_metadata_fields']>0 for u in units),'default_high_confidence_rows':0,'defects_closed_by_script_alone':[],'defects_candidate_for_closure_after_semantic_readback':['D12-01','D12-02','D12-08','D12-09','D12-12']
}
if len(assign)!=2332 or qa['search_required_rows']!=19 or outside_bad or nopage_bad:
    qa['status']='FAIL'
OUT_QA.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False))
