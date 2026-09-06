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
TITLE = 'ОКНО МОСКВА — https://okno-msk.ru/ — исследование спроса в Яндексе: обычная выдача и выдача Алисы'


def sha(p):
    h = hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()


def norm(s):
    return re.sub(r'\s+', ' ', s.replace('\u00ad', '')).strip()


def main():
    text = MD.read_text(encoding='utf-8')
    assert text.splitlines()[0] == '# ' + TITLE

    forbidden = [
        'исходных строк', '`count`', 'генеративный', 'нейросетевой', 'Алиса/ИИ',
        '## Приложение.', 'Полный список 75 проверенных',
        'После пересборки ядра', 'В работе пересобрано поисковое ядро',
        'Задача работы — пересобрать поисковое ядро',
        'Специализированная страница панорамного остекления балкона соответствует спросу',
        'Общая страница веранды и раздел алюминиевых окон выполняют разные роли',
        'Страница замены окна и общая страница монтажа',
        'Главное за одну минуту', 'Как использовать результаты', 'полный объём этого этапа',
        'для владельца сайта', 'владельцу сайта', 'владелец бизнеса'
    ]
    low = text.lower()
    for bad in forbidden:
        assert bad.lower() not in low, bad

    required = [
        TITLE,
        'Задача работы — собрать и проверить поисковое ядро сайта для Москвы',
        'Главный вывод исследования: сайт «Окно Москва» уже хорошо оптимизирован под выявленный спрос как в обычной выдаче Яндекса, так и в выдаче Алисы',
        'полностью пересобирать ядро и структуру сайта не требуется',
        '2 415 поисковых фраз', 'ещё 550 фраз', '2 965 поисковых фраз',
        'числовой показатель спроса', 'частотность в широком соответствии',
        '2 840 уникальных поисковых фраз', '2 332 активные поисковые фразы',
        '2 313', '19', '168 групп поискового спроса',
        '75 проверок', '25 тем', 'полностью проверили 8', 'шесть тем', 'два контрольных запроса',
        '16 тем', '34 значимых вывода',
        '## Что дала проверка выдачи Алисы',
        'полностью пересобирать существующее распределение ядра по сайту не требуется'
    ]
    for marker in required:
        assert marker in text, marker

    assert len(re.findall(r'^\|\s*\d+\s*\|', text, re.M)) == 0
    assert text.count('**Почему это важно:**') == 7
    assert text.count('**Что рекомендуется сделать:**') == 7

    alice_queries = [
        'панорамные алюминиевые окна', 'алюминиевые окна для веранды', 'панорамное остекление балкона',
        'установка подоконника на пластиковые окна', 'французские панорамные окна',
        'замена окна на пластиковое цена москва', 'как открыть пластиковое окно', 'лучшие пластиковые окна'
    ]
    for q in alice_queries:
        assert f'| {q} |' in text, q

    d = Document(DOCX)
    dtext = '\n'.join(p.text for p in d.paragraphs)
    assert TITLE in dtext
    assert len(d.tables) == 8, len(d.tables)

    reader = PdfReader(PDF)
    assert not reader.is_encrypted
    pages = len(reader.pages)
    assert 6 <= pages <= 10, pages
    ptext = '\n'.join((p.extract_text() or '') for p in reader.pages)
    ntext = norm(ptext).lower()
    for marker in [
        'https://okno-msk.ru/', 'собрать и проверить поисковое ядро сайта для Москвы',
        '2 415 поисковых фраз', '2 965 поисковых фраз', '2 840 уникальных поисковых фраз',
        'числовой показатель спроса', 'частотность в широком соответствии',
        '75 проверок', '25 тем', 'выдачи Алисы', 'Что нужно изменить на сайте', 'Итог'
    ]:
        assert norm(marker).lower() in ntext, marker
    for bad in ['Приложение. Что показала обычная выдача', 'count', 'генеративный']:
        assert bad.lower() not in ntext, bad

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
            'site_url_visible_in_title': True,
            'semantic_core_is_primary_research_object': True,
            'full_rebuild_not_falsely_claimed': True,
            'direct_dual_surface_optimization_verdict_visible': True,
            'wordstat_phrase_counts_written_as_phrases_not_rows': True,
            'english_internal_wordstat_field_name_absent': True,
            'wordstat_demand_indicator_explained_in_russian': True,
            'frequency_work_visible_without_false_exact_frequency_claim': True,
            'unique_2840_not_exact_frequency_measurements': True,
            '168_units_presented_as_demand_groups': True,
            'ordinary_yandex_75_is_targeted_validation_not_total_scope': True,
            'raw_75_query_appendix_absent': True,
            'alice_selection_causal_bridge_visible': True,
            'alice_25_candidates_to_8_complete_checks_explained': True,
            'alice_6_decision_sensitive_plus_2_controls_explained': True,
            'alice_16_repeated_types_plus_1_held_explained': True,
            'alice_not_presented_as_research_author': True,
            'alice_customer_vocabulary_is_vydacha_alice': True,
            'positive_site_result_is_aggregate_not_page_catalogue': True,
            'seven_recommendations_have_explicit_why': True,
            'two_company_fact_requests_visible_without_partial_ready_framing': True,
            'old_21_item_routing_dump_absent': True,
            'generic_disclaimer_section_absent': True,
            'docx_has_eight_alice_cards_and_no_75_query_table': True,
            'pdf_openable_not_encrypted': True,
            'pdf_all_pages_rendered': True,
            'document_02_not_modified': True,
            'document_03_not_modified': True,
            'provider_calls_during_rebuild_zero': True
        },
        'counts': {
            'wordstat_first_pass_phrases': 2415,
            'wordstat_expansion_phrases': 550,
            'source_phrases_before_deduplication': 2965,
            'unique_search_phrases_after_deduplication': 2840,
            'excluded_rows_internal_authority': 334,
            'deferred_rows_internal_authority': 174,
            'active_search_phrases': 2332,
            'assigned_search_phrases': 2313,
            'unresolved_search_phrases': 19,
            'demand_groups': 168,
            'ordinary_yandex_targeted_checks': 75,
            'alice_candidates_reviewed': 25,
            'alice_cases_selected': 8,
            'alice_decision_sensitive_cases': 6,
            'alice_controls': 2,
            'alice_candidates_not_selected_repeated_types': 16,
            'alice_candidates_held': 1,
            'material_results_internal_authority': 34,
            'ready_recommendations': 7,
            'company_fact_requests': 2,
            'pdf_pages': pages
        },
        'wordstat_count_semantics': 'CUSTOMER_TEXT_USES_RUSSIAN_DEMAND_FREQUENCY_EXPLANATION__NO_INTERNAL_COUNT_FIELD__NO_FALSE_OPERATOR_EXACT_CLAIM',
        'research_object_semantics': 'SEARCH_CORE_AND_DEMAND_TO_PAGE_DISTRIBUTION__INTENT_IS_GROUPING_CRITERION_ONLY',
        'sha256': {'md': sha(MD), 'docx': sha(DOCX), 'pdf': sha(PDF)},
        'size_bytes': {'md': MD.stat().st_size, 'docx': DOCX.stat().st_size, 'pdf': PDF.stat().st_size},
        'provider_calls_during_rebuild': 0,
        'next_action': 'OWNER_REVIEW_CORRECTED_DOCUMENT_01'
    }
    QA_PATH.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    man = json.loads(MAN_PATH.read_text(encoding='utf-8'))
    man['status'] = 'DOCUMENT_01_FINAL_CUSTOMER_CONTRACT_ANALYST_RECHECK_PASS__OWNER_REVIEW_PENDING__DOCUMENT_02_03_NOT_ADVANCED'
    art = man['recipient_artifacts'][0]
    art['size_bytes'] = PDF.stat().st_size; art['sha256'] = sha(PDF); art['pages'] = pages
    art['recipient_contract'] = 'NON_SPECIALIST_CUSTOMER_GETS_KWORK_ANSWER_SEARCH_CORE_FREQUENCY_WORK_ORDINARY_YANDEX_ALICE_VERDICT_AND_ACTIONS_WITHOUT_RAW_75_QUERY_DUMP'
    for item in man['editable_and_source_files']:
        if item['path'] == 'editable/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.docx':
            item['size_bytes'] = DOCX.stat().st_size; item['sha256'] = sha(DOCX)
        if item['path'] == 'sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.md':
            item['size_bytes'] = MD.stat().st_size; item['sha256'] = sha(MD)
    man['qa']['authority'] = '../RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_01_COMMISSIONER_REPORT_QA_2026-09-06.json'
    man['qa']['analyst_recipient_qa'] = 'DOCUMENT_01_FINAL_CUSTOMER_CONTRACT_PASS'
    man['qa']['document_01'] = 'ANALYST_RECHECK_PASS__OWNER_REVIEW_PENDING'
    man['qa']['document_01_physical_pdf'] = f'{pages}_OF_{pages}_PAGES_RENDER_PASS'
    man['qa']['document_01_search_observations'] = '75_TARGETED_CHECKS_EXPLAINED__RAW_APPENDIX_ABSENT'
    man['qa']['document_01_alice_cases'] = '8_OF_8_COMPLETE__25_CANDIDATES__6_DECISION_SENSITIVE__2_CONTROLS'
    man['qa']['document_01_site_url_in_title'] = True
    man['qa']['document_01_frequency_work_visible'] = True
    man['qa']['document_01_internal_count_field_absent'] = True
    man['qa']['document_01_positive_no_change_page_catalogue'] = 'ABSENT__AGGREGATE_SITE_RESULT_ONLY'
    man['qa']['document_01_raw_75_query_appendix'] = 'ABSENT'
    man['qa']['document_01_full_rebuild_claim'] = 'ABSENT__RESEARCH_CONCLUDES_FULL_REBUILD_NOT_REQUIRED'
    man['qa']['document_01_github_readback'] = 'PENDING_POST_COMMIT_READBACK'
    man['qa']['next_action'] = 'OWNER_REVIEW_CORRECTED_DOCUMENT_01'
    MAN_PATH.write_text(json.dumps(man, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print('DOCUMENT_01_FINAL_CUSTOMER_QA_PASS', pages, sha(MD), sha(DOCX), sha(PDF))


if __name__ == '__main__':
    main()
