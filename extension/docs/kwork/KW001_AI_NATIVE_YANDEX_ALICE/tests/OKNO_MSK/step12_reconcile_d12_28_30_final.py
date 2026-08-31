import csv,json
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parent

def read(name):
    with (R/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))

a=read('STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv')
x=read('STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V7.tsv')
m=read('STEP_12_PHRASE_ACTION_MAP_FINAL_V6.tsv')
l=read('STEP_12_INTERNAL_LINK_ACTIONS_V6.tsv')
p=read('STEP_12_STEP13_CANDIDATE_PAIRS_V6.tsv')
q=json.loads((R/'STEP_12_D12_28_30_INDEPENDENT_QA.json').read_text(encoding='utf-8'))
b=json.loads((R/'STEP_12_D12_28_30_BUILD_QA.json').read_text(encoding='utf-8'))

assert q['status']=='STEP12_D12_28_D12_29_D12_30_INDEPENDENT_PASS' and q['findings']==0
assert len(x)==len(m)==2332
assert sum(bool(r.get('final_structural_unit_id')) for r in x)==2313
assert len(a)==168
assert len(p)==195
assert q['expected_pair_keys']==q['actual_pair_rows']==195
assert not q['step13_executed']

out={
 'date':'2026-08-31',
 'status':'STEP12_D12_28_D12_29_D12_30_FINAL_RECONCILIATION_PASS',
 'source_active_phrases':2332,
 'assigned_phrases':2313,
 'unresolved_or_search_required_phrases':19,
 'final_phrase_action_rows':len(m),
 'final_structural_units':len(a),
 'structural_action_counts':dict(sorted(Counter(r['structural_action'] for r in a).items())),
 'structural_gap_counts':dict(sorted(Counter(r.get('structural_gap_state','') for r in a).items())),
 'content_enhancement_counts':dict(sorted(Counter(r.get('content_enhancement_state','') for r in a).items())),
 'legacy_gap_type_counts':dict(sorted(Counter(r.get('gap_type','') for r in a).items())),
 'recommendation_maturity_counts':dict(sorted(Counter(r.get('recommendation_maturity','') for r in a).items())),
 'final_confidence_counts':dict(sorted(Counter(r.get('final_confidence','') for r in a).items())),
 'link_action_counts':dict(sorted(Counter(r['link_action_state'] for r in l).items())),
 'final_link_rows':len(l),
 'prior_implement_links_reviewed':q['old_implement_links_reviewed'],
 'retained_implement_links':q['retained_implement_links'],
 'affected_source_units':q['affected_source_units'],
 'affected_source_phrases':q['affected_source_phrases'],
 'exact_reassignments':q['exact_reassignments'],
 'quality_gap_units_after_revalidation':q['final_quality_gap_units'],
 'candidate_pairs':len(p),
 'pairs_requiring_step13':sum(r['later_direct_search_check_needed']=='true' for r in p),
 'step13_dependency_units':sum(r.get('step13_dependency_required','').lower()=='true' for r in a),
 'new_page_actions':sum(r['structural_action'] in {'NEW_COMMERCIAL_PAGE','NEW_INFORMATIONAL_PAGE'} for r in a),
 'proposed_new_refs':sum('PROPOSED_NEW:' in (r.get('primary_page_candidate','')+' '+r.get('supporting_page','')) for r in a),
 'quality_gap_without_explicit_missing_need':b['quality_gap_without_explicit_missing_need'],
 'independent_findings':q['findings'],
 'final_github_readback_pending':True,
 'step13_executed':False,
 'reconciliation_origin':'V7_ASSIGNMENTS_V6_ACTIONS_V6_MAP_V6_LINKS_V6_PAIRS_PLUS_INDEPENDENT_D12_28_29_30_QA'
}
assert out['new_page_actions']==0
assert out['proposed_new_refs']==0
assert out['quality_gap_without_explicit_missing_need']==0
(R/'STEP_12_D12_28_30_FINAL_RECONCILIATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
