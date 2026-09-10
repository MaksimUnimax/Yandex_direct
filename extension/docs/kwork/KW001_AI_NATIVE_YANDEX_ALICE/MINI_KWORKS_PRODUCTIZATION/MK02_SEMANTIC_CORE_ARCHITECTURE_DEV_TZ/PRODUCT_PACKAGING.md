# MK02 — PRODUCT PACKAGING

Status: **PHASE 6 OWNER-ACCEPTED PHYSICAL PACKAGE / PHASE 7 QA NEXT**

Рабочее название продукта:

**«Семантическое ядро + SEO-структура сайта + ТЗ на доработку»**

## 1. Решение Phase 6

После OKNO_MSK MK02-only rehearsal клиентский пакет MK02 фиксируется как **три физических файла + короткое сообщение при передаче**:

1. **XLSX — рабочая книга исследования и внедрения**.
2. **PDF — аналитический отчёт «Что показало исследование спроса и структуры»**.
3. **PDF — action-first документ «ТЗ на доработку сайта»**.
4. **Короткое сообщение в Kwork/чате** — перечисляет вложения и порядок работы; отдельным TXT-файлом не создаётся.

Canonical package formula:

```text
XLSX WORKING AUTHORITY
+ ANALYTICAL PDF
+ IMPLEMENTATION-TZ PDF
+ SHORT HANDOFF MESSAGE
```

Это решение относится к физическому пакету. Логические требования из `DELIVERABLE_SPEC.md` остаются обязательными независимо от формата.

## 2. Почему аналитический отчёт и ТЗ не объединяются

Phase-5 rehearsal создал два самостоятельных recipient tasks:

```text
OWNER / MANAGER TASK
= понять, что исследование показало и почему приняты архитектурные решения

IMPLEMENTER TASK
= понять, что именно менять, где, почему, что нельзя ломать и как принять результат
```

Объединение этих задач в один универсальный документ создаёт повторяемый риск:

- аналитическая часть превращается в длинный execution protocol;
- action-first часть теряется внутри объяснения исследования;
- получателю приходится искать готовые действия среди summary/limitations;
- либо, наоборот, управленческая логика исчезает ради компактного списка задач.

Поэтому:

```text
ANALYTICAL PDF != IMPLEMENTATION-TZ PDF
```

Оба документа должны быть self-contained в своей роли и не требовать знания внутреннего репозитория.

## 3. Роль XLSX

`XLSX = основной рабочий источник для фильтрации, детализации и передачи между специалистами.`

Phase-5 rehearsal подтвердил один workbook как удобный container для связанных клиентских views. В OKNO_MSK кандидат содержит 13 листов; точное число листов не является универсальным коммерческим лимитом, если логические views сохранены.

В workbook должны оставаться доступными как минимум:

- как пользоваться результатом;
- главные выводы;
- полное row accounting семантики;
- рабочие запросы и группы;
- карта phrase/task → page;
- current/target architecture views;
- current→target delta;
- ТЗ/implementation work packages;
- clarifications / recheck / HOLD;
- page relationships;
- acceptance/verification information.

Рабочая книга не должна заставлять клиента вручную соединять внутренние TSV/JSON или знать repository IDs.

## 4. Роль аналитического PDF

`ANALYTICAL PDF = управленческое объяснение результата.`

Он должен отвечать прежде всего на вопрос:

> **Что исследование показало о спросе, текущих владельцах страниц, целевой поисковой архитектуре и необходимости/отсутствии изменений?**

Обязательные классы содержания, когда они подтверждены текущим заказом:

- scope и Yandex-only boundary;
- размер и состав принятой/спорной/исключённой семантики;
- материальные user-task / cluster findings;
- page-ownership coverage;
- отличия exact owner / family owner / support page;
- текущая и целевая Search architecture;
- material current→target deltas;
- KEEP / NO_CHANGE findings;
- что действительно требует изменения сайта;
- что остаётся unresolved и почему;
- ограничения evidence и claim boundaries.

Permanent rule:

```text
CLIENT ANALYTICAL REPORT != EXECUTION PROTOCOL
CORRECT COUNTS + CLEAN LAYOUT != ANALYTICAL VALUE
```

История provider-вызовов, git commits, QA chronology и внутренние Stage/Step IDs не являются клиентским повествованием.

## 5. Роль PDF «ТЗ на доработку сайта»

`IMPLEMENTATION-TZ PDF = action-first инструкция по evidence-resolved действиям.`

Документ открывается готовыми к выполнению действиями, а затем отдельно показывает pending/clarification/recheck/no-change состояния.

Для каждого READY действия, где применимо, клиент должен видеть:

```text
Страница / объект
Зачем менять
Что сделать
Где именно
Порядок / способ внедрения
Что сохранить / не сломать
Какие зависимости или ограничения действуют
Как проверить результат
```

Для неготового действия должно быть понятно:

```text
что уже доказано
что именно ещё неизвестно
как получить недостающий ответ
какое решение станет возможным после ответа
```

Запрещено превращать semantic mapping или отсутствие точного владельца в автоматически готовое физическое изменение.

## 6. Почему DOCX не входит в базовую поставку V1

DOCX не является обязательным четвёртым клиентским файлом в base MK02 V1.

Причины:

- редактируемая рабочая детализация уже существует в XLSX;
- одновременная поставка PDF + DOCX одной и той же инструкции создаёт две клиентские версии одного содержания;
- release/readback и recipient QA должны проверять один канонический экземпляр каждого документа;
- PDF лучше фиксирует принятую версию ТЗ для передачи и приёмки.

Если конкретному клиенту понадобится редактируемая текстовая копия ТЗ, её можно подготовить отдельно из того же accepted source, но это **не базовое обещание MK02 V1** и не должно создавать самостоятельную расходящуюся authority.

Внутренний DOCX, если используется в materialization pipeline, является source/intermediate artifact, а не обязательным client attachment.

## 7. Имена клиентских файлов

Базовый naming pattern:

```text
SEMANTIC_CORE_AND_SEO_STRUCTURE_<CLIENT_OR_DOMAIN>_<YYYY-MM-DD>.xlsx
RESEARCH_AND_ARCHITECTURE_REPORT_<CLIENT_OR_DOMAIN>_<YYYY-MM-DD>.pdf
SITE_IMPROVEMENT_TZ_<CLIENT_OR_DOMAIN>_<YYYY-MM-DD>.pdf
```

Внутренний идентификатор MK02, Stage/Step ID и test-case ID не обязаны попадать в клиентские имена.

## 8. Что клиенту автоматически не отправляется

Не входят в обычную клиентскую поставку:

- внутренние TSV / TSV.GZ authorities;
- JSON manifests и build receipts;
- machine-QA outputs;
- source-code generators/validators;
- git/readback receipts;
- внутренние traceability ledgers;
- repository-only Markdown;
- raw provider chronology.

Эти материалы сохраняются как evidence/audit layer и используются для QA, но не подменяют client-facing package.

## 9. Обязательная Yandex-only граница

Во всех трёх физических файлах должно быть явно понятно, что базовая работа MK02 относится к экосистеме Яндекса.

Base MK02 не включает:

- Google Search / Search Console / Keyword Planner / Google SEO;
- competitor-derived Step5A semantic expansion;
- Alice / Yandex Neuro / GenSearch / AEO;
- website implementation itself;
- отдельный полный technical SEO audit;
- гарантии роста позиций, трафика, лидов или выручки;
- самостоятельный historical harmful-cannibalization audit;
- выдуманный production schedule.

## 10. Page-count и file-count boundaries

Количество страниц PDF **не является критерием качества**.

Количество листов XLSX **не является самоцелью**.

Физический пакет из трёх файлов фиксируется потому, что rehearsal показал три разные задачи клиента, а не потому, что у продукта должен быть заранее заданный file count.

Если будущая версия продукта докажет другой recipient need, package меняется только через versioned productization review, а не случайно внутри одного заказа.

## 11. Phase-5 evidence, повлиявший на решение

OKNO_MSK rehearsal подтвердил:

```text
SEMANTIC UNIVERSE = 2840
WORKING / REVIEW / EXCLUDED = 2185 / 187 / 468
ACTIVE PHRASE→PAGE MAP = 2185
ACTIVE TARGET UNITS = 160
IMPLEMENTATION PACKAGES = 47
READY / PENDING BUSINESS / PENDING PLACEMENT / RECHECK / MAPPING / NO CHANGE / HOLD
= 3 / 1 / 10 / 4 / 19 / 9 / 1
```

Такой объём одновременно требует:

- фильтруемого XLSX для деталей;
- отдельной аналитической выжимки для владельца/руководителя;
- отдельного action-first документа для внедрения.

Эти числа являются evidence конкретного rehearsal и **не становятся коммерческими лимитами**. Limits и price определяются только на Phase 8.

## 12. Phase 7 — что ещё должно быть доказано

Phase 6 фиксирует **package design**, но ещё не заменяет последующий product/recipient QA.

До Phase-7 PASS нужно на OKNO_MSK materialize и проверить финальную форму пакета:

1. XLSX как клиентский рабочий файл.
2. Аналитический PDF из accepted analytical source.
3. Implementation-TZ PDF из accepted action-first source.
4. Короткое handoff message из `CLIENT_HANDOFF_TEMPLATE.md`.

Phase 7 обязан проверить:

- source→file consistency;
- полный row/count reconciliation;
- отсутствие stale 7-READY состояния;
- client-language cleanliness;
- отсутствие internal-ID leakage;
- physical rendering обоих PDF;
- usability XLSX;
- точность hyperlinks/URLs;
- самостоятельную recipient usefulness каждого документа;
- Yandex-only scope во всех client files;
- remote persistence/readback.

## 13. Phase-6 Definition of Done

```text
PHASE-5 REHEARSAL READ / ACCEPTED AS INPUT
+ CANDIDATE XLSX REVIEWED
+ ANALYTICAL VIEW REVIEWED
+ ACTION-FIRST VIEW REVIEWED
+ COMBINED-DOCUMENT OPTION REJECTED WITH REASON
+ XLSX + TWO-PDF SPLIT FROZEN
+ DOCX BASE PROMISE = NO
+ INTERNAL SIDECARS EXCLUDED FROM CLIENT PACKAGE
+ YANDEX-ONLY BOUNDARY PRESERVED
+ NO PAGE-COUNT QUALITY PROXY
+ NO PRICE/LIMITS INVENTED
+ NO CARD/VISUAL WORK STARTED
= PHASE 6 PASS
```

Next gate:

```text
PHASE 7 = PRODUCT / RECIPIENT QA OF THE FROZEN PHYSICAL PACKAGE
```
