import csv, json
from pathlib import Path

R = Path(__file__).resolve().parent
LEDGER = R / 'STEP_12_CORRECTION_DEFECT_LEDGER.tsv'
STATE = R / 'STEP_12_CORRECTION_CURRENT_STATE.json'
FLOW = R / 'JOB_FLOW.md'
INCIDENT = R / 'STEP_12_THIRD_EXTERNAL_METHOD_AUDIT_GAPS_2026-08-31.md'

FIELDS = ['defect_id','short_name','first_run_behavior','why_it_seemed_reasonable','why_it_is_insufficient_or_wrong','root_cause','corrective_action','verification_required','status','correction_artifact','notes']

NEW = [
    {
        'defect_id':'D12-21','short_name':'CONTENT_GAP_TYPE_NOT_EXPLICIT',
        'first_run_behavior':'V3 records current_page_fit and existing_content_reuse but does not explicitly classify whether the remaining problem is a topic gap, intent gap, quality gap, originality/value gap, mixed gap, or insufficient evidence.',
        'why_it_seemed_reasonable':'The selected structural action already implied much of the diagnosis: CREATE suggested absence, EXPAND suggested under-coverage, and ROUTE suggested another current owner.',
        'why_it_is_insufficient_or_wrong':'Different gap causes can lead to the same action label but require different implementation. Without an explicit gap type, CREATE can be justified by an ownership gap, while UPDATE can hide an intent mismatch or quality problem.',
        'root_cause':'The method moved directly from user task/current page evidence to structural action instead of materializing the intermediate content-gap diagnosis required by current content-gap methodology.',
        'corrective_action':'Add GAP_TYPE and GAP_EVIDENCE to every final structural unit. Allowed states: NONE, TOPIC_GAP, INTENT_GAP, QUALITY_GAP, ORIGINALITY_GAP, MIXED_GAP, EVIDENCE_INSUFFICIENT. CREATE may survive only a verified TOPIC_GAP after all other gates.',
        'verification_required':'160/160 final units have gap_type and gap_evidence; no CREATE exists without TOPIC_GAP; all EXPAND/SECTION/ROUTE actions have a gap diagnosis consistent with the action; independent QA recomputes coverage.',
        'status':'OPEN','correction_artifact':'','notes':'Raised by third external method audit after Semrush 2026 content-gap guidance.'
    },
    {
        'defect_id':'D12-22','short_name':'KEEP_OVERSTATES_NO_CHANGE_WITHOUT_PERFORMANCE_DATA',
        'first_run_behavior':'KEEP_EXISTING_STRUCTURE can be read as a final recommendation that the page needs no further work even though the base job has no Yandex Webmaster/Metrika conversion/performance access.',
        'why_it_seemed_reasonable':'Step 12 is a structural step and a strong page/task fit is enough to say the existing URL is the correct structural owner.',
        'why_it_is_insufficient_or_wrong':'A structurally correct owner can still need content/SEO/conversion improvement. Current content-audit guidance uses performance and business outcomes to distinguish keep-as-is from update. Without those data, "keep structure" must not be presented as "no optimization needed".',
        'root_cause':'The action label collapsed structural ownership and page-performance/content sufficiency into one human-readable conclusion.',
        'corrective_action':'Separate STRUCTURAL_OWNER_DECISION from OPTIMIZATION_STATE. Preserve KEEP_EXISTING_STRUCTURE only as structural ownership. Add PERFORMANCE_EVIDENCE_STATE and OPTIMIZATION_READINESS; when account analytics are unavailable, use NOT_AVAILABLE_IN_BASE_SCOPE and do not claim NO_CONTENT_CHANGE_NEEDED.',
        'verification_required':'Every KEEP row explicitly states structural-only meaning; 58 historical KEEP rows do not imply no optimization; performance evidence state is materialized for 160/160 units; missing analytics cannot produce a content-performance PASS claim.',
        'status':'OPEN','correction_artifact':'','notes':'Base Kwork scope excludes Webmaster/Metrika account access; correction must preserve that scope rather than fabricate data.'
    },
    {
        'defect_id':'D12-23','short_name':'TARGET_VS_YANDEX_RELEVANT_URL_NOT_MATERIALIZED',
        'first_run_behavior':'Step 12 stores the intended primary page but does not expose, per structural unit, whether ordinary Yandex Search actually selected that URL, another target-domain URL, no target-domain URL, or the query was not directly checked.',
        'why_it_seemed_reasonable':'Step 11 already documented that TARGET_URL is intended ownership and the Step-9/11 target domain often did not rank in the sampled top results.',
        'why_it_is_insufficient_or_wrong':'An intended target and a search-engine-selected relevant URL are different facts. A mismatch can change whether KEEP/EXPAND is safe or whether Step 13 needs a stronger boundary review.',
        'root_cause':'Search evidence was summarized as search_boundary_support instead of materializing the explicit intended-target versus observed-relevant-URL state.',
        'corrective_action':'Add INTENDED_TARGET_URL, CURRENT_YANDEX_RELEVANT_URL, and RELEVANT_URL_MATCH_STATE = MATCH / MISMATCH / SITE_NOT_OBSERVED / NOT_DIRECTLY_CHECKED. Populate from persisted Step-9/11 evidence only; never infer rankings.',
        'verification_required':'160/160 units have an explicit match state; observed relevant URLs come only from persisted ordinary Search evidence; no NOT_DIRECTLY_CHECKED row is represented as MATCH; MISMATCH/SITE_NOT_OBSERVED cannot silently strengthen maturity.',
        'status':'OPEN','correction_artifact':'','notes':'No new paid Search is authorized merely to fill missing states.'
    },
    {
        'defect_id':'D12-24','short_name':'SERP_CONTENT_TYPE_FORMAT_ANGLE_NOT_EXPLICIT',
        'first_run_behavior':'search_boundary_support records whether Search evidence exists but does not separately preserve the expected content type, format and angle observed for material page-boundary cases.',
        'why_it_seemed_reasonable':'Broad intent classes and direct Search decisions were enough for many obvious commercial/product/service owners.',
        'why_it_is_insufficient_or_wrong':'Informational or commercial intent alone does not tell whether Search expects a how-to, comparison, list, calculator, landing page, product page, forum/reviews or other format. That distinction can change structural action.',
        'root_cause':'SERP evidence was compressed into one support-strength field instead of preserving the format dimensions that justified the boundary.',
        'corrective_action':'For units with direct material Search evidence, add SERP_EXPECTED_CONTENT_TYPE, SERP_EXPECTED_FORMAT and SERP_EXPECTED_ANGLE; otherwise explicitly mark NOT_OBSERVED/NOT_MATERIAL. Do not fabricate a format from broad intent.',
        'verification_required':'Every structural unit has explicit SERP format-state fields; direct-evidence units preserve observed format/angle where supported; non-observed rows remain explicit; format evidence is used only where it can change the page boundary.',
        'status':'OPEN','correction_artifact':'','notes':'Third external audit source: Ahrefs/Semrush guidance on SERP content type/format/angle.'
    },
    {
        'defect_id':'D12-25','short_name':'OWNER_GOAL_EVIDENCE_SOURCE_NOT_STRONG_ENOUGH',
        'first_run_behavior':'V3 often infers owner goals from public site role and stores that inference, but the source strength does not fully constrain recommendation maturity when the owner policy could materially change the content strategy.',
        'why_it_seemed_reasonable':'The public commercial site usually makes the primary lead/sales objective obvious, and the base package does not include internal sales/support interviews.',
        'why_it_is_insufficient_or_wrong':'Public-site inference is weaker than a client-stated objective, analytics or sales/support evidence. Some businesses intentionally use low-direct-conversion informational content for authority or top-of-funnel acquisition.',
        'root_cause':'Owner goal was added as a field after the second audit, but evidence-source hierarchy and owner-policy uncertainty were not fully integrated into maturity/action readiness.',
        'corrective_action':'Add OWNER_GOAL_EVIDENCE_SOURCE = CLIENT_STATED / ANALYTICS_OBSERVED / SALES_SUPPORT_EVIDENCE / PUBLIC_SITE_INFERRED / UNKNOWN and OWNER_POLICY_MATERIALITY. If a policy-sensitive action relies only on inference, mark provisional or OWNER_POLICY_REQUIRED rather than treating inference as explicit owner instruction.',
        'verification_required':'160/160 units have owner-goal source; policy-sensitive content actions identify materiality; no inferred owner goal is described as client-stated; missing owner policy remains visible instead of guessed.',
        'status':'OPEN','correction_artifact':'','notes':'Does not require expanding Kwork scope; it requires honest evidence-source labeling.'
    },
    {
        'defect_id':'D12-26','short_name':'INTERNAL_LINK_IMPLEMENTATION_NOT_MATERIALIZED_FOR_EXISTING_PAGE_ACTIONS',
        'first_run_behavior':'Detailed hierarchy/internal-link plans were built for proposed new pages, while many final ROUTE, SECTION and EXPAND actions only contain primary/supporting URLs and not a concrete implementable link instruction.',
        'why_it_seemed_reasonable':'Primary/supporting URLs already express the conceptual relationship, and the initial hierarchy task focused on avoiding orphaned new pages.',
        'why_it_is_insufficient_or_wrong':'After all five CREATE ideas were withdrawn, most structural value is now in relationships among existing pages. A ROUTE recommendation without source URL, target URL, placement/purpose and anchor context is not fully implementable.',
        'root_cause':'Internal linking was treated mainly as a new-page hierarchy concern instead of part of every existing-page routing/section decision.',
        'corrective_action':'Build STEP_12_INTERNAL_LINK_ACTIONS.tsv for material ROUTE/SECTION/EXPAND/supporting relationships with source_url, target_url, relation_type, placement_context, anchor_concept, user_journey_purpose, business_handoff and evidence origin. Do not invent a link where source/target context is unsupported.',
        'verification_required':'Every material ROUTE relation has at least one explicit implementable link action or a justified NOT_APPLICABLE/DEFER state; link source/target URLs are current/known; zero links point to withdrawn PROPOSED_NEW pages; independent QA checks coverage and duplicates.',
        'status':'OPEN','correction_artifact':'','notes':'Especially material now that current architecture has 46 ROUTE, 12 SECTION and 14 EXPAND actions and zero new pages.'
    },
]

with LEDGER.open(encoding='utf-8', newline='') as f:
    rows = list(csv.DictReader(f, delimiter='\t'))
by = {r['defect_id']: r for r in rows}
for item in NEW:
    if item['defect_id'] in by:
        raise RuntimeError(f"defect already exists: {item['defect_id']}")
rows.extend(NEW)
with LEDGER.open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS, delimiter='\t', lineterminator='\n')
    w.writeheader(); w.writerows(rows)

state = json.loads(STATE.read_text(encoding='utf-8'))
new_ids = [x['defect_id'] for x in NEW]
state['status'] = 'REOPENED_AFTER_THIRD_EXTERNAL_METHOD_AUDIT'
state['open_defects'] = new_ids
state['verified_fixed_defects'] = [x for x in state.get('verified_fixed_defects', []) if x not in new_ids]
state['current_correction_item'] = new_ids[0]
for d in new_ids:
    if d not in state['correction_order']:
        state['correction_order'].append(d)
state['step13_blocked'] = True
state['step12_complete'] = False
state['next_step_allowed'] = False
state['next_major_step'] = 'STEP_12_THIRD_EXTERNAL_METHOD_AUDIT_CORRECTION'
state['step13_status'] = 'BLOCKED_BY_REOPENED_STEP12'
state['step13_executed'] = False
state['final_github_readback'] = False
state['canonical_closure_readback_passed'] = False
state['next_action'] = 'Resolve D12-21..D12-26: gap typing, structural-vs-performance separation, target-vs-relevant URL state, SERP format/angle evidence, owner-goal evidence source, and implementable internal-link actions; rebuild Step12 outputs and independent QA before Step13.'
STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

incident = '''# Step 12 — third external method audit gaps\n\nDate: 2026-08-31\nStatus: **REOPEN STEP 12 / D12-21..D12-26 REGISTERED**\n\nThe third external literature audit found six method gaps that remained after the second correction. They are registered before repair so they cannot disappear from chat context or be silently absorbed into a later PASS.\n\n- D12-21: explicit content-gap type missing.\n- D12-22: structural KEEP can be misread as performance/content "do nothing" without analytics.\n- D12-23: intended target vs observed Yandex relevant URL not materialized.\n- D12-24: SERP content type / format / angle not explicit.\n- D12-25: owner-goal evidence source strength not fully reflected in readiness.\n- D12-26: internal-link implementation not materialized for existing-page actions.\n\nUntil all six are independently corrected and read back from GitHub:\n\n```text\nSTEP12_COMPLETE = false\nSTEP13_BLOCKED = true\nSTEP13_EXECUTED = false\n```\n'''
INCIDENT.write_text(incident, encoding='utf-8')

flow = FLOW.read_text(encoding='utf-8')
flow += '\n\n## Third external-method audit reopen — 2026-08-31\n\n```text\nKW001_OKNO_MSK_STEP12_COMPLETE = false\nKW001_OKNO_MSK_STEP12_THIRD_AUDIT_OPEN_DEFECTS = D12-21,D12-22,D12-23,D12-24,D12-25,D12-26\nKW001_OKNO_MSK_STEP13_STATUS = BLOCKED_BY_REOPENED_STEP12\nKW001_OKNO_MSK_STEP13_EXECUTED = false\n```\n'
FLOW.write_text(flow, encoding='utf-8')

print('STEP12_THIRD_AUDIT_DEFECTS_REGISTERED', ','.join(new_ids))
