# KW-001 — Step 20 Report №01 customer research-report gate

Updated: 2026-09-06  
Status: **ACTIVE / UNIVERSAL / REPORT-01-SPECIFIC NON-REPEAT CONTROL**  
Scope: **Report №01 only — customer-facing research report**

This gate records the permanent recipient rules learned from the repeated owner review of Report №01. It is stricter than a data-correctness check: the report must preserve the real research object, explain the completed workflow correctly, and translate analytical truth into a useful document for a non-specialist customer.

## 1. Research object must not be silently changed in the report

When the sold work is a rebuild of a semantic/search core and distribution of search demand across pages, Report №01 must say exactly that.

```text
PRIMARY RESEARCH OBJECT
= SEARCH / SEMANTIC CORE + SEARCH DEMAND + QUERY-TO-PAGE DISTRIBUTION

USER INTENT / WHAT THE SEARCHER WANTS
= A CRITERION USED TO GROUP QUERIES AND SEPARATE DIFFERENT MEANINGS

GROUPING CRITERION
!= PRIMARY RESEARCH OBJECT
```

A report fails if it turns the completed semantic-core research into a different-sounding product such as “research of user tasks” merely because intent was used during clustering.

Correct client logic should be equivalent to:

```text
SITE STUDIED
→ STARTING DEMAND DIRECTIONS FROZEN
→ WORDSTAT DEMAND COLLECTED
→ TARGETED GAPS EXPANDED
→ DUPLICATES / NOISE CLEANED
→ ACTIVE SEARCH FORMULATIONS SELECTED
→ CLOSE FORMULATIONS GROUPED BY MEANING / INTENT
→ QUERY GROUPS DISTRIBUTED ACROSS PAGES
→ AMBIGUOUS BORDERS CHECKED IN ORDINARY YANDEX
→ SELECTED MATERIAL DECISIONS CHECKED AGAINST ALICE-BASED ANSWERS
→ PAGE / CONTENT DECISIONS PRODUCED
```

## 2. Wordstat counts must preserve their actual measurement meaning

A unique phrase count after deduplication must never be presented as a count of exact-frequency measurements unless exact-frequency operators were actually used and preserved as evidence.

```text
UNIQUE SEARCH FORMULATION COUNT
!= EXACT-FREQUENCY MEASUREMENT COUNT

BROAD WORDSTAT DISCOVERY ROW WITH A NUMERIC COUNT
!= SEPARATE OPERATOR-EXACT FREQUENCY MEASUREMENT
```

If the acquisition used broad discovery mode, the customer report must explain that the numeric Wordstat values belong to the returned rows, while the post-cleanup phrase total is the number of unique formulations after deduplication.

Hard failure examples:

```text
"2 840 exact queries" when 2 840 means unique phrase keys
"2 840 exact frequencies measured" without exact-operator evidence
```

## 3. Recipient and purpose

The recipient is the Kwork customer, not an assumed owner, SEO specialist, editor or developer.

From Report №01 alone the customer should understand:

```text
WHAT WAS RESEARCHED?
HOW WAS THE SEARCH CORE COLLECTED AND CLEANED?
HOW LARGE WAS THE FULL DEMAND SET?
HOW WERE QUERIES GROUPED AND DISTRIBUTED ACROSS PAGES?
WHY WAS ONLY A SUBSET CHECKED MANUALLY IN ORDINARY YANDEX?
WHY WERE ONLY SELECTED THEMES CHECKED WITH ALICE-BASED ANSWERS?
WHAT DID THOSE CHECKS CONFIRM OR REFINE?
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

When the evidence confirms that an existing page or pair of pages already has the right role, say so positively.

```text
GOOD: EXISTING PAGE REMAINS THE MAIN PAGE FOR THIS DEMAND
GOOD: BOTH EXISTING PAGES HAVE DISTINCT VERIFIED ROLES
GOOD: CURRENT STRUCTURE IS SUPPORTED; BUDGET SHOULD GO TO THE IDENTIFIED CONTENT IMPROVEMENT
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

## 9. Ordinary Yandex and Alice-based answers have different evidence roles

Ordinary Yandex is used selectively to resolve ambiguous query meaning, group borders and page roles that cannot be confidently resolved from the query wording and current site alone.

Alice-based answers in Yandex are an additional selected verification layer. They do not replace the semantic-core analysis and must not be presented as the author of the research conclusion.

The report must explain:

```text
SUBSET OF WHAT FULL SCOPE?
WHY THESE CASES WERE SELECTED?
WHAT COULD THE CHECK CHANGE OR CONFIRM?
WHAT DID THE ORDINARY YANDEX / ALICE-BASED ANSWER ADD?
HOW DID THAT AFFECT THE SITE DECISION?
```

A targeted validation subset must never look like the total amount of research performed.

## 10. Report structure

Recommended connected structure:

```text
TASK
→ DIRECT RESULT
→ HOW THE SEMANTIC CORE WAS BUILT
→ WHAT ORDINARY YANDEX VALIDATION ADDED
→ WHAT THE SELECTED ALICE-BASED CHECKS ADDED
→ READY SITE IMPROVEMENTS WITH REASONS
→ WHAT ALREADY WORKS CORRECTLY
→ SPECIFIC COMPANY FACTS NEEDED FOR NEXT EDITS
→ FINAL ANSWER
→ SUPPORTING APPENDIX
```

Main report = answer, reasoning and actions. Appendix = detailed supporting observations.

## 11. Report №01 hard FAIL inventory

Any applicable item below causes recipient FAIL even if the underlying analysis is correct:

```text
SEMANTIC_CORE_RESEARCH_REFRAMED_AS_USER_TASK_RESEARCH
UNIQUE_PHRASE_COUNT_MISREPRESENTED_AS_EXACT_FREQUENCY_COUNT
BROAD_WORDSTAT_DISCOVERY_MISREPRESENTED_AS_EXACT_OPERATOR_MEASUREMENT
TARGETED_ORDINARY_YANDEX_COUNT_AMBIGUOUS_AS_TOTAL_RESEARCH_SCOPE
ALICE_CASE_COUNT_SHOWN_WITHOUT_SELECTION_LOGIC
ALICE_PRESENTED_AS RESEARCH AUTHOR
INTERNAL TAXONOMY EXPOSED TO CUSTOMER
RECOMMENDATION_WITHOUT WHY
PARTIAL_READINESS SOLD AS A RESULT
CHANGES_FORBIDDEN SOLD AS A RESULT
DISPUTED_FAMILIES USED AS CLIENT SECTION
NEGATIVE_NO_ACTION ITEMS USED AS PRIORITY TASKS
FALSE_OPPOSITE_GOAL INVENTED
SOURCE_NATIVE_BRAND OR VERBATIM QUERY SPELLING LOST
FULL WORKFLOW NOT EXPLAINED IN CLIENT LANGUAGE
MAIN RESULT HIDDEN BEHIND METHOD OR STATUS COUNTS
```

## 12. PASS gate

Report №01 may pass only when:

```text
SEMANTIC_CORE_IS_PRIMARY_RESEARCH_OBJECT = true
USER_INTENT_IS_GROUPING_CRITERION_NOT_RESEARCH_OBJECT = true
WORDSTAT_MEASUREMENT_MODE_EXPLAINED_CORRECTLY = true
UNIQUE_PHRASE_COUNTS_NOT_MISLABELED_AS_EXACT_FREQUENCY = true
QUERY_TO_PAGE_DISTRIBUTION_VISIBLE = true
ORDINARY_YANDEX_SUBSET_RELATION_TO_FULL_SCOPE_VISIBLE = true
ALICE_SELECTION_AND_VALUE_CLEAR = true
RESEARCH_AGENCY_REMAINS_WITH_ANALYSIS_NOT_ALICE = true
READY_RECOMMENDATIONS_HAVE_FINDING_AND_WHY = true
POSITIVE_EXISTING_SITE_FINDINGS_VISIBLE = true
UNRESOLVED_BUSINESS_FACTS_TRANSLATED_INTO SPECIFIC_CONFIRMATIONS = true
NO_NEGATIVE_PSEUDO_ACTIONS_IN_MAIN_PLAN = true
NO_FALSE_OPPOSITE_GOAL = true
INTERNAL_STATUS_TAXONOMY_ABSENT_FROM CLIENT STRUCTURE = true
SOURCE_NATIVE_BRANDS_AND_VERBATIM_QUERIES_PRESERVED = true
FULL_WORKFLOW_EXPLAINED_IN ORDINARY LANGUAGE = true
OWNER / CUSTOMER WALKTHROUGH = PASS
```
