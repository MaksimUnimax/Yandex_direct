from pathlib import Path
import json

import document01_step5a_competitor_amendment as base
import document01_step5a_linear_roadmap_rebuild as linear
import document01_step5a_linear_roadmap_rebuild_v3 as v3

ROOT = Path(__file__).resolve().parent
REL = ROOT / 'OKNO_MSK_RESEARCH_RELEASE_STEP05A_PROPAGATED_2026-09-09'
SRC = REL / 'sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.md'

REPLACEMENTS = {
    'В последовательность исследования входит отдельный этап проверки конкурентных пробелов.':
        'В последовательность исследования входит этап проверки конкурентных пробелов.',
    'Эти 16 фраз сразу объединили с остальным спросом; они не существовали как отдельное «дополнение» к уже завершённому ядру.':
        'Эти 16 фраз сразу объединили с остальным спросом и дальше обрабатывали как часть единого семантического корпуса.',
    'Поэтому решения по ним принимались не как поздняя поправка к готовому отчёту, а внутри той же цепочки распределения спроса по страницам.':
        'Поэтому решения по ним принимались внутри той же цепочки распределения спроса по страницам, что и по остальному активному ядру.',
    'Её практический результат — расширение семантического покрытия и более точное распределение новых формулировок между существующими материалами без искусственного раздувания структуры.':
        'Практический результат этого этапа — расширение семантического покрытия и более точное распределение новых формулировок между существующими материалами без искусственного раздувания структуры.',
}


def patch_source():
    text = SRC.read_text(encoding='utf-8')
    for old, new in REPLACEMENTS.items():
        assert old in text, old
        text = text.replace(old, new)

    forbidden = [
        'После основного исследования',
        'Дополнительный анализ конкурентов',
        'после анализа конкурентов',
        'По первоначальному ядру',
        'проверок исходного ядра',
        'цепочка дополнительной работы',
        'отдельное «дополнение» к уже завершённому ядру',
        'поздняя поправка к готовому отчёту',
    ]
    low = text.lower()
    for phrase in forbidden:
        assert phrase.lower() not in low, phrase

    result = text[text.index('## Результат исследования'):text.index('\n## Как проводилась работа')]
    assert result.index('### Анализ конкурентов и расширение семантики') < result.index('Обычная выдача Яндекса использовалась для тех формулировок') < result.index('Проверка ядра по выдаче Алисы была одной из основных частей работы.')

    method = text[text.index('## Как проводилась работа'):text.index('\n## Что показала обычная выдача Яндекса')]
    assert method.index('Затем собрали базовый спрос в Wordstat') < method.index('Следующим этапом дорожной карты был анализ конкурентных пробелов.') < method.index('После объединения базового и конкурентного сбора итоговый сохранённый корпус составил 2 856 уникальных фраз.')

    SRC.write_text(text, encoding='utf-8')
    return text


def main():
    text = patch_source()
    base.build_docx(text)
    v3.repeat_table_headers()
    base.build_pdf()

    base_result = base.qa_all(text)
    base.refresh_manifest()
    linear.refresh_linear_manifest()
    v3.refresh_manifest()
    base_result = base.qa_all(text)
    linear_result = v3.adapted_linear_qa(text, base_result)
    order_result = v3.qa(text, base_result, linear_result)

    print(json.dumps({
        'status': 'PASS',
        'base_qa': f'{base_result["checks_passed"]}/{base_result["checks_total"]}',
        'linear_qa': f'{linear_result["checks_passed"]}/{linear_result["checks_total"]}',
        'order_qa': f'{order_result["checks_passed"]}/{order_result["checks_total"]}',
        'source_sha256': order_result['source_sha256'],
        'docx_sha256': order_result['docx_sha256'],
        'pdf_sha256': order_result['pdf_sha256'],
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
