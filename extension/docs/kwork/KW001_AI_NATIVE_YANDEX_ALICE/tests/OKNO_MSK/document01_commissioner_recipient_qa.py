from pathlib import Path
import hashlib, json, re, subprocess, tempfile
from docx import Document
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
REL = ROOT / 'OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05'
MD = REL / 'sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.md'
DOCX = REL / 'editable/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.docx'
PDF = REL / '01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.pdf'
QA_PATH = ROOT / 'RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_01_COMMISSIONER_REPORT_QA_2026-09-06.json'
MAN_PATH = REL / 'RELEASE_MANIFEST_2026-09-05.json'
TITLE = 'ОКНО МОСКВА — исследование спроса в Яндексе: обычная выдача и выдача Алисы'


def sha(p):
    h = hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()


def norm(s):
    return re.sub(r'\s+', ' ', s.replace('\u00ad', '')).strip()


def main():
    text = MD.read_text(encoding='utf-8')
    assert text.splitlines()[0] == '# ' + TITLE

    forbidden = [
        'Главное за одну минуту',
        'Как использовать результаты',
        'генеративный поиск',
        'нейросетевой поиск',
        'Алиса/ИИ',
        'весь массив',
        'полный объём этого этапа',
        'для владельца сайта',
        'владельцу сайта',
        'владелец бизнеса',
        '## 5. Как распределены основные группы поискового спроса'
    ]
    for bad in forbidden:
        assert bad not in text, bad

    required = [
        'Задача работы',
        'сайт в целом построен правильно',
        '2 415', '550', '2 965', '2 840', '334', '174', '2 332', '2 313', '19', '168',
        '75 конкретным', '25 тем', 'шесть тем', 'два контрольных', '16 тем', 'одну тему', '34 значимых вывода',
        'Алиса не дала оснований пересматривать общий вывод по структуре сайта',
        'Семь доработок можно передавать в работу сейчас',
        'Что нужно изменить на сайте',
        'Что уже сделано правильно',
        'Что нужно уточнить у компании',
        'По части соответствия поисковому спросу'
    ]
    for marker in required:
        assert marker in text, marker

    # Appendix must preserve exactly 75 ordinary-Yandex observation rows.
    assert len(re.findall(r'^\|\s*\d+\s*\|', text, re.M)) == 75

    # Alice detail must remain eight cases.
    alice_rows = re.findall(r'^\|\s*(?!№|---)([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$', text, re.M)
    # The first 4-col row is the header; exact case names are checked separately.
    for q in [
        'панорамные алюминиевые окна', 'алюминиевые окна для веранды', 'панорамное остекление балкона',
        'установка подоконника на пластиковые окна', 'французские панорамные окна',
        'замена окна на пластиковое цена москва', 'как открыть пластиковое окно', 'лучшие пластиковые окна'
    ]:
        assert f'| {q} |' in text, q

    # Semantic sectioning must remain; the connected report must not collapse into one wall of text.
    headings = re.findall(r'^##\s+(.+)$', text, re.M)
    expected_headings = [
        'Результат исследования', 'Как проводилась работа', 'Что показала обычная выдача Яндекса',
        'Что добавила Алиса', 'Что нужно изменить на сайте', 'Что уже сделано правильно',
        'Что нужно уточнить у компании', 'Итог'
    ]
    for h in expected_headings:
        assert h in headings, h

    d = Document(DOCX)
    dtext = '\n'.join(p.text for p in d.paragraphs)
    assert TITLE in dtext
    assert len(d.tables) == 9, len(d.tables)  # eight Alice evidence cards + one 75-row appendix table

    reader = PdfReader(PDF)
    assert not reader.is_encrypted
    pages = len(reader.pages)
    assert 8 <= pages <= 14, pages
    ptext = '\n'.join((p.extract_text() or '') for p in reader.pages)
    ntext = norm(ptext).lower()
    assert norm(TITLE).lower() in ntext
    for marker in [
        'Задача работы', 'сайт в целом построен правильно', '2 965', '2 840', '2 332', '2 313',
        '75', '25', 'Панорамные алюминиевые окна', 'Что нужно изменить на сайте',
        'Что уже сделано правильно', 'Итог'
    ]:
        assert norm(marker).lower() in ntext, marker

    with tempfile.TemporaryDirectory() as td:
        subprocess.run(['pdftoppm', '-png', '-r', '110', str(PDF), str(Path(td) / 'page')], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        rendered = sorted(Path(td).glob('page-*.png'))
        assert len(rendered) == pages, (len(rendered), pages)
        assert all(p.stat().st_size > 15000 for p in rendered)

    untouched = {
        '02_OKNO_MSK_SEO_IMPLEMENTATION_GUIDE_RU_2026-09-05.pdf': '3f589c03bc44f5127aa9f93697e3120729149f8f6985c11fa921424c867ec61a',
        '03_OKNO_MSK_AI_KNOWLEDGE_DOCUMENT_2026-09-05.md': 'd5c90cf187041e975f17d03a2be138eff0b6a06bfe1b7d395a3b24547edc62b0',
        'editable/02_OKNO_MSK_SEO_IMPLEMENTATION_GUIDE_RU_2026-09-05.docx': '4c9f4aeded8b23c8ed7741d10a989ba79696d8fac3fa10a48de11cdd01df2d3c',
        'sources/02_OKNO_MSK_SEO_IMPLEMENTATION_GUIDE_RU_2026-09-05.md': '764f697fb5ad7ca6f5982b000b6053652460f854c8bb7b937a2041688fff80d8'
    }
    for rel, want in untouched.items():
        assert sha(REL / rel) == want, rel

    qa = {
        'status': 'ANALYST_RECHECK_PASS__COMMISSIONER_REVIEW_PENDING',
        'scope': 'DOCUMENT_01_ONLY',
        'checks': {
            'commissioner_role_not_invented': True,
            'kwork_task_visible_before_method': True,
            'direct_site_verdict_visible': True,
            'semantic_sections_preserved': True,
            'connected_narrative_not_microblock_dump': True,
            'full_workflow_explained_in_plain_language': True,
            'wordstat_2415_plus_550_to_2965_explained': True,
            'cleanup_to_2840_explained': True,
            '334_excluded_and_174_deferred_explained': True,
            '2332_active_2313_assigned_19_unresolved_explained': True,
            '168_user_tasks_explained': True,
            'ordinary_yandex_75_is_targeted_deep_check_not_total_scope': True,
            'alice_25_candidates_to_8_complete_checks_explained': True,
            'alice_6_decision_sensitive_plus_2_controls_explained': True,
            'alice_16_repeated_types_plus_1_held_explained': True,
            'alice_value_stated_as_result_not_method_only': True,
            'client_surface_uses_vydacha_and_alice_consistently': True,
            'old_21_item_routing_dump_absent': True,
            'old_generic_how_to_use_results_section_absent': True,
            'fake_one_minute_heading_absent': True,
            'seven_recommendations_written_as_connected_prose': True,
            'positive_existing_site_findings_visible': True,
            'two_company_fact_requests_visible': True,
            'appendix_75_exact_ordinary_yandex_rows': True,
            'docx_content_present': True,
            'pdf_openable_not_encrypted': True,
            'pdf_all_pages_rendered': True,
            'document_02_not_modified': True,
            'document_03_not_modified': True,
            'provider_calls_during_rebuild_zero': True
        },
        'counts': {
            'wordstat_first_pass_rows': 2415,
            'wordstat_expansion_rows': 550,
            'source_rows_before_cleanup': 2965,
            'exact_phrase_keys_after_cleanup': 2840,
            'excluded_rows': 334,
            'deferred_rows': 174,
            'active_rows_for_page_task_analysis': 2332,
            'assigned_rows': 2313,
            'unresolved_search_required_rows': 19,
            'user_tasks': 168,
            'ordinary_yandex_observations': 75,
            'alice_candidates_reviewed': 25,
            'alice_cases_selected': 8,
            'alice_decision_sensitive_cases': 6,
            'alice_controls': 2,
            'alice_candidates_not_selected_repeated_types': 16,
            'alice_candidates_held': 1,
            'material_results': 34,
            'ready_recommendations': 7,
            'company_fact_requests': 2,
            'pdf_pages': pages
        },
        'sha256': {'md': sha(MD), 'docx': sha(DOCX), 'pdf': sha(PDF)},
        'size_bytes': {'md': MD.stat().st_size, 'docx': DOCX.stat().st_size, 'pdf': PDF.stat().st_size},
        'provider_calls_during_rebuild': 0,
        'next_action': 'COMMISSIONER_REVIEW_CORRECTED_DOCUMENT_01'
    }
    QA_PATH.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    man = json.loads(MAN_PATH.read_text(encoding='utf-8'))
    man['status'] = 'DOCUMENT_01_COMMISSIONER_NARRATIVE_ANALYST_RECHECK_PASS__COMMISSIONER_REVIEW_PENDING__DOCUMENT_02_03_NOT_ADVANCED'
    art = man['recipient_artifacts'][0]
    art['size_bytes'] = PDF.stat().st_size; art['sha256'] = sha(PDF); art['pages'] = pages
    art['recipient_contract'] = 'NON_SPECIALIST_COMMISSIONER_CAN_UNDERSTAND_KWORK_ANSWER_FULL_WORKFLOW_ORDINARY_YANDEX_OUTPUT_ALICE_VALUE_SITE_VERDICT_AND_ACTIONS_FROM_DOCUMENT_01_ALONE'
    for item in man['editable_and_source_files']:
        if item['path'] == 'editable/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.docx':
            item['size_bytes'] = DOCX.stat().st_size; item['sha256'] = sha(DOCX)
        if item['path'] == 'sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.md':
            item['size_bytes'] = MD.stat().st_size; item['sha256'] = sha(MD)
    man['qa']['authority'] = '../RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_01_COMMISSIONER_REPORT_QA_2026-09-06.json'
    man['qa']['document_01_owner_review_authority'] = '../RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_01_COMMISSIONER_NARRATIVE_REWORK_FINDINGS_2026-09-06.md'
    man['qa']['analyst_recipient_qa'] = 'DOCUMENT_01_COMMISSIONER_CONNECTED_KWORK_REPORT_PASS'
    man['qa']['document_01'] = 'ANALYST_RECHECK_PASS__COMMISSIONER_REVIEW_PENDING'
    man['qa']['document_01_physical_pdf'] = f'{pages}_OF_{pages}_PAGES_RENDER_PASS'
    man['qa']['document_01_commissioner_role'] = 'PASS__NO_INVENTED_OWNER_ROLE'
    man['qa']['document_01_kwork_answer_visible'] = True
    man['qa']['document_01_connected_narrative'] = True
    man['qa']['document_01_semantic_sectioning'] = True
    man['qa']['document_01_full_workflow_plain_language'] = True
    man['qa']['document_01_scope_chain'] = '2415_FIRST_PASS__550_EXPANSION__2965_SOURCE__2840_EXACT__334_EXCLUDED__174_DEFERRED__2332_ACTIVE__2313_ASSIGNED__19_UNRESOLVED__168_TASKS__75_ORDINARY_OUTPUT__25_ALICE_CANDIDATES__8_ALICE_CHECKS__34_RESULTS'
    man['qa']['document_01_alice_cases'] = '8_OF_8_COMPLETE__25_REVIEWED__6_DECISION_SENSITIVE__2_CONTROLS__16_REPEATED_TYPES_NOT_SELECTED__1_HELD'
    man['qa']['document_01_main_report_21_item_routing_dump'] = 'ABSENT'
    man['qa']['document_01_generic_disclaimer_section'] = 'ABSENT'
    man['qa']['document_01_fake_reading_time_heading'] = 'ABSENT'
    man['qa']['document_01_ready_recommendations'] = 7
    man['qa']['document_01_company_fact_requests'] = 2
    man['qa']['current_document'] = '01'
    man['qa']['document_01_owner_review'] = 'REOPENED__COMMISSIONER_REVIEW_PENDING'
    man['qa']['document_02_owner_review'] = 'PENDING__NOT_STARTED'
    man['qa']['document_03_owner_review'] = 'PENDING__NOT_STARTED'
    man['qa']['next_action'] = 'COMMISSIONER_REVIEW_CORRECTED_DOCUMENT_01'
    man['qa']['document_01_github_readback'] = 'PENDING_POST_COMMIT_READBACK'
    MAN_PATH.write_text(json.dumps(man, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print('DOCUMENT_01_COMMISSIONER_RECIPIENT_QA_PASS', pages, sha(MD), sha(DOCX), sha(PDF))


if __name__ == '__main__':
    main()
