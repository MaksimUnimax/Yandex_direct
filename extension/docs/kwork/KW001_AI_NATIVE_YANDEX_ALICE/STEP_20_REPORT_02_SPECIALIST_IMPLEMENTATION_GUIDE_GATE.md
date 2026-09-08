# KW-001 — Step 20 Report №02 canonical implementation-report gate

Updated: 2026-09-08  
Status: **ACTIVE / UNIVERSAL / OWNER-LOCKED / CANONICAL FOR REPORT №02**  
Scope: **Report №02 only**

> Legacy filename note: the file name contains `SPECIALIST_IMPLEMENTATION_GUIDE` for repository continuity. The client-facing document itself MUST NOT be named or framed as a specialist/SEO guide.

This is the primary permanent authority for how Report №02 must be built in future jobs.

Supplemental authorities:

- `STEP_20_REPORT_02_IMPLEMENTATION_REPORT_FORMAT_GATE.md` — plain-language report architecture;
- `STEP_20_REPORT_02_SPECIALIST_IMPLEMENTATION_GUIDE_LAYOUT_GATE.md` — DOCX/PDF physical layout.

All three must agree. If a supplemental gate conflicts with this file, this file wins until the conflict is corrected.

---

## 1. What Report №02 is

Visible client title:

```text
Внедрение рекомендации
```

Purpose:

```text
COMPLETED RESEARCH
-> CONCRETE SITE ACTIONS
-> CONCRETE CLARIFICATIONS
-> PLAIN SUPPORTING TABLES
-> CLEAR IMPLEMENTATION / CHECK METHOD
```

Report №02 is not a second research report, not an internal project database, not an audit log and not a document identified by the recipient's profession.

The client must be able to understand the document even without SEO expertise.

Permanent rule:

```text
DOCUMENT IDENTITY = PURPOSE / RESULT
DOCUMENT IDENTITY != RECIPIENT JOB TITLE
```

Forbidden client-facing identity/branding unless a separate owner contract explicitly requires it:

- «руководство специалиста»;
- «SEO-специалист»;
- «для SEO-специалиста»;
- «для редактора»;
- «для разработчика»;
- other profession-first naming.

---

## 2. Report №02 is action-first

The main document must answer, in this order:

1. what can be implemented now;
2. what needs one concrete clarification before implementation;
3. where each topic belongs on the existing site and how to use that information;
4. what unresolved questions must be checked, why and how;
5. which existing pages should be connected and how such a connection is implemented;
6. how to check the completed result;
7. which external materials were actually used.

Research-method detail is secondary. Report №01 carries the full research narrative. Report №04 carries the detailed phrase/data workbook.

Do not lead Report №02 with a long funnel of collection, cleanup, clustering, provider calls or internal stages unless a specific short fact is required to understand an implementation decision.

---

## 3. Canonical client structure

Default Report №02 structure:

```text
# Внедрение рекомендации

1. Что находится в документе
2. Готовые рекомендации
3. Что уточнить перед внедрением
4. Распределение тем по страницам
5. Проверки перед следующими изменениями
6. Связи между страницами
7. Как проверить результат
8. Материалы, использованные в исследовании
```

A different section count is allowed only when the job genuinely has no material for one of these blocks or requires an additional block. The logic remains the same.

The opening section should explain the contents in ordinary Russian and may include a compact map such as:

- ready recommendations;
- recommendations after clarification;
- topic-to-page rows;
- checks before further changes;
- page-to-page connections.

The summary must explain what each block means, not merely show counts.

---

## 4. Fully ready recommendation — required format

Each ready recommendation is a self-contained implementation task.

Use the following fields when applicable:

```text
Страница
Зачем менять
Что сделать
Где
Порядок работы
Пример
Проверка результата
```

### 4.1 `Зачем менять`

Explain the actual user/site problem in normal Russian.

Do not restate an internal status, action code or research enum.

### 4.2 `Что сделать`

State the final requested change directly.

### 4.3 `Где`

Give one evidence-backed placement when placement is required.

If the completed research supports only alternatives, the recommendation is not fully ready and moves to the clarification section.

### 4.4 `Порядок работы`

Only professional implementation operations belong here.

Good:

1. Добавить подраздел …
2. Разделить понятия …
3. Раскрыть сценарий …
4. Связать окончательные параметры с замером …

Bad filler:

- «Откройте страницу»;
- «Перейдите по ссылке»;
- «Найдите блок»;
- «Найдите заголовок»;
- «Проверьте результат» as a fake implementation step.

### 4.5 `Пример`

Use a practical wording/example when it materially helps implementation and is supported by evidence.

Project-proposed additions may be highlighted in bold.

### 4.6 `Проверка результата`

Describe the observable finished state.

Material preservation requirements belong here or inside the concrete action when needed, for example:

- existing price/calculator remains available;
- existing URL remains the same;
- existing manufacturer order remains the same.

Do not create a separate defensive section made mostly of preservation rules.

---

## 5. Recommendations requiring clarification

A useful but incomplete recommendation is not hidden and is not inflated into a ready task.

Use:

```text
Страница
Что хотим добавить / изменить
Что нужно уточнить
После уточнения
```

The missing fact must be concrete.

Good:

- выбрать одно место размещения блока;
- получить у компании фактический состав услуги;
- подтвердить применимость функции для конкретной системы;
- разметить существующие карточки по категориям.

Bad:

- «получить доказательство»;
- «не выдавать за готовую задачу»;
- «действие остаётся частичным»;
- generic status language.

`После уточнения` must explain what concrete deliverable/action becomes possible once the answer is obtained.

---

## 6. Topic-to-page mapping must be understandable to a non-specialist

Do not call the client section merely «семантические назначения» without explanation.

Preferred section name:

```text
Распределение тем по страницам
```

Before the table explain three things:

### Что это

Each row shows a topic/user question and the existing page where that topic should primarily be disclosed. A related page may cover a neighbouring question.

### Для чего

The table is used when preparing new text or updating existing pages so the topic strengthens the correct existing page instead of being scattered arbitrarily.

### Как использовать

Explain the columns in ordinary Russian:

```text
Тема / вопрос пользователя
Где раскрывать тему
Связанная страница
```

The main page is where the core information on the topic belongs. The related page is where the neighbouring/continuing question can be covered.

A bare sentence such as «использовать при ведении семантического ядра и контент-плана» is insufficient.

Do not repeat identical defensive phrases on every row.

---

## 7. Additional checks must explain purpose, method and decision

Preferred section name:

```text
Проверки перед следующими изменениями
```

Every check must answer:

```text
ЧТО НУЖНО ПОНЯТЬ
ЗАЧЕМ ЭТО НУЖНО
КАК ПРОВЕРИТЬ
КАКОЕ РЕШЕНИЕ ПРИНИМАЕТСЯ ПО РЕЗУЛЬТАТУ
```

A reader without SEO expertise must understand why the check exists.

Do not write «провести дополнительную проверку» without explaining the decision it supports.

---

## 8. Page-to-page connections must explain what they are and how to implement them

Do not present bare source→target pairs as unexplained technical candidates.

Preferred section name:

```text
Связи между страницами
```

Before the table explain:

### Что это

The first page is where the transition begins; the second is where the visitor goes for continuation or deeper detail on the topic.

### Для чего

The connection helps a visitor move naturally from a general explanation to a more detailed service, instruction or related material. It also connects closely related site content into a coherent path.

### Как внедрять

On the source page, choose the paragraph where the target topic naturally appears. Add a meaningful link whose wording describes the target content. Check that the sentence reads naturally and the link leads to the intended page.

Preferred columns:

```text
Откуда ведём
Куда ведём
```

The table defines the direction of the transition. The exact paragraph and wording are chosen during implementation from the existing source text unless already proved by completed research.

A bare instruction such as «определить блок, окружающий текст и формулировку ссылки» is a failure because it describes missing detail without explaining the task.

Duplicate source→target authority rows must be consolidated into one visible pair unless materially different contexts are explicitly shown.

---

## 9. No standalone defensive preservation section

A standalone client section equivalent to:

```text
Требования к существующей структуре
Что нельзя менять
Что не делать
```

is forbidden.

If preservation matters to a concrete recommendation, state it only in that recommendation or its result-check.

Client space is for required work, useful explanation and concrete clarification.

---

## 10. Client report describes required work, not absence of work

Permanent rule:

```text
CLIENT REPORT = WHAT TO DO + WHY + HOW + RESULT
CLIENT REPORT != LIST OF THINGS NOT TO DO
```

Avoid negative pseudo-actions such as:

- «не создавать»;
- «не менять»;
- «не внедрять»;
- «не размещать»;
- «не объединять»;
- «не выдавать за готовую задачу»;
- «из этого не следует…».

When preservation is genuinely part of acceptance, phrase it positively and locally:

```text
BAD: Не менять цены и калькулятор.
GOOD: Цены и калькулятор остаются на месте.
```

Do not remove legitimate factual negation from normal Russian merely to satisfy a mechanical rule. The ban is on pseudo-actions and defensive policy prose, not on the Russian particle «не» itself.

---

## 11. No internal process narration in client prose

Do not tell the client about report-production controls such as:

- «новые факты не собирались»;
- «отчёт не расширяет исследование»;
- post-hoc evidence;
- quarantine;
- provider-call count;
- owner FAIL history;
- validator history;
- internal state-machine transitions.

These belong in repository QA/provenance only.

The client report may explain a real evidence limitation when that limitation directly affects what can be implemented.

---

## 12. Report materialization must not become new project research

This is a critical cost boundary.

```text
REPORT MATERIALIZATION != NEW PROJECT RESEARCH
```

If completed research lacks exact placement, classification, business detail, Search evidence, current-page fact or other implementation evidence:

```text
DISCLOSE CONCRETE GAP
-> MOVE TO CLARIFICATION / CHECK
-> STATE THE REQUIRED ANSWER
```

Do not silently fill the gap by:

- rereading the client site;
- recrawling a large site section;
- classifying a new object set;
- repeating Search / Wordstat / Alice / AI calls;
- collecting new business facts.

A separate owner-authorized research/revalidation task may do this, but it is new work and must not be backdated into the completed research.

Fresh external methodology/bibliography validation is allowed when the report contract requires current references, provided it does not create or upgrade project-specific findings.

---

## 13. Evidence precision

### 13.1 Ready means evidenced enough to implement

A recommendation is ready only when the completed evidence supports the page/object, required change and necessary implementation detail.

Do not rescue readiness with post-report research.

### 13.2 Temporal facts stay attached to the evidenced object

```text
RANKING YEAR != PUBLICATION DATE
OBSERVATION DATE != PAGE PUBLICATION DATE
DATA SNAPSHOT DATE != CONTENT UPDATE DATE
CURRENT-YEAR WORDING != VERIFIED PUBLICATION DATE
```

### 13.3 Business facts require business evidence

Company-specific inclusions, exclusions, materials, warranties, obligations, prices or service boundaries require direct business evidence.

When missing, ask for the exact concrete fact in the clarification section.

### 13.4 Placeholders are forbidden in ready recommendations

No `[дата проверки]`, TBD, TODO or invented future values in ready client text.

---

## 14. Client language and traceability

Report №02 is written in natural Russian.

Project-internal traceability must stay out of client prose:

- action IDs;
- filenames;
- QA IDs;
- internal enum values;
- Stage/Step/CV/OR labels;
- repository-only terminology.

Official brands, URLs and unavoidable official external identifiers may remain in their official form.

Do not identify the report through a profession label such as SEO specialist/editor/developer.

---

## 15. Bibliography

The final substantive section lists external materials actually used when they are material to the report.

Each item contains:

1. title;
2. publisher/source;
3. direct URL.

The bibliography must cover material external surfaces actually discussed, including Yandex/Alice material where relevant.

Do not blindly copy a prior bibliography without required freshness validation.

---

## 16. Physical DOCX/PDF quality

The final committed artifact must pass the layout gate.

At minimum:

```text
EMPTY CONTENTS / TOC HEADING = 0
ORPHAN FIELD LABELS = 0
CLIPPED TEXT = 0
OVERLAPPED TEXT = 0
BROKEN GLYPHS = 0
BROKEN TABLES = 0
DIRECT URLS LEGIBLE = true
BOLD EXAMPLES LEGIBLE = true
FINAL COMMITTED PDF PAGES VISUALLY INSPECTED = true
```

Do not claim visual PASS from a predecessor render or a different binary.

---

## 17. Owner-identified failure classes — permanent memory

Every future Report №02 must explicitly avoid all failures below.

### Failure A — internal traceability leaked into client report
Action IDs, filenames, QA references or internal enums were shown to the client.

### Failure B — generic template steps replaced real implementation
Seven different actions were given nearly identical generic step lists.

### Failure C — ambiguous placement was presented as ready
Alternatives such as «before X or Y» were written as implementation-ready.

### Failure D — analysis was left to the implementer
A filtering/classification task named categories but left the actual mapping to the person receiving a supposedly ready instruction.

### Failure E — placeholder remained in a ready example
A ready recommendation contained an unresolved `[дата проверки]`-style placeholder.

### Failure F — numbering was presented as schedule
Document numbering implied execution order without a real scheduling decision.

### Failure G — duplicate visible link pair was hidden by row-count QA
Two internal authority rows became the same client-visible source→target pair.

### Failure H — bibliography missed a material external surface
The report discussed Alice/AI while the bibliography lacked relevant current official Yandex material.

### Failure I — temporal attribute was transferred to the wrong fact
`ranking for 2024` became `article published in 2024`.

### Failure J — report production expanded into expensive new research
Missing report detail triggered new client-site reads and a 224-card / 19-page portfolio classification after research was already complete.

### Failure K — internal process narration leaked into client prose
The report discussed what the project did not collect, scope controls, quarantine or authorization instead of the result.

### Failure L — negative pseudo-actions replaced required work
The client was told what not to create/change/implement instead of what to do.

### Failure M — obvious browser/editor mechanics were presented as implementation
Instructions such as «откройте», «найдите», «перейдите», «проверьте» padded the steps.

### Failure N — instructions were duplicated across fields and rows
Location, preservation, acceptance and no-change wording repeated instead of appearing once in the right place.

### Failure O — empty contents furniture was shipped
The PDF displayed «Содержание» with no useful contents entries.

### Failure P — mini-heading was orphaned from its content
Labels such as «Что уточнить» or «Пример» remained alone at the bottom of a page.

### Failure Q — recipient profession became the document identity
The document was branded as a specialist/SEO guide instead of naming the result.

### Failure R — 46-row topic table had no plain-language operational meaning
The reader saw «семантические назначения» but could not understand what the rows were for or how to use them.

### Failure S — 14 page pairs were unexplained technical candidates
The report listed pairs and requested «block/context/link wording» without explaining what the transition meant, why it helped or how it was implemented.

### Failure T — standalone «Требования к существующей структуре» section
A defensive preservation list occupied client space without advancing implementation.

### Failure U — implementation report reproduced research framing instead of an action plan
The document mixed research narrative, raw registers and internal workflow instead of prioritizing recommendations and usable next steps.

---

## 18. Canonical PASS gate for Report №02

Report №02 may pass only when all applicable checks below pass:

```text
VISIBLE TITLE = Внедрение рекомендации
CLIENT PROFESSION / ROLE BRANDING = absent
ACTION-FIRST STRUCTURE = true
READY RECOMMENDATIONS = WHAT + WHY + WHERE + HOW + EXAMPLE/RESULT CHECK where applicable
GENERIC READY STEP REUSE = 0
READY AMBIGUOUS PLACEMENT = 0
CLIENT PLACEHOLDERS = 0
CLARIFICATION ITEMS NAME EXACT ANSWER NEEDED = true
TOPIC-TO-PAGE REGISTER HAS WHAT / WHY / HOW = true
TOPIC-TO-PAGE COLUMNS ARE PLAIN RUSSIAN = true
ADDITIONAL CHECKS HAVE PURPOSE + METHOD + DECISION = true
PAGE-CONNECTION REGISTER HAS WHAT / WHY / HOW = true
PAGE-CONNECTION COLUMNS ARE PLAIN RUSSIAN = true
DUPLICATE VISIBLE PAGE PAIRS WITHOUT EXPLANATION = 0
STANDALONE PRESERVATION / PROHIBITION SECTION = absent
NEGATIVE PSEUDO-ACTION INSTRUCTIONS = 0
OBVIOUS OPEN / FIND / NAVIGATE FILLER STEPS = 0
PROCESS-HISTORY NARRATION IN CLIENT REPORT = 0
PROJECT-INTERNAL IDS / FILENAMES / ENUMS / QA LOCATORS = 0
REPORT-STAGE NEW PROJECT FACT COLLECTION = 0 unless separately owner-authorized
POST-HOC EVIDENCE USED TO UPGRADE READINESS = 0
TEMPORAL FACT ATTRIBUTION = EXACT EVIDENCE MATCH
UNSUPPORTED BUSINESS FACTS = 0
RAW RESEARCH FUNNEL DOMINATING REPORT = absent
BIBLIOGRAPHY COVERS MATERIAL EXTERNAL SURFACES = true
NON-SPECIALIST OWNER CAN EXPLAIN EVERY NON-OBVIOUS SECTION = true
NATURAL RUSSIAN PROSE = true
GENERATED / TEMPLATE FILLER = absent
MD / DOCX / PDF CONTENT EQUIVALENCE = PASS
EMPTY TOC HEADING = 0
ORPHAN FIELD LABELS = 0
FINAL COMMITTED PDF VISUAL READBACK = PASS
```

The final question before PASS is simple:

```text
CAN A PERSON WHO DID NOT PARTICIPATE IN THE RESEARCH UNDERSTAND:
WHAT TO DO,
WHY TO DO IT,
HOW TO DO IT,
WHAT MUST BE CLARIFIED,
AND WHAT EACH SUPPORTING TABLE IS FOR?
```

If not, Report №02 is not ready.
