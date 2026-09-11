# MK02 — PRODUCT PACKAGING

Status: **PHASE 7 MARKET-GRADE PACKAGE VALIDATED / PHASE 8 ECONOMICS NEXT**

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

## 12. Historical Phase 7 — initial validation result

Phase 7 materialized the frozen three-file package on OKNO_MSK and validated it as the real recipient delivery.

Final client artifacts:

```text
SEMANTIC_CORE_AND_SEO_STRUCTURE_OKNO_MSK_2026-09-10.xlsx
blob = b2ec26f1c932461e6a1a807e833d254225e62d65
sha256 = be1996ad6b356187de55afeabc57ba33fd3aa77b0be0850ebe9938638944040a

RESEARCH_AND_ARCHITECTURE_REPORT_OKNO_MSK_2026-09-10.pdf
blob = 149dfe55010e099d03d048f6686775ea74dd3edd
sha256 = 851463f469480a3a977eaa327fecc475644945df7cd1a8e6ba883ee33140b2b7

SITE_IMPROVEMENT_TZ_OKNO_MSK_2026-09-10.pdf
blob = 7aedd3d74cae8bed3ac2fe43aab5e716536d3d9d
sha256 = d12b0b3bd8d70c9aff5aea793d3a94b147be1555e547c03729e4e2caa5b7dfc1
```

Validated gates:

- semantic/ownership/action row accounting preserved;
- 47 work packages reconcile to `3 / 1 / 10 / 4 / 19 / 9 / 1`;
- final XLSX has 13 visible sheets, zero formula errors and zero forbidden client-token hits in visible/package XML layers;
- analytical PDF: 2/2 final pages visually inspected after the orphan-heading correction;
- implementation-TZ PDF: 2/2 final pages visually inspected;
- both PDFs parse and pass client-language scans;
- Yandex-only and uncertainty/readiness boundaries are preserved;
- provider calls in Phase 7 = 0;
- Phase-5 semantic/ownership/architecture/action authorities modified in Phase 7 = 0.

The client package design remains exactly the Phase-6 decision: one XLSX + two separate PDFs + a short handoff message.

## 13. Phase-7 Definition of Done

```text
FROZEN PHYSICAL PACKAGE MATERIALIZED
+ G13 CROSS-VIEW CONSISTENCY PASS
+ G14 CLIENT LANGUAGE / REPORT QUALITY PASS
+ G15 PHYSICAL / RECIPIENT / PERSISTENCE PASS
+ FINAL XLSX PACKAGE-LAYER SCAN PASS
+ BOTH FINAL PDF RENDERS REVIEWED
+ FINAL HASH IDENTITIES RECORDED
+ GENERATOR REGRESSION FIXED
+ PROVIDER CALLS = 0
= PHASE 7 PASS
```

Next gate:

```text
PHASE 8 = PRICE / LIMITS / ECONOMICS
```

## 14. Phase 7 market-grade corrective package — current delivery

The initial package and the first target-first package remain historical evidence. The current recipient delivery is the separately versioned directory:

`tests/OKNO_MSK/CLIENT_DELIVERY_PHASE_7_TARGET_FIRST_MARKET_GRADE_2026-09-10`

It contains exactly three files:

```text
SEMANTIC_CORE_AND_TARGET_SEO_STRUCTURE_OKNO_MSK_2026-09-10.xlsx
sha256 = d420309ac7de2df418ddfc5c7d51a0c8680a1d35ff7458359ad56da99e213551

TARGET_SEO_ARCHITECTURE_REPORT_OKNO_MSK_2026-09-10.pdf
sha256 = a21b24b40fca465510bf6735dce38292dfff3b95f4b1ec7deca1f819d4acb663

TARGET_PAGE_SPECIFICATION_TZ_OKNO_MSK_2026-09-10.pdf
sha256 = a8b185d568f9d83ef354842dbd070c06000e59944af67b5cef2fb6489b2f2b8a
```

Validated market-grade result:

- 2 840 source rows reconcile to 2 185 working, 187 review and 468 excluded;
- 2 185 phrase routes retain individual Wordstat evidence;
- 161 cluster/task routes resolve into 60 target roles and 60 full page specs;
- reconciliation remains 48 KEEP / 7 OPTIMIZE / 4 ROUTE / 1 RECHECK; physical delta remains 14; CREATE remains 0;
- XLSX has 13 usable sheets, final-byte package QA PASS and 13/13 visually inspected previews;
- analytical PDF has a scannable complete 60-role tree and 24/24 inspected final-byte renders;
- TZ PDF keeps the complete 60-role compact register and uses 12 selective detail cards, with 28/28 inspected final-byte renders;
- machine QA = 58/58 PASS; final-files-only recipient QA = 10/10 PASS;
- new provider calls = 0; no fake CREATE was introduced.

The permanent quality rule is semantic, not mechanical: no fixed workbook sheet count or PDF page count is a release authority.
