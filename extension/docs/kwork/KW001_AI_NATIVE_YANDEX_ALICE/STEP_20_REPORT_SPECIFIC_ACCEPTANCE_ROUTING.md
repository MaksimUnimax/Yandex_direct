# KW-001 — Step 20 report-specific acceptance routing

Updated: 2026-09-07  
Status: **ACTIVE / UNIVERSAL ROUTING / REPORT-SPECIFIC RULE SEPARATION**  
Scope: **Step 19 materialization + Step 20 recipient acceptance**

Step 20 must not apply one report's presentation rules blindly to every deliverable. Each promised report has a different recipient task and therefore a different acceptance contract.

```text
COMMON HUMAN-WRITING QUALITY
+ REPORT-SPECIFIC RECIPIENT CONTRACT
= STEP 20 ACCEPTANCE FOR THAT REPORT
```

## Universal research-scope freeze during report materialization

Step 19/20 is primarily a **materialization, explanation and recipient-acceptance stage for research that has already been performed**. It is not permission to silently start a new research pass merely because the report would look more complete with additional evidence.

This is a critical cost and scope boundary.

```text
REPORT MATERIALIZATION
!=
NEW RESEARCH

MISSING IMPLEMENTATION DETAIL IN PRESERVED EVIDENCE
!=
AUTOMATIC AUTHORIZATION TO COLLECT IT NOW
```

When a report exposes that a desired field, exact placement, classification, current-page detail, business fact, Search observation, AI observation or other project fact was not established by the completed research, the default response is:

1. state the evidence boundary honestly;
2. downgrade readiness or move the item to clarification / additional-check status where necessary;
3. identify the exact missing evidence;
4. do **not** acquire that evidence during report production unless the owner separately authorizes a new research/revalidation task.

The reporting stage must not silently expand scope by:

- recrawling the client site to fill gaps in an implementation card;
- classifying a large new set of site objects that was not classified during the research;
- rerunning Search / Wordstat / Alice / AI checks to make a recommendation look more complete;
- collecting new business facts to rescue an unsupported ready action;
- using post-hoc evidence to upgrade `not ready / partial / unresolved` into ready without an explicitly authorized new evidence step.

This failure is especially serious when it creates material time, provider or browsing cost after the research was already declared complete.

```text
COMPLETED RESEARCH AUTHORITY
-> REPORT MATERIALIZATION

IF EVIDENCE GAP FOUND:
-> DISCLOSE / DOWNGRADE / NAME REQUIRED EVIDENCE

NOT:
-> SILENTLY PERFORM NEW RESEARCH
```

### Allowed exception — external methodology/source freshness

Freshly checking **external public methodology/documentation sources** for the report bibliography is different from recollecting project facts. It is allowed or required when the report contract requires current sources, provided it does not change project-specific analytical conclusions by itself.

```text
FRESH METHODOLOGY / BIBLIOGRAPHY REVIEW = ALLOWED WHEN REQUIRED
FRESH PROJECT FACT / SITE / SEARCH / AI EVIDENCE COLLECTION = OWNER-AUTHORIZED NEW WORK ONLY
```

Any explicitly owner-authorized new research/revalidation must be recorded as a separate evidence-producing step with its own scope, cost boundary and authority. It must not be backdated or presented as if it belonged to the original completed research.

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

## Отдельный результат — полное семантическое ядро

Canonical authority:

`STEP_20_STANDALONE_SEMANTIC_CORE_GATE.md`

Purpose: give an SEO/semantic/implementation specialist a standalone XLSX for filtering, sorting, cluster review, phrase→page work, unresolved review and prioritization.

```text
REPORT №02 SPECIALIST GUIDE
!=
STANDALONE SEMANTIC CORE XLSX
```

They may serve similar specialist recipients, but they are separate physical deliverables. The standalone core requires its own data reconciliation, workbook usability, technical-traceability boundary and Russian recipient-language QA.

## Report №03

No new report-specific universal presentation gate is promoted here yet. Report №03 must be reviewed against its own recipient task before Report №01 or Report №02 rules are copied into it.

```text
REPORT_01_RULE != AUTOMATIC_REPORT_02_RULE
REPORT_02_RULE != AUTOMATIC_REPORT_03_RULE
SHARED_RULE MUST BE EXPLICITLY IDENTIFIED AS SHARED
```

## Routing rule

Before final QA of any deliverable:

1. identify the report/deliverable and recipient task;
2. read the common Step 20 QA authorities;
3. read the matching report-specific gate;
4. apply only the shared rules plus the correct report-specific rules;
5. verify that report production did not silently acquire new project-specific evidence outside the completed research scope;
6. do not mark another report PASS merely because one report's gate passed.
