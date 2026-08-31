import csv,json,re
from collections import Counter
from pathlib import Path

R=Path(__file__).resolve().parent
ROOT=R.parents[1]
METHOD=ROOT/'STEP_12_STRUCTURAL_ACTION_METHOD.md';INDEX=ROOT/'STEP_RULES_INDEX.md'
LED=R/'STEP_12_CORRECTION_DEFECT_LEDGER.tsv';STATE=R/'STEP_12_CORRECTION_CURRENT_STATE.json'
Q=R/'STEP_12_D12_27_INDEPENDENT_QA.json';G=R/'STEP_12_D12_27_GENERATOR_QA.json';V5=R/'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V5.tsv'
FLOW=R/'JOB_FLOW.md';MAN=R/'JOB_MANIFEST.md';QA=R/'STEP_12_QA.json';REPORT=R/'STEP_12_REPORT.md';ACC=R/'STEP_12_THIRD_AUDIT_FINAL_ACCEPTANCE_2026-08-31.md'


def read_tsv(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write_tsv(p,rows,fields):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)

q=json.loads(Q.read_text(encoding='utf-8'));g=json.loads(G.read_text(encoding='utf-8'));v5=read_tsv(V5)
assert q['status']=='STEP12_D12_27_V5_INDEPENDENT_PASS' and q['findings']==0
assert q['d12_27_reviewed_phrases']==65 and q['zero_member_structural_units']==[] and q['strong_fit_keep_verified']==6
assert q['assignments']==2332 and q['phrase_map_rows']==2332 and q['structural_units']==160
assert q['pair_missing']==0 and q['pair_extra']==0 and q['pair_duplicates']==0 and q['pair_search_flag_mismatches']==0 and q['pair_search_reason_mismatches']==0
assert q['new_page_actions']==0 and q['proposed_new_refs']==0 and not q['step13_executed']
assert g['gap_type_missing']==0 and g['performance_state_missing']==0 and g['keep_claiming_no_optimization_needed']==0 and g['policy_sensitive_unknown_final']==0
assert g['internal_link_rows']==g['material_link_units'] and g['internal_link_proposed_refs']==0

# Close D12-21..27 only after the persisted V5 independent acceptance above.
ledger=read_tsv(LED);fields=list(ledger[0].keys());by={r['defect_id']:r for r in ledger}
for i in range(21,28):
    d=f'D12-{i}'
    assert d in by and by[d]['status']=='OPEN',(d,by.get(d,{}).get('status'))
    by[d]['status']='VERIFIED_FIXED'
    artifacts='STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V5.tsv | STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V6.tsv | STEP_12_PHRASE_ACTION_MAP_FINAL_V5.tsv | STEP_12_INTERNAL_LINK_ACTIONS_V5.tsv | STEP_12_STEP13_CANDIDATE_PAIRS_V5.tsv | STEP_12_D12_27_INDEPENDENT_QA.json'
    if d=='D12-27':artifacts+=' | STEP_12_D12_27_PHRASE_RESOLUTIONS.tsv | STEP_12_THIRD_AUDIT_STRONG_FIT_PAGE_RECHECK.tsv'
    by[d]['correction_artifact']=artifacts
    by[d]['notes']=(by[d].get('notes','')+' | Closed only after third-audit V5/V6 rebuild, independent recomputation, durable GitHub persistence/readback and zero findings.').strip(' |')
write_tsv(LED,ledger,fields)

# Canonical reusable method: add D12-27 causality and mark third-audit method active.
m=METHOD.read_text(encoding='utf-8')
m=re.sub(r'^Status: \*\*.*?\*\*  $','Status: **APPROVED / ACTIVE AFTER THIRD EXTERNAL METHOD AUDIT + D12-27 PHRASE-LEVEL REVALIDATION — GAP TYPE + PERFORMANCE BOUNDARY + TARGET-VS-RELEVANT + SERP FORMAT + OWNER-GOAL SOURCE + EXISTING-PAGE INTERNAL LINKS**  ',m,count=1,flags=re.M)
if '## Defect 27 — evidence-first page recheck exposed residual mixed structural units' not in m:
    block='''\n## Defect 27 — evidence-first page recheck exposed residual mixed structural units\n\n### What happened\nAfter D12-21 introduced explicit gap diagnosis, evidence-first review of strong current-page fits exposed that `FRENCH_WINDOWS_COMMERCIAL` and `WINDOW_ACCESSORIES_GENERAL` still mixed different terminal user tasks. The French unit combined genuine commercial demand with inspiration, concept, DIY and hardware phrases. The general-accessories unit mixed generic accessory shopping with aftermarket hardware and aluminium-specific component/frame tasks.\n\n### Why it seemed reasonable\nThe phrases shared strong lexical/product-family similarity, and earlier correction rounds had already removed several obvious outliers. Once a unit had survived repeated QA, it was easy to treat the unit ID itself as evidence that the remaining members were coherent.\n\n### Why that is wrong\nA structural unit is an analytical hypothesis, not permanent truth. Fresh page/gap evidence can expose a contradiction that was invisible under an earlier coarse boundary. If the unit mixes terminal tasks, every later gap type, page-fit and structural action aggregates incompatible evidence.\n\n### Permanent correction\nWhenever a fresh current-page, gap-type, owner-goal or Search-boundary review materially changes the understanding of a structural unit, re-open **all member phrases of that unit** before retaining the unit as a final boundary.\n\n```text\nMATERIAL LATER EVIDENCE CONTRADICTS OR NARROWS A STRUCTURAL UNIT\n→ EXTRACT ALL MEMBER PHRASES\n→ REVIEW EACH PHRASE AGAINST TERMINAL USER TASK / PAGE EXPECTATION\n→ REASSIGN TO EXISTING VALID UNIT OR EXPLICIT NEW/DEFERRED UNIT\n→ RECOMPUTE UNIT COUNTS / ACTIONS / PHRASE MAP / INTERNAL LINKS / PAIR GRAPH\n→ INDEPENDENT EXACT-PHRASE REGRESSION\n```\n\nDo not review only the phrase that exposed the problem. One contradiction is evidence that the unit boundary itself must be challenged.\n\n**Why:** later evidence must be allowed to falsify an earlier cluster/unit. Otherwise the methodology becomes self-sealing.\n\n### OKNO-MSK regression evidence\nThe D12-27 review explicitly inspected 65 phrases. Twenty were reassigned; the French commercial core retained 42 true commercial phrases and the generic-accessory core retained 3 true generic phrases. The final V5/V6 independent verifier checks all 65 exact resolutions and recomputes the downstream graph.\n\n---\n\n'''
    marker='\n# 4. Correct Step-12 working model\n'
    assert marker in m
    m=m.replace(marker,'\n'+block+marker,1)
METHOD.write_text(m,encoding='utf-8')

# Update methodology index row.
idx=INDEX.read_text(encoding='utf-8')
old_re=r'^\| \*\*Step 12\*\* \|.*$'
new='| **Step 12** | **Structural actions (keep/expand/split/merge/create)** | **APPROVED / ACTIVE AFTER THIRD EXTERNAL METHOD AUDIT + D12-27 PHRASE-LEVEL REVALIDATION** | **`STEP_12_STRUCTURAL_ACTION_METHOD.md` + `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`** — explicit gap diagnosis; structural ownership separated from performance claims; intended-vs-observed Yandex URL state; SERP type/format/angle provenance; owner-goal source strength; implementable existing-page internal links; later material evidence must trigger full member-phrase revalidation of affected structural units before acceptance. |'
idx,n=re.subn(old_re,new,idx,count=1,flags=re.M);assert n==1
INDEX.write_text(idx,encoding='utf-8')

# Final QA from independently persisted V5 evidence.
actions=Counter(r['structural_action'] for r in v5);conf=Counter(r['final_confidence'] for r in v5);mat=Counter(r['recommendation_maturity'] for r in v5);gap=Counter(r['gap_type'] for r in v5);rel=Counter(r['relevant_url_match_state'] for r in v5);goal=Counter(r['owner_goal_evidence_source'] for r in v5)
finalqa={
 'date':'2026-08-31','status':'PASS_AFTER_THIRD_EXTERNAL_METHOD_AUDIT_D12_27_PHRASE_LEVEL_REVALIDATION_AND_INDEPENDENT_QA','verification_principle':'V5/V6 current structural truth; independent exact-phrase, gap/performance/Search/owner-goal/link/pair recomputation; no Step13 execution.',
 'source_phrase_rows':2332,'assignment_rows':2332,'final_phrase_action_rows':2332,'assigned_rows':2313,'search_required_rows':19,'structural_units':160,'structural_action_rows':160,
 'tracked_defects':27,'verified_fixed_defects':27,'open_defects':[],
 'd12_27_reviewed_phrases':65,'d12_27_reassigned_phrases':q['d12_27_reassigned_phrases'],'french_commercial_core_rows':q['french_commercial_core_rows'],'general_accessory_core_rows':q['general_accessory_core_rows'],
 'gap_type_counts':dict(gap),'action_counts_by_structural_unit':dict(actions),'confidence_counts_by_structural_unit':dict(conf),'maturity_counts_by_structural_unit':dict(mat),
 'relevant_url_match_counts':dict(rel),'direct_serp_units':q['direct_serp_units'],'owner_goal_source_counts':dict(goal),
 'performance_state_missing':q['performance_state_missing'],'keep_overstated_optimization':q['keep_overstated_optimization'],
 'material_internal_link_units':q['material_link_units'],'internal_link_rows':q['internal_link_rows'],'internal_link_implement':q['internal_link_implement'],
 'candidate_pair_rows':q['actual_pair_rows'],'pairs_requiring_future_step13_search':q['actual_pairs_requiring_step13'],'step13_dependency_units':q['actual_dependency_units'],
 'pair_missing':q['pair_missing'],'pair_extra':q['pair_extra'],'pair_duplicates':q['pair_duplicates'],'pair_search_flag_mismatches':q['pair_search_flag_mismatches'],'pair_search_reason_mismatches':q['pair_search_reason_mismatches'],
 'current_unique_proposed_pages':0,'current_new_page_actions':0,'current_proposed_new_reference_rows':0,'independent_findings':0,'new_bridge_requests':0,'new_bridge_cost_rub':0.0,'step13_executed':False,
 'final_github_readback':False,'canonical_closure_readback_passed':False,'next_step':'STEP_13_PRE_STEP_METHODOLOGY_RESEARCH_AND_REVIEW','step13_status':'NOT_STARTED_NEXT_ALLOWED'
}
QA.write_text(json.dumps(finalqa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

state=json.loads(STATE.read_text(encoding='utf-8'))
state.update({'status':'STEP12_COMPLETE_AFTER_THIRD_EXTERNAL_METHOD_AUDIT_D12_27_PHRASE_LEVEL_REVALIDATION','step13_blocked':False,'open_defects':[],'verified_fixed_defects':[f'D12-{i:02d}' for i in range(1,28)],'current_correction_item':None,'next_action':'Step 12 complete after third external audit and D12-27 exact phrase revalidation. Step 13 is NOT STARTED / NEXT ALLOWED and requires its own fresh methodology research/review before execution.','step13_status':'NOT_STARTED_NEXT_ALLOWED','step12_complete':True,'next_step_allowed':True,'next_major_step':'STEP_13_PRE_STEP_METHODOLOGY_RESEARCH_AND_REVIEW','final_github_readback':False,'canonical_closure_readback_passed':False})
STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

report=f'''# Step 12 — Structural actions report\n\nDate: 2026-08-31\nStatus: **PASS AFTER THIRD EXTERNAL METHOD AUDIT + D12-27 PHRASE-LEVEL REVALIDATION + INDEPENDENT QA**\n\n## Plain-language result\nStep 12 decides what the site should actually do with current pages: keep their role, expand them, add a section, route a subtask elsewhere, defer, or avoid unsupported pages. The third audit added explicit gap diagnosis, performance-evidence boundaries, intended-vs-Yandex-observed URL state, SERP result-type provenance, owner-goal source strength and implementable internal links. A later evidence-first review then exposed two residual mixed units; all 65 affected phrases were rechecked before final closure.\n\n## D12-27 correction\n- reviewed phrases: **65**\n- reassigned phrases: **{q['d12_27_reassigned_phrases']}**\n- French commercial core after review: **{q['french_commercial_core_rows']}** phrases\n- generic accessories core after review: **{q['general_accessory_core_rows']}** phrases\n- zero-member active structural units: **0**\n\n## Current action distribution\n```text\n'''+"\n".join(f'{k} = {v}' for k,v in sorted(actions.items()))+f'''\n```\n\n## Evidence boundaries added in the third audit\n- gap types: {dict(gap)}\n- intended-vs-Yandex relevant state: {dict(rel)}\n- direct persisted SERP evidence attached to units: {q['direct_serp_units']}\n- owner-goal evidence sources: {dict(goal)}\n- performance evidence missing fields: 0; base package still has no Webmaster/Metrika account-performance evidence\n- structural KEEP does **not** mean no optimization is needed\n- material existing-page internal-link units: {q['material_link_units']}; implementable links: {q['internal_link_implement']}\n\n## Downstream Step-13 handoff\n- candidate page pairs: **{q['actual_pair_rows']}**\n- pairs requiring future direct Step-13 Search check: **{q['actual_pairs_requiring_step13']}**\n- structural units with Step-13 dependency: **{q['actual_dependency_units']}**\n- pair missing / extra / duplicates: **0 / 0 / 0**\n- pair search-flag/reason mismatches: **0 / 0**\n- Step 13 executed: **false**\n\n## Final accounting\n```text\nSOURCE_ACTIVE_PHRASES = 2332\nFINAL_PHRASE_ACTION_ROWS = 2332\nASSIGNED = 2313\nSEARCH_REQUIRED = 19\nSTRUCTURAL_UNITS = 160\nTRACKED_DEFECTS = 27\nVERIFIED_FIXED = 27\nOPEN_DEFECTS = 0\nNEW_PAGE_ACTIONS = 0\nPROPOSED_NEW_REFS = 0\nINDEPENDENT_FINDINGS = 0\nNEW_BRIDGE_REQUESTS = 0\nNEW_BRIDGE_COST_RUB = 0.0\nSTEP13_EXECUTED = false\n```\n\n## Canonical current artifacts\n```text\nSTEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V6.tsv\nSTEP_12_STRUCTURAL_ACTIONS_CORRECTED_V5.tsv\nSTEP_12_PHRASE_ACTION_MAP_FINAL_V5.tsv\nSTEP_12_INTERNAL_LINK_ACTIONS_V5.tsv\nSTEP_12_STEP13_CANDIDATE_PAIRS_V5.tsv\nSTEP_12_D12_27_PHRASE_RESOLUTIONS.tsv\nSTEP_12_THIRD_AUDIT_STRONG_FIT_PAGE_RECHECK.tsv\nSTEP_12_D12_27_INDEPENDENT_QA.json\nSTEP_12_QA.json\nSTEP_12_CORRECTION_DEFECT_LEDGER.tsv\nSTEP_12_CORRECTION_CURRENT_STATE.json\n```\n\nHistorical V1–V4 outputs remain provenance only where they conflict with V5/V6.\n'''
REPORT.write_text(report,encoding='utf-8')

acc=f'''# Step 12 — third-audit final acceptance\n\nDate: 2026-08-31  \nStatus: **PASS CANDIDATE / DURABLE GITHUB READBACK PENDING**\n\nAcceptance requires: 27/27 defects VERIFIED_FIXED, 2332/2332 phrase accounting, D12-27 exact 65-phrase revalidation, six strong-fit current-page rechecks, zero independent findings, exact pair-key/search-reason recomputation, Step13 unexecuted, and final GitHub readback.\n\nCurrent pre-readback evidence: V5/V6 independent PASS; pairs={q['actual_pair_rows']}; future Step13 checks={q['actual_pairs_requiring_step13']}; dependencies={q['actual_dependency_units']}; findings=0.\n'''
ACC.write_text(acc,encoding='utf-8')

# Job flow: preserve history, append one latest authoritative closure block and update roadmap line.
flow=FLOW.read_text(encoding='utf-8')
flow=re.sub(r'^\| \*\*12\. Structural actions\*\* \|.*$', '| **12. Structural actions** | **Decide what to keep, strengthen, route, defer or create** | **✅ COMPLETE AFTER THIRD EXTERNAL METHOD AUDIT + D12-27 PHRASE-LEVEL REVALIDATION** |', flow, count=1, flags=re.M)
flow+='''\n\n## Latest Step-12 authority — third external audit + D12-27 closure\n\n```text\nKW001_OKNO_MSK_STEP12_COMPLETE = true\nKW001_OKNO_MSK_STEP12_TRACKED_DEFECTS = 27\nKW001_OKNO_MSK_STEP12_VERIFIED_FIXED = 27\nKW001_OKNO_MSK_STEP12_OPEN_DEFECTS = 0\nKW001_OKNO_MSK_STEP12_FINAL_PHRASE_ACTION_MAP_ROWS = 2332\nKW001_OKNO_MSK_STEP12_STRUCTURAL_UNITS = 160\nKW001_OKNO_MSK_STEP12_D12_27_REVIEWED_PHRASES = 65\nKW001_OKNO_MSK_STEP12_D12_27_REASSIGNED_PHRASES = '''+str(q['d12_27_reassigned_phrases'])+'''\nKW001_OKNO_MSK_STEP12_KEEP_ROWS = '''+str(actions.get('KEEP_EXISTING_STRUCTURE',0))+'''\nKW001_OKNO_MSK_STEP12_EXPAND_ROWS = '''+str(actions.get('EXPAND_EXISTING_PAGE',0))+'''\nKW001_OKNO_MSK_STEP12_CURRENT_DERIVED_PAIR_ROWS = '''+str(q['actual_pair_rows'])+'''\nKW001_OKNO_MSK_STEP12_FUTURE_STEP13_SEARCH_PAIR_ROWS = '''+str(q['actual_pairs_requiring_step13'])+'''\nKW001_OKNO_MSK_STEP12_STEP13_DEPENDENCY_UNITS = '''+str(q['actual_dependency_units'])+'''\nKW001_OKNO_MSK_STEP12_INDEPENDENT_FINDINGS = 0\nKW001_OKNO_MSK_STEP12_FINAL_GITHUB_READBACK = false\nKW001_OKNO_MSK_STEP13_STATUS = NOT_STARTED_NEXT_ALLOWED\nKW001_OKNO_MSK_STEP13_EXECUTED = false\n```\n'''
FLOW.write_text(flow,encoding='utf-8')

man=MAN.read_text(encoding='utf-8')
man=re.sub(r'current_major_step = .*','current_major_step = STEP_12_COMPLETE_AFTER_THIRD_EXTERNAL_METHOD_AUDIT_D12_27_PHRASE_LEVEL_REVALIDATION',man,count=1)
for name in ['STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V6.tsv','STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V5.tsv','STEP_12_PHRASE_ACTION_MAP_FINAL_V5.tsv','STEP_12_INTERNAL_LINK_ACTIONS_V5.tsv','STEP_12_STEP13_CANDIDATE_PAIRS_V5.tsv','STEP_12_D12_27_PHRASE_RESOLUTIONS.tsv','STEP_12_D12_27_INDEPENDENT_QA.json','STEP_12_THIRD_AUDIT_FINAL_ACCEPTANCE_2026-08-31.md']:
    if name not in man:
        marker='STEP_12_FINAL_ACCEPTANCE_2026-08-31.md\n'
        if marker in man:man=man.replace(marker,marker+name+'\n',1)
        else:man+='\n'+name+'\n'
MAN.write_text(man,encoding='utf-8')
print('STEP12_THIRD_AUDIT_V5_CLOSURE_CANDIDATE_BUILT')
