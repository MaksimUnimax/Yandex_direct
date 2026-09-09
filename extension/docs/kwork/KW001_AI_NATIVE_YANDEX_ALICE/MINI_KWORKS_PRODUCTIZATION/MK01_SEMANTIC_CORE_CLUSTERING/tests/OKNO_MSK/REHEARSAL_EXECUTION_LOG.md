# MK01 / OKNO_MSK — журнал автономного rehearsal

Статус: **STEPS 00–10 EXECUTED FROM PRESERVED EVIDENCE / MATERIALIZATION PASS**

Дата автономной проекции: **2026-09-09**  
Новые обращения к провайдерам: **0**  
Источник universe: `STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv`, 2840 строки, до Step 5A.

## Сквозная сверка

```text
2965 сохранённых occurrence-наблюдений
- 125 повторных occurrence-наблюдений
= 2840 уникальных точных фраз

2840 фраз
= 2185 в рабочем ядре
 + 187 на проверке / с сохранённой неопределённостью
 + 468 исключённых с причиной

468 исключённых
= 334 исключены при построчной очистке
 + 134 отнесены к подтверждённо посторонним задачам после кластеризации

59 смысловых групп
= 54 рабочие группы
 + 5 подтверждённо посторонних групп
```

## STEP 00 — фиксация заказа и scope

| Поле | Фактическое выполнение |
|---|---|
| Input | Публичный сайт `https://okno-msk.ru/`, исходный `TEST_ORDER.md`, `OPEN_QUESTIONS_FOR_CLIENT.md`, сохранённая приёмка Step 01 |
| Authority | `CLIENT_INPUT_CONTRACT.md`, `PRODUCT_SCOPE.md`, `steps/STEP_00_ORDER_SCOPE_FREEZE.md` |
| Операция | Фактический контекст пилота переложен в автономный заказ только MK01; зафиксированы сайт, Москва, 16 направлений, B2C-контекст, Yandex-only и явные исключения продукта |
| Output | `MOCK_CLIENT_ORDER.md` |
| Сверка | 1 заказ; 16 направлений; обязательные Webmaster / Metrika / Direct / Google-входы = 0 |
| Неопределённость | Неизвестны маржинальность, загрузка производства и самостоятельный коммерческий приоритет сервисов/аксессуаров/рассрочки; они не выдуманы |
| QA | PASS: freeze gate заполнен, scope не расширен |

## STEP 01 — текущий сайт и бизнес-модель

| Поле | Фактическое выполнение |
|---|---|
| Input | Сохранённый обход публичного сайта и принятые job-specific модели |
| Authority | `STEP_01_MERGED_SITE_INVENTORY.md`, `STEP_01_MERGED_BUSINESS_PAGE_MODEL.md`, `STEP_01_MULTI_PASS_DISCOVERY_CROSSCHECK.md`, `STEP_01_ACCEPTANCE.md` |
| Операция | Из preserved evidence взяты только бизнес, предложение, регион и словарь, необходимые для семантики; поздние решения о страницах не переносились |
| Output | Business/site context в `MOCK_CLIENT_ORDER.md`; граница использования в `SOURCE_AUTHORITY_AUDIT.md` |
| Сверка | В исходном discovery были прочитаны 64 публичных URL; новых открытий сайта в rehearsal = 0 |
| Неопределённость | Снимок сайта относится к 2026-08-28; актуальность после снимка не предполагается |
| QA | PASS WITH RECORDED FRESHNESS LIMIT: preserved snapshot достаточен для replay, но не объявлен новым обходом |

## STEP 02 — план Wordstat-сбора

| Поле | Фактическое выполнение |
|---|---|
| Input | Зафиксированные направления заказа и словарь существующего сайта |
| Authority | `STEP_02_SEED_QUERY_PLAN.md`, `STEP_02_ACCEPTANCE.md` |
| Операция | Проверена сохранённая manifest-first матрица исходных запросов и stop logic; seed не трактовался как автоматически валидная финальная фраза |
| Output | 18 исходных запросов первого прохода; план одного точечного второго прохода |
| Сверка | 18 seed-запросов; регион 213 / Москва; все устройства; операторов нет; лимит 200 фраз на запрос |
| Неопределённость | Seeds задают направления сбора, а не финальные кластеры, URL или приоритеты |
| QA | PASS: каждый seed имеет связь с зафиксированным направлением, рекурсивное расширение не разрешено автоматически |

## STEP 03 — Wordstat acquisition / persistence

| Поле | Фактическое выполнение |
|---|---|
| Input | 18 зафиксированных запросов первого прохода |
| Authority | `STEP_03R_S01..S18_RAW_PROVIDER_RESULT_2026-08-29.json`, `STEP_03R_S01..S18_RAW_NORMALIZED.tsv`, checkpoints, `STEP_03R_FINAL_RECONCILIATION_2026-08-29.md` |
| Операция | Проверены сохранённые raw/normalized пакеты и их reconciliation; повторного получения данных не было |
| Output | 2415 occurrence-строк: 2153 строки результатов и 262 строки связанных запросов |
| Сверка | 18/18 запросов завершены; сохранённая стоимость исходного выполнения 0,36 ₽; provider calls rehearsal = 0 |
| Неопределённость | Метрика широкого сбора без операторов не объявлена точной частотностью |
| QA | PASS: нормализованные строки имеют source IDs и соответствуют сохранённому batch-учёту |

## STEP 04 — первичная сортировка

| Поле | Фактическое выполнение |
|---|---|
| Input | 2415 occurrence-строк первого прохода и зафиксированная бизнес-модель |
| Authority | `STEP_04_PROGRESSIVE_CLEANUP_1.md`, `STEP_04_ACCEPTANCE.md`, `STEP_04_METHOD_REVIEW_CORRECTION.md` |
| Операция | Воспроизведена консервативная трёхстатусная логика `KEEP / REVIEW / REJECT_OBVIOUS`; низкий спрос и принадлежность к associations не использованы как автоматическое основание |
| Output | Промежуточная смысловая триаж-модель и четыре доказанных пробела для второго прохода |
| Сверка | Потерянных строк = 0; молчаливых удалений = 0 |
| Неопределённость | Accessory, repair, finance и informational задачи сохранялись для дальнейшего решения |
| QA | PASS: спорное сохранялось в REVIEW, кластеризация и page ownership не выполнялись |

## STEP 05 — точечный второй Wordstat-сбор

| Поле | Фактическое выполнение |
|---|---|
| Input | Четыре обоснованных пробела: оконная фурнитура, панорамные окна, остекление балкона с выносом, окна для частного дома |
| Authority | `STEP_05_WORDSTAT_PASS2_MANIFEST.md`, `STEP_05_P2_01..04_RAW_NORMALIZED.tsv`, checkpoints, `STEP_05_ACCEPTANCE.md` |
| Операция | Проверены четыре сохранённых пакета точечного второго прохода и его stop decision; новых запросов не выполнялось |
| Output | 550 union-compatible occurrence-строк |
| Сверка | 4/4 исходных запросов успешны; дубликатов входа = 0; сохранённая стоимость исходного выполнения 0,08 ₽; provider calls rehearsal = 0 |
| Неопределённость | Новая лексика не принята автоматически; третий рекурсивный проход не разрешён |
| QA | PASS: все 550 строк сохранены, expansion stopped после доказанного прироста |

## STEP 06 — построчная семантическая очистка

| Поле | Фактическое выполнение |
|---|---|
| Input | 2965 occurrence-строк двух Wordstat-проходов |
| Authority | `STEP_07C_SEMANTIC_CORRECTION_OCCURRENCES.tsv`, `STEP_07C_SEMANTIC_CORRECTION_WORKING.tsv`, `STEP_07C_SEMANTIC_CORRECTION_SUMMARY.json`, QA cases и acceptance |
| Операция | Проверен exact-text dedupe и полный corrected row-level decision; каждая ранее принятая строка получила положительное основание, default KEEP отсутствует |
| Output | 2840 уникальных фраз: KEEP 1388, REVIEW 1118, EXCLUDE_SCOPE 180, EXCLUDE_IRRELEVANT 120, EXCLUDE_MECHANICAL 34 |
| Сверка | 2965 − 125 повторных наблюдений = 2840; фраз с несколькими наблюдениями = 101; неавтоматически слитых non-exact кандидатов = 18 строк / 9 групп |
| Неопределённость | 1118 REVIEW сохранены; 174 association-only строки позднее отложены, а не приняты или удалены |
| QA | PASS: no silent default KEEP, low-frequency exclusion = false, association auto-keep = false, QA failures = 0 |

## STEP 07 — semantic freeze / routing

| Поле | Фактическое выполнение |
|---|---|
| Input | 2840 уникальных фраз после исправленной построчной очистки |
| Authority | `STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv`, `STEP_08_REVIEW_RESOLUTION_ROUTES.tsv`, reconciliation и acceptance |
| Операция | Зафиксирован единый pre-Search universe и назначен следующий маршрут каждой строке без потери исключений и неопределённости |
| Output | CORE_CANDIDATE 1388; REVIEW_SEARCH 944; REVIEW_DEFERRED 174; EXCLUDED_PRESERVED 334 |
| Сверка | 1388 + 944 + 174 + 334 = 2840; уникальных phrase keys = 2840; duplicate keys = 0 |
| Неопределённость | Маршрут REVIEW_SEARCH означает необходимость evidence, а не обещание включения |
| QA | PASS: исходный SHA-256 `73f52fd48ae925573b9739292b8c8893a8db40014775859c9630367703873d1f` заморожен |

## STEP 08 — точечный обычный поиск Яндекса

| Поле | Фактическое выполнение |
|---|---|
| Input | Ограниченная выборка точных вопросов из REVIEW_SEARCH, non-exact дублей и контрольных anchors |
| Authority | `STEP_09_SEARCH_PROBE_MANIFEST.tsv`, `STEP_09_SERP_RESULTS.tsv`, `STEP_09_SERP_R2_PROJECTION_RAW_PART_01..04.tsv`, `STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv`, acceptance |
| Операция | Повторно проверена полнота сохранённой проекции: 75 точных запросов, 750 TOP-10 строк и 75 решений; evidence не переносился на непроверенные семейства |
| Output | 75 direct evidence decisions для cluster stage |
| Сверка | 75/75 запросов; 750/750 ранжированных строк; 8/8 активных non-exact сравнений; provider calls rehearsal = 0 |
| Неопределённость | Для запросов 2–75 нет полного raw XML и всех исходных request IDs; ограничение сохранено, replay ради bookkeeping не выполнялся |
| QA | PASS WITH RECORDED RAW-FIDELITY LIMITATION: нормализованный TOP-10 ledger полный, per-item raw ledger неполный |

## STEP 09 — task-first clustering

| Поле | Фактическое выполнение |
|---|---|
| Input | Полный 2840-row universe, 75 точечных Search-наблюдений и сохранённые неопределённости |
| Authority | `STEP_10_FRESH_R1_ASSIGNMENTS_FINAL.tsv`, `STEP_10_FRESH_R1_TAXONOMY_FINAL.tsv`, `STEP_10_FRESH_R1_CLUSTER_SUMMARY_FINAL.tsv`, final QA |
| Операция | Проверена финальная assignment authority и phrase-set equality; технические коды 59 групп переведены в русские названия, задачи, intent и границы. Членство определено по пользовательской задаче, а не только по словам или URL |
| Output | ASSIGNED 2319; SEARCH_REQUIRED 13; PRESERVED_DEFERRED 174; PRESERVED_EXCLUDED 334; 59 групп |
| Сверка | Assignment rows = 2840; set difference vs Step 08 = 0; 2319 + 13 + 174 + 334 = 2840 |
| Неопределённость | 187 строк не превращены в cluster members. Внутри ASSIGNED выявлено 134 строки пяти групп с `business_fit=OUTSIDE`; они не выданы как рабочее ядро |
| QA | PASS: 59/59 групп имеют членов, representative — реальная фраза группы, target count отсутствует, page architecture не используется |

## STEP 10 — клиентская материализация и QA

| Поле | Фактическое выполнение |
|---|---|
| Input | 2840-row Step-08 authority, финальные Step-10 assignments/taxonomy, occurrence provenance, 75 Search decisions; Stage-5 master только для set cross-check; Step5A только для отрицательного contamination control |
| Authority | `DELIVERABLE_SPEC.md`, `QA_AND_RELEASE.md`, `SOURCE_AUTHORITY_AUDIT.md` |
| Операция | Генератор `build_mk01_rehearsal.mjs` выполнил проверяемые join/set/count assertions, создал клиентский XLSX и два TSV, пересчитал, повторно импортировал и отрендерил все 7 листов |
| Output | `MK01_OKNO_MSK_SEMANTIC_CORE_2026-09-09.xlsx`, semantic universe TSV, cluster summary TSV, build report, manifest, delivery summary |
| Сверка | Universe 2840; working 2185; review 187; excluded 468; groups 59; Step5A contamination 0; silent loss 0; duplicate keys 0 |
| Неопределённость | 13 строк требуют нового точечного Search в будущем заказе; 174 отложены до нового основания. Эти gaps показаны клиенту |
| QA | MATERIALIZATION PASS: 7 листов читаются после повторного импорта, формульных ошибок нет, визуальные рендеры проверены; полный G0–G12 оформляется отдельным `QA_REPORT.md` |

## Физические результаты materialization

| Artifact | Объём | Назначение |
|---|---:|---|
| `MK01_SEMANTIC_UNIVERSE_2026-09-09.tsv.gz` | 2840 строк после lossless-распаковки | полный машинно проверяемый UTF-8 TSV universe с provenance |
| `MK01_CLUSTER_SUMMARY_2026-09-09.tsv` | 59 строк | машинно проверяемая сводка групп |
| `MK01_OKNO_MSK_SEMANTIC_CORE_2026-09-09.xlsx` | 7 листов | самостоятельный клиентский результат |
| `MK01_WORKBOOK_BUILD_REPORT_2026-09-09.json` | 7 bounded inspections + 2 error scans | техническое доказательство сборки и повторного чтения |
| `MK01_MATERIALIZATION_MANIFEST_2026-09-09.json` | 1 manifest | counts, hashes, invariants и identities входов/выходов |

## Scope leakage control

```text
STEP5A_PHRASES_IN_UNIVERSE = 0
INTEGRATED_2856_USED_AS_SOURCE = false
QUERY_TO_URL_MAPPING_EXPORTED = false
NEW_ARCHITECTURE_EXPORTED = false
CREATE_SPLIT_MERGE_RECOMMENDATIONS_EXPORTED = false
INTERNAL_LINKING_EXPORTED = false
CONTENT_TZ_EXPORTED = false
AI_CONCLUSIONS_EXPORTED = false
GOOGLE_DATA_EXPORTED = false
```
