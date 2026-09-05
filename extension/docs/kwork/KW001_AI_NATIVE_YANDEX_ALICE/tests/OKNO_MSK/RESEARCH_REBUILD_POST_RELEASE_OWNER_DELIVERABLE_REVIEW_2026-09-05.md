# OKNO_MSK — post-release owner deliverable review

Дата открытия: 2026-09-05  
Статус: **IN_PROGRESS / OWNER_REVIEW_REWORK_REQUIRED**  
Класс работы: **POST_RELEASE_OWNER_DELIVERABLE_REVIEW / NOT A NEW ROADMAP STAGE**  
Исходный release: `OKNO_MSK_RESEARCH_RELEASE_2026-09-05`  
Исходный release authority: Stage 0–15 completed; этот review не стирает исторический release PASS, но **перекрывает утверждение о финальной recipient acceptance до закрытия выявленных дефектов**.

## 1. Зачем открыт review

После завершения Stage 0–15 владелец начал проверять сами конечные recipient-specific артефакты, а не только QA-отчеты об их наличии и согласованности. Проверка показала новый класс дефекта: глубокая аналитика и корректная каноническая база могут существовать, но конкретный файл для конкретного получателя все равно может быть слишком сжатым, слишком внутренним, недостаточно исполнимым или неправильно материализованным для своего назначения.

Новая обязательная граница:

```text
PACKAGE-WIDE TRUTH EXISTS
!= EACH PROMISED RECIPIENT ARTIFACT IS COMPLETE FOR ITS OWN PURPOSE

CORRECT DATABASE
!= CLIENT-USABLE WORKBOOK

MACHINE-READABLE
!= AI-CONSULTANT-USABLE

INTERNAL QA PASS
!= OWNER / COMMISSIONER ACCEPTANCE
```

Исторические Stage 0–15 артефакты сохраняются как provenance. В диагностическом review сначала фиксируется полный defect set по каждому финальному deliverable, затем выполняется единый correction/materialization pass и повторная recipient-specific QA.

Нумерация в этом review всегда совпадает с физической нумерацией release-файлов. Отдельная скрытая очередь `Reviewed artifact 01/02/03` запрещена, потому что она ранее привела к тому, что workbook №04 был назван «artifact 03» и смешан с реальным release file №03.

## 2. Release file 01 — клиентский исследовательский отчет

Источник: `OKNO_MSK_RESEARCH_RELEASE_2026-09-05/sources/OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.md`.

### Что сделано правильно

- нормальный русский язык вместо служебной выгрузки;
- ранний главный вывод;
- показаны положительные `retain / no-change` результаты;
- названы конкретные страницы и основные изменения;
- ordinary Search и AI разделены;
- AI не представлен как магическое доказательство или количество вызовов;
- неопределенность не скрыта;
- запрещенные сильные claims сохранены.

### CR-01 — полноценное исследование снова сжато до executive-summary уровня

**Ошибка:** глубокая Stage-8 truth layer существует, но клиентский отчет в основном показывает краткие итоги и ограниченный список приоритетных рекомендаций. Он не материализует обещанную исследовательскую цепочку по существенным выводам.

**Почему это проблема:** первоначальная причина rebuild — клиент не должен реконструировать исследование из внутренних файлов. Наличие master report где-то в package не заменяет полноту самого обещанного клиентского research report.

**Как исправить:** расширить клиентский report из текущего master authority. Для каждого материального finding или группы однотипных findings показывать эквивалентную цепочку:

```text
ЧТО ПРОВЕРЯЛИ
-> ЧТО ЕСТЬ СЕЙЧАС
-> ДОКАЗАТЕЛЬСТВО
-> ЧТО ЭТО ЗНАЧИТ
-> ЧТО ПРАВИЛЬНО / НЕПРАВИЛЬНО
-> КАК ДОЛЖНО БЫТЬ
-> ЧТО ИМЕННО И ГДЕ МЕНЯТЬ
-> КЛЮЧЕВЫЕ ЗАПРОСЫ / ТЕМЫ / ВОПРОСЫ
-> ПРИМЕР, ЕСЛИ ОН ОБОСНОВАН
-> ЧТО НЕ МЕНЯТЬ
-> ОГРАНИЧЕНИЕ / НЕОПРЕДЕЛЕННОСТЬ
```

### CR-02 — ordinary Search показан почти только агрегированными выводами

**Ошибка:** клиент видит несколько общих тезисов, тогда как accepted evidence содержит отдельные material Search cases.

**Как исправить:** добавить client-readable Search case layer: запрос/семейство, что наблюдалось, какой тип задачи/страницы подтвержден, какое решение из этого следует и какая граница переноса доказательства.

**Non-repeat:** `SEARCH EVIDENCE PRESENT IN INTERNAL LEDGER != SEARCH RESEARCH VISIBLE TO CLIENT`.

### CR-03 — AI causal work снова чрезмерно агрегирован

**Ошибка:** сводные verdict counts видимы, но полный смысл отдельных AI cases почти не показан в клиентском report.

**Как исправить:** для каждого material AI case дать компактную карточку:

```text
ПОЧЕМУ ВЫБРАЛИ
-> РЕШЕНИЕ ДО AI
-> ЧТО ПОКАЗАЛ AI
-> ЧТО ИЗМЕНИЛОСЬ / ПОДТВЕРДИЛОСЬ / ОСТАЛОСЬ НЕДОСТАТОЧНЫМ
-> КАКОЕ ДЕЙСТВИЕ ИЛИ NO-ACTION СЛЕДУЕТ
-> ОГРАНИЧЕНИЕ
```

**Non-repeat:** `AI CAUSAL LEDGER COMPLETE != AI VALUE CLIENT-VISIBLE`.

### CR-04 — полная карта решений схлопнута в небольшой список приоритетов

**Ошибка:** полный action universe существует, но обычный клиент не получает компактной полной карты `retain / reroute / improve / no-new-page / recheck / hold`.

**Как исправить:** добавить сводную карту всех материальных решений по страницам/темам с человекочитаемым статусом и ссылкой на подробное SEO-ТЗ.

### CR-05 — uncertainty показана числами, но недостаточно объяснена тематически

**Ошибка:** counts честно сохранены, но клиенту трудно понять, какие классы тем туда попали, почему они не закрыты и влияет ли это на готовые рекомендации.

**Как исправить:** сгруппировать uncertainty по причинам/темам/влиянию и дать правило, когда каждый класс надо переоткрыть.

### CR-06 — package-level completeness ошибочно использована как доказательство client-report completeness

**Root cause:** QA проверила, что нужное знание существует где-то в согласованном package, но не проверила, что конкретный promised recipient artifact сам выполняет свой контракт.

**Correct rule:** `EVIDENCE EXISTS SOMEWHERE IN PACKAGE != PROMISED CLIENT REPORT COMPLETE`.

## 3. Release file 02 — SEO implementation guide

Источник: `OKNO_MSK_RESEARCH_RELEASE_2026-09-05/sources/OKNO_MSK_SEO_IMPLEMENTATION_GUIDE_RU_2026-09-05.md`.

### Что сделано правильно

Контентные action cards в значительной части реально содержат `AS-IS`, evidence, `TO-BE`, точное логическое место, темы, фразы, вопросы, implementation example, acceptance и do-not-do boundary. `NOT_READY`/`HOLD` не были искусственно превращены в готовые задания. Список внутренних ссылок и routing map также материализованы.

### SG-01 — русскоязычный specialist artifact содержит большой объем англоязычной внутренней прозы

**Ошибка:** поля `AS-IS`, `WHY`, `TO-BE`, internal relationships и do-not-do в routing/action rows часто остаются английскими служебными формулировками.

**Как исправить:** весь объясняющий и исполнимый текст recipient-facing SEO guide должен быть на требуемом языке. Латиница/английский допускаются для URL, ID, стандартных технических токенов и неизменяемых имен, но не вместо объяснения действия.

**Non-repeat:** `SOURCE LANGUAGE MAY BE INTERNAL != RECIPIENT INSTRUCTION LANGUAGE`.

### SG-02 — routing/ownership action ошибочно считается готовым website implementation ticket

**Ошибка:** аналитически правильный owner/routing row часто содержит шаблонное `семантическое владение, хлебные крошки и контекстные ссылки`, не указывая, требуется ли вообще изменение реального сайта и какое именно.

**Как исправить:** каждому READY work package присвоить явный `IMPLEMENTATION_MODE`, например эквивалент:

```text
SEMANTIC_MAPPING_ONLY
CONTEXTUAL_LINK
NAVIGATION_CHANGE
CONTENT_BLOCK
METADATA_OR_LABEL_CHANGE
NO_SITE_CHANGE
RECHECK_ONLY
HOLD
```

Для каждого mode обязательны свои точные поля. Аналитическое переназначение владельца не должно автоматически превращаться в правку breadcrumbs/контента/навигации.

### SG-03 — link specification недостаточно точна для непосредственного внедрения

**Ошибка:** `source -> target -> meaning` полезно, но исполнитель все еще выбирает место и формулировку сам.

**Как исправить:** для READY link-task материализовать:

```text
SOURCE_PAGE
SOURCE_BLOCK_OR_LOCATION
TARGET_PAGE
RECOMMENDED_ANCHOR_OR_ANCHOR_INTENT
SURROUNDING_CONTEXT / SENTENCE INTENT
WHY_THIS_PLACEMENT
ACCEPTANCE_CHECK
```

Если placement не доказан, задача остается `PENDING_DETAIL`, а не `READY_LINK`.

### SG-04 — routing map не определяет, что именно должен сделать исполнитель

**Ошибка:** `primary page + support pages` — хорошая архитектурная карта, но инструкция уровня «отразить задачу либо дать переход» оставляет исполнительское решение неразрешенным.

**Как исправить:** для каждой routing row отдельно зафиксировать `implementation_mode`, real-site change yes/no, target block/link/navigation location и acceptance.

### SG-05 — technical source locator подменяет объяснение evidence

**Ошибка:** поле «Доказательство» часто содержит только имя внутреннего TSV/ledger.

**Как исправить:** recipient-facing spec должен содержать две части:

```text
EVIDENCE_MEANING = коротко, какой наблюдаемый факт поддерживает решение
EVIDENCE_LOCATOR = технический источник для трассировки
```

Файл/ID — это locator, а не объяснение доказательства.

### SG-06 — полнота карточки проверялась по наличию полей, а не по фактической исполнимости каждого типа action

**Root cause:** единый шаблон action-card был применен к разным типам работы; для content actions он часто достаточен, для routing/link/ownership — нет.

**Correct rule:** `FIELDS PRESENT != EXECUTION DECISION RESOLVED`.

## 4. Release file 03 — AI SEO-консультант по конкретному сайту

Исторический release artifact: `OKNO_MSK_RESEARCH_RELEASE_2026-09-05/03_OKNO_MSK_AI_KNOWLEDGE_DOCUMENT_2026-09-05.json`.

Обязательное исходное owner authority: `RESEARCH_REPORT_REBUILD_OWNER_CLARIFICATION_AI_IMPLEMENTATION_PATH_2026-09-04.md`.

Stage-1 acceptance authority: `RESEARCH_REBUILD_STAGE_01_PRODUCT_PROMISE_AND_ACCEPTANCE_MATRIX_2026-09-04.md`.

Current correction authority: `RESEARCH_REBUILD_POST_RELEASE_AI_KNOWLEDGE_RECIPIENT_CONTRACT_CORRECTION_2026-09-05.md`.

### Для чего файл №03 нужен на самом деле

В owner clarification назначение зафиксировано однозначно: №03 нельзя трактовать только как архив знаний, контекст для продолжения проекта другой AI-системой или внутренний перенос состояния между диалогами.

№03 — самостоятельный клиентский путь **внедрения тех же подтвержденных работ по сайту**, которые в варианте №02 выполняет человек — SEO-специалист.

Правильная модель:

```text
№02
= ЧЕЛОВЕК-SEO-СПЕЦИАЛИСТ ВЫПОЛНЯЕТ ПОДТВЕРЖДЕННЫЕ РАБОТЫ

№03
= AI СТАНОВИТСЯ ПЕРСОНАЛЬНЫМ SEO-КОНСУЛЬТАНТОМ ПО ЭТОМУ САЙТУ
-> ЗАКАЗЧИК ЗАДАЕТ ОБЫЧНЫЕ ВОПРОСЫ
-> AI ОБЪЯСНЯЕТ ЧТО / ПОЧЕМУ / КАК / КАК ПРОВЕРИТЬ
-> ЗАКАЗЧИК САМОСТОЯТЕЛЬНО ВНОСИТ ИЗМЕНЕНИЯ
```

Заказчик не обязан разбираться в SEO. AI должен переводить полную профессиональную логику исследования в понятные пошаговые инструкции.

### Что означает «я уже выполнил часть работ — что делать дальше»

Это вопрос о **прогрессе заказчика по внедрению подтвержденных изменений на сайте**.

Он не имеет отношения к Stage/Step, `EXECUTION_CURSOR`, post-release review или продолжению внутреннего исследовательского roadmap.

```text
CLIENT SITE IMPLEMENTATION PROGRESS
!= INTERNAL RESEARCH ROADMAP CHECKPOINT
```

### Что сделано правильно исторической Stage-11 materialization

- полный semantic master был сохранен в data layer;
- 168 canonical units и 34 actions были включены;
- Search/AI evidence, Search-case explanations, links, routes, page validations и uncertainty были включены;
- current-vs-historical authority boundary была явно задана;
- запрет на превращение uncertainty в решение был сохранен;
- exact-query Search evidence не разрешалось автоматически переносить на всё семейство;
- AI verdict не приравнивался к decision value без delta.

То есть Stage 11 сохранил значительный объем правильной research truth. Дефект не доказывает потерю canonical data; он относится к recipient function, primary format, practical implementation usability и QA.

### AI-01 — финальная materialization/packaging не доказывает owner-defined функцию «персональный SEO-консультант»

**Ошибка:** наличие self-contained data bundle и interpretation rules не доказывает, что заказчик без SEO-знаний может загрузить №03, задать обычный вопрос и получить практическое объяснение и пошаговую инструкцию по внедрению.

**Как исправить:** corrected №03 должен прямо строиться как AI consultant knowledge/instruction document и проходить practical client-question QA.

### AI-02 — JSON выбран как основной AI artifact без доказанного recipient-format основания

Roadmap разрешал машинно-ориентированную структуру и технические идентификаторы, если они повышают точность, но требовал сохранить человекочитаемый смысл. Требования «основной файл обязательно JSON» в owner contract нет.

**Как исправить:** corrected primary №03 материализовать как self-contained LLM-readable Markdown (`.md`). JSON может оставаться companion data annex для row-level completeness.

```text
MACHINE-READABLE != AI-CONSULTANT-USABLE
```

### AI-03 — полная research logic должна обслуживать практическое внедрение, а не только справочный поиск по данным

№03 нельзя сводить ни к списку команд, ни к data archive. Для material decisions AI должен иметь цепочку current state → evidence → interpretation → decision → why → target state → exact action → dependencies/do-not-break → acceptance → limitation.

Иначе AI не сможет корректно отвечать на незаранее перечисленные вопросы заказчика.

### AI-04 — не доказано равенство практического workset между №02 и №03

Owner authority требует, чтобы оба пути реализовывали **одни и те же подтвержденные изменения**.

Stage-13 cross-view consistency проверил 26 material claims, но practical AI-consultant acceptance должна отдельно доказать:

```text
VARIANT_03_CONFIRMED_WORKSET
== VARIANT_02_CONFIRMED_WORKSET
```

AI не должен добавлять новые неподтвержденные работы только потому, что модель умеет генерировать SEO-идеи.

### AI-05 — Stage-11 QA проверял serialization/counts, а не практическую задачу заказчика

Исторический QA проверял `json_parse`, `self_contained` и counts. Это data-integrity QA, а не proof того, что локальная/new-context LLM умеет провести заказчика по внедрению.

**Correct rule:** `JSON_PARSE_PASS != AI-SEO-CONSULTANT PASS`.

### AI-06 — отсутствовал строгий offline practical walkthrough по owner questions

Owner clarification требует моделировать отдельную локальную LLM без интернета, live-site, Yandex, API, GitHub, предыдущего диалога и внутренних файлов; ей доступен только №03.

Нужно проверять вопросы типа:

- что на странице не так;
- что уже правильно и нельзя ломать;
- почему это проблема и чем подтверждено;
- как исправить пошагово;
- какие блоки/темы/запросы менять;
- как связать страницы;
- какое ТЗ дать разработчику/автору;
- как проверить результат;
- после выполненной части подтвержденных работ — какой шаг внедрения следующий;
- где данных недостаточно и категоричный ответ запрещен.

### AI-07 — внутренняя project-execution semantics должна быть явно отделена от клиентского внедрения

Чтобы не повторять текущую ошибку интерпретации, corrected contract фиксирует:

```text
AI CLIENT IMPLEMENTATION CONSULTANT
!= INTERNAL RESEARCH EXECUTION HANDOFF

AI KNOWLEDGE DOCUMENT
!= EXECUTION_CURSOR
```

№03 помогает заказчику реализовать подтвержденные изменения на **сайте**, а не продолжать наш repository roadmap.

### AI-08 — corrected physical №03 еще не материализован

На момент review физически существует исторический JSON. Corrected `.md` должен быть создан в едином correction/materialization pass, reconciled с №02 и проверен offline practical AI QA.

Исторический JSON и Stage-15 manifest сохраняются как provenance и не переписываются задним числом.

## 5. Release file 04 — rebuilt workbook

Artifact: `OKNO_MSK_RESEARCH_RELEASE_2026-09-05/04_OKNO_MSK_REBUILT_RESEARCH_WORKBOOK_2026-09-05.xlsx`.

Основания текущего review: Stage-12 materialization manifest/QA + канонические row-level source specifications, из которых workbook построен. Бинарный workbook не переписывается в этом диагностическом проходе.

### Что сделано правильно

- workbook построен из current semantic master и current action authority, а не из withdrawn historical workbook;
- correction/overlay precedence разрешен upstream и не реконструируется ad hoc;
- materialized full semantic core, units, actions, implementation, evidence, AI, links, routes и uncertainty;
- `NOT_READY/HOLD` сохранены;
- formula/source/count/readback QA прошли.

Это исправляет старый критический materialization defect.

### WB-01 — semantic correctness ошибочно приравнена к client workbook usability

**Ошибка класса QA:** Stage-12 PASS доказывает корректность authority, row counts, формул, render/openability и source reconciliation. Он не доказывает, что workbook является удобной самостоятельной decision surface для получателя.

**Correct rule:** `CORRECT DATABASE != CLIENT-USABLE WORKBOOK`.

### WB-02 — workbook front door остается слишком внутренне ориентированным

Материализация организована вокруг технических слоев `Semantic Master / Units / Actions / Implementation / Evidence / AI Cases / Links / Routes / Uncertainty`. Такие листы полезны как audit/detail layer, но для клиентского workbook требуется отдельная front-door decision surface, которая не заставляет получателя понимать внутреннюю архитектуру проекта.

**Как исправить:** сохранить полные authority sheets как detail/appendix, но добавить/усилить человекочитаемые входные листы:

```text
КАК ПОЛЬЗОВАТЬСЯ
КЛЮЧЕВЫЕ ВЫВОДЫ
КАРТА СТРАНИЦ И РЕШЕНИЙ
ЧТО ДЕЛАТЬ / ЧТО НЕ ДЕЛАТЬ / ЧТО ЖДЕТ ДОКАЗАТЕЛЬСТВ
ПЛАН ВНЕДРЕНИЯ ПО ГОТОВНОСТИ
ПОИСК И AI — ЧТО ДОКАЗАНО
```

Названия и объяснения recipient-facing листов должны соответствовать языковому контракту.

### WB-03 — workbook наследует mixed-language и implementation-precision дефекты Stage-6/SEO source

Implementation/Actions/Links/Routes materialized из тех же row-level authorities. Поэтому англоязычная внутренняя проза, template routing instructions, filename-only evidence и неразрешенный implementation mode не должны считаться исправленными только потому, что появились в XLSX.

**Correct rule:** `MATERIALIZED DEFECT != RESOLVED DEFECT`.

### WB-04 — Links и Routes нельзя считать полностью implementation-ready только по наличию строк

Для links нужны placement/anchor/context поля; для routes — explicit implementation mode и real-site change. Пока это не материализовано, workbook должен различать `ANALYTICAL_ROUTE` от `READY_IMPLEMENTATION_TASK`.

### WB-05 — workbook QA не содержит recipient-task walkthrough как отдельный hard gate

Текущий QA подтверждает render/visual/formulas/counts, но не фиксирует проверку сценариев вроде:

- клиент без знания репозитория находит решение по странице;
- специалист понимает, какое реальное изменение сайта требуется;
- пользователь отличает `READY`, `NO_CHANGE`, `HOLD`, `RECHECK`;
- evidence можно понять без открытия внутреннего TSV;
- Search/AI/uncertainty находятся без manual join нескольких листов.

**Как исправить:** добавить recipient-task walkthrough и usability verdict независимо от physical render QA.

### WB-06 — direct binary visual re-review pending in this owner review

GitHub connector подтверждает persisted binary identity и materialization sources, но в текущем owner-review ходе бинарный XLSX еще не был независимо открыт локально как spreadsheet. Поэтому layout-level новые claims сверх persisted Stage-12/14 render QA не делаются. Если визуальный/interactive usability станет material для correction, workbook должен быть открыт как workbook и проверен напрямую перед закрытием review.

## 6. Общий root cause четырех основных deliverables

```text
DEEP ANALYSIS EXISTS
+ CANONICAL DATA IS CORRECT
+ PACKAGE-WIDE QA IS GREEN
BUT
RECIPIENT-SPECIFIC PRODUCT CONTRACT IS TESTED TOO WEAKLY
=
OWNER FINDS MATERIAL RECIPIENT DEFECTS AFTER RELEASE
```

Stage 19/20 должны проверять не только наличие знания в package, а самостоятельную полноту каждого обещанного recipient artifact для его конкретного получателя и реальной recipient task.

Отдельные non-equivalences:

```text
PACKAGE-WIDE TRUTH != RECIPIENT-ARTIFACT COMPLETENESS
FIELDS PRESENT != EXECUTABLE SPECIALIST TASK
CORRECT DATABASE != CLIENT-USABLE WORKBOOK
MACHINE-READABLE != AI-CONSULTANT-USABLE
AI CLIENT IMPLEMENTATION CONSULTANT != INTERNAL RESEARCH EXECUTION CHECKPOINT
```

## 7. Required correction pass after review closes

После разбора всех финальных deliverables выполнить один согласованный correction pass:

1. не менять без причины Stage-5 semantic/action truth;
2. расширить client report из master authority, а не изобретать новое исследование;
3. полностью локализовать recipient-facing SEO instructions;
4. довести routing/link/ownership work packages до явного implementation mode и точного placement там, где это требуется;
5. материализовать corrected release file №03 как self-contained Markdown AI SEO-consultant document для заказчика;
6. обеспечить, что №03 содержит тот же подтвержденный workset, что №02, но объясняет его для клиента без SEO-знаний;
7. включить в №03 достаточные WHY / HOW / dependencies / do-not-break / acceptance checks и полную research logic;
8. JSON при необходимости оставить companion structured data layer, но не считать serialization proof recipient usability;
9. не переносить в №03 `EXECUTION_CURSOR`, внутренний roadmap или checkpoint semantics;
10. пересобрать workbook из исправленных client/spec authorities;
11. сохранить technical detail sheets, но дать нормальную recipient front door;
12. повторить cross-view reconciliation, включая equality workset №02 ↔ №03;
13. провести offline clean-context practical AI-consultant walkthrough;
14. повторить recipient-specific product QA;
15. только после owner/commissioner review вернуть финальный recipient acceptance.

## 8. Permanent lessons promoted by this review

Постоянные companion gates для Steps 18–20 должны содержать универсальные failure classes и hard gates. В Level1 нельзя переносить конкретные домены, URL, action IDs или counts этого теста.

Для AI recipient обязательно закрепить:

```text
AI CLIENT IMPLEMENTATION CONSULTANT != INTERNAL RESEARCH EXECUTION HANDOFF
MACHINE-READABLE != AI-CONSULTANT-USABLE
JSON_PARSE_PASS != AI-CONSULTANT PASS
AI PATH CONFIRMED WORKSET == HUMAN SPECIALIST PATH CONFIRMED WORKSET
```

## 9. Review status by physical release file

- [x] Release file 01 — Client research report: defect set recorded
- [x] Release file 02 — SEO specialist guide: defect set recorded
- [x] Release file 03 — AI SEO-consultant artifact: recipient-purpose / format / practical implementation / QA defect set recorded; corrected physical `.md` pending correction pass
- [x] Release file 04 — Workbook: structural/materialization review complete; direct binary owner usability check remains pending if material
- [ ] Release README / delivery message — recipient wording review
- [ ] Final package-level recipient experience

Следующий диагностический объект: **release README / delivery message и package-level recipient experience**.
