# MINI-KWORK SERIES — SERP MODE PRODUCTIZATION GATE

Date: 2026-09-10
Status: **OWNER-APPROVED / SERIES-LEVEL / MANDATORY / PRODUCTIZATION-ONLY**
Applies to: MK01–MK07 and future versioned mini-kworks.

This is a mandatory addendum to `MINI_KWORK_DEVELOPMENT_PROTOCOL.md`.

## Research authority

Before freezing the roadmap of each mini-kwork/version, read the portfolio research:

`../../../KWORK_SERP_COVERAGE_MODE_RESEARCH_2026-09-10.md`

Also obey:

`../../../KWORK_SERP_MODE_PRODUCTIZATION_GATE_2026-09-10.md`

## One-time productization decision

During Phase 3–4 method extraction/roadmap design, every mini-kwork that could use ordinary Search must explicitly compare and freeze one of:

```text
FULL_SERP_COVERAGE
SELECTIVE_DECISION_SERP
HYBRID_SCOPED_FULL
NO_ORGANIC_SERP_BASE
```

This proof happens while the product is being designed, not on every future client order.

```text
MINI-KWORK PRODUCTIZATION
-> research exact sold result
-> prove appropriate SERP mode
-> materialize local Level-1 decision
-> update product scope/general rules/step rules/roadmap/QA/economics
-> rehearse
-> freeze

NORMAL CLIENT ORDER
-> execute frozen mini-kwork mode
-> no full-vs-selective redesign
```

## Mandatory local materialization

Before Phase 5 large-data rehearsal (or before final product freeze when this gate is introduced retroactively), the mini-kwork must contain an equivalent local `SERP_COVERAGE_MODE_DECISION*.md` with:

```text
SOLD RESULT
SERP MODE
WHY THIS MODE IS SUFFICIENT/NECESSARY
SEARCH INPUT SET
SEARCH EXCLUSIONS
REUSE RULE
FRESH SEARCH TRIGGERS
UNPROBED/FAILED BEHAVIOR
PROVIDER/COST ROUTE
CLAIM BOUNDARY
REHEARSAL TEST
```

## Consistency audit addition

The Phase-4 method consistency audit must additionally verify:

```text
SERP_MODE_DECISION_PRESENT = true
RESEARCH_AUTHORITY_REFERENCED = true
PRODUCT_SCOPE_MATCHES_SERP_MODE = true
GENERAL_RULES_MATCH_SERP_MODE = true
SEARCH STEP MATCHES_SERP_MODE = true
DELIVERABLE CLAIMS MATCH SERP_MODE = true
QA MATCHES SERP_MODE = true
ECONOMICS COUNTS CORRECT SEARCH BURDEN = true
PER_CLIENT_REPROOF_REQUIRED = false
```

## Existing products / future products

Current decision registry:

`SERP_MODE_DECISION_REGISTRY_2026-09-10.md`

Do not infer the mode for an undeveloped future mini-kwork solely from its name or from another product.

## Re-open rule

A frozen mini-kwork reopens SERP mode only after a material version change, changed promise/operating mode/provider route, a demonstrated method defect, or explicit owner version reopen.

## Marker

```text
MINI_KWORK_SERP_MODE_MUST_BE_PROVED_DURING_PRODUCTIZATION = true
MINI_KWORK_SERP_MODE_PER_CLIENT_REPROOF = false
MINI_KWORK_SERP_RESEARCH_AUTHORITY = KWORK_SERP_COVERAGE_MODE_RESEARCH_2026-09-10.md
```