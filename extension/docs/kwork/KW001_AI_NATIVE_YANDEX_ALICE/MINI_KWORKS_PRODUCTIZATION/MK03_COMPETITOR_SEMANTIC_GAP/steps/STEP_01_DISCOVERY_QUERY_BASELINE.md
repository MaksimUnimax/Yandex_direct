# MK03 STEP 01 — REPRESENTATIVE YANDEX DISCOVERY BASELINE

## Purpose
Create a bounded set of representative in-scope query families sufficient to discover real organic competitors.

## Why this step exists
Competitors must be discovered from actual search jobs, but MK03 must not silently perform a complete MK01 semantic-core rebuild.

## Inputs
Step00 scope/current coverage; preserved relevant semantic/query evidence when available.

## Required evidence
Representative client search directions tied to real business offers/use cases and target region.

## Method
1. Reuse current preserved query families where valid.
2. Cover material business/search directions rather than every lexical variant.
3. Prefer category/service/use-case/attribute families with discovery value.
4. Expand only when a named business direction is not represented sufficiently to discover competitors.
5. Record why each family is present and the stop rationale.

## Outputs
`DISCOVERY_QUERY_FAMILY_MANIFEST` with family, representative query/queries, business direction, evidence source and purpose.

## Source authority
Parent Step5A competitor discovery method; information-gain and scale controls; local PRODUCT_SCOPE.

## Known failures / root causes
- fixed top-frequency N treated as representative;
- exhaustive semantic rebuild;
- unsupported/off-scope family included because query volume is high.

## Non-repeat controls
`REPRESENTATIVE DISCOVERY SET != COMPLETE CORE`; every family needs explicit discovery purpose.

## Claim boundary
This manifest is sufficient for competitor discovery under the frozen scope; it is not sold as the client's complete semantic core.

## Unknown behavior
If a material business direction cannot be represented from preserved/current evidence, mark the named gap and use only an authorized bounded acquisition route.

## PASS gate
All material business directions needed for competitor discovery are represented; no completeness overclaim; explicit stop rationale exists.

## Client-facing meaning
“We used representative searches for the main directions of your business so the competitor set comes from Yandex, not from guesses.”
