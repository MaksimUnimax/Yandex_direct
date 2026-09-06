from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / 'STEP_RULES_INDEX.md'
LEGACY = ROOT / 'STEP_20_CLIENT_REPORT_COMMISSIONER_NARRATIVE_AND_DEAI_GATE.md'

s = INDEX.read_text(encoding='utf-8')

# Route Step 20 through explicit report-specific acceptance rules.
anchor = '`STEP_20_CLIENT_REPORT_COMMISSIONER_NARRATIVE_AND_DEAI_GATE.md`'
routing = '`STEP_20_REPORT_SPECIFIC_ACCEPTANCE_ROUTING.md`'
assert anchor in s
if routing not in s:
    s = s.replace(anchor, anchor + ' + ' + routing, 1)

summary_anchor = 'Package-wide PASS != recipient-specific PASS; analyst assurance != owner/commissioner acceptance.'
summary_extra = ' Report-specific routing is mandatory: Report №01 customer-research rules must not be imposed wholesale on Report №02 specialist implementation guidance, and Report №03 requires its own review before inheritance.'
if summary_extra.strip() not in s:
    assert summary_anchor in s
    s = s.replace(summary_anchor, summary_anchor + summary_extra, 1)

INDEX.write_text(s, encoding='utf-8')

# Correct the scope of the earlier commissioner/de-AI gate: it came from Report №01 rework.
g = LEGACY.read_text(encoding='utf-8')
g = g.replace(
    'Status: **ACTIVE / UNIVERSAL / PERMANENT NON-REPEAT CONTROL**  \nScope: **Step 19 materialization + Step 20 recipient acceptance / Level 1**',
    'Status: **ACTIVE AS LEGACY SHARED QUALITY BRIDGE / REPORT-SPECIFIC ROUTING REQUIRED**  \nScope: **Step 19 materialization + Step 20 recipient acceptance / Level 1**'
)

routing_note = '''\n## Report-specific applicability correction\n\nThis file originated from the owner-directed rework of **Report №01**. It must not be applied wholesale to every deliverable. Canonical applicability now routes through:\n\n`STEP_20_REPORT_SPECIFIC_ACCEPTANCE_ROUTING.md`\n\nReport-specific authorities:\n\n- `STEP_20_REPORT_01_CUSTOMER_RESEARCH_REPORT_GATE.md` — full customer-facing research-report rules and the complete Report №01 failure inventory;\n- `STEP_20_REPORT_02_SPECIALIST_IMPLEMENTATION_GUIDE_GATE.md` — only the transferable writing-quality controls plus the denser technical requirements needed by an SEO/implementation specialist;\n- Report №03 — no presentation rules are inherited automatically before its own review.\n\n```text\nREPORT_01_SIMPLICITY != REPORT_02_SIMPLICITY\nREPORT_01_FAILURE_INVENTORY != AUTOMATIC_REPORT_02_FAILURE_INVENTORY\nCONNECTED HUMAN NARRATIVE = SHARED\nNATURAL NON-GENERATED WORDING = SHARED\nMEANINGFUL SECTIONS = SHARED\nSPECIALIST TERMINOLOGY = ALLOWED / EXPECTED IN REPORT_02\n```\n\nThe sections below remain useful historical/shared guidance, but the report-specific gates above control final acceptance.\n'''
marker = 'Concrete client domains, URLs, counts, query strings, brands, action IDs and current-job findings are forbidden in this Level-1 rule. Those belong in Level 2.\n'
if '## Report-specific applicability correction' not in g:
    assert marker in g
    g = g.replace(marker, marker + routing_note, 1)

g = g.replace('## 13. Known failure inventory from owner-directed post-release rework', '## 13. Report №01 failure inventory from owner-directed post-release rework')

LEGACY.write_text(g, encoding='utf-8')
print('STEP20_REPORT_SPECIFIC_ROUTING_PATCH_PASS')
