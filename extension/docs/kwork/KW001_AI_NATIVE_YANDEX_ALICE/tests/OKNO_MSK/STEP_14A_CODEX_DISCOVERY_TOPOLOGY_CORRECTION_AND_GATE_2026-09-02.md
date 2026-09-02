# OKNO_MSK — Step 14A Codex discovery/topology correction and gate

Date: 2026-09-02
Status: **REOPENED / MANDATORY CORRECTION / CODEX RUN REQUIRED BEFORE STEP 14 FINAL PASS**
Parent step: 14 — Search-only architecture freeze

## Owner instruction

The owner explicitly required Codex execution to become a mandatory condition where current-site page completeness/topology matters. ChatGPT must provide the exact Codex prompt; the owner passes it to Codex; the resulting repository artifacts are returned to ChatGPT for readback, reconciliation and final Step 14 closure.

## What was wrong in the first Step 14 closure

The first Step 14 execution correctly rechecked 59 known implementation-critical URLs and preserved semantic/accounting gates, but it treated that known-URL universe as sufficient evidence for current-site completeness.

It also froze 15 recommended internal-link actions after verifying source/target/current semantic compatibility, but that is not equivalent to literal current HTML `<a href>` evidence.

Canonical defect:

```text
KNOWN_URL_RECHECK was elevated to CURRENT_SITE_DISCOVERY.
SOURCE_LIVE + TARGET_LIVE + SEMANTIC_FIT was elevated to EDGE_IMPLEMENTED.
```

## Why this happened

The method correctly tried to avoid uncontrolled scope expansion and unsupported new-page/destructive actions. However, that control was applied too broadly: the upstream Step 12/13 URL universe was implicitly treated as the complete current public-site universe.

The reasoning/process chain that caused the defect was:

```text
upstream architecture is accepted
-> avoid speculative expansion
-> recheck all known implementation-critical URLs
-> all known URLs are live
-> mistakenly infer current architecture coverage is sufficient
```

A second similar chain affected internal links:

```text
Step 12 recommended edge survives semantic/current endpoint checks
-> source live
-> target live
-> role/relevance compatible
-> mistakenly infer current implementation is verified
```

The missing control was an independent deterministic discovery/topology layer.

## Repository evidence that made this omission avoidable

Step 11 already contains Codex discovery/profile artifacts including:

```text
STEP_11_CODEX_DISCOVERED_URLS.tsv
STEP_11_CODEX_PAGE_PROFILE_LEDGER.tsv
STEP_11_CODEX_CURRENT_PAGE_REFRESH_REPORT_2026-08-30.md
```

Therefore the omission in Step 14 is recorded as a process regression: an available and already-used deterministic discovery pattern was not promoted into the Step 14 acceptance gate.

## Mandatory correction

Step 14 semantic results are not discarded. The following remain provisional-preserved unless Codex evidence contradicts an affected unit:

```text
ACTIVE_PHRASES = 2332
ASSIGNED = 2313
UNRESOLVED = 19
STRUCTURAL_UNITS = 168
STEP13_EFFECTIVE_PAIRS = 199
STEP13_QUERY_FAMILY_CASES = 21
SUPPORTED_NEW_PAGE_ACTIONS = 0
SUPPORTED_DESTRUCTIVE_ACTIONS = 0
```

Step 14 overall closure is reopened until Step 14A completes.

Required Step 14A outputs:

```text
STEP_14A_CODEX_SITE_DISCOVERY_URLS.tsv
STEP_14A_CODEX_INTERNAL_LINK_GRAPH.tsv
STEP_14A_CODEX_PAGE_PROFILE_LEDGER.tsv
STEP_14A_CODEX_UPSTREAM_RECONCILIATION.tsv
STEP_14A_CODEX_REQUIRED_EDGE_VERIFICATION.tsv
STEP_14A_CODEX_QA.json
STEP_14A_CODEX_REPORT.md
```

A deterministic runner/script used to generate them must also be committed when practical.

## Minimum Step 14A coverage

1. Homepage/BFS-style crawl of same-site public HTML links.
2. Public sitemap discovery as an additional source.
3. URL normalization and deduplication.
4. Fetch state/status/final URL/redirect evidence.
5. Literal internal `<a href>` extraction.
6. Source->target internal graph with anchor text when available.
7. Crawl depth/reachability sufficient to identify coverage gaps.
8. Sitemap-only/crawl-only/orphan-candidate/broken internal cases when observable.
9. Reconciliation of discovered URLs against Step 12/13/14 known URL universe.
10. Exact current-HTML verification of all 15 Step 14 planned IMPLEMENT edges.
11. Separate current as-is topology from target recommendation.
12. Machine QA with fail-closed blockers.

## Analytical reconciliation after Codex

ChatGPT must review every newly discovered URL that is not already represented in the upstream architecture and classify:

```text
ARCHITECTURE_MATERIAL
NON_MATERIAL_WITH_REASON
OUT_OF_SCOPE_WITH_REASON
```

For `ARCHITECTURE_MATERIAL`, reopen only affected units/cases and rerun required local QA. Do not silently assign/drop phrases or globally rebuild unaffected units.

For each planned internal edge, preserve both dimensions:

```text
RECOMMENDATION_STATE
AS_IS_TOPOLOGY_STATE
```

with at least:

```text
AS_IS_PRESENT
AS_IS_ABSENT_PLANNED
BLOCKED_OR_UNVERIFIED
NOT_APPLICABLE
```

## Pass gate

Step 14 may return to final PASS only if:

```text
CODEX_RUN_EXECUTED = true
CODEX_OUTPUTS_PERSISTED = true
GITHUB_READBACK = PASS
DISCOVERED_URL_RECONCILIATION_COMPLETE = true
UNEXPLAINED_RELEVANT_DISCOVERED_URLS = 0
ALL_15_REQUIRED_EDGES_CLASSIFIED_FROM_LITERAL_HTML = true
CURRENT_TOPOLOGY_SEPARATE_FROM_TARGET_RECOMMENDATION = true
MATERIAL_AFFECTED_UNITS_REOPENED_AND_RECHECKED = true when applicable
SILENT_ASSIGNMENT = 0
SILENT_DROP = 0
UNSUPPORTED_NEW_PAGE = 0
UNSUPPORTED_DESTRUCTIVE_ACTION = 0
AI_GENSEARCH_USED = 0
STEP15_EXECUTED = false
QA_BLOCKERS = 0
```

## Current step status

```text
STEP_14_SEMANTIC_FREEZE = PROVISIONAL_PASS_PRESERVED
STEP_14_CURRENT_SITE_COMPLETENESS = REOPENED
STEP_14_AS_IS_TOPOLOGY = REOPENED
STEP_14_OVERALL = REOPENED_PENDING_MANDATORY_CODEX_RUN
STEP_15 = BLOCKED
```

Authority addendum:
`RULES_ARCHITECTURE_CODEX_SITE_DISCOVERY_GATE_ADDENDUM_2026-09-02.md`
