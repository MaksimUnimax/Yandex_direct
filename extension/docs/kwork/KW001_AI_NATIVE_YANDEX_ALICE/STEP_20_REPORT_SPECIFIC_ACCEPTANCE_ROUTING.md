# KW-001 — Step 20 report-specific acceptance routing

Updated: 2026-09-06  
Status: **ACTIVE / UNIVERSAL ROUTING / REPORT-SPECIFIC RULE SEPARATION**  
Scope: **Step 19 materialization + Step 20 recipient acceptance**

Step 20 must not apply one report's presentation rules blindly to every deliverable. Each promised report has a different recipient task and therefore a different acceptance contract.

```text
COMMON HUMAN-WRITING QUALITY
+ REPORT-SPECIFIC RECIPIENT CONTRACT
= STEP 20 ACCEPTANCE FOR THAT REPORT
```

## Report №01 — customer research report

Canonical authority:

`STEP_20_REPORT_01_CUSTOMER_RESEARCH_REPORT_GATE.md`

Purpose: give the customer of the Kwork a complete, understandable answer to the commissioned research question without requiring SEO expertise or repository knowledge.

Report №01 therefore carries the full set of lessons discovered during the owner-directed rewrite of the first report: direct answer to the Kwork, plain language, connected explanation of the work, explicit site verdict, clear role of ordinary Yandex output and Alice output, selected-check explanation, natural recommendations and evidence moved to appendices when detail interrupts the answer.

## Report №02 — specialist implementation guide

Canonical authority:

`STEP_20_REPORT_02_SPECIALIST_IMPLEMENTATION_GUIDE_GATE.md`

Purpose: let an SEO specialist or implementer understand what was researched, how the conclusions were derived, and exactly what must be changed or preserved on the site.

Report №02 inherits only the transferable quality controls from Report №01:

```text
MEANINGFUL SEMANTIC SECTIONS
CONNECTED NARRATIVE
NATURAL HUMAN WORDING
NO GENERATED / TEMPLATE-LIKE FILLER
NO UNDEFINED OR ABSURD PHRASES
CLAIM → EVIDENCE → ACTION CONTINUITY
EXACT SCOPE / SELECTION LOGIC WHEN MATERIAL
```

It does **not** inherit the non-specialist simplicity requirement. Professional SEO, semantic, architecture and implementation terminology is allowed and expected when it helps execution. Report №02 also requires denser technical explanation of acquisition, filtering, exclusions, clustering, mapping, validation, uncertainty and implementation details.

A repeated structured action schema may be appropriate in Report №02 because the specialist must execute and verify work. The same repeated schema can be a failure in Report №01 when it makes a customer-facing narrative read like a generated questionnaire.

## Report №03

No new report-specific universal presentation gate is promoted here yet. Report №03 must be reviewed against its own recipient task before Report №01 or Report №02 rules are copied into it.

```text
REPORT_01_RULE != AUTOMATIC_REPORT_02_RULE
REPORT_02_RULE != AUTOMATIC_REPORT_03_RULE
SHARED_RULE MUST BE EXPLICITLY IDENTIFIED AS SHARED
```

## Routing rule

Before final QA of any deliverable:

1. identify the report number and recipient task;
2. read the common Step 20 QA authorities;
3. read the matching report-specific gate;
4. apply only the shared rules plus the correct report-specific rules;
5. do not mark another report PASS merely because one report's gate passed.
