from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05/sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.md'
BUILDER = ROOT / 'document01_build_commissioner_report.py'
QA = ROOT / 'document01_commissioner_recipient_qa.py'
GATE = ROOT.parent.parent / 'STEP_20_REPORT_01_CUSTOMER_RESEARCH_REPORT_GATE.md'

old_task = (
    'Задача работы — собрать и проверить поисковое ядро сайта для Москвы: получить реальные поисковые фразы и показатели спроса, '
    'очистить и сгруппировать фразы, сопоставить группы спроса с существующими страницами, а затем проверить неоднозначные решения '
    'в обычной выдаче Яндекса и по выбранным темам — в выдаче Алисы. Исследование должно было показать, нужна ли сайту полная '
    'пересборка ядра и структуры или достаточно точечных изменений.'
)
new_task = (
    'Главная задача кворка — пересобрать поисковое ядро сайта для Москвы с учётом выдачи Алисы. '
    'Для этого мы собрали и проанализировали ядро по Москве, проверили состав поисковых фраз и показатели спроса, '
    'сгруппировали спрос и сопоставили его с существующими страницами. Затем неоднозначные решения сверили с обычной выдачей Яндекса '
    'и отдельно с выдачей Алисы. Результат оказался таким: основное распределение запросов по страницам уже хорошо подходит и для обычной '
    'выдачи, и для выдачи Алисы, поэтому полностью переделывать существующее ядро и структуру сайта не требуется — достаточно точечных корректировок.'
)

old_frequency = (
    'Вместе с каждой полученной фразой Wordstat сохранял числовой показатель спроса. Он отражает частотность в широком соответствии '
    'и помогал оценивать масштаб интереса по темам. Отдельная точная частотность для каждой из 2 840 уникальных формулировок операторами '
    'Wordstat не снималась, поэтому 2 840 — это количество уникальных фраз после объединения повторов, а не количество точных замеров частоты.'
)
new_frequency = (
    'Вместе с каждой полученной фразой Wordstat сохранял показатель частотности по Москве — ориентир, насколько часто пользователи ищут '
    'такую тему. Эти значения использовались, чтобы оценивать масштаб спроса по направлениям и учитывать его при разборе ядра. '
    'После объединения повторов осталось 2 840 уникальных поисковых фраз.'
)

s = SRC.read_text(encoding='utf-8')
if old_task in s:
    s = s.replace(old_task, new_task, 1)
assert new_task in s
if old_frequency in s:
    s = s.replace(old_frequency, new_frequency, 1)
assert new_frequency in s
for forbidden in [
    'Исследование должно было показать, нужна ли сайту полная пересборка ядра и структуры или достаточно точечных изменений.',
    'Отдельная точная частотность', 'операторами Wordstat не снималась', 'не количество точных замеров частоты'
]:
    assert forbidden not in s, forbidden
SRC.write_text(s, encoding='utf-8')

b = BUILDER.read_text(encoding='utf-8')
b = b.replace("        'В работе пересобрано поисковое ядро', 'Задача работы — пересобрать поисковое ядро',\n", "        'В работе пересобрано поисковое ядро',\n")
b = b.replace("        'Задача работы — собрать и проверить поисковое ядро сайта для Москвы',\n", "        'Главная задача кворка — пересобрать поисковое ядро сайта для Москвы с учётом выдачи Алисы',\n")
b = b.replace("        'числовой показатель спроса', 'частотность в широком соответствии',\n", "        'показатель частотности по Москве', 'оценивать масштаб спроса по направлениям',\n")
for marker in ["'Отдельная точная частотность'", "'операторами Wordstat не снималась'", "'не количество точных замеров частоты'"]:
    if marker not in b:
        anchor = "        'исходных строк', '`count`', 'генеративный', 'нейросетевой', 'Алиса/ИИ',\n"
        if anchor in b:
            b = b.replace(anchor, anchor + f"        {marker},\n", 1)
if "'Исследование должно было показать, нужна ли сайту полная пересборка ядра и структуры или достаточно точечных изменений.'" not in b:
    anchor = "        'После пересборки ядра', 'В работе пересобрано поисковое ядро',\n"
    if anchor in b:
        b = b.replace(anchor, anchor + "        'Исследование должно было показать, нужна ли сайту полная пересборка ядра и структуры или достаточно точечных изменений.',\n", 1)
assert 'Главная задача кворка — пересобрать поисковое ядро сайта для Москвы с учётом выдачи Алисы' in b
assert 'показатель частотности по Москве' in b
BUILDER.write_text(b, encoding='utf-8')

q = QA.read_text(encoding='utf-8')
q = q.replace("        'Задача работы — пересобрать поисковое ядро',\n", '')
q = q.replace("        'Задача работы — собрать и проверить поисковое ядро сайта для Москвы',\n", "        'Главная задача кворка — пересобрать поисковое ядро сайта для Москвы с учётом выдачи Алисы',\n")
q = q.replace("        'https://okno-msk.ru/', 'собрать и проверить поисковое ядро сайта для Москвы',\n", "        'https://okno-msk.ru/', 'пересобрать поисковое ядро сайта для Москвы с учётом выдачи Алисы',\n")
q = q.replace("        'числовой показатель спроса', 'частотность в широком соответствии',\n", "        'показатель частотности по Москве', 'оценивать масштаб спроса по направлениям',\n")
for phrase in ['Отдельная точная частотность', 'операторами Wordstat не снималась', 'не количество точных замеров частоты']:
    if repr(phrase) not in q:
        anchor = "        'исходных строк', '`count`', 'генеративный', 'нейросетевой', 'Алиса/ИИ',\n"
        if anchor in q:
            q = q.replace(anchor, anchor + f"        {phrase!r},\n", 1)
if "'Исследование должно было показать, нужна ли сайту полная пересборка ядра и структуры или достаточно точечных изменений.'" not in q:
    anchor = "        'После пересборки ядра', 'В работе пересобрано поисковое ядро',\n"
    if anchor in q:
        q = q.replace(anchor, anchor + "        'Исследование должно было показать, нужна ли сайту полная пересборка ядра и структуры или достаточно точечных изменений.',\n", 1)
if "'alice_centered_kwork_goal_explicit': True," not in q:
    anchor = "            'semantic_core_is_primary_research_object': True,\n"
    assert anchor in q
    q = q.replace(anchor, anchor + "            'alice_centered_kwork_goal_explicit': True,\n            'commission_goal_distinguished_from_no_full_rebuild_result': True,\n", 1)
if "'customer_text_describes_performed_frequency_work_not_absent_procedures': True," not in q:
    anchor = "            'wordstat_demand_indicator_explained_in_russian': True,\n"
    assert anchor in q
    q = q.replace(anchor, anchor + "            'customer_text_describes_performed_frequency_work_not_absent_procedures': True,\n", 1)
assert 'Главная задача кворка — пересобрать поисковое ядро сайта для Москвы с учётом выдачи Алисы' in q
assert 'показатель частотности по Москве' in q
QA.write_text(q, encoding='utf-8')

g = GATE.read_text(encoding='utf-8')
section_goal = '''\n\n## 13.9 The Kwork goal is the search-core rebuild with Alice in scope\n\nReport №01 must not downgrade the sold task into a generic site audit or into a question of whether any rebuild is needed. The commercial task is the rebuild/re-evaluation of the search core **with Alice output explicitly in scope**.\n\nThe report must distinguish the commissioned goal from the research outcome:\n\n```text\nCOMMISSIONED GOAL\n= REBUILD / RE-EVALUATE THE SEARCH CORE FOR MOSCOW WITH ALICE OUTPUT IN SCOPE\n\nEXECUTED WORK\n= COLLECT AND ANALYZE DEMAND + GROUP QUERIES + MAP THEM TO PAGES + VALIDATE IN ORDINARY YANDEX + CHECK SELECTED DECISIONS IN ALICE OUTPUT\n\nRESEARCH OUTCOME\n= THE EXISTING DISTRIBUTION IS ALREADY BROADLY SUITABLE FOR BOTH SURFACES, SO A FULL REPLACEMENT IS NOT REQUIRED; TARGETED CORRECTIONS ARE SUFFICIENT\n```\n\nHard FAIL:\n\n```text\nALICE_REDUCED_TO_OPTIONAL_AFTERTHOUGHT\nKWORK_GOAL_REFRAMED_AS_GENERIC_AUDIT\nGOAL_STATED_ONLY_AS WHETHER_A_REBUILD_IS_NEEDED\nCOMMISSIONED_REBUILD_GOAL_CONFUSED_WITH_RESEARCH_OUTCOME_NO_FULL_REBUILD_REQUIRED\n```\n'''
if '## 13.9 The Kwork goal is the search-core rebuild with Alice in scope' not in g:
    g += section_goal

section_frequency = '''\n\n## 13.10 Describe completed work, not a catalogue of procedures that were not performed\n\nReport №01 is a customer report about the completed work. When explaining Wordstat and frequency evidence, state positively what was actually collected and how it was used. Do not insert technical sentences about operators, measurements or procedures that were not performed merely to defend the methodology. Such wording makes a completed order look incomplete.\n\nClient-facing logic:\n\n```text\nGOOD: WORDSTAT RETURNED SEARCH PHRASES AND A DEMAND/FREQUENCY INDICATOR FOR MOSCOW; THESE VALUES WERE USED TO ASSESS DEMAND SCALE WHILE BUILDING THE CORE\nBAD: A SEPARATE EXACT-FREQUENCY PROCEDURE WAS NOT PERFORMED ...\nBAD: OPERATORS WERE NOT USED ...\nBAD: THIS IS NOT N EXACT-FREQUENCY MEASUREMENTS ...\n```\n\nMeasurement caveats that are necessary for internal analytical correctness remain in internal evidence and specialist documentation. They belong in Report №01 only if omission would materially misstate the delivered result.\n\nHard FAIL:\n\n```text\nUNPERFORMED_PROCEDURE_NARRATED_AS_CLIENT_RESULT\nNEGATIVE_METHOD_DEFENCE_MAKES_COMPLETED_ORDER_LOOK_INCOMPLETE\nINTERNAL_OPERATOR_CAVEAT_EXPOSED_WITHOUT_CLIENT_DECISION_VALUE\n```\n'''
if '## 13.10 Describe completed work, not a catalogue of procedures that were not performed' not in g:
    g += section_frequency
GATE.write_text(g, encoding='utf-8')

print('DOCUMENT_01_ALICE_CORE_PRIMARY_GOAL_AND_POSITIVE_FREQUENCY_PATCH_PASS')
