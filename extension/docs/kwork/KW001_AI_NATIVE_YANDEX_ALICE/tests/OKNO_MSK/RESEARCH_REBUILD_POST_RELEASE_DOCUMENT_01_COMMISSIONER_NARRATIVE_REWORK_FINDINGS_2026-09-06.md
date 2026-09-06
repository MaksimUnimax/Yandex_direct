# OKNO_MSK — Document №01 commissioner-narrative rework findings

Date: 2026-09-06
Status: **REWORK_REQUIRED / DOCUMENT_01_ONLY**

This file records the owner-directed defects found after the previous 10-page Document №01 rebuild. It is Level-2 job evidence and must not be generalized into current-job facts outside OKNO_MSK.

## Recipient correction

The report recipient is the **заказчик** of the Kwork. The report must not assume that the commissioner is the business owner, site owner, editor, SEO specialist or developer.

Previous wording equivalent to `для владельца сайта`, `для владельца бизнеса`, `owner-facing` is not valid client framing for this job unless a factual role is explicitly known.

## Main report contract

Document №01 must be understandable to an ordinary non-specialist commissioner and must answer the Kwork itself.

The connected client narrative must answer, in this order of meaning:

1. what was commissioned / what question was investigated;
2. what work was actually completed;
3. what the ordinary Yandex output showed;
4. what Alice added beyond the ordinary output;
5. whether the current site/page structure is generally correct or materially wrong relative to the researched demand;
6. what specifically needs to change and why;
7. what is already correct and should be preserved;
8. what two factual company inputs are still needed;
9. what the final answer to the Kwork is.

Meaningful sections are required. The report must **not** be flattened into a single wall of text. The defect is disconnected micro-section fragmentation and mechanical template repetition, not sectioning itself.

## New explicit defects to prevent

### D01-CN-01 — invented recipient role

FAIL: `owner`, `business owner`, `site owner` used as though the commissioner role were known.

Correction: neutral commissioner language; use `заказчик` only where naming the recipient is useful.

### D01-CN-02 — report does not answer the Kwork early enough

FAIL: first page starts with report meta-description, reading-time marketing or implementation counts before the overall research answer.

Correction: after the title, state the task and direct overall conclusion on the site relative to the researched demand, ordinary Yandex output and Alice output.

### D01-CN-03 — generated marketing heading

FAIL: `Главное за одну минуту` or any invented reading-time promise.

Correction: use a factual heading such as `Результат исследования` or write the opening conclusion without a decorative heading.

### D01-CN-04 — internal stage language

FAIL: `полный объём этого этапа`, `на этом этапе`, or any phrase that makes the commissioner ask `какого этапа?`.

Correction: name the actual work directly: `для проверки в Алисе были отобраны...`, `из 25 рассмотренных тем...`.

### D01-CN-05 — method / QA schema used as document outline

FAIL: one section per count or internal check (`why 75`, `why 8`, `34 results`, routing list) when these are only supporting details.

Correction: integrate counts into the meaningful narrative sections `Как проводилась работа`, `Что показала обычная выдача`, `Что добавила Алиса`.

### D01-CN-06 — number chain becomes the story

FAIL: `2840 → 2313 → 168 → 75 → 25 → 8 → 34` presented as a self-explanatory product result.

Correction: explain in prose what each number means, why the deeper subsets are smaller, and what decisions the deeper checks supported. A compact count summary may remain only as secondary reference.

### D01-CN-07 — ordinary-Yandex subset ambiguity

FAIL: 75 exact observations can be read as though only 75 requests were researched.

Correction: say that 2,840 accepted requests were analyzed semantically; 75 exact ordinary-Yandex outputs were used as targeted deeper checks where the result could confirm or change a page/task decision.

### D01-CN-08 — Alice subset misframed

FAIL: `8 checks are not the whole volume`.

Correction: the 8 Alice checks are the complete Alice verification performed for this job. Explain: 25 candidate themes reviewed; 6 decision-sensitive cases + 2 controls selected; 16 did not add a distinct decision type; 1 held.

### D01-CN-09 — surface/process terminology confusion

FAIL: `поиск` used where the report actually discusses the observed result surface.

Correction: client title and narrative use `обычная выдача Яндекса` and `выдача Алисы` where the observed output is meant.

### D01-CN-10 — multiple names for the same Alice surface

FAIL: alternating `Алиса`, `ИИ`, `AI`, `нейросетевой`, `генеративный` as if different systems were tested.

Correction: in Document №01 use `Алиса` consistently. Technical provenance remains in internal evidence files.

### D01-CN-11 — no direct overall site verdict

FAIL: report lists observations and changes but never plainly says whether the current page structure is generally appropriate for the researched demand.

Correction: state the evidence-bounded verdict directly: the current page structure is generally appropriate for the researched demand; no broad structural rebuild or mass new-page creation is justified by the completed research; the actionable gaps are concentrated in specific existing pages plus two fact-dependent edits.

### D01-CN-12 — Alice value described only as method

FAIL: report says Alice was checked but does not say what this changed for the Kwork answer.

Correction: state the cross-case result: Alice did not justify a structural rebuild; it refined the content required on several existing pages and confirmed stable page-role conclusions in control cases.

### D01-CN-13 — exhaustive no-change catalogue in main report

FAIL: 21 routing topics or 34-result dump included mainly to prove completeness.

Correction: retain only a short connected section on what is already correct; preserve exhaustive evidence in structured authorities / appendices.

### D01-CN-14 — cloned recommendation forms

FAIL: seven recommendations repeated with identical `Что обнаружено / Почему / Что изменить / Где / Что сохранить / Результат / Как проверить` form.

Correction: keep the reasoning content but write each recommendation as natural connected prose under a meaningful page/topic heading. Use a short implementation note or check only where useful.

### D01-CN-15 — generic defensive disclaimer section

FAIL: `Как использовать результаты без лишних выводов` in the main client report.

Correction: remove the generic section. Put a limitation next to the claim it actually limits only when necessary. Keep methodological guardrails in internal QA / specialist evidence.

### D01-CN-16 — generated / templated language accumulation

FAIL patterns observed in prior revision:

- fake reading-time promise;
- repeated generic transition phrases;
- repeated meta-description of the report itself;
- overly symmetrical mini-blocks;
- abstract corporate phrases instead of direct conclusions;
- repeated restatement of the same method/counts in opening and final section.

Correction: connected factual prose; semantic sections; natural sentence/paragraph variation driven by the actual finding; no decorative marketing copy.

### D01-CN-17 — final section repeats method instead of answering the Kwork

FAIL: final paragraph again recites counts and selection logic.

Correction: final section must state the actual research answer: overall state of the site relative to demand, what needs to change, what Alice added, and what remains fact-dependent.

## Required new Document №01 structure

The exact headings may change, but the meaning must follow this connected order:

```text
TITLE
→ TASK + DIRECT ANSWER TO THE KWORK
→ HOW THE WORK WAS CARRIED OUT
→ WHAT ORDINARY YANDEX OUTPUT SHOWED
→ WHAT ALICE ADDED
→ OVERALL CONCLUSION ABOUT CURRENT SITE / PAGE STRUCTURE
→ SPECIFIC CHANGES AND WHY
→ WHAT IS ALREADY CORRECT
→ TWO COMPANY FACTS STILL NEEDED
→ FINAL ANSWER
→ APPENDIX: 75 EXACT ORDINARY-YANDEX OBSERVATIONS
```

Semantic separation is mandatory. One undifferentiated text wall is also FAIL.

## Execution boundary

- Rebuild Document №01 only.
- Do not start Document №02.
- Do not start Document №03.
- Do not restart research stages.
- Do not make new Wordstat / ordinary Yandex / Alice / provider calls.
- Use preserved canonical evidence.
- Regenerate DOCX/PDF from corrected source; do not hand-edit the PDF.
- Run recipient QA and remote readback again.

Current status after these findings:

```text
CURRENT_DOCUMENT = 01
DOCUMENT_01_ANALYST_RECHECK = REOPENED__REWORK_REQUIRED
DOCUMENT_01_OWNER_REVIEW = REOPENED__REWORK_REQUIRED
DOCUMENT_02 = NOT_STARTED
DOCUMENT_03 = NOT_STARTED
NEXT_ACTION = REBUILD_DOCUMENT_01_AS_COMMISSIONER_FACING_CONNECTED_KWORK_REPORT
```