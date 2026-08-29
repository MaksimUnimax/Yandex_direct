# KW-001 — SOURCE TO METHOD TRACEABILITY GATE

Date: 2026-08-29
Status: **ACTIVE / UNIVERSAL / OWNER-APPROVED / OWNER-LOCKED**

## Purpose

External research before a step is not useful if ChatGPT can collect good sources and then invent unsupported method states, thresholds, routes or decisions anyway.

Canonical rule:

```text
RESEARCH_COLLECTED != METHOD_VALIDATED
```

This gate converts external research from background reading into a constraint on the actual method.

## Mandatory rule before every major step

Every material method element must have an explicit trace:

```text
METHOD ELEMENT
→ DIRECT SOURCE OR PROJECT EVIDENCE
→ EXACT CLAIM THE SOURCE/EVIDENCE SUPPORTS
→ PROJECT-SPECIFIC ADDITION, IF ANY
→ REAL EXECUTABLE NEXT ACTION / OBSERVABLE OUTPUT
```

A material method element includes any:

```text
status/state
classification category
routing category
threshold
filter
merge rule
selection rule
sampling rule
provider action
pass/fail condition
page/cluster decision rule
priority rule
```

If a method element cannot complete that trace, it is unsupported.

```text
UNSUPPORTED_METHOD_ELEMENT = BLOCKED
```

## Direct sources are mandatory

The owner-facing pre-step report must include direct links next to the claims they support.

Source classes:

```text
OFFICIAL
INDUSTRY_PRACTICE
PROJECT_TEST_VALIDATED
ANALYST_HEURISTIC / PROJECT-SPECIFIC
```

`ANALYST_HEURISTIC` is allowed only when:

```text
1. no stronger source defines the exact mechanic;
2. the project need is explicit;
3. the heuristic does not contradict external evidence;
4. it maps to a real executable action/output;
5. it is labelled as project-specific rather than presented as external methodology.
```

## Unsupported symmetry / invented taxonomies are forbidden

Do not create states merely because a symmetric taxonomy looks complete.

Example of the failure this gate prevents:

```text
real evidence route = SEARCH
known evaluation dimension = BUSINESS FIT

WRONG:
SEARCH
BUSINESS
SEARCH_AND_BUSINESS

unless BUSINESS is an actual independently available evidence source/action.
```

An empty category is not automatically wrong, but if a category has:

```text
no rows
+ no external methodological support
+ no proven project necessity
+ no executable next action
```

then the default conclusion is that the category should not exist.

## Evaluation dimension != evidence route

Do not convert an analytical dimension into an evidence source merely because both matter to a decision.

Examples:

```text
search intent = analytical/evidence dimension
business potential = analytical/evaluation dimension
search result = observable evidence source
client CRM/margin/capacity = separate evidence only if actually available
```

If private client data is unavailable, preserve that as a limitation or later client-confirmation point. Do not invent a future route that the workflow cannot execute.

## Mandatory adversarial questions

Before authorization ask for every material method element:

```text
Where did this element come from?
Which direct source supports it?
What exactly does that source say that justifies this element?
Am I extending the source beyond what it supports?
If project-specific, what concrete problem requires it?
What real next action executes it?
What happens if no data ever enters this state?
Can the method be simpler without losing necessary evidence?
Did I invent this category because it looked tidy rather than because the data/method requires it?
```

## Required owner-facing trace table

For every major step, before authorization, show or record at least:

```text
| Method element | Source / evidence | What it supports | Project-specific part | Executable action/output |
```

The table may group repeated rules, but no material state/rule may be omitted.

## Pass gate

Before execution:

```text
DIRECT_SOURCE_LINKS_PRESENT = true
MATERIAL_METHOD_ELEMENTS_TRACED = true
UNSUPPORTED_METHOD_ELEMENTS = 0
NON_EXECUTABLE_EVIDENCE_ROUTES = 0
PROJECT_SPECIFIC_ELEMENTS_LABELLED = true
SOURCE_CLAIMS_NOT_OVEREXTENDED = true
```

If any fail:

```text
METHOD_VERDICT = CORRECTION_REQUIRED
STEP_AUTHORIZATION = BLOCKED
EXECUTION = BLOCKED
```

## Error that caused this universal rule

A Step-8 Search-stage freeze correctly researched Yandex, Ahrefs and Semrush, but then invented `REVIEW_BUSINESS` and `REVIEW_SEARCH_AND_BUSINESS` routing states. The sources supported user need/site fit, intent, business potential and downstream clustering/mapping, but did not support treating internal business priority as a separate evidence provider.

The process failure was not lack of sources. It was failure to trace each invented method element back to the source claim before execution.

Direct supporting methodology checked during correction:

- Yandex — user need/site-query fit: https://yandex.ru/support/webmaster/ru/recommendations/targeting
- Yandex — target query selection/potential: https://yandex.ru/support/webmaster/ru/service/queries-selection
- Yandex — query/page Search evidence: https://www.yandex.ru/support/webmaster/ru/service/search-queries
- Ahrefs — keyword/search intent: https://ahrefs.com/blog/keyword-intent/
- Ahrefs — business potential + intent/content strategy: https://ahrefs.com/blog/keyword-strategy/
- Semrush — clustering by shared intent: https://www.semrush.com/blog/keyword-clustering/
- Semrush — keyword mapping: https://www.semrush.com/blog/keyword-mapping/

Markers:

```text
KW001_SOURCE_TO_METHOD_TRACEABILITY_REQUIRED = true
KW001_RESEARCH_COLLECTED_NOT_EQUAL_METHOD_VALIDATED = true
KW001_UNSUPPORTED_METHOD_ELEMENT_FORBIDDEN = true
KW001_NON_EXECUTABLE_EVIDENCE_ROUTE_FORBIDDEN = true
KW001_PROJECT_SPECIFIC_METHOD_MUST_BE_LABELLED = true
KW001_DIRECT_SOURCE_LINKS_REQUIRED_FOR_METHOD_CLAIMS = true
```