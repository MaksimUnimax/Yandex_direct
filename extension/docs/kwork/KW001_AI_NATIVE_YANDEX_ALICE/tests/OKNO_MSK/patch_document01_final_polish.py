from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05/sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.md'
text = SRC.read_text(encoding='utf-8')
text = text.replace(
    'Выдача Алисы была дополнительно проверена по восьми выбранным темам и помогли точнее сформулировать часть рекомендаций.',
    'Выдачу Алисы дополнительно проверили по восьми выбранным темам; это помогло точнее сформулировать часть рекомендаций.'
)
assert 'Выдача Алисы была дополнительно проверена по восьми выбранным темам и помогли' not in text
SRC.write_text(text, encoding='utf-8')
print('DOCUMENT_01_FINAL_POLISH_PASS')

# Permanent final overlay: keep the commissioned goal centered on rebuilding/re-evaluating
# the search core with Alice output in scope, and describe only frequency work that was
# actually performed in the non-specialist Report 01.
runpy.run_path(str(ROOT / 'patch_document01_alice_core_primary_goal.py'), run_name='__main__')
