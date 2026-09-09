from pathlib import Path
import json
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

import document01_step5a_competitor_amendment as base
import document01_step5a_linear_roadmap_rebuild as v1

ROOT = Path(__file__).resolve().parent
REL = ROOT / 'OKNO_MSK_RESEARCH_RELEASE_STEP05A_PROPAGATED_2026-09-09'
SRC = REL / 'sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.md'
DOCX = REL / 'editable/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.docx'


def replace_section(text, start_heading, end_heading, replacement):
    assert text.count(start_heading) == 1, (start_heading, text.count(start_heading))
    a = text.index(start_heading)
    b = text.index('\n' + end_heading, a)
    return text[:a] + replacement.rstrip() + '\n\n' + text[b + 1:]


def patch_source_v2():
    text = SRC.read_text(encoding='utf-8')

    competitor_block = v1.COMPETITOR_BLOCK
    competitor_block = competitor_block.replace(
        '9 сайтов → 44 страницы',
        '9 конкурентов → 44 страницы',
    )
    competitor_block = competitor_block.replace(
        'из них выделили 20 кандидатных формулировок, которым требовалась более точная смысловая проверка;',
        'из них выделили 20 кандидатов на точную смысловую проверку;',
    )
    competitor_block = competitor_block.replace(
        'итогом стали 16 принятых поисковых фраз в семи подтверждённых направлениях.',
        'итогом стали 16 новых поисковых фраз, принятых в семи подтверждённых направлениях.',
    )

    old_heading = '### Дополнительный анализ конкурентов и расширение ядра'
    assert old_heading in text
    a = text.index(old_heading)
    b = text.index('\n## Как проводилась работа', a)
    text = text[:a] + competitor_block.rstrip() + '\n\n' + text[b + 1:]

    text = replace_section(
        text,
        '## Как проводилась работа',
        '## Что показала обычная выдача Яндекса',
        v1.METHOD_BLOCK,
    )
    text = replace_section(
        text,
        '## Что показала обычная выдача Яндекса',
        '## Как сайт соответствует выдаче Алисы',
        v1.SEARCH_BLOCK,
    )

    old_summary = (
        'Обычная выдача Яндекса использовалась для тех формулировок, где от результата зависело правильное распределение спроса: '
        'например, нужно было отделить покупку от монтажа, объект остекления от материала, информационный интерес от коммерческой услуги. '
        'По первоначальному ядру сохранена выдача по 75 таким запросам. После анализа конкурентов ещё 6 новых спорных формулировок были отдельно проверены '
        'в обычной выдаче Яндекса. Всего в исследовании сохранена точная выдача по 81 запросу.'
    )
    new_summary = (
        'Обычная выдача Яндекса использовалась для тех формулировок, где от результата зависело правильное распределение спроса: например, нужно было отделить '
        'покупку от монтажа, объект остекления от материала, информационный интерес от коммерческой услуги. В основной цепочке семантических и страничных решений '
        'сохранена точная выдача по 81 запросу. Отдельно внутри этапа анализа конкурентов обычная выдача использовалась для обнаружения и подтверждения новых направлений; '
        'эти проверки относятся к сбору и расширению семантики и поэтому не смешиваются с 81 проверкой итоговых границ.'
    )
    assert old_summary in text
    text = text.replace(old_summary, new_summary)

    old_final = (
        'Для Москвы собрано и проверено поисковое ядро под современную выдачу Яндекса с Алисой: поисковые фразы очищены и сгруппированы, активный спрос сопоставлен '
        'с существующими страницами, спорные границы проверены в обычной выдаче Яндекса, а соответствие полученного распределения — в выдаче Алисы.'
    )
    new_final = (
        'Для Москвы собрано и проверено поисковое ядро под современную выдачу Яндекса с Алисой. В одной последовательности изучили сайт и границы бизнеса, собрали базовый спрос '
        'в Wordstat, проверили конкурентные пробелы по девяти реальным конкурентам из Яндекса, расширили общий корпус на 16 подтверждённых фраз, провели финальную очистку и группировку, '
        'сопоставили активный спрос с существующими страницами, проверили спорные границы в обычной выдаче Яндекса и затем проверили полученное распределение по выдаче Алисы.'
    )
    assert old_final in text
    text = text.replace(old_final, new_final)

    old_search_final = (
        'В обычной выдаче сохранена точная проверка 81 запроса: 75 неоднозначных случаев исходного ядра и ещё 6 формулировок, появившихся после анализа конкурентов. '
        'Восемь случаев по выдаче Алисы — это углублённо зафиксированные проверки разных типов решений внутри общей работы по ядру под Алису.'
    )
    new_search_final = (
        'В основной цепочке семантических и страничных решений сохранена точная проверка 81 запроса: 75 базовых неоднозначных границ и 6 формулировок конкурентного этапа, '
        'для которых после объединения корпуса требовалось подтвердить точного владельца или границу услуги. Восемь случаев по выдаче Алисы — это углублённо зафиксированные '
        'проверки разных типов решений внутри общей работы по ядру под Алису.'
    )
    assert old_search_final in text
    text = text.replace(old_search_final, new_search_final)

    forbidden = [
        'после основного исследования',
        'дополнительный анализ конкурентов',
        'после анализа конкурентов',
        'по первоначальному ядру',
        'проверок исходного ядра',
        'цепочка дополнительной работы',
        'дополнительная проверка не дала оснований',
    ]
    low = text.lower()
    for phrase in forbidden:
        assert phrase not in low, phrase

    SRC.write_text(text, encoding='utf-8')
    return text


def repeat_table_headers():
    doc = Document(DOCX)
    for table in doc.tables:
        if not table.rows:
            continue
        trPr = table.rows[0]._tr.get_or_add_trPr()
        if trPr.find(qn('w:tblHeader')) is None:
            hdr = OxmlElement('w:tblHeader')
            hdr.set(qn('w:val'), 'true')
            trPr.append(hdr)
    doc.save(DOCX)


def main():
    text = patch_source_v2()
    base.build_docx(text)
    repeat_table_headers()
    base.build_pdf()

    base_result = base.qa_all(text)
    base.refresh_manifest()
    v1.refresh_linear_manifest()
    base_result = base.qa_all(text)
    result = v1.linear_qa(text, base_result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
