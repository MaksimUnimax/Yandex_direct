# KW-001 — Step 20 Report №01 customer research-report gate

Updated: 2026-09-06  
Status: **ACTIVE / UNIVERSAL / REPORT-01-SPECIFIC NON-REPEAT CONTROL**  
Scope: **Report №01 only — customer-facing research report**

This gate records what the first report must look like after the owner-directed post-release rework. These rules belong to Report №01 unless a separate report-specific authority explicitly promotes a subset as shared.

## 1. Recipient and purpose

The recipient is the **customer / заказчик of the Kwork**, not an assumed business owner, site owner, editor, developer or SEO specialist.

Report №01 must answer the sold research task itself. A non-specialist customer should understand from this document alone:

```text
WHAT WAS THE KWORK TASK?
WHAT WORK WAS ACTUALLY DONE?
HOW LARGE WAS THE RESEARCH?
HOW WAS DEMAND CLEANED / GROUPED / CHECKED?
WHAT DID ORDINARY YANDEX OUTPUT ADD?
WHAT DID THE ALICE OUTPUT CHECK ADD?
IS THE CURRENT SITE GENERALLY WELL OPTIMIZED FOR THE RESEARCHED DEMAND?
WHAT IS ALREADY CORRECT?
WHAT NEEDS TO CHANGE?
WHY DOES IT NEED TO CHANGE?
WHAT STILL REQUIRES A FACT FROM THE COMPANY?
```

## 2. Direct answer to the Kwork must be visible early

The report must not hide the main answer behind methodology or internal classifications.

When the evidence supports it, the customer-facing verdict should directly state whether the site is already well optimized for the researched demand in both compared Yandex surfaces.

For work that explicitly compares ordinary Yandex output and Alice output, the final report should answer the combined question, for example:

```text
THE SITE IS ALREADY WELL OPTIMIZED FOR THE RESEARCHED DEMAND
UNDER ORDINARY YANDEX OUTPUT
AND UNDER ALICE OUTPUT
```

This claim must remain bounded by the actual research. It does not mean a guaranteed ranking, traffic or revenue result.

A report that discusses ordinary Yandex and Alice separately but never gives the customer the combined optimization verdict fails the sold Kwork.

## 3. Research agency must remain with the analyst, not Alice

The work is performed by the research process and analyst. Alice is one checked result surface / evidence source.

```text
ANALYST / RESEARCH PROCESS PERFORMS THE STUDY
ALICE OUTPUT IS EVIDENCE USED IN THE STUDY
ALICE != AUTHOR OF THE SITE CONCLUSION
```

Avoid wording that makes it sound as if the customer paid only to ask a neural assistant for an answer:

```text
BAD: "Алиса показала, что страницу нужно изменить"
BAD: "Алиса решила, какая страница правильная"
BAD: "Алиса дала вывод по структуре сайта"
```

Prefer wording that preserves research agency:

```text
GOOD: "проверка выдачи Алисы показала..."
GOOD: "сравнение с выдачей Алисы подтвердило..."
GOOD: "в выдаче Алисы сохранился тот же пользовательский сценарий..."
GOOD: "сопоставление обычной выдачи с выдачей Алисы помогло уточнить..."
```

The customer should understand that conclusions came from the combined analysis of demand, current pages, ordinary Yandex output and the selected Alice-output checks.

## 4. Correct narrative structure learned from the accepted rewrite

Report №01 should be built as a connected answer, not as an export of the internal database.

Recommended high-level logic:

```text
KWORK TASK
→ DIRECT RESEARCH RESULT
→ HOW THE WORK WAS DONE
→ WHAT ORDINARY YANDEX OUTPUT SHOWED
→ WHAT THE ALICE-OUTPUT CHECK ADDED
→ WHAT TO CHANGE ON THE SITE
→ WHAT IS ALREADY CORRECT
→ WHAT FACTS ARE STILL NEEDED
→ FINAL ANSWER
→ SUPPORTING APPENDIX
```

Meaningful sections are mandatory. A single text wall is a failure. The failure is also the opposite extreme: many disconnected micro-blocks or identical mini-forms that destroy the narrative.

## 5. The full work must be explained in ordinary language

The customer must see that substantial research was performed, but the explanation should remain understandable without specialist vocabulary.

The narrative should explain the real progression:

```text
SITE STUDIED
→ DEMAND COLLECTED
→ NOISE / IRRELEVANT REQUESTS REMOVED OR DEFERRED
→ REQUESTS GROUPED BY USER TASK
→ TASKS MAPPED TO EXISTING PAGES
→ AMBIGUOUS / MATERIAL CASES CHECKED IN ORDINARY YANDEX OUTPUT
→ MATERIAL CASES SELECTED FOR ALICE OUTPUT CHECK
→ RESULTS COMPARED
→ SITE CONCLUSIONS AND RECOMMENDATIONS PRODUCED
```

Counts should be shown when they help the customer understand scale or selection. Every count must be explained: what it counts, how it relates to the previous count, and why a smaller subset was checked more deeply.

## 6. Ordinary Yandex and Alice must have clear, different roles

Ordinary Yandex output is used to validate how specific queries are represented in the real search result surface and to resolve ambiguous user tasks or page roles.

Alice output is used selectively where it can add, challenge or refine a material conclusion.

The report must explain why the Alice checks were selected and why the selected set is sufficient for the research question. If the executed Alice set is complete for the job, it must not be described as an incomplete fragment.

## 7. Alice must be visible as part of the sold product

When Alice is a differentiator of the Kwork, it must be visible in:

- the title or first screen;
- the description of completed work;
- the combined site verdict;
- the explanation of what extra value the comparison added;
- the final answer.

Do not alternate `Алиса`, `ИИ`, `AI`, `нейросетевой поиск`, `генеративный поиск` as if different systems were tested. Use the job-approved customer-facing name consistently.

## 8. Recommendations must read as real reasoning

Each recommendation must make the logic understandable:

```text
CURRENT PAGE / CURRENT SITUATION
→ SPECIFIC PROBLEM
→ WHY IT MATTERS TO THE USER / SEARCH TASK
→ WHAT TO CHANGE
→ WHAT THE RESULT SHOULD BECOME
```

Report №01 should not mechanically repeat the same implementation-ticket field labels for every recommendation. Natural connected prose under meaningful topic headings is preferred.

The detailed specialist action schema belongs to Report №02.

## 9. Positive findings are part of the paid result

If the research confirms that current page roles or site structure are already correct, say so clearly. The customer paid not only to find problems but also to learn what does **not** need rebuilding.

Do not inflate the report with a long no-change catalogue. Summarize the positive structural result and show only the examples needed to understand the conclusion.

## 10. Evidence detail belongs in the right place

Exact-query evidence, large observation tables and completeness ledgers should remain available, but they do not need to dominate the main narrative.

```text
MAIN REPORT = ANSWER + REASONING + ACTIONS
APPENDIX = DETAILED SUPPORTING EVIDENCE
```

A detailed appendix is appropriate when it proves the work without forcing the customer to read every raw row before understanding the result.

## 11. Report №01 failure inventory

The following failures were observed during repeated rework of the first report and are Report-01-specific non-repeat controls:

```text
DATE / VERSION METADATA OCCUPIES FIRST SCREEN
ALICE DIFFERENTIATOR ABSENT FROM TITLE
"GENERATIVE" / "NEURAL" TERMS USED BEFORE CLIENT MEANING
SEARCH PROCESS NAMED WHEN THE OBSERVED OUTPUT SURFACE IS MEANT
ALICE / AI / ИИ LABELS MIXED
SELECTIVE ALICE COUNT SHOWN WITHOUT SELECTION REASON
COMPLETE ALICE CHECK MISDESCRIBED AS "NOT THE WHOLE RESEARCH"
UNDEFINED INTERNAL "STAGE" LANGUAGE
TARGETED ORDINARY-YANDEX COUNT SHOWN WITHOUT RELATION TO TOTAL DEMAND
VAGUE "WHOLE ARRAY" INSTEAD OF EXACT SCOPE
FULL WORKFLOW NOT EXPLAINED
PAGE-ROUTING RESULTS PRESENTED AS CUSTOMER TASKS
LONG NO-CHANGE CATALOGUE DOMINATES REPORT
INTERNAL STATUS / QA DUMP USED AS REPORT OUTLINE
GENERIC "HOW TO USE RESULTS" DISCLAIMER SECTION
ASSUMED OWNER ROLE INSTEAD OF CUSTOMER
FAKE READING-TIME HEADING SUCH AS "IN ONE MINUTE"
RECOMMENDATIONS WRITTEN AS CLONED FORMS
NO DIRECT SITE / STRUCTURE VERDICT
NO DIRECT DUAL-SURFACE OPTIMIZATION VERDICT WHEN THE KWORK REQUIRES IT
ALICE DESCRIBED AS IF IT PERFORMED THE WHOLE RESEARCH
ALICE CONTRIBUTION DESCRIBED ONLY AS METHOD, NOT AS EFFECT ON THE RESULT
FINAL SECTION REPEATS COUNTS INSTEAD OF ANSWERING THE KWORK
```

## 12. PASS gate for Report №01

Report №01 may pass only when:

```text
RECIPIENT = CUSTOMER / ЗАКАЗЧИК
KWORK_TASK_VISIBLE = true
DIRECT_RESEARCH_ANSWER_VISIBLE_EARLY = true
DUAL_SURFACE_OPTIMIZATION_VERDICT_VISIBLE_WHEN_SUPPORTED = true
RESEARCH_AGENCY_REMAINS_WITH_ANALYSIS_NOT_ALICE = true
SEMANTIC_SECTIONS = clear
CONNECTED_NARRATIVE = true
FULL_WORKFLOW_EXPLAINED_IN_ORDINARY_LANGUAGE = true
COUNTS_EXPLAINED_IN_CONTEXT = true
ORDINARY_YANDEX_ROLE_CLEAR = true
ALICE_SELECTION_AND_VALUE_CLEAR = true
ALICE_SINGLE_CLIENT_NAME = true
READY_RECOMMENDATIONS_HAVE_REASONING = true
POSITIVE_EXISTING_SITE_RESULT_VISIBLE = true
DETAIL_EVIDENCE_MOVED_TO_APPENDIX_WHEN_NEEDED = true
GENERATED_TEMPLATE_PRESENTATION = absent
FINAL_SECTION_ANSWERS_KWORK = true
```
