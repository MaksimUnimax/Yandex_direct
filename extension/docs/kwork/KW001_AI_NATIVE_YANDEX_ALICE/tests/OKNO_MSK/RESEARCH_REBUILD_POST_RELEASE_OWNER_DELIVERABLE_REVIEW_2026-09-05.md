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
!= LLM-USABLE

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

## 4. Release file 03 — AI knowledge document

Исторический release artifact: `OKNO_MSK_RESEARCH_RELEASE_2026-09-05/03_OKNO_MSK_AI_KNOWLEDGE_DOCUMENT_2026-09-05.json`.

Исторический Stage-11 guide: `RESEARCH_REBUILD_STAGE_11_AI_KNOWLEDGE_DOCUMENT_GUIDE_2026-09-05.md`.

Исторический Stage-11 QA: `RESEARCH_REBUILD_STAGE_11_QA_2026-09-05.json`.

### Для чего файл №03 нужен на самом деле

Файл №03 нужен для **передачи результатов выполненного исследования другой AI-системе**.

Пользователь должен иметь возможность загрузить один основной AI knowledge document в новый чат / новую AI-систему и затем дать конкретную новую задачу, для которой нужны результаты этого исследования. Новый AI должен получить достаточный контекст о том, что исследовалось, какие данные/evidence использовались, какие решения приняты и почему, что подтверждено, что рекомендовано, что осталось неопределенным и какие выводы делать нельзя.

Это **не** execution cursor, не roadmap handoff, не checkpoint и не инструкция автоматически продолжать внутренний проект.

```text
AI RESEARCH KNOWLEDGE HANDOFF
!= INTERNAL EXECUTION HANDOFF

RESEARCH CONTEXT TRANSFER
!= CONTINUE ROADMAP FROM LAST CHECKPOINT
```

Любая новая работа определяется отдельным запросом пользователя. Файл №03 только переносит знания о выполненном исследовании, необходимые AI для такой новой задачи.

### Как должен использоваться исправленный №03

```text
USER UPLOADS ONE PRIMARY AI KNOWLEDGE DOCUMENT
-> AI READS IT AS SELF-CONTAINED RESEARCH CONTEXT
-> USER PROVIDES A NEW TASK
-> AI USES THE RESEARCH FINDINGS / EVIDENCE / BOUNDARIES FOR THAT TASK
```

Новый AI не должен самостоятельно восстанавливать Stage/Step, `EXECUTION_CURSOR`, review queue или автоматически выполнять следующий внутренний этап только потому, что knowledge document был загружен.

### Что сделано правильно исторической Stage-11 materialization

- полный semantic master был сохранен в data layer;
- 168 canonical units и 34 actions были включены;
- Search/AI evidence, Search-case explanations, links, routes, page validations и uncertainty были включены;
- current-vs-historical authority boundary была явно задана;
- запрет на превращение uncertainty в решение был сохранен;
- exact-query Search evidence не разрешалось автоматически переносить на всё семейство;
- AI verdict не приравнивался к decision value без delta.

То есть Stage 11 сохранил значительный объем правильной исследовательской truth. Дефект относится прежде всего к recipient contract, primary format и recipient-specific QA, а не является доказательством потери всего canonical data layer.

### AI-01 — JSON выбран как основной AI knowledge document без доказанного recipient-format основания

**Ошибка:** исторический Stage-11 guide просто объявил `.json` основным AI-артефактом. Постоянный product contract не требовал именно JSON и не доказывал, что serialization-oriented формат лучше всего выполняет задачу передачи исследовательского контекста LLM.

**Как исправить:** исправленный основной файл №03 материализовать как самодостаточный LLM-readable Markdown document (`.md`). JSON может оставаться дополнительным структурированным data annex для полного row-level universe, но не автоматически подменять основной knowledge/context layer.

**Correct rule:** `MACHINE-READABLE != LLM-USABLE`.

### AI-02 — self-contained data ошибочно приравнен к self-contained knowledge

**Ошибка:** наличие всех таблиц/rows/IDs само по себе не доказывает, что новый AI восстановит смысл исследования: цель, метод, причинность решений, роль evidence, ограничения и uncertainty.

**Как исправить:** основной `.md` должен связно материализовать как минимум:

```text
WHAT WAS RESEARCHED
BUSINESS / SITE / SCOPE
RESEARCH PURPOSE
EVIDENCE CLASSES AND METHOD
CURRENT SEMANTIC / PAGE MODEL
MATERIAL FINDINGS
WHY EACH MATERIAL DECISION EXISTS
ORDINARY SEARCH CONTRIBUTION
AI CAUSAL CONTRIBUTION
KEEP / RETAIN / NO_CHANGE / DE_RISK
RECOMMENDED CHANGES
UNCERTAINTY / HOLD / RECHECK / SEARCH_REQUIRED
CLAIM BOUNDARIES / FORBIDDEN INFERENCES
CURRENT RESEARCH AUTHORITY PRIORITY
```

Полные row-level данные могут находиться в приложении/структурированном слое, но knowledge document не должен заставлять AI самостоятельно реконструировать повествование из массива внутренних объектов.

### AI-03 — Stage-11 QA проверял serialization/counts, а не реальную задачу AI-получателя

Исторический QA проверял `json_parse`, `self_contained` и counts по semantic/unit/action/evidence/search/AI/uncertainty/link/routing rows.

Это полезная data-integrity проверка, но она не отвечает на вопрос:

> сможет ли новая AI-система, получив только основной файл №03 и новую пользовательскую задачу, правильно использовать результаты исследования без GitHub/старых чатов и без выдумывания отсутствующего контекста?

**Correct rule:** `JSON_PARSE_PASS != AI_HANDOFF_PASS`.

### AI-04 — отсутствовал clean-context AI recipient walkthrough

**Как исправить:** перед PASS провести реальный clean-context test. Новая AI-сессия получает только основной knowledge document и набор recipient tasks, например:

- объяснить, почему для конкретной material page/topic принято текущее решение;
- отделить подтвержденный `NO_CHANGE/KEEP` от `HOLD/RECHECK`;
- показать, что именно ordinary Search поддержал и где заканчивается evidence boundary;
- объяснить material AI case и его decision delta;
- назвать unsupported claim, который нельзя делать;
- использовать результаты исследования для новой производной пользовательской задачи без repository reconstruction.

PASS возможен только если ответы соответствуют current research authorities и не требуют внутреннего execution state.

### AI-05 — release usage был сформулирован слишком технически

Исторический README говорил AI-системе «загрузить файл 03 и следовать interpretation rules». Это не объясняло нормальный recipient workflow и усиливало восприятие №03 как автономного исполнительного пакета.

**Как исправить:** usage должен быть пользовательским:

```text
UPLOAD KNOWLEDGE DOCUMENT
-> TREAT AS RESEARCH CONTEXT
-> USER ASKS A NEW TASK
-> AI USES RESEARCH RESULTS FOR THAT TASK
```

### AI-06 — non-purpose boundary не был достаточно жестко зафиксирован

Документация должна прямо запрещать смешение AI knowledge document с внутренними файлами управления выполнением.

```text
AI KNOWLEDGE DOCUMENT != EXECUTION_CURSOR
AI KNOWLEDGE DOCUMENT != ROADMAP CHECKPOINT
AI KNOWLEDGE DOCUMENT != AUTOMATIC NEXT-STAGE INSTRUCTION
```

Новый AI может выполнять новую работу только по отдельной пользовательской задаче; сам факт загрузки №03 не является разрешением или инструкцией продолжать внутренний roadmap.

### AI-07 — физический corrected artifact еще не материализован

На момент этого review в историческом release физически лежит JSON №03. Исправленный Markdown №03 должен быть создан в едином correction/materialization pass после завершения defect discovery, затем проверен clean-context AI recipient QA и только после этого заменять исторический JSON как current accepted recipient artifact.

Исторический JSON и release manifest сохраняются как provenance того, что реально было выпущено; они не переписываются задним числом так, будто исправленный `.md` существовал в Stage 15.

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

Stage 19/20 должны проверять не только наличие знания в package, а самостоятельную полноту каждого обещанного recipient artifact для его конкретного получателя.

Отдельные non-equivalences:

```text
PACKAGE-WIDE TRUTH != RECIPIENT-ARTIFACT COMPLETENESS
FIELDS PRESENT != EXECUTABLE SPECIALIST TASK
CORRECT DATABASE != CLIENT-USABLE WORKBOOK
MACHINE-READABLE != LLM-USABLE
AI RESEARCH HANDOFF != EXECUTION CHECKPOINT
```

## 7. Required correction pass after review closes

После разбора всех финальных deliverables выполнить один согласованный correction pass:

1. не менять без причины Stage-5 semantic/action truth;
2. расширить client report из master authority, а не изобретать новое исследование;
3. полностью локализовать recipient-facing SEO instructions;
4. довести routing/link/ownership work packages до явного implementation mode и точного placement там, где это требуется;
5. материализовать corrected release file №03 как self-contained LLM-readable Markdown research knowledge handoff; JSON при необходимости оставить только как structured data annex;
6. не включать в №03 `EXECUTION_CURSOR`, roadmap continuation или автоматическую next-stage semantics как его назначение;
7. пересобрать workbook из исправленных client/spec authorities;
8. сохранить technical detail sheets, но дать нормальную recipient front door;
9. повторить cross-view reconciliation;
10. провести отдельный clean-context AI recipient walkthrough для №03;
11. повторить recipient-specific product QA;
12. только после owner/commissioner review вернуть финальный recipient acceptance.

## 8. Permanent lessons promoted by this review

Постоянные companion gates для Steps 18–20 должны содержать универсальные failure classes и hard gates. В Level1 нельзя переносить конкретные домены, URL, action IDs или counts этого теста.

Для AI recipient обязательно закрепить:

```text
AI RESEARCH KNOWLEDGE HANDOFF != EXECUTION HANDOFF
MACHINE-READABLE != LLM-USABLE
JSON_PARSE_PASS != AI_HANDOFF_PASS
SELF-CONTAINED DATA != SELF-CONTAINED KNOWLEDGE
```

## 9. Review status by physical release file

- [x] Release file 01 — Client research report: defect set recorded
- [x] Release file 02 — SEO specialist guide: defect set recorded
- [x] Release file 03 — AI knowledge document: recipient-purpose / format / QA defect set recorded; corrected physical `.md` pending correction pass
- [x] Release file 04 — Workbook: structural/materialization review complete; direct binary owner usability check remains pending if material
- [ ] Release README / delivery message — recipient wording review
- [ ] Final package-level recipient experience

Следующий диагностический объект: **release README / delivery message и package-level recipient experience**.
