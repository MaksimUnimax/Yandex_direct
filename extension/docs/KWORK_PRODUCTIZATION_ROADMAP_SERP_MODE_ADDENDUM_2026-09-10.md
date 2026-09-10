# KWORK PRODUCTIZATION ROADMAP — SERP MODE ADDENDUM

Date: 2026-09-10
Status: **OWNER-APPROVED / MANDATORY PORTFOLIO ADDENDUM**
Applies with: `KWORK_PRODUCTIZATION_ROADMAP_2026-08-28.md`.

## Research authority

Every Kwork productization must read:

`KWORK_SERP_COVERAGE_MODE_RESEARCH_2026-09-10.md`

and obey:

`KWORK_SERP_MODE_PRODUCTIZATION_GATE_2026-09-10.md`.

## Productization insertion point

For each KW product/version, after commercial promise/scope is understood and before the execution roadmap is frozen:

```text
SOLD RESULT FREEZE
-> SERP MODE RESEARCH / PRODUCT-SPECIFIC PROOF
-> FREEZE LOCAL SERP MODE
-> BUILD/UPDATE STEP ROADMAP
-> REHEARSE CHOSEN MODE
-> MEASURE COST/WORKLOAD
-> RUNBOOK FREEZE
```

This proof is performed once for the product/version.

Normal future client orders do not repeat FULL-vs-SELECTIVE research; they follow the frozen product method.

## Required mode values

```text
FULL_SERP_COVERAGE
SELECTIVE_DECISION_SERP
HYBRID_SCOPED_FULL
NO_ORGANIC_SERP_BASE
```

## Current portfolio state

```text
KW-001 = SELECTIVE_DECISION_SERP
KW-002 = FULL_SERP_COVERAGE (owner-frozen 2026-09-10)
KW-003..KW-008 = PENDING_PRODUCTIZATION_DECISION
```

Future Kworks are deliberately not pre-decided here. Their exact sold result, evidence need, provider path, economics and rehearsal must be inspected at their productization turn.

## KW-002 special boundary

`FULL_SERP_COVERAGE` applies only to the final cleaned / delivery-selected Search-stage set.

It does not authorize:

```text
RAW Wordstat -> Search all
excluded/reserve -> Search by default
SERP overlap -> automatic page truth
Work/LLM -> manual parsing of every raw SERP body
```

## Economics dependency

SERP mode must be frozen before package economics are finally accepted because provider/processing burden differs materially between FULL and SELECTIVE modes.

If a cheaper provider transport such as Yandex deferred Search is considered, transport capability must be separately implemented/validated; a published provider feature is not automatically an accepted Bridge capability.

Deferred-Search research:

`YANDEX_SEARCH_ASYNC_DEFERRED_RESEARCH_2026-09-10.md`
