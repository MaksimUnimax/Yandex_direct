# KW-002 Blood & Sand — post-sanitation Step04 pre-step external research

Date checked: 2026-09-11
Status: **PRE-STEP EXTERNAL METHOD RESEARCH COMPLETE / EXECUTION METHOD CONFIRMED WITH BOUNDARIES**

Current step:

`POST-SANITATION STEP04 FULL-VOLUME FAMILY TRIAGE REWRITE`

Mandatory anti-regression authority:

`LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`

Job failure authority:

`KW002_EXECUTION_FAILURE_LEDGER_2026-09-11.md`

## Exact methodological questions checked

1. Is grouping search demand into semantic/intent families a legitimate analytical operation before final page mapping?
2. Should ambiguous phrases be resolved by token rules alone?
3. Is final SEO clustering equivalent to preliminary topical/family grouping?
4. Should SERP similarity be reserved for a later stronger clustering/page-ownership decision?
5. Can demand/frequency alone define relevance/family priority?

## Source-to-method trace

| source_id | source_title | publisher | source_class | url | checked_at | method_element_supported | exact_claim_supported | project_specific_application | claim_boundary |
|---|---|---|---|---|---|---|---|---|---|
| S04-01 | Подбор поисковых запросов и анализ рынка | Yandex Webmaster | OFFICIAL_SEARCH_ENGINE | https://yandex.ru/support/webmaster/ru/service/queries-selection | 2026-09-11 | semantic/intent grouping; demand discovery; market pages | Yandex describes a cluster as automatic grouping of queries close by meaning or intent; tool exposes demand/clicks/competition and additional queries/popular pages | Step04 may organize corrected demand into preliminary meaning/intent families and flag gaps | This does not prove final query-to-page ownership or our family labels |
| S04-02 | Как измеряется и улучшается качество Поиска | Yandex Webmaster | OFFICIAL_SEARCH_ENGINE | https://yandex.ru/support/webmaster/ru/search-quality | 2026-09-11 | user-task relevance boundary | Yandex states Search aims to provide relevant information that helps the user solve the task; search analyzes query/content/context factors | Step04 must not treat a lexical token as sufficient proof of user task/referent; ambiguity survives | Does not prescribe a specific SEO family-triage algorithm |
| S04-03 | Как сделать кластеризацию запросов по ТОП-10 | Topvisor | INDUSTRY_PRACTICE | https://topvisor.com/ru/support/clustering/ | 2026-09-11 | later SERP-based clustering boundary | Topvisor clusters queries based on sites in TOP-10 and uses it for site-structure work | Confirms final clustering should remain later, after ordinary SERP evidence, rather than being silently performed at Step04 | Tool-specific implementation; not an official Yandex rule |
| S04-04 | How To Do Keyword Clustering the Easy Way | Ahrefs | INDUSTRY_PRACTICE | https://ahrefs.com/blog/keyword-clustering/ | 2026-09-11 | intent/SERP similarity vs term buckets | Ahrefs describes final keyword clustering as grouping same/similar intent, commonly via similar search results; term clustering is separately useful for topical buckets/trends | Step04 may form topical/family buckets; Step13 later uses SERP+intent evidence for final clusters | Examples use Google/Ahrefs; principle is corroborative, not Yandex-specific |
| S04-05 | How to Do Keyword Clustering & Why It Helps SEO | Semrush | INDUSTRY_PRACTICE | https://www.semrush.com/blog/keyword-clustering/ | 2026-09-11 | subtle intent differences; SERP similarity | Semrush describes clustering by shared intent and SERP similarity and shows subtle wording can alter intent | Step04 must preserve mixed/ambiguous cases rather than forcing them into final cluster/page decisions | Third-party practice, not official Yandex guidance |
| S04-06 | Keyword Intent: What It Is and How to Use It in Your SEO Strategy | Ahrefs | INDUSTRY_PRACTICE | https://ahrefs.com/blog/keyword-intent/ | 2026-09-11 | early intent map vs later SERP refinement | Ahrefs distinguishes keyword intent as an earlier research filter and discusses mixed intent/SERP-based identification | Supports preliminary user-task/family hints but not destructive final intent assignment in Step04 | Third-party practice; later project Yandex SERP remains authority for final clustering |

## Method conclusion

External evidence supports the existing staged design with the following explicit boundary:

```text
STEP04 = PRELIMINARY FAMILY / TOPIC / CONTEXT TRIAGE
STEP04 != FINAL SERP CLUSTERING
STEP04 != QUERY->PAGE OWNERSHIP
STEP04 != FINAL INTENT VERDICT FOR AMBIGUOUS ROWS
```

Step04 may use:

- frozen client/business/assortment evidence;
- corrected Step03B KEEP/HOLD states;
- normalized phrase text and preserved lineage;
- family-level semantic/context patterns;
- frequency/demand only as descriptive/supporting evidence, never sole relevance proof.

Step04 must preserve:

- ambiguous/mixed referents;
- unresolved product-vs-information collisions;
- gaps that genuinely justify later targeted expansion;
- feedback where Step03B still appears too broad/narrow, without silently rewriting Step03B.

Step04 must not perform:

- final row-level KEEP/REJECT cleanup;
- final intent classification;
- ordinary SERP acquisition;
- SERP-overlap clustering;
- page ownership;
- IA/Page Jobs;
- Step05 acquisition.

## Required anti-regression effect on execution

The Work pass must explicitly test these historical failures:

```text
F03B-1 broad token/regex collision
F03B-2 business-token fallback overriding foreign context
F03B-3 mechanical QA mistaken for semantic QA
F03B-4 ambiguity destroyed too early
F04-1 missing occurrence-level family ledger
F04-2 example-only patch instead of rule-level rerun
F04-3 upstream sanitation correction invalidating downstream family conclusions
```

## Gate

```text
PRE_STEP_EXTERNAL_RESEARCH = PASS
SOURCE_DISCLOSURE_IN_CHAT = PASS
SOURCE_TO_METHOD_TRACE = PASS
KNOWN_FAILURES_IDENTIFIED = PASS
METHOD_BOUNDARY_CONFIRMED = PASS
PROVIDER_CALLS_REQUIRED_FOR_STEP04 = 0
STEP05_ALLOWED = false
POST_SANITATION_STEP04_WORK_EXECUTION = ALLOWED AFTER CANONICAL WORK PROMPT FREEZE
```
