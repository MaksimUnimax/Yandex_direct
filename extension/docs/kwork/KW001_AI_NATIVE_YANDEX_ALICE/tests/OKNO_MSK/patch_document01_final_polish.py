from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05/sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.md'
BUILDER = ROOT / 'document01_build_commissioner_report.py'
QA = ROOT / 'document01_commissioner_recipient_qa.py'
GATE = (ROOT / '../../STEP_20_REPORT_01_CUSTOMER_RESEARCH_REPORT_GATE.md').resolve()
text = SRC.read_text(encoding='utf-8')

# The authoritative Alice-first contract is materialized before this hook.
# This final pass removes defensive references to superseded report versions and
# internal product/platform terminology so the customer sees only the completed work.
replacements = {
    'Выдача Алисы была дополнительно проверена по восьми выбранным темам и помогли точнее сформулировать часть рекомендаций.':
        'Выдачу Алисы проверили по восьми выбранным темам; это помогло точнее сформулировать часть рекомендаций.',
    'Проверка по этой выдаче — одна из основных частей кворка по пересборке ядра под современный поиск, а не действие после «основной» SEO-работы.':
        'Проверка по этой выдаче — одна из основных частей работы по пересборке ядра под современный поиск. Она использовалась, чтобы оценить, соответствует ли распределение спроса по страницам тому, как эти темы раскрываются в выдаче Алисы.',
    'Восемь карточек ниже — не весь объём работы с Алисой, а углублённо зафиксированные случаи, на которых проверялись разные типы решений и уточнялось содержание конкретных страниц.':
        'Восемь карточек ниже показывают углублённо зафиксированные случаи разных типов. На них уточнялись конкретные решения по страницам после общего вывода о соответствии сайта выдаче Алисы.',
    'Эти 75 проверок — не весь объём исследования, а точечная проверка решений внутри уже собранного ядра.':
        'Эти 75 проверок служили точечной проверкой решений внутри уже собранного ядра.',
    'Это не отдельный маленький набор вместо всего ядра: к этому моменту уже были собраны, очищены и сгруппированы тысячи поисковых фраз. Обычная выдача использовалась именно там, где требовалось подтвердить границу между группами или роль страницы.':
        'К этому моменту уже были собраны, очищены и сгруппированы тысячи поисковых фраз. Обычная выдача использовалась там, где требовалось подтвердить границу между группами или роль страницы.',
    'Восемь случаев по выдаче Алисы — это углублённо зафиксированные проверки разных типов решений внутри общей работы по ядру под Алису, а не вся ценность работы с Алисой.':
        'Восемь случаев по выдаче Алисы — это углублённо зафиксированные проверки разных типов решений внутри общей работы по ядру под Алису.',
    'Главная задача кворка — пересобрать и проверить поисковое ядро сайта «Окно Москва» для Москвы под Алису — под современную выдачу Яндекса, где вместе с обычными результатами часть поискового ответа формирует Алиса. Для этого мы собрали реальные поисковые фразы и показатели спроса, очистили и сгруппировали ядро, распределили спрос между существующими страницами и проверили, насколько это распределение соответствует обычной выдаче Яндекса и выдаче Алисы.':
        'Цель работы — пересобрать поисковое ядро сайта «Окно Москва» с учётом выдачи Алисы. Поиск в Яндексе изменился: по части запросов вместе с обычными результатами пользователь получает ответ Алисы. Поэтому мы собрали поисковые фразы и показатели спроса по Москве, очистили и сгруппировали ядро, распределили спрос между существующими страницами и проверили, насколько это распределение соответствует обычной выдаче Яндекса и выдаче Алисы.',
    'Проверка ядра по выдаче Алисы была одной из основных частей кворка.':
        'Проверка ядра по выдаче Алисы была одной из основных частей работы.',
    'Это отвечало на главный вопрос кворка:':
        'Это отвечало на главный вопрос исследования:',
    'Главный результат кворка:':
        'Главный результат исследования:'
}
for before, after in replacements.items():
    text = text.replace(before, after)

for forbidden in [
    'Выдача Алисы была дополнительно проверена',
    'не действие после «основной» SEO-работы',
    'не весь объём работы с Алисой',
    'не вся ценность работы с Алисой',
    'Это не отдельный маленький набор вместо всего ядра'
]:
    assert forbidden not in text, forbidden

low = text.lower()
assert 'кворк' not in low
assert 'kwork' not in low

positive_marker = 'Восемь карточек ниже показывают углублённо зафиксированные случаи разных типов.'
opening_marker = 'Цель работы — пересобрать поисковое ядро сайта «Окно Москва» с учётом выдачи Алисы.'
assert opening_marker in text
assert positive_marker in text
assert 'Главный результат проверки: существующее распределение основных групп спроса по страницам в целом соответствует выдаче Алисы' in text
SRC.write_text(text, encoding='utf-8')

# Keep deterministic build/QA markers aligned with the client wording and make
# any future internal Kwork leakage a hard failure.
for path in [BUILDER, QA]:
    code = path.read_text(encoding='utf-8')
    code = code.replace('Восемь карточек ниже — не весь объём работы с Алисой', positive_marker)
    code = code.replace("'Главная задача кворка — пересобрать и проверить поисковое ядро',", "'Цель работы — пересобрать поисковое ядро сайта «Окно Москва» с учётом выдачи Алисы.',")
    code = code.replace("'Главная задача кворка',", "'Цель работы — пересобрать поисковое ядро',")
    code = code.replace("'под Алису — под современную выдачу Яндекса',", "'Поиск в Яндексе изменился:',")
    if "'кворк', 'kwork'" not in code:
        code = code.replace("'исходных строк',", "'исходных строк', 'кворк', 'kwork',", 1)
    path.write_text(code, encoding='utf-8')
    assert positive_marker in code
    assert 'Главная задача кворка' not in code
    assert 'под Алису — под современную выдачу Яндекса' not in code
    assert "'кворк', 'kwork'" in code

# Permanent non-repeat rule: internal marketplace/product terminology is allowed
# in project methodology, but must never leak into the customer-facing Report 01.
gate = GATE.read_text(encoding='utf-8')
rule = '''

### 13.11 Internal product/platform wording must not leak into Report №01

`Kwork` / `кворк` are internal marketplace/product-context terms. They may be used in project methodology, but they must never appear in the customer-facing research report. Report №01 must speak only about the customer's site, the work, the research, the findings and the recommendations.

```text
INTERNAL_PRODUCT_OR_PLATFORM_TERM_EXPOSED_TO_CUSTOMER = FAIL
KWORK_WORD_ABSENT_FROM_REPORT_01 = true
CLIENT_REPORT_USES_WORK_RESEARCH_SITE_LANGUAGE_ONLY = true
```
'''
if '### 13.11 Internal product/platform wording must not leak into Report №01' not in gate:
    gate = gate.rstrip() + rule + '\n'
GATE.write_text(gate, encoding='utf-8')

print('DOCUMENT_01_FINAL_POLISH_PASS__NO_INTERNAL_KWORK_LEAK')
