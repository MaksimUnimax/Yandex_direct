from pathlib import Path
import hashlib
import json

from pypdf import PdfReader

import document01_step5a_competitor_amendment as base
import document01_step5a_linear_roadmap_rebuild as linear
import document01_step5a_linear_roadmap_rebuild_v3 as v3

ROOT = Path(__file__).resolve().parent
REL = ROOT / 'OKNO_MSK_RESEARCH_RELEASE_STEP05A_PROPAGATED_2026-09-09'
SRC = REL / 'sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.md'
DOCX = REL / 'editable/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.docx'
PDF = REL / '01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.pdf'
MANIFEST = REL / 'RELEASE_MANIFEST_2026-09-09.json'

EVIDENCE_ROOT = ROOT / 'STEP_05A_FIRST_EXECUTION_2026-09-08'
SEARCH_SUMMARY = EVIDENCE_ROOT / 'STEP_05A_SEARCH_ACQUISITION_SUMMARY_2026-09-08.md'
MERGE_REPORT = EVIDENCE_ROOT / 'STEP_05A_SEARCH_DECISION_MERGE_REPORT.md'
CLIENT_PREVIEW = EVIDENCE_ROOT / 'STEP_05A_CLIENT_FACING_COMPETITOR_GAP_PREVIEW_RU.md'
FINAL_GAP_REGISTER = EVIDENCE_ROOT / 'STEP_05A_FINAL_GAP_DECISION_REGISTER.tsv'

QA = ROOT / 'DOCUMENT_01_STEP05A_EVIDENCE_CLAIM_GATE_QA_2026-09-09.json'
LOG = ROOT / 'DOCUMENT_01_STEP05A_EVIDENCE_CLAIM_GATE_REBUILD_2026-09-09.md'


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def patch_source():
    text = SRC.read_text(encoding='utf-8')

    replacements = {
        'Случайный обход сайтов и расширение списка конкурентов только по названию домена не использовались.': '',
        '''- 14 направлений передали в Wordstat для проверки реального спроса;\n- по этим направлениям получили 160 проверяемых формулировок;\n- из них выделили 20 кандидатов на точную смысловую проверку;\n- для спорных направлений были предусмотрены 9 проверок в обычной выдаче Яндекса: 7 дали сохранённую TOP10, по 2 устойчивого результата не получили и не усиливали решение догадками;\n- итогом стали 16 новых поисковых фраз, принятых в семи подтверждённых направлениях.''':
        '''- для 14 направлений выполнили отдельные проверки Wordstat;\n- Wordstat вернул 160 строк запросов и связанных формулировок;\n- после очистки осталось 20 потенциально новых формулировок, объединённых в девять направлений для проверки текущей выдачей Яндекса;\n- по всем девяти направлениям выполнили запросы к текущей выдаче: по семи сохранены TOP10, по двум результат запроса остался неопределённым;\n- по семи направлениям с достаточными данными в общий семантический процесс приняли 16 новых поисковых фраз.''',
        'Линейная цепочка этого этапа: **реальные конкуренты в Яндексе → 9 конкурентов → 44 страницы → 92 тематических упоминания → 43 сводных направления → 14 направлений в Wordstat → 160 формулировок → 20 кандидатов → проверка спорных направлений в обычном Яндексе → 16 принятых фраз в 7 направлениях → объединение с общим семантическим корпусом.**':
        'Линейная цепочка этого этапа: **реальные конкуренты в Яндексе → 9 конкурентов → 44 страницы → 92 тематических упоминания → 43 сводных направления → 14 проверок Wordstat → 160 возвращённых строк → 20 потенциально новых формулировок → 9 направлений с запросами к текущей выдаче → 7 направлений с сохранёнными TOP10 + 2 направления с неопределённым результатом запроса → 16 принятых фраз в 7 направлениях → объединение с общим семантическим корпусом.**',
        'Две отдельные темы — «окна для старого фонда» и «кладовая на балконе» — не были превращены в новые страницы или готовые задания: имеющихся данных оказалось недостаточно для такого решения.':
        'По двум темам — «окна для старого фонда» и «кладовая на балконе» — результат запроса к текущей выдаче остался неопределённым. Поэтому подтверждения, достаточного для включения этих тем в текущие семантические решения, нет.',
        'Новую страницу по ним не создаём и готовое задание на сайт не формируем без подтверждения этих границ.':
        'Для этих шести фраз точная страница для внедрения в текущей версии исследования не определена.',
        'Этап анализа конкурентов не дал оснований создавать отдельные новые страницы: **новых страниц — 0, новых готовых физических изменений сайта — 0**. Практический результат этого этапа — расширение семантического покрытия и более точное распределение новых формулировок между существующими материалами без искусственного раздувания структуры.':
        'Практический результат этапа: 16 подтверждённых фраз вошли в единый семантический корпус. После последующей очистки, группировки и распределения девять из них получили точное назначение на существующие страницы, семь остались активными без точного назначения.',
        'Конкурентный анализ использовался как один из штатных источников расширения семантики. Сам факт наличия темы у другого сайта не считался доказательством спроса, необходимости новой страницы или будущего трафика: решение требовало подтверждения спроса, соответствия бизнесу и поискового смысла.':
        'Конкурентный анализ использовался как один из штатных источников расширения семантики. Тема на странице конкурента служила исходным сигналом; для включения формулировки в ядро требовались подтверждение спроса, соответствие бизнесу и проверка поискового смысла.',
        'Следующим этапом дорожной карты был анализ конкурентных пробелов. По реальной выдаче Яндекса выбрали девять конкурентов и разобрали 44 страницы, на которых зафиксировали 92 тематических упоминания. Их свели в 43 направления и сравнили с уже собранным спросом и границами бизнеса. 14 направлений передали в Wordstat, получили 160 формулировок, выделили 20 кандидатов для более точной проверки и в итоге приняли 16 новых фраз в семи направлениях. Эти 16 фраз сразу объединили с остальным спросом и дальше обрабатывали как часть единого семантического корпуса.':
        'Следующим этапом дорожной карты был анализ конкурентных пробелов. По реальной выдаче Яндекса выбрали девять конкурентов и разобрали 44 страницы, на которых зафиксировали 92 тематических упоминания. Их свели в 43 направления и сравнили с уже собранным спросом и границами бизнеса. Для 14 направлений выполнили отдельные проверки Wordstat; Wordstat вернул 160 строк запросов и связанных формулировок. После очистки осталось 20 потенциально новых формулировок, объединённых в девять направлений. По всем девяти направлениям выполнили запросы к текущей выдаче Яндекса: по семи сохранили TOP10, по двум результат запроса остался неопределённым. По семи направлениям с достаточными данными приняли 16 новых фраз. Эти 16 фраз сразу объединили с остальным спросом и дальше обрабатывали как часть единого семантического корпуса.',
        'В результате все источники — сайт, Wordstat, реальные конкуренты из Яндекса, обычная выдача и выдача Алисы — прошли через одну последовательность принятия решений. Конкурентный этап расширил общий корпус на 16 подтверждённых фраз, но не создал отдельную параллельную версию ядра и не потребовал новых страниц.':
        'В результате все источники — сайт, Wordstat, реальные конкуренты из Яндекса, обычная выдача и выдача Алисы — прошли через одну последовательность принятия решений. Конкурентный этап расширил общий корпус на 16 подтверждённых фраз; после дальнейшей обработки девять получили точное назначение на существующие страницы, семь остались активными без точного назначения.',
        '**Сайт и границы бизнеса → базовый Wordstat → 2 840 уникальных фраз → анализ 9 конкурентов и 44 страниц → проверка конкурентных пробелов в Wordstat и обычном Яндексе → 16 принятых фраз → общий корпус 2 856 → финальная очистка → 2 348 активных фраз → 168 групп → назначение страниц → 81 точная Search-проверка для итоговых границ → проверка по выдаче Алисы → 8 углублённых разборов → готовые рекомендации и зафиксированные неопределённости.**':
        '**Сайт и границы бизнеса → базовый Wordstat → 2 840 уникальных фраз → анализ 9 конкурентов и 44 страниц → 14 проверок Wordstat → 160 возвращённых строк → 20 потенциально новых формулировок → 9 направлений с запросами к текущей выдаче (7 сохранённых TOP10, 2 неопределённых результата) → 16 принятых фраз → общий корпус 2 856 → финальная очистка → 2 348 активных фраз → 168 групп → назначение страниц → 81 точная проверка обычной выдачи для итоговых границ → проверка по выдаче Алисы → 8 углублённых разборов → готовые рекомендации и зафиксированные неопределённости.**',
    }

    for old, new in replacements.items():
        if old not in text:
            raise AssertionError('Expected source fragment not found: ' + old[:160])
        text = text.replace(old, new)

    # Exact-page decisions are the positive result. Do not attach a repeated
    # client-facing pseudo-action about a page that was not created.
    text = text.replace(' Отдельная новая страница не требуется.', '')

    SRC.write_text(text, encoding='utf-8')
    return text


def refresh_manifest():
    base.refresh_manifest()
    linear.refresh_linear_manifest()
    v3.refresh_manifest()
    data = json.loads(MANIFEST.read_text(encoding='utf-8'))
    data['report01_step5a_evidence_claim_gate'] = 'PASS'
    data['report01_step5a_search_requirements'] = 9
    data['report01_step5a_search_succeeded'] = 7
    data['report01_step5a_search_outcome_unknown'] = 2
    data['report01_step5a_search_serp_rows'] = 70
    data['report01_step5a_nonperformed_client_pseudo_results'] = 0
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def evidence_qa(text):
    search = SEARCH_SUMMARY.read_text(encoding='utf-8')
    merge = MERGE_REPORT.read_text(encoding='utf-8')
    preview = CLIENT_PREVIEW.read_text(encoding='utf-8')
    register = FINAL_GAP_REGISTER.read_text(encoding='utf-8')
    docx = base.docx_text()
    pdf = base.pdf_text()

    checks = {}

    # Durable evidence authority checks.
    checks['evidence_search_requirements_9'] = 'SEARCH_REQUIREMENTS_ACCOUNTED = 9 / 9' in search
    checks['evidence_search_success_7'] = 'SUCCESSFUL_SEARCH_REQUIREMENTS = 7' in search
    checks['evidence_search_unknown_2'] = 'OUTCOME_UNKNOWN_REQUIREMENTS = 2' in search
    checks['evidence_search_rows_70'] = 'SUCCESSFUL_SERP_ROWS = 70' in search
    checks['evidence_merge_accepted_16'] = 'SEMANTIC_PIPELINE_DELTA_ROWS = 16' in merge
    checks['evidence_merge_routes_7'] = 'FINAL_ADD_TO_PIPELINE = 7' in merge
    checks['evidence_merge_hold_2'] = 'FINAL_HOLD_EVIDENCE = 2' in merge
    checks['evidence_upstream_44'] = '44 inspected targets' in merge
    checks['evidence_upstream_92'] = '92 candidate occurrences' in merge
    checks['evidence_upstream_43'] = '43 directions' in merge
    checks['evidence_upstream_14'] = '14 Wordstat seeds' in merge
    checks['evidence_upstream_160'] = '160 returned Wordstat rows' in merge
    checks['evidence_preview_22_14_3_4'] = all(s in preview for s in [
        '22 уже были нормально представлены',
        '14 стоило дополнительно проверить через Wordstat',
        '3 не соответствовали подтверждённому предложению компании',
        '4 нельзя было продвигать дальше без уточнений',
    ])
    checks['evidence_old_housing_hold'] = '\tOLD_HOUSING_WINDOWS\tокна для старого фонда\tOUTCOME_UNKNOWN\t' in register and '\tHOLD_EVIDENCE\t' in register
    checks['evidence_storage_hold'] = '\tBALCONY_AS_STORAGE\tкладовая на балконе\tOUTCOME_UNKNOWN\t' in register

    # Client-facing completed-work claims must match that evidence.
    required_client_claims = [
        'девять сайтов',
        '44 страницах',
        '92 тематических упоминания',
        '43 направления',
        'для 14 направлений выполнили отдельные проверки Wordstat',
        'Wordstat вернул 160 строк запросов и связанных формулировок',
        '20 потенциально новых формулировок',
        'по всем девяти направлениям выполнили запросы к текущей выдаче',
        'по семи сохранены TOP10',
        'по двум результат запроса остался неопределённым',
        '16 новых поисковых фраз',
        'окна для старого фонда',
        'кладовая на балконе',
        '2 856 уникальных фраз',
        '2 348',
        '2 322',
        '26 оставлены',
        '168 групп',
    ]
    for claim in required_client_claims:
        checks['source_claim_' + claim] = claim in text

    # No client pseudo-result describing a procedure/action that was not performed.
    forbidden = [
        'были предусмотрены 9 проверок',
        'по 2 устойчивого результата не получили',
        'не были превращены в новые страницы',
        'новых страниц — 0',
        'новых готовых физических изменений сайта — 0',
        'Новую страницу по ним не создаём',
        'готовое задание на сайт не формируем',
        'Отдельная новая страница не требуется',
        'Случайный обход сайтов',
        'не потребовал новых страниц',
        'не создал отдельную параллельную версию ядра',
    ]
    for phrase in forbidden:
        checks['source_forbidden_' + phrase] = phrase not in text
        checks['docx_forbidden_' + phrase] = phrase not in docx
        checks['pdf_forbidden_' + phrase] = phrase not in pdf

    # All accepted phrases must remain present in all delivery formats.
    for phrase in base.PHRASES:
        checks['source_phrase_' + phrase] = phrase in text
        checks['docx_phrase_' + phrase] = phrase in docx
        checks['pdf_phrase_' + phrase] = phrase in pdf

    # Step 5A remains a normal roadmap stage, not a late amendment.
    result = text[text.index('## Результат исследования'):text.index('\n## Как проводилась работа')]
    checks['result_linear_order'] = (
        result.index('### Анализ конкурентов и расширение семантики')
        < result.index('Обычная выдача Яндекса использовалась для тех формулировок')
        < result.index('Проверка ядра по выдаче Алисы была одной из основных частей работы.')
    )
    method = text[text.index('## Как проводилась работа'):text.index('\n## Что показала обычная выдача Яндекса')]
    checks['method_linear_order'] = (
        method.index('Затем собрали базовый спрос в Wordstat')
        < method.index('Следующим этапом дорожной карты был анализ конкурентных пробелов.')
        < method.index('После объединения базового и конкурентного сбора итоговый сохранённый корпус составил 2 856 уникальных фраз.')
    )
    checks['search_roles_not_conflated'] = 'не смешиваются с 81 проверкой итоговых границ' in text

    pages = len(PdfReader(str(PDF)).pages)
    checks['pdf_has_pages'] = pages > 0

    failed = [name for name, ok in checks.items() if not ok]
    result_obj = {
        'schema': 'OKNO_MSK_DOCUMENT01_STEP05A_EVIDENCE_CLAIM_GATE_QA_V1',
        'date': '2026-09-09',
        'status': 'PASS' if not failed else 'FAIL',
        'checks_total': len(checks),
        'checks_passed': len(checks) - len(failed),
        'checks_failed': failed,
        'provider_calls': 0,
        'step5a_search_requirements': 9,
        'step5a_search_succeeded': 7,
        'step5a_search_outcome_unknown': 2,
        'step5a_search_serp_rows': 70,
        'accepted_step5a_phrases': 16,
        'pdf_pages': pages,
        'evidence_authorities': [
            str(SEARCH_SUMMARY.relative_to(ROOT)),
            str(MERGE_REPORT.relative_to(ROOT)),
            str(CLIENT_PREVIEW.relative_to(ROOT)),
            str(FINAL_GAP_REGISTER.relative_to(ROOT)),
        ],
        'source_sha256': sha256(SRC),
        'docx_sha256': sha256(DOCX),
        'pdf_sha256': sha256(PDF),
        'manifest_sha256': sha256(MANIFEST),
    }
    QA.write_text(json.dumps(result_obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if failed:
        raise AssertionError(failed)
    return result_obj


def write_log(result):
    LOG.write_text(
        '# Document 01 — Step5A evidence-claim gate correction\n\n'
        'Status: **PASS**\n\n'
        'The client Step5A narrative was reconciled against persisted execution evidence.\n\n'
        '- 9 current-Yandex Search requirements were actually executed/accounted.\n'
        '- 7 returned preserved TOP10 evidence; 2 remained outcome-unknown.\n'
        '- 20 means potentially new Wordstat formulations, not 20 Search executions.\n'
        '- The 16 accepted phrases remain fully present.\n'
        '- Client pseudo-results about pages/actions that were not performed were removed.\n'
        '- Step5A remains in its canonical linear roadmap position.\n'
        '- Provider calls during this correction: 0.\n\n'
        f'QA: {result["checks_passed"]}/{result["checks_total"]} PASS\n\n'
        f'Source SHA-256: `{result["source_sha256"]}`\n'
        f'DOCX SHA-256: `{result["docx_sha256"]}`\n'
        f'PDF SHA-256: `{result["pdf_sha256"]}`\n',
        encoding='utf-8'
    )


def main():
    text = patch_source()
    base.build_docx(text)
    v3.repeat_table_headers()
    base.build_pdf()
    refresh_manifest()
    result = evidence_qa(text)
    write_log(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
