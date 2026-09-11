# MK03 STEP 06 — MATERIAL CURRENT YANDEX SEARCH CONFIRMATION

## Purpose
Use current ordinary Yandex Search only where it can materially change acceptance, exact competitor visibility, intent or page-type interpretation.

## Why this step exists
Page text and Wordstat demand do not prove exact current Search visibility or SERP intent.

## Inputs
New sanitized candidates/HOLD rows; competitor discovery evidence; named unresolved decisions.

## Required evidence
Current regional Search response or still-valid preserved exact observation for each tested query.

## Method
1. Build a bounded Search manifest from material new candidates, ambiguous modifiers, acceptance boundaries and controls.
2. Reuse current exact observations where valid.
3. For each tested query record query, region, competitor domains/URLs/result type/order as available and observation date.
4. Mark tested and untested rows distinctly.
5. Expand the tranche only when another Search can materially change a decision.

## Outputs
`COMPETITOR_QUERY_VISIBILITY_MATRIX` plus tested/unprobed state.

## Source authority
`SERP_COVERAGE_MODE_DECISION_2026-09-11.md`; parent Step5A 5A.6; exact-query generalization controls.

## Known failures / root causes
- bulk Search for every raw row;
- highest-frequency N used as universal sample;
- anchor result generalized to all family members;
- Search absence interpreted as site absence.

## Non-repeat controls
`EXACT OBSERVATION != FAMILY PROOF`; `SELECTIVE != SILENT GENERALIZATION`.

## Claim boundary
Only tested exact queries are Search-confirmed. Untested rows may be analytically classified but cannot inherit exact visibility claims.

## Unknown behavior
Provider failure/inconclusive SERP keeps SEARCH_REQUIRED/HOLD state for decisions that genuinely require Search evidence.

## PASS gate
Every exact competitor visibility claim has a direct locator; tested vs untested is explicit; no unnecessary raw-row bulk Search.

## Client-facing meaning
“We separately mark which competitor/query relationships were actually checked in current Yandex results.”
