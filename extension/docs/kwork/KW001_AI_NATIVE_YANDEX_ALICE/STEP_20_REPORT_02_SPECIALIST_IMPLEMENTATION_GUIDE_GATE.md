# KW-001 — Step 20 Report №02 specialist implementation-guide gate

Updated: 2026-09-06  
Status: **ACTIVE / UNIVERSAL / REPORT-02-SPECIFIC TRANSFER CONTROL**  
Scope: **Report №02 only — SEO / implementation specialist guide**

This gate defines which presentation lessons transfer from Report №01 and which do not. It does not mark any current Report №02 artifact PASS; it governs the next owner review and rework of Report №02.

## 1. Recipient and purpose

The recipient is an SEO specialist / implementer who must understand the research lineage and execute safe, evidence-backed changes.

Report №02 is not required to be simplified to non-specialist language. Professional terminology is expected when it improves precision.

```text
REPORT_01 = CUSTOMER RESEARCH ANSWER
REPORT_02 = SPECIALIST IMPLEMENTATION GUIDE
```

## 2. What transfers from Report №01

The following writing-quality rules remain mandatory:

```text
MEANINGFUL SEMANTIC SECTIONS
CONNECTED NARRATIVE BETWEEN SECTIONS
NATURAL HUMAN WORDING
NO GENERATED / TEMPLATE-LIKE FILLER
NO ABSURD OR UNDEFINED PHRASES
NO FAKE READING-TIME HEADINGS
NO VAGUE META-PHRASES WITHOUT A REFERENT
NO INTERNAL DATABASE DUMP USED AS THE DOCUMENT OUTLINE
CLAIM → EVIDENCE → ACTION CONTINUITY
EXACT COUNTS / SELECTION LOGIC WHEN MATERIAL
```

A specialist report may be dense, but it must still read like a coherent technical document written by a competent analyst, not like a generated form or stitched QA export.

## 3. What does NOT transfer from Report №01

Do not impose Report №01's maximum-simplicity requirement on Report №02.

The following are allowed and often required when defined correctly:

```text
SEO TERMINOLOGY
SEMANTIC CLUSTERING TERMINOLOGY
PAGE OWNERSHIP / INTENT / ROUTING TERMINOLOGY
ARCHITECTURE / CANNIBALIZATION / OVERLAP TERMINOLOGY
IMPLEMENTATION MODES
READINESS / DEPENDENCY / CONFIDENCE STATES
EVIDENCE LOCATORS
ACCEPTANCE CRITERIA
```

The specialist should not have to reverse-engineer technical meaning from oversimplified customer wording.

## 4. Report №02 must explain the depth of completed research more fully

The specialist must understand not only the final action but how the action was derived.

The report should explain, at an appropriate technical level:

```text
SITE / OFFER INVENTORY
→ DEMAND ACQUISITION
→ TARGETED EXPANSION
→ CLEANUP / EXCLUSIONS / DEFERRED STATES
→ CLUSTERING BY USER TASK
→ PHRASE-TO-PAGE / PAGE-OWNERSHIP MAPPING
→ ORDINARY YANDEX VALIDATION
→ ALICE CASE SELECTION AND VALIDATION
→ SEARCH-vs-ALICE COMPARISON
→ STRUCTURAL / CONTENT / NAVIGATION DECISION
→ IMPLEMENTATION READINESS
```

This is important for two reasons:

1. the specialist can verify that a recommendation is not an isolated guess;
2. the specialist can see the real scale of the research and understand which filters, selections and reconciliations produced the final action.

Counts should be shown when they materially explain the funnel or prove completeness, but not as vanity metrics.

## 5. Selection, filtering and clustering must be technically legible

Report №02 should explain:

- what entered the research;
- what was excluded and on what principle;
- what remained deferred / unresolved and why;
- how queries were grouped into user tasks;
- how task clusters were mapped to pages;
- how ambiguous cases were escalated to ordinary Yandex checks;
- how Alice cases were selected and why the selected set was sufficient;
- how later corrections propagated into the final semantic and action authorities.

The goal is not to reproduce every internal file. The goal is to make the analytical chain auditable enough that a specialist trusts and can use the result.

## 6. Report №02 must be implementation-dense

For every real site change that is ready to execute, the specialist should be able to find the information needed to implement it without repository archaeology.

Depending on action type, the guide should provide:

```text
ACTION ID / TRACEABLE REFERENCE
TARGET URL OR OBJECT
IMPLEMENTATION MODE
CURRENT STATE
PROBLEM / CAUSAL REASON
EVIDENCE MEANING + LOCATOR
EXACT CHANGE
EXACT LOCATION / BLOCK / COMPONENT WHEN KNOWN
DEPENDENCIES
WHAT MUST BE PRESERVED
WHAT MUST NOT BE CLAIMED OR CHANGED
READINESS / BLOCKER STATE
ACCEPTANCE CRITERIA
FOLLOW-UP CHECK WHEN REQUIRED
```

Unlike Report №01, a repeated structured action schema is acceptable here when it improves execution consistency. The repeated fields must carry real content and must not become filler.

## 7. Physical change must be separated from analytical mapping

A specialist guide must make a hard distinction between:

```text
SEMANTIC_MAPPING_ONLY
CONTENT_BLOCK
NAVIGATION_CHANGE
CONTEXTUAL_LINK
RECHECK_ONLY
NO_SITE_CHANGE
HOLD / NOT_READY
```

An analytical page assignment must not silently become a CMS change. A possible internal link must not become implementation-ready without exact source context and placement evidence.

## 8. Natural language still matters

Technical precision does not justify awkward generated phrasing.

Avoid:

- repeated corporate filler;
- undefined abstract phrases such as `этот этап`, `значимая ценность`, `данный слой`;
- sentences whose subject is an AI system when the actual actor is the research process;
- robotic restatement of the same status in every paragraph;
- huge blocks of status tokens with no human explanation of what they mean for implementation.

Use specialist terms, but connect them with normal explanatory prose.

## 9. Alice wording in Report №02

Report №02 may use more technical language than Report №01, but research agency still belongs to the analysis.

Prefer:

```text
"проверка выдачи Алисы подтверждает..."
"сопоставление ordinary Yandex / Alice evidence..."
"в Alice-output case зафиксирован..."
```

Avoid writing as though Alice independently performed the semantic research, selected the architecture or authored the implementation decision.

## 10. Report №02 PASS gate

Report №02 may pass only when:

```text
RECIPIENT = SEO / IMPLEMENTATION SPECIALIST
SEMANTIC_SECTIONS = clear
CONNECTED_TECHNICAL_NARRATIVE = true
PROFESSIONAL_TERMINOLOGY = allowed_and_defined
RESEARCH_FUNNEL_EXPLAINED = true
FILTERING / EXCLUSION / DEFERRED LOGIC_EXPLAINED = true
CLUSTERING_AND_PAGE_MAPPING_EXPLAINED = true
ORDINARY_YANDEX_VALIDATION_ROLE_EXPLAINED = true
ALICE_SELECTION_AND_COMPARISON_EXPLAINED = true
ACTION_DERIVATION_TRACEABLE = true
PHYSICAL_CHANGE_SEPARATED_FROM_ANALYTICAL_MAPPING = true
READY_ACTIONS_HAVE_EXECUTABLE_DETAIL = true
BLOCKED_ACTIONS_HAVE_CLEAR_BLOCKER_AND_REQUIRED_EVIDENCE = true
ACCEPTANCE_CRITERIA_PRESENT_WHERE_IMPLEMENTATION_READY = true
NATURAL_HUMAN_TECHNICAL_PROSE = true
GENERATED_TEMPLATE_FILLER = absent
```

Report №02 must demonstrate both the depth of the research and the exact implementation consequence. It should not be simplified into Report №01, and it should not be reduced to an internal action database dump.
