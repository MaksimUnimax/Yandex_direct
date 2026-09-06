from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05/sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.md'
BUILDER = ROOT / 'document01_build_commissioner_report.py'
QA = ROOT / 'document01_commissioner_recipient_qa.py'

# Final owner-review wording correction applied after the canonical payload is materialized.
# It makes the Wordstat measurement semantics explicit and keeps the Alice surface positioned
# as the generative answer in Yandex Search based on Alice technologies.
text = SRC.read_text(encoding='utf-8')
replacements = {
    'Сбор Wordstat выполнялся в широком режиме для обнаружения формулировок, а не как отдельный замер точной частотности каждой фразы. В каждой сохранённой строке есть числовой показатель Wordstat, но 2 840 после очистки — это число уникальных поисковых формулировок после объединения повторов, а не 2 840 отдельных замеров точной частотности.':
    'Сбор Wordstat был широким поисковым сбором без операторов точной частотности для каждой фразы. В сохранённых строках есть показатель Wordstat `count`, но 2 840 после очистки — это число уникальных поисковых формулировок после объединения повторов, а не 2 840 отдельных замеров точной частотности.',
    'Под ответами Алисы здесь имеется в виду ответ в поиске Яндекса, сформированный с помощью технологий Алисы.':
    'Под ответами Алисы здесь имеется в виду генеративный ответ в поиске Яндекса, работающий на технологиях Алисы.',
    'Главный результат: сравнение с ответами Алисы не изменило общую картину распределения спроса по сайту.':
    'Главный результат: ответы Алисы не потребовали пересматривать общую картину распределения спроса по сайту.'
}
for before, after in replacements.items():
    assert before in text or after in text, before
    text = text.replace(before, after)
SRC.write_text(text, encoding='utf-8')

builder = BUILDER.read_text(encoding='utf-8')
builder = builder.replace(
    "'Под ответами Алисы здесь имеется в виду ответ в поиске Яндекса, сформированный с помощью технологий Алисы',",
    "'Под ответами Алисы здесь имеется в виду генеративный ответ в поиске Яндекса, работающий на технологиях Алисы',"
)
needle = "    for marker in required:\n        assert marker in text, marker\n\n    assert text.count('**Почему это важно:**') == 7"
replacement = "    for marker in required:\n        assert marker in text, marker\n    assert 'без операторов точной частотности' in text\n    assert 'показатель Wordstat `count`' in text\n\n    assert text.count('**Почему это важно:**') == 7"
assert needle in builder or replacement in builder
builder = builder.replace(needle, replacement)
BUILDER.write_text(builder, encoding='utf-8')

qa = QA.read_text(encoding='utf-8')
qa = qa.replace(
    "'Сбор Wordstat выполнялся в широком режиме для обнаружения формулировок',",
    "'без операторов точной частотности',\n        'показатель Wordstat `count`',"
)
qa = qa.replace(
    "'Под ответами Алисы здесь имеется в виду ответ в поиске Яндекса, сформированный с помощью технологий Алисы',",
    "'Под ответами Алисы здесь имеется в виду генеративный ответ в поиске Яндекса, работающий на технологиях Алисы',"
)
qa = qa.replace(
    "'Главный результат: сравнение с ответами Алисы не изменило общую картину распределения спроса по сайту',",
    "'Главный результат: ответы Алисы не потребовали пересматривать общую картину распределения спроса по сайту',"
)
QA.write_text(qa, encoding='utf-8')

final = SRC.read_text(encoding='utf-8')
for marker in [
    'без операторов точной частотности',
    'показатель Wordstat `count`',
    'генеративный ответ в поиске Яндекса, работающий на технологиях Алисы',
    'а не отдельным предметом исследования'
]:
    assert marker in final, marker

print('DOCUMENT_01_EXPLICIT_WORDSTAT_AND_ALICE_POSITIONING_PATCH_PASS')
