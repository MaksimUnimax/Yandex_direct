# OKNO_MSK — corrected recipient contract for release file 03 AI knowledge document

Дата: 2026-09-05  
Статус: **CURRENT / POST-RELEASE OWNER CORRECTION AUTHORITY / REWORK REQUIRED**  
Класс: **RECIPIENT CONTRACT CORRECTION / NOT A NEW ROADMAP STAGE**

Этот документ исправляет recipient-purpose, physical-format и acceptance-contract для release file №03. Он не переписывает исторический Stage-11/Stage-15 provenance и не утверждает, что corrected physical artifact уже материализован.

## 1. Исторический факт

Исторический Stage-11/Stage-15 выпуск материализовал AI knowledge artifact как JSON:

`03_OKNO_MSK_AI_KNOWLEDGE_DOCUMENT_2026-09-05.json`

Исторический Stage-11 QA проверял parseability, self-contained data presence и counts. Эти артефакты сохраняются как evidence того, что реально было выпущено.

Они не являются доказательством того, что JSON был правильным основным recipient format для LLM.

## 2. Для чего нужен третий документ

Release file №03 нужен для **передачи результатов выполненного исследования другой AI-системе**.

Пользователь должен иметь возможность загрузить один основной AI knowledge document в новый чат / новую AI-систему и затем дать конкретную новую пользовательскую задачу, для которой нужны результаты этого исследования.

Новый AI должен получить из документа достаточный контекст, чтобы правильно понимать и использовать результаты исследования без необходимости заново объяснять проект пользователем и без необходимости восстанавливать смысл из GitHub, прежних чатов или внутренних служебных файлов.

Главная функция:

```text
COMPLETED RESEARCH
-> SELF-CONTAINED AI-READABLE KNOWLEDGE HANDOFF
-> USER SUPPLIES A NEW TASK
-> AI USES THE RESEARCH RESULTS FOR THAT TASK
```

## 3. Для чего третий документ НЕ нужен

Release file №03 не является:

- execution cursor;
- roadmap handoff;
- checkpoint recovery file;
- внутренней очередью review;
- инструкцией автоматически продолжать Stage/Step;
- разрешением выполнять следующий внутренний этап;
- заменой отдельного пользовательского запроса.

Обязательная граница:

```text
AI RESEARCH KNOWLEDGE HANDOFF
!= INTERNAL EXECUTION HANDOFF

RESEARCH CONTEXT TRANSFER
!= CONTINUE ROADMAP FROM LAST CHECKPOINT

AI KNOWLEDGE DOCUMENT
!= EXECUTION_CURSOR
```

Сам факт загрузки №03 не запускает никакую работу. Новая работа определяется только отдельной задачей пользователя.

## 4. Как пользователь должен использовать №03

1. Открыть новый чат / новую AI-систему.
2. Загрузить основной AI knowledge document.
3. Указать, что документ содержит самодостаточный контекст результатов исследования и должен использоваться как source context.
4. Дать конкретную новую задачу.
5. AI использует зафиксированные выводы, evidence, решения, ограничения и uncertainty именно для этой пользовательской задачи.
6. Если в документе нет факта, AI не должен превращать его в известный.

Примеры допустимого применения после загрузки №03:

- объяснить, почему по конкретной странице/теме принято определенное решение;
- подготовить производный материал на основе исследования;
- сравнить варианты с учетом уже доказанных findings;
- разобрать Search/AI evidence по конкретному вопросу;
- использовать research findings при новой SEO-задаче пользователя;
- показать, какие выводы подтверждены, а какие остаются HOLD/RECHECK/SEARCH_REQUIRED.

Эти примеры не являются автоматической очередью действий.

## 5. Что основной AI knowledge document должен передавать

Документ должен позволять новому AI восстановить смысл выполненного исследования, а не только наличие строк/ID.

Минимальный material knowledge universe:

```text
WHAT WAS RESEARCHED
BUSINESS / SITE / SCOPE
RESEARCH PURPOSE
RESEARCH METHOD
EVIDENCE CLASSES
ORDINARY SEARCH ROLE AND BOUNDARIES
AI EVIDENCE ROLE AND BOUNDARIES
CURRENT ACCEPTED SEMANTIC / PAGE MODEL
MATERIAL FINDINGS
MATERIAL DECISIONS
WHY EACH MATERIAL DECISION EXISTS
KEEP / RETAIN / NO_CHANGE / DE_RISK FINDINGS
SUPPORTED CHANGES
NO-ACTION / NO-DESTRUCTIVE-ACTION BOUNDARIES
UNCERTAINTY
SEARCH_REQUIRED
REVIEW_DEFERRED
HOLD / RECHECK
FORBIDDEN OR UNSUPPORTED CLAIMS
CURRENT RESEARCH AUTHORITY PRIORITY
```

По материальным выводам должна быть восстановима эквивалентная причинная цепочка:

```text
FACT / OBSERVATION
-> EVIDENCE OBJECT
-> INTERPRETATION
-> SUPPORTED DECISION
-> LIMITATION
-> ACTION OR EXPLICIT NO-ACTION
```

## 6. Исправленный primary physical format

Основной corrected release file №03 должен быть материализован как **LLM-readable Markdown document (`.md`)**.

Причина: primary artifact должен быть оптимизирован под чтение, понимание контекста и reasoning новой AI-системой, а не под удобство serialization/counting.

Structured JSON может быть сохранен как дополнительное приложение для полного row-level universe и машинных связей, если это полезно для конкретного AI/tooling environment.

Но:

```text
MACHINE-READABLE
!= LLM-USABLE

JSON_PARSE_PASS
!= AI_HANDOFF_PASS

ALL ROWS PRESENT
!= RESEARCH MEANING RECOVERABLE

SELF-CONTAINED DATA
!= SELF-CONTAINED KNOWLEDGE
```

Если в будущем другой формат будет выбран как sole primary AI artifact, deliverable contract обязан отдельно доказать, почему он лучше или эквивалентен для реальной recipient task.

## 7. Что делать с историческим JSON

Исторический JSON не удаляется и не переписывается задним числом.

Он остается:

```text
HISTORICAL STAGE-11 / STAGE-15 PROVENANCE
```

и может быть повторно использован при corrected materialization как structured source/data annex, если его содержимое reconciles with current research authorities.

Он не должен автоматически называться текущим accepted primary AI knowledge document после исправления.

## 8. Исправленный AI recipient QA

Старый QA вида `json_parse + row counts + self_contained=true` недостаточен.

Требуется clean-context recipient test.

Условия теста:

```text
NEW AI CONTEXT
NO PREVIOUS CHAT
NO GITHUB CONTEXT
NO EXECUTION CURSOR
NO HIDDEN PROJECT STATE
PRIMARY AI KNOWLEDGE DOCUMENT ONLY
+ EXPLICIT USER TASK
```

AI должен корректно уметь:

- объяснить предмет и цель исследования;
- восстановить material research findings;
- объяснить причины material decisions;
- отделить `KEEP/NO_CHANGE` от `HOLD/RECHECK`;
- объяснить вклад ordinary Search и границу переноса evidence;
- объяснить material AI causal case и его decision delta;
- распознать uncertainty как uncertainty;
- назвать unsupported claim, который нельзя делать;
- использовать research context в новой пользовательской задаче;
- не требовать внутреннего Stage/Step state для понимания исследования;
- не начинать внутреннюю roadmap execution без отдельной команды пользователя.

Hard PASS markers:

```text
AI_HANDOFF_PURPOSE_CORRECT = true
AI_HANDOFF_PRIMARY_FORMAT_RECIPIENT_JUSTIFIED = true
AI_HANDOFF_RESEARCH_MEANING_SELF_CONTAINED = true
AI_HANDOFF_NOT_EXECUTION_CURSOR = true
AI_HANDOFF_CLEAN_CONTEXT_QA = PASS
AI_HANDOFF_UNSUPPORTED_INFERENCE_RATE = 0 for declared hard-boundary cases
```

## 9. Что должно быть исправлено при едином correction/materialization pass

1. Создать corrected current №03 `.md` из current accepted research authorities.
2. Сохранить narrative/context layer как primary.
3. При необходимости вынести полный structured row-level слой в companion JSON/data annex.
4. Не переносить в назначение №03 `EXECUTION_CURSOR`, roadmap continuation или checkpoint semantics.
5. Обновить corrected release README/manifest уже для нового corrected artifact set, а не переписывать исторический Stage-15 manifest.
6. Провести clean-context AI recipient QA.
7. Cross-reconcile corrected №03 с client report, SEO guide и workbook.
8. Только после этого возвращать current recipient acceptance для AI artifact.

## 10. Историческая граница

Stage 0–15 historical completion и исторические commit/blob SHA остаются provenance. Этот correction authority объясняет, **что должно быть текущей исправленной версией**, а не меняет историю того, что было выпущено.
