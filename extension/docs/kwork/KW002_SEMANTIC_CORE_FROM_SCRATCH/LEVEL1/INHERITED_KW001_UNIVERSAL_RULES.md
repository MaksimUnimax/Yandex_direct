# KW-002 — INHERITED UNIVERSAL RULES FROM KW-001

Status: **ACTIVE / OWNER-AUTHORIZED / REQUIRED**  
Purpose: перенос универсальных правил, уже заработанных и исправленных в KW-001, в Level 1 KW-002 без повторного изобретения процесса.

## 0. Важная адаптация терминов

В поздних документах KW-001 слово `Level 2` местами использовалось для current-job workspace. Для KW-002 владелец зафиксировал другую иерархию документации:

```text
LEVEL 1 = общие правила всего KW-002
LEVEL 2 = универсальные правила/методика отдельных шагов KW-002
work/<JOB_ID>/ = факты, evidence, статус и артефакты конкретного заказа
```

Поэтому при переносе правил KW-001 вся логика, относившая конкретные данные клиента к current-job workspace, в KW-002 применяется к `work/<JOB_ID>/`, а не к Level 2.

---

# RULE 1 — Goal-first: сначала цель, потом методика и действия

### Правило

Перед каждым крупным шагом запрещено сразу переходить к поиску методики, API, Wordstat, Search, анализу таблиц или редактированию артефактов.

Сначала в чате должны быть восстановлены:

```text
ЦЕЛЬ ВСЕГО КВОРКА
ПОЛНЫЙ ROADMAP ОТ НАЧАЛА ДО ВЫДАЧИ КЛИЕНТУ
ЧТО УЖЕ РЕАЛЬНО ЗАВЕРШЕНО
ЧТО ЕЩЁ ОСТАЛОСЬ
ЦЕЛЬ ТЕКУЩЕГО ШАГА
КАКУЮ ПРОБЛЕМУ ОН РЕШАЕТ
КАКОЙ КОНКРЕТНЫЙ РЕЗУЛЬТАТ ДОЛЖЕН ПОЯВИТЬСЯ
```

Только после этого можно исследовать методику и выполнять шаг.

### Зачем

Чтобы техническая активность не подменяла цель заказа.

### Ошибка, которую блокирует

```text
API CALL / FILE / ANALYSIS TEXT / COMMIT
WAS TREATED AS
BUSINESS STEP COMPLETION
```

### PASS

Шаг может быть завершён только если заранее объявленный результат существует, сохранён, проверен и пригоден следующему шагу.

Source KW-001: `STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md`.

---

# RULE 2 — Полный roadmap обязателен перед и после каждого крупного шага

### Правило

Перед каждым major step и после него показывается один непрерывный roadmap всей работы, а не только текущий кусок.

Roadmap должен сохранять:

```text
все завершённые этапы
текущий этап
все будущие этапы
исправления/rework, если прошлый PASS позже оказался неверным
финальные deliverables / QA / revision / close
```

Списки `COMPLETED` и `REMAINING` не заменяют полный roadmap.

### Зачем

Чтобы новый контекст не восстанавливал ход работы по памяти, коммитам или догадкам.

### PASS

Владелец в любой момент видит: что строим, где стоим, что сделано, что дальше.

Source KW-001: `STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md`.

---

# RULE 3 — Обязательное объяснение простыми словами

### Правило

До выполнения шага в конце pre-step отчёта должно быть:

```text
Зачем нужен этот шаг?
Что конкретно будем делать?
Что получим в конце?
```

После шага:

```text
Зачем делали?
Что фактически сделали?
Что получили и что это даёт дальше?
```

Нельзя использовать внутренние слова `cluster`, `SERP`, `ownership`, `canonical`, `batch`, `ledger`, `provider` как объяснение само по себе.

### Зачем

Техническая полнота не равна понятности владельцу/клиенту.

### PASS

Шаг понятен человеку без знания SEO/API/аналитики.

Source KW-001: `STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md`.

---

# RULE 4 — Перед каждым шагом заново читать прошлые ошибки и non-repeat controls

### Правило

Перед major step нельзя вспоминать прошлые ошибки по памяти. Нужно заново открыть постоянный lessons/rules authority и явно выписать:

```text
какие прошлые ошибки относятся к этому шагу
что именно тогда сломалось
почему сломалось
какой контроль предотвращает повтор сейчас
```

Если релевантных ошибок нет — это тоже говорится явно.

### Зачем

Чтобы уже найденные дефекты не повторялись через несколько шагов/диалогов.

### PASS

Все релевантные non-repeat controls проверены перед переходом.

Source KW-001: `PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md`, `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md`.

---

# RULE 5 — Метод нельзя подтверждать собственной методичкой

### Правило

Каждый материальный элемент метода классифицируется:

```text
OFFICIAL
INDUSTRY_PRACTICE
PROJECT_TEST_VALIDATED
ANALYST_HEURISTIC / PROJECT-SPECIFIC
```

Внутренний runbook задаёт процесс, но не является независимым доказательством собственной правильности.

### Зачем

Чтобы проект не превратился в замкнутую систему: «правило верно, потому что мы раньше его записали».

### PASS

Для каждого важного решения понятно, откуда оно взялось и какой уровень доказательства имеет.

Source KW-001: `PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md`.

---

# RULE 6 — SOURCE → METHOD TRACE обязателен для каждого материального правила

### Правило

Каждый существенный элемент шага обязан иметь цепочку:

```text
METHOD ELEMENT
→ DIRECT SOURCE / PROJECT EVIDENCE / OWNER REQUIREMENT
→ EXACT CLAIM SUPPORTED
→ PROJECT-SPECIFIC ADDITION (если есть)
→ EXECUTABLE ACTION / OBSERVABLE OUTPUT
```

Это относится к:

```text
states/statuses
thresholds
filters
merge/split rules
sampling
routing
provider actions
pass/fail criteria
page/cluster rules
```

### Запрещено

Придумывать красивые симметричные состояния без реального источника или исполнимого действия.

```text
EVALUATION DIMENSION != EVIDENCE ROUTE
```

### PASS

```text
UNSUPPORTED_METHOD_ELEMENTS = 0
NON_EXECUTABLE_EVIDENCE_ROUTES = 0
```

Source KW-001: `SOURCE_TO_METHOD_TRACEABILITY_GATE.md`.

---

# RULE 7 — Исследование считается внедрённым только когда стало исполнимой схемой

### Правило

Найти хороший источник недостаточно. Каждое материальное требование превращается в:

```text
SOURCE
→ RESEARCH STATEMENT
→ REQUIREMENT CLASS
→ CURRENT MODE
→ ACTION / COLLECTION
→ ARTIFACT FIELD / OUTPUT
→ FAILURE POLICY
→ CLAIM BOUNDARY
→ QA CHECK
→ ACCEPTANCE CHECK
```

Допустимые классы:

```text
BASE_REQUIRED
OPTIONAL_ENHANCEMENT
CONDITIONAL_REQUIRED
FORBIDDEN_CLAIM_BOUNDARY
METHOD_CONTEXT_ONLY
```

### Зачем

Чтобы полезное внешнее исследование не оставалось декоративной заметкой.

### Канонические различия

```text
SOURCE_DISCOVERED != REQUIREMENT_OPERATIONALIZED
RESEARCH_STATEMENT != EXECUTION_CONTROL
LIMITATION_DISCLOSED != LIMITATION_GOVERNED
```

### PASS

Каждый material requirement отражён в действии, данных, QA и границах утверждений.

Source KW-001: `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`.

---

# RULE 8 — Перед платным/лимитируемым provider request нужен information-gain justification

### Правило

Перед новым платным/API/Search запросом записать:

```text
какой точный вопрос решаем
почему сохранённых данных недостаточно
какая операция нужна
какой новый информационный выигрыш ожидается
стоимость/квота
retry boundary
куда будет сохранён результат
какой acceptance decision использует результат
```

Provider availability сама по себе не является причиной делать запрос.

### Зачем

Не делать бессмысленные повторы и одновременно не экономить там, где прямое доказательство действительно нужно.

Source KW-001: `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`, `EVIDENCE_QUALITY_AND_PROVIDER_COST_POLICY.md`.

---

# RULE 9 — Качество доказательства важнее минимизации provider cost

### Правило

```text
RESULT QUALITY > PROVIDER COST MINIMIZATION
DELIVERY TIME > PROVIDER COST MINIMIZATION
EVIDENCE RELIABILITY > PROVIDER COST MINIMIZATION
```

Если прямой источник Яндекса существенно лучше отвечает на вопрос, стоимость не должна автоматически отправлять нас к догадке или слабой косвенной проверке.

Но:

```text
MORE REQUESTS != BETTER METHOD
```

Новый запрос должен добавлять coverage/freshness/confidence/directness/error detection/time saving/client-result quality.

### Зачем

Не строить дешёвую, но слабую SEO-аналитику.

### PASS

Стоимость измерена и учтена в экономике кворка, но качество не деградировано ради временной цены пакета.

Source KW-001: `EVIDENCE_QUALITY_AND_PROVIDER_COST_POLICY.md`.

---

# RULE 10 — Bridge используется как руки для evidence, а не как аналитик

### Разделение ролей

```text
Yandex Marketing Bridge
= provider acquisition / persistence / batching / recovery / provenance

ChatGPT main workflow
= аналитическое решение / метод / QA / клиентское объяснение

ChatGPT Work
= большие данные / преобразование / артефакты по разрешённой методике

Owner
= authorization / business truth / commercial scope
```

Bridge не определяет SEO-стратегию, кластеры или страницы только потому, что умеет собрать данные.

Source KW-001: `RULES_ARCHITECTURE.md`, provider gates.

---

# RULE 11 — Перед каждым Bridge command явно назвать режим

### Правило

Перед командой владельцу/оператору обязательно написать:

```text
ACTIVE SERVICE
EXECUTION MODE
ADDITIONAL MATERIAL STATE
billable/request effect, если релевантно
```

Нельзя рассчитывать, что оператор помнит состояние расширения из прошлого сообщения.

### Зачем

В KW-001 уже был случай, когда команда ушла при активном другом service и пришлось повторять действие.

Source KW-001: `DIALOGUE_AND_ANALYTICAL_DISCIPLINE.md`.

---

# RULE 12 — Provider success != project evidence completion

### Правило

После каждого substantive Bridge result:

```text
provider outcome known
→ complete required result received
→ COMPLETE useful evidence saved durably
→ readback
→ count / field / provenance reconciliation
→ only then next provider action or downstream analysis
```

Не являются доказательством завершения:

```text
HTTP 200
request_executed=true
SUCCEEDED
terminal count
cost recorded
summary
representative examples
```

### Зачем

KW-001 уже получил технически успешные запросы, от которых были сохранены только примеры/сводки; downstream потерял полный массив.

### Жёсткое правило для semantic acquisition

```text
EVERY RETURNED ROW FROM EVERY AUTHORIZED REQUEST MUST BE DURABLY PRESERVED
```

Сохраняются также дубликаты raw observations, исключённые, low-frequency, REVIEW/HOLD и association rows. Фильтрация происходит позже.

### PASS

Returned/saved/verified counts reconciled; нужные поля/provenance не потеряны.

Source KW-001: `BRIDGE_EVIDENCE_PERSISTENCE_GATE.md`, `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` Step 3.

---

# RULE 13 — Анализировать provider evidence после durable readback

### Правило

```text
USEFUL PROVIDER EVIDENCE
→ DURABLE STORAGE
→ READBACK
→ ANALYZE FROM SAVED AUTHORITY
```

Chat/runtime paste — транспорт, а не единственная копия project truth.

### Зачем

Чтобы после длинного диалога, перезапуска или нового контекста не восстанавливать evidence по памяти.

Source KW-001: `BRIDGE_EVIDENCE_PERSISTENCE_GATE.md`.

---

# RULE 14 — Не соглашаться автоматически с возражением владельца

### Правило

Owner authority обязателен для:

```text
реальных бизнес-фактов
scope
authorization
commercial priority
owner decisions
```

Но аналитическое возражение проверяется:

```text
RESTATE POINT
→ CURRENT LOGIC
→ EVIDENCE VS ASSUMPTION
→ RULES + SOURCES + CURRENT EVIDENCE CHECK
→ REAL DEFECT | COMMUNICATION DEFECT | UNCERTAINTY | NO DEFECT
→ CHANGE ONLY IF JUSTIFIED
```

### Зачем

Сильная формулировка/повтор не должна подменять аналитическую проверку.

Source KW-001: `DIALOGUE_AND_ANALYTICAL_DISCIPLINE.md`.

---

# RULE 15 — Универсальные правила owner-locked; конкретный заказ не переписывает метод автоматически

### Правило

Ошибка текущего заказа сначала фиксируется в `work/<JOB_ID>/`.

Если она выглядит универсальной:

```text
JOB INCIDENT
→ PROPOSE FAILURE CLASS / ROOT CAUSE / CONTROL
→ OWNER REVIEW
→ ONLY EXPLICIT OWNER AUTHORIZATION MAY CHANGE LEVEL 1 / LEVEL 2
```

### Запрещено

Автоматически превращать один случай клиента в вечное правило.

### Зачем

KW-001 уже загрязнял постоянные методы конкретными URL, counts, case IDs и incident details.

Source KW-001: `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`, `JOB_WORKSPACE_LIFECYCLE.md`.

---

# RULE 16 — Permanent method не содержит данные конкретного заказа

### Запрещено в Level 1 и Level 2

```text
client/test name as method input
client domain/URL
current query/cluster/action IDs
current row/page/query totals as universal thresholds
current provider receipt/request ID/cost
current commit SHA/job status
current product vocabulary presented as universal law
```

Допустимы параметризованные placeholders и generic examples.

### Каноническое правило

```text
JOB EVIDENCE MAY EARN A RULE
BUT
JOB EVIDENCE MUST NOT BECOME THE RULE INPUT
```

### PASS

Перед финализацией постоянного правила выполняется contamination audit.

Source KW-001: `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.

---

# RULE 17 — Material authority mutation инвалидирует зависимые PASS

### Правило

Если меняется material canonical decision/assignment/taxonomy/entity:

```text
MUTATION
→ IMPACT SET
→ INVALIDATE AFFECTED PASSES
→ REBUILD DERIVED FIELDS
→ REBUILD MATERIAL DOWNSTREAM CONSUMERS
→ RECONCILE TO NEW AUTHORITY
→ INDEPENDENT QA
→ PERSIST + READBACK
→ ONLY THEN PASS AGAIN
```

### Зачем

Исправление одного ID/строки не гарантирует, что зависимые поля, таблицы и отчёты перестали содержать старое решение.

### Каноническое различие

```text
CORRECTED ID != CORRECTED SEMANTIC STATE
```

Source KW-001: `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`.

---

# RULE 18 — Не стирать неопределённость ради красивого полного результата

### Правило

```text
REVIEW / HOLD / SEARCH_REQUIRED / DEFERRED / UNRESOLVED
= GOVERNED DATA
!= EMPTY CELL TO FORCE-COMPLETE
```

Перевод unresolved → resolved требует нового evidence + decision authority + transition lineage + rebuild dependent fields.

### Зачем

Полнота клиентского файла не должна превращать неизвестное в выдуманный ответ.

Source KW-001: `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`.

---

# RULE 19 — Concrete step must embed its own gates; ссылки на Level 1 недостаточно

### Правило

Каждый конкретный шаг в `work/<JOB_ID>/` должен материализовать минимум:

```text
KWORK_GOAL
FULL_ROADMAP
COMPLETED
REMAINING
STEP_GOAL
STEP_SOLVES
REQUIRED_OUTPUT
RELEVANT_PRIOR_ERRORS
NON_REPEAT_CONTROLS
METHOD_SOURCES
METHOD_PLAN
PASS_CONDITION
```

Если шаг использует Bridge, он дополнительно содержит:

```text
YMB_STEP_OBJECTIVE
YMB_REQUIRED_MODE
YMB_REQUIRED_SAVED_RESULT
YMB_COMPLETENESS_CHECK
YMB_STOP_CONDITION
```

Просто написать «см. universal file» недостаточно.

Source KW-001: `PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md`, `STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md`.

---

# RULE 20 — End-of-step quantitative accounting обязателен

### Правило

По окончании каждого шага показать все применимые числа:

```text
planned
processed
provider attempts
provider executed
returned
saved
verified
deduplicated
excluded
retained
review/hold
analyzed
artifacts
errors / outcome_unknown
provider cost
```

Количество должно сходиться с объявленным результатом шага.

### PASS

Если counts не reconcile — шаг `INCOMPLETE`, следующий заблокирован.

Source KW-001: `PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md`, `STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md`.

---

# RULE 21 — Каждый шаг заканчивается явным transition decision

```text
NEXT_STEP_ALLOWED = true | false
```

`true` только если:

```text
required output exists
required evidence/artifacts persisted
verification passed
counts reconcile
roadmap/status updated
blocking uncertainty absent or correctly routed
non-repeat controls passed
```

Source KW-001: `STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md`.

---

# RULE 22 — Большие данные → ChatGPT Work, а не урезание качества

KW-002 owner-specific addition, compatible with KW-001 large-run experiment lessons:

```text
IF ORDINARY CHAT CANNOT RELIABLY PROCESS COMPLETE DATASET
THEN
DO NOT SAMPLE FOR CONVENIENCE
DO NOT DROP ROWS
DO NOT REPLACE ANALYSIS WITH SUMMARY
→ FREEZE WORK HANDOFF MANIFEST
→ USE OWNER-SUPPLIED CANONICAL WORK PROMPT
→ RUN COMPLETE EXECUTION UNIT IN CHATGPT WORK
→ RETURN ARTIFACTS
→ VERIFY SOURCE MANIFEST / COUNTS / JOINS / HOLD / QA
→ ONLY THEN ACCEPT
```

Work is execution environment, not method authority.

Canonical KW-002 authority: `LEVEL1/WORK_HANDOFF_RULE.md`.

---

# RULE 23 — Job close only after handoff/revisions/provider actions are really closed

```text
ANALYSIS COMPLETE
!=
JOB SAFE TO CLOSE
```

Close only after:

```text
final deliverables complete
handoff complete
revision/rework closed
no pending provider/operator action
safe_to_close=true
```

Source KW-001: `JOB_WORKSPACE_LIFECYCLE.md`.

---

# REQUIRED LEVEL-1 READ ORDER FOR KW-002

Before every major step:

```text
1. LEVEL1/INHERITED_KW001_UNIVERSAL_RULES.md
2. LEVEL1/COMMON_RULES.md
3. LEVEL1/METHOD_SOURCE_AND_EVIDENCE_RULES.md
4. LEVEL1/CLIENT_INTAKE_AND_SCOPE_RULE.md when scope/client inputs are material
5. LEVEL1/JOB_DATA_SEPARATION_AND_LIFECYCLE.md
6. LEVEL1/WORK_HANDOFF_RULE.md when large-data risk exists
7. current LEVEL2 step method
8. current work/<JOB_ID>/ manifest / flow / evidence
```

## Inherited source authorities

Primary KW-001 universal authorities used for this transfer:

```text
DIALOGUE_AND_ANALYTICAL_DISCIPLINE.md
STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md
PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md
SOURCE_TO_METHOD_TRACEABILITY_GATE.md
RESEARCH_TO_EXECUTION_SCHEMA_GATE.md
BRIDGE_EVIDENCE_PERSISTENCE_GATE.md
EVIDENCE_QUALITY_AND_PROVIDER_COST_POLICY.md
PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md
JOB_WORKSPACE_LIFECYCLE.md
STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md
```

## Markers

```text
KW002_KW001_LEVEL1_RULE_INHERITANCE_COMPLETE = true
KW002_GOAL_FIRST_REQUIRED = true
KW002_FULL_ROADMAP_EVERY_MAJOR_STEP = true
KW002_PRIOR_ERROR_REREAD_REQUIRED = true
KW002_SOURCE_TO_METHOD_TRACE_REQUIRED = true
KW002_RESEARCH_TO_EXECUTION_SCHEMA_REQUIRED = true
KW002_PROVIDER_RESULT_COMPLETENESS_REQUIRED = true
KW002_COMPLETE_RETURNED_ROWS_PERSISTENCE_REQUIRED = true
KW002_PROVIDER_QUALITY_BEFORE_COST_MINIMIZATION = true
KW002_LEVEL1_LEVEL2_OWNER_LOCKED = true
KW002_JOB_DATA_MUST_NOT_CONTAMINATE_PERMANENT_METHOD = true
KW002_AUTHORITY_MUTATION_REBUILD_REQUIRED = true
KW002_UNCERTAINTY_CONTINUITY_REQUIRED = true
KW002_PLAIN_LANGUAGE_SUMMARY_REQUIRED = true
KW002_QUANTITATIVE_ACCOUNTING_REQUIRED = true
KW002_NEXT_STEP_ALLOWED_REQUIRED = true
KW002_WORK_HANDOFF_RULE_REQUIRED_WHEN_TRIGGERED = true
```