# KWORK PORTFOLIO — SERP COVERAGE MODE RESEARCH

Date: 2026-09-10
Status: **PORTFOLIO-LEVEL METHOD RESEARCH / OWNER-DIRECTED INPUT**
Scope: all current/future Kwork products and mini-kworks that use ordinary Yandex Search as semantic/page evidence.

## 1. Research question

The project must distinguish two legitimate ordinary-Search evidence strategies:

```text
FULL_SERP_COVERAGE
= direct current SERP evidence exists for every phrase in the declared final Search-covered set.

SELECTIVE_DECISION_SERP
= every governed phrase is still semantically processed, but direct current SERP is acquired/reused only for product-defined decision-relevant anchors, conflicts, boundaries, controls or unresolved cases.
```

A third valid product mode is:

```text
NO_ORGANIC_SERP_BASE
= the sold result does not require ordinary organic SERP as a normal base evidence layer.
```

A fourth scoped mode is:

```text
HYBRID_SCOPED_FULL
= selected sub-universes receive FULL_SERP_COVERAGE while the rest uses SELECTIVE_DECISION_SERP or no fresh Search.
```

These modes are different product-method choices. None is universally correct for every Kwork.

## 2. What was previously confused

Three axes must remain separate:

```text
A. CLUSTERING BASIS
   semantic/task/intent
   SERP overlap
   hybrid

B. SEARCH COVERAGE
   every phrase in declared set
   selected decision-relevant phrases
   none

C. EXECUTION ENGINE
   deterministic code/tool
   LLM/Work
   human review
   hybrid
```

`FULL SERP != LLM MUST READ EVERY RAW SERP BODY`.

`SELECTIVE SERP != ONLY SOME PHRASES RECEIVE SEMANTIC ANALYSIS`.

`AUTOMATED CLUSTERING != FULL SERP BY DEFINITION`.

## 3. External sources and exact implications

### Yandex Webmaster — query selection / clustering context
https://yandex.ru/support/webmaster/ru/service/queries-selection

Supports:
- queries can be grouped by meaning/user intent;
- target-query selection may use demand, clicks and competition;
- non-target requests can be excluded.

Does not prove:
- every semantic product must obtain a fresh TOP for every phrase;
- any universal sample size is sufficient.

### Topvisor — SERP clustering method
https://topvisor.com/ru/support/clustering/method/

Supports:
- SERP-based clustering obtains search results for compared phrases;
- URL overlap can be processed under configurable Soft/Moderate/Hard-style logic;
- overlap degree is configurable rather than one universal semantic truth.

Implication:
FULL_SERP_COVERAGE is a legitimate professional method when the sold result is SERP-based clustering or when direct page-compatibility evidence is intentionally required for the declared set.

### Rush Analytics — keyword clustering
https://www.rush-analytics.ru/faq/klasterizaciya-zaprosov-semanticheskogo-yadra-rukovodstvo

Supports:
- search-result similarity is a standard grouping route;
- cleaning before clustering is required;
- automated grouping still benefits from manual/analytical review.

### Ahrefs — keyword clustering
https://ahrefs.com/blog/keyword-clustering/

Supports:
- search intent and SERP similarity are related but not identical analytical dimensions;
- pair/query SERPs can resolve same-page compatibility;
- automated output can require analyst correction.

### Ahrefs — keyword clustering tools / Parent Topic / term clustering
https://ahrefs.com/blog/keyword-clustering-tools/

Supports:
- not every clustering workflow requires a fresh full-SERP comparison conducted manually at execution time;
- term clustering is useful for topical discovery but does not prove same-page intent;
- existing indexed/provider-derived search evidence can enable faster grouping routes.

### Semrush — keyword clustering
https://www.semrush.com/blog/keyword-clustering/

Supports:
- intent, content completeness/user journey and SERP evidence can all matter;
- lexical similarity alone is insufficient for page-level decisions.

### Semrush — clustering/topic-modeling methods
https://www.semrush.com/blog/what-are-methods-for-keyword-clustering-and-topic-modeling/

Supports:
- semantic/topic-modeling and SERP-based/automated routes are distinct useful methods;
- there is no basis for forcing one method on every product.

### SE Ranking — keyword clustering
https://seranking.com/blog/keyword-clustering/

Supports:
- morphology/semantic grouping and SERP-based grouping are distinct approaches;
- automated grouping is particularly useful for larger lists/new structures;
- final review remains important.

## 4. FULL_SERP_COVERAGE — when it is justified

Use FULL when the sold promise materially depends on direct observed SERP compatibility for every phrase in the declared Search set.

Strong cases:

```text
standalone "clustering by Yandex TOP" product
final clustering for a greenfield/new target architecture when the product explicitly promises SERP-grounded page boundaries
client-provided keyword list whose page compatibility is the core object of the order
scoped sub-universe where every phrase must have current direct Search evidence before page design
```

FULL provides stronger direct observation coverage and reduces blind spots caused by analyst-selected sampling.

FULL does NOT mean:

```text
run Search on RAW acquisition occurrences
run Search on excluded/reserve phrases by default
accept overlap as automatic page truth
skip business-fit/task/intent review
feed every raw Search body to Work
```

Required architecture:

```text
cleaned/frozen Search set
-> direct/reused SERP for every member
-> deterministic projection/URL comparison where useful
-> semantic/business review
-> final clustering/page decision
```

## 5. SELECTIVE_DECISION_SERP — when it is justified

Use SELECTIVE when ordinary Search is evidence for specific decisions rather than the sold primary dataset.

Strong cases:

```text
existing-site semantic rebuild
semantic core/cleanup product not sold as full TOP clustering
competitor/niche diagnostic research
page ownership or cannibalization work with existing site/history where only unresolved current boundaries need fresh Search
AI/Alice diagnostic products where ordinary Search forms a baseline/control set rather than a complete rank study
implementation-TZ work using already accepted upstream semantic authority
```

Correct SELECTIVE design:

```text
all governed phrases receive semantic/accounting treatment
-> identify explicit Search-resolvable decisions
-> build bounded Search manifest
-> include anchors + conflicting modifiers + ambiguous cases + controls
-> acquire/reuse direct Search evidence
-> do not silently generalize to unprobed rows
-> leave unresolved state where evidence is still insufficient
-> expand tranche only when another Search can materially change a decision
```

SELECTIVE does NOT mean:
- choose the highest-frequency N and call them representative;
- one cleanup reason/source seed automatically defines an intent family;
- unprobed phrase is "Search-confirmed";
- a fixed number such as 40/75 is universally sufficient.

## 6. HYBRID_SCOPED_FULL

Use HYBRID when the product contains materially different subproblems.

Example:

```text
existing site with 1500 active phrases
-> selective current Search for most established sections
-> full SERP coverage for one new/rebuilt 300-phrase category subtree
```

This must be frozen at product/method level or by an explicit versioned product branch; it must not emerge silently during an order.

## 7. NO_ORGANIC_SERP_BASE

Products whose sold evidence is primarily advertising/account performance, exact-frequency enrichment, implementation from accepted upstream authority or imported datasets may not need organic SERP as a normal base route.

Fresh ordinary Search is then optional and must have a named evidence purpose.

## 8. Portfolio design rule

SERP coverage mode is a PRODUCTIZATION decision, not a recurring per-order methodology debate.

Required one-time sequence for each Kwork/mini-kwork version:

```text
freeze sold result
-> read this research
-> inspect source methods relevant to that result
-> inspect current Bridge/provider capabilities and costs
-> compare FULL / SELECTIVE / HYBRID / NONE
-> document why chosen mode proves the sold result with acceptable workload/cost
-> rehearse chosen mode
-> freeze it in that product's Level-1 roadmap/rules/runbook
-> ordinary client jobs execute the frozen mode
```

A new client order must not re-prove the mode from scratch.

Re-open mode selection only when the commercial promise, supported operating mode, provider route, cost model or product version materially changes.

## 9. Current product decisions vs pending decisions

Current owner/product state:

```text
KW-001 = SELECTIVE_DECISION_SERP
Reason: existing-site AI-native semantic rebuild; accepted methodology uses bounded Search for material boundaries rather than full per-keyword TOP coverage.

KW-002 = FULL_SERP_COVERAGE
Owner decision: 2026-09-10.
Scope: only the final cleaned / delivery-selected Search set, NOT RAW Wordstat occurrences or reserve/excluded rows.
Purpose: full SERP-grounded final clustering/page architecture for the greenfield/from-scratch product.

KW-003..KW-008 = PENDING_PRODUCTIZATION_DECISION
Do not pre-freeze from portfolio analogy. Decide once when each product roadmap is developed.
```

Mini-kwork decisions are governed separately by the mini-kwork productization gate/registry.

## 10. Evidence and claim rules common to both Search modes

```text
EXACT QUERY OBSERVATION != UNPROBED QUERY EVIDENCE
SERP OVERLAP != AUTOMATIC SAME-PAGE TRUTH
DOMAIN OVERLAP != URL OVERLAP
CURRENT SERP != HISTORICAL QUERY-URL COMPETITION
SEARCH ABSENCE != SITE ABSENCE
FULL COVERAGE != CORRECT CLUSTERING WITHOUT SEMANTIC QA
SELECTIVE COVERAGE != PERMISSION TO HIDE UNRESOLVED ROWS
```

## 11. Data-processing rule

Large Search evidence should be separated into:

```text
RAW SEARCH EVIDENCE = durable machine provenance
COMPACT SERP PROJECTION = query -> ranked URLs/domains/result types
DETERMINISTIC COMPARISON = URL overlap / graph / candidate groups when method uses it
ANALYST/WORK INPUT = compact candidates + conflicts + boundaries + representative evidence
```

LLM/Work should not be used as a calculator for millions of pairwise URL comparisons.

## 12. Cost is a factor, not the method authority

The chosen SERP mode must account for provider cost and operator/LLM burden, but price alone does not decide methodological sufficiency.

Current Yandex Search API pricing research is maintained separately in:

`YANDEX_SEARCH_ASYNC_DEFERRED_RESEARCH_2026-09-10.md`

## 13. Portfolio acceptance rule

Before a Kwork/MK becomes READY_TO_SELL, its Level-1 authority must contain:

```text
SERP_COVERAGE_MODE = FULL_SERP_COVERAGE | SELECTIVE_DECISION_SERP | HYBRID_SCOPED_FULL | NO_ORGANIC_SERP_BASE
WHY_THIS_MODE_FITS_SOLD_RESULT
SEARCH_SET_DEFINITION
REUSE_RULE
FRESH_SEARCH_TRIGGER
WHAT_COUNTS_AS_SEARCH_COVERED
UNPROBED/FAILED BEHAVIOR
PROVIDER/COST ROUTE
CLAIM BOUNDARY
REHEARSAL RESULT
```

If this decision is missing, productization is incomplete.