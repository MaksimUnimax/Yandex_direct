# MK03 STEP 00 — SCOPE AND CURRENT-SITE BASELINE

## Purpose
Freeze the exact client site, region, business boundary and current public coverage needed for competitor-gap comparison.

## Why this step exists
A competitor gap is meaningless without knowing what business/search directions belong to the client and what the current site already covers.

## Inputs
- public site URL;
- target region;
- optional client exclusions/priority directions;
- optional competitor hints;
- preserved current site evidence if still valid.

## Required evidence
Current public site evidence sufficient to identify material offer/direction coverage. Old inventories may assist but cannot prove current absence.

## Method
1. Confirm public site and target region.
2. Inspect current public offer/directions without requiring the client to restate obvious site content.
3. Record material ambiguities as explicit questions/HOLD.
4. Build a current coverage baseline by direction/topic/page type sufficient for later gap comparison.
5. Do not create a full MK01 semantic core here.

## Outputs
- `SCOPE_BASELINE`;
- `CLIENT_CURRENT_COVERAGE_BASELINE`;
- `BUSINESS_AMBIGUITY_REGISTER` when needed.

## Source authority
`PRODUCT_SCOPE.md`; `CLIENT_INPUT_CONTRACT.md`; parent current-site freshness/business-boundary authorities.

## Known failures / root causes
- stale inventory creates false gap;
- client description replaces current site evidence;
- full semantic-core rebuild is performed before competitor analysis.

## Non-repeat controls
`OLD ABSENCE != CURRENT ABSENCE`; `MK03 BASELINE != MK01`.

## Claim boundary
Current public inspection supports current observed coverage only; it does not prove historical coverage or business priorities not stated/evidenced.

## Unknown behavior
Material unresolved business ambiguity remains HOLD and must not be converted into accepted/rejected gap by guess.

## PASS gate
Site/region frozen; material current coverage baseline exists; unresolved business ambiguity is explicit; no silent MK01 expansion.

## Client-facing meaning
“We first fixed what your site actually offers now and the region in which competitors must be compared.”
