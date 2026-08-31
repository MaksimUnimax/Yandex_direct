import csv,json
from pathlib import Path
R=Path(__file__).resolve().parent
LED=R/'STEP_12_CORRECTION_DEFECT_LEDGER.tsv'
STATE=R/'STEP_12_CORRECTION_CURRENT_STATE.json'
with LED.open(encoding='utf-8',newline='') as f:
    rows=list(csv.DictReader(f,delimiter='\t')); fields=list(rows[0].keys())
by={r['defect_id']:r for r in rows}
new=[
{
'defect_id':'D12-16','short_name':'FALSE_CREATE_PANORAMIC_EXISTING_PAGE_MISSED','first_run_behavior':'Step 12 proposed PROPOSED_NEW:/panoramnye-okna/ for the panoramic commercial core.','why_it_seemed_reasonable':'The accepted Step-1 inventory contained panoramic balcony and informational pages but not the broad current commercial panoramic landing; strong Wordstat demand and a coherent commercial task made a new page look like a real gap.','why_it_is_insufficient_or_wrong':'Fresh first-party discovery proved a full current commercial landing already exists at /okna-rehau/panoramnoe-osteklenie/ with price, order/measurement CTA, product options, installation and warranty. CREATE would manufacture a duplicate/overlap problem.','root_cause':'Old inventory absence and Step-11 no-owner state were treated as current absence. The external method said to review existing pages, but that principle had not been converted into a mandatory fresh immediately-before-CREATE execution gate.','corrective_action':'Withdraw the panoramic CREATE; reuse the current commercial page as primary; route informational/object/private-house panoramic tasks to existing current pages; add CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md and require fresh current-site checks immediately before CREATE.','verification_required':'Panoramic NEW_* action = 0; primary current commercial page is /okna-rehau/panoramnoe-osteklenie/; no withdrawn PROPOSED_NEW panoramic reference remains; V3 phrase map/pair graph independently passes and GitHub readback succeeds.','status':'OPEN','correction_artifact':'','notes':'Post-close owner challenge. This defect proves NOT_FOUND_IN_OLD_INVENTORY != ABSENT_NOW.'
},
{
'defect_id':'D12-17','short_name':'DIY_INSTALLATION_CONFLICTS_WITH_OWNER_COMMERCIAL_OBJECTIVE','first_run_behavior':'Step 12 proposed a standalone step-by-step PVC-window self-installation article because the informational task had strong demand and direct informational Search evidence.','why_it_seemed_reasonable':'The user task was coherent, demand was strong, informational SERPs supported a guide format and the company has genuine installation expertise. Under an SEO-only model the opportunity looked strong.','why_it_is_insufficient_or_wrong':'The live site sells professional installation as a core paid service and explicitly discourages self-installation because of technical, quality and safety risks. A neutral enabling DIY tutorial can help users avoid the paid outcome the owner is trying to sell.','root_cause':'BUSINESS_TRUTH was confused with OWNER_BUSINESS_GOAL_ALIGNMENT. The method asked whether the business could truthfully discuss the topic but not whether ranking in the proposed format advances the owner’s desired outcome. External research about business relevance remained narrative instead of an explicit field/gate.','corrective_action':'Withdraw the neutral DIY CREATE. Serve the informational need through the professional installation page using requirements, risks, preparation, common mistakes and professional-service rationale. Add explicit OWNER_PRIMARY_GOAL, DESIRED_USER_OUTCOME, BUSINESS_POTENTIAL, CONTENT_ROLE and COUNTERPRODUCTIVE_TO_CORE_OFFER controls.','verification_required':'DIY installation NEW_INFORMATIONAL_PAGE = 0; unit routes to current installation service with business-aligned content role; owner-goal/business-potential fields are populated; independent V3 QA/readback passes.','status':'OPEN','correction_artifact':'','notes':'Post-close owner challenge. SEARCH_DEMAND != BUSINESS_VALUE.'
},
{
'defect_id':'D12-18','short_name':'BROAD_DIY_REPAIR_CREATE_IGNORED_EXISTING_CONTENT_AND_PAID_SERVICE_BOUNDARY','first_run_behavior':'Step 12 proposed one broad new DIY repair + adjustment page serving several repair/maintenance/operation subunits.','why_it_seemed_reasonable':'The paid repair page did not own the whole informational task; demand existed and a broad guide seemed capable of consolidating useful self-help.','why_it_is_insufficient_or_wrong':'The current site already publishes substantial low-risk self-help for adjustment, seasonal mode and opening problems, while complex repair is a paid professional service. The proposed broad guide duplicated current self-help and blurred the safe-self-help -> paid-repair boundary.','root_cause':'NO_SINGLE_OWNER was promoted to CONTENT_GAP. Step 12 checked exact page ownership but did not audit distributed current content coverage and owner-intended handoff before NEW_INFORMATIONAL_PAGE.','corrective_action':'Withdraw the broad DIY repair/adjustment CREATE. Reuse exact current self-help pages for low-risk tasks, use repair service as professional handoff, and require existing-content reuse audit before every informational CREATE.','verification_required':'Broad DIY repair NEW_* action = 0; adjustment/operation/maintenance tasks route to current self-help pages and complex repair to current repair service; no withdrawn proposed DIY URL survives; V3 independent QA/readback passes.','status':'OPEN','correction_artifact':'','notes':'Post-close owner challenge. PAGE_OWNERSHIP_GAP != CONTENT_GAP.'
}
]
for x in new:
    if x['defect_id'] not in by:
        rows.append(x)
# stable numeric ordering
rows.sort(key=lambda r:int(r['defect_id'].split('-')[1]))
with LED.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
s=json.loads(STATE.read_text(encoding='utf-8'))
for d in ['D12-16','D12-17','D12-18']:
    if d not in s['open_defects']:s['open_defects'].append(d)
    if d not in s['correction_order']:s['correction_order'].append(d)
s['open_defects']=sorted(set(s['open_defects']),key=lambda x:int(x.split('-')[1]))
s['correction_order']=sorted(set(s['correction_order']),key=lambda x:int(x.split('-')[1]))
STATE.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('STEP12_D12_16_18_LEDGER_REGISTERED')
