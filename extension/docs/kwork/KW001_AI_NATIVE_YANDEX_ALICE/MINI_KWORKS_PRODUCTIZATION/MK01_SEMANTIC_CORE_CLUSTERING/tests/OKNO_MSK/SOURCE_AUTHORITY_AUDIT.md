# MK01 / OKNO_MSK — аудит исходной authority

Статус: **PASS / PRE-STEP5A UNIVERSE ДОКАЗАН**

Дата аудита: **2026-09-09**  
Начальный live remote HEAD: `99f748ecc0ff83afd064d99717c24b93222d3b23`

## 1. Точный источник 2840-строчного universe

Authority состава фраз, состояния до обычного поиска и сохранённого Wordstat provenance:

```text
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv
```

Проверенные идентификаторы текущего файла:

```text
data rows = 2840
unique phrase keys = 2840
duplicate phrase keys = 0
SHA-256 = 73f52fd48ae925573b9739292b8c8893a8db40014775859c9630367703873d1f
Git blob = 17d4016b0b333b0b2124c5a380e3da044e59563b
last modifying commit = 976f6169bee2b32eabe8a18c6fc3d7034b3889fc
commit date = 2026-08-29 07:44:33 +0000
commit subject = KW001 OKNO: regenerate Step 08 after route-method correction [kw001-step08-route-correction-output]
```

Этот файл выбран как точная membership authority для MK01, потому что он:

- уже содержит полный нормализованный набор после Wordstat-сбора и построчной очистки;
- сохраняет все активные, спорные, отложенные и исключённые фразы;
- хранит частотность и source-level provenance по каждой фразе;
- создан до кластеризации и задолго до первого выполнения Step 5A;
- не содержит конкурентных добавлений;
- не зависит от URL-владения или поздней архитектуры сайта.

## 2. Схема source authority

Текущий TSV содержит 16 колонок:

```text
phrase
historical_status
historical_reason
corrected_status
corrected_reason
semantic_confidence
source_occurrences
result_occurrences
association_occurrences
max_result_count
max_association_count
source_ids
provenance
search_stage_disposition
next_resolution_route
route_reason
```

Для клиентского MK01 используются содержание фразы, показатели спроса, причины очистки, состояние, неопределённость и понятный индикатор происхождения. Внутренние коды переводятся в русский display-слой; исходные значения остаются во внутреннем TSV для проверки.

## 3. Происхождение 2840 строк

Состав universe воспроизводится из сохранённых Wordstat occurrence-строк:

| Слой | Строк |
|---|---:|
| Первый проход: 18 зафиксированных запросов Вордстата | 2415 |
| Точечный второй проход: 4 обоснованных запроса Вордстата | 550 |
| Все исходные occurrence-строки | 2965 |
| Строки результата | 2636 |
| Строки связанных запросов | 329 |
| Схлопнутые точные повторные occurrence-строки | 125 |
| Фразы с несколькими occurrence-строками | 101 |
| Уникальные точные фразы | **2840** |

Дедупликация выполнялась только по точному нормализованному тексту. Все 2965 исходных наблюдений сохранены в occurrence-слое, поэтому 125 повторных наблюдений не потеряны.

Источник occurrence-слоя:

```text
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_07C_SEMANTIC_CORRECTION_OCCURRENCES.tsv
data rows = 2965
SHA-256 = 8b89585f479d6c3d42c45fcccdfe2eacebabc54adef18eb59b992628b4dff26e
last modifying commit = 03444165367818f6c8f96d35b253b7b9e2da5a01
```

## 4. Состояния на границе Step 08

```text
CORE_CANDIDATE = 1388
REVIEW_SEARCH = 944
REVIEW_DEFERRED = 174
EXCLUDED_PRESERVED = 334
TOTAL = 2840
```

Это вход в точечную проверку обычной выдачи и кластеризацию, а не финальный клиентский статус.

## 5. Финальная MK01 cluster authority

Для автономного результата MK01 используется принятая pre-Step5A кластеризация:

```text
STEP_10_FRESH_R1_ASSIGNMENTS_FINAL.tsv
STEP_10_FRESH_R1_TAXONOMY_FINAL.tsv
STEP_10_FRESH_R1_CLUSTER_SUMMARY_FINAL.tsv
```

Проверенные факты:

```text
assignment rows = 2840
assignment unique phrases = 2840
phrase-set difference vs STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv = 0 in both directions
ASSIGNED = 2319
SEARCH_REQUIRED = 13
PRESERVED_DEFERRED = 174
PRESERVED_EXCLUDED = 334
active rows accounted = 2332
final clusters with member evidence = 59
target cluster count used = false
```

Идентификаторы:

| Artifact | SHA-256 | Last modifying commit |
|---|---|---|
| `STEP_10_FRESH_R1_ASSIGNMENTS_FINAL.tsv` | `ad97b8873b4dee78a1c9453cc6fe9ec8efb1cf1b9d18c436bd0475dd088b15c7` | `490b1567893fcbb1e05fbf5150ca311954d36ba8` |
| `STEP_10_FRESH_R1_TAXONOMY_FINAL.tsv` | `3cd28de9aae7935563f1116bce54198047625597cde4ef96db181a86f74ad14a` | `35e652cc0402a83fd696860f767842906c9a3997` |
| `STEP_10_FRESH_R1_CLUSTER_SUMMARY_FINAL.tsv` | `7dce38ae772473b447418ab3c5f7dbcb626cc0ea3cc82f78e480081496ffb230` | `35e652cc0402a83fd696860f767842906c9a3997` |

Эти файлы являются cluster authority MK01. Они не назначают клиенту URL и не требуют переноса поздних архитектурных решений.

## 6. Обычная выдача Яндекса

Сохранённая точечная проверка до Step 5A:

```text
selected exact queries = 75
normalized TOP-10 rows = 750
exact phrases present in 2840-row universe = 66
control/anchor formulations outside the universe = 9
region = 213 / Москва
direct evidence decisions = 75/75
new Search calls in this rehearsal = 0
```

`STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv` используется только для уже проверенных точных запросов. Из 75 решений 66 присоединяются к совпадающим exact phrase-строкам universe; 9 сохранены как контрольные/anchor-наблюдения вне 2840-row membership и не создают новых строк. Наблюдение по одной фразе не переносится автоматически на непроверенное семейство.

Известное ограничение сохранено: для запросов 2–75 доступна нормализованная TOP-10 проекция, но не полный raw XML и не все исходные provider request IDs. Повторный платный сбор ради восстановления утраченного bookkeeping не выполняется.

## 7. Проверка через более поздний pre-Step5A master

Файл:

```text
RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv
data rows = 2840
unique phrases = 2840
SHA-256 = 94c8baf092831b5db45eddca1e712cdd579e2eda3cf6662af1b3aeaed5341fa2
last modifying commit = a505c50b77dce02af105f48d43f30fdc66fd30e6
```

Его phrase-set совпадает с Step 08 и финальными Step-10 assignments: расхождений `0` в обе стороны. Это дополнительное доказательство стабильности 2840-строчного набора до Step 5A.

Однако Stage-5 master содержит более поздние поля конкретных страниц, владельцев, структурных действий и архитектурных решений. Поэтому он используется в MK01 только как cross-check состава, lineage и известных ограничений. Эти downstream-поля не становятся клиентским результатом MK01.

## 8. Почему integrated 2856-row core запрещён как источник

Поздний файл:

```text
STEP_05A_INTEGRATED_SEMANTIC_CORE_2026-09-09/FINAL_SEMANTIC_MASTER_STEP05A_INTEGRATED_2026-09-09.tsv
data rows = 2856
base rows = 2840
Step5A rows = 16
SHA-256 = f5fb9f8a2f597b72863341b5e0d867122dbccbc03007110ed1ecc7839ccbb410
added commit = 221b6af4ab2a555ea069a76c9fabec2a02768f3a
```

Его разность относительно доказанного base universe состоит ровно из 16 фраз принятой Step5A delta. Base-фраз, отсутствующих в integrated core, нет. Использование integrated core добавило бы отдельно продаваемое конкурентное расширение в базовый MK01, поэтому этот файл не является источником результата.

Контрольные 16 фраз хранятся в:

```text
STEP_05A_FIRST_EXECUTION_2026-09-08/STEP_05A_ACCEPTED_SEMANTIC_PIPELINE_DELTA.tsv
data rows = 16
commit = 272bd944180ca06acdc5e319889a401aa00c874c
```

Phase-5 QA сравнивает результат с этим набором и требует `Step5A contamination = 0`.

## 9. Связанные preserved files

| Назначение | Preserved artifact | Роль в MK01 |
|---|---|---|
| Исходный заказ и сайт | `TEST_ORDER.md`, `STEP_01_ACCEPTANCE.md`, `STEP_01_MERGED_BUSINESS_PAGE_MODEL.md`, `OPEN_QUESTIONS_FOR_CLIENT.md` | фактический бизнес-контекст без поздних рекомендаций |
| План сбора | `STEP_02_SEED_QUERY_PLAN.md`, `STEP_02_ACCEPTANCE.md` | 18 исходных seed-направлений и правила второго прохода |
| Первый Wordstat-проход | `STEP_03R_S01..S18_RAW_NORMALIZED.tsv`, raw JSON и checkpoints | 2415 occurrence-строк, регион и режим сбора |
| Второй Wordstat-проход | `STEP_05_P2_01..04_RAW_NORMALIZED.tsv`, manifest и acceptance | 550 union-compatible occurrence-строк |
| Полный occurrence audit | `STEP_07C_SEMANTIC_CORRECTION_OCCURRENCES.tsv` | сохранение всех 2965 наблюдений |
| Membership, demand, provenance, routing | `STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv` | главная 2840-row source authority |
| Точечный Search | `STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv`, `STEP_09_SERP_RESULTS.tsv`, R2 projection parts | только bounded exact-query evidence |
| Кластеризация | `STEP_10_FRESH_R1_ASSIGNMENTS_FINAL.tsv`, taxonomy и summary | 59 task-first clusters, 2840-row accounting |
| Более поздний pre-Step5A master | `RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv` | cross-check phrase-set/lineage; downstream поля не экспортируются |
| Step5A delta и integrated core | Step5A delta + 2856-row integrated master | только отрицательный contamination control |

## 10. Итог аудита

```text
PRE_STEP5A_SOURCE_AUTHORITY_PROVED = true
SOURCE_UNIVERSE_ROWS = 2840
SOURCE_UNIQUE_PHRASES = 2840
SOURCE_DUPLICATE_PHRASE_KEYS = 0
RAW_OCCURRENCES_PRESERVED = 2965
STEP08_STEP10_PHRASE_SET_DIFFERENCE = 0
STEP08_STAGE5_PHRASE_SET_DIFFERENCE = 0
STEP5A_ADDITIONS_IDENTIFIED = 16
INTEGRATED_2856_USED_AS_SOURCE = false
PROVIDER_CALLS_DURING_REHEARSAL = 0
BLOCKER = NONE
```
