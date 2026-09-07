# OKNO_MSK — исправление границы исследования и финальная узкая коррекция A031 документа №02

Дата: 2026-09-07  
Статус: `ANALYST_RECHECK_PASS__OWNER_REVIEW_PENDING`

## История приёмки и инцидента

1. Первая перестройка отчёта №02 получила `ANALYST_QA_PASS`.
2. Владелец вернул её с результатом `FAIL` по содержательным и клиентским дефектам.
3. Первоначальная вторая коррекция выполнила новые чтения сайта и классификацию портфолио на этапе отчёта, потому что предыдущая инструкция ошибочно предписала заполнить пробелы внедрения свежими фактами.
4. Владелец квалифицировал это как отдельный серьёзный процессный отказ: `REPORT MATERIALIZATION != NEW RESEARCH`.
5. Универсальная заморозка исследовательского объёма из удалённого коммита `54202abf62d46caf529751c133b5864e9935f9d1` интегрирована как действующая власть и не изменялась.
6. Новые проектные материалы помещены в карантин, документ №02 повторно собран только из завершённого исследования и принятых допущений, существовавших до ошибочного сбора.
7. После аналитического PASS заморозки объёма владелец обнаружил один остаточный дефект A031: год рейтинга был ошибочно перенесён на дату публикации статьи, а место было усилено до неподтверждённой позиции перед списком.
8. Финальная узкая коррекция оставила A031 готовым, но привязала 2024 год только к рейтингу, вернула размещение к доказанной границе раздела и запретила вывод о дате публикации статьи.
9. Финальная аналитическая перепроверка выполнена; приёмка владельцем остаётся ожидаемой.

## Что было помещено в карантин

- `RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_02_CURRENT_SITE_PLACEMENT_EVIDENCE_2026-09-07.md`;
- `RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_02_PORTFOLIO_MAPPING_EVIDENCE_2026-09-07.tsv`.

Оба файла явно помечены:

```text
POST_HOC_REPORT_STAGE_COLLECTION
NOT ORIGINAL RESEARCH AUTHORITY
NOT AUTHORIZED TO UPGRADE READINESS
PROVENANCE / OWNER-IDENTIFIED INCIDENT HISTORY ONLY
```

Файлы сохранены для аудита затрат и истории ошибки. Генератор, валидатор и клиентский отчёт не используют их для фактов, точности размещения, классификации или повышения готовности.

## Итоговая готовность по завершённому исследованию

Полностью готовыми остались три изменения, для которых сохранённая власть уже содержала одну достаточную границу размещения:

- французские окна — после вводного определения и до последующей ценовой/конфигурационной части;
- критерии размера ПВХ-двери — после блока о видах створок и до цен;
- безопасная историческая коррекция рейтинга 2024 года — в разделе «Рейтинг производителей оконных профилей», в той части, где рейтинг 2024 года назван актуальным «в этом году».

В частичное состояние переведены пять пунктов:

- размеры окон частного дома — сохранённая власть указывает два возможных места;
- монтаж ПВХ-дверей — не установлено одно место и не подтверждён состав услуги;
- вентиляция алюминиевого остекления — сохранённая власть указывает два возможных участка;
- портфолио — необходимость навигации подтверждена, но карточки в завершённом исследовании не классифицированы;
- панорамное алюминиевое остекление — сохранённая власть указывает два возможных участка.

Четыре прежних вопроса проверки и двадцать отложенных тем остаются заблокированными. Пятнадцать сохранённых строк потенциальных ссылок сведены в четырнадцать видимых уникальных решений без чтения страниц.

## Контроль объёма после уточнения владельца

```text
REPORT_STAGE_NEW_PROJECT_FACT_COLLECTION = 0
UNAUTHORIZED_CURRENT_SITE_RECOLLECTION_AFTER_CLARIFICATION = 0
UNAUTHORIZED_SEARCH_RECOLLECTION = 0
UNAUTHORIZED_WORDSTAT_RECOLLECTION = 0
UNAUTHORIZED_ALICE_AI_RECOLLECTION = 0
POST_HOC_REPORT_STAGE_EVIDENCE_USED_TO_UPGRADE_READINESS = 0
REPORT_PROJECT_FACTS_TRACE_TO_PRE_EXISTING_RESEARCH_AUTHORITY = PASS
EXTERNAL_METHODOLOGY_BIBLIOGRAPHY_FRESHNESS = PASS
```

Свежая проверка десяти внешних методических источников сохранена: она не создаёт фактов об OKNO_MSK и не повышает готовность проектных действий.

## Материализация и QA

```text
READY_PHYSICAL_ACTIONS = 3
PARTIAL_ACTIONS = 5
BLOCKED_RECHECK_ITEMS = 4
MAPPING_ONLY_RESULTS = 46
INTERNAL_LINK_AUTHORITY_ROWS = 15
VISIBLE_UNIQUE_LINK_DECISIONS = 14
DUPLICATE_VISIBLE_LINK_PAIRS_WITHOUT_EXPLANATION = 0
CLIENT_POST_HOC_PORTFOLIO_MAPPING_ROWS = 0
PROJECT_INTERNAL_IDS_IN_CLIENT_REPORT = 0
PROJECT_INTERNAL_FILENAMES_IN_CLIENT_REPORT = 0
PROJECT_INTERNAL_ENUMS_IN_CLIENT_REPORT = 0
CLIENT_PLACEHOLDERS = 0
ARTICLE_PUBLICATION_DATE_CLAIM = 0
RANKING_YEAR_2024_CLAIM = present
CURRENT_RANKING_CLAIM = 0
NEW_RANKING_DATE = 0
TEMPORAL_FACT_ATTRIBUTION = PASS
MARKDOWN_DOCX_PDF_EQUIVALENCE = PASS
VISUAL_QA = PASS__19_OF_19_PAGES
DOCUMENT_01_MODIFIED = false
DOCUMENT_03_MODIFIED = false
SEMANTIC_CORE_04_MODIFIED = false
```

- Markdown: 64 547 байт; SHA-256 `cbaad2ad0e8d6be4413fa0384cb3ca7e87ca9c83e202e9209f0d31ffafcc6ffd`.
- DOCX: 32 862 байта; SHA-256 `5307486541988d97fb21b9772b1c543865671728605a9cd383d98360a14453f3`.
- PDF: 251 160 байт; 19 страниц; SHA-256 `5f590d88c6da7912bc04a73f9ce9c60e7c4a15a6b54b56a007d831844a0c9f88`.
- Детерминированная проверка: 53/53, `PASS`.
- Все 19 страниц финального PDF и независимый рендер DOCX визуально проверены.

## Следующее действие

```text
CURRENT_RESULT = ANALYST_RECHECK_PASS
OWNER_REVIEW = PENDING
NEXT_ACTION = OWNER_REVIEW_FINAL_CORRECTED_DOCUMENT_02__DO_NOT_START_DOCUMENT_03
```
