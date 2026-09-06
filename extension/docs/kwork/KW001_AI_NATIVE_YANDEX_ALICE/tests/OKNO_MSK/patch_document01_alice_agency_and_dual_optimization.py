from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05/sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.md'
text = SRC.read_text(encoding='utf-8')

# Historical patch hook retained for workflow compatibility. The current source is authoritative
# and must not be rewritten back to the superseded "user-task research" narrative.
required = [
    '# ОКНО МОСКВА — поисковое ядро сайта: спрос, обычный Яндекс и ответы Алисы',
    'Задача работы — пересобрать поисковое ядро сайта для Москвы',
    '168 групп поискового спроса',
    'а не отдельным предметом исследования',
    'а не 2 840 отдельных замеров точной частотности',
    'Что дала проверка ответов Алисы'
]
for marker in required:
    assert marker in text, marker

for forbidden in ['2 840 точных поисковых формулировок', 'пользовательских задач и подзадач', 'спорные семьи', 'изменения запрещены', 'частично готовая работа']:
    assert forbidden.lower() not in text.lower(), forbidden

print('DOCUMENT_01_CURRENT_SEMANTIC_CORE_SOURCE_GUARD_PASS')
