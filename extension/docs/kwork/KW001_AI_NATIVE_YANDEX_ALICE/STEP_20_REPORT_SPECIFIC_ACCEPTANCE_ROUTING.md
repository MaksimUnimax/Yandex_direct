# KW-001 — Step 20 report-specific acceptance routing

Updated: 2026-09-08  
Status: **ACTIVE / UNIVERSAL ROUTING / REPORT-SPECIFIC RULE SEPARATION**  
Scope: **Step 19 materialization + Step 20 recipient acceptance**

Step 20 must not apply one report's presentation rules blindly to every deliverable. Each promised report has a different recipient task and therefore a different acceptance contract.

```text
COMMON HUMAN-WRITING QUALITY
+ REPORT-SPECIFIC CLIENT CONTRACT
= STEP 20 ACCEPTANCE FOR THAT REPORT
```

## Universal research-scope freeze during report materialization

Step 19/20 is primarily a materialization, explanation and recipient-acceptance stage for research that has already been performed. It is not permission to silently start a new research pass merely because the report would look more complete with additional evidence.

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
2. move the item to clarification / additional-check status where necessary;
3. identify the exact missing evidence or answer;
4. do not acquire that evidence during report production unless the owner separately authorizes a new research/revalidation task.

The reporting stage must not silently expand scope by:

- recrawling the client site to fill gaps in an implementation card;
- classifying a large new set of site objects that was not classified during the research;
- rerunning Search / Wordstat / Alice / AI checks to make a recommendation look more complete;
- collecting new business facts to rescue an unsupported ready action;
- using post-hoc evidence to upgrade `not ready / partial / unresolved` into ready without an explicitly authorized new evidence step.

Freshly checking external public methodology/documentation sources for bibliography freshness is different from recollecting project facts and may be allowed when the report contract requires it.

Any explicitly owner-authorized new research/revalidation must be recorded as a separate evidence-producing step. It must not be backdated or presented as if it belonged to the original completed research.

## Report №01 — customer research report

Canonical authority:

`STEP_20_REPORT_01_CUSTOMER_RESEARCH_REPORT_GATE.md`

Purpose: give the customer a complete, understandable answer to the commissioned research question without requiring specialist knowledge or repository context.

## Report №02 — «Внедрение рекомендации»

Primary canonical authority:

`STEP_20_REPORT_02_SPECIALIST_IMPLEMENTATION_GUIDE_GATE.md`

The filename is historical. The client-facing document itself is purpose-led and must use the visible title:

```text
Внедрение рекомендации
```

Supplemental format authority:

`STEP_20_REPORT_02_IMPLEMENTATION_REPORT_FORMAT_GATE.md`

Physical-layout authority:

`STEP_20_REPORT_02_SPECIALIST_IMPLEMENTATION_GUIDE_LAYOUT_GATE.md`

All three gates are mandatory for Report №02 acceptance.

Report №02 purpose:

```text
COMPLETED RESEARCH
-> CONCRETE SITE RECOMMENDATIONS
-> CONCRETE CLARIFICATIONS
-> EXPLAINED SUPPORTING TABLES
-> CLEAR NEXT ACTION / IMPLEMENTATION METHOD
```

It is not identified by the recipient profession. It must be understandable even to a non-specialist owner while still being concrete enough for implementation.

Current permanent owner lessons for Report №02 include:

- visible title names the result, not an SEO/specialist/editor/developer role;
- main document is action-first, not a second research report;
- ready recommendation explains what, why, where, how and the completed result;
- incomplete recommendation states the exact clarification required;
- every non-obvious table explains what it is, why it exists and how to use it;
- the 46 topic rows are presented as `Распределение тем по страницам` in ordinary Russian;
- the 14 page pairs are presented as `Связи между страницами` with purpose and implementation method;
- the four unresolved checks explain purpose, method and resulting decision;
- no standalone `Требования к существующей структуре` / prohibition section;
- no negative pseudo-actions, process diary, internal IDs or beginner `open/find/navigate` filler;
- no report-stage new project research to fill evidence gaps;
- no ambiguous placement or invented temporal/business facts;
- final committed PDF must pass physical visual readback.

The full owner-identified failure history A–U, including physical failures O–P, is preserved in the primary canonical Report №02 gate and must be read before generating a future Report №02.

## Отдельный результат — полное семантическое ядро

Canonical authority:

`STEP_20_STANDALONE_SEMANTIC_CORE_GATE.md`

The standalone semantic-core workbook is a separate physical deliverable and has its own acceptance contract.

```text
REPORT №02 «ВНЕДРЕНИЕ РЕКОМЕНДАЦИИ»
!=
STANDALONE SEMANTIC CORE XLSX
```

## Report №03

No new report-specific universal presentation gate is promoted here yet. Report №03 must be reviewed against its own recipient task before Report №01 or Report №02 rules are copied into it.

```text
REPORT_01_RULE != AUTOMATIC_REPORT_02_RULE
REPORT_02_RULE != AUTOMATIC_REPORT_03_RULE
SHARED_RULE MUST BE EXPLICITLY IDENTIFIED AS SHARED
```

## Routing rule

Before final QA of any deliverable:

1. identify the report/deliverable and its actual client task;
2. read the common Step 20 QA authorities;
3. read the matching report-specific gate(s);
4. for Report №02, read the primary canonical gate, the implementation-report format gate and the physical-layout gate;
5. apply the Report №02 client-visible title/structure from the canonical gate, not legacy filename wording;
6. verify that every non-obvious section can be explained in ordinary Russian by a reader who did not participate in the research;
7. verify that report production did not silently acquire new project-specific evidence outside the completed research scope;
8. inspect the final committed recipient artifact, not only source text or a predecessor render;
9. do not mark another report PASS merely because one report's gate passed.
