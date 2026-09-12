# KW-002 Blood & Sand — Step06 preparation-rule violation and correction

Date: 2026-09-12
Status: **JOB-SPECIFIC PRE-STEP DEFECT RECORDED / V1 PREPARATION SUPERSEDED FOR EXECUTION / NO SEARCH CALLS**

## Incident

The first Step06 preparation package was materialized and described as `PREPARATION PASS` before the mandatory owner-facing pre-step report had been shown in chat in the order required by `LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md` and `LEVEL1/COMMON_RULES.md`.

No ordinary Yandex Search, GenSearch, AI-search or Wordstat provider call was executed under that invalid preparation state.

## Existing universal rule already covered this

This incident does **not** create a new Level1/Level2 rule. The existing mandatory order is:

```text
WHOLE KWORK GOAL
→ FULL ROADMAP
→ COMPLETED
→ REMAINING
→ CURRENT STEP GOAL / PROBLEM / REQUIRED OUTPUT
→ RELEVANT PRIOR ERRORS
→ NON-REPEAT CONTROLS
→ FRESH INTERNET RESEARCH
→ CLICKABLE OWNER-FACING SOURCE DISCLOSURE
→ SOURCE→METHOD TRACE
→ METHOD / EXECUTION PLAN
→ BRIDGE / WORK GATE
→ PASS CONDITIONS
→ PLAIN-RUSSIAN WHY / WHAT / RESULT / BLOCKER / NEXT ACTION
→ ONLY THEN MATERIAL STEP EXECUTION
```

## V1 preparation defects found during correction

### Defect A — owner-facing disclosure gate was prematurely marked PASS

`STEP_06_PREPARATION_GATE_2026-09-12.md` claimed owner-facing disclosure/pass state before the mandatory full chat report actually existed.

Correction: V2 does not treat repository publication as a substitute for owner-facing disclosure.

### Defect B — coverage-direction accounting was wrong

The V1 TSV contains 11 distinct `coverage_direction` values, while the V1 gate/cursor stated `COVERAGE_DIRECTIONS = 10`.

Correction: V2 performs explicit manifest accounting and adds the previously omitted observed Step04 access/acquisition task family, producing 12 distinct coverage directions.

### Defect C — unsupported description of top-20 depth

The V1 gate described `groupsOnPage=20` as roughly “two ordinary result pages”. That is not part of the Yandex Search API contract and is removed.

Correction: V2 states only what current official docs support: XML `groupsOnPage` allows 1..100 and currently defaults to 20; project use of top-20 for Step06 is a bounded job heuristic for competitor discovery, not proof of complete SERP coverage.

### Defect D — original Base64/XML was incorrectly made mandatory

V1 treated loss of original `rawData` as an automatic F03 failure.

Existing Level1 evidence rules explicitly allow:

```text
raw OR durable normalized result reference
```

Correction: Step06 requires complete preservation of every returned result row and the fields/provenance required by Step06. Current repository Search normalization preserves all XML `<doc>` rows into a full result array with rank/url/domain/title/snippet/modtime and serializes the complete normalized envelope. Original Base64/XML is useful but is not independently required by the current universal rule for this Step06 purpose.

This does not waive completeness: row loss, field loss that prevents Step06 decisions, truncation of the result list, or chat-only evidence still fails F03.

### Defect E — runtime/source authority remains unresolved

The immediately preceding owner-supplied Bridge provider result reported installed runtime version `0.1.4`, while current branch `extension/src/shared/product.js` reports `0.1.2`.

The repository contains no `0.1.4` source string/commit found during the current preparation recheck.

Correction: a non-provider runtime/schema handshake or authoritative runtime-source reconciliation is required before any Step06 Search provider release.

## V1 disposition

Historical files remain for provenance but are superseded for execution decisions:

- `STEP_06_PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_TRACE_2026-09-12.md`
- `STEP_06_REPRESENTATIVE_QUERY_MANIFEST_V1_2026-09-12.tsv`
- `STEP_06_PREPARATION_GATE_2026-09-12.md`

Current corrected package uses V2 artifacts.

## Hard boundary

```text
STEP06_ACTUAL_EXECUTION = NOT_STARTED
V1_PREPARATION_EXECUTION_AUTHORITY = false
ORDINARY_SEARCH_CALLS_DURING_CORRECTION = 0
GENSEARCH_CALLS_DURING_CORRECTION = 0
WORDSTAT_CALLS_DURING_CORRECTION = 0
AI_SEARCH_CALLS_DURING_CORRECTION = 0
STEP07_STARTED = false
STEP08_STARTED = false
```
