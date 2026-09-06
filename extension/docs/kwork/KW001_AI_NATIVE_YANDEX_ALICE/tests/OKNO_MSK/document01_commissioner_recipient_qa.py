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
TITLE = 'ОКНО МОСКВА — поисковое ядро сайта: спрос, обычный Яндекс и ответы Алисы'


def sha(p):
    h = hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()


def norm(s):
    return re.sub(r'\s+', ' ', s.replace('\u00ad', '')).strip()


def main():
    text = MD.read_text(encoding='utf-8')
    low = text.lower()
    assert text.splitlines()[0] == '# ' + TITLE

    # Hard fail inventory from owner review + semantic-core framing repair.
    forbidden = [
        'главное за одну минуту', 'как использовать результаты',
        'для владельца сайта', 'владельцу сайта', 'владелец бизнеса',
        '2 840 точных поисковых формулировок', 'точных поисковых формулировок',
        'пользовательских задач', 'пользовательская задача',
        'спорные семьи', 'спорные семейства', 'изменения запрещены', 'частично готов',
        'связанные страницы', 'семантический маппинг', 'family owner', 'structural unit',
        'causal delta', 'proxy', 'ready', 'recheck', 'search_required', 'pending_business_detail',
        'цель — не расширять сайт', 'цель не расширять сайт любой ценой',
        'не создавать новые страницы'
    ]
    for bad in forbidden:
        assert bad not in low, bad

    required = [
        'Задача работы — пересобрать поисковое ядро сайта для Москвы',
        '18 широких стартовых формулировок',
        'Первый проход Wordstat дал 2 415 исходных строк',
        'Это расширение добавило ещё 550 строк',
        'Всего перед очисткой было 2 965 исходных строк',
        'без операторов точной частотности',
        'показатель Wordstat `count`',
        '2 840 после очистки — это число уникальных поисковых формулировок',
        'а не 2 840 отдельных замеров точной частотности',
        '2 332 активные поисковые формулировки', '2 313', '19', '168 групп поискового спроса',
        'Это было критерием для правильного объединения запросов и распределения их по страницам, а не отдельным предметом исследования',
        '75 проверок — не весь объём исследования',
        'Восемь выбрали для полного сравнения',
        'шесть — потому что ответ мог уточнить решение по странице',
        'две — как контроль уже ясного вывода обычной выдачи',
        'Ещё 16 тем повторяли', 'одну тему оставили без дальнейшей проверки',
        '34 значимых вывода',
        'Под ответами Алисы здесь имеется в виду генеративный ответ в поиске Яндекса, работающий на технологиях Алисы',
        'Главный результат: ответы Алисы не потребовали пересматривать общую картину распределения спроса по сайту',
        'Семь доработок можно передавать в работу сейчас',
        'Что нужно уточнить у компании для двух следующих улучшений',
        'Сайт → Wordstat → очистка и объединение повторов → 168 групп поискового спроса'
    ]
    for marker in required:
        assert marker in text, marker

    # Every ready recommendation must carry explicit client reasoning.
    assert text.count('**Почему это важно:**') == 7
    assert text.count('**Что рекомендуется сделать:**') == 7
    assert text.count('**Что обнаружено:**') == 7
    assert text.count('**Что сохранить:**') == 7
    assert text.count('**Как должен выглядеть результат:**') == 7
    assert text.count('**Как проверить:**') == 7

    # Evidence completeness.
    assert len(re.findall(r'^\|\s*\d+\s*\|', text, re.M)) == 75
    alice_queries = [
        'панорамные алюминиевые окна', 'алюминиевые окна для веранды', 'панорамное остекление балкона',
        'установка подоконника на пластиковые окна', 'французские панорамные окна',
        'замена окна на пластиковое цена москва', 'как открыть пластиковое окно', 'лучшие пластиковые окна'
    ]
    for q in alice_queries:
        assert f'| {q} |' in text, q
    for native in ['REHAU', 'Provedal', 'KBE', 'Accado', 'Vorne', 'Futurus', 'fapim', 'rehau thermo']:
        assert native in text, native

    headings = re.findall(r'^##\s+(.+)$', text, re.M)
    for h in [
        'Результат исследования', 'Как проводилась работа', 'Что показала обычная выдача Яндекса',
        'Что дала проверка ответов Алисы', 'Что нужно изменить на сайте',
        'Что на сайте уже работает правильно', 'Что нужно уточнить у компании для двух следующих улучшений', 'Итог'
    ]:
        assert h in headings, h

    d = Document(DOCX)
    dtext = '\n'.join(p.text for p in d.paragraphs)
    assert TITLE in dtext
    assert len(d.tables) == 9, len(d.tables)  # eight Alice cards + one 75-row appendix

    reader = PdfReader(PDF)
    assert not reader.is_encrypted
    pages = len(reader.pages)
    assert 8 <= pages <= 14, pages
    ptext = '\n'.join((p.extract_text() or '') for p in reader.pages)
    ntext = norm(ptext).lower()
    for marker in [
        TITLE, 'Задача работы', '2 965', '2 840', '2 332', '2 313', '168 групп поискового спроса',
        '75 проверок', 'Под ответами Алисы', 'Что нужно изменить на сайте',
        'Что на сайте уже работает правильно', 'Итог'
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
        'status': 'ANALYST_RECHECK_PASS__OWNER_REVIEW_PENDING',
        'scope': 'DOCUMENT_01_ONLY',
        'checks': {
            'semantic_core_is_primary_research_object': True,
            'user_intent_is_grouping_criterion_not_research_object': True,
            'wordstat_broad_discovery_mode_explained': True,
            'unique_2840_not_exact_frequency_measurements': True,
            '168_units_presented_as_demand_groups': True,
            'full_semantic_workflow_visible': True,
            'wordstat_2415_plus_550_to_2965_explained': True,
            '334_excluded_and_174_deferred_explained': True,
            '2332_active_2313_assigned_19_unresolved_explained': True,
            'ordinary_yandex_75_is_targeted_validation_not_total_scope': True,
            'alice_25_candidates_to_8_complete_checks_explained': True,
            'alice_6_decision_sensitive_plus_2_controls_explained': True,
            'alice_16_repeated_types_plus_1_held_explained': True,
            'alice_not_presented_as_research_author': True,
            'seven_recommendations_have_explicit_finding_why_action_place_preserve_result_check': True,
            'positive_existing_site_findings_visible': True,
            'two_company_fact_requests_visible_without_partial_ready_framing': True,
            'negative_pseudo_actions_absent_from_main_plan': True,
            'false_opposite_goal_absent': True,
            'internal_status_and_project_taxonomy_absent_from_client_text': True,
            'source_native_brands_and_verbatim_queries_preserved': True,
            'appendix_75_ordinary_yandex_rows': True,
            'eight_alice_comparison_cases': True,
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
            'unique_search_formulations_after_deduplication': 2840,
            'excluded_rows': 334,
            'deferred_rows': 174,
            'active_formulations_for_page_distribution_analysis': 2332,
            'assigned_formulations': 2313,
            'unresolved_formulations': 19,
            'demand_groups': 168,
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
        'wordstat_count_semantics': '2840_UNIQUE_SEARCH_FORMULATIONS_AFTER_DEDUPLICATION__NOT_2840_EXACT_FREQUENCY_MEASUREMENTS',
        'research_object_semantics': 'SEMANTIC_SEARCH_CORE_AND_QUERY_TO_PAGE_DISTRIBUTION__USER_INTENT_IS_GROUPING_CRITERION_ONLY',
        'sha256': {'md': sha(MD), 'docx': sha(DOCX), 'pdf': sha(PDF)},
        'size_bytes': {'md': MD.stat().st_size, 'docx': DOCX.stat().st_size, 'pdf': PDF.stat().st_size},
        'provider_calls_during_rebuild': 0,
        'next_action': 'OWNER_REVIEW_CORRECTED_DOCUMENT_01'
    }
    QA_PATH.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    man = json.loads(MAN_PATH.read_text(encoding='utf-8'))
    man['status'] = 'DOCUMENT_01_SEMANTIC_CORE_FRAMING_ANALYST_RECHECK_PASS__OWNER_REVIEW_PENDING__DOCUMENT_02_03_NOT_ADVANCED'
    art = man['recipient_artifacts'][0]
    art['size_bytes'] = PDF.stat().st_size
    art['sha256'] = sha(PDF)
    art['pages'] = pages
    art['recipient_contract'] = 'NON_SPECIALIST_CUSTOMER_CAN_UNDERSTAND_SEMANTIC_CORE_REBUILD_WORDSTAT_SCOPE_QUERY_TO_PAGE_DISTRIBUTION_ORDINARY_YANDEX_VALIDATION_ALICE_VALUE_AND_ACTIONS_FROM_DOCUMENT_01_ALONE'
    for item in man['editable_and_source_files']:
        if item['path'] == 'editable/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.docx':
            item['size_bytes'] = DOCX.stat().st_size; item['sha256'] = sha(DOCX)
        if item['path'] == 'sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.md':
            item['size_bytes'] = MD.stat().st_size; item['sha256'] = sha(MD)

    mqa = man.setdefault('qa', {})
    # Remove stale labels that encoded the defect we are repairing.
    for stale in [
        'document_01_exact_count_relationship_explained', 'document_01_scope_counts',
        'document_01_scope_chain', 'document_01_user_tasks', 'document_01_168_user_tasks_explained'
    ]:
        mqa.pop(stale, None)
    mqa.update({
        'authority': '../RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_01_COMMISSIONER_REPORT_QA_2026-09-06.json',
        'analyst_recipient_qa': 'DOCUMENT_01_SEMANTIC_CORE_CLIENT_REPORT_PASS',
        'document_01': 'ANALYST_RECHECK_PASS__OWNER_REVIEW_PENDING',
        'document_01_physical_pdf': f'{pages}_OF_{pages}_PAGES_RENDER_PASS',
        'document_01_semantic_core_primary_object': True,
        'document_01_user_intent_role': 'GROUPING_CRITERION_ONLY__NOT_RESEARCH_OBJECT',
        'document_01_wordstat_count_semantics': '2840_UNIQUE_FORMULATIONS__NOT_2840_EXACT_FREQUENCY_MEASUREMENTS',
        'document_01_scope_chain': '2415_FIRST_PASS__550_EXPANSION__2965_SOURCE_ROWS__2840_UNIQUE_FORMULATIONS__334_EXCLUDED__174_DEFERRED__2332_ACTIVE__2313_ASSIGNED__19_UNRESOLVED__168_DEMAND_GROUPS__75_ORDINARY_YANDEX_OBSERVATIONS__25_ALICE_CANDIDATES__8_ALICE_CHECKS__34_RESULTS',
        'document_01_ordinary_yandex_subset_relation': '75_TARGETED_VALIDATION_OBSERVATIONS_INSIDE_ALREADY_ANALYZED_SEMANTIC_CORE',
        'document_01_alice_cases': '8_OF_8_COMPLETE__25_REVIEWED__6_DECISION_SENSITIVE__2_CONTROLS__16_REPEATED_TYPES_NOT_SELECTED__1_HELD',
        'document_01_ready_recommendations': 7,
        'document_01_ready_recommendations_with_explicit_why': 7,
        'document_01_company_fact_requests': 2,
        'document_01_negative_pseudo_actions_in_main_plan': 0,
        'document_01_internal_taxonomy_hits': 0,
        'document_01_source_native_brands_preserved': True,
        'current_document': '01',
        'document_01_owner_review': 'PENDING__AWAITING_RECHECK',
        'document_02_owner_review': 'PENDING__NOT_STARTED',
        'document_03_owner_review': 'PENDING__NOT_STARTED',
        'final_owner_recipient_acceptance': 'OPEN',
        'next_action': 'OWNER_REVIEW_CORRECTED_DOCUMENT_01',
        'document_01_github_readback': 'PENDING_POST_COMMIT_READBACK'
    })
    man['provider_calls'] = 0
    man['paid_cost_rub'] = 0
    MAN_PATH.write_text(json.dumps(man, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print('DOCUMENT_01_SEMANTIC_CORE_RECIPIENT_QA_PASS', pages, sha(MD), sha(DOCX), sha(PDF))


if __name__ == '__main__':
    main()
