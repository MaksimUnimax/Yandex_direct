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

    # The result section itself must now have the same roadmap order as the method section.
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

    failed = [k for k,v in checks.items() if not v]
    out = {
        'schema': 'OKNO_MSK_DOCUMENT01_STEP05A_LINEAR_ORDER_QA_V1',
        'date': '2026-09-09',
        'status': 'PASS' if not failed else 'FAIL',
        'checks_total': len(checks),
        'checks_passed': len(checks)-len(failed),
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
    linear_result = linear.linear_qa(text, base_result)
    qa(text, base_result, linear_result)


if __name__ == '__main__':
    main()
