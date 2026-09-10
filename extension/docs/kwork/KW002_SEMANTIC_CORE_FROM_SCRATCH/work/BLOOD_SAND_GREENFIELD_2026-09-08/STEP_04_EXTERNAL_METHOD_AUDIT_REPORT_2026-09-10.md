# STEP 04 — внешний методический ретроспективный аудит

Дата: 2026-09-10  
Проверяемый результат: commit `91fc6e1ce155c0f854c9d3c7ebf5a7b5dea40d70`  
Статус аудита: **COMPLETE / PASS**  
Вердикт качеству Step04: **REWORK_REQUIRED**  
Оценка: **87/100 = 8.7/10**

## Что именно проверялось

Проверен первый завершённый Step04 как предварительная семейная сортировка полного Step03-корпуса. Это не повтор Step04, не Step05 и не попытка защитить прежний PASS. Поздний Step05 E013/`!чётки` и любые другие post-Step04 данные в оценке не использованы.

Публичный веб использовался только для чтения 12 разрешённых методических URL. Новых Wordstat, Yandex Search, GenSearch, Alice или AI-search вызовов не было. Закрытые прошлые исследования Blood & Sand не открывались.

## Проверка внешних источников

| ID | Источник | Издатель | URL | Доступ 2026-09-10 | Использованное положение | Граница утверждения |
| --- | --- | --- | --- | --- | --- | --- |
| S04-AUD-01 | Обучение — Как работать со спросом в поиске Яндекса | Yandex Webmaster | [ссылка](https://yandex.ru/support/webmaster/ru/training) | ACCESSIBLE / VERIFIED | Сначала структурируют спрос и оценивают релевантность/пригодность; посадочная страница идёт позже. | Не задаёт пять проектных статусов и не подтверждает релевантность конкретной фразы. |
| S04-AUD-02 | Подбор поисковых запросов и анализ рынка β | Yandex Webmaster | [ссылка](https://yandex.ru/support/webmaster/ru/service/queries-selection) | ACCESSIBLE / VERIFIED | Подходящие и неочевидные формулировки надо находить и оценивать отдельно; кластеризация определяется через смысл/интент. | Не определяет бизнес-факты Blood & Sand и не делает каждую найденную фразу целевой. |
| S04-AUD-03 | Добавили кластеризацию в «Подбор запросов и анализ рынка β» | Yandex Webmaster Blog | [ссылка](https://webmaster.yandex.ru/blog/wordcraft-clusterization) | ACCESSIBLE / VERIFIED | Кластер — запросы, близкие по смыслу или намерению; информационные и коммерческие смыслы могут различаться. | Описывает downstream-кластеризацию; не требует от Step04 готовых страниц. |
| S04-AUD-04 | На какие вопросы отвечает ваш сайт | Yandex Webmaster | [ссылка](https://yandex.ru/support/webmaster/ru/recommendations/targeting?lang=ru) | ACCESSIBLE / VERIFIED | Related-запросы раскрывают синонимы и неочевидные уточнения; популярность может меняться. | Related-канал не означает автоматическую пригодность для бизнеса. |
| S04-AUD-05 | Операторы | Yandex Wordstat | [ссылка](https://yandex.ru/support2/wordstat/ru/content/operators) | ACCESSIBLE / VERIFIED | Операторы -, !, +, кавычки, [], () и \| позволяют уточнять форму, состав, порядок и альтернативы. | Операторы уточняют сбор, но не решают релевантность или кластер. |
| S04-AUD-06 | Keyword Intent: What It Is and How to Use It in Your SEO Strategy | Ahrefs | [ссылка](https://ahrefs.com/blog/keyword-intent/) | ACCESSIBLE / VERIFIED | Причина запроса и соответствие реальной способности сайта обслужить его важнее привлекательного объёма; mixed intent существует. | Google-oriented industry practice; не официальный алгоритм Яндекса. |
| S04-AUD-07 | How to Focus on Topics (Not Keywords) in Your SEO Strategy | Ahrefs | [ссылка](https://ahrefs.com/blog/topics-not-keywords/) | ACCESSIBLE / VERIFIED | Одинаковые слова могут относиться к разным сущностям; для неоднозначных тем нужны сигналы лучше частотности. | Профессиональная методика, не источник клиентской истины. |
| S04-AUD-08 | Keyword Clustering in Seconds: Save Time With Keywords Explorer Tool | Ahrefs | [ссылка](https://ahrefs.com/blog/keyword-clustering-tools/) | ACCESSIBLE / VERIFIED | Term clustering полезен для предварительных тематических buckets; intent/page clustering — отдельный режим. | Предварительный bucket не становится финальным page cluster. |
| S04-AUD-09 | How To Do Keyword Clustering the Easy Way | Ahrefs | [ссылка](https://ahrefs.com/blog/keyword-clustering/) | ACCESSIBLE / VERIFIED | Page-oriented clustering опирается на похожий intent/результаты и остаётся интерпретируемым. | Google/SERP practice; на Step04 обычной Search-выдачи ещё нет. |
| S04-AUD-10 | How to Do Keyword Clustering & Why It Helps SEO | Semrush | [ссылка](https://www.semrush.com/blog/keyword-clustering/) | ACCESSIBLE / VERIFIED | Intent, SERP similarity, content coherence и user journey — разные сигналы; низкочастотные фразы могут быть значимы вместе. | Downstream page-oriented guidance, не разрешение проектировать страницы на Step04. |
| S04-AUD-11 | What are methods for keyword clustering and topic modeling? | Semrush | [ссылка](https://www.semrush.com/blog/what-are-methods-for-keyword-clustering-and-topic-modeling/) | ACCESSIBLE / VERIFIED | Допустимы intent, SERP overlap, semantic similarity и manual review. | Не объявляет ручную предварительную группу финальным SEO-кластером. |
| S04-AUD-12 | A taxonomy of web search | Andrei Z. Broder / SIGIR Forum | [ссылка](https://research.google/pubs/a-taxonomy-of-web-search/) | PARTIAL — BIBLIOGRAPHIC LANDING PAGE ONLY | Сохранённая аудитная сводка указывает на различие informational, navigational/entity и transactional needs. | Публичная страница отдала только библиографию без видимого abstract; содержательное положение используется лишь как вторичная сохранённая сводка. |

S04-AUD-12 доступен только частично: страница подтверждает автора, название, журнал и год, но не показывает текст abstract. Поэтому его содержательная taxonomy-proposition не используется как самостоятельно проверенная цитата; она отмечена только как вторичная сохранённая сводка. Основные выводы аудита и без неё полностью опираются на доступные Yandex/Ahrefs/Semrush источники.

## ЗАФИКСИРОВАННЫЙ МЕТОД АУДИТА — ДО СРАВНЕНИЯ СО СТАРЫМИ СТРОКАМИ

Ниже чек-лист, зафиксированный после проверки внешних источников и до повторного открытия F001..F032/E001..E017.

| Тест | Название | Зафиксированное правило |
| --- | --- | --- |
| M01 | FULL INPUT BEFORE JUDGMENT | 79/79 sources and all 25,979 occurrences before semantic comparison. |
| M02 | BUSINESS FIT IS SEPARATE FROM DEMAND | Observed wording/count is not automatic Blood & Sand relevance. |
| M03 | SEMANTIC / USER-PURPOSE / REFERENT BOUNDARIES BEAT TOKEN MATCHING | Entity/media/game/vehicle/person/place/astrology/practice context controls the boundary. |
| M04 | AMBIGUITY MUST STAY EXPLICIT | Unresolved meaning stays mixed/evidence-needed. |
| M05 | FREQUENCY IS NOT A RELEVANCE VERDICT | No high-volume rescue or low-volume rejection. |
| M06 | RELATED / NON-OBVIOUS WORDING IS COVERAGE EVIDENCE | Related wording can justify bounded expansion, not automatic KEEP. |
| M07 | PRELIMINARY FAMILY/TOPIC BUCKET != FINAL SEO CLUSTER | Step04 is exploratory organization. |
| M08 | FINAL PAGE CLUSTERING IS DOWNSTREAM | SERP/page evidence belongs to Steps 12–14. |
| M09 | PROVENANCE MUST SURVIVE SUMMARIZATION | Family decisions must trace to runs/seeds/carriers/business authority. |
| M10 | GAP/EXPANSION ROUTE MUST MATCH THE UNCERTAINTY | Client facts go to owner; vocabulary evidence may go to later authorized acquisition. |

## Независимая проверка корпуса и чисел

| Показатель | Старое заявление | Пересчитано независимо | Итог |
| --- | ---: | ---: | --- |
| CANONICAL_PRIMARY_PROBES | 79 | 79 | PASS |
| UNIQUE_RUN_ORDERS | 79 | 79, диапазон 1..79 | PASS |
| CURRENT_SOURCE_RESOLUTION | 79/79 | 79/79 | PASS |
| RESULT_OCCURRENCES | 24722 | 24722 | PASS |
| ASSOCIATION_OCCURRENCES | 1257 | 1257 | PASS |
| TOTAL_OCCURRENCES | 25979 | 25979 | PASS |
| FAMILY_ROWS | 32 | 32, уникальные F001..F032 | PASS |
| EXPANSION_QUEUE_ROWS | 17 | 17, уникальные E001..E017 | PASS |
| OWNER_OR_CLIENT_FACT_ROWS | 6 | 6 | PASS |
| PROVIDER_RELEVANT_QUEUE_ROWS | 15 | 15 | PASS |
| SILENT_DROPS | 0 | 0 по числовому reconciliation: сумма family counts = 25979 | PASS WITH REPRODUCIBILITY LIMIT |

Полностью реконструированы 79 текущих источников: 24 722 results и 1 257 associations. Пустые outcomes: 49, 50, 51, 57, 66, 67, 70. Все 96 файлов Step03 RAW tree были byte-read. Источники 32–48 и 50–51 взяты по принятой replacement mapping; исторические сломанные gzip не использованы как текущий gate.

Ограничение: опубликованный Step04 сохраняет family-level run/seed/carrier provenance и агрегатные counts, но не occurrence-level membership. Поэтому арифметически silent drops = 0, однако конкретную биекцию 25 979 occurrence IDs к 32 строкам нельзя независимо повторить по долговечным артефактам. Это D14 и причина вычета по H.

## Независимая reference re-triage

Независимая карта естественно дала **21 предварительную смысловую границу**, а не 32 строки. Разница нормальна: семь старых строк были отдельными нулевыми исходами, тогда как reference map рассматривает их как одну типологическую границу R21 с раздельной provenance.

| ID | Граница | Смысл |
| --- | --- | --- |
| R01 | Общие товарные классы | амулет/оберег/талисман без чужого референта |
| R02 | Чётки как предмет | отдельно от чётко/чёткий |
| R03 | Коммерческие модификаторы | купить/цена/заказать при поддержанном товаре |
| R04 | Товар для автомобиля | отдельно от моделей и запчастей |
| R05 | Каталожное имя + товарное слово | сильный предварительный сигнал |
| R06 | Короткое каталожное имя | plausible или mixed по контексту |
| R07 | Значение/история/мифология/тату/визуал | информационные и alternate-form ветви |
| R08 | Форма/материал | неподтверждённый клиентский факт |
| R09 | Эффект/аудитория | неподтверждённый клиентский факт |
| R10 | Зодиак + товар/коммерция | правдоподобная товарная ветвь |
| R11 | Общая астрология | иной user purpose |
| R12 | Молитва/мантра/практика | граница с физическим товаром |
| R13 | Chery/Renault/автодетали | чужой автомобильный референт |
| R14 | Игры и игровые предметы | явные game/franchise контексты |
| R15 | Книги/медиа/музыка | только при явном маркере; голые названия держать ambiguous |
| R16 | Места/организации/люди/бренды | явные именованные сущности |
| R17 | AUM industrial/organization | AUMA и Аум Синрикё отдельно от Ом/Аум товара |
| R18 | Другие товары/сущности | явный неассортиментный объект |
| R19 | Морфологический шум | контекстный, не токен-список |
| R20 | Related/association discovery | evidence for coverage, не acceptance |
| R21 | Пустой текущий исход | coverage question, не no-demand verdict |

Это не финальный keyword cleanup и не page cluster. Карта лишь показывает, какие смыслы надо держать раздельно до later Search/SERP stages.

## Сравнение с исходными 32 family rows

25 из 32 строк сохраняются без изменения. Изменения нужны в: **F010,F011,F015,F017,F022,F025,F032**.

| ID | Аудитный вердикт | Причина |
| --- | --- | --- |
| F010 | KEEP_WITH_WORDING_FIX | umbrella смешивает несколько user-purpose ветвей; mixed-state спасает от ложной финальности, но label надо уточнить |
| F011 | SPLIT_FAMILY | “сельский детектив чернобог” ошибочно классифицирован как эффект/аудитория |
| F015 | KEEP_WITH_WORDING_FIX | авто-краска не является моделью/деталью; scope verdict остаётся out-of-scope |
| F017 | SPLIT_FAMILY | bare “счастливый амулет” должен быть mixed, explicit media — out-of-scope |
| F022 | SPLIT_FAMILY | bare “талисман кота” не доказывает явный чужой референт |
| F025 | SPLIT_FAMILY | “оберег для водителя и автомобиля” надо вернуть в поддержанный car-use F003 |
| F032 | MERGE_FAMILY | exact-form zero уже покрыт наблюдаемыми car-use синонимами; это не отдельный material gap |

Подробное решение по каждой F001..F032 находится в `STEP_04_FAMILY_ROW_EXTERNAL_AUDIT_2026-09-10.tsv`.

## Сравнение с исходными 17 expansion rows

Изменения нужны в: **E004,E007,E014,E017**. Рекомендуемый queue после rework: **15 строк**, owner/client fact rows = **5**, provider-relevant rows = **13**. Это рекомендация аудита, не выполненный Step05.

- E004 + E017: объединить в один client-fact-gated item про физическую форму/молитвенную границу.
- E007 + E014: объединить в один car-use/vehicle-collision item; отдельный fan-out точной формы `для авто` имеет низкий прирост информации.

Остальные 13 queue rows имеют корректный тип маршрута: бизнес-факты идут владельцу, search-vocabulary gaps — в будущую отдельно разрешённую acquisition.

## Реестр дефектов

| Класс | ID | Severity | Конкретное доказательство | Методические источники | Минимальное исправление |
| --- | --- | --- | --- | --- | --- |
| D14 QA_OR_REPRODUCIBILITY_DEFECT | GLOBAL | MATERIAL | Сумма family counts = 25 979, но occurrence→family ledger/правила не опубликованы; нельзя независимо доказать конкретное распределение без исходного scratch-кода. | [S04-AUD-01](https://yandex.ru/support/webmaster/ru/training), [S04-AUD-11](https://www.semrush.com/blog/what-are-methods-for-keyword-clustering-and-topic-modeling/) | Опубликовать детерминированную карту run+channel+position→family и повторить partition QA. |
| D03 SEMANTIC_OVERBROAD_GROUPING | F010 | MINOR | В одной umbrella-строке объединены значение/история, фото/визуал, руны и татуировки. | [S04-AUD-03](https://webmaster.yandex.ru/blog/wordcraft-clusterization), [S04-AUD-10](https://www.semrush.com/blog/keyword-clustering/) | Переименовать как umbrella и показать подграницы без финального clustering. |
| D07 FREQUENCY_OR_TOKEN_SHORTCUT | F011 | MATERIAL | “сельский детектив чернобог” попал в эффекты/аудитории; смысл фразы медийный, вероятен ложный substring-match по “дет”. | [S04-AUD-07](https://ahrefs.com/blog/topics-not-keywords/), [S04-AUD-11](https://www.semrush.com/blog/what-are-methods-for-keyword-clustering-and-topic-modeling/) | Исправить границы токенов и перенести фразу в media. |
| D03 SEMANTIC_OVERBROAD_GROUPING | F015 | MINOR | “амулет краска для машины” — авто-краска/цвет, а не модель или деталь. Scope verdict верен, label неточен. | [S04-AUD-07](https://ahrefs.com/blog/topics-not-keywords/) | Расширить label или перенести в F022. |
| D06 FALSE_OR_EXCESSIVE_AMBIGUITY; D08 MISLABELED_TRIAGE_STATE | F017 | MATERIAL | Голое “счастливый амулет” не имеет явного media-marker, но объявлено obvious out-of-scope вместе с “дзен/рассказы”. | [S04-AUD-06](https://ahrefs.com/blog/keyword-intent/), [S04-AUD-07](https://ahrefs.com/blog/topics-not-keywords/) | Разделить explicit media и bare ambiguous phrase. |
| D06 FALSE_OR_EXCESSIVE_AMBIGUITY; D08 MISLABELED_TRIAGE_STATE | F022 | MATERIAL | “талисман кота” без контекста не доказывает чужой товар/произведение. | [S04-AUD-06](https://ahrefs.com/blog/keyword-intent/), [S04-AUD-07](https://ahrefs.com/blog/topics-not-keywords/) | Перенести bare phrase в mixed/ambiguous. |
| D08 MISLABELED_TRIAGE_STATE | F025 | MATERIAL | “оберег для водителя и автомобиля” прямо соответствует подтверждённому car-use, но оставлен в residual mixed. | [S04-AUD-01](https://yandex.ru/support/webmaster/ru/training), [S04-AUD-06](https://ahrefs.com/blog/keyword-intent/) | Перенести в F003 и пересчитать. |
| D10 FALSE_OR_LOW_VALUE_COVERAGE_GAP | F032 | MATERIAL | Пустая точная форма “талисман для авто” стала отдельным gap, хотя эквивалентные car-use формулировки уже наблюдались. | [S04-AUD-02](https://yandex.ru/support/webmaster/ru/service/queries-selection), [S04-AUD-04](https://yandex.ru/support/webmaster/ru/recommendations/targeting?lang=ru) | Слить с F003 как zero exact variant, не как отдельный expansion family. |
| D11 WRONG_EVIDENCE_ROUTE | E007;E014 | MATERIAL | Две queue-строки отвечают на одну car-use/vehicle collision boundary; отдельный exact-form fan-out имеет низкий information gain. | [S04-AUD-02](https://yandex.ru/support/webmaster/ru/service/queries-selection), [S04-AUD-05](https://yandex.ru/support2/wordstat/ru/content/operators) | Объединить в один bounded item. |
| D11 WRONG_EVIDENCE_ROUTE | E004;E017 | MATERIAL | Обе строки требуют одного owner fact о физической форме “Молитва Иоанн Златоуст” и затем одного условного probe. | [S04-AUD-02](https://yandex.ru/support/webmaster/ru/service/queries-selection), [S04-AUD-06](https://ahrefs.com/blog/keyword-intent/) | Объединить, сохранив всю provenance. |

## Сильные стороны

1. Полный corpus accounting: 79/79 и 25 979/25 979 по арифметике.
2. Сильные контекстные границы Chery/Renault, games, AUM industrial/cult, astrology и prayer/practice.
3. Частотность не использована как автоматический relevance verdict.
4. Реальная неоднозначность в основном сохранена через mixed/ambiguous, а не forced KEEP/REJECT.
5. Не выполнены преждевременные final clustering, URL, IA или page ownership.

## Слабые стороны

1. Нет долговечной occurrence→family карты для независимой репликации partition QA.
2. Несколько очевидных member-level ошибок видны даже в representative phrases.
3. Две bare ambiguous phrases преждевременно объявлены obvious out-of-scope.
4. Один прямой car-use запрос оставлен в residual mixed.
5. Queue содержит две дублирующие пары и один низкоинформативный exact-form gap.

## Что исправить до продолжения Step05

1. Исправить F011/F017/F022/F025 и пересчитать связанные counts/examples.
2. Уточнить labels F010/F015.
3. Слить F032 в F003 как zero exact-form observation, а не отдельный requires-expansion family.
4. Объединить E004+E017 и E007+E014; ожидаемый queue = 15 строк.
5. Материализовать occurrence ID `run_order + channel + position` → family_id и детерминированные reason fields; доказать отсутствие drop/duplicate на уровне идентичностей.
6. Повторить Step04 semantic QA без новых provider calls.

## Итог

Исходный вывод Step04 **материально не меняется**: полный корпус обработан, основные бизнес/шум/коллизионные границы найдены, downstream page decisions не придуманы. Но feed-forward нельзя безопасно продолжать как есть: семь family rows, четыре queue rows и воспроизводимость partition требуют ограниченного rework.

```text
AUDIT_VERDICT = REWORK_REQUIRED
QUALITY_SCORE_100 = 87/100
QUALITY_SCORE_10 = 8.7/10
STEP04_CONCLUSION_MATERIALLY_CHANGES = NO
STEP05_RESUME_RECOMMENDATION = KEEP_PAUSED_PENDING_STEP04_REWORK
PROVIDER_CALLS_DURING_AUDIT = 0
POST_STEP04_EVIDENCE_USED_IN_SCORE = 0
SEALED_SOURCE_VIOLATIONS = 0
```
