# MK03 — SERP COVERAGE MODE DECISION

Date: 2026-09-11
Status: **PHASE 3 METHOD DECISION / FROZEN FOR V1 REHEARSAL**

## Sold result

Real Yandex organic competitors -> evidence-bearing competitor pages -> competitor-derived demand candidates -> confirmed competitor/missed-demand gaps.

## Decision

```text
SERP_COVERAGE_MODE = SELECTIVE_DECISION_SERP
```

## Why this mode fits

Portfolio research explicitly identifies competitor/niche diagnostic research as a strong SELECTIVE case.

MK03 needs ordinary Yandex Search for two different bounded purposes:

1. discover real organic competitors from representative in-scope query families;
2. confirm material exact query→competitor visibility and page-type/intent facts before making those exact claims.

MK03 does not sell full rank tracking, SERP-based clustering for every accepted phrase, or full reverse-domain competitor keyword enumeration. Therefore fresh SERP for every raw/Wordstat phrase would add cost and data volume without being necessary to prove the sold result.

## Search input set

### Discovery set
Representative sanitized client-demand query families chosen to cover materially different in-scope search jobs/directions, not merely the highest-frequency N queries.

### Confirmation set
Material new candidate queries/families where fresh Search can change:

- competitor visibility claim;
- intent/page-type interpretation;
- gap acceptance versus HOLD/REJECT;
- material boundary/conflict.

## Exclusions

Do not fresh-search by default:

- raw Wordstat occurrences;
- duplicates;
- clear off-scope rows;
- every competitor heading/seed;
- every already-covered phrase;
- reserve rows whose Search result cannot change a product decision.

## Reuse rule

Reuse preserved Search evidence only when query, region, evidence purpose and freshness remain sufficient for the current decision. Historical presence is not current visibility.

## Fresh Search triggers

Acquire/reacquire Search when:

- competitor discovery requires current regional SERP evidence;
- an exact query→competitor claim will be shown to the client without sufficient current evidence;
- current intent/page type is material to a gap decision and unresolved;
- preserved evidence is stale or mismatched to region/query/purpose;
- an additional probe can materially resolve a HOLD/conflict.

## What counts as Search-covered

Only the exact tested query and recorded current observation are Search-covered.

```text
EXACT TESTED QUERY != FAMILY-WIDE CONFIRMATION
OBSERVED DOMAIN/URL != FULL COMPETITOR VISIBILITY HISTORY
```

## Unprobed / failed behavior

Unprobed rows must not be described as Search-confirmed.

Provider failure or insufficient evidence -> preserve `HOLD_EVIDENCE / SEARCH_REQUIRED / UNKNOWN` for the affected claim. Do not infer current ranking from competitor page text.

## Provider / cost route

Base route: current Yandex Search access available to the project/product execution. Search burden is measured during Phase 5 for economics. Cost cannot weaken the evidence required for a claim; instead reduce unsupported claim scope or preserve HOLD.

## Claim boundary

```text
SELECTIVE SEARCH != SELECTIVE SEMANTIC ACCOUNTING
```

All governed competitor-derived candidates must still be normalized, sanitized, reconciled and routed. Selective refers only to direct current SERP acquisition.

## Rehearsal test

Phase 5 must prove that:

- representative discovery families recover real relevant Yandex organic competitors;
- exact visibility claims have direct current Search evidence;
- unprobed candidates are not mislabeled Search-confirmed;
- expanding Search beyond the manifest occurs only for a named unresolved decision;
- final gap decisions remain reconstructable from competitor page + Wordstat + Search evidence as applicable.

## Sources

- `../../../KWORK_SERP_COVERAGE_MODE_RESEARCH_2026-09-10.md`
- `../MINI_KWORK_SERP_MODE_PRODUCTIZATION_GATE_2026-09-10.md`
- `../../STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md`
- `../../STEP_05A_VOLUME_SANITATION_ADDENDUM_2026-09-10.md`
