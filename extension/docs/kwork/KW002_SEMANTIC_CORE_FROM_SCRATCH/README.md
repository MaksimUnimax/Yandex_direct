# KW-002 — семантическое ядро и структура сайта с нуля под современный Яндекс

Status: **ACTIVE / PRODUCTIZATION REHEARSAL PREPARATION**  
Owner decision: 2026-09-08

Working client-facing title:

`Соберу с нуля семантическое ядро и структуру сайта под современный Яндекс — обычная выдача + Алиса AI`

## 1. Что продаёт KW-002

KW-002 не пересобирает существующее ядро и не начинается с готовой структуры сайта.

Продукт должен уметь получить минимальный бриф нового клиента и пройти полный путь:

```text
бизнес + ассортимент + регион + коммерческая цель
→ первичная карта тем
→ Wordstat
→ очистка / расширение
→ реальные поисковые конкуренты Яндекса
→ конкурентное семантическое расширение
→ второй Wordstat
→ полный кандидатный semantic master
→ текущая органическая выдача Яндекса
→ кластеризация по пользовательской задаче + интенту + SERP-сходству
→ Search-only query→page map и архитектура сайта
→ выбор контрольных AI-search кейсов
→ evidence из генеративной выдачи/ответов Яндекса
→ Search-vs-AI reconciliation
→ финальное ядро
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

## 2. Нет универсального лимита числа запросов

KW-002 не имеет постоянного методического ограничения `500 запросов`.

```text
RAW CANDIDATES = столько, сколько объективно даёт исследование в согласованной нише/границах заказа
FINAL RETAINED CORE = столько, сколько прошло доказательную очистку и входит в зафиксированный коммерческий scope заказа
BRIDGE BATCH LIMIT = только технический размер одного batch/job, не лимит продукта
```

При необходимости большие наборы обрабатываются несколькими provider jobs и/или через ChatGPT Work по отдельному Level-1 правилу.

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
- правило ChatGPT Work для больших данных;
- жизненный цикл заказа;
- правила клиентских артефактов и QA;
- правила отделения универсальной методики от конкретного заказа.

### LEVEL 2

`LEVEL2/`

Содержит универсальные шаги выполнения KW-002:

- зачем нужен шаг;
- какие входы допустимы;
- какой метод используем;
- какие правила перенесены/адаптированы из KW-001;
- какие внешние источники поддерживают метод;
- что создаём;
- что считается PASS/FAIL/HOLD;
- какие данные передаются следующему шагу.

### work/<JOB_ID>/

Только конкретный заказ:

- frozen brief;
- client facts;
- allowed inputs;
- запрещённые prior-research sources;
- текущие seed/query/page IDs;
- provider evidence;
- raw/cleaned tables;
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

## 5. Основные внешние методические опоры

Official Yandex:

- https://yandex.ru/support2/wordstat/ru/
- https://yandex.ru/support2/wordstat/ru/content/operators
- https://yandex.ru/support/webmaster/ru/epos
- https://yandex.ru/support/webmaster/ru/recommendations/site-structure
- https://yandex.ru/support/webmaster/ru/alice
- https://yandex.ru/support/webmaster/ru/service/alice-answers

Industry corroboration for clustering:

- https://ahrefs.com/blog/keyword-clustering/
- https://www.semrush.com/blog/keyword-clustering/

These sources do not replace project evidence. They support the method; current Yandex demand/SERP evidence decides the current order.

## 6. Execution authority

Before each major step:

```text
READ LEVEL1
→ READ current LEVEL2 step
→ READ current work/<JOB_ID>/ state/evidence
→ review current external methodology where the step requires it
→ explain why/how/result to owner in plain language
→ obtain authorization when required
→ execute
→ persist complete result
→ read back / QA
→ update job flow
```

Do not start Step 0 until the owner accepts the prepared KW-002 roadmap and documentation scaffold.
