# KW-002 — семантическое ядро и структура сайта с нуля под современный Яндекс

Status: **ACTIVE / OWNER-APPROVED DATA-VOLUME METHODOLOGY REVISION 2026-09-10**  
Owner decision: 2026-09-08; volume-pipeline revision: 2026-09-10

Working client-facing title:

`Соберу с нуля семантическое ядро и структуру сайта под современный Яндекс — обычная выдача + Алиса AI`

## 1. Что продаёт KW-002

KW-002 не пересобирает существующее ядро и не начинается с готовой структуры сайта.

Продукт должен уметь получить минимальный бриф нового клиента и пройти полный путь:

```text
бизнес + ассортимент + регион + коммерческая цель + купленный объём результата
→ первичная карта тем
→ Wordstat RAW
→ RAW normalization / exact+safe implicit deduplication
→ high-confidence sanitation / stop-topics / obvious foreign meanings
→ компактный sanitized candidate pool
→ first family triage
→ targeted expansion + немедленная повторная sanitation
→ реальные поисковые конкуренты Яндекса
→ конкурентное семантическое расширение
→ второй Wordstat + немедленная повторная sanitation
→ candidate semantic master + valid reserve
→ nuanced relevance / intent / user-job review
→ delivery-scope selection под купленный лимит
→ текущая органическая выдача Яндекса только для выбранного набора
→ кластеризация по пользовательской задаче + интенту + SERP-сходству
→ Search-only query→page map и архитектура сайта
→ выбор контрольных AI-search кейсов
→ evidence из генеративной выдачи/ответов Яндекса
→ Search-vs-AI reconciliation
→ финальное ядро в пределах купленного объёма
→ распределение по страницам
→ IA / Page Jobs / внутренняя связность
→ клиентские артефакты
→ QA / revision rehearsal / productization measurement
```

Ключевая формулировка:

```text
AI-SEARCH EVIDENCE != "СПРОСИТЬ АЛИСУ, КАК ДЕЛАТЬ SEO"
```

Мы исследуем, как современный Яндекс понимает пользовательские задачи в обычной органической выдаче и в генеративных ответах Алисы AI, какие типы страниц и источников используются и меняет ли это решение о кластере, странице или её Page Job.

## 2. RAW-объём и клиентский объём — разные сущности

KW-002 больше не трактует весь provider output как рабочее/клиентское ядро.

```text
RAW_OCCURRENCE_POOL = полный lossless provider evidence; может быть десятки тысяч строк
NORMALIZED_UNIQUE_POOL = уникальные аналитические фразы со всей lineage
SANITIZED_CANDIDATE_POOL = кандидаты после ранней консервативной чистки
DELIVERY_SELECTED_SET = фразы, выбранные под купленный объём
VALID_RESERVE_SET = валидные фразы вне купленного лимита
FINAL_DELIVERED_CORE <= DELIVERY_KEYWORD_CAP
```

Подробное обязательное правило:

`LEVEL1/DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md`

### Коммерческий лимит

Каждый заказ на Step00 фиксирует `DELIVERY_KEYWORD_CAP`.

Технические/provider batch limits и объём RAW не являются клиентским лимитом.

Текущая productization safety policy:

```text
STANDARD_KWORK_DELIVERY_CEILING = 1500 final phrases
>1500 = только отдельный custom/owner-approved scope
```

`до N фраз` — это максимум результата, а не обещание искусственно добить файл мусором до N.

Платное `+N` расширяет **объём очищенного deliverable**: сначала используются следующие валидные фразы из `VALID_RESERVE_SET` по coverage-aware priority; дополнительный provider acquisition нужен только если reserve реально недостаточен для купленного расширения.

### Отбор не равен сортировке по частоте

Приоритет учитывает:

```text
business/assortment fit
coverage важных товарных/сервисных направлений
intent / user job / ambiguity
Yandex demand/frequency
clicks where available
competition/rankability where available
redundancy / canonicality
cluster/topic representativeness
incremental coverage value
```

Высокая частота сама по себе не делает запрос релевантным; низкая частота сама по себе не удаляет бизнес-поддержанный запрос.

## 3. Документационная архитектура

Структура KW-002 жёстко трёхчастная:

```text
LEVEL 1 — общие правила всего кворка
LEVEL 2 — правила и методика конкретных шагов
work/<JOB_ID>/ — данные, evidence, статус и артефакты конкретного заказа
```

### LEVEL 1

`LEVEL1/`

Содержит только универсальные правила:

- продукт и границы обещания;
- минимальный клиентский intake;
- правила evidence/source/Bridge;
- аналитическая дисциплина;
- разделение RAW / normalized / sanitized / delivery / reserve;
- ранняя sanitation и коммерческий delivery cap;
- правило ChatGPT Work для больших данных;
- жизненный цикл заказа;
- правила клиентских артефактов и QA;
- правила отделения универсальной методики от конкретного заказа.

### LEVEL 2

`LEVEL2/`

Содержит универсальные шаги выполнения KW-002:

- зачем нужен шаг;
- какие входы допустимы;
- какой data layer шаг читает и создаёт;
- какой метод используем;
- какие автоматические/машинные фильтры обязательны;
- какие правила перенесены/адаптированы из KW-001;
- какие внешние источники поддерживают метод;
- что создаём;
- что считается PASS/FAIL/HOLD;
- какие данные передаются следующему шагу.

### work/<JOB_ID>/

Только конкретный заказ:

- frozen brief;
- client facts;
- purchased `DELIVERY_KEYWORD_CAP`;
- allowed inputs;
- запрещённые prior-research sources;
- текущие seed/query/page IDs;
- provider evidence;
- raw/normalized/sanitized/reserve/delivery tables;
- Work handoffs;
- текущие решения;
- final deliverables;
- revision/productization measurement.

Конкретные данные заказа не являются Level 1 или Level 2 методикой.

## 4. Первый тестовый заказ

```text
JOB_ID = BLOOD_SAND_GREENFIELD_2026-09-08
BUSINESS = Blood & Sand
MODE = CLEAN GREENFIELD REHEARSAL
PRIOR BLOOD_SAND SEO/ALICE/COMPETITOR RESEARCH = SEALED
```

На вход разрешается только минимальная информация, которую мог бы передать обычный новый заказчик, плюс raw/current assortment facts.

Старые Wordstat, Search, Alice, opportunity-map, competitor conclusions, clusters and page decisions Blood & Sand запрещены как вход до финальной заморозки результата KW-002.

После финальной заморозки старое исследование открывается только для отдельного demo/regression comparison, чтобы измерить, что KW-002 самостоятельно воспроизвёл, пропустил или улучшил.

После owner-approved volume-method revision текущий Blood & Sand job обязан мигрировать через новые Step03A/03B gates до возобновления Step05. Уже собранный RAW не уничтожается и не запрашивается заново только из-за изменения pipeline.

## 5. Основные внешние методические опоры

Official Yandex:

- https://yandex.ru/support2/wordstat/ru/
- https://yandex.ru/support2/wordstat/ru/content/operators
- https://yandex.ru/support/webmaster/ru/service/queries-selection
- https://yandex.ru/support/webmaster/ru/epos
- https://yandex.ru/support/webmaster/ru/recommendations/site-structure
- https://yandex.ru/support/webmaster/ru/alice
- https://yandex.ru/support/webmaster/ru/service/alice-answers

Cleaning / large semantic sets:

- https://journal.topvisor.com/ru/seo-kitchen/how-to-understand-from-which-requests-clean-the-core/
- https://topvisor.com/ru/support/implicit-duplicates/
- https://www.key-collector.ru/docs/tools/implicit-duplicates/

Industry corroboration for intent / prioritization / clustering:

- https://ahrefs.com/blog/keyword-intent/
- https://ahrefs.com/blog/keyword-strategy/
- https://ahrefs.com/blog/keyword-analysis-for-seo/
- https://ahrefs.com/blog/keyword-clustering/
- https://www.semrush.com/blog/keyword-clustering/

These sources do not replace project evidence. They support the method; current Yandex demand/SERP evidence and client business scope decide the current order.

## 6. Execution authority

Before each major step:

```text
READ LEVEL1
→ READ current LEVEL2 step
→ READ current work/<JOB_ID>/ state/evidence
→ confirm current data layer and row counts
→ review current external methodology where the step requires it
→ explain why/how/result to owner in plain language
→ obtain authorization when required
→ execute
→ persist complete result
→ read back / QA
→ update job flow
```

### Large-data execution rule

Never hand an LLM a complete multi-megabyte RAW occurrence ledger merely because it exists.

```text
RAW -> machine evidence / audit
normalized + sanitized candidates -> analyst/LLM semantic work
delivery-selected set -> expensive Search/SERP/clustering
```

Any step that increases acquisition volume must immediately pass new evidence through the same normalization/sanitation gate before union with the working candidate set.
