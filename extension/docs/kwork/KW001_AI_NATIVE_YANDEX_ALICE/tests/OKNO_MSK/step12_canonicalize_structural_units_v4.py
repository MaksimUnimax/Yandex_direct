import csv, json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V3.tsv'
HIST = ROOT / 'STEP_12_PHRASE_ACTION_MAP.tsv'
OUT_ASSIGN = ROOT / 'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V4.tsv'
OUT_UNITS = ROOT / 'STEP_12_STRUCTURAL_UNITS_V4.tsv'
OUT_CORR = ROOT / 'STEP_12_STRUCTURAL_UNIT_CORRECTIONS_V4.tsv'
OUT_SALVAGE = ROOT / 'STEP_12_NO_PAGE_OUTSIDE_SALVAGE_REVIEW_V4.tsv'
OUT_QA = ROOT / 'STEP_12_STRUCTURAL_UNIT_CORRECTION_QA_V4.json'

BALCONY='https://okno-msk.ru/balkony-i-lodzhii/'
BALCONY_COLD='https://okno-msk.ru/balkony-i-lodzhii/holodnoe-osteklenie/'
BALCONY_PAN='https://okno-msk.ru/balkony-i-lodzhii/panoramnoe-osteklenie-balkona/'
ALU_SLIDE='https://okno-msk.ru/alyuminievye-okna/razdvizhnye/'
VERANDA='https://okno-msk.ru/verandy/'
PAN_INFO='https://okno-msk.ru/stati/panoramnoe-osteklenie-eto-dan-mode-ili-praktichnoe-reshenie/'
FINISH='https://okno-msk.ru/uslugi/otdelka-otkosov/'
REPAIR='https://okno-msk.ru/uslugi/remont-okon/'
ACCESS='https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/'
MOSQUITO=ACCESS+'moskitnye-setki/'
PROPOSED_PAN='PROPOSED_NEW:/panoramnye-okna/'
PROPOSED_HW='PROPOSED_NEW:/stati/okonnaya-furnitura-vidy-brendy-kak-vybrat/'
PROPOSED_REPAIR='PROPOSED_NEW:/stati/remont-i-regulirovka-plastikovyh-okon-svoimi-rukami/'


def read(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(path,rows,fields):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)

rows=read(SRC); hist=read(HIST); hist_by={r['phrase']:r for r in hist}
if len(rows)!=2332 or len(hist)!=2332: raise RuntimeError('input accounting mismatch')

# Canonical metadata for units that V3 readback showed were semantically one unit but had textual/role metadata drift.
CANON={
'BALCONY_GLAZING_GENERAL': dict(task='order balcony/loggia glazing',intent='SERVICE',state='IN_SCOPE',role='PRIMARY_EXISTING_SERVICE',primary=BALCONY,support='',maturity='PENDING_STEP12_ACTION_REEVALUATION',reason='Canonical broad balcony/loggia glazing unit; rescued open-balcony glazing phrase shares this same service task.'),
'MOSQUITO_NET_INSTALLATION_SERVICE': dict(task='order professional mosquito-net installation',intent='SERVICE',state='IN_SCOPE',role='PRIMARY_EXISTING_SERVICE',primary=MOSQUITO,support='',maturity='PENDING_STEP12_ACTION_REEVALUATION',reason='Canonical mosquito-net installation unit; the salvaged mixed phrase and historical installation phrases share the same service task.'),
'PANORAMIC_BALCONY_GLAZING': dict(task='order/understand panoramic balcony/loggia glazing',intent='SERVICE',state='IN_SCOPE',role='PRIMARY_EXISTING_SERVICE',primary=BALCONY_PAN,support=BALCONY,maturity='PENDING_STEP12_ACTION_REEVALUATION',reason='Canonical object-specific panoramic balcony/loggia glazing unit.'),
'PANORAMIC_OUTDOOR_GLAZING': dict(task='plan/order panoramic glazing for veranda/terrace/gazebo',intent='SERVICE_OR_COMMERCIAL',state='IN_SCOPE',role='PRIMARY_EXISTING_SERVICE',primary=VERANDA,support=PROPOSED_PAN,maturity='PROVISIONAL_PENDING_SEARCH_BOUNDARY',reason='Canonical outdoor-object panoramic glazing unit; relation to a future broad panoramic commercial page remains provisional.'),
'PANORAMIC_WINDOW_TECH_SELECTION_INFO': dict(task='understand/select panoramic window types, safety, thermal and suitability options',intent='INFO',state='IN_SCOPE',role='PROVISIONAL_EXISTING_INFO',primary=PAN_INFO,support=PROPOSED_PAN,maturity='PROVISIONAL_PENDING_PAGE_FIT',reason='Canonical panoramic technical/selection unit; existing explanatory article is primary candidate while relation to a broad commercial panoramic page remains provisional.'),
'WINDOW_FINISHING_SERVICE': dict(task='order professional window slopes/surround/related finishing work',intent='SERVICE',state='IN_SCOPE',role='PRIMARY_EXISTING_SERVICE',primary=FINISH,support='',maturity='PENDING_STEP12_ACTION_REEVALUATION',reason='Canonical finishing-service unit including salvaged slope-related phrases.'),
'WINDOW_HARDWARE_MAINTENANCE_INFO': dict(task='learn/select maintenance and lubrication for window hardware',intent='INFO',state='IN_SCOPE',role='SUPPORTING_CONTENT',primary=PROPOSED_REPAIR,support=REPAIR,maturity='PENDING_STEP12_ACTION_REEVALUATION',reason='Canonical maintenance/lubrication information unit; buying lubricant is subordinate to the maintenance task.'),
'WINDOW_HARDWARE_SELECTION_GUIDE': dict(task='understand and select window hardware types, construction, brands and manufacturers',intent='INFO',state='IN_SCOPE',role='NEW_INFORMATIONAL_CANDIDATE',primary=PROPOSED_HW,support=ACCESS,maturity='PENDING_STEP12_ACTION_REEVALUATION',reason='Canonical hardware explanation/selection unit after brand-review and maintenance tasks were separated.'),
}

canonicalized=0
split_rows=0
for r in rows:
    uid=r['final_structural_unit_id']
    if uid=='BALCONY_ALUMINIUM_SLIDING_GLAZING':
        # V3 proved one structural unit still hid two page-boundary states. Split by explicit cold task because cold and general balcony pages are materially different current destinations.
        if 'холод' in r['phrase'].lower():
            r['final_structural_unit_id']='BALCONY_ALUMINIUM_SLIDING_COLD'
            r['final_unit_task']='order cold aluminium sliding glazing for balcony/loggia'
            r['primary_page_candidate']=BALCONY_COLD
            r['supporting_page']=ALU_SLIDE
            r['correction_reason']='Explicit cold balcony task: current cold-balcony page is the object/task candidate; sliding-aluminium page remains supporting material/opening context.'
        else:
            r['final_structural_unit_id']='BALCONY_ALUMINIUM_SLIDING_GENERAL'
            r['final_unit_task']='order aluminium sliding glazing for balcony/loggia'
            r['primary_page_candidate']=BALCONY
            r['supporting_page']=ALU_SLIDE
            r['correction_reason']='General balcony/loggia sliding-aluminium task: broad balcony page is the object/task candidate; sliding-aluminium page remains supporting material/opening context.'
        r['intent_type']='SERVICE';r['business_scope_state']='IN_SCOPE';r['unit_page_role']='PROVISIONAL_OBJECT_VS_MATERIAL_PAGE';r['recommendation_maturity']='PROVISIONAL_PENDING_SEARCH_BOUNDARY';r['assignment_origin']='V4_SEMANTIC_UNIT_SPLIT_AFTER_READBACK';split_rows+=1
        continue
    if uid in CANON:
        c=CANON[uid]
        r['final_unit_task']=c['task'];r['intent_type']=c['intent'];r['business_scope_state']=c['state'];r['unit_page_role']=c['role'];r['primary_page_candidate']=c['primary'];r['supporting_page']=c['support'];r['recommendation_maturity']=c['maturity'];r['correction_reason']=c['reason']
        if r['assignment_origin']=='UNCHANGED_BASE_UNIT': r['assignment_origin']='V4_CANONICALIZED_BASE_UNIT'
        else: r['assignment_origin']=r['assignment_origin']+'+V4_CANONICALIZED'
        canonicalized+=1

# Unit summary and consistency check.
groups=defaultdict(list)
for r in rows:
    if r['final_structural_unit_id']:groups[r['final_structural_unit_id']].append(r)
units=[]
for uid,rs in sorted(groups.items()):
    def vals(k): return sorted({x[k] for x in rs if x[k]})
    dimensions=['final_unit_task','intent_type','business_scope_state','unit_page_role','primary_page_candidate','supporting_page','recommendation_maturity']
    incons={k:vals(k) for k in dimensions if len(vals(k))>1}
    first=rs[0]
    units.append({
        'structural_unit_id':uid,'phrase_count':len(rs),'source_effective_clusters':';'.join(sorted({x['original_effective_cluster_id'] for x in rs})),'user_task':first['final_unit_task'],'intent_type':first['intent_type'],'business_scope_state':first['business_scope_state'],'unit_page_role':first['unit_page_role'],'primary_page_candidate':first['primary_page_candidate'],'supporting_page':first['supporting_page'],'recommendation_maturity':first['recommendation_maturity'],'confidence':'PENDING_EVIDENCE_DERIVATION','assignment_origin_mix':';'.join(f'{k}:{v}' for k,v in sorted(Counter(x['assignment_origin'] for x in rs).items())),'unit_reason':first['correction_reason'],'inconsistent_unit_metadata_fields':len(incons),'inconsistent_metadata_detail':json.dumps(incons,ensure_ascii=False) if incons else ''
    })

# Rebuild corrections relative to historical Step 12.
corr=[]
for r in rows:
    if not r['original_effective_cluster_id']: continue
    h=hist_by[r['phrase']]
    changed=(r['final_structural_unit_id']!=r['original_effective_cluster_id'] or h['routing_override']=='true' or r['assignment_origin'] not in {'UNCHANGED_BASE_UNIT'})
    if changed:
        corr.append({'phrase':r['phrase'],'original_effective_cluster_id':r['original_effective_cluster_id'],'historical_step12_structural_unit_id':h['structural_unit_id'],'historical_step12_target':h['target_or_new_page'],'corrected_structural_unit_id':r['final_structural_unit_id'],'corrected_unit_task':r['final_unit_task'],'corrected_primary_page_candidate':r['primary_page_candidate'],'corrected_supporting_page':r['supporting_page'],'corrected_page_role':r['unit_page_role'],'corrected_business_scope_state':r['business_scope_state'],'recommendation_maturity':r['recommendation_maturity'],'correction_reason':r['correction_reason'],'correction_origin':r['assignment_origin'],'review_status':'CANDIDATE_V4_PENDING_SEMANTIC_ACCEPTANCE'})

# Preserve/rebuild historical no-page/outside review.
cluster_action={}
for h in hist:
    cid=h['effective_cluster_id']
    if cid and h['cluster_structural_action'] and cid not in cluster_action: cluster_action[cid]=h['cluster_structural_action']
salvage=[]
for r in rows:
    cid=r['original_effective_cluster_id'];act=cluster_action.get(cid,'')
    if act not in {'NO_STANDALONE_PAGE','OUTSIDE_SCOPE_NO_ACTION'}:continue
    s=r['business_scope_state']
    if s=='OUTSIDE_SCOPE': disp='OUTSIDE_CONFIRMED'
    elif s.startswith('NO_STANDALONE'): disp='NO_STANDALONE_CONFIRMED'
    elif s.startswith('DEFERRED'): disp='EXPLICITLY_DEFERRED'
    else: disp='SALVAGED_TO_IN_SCOPE_UNIT'
    salvage.append({'phrase':r['phrase'],'historical_cluster_id':cid,'historical_cluster_action':act,'final_structural_unit_id':r['final_structural_unit_id'],'final_business_scope_state':s,'final_page_role':r['unit_page_role'],'primary_page_candidate':r['primary_page_candidate'],'supporting_page':r['supporting_page'],'recommendation_maturity':r['recommendation_maturity'],'review_disposition':disp,'review_reason':r['correction_reason'],'review_status':'CANDIDATE_V4_PENDING_SEMANTIC_ACCEPTANCE'})

write(OUT_ASSIGN,rows,list(rows[0].keys()));write(OUT_UNITS,units,list(units[0].keys()));write(OUT_CORR,corr,list(corr[0].keys()));write(OUT_SALVAGE,salvage,list(salvage[0].keys()))

hist_overrides=[r for r in rows if r['historical_routing_override']=='true']
metadata_bad=[u for u in units if u['inconsistent_unit_metadata_fields']]
mandatory_mixed={'WINDOW_INSTALLATION_DIY_INFO','PANORAMIC_WINDOWS_COMMERCIAL','GLAZING_PERMISSION_INFO','WOOD_WINDOWS_COMMERCIAL','WINDOW_HARDWARE_INFO','WINDOW_REPAIR_DIY_INFO','WINDOW_HARDWARE_SHOPPING','WINDOW_ACCESSORIES_SHOPPING'}
active_unit_ids={u['structural_unit_id'] for u in units}
qa={
    'status':'CANDIDATE_V4_READY_FOR_MANUAL_SEMANTIC_ACCEPTANCE',
    'source_rows':len(rows),
    'search_required_rows':sum(not r['final_structural_unit_id'] for r in rows),
    'structural_units':len(units),
    'correction_rows':len(corr),
    'historical_override_rows':len(hist_overrides),
    'historical_override_rows_with_explicit_final_unit':sum(bool(r['final_structural_unit_id']) for r in hist_overrides),
    'hidden_runtime_override_rules_in_v4_output':0,
    'v4_canonicalized_phrase_rows':canonicalized,
    'v4_split_balcony_aluminium_rows':split_rows,
    'unit_metadata_inconsistency_rows':len(metadata_bad),
    'unit_metadata_inconsistency_ids':[u['structural_unit_id'] for u in metadata_bad],
    'mandatory_mixed_original_units_still_final':sorted(mandatory_mixed & active_unit_ids),
    'historical_no_page_or_outside_review_rows':len(salvage),
    'salvaged_to_in_scope_units':sum(r['review_disposition']=='SALVAGED_TO_IN_SCOPE_UNIT' for r in salvage),
    'explicitly_deferred_rows':sum(r['review_disposition']=='EXPLICITLY_DEFERRED' for r in salvage),
    'outside_confirmed_rows':sum(r['review_disposition']=='OUTSIDE_CONFIRMED' for r in salvage),
    'no_standalone_confirmed_rows':sum(r['review_disposition']=='NO_STANDALONE_CONFIRMED' for r in salvage),
    'default_high_confidence_rows':0,
    'defects_closed_by_script_alone':[],
    'defects_candidate_for_manual_acceptance':['D12-01','D12-02','D12-08','D12-09','D12-12']
}
if len(rows)!=2332 or qa['search_required_rows']!=19 or len(hist_overrides)!=191 or qa['historical_override_rows_with_explicit_final_unit']!=191 or metadata_bad or qa['mandatory_mixed_original_units_still_final']:
    qa['status']='FAIL'
OUT_QA.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False))
