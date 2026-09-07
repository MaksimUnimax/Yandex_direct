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

s = SRC.read_text(encoding='utf-8')
if old_task in s:
    s = s.replace(old_task, new_task, 1)
assert new_task in s
assert 'Исследование должно было показать, нужна ли сайту полная пересборка ядра и структуры или достаточно точечных изменений.' not in s
SRC.write_text(s, encoding='utf-8')

b = BUILDER.read_text(encoding='utf-8')
b = b.replace("        'В работе пересобрано поисковое ядро', 'Задача работы — пересобрать поисковое ядро',\n", "        'В работе пересобрано поисковое ядро',\n")
b = b.replace("        'Задача работы — собрать и проверить поисковое ядро сайта для Москвы',\n", "        'Главная задача кворка — пересобрать поисковое ядро сайта для Москвы с учётом выдачи Алисы',\n")
if "'Исследование должно было показать, нужна ли сайту полная пересборка ядра и структуры или достаточно точечных изменений.'" not in b:
    anchor = "        'После пересборки ядра', 'В работе пересобрано поисковое ядро',\n"
    if anchor in b:
        b = b.replace(anchor, anchor + "        'Исследование должно было показать, нужна ли сайту полная пересборка ядра и структуры или достаточно точечных изменений.',\n", 1)
assert 'Главная задача кворка — пересобрать поисковое ядро сайта для Москвы с учётом выдачи Алисы' in b
BUILDER.write_text(b, encoding='utf-8')

q = QA.read_text(encoding='utf-8')
q = q.replace("        'Задача работы — пересобрать поисковое ядро',\n", '')
q = q.replace("        'Задача работы — собрать и проверить поисковое ядро сайта для Москвы',\n", "        'Главная задача кворка — пересобрать поисковое ядро сайта для Москвы с учётом выдачи Алисы',\n")
q = q.replace("        'https://okno-msk.ru/', 'собрать и проверить поисковое ядро сайта для Москвы',\n", "        'https://okno-msk.ru/', 'пересобрать поисковое ядро сайта для Москвы с учётом выдачи Алисы',\n")
if "'Исследование должно было показать, нужна ли сайту полная пересборка ядра и структуры или достаточно точечных изменений.'" not in q:
    anchor = "        'После пересборки ядра', 'В работе пересобрано поисковое ядро',\n"
    if anchor in q:
        q = q.replace(anchor, anchor + "        'Исследование должно было показать, нужна ли сайту полная пересборка ядра и структуры или достаточно точечных изменений.',\n", 1)
if "'alice_centered_kwork_goal_explicit': True," not in q:
    anchor = "            'semantic_core_is_primary_research_object': True,\n"
    assert anchor in q
    q = q.replace(anchor, anchor + "            'alice_centered_kwork_goal_explicit': True,\n            'commission_goal_distinguished_from_no_full_rebuild_result': True,\n", 1)
assert 'Главная задача кворка — пересобрать поисковое ядро сайта для Москвы с учётом выдачи Алисы' in q
QA.write_text(q, encoding='utf-8')

g = GATE.read_text(encoding='utf-8')
section = '''\n\n## 13.9 The Kwork goal is the search-core rebuild with Alice in scope\n\nReport №01 must not downgrade the sold task into a generic site audit or into a question of whether any rebuild is needed. The commercial task is the rebuild/re-evaluation of the search core **with Alice output explicitly in scope**.\n\nThe report must distinguish the commissioned goal from the research outcome:\n\n```text\nCOMMISSIONED GOAL\n= REBUILD / RE-EVALUATE THE SEARCH CORE FOR MOSCOW WITH ALICE OUTPUT IN SCOPE\n\nEXECUTED WORK\n= COLLECT AND ANALYZE DEMAND + GROUP QUERIES + MAP THEM TO PAGES + VALIDATE IN ORDINARY YANDEX + CHECK SELECTED DECISIONS IN ALICE OUTPUT\n\nRESEARCH OUTCOME\n= THE EXISTING DISTRIBUTION IS ALREADY BROADLY SUITABLE FOR BOTH SURFACES, SO A FULL REPLACEMENT IS NOT REQUIRED; TARGETED CORRECTIONS ARE SUFFICIENT\n```\n\nHard FAIL:\n\n```text\nALICE_REDUCED_TO_OPTIONAL_AFTERTHOUGHT\nKWORK_GOAL_REFRAMED_AS_GENERIC_AUDIT\nGOAL_STATED_ONLY_AS WHETHER_A_REBUILD_IS_NEEDED\nCOMMISSIONED_REBUILD_GOAL_CONFUSED_WITH_RESEARCH_OUTCOME_NO_FULL_REBUILD_REQUIRED\n```\n'''
if '## 13.9 The Kwork goal is the search-core rebuild with Alice in scope' not in g:
    g += section
GATE.write_text(g, encoding='utf-8')

print('DOCUMENT_01_ALICE_CORE_PRIMARY_GOAL_PATCH_PASS')
