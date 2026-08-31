import csv,json
from pathlib import Path
R=Path(__file__).resolve().parent
K=R.parent.parent
METHOD=K/'STEP_12_STRUCTURAL_ACTION_METHOD.md'
INDEX=K/'STEP_RULES_INDEX.md'
STATE=R/'STEP_12_CORRECTION_CURRENT_STATE.json'
POST=R/'STEP_12_POST_PASS_EVIDENCE_INDEPENDENCE_DEFECT_LEDGER.tsv'
MAN=R/'JOB_MANIFEST.md'
FLOW=R/'JOB_FLOW.md'
REC=R/'STEP_12_D12_28_30_FINAL_RECONCILIATION.json'
QA=R/'STEP_12_D12_28_30_INDEPENDENT_QA.json'
ACC=R/'STEP_12_D12_28_30_FINAL_ACCEPTANCE_2026-08-31.md'

rec=json.loads(REC.read_text(encoding='utf-8')); qa=json.loads(QA.read_text(encoding='utf-8'))
assert rec['status']=='STEP12_D12_28_D12_29_D12_30_FINAL_RECONCILIATION_PASS'
assert qa['status']=='STEP12_D12_28_D12_29_D12_30_INDEPENDENT_PASS' and qa['findings']==0
assert rec['source_active_phrases']==rec['final_phrase_action_rows']==2332
assert rec['quality_gap_without_explicit_missing_need']==0
assert rec['new_page_actions']==0 and rec['proposed_new_refs']==0
assert not rec['step13_executed'] and not qa['step13_executed']

# Defect-specific evidence has already been durably saved/read back by the V6 and reconciliation workflows.
with POST.open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f,delimiter='\t')); fields=list(rows[0])
art={
'D12-28':'STEP_12_D12_28_CURRENT_CONTENT_REVALIDATION.tsv | STEP_12_D12_30_INDEPENDENT_MEMBER_QA.tsv | STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv | STEP_12_PHRASE_ACTION_MAP_FINAL_V6.tsv | STEP_12_D12_28_30_INDEPENDENT_QA.json | STEP_12_D12_28_30_FINAL_RECONCILIATION.json',
'D12-29':'STEP_12_D12_29_CURRENT_LINK_VALIDATION.tsv | STEP_12_INTERNAL_LINK_ACTIONS_V6.tsv | STEP_12_D12_28_30_INDEPENDENT_QA.json | STEP_12_D12_28_30_FINAL_RECONCILIATION.json',
'D12-30':'STEP_12_D12_28_MEMBER_PHRASES_PACKET.tsv | STEP_12_D12_30_PHRASE_RESOLUTIONS.tsv | STEP_12_D12_30_INDEPENDENT_MEMBER_QA.tsv | STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V7.tsv | STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv | STEP_12_PHRASE_ACTION_MAP_FINAL_V6.tsv | STEP_12_STEP13_CANDIDATE_PAIRS_V6.tsv | STEP_12_D12_28_30_INDEPENDENT_QA.json'
}
for r in rows:
    assert r['defect_id'] in art
    r['status']='VERIFIED_FIXED'
    r['correction_artifact']=art[r['defect_id']]
    suffix=' Closed only after current-content/current-link evidence was materialized before action, the complete affected member class was revalidated, downstream V6/V7 artifacts were rebuilt, independent QA returned zero findings, and saved artifacts were durably read back from GitHub.'
    if suffix.strip() not in r['notes']: r['notes']=(r['notes']+suffix).strip()
with POST.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)

# Candidate state: defects are fixed, but Step12 remains blocked until the closure-state commit itself is read back.
verified=[f'D12-{i:02d}' for i in range(1,31)]
state={
 'date':'2026-08-31','step':12,
 'status':'D12_28_D12_29_D12_30_CLOSURE_CANDIDATE_PENDING_FINAL_STATE_READBACK',
 'historical_first_pass_preserved':True,'historical_first_pass_acceptance_withdrawn':True,
 'third_audit_acceptance_preserved_as_superseded':True,
 'post_pass_evidence_independence_correction_complete':True,
 'step13_blocked':True,'open_defects':[],'verified_fixed_defects':verified,'current_correction_item':None,
 'canonical_defect_ledgers':['STEP_12_CORRECTION_DEFECT_LEDGER.tsv','STEP_12_POST_PASS_EVIDENCE_INDEPENDENCE_DEFECT_LEDGER.tsv'],
 'canonical_reusable_method':'../../STEP_12_STRUCTURAL_ACTION_METHOD.md',
 'canonical_evidence_independence_rule':'../../STEP_12_EVIDENCE_INDEPENDENCE_AND_CURRENT_CONTENT_VALIDATION.md',
 'canonical_global_coherence_rule':'../../STEP_12_GLOBAL_COHERENCE_REVALIDATION_GATE.md',
 'current_final_reconciliation':'STEP_12_D12_28_30_FINAL_RECONCILIATION.json',
 'current_independent_qa':'STEP_12_D12_28_30_INDEPENDENT_QA.json',
 'rule':'Defect evidence is verified fixed only from causally upstream current evidence plus independent recomputation. Step completion is withheld until the closure state itself is saved and read back from GitHub.',
 'next_action':'Read back candidate closure state/rules/job authorities from GitHub; only then finalize Step12 completion. Step13 remains blocked during this readback gate.',
 'step13_executed':False,'step13_status':'BLOCKED_PENDING_STEP12_FINAL_STATE_READBACK',
 'step12_complete':False,'next_step_allowed':False,
 'next_major_step':'STEP_12_D12_28_D12_29_D12_30_FINAL_STATE_READBACK',
 'final_github_readback':False,'canonical_closure_readback_passed':False
}
STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Rules index stays non-complete until this candidate state is read back, but explicitly records the successful correction evidence.
t=INDEX.read_text(encoding='utf-8')
old='| **Step 12** | **Structural actions (keep/expand/split/merge/create)** | **REOPENED / POST-PASS D12-28..D12-30 EVIDENCE-INDEPENDENCE + GLOBAL-COHERENCE CORRECTION IN PROGRESS** | **`STEP_12_STRUCTURAL_ACTION_METHOD.md` + `STEP_12_THIRD_AUDIT_EXECUTION_ORDER_CLARIFICATION.md` + `STEP_12_EVIDENCE_INDEPENDENCE_AND_CURRENT_CONTENT_VALIDATION.md` + `STEP_12_GLOBAL_COHERENCE_REVALIDATION_GATE.md` + `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`** — historical D12-01..D12-27 corrections remain valid evidence, but prior completion is withdrawn because action-derived QUALITY_GAP and routing-derived IMPLEMENT states were not independently proven and D12-27 known-regression QA was not a global coherence pass. Current acceptance requires fresh current-content evidence for every affected content-changing action, current source+target validation for every IMPLEMENT link, complete 322-phrase member review for the 20 affected units, downstream rebuild, independent recomputation and GitHub readback. Step 13 remains blocked until current-job closure. |'
new='| **Step 12** | **Structural actions (keep/expand/split/merge/create)** | **CLOSURE CANDIDATE / D12-28..D12-30 EVIDENCE-INDEPENDENCE + GLOBAL-COHERENCE REVALIDATION PASS / FINAL STATE READBACK PENDING** | **`STEP_12_STRUCTURAL_ACTION_METHOD.md` + `STEP_12_THIRD_AUDIT_EXECUTION_ORDER_CLARIFICATION.md` + `STEP_12_EVIDENCE_INDEPENDENCE_AND_CURRENT_CONTENT_VALIDATION.md` + `STEP_12_GLOBAL_COHERENCE_REVALIDATION_GATE.md` + `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`** — post-PASS audit proved why the prior PASS was wrong: action/schema consistency was mistaken for causal evidence, routing edges were mistaken for validated links, and known-regression zero was mistaken for global coherence. Current correction has re-read all 20 historical QUALITY_GAP units (322 phrases), applied 49 exact reassignments, independently revalidated all 28 prior IMPLEMENT links, rebuilt the full 2332-row downstream, and passed independent QA with zero findings. Step remains blocked only until this closure-state commit is itself read back from GitHub. |'
assert old in t;t=t.replace(old,new)
INDEX.write_text(t,encoding='utf-8')

# Main method must itself expose the repeated failure, not rely only on companion docs.
m=METHOD.read_text(encoding='utf-8')
old_status='Status: **APPROVED / ACTIVE AFTER THIRD EXTERNAL METHOD AUDIT + D12-27 PHRASE-LEVEL REVALIDATION — GAP TYPE + PERFORMANCE BOUNDARY + TARGET-VS-RELEVANT + SERP FORMAT + OWNER-GOAL SOURCE + EXISTING-PAGE INTERNAL LINKS**'
if old_status in m:
    m=m.replace(old_status,'Status: **CLOSURE CANDIDATE AFTER D12-28..D12-30 EVIDENCE-INDEPENDENCE + GLOBAL-COHERENCE CORRECTION — FINAL STATE READBACK PENDING**')
section='''\n\n---\n\n# 14. Post-PASS D12-28..D12-30 correction — why the method failed again\n\nThe prior D12-27 closure was later withdrawn after a new external-method audit proved that Step 12 could still pass while material claims were circular or insufficiently falsified. This was **not a lack-of-research failure**. The sources had already identified the right concepts. The failure was translating those concepts into fields and then verifying the fields instead of independently verifying the real-world claim.\n\nCanonical failure chain:\n\n```text\nEXTERNAL PRINCIPLE\n→ ADD FIELD / STATE\n→ GENERATOR POPULATES FIELD FROM ITS OWN ACTION LOGIC\n→ VERIFIER CHECKS FIELD PRESENCE / ACTION CONSISTENCY\n→ FALSE PASS\n```\n\nConcrete failures:\n\n```text\nEXPAND / SECTION\n→ generator wrote QUALITY_GAP\n→ generic gap_evidence restated that fuller coverage was needed\n→ verifier checked that gap_type existed and matched action\n→ current page was not independently required to prove the missing need\n\nROUTING GRAPH EDGE\n→ generator wrote IMPLEMENT internal link\n→ verifier checked source/target fields and coverage\n→ current source context + current target task fit were not independently required\n\nKNOWN D12-27 PHRASES FIXED\n→ exact regression set became zero\n→ verifier treated that as enough\n→ later review found other mixed units outside the known regression set\n```\n\nPermanent root-cause rules:\n\n```text\nSCHEMA COMPLETENESS != EVIDENCE COMPLETENESS\nACTION CONSISTENCY != CAUSAL VALIDATION\nACTION MUST NEVER BE AN EVIDENCE SOURCE FOR ITSELF\nKNOWN URL != PAGE FIT\nROUTING EDGE != IMPLEMENTABLE LINK\nKNOWN_REGRESSION_ZERO != GLOBAL_SEMANTIC_COHERENCE_PASS\n```\n\nTherefore every future Step 12 must also read and obey:\n\n- `STEP_12_EVIDENCE_INDEPENDENCE_AND_CURRENT_CONTENT_VALIDATION.md`;\n- `STEP_12_GLOBAL_COHERENCE_REVALIDATION_GATE.md`;\n- `STEP_12_THIRD_AUDIT_EXECUTION_ORDER_CLARIFICATION.md`;\n- `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`.\n\nCurrent OKNO-MSK correction proof before final state readback:\n\n```text\n20 historical QUALITY_GAP units re-read from current content\n322/322 affected member phrases re-reviewed\n49 exact phrase reassignments\n8 QUALITY_GAP remain, each with explicit missing need\n28/28 historical IMPLEMENT links revalidated\n15 IMPLEMENT retained; 13 downgraded to explicit DEFER states\n2332/2332 final phrase map\n168 structural units\n195 candidate pairs independently reconciled\nindependent findings = 0\nnew page actions = 0\nStep13 executed = false\n```\n\nThe final reusable PASS still requires durable readback of the closure state itself.\n'''
if '# 14. Post-PASS D12-28..D12-30 correction' not in m:m+=section
METHOD.write_text(m,encoding='utf-8')

# Job manifest top-level current state.
man=MAN.read_text(encoding='utf-8')
for old,newv in [
('current_major_step = STEP_12_COMPLETE_AFTER_THIRD_EXTERNAL_METHOD_AUDIT_D12_27_PHRASE_LEVEL_REVALIDATION','current_major_step = STEP_12_D12_28_D12_29_D12_30_CLOSURE_CANDIDATE_PENDING_FINAL_STATE_READBACK'),
('next_major_step = STEP_13_PRE_STEP_METHODOLOGY_RESEARCH_AND_REVIEW','next_major_step = STEP_12_FINAL_STATE_READBACK_THEN_STEP_13_PRE_STEP_METHODOLOGY_RESEARCH_AND_REVIEW')]:
    if old in man:man=man.replace(old,newv,1)
manifest_append='''\n\n## Latest Step-12 authority — post-PASS D12-28..D12-30 correction\n\nStatus: **CLOSURE CANDIDATE / FINAL STATE READBACK PENDING**\n\nCanonical current artifacts:\n\n```text\n../../STEP_12_EVIDENCE_INDEPENDENCE_AND_CURRENT_CONTENT_VALIDATION.md\n../../STEP_12_GLOBAL_COHERENCE_REVALIDATION_GATE.md\nSTEP_12_D12_28_CURRENT_CONTENT_REVALIDATION.tsv\nSTEP_12_D12_29_CURRENT_LINK_VALIDATION.tsv\nSTEP_12_D12_30_PHRASE_RESOLUTIONS.tsv\nSTEP_12_D12_30_INDEPENDENT_MEMBER_QA.tsv\nSTEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V7.tsv\nSTEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv\nSTEP_12_PHRASE_ACTION_MAP_FINAL_V6.tsv\nSTEP_12_INTERNAL_LINK_ACTIONS_V6.tsv\nSTEP_12_STEP13_CANDIDATE_PAIRS_V6.tsv\nSTEP_12_D12_28_30_INDEPENDENT_QA.json\nSTEP_12_D12_28_30_FINAL_RECONCILIATION.json\nSTEP_12_D12_28_30_FINAL_ACCEPTANCE_2026-08-31.md\n```\n\nUntil closure-state readback completes, Step 13 remains blocked.\n'''
if '## Latest Step-12 authority — post-PASS D12-28..D12-30 correction' not in man:man+=manifest_append
MAN.write_text(man,encoding='utf-8')

# Job flow keeps history but appends the new current authority and updates the roadmap row.
flow=FLOW.read_text(encoding='utf-8')
oldrow='| **12. Structural actions** | **Decide what to keep, strengthen, route, defer or create** | **✅ COMPLETE AFTER THIRD EXTERNAL METHOD AUDIT + D12-27 PHRASE-LEVEL REVALIDATION** |'
newrow='| **12. Structural actions** | **Decide what to keep, strengthen, route, defer or create** | **🔁 CLOSURE CANDIDATE AFTER D12-28..D12-30 / FINAL STATE READBACK PENDING** |'
if oldrow in flow:flow=flow.replace(oldrow,newrow)
flow_append=f'''\n\n## Post-PASS Step-12 correction — D12-28..D12-30\n\nStatus: **CLOSURE CANDIDATE / FINAL STATE READBACK PENDING**\n\nWhy the previous PASS was withdrawn:\n\n```text\nSCHEMA COMPLETENESS WAS TREATED AS EVIDENCE COMPLETENESS\nACTION CONSISTENCY WAS TREATED AS CAUSAL VALIDATION\nROUTING GRAPH EDGE WAS TREATED AS IMPLEMENTABLE LINK PROOF\nKNOWN D12-27 REGRESSION ZERO WAS TREATED AS GLOBAL COHERENCE\n```\n\nCurrent independently verified correction:\n\n```text\nSOURCE_ACTIVE_PHRASES = {rec['source_active_phrases']}\nFINAL_PHRASE_ACTION_ROWS = {rec['final_phrase_action_rows']}\nASSIGNED = {rec['assigned_phrases']}\nUNRESOLVED_OR_SEARCH_REQUIRED = {rec['unresolved_or_search_required_phrases']}\nSTRUCTURAL_UNITS = {rec['final_structural_units']}\nAFFECTED_SOURCE_UNITS = {rec['affected_source_units']}\nAFFECTED_SOURCE_PHRASES = {rec['affected_source_phrases']}\nEXACT_REASSIGNMENTS = {rec['exact_reassignments']}\nQUALITY_GAP_AFTER_REVALIDATION = {rec['quality_gap_units_after_revalidation']}\nQUALITY_GAP_WITHOUT_EXPLICIT_MISSING_NEED = {rec['quality_gap_without_explicit_missing_need']}\nPRIOR_IMPLEMENT_LINKS_REVIEWED = {rec['prior_implement_links_reviewed']}\nRETAINED_IMPLEMENT_LINKS = {rec['retained_implement_links']}\nFINAL_LINK_ROWS = {rec['final_link_rows']}\nCANDIDATE_PAIRS = {rec['candidate_pairs']}\nPAIRS_REQUIRING_STEP13 = {rec['pairs_requiring_step13']}\nSTEP13_DEPENDENCY_UNITS = {rec['step13_dependency_units']}\nNEW_PAGE_ACTIONS = {rec['new_page_actions']}\nPROPOSED_NEW_REFS = {rec['proposed_new_refs']}\nINDEPENDENT_FINDINGS = {rec['independent_findings']}\nSTEP13_EXECUTED = false\n```\n\nStep 13 remains blocked until this closure-state commit receives durable GitHub readback.\n'''
if '## Post-PASS Step-12 correction — D12-28..D12-30' not in flow:flow+=flow_append
FLOW.write_text(flow,encoding='utf-8')

ACC.write_text(f'''# Step 12 — D12-28..D12-30 final acceptance\n\nDate: 2026-08-31  \nStatus: **CLOSURE CANDIDATE / FINAL STATE READBACK PENDING**\n\nThe previous D12-27 PASS was withdrawn because later external-method review proved three additional failure classes:\n\n- D12-28 — QUALITY_GAP / EXPAND / SECTION could be generated from the action instead of independently proven from current page deficits;\n- D12-29 — IMPLEMENT links could be generated from the routing graph without current source-context + target-fit validation;\n- D12-30 — zero known D12-27 regressions did not prove global coherence across the later affected class.\n\nPermanent non-repeat controls are now in `STEP_12_EVIDENCE_INDEPENDENCE_AND_CURRENT_CONTENT_VALIDATION.md` and `STEP_12_GLOBAL_COHERENCE_REVALIDATION_GATE.md`, and the main Step-12 method explicitly records why the prior PASS was false.\n\nCorrection evidence before final closure-state readback:\n\n```text\nD12-28..D12-30 defect-specific status = VERIFIED_FIXED\n2332/2332 final phrase-action accounting\n322/322 affected phrases independently reviewed\n49 exact phrase reassignments\n168 final structural units\n8 final QUALITY_GAP, all with explicit missing needs\n28/28 prior IMPLEMENT links current-content revalidated\n15 IMPLEMENT retained\n13 prior IMPLEMENT downgraded to DEFER\n58 final link rows\n195/195 independently reconciled candidate pairs\nnew page actions = 0\nproposed-new refs = 0\nindependent findings = 0\nStep13 executed = false\n```\n\nStep 12 is **not yet marked complete in this candidate commit**. Completion is allowed only after this candidate state, method authority, rules index, defect ledger and job authorities are read back from GitHub.\n''',encoding='utf-8')
print('STEP12_D12_28_30_CLOSURE_CANDIDATE_READY')
