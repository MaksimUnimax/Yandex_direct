from pathlib import Path
import hashlib, json
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pypdf import PdfReader

import document01_step5a_competitor_amendment as base
import document01_step5a_linear_roadmap_rebuild as linear

ROOT = Path(__file__).resolve().parent
REL = ROOT / 'OKNO_MSK_RESEARCH_RELEASE_STEP05A_PROPAGATED_2026-09-09'
SRC = REL / 'sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.md'
DOCX = REL / 'editable/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.docx'
PDF = REL / '01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.pdf'
MANIFEST = REL / 'RELEASE_MANIFEST_2026-09-09.json'
QA = ROOT / 'DOCUMENT_01_STEP05A_LINEAR_ORDER_QA_2026-09-09.json'
LOG = ROOT / 'DOCUMENT_01_STEP05A_LINEAR_ORDER_REBUILD_2026-09-09.md'
LINEAR_QA = ROOT / 'DOCUMENT_01_STEP05A_LINEAR_ROADMAP_QA_2026-09-09.json'
LINEAR_LOG = ROOT / 'DOCUMENT_01_STEP05A_LINEAR_ROADMAP_REBUILD_2026-09-09.md'


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def move_competitor_block_into_linear_result_order():
    text = SRC.read_text(encoding='utf-8')
    comp_heading = '### Анализ конкурентов и расширение семантики'
    method_heading = '## Как проводилась работа'
    search_summary = 'Обычная выдача Яндекса использовалась для тех формулировок, где от результата зависело правильное распределение спроса:'
    alice_summary = 'Проверка ядра по выдаче Алисы была одной из основных частей работы.'

    assert text.count(comp_heading) == 1
    assert text.count(method_heading) == 1
    assert text.count(search_summary) == 1
    assert text.count(alice_summary) == 1

    cs = text.index(comp_heading)
    ce = text.index('\n' + method_heading, cs)
    block = text[cs:ce].strip()
    text = text[:cs].rstrip() + '\n\n' + text[ce + 1:]

    insert_at = text.index(search_summary)
    text = text[:insert_at].rstrip() + '\n\n' + block + '\n\n' + text[insert_at:]

    text = text.replace('Конкурентная ветка исследования не дала оснований создавать отдельные новые страницы:',
                        'Этап анализа конкурентов не дал оснований создавать отдельные новые страницы:')
    text = text.replace('Отдельно внутри этапа анализа конкурентов обычная выдача использовалась для обнаружения и подтверждения новых направлений;',
                        'Внутри этапа анализа конкурентов обычная выдача использовалась для обнаружения и подтверждения новых направлений;')
    text = text.replace('Обычная выдача использовалась в двух строго разделённых ролях.',
                        'Обычная выдача использовалась в двух разных ролях.')

    result_end = text.index('\n' + method_heading)
    result = text[text.index('## Результат исследования'):result_end]
    assert result.index(comp_heading) < result.index(search_summary) < result.index(alice_summary)

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


def refresh_manifest():
    data = json.loads(MANIFEST.read_text(encoding='utf-8'))
    data['report01_competitor_analysis_narrative'] = 'LINEAR_ROADMAP_STAGE'
    data['report01_competitor_result_section_order'] = 'BEFORE_FINAL_SEARCH_AND_ALICE_SUMMARY'
    data['report01_competitor_stage_position'] = 'AFTER_BASE_WORDSTAT_BEFORE_FINAL_CLEANUP_FREEZE'
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def adapted_linear_qa(text, base_result):
    """Same 28 semantic checks as the original linear QA, updated only for v3 wording."""
    doc_text = base.docx_text()
    pdf_text = base.pdf_text()
    checks = {
        'linear_heading_source': '### Анализ конкурентов и расширение семантики' in text,
        'linear_heading_docx': 'Анализ конкурентов и расширение семантики' in doc_text,
        'linear_heading_pdf': 'Анализ конкурентов и расширение семантики' in pdf_text,
        'roadmap_position_explicit': 'после базового сбора спроса в Wordstat и до окончательной очистки, группировки и назначения страниц' in text,
        'merged_before_final_cleanup': 'до финальной очистки, группировки и назначения страниц' in text,
        'unified_corpus_2856': 'общий корпус 2 856' in text,
        'active_2348': '2 348 активных фраз' in text,
        'exact_2322': '2 322' in text,
        'hold_26': '26 оставили' in text or '26 оставлены' in text,
        'competitors_9': 'девять конкурентов' in text or '9 конкурентов' in text,
        'pages_44': '44 страницы' in text,
        'mentions_92': '92 тематических упоминания' in text,
        'directions_43': '43 направления' in text,
        'wordstat_14': '14 направлений' in text,
        'wordstat_160': '160' in text,
        'candidate_20': '20 кандидат' in text,
        'accepted_16': '16 принятых' in text or '16 подтверждённых' in text or '16 новых поисковых фраз' in text,
        'no_new_pages': 'новых страниц — 0' in text,
        'search_roles_separated': 'Обычная выдача использовалась в двух разных ролях.' in text,
        'alice_after_unified_semantics': 'Затем полученное распределение спроса по страницам проверили по выдаче Алисы.' in text,
        'base_qa_pass': base_result['status'] == 'PASS',
    }
    for bad in [
        'После основного исследования', 'Дополнительный анализ конкурентов', 'после анализа конкурентов',
        'По первоначальному ядру', 'проверок исходного ядра', 'цепочка дополнительной работы',
        'Дополнительная проверка не дала оснований'
    ]:
        checks['forbidden_' + bad] = bad not in text and bad not in doc_text and bad not in pdf_text

    assert len(checks) == 28, len(checks)
    failed = [k for k, v in checks.items() if not v]
    result = {
        'schema': 'OKNO_MSK_DOCUMENT01_STEP05A_LINEAR_ROADMAP_QA_V2',
        'date': '2026-09-09',
        'status': 'PASS' if not failed else 'FAIL',
        'checks_total': len(checks),
        'checks_passed': len(checks) - len(failed),
        'checks_failed': failed,
        'base_competitor_amendment_checks_total': base_result['checks_total'],
        'base_competitor_amendment_checks_passed': base_result['checks_passed'],
        'pdf_pages': len(PdfReader(str(PDF)).pages),
        'source_sha256': sha256(SRC),
        'docx_sha256': sha256(DOCX),
        'pdf_sha256': sha256(PDF),
        'manifest_sha256': sha256(MANIFEST),
    }
    LINEAR_QA.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if failed:
        raise AssertionError(failed)
    LINEAR_LOG.write_text(
        '# Document 01 — linear roadmap integration of competitor analysis\n\n'
        'Status: **PASS**\n\n'
        'Competitor analysis is a canonical Step5A acquisition/coverage stage inside one research line: base Wordstat → competitor gap analysis → merged semantic corpus → final cleanup/grouping → Search page decisions → Alice → recommendations.\n\n'
        f'PDF pages: {result["pdf_pages"]}\n\n'
        f'Source SHA-256: `{result["source_sha256"]}`\n'
        f'DOCX SHA-256: `{result["docx_sha256"]}`\n'
        f'PDF SHA-256: `{result["pdf_sha256"]}`\n',
        encoding='utf-8'
    )
    return result


def qa(text, base_result, linear_result):
    doc_text = base.docx_text()
    pdf_text = base.pdf_text()
    checks = {}
    for name, blob in [('source', text), ('docx', doc_text), ('pdf', pdf_text)]:
        checks[f'{name}_heading'] = 'Анализ конкурентов и расширение семантики' in blob
        checks[f'{name}_no_late_after_main'] = 'После основного исследования' not in blob
        checks[f'{name}_no_late_after_competitor'] = 'после анализа конкурентов' not in blob.lower()
        checks[f'{name}_no_additional_competitor_heading'] = 'Дополнительный анализ конкурентов' not in blob

    result_start = text.index('## Результат исследования')
    result_end = text.index('\n## Как проводилась работа')
    result = text[result_start:result_end]
    checks['result_order_competitor_before_search'] = result.index('### Анализ конкурентов и расширение семантики') < result.index('Обычная выдача Яндекса использовалась для тех формулировок')
    checks['result_order_search_before_alice'] = result.index('Обычная выдача Яндекса использовалась для тех формулировок') < result.index('Проверка ядра по выдаче Алисы была одной из основных частей работы.')
    checks['method_chain_is_linear'] = '**Сайт и границы бизнеса → базовый Wordstat → 2 840 уникальных фраз → анализ 9 конкурентов и 44 страниц →' in text
    checks['accepted_before_cleanup'] = 'до финальной очистки, группировки и назначения страниц' in text
    checks['corpus_2856'] = '2 856' in text
    checks['all_16_present'] = all(p in text for p in base.PHRASES)
    checks['base_104_pass'] = base_result['status'] == 'PASS' and base_result['checks_passed'] == 104
    checks['linear_28_pass'] = linear_result['status'] == 'PASS' and linear_result['checks_passed'] == 28

    failed = [k for k, v in checks.items() if not v]
    out = {
        'schema': 'OKNO_MSK_DOCUMENT01_STEP05A_LINEAR_ORDER_QA_V1',
        'date': '2026-09-09',
        'status': 'PASS' if not failed else 'FAIL',
        'checks_total': len(checks),
        'checks_passed': len(checks) - len(failed),
        'checks_failed': failed,
        'base_checks': '104/104',
        'linear_roadmap_checks': '28/28',
        'pdf_pages': len(PdfReader(str(PDF)).pages),
        'source_sha256': sha256(SRC),
        'docx_sha256': sha256(DOCX),
        'pdf_sha256': sha256(PDF),
        'manifest_sha256': sha256(MANIFEST),
    }
    QA.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if failed:
        raise AssertionError(failed)
    LOG.write_text(
        '# Document 01 — Step5A linear order across the whole report\n\n'
        'Status: **PASS**\n\n'
        'The competitor analysis is placed before final Search/Alice conclusions in the result section and in its canonical roadmap position in the method section.\n\n'
        f'Source SHA-256: `{out["source_sha256"]}`\n'
        f'DOCX SHA-256: `{out["docx_sha256"]}`\n'
        f'PDF SHA-256: `{out["pdf_sha256"]}`\n',
        encoding='utf-8'
    )
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return out


def main():
    text = move_competitor_block_into_linear_result_order()
    base.build_docx(text)
    repeat_table_headers()
    base.build_pdf()
    base_result = base.qa_all(text)
    base.refresh_manifest()
    linear.refresh_linear_manifest()
    refresh_manifest()
    base_result = base.qa_all(text)
    linear_result = adapted_linear_qa(text, base_result)
    qa(text, base_result, linear_result)


if __name__ == '__main__':
    main()
