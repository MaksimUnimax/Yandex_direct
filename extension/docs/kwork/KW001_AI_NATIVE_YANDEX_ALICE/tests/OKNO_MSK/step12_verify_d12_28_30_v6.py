import csv,json,itertools
from collections import defaultdict,Counter
from pathlib import Path
R=Path(__file__).resolve().parent

def read(name):
    with (R/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def norm(u):
    u=(u or '').strip()
    if u and u!='https://okno-msk.ru/':u=u.rstrip('/')
    return u

def b(v):return str(v).strip().lower()=='true'

base_assign=read('STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V6.tsv')
packet=read('STEP_12_D12_28_MEMBER_PHRASES_PACKET.tsv')
content=read('STEP_12_D12_28_CURRENT_CONTENT_REVALIDATION.tsv')
res=read('STEP_12_D12_30_PHRASE_RESOLUTIONS.tsv')
semqa=read('STEP_12_D12_30_INDEPENDENT_MEMBER_QA.tsv')
newdefs=read('STEP_12_D12_30_NEW_UNIT_DEFINITIONS.tsv')
oldlinks=read('STEP_12_INTERNAL_LINK_ACTIONS_V5.tsv')
lval=read('STEP_12_D12_29_CURRENT_LINK_VALIDATION.tsv')
assign=read('STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V7.tsv')
actions=read('STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv')
phrase_map=read('STEP_12_PHRASE_ACTION_MAP_FINAL_V6.tsv')
links=read('STEP_12_INTERNAL_LINK_ACTIONS_V6.tsv')
pairs=read('STEP_12_STEP13_CANDIDATE_PAIRS_V6.tsv')
state=json.loads((R/'STEP_12_CORRECTION_CURRENT_STATE.json').read_text(encoding='utf-8'))

findings=[]
def ck(cond,id,detail=''):
    if not cond:findings.append({'check_id':id,'finding':detail or id})

# Raw scope/accounting independent of final action labels.
ck(len(base_assign)==2332,'BASE_ASSIGNMENT_2332',str(len(base_assign)))
ck(len(assign)==2332,'FINAL_ASSIGNMENT_2332',str(len(assign)))
ck(len(phrase_map)==2332,'FINAL_PHRASE_MAP_2332',str(len(phrase_map)))
ck(len({r['phrase'] for r in assign})==2332,'FINAL_PHRASES_UNIQUE')
ck(sum(bool(r.get('final_structural_unit_id')) for r in assign)==2313,'FINAL_ASSIGNED_2313')
ck(len(content)==20,'D12_28_EXACT_20_UNITS',str(len(content)))
ck(len(packet)==322,'D12_28_EXACT_322_SOURCE_PHRASES',str(len(packet)))
ck(len(res)==49,'D12_30_EXACT_49_REASSIGNMENTS',str(len(res)))
ck(len(semqa)==20,'D12_30_SEMANTIC_QA_20_UNITS',str(len(semqa)))
ck(sum(int(r['source_phrase_count']) for r in semqa)==322,'D12_30_SEMANTIC_QA_322_SOURCE')
ck(sum(int(r['detected_misfit_count']) for r in semqa)==49,'D12_30_SEMANTIC_QA_49_MISFITS')
ck(sum(int(r['expected_retained_source_members']) for r in semqa)==273,'D12_30_SEMANTIC_QA_273_RETAINED')
ck(all(b(r['all_source_members_independently_reviewed']) for r in semqa),'D12_30_ALL_SOURCE_MEMBERS_REVIEWED')

# Content evidence is causally upstream from action and cannot be generic action restatement.
prohibited=('accepted structural action requires materially fuller','expand was selected','section was selected')
for r in content:
    uid=r['structural_unit_id']
    ck(b(r['all_member_phrases_reviewed']),f'CONTENT_ALL_MEMBERS_{uid}')
    ck(r['current_page_read_date']=='2026-08-31',f'CONTENT_FRESH_READ_{uid}',r['current_page_read_date'])
    ck(bool(r['current_page_evidence'].strip()),f'CONTENT_EVIDENCE_{uid}')
    blob=(r['current_page_evidence']+' '+r['resolution_rationale']).lower()
    ck(not any(x in blob for x in prohibited),f'CONTENT_NOT_ACTION_DERIVED_{uid}',blob)
    if r['content_enhancement_state']=='QUALITY_GAP':
        ck(bool(r['explicit_missing_needs'].strip()),f'QUALITY_EXPLICIT_MISSING_{uid}')
        ck(r['content_action_resolution'] in {'EXPAND_EXISTING_PAGE','ADD_SECTION_OR_FAQ_TO_EXISTING'},f'QUALITY_HAS_CONTENT_ACTION_{uid}',r['content_action_resolution'])

# Resolution application: exact phrase + old membership from raw base -> explicit corrected membership in final.
base_by_phrase=defaultdict(list);final_by_phrase={r['phrase']:r for r in assign}
for r in base_assign:base_by_phrase[r['phrase']].append(r)
for rr in res:
    hits=[r for r in base_by_phrase[rr['phrase']] if r.get('final_structural_unit_id')==rr['old_structural_unit_id']]
    ck(len(hits)==1,'RESOLUTION_BASE_EXACT_'+rr['phrase'],str(len(hits)))
    ck(final_by_phrase[rr['phrase']].get('final_structural_unit_id')==rr['corrected_structural_unit_id'],'RESOLUTION_FINAL_'+rr['phrase'],final_by_phrase[rr['phrase']].get('final_structural_unit_id',''))

# Independent source-unit retained counts from the separate semantic QA ledger.
packet_by=defaultdict(set)
for r in packet:packet_by[r['structural_unit_id']].add(r['phrase'])
final_units=defaultdict(set)
for r in assign:
    if r.get('final_structural_unit_id'):final_units[r['final_structural_unit_id']].add(r['phrase'])
for q in semqa:
    uid=q['structural_unit_id'];source=packet_by[uid]
    retained=len(source & final_units.get(uid,set()))
    ck(len(source)==int(q['source_phrase_count']),f'SEMQA_SOURCE_COUNT_{uid}',f'{len(source)}')
    ck(retained==int(q['expected_retained_source_members']),f'SEMQA_RETAINED_COUNT_{uid}',f'{retained}')
    if q['independent_semantic_verdict']=='ZERO_MEMBER_EXPECTED':ck(uid not in {a['structural_unit_id'] for a in actions},f'ZERO_UNIT_REMOVED_{uid}')

# Every active assigned unit has exactly one action and phrase_count/source accounting matches final assignments.
action_by={r['structural_unit_id']:r for r in actions}
ck(len(action_by)==len(actions),'ACTIONS_UNIQUE_IDS')
ck(set(final_units)==set(action_by),'ACTION_UNIT_SET_EQUALS_ASSIGNMENT_UNIT_SET',f'missing={sorted(set(final_units)-set(action_by))[:10]} extra={sorted(set(action_by)-set(final_units))[:10]}')
for uid,phr in final_units.items():
    ck(int(action_by[uid]['phrase_count'])==len(phr),f'ACTION_COUNT_{uid}',f"{action_by[uid]['phrase_count']} vs {len(phr)}")

# Separate structural/content gap model present. Any final QUALITY_GAP must have current independent evidence.
quality=[]
for a in actions:
    ck(bool(a.get('structural_gap_state','').strip()),f'SEPARATED_STRUCTURAL_GAP_{a["structural_unit_id"]}')
    ck(bool(a.get('content_enhancement_state','').strip()),f'SEPARATED_CONTENT_GAP_{a["structural_unit_id"]}')
    if a.get('content_enhancement_state')=='QUALITY_GAP':quality.append(a)
for a in quality:
    uid=a['structural_unit_id']
    ck(a.get('current_content_read_date')=='2026-08-31',f'FINAL_QUALITY_CURRENT_READ_{uid}')
    ck(bool(a.get('explicit_missing_needs','').strip()),f'FINAL_QUALITY_MISSING_NEEDS_{uid}')
    blob=(a.get('gap_evidence','')+' '+a.get('current_content_evidence','')).lower()
    ck('accepted structural action requires materially fuller' not in blob,f'FINAL_QUALITY_NOT_OLD_CIRCULAR_{uid}')
ck(all(a.get('structural_action') not in {'NEW_COMMERCIAL_PAGE','NEW_INFORMATIONAL_PAGE'} for a in actions),'NO_NEW_PAGE_ACTIONS')
ck(all('NO_CONTENT_CHANGE_NEEDED' not in (a.get('optimization_readiness','')+a.get('gap_evidence','')) for a in actions),'KEEP_NOT_PERFORMANCE_PASS')

# New explicit units are all materialized, but their definitions do not silently become CREATE.
for d in newdefs:
    ck(d['structural_unit_id'] in action_by,f'NEW_UNIT_PRESENT_{d["structural_unit_id"]}')
    if d['structural_action']=='DEFER_PENDING_EVIDENCE':ck(action_by[d['structural_unit_id']]['structural_action']=='DEFER_PENDING_EVIDENCE',f'NEW_UNIT_STAYS_DEFER_{d["structural_unit_id"]}')

# D12-29: old IMPLEMENT set must be exactly the validation set; every retained IMPLEMENT has current evidence and helpfulness.
old_impl={r['link_action_id']:r for r in oldlinks if r['link_action_state']=='IMPLEMENT'}
val_by={r['link_action_id']:r for r in lval}
ck(len(old_impl)==28,'OLD_IMPLEMENT_28',str(len(old_impl)))
ck(set(old_impl)==set(val_by),'VALIDATION_COVERS_ALL_OLD_IMPLEMENT')
final_link_by={r['link_action_id']:r for r in links}
for lid,v in val_by.items():
    ck(lid in final_link_by,f'VALIDATED_LINK_PRESENT_{lid}')
    if lid not in final_link_by:continue
    fl=final_link_by[lid]
    ck(fl['link_action_state']==v['corrected_link_action_state'],f'VALIDATED_LINK_STATE_{lid}',fl['link_action_state'])
    ck(fl['structural_unit_id']==v['corrected_structural_unit_id'],f'VALIDATED_LINK_UNIT_{lid}',fl['structural_unit_id'])
    if v['corrected_link_action_state']=='IMPLEMENT':
        ck(v['current_source_read_date']=='2026-08-31' and v['current_target_read_date']=='2026-08-31',f'IMPLEMENT_CURRENT_READS_{lid}')
        ck(bool(v['source_context_evidence'].strip()),f'IMPLEMENT_SOURCE_CONTEXT_{lid}')
        ck(bool(v['target_task_fit_evidence'].strip()),f'IMPLEMENT_TARGET_FIT_{lid}')
        ck(b(v['user_next_step_helpful']),f'IMPLEMENT_HELPFUL_{lid}')
        ck(fl['evidence_origin']=='D12_29_CURRENT_SOURCE_TARGET_VALIDATION',f'IMPLEMENT_VALIDATION_ORIGIN_{lid}',fl['evidence_origin'])
for fl in links:
    if fl['link_action_state']=='IMPLEMENT':ck(fl['link_action_id'] in val_by,f'NO_UNVALIDATED_IMPLEMENT_{fl["link_action_id"]}')

# Pair universe independently recomputed from final routing graph; compare key set, not generator pair IDs.
def addkey(s,a,b):
    a,b=norm(a),norm(b)
    if a and b and a!=b:s.add(tuple(sorted((a,b))))
expected=set()
for a in actions:addkey(expected,a.get('primary_page_candidate',''),a.get('supporting_page',''))
cluster_pages=defaultdict(set)
for ar in assign:
    uid=ar.get('final_structural_unit_id','');c=ar.get('original_effective_cluster_id','')
    if uid and c and uid in action_by:
        p=norm(action_by[uid].get('primary_page_candidate',''))
        if p:cluster_pages[c].add(p)
for pageset in cluster_pages.values():
    if len(pageset)>1:
        for x,y in itertools.combinations(sorted(pageset),2):expected.add((x,y))
actual={tuple(sorted((norm(p['page_a']),norm(p['page_b'])))) for p in pairs}
ck(expected==actual,'PAIR_KEY_SET_EXACT',f'missing={len(expected-actual)} extra={len(actual-expected)}')
ck(len(actual)==len(pairs),'PAIR_KEYS_UNIQUE')

# Phrase map must be a deterministic projection of final assignment/action rows for assigned phrases.
pmap={r['phrase']:r for r in phrase_map}
for ar in assign:
    ph=ar['phrase'];uid=ar.get('final_structural_unit_id','')
    if uid:
        ck(pmap[ph]['final_structural_unit_id']==uid,f'PHRASE_MAP_UNIT_{ph}')
        ck(pmap[ph]['structural_action']==action_by[uid]['structural_action'],f'PHRASE_MAP_ACTION_{ph}')

# Current job must remain reopened until this verifier and durable readback are accepted; Step13 untouched.
ck(state.get('step12_complete') is False,'STATE_STEP12_REOPENED')
ck(state.get('step13_blocked') is True,'STATE_STEP13_BLOCKED')
ck(state.get('step13_executed') is False,'STATE_STEP13_NOT_EXECUTED')
ck(set(state.get('open_defects',[]))=={'D12-28','D12-29','D12-30'},'STATE_OPEN_DEFECTS_28_30',str(state.get('open_defects')))

out={'date':'2026-08-31','status':'STEP12_D12_28_D12_29_D12_30_INDEPENDENT_PASS' if not findings else 'STEP12_D12_28_D12_29_D12_30_INDEPENDENT_FAIL','findings':len(findings),'source_assignments':len(base_assign),'final_assignments':len(assign),'final_phrase_map_rows':len(phrase_map),'affected_source_units':len(semqa),'affected_source_phrases':sum(int(r['source_phrase_count']) for r in semqa),'exact_reassignments':len(res),'final_structural_units':len(actions),'final_quality_gap_units':len(quality),'old_implement_links_reviewed':len(val_by),'retained_implement_links':sum(v['corrected_link_action_state']=='IMPLEMENT' for v in lval),'final_link_rows':len(links),'expected_pair_keys':len(expected),'actual_pair_rows':len(pairs),'new_page_actions':sum(a['structural_action'] in {'NEW_COMMERCIAL_PAGE','NEW_INFORMATIONAL_PAGE'} for a in actions),'step13_executed':False,'verification_origin':'INDEPENDENT_RAW_PACKET_PLUS_CURRENT_CONTENT_LEDGER_PLUS_SECOND_SEMANTIC_MEMBER_QA_PLUS_CURRENT_LINK_VALIDATION_RECOMPUTATION_WITHOUT_FINAL_ACTION_AS_GAP_INPUT'}
(R/'STEP_12_D12_28_30_INDEPENDENT_QA.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (R/'STEP_12_D12_28_30_INDEPENDENT_QA_FINDINGS.tsv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['check_id','finding'],delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(findings)
print(json.dumps(out,ensure_ascii=False,indent=2))
if findings:
    for x in findings[:50]:print(x)
    raise SystemExit(1)
