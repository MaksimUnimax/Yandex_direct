# KW-001 — Step 20 commissioner-facing narrative and de-AI gate

Updated: 2026-09-06  
Status: **ACTIVE AS LEGACY SHARED QUALITY BRIDGE / REPORT-SPECIFIC ROUTING REQUIRED**  
Scope: **Step 19 materialization + Step 20 recipient acceptance / Level 1**

This gate prevents an analytically correct report from failing as a paid deliverable because it is written for an invented recipient role, does not answer the commissioned Kwork directly, exposes internal workflow language, or reads like a generated template instead of a coherent report for a non-specialist commissioner.

Concrete client domains, URLs, counts, query strings, brands, action IDs and current-job findings are forbidden in this Level-1 rule. Those belong in Level 2.

## Report-specific applicability correction

This file originated from the owner-directed rework of **Report №01**. It must not be applied wholesale to every deliverable. Canonical applicability now routes through:

`STEP_20_REPORT_SPECIFIC_ACCEPTANCE_ROUTING.md`

Report-specific authorities:

- `STEP_20_REPORT_01_CUSTOMER_RESEARCH_REPORT_GATE.md` — full customer-facing research-report rules and the complete Report №01 failure inventory;
- `STEP_20_REPORT_02_SPECIALIST_IMPLEMENTATION_GUIDE_GATE.md` — only the transferable writing-quality controls plus the denser technical requirements needed by an SEO/implementation specialist;
- Report №03 — no presentation rules are inherited automatically before its own review.

```text
REPORT_01_SIMPLICITY != REPORT_02_SIMPLICITY
REPORT_01_FAILURE_INVENTORY != AUTOMATIC_REPORT_02_FAILURE_INVENTORY
CONNECTED HUMAN NARRATIVE = SHARED
NATURAL NON-GENERATED WORDING = SHARED
MEANINGFUL SECTIONS = SHARED
SPECIALIST TERMINOLOGY = ALLOWED / EXPECTED IN REPORT_02
```

The sections below remain useful historical/shared guidance, but the report-specific gates above control final acceptance.

## 1. Recipient identity: commissioner, not an invented role

Unless the contract explicitly names another role, the recipient is the **commissioner / customer of the work**.

Do not silently replace the commissioner with:

```text
BUSINESS OWNER
SITE OWNER
EDITOR
SEO SPECIALIST
DEVELOPER
MARKETING MANAGER
```

The commissioner may happen to hold one of those roles, but the report must not assume it.

```text
COMMISSIONER != ASSUMED BUSINESS OWNER
COMMISSIONER != ASSUMED SITE OWNER
```

Client-facing language should therefore use neutral wording such as `заказчик`, `для принятия решения`, `на сайте`, `в работе`, or omit the role when it adds no value.

## 2. The report must answer the sold Kwork first

The first substantive part of the report must answer the commissioned question in ordinary language before diving into detailed evidence.

For a research Kwork, the commissioner should quickly understand:

```text
WHAT WAS INVESTIGATED?
WHAT IS THE OVERALL ANSWER?
WHAT IS GENERALLY CORRECT ON THE CURRENT SITE / STRUCTURE?
WHAT IS WEAK / MISSING / WRONG?
WHAT SHOULD ACTUALLY CHANGE?
WHAT DID ORDINARY YANDEX OUTPUT SHOW?
WHAT DID ALICE ADD WHEN ALICE IS PART OF THE SOLD PRODUCT?
```

A report fails when the commissioner must first read internal methodology, classifications, disclaimers or QA accounting before discovering the answer to the Kwork.

## 3. Semantic sections are required; disconnected micro-blocks are not

**Meaningful sectioning is required.** A report must not become one unstructured wall of text.

Correct principle:

```text
SEMANTIC SECTIONS = REQUIRED
CONNECTED PROSE INSIDE EACH SECTION = REQUIRED
DISCONNECTED MICRO-SECTIONS / TEMPLATE FRAGMENTATION = FAIL
```

A good high-level structure may look like:

```text
ANSWER TO THE KWORK
→ WHAT WAS DONE
→ WHAT ORDINARY YANDEX SHOWED
→ WHAT ALICE ADDED
→ OVERALL SITE / STRUCTURE CONCLUSION
→ WHAT SHOULD CHANGE AND WHY
→ EVIDENCE APPENDICES
```

The exact headings may differ by job, but each section must have a clear purpose and continue the previous thought.

The failure is **not** the existence of blocks or headings. The failure is excessive fragmentation into many small independent sections that could be shuffled without changing meaning, or repeated identical mini-forms that make the report read like a generated template.

## 4. Explain the full work as a connected process, without exposing the internal stage machine

The commissioner must understand what was actually done from beginning to end.

A client-facing explanation may follow the real work logically:

```text
SITE / OFFER STUDIED
→ DEMAND COLLECTED AND CLEANED
→ REQUESTS GROUPED BY USER TASK
→ TASKS COMPARED WITH EXISTING PAGES
→ ORDINARY YANDEX OUTPUT CHECKED WHERE IT COULD CHANGE OR CONFIRM A DECISION
→ ALICE CHECKED WHERE IT COULD ADD OR CHALLENGE A MATERIAL CONCLUSION
→ RESULTS COMPARED
→ SITE / PAGE RECOMMENDATIONS PRODUCED
```

Do not expose undefined internal phrases such as:

```text
THIS STAGE
THE NEXT STAGE
THE CURRENT LAYER
THE CAUSAL PHASE
THE SELECTED UNIVERSE
```

unless the client-facing report has explicitly defined them and they are genuinely useful to the commissioner.

## 5. Numbers support the narrative; numbers are not the narrative

Exact scope numbers are useful only when tied to meaning.

Every material count shown in the report should answer:

```text
WHAT DOES THIS NUMBER COUNT?
HOW DOES IT RELATE TO THE LARGER SCOPE?
WHY WAS A SMALLER SUBSET CHECKED MORE DEEPLY?
WHAT DECISION DID THAT CHECK HELP MAKE OR VERIFY?
```

Do not present a chain of numbers as though the chain itself were the report.

Do not use vague substitutes such as `весь массив` when exact scope exists.

## 6. Selective Alice checks must be described as the complete chosen check, not an incomplete fragment

When Alice is used selectively, the commissioner must understand:

```text
HOW MANY CANDIDATE THEMES WERE CONSIDERED
HOW MANY WERE CHECKED IN ALICE
WHAT MADE THOSE CASES MATERIAL
WHAT CONTROL CASES WERE INCLUDED, IF ANY
WHY OTHER CANDIDATES WOULD NOT ADD A NEW DECISION TYPE
WHY THE CHOSEN SET IS SUFFICIENT FOR THE COMMISSIONED QUESTION
```

Do not write that the Alice checks are `not the whole amount of research` if those checks are in fact the complete Alice work performed for the job.

Do not write `full volume of this stage` or equivalent internal language. The commissioner should never have to ask: `what stage?`

## 7. Use the actual observed surface name consistently

If the work compares ordinary Yandex output with Alice output, client wording must describe the **result surface**, not silently switch to the process name.

```text
SEARCH PROCESS != SEARCH OUTPUT
```

If the current job is about Alice, use `Алиса` consistently unless another term is necessary and explicitly explained. Do not alternate `Алиса`, `AI`, `ИИ`, `нейросетевой поиск`, `генеративный поиск` as though they were separate systems.

## 8. The report must state the overall site conclusion directly

A research report must not hide behind neutral observations.

When evidence supports it, the report should directly say whether:

```text
THE CURRENT STRUCTURE IS GENERALLY APPROPRIATE
THE CURRENT STRUCTURE HAS MATERIAL GAPS
SPECIFIC EXISTING PAGES NEED IMPROVEMENT
NEW PAGES ARE JUSTIFIED
NEW PAGES ARE NOT JUSTIFIED
PAGE ROLES ARE CONFUSED
PAGE ROLES ARE GENERALLY CORRECT
```

This conclusion must remain evidence-bounded, but it must still be a conclusion.

## 9. Recommendations need reasoning, not cloned forms

Every material recommendation still needs the logic:

```text
CURRENT SITUATION
→ PROBLEM
→ WHY IT MATTERS
→ WHAT TO CHANGE
→ WHAT RESULT IS EXPECTED
```

But the commissioner report does **not** have to repeat the same seven labels for every recommendation.

Repeated implementation-ticket fields such as:

```text
WHAT WAS FOUND
WHY IT MATTERS
WHAT TO CHANGE
WHERE
WHAT TO PRESERVE
EXPECTED RESULT
HOW TO CHECK
```

may be appropriate in a specialist implementation document, but mechanically repeating the same form throughout the commissioner report creates an artificial, generated-template rhythm.

Use semantic subsections where they help understanding, but let the prose structure follow the actual finding.

## 10. Methodological guardrails belong only where they affect a real decision

Do not add a generic final section equivalent to:

```text
HOW TO USE RESULTS
WHAT THIS DOES NOT PROVE
GENERAL WARNINGS
```

A limitation should appear next to the claim it limits, and only when omitting it could realistically mislead the commissioner.

Analyst / QA guardrails such as the following normally belong in internal evidence or a technical appendix, not the main commissioner narrative:

```text
ONE EXACT QUERY DOES NOT AUTOMATICALLY GENERALIZE
ABSENCE IN ONE SEARCH OUTPUT DOES NOT PROVE PAGE NON-EXISTENCE
ONE ALICE ANSWER IS NOT AN ARCHITECTURE AUTHORITY
NO TRAFFIC / REVENUE GUARANTEE WITHOUT SEPARATE EVIDENCE
```

These rules may be methodologically correct, but they must not replace the answer to the Kwork.

## 11. Detailed evidence moves to appendices when it interrupts the answer

Long exact-query tables, raw observations, complete routing maps and evidence ledgers belong in appendices or specialist artifacts when the main conclusion does not require reading every row.

```text
COMPLETE EVIDENCE PRESERVED
!= ALL EVIDENCE MUST DOMINATE MAIN NARRATIVE
```

The main report should use detailed evidence to support conclusions, not reproduce internal completeness for its own sake.

## 12. Generated / templated presentation failure classes

The following patterns are not proof of machine authorship individually, but their accumulation creates an obviously generated or templated client experience and requires rework:

```text
FAKE READING-TIME PROMISES OR MARKETING HEADINGS (e.g. "IN ONE MINUTE")
OVERLY SYMMETRICAL SECTION STRUCTURE
IDENTICAL SENTENCE RHYTHM ACROSS MANY FINDINGS
REPEATED TRANSITION PHRASES THAT ADD NO INFORMATION
GENERIC CORPORATE PHRASES IN PLACE OF CONCRETE CONCLUSIONS
EXCESSIVE META-EXPLANATION OF THE REPORT ITSELF
EXCESSIVE DEFENSIVE DISCLAIMERS
MECHANICAL ENUMERATION OF EVERYTHING CHECKED
PARALLEL RECOMMENDATION FORMS REPEATED REGARDLESS OF FINDING TYPE
ABSTRACT PHRASES SUCH AS "PRACTICAL VALUE", "SIGNIFICANT RESULTS", "THIS STAGE" WITHOUT A CONCRETE REFERENT
RESTATING THE SAME CONCLUSION IN INTRODUCTION, SUMMARY, METHOD AND FINAL SECTION
```

The correction is not to remove meaningful structure. The correction is to keep semantic sections while making the prose inside and between them concrete, connected and specific to the actual research.

## 13. Report №01 failure inventory from owner-directed post-release rework

The following failure classes must not be reintroduced:

```text
DATE / VERSION METADATA OCCUPIES FIRST SCREEN
SOLD ALICE DIFFERENTIATOR ABSENT FROM TITLE
TECHNICAL "GENERATIVE" TERM USED BEFORE CLIENT MEANING
WRONG SURFACE WORD: SEARCH PROCESS USED WHEN OUTPUT WAS STUDIED
ALICE / AI / NEURAL / GENERATIVE LABELS MIXED AS IF MULTIPLE SYSTEMS
SELECTIVE ALICE CHECK COUNT SHOWN WITHOUT WHY THESE CASES WERE CHOSEN
COMPLETE ALICE CHECK SET MISDESCRIBED AS "NOT THE WHOLE VOLUME"
INTERNAL "STAGE" WORDING EXPOSED TO COMMISSIONER
TARGETED ORDINARY-SEARCH COUNT SHOWN WITHOUT RELATION TO TOTAL DEMAND
VAGUE "WHOLE ARRAY" WORDING USED INSTEAD OF EXACT SCOPE
FULL WORKFLOW NOT EXPLAINED IN HUMAN LANGUAGE
PAGE-ROUTING RESULTS SHOWN AS IF THEY WERE FUTURE TASKS
LONG NO-CHANGE CATALOGUE INCLUDED JUST TO PROVE COMPLETENESS
INTERNAL RESULT / STATUS DUMP USED AS CLIENT STRUCTURE
GENERIC "HOW TO USE RESULTS" DISCLAIMER SECTION INSERTED INTO MAIN REPORT
ASSUMED "BUSINESS OWNER" / "SITE OWNER" RECIPIENT INSTEAD OF COMMISSIONER
EXECUTIVE SUMMARY WRITTEN AS A MARKETING WIDGET ("IN ONE MINUTE")
REPORT BUILT FROM QA COUNTS RATHER THAN THE COMMISSIONED QUESTION
RECOMMENDATIONS WRITTEN AS CLONED FORMS RATHER THAN NATURAL REASONING
MAIN CONCLUSION DOES NOT DIRECTLY SAY WHETHER CURRENT SITE / STRUCTURE IS GENERALLY CORRECT OR PROBLEMATIC
ALICE CONTRIBUTION DESCRIBED AS METHOD BUT NOT AS A RESULT THAT AFFECTED THE SITE CONCLUSION
FINAL SECTION REPEATS METHOD / COUNTS INSTEAD OF ANSWERING THE KWORK
```

## 14. Root cause

Recurring root cause:

```text
INTERNAL DATABASE / QA SCHEMA
→ USED AS DOCUMENT OUTLINE
→ EACH CORRECTION BECOMES ANOTHER CLIENT-FACING BLOCK
→ REPORT BECOMES FORMALLY COMPLETE BUT HUMANLY DISCONNECTED
```

Correct materialization reverses that direction:

```text
COMMISSIONED QUESTION
→ CONNECTED CLIENT NARRATIVE
→ MATERIAL CONCLUSIONS
→ ACTIONS / RECOMMENDATIONS
→ SUPPORTING EVIDENCE
→ INTERNAL QA STAYS INTERNAL
```

## 15. Hard FAIL conditions

```text
RECIPIENT_ROLE_INVENTED_WITHOUT CONTRACT
COMMISSIONED_KWORK_NOT_ANSWERED DIRECTLY
MEANINGFUL_SECTIONING_ABSENT
DISCONNECTED_MICRO_SECTION_FRAGMENTATION
INTERNAL_STAGE_WORDING_VISIBLE_TO COMMISSIONER
COUNT_CHAIN_USED_AS MAIN STORY
ALICE_SELECTION_NOT EXPLAINED AS COMPLETE SUFFICIENT CHECK
SEARCH_PROCESS_WORD USED WHERE SEARCH_OUTPUT IS MEANT
MULTIPLE CLIENT LABELS USED FOR SAME ALICE SURFACE
NO DIRECT OVERALL SITE / STRUCTURE CONCLUSION
MECHANICALLY CLONED RECOMMENDATION FORMS DOMINATE REPORT
GENERIC METHODOLOGY / DISCLAIMER SECTION REPLACES CLIENT CONCLUSION
DETAILED EVIDENCE DUMP DOMINATES MAIN NARRATIVE WITHOUT DECISION NEED
GENERATED_TEMPLATE_PRESENTATION_ACCUMULATION
```

## 16. PASS gate

A commissioner-facing research report may pass only when all applicable statements are true:

```text
RECIPIENT = COMMISSIONER UNLESS CONTRACT SAYS OTHERWISE
SOLD_KWORK_ANSWER_VISIBLE EARLY
SEMANTIC_SECTIONS_CLEAR = true
SECTIONS_FORM_ONE_CONNECTED_REASONING_CHAIN = true
FULL_WORK_EXPLAINED WITHOUT INTERNAL STAGE MACHINE = true
MATERIAL_COUNTS_EXPLAINED IN CONTEXT = true
ALICE_SELECTION_AND_SUFFICIENCY_EXPLAINED = true when applicable
ONE CLIENT-FACING NAME PER OBSERVED SURFACE = true
OVERALL_SITE_CONCLUSION_DIRECT = true
RECOMMENDATIONS_READ AS NATURAL REASONING = true
METHOD_GUARDRAILS_SUBORDINATE TO DECISIONS = true
DETAILED_EVIDENCE_MOVED TO APPENDICES WHEN IT INTERRUPTS THE ANSWER = true
GENERATED_TEMPLATE_PRESENTATION = absent
FINAL_SECTION_ANSWERS KWORK = true
```

Step 20 must test the report as a paid answer to the commission, not merely as a container that includes all known facts.