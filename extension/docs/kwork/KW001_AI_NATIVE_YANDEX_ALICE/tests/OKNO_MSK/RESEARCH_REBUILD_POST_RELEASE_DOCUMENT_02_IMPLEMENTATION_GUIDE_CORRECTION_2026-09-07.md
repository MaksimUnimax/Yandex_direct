# OKNO_MSK — исправление границы исследования при материализации документа №02

Дата: 2026-09-07  
Статус: `ANALYST_RECHECK_PASS__OWNER_REVIEW_PENDING`

## История приёмки и инцидента

1. Первая перестройка отчёта №02 получила `ANALYST_QA_PASS`.
2. Владелец вернул её с результатом `FAIL` по содержательным и клиентским дефектам.
3. Первоначальная вторая коррекция выполнила новые чтения сайта и классификацию портфолио на этапе отчёта, потому что предыдущая инструкция ошибочно предписала заполнить пробелы внедрения свежими фактами.
4. Владелец квалифицировал это как отдельный серьёзный процессный отказ: `REPORT MATERIALIZATION != NEW RESEARCH`.
5. Универсальная заморозка исследовательского объёма из удалённого коммита `54202abf62d46caf529751c133b5864e9935f9d1` интегрирована как действующая власть и не изменялась.
6. Новые проектные материалы помещены в карантин, документ №02 повторно собран только из завершённого исследования и принятых допущений, существовавших до ошибочного сбора.

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
- безопасная историческая коррекция рейтинга 2024 года — в разделе рейтинга непосредственно перед сохранённым списком.

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
MARKDOWN_DOCX_PDF_EQUIVALENCE = PASS
VISUAL_QA = PASS__19_OF_19_PAGES
DOCUMENT_01_MODIFIED = false
DOCUMENT_03_MODIFIED = false
SEMANTIC_CORE_04_MODIFIED = false
```

- Markdown: 64 343 байта; SHA-256 `31865ced072f34e92ec30ebb03beea1e4c6baf06597044902e2f4147df938a7c`.
- DOCX: 32 962 байта; SHA-256 `4e1d66bab0b57dafb801523f1428bfbc972eb3b1a02855aa3f99aa5041e1b54d`.
- PDF: 251 306 байт; 19 страниц; SHA-256 `4de84deb43ce2b821970abed72915ed167930e57defd1e8311d7b02ea5e2f17a`.
- Детерминированная проверка: 45/45, `PASS`.
- Все 19 страниц финального PDF и независимый рендер DOCX визуально проверены.

## Следующее действие

```text
CURRENT_RESULT = ANALYST_RECHECK_PASS
OWNER_REVIEW = PENDING
NEXT_ACTION = OWNER_REVIEW_SCOPE_CORRECTED_DOCUMENT_02__DO_NOT_START_DOCUMENT_03
```
