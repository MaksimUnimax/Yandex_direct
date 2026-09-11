# MK03 STEP 02 — REAL ORGANIC COMPETITOR DISCOVERY

## Purpose
Identify domains that actually recur in current regional Yandex organic results for in-scope query families.

## Why this step exists
Business rivals and organic search competitors are not the same set.

## Inputs
Discovery query-family manifest; target region; reusable current Search evidence where valid.

## Required evidence
Current regional ordinary Yandex Search observations for representative queries/families.

## Method
1. Acquire/reuse Search results for the discovery manifest under SELECTIVE_DECISION_SERP.
2. Record returned domains/URLs/result types and observed order/position when available.
3. Aggregate recurring domains across materially different relevant families.
4. Classify candidates for routing: direct business competitor, other organic model, aggregator/directory, marketplace, manufacturer/brand, informational publisher, other review.
5. Accept a domain as a search competitor only where current evidence supports material competition.
6. Continue discovery only while new domains add material information.

## Outputs
`COMPETITOR_DISCOVERY_REGISTER` and search evidence locators.

## Source authority
`STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md`; `SERP_COVERAGE_MODE_DECISION_2026-09-11.md`.

## Known failures / root causes
- client competitor list accepted as truth;
- one accidental appearance treated as material competitor without context;
- fixed competitor quota forces noise;
- business-model classification presented as Yandex taxonomy.

## Non-repeat controls
`BUSINESS RIVAL != SEARCH COMPETITOR`; classification is project routing only; no fixed domain count.

## Claim boundary
MK03 proves observed organic competition in tested regional query families, not market share, traffic, revenue or full ranking footprint.

## Unknown behavior
Ambiguous/weak candidate domains may remain review-only and must not be promoted to “main competitor” without sufficient evidence.

## PASS gate
Every accepted competitor has a current discovery locator; family coverage is material; stop rationale recorded.

## Client-facing meaning
“These are competitors that actually appeared in Yandex for searches relevant to your business.”
