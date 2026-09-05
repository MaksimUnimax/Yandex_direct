# OKNO_MSK — инструкция к AI knowledge handoff

**Дата:** 2026-09-05  
**Статус:** CURRENT RECIPIENT CONTRACT CORRECTION / HISTORICAL STAGE-11 ARTIFACT PRESERVED

Исторический Stage-11 AI-артефакт был материализован как `RESEARCH_REBUILD_STAGE_11_AI_KNOWLEDGE_DOCUMENT_2026-09-05.json`. Этот факт сохраняется как provenance и не является доказательством того, что JSON был правильным основным форматом для AI-получателя.

Текущий post-release owner review исправляет recipient contract: основной AI knowledge handoff должен быть самодостаточным документом, оптимизированным для чтения и понимания новой AI-системой. Базовый физический формат для исправленной материализации — Markdown (`.md`). Структурированный JSON допустим как дополнительное data-приложение, если он нужен для сохранения row-level данных и машинных связей, но он не подменяет основной knowledge/context document.

## Назначение

Третий release-deliverable нужен для **передачи результатов выполненного исследования другой AI-системе**.

Пользователь должен иметь возможность загрузить один основной AI knowledge document в новый чат / новую AI-систему и затем задавать новые вопросы и задачи, опирающиеся на выполненное исследование, без необходимости заново объяснять проект и без необходимости для AI восстанавливать смысл из GitHub, прежних чатов или внутренних служебных файлов.

Документ должен передавать как единый связный контекст:

- что исследовалось;
- бизнес/site scope и цель исследования;
- какие источники и evidence classes использовались;
- как интерпретировались ordinary Search и AI evidence;
- текущую принятую semantic/page model;
- материальные решения и причины этих решений;
- подтвержденные `KEEP / RETAIN / NO_CHANGE / DE_RISK` результаты;
- рекомендованные изменения;
- Search cases и границы переноса evidence;
- AI causal cases и фактический decision delta;
- uncertainty / SEARCH_REQUIRED / REVIEW_DEFERRED / HOLD и причины этих состояний;
- ограничения и запрещенные сильные выводы;
- приоритет current research authorities над историческими/withdrawn результатами.

Исторический data layer содержит полный semantic master (2 840 строк), 168 канонических единиц, 34 действия и их реализационные спецификации, Search/AI evidence layer, 21 Search-case explanation, 15 ссылок, 46 маршрутов, текущие page-validations и 221 запись неопределённости. Исправленный AI knowledge document должен сохранять материальный смысл этого accepted research universe без потери причинно-следственных связей.

## Как использовать

1. Загрузить основной `.md` AI knowledge document в новый чат / новую AI-систему.
2. Попросить AI сначала использовать этот документ как самодостаточный контекст результатов исследования.
3. После этого дать AI конкретную новую пользовательскую задачу: объяснить решение, проанализировать страницу/тему, подготовить производный материал, сравнить варианты или выполнить другую работу, для которой нужны результаты исследования.
4. AI должен опираться на зафиксированные evidence/decision boundaries и не превращать отсутствующий факт в известный.

Этот документ **не является** execution cursor, roadmap handoff, checkpoint или автоматической инструкцией продолжать внутреннюю исследовательскую работу.

```text
AI RESEARCH KNOWLEDGE HANDOFF
!= INTERNAL EXECUTION HANDOFF

RESEARCH CONTEXT TRANSFER
!= CONTINUE ROADMAP FROM LAST CHECKPOINT
```

Новый AI не обязан восстанавливать Stage/Step, `EXECUTION_CURSOR`, внутреннюю очередь review или автоматически выполнять следующий этап. Любая новая работа определяется отдельным запросом пользователя.

## Как рассуждать по материалам исследования

Для каждого существенного вывода сохранять эквивалентную цепочку:

**факт → объект доказательства → поддержанный вывод → ограничение → действие или явное отсутствие действия**.

Нельзя:

- брать исторический клиентский пакет как текущую исследовательскую истину;
- заменять задачу/intent/role полями от старой единицы после correction;
- превращать неопределённость в решение;
- переносить exact-query Search observation на всё семейство без записанной границы;
- считать AI-ответ ценностью без decision delta;
- представлять NOT_READY/HOLD как готовое доказанное действие;
- советовать merge/delete/redirect для overlap-кейса без достаточного нового доказательства;
- интерпретировать сам факт наличия JSON/таблицы/ID как объяснение смысла evidence;
- автоматически продолжать внутренний roadmap только потому, что knowledge document был загружен.

## Приоритет исследовательских данных

1. current `semantic_master`;
2. current `canonical_units`;
3. current implementation/action specifications;
4. link/routing specifications;
5. evidence register, Search cases и AI causal cases;
6. residual uncertainty;
7. исторические материалы — только как provenance там, где они не противоречат current authority.

## Проверенная сводка исторической Stage-11 materialization

- 2 840 исходных уникальных фраз сохранены;
- 2 313 назначены;
- 19 SEARCH_REQUIRED;
- 174 REVIEW_DEFERRED;
- 334 EXCLUDED_PRESERVED;
- 168 структурных единиц;
- 69 атомарных semantic corrections;
- 34 действия;
- 0 new-page actions;
- AI: 0 CHANGE / 4 DE_RISK / 3 NO_CHANGE / 1 INSUFFICIENT;
- 0 AI architecture changes.

Любой иной исследовательский вывод должен быть объяснён явно предоставленным новым evidence/authority, а не догадкой.

## Исправленный acceptance principle

Исторический Stage-11 QA доказал parseability/self-contained data presence, но не recipient usability для новой AI-системы. Поэтому действуют обязательные non-equivalences:

```text
MACHINE-READABLE != LLM-USABLE
JSON_PARSE_PASS != AI_HANDOFF_PASS
ALL ROWS PRESENT != RESEARCH MEANING RECOVERABLE
SELF_CONTAINED DATA != SELF_CONTAINED KNOWLEDGE
```

Исправленная материализация №03 может получить PASS только после clean-context проверки: новая AI-система получает основной knowledge document без репозитория и прежних чатов и способна правильно восстановить смысл выполненного исследования, его решения, доказательства, ограничения и неопределённость, после чего использовать их в новой задаче пользователя без выдумывания отсутствующих фактов.
