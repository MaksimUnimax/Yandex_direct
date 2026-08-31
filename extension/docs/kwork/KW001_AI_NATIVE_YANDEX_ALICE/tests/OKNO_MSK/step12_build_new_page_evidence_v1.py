import csv, json, statistics
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent
ASSIGN=ROOT/'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V4.tsv'
STEP08=ROOT/'STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv'
STEP09=ROOT/'STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv'
OUT=ROOT/'STEP_12_NEW_PAGE_EVIDENCE.tsv'
OUT_PHRASES=ROOT/'STEP_12_NEW_PAGE_DEMAND_PHRASE_EVIDENCE.tsv'
OUT_QA=ROOT/'STEP_12_NEW_PAGE_EVIDENCE_QA.json'

CANDIDATES={
    'PANORAMIC_WINDOWS_COMMERCIAL': {
        'page':'PROPOSED_NEW:/panoramnye-okna/',
        'core_units':['PANORAMIC_WINDOWS_COMMERCIAL_CORE'],
        'support_units':['PANORAMIC_WINDOW_TECH_SELECTION_INFO','PANORAMIC_OUTDOOR_GLAZING'],
        'page_kind':'COMMERCIAL',
        'business_truth':'VERIFIED_CATEGORY_ADJACENT_TO_CURRENT_WINDOW_GLAZING_OFFER',
        'current_alternative':'Existing French/balcony/veranda/informational pages are narrower by object/form; no broad commercial panoramic owner was verified in Step 11.',
    },
    'WINDOW_HARDWARE_GUIDE': {
        'page':'PROPOSED_NEW:/stati/okonnaya-furnitura-vidy-brendy-kak-vybrat/',
        'core_units':['WINDOW_HARDWARE_SELECTION_GUIDE'],
        'support_units':['WINDOW_COMPONENT_SELECTION_INFO','WINDOW_HARDWARE_STANDARD_INFO'],
        'page_kind':'INFORMATIONAL',
        'business_truth':'VERIFIED_ADJACENT_EXPERTISE_AND_ACCESSORY/REPAIR_CONTEXT',
        'current_alternative':'Hardware information is fragmented across accessory/product/repair pages; broad first-party guide owner not verified.',
    },
    'PVC_WINDOW_INSTALLATION_DIY_GUIDE': {
        'page':'PROPOSED_NEW:/stati/ustanovka-plastikovyh-okon-svoimi-rukami/',
        'core_units':['PVC_WINDOW_INSTALLATION_DIY'],
        'support_units':['WINDOW_INSTALLATION_MATERIALS_INFO'],
        'page_kind':'INFORMATIONAL',
        'business_truth':'VERIFIED_EXPERTISE_FROM_CURRENT_PROFESSIONAL_INSTALLATION_OFFER',
        'current_alternative':'Current professional installation page does not serve a full DIY instruction task.',
    },
    'PVC_WINDOW_REPAIR_DIY_GUIDE': {
        'page':'PROPOSED_NEW:/stati/remont-i-regulirovka-plastikovyh-okon-svoimi-rukami/',
        'core_units':['PVC_WINDOW_REPAIR_DIY_GENERAL','PVC_WINDOW_ADJUSTMENT_DIY'],
        'support_units':['WINDOW_HARDWARE_MAINTENANCE_INFO'],
        'page_kind':'INFORMATIONAL',
        'business_truth':'VERIFIED_EXPERTISE_FROM_CURRENT_PROFESSIONAL_REPAIR_OFFER',
        'current_alternative':'Current repair service page is transactional/professional; narrow self-help content exists but no broad corrected DIY owner was verified.',
    },
    'WINDOW_REPLACEMENT_SERVICE': {
        'page':'PROPOSED_NEW:/uslugi/zamena-okon/',
        'core_units':['WINDOW_REPLACEMENT_SERVICE'],
        'support_units':[],
        'page_kind':'COMMERCIAL_SERVICE',
        'business_truth':'VERIFIED_AS_WORKFLOW_WITHIN_CURRENT_INSTALLATION/OFFER_BUT_STANDALONE_SERVICE_ROLE_NOT_FULLY_PROVEN',
        'current_alternative':'Current installation page covers old-window demolition + new-window installation but Step 11 found replacement-specific ownership only MEDIUM.',
    },
}


def read_tsv(path, skip_comments=False):
    if skip_comments:
        lines=[x for x in path.read_text(encoding='utf-8').splitlines() if x.strip() and not x.lstrip().startswith('#')]
        if not lines:return []
        return list(csv.DictReader(lines,delimiter='\t'))
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))

assign=read_tsv(ASSIGN)
step08=read_tsv(STEP08)
step09=read_tsv(STEP09)
if len(assign)!=2332: raise RuntimeError('V4 assignment accounting mismatch')
step08_by={r['phrase']:r for r in step08}
step09_by={r['query']:r for r in step09}

# Independent direct Wordstat index from all persisted normalized acquisition files.
# Only section=result is direct demand. Association rows are not used as direct demand.
wordstat_direct=defaultdict(list)
wordstat_assoc=defaultdict(list)
wordstat_files=[]
for p in sorted(ROOT.glob('STEP_03R_*RAW_NORMALIZED.tsv'))+sorted(ROOT.glob('STEP_05_*RAW_NORMALIZED.tsv')):
    rows=read_tsv(p,skip_comments=True)
    if not rows: continue
    if not {'section','phrase','count'} <= set(rows[0]): continue
    wordstat_files.append(p.name)
    for r in rows:
        try: count=int(float(r['count']))
        except: continue
        rec={'count':count,'file':p.name,'section':r['section']}
        if r['section']=='result': wordstat_direct[r['phrase']].append(rec)
        elif r['section']=='association': wordstat_assoc[r['phrase']].append(rec)

# V4 structural-unit membership.
unit_members=defaultdict(list)
for r in assign:
    if r['final_structural_unit_id']:
        unit_members[r['final_structural_unit_id']].append(r)

phrase_rows=[]
summary_rows=[]
for cid,cfg in CANDIDATES.items():
    core=[]
    for uid in cfg['core_units']:
        core.extend(unit_members.get(uid,[]))
    support=[]
    for uid in cfg['support_units']:
        support.extend(unit_members.get(uid,[]))
    core_by={r['phrase']:r for r in core}
    support_by={r['phrase']:r for r in support if r['phrase'] not in core_by}
    core_phrases=sorted(core_by)
    support_phrases=sorted(support_by)
    if not core_phrases: raise RuntimeError(f'{cid}: no core phrases')

    direct_counts=[]
    direct_phrase_count=0
    assoc_only=0
    no_acq=0
    search_matches=[]
    top=[]
    for phrase in core_phrases:
        s08=step08_by.get(phrase)
        direct_obs=wordstat_direct.get(phrase,[])
        assoc_obs=wordstat_assoc.get(phrase,[])
        direct_max=max([x['count'] for x in direct_obs],default=0)
        # Cross-check against Step08 max_result_count when available; don't silently overwrite disagreement.
        s08_max=int(s08['max_result_count']) if s08 and s08.get('max_result_count') else 0
        s08_result_occ=int(s08['result_occurrences']) if s08 and s08.get('result_occurrences') else 0
        s08_assoc_occ=int(s08['association_occurrences']) if s08 and s08.get('association_occurrences') else 0
        crosscheck='MATCH_OR_NO_DUPLICATE_RAW_ROW'
        if direct_max and s08_max and direct_max!=s08_max: crosscheck='MISMATCH_REVIEW_REQUIRED'
        effective_direct=max(direct_max,s08_max) if (direct_max or s08_result_occ) else 0
        if effective_direct:
            direct_phrase_count+=1; direct_counts.append(effective_direct); top.append((effective_direct,phrase,s08['provenance'] if s08 else '',','.join(sorted({x['file'] for x in direct_obs}))))
        elif assoc_obs or s08_assoc_occ:
            assoc_only+=1
        else:
            no_acq+=1
        q=step09_by.get(phrase)
        if q:
            search_matches.append(q)
        phrase_rows.append({
            'candidate_id':cid,'proposed_page':cfg['page'],'evidence_role':'CORE','structural_unit_id':core_by[phrase]['final_structural_unit_id'],'phrase':phrase,
            'wordstat_direct_result_count':effective_direct,'wordstat_step08_result_occurrences':s08_result_occ,'wordstat_step08_association_occurrences':s08_assoc_occ,
            'wordstat_provenance':s08['provenance'] if s08 else '', 'raw_normalized_sources':','.join(sorted({x['file'] for x in direct_obs})),'wordstat_crosscheck':crosscheck,
            'direct_search_probe_id':q['probe_id'] if q else '', 'direct_search_observed_job':q['observed_serp_job'] if q else '', 'direct_search_result_type':q['dominant_result_type'] if q else '',
            'direct_search_handoff':q['step10_handoff'] if q else '', 'direct_search_confidence':q['confidence'] if q else '', 'search_evidence_scope':q['evidence_scope'] if q else '',
        })
    # Supporting phrases are listed but never counted as core standalone demand.
    for phrase in support_phrases:
        s08=step08_by.get(phrase);q=step09_by.get(phrase)
        phrase_rows.append({'candidate_id':cid,'proposed_page':cfg['page'],'evidence_role':'SUPPORTING_NOT_CORE_DEMAND','structural_unit_id':support_by[phrase]['final_structural_unit_id'],'phrase':phrase,
            'wordstat_direct_result_count':int(s08['max_result_count']) if s08 and s08.get('max_result_count') else 0,
            'wordstat_step08_result_occurrences':int(s08['result_occurrences']) if s08 and s08.get('result_occurrences') else 0,
            'wordstat_step08_association_occurrences':int(s08['association_occurrences']) if s08 and s08.get('association_occurrences') else 0,
            'wordstat_provenance':s08['provenance'] if s08 else '', 'raw_normalized_sources':'', 'wordstat_crosscheck':'SUPPORTING_NOT_INCLUDED_IN_CORE_DEMAND_VERDICT',
            'direct_search_probe_id':q['probe_id'] if q else '', 'direct_search_observed_job':q['observed_serp_job'] if q else '', 'direct_search_result_type':q['dominant_result_type'] if q else '', 'direct_search_handoff':q['step10_handoff'] if q else '', 'direct_search_confidence':q['confidence'] if q else '', 'search_evidence_scope':q['evidence_scope'] if q else ''})

    top=sorted(top,reverse=True)[:12]
    top_txt=' || '.join(f'{p}={n} [{prov or raw}]' for n,p,prov,raw in top)
    search_txt=' || '.join(f"{q['query']} -> {q['observed_serp_job']} / {q['dominant_result_type']} / {q['step10_handoff']}" for q in search_matches)
    direct_search_n=len(search_matches)
    result_types=sorted({q['dominant_result_type'] for q in search_matches})
    jobs=sorted({q['observed_serp_job'] for q in search_matches})
    # Demand verdict uses observed direct counts only; no sum of overlapping phrases is called total demand.
    if direct_phrase_count>=3 and max(direct_counts or [0])>=100:
        demand_verdict='STRONG_DIRECT_WORDSTAT_SUPPORT'
    elif direct_phrase_count>=1:
        demand_verdict='PARTIAL_DIRECT_WORDSTAT_SUPPORT'
    else:
        demand_verdict='NO_DIRECT_WORDSTAT_SUPPORT_IN_PERSISTED_SET'
    if direct_search_n:
        search_verdict='DIRECT_SEARCH_EVIDENCE_AVAILABLE_FOR_CORE_PHRASES'
        boundary_gap='NO_GAP_FOR_OBSERVED_CORE_QUERIES__DO_NOT_TRANSFER_TO_UNPROBED_PHRASES'
    else:
        search_verdict='NO_DIRECT_STEP09_CORE_QUERY'
        boundary_gap='MATERIAL_SEARCH_PAGE_BOUNDARY_NOT_DIRECTLY_PROBED'
    maturity='PROVISIONAL_PENDING_SEARCH_BOUNDARY' if not direct_search_n else 'EVIDENCE_SUPPORTED_PENDING_ACTION_REEVALUATION'
    summary_rows.append({
        'candidate_id':cid,'proposed_page':cfg['page'],'page_kind':cfg['page_kind'],'core_structural_units':';'.join(cfg['core_units']),'supporting_structural_units':';'.join(cfg['support_units']),
        'core_phrase_count_coverage':len(core_phrases),'supporting_phrase_count_not_used_as_core_demand':len(support_phrases),
        'core_phrases_with_direct_wordstat_result':direct_phrase_count,'core_phrases_association_only':assoc_only,'core_phrases_without_persisted_acquisition_count':no_acq,
        'max_direct_wordstat_count_observed':max(direct_counts or [0]),'median_direct_wordstat_count_observed':statistics.median(direct_counts) if direct_counts else 0,
        'top_direct_wordstat_evidence':top_txt,'wordstat_demand_verdict':demand_verdict,
        'direct_step09_core_queries':direct_search_n,'direct_step09_query_evidence':search_txt,'direct_search_jobs':';'.join(jobs),'direct_search_result_types':';'.join(result_types),'search_page_type_verdict':search_verdict,
        'business_truth':cfg['business_truth'],'current_page_alternative':cfg['current_alternative'],'search_boundary_gap':boundary_gap,'candidate_maturity_after_existing_evidence':maturity,
        'evidence_limit':'Wordstat phrase counts overlap semantically and are NOT summed as total unique demand. Step09 evidence applies only to directly probed queries; no transfer to unprobed neighbours.'
    })

write_fields=list(summary_rows[0].keys())
with OUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=write_fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(summary_rows)
with OUT_PHRASES.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(phrase_rows[0].keys()),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(phrase_rows)

mismatches=[r for r in phrase_rows if r['wordstat_crosscheck']=='MISMATCH_REVIEW_REQUIRED']
qa={
    'status':'CANDIDATE_NEW_PAGE_EVIDENCE_MATRIX_READY_FOR_MANUAL_REVIEW',
    'candidate_pages':len(summary_rows),'candidate_ids':[r['candidate_id'] for r in summary_rows],
    'phrase_evidence_rows':len(phrase_rows),'wordstat_source_files_used':wordstat_files,
    'direct_wordstat_only_for_demand':True,'association_not_counted_as_direct_demand':True,'phrase_counts_not_summed_as_total_unique_demand':True,
    'step09_direct_query_only_no_transfer':True,'wordstat_raw_vs_step08_mismatch_rows':len(mismatches),'wordstat_raw_vs_step08_mismatch_phrases':[r['phrase'] for r in mismatches],
    'candidates_without_direct_step09_core_query':[r['candidate_id'] for r in summary_rows if int(r['direct_step09_core_queries'])==0],
    'defects_closed_by_script_alone':[], 'defects_candidate_for_closure_after_manual_review':['D12-03','D12-10'],
    'new_bridge_requests':0,'new_bridge_cost_rub':0.0,
}
if len(summary_rows)!=5 or mismatches:
    qa['status']='FAIL'
OUT_QA.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False))
