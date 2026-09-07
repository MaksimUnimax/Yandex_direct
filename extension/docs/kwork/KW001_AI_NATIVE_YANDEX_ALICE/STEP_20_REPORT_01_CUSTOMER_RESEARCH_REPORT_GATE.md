# KW-001 — Step 20 Report №01 customer research-report gate

Updated: 2026-09-07  
Status: **ACTIVE / UNIVERSAL / REPORT-01-SPECIFIC NON-REPEAT CONTROL**  
Scope: **Report №01 only — customer-facing research report**

This gate records the permanent recipient rules learned from the repeated owner review of Report №01. It is stricter than a data-correctness check: the report must preserve the real research object, explain the completed workflow correctly, and translate analytical truth into a useful document for a non-specialist customer.

## 1. Research object must not be silently changed in the report

The sold work is an Alice-native rebuild / re-evaluation of the semantic/search core for modern Yandex Search.

```text
PRIMARY COMMERCIAL OBJECTIVE
= SEARCH / SEMANTIC CORE UNDER MODERN YANDEX SEARCH, INCLUDING ALICE

PRIMARY RESEARCH OBJECT
= SEARCH / SEMANTIC CORE + SEARCH DEMAND + QUERY-TO-PAGE DISTRIBUTION

USER INTENT / WHAT THE SEARCHER WANTS
= A CRITERION USED TO GROUP QUERIES AND SEPARATE DIFFERENT MEANINGS

GROUPING CRITERION
!= PRIMARY RESEARCH OBJECT
```

A report fails if it turns the completed semantic-core research into a different-sounding product such as “research of user tasks”, or if it reframes the Kwork as ordinary SEO with Alice checked only afterward.

Correct client logic should be equivalent to:

```text
SITE STUDIED
→ STARTING DEMAND DIRECTIONS FROZEN
→ WORDSTAT DEMAND COLLECTED FOR THE TARGET REGION
→ TARGETED GAPS EXPANDED
→ DUPLICATES / NOISE CLEANED
→ ACTIVE SEARCH PHRASES SELECTED
→ CLOSE PHRASES GROUPED BY MEANING / INTENT
→ QUERY GROUPS DISTRIBUTED ACROSS PAGES
→ ORDINARY YANDEX USED TO RESOLVE RELEVANT SEARCH BOUNDARIES
→ THE CORE / PAGE DISTRIBUTION EVALUATED AGAINST ALICE AS PART OF THE SOLD TASK
→ OVERALL ALICE-COMPATIBILITY CONCLUSION FOR THE SITE FORMED
→ SELECTED ALICE CASES USED FOR DEEPER CONTENT / DECISION REFINEMENT
→ PAGE / CONTENT DECISIONS PRODUCED
```

## 2. Wordstat counts must preserve their actual measurement meaning

A unique phrase count after deduplication must never be presented as a count of exact-frequency measurements unless that measurement was actually performed and preserved as evidence.

```text
UNIQUE SEARCH PHRASE COUNT
!= A DIFFERENT MEASUREMENT TYPE
```

For Report №01, explain **what was actually done**: phrases were collected for the target region together with the Wordstat demand/frequency indicator and then cleaned/deduplicated. Do not turn the client narrative into a list of measurements or procedures that were not performed unless their absence is a real limitation of the sold result.

Hard failure examples:

```text
"2 840 exact frequencies measured" without evidence
"exact-frequency operators were not used" presented as a client-facing pseudo-result when it is not a blocker
```

## 3. Recipient and purpose

The recipient is the Kwork customer, not an assumed owner, SEO specialist, editor or developer.

From Report №01 alone the customer should understand:

```text
WHAT WAS SOLD? = REBUILD / RE-EVALUATE THE CORE UNDER ALICE / MODERN YANDEX SEARCH
WHAT WAS RESEARCHED?
HOW WAS THE SEARCH CORE COLLECTED AND CLEANED?
HOW LARGE WAS THE FULL DEMAND SET?
HOW WERE QUERIES GROUPED AND DISTRIBUTED ACROSS PAGES?
WHAT DID ORDINARY YANDEX ADD?
HOW WAS THE CORE CHECKED AGAINST ALICE AS A CORE PART OF THE KWORK?
DOES THE SITE ALREADY MATCH ALICE OUTPUT WELL OR NOT?
WHY WERE SOME ALICE THEMES THEN CHECKED MORE DEEPLY?
WHAT DID THOSE DEEPER CHECKS REFINE?
WHAT ALREADY WORKS CORRECTLY?
WHAT SHOULD BE IMPROVED NOW AND WHY?
WHAT FACTS MUST THE COMPANY CONFIRM BEFORE THE REMAINING EDITS?
```

## 4. Client language must not expose internal project taxonomy

Do not make the customer learn internal classes or repository vocabulary.

Forbidden as client-facing structure or unexplained decision language:

```text
RELATED PAGES
FAMILY OWNER
STRUCTURAL UNIT
SEMANTIC MAPPING
CAUSAL DELTA
PROXY
READY / HOLD / RECHECK / SEARCH_REQUIRED
PENDING_BUSINESS_DETAIL
CONTROVERSIAL / DISPUTED FAMILIES
PARTIALLY READY WORK
CHANGES FORBIDDEN
```

Source-native brand names, product names and verbatim search strings are evidence and must be preserved in their native spelling.

## 5. Every ready recommendation must explain the reason

Every material recommendation must contain, explicitly or in unmistakably connected prose:

```text
WHAT WAS FOUND
WHY IT MATTERS
WHAT SHOULD BE CHANGED
WHERE
WHAT ALREADY WORKS AND SHOULD BE PRESERVED
WHAT THE RESULT SHOULD LOOK LIKE
HOW TO CHECK THE RESULT
```

A recommendation that only says what to edit is incomplete. Do not invent ranking, traffic, conversion or revenue promises that the evidence does not support.

## 6. Do not sell uncertainty or internal readiness states

Unknown facts must remain honest, but they must be translated into a concrete customer decision:

```text
WHAT IS ALREADY KNOWN
WHAT SPECIFIC FACT THE COMPANY MUST CONFIRM
WHY THAT FACT IS NEEDED
WHAT EDIT BECOMES POSSIBLE AFTER CONFIRMATION
WHETHER CURRENT READY WORK IS BLOCKED
```

Do not headline uncertainty as “partial readiness”, “hold”, “recheck”, “forbidden changes” or similar internal states.

## 7. Correct existing structure is positive value, not a negative pseudo-action

When the evidence confirms that the existing demand-to-page distribution already works, state that as a site-wide positive result for the customer. Do not prove it by listing a small catalogue of already-correct pages.

```text
GOOD: A MATERIAL PART OF THE CURRENT DEMAND-TO-PAGE DISTRIBUTION IS ALREADY CORRECT
GOOD: THE SITE IS ALREADY BROADLY SUITABLE FOR ORDINARY YANDEX AND ALICE
GOOD: WORK SHOULD FOCUS ON THE IDENTIFIED TARGETED IMPROVEMENTS
```

Do not turn this into main-plan pseudo-actions such as:

```text
DO NOT CREATE A PAGE
DO NOT CHANGE ARCHITECTURE
NO ACTION
CHANGES FORBIDDEN
```

A negative warning may appear only as a narrow guardrail inside a positive recommendation.

## 8. Do not invent a false opposite goal

Never explain the result by claiming that the project goal was “not to expand the site at any cost”, “not to create as many pages as possible”, or any other opposite strategy the customer never commissioned.

State the actual task and result directly.

## 9. Ordinary Yandex and Alice are both core evidence surfaces of the sold product

**Alice is not an additional or optional afterthought.** The Kwork exists because Yandex Search has changed: the search experience now includes both ordinary results and Alice-generated answers. The semantic core is being rebuilt / re-evaluated for that new reality.

Ordinary Yandex remains an important evidence surface for ambiguous query meaning, group borders and page roles. Alice is the second required surface against which the resulting semantic/page decisions are evaluated.

The report must first answer the product-level question:

```text
DOES THE EXISTING / REBUILT DEMAND-TO-PAGE DISTRIBUTION FIT ALICE OUTPUT?
IS THERE A SYSTEMIC ALICE-DRIVEN NEED TO CHANGE THE CORE / STRUCTURE?
OR IS THE SITE ALREADY BROADLY SUITABLE FOR ALICE AND ONLY TARGETED CONTENT CHANGES ARE NEEDED?
```

Only after that overall Alice-relevance conclusion is clear may the report describe the bounded selected Alice cases used to refine particular decisions or content blocks.

A bounded Alice diagnostic set is an **execution method**, not evidence that Alice was only “additionally checked”.

Hard failure client wording:

```text
ALICE WAS USED ONLY AS AN ADDITIONAL CHECK
AFTER THE MAIN SEO WORK WE ALSO LOOKED AT ALICE
ALICE WAS AN OPTIONAL EXTRA SOURCE
ONLY EIGHT ALICE QUERIES = THE ENTIRE ALICE VALUE OF THE PRODUCT
```

## 10. Report structure

Recommended connected structure:

```text
TASK: CORE UNDER ALICE / MODERN YANDEX
→ DIRECT RESULT FOR BOTH ORDINARY YANDEX AND ALICE
→ HOW THE SEMANTIC CORE WAS BUILT
→ WHAT ORDINARY YANDEX EVIDENCE ADDED
→ HOW THE RESULTING CORE / PAGE DISTRIBUTION CORRESPONDS TO ALICE
→ OVERALL ALICE-COMPATIBILITY VERDICT
→ WHY SELECTED ALICE CASES WERE THEN USED FOR DEEPER REFINEMENT
→ READY SITE IMPROVEMENTS WITH REASONS
→ AGGREGATE POSITIVE RESULT FOR WHAT ALREADY WORKS
→ SPECIFIC COMPANY FACTS NEEDED FOR NEXT EDITS
→ FINAL ANSWER TO THE KWORK
```

Main report = answer, reasoning and actions. Raw evidence registers stay in internal/specialist authorities unless they are specifically useful to this recipient.

## 11. Report №01 hard FAIL inventory

Any applicable item below causes recipient FAIL even if the underlying analysis is correct:

```text
KWORK_GOAL_NOT_ALICE_NATIVE
ALICE_REFRAMED_AS_ADDITIONAL_OR_OPTIONAL_AFTERTHOUGHT
ALICE_COMPATIBILITY_VERDICT_MISSING
SELECTED_ALICE_CASES_PRESENTED_AS_IF_THEY_WERE_THE_ENTIRE_ALICE_SCOPE/VALUE
SEMANTIC_CORE_RESEARCH_REFRAMED_AS_USER_TASK_RESEARCH
UNIQUE_PHRASE_COUNT_MISREPRESENTED_AS A DIFFERENT MEASUREMENT
NON_PERFORMED_PROCEDURE_DESCRIBED_AS CLIENT-FACING PSEUDO-RESULT
TARGETED_ORDINARY_YANDEX_COUNT_AMBIGUOUS_AS_TOTAL_RESEARCH_SCOPE
ALICE_CASE_COUNT_SHOWN_WITHOUT_SELECTION_LOGIC
ALICE_PRESENTED_AS RESEARCH AUTHOR
INTERNAL_TAXONOMY_EXPOSED_TO_CUSTOMER
RECOMMENDATION_WITHOUT_WHY
PARTIAL_READINESS_SOLD_AS_A_RESULT
CHANGES_FORBIDDEN_SOLD_AS_A_RESULT
DISPUTED_FAMILIES_USED_AS_CLIENT_SECTION
NEGATIVE_NO_ACTION_ITEMS_USED_AS_PRIORITY_TASKS
FALSE_OPPOSITE_GOAL_INVENTED
SOURCE_NATIVE_BRAND_OR_VERBATIM_QUERY_SPELLING_LOST
FULL_WORKFLOW_NOT_EXPLAINED_IN_CLIENT_LANGUAGE
MAIN_RESULT_HIDDEN_BEHIND_METHOD_OR_STATUS_COUNTS
```

## 12. PASS gate

Report №01 may pass only when:

```text
KWORK_GOAL_EXPLICITLY_ALICE_NATIVE = true
ALICE_IS_CORE_PRODUCT_SURFACE_NOT_ADDITIONAL_AFTERTHOUGHT = true
ALICE_COMPATIBILITY_SITE_VERDICT_VISIBLE = true
SELECTED_ALICE_CASES_EXPLAINED_AS_DEEPER_REFINEMENT_METHOD = true
SEMANTIC_CORE_IS_PRIMARY_RESEARCH_OBJECT = true
USER_INTENT_IS_GROUPING_CRITERION_NOT_RESEARCH_OBJECT = true
WORDSTAT_WORK_DESCRIBES_WHAT_WAS_DONE = true
NO_CLIENT_PSEUDO_RESULT_ABOUT_NON_PERFORMED_PROCEDURES = true
QUERY_TO_PAGE_DISTRIBUTION_VISIBLE = true
ORDINARY_YANDEX_SUBSET_RELATION_TO_FULL_SCOPE_VISIBLE = true
ALICE_SELECTION_AND_VALUE_CLEAR = true
RESEARCH_AGENCY_REMAINS_WITH_ANALYSIS_NOT_ALICE = true
READY_RECOMMENDATIONS_HAVE_FINDING_AND_WHY = true
POSITIVE_EXISTING_SITE_FINDINGS_VISIBLE_IN_AGGREGATE = true
UNRESOLVED_BUSINESS_FACTS_TRANSLATED_INTO_SPECIFIC_CONFIRMATIONS = true
NO_NEGATIVE_PSEUDO_ACTIONS_IN_MAIN_PLAN = true
NO_FALSE_OPPOSITE_GOAL = true
INTERNAL_STATUS_TAXONOMY_ABSENT_FROM_CLIENT_STRUCTURE = true
SOURCE_NATIVE_BRANDS_AND_VERBATIM_QUERIES_PRESERVED = true
FULL_WORKFLOW_EXPLAINED_IN_ORDINARY_LANGUAGE = true
OWNER / CUSTOMER WALKTHROUGH = PASS
```

## 13. Superseding owner corrections — final Report №01 presentation contract

The rules in this section supersede any older Report №01 wording that conflicts with them.

### 13.1 Site URL belongs in the title

The customer must see the researched site directly in the title. A project name without the site URL is not sufficient.

```text
REPORT_01_TITLE_CONTAINS_RESEARCHED_SITE_URL = true
```

### 13.2 Customer language uses search phrases, not storage-row vocabulary

Internal storage terminology such as `row`, `record`, field names or wire labels must not leak into the non-specialist report when the customer-facing meaning is simply a search phrase or a demand indicator.

```text
INTERNAL: 2415 rows
CUSTOMER: 2415 search phrases

INTERNAL: Wordstat field count
CUSTOMER: demand / frequency indicator returned with the phrase
```

Report №01 must not expose an English internal field name such as `count`.

### 13.3 Frequency work must be visible by describing completed work

The report must explain that Wordstat collection was performed for the target region and that the collected phrases carried a demand/frequency indicator. This is part of semantic-core work and must not disappear behind only logical/intent discussion.

Do **not** add a client-facing sentence about a frequency procedure that was not performed merely to defend methodology. Internal QA can preserve measurement semantics without making the customer read a list of omissions.

```text
DEMAND / FREQUENCY WORK VISIBLE = true
CLIENT_TEXT_DESCRIBES_COMPLETED_WORK = true
NON_PERFORMED_FREQUENCY_PROCEDURE_AS_PSEUDO_RESULT = false
```

### 13.4 Distinguish the commissioned rebuild goal from the site-specific outcome

The **commissioned goal** is to rebuild / re-evaluate the semantic core under Alice / modern Yandex Search.

The **site-specific outcome** may be that the existing core/structure already fits both ordinary Yandex and Alice well enough that a full replacement is unnecessary.

```text
COMMISSIONED_GOAL = CORE_UNDER_ALICE
SITE_RESULT = FULL_REPLACEMENT_MAY_NOT_BE_REQUIRED
```

Never turn the second statement into a replacement for the first.

### 13.5 Alice case count must come after the overall Alice result

Before the number of selected/deep Alice checks is stated, the report must establish:

```text
ALICE IS A CORE PART OF THE KWORK
THE SEMANTIC / PAGE DISTRIBUTION WAS EVALUATED AGAINST ALICE
THE OVERALL RESULT: SITE CORRESPONDS WELL / DOES NOT CORRESPOND WELL TO ALICE
ONLY THEN: WHICH THEMES WERE SELECTED FOR DEEPER ALICE REFINEMENT AND WHY
```

For OKNO_MSK, the intended narrative is:

```text
GENERAL ALICE-COMPATIBILITY RESULT = broadly positive; no systemic rebuild needed
DEEPER ALICE CANDIDATES = 25
FULL DEEP CHECKS = 8 = 6 decision-sensitive + 2 controls
PURPOSE OF 8 = refine specific content/page decisions after the overall Alice result, not define the whole Alice scope
```

A naked `25 -> 8` transition, or wording that makes those 8 look like the only Alice work/value, is FAIL.

### 13.6 Positive site result must be summarized, not turned into a catalogue of a few correct pages

For a non-specialist customer, Report №01 must not enumerate several already-correct pages merely to prove that positive checks existed. Such a list can falsely imply that only those pages were studied.

The main report should state the site-wide conclusion in aggregate form:

```text
A MATERIAL PART OF THE EXISTING DEMAND-TO-PAGE DISTRIBUTION IS ALREADY CORRECT
THE SITE IS ALREADY BROADLY SUITABLE FOR ORDINARY YANDEX AND ALICE
THEREFORE MASS RESTRUCTURING IS NOT REQUIRED
WORK SHOULD FOCUS ON THE IDENTIFIED TARGETED IMPROVEMENTS
```

Concrete URLs belong in ready recommendations or where a specific example is necessary to understand a material decision, not in a no-change catalogue.

### 13.7 The raw 75-query appendix is forbidden in Report №01

The 75 ordinary-Yandex observations remain preserved in internal evidence authorities. They must not be dumped into the customer report as a raw appendix.

Report №01 may state that 75 targeted checks were performed and explain why they were selected, but the raw observation register belongs to internal evidence / specialist materials.

```text
RAW_75_QUERY_APPENDIX_IN_REPORT_01 = FAIL
INTERNAL_75_QUERY_EVIDENCE_PRESERVED = true
```

### 13.8 Alice vocabulary for Report №01

The agreed customer-facing concept is `выдача Алисы`. Do not rotate between `AI`, `ИИ`, `generative`, `neural`, technical provider labels or other aliases in Report №01.

Technical names may remain in provenance/evidence files, but the customer report must use one stable ordinary-language name.

### 13.9 The Kwork goal is the core under Alice / the new search reality

This is the permanent non-negotiable product framing:

```text
ЦЕЛЬ КВОРКА
= ПЕРЕСОБРАТЬ / ПЕРЕПРОВЕРИТЬ ПОИСКОВОЕ ЯДРО ПОД АЛИСУ
= АДАПТИРОВАТЬ СЕМАНТИКУ ПОД НОВОЕ ВРЕМЯ, КОГДА ЧАСТЬ ВЫДАЧИ ЯНДЕКСА — ОТВЕТЫ АЛИСЫ
= ПРИ ЭТОМ СОХРАНИТЬ КОРРЕКТНОСТЬ ДЛЯ ОБЫЧНОЙ ВЫДАЧИ
```

Report №01 fails if Alice reads like a small comparison made after an otherwise complete ordinary-SEO study.

### 13.10 Updated hard FAILs

```text
SITE_URL_ABSENT_FROM_REPORT01_TITLE
RAW_STORAGE_ROW_TERM_USED_WHERE_CUSTOMER_MEANS_SEARCH_PHRASE
ENGLISH_INTERNAL_WORDSTAT_FIELD_NAME_EXPOSED
FREQUENCY_WORK_MISSING_FROM_WORKFLOW_NARRATIVE
NON_PERFORMED_PROCEDURE_WRITTEN_AS_IF_ITS_ABSENCE_WERE_A_DELIVERABLE
COMMISSIONED_ALICE_NATIVE_GOAL_REPLACED_BY_GENERIC_AUDIT_GOAL
ALICE_DESCRIBED_AS_ADDITIONAL_CHECK
ALICE_GENERAL_COMPATIBILITY_VERDICT_MISSING
ALICE_DEEP_CASE_COUNT_APPEARS_BEFORE_OVERALL_ALICE_RESULT
POSITIVE_RESULT_EXPANDED_INTO_SMALL_CATALOGUE_OF_ALREADY-CORRECT_PAGES
RAW_75_QUERY_APPENDIX_PRESENT_IN_REPORT_01
GENERATIVE / AI / NEURAL_ALIAS_USED_INSTEAD_OF_AGREED_ALICE_VOCABULARY
```

### 13.11 Updated PASS additions

```text
SITE_URL_VISIBLE_IN_TITLE = true
SEARCH_PHRASE_COUNTS_WRITTEN_AS_PHRASES_FOR_CUSTOMER = true
WORDSTAT_DEMAND_INDICATOR_EXPLAINED_IN_RUSSIAN = true
CLIENT_TEXT_FOCUSES_ON_COMPLETED_FREQUENCY_WORK = true
KWORK_GOAL_ALICE_NATIVE = true
ALICE_NOT_ADDITIONAL_AFTERTHOUGHT = true
GENERAL_ALICE_COMPATIBILITY_RESULT_VISIBLE_BEFORE_DEEP_CASES = true
DEEP_ALICE_CASES_POSITIONED_AS_REFINEMENT_AFTER_GENERAL_RESULT = true
POSITIVE_SITE_RESULT_SUMMARIZED_WITHOUT_NO-CHANGE_PAGE_CATALOGUE = true
RAW_75_QUERY_APPENDIX_ABSENT = true
ALICE_CUSTOMER_VOCABULARY_STABLE = true
```
