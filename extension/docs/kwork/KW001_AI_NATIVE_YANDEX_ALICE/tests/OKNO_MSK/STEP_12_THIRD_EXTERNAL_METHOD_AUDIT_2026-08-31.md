# Step 12 — third external method audit / source-to-method trace

Date: 2026-08-31
Status: **SOURCE TRACE FOR D12-21..D12-26 CORRECTION**

## Purpose

This audit exists because the second corrected Step-12 pass was technically clean but a new external-method review showed that several evidence concepts were still compressed. The goal is not to copy vendor terminology mechanically. The goal is to identify which external recommendations materially constrain the structural decision and convert those constraints into explicit Step-12 evidence fields and fail-closed checks.

## Source 1 — Yandex Webmaster: Site structure

https://yandex.ru/support/webmaster/ru/recommendations/site-structure

Current guidance: pages must belong to a clear section; ordinary HTML links should make documents reachable; navigation should help users find the needed documents; text links to other sections provide useful context to the crawler.

### Step-12 consequence

A relationship such as `ROUTE_TO_EXISTING_PAGE_AS_SUBTASK` is not fully implementation-ready merely because primary/supporting URLs are present. When a real page-to-page journey is evidenced, Step 12 should materialize the source/target link relationship and user purpose. If no distinct source page is evidenced, it must say so instead of inventing a link.

Supports: D12-26.

## Source 2 — Semrush: Content gap analysis, 2026-06-23

https://www.semrush.com/blog/content-gap-analysis/

Current guidance distinguishes different gap causes instead of treating every missing/weak answer as the same problem. It explicitly discusses absent topics, intent mismatch, quality gaps, and originality gaps, and says different gaps can require a new page, an update, clearer structure, or supporting detail. It also stresses audience-led evidence beyond keyword lists.

### Step-12 consequence

Step 12 must diagnose the problem before prescribing the structural action. Add `gap_type` and `gap_evidence`. `NO OWNER` is not enough to claim a topic gap. `CREATE` can survive only a verified topic gap after reuse/current-site/business/search gates.

Supports: D12-21 and partly D12-25.

## Source 3 — Semrush: Content audit, 2026-05-04

https://www.semrush.com/blog/content-audit/

Current guidance defines content audit as analysis of how existing content performs and supports business goals. It uses performance, conversions, rankings/visibility and other outcome data to decide whether content should be kept, updated, consolidated or removed.

### Step-12 consequence

Structural page ownership is not the same conclusion as page-performance sufficiency. In this base Kwork package there is no authorized Yandex Webmaster/Metrika account access, so `KEEP_EXISTING_STRUCTURE` can mean "keep this URL/role" but cannot honestly mean "no optimization/content improvement is needed". The evidence gap is recorded, not filled by inference.

Supports: D12-22.

## Source 4 — Topvisor: target URL vs relevant URL, updated 2026-02-10

https://topvisor.com/ru/support/rankings/target-url/

The reference distinguishes a target URL from the relevant URL actually selected in the search results. The relevant URL is derived from the search engine result, not manually chosen.

### Step-12 consequence

Persist `intended_target_url`, `current_yandex_relevant_url`, and `relevant_url_match_state`. Never convert intended ownership into a claim that Yandex is already choosing that URL.

Supports: D12-23.

## Source 5 — Rush Analytics: semantic core / relevant URL / existing-site structure

https://www.rush-analytics.ru/faq/kak-sostavit-semanticheskoe-yadro-sajta
https://www.rush-analytics.ru/faq/kak-sozdat-strukturu-sayta-na-osnove-semanticheskogo-yadra

The current guidance checks whether an existing site already has a relevant/ranking URL for a clustered query and, for an existing site, uses the suitable existing URL when appropriate; a new URL is considered when no suitable URL exists. It explicitly treats relevant URL evidence as part of the old-page-vs-new-page decision.

### Step-12 consequence

Current Search evidence and current site/page evidence must remain separate but comparable. Missing target-domain visibility is an observed state, not proof of no page; a suitable current page can still be the intended structural owner.

Supports: D12-23 and the existing freshness/reuse gate.

## Source 6 — Ahrefs: Keyword strategy, updated 2026-03-13

https://ahrefs.com/blog/keyword-strategy/

Current guidance says that traffic potential and business value are not enough unless the content also matches what searchers expect. It recommends reading current top results and analysing content type, format and angle.

### Step-12 consequence

For material page-boundary decisions, broad `INFORMATIONAL/COMMERCIAL` intent is insufficient. Persist the observed content type/format/angle when the acquired Search evidence actually contains it. If old evidence did not separately record a dimension, mark that limitation rather than hallucinating it.

Supports: D12-24 and D12-25.

## Source 7 — Ahrefs: Keyword intent, 2026-03-13

https://ahrefs.com/blog/keyword-intent/

Current guidance treats keyword intent as an earlier strategy filter: a keyword should fit something the site can realistically serve and convert; attractive volume alone is insufficient. Informational demand is worth targeting when it supports the broader strategy and can naturally connect to the product/business context.

### Step-12 consequence

Owner/business goal evidence must be source-labelled. Public-site inference is not equivalent to a client-stated policy. A policy-sensitive content action cannot silently treat inferred goals as explicit owner instructions.

Supports: D12-25.

## Source 8 — Ahrefs: Internal links for SEO, updated 2026-03-10

https://ahrefs.com/blog/internal-links-for-seo/

Current guidance describes internal links as navigation and search-engine context. It recommends links to important products/services/cornerstone content, contextually relevant links that genuinely help the reader, and adding internal links while updating older content.

### Step-12 consequence

Internal-link implementation is relevant to existing-page UPDATE/ROUTE relationships, not only newly created pages. Step 12 should materialize a link where a current source-to-target journey is evidenced, while avoiding artificial links merely to fill a QA table.

Supports: D12-26.

## Important source-boundary note

Ahrefs examples are Google-centric. They support general information-architecture/search-intent/internal-link reasoning, not a claim about a specific Yandex ranking algorithm. Yandex-specific structural claims use Yandex Webmaster and persisted Yandex Search evidence. Topvisor/Rush support workflow distinctions and tooling concepts, not authoritative Yandex algorithm rules.

## Resulting mandatory fields for Step 12

```text
gap_type
gap_evidence
performance_evidence_state
optimization_readiness
intended_target_url
current_yandex_relevant_url
relevant_url_match_state
direct_serp_queries
serp_observed_user_job
serp_expected_content_type
serp_expected_format
serp_expected_angle
serp_format_evidence_state
owner_goal_evidence_source
owner_policy_materiality
owner_goal_evidence_note
```

Separate implementation ledger for material existing-page relations:

```text
STEP_12_INTERNAL_LINK_ACTIONS.tsv
```

## Why these are not optional decoration

Each field closes a distinct false inference:

```text
ACTION != GAP DIAGNOSIS
STRUCTURAL OWNER != PERFORMANCE PASS
INTENDED TARGET != SEARCH-OBSERVED RELEVANT URL
BROAD INTENT != CONTENT TYPE / FORMAT / ANGLE
PUBLIC-SITE INFERENCE != CLIENT-STATED BUSINESS POLICY
PAGE RELATION != IMPLEMENTABLE INTERNAL LINK
```

If a source dimension is unavailable in the sold scope, the method records `NOT_AVAILABLE / NOT_DIRECTLY_CHECKED / UNKNOWN` and constrains the conclusion. It does not fabricate evidence or automatically purchase additional provider data.
