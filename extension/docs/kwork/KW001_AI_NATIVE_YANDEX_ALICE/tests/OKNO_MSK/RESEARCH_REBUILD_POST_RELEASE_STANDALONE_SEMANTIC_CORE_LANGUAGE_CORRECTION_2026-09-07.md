# OKNO_MSK — исправление языка отдельного семантического ядра

Дата: 2026-09-07

Статус: `COMPLETE__DATA_WORKBOOK_RUSSIAN_LANGUAGE_VISUAL_QA_PASS__PERSISTED_IN_GITHUB`

## 1. Дефект owner review

Первый standalone XLSX был аналитически корректен и прошёл 51/51 первоначальных автоматических проверок, но не прошёл проверку языка получателя. В обычные клиентские заголовки, значения и пояснения попали технические английские API/schema/project labels.

Примеры утечки: `Wordstat result count`, `Wordstat association count`, `BROAD_GETTOP_NO_OPERATORS`, `MAX_PER_PHRASE_SEPARATELY_FOR_RESULT_AND_ASSOCIATION`, `DEVICE_ALL`, `RESULT`, `ASSOCIATION_ONLY`, `NO_POSITIVE_COUNT`, `Provenance`, `Source authority`, `Higher-precedence authority`, `broad result`, `broad_result`, а также необъяснённые статусы/действия `ASSIGNED`, `ASSIGNED_HOLD`, `SEARCH_REQUIRED`, `REVIEW_DEFERRED`, `EXCLUDED_PRESERVED`, `NO_STANDALONE_PAGE`, `OUTSIDE_SCOPE_NO_ACTION`, `DEFER_PENDING_EVIDENCE`, `KEEP_EXISTING_STRUCTURE`, `ROUTE_TO_EXISTING_PAGE_AS_SUBTASK` и другие значения тех же классов.

Это дефект продукта и представления. Дефекта канонической семантики, кластеров, страниц или частотности не установлено.

## 2. Почему первоначальный QA прошёл

Первоначальный QA проверял полноту строк, Stage-5/Step-08 equivalence, отсутствие подмены устаревшим Step-19, числовые значения, формулы, листы, таблицы, фильтры, freeze panes и визуальный рендер. Он не сканировал клиентские поля на необъяснённые internal English/API/project codes.

```text
INTERNAL REPRESENTATION WAS TREATED AS CLIENT PRESENTATION
TECHNICAL TRACEABILITY WAS CONFUSED WITH CLIENT READABILITY
SPECIALIST RECIPIENT WAS TREATED AS PERMISSION TO DUMP INTERNAL SCHEMA
```

## 3. Терминологическая власть

Официальный русский клиентский язык берётся из интерфейса Вордстата: «Вордстат», «Топы запросов», «популярные запросы», «похожие запросы», «число запросов», «регион», «тип устройства», «все устройства», «без операторов».

Технические API-идентификаторы `GetTop`, `DEVICE_ALL`, `results[]`, `associations[]`, `phrase`, `count` сохраняются только для воспроизводимости в коде, QA и явно технических строках/полях.

Проектные enum/status/action/maturity/uncertainty codes сохраняются только как вторичная трассировка вместе с основным русским отображением.

Источники:

- https://yandex.ru/support2/wordstat/ru/interface/new
- https://yandex.ru/support2/wordstat/ru/content/operators
- https://aistudio.yandex.ru/ru/docs/search-api/operations/wordstat-gettop
- https://yandex.ru/support/webmaster/ru/recommendations/targeting
- https://www.semrush.com/blog/keyword-clustering/
- https://www.semrush.com/blog/keyword-mapping/
- https://ahrefs.com/blog/keyword-intent/
- https://ahrefs.com/blog/keyword-cannibalization/

## 4. Исправленная терминология и materializer

Materializer теперь использует детерминированные русские display maps для всех реально встречающихся клиентских категорий: семантического статуса, интента, границы бизнеса, роли страницы, структурного действия, готовности, неопределённости, уверенности, поискового маршрута, роли частотности и контентных состояний.

Основные заголовки/значения заменены на «Число запросов — популярные», «Число запросов — похожие», «Топы запросов Вордстата, без операторов», «Все устройства», «Количество исходных наблюдений», «Происхождение данных», «Источник решения» и «Приоритетный источник решения». Английское `broad` удалено из обычных пояснений.

Неизвестный client-visible enum без русского label завершает build ошибкой. Технические коды остаются в `06_Справочник` и явно обозначенных технических полях.

## 5. Validator / language QA

Независимый validator не импортирует display maps из materializer. Он отдельно:

- перечисляет значения категорий из Stage-5/Step-08 authorities;
- требует полного независимого русского mapping;
- проверяет dictionary coverage;
- сканирует все шесть листов;
- допускает Latin/machine text только в явных ID/URL/file/source/technical-code surfaces;
- запрещает известные internal English/API labels и необъяснённые enum patterns в обычной презентации;
- требует ноль forbidden hits и ноль unmapped enums.

## 6. Неизменная аналитическая власть

Materializer продолжает брать semantic/page truth только из Stage-5, unit truth из Stage-5 unit authority, frequency/provenance из Step-08. Устаревший Step-19 остаётся исторической трассировкой и не является финальной властью.

Контрольные значения до/после должны остаться: 2 840 уникальных фраз; 2 332 активных; 2 313 назначенных; 19 требуют проверки; 168 структурных единиц; 60 URL; 393 управляемые строки без URL, включая 246 / 115 / 32. Финальные подтверждённые значения будут записаны после Block-C regeneration/QA.

## 7. Контроль хэша

- исходный XLSX до первой языковой коррекции SHA-256: `d0df6724ed00af70bd07a8f1a22dcc2679d6023f1c4938697c3a793679a8d550`;
- XLSX после первой, частичной языковой коррекции SHA-256: `4f3835b32d6d59969bb947d12dcbd33e36044d3ce8ae47670c83c4fdcdfd5522`;
- финально исправленный XLSX SHA-256: `cee26a8d7d4a8381d4706c7940b739c3afca652034e9e3630053e35bd0184e3a`;
- финально исправленный XLSX размер: `1431390` байт.

Финальный language scan: 181172 непустые ячейки; 154488 обычных клиентских; 26684 технических/ID ячеек освобождены по явному allowlist; forbidden hits = 0; unmapped enum values = 0; primary English machine-value leakage = 0.

## 7A. Остаточный дефект названия листа

Повторная owner review установила, что первая языковая коррекция успешно перевела заголовки и значения ячеек, но оставила видимое название листа `05_SEARCH_REQUIRED`. Валидатор проверял содержимое ячеек, но не считал названия листов частью клиентского представления.

```text
CELL LANGUAGE QA
WAS INCORRECTLY TREATED AS
WHOLE-WORKBOOK LANGUAGE QA
```

Исправленное правило:

```text
WORKBOOK CLIENT LANGUAGE
= SHEET TITLES
+ HEADERS
+ ORDINARY CLIENT CELLS
+ HUMAN EXPLANATIONS
```

Клиентский лист переименован в `05_Проверка_в_Яндексе`. Канонический внутренний статус `SEARCH_REQUIRED` не изменён. Validator теперь отдельно сканирует worksheet titles и требует `UNEXPLAINED_INTERNAL_ENGLISH_IN_WORKSHEET_TITLES = 0`.

Финальная проверка: названий листов проверено 6; запрещённых попаданий в названиях — 0; обычных клиентских ячеек проверено 154488; технических/ID ячеек освобождено по allowlist 26684; запрещённых попаданий в заголовках и обычных ячейках — 0; неизвестных unmapped enum — 0. Data QA, workbook QA, Russian client-language QA и визуальный просмотр всех шести листов: `PASS`.

История результата сохранена явно: `INITIAL_DATA_QA = PASS`; `FIRST_OWNER_LANGUAGE_REVIEW = FAIL`; `FIRST_LANGUAGE_CORRECTION = PARTIAL__RESIDUAL_SHEET_TITLE_DEFECT_FOUND`; `FINAL_LANGUAGE_CORRECTION = PASS`.

## 8. Постоянные методологические исправления

В Level-1 добавлены: отдельный Step20 standalone semantic-core gate; routing отдельного XLSX рядом с Report №02; разделение machine/client display в Step19; русский language QA; complete reusable occurrence schema для Step3; union-compatible второй сбор Step5; 100% phrase→demand/provenance handoff Step8; cross-step принцип `COLLECT ONCE / PRESERVE COMPLETELY / DERIVE MANY VIEWS LATER`.

Поздний Step19/20 не должен повторно обращаться к провайдеру из-за собственной ранней потери уже возвращённых полей. Новый сбор разрешается только для действительно нового информационного требования.

## 9. Границы выполнения

```text
NEW_PROVIDER_CALLS = 0
DOCUMENTS_01_02_03_MODIFIED = false
SEMANTIC_AUTHORITY_CHANGED = false
```
