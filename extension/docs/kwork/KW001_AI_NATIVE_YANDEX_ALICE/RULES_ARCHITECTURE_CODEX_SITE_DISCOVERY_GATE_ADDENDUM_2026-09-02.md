# KW-001 — mandatory Codex current-site discovery and topology gate addendum

Date: 2026-09-02
Status: **ACTIVE / UNIVERSAL PROCESS ADDENDUM / OWNER-APPROVED / OWNER-LOCKED**
Authority: latest explicit owner instruction; supplements `RULES_ARCHITECTURE.md`, `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`, and step-specific methods.

## Purpose

This addendum prevents a known-page recheck from being mistaken for complete current-site discovery and prevents live endpoint checks from being mistaken for proof that an internal link actually exists in HTML.

Canonical non-equivalences:

```text
KNOWN_URL_RECHECK != CURRENT_SITE_DISCOVERY
UPSTREAM_INPUT_UNIVERSE != CURRENT_SITE_UNIVERSE
SOURCE_LIVE + TARGET_LIVE != EDGE_IMPLEMENTED
SEMANTIC_LINK_RECOMMENDATION != CURRENT_AS_IS_LINK
```

## Mandatory gate

For every major step whose acceptance depends materially on any of the following:

```text
complete or near-complete public page discovery;
current public-site architecture;
current internal-link topology;
current crawl reachability;
orphan or sitemap-only detection;
exact current source->target link existence;
reconciliation of planned architecture against the actual site;
```

ChatGPT MUST require a deterministic Codex/code run before the step may close as complete.

Canonical rule:

```text
SITE_COMPLETENESS_OR_TOPOLOGY_MATERIAL = true
-> CODEX_DETERMINISTIC_DISCOVERY_RUN_REQUIRED = true
-> CODEX_OUTPUT_PERSISTED_IN_GITHUB = true
-> GITHUB_READBACK_REQUIRED = true
-> ANALYTICAL_RECONCILIATION_REQUIRED = true
-> ONLY THEN STEP_PASS_MAY_BE_CONSIDERED
```

ChatGPT's own web reads are an independent semantic/current-content validation layer. They are NOT sufficient evidence of full URL-universe completeness when a deterministic crawl can test that claim.

## Required Codex responsibilities

The Codex/code layer must, as applicable to the site and step:

1. discover public URLs from the homepage crawl and normal HTML links;
2. use public sitemap(s) as an additional discovery source, not as the sole source;
3. normalize and deduplicate URLs while preserving evidence of discovery origin;
4. fetch/recheck discovered public HTML pages with bounded retries and explicit failure states;
5. extract literal internal `<a href>` edges from fetched HTML;
6. persist source URL, target URL, anchor text when available, link evidence/provenance, and fetch state;
7. calculate or persist crawl depth/reachability sufficient for the current analytical goal;
8. identify sitemap-only, crawl-only, orphan-candidate, redirect, failed and broken-internal-edge cases when observable;
9. reconcile newly discovered URLs against the upstream architecture/input universe;
10. verify every step-required planned internal edge against literal current HTML and classify it separately from the recommendation;
11. write machine-readable outputs and a human-readable report into the current job workspace;
12. run deterministic QA and leave the job fail-closed on material coverage gaps.

## Separation of responsibilities

```text
CODEX / DETERMINISTIC CODE
= discovery completeness, HTML extraction, link graph, mechanical reconciliation, repeatable QA

CHATGPT ANALYTICAL LAYER
= semantic relevance, user intent, page responsibility, architecture materiality, affected-unit reopen decisions, claim boundaries

OWNER
= authorization and any scope/cost/site-mutation decision
```

Codex output must not silently make semantic ownership decisions or authorize new pages, redirects, canonicals, merges, deletion, provider spending, or site mutation.

## Required current-vs-target states

Current topology and recommended architecture must be stored separately.

For planned internal-link actions, at minimum distinguish:

```text
AS_IS_PRESENT
AS_IS_ABSENT_PLANNED
BLOCKED_OR_UNVERIFIED
NOT_APPLICABLE
```

A recommendation may remain valid when `AS_IS_ABSENT_PLANNED`; it must not be reported as a currently implemented edge.

## Reopen policy

A newly discovered URL does not automatically invalidate the entire upstream architecture.

```text
NEWLY_DISCOVERED_URL
-> semantic relevance review
-> if architecture-material: reopen only affected unit(s)/case(s)
-> if non-material: persist with reason and keep freeze unchanged
```

No relevant discovered URL may be silently ignored.

## Fail-closed acceptance

A step depending on site completeness/topology MUST NOT close as PASS when any of these is true:

```text
required Codex run not executed;
Codex outputs not persisted/read back;
material crawl/discovery coverage gap unexplained;
new relevant discovered URL not reconciled;
required planned internal edge not classified from literal HTML evidence;
current topology and target recommendation conflated;
mechanical QA has unresolved blockers.
```

## Non-repeat lesson

The error that triggered this rule was caused by treating a recheck of known upstream URLs as proof of the full current-site universe, and by treating live source/target endpoints plus semantic fit as proof of literal link implementation. The control is therefore not "check more pages manually"; the control is **mandatory deterministic discovery/topology evidence before a completeness-dependent PASS**.
