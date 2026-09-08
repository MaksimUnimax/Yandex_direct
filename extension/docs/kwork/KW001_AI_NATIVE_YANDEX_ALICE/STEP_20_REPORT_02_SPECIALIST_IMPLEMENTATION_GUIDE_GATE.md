# KW-001 — Step 20 Report №02 specialist implementation-guide gate

Updated: 2026-09-08  
Status: **ACTIVE / UNIVERSAL / OWNER-LOCKED**  
Scope: **Report №02 only — implementation guide for the specialist who will directly apply changes**

This gate defines the permanent recipient contract for Report №02. It does not mark a current artifact PASS by itself.

---

## 1. Recipient and purpose

Recipient: SEO specialist, editor or developer who will perform the accepted work.

Report №02 is an implementation guide. It must let the specialist understand:

- which page/object is involved;
- what problem was found;
- what exact change is required;
- where the change belongs when the completed research proved placement;
- which professional operations to perform;
- what the result may look like;
- what must be preserved as part of the accepted result;
- how the completed result is accepted;
- which concrete fact must first be clarified when the work is not yet implementation-ready.

The report is not an internal action database, repository audit log, process diary or tutorial on how to open a page/editor.

---

## 2. Report materialization must not expand into new research

The reporting stage materializes the completed research authority.

```text
REPORT MATERIALIZATION != NEW PROJECT RESEARCH
```

If a detail required for implementation is missing from preserved evidence:

```text
NAME THE CONCRETE CLARIFICATION
-> KEEP THE ITEM OUT OF THE FULLY READY SET
-> STATE THE RESULT REQUIRED FROM THAT CLARIFICATION
```

Do not collect a missing project fact during report writing unless the owner explicitly authorizes a separate evidence-producing task.

Examples of unauthorized report-stage expansion:

- rereading client pages to rescue exact placement;
- recrawling large site sections;
- classifying objects that were not classified during the completed research;
- repeating Search / Wordstat / Alice / AI acquisition;
- collecting new business facts from the client.

External methodology/bibliography freshness may be revalidated when required by the report contract. It must not create or upgrade project-specific findings.

Post-hoc evidence created by an unauthorized report-stage expansion remains provenance only and cannot upgrade readiness.

---

## 3. Client report contains required work, not absence of work

The client-facing Report №02 must describe what the specialist actually needs to do.

```text
CLIENT REPORT = REQUIRED ACTIONS + REQUIRED CLARIFICATIONS + ACCEPTANCE RESULT
CLIENT REPORT != LIST OF THINGS NOT TO DO
```

### 3.1 Negative pseudo-actions are forbidden

Do not fill the client report with instructions such as:

- «не создавать»;
- «не менять»;
- «не внедрять»;
- «не размещать»;
- «не объединять»;
- «не выдавать за готовую задачу»;
- «не считать скрытой задачей»;
- «из этого не следует…».

If preservation is material, write it as a positive required action:

```text
BAD: Не создавать новый URL.
GOOD: Использовать существующий URL.

BAD: Не менять цены и калькулятор.
GOOD: Сохранить существующие цены и калькулятор.
```

If an item needs more evidence, write the exact next action:

```text
BAD: Не внедрять до получения доказательства.
GOOD: Уточнить у компании состав монтажной услуги.
GOOD: Выбрать одно место размещения блока.
GOOD: Разметить карточки по категориям.
```

### 3.2 Process-history narration is forbidden in the client report

Do not tell the recipient about internal process events that are irrelevant to execution, including wording equivalent to:

- «новые факты не собирались»;
- «отчёт не расширяет исследование»;
- «post-hoc evidence не использовался»;
- «отдельно санкционированная работа»;
- «провайдеры не вызывались»;
- internal correction history / owner-fail history / QA history.

Such information belongs in repository evidence, correction logs and QA only.

The client report may explain the actual completed research and actual evidence boundaries when they materially affect the specialist's decision.

---

## 4. Specialist instructions contain professional operations only

The specialist already knows how to open a URL, find a heading and use an editor.

The `Работы` / step-by-step section must contain only meaningful professional operations.

Forbidden filler steps include:

- «Откройте страницу»;
- «Перейдите по ссылке»;
- «Найдите указанный блок»;
- «Найдите заголовок»;
- «Проверьте результат» as a substitute for acceptance criteria;
- generic «сохраните всё остальное»;
- any obvious UI/navigation mechanics that do not change the implementation decision.

Correct action steps start directly with the change, for example:

1. Добавить подраздел …
2. Разделить понятия …
3. Раскрыть сценарий …
4. Связать окончательные параметры с замером …

Location is stated once in `Где изменить`. Acceptance is stated once in `Критерии приёмки`. Do not repeat those fields as pseudo-steps.

---

## 5. Mandatory structure of a fully ready item

For every fully ready real site change, include:

1. short action name;
2. direct page/object;
3. `Проблема` — actual deficiency in normal Russian;
4. `Что изменить` — exact requested result;
5. `Где изменить` — one evidenced placement where required;
6. `Работы` — action-specific professional operations only;
7. practical example where useful and evidence-safe;
8. `Сохранить` — only material elements that form part of the accepted result;
9. `Критерии приёмки` — observable completed-state criteria.

Do not duplicate the same instruction across several fields.

A ready action is executable from the completed research. If exact placement/classification/business detail is missing, the item moves to the clarification section.

---

## 6. Items requiring clarification

A non-ready but useful finding is presented as a concrete work package, not as a meta-status lecture.

Use:

- `Что уже определено`;
- `Что уточнить`;
- `Содержание будущего блока` or `Результат уточнения` when relevant.

Do not write:

- «задание остаётся частичным»;
- «не должно выдаваться за готовое»;
- «получить названное доказательство»;
- «граница приёмки сейчас»;
- generic readiness/status explanations.

The recipient should see exactly which fact or implementation decision is missing.

---

## 7. Semantic assignments and internal links

### 7.1 Semantic assignments

If the standalone semantic core exists, Report №02 may show a compact register:

- topic/task;
- main page;
- supporting page(s).

Do not repeat an identical sentence such as «физически страницу не менять» on every row.

A short section-level explanation is enough: these assignments are used for semantic-core and content-plan work.

### 7.2 Internal links

A link relationship that lacks exact context is shown as a pair requiring detailing.

Client-visible fields should be useful to the specialist, for example:

- source page;
- target page;
- section-level instruction explaining what must be detailed: exact source block, surrounding text, link wording and user-transition role.

Do not repeat the same `чего не хватает` sentence 14 times.

Duplicate source→target authority rows must be consolidated into one visible decision unless the contexts are materially distinct and explicitly shown.

---

## 8. Positive preservation language

Preservation constraints are allowed when they are actual implementation requirements, but must be phrased positively.

Examples:

- «Сохранить существующий URL»;
- «Сохранить текущий порядок производителей»;
- «Сохранить существующие цены и калькулятор»;
- «Сохранить раздельные роли страниц до результата проверки».

A whole client-facing section made of prohibitions is forbidden.

---

## 9. Evidence precision

### 9.1 Exact placement

Placement must come from completed preserved evidence.

If evidence supports only alternatives, do not browse the site during reporting to choose one. Put the item in the clarification section and state the exact placement decision that must be made later.

### 9.2 Temporal facts

A temporal attribute remains attached to the exact evidenced object.

```text
RANKING YEAR != PUBLICATION DATE
OBSERVATION DATE != PAGE PUBLICATION DATE
DATA SNAPSHOT DATE != CONTENT UPDATE DATE
CURRENT-YEAR WORDING != VERIFIED PUBLICATION DATE
```

Do not transfer a date/year from one fact to another during client writing.

### 9.3 Business facts

Company-specific inclusions, exclusions, warranties, materials, obligations, prices or service boundaries require direct business evidence.

When missing, write the concrete clarification required from the company.

---

## 10. Client language and internal traceability

For a Russian report:

- project-invented terms/codes are expressed in normal Russian or omitted;
- project action IDs, internal filenames, QA IDs and internal enum values are forbidden in the client report;
- official brands, URLs and unavoidable external technical identifiers may remain Latin/English;
- internal traceability stays in repository evidence.

```text
CLIENT REPORT = NO PROJECT-INTERNAL IDS / FILENAMES / ENUMS / QA LOCATORS
```

---

## 11. Research explanation and Wordstat/Alice wording

The report may briefly explain how the implementation plan was obtained when that helps the specialist:

- site/business inventory;
- demand collection and cleanup;
- clustering/task grouping;
- phrase/page mapping;
- ordinary Yandex validation;
- Alice/AI comparison when material;
- final implementation decision.

Do not narrate internal correction mechanics.

For Wordstat, use the official meaning of the preserved metric. Broad/no-operator observations are not exact phrase frequency or a traffic forecast.

Alice/AI output is evidence observed and compared with the research decision; it is not the research author.

---

## 12. Bibliography

The final substantive section contains the external materials actually used.

Each item includes:

1. title;
2. publisher/source;
3. direct URL.

Sources are freshly revalidated when the job/report contract requires it. A prior project bibliography is not copied blindly.

---

## 13. Known failure classes — permanent memory

The following failures are owner-identified and must be prevented in every future Report №02:

### Failure A — internal traceability leaked into client report
Action IDs, filenames, QA references or internal enum values were shown to the recipient.

### Failure B — generic steps were presented as implementation steps
Repeated template steps replaced action-specific professional operations.

### Failure C — ambiguous placement was presented as ready
Alternative locations were written as if the implementation was fully defined.

### Failure D — analysis was left to the implementer
A category/filter task named categories but did not supply the completed mapping or explicitly request the missing mapping work.

### Failure E — placeholder in a ready instruction
A ready example contained an unresolved value such as `[дата проверки]`.

### Failure F — numbering implied a schedule
Document numbering was presented as implementation order without a real schedule decision.

### Failure G — duplicate link pair hidden by row-count QA
Two authority rows became the same visible source→target decision.

### Failure H — bibliography missed a material evidence surface
The report discussed Alice/AI while the bibliography lacked the current official surface documentation.

### Failure I — temporal attribute transferred to the wrong object
`ranking 2024` was rewritten as `article published in 2024`.

### Failure J — report materialization expanded into new research
Missing implementation detail triggered new site reads / portfolio classification during reporting.

### Failure K — internal process narration leaked into client prose
The report told the recipient that new facts were not collected, scope was not expanded, evidence was quarantined, or a later check required special authorization.

### Failure L — negative pseudo-actions replaced actual work
The report repeatedly told the specialist what not to create/change/implement instead of stating the required action or clarification.

### Failure M — obvious browser/editor mechanics were called implementation steps
Steps such as «откройте страницу», «найдите блок», «проверьте» inflated the guide without helping a specialist perform the work.

### Failure N — the same instruction was repeated across fields/rows
Location, preservation, acceptance or semantic no-change text was duplicated instead of being stated once in the proper section.

---

## 14. Report №02 PASS gate

Report №02 may pass only when:

```text
RECIPIENT = DIRECT SPECIALIST / IMPLEMENTER
CLIENT PURPOSE = EXECUTION
REPORT-STAGE NEW PROJECT FACT COLLECTION = 0 unless separately owner-authorized
POST-HOC EVIDENCE USED TO UPGRADE READINESS = 0
PROJECT-INTERNAL IDS / FILENAMES / ENUMS / QA LOCATORS IN CLIENT REPORT = 0
CLIENT PLACEHOLDERS = 0
PROCESS-HISTORY NARRATION IN CLIENT REPORT = 0
NEGATIVE PSEUDO-ACTION INSTRUCTIONS = 0
OBVIOUS OPEN/FIND/NAVIGATE/CHECK FILLER STEPS = 0
READY ACTION GENERIC STEP TEMPLATE REUSE = 0
READY ACTIONS HAVE DIRECT PAGE/OBJECT = true where applicable
READY ACTIONS HAVE ONE EVIDENCED PLACEMENT = true where placement is required
READY ACTIONS HAVE ACTION-SPECIFIC PROFESSIONAL OPERATIONS = true
READY ACTIONS HAVE PRACTICAL EXAMPLE = true where useful and evidence-safe
READY ACTIONS HAVE OBSERVABLE ACCEPTANCE CRITERIA = true
CLARIFICATION ITEMS NAME THE EXACT MISSING FACT/DECISION = true
SEMANTIC ASSIGNMENTS ARE COMPACT AND NON-REPETITIVE = true
INTERNAL LINK DECISIONS ARE UNIQUE OR EXPLICITLY DISTINGUISHED = true
TEMPORAL FACT ATTRIBUTION = EXACT EVIDENCE MATCH
UNSUPPORTED BUSINESS FACTS = 0
BIBLIOGRAPHY COVERS MATERIAL EXTERNAL SURFACES = true
NATURAL RUSSIAN TECHNICAL PROSE = true
GENERATED / TEMPLATE FILLER = absent
MD / DOCX / PDF CONTENT EQUIVALENCE = PASS
PHYSICAL PDF / DOCX VISUAL QA = PASS
```

A PASS document should read like a competent specialist brief: concise, concrete and directly useful. It must not read like an audit log, policy memo or beginner tutorial.
