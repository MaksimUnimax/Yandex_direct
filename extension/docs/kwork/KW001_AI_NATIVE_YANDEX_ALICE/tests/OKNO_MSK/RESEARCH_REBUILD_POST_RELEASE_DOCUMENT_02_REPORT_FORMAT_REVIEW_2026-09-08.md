# OKNO_MSK — review of Report №02 format against implementation-report practice

Date: 2026-09-08
Status: METHOD REVIEW COMPLETE
Scope: external reporting methodology only; no new OKNO_MSK project facts were collected.

## Why this review was opened

Owner review showed that the current Report №02 still mixed three different things:

1. concrete recommendations that can be implemented;
2. reference data produced by the research;
3. internal control language about what the recipient should or should not do.

This made the document difficult to understand for a non-specialist even though individual facts were correct.

## External reporting patterns reviewed

### Search Engine Journal — technical audit deliverables

Source: “Understanding the Role of a Technical SEO Audit”
https://www.searchenginejournal.com/technical-seo-audit-role/342797/

Relevant reporting pattern:

- keep the written report manageable;
- keep supporting data separate or clearly annotated;
- include a practical work list / activity register;
- design the deliverable around implementation, not around reproducing every piece of audit data.

### Ahrefs — enterprise audit deliverables

Source: “What is an Enterprise SEO Audit & How To Do One”
https://ahrefs.com/blog/enterprise-seo-audit/

Relevant reporting pattern:

- focus the main deliverable on the small number of issues/opportunities that matter most;
- avoid making the main report a huge catalogue that nobody can act on;
- adapt the deliverable to the people who will use it.

### Semrush — content audit action plan

Source: “How to do a website content audit”
https://www.semrush.com/blog/content-audit/

Relevant reporting pattern:

- analysis must be converted into an action plan;
- each object receives a clear action/state;
- the implementation view should make the next action obvious.

### U.S. GAO — recommendation quality

Source: Government Auditing Standards, recommendations section
https://www.gao.gov/assets/a76972.html

Relevant reporting pattern:

- recommendations must follow logically from findings;
- recommended actions should be specific, practical and measurable;
- the report should make the required action clear to a knowledgeable reader.

## Applied conclusion for OKNO_MSK Report №02

The main document must be an action-first implementation report, not a raw research register.

Permanent structure rule:

```text
MAIN REPORT
= WHAT TO CHANGE + WHY + HOW + RESULT

SUPPORTING TABLE
= WHAT DATA TO USE WHEN IMPLEMENTING OR PREPARING THE NEXT STEP
```

A table that contains research output is not self-explanatory. Before any non-obvious table, the report must explain in ordinary Russian:

1. what this table represents;
2. why it is useful;
3. how to use it in practice.

## Owner-identified format defects from the current document

### Defect Q — recipient role became the document title

The report displayed wording such as “руководство специалиста” and “для SEO-специалиста, редактора и разработчика”.

Correction:

- the client document is named by its purpose/result;
- recipient job titles are omitted unless they are materially necessary to a concrete task.

### Defect R — semantic/page routing register was shown without plain-language meaning

A 46-row table was labelled “Семантические назначения” and followed by abstract wording about a semantic core and content plan.

Correction:

- use plain heading “Распределение тем по страницам”;
- explain what “main page” and “related page” mean;
- explain why the table exists and how it is used when writing or updating content;
- use plain column names.

### Defect S — internal-link candidate register was shown without purpose or method

A 14-pair table said only that a block, surrounding text and link wording must be determined.

Correction:

- explain what a pair of pages means;
- explain why such a transition is useful to the visitor and to the site structure;
- explain the implementation method in ordinary language;
- keep the pair table as the direction of the transition, not as a substitute for the method.

### Defect T — standalone preservation section replaced implementation value

The section “Требования к существующей структуре” was a defensive list rather than an implementation step.

Correction:

- remove the standalone section;
- keep only concrete preservation conditions inside the acceptance criteria of the recommendation where they are actually material.

### Defect U — research-process framing dominated the implementation document

Long funnel explanations and internal terminology made the implementation report look like a second research report.

Correction:

- the implementation report starts with the work map and recommendations;
- detailed research explanation remains in Report №01 and the data workbook;
- Report №02 keeps only the minimum context needed to understand why a recommendation exists.

## Acceptance consequence

Report №02 can pass only when a non-specialist owner can answer, from the document itself:

- what will be changed now;
- what still needs a concrete clarification;
- what the 46 topic-to-page rows mean and how they are used;
- what the 14 page-to-page pairs mean and how a link is implemented;
- what result is expected from each additional check.

No implementation schedule, owner assignment, effort estimate or business impact number may be invented when those decisions were not part of the completed work.
