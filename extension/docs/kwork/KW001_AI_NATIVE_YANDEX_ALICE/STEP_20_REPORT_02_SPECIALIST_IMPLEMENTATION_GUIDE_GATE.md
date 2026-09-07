# KW-001 — Step 20 Report №02 specialist implementation-guide gate

Updated: 2026-09-07  
Status: **ACTIVE / UNIVERSAL / OWNER-APPROVED / OWNER-LOCKED**  
Scope: **Report №02 only — implementation guide for the specialist who will directly apply changes**

This gate defines the permanent recipient contract for Report №02. It does not mark any current job artifact PASS by itself.

---

## 1. Recipient and purpose

Recipient: the specialist who will directly apply the accepted changes to the site.

Report №02 is not a summary of the research and not an internal action database. It is an **implementation instruction**.

```text
REPORT №01
= explain what was researched, what was found and what it means to the commissioner

REPORT №02
= show the implementer exactly what is wrong, where it is wrong, why it matters, what to do, how it may look and how to verify the result

STANDALONE SEMANTIC CORE
= full working phrase / cluster / page dataset used alongside Report №02 when semantic detail is needed
```

The implementer must not need repository archaeology, internal project history or interpretation of machine codes in order to perform the work.

---

## 2. Language rule — internal invented English is forbidden in the client document

For a Russian Report №02, all terminology invented by the project, model, generator or internal schema must be shown in Russian.

```text
PROJECT-INVENTED TERM -> RUSSIAN CLIENT TERM
INTERNAL ENUM -> RUSSIAN CLIENT EXPLANATION
INTERNAL MODE NAME -> RUSSIAN CLIENT EXPLANATION
INTERNAL PRIORITY CODE -> RUSSIAN CLIENT EXPLANATION
INTERNAL READINESS CODE -> RUSSIAN CLIENT EXPLANATION
INTERNAL EVIDENCE ROUTE -> RUSSIAN CLIENT EXPLANATION
```

Latin/English is allowed only when it is genuinely necessary and comes from an external official/current source or is an unavoidable proper technical identifier, for example:

- official product or brand name;
- direct URL;
- official API/method/field name when the technical identifier itself is material;
- a professional term that is explicitly used by the current authoritative source and has no clearer Russian replacement for the recipient task.

A project-internal code does **not** become an allowed professional term merely because the recipient is a specialist.

Examples of the failure to prevent:

```text
CONTENT_BLOCK
SEMANTIC_MAPPING_ONLY
RECHECK_ONLY
READY_ANALYTICAL_MAPPING
NOT_READY__EVIDENCE_REQUIRED
P1_HIGH
REAL_SITE_CHANGE
```

These may remain in internal authorities and QA, but they must not appear in the client report at all. The same prohibition applies to project action IDs, source filenames and QA references even when they are labelled as technical detail.

```text
CLIENT REPORT = NO PROJECT-INTERNAL ACTION IDS / FILENAMES / QA IDS
INTERNAL TRACEABILITY BELONGS IN PROJECT EVIDENCE
```

```text
SPECIALIST RECIPIENT != PERMISSION TO DUMP INTERNAL SCHEMA
TECHNICAL PRECISION != INTERNAL ENGLISH ENUMS
```

---

## 3. Core difference from Report №01

Report №01 answers:

```text
WHAT WAS DONE?
WHAT WAS FOUND?
WHAT DOES IT MEAN?
```

Report №02 answers:

```text
WHAT EXACTLY MUST BE CHANGED?
ON WHICH PAGE?
WHAT IS WRONG NOW?
WHY IS IT WRONG / INCOMPLETE?
WHERE EXACTLY SHOULD THE CHANGE BE MADE?
WHAT STEPS SHOULD THE IMPLEMENTER TAKE?
WHAT MAY THE RESULT LOOK LIKE?
WHAT MUST NOT BE BROKEN OR INVENTED?
HOW DO WE VERIFY THAT THE CHANGE WAS IMPLEMENTED CORRECTLY?
```

Report №02 may use professional SEO/search/content terminology when it is genuinely useful, but it must remain normal Russian technical prose rather than a translated database export.

---

## 4. Every actionable deficiency must be a separate numbered implementation item

Do not compress actionable deficiencies merely because there are many of them.

```text
ONE MATERIAL IMPLEMENTATION DEFICIENCY / CHANGE
-> ONE NUMBERED IMPLEMENTATION ITEM
```

If there are 7 actions, show 7 items. If there are 37, show 37 items unless several are truly the same atomic change on the same object and can be executed/accepted together without losing meaning.

The implementer should be able to mark each numbered item independently as:

- done;
- not done;
- blocked;
- requires clarification.

A giant narrative paragraph containing several different changes is not acceptable.

---

## 5. Mandatory structure of every ready implementation item

For every real site change that is sufficiently supported to execute, include all material fields below in natural Russian.

### 5.1 Number and short action name

A concise action title that tells the implementer what must happen.

### 5.2 Exact page / object

Give the direct public URL whenever the work belongs to a concrete page.

If the work belongs to another exact object, identify it unambiguously.

### 5.3 What is wrong now

Explain the actual current deficiency in normal language.

Examples of acceptable deficiency descriptions:

- the page owns the correct search task but does not explain a material subtask;
- two pages have overlapping roles that require verification before any destructive change;
- the page lacks a necessary explanatory block;
- the navigation path does not expose a supported destination;
- the content makes a claim broader than current business evidence supports.

Do not write only an internal status or action label.

### 5.4 Why this is a problem

Explain the causal reason supported by the research:

- what user/search task is not fully answered;
- what ordinary Yandex evidence showed when material;
- what current-page/content evidence showed;
- what Alice/AI evidence added or did not add when material;
- why the proposed correction follows from that evidence.

This must be a real explanation, not a filename used as a substitute for reasoning.

### 5.5 Where exactly to change

Specify the implementable location when evidence supports it:

- after which existing block;
- before which form/calculator/section;
- inside which existing section;
- in which navigation element;
- on which exact page.

If the exact placement is not evidenced, do not invent it. Move the item to the blocked/clarification section instead of pretending it is implementation-ready.

### 5.6 Step-by-step implementation

Write concrete numbered implementation steps.

Example pattern:

1. Open the exact page.
2. Locate the stated block.
3. Preserve the listed existing content/element.
4. Insert/change the specified material.
5. Do not add unsupported company facts.
6. Verify the acceptance criteria.

Steps must describe the work, not internal analysis stages.

Every ready action must have its own action-specific sequence. Repeating a generic pattern such as “open page — preserve elements — add material — check limitations — check acceptance” does not satisfy this requirement. The steps must name the verified current headings/blocks, the exact insertion sequence, the content decision already made, the elements to preserve and the item-specific acceptance check. The implementer executes the decision and must not be left to repeat the analysis.

If an action classifies or filters existing objects, the report must supply the actual object-to-category mapping or a complete deterministic mapping rule covering every existing object. Any object that cannot be classified from evidence must have an explicit fallback or make the action not ready.

### 5.7 Example of how the result may look

When the task involves text/content, provide a practical example of the resulting fragment whenever evidence allows it.

If an exact current-page excerpt is available and safe to reproduce, the report may show a short relevant current fragment followed by the proposed version.

The proposed addition/change must be visually obvious.

For Markdown/source material, new wording should be highlighted in **bold** inside the example.

Example pattern:

```markdown
Current meaning:
«Замер и установка выполняются специалистами компании.»

Possible corrected fragment:
«Замер и установка выполняются специалистами компании. **Перед монтажом специалист проверяет проём и согласованную комплектацию. После установки выполняются регулировка конструкции и итоговая проверка работы двери.**»
```

The example is an implementation aid, not permission to invent business facts. Any company-specific inclusions, exclusions, warranties, materials, prices, terms or obligations require direct evidence.

If no exact wording is justified, say explicitly that the implementer must preserve the required meaning rather than copy fabricated prose.

### 5.8 What must be preserved

State what the specialist must not accidentally remove/change:

- correct page ownership;
- current useful block;
- current URL;
- existing price/calculator where relevant;
- supported claims;
- working navigation;
- supported page separation.

Positive `KEEP / NO CHANGE / DE-RISK` findings are implementation constraints, not missing work.

### 5.9 What must not be claimed or invented

Explicitly state any evidence boundary relevant to implementation.

Examples:

- do not promise an unconfirmed product/brand;
- do not state company-specific service inclusions without business confirmation;
- do not invent universal dimensions/norms;
- do not merge/delete/redirect pages when harm has not been proven;
- do not create a new page where the accepted result is semantic routing to an existing page.

### 5.10 Acceptance criteria

State how the implementer/recipient verifies that this exact item is complete.

Acceptance must test the requested implementation result, not merely that “content was edited”.

---

## 6. Partial / blocked items must not look ready

A finding may be valid while part of the implementation detail is unsupported.

Split the item into:

```text
WHAT IS ALREADY SUPPORTED AND MAY BE DONE
+
WHAT REQUIRES ADDITIONAL FACT / CHECK BEFORE PUBLICATION OR IMPLEMENTATION
```

For a blocked item explain:

1. the exact unresolved question;
2. why current evidence is insufficient;
3. what evidence/fact must be obtained;
4. what action becomes permissible after that evidence exists;
5. what must remain unchanged until then.

Do not attach a ready-looking text example to a claim whose factual content is not supported.

---

## 7. Separate physical site changes from analytical mapping

Report №02 must not make semantic/page mapping look like a site edit.

Use clear Russian sections such as:

- **Изменения сайта, готовые к внедрению**;
- **Можно выполнить частично — требуется подтверждение отдельных фактов**;
- **Семантические назначения — сайт физически не менять**;
- **Нужна дополнительная проверка — пока не внедрять**;
- **Потенциальные внутренние ссылки — не готовы без точного места и контекста**;
- **Что сохранить без изменений**.

Internal mode names may exist in technical evidence but must not be the visible client section names.

---

## 8. Recommended document architecture

Unless a current job requires an equally clear equivalent, Report №02 should be organized in this order.

### 8.1 What this document is and how to use it

Explain that:

- Report №02 is the implementation guide;
- the separate semantic-core workbook contains the full phrase/cluster/page data;
- the specialist should use the workbook when full semantic detail is needed rather than expecting all phrases to be repeated inside every implementation item.

### 8.2 Short technical explanation of how the implementation plan was obtained

Explain the research chain at a useful specialist level:

```text
site/business inventory
-> demand acquisition
-> targeted expansion when justified
-> cleanup/exclusions/deferred states
-> task/intent clustering
-> phrase-to-page/page ownership mapping
-> ordinary Yandex validation
-> Alice/AI validation when in scope
-> comparison/reconciliation
-> structural/content/navigation decision
-> implementation readiness
```

Use exact counts when they prove completeness or explain the funnel. Do not turn counts into the narrative itself.

### 8.3 Summary map of work

Before the detailed cards, show the recipient what categories exist:

- ready physical changes;
- partial changes;
- mapping-only results;
- blocked/recheck items;
- potential internal links requiring more detail;
- explicit no-change/preserve findings.

### 8.4 Ready physical changes

Put the work that can actually be implemented now first.

Each action gets the full implementation-item structure from Section 5.

### 8.5 Partial changes requiring business/detail confirmation

Keep supported content separate from unsupported company-specific facts.

### 8.6 Semantic assignments without physical site changes

Use a compact table or compact numbered register rather than repeating full implementation cards.

Recommended fields:

- topic/task;
- main page;
- supporting page when applicable;
- what the mapping means;
- explicit statement that no physical site change follows from this row;
- reference to the full semantic-core workbook for the complete phrase set.

### 8.7 Do not implement yet

Group overlap/cannibalization uncertainty, unconfirmed assortment/business facts, hold states and other evidence-blocked actions here.

Each item must state the blocker and the evidence required to reopen it.

### 8.8 Potential internal links

A proposed link is not implementation-ready until there is an exact source page/block/context, target, anchor meaning and conflict check.

If those details are absent, state clearly that the link is a candidate requiring clarification rather than a placement instruction.

### 8.9 What must remain unchanged

Give the specialist a compact preservation list:

- existing pages/owners that research supports;
- pages that should not be merged/deleted/redirected;
- tasks that should remain on existing pages;
- supported no-change/de-risk findings.

### 8.10 Verification after implementation

Explain how to confirm both:

- technical implementation acceptance;
- later search/analytics observation when relevant and available.

Do not promise traffic/revenue outcomes without evidence.

### 8.11 Materials used

This section is mandatory and must be the final substantive section of Report №02.

---

## 9. Do not duplicate the full semantic core inside every action card

If a standalone semantic-core workbook exists, long lists of all related phrases should not be repeated in every implementation item merely because they are available.

For a ready action, keep only what helps execution:

- cluster/topic name;
- main representative query when useful;
- a small number of illustrative queries when they clarify the user task;
- direct reference to the relevant sheet/view in the semantic-core workbook for the complete phrase set.

```text
FULL SEMANTIC DETAIL BELONGS IN THE SEMANTIC CORE
IMPLEMENTATION DETAIL BELONGS IN REPORT №02
```

This keeps Report №02 executable rather than enormous.

---

## 10. Evidence must be explained; technical traceability stays in project evidence

A filename such as an internal TSV/JSON/MD artifact is not an explanation of why the action is correct.

Primary client presentation:

```text
Основание решения:
plain-language explanation of the observed evidence and causal conclusion
```

Source filenames, stable project IDs and QA locators belong only in repository evidence. They are forbidden in the client-facing Markdown, DOCX and PDF. The specialist should understand the action without opening the internal artifact.

---

## 11. Priority must not masquerade as a production schedule

Report №02 may show analytical importance, but the wording must distinguish it from actual implementation scheduling.

Russian primary display example:

```text
Аналитический приоритет: высокий
```

An internal priority code is not necessary in the main document and, if retained for traceability, is secondary only.

```text
ANALYTICAL PRIORITY != COMMITTED IMPLEMENTATION ORDER
```

Do not invent `сейчас / потом / спринт / срок / трудоёмкость` without owner/implementer calibration.

---

## 12. Wordstat / demand explanation in Report №02

When demand data materially supports an action, explain the preserved metric once in the methodology/research-chain section and then use it consistently.

For Yandex Wordstat data, client-facing terminology must follow current official Yandex documentation for the relevant interface/method.

Do not call no-operator/broad observations exact phrase frequency or traffic forecast.

Do not present overlapping cluster sums as unique market volume.

The full phrase-level frequency detail belongs in the standalone semantic core when that artifact exists.

---

## 13. Alice / AI wording

Use the actual tested surface name and current official terminology.

Do not write as though Alice independently performed the research or authored the architecture decision.

Correct causal structure:

```text
research selected a case
-> Alice/AI output was observed
-> it was compared with the frozen Search-only decision
-> the comparison changed, confirmed, de-risked or failed to resolve a decision
```

When AI adds no implementation change, that is a valid result and should be expressed as a preservation/de-risk conclusion where relevant.

---

## 14. Mandatory final numbered list of materials used

The end of Report №02 must contain a numbered list of the external materials actually used to define/verify the work.

Each item must include:

1. material/article/document title;
2. publisher/source;
3. direct URL.

Example form:

```text
1. «Название материала» — Яндекс. https://...
2. «Название статьи» — Semrush. https://...
3. «Название материала» — Ahrefs. https://...
```

The list must include the materials actually used for the current project/research/method decisions, not every source ever seen by the project.

### 14.1 Freshness rule — sources must be revalidated for every project

A previous project source list is never copied blindly into a new project.

Before executing Report №02 for each new job:

1. perform fresh source/method review appropriate to the current task;
2. verify that each reused source still exists and remains current/relevant;
3. search for newer official/current guidance where the topic is time-sensitive or methodology has materially evolved;
4. keep a previously used source only if fresh review confirms it is still suitable;
5. remove sources that were not actually used in the current work;
6. add newly used sources.

```text
PREVIOUS PROJECT SOURCE LIST != CURRENT PROJECT SOURCE AUTHORITY
SAME URL MAY REAPPEAR ONLY AFTER FRESH REVALIDATION
```

The internal method/evidence record should preserve what each source influenced. The client report needs the clean final numbered bibliography with direct links.

---

## 15. Known failure classes to prevent

### Failure 1 — internal action database used as the report

**Symptom:** document opens with internal modes/statuses and then repeats one database-shaped card after another.

**Root cause:** internal execution representation was treated as recipient documentation.

**Correct control:** organize by implementer task and use Russian human-readable sections/cards.

### Failure 2 — action says what to do but not what is wrong

**Root cause:** final recommendation was copied without causal explanation.

**Correct control:** every ready action has `what is wrong -> why -> where -> steps -> example -> acceptance`.

### Failure 3 — evidence filename replaces evidence meaning

**Correct control:** explain observed evidence in normal language; filename is secondary traceability only.

### Failure 4 — huge phrase lists obscure implementation

**Correct control:** complete phrase sets stay in standalone semantic core; Report №02 keeps only execution-relevant examples/representatives.

### Failure 5 — unsupported company fact embedded in a ready text example

**Correct control:** split supported generic implementation from business-specific facts requiring confirmation.

### Failure 6 — analytical mapping presented as site work

**Correct control:** explicit separate section saying the site is not physically changed by these mappings.

### Failure 7 — potential internal link presented as ready

**Correct control:** exact source context/placement/target/anchor meaning required before implementation-ready status.

### Failure 8 — no-change result disappears

**Correct control:** include a preservation section so specialist knows what not to “improve”.

### Failure 9 — internal English/project codes treated as professional terminology

**Correct control:** only external official/current terminology or unavoidable proper technical identifiers may remain Latin/English; everything invented by the project is Russian in the client document.

### Failure 10 — same bibliography copied project to project

**Root cause:** method memory substituted for current method/source review.

**Correct control:** fresh source validation every job; old links survive only after current revalidation and actual use.

### Failure 11 — examples look authoritative despite insufficient evidence

**Correct control:** example text is supplied only within the supported factual boundary; otherwise give structure/meaning requirements and explicitly mark missing facts.

### Failure A — internal traceability leaked into client report

**What failed:** the report removed internal status codes but still exposed action IDs, internal filenames and QA references.

**Root cause:** secondary traceability was incorrectly treated as client-useful technical detail.

**Correct control:** the client report contains no project-internal action IDs, filenames or QA IDs. Repository evidence preserves them separately.

### Failure B — generic steps were presented as implementation steps

**What failed:** ready actions repeated nearly the same generic editing sequence.

**Root cause:** structured card completeness was confused with executable detail.

**Correct control:** every ready action has its own action-specific steps and leaves no actual editing sequence for the implementer to infer.

### Failure C — ambiguous placement in a ready action

**What failed:** placement used alternatives such as “before the calculator or request form”, “after disadvantages or in advice” and “after opening methods or profile comparison”.

**Correct control:** a ready implementation has one evidenced placement. If alternatives are all that evidence supports, downgrade the exact-placement claim or obtain a current-page read. Never invent a placement.

### Failure D — implementation analysis was left to the implementer

**What failed:** a filtering action named desired categories but did not map existing portfolio objects to them.

**Correct control:** classification/filtering instructions supply the object-to-category mapping or mark unresolved classification as not ready. The implementer executes the decision and does not repeat the research.

### Failure E — placeholder in a ready implementation example

**What failed:** a ready action contained an unresolved value such as `[дата проверки]`.

**Correct control:** ready client instructions contain no placeholders. Split a safe ready correction from a later evidence-dependent update when fresh facts are required.

### Failure F — numbering implied an implementation sequence

**What failed:** numbering was described as the required implementation order even though analytical priority is not a schedule.

**Correct control:** numbering is navigation and acceptance identification only. Actual sequencing requires owner/implementer calibration with resources, effort and dependencies where relevant.

### Failure G — duplicate link pair hidden by row-count QA

**What failed:** two authority rows produced an indistinguishable repeated source-to-target pair in the client table.

**Correct control:** authority row count is not the same as unique client link decisions. Validate `(source URL, target URL)` uniqueness. Consolidate an identical decision; if the same pair represents distinct contexts, show one pair with multiple reasons or clearly distinguish the subrows.

### Failure H — bibliography did not cover a material evidence surface

**What failed:** the report discussed Alice evidence without a current Alice/Yandex AI methodology or documentation source.

**Correct control:** every material external method or result surface discussed in the report has a current revalidated source when a public source exists. Bibliography completeness is semantic, not merely a minimum item count.

---

## 16. Report №02 PASS gate

Report №02 may pass only when:

```text
RECIPIENT = DIRECT IMPLEMENTER
DOCUMENT PURPOSE = IMPLEMENTATION GUIDE
CURRENT EXTERNAL METHOD / SOURCE REVIEW = PASS
SOURCE LIST FRESHLY REVALIDATED FOR THIS JOB = PASS
PROJECT-INVENTED CLIENT ENGLISH = 0
PROJECT-INTERNAL IDS IN CLIENT REPORT = 0
PROJECT-INTERNAL FILENAMES IN CLIENT REPORT = 0
PROJECT-INTERNAL ENUMS IN CLIENT REPORT = 0
CLIENT PLACEHOLDERS = 0
READY PHYSICAL CHANGES IDENTIFIABLE = true
EACH READY CHANGE HAS DIRECT PAGE/OBJECT = true where applicable
EACH READY CHANGE EXPLAINS CURRENT DEFECT = true
EACH READY CHANGE EXPLAINS WHY = true
EACH READY CHANGE HAS EXACT LOCATION = true where evidence supports implementation readiness
EACH READY CHANGE HAS STEP-BY-STEP ACTION = true
READY ACTION GENERIC STEP TEMPLATE REUSE = 0
CLASSIFICATION ACTIONS INCLUDE COMPLETE OBJECT-TO-CATEGORY DECISION = true
CONTENT CHANGES HAVE SAFE PRACTICAL EXAMPLE = true where evidence allows
PROPOSED ADDITIONS ARE VISUALLY DISTINGUISHABLE = true
UNSUPPORTED BUSINESS FACTS IN EXAMPLES = 0
WHAT TO PRESERVE IS EXPLICIT = true
ACCEPTANCE CRITERIA PRESENT = true
PARTIAL / BLOCKED ITEMS SEPARATED FROM READY = true
ANALYTICAL MAPPING SEPARATED FROM PHYSICAL SITE CHANGE = true
POTENTIAL LINKS WITHOUT EXACT CONTEXT PRESENTED AS READY = 0
VISIBLE LINK PAIRS UNIQUE OR EXPLICITLY DISTINGUISHED = true
UNEXPLAINED DUPLICATE VISIBLE LINK PAIRS = 0
FULL SEMANTIC CORE IS NOT REDUNDANTLY DUMPED INTO ACTION CARDS = true
EVIDENCE MEANING PRECEDES INTERNAL LOCATOR = true
ANALYTICAL PRIORITY NOT MISREPRESENTED AS SCHEDULE = true
NO-CHANGE / PRESERVE FINDINGS VISIBLE = true
FINAL NUMBERED MATERIALS LIST PRESENT = true
EACH MATERIAL HAS TITLE + SOURCE + DIRECT URL = true
MATERIALS LIST CONTAINS ONLY CURRENTLY USED / REVALIDATED SOURCES = true
BIBLIOGRAPHY COVERS EVERY MATERIAL EXTERNAL METHOD / RESULT SURFACE = true
NATURAL RUSSIAN TECHNICAL PROSE = true
GENERATED TEMPLATE FILLER = absent
OWNER / IMPLEMENTER TASK WALKTHROUGH = PASS
```

Report №02 must be directly executable. The implementer should be able to open the document, choose item 1, follow its steps on the linked page, compare the result with the supplied example/meaning, verify acceptance, then move to item 2 without reconstructing the research repository.
