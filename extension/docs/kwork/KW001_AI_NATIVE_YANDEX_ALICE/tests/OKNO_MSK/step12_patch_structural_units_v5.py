import csv, json
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V4.tsv'
HIST=ROOT/'STEP_12_PHRASE_ACTION_MAP.tsv'
OUT_ASSIGN=ROOT/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv'
OUT_UNITS=ROOT/'STEP_12_STRUCTURAL_UNITS_V5.tsv'
OUT_CORR=ROOT/'STEP_12_STRUCTURAL_UNIT_CORRECTIONS_V5.tsv'
OUT_QA=ROOT/'STEP_12_STRUCTURAL_UNIT_CORRECTION_QA_V5.json'


def read(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(path,rows,fields):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)

rows=read(SRC);hist=read(HIST);hist_by={r['phrase']:r for r in hist}
if len(rows)!=2332: raise RuntimeError('V4 rows mismatch')

TARGET='оконная фурнитура отзывы'
matched=0
for r in rows:
    if r['phrase']==TARGET:
        assert r['final_structural_unit_id']=='WINDOW_HARDWARE_SELECTION_GUIDE'
        r['final_structural_unit_id']='WINDOW_HARDWARE_GENERIC_REVIEWS_INFO'
        r['final_unit_task']='read reviews/experience about window hardware in general'
        r['intent_type']='INFO'
        r['business_scope_state']='NO_STANDALONE_FIRST_PARTY'
        r['unit_page_role']='UNSERVABLE_NEUTRAL_REVIEW'
        r['primary_page_candidate']=''
        r['supporting_page']=''
        r['recommendation_maturity']='FINAL_WITHIN_STEP12_EVIDENCE'
        r['assignment_origin']='D12_02_REOPENED_DIRECT_SEARCH_CORRECTION'
        r['correction_reason']='Direct Step09 Search for this exact phrase showed WINDOW_HARDWARE_REVIEWS with REVIEWS_FORUM_INFORMATION / INFORMATIONAL_NON_LANDING. It is therefore not evidence for a general first-party selection guide and is separated as a generic reviews task.'
        matched+=1
if matched!=1: raise RuntimeError(f'target matches={matched}')

# Rebuild canonical unit summary.
groups=defaultdict(list)
for r in rows:
    if r['final_structural_unit_id']:groups[r['final_structural_unit_id']].append(r)
units=[]
for uid,rs in sorted(groups.items()):
    dims=['final_unit_task','intent_type','business_scope_state','unit_page_role','primary_page_candidate','supporting_page','recommendation_maturity']
    vals={k:sorted({x[k] for x in rs if x[k]}) for k in dims}
    incons={k:v for k,v in vals.items() if len(v)>1}
    first=rs[0]
    units.append({'structural_unit_id':uid,'phrase_count':len(rs),'source_effective_clusters':';'.join(sorted({x['original_effective_cluster_id'] for x in rs})),'user_task':first['final_unit_task'],'intent_type':first['intent_type'],'business_scope_state':first['business_scope_state'],'unit_page_role':first['unit_page_role'],'primary_page_candidate':first['primary_page_candidate'],'supporting_page':first['supporting_page'],'recommendation_maturity':first['recommendation_maturity'],'confidence':'PENDING_EVIDENCE_DERIVATION','assignment_origin_mix':';'.join(f'{k}:{v}' for k,v in sorted(Counter(x['assignment_origin'] for x in rs).items())),'unit_reason':first['correction_reason'],'inconsistent_unit_metadata_fields':len(incons),'inconsistent_metadata_detail':json.dumps(incons,ensure_ascii=False) if incons else ''})

corr=[]
for r in rows:
    if not r['original_effective_cluster_id']:continue
    h=hist_by[r['phrase']]
    changed=(r['final_structural_unit_id']!=r['original_effective_cluster_id'] or h['routing_override']=='true' or r['assignment_origin'] not in {'UNCHANGED_BASE_UNIT'})
    if changed:
        corr.append({'phrase':r['phrase'],'original_effective_cluster_id':r['original_effective_cluster_id'],'historical_step12_structural_unit_id':h['structural_unit_id'],'historical_step12_target':h['target_or_new_page'],'corrected_structural_unit_id':r['final_structural_unit_id'],'corrected_unit_task':r['final_unit_task'],'corrected_primary_page_candidate':r['primary_page_candidate'],'corrected_supporting_page':r['supporting_page'],'corrected_page_role':r['unit_page_role'],'corrected_business_scope_state':r['business_scope_state'],'recommendation_maturity':r['recommendation_maturity'],'correction_reason':r['correction_reason'],'correction_origin':r['assignment_origin'],'review_status':'CANDIDATE_V5_PENDING_REACCEPTANCE'})

write(OUT_ASSIGN,rows,list(rows[0].keys()));write(OUT_UNITS,units,list(units[0].keys()));write(OUT_CORR,corr,list(corr[0].keys()))
unit_bad=[u for u in units if u['inconsistent_unit_metadata_fields']]
selection=next(u for u in units if u['structural_unit_id']=='WINDOW_HARDWARE_SELECTION_GUIDE')
reviews=next(u for u in units if u['structural_unit_id']=='WINDOW_HARDWARE_GENERIC_REVIEWS_INFO')
qa={'status':'CANDIDATE_V5_READY_FOR_D12_02_REACCEPTANCE','source_rows':len(rows),'search_required_rows':sum(not r['final_structural_unit_id'] for r in rows),'structural_units':len(units),'correction_rows':len(corr),'residual_hardware_review_rows_corrected':matched,'hardware_selection_guide_phrase_count_after_correction':selection['phrase_count'],'hardware_generic_reviews_phrase_count':reviews['phrase_count'],'unit_metadata_inconsistency_rows':len(unit_bad),'default_high_confidence_rows':0,'defects_closed_by_script_alone':[],'defects_candidate_for_reacceptance':['D12-02']}
if len(rows)!=2332 or qa['search_required_rows']!=19 or unit_bad or matched!=1: qa['status']='FAIL'
OUT_QA.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False))
