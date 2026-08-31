import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / 'STEP_12_CORRECTION_DEFECT_LEDGER.tsv'
STATE = ROOT / 'STEP_12_CORRECTION_CURRENT_STATE.json'
PLAN = ROOT / 'STEP_12_CORRECTION_PLAN_2026-08-31.md'

with LEDGER.open(encoding='utf-8', newline='') as f:
    rows = list(csv.DictReader(f, delimiter='\t'))
fields = list(rows[0].keys())
if not any(r['defect_id'] == 'D12-12' for r in rows):
    rows.append({
        'defect_id': 'D12-12',
        'short_name': 'UPSTREAM_OUTSIDE_SCOPE_CONFLICT_WITH_VERIFIED_SITE_OFFER',
        'first_run_behavior': 'Step 12 inherited OUTSIDE_SCOPE/NO_PAGE decisions even when full phrase review exposed member phrases that match verified existing site offers/pages, e.g. blinds and several glazing/window use-case phrases.',
        'why_it_seemed_reasonable': 'Outside-scope states came from accepted upstream clustering/ownership and were therefore treated as frozen business truth.',
        'why_it_is_insufficient_or_wrong': 'Later phrase-level evidence and the persisted site inventory can contradict an upstream outside-scope label. Blind inheritance strands valid demand and can hide an existing page that the site actually offers.',
        'root_cause': 'Upstream status authority was treated as stronger than contradictory current phrase/site evidence instead of triggering an explicit correction overlay.',
        'corrective_action': 'Re-audit every OUTSIDE_SCOPE and NO_STANDALONE member against the verified site inventory and current business scope; create explicit correction rows for in-scope salvageable phrases while preserving upstream history.',
        'verification_required': 'All historical OUTSIDE/NO_PAGE phrases are accounted in a review ledger; any phrase contradicting verified site offer is reassigned or explicitly deferred; known blinds/open-balcony/panoramic-use-case contradictions are resolved; stranded verified-offer phrases = 0.',
        'status': 'OPEN',
        'correction_artifact': '',
        'notes': 'Discovered during D12-01/D12-02 correction preparation; covered by the permanent salvage principle but tracked separately so this concrete failure cannot be lost.'
    })
with LEDGER.open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
    w.writeheader(); w.writerows(rows)

state = json.loads(STATE.read_text(encoding='utf-8'))
if 'D12-12' not in state['open_defects']:
    state['open_defects'].append('D12-12')
if 'D12-12' not in state['correction_order']:
    idx = state['correction_order'].index('D12-09') + 1
    state['correction_order'].insert(idx, 'D12-12')
STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

plan = PLAN.read_text(encoding='utf-8')
heading = '## Correction item 12 — do not blindly inherit OUTSIDE when site evidence contradicts it'
if heading not in plan:
    plan += '''\n## Correction item 12 — do not blindly inherit OUTSIDE when site evidence contradicts it\n\n### What exposed the problem\n\nThe full correction review found phrases marked outside/no-page even though the persisted site inventory shows a matching current offer/page. The clearest example is blinds: the site inventory contains an existing blinds page while the entire curtains/blinds cluster had been inherited as outside scope. Other mixed outside/no-page groups also contain salvageable glazing/window-use-case phrases.\n\n### Why this matters\n\nAn upstream status is historical evidence, not permission to ignore newer contradictory evidence. If the site actually offers the thing and the phrase asks for that thing, the current step must surface the contradiction and create a correction overlay instead of preserving a false outside label for convenience.\n\n### Repair\n\nRe-audit every historical OUTSIDE/NO_STANDALONE phrase against the verified site inventory. Preserve the old state for provenance, but materialize every in-scope correction and prove that no verified-offer phrase remains stranded.\n'''
PLAN.write_text(plan, encoding='utf-8')
