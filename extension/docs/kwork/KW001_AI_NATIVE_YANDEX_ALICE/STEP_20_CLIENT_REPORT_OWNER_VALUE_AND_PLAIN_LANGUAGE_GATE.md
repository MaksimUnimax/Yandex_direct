# KW-001 — Step 20 client-report owner-value and plain-language gate

Updated: 2026-09-06  
Status: **ACTIVE / UNIVERSAL / PERMANENT NON-REPEAT CONTROL**  
Scope: **Step 19 materialization + Step 20 recipient acceptance / Level 1**

This gate prevents a client research report from passing merely because it is analytically correct, complete, Russian-language and traceable. A client report must also be understandable, decision-oriented and commercially usable by a non-specialist owner.

Concrete client domains, URLs, query counts, action IDs, brands and current-job findings are forbidden in this Level-1 gate.

## 1. Failure class — internal analytical framing leaked into a client product

A report may contain correct facts and still fail the sold client experience when it presents the work as an internal audit log, uncertainty ledger, prohibited-action list or taxonomy of analytical states.

```text
ANALYTICAL CORRECTNESS
!= CLIENT VALUE COMMUNICATION

RUSSIAN WORDS
!= NON-SPECIALIST LANGUAGE

FULL DECISION MAP
!= ACTION PLAN WRITTEN FOR AN OWNER

UNCERTAINTY PRESERVED
!= UNCERTAINTY SHOULD LEAD THE SALES/CLIENT NARRATIVE
```

The owner must be able to understand what was learned, why it matters, what is worth doing, what is already good, what requires one missing fact before implementation, and where spending is unnecessary.

## 2. Executive-summary value gate

The executive summary must lead with useful conclusions, not with internal uncertainty, prohibitions, counts of analytical states or descriptions of the research production process.

The first screen/page should answer in ordinary language:

```text
WHAT IS ALREADY WORKING WELL
WHAT THE RESEARCH FOUND THAT IS WORTH IMPROVING
WHICH IMPROVEMENTS HAVE THE HIGHEST PRACTICAL PRIORITY
WHAT CAN BE IMPLEMENTED NOW
WHAT REQUIRES ONE SPECIFIC CONFIRMATION BEFORE IMPLEMENTATION
WHERE THE RESEARCH SAVED THE CLIENT FROM UNNECESSARY WORK / DUPLICATION
```

Do not lead with headings or summary language equivalent to:

```text
PARTIALLY READY WORK
CHANGES FORBIDDEN
CONTROVERSIAL / DISPUTED FAMILIES
UNRESOLVED STATES
HOLD / RECHECK / SEARCH_REQUIRED
NO-ACTION COUNT
ANALYTICAL-MAPPING COUNT
```

Those states may remain in internal authority and QA. In the client report they must be translated into owner decisions and placed only where materially needed.

## 3. Uncertainty must be converted into a decision, not sold as a product feature

Do not hide uncertainty or invent certainty. Instead convert every material unresolved point into a client-usable structure:

```text
WHAT IS ALREADY KNOWN
WHAT DECISION CAN BE MADE NOW
WHAT SINGLE FACT / CHECK IS STILL NEEDED, IF ANY
WHY THAT FACT MATTERS
WHAT THE OWNER SHOULD DO NEXT IF THEY WANT TO CONTINUE THIS ITEM
WHETHER IT BLOCKS ANY CURRENT READY WORK
```

Client-facing wording should prefer concepts such as:

```text
REQUIRES CONFIRMATION BEFORE IMPLEMENTATION
CAN BE DECIDED AFTER BUSINESS DETAIL IS CONFIRMED
CURRENT STRUCTURE IS VALIDATED; ADDITIONAL WORK IS NOT JUSTIFIED NOW
ADDITIONAL DATA IS NEEDED BEFORE ALLOCATING BUDGET
```

Do not create a headline section whose primary product value is "uncertainty", "forbidden changes", "partial readiness" or equivalent negative/internal state framing.

## 4. Non-specialist vocabulary gate

The intended owner must not need SEO, information-architecture, semantic-clustering or internal-project vocabulary to understand the report.

Every client-facing concept must satisfy one of these:

1. ordinary business language is used directly; or
2. an unavoidable specialist term is immediately explained in ordinary language before it is used for a decision.

Do not use unexplained abstractions such as:

```text
RELATED PAGES
FAMILY OWNER
STRUCTURAL UNIT
SEMANTIC MAPPING
ARCHITECTURE CHANGE
CAUSAL CASE
SEARCH-ONLY DECISION
EVIDENCE LAYER
READY / HOLD / RECHECK CLASS
```

Prefer direct descriptions, for example:

```text
TWO PAGES THAT ANSWER SIMILAR USER QUESTIONS
THE PAGE THAT SHOULD ANSWER THIS GROUP OF SEARCH REQUESTS
THE CURRENT SITE SECTION
A CONTENT / NAVIGATION CHANGE ON A REAL PAGE
AN ADDITIONAL CHECK USED TO CONFIRM THE RECOMMENDATION
```

Source-native brand names, product names and verbatim query strings are evidence and must not be translated or transliterated merely to satisfy the language gate.

## 5. Every recommended change must explain WHY

A client action card cannot pass with only:

```text
WHAT TO DO
WHERE TO DO IT
LIMITATION
ACCEPTANCE CHECK
```

The minimum owner-facing chain is:

```text
WHAT WAS FOUND
WHY IT MATTERS TO THE USER / OWNER
WHAT SHOULD BE CHANGED
WHY THIS CHANGE IS THE RIGHT RESPONSE TO THE FINDING
WHERE IT APPLIES
WHAT ALREADY WORKS AND MUST BE PRESERVED
WHAT THE RESULT SHOULD LOOK LIKE
HOW TO CHECK THE RESULT
```

The `WHY IT MATTERS` field is mandatory for every material recommendation. It must be specific to the finding and must not use unsupported promises about rankings, traffic, revenue or conversion.

## 6. No-action findings must be framed as validated value, not as tasks to do nothing

A client action plan must not contain negative pseudo-actions such as:

```text
DO NOT CREATE PAGE
DO NOT CHANGE ARCHITECTURE
DO NOT MERGE
NO ACTION
```

when the real finding is that the current state is appropriate.

Translate them into positive owner value:

```text
KEEP THE CURRENT PAGE STRUCTURE — IT ALREADY COVERS THE VERIFIED USER TASK
USE THE EXISTING PAGE FOR THIS DEMAND — A DUPLICATE PAGE IS NOT JUSTIFIED
PRESERVE BOTH PAGES — THEY SERVE DIFFERENT VERIFIED USER NEEDS
FOCUS BUDGET ON THE IDENTIFIED PAGE IMPROVEMENTS INSTEAD OF NEW PAGE CREATION
```

A "do not" may appear only as a guardrail inside a positive recommendation when it prevents a concrete harmful implementation error.

## 7. Do not manufacture a false opposite goal

The report must not explain the result by inventing an opposing objective that the client never set, for example:

```text
THE GOAL IS NOT TO EXPAND THE SITE AT ANY COST
THE RESULT IS NOT TO CREATE AS MANY PAGES AS POSSIBLE
```

State the actual research purpose and actual result directly:

```text
THE RESEARCH IDENTIFIED WHICH EXISTING PAGES SHOULD BE STRENGTHENED, WHICH USER TASKS THEY SHOULD COVER, AND WHERE A NEW PAGE IS OR IS NOT JUSTIFIED BY EVIDENCE
```

Never imply that the commissioned goal was mass expansion, reduction, merging or another strategy unless that goal was explicitly part of the job contract.

## 8. Internal taxonomies must be converted into client topics

Internal classes may be useful for analysis but are not automatically valid client section titles.

Do not expose headings equivalent to:

```text
CONTROVERSIAL QUERY FAMILIES
PARTIALLY READY ACTIONS
FORBIDDEN CHANGES
ANALYTICAL-ONLY MAPPINGS
AI CAUSAL CASES
UNRESOLVED / HOLD UNIVERSE
```

Translate the same material into client topics, for example:

```text
HOW THE MAIN GROUPS OF SEARCH DEMAND ARE DISTRIBUTED ACROSS SITE PAGES
WHAT TO IMPROVE ON EXISTING PAGES
WHAT INFORMATION THE COMPANY SHOULD CONFIRM BEFORE A SPECIFIC EDIT
WHAT THE RESEARCH CONFIRMED IS ALREADY CORRECT
ADDITIONAL CHECKS THAT STRENGTHENED THE RECOMMENDATIONS
```

## 9. Search / AI methodology must be subordinate to the business conclusion

When ordinary Search or an AI-assisted search mode is part of the evidence, the client report should explain its contribution in plain language, not reproduce internal provider taxonomy.

The client should understand:

```text
WHAT QUESTION WAS CHECKED
WHAT THE SEARCH RESULTS / AUTOMATED SEARCH ANSWER SHOWED
HOW THAT CONFIRMED OR CHANGED THE RECOMMENDATION
WHAT THE CHECK DOES NOT PROVE
```

Do not require the client to understand terms such as provider, causal delta, proxy, Search-only, architecture layer, model family or internal experiment state.

If a distinction between two Yandex surfaces is material, explain it in one ordinary-language sentence and only where needed.

## 10. Commercial usefulness test for the final report

Before Step 20 PASS, perform a fresh-owner walkthrough. The reviewer must be able to answer, from the report alone and without project vocabulary:

```text
WHAT ARE THE 3–10 MOST USEFUL FINDINGS FOR ME?
WHAT SHOULD I DO FIRST AND WHY?
WHAT EXACTLY SHOULD CHANGE ON EACH RECOMMENDED PAGE AND WHY?
WHAT IS ALREADY GOOD AND SHOULD BE KEPT?
WHERE CAN I AVOID SPENDING MONEY ON UNNECESSARY DUPLICATION OR REWORK?
WHAT ONE OR TWO FACTS DO I NEED TO CONFIRM BEFORE THE REMAINING IMPLEMENTATION ITEM(S)?
CAN I EXPLAIN THE RECOMMENDATIONS TO A WRITER / DEVELOPER WITHOUT LEARNING THE RESEARCH METHOD?
```

If the reviewer instead has to learn the project's classifications, status codes, evidence architecture or uncertainty taxonomy, the client report fails.

## 11. Client-report hard FAIL conditions

Any applicable condition below causes recipient FAIL even when all underlying analysis is correct:

```text
EXECUTIVE_SUMMARY_LEADS_WITH_INTERNAL_UNCERTAINTY_OR_PROHIBITIONS
NEGATIVE_INTERNAL_STATUS_USED_AS_CLIENT_SECTION_TITLE
UNEXPLAINED_SPECIALIST_OR_PROJECT_TERM_IN_DECISION_PROSE
RECOMMENDED_ACTION_WITHOUT_FINDING_AND_WHY
NO_ACTION_ITEM_PRESENTED_AS_A TASK IN THE MAIN ACTION PLAN
FALSE_OPPOSITE_GOAL_INVENTED_TO_EXPLAIN_THE_RESULT
INTERNAL_QUERY_FAMILY_OR_CAUSAL_TAXONOMY_EXPOSED_AS_CLIENT_STRUCTURE
SEARCH_OR_AI_METHOD_EXPLAINED_IN_PROVIDER/PROJECT JARGON
SOURCE_NATIVE_BRAND_OR_VERBATIM_QUERY_TRANSLITERATED WITHOUT CONTRACTUAL REASON
CLIENT_MUST_UNDERSTAND_INTERNAL_RESEARCH_PROCESS TO UNDERSTAND A RECOMMENDATION
```

## 12. PASS gate

A full client research report may pass only when all applicable statements are true:

```text
OWNER_VALUE_VISIBLE_IN_FIRST_SCREEN = true
READY_RECOMMENDATIONS_HAVE_FINDING_AND_WHY = true
CURRENTLY_CORRECT_STATES_ARE_FRAMED_AS_POSITIVE_VALIDATED_VALUE = true
UNRESOLVED_ITEMS_ARE_TRANSLATED_INTO_SPECIFIC_CONFIRMATION / NEXT-DECISION LANGUAGE = true
NON_SPECIALIST_OWNER_CAN_UNDERSTAND_EVERY MATERIAL RECOMMENDATION = true
INTERNAL_STATUS_TAXONOMY_NOT_USED_AS_CLIENT_INFORMATION_ARCHITECTURE = true
SEARCH_AI_METHOD_SUBORDINATE_TO_CLIENT_CONCLUSION = true
NO_FALSE_OPPOSITE_GOAL = true
NO_NEGATIVE_PSEUDO_ACTIONS_IN_MAIN_ACTION_PLAN = true
SOURCE_NATIVE_BRANDS_AND_VERBATIM_EVIDENCE_PRESERVED = true
OWNER_WALKTHROUGH = PASS
```

## 13. Non-repeat purpose

The purpose is to prevent a technically correct research package from becoming an unsellable or confusing client document.

Step 19 must materialize the research into owner language. Step 20 must verify the report as a client product, not as an analyst reading their own work.

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.
