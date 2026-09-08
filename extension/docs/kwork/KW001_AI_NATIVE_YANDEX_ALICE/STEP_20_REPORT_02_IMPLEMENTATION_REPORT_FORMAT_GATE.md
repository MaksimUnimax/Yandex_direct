# KW-001 — Step 20 Report №02 implementation-report format gate

Updated: 2026-09-08
Status: ACTIVE / REPORT №02 / PERMANENT
Scope: client-facing structure and explanation quality of Report №02

This gate supplements:

- `STEP_20_REPORT_02_SPECIALIST_IMPLEMENTATION_GUIDE_GATE.md`
- `STEP_20_REPORT_02_SPECIALIST_IMPLEMENTATION_GUIDE_LAYOUT_GATE.md`

Despite legacy filenames, the client-facing document itself must be neutral and purpose-led.

## 1. Document title names the result, not the recipient role

Client title/header must describe what the document is for.

For the current OKNO_MSK contract the visible title is:

```text
Внедрение рекомендации
```

Client-facing role branding such as the following is forbidden unless a specific task genuinely requires a named role:

```text
руководство специалиста
для SEO-специалиста
для редактора
для разработчика
```

Permanent rule:

```text
DOCUMENT TITLE = PURPOSE / RESULT
DOCUMENT TITLE != RECIPIENT JOB TITLE
```

## 2. Main report is action-first

External implementation-report review is recorded in:

`tests/OKNO_MSK/RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_02_REPORT_FORMAT_REVIEW_2026-09-08.md`

The transferable rule is:

```text
MAIN REPORT
= WHAT TO CHANGE + WHY + HOW + EXPECTED RESULT

SUPPORTING DATA
= REFERENCE FOR IMPLEMENTATION / NEXT STEP
```

The implementation document must not read like a second research report or a raw database export.

## 3. Every non-obvious register must explain WHAT / WHY / HOW

Before a table/register whose meaning is not self-evident, the client report must explain in ordinary Russian:

1. **Что это** — what each row/column represents;
2. **Для чего** — why the data is useful;
3. **Как использовать / как внедрять** — what a person actually does with it.

A bare count plus a table is a failure.

## 4. Topic-to-page mapping must be understandable without SEO jargon

The 46 routing rows must be presented as **Распределение тем по страницам**.

The report must explain:

- a topic/user question is assigned to an existing page;
- the main page is where the topic is primarily disclosed;
- a related page may supplement the topic;
- the table is used when writing or updating content so the correct existing page is strengthened.

Preferred client columns:

```text
Тема / вопрос пользователя
Где раскрывать тему
Связанная страница
```

A phrase such as “использовать при ведении семантического ядра и контент-плана” is insufficient by itself.

## 5. Page-to-page link pairs must explain purpose and method

The 14 visible page pairs must be presented as understandable directions for internal transitions.

The report must explain:

- first page = where the transition starts;
- second page = where the visitor goes;
- why the transition is useful;
- how the exact paragraph and link wording are selected during implementation.

A bare instruction such as “определить блок, окружающий текст и формулировку ссылки” is a failure because it states missing detail without explaining the task.

Preferred client columns:

```text
Откуда ведём
Куда ведём
```

## 6. No standalone defensive preservation section

A standalone section equivalent to:

```text
Требования к существующей структуре
Что нельзя менять
Что не делать
```

is forbidden in the client document.

A material preservation requirement belongs only inside the concrete recommendation where it is needed for correct acceptance.

## 7. Additional checks must explain the decision they support

For each unresolved structural/content question, the report must state:

```text
WHAT MUST BE UNDERSTOOD
WHY IT MATTERS
HOW TO CHECK
WHAT DECISION FOLLOWS
```

The reader must understand the purpose of the check even without professional SEO knowledge.

## 8. Research-method detail is secondary

Report №01 carries the full research narrative.
Report №04 carries the detailed phrase/data workbook.

Report №02 may show only the minimum research context needed to understand the action plan.

Do not lead Report №02 with a long collection/clustering/provider funnel when that information does not help implementation.

## 9. Known failure classes added by owner review

### Failure Q — recipient role used as the document identity
The report was titled as a specialist/SEO deliverable instead of naming the result.

### Failure R — 46-row routing table had no plain-language operational meaning
The reader could not understand what the table was for or how to use it.

### Failure S — 14 page pairs were presented as unexplained technical candidates
The reader could not understand what the pair meant, why the link was useful or how it would be implemented.

### Failure T — standalone “Требования к существующей структуре” section
A defensive preservation list occupied client space without advancing implementation.

### Failure U — implementation report reproduced research framing instead of an action plan
The document mixed findings, raw registers and internal workflow instead of prioritizing recommendations and usable next steps.

## 10. PASS gate

Report №02 may pass only when:

```text
VISIBLE TITLE = Внедрение рекомендации
CLIENT ROLE-BRANDING HITS = 0
ACTION-FIRST STRUCTURE = true
READY RECOMMENDATIONS ARE EXPLAINED = true
CLARIFICATION ITEMS NAME A CONCRETE ANSWER NEEDED = true
TOPIC-TO-PAGE TABLE HAS WHAT/WHY/HOW EXPLANATION = true
TOPIC-TO-PAGE COLUMNS ARE PLAIN RUSSIAN = true
PAGE-LINK TABLE HAS WHAT/WHY/HOW EXPLANATION = true
PAGE-LINK COLUMNS ARE PLAIN RUSSIAN = true
ADDITIONAL CHECKS HAVE PURPOSE + METHOD + DECISION = true
STANDALONE PRESERVATION SECTION = absent
RAW RESEARCH FUNNEL DOMINATING REPORT = absent
NON-SPECIALIST OWNER CAN EXPLAIN SECTIONS 4-6 = true
MD / DOCX / PDF CONTENT EQUIVALENCE = PASS
FINAL PDF VISUAL READBACK = PASS
```
