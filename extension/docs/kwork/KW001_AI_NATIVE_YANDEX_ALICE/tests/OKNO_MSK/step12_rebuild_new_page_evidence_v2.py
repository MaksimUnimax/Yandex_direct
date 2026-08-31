import csv, json, statistics
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent
ASSIGN=ROOT/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv'
V1_SUM=ROOT/'STEP_12_NEW_PAGE_EVIDENCE.tsv'
V1_PH=ROOT/'STEP_12_NEW_PAGE_DEMAND_PHRASE_EVIDENCE.tsv'
OUT=ROOT/'STEP_12_NEW_PAGE_EVIDENCE_V2.tsv'
OUT_PH=ROOT/'STEP_12_NEW_PAGE_DEMAND_PHRASE_EVIDENCE_V2.tsv'
OUT_QA=ROOT/'STEP_12_NEW_PAGE_EVIDENCE_QA_V2.json'

CANDIDATES={
'PANORAMIC_WINDOWS_COMMERCIAL':(['PANORAMIC_WINDOWS_COMMERCIAL_CORE'],['PANORAMIC_WINDOW_TECH_SELECTION_INFO','PANORAMIC_OUTDOOR_GLAZING']),
'WINDOW_HARDWARE_GUIDE':(['WINDOW_HARDWARE_SELECTION_GUIDE'],['WINDOW_COMPONENT_SELECTION_INFO','WINDOW_HARDWARE_STANDARD_INFO']),
'PVC_WINDOW_INSTALLATION_DIY_GUIDE':(['PVC_WINDOW_INSTALLATION_DIY'],['WINDOW_INSTALLATION_MATERIALS_INFO']),
'PVC_WINDOW_REPAIR_DIY_GUIDE':(['PVC_WINDOW_REPAIR_DIY_GENERAL','PVC_WINDOW_ADJUSTMENT_DIY'],['WINDOW_HARDWARE_MAINTENANCE_INFO']),
'WINDOW_REPLACEMENT_SERVICE':(['WINDOW_REPLACEMENT_SERVICE'],[]),
}

def read(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(path,rows,fields):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)

assign=read(ASSIGN);v1sum={r['candidate_id']:r for r in read(V1_SUM)};v1ph=read(V1_PH)
if len(assign)!=2332:raise RuntimeError('V5 assignment mismatch')
unit_by_phrase={r['phrase']:r['final_structural_unit_id'] for r in assign}

# Reclassify V1 evidence rows by the accepted V5 unit membership. The evidence measurements themselves are preserved.
new_ph=[]
removed=[]
for r in v1ph:
    cid=r['candidate_id'];core,support=CANDIDATES[cid];uid=unit_by_phrase.get(r['phrase'],'')
    if uid in core: role='CORE'
    elif uid in support: role='SUPPORTING_NOT_CORE_DEMAND'
    else:
        role='REMOVED_FROM_CANDIDATE_BY_V5_SEMANTIC_CORRECTION';removed.append((cid,r['phrase'],uid))
    x=dict(r);x['structural_unit_id']=uid;x['evidence_role']=role;new_ph.append(x)
write(OUT_PH,new_ph,list(new_ph[0].keys()))

sum_rows=[]
for cid,(core_units,support_units) in CANDIDATES.items():
    base=v1sum[cid]
    core=[r for r in new_ph if r['candidate_id']==cid and r['evidence_role']=='CORE']
    support=[r for r in new_ph if r['candidate_id']==cid and r['evidence_role']=='SUPPORTING_NOT_CORE_DEMAND']
    counts=[int(float(r['wordstat_direct_result_count'])) for r in core if int(float(r['wordstat_direct_result_count']))>0]
    direct_search=[r for r in core if r['direct_search_probe_id']]
    assoc=sum(int(r['wordstat_step08_association_occurrences'])>0 and int(float(r['wordstat_direct_result_count']))==0 for r in core)
    no_count=sum(int(r['wordstat_step08_association_occurrences'])==0 and int(float(r['wordstat_direct_result_count']))==0 for r in core)
    top=sorted([(int(float(r['wordstat_direct_result_count'])),r['phrase'],r['wordstat_provenance']) for r in core if int(float(r['wordstat_direct_result_count']))>0],reverse=True)[:12]
    top_txt=' || '.join(f'{p}={n} [{prov}]' for n,p,prov in top)
    if len(counts)>=3 and max(counts or [0])>=100: demand='STRONG_DIRECT_WORDSTAT_SUPPORT'
    elif counts: demand='PARTIAL_DIRECT_WORDSTAT_SUPPORT'
    else:demand='NO_DIRECT_WORDSTAT_SUPPORT_IN_PERSISTED_SET'
    search_txt=' || '.join(f"{r['phrase']} -> {r['direct_search_observed_job']} / {r['direct_search_result_type']} / {r['direct_search_handoff']}" for r in direct_search)
    jobs=sorted({r['direct_search_observed_job'] for r in direct_search});types=sorted({r['direct_search_result_type'] for r in direct_search})
    search_verdict='DIRECT_SEARCH_EVIDENCE_AVAILABLE_FOR_CORE_PHRASES' if direct_search else 'NO_DIRECT_STEP09_CORE_QUERY'
    gap='NO_GAP_FOR_OBSERVED_CORE_QUERIES__DO_NOT_TRANSFER_TO_UNPROBED_PHRASES' if direct_search else 'MATERIAL_SEARCH_PAGE_BOUNDARY_NOT_DIRECTLY_PROBED'
    maturity='EVIDENCE_SUPPORTED_PENDING_ACTION_REEVALUATION' if direct_search else 'PROVISIONAL_PENDING_SEARCH_BOUNDARY'
    x=dict(base)
    x.update({
        'core_structural_units':';'.join(core_units),'supporting_structural_units':';'.join(support_units),
        'core_phrase_count_coverage':len(core),'supporting_phrase_count_not_used_as_core_demand':len(support),
        'core_phrases_with_direct_wordstat_result':len(counts),'core_phrases_association_only':assoc,'core_phrases_without_persisted_acquisition_count':no_count,
        'max_direct_wordstat_count_observed':max(counts or [0]),'median_direct_wordstat_count_observed':statistics.median(counts) if counts else 0,
        'top_direct_wordstat_evidence':top_txt,'wordstat_demand_verdict':demand,'direct_step09_core_queries':len(direct_search),'direct_step09_query_evidence':search_txt,
        'direct_search_jobs':';'.join(jobs),'direct_search_result_types':';'.join(types),'search_page_type_verdict':search_verdict,'search_boundary_gap':gap,'candidate_maturity_after_existing_evidence':maturity,
    })
    sum_rows.append(x)
write(OUT,sum_rows,list(sum_rows[0].keys()))

hw=next(r for r in sum_rows if r['candidate_id']=='WINDOW_HARDWARE_GUIDE')
qa={'status':'CANDIDATE_V2_READY_FOR_MANUAL_EVIDENCE_ACCEPTANCE','candidate_pages':5,'phrase_evidence_rows':len(new_ph),'removed_from_candidate_rows':len(removed),'removed_rows':[{'candidate_id':a,'phrase':b,'new_unit':c} for a,b,c in removed],'hardware_guide_core_phrases':int(hw['core_phrase_count_coverage']),'hardware_guide_direct_step09_core_queries':int(hw['direct_step09_core_queries']),'association_not_counted_as_direct_demand':True,'phrase_counts_not_summed_as_total_unique_demand':True,'step09_direct_query_only_no_transfer':True,'candidates_without_direct_step09_core_query':[r['candidate_id'] for r in sum_rows if int(r['direct_step09_core_queries'])==0],'defects_closed_by_script_alone':[],'defects_candidate_for_closure_after_manual_review':['D12-02','D12-03','D12-10'],'new_bridge_requests':0,'new_bridge_cost_rub':0.0}
if len(sum_rows)!=5 or len(removed)!=1 or removed[0][1]!='оконная фурнитура отзывы' or int(hw['direct_step09_core_queries'])!=0:qa['status']='FAIL'
OUT_QA.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False))
