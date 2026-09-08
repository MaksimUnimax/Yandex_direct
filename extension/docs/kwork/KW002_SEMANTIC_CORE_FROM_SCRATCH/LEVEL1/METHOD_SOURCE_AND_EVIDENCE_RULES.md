# KW-002 — LEVEL 1 METHOD SOURCE AND EVIDENCE RULES

Status: **ACTIVE / OWNER-AUTHORIZED SCAFFOLD**

## 1. Source classes

Material method elements must be labelled by source class:

```text
OFFICIAL_YANDEX
INDUSTRY_PRACTICE
PROJECT_TEST_VALIDATED
INHERITED_KW001_RULE
ANALYST_HEURISTIC
OWNER_SCOPE_RULE
```

A project-authored rule does not prove itself.

## 2. Current external method base

Official Yandex sources:

```text
Wordstat overview:
https://yandex.ru/support2/wordstat/ru/

Wordstat operators:
https://yandex.ru/support2/wordstat/ru/content/operators

Yandex relevance / E-P-O-S / user task:
https://yandex.ru/support/webmaster/ru/epos

Site structure:
https://yandex.ru/support/webmaster/ru/recommendations/site-structure

How Alice AI answers / source selection:
https://yandex.ru/support/webmaster/ru/alice

Alice AI site visibility / competitor-content examples:
https://yandex.ru/support/webmaster/ru/service/alice-answers
```

Industry corroboration for keyword clustering:

```text
Ahrefs keyword clustering:
https://ahrefs.com/blog/keyword-clustering/

Semrush keyword clustering:
https://www.semrush.com/blog/keyword-clustering/
```

These sources support the execution design. They do not substitute for current-job provider/Search evidence.

## 3. Core supported method principles

### Demand acquisition

Wordstat is used to discover and measure Yandex search-demand formulations, related searches, regional demand and dynamics where needed.

Wordstat operators may be used deliberately when the question requires phrase-form/order/word-count refinement. Operator measurements must not be confused with broad unquoted demand.

### User-task first

A phrase is not assigned to a page merely because its words resemble another phrase. Page/cluster decisions must consider the task the user is trying to solve and the type of result/page that Yandex currently rewards for that task.

### SERP similarity is evidence, not an automatic verdict

Keyword clustering may use similarity/overlap of current Yandex result sets together with semantic meaning and intent.

There is no universal project rule such as:

```text
shared_urls >= N => same page
```

Any numeric threshold used in a specific job is a job-level heuristic/configuration and must be justified against that dataset.

### Site architecture

Final planned pages must form a clear structure, be assigned to logical sections and have unique URL roles. A retained important page/job must not become an orphan in the final IA.

### AI-search evidence

Yandex states that generative answers use search-derived content and may cite source pages. AI-search output can vary over time and source order is not a ranking list.

Therefore AI-search evidence is used as bounded current evidence about:

```text
user-task framing
answer structure
source/page types
commercial vs informational orientation
content depth/coverage signals
```

It is not used to promise stable future inclusion or ranking.

## 4. Source-to-method trace

Every Level 2 step must state:

```text
METHOD ELEMENT
→ SOURCE CLASS
→ WHY IT SUPPORTS THE STEP
→ EXECUTABLE ACTION
→ CLAIM BOUNDARY
→ PASS/FAIL/HOLD CHECK
```

## 5. Evidence preservation

Provider and Search evidence must preserve at minimum:

```text
query/seed
region
observation time/job identity
provider/search mode
raw or durable normalized result reference
source/provenance
status/error truth
```

Derived tables must keep deterministic links back to upstream evidence.

## 6. Cost does not define analytical truth

Provider cost is tracked because the Kwork must be commercially repeatable.

But:

```text
CHEAPEST EVIDENCE ROUTE != AUTOMATICALLY BEST METHOD
MOST EXPENSIVE EVIDENCE ROUTE != AUTOMATICALLY HIGHER QUALITY
```

Use information gain, relevance, durability and claim requirements to decide whether another call is justified.
