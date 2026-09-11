# MK03 STEP 08 — BOUNDED STRUCTURAL OPPORTUNITY INTERPRETATION

## Purpose
Translate confirmed gaps into useful next-step content/page/section opportunity notes without silently delivering MK02/MK05.

## Why this step exists
A client needs to know what a confirmed gap may imply, but semantic absence alone cannot prove final architecture.

## Inputs
CONFIRMED_GAP decisions plus current-site context and page-type/intent evidence available from prior steps.

## Required evidence
Gap evidence, current coverage state, observed competitor page types and Search intent/page-type evidence where material.

## Method
For each confirmed gap, state one bounded result when supported:

```text
CONTENT/TOPIC EXPANSION OPPORTUNITY
EXISTING-PAGE COVERAGE OPPORTUNITY
NEW LANDING-PAGE CANDIDATE — REQUIRES ARCHITECTURE VALIDATION
NEW SECTION/CATEGORY CANDIDATE — REQUIRES ARCHITECTURE VALIDATION
INFORMATIONAL CONTENT CANDIDATE
NO STRUCTURAL RECOMMENDATION YET
```

Explain evidence meaning, expected user task and what additional decision is needed before implementation where applicable.

Do not assign final target URL, complete ownership hierarchy, internal-link architecture or implementation-ready ticket unless separately in scope.

## Outputs
`STRUCTURAL_OPPORTUNITY_REGISTER` linked to gap IDs.

## Source authority
PRODUCT_SCOPE neighbouring-product boundaries; Step5A “no automatic page creation” rule; reusable MK02 target/action separation lesson.

## Known failures / root causes
- confirmed gap auto-converted to CREATE;
- competitor page type copied mechanically;
- full target architecture leaked into MK03;
- vague “consider SEO page” notes without evidence meaning.

## Non-repeat controls
`GAP != CREATE`; every structural note names its confidence/boundary and next required validation.

## Claim boundary
These are opportunity interpretations, not final architecture or ready implementation tasks.

## Unknown behavior
If evidence does not distinguish content expansion vs separate landing page, emit `NO STRUCTURAL RECOMMENDATION YET` or a candidate requiring architecture validation.

## PASS gate
Every opportunity is evidence-linked; automatic page creation = 0; neighbouring-product leakage = 0.

## Client-facing meaning
“For confirmed gaps we show what kind of opportunity they may create and where a separate architecture decision is still needed.”
