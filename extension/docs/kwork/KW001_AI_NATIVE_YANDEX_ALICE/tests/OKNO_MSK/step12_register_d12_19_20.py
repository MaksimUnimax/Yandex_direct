import csv,json
from pathlib import Path
R=Path(__file__).resolve().parent
LED=R/'STEP_12_CORRECTION_DEFECT_LEDGER.tsv'
STATE=R/'STEP_12_CORRECTION_CURRENT_STATE.json'
CH=R/'STEP_12_POST_CLOSE_OWNER_CHALLENGE_2026-08-31.md'

with LED.open(encoding='utf-8',newline='') as f:
    rows=list(csv.DictReader(f,delimiter='\t')); fields=list(rows[0].keys())
by={r['defect_id'] for r in rows}
new=[
{
'defect_id':'D12-19','short_name':'SECOND_FALSE_CREATE_EXISTING_REPLACEMENT_PAGE','first_run_behavior':'Step 12 proposed PROPOSED_NEW:/uslugi/zamena-okon/ for WINDOW_REPLACEMENT_SERVICE.','why_it_seemed_reasonable':'Step 11 had only MEDIUM replacement ownership and the known installation page was broader; strong Wordstat demand made a standalone replacement service page look plausible.','why_it_is_insufficient_or_wrong':'Fresh current-site discovery proves an existing commercial landing /okna-rehau/po-tipu-doma/zamena-okon-v-kvartire/ already offers window replacement with price, CTA, product options and installation workflow. A second replacement landing could duplicate/overlap the live page.','root_cause':'The same stale-absence failure as D12-16: Step 12 trusted the earlier inventory/ownership gap instead of re-running current existence discovery immediately before CREATE.','corrective_action':'Withdraw the proposed /uslugi/zamena-okon/ CREATE. Re-audit replacement phrases against the existing replacement-in-apartment page, installation page, aluminium family and repair/replacement decision content.','verification_required':'No replacement NEW_* action remains unless a fresh current-site check proves a distinct uncovered task; current existing replacement page is materialized as a candidate/owner; final phrase/action map and pair graph are rebuilt.','status':'OPEN','correction_artifact':'','notes':'Registered after owner-requested all-candidate fresh recheck.'
},
{
'defect_id':'D12-20','short_name':'HARDWARE_GUIDE_EXISTING_CONTENT_REUSE_NOT_AUDITED','first_run_behavior':'Step 12 proposed a new broad informational guide /stati/okonnaya-furnitura-vidy-brendy-kak-vybrat/.','why_it_seemed_reasonable':'The hardware-selection unit had a coherent informational theme, some direct Wordstat demand, and no single dedicated guide in the accepted Step-1 inventory.','why_it_is_insufficient_or_wrong':'Current first-party content already contains a substantial hardware-selection section inside /stati/kak-vybrat-plastikovye-okna/ and multiple specific hardware/accessory pages. A page-ownership gap was incorrectly treated as a content gap.','root_cause':'Step 12 checked whether one exact owner existed but did not run a fresh existing-content reuse audit across broader current articles and component pages before CREATE.','corrective_action':'Withdraw broad hardware-guide CREATE unless a fresh reuse audit proves a remaining standalone task. Prefer expanding the current choose-windows article and routing specific component/purchase/maintenance needs to existing pages.','verification_required':'No hardware-guide NEW_* action remains without proof of an uncovered content gap after current-site reuse audit; affected units have explicit existing-page actions; final map/QA rebuilt.','status':'OPEN','correction_artifact':'','notes':'Specific current-job instance of the new reusable existing-content reuse gate.'
}
]
for x in new:
    if x['defect_id'] not in by: rows.append(x)
with LED.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)

s=json.loads(STATE.read_text(encoding='utf-8'))
for d in ['D12-19','D12-20']:
    if d not in s['open_defects']: s['open_defects'].append(d)
    if d not in s['correction_order']: s['correction_order'].append(d)
s['current_correction_item']='D12-16'
s['next_action']='Resolve D12-16..D12-20 under the new current-site freshness, owner-goal and existing-content reuse gates; re-evaluate all five former new-page candidates; rebuild Step12 outputs and independent QA. Step13 remains blocked.'
s['step13_blocked']=True;s['step12_complete']=False;s['next_step_allowed']=False;s['step13_status']='BLOCKED_BY_REOPENED_STEP12';s['final_github_readback']=False;s['canonical_closure_readback_passed']=False
STATE.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

text=CH.read_text(encoding='utf-8')
if '## D12-19 — second false CREATE' not in text:
    text += '''\n---\n\n## D12-19 — second false CREATE: replacement page already exists\n\nThe accepted Step 12 proposed `PROPOSED_NEW:/uslugi/zamena-okon/`. Fresh first-party discovery found `https://okno-msk.ru/okna-rehau/po-tipu-doma/zamena-okon-v-kvartire/`, a current commercial page with price, CTA, replacement rationale, product options and installation workflow. This proves the stale-absence failure was systematic, not a one-off panoramic-page miss. Withdraw CREATE and re-audit the replacement phrase set against current replacement/installation/aluminium/repair pages.\n\nStatus: **OPEN**\n\n---\n\n## D12-20 — hardware guide CREATE ignored existing-content reuse\n\nThe accepted Step 12 proposed `PROPOSED_NEW:/stati/okonnaya-furnitura-vidy-brendy-kak-vybrat/`. Fresh current-site review shows that `/stati/kak-vybrat-plastikovye-okna/` already contains a substantial hardware-selection section, while specific hardware/accessory pages cover product-level needs. The old logic confused `no single exact owner` with `no useful current content`. Withdraw broad CREATE unless a fresh content-reuse audit proves a distinct uncovered task; prefer expand/section/route actions first.\n\nStatus: **OPEN**\n'''
    CH.write_text(text,encoding='utf-8')
print('D12_19_20_REGISTERED')
