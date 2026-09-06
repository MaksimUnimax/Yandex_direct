from pathlib import Path

ROOT = Path(__file__).resolve().parent
P = ROOT / 'STEP_RULES_INDEX.md'
s = P.read_text(encoding='utf-8')

old = "`STEP_20_FINAL_QA_AND_RELEASE_ASSURANCE_METHOD.md` + `STEP_20_RECIPIENT_ACCEPTANCE_DEPTH_GATE.md` + `STEP_20_CLIENT_REPORT_OWNER_VALUE_AND_PLAIN_LANGUAGE_GATE.md` + `STEP_20_CLIENT_REPORT_RESULT_SURFACE_SCOPE_AND_ACTIONABILITY_GATE.md`"
new = old + " + `STEP_20_CLIENT_REPORT_COMMISSIONER_NARRATIVE_AND_DEAI_GATE.md`"
if 'STEP_20_CLIENT_REPORT_COMMISSIONER_NARRATIVE_AND_DEAI_GATE.md' not in s:
    assert old in s
    s = s.replace(old, new, 1)

needle = "FULL_RESEARCH_COMPLETENESS != EXHAUSTIVE NO-ACTION DUMP IN MAIN REPORT"
extra = """
COMMISSIONER != ASSUMED BUSINESS OWNER / SITE OWNER
SEMANTIC SECTIONS REQUIRED != ONE UNBROKEN TEXT WALL
SEMANTIC SECTIONS REQUIRED != DISCONNECTED MICRO-BLOCK FRAGMENTATION
COMPLETE CLIENT REPORT != QA CHECKLIST USED AS DOCUMENT OUTLINE
EXACT COUNTS SUPPORT NARRATIVE != COUNTS ARE THE NARRATIVE
INTERNAL STAGE LANGUAGE != COMMISSIONER-FACING WORK DESCRIPTION
GENERATED TEMPLATE SYMMETRY != CLEAR CLIENT STRUCTURE
GENERIC DISCLAIMER SECTION != ANSWER TO THE KWORK"""
if 'COMMISSIONER != ASSUMED BUSINESS OWNER / SITE OWNER' not in s:
    assert needle in s
    s = s.replace(needle, needle + extra, 1)

summary_needle = "and keep the main report concentrated on decisions, changes and reasons rather than exhaustive no-change routing."
summary_extra = " It must address the commissioner rather than inventing an owner role, keep meaningful semantic sections while avoiding disconnected micro-block fragmentation, explain the completed work as one causal narrative, answer the sold Kwork directly, and reject generated-template presentation patterns such as fake reading-time headings, cloned recommendation forms and generic defensive disclaimer sections."
if 'fake reading-time headings' not in s:
    assert summary_needle in s
    s = s.replace(summary_needle, summary_needle + summary_extra, 1)

P.write_text(s, encoding='utf-8')
print('STEP20_COMMISSIONER_INDEX_PATCH_PASS')
