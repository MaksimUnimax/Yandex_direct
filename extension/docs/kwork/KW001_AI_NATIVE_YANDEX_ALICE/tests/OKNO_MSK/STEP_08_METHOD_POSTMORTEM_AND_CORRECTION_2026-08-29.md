# KW-001 / OKNO-MSK — STEP 08 METHOD POSTMORTEM AND CORRECTION

Date: 2026-08-29
Status: **CORRECTION APPLIED / ORIGINAL ROUTING MODEL SUPERSEDED**

## What was done wrong

The original Step-08 routing model introduced:

```text
REVIEW_BUSINESS
REVIEW_SEARCH_AND_BUSINESS
```

and then defended `REVIEW_BUSINESS = 0` as a valid empty category.

That was methodologically wrong.

No external source used in the Step-08 research defined `business` as a separate downstream evidence provider or resolution route. The model confused two different concepts:

```text
SEARCH INTENT / SERP EVIDENCE
= what the user means and what result/page type Search rewards

BUSINESS RELEVANCE / BUSINESS POTENTIAL
= whether the known offer can naturally satisfy and benefit from that demand
```

It then made a second mistake by mixing those with:

```text
INTERNAL BUSINESS PRIORITY
= margin, capacity, strategic growth preference, operational priority
```

Internal priority may be unavailable in a public-site rehearsal, but that does not create a semantic route called `BUSINESS`.

## Direct external sources

### Yandex — user need and site/query fit

https://yandex.ru/support/webmaster/ru/recommendations/targeting

Yandex states that Search answers users' questions and that page content should match how users formulate their needs. It recommends selecting suitable phrases around the product/service.

Method consequence:

```text
QUERY RELEVANCE
= user need + known site/business offer
```

This source does not establish a separate `business evidence queue`.

### Yandex — selecting target queries

https://yandex.ru/support/webmaster/ru/service/queries-selection

Yandex describes selecting suitable queries, analyzing their potential and studying pages/competition.

Method consequence:

```text
query suitability/potential is evaluated for the site;
not delegated to a fictitious future business-data route.
```

### Yandex — query/page evidence

https://www.yandex.ru/support/webmaster/ru/service/search-queries

Yandex exposes which pages appear for which queries.

Method consequence:

```text
query/page compatibility belongs to Search evidence.
```

### Ahrefs — keyword/search intent

https://ahrefs.com/blog/keyword-intent/

Updated 2026-03-13. Ahrefs describes keyword intent as the reason behind a query and as a filter for whether a keyword belongs in a strategy. It separately discusses Business Potential.

Method consequence:

```text
INTENT != BUSINESS POTENTIAL
but
both are evaluation dimensions;
neither is automatically a separate evidence-provider route.
```

### Ahrefs — keyword strategy

https://ahrefs.com/blog/keyword-strategy/

Updated 2026-03-13. The strategy separates scoring business potential from mapping keywords to search intent/content type and later priority/topic organization.

Method consequence:

```text
business potential helps evaluate/prioritize a keyword;
search intent helps understand expected content/result fit;
these should not be encoded as parallel evidence queues unless actual separate evidence sources exist.
```

### Semrush — clustering by shared intent

https://www.semrush.com/blog/keyword-clustering/

Semrush defines clustering around terms that share the same search intent and can be targeted on one page.

Method consequence:

```text
final cluster/page compatibility belongs downstream of intent/SERP evidence.
```

### Semrush — keyword mapping

https://www.semrush.com/blog/keyword-mapping/

Updated 2026-07-27. Keyword mapping connects target topics/keywords with existing or planned pages and is sensitive to changes in search results.

Method consequence:

```text
page ownership/mapping remains downstream;
Step 8 should only freeze and route evidence.
```

## Root cause

The central process failure was:

```text
EXTERNAL RESEARCH WAS COLLECTED
but
EACH INVENTED METHOD ELEMENT WAS NOT TRACED BACK TO A SOURCE OR PROVEN PROJECT NEED
```

I used the sources as general confirmation that the overall workflow sounded reasonable, then invented a symmetric taxonomy because it looked organized:

```text
SEARCH
BUSINESS
SEARCH + BUSINESS
DEFERRED
```

That is exactly what the pre-step research is supposed to prevent.

The empty `REVIEW_BUSINESS = 0` should have triggered the question:

```text
Does this class actually represent a necessary real workflow action?
```

Instead it was defended after the fact.

## Why the old model was invalid

A routing state must correspond to a real next evidence action.

In this job there is no provider, account, dataset or planned interaction that can execute:

```text
RESOLVE_BY_BUSINESS
```

The current base rehearsal explicitly has no private CRM/margin/capacity strategy data.

Therefore `REVIEW_BUSINESS` and `REVIEW_SEARCH_AND_BUSINESS` were not actionable evidence routes.

## Corrected method

The corrected Step-08 routing model contains only:

```text
CORE_CANDIDATE
REVIEW_SEARCH
REVIEW_DEFERRED
EXCLUDED_PRESERVED
```

Exact meanings:

```text
CORE_CANDIDATE
= accepted Step-07C KEEP.

REVIEW_SEARCH
= ordinary Search/SERP evidence is required to resolve intent, relevance, result type, semantic/page boundary or compatibility.

REVIEW_DEFERRED
= unresolved evidence preserved without an immediate bounded Search action; current class is association-only evidence.

EXCLUDED_PRESERVED
= accepted Step-07C exclusion retained only for audit.
```

These names are PROJECT-SPECIFIC mechanics, not external standards.

## Corrected numerical truth

```text
CORE_CANDIDATE = 1388
REVIEW_SEARCH = 944
REVIEW_DEFERRED = 174
EXCLUDED_PRESERVED = 334
TOTAL = 2840

all REVIEW routed = 1118/1118
REVIEW_BUSINESS = removed / forbidden
REVIEW_SEARCH_AND_BUSINESS = removed / forbidden
silent drops = 0
Step-07C semantic status rewrites = 0
```

## Non-exact duplicate correction

The corrected duplicate routes are:

```text
ORDINARY_SEARCH_BEFORE_ANY_NONEXACT_MERGE = 8 groups
DEFER_UNLESS_GROUP_SELECTED_FOR_SEARCH = 1 group
AUTO_MERGED = 0
```

No duplicate group is routed to a nonexistent business evidence channel.

## New non-repeat rule

Before execution, every material method element must have this trace:

```text
METHOD ELEMENT
→ DIRECT SOURCE OR PROJECT EVIDENCE
→ EXACT CLAIM THE SOURCE SUPPORTS
→ PROJECT-SPECIFIC ADDITION, IF ANY
→ REAL EXECUTABLE NEXT ACTION
```

If any one of these is missing:

```text
METHOD_ELEMENT = UNSUPPORTED
EXECUTION = BLOCKED
```

Canonical lesson:

```text
RESEARCH_COLLECTED != METHOD_VALIDATED
SOURCE_TO_METHOD_TRACEABILITY_REQUIRED = true
UNSUPPORTED_DECISION_STATE_FORBIDDEN = true
NON_EXECUTABLE_EVIDENCE_ROUTE_FORBIDDEN = true
```

## Current boundary

This correction does not authorize Step 9. Step 9 still requires its own fresh pre-step method research, source-to-method traceability, owner-facing review and explicit authorization.