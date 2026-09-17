# KW-002 — STEP 06 SEARCH COMPETITOR / SERP ANALYSIS

Status: **ACTIVE METHOD AUTHORITY**  
Version date: 2026-09-17

## 1. Purpose

Step06 identifies which domains and concrete pages actually occupy a bounded current Yandex organic-result set for representative demand probes.

```text
BUSINESS RIVAL != SEARCH COMPETITOR
PRELIMINARY FAMILY != FINAL INTENT
REPRESENTATIVE QUERY != FINAL KEYWORD
DOMAIN OVERLAP != FINAL SERP CLUSTER
STEP06 != FINAL QUERY->PAGE OWNERSHIP
```

A marketplace, encyclopedia, publisher, directory, specialist seller or other surface can be a Search competitor without being a direct business rival.

## 2. External method basis

Yandex-specific authority:

- Yandex Webmaster, “Подбор поисковых запросов и анализ рынка”: https://yandex.ru/support/webmaster/ru/service/queries-selection

Cross-industry SERP-analysis / clustering references (method support, not Yandex ranking authority):

- Ahrefs, Search Intent / 3Cs: https://ahrefs.com/blog/search-intent/
- Ahrefs, SERPs / Top-10 intent review: https://ahrefs.com/blog/serps/
- Ahrefs, SEO Competitor Analysis: https://ahrefs.com/blog/seo-competitor-analysis/
- SE Ranking, keyword clustering help: https://help.seranking.com/hc/ru/articles/16332627413148-%D0%9A%D0%B0%D0%BA-%D0%BA%D0%BB%D0%B0%D1%81%D1%82%D0%B5%D1%80%D0%B8%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D1%8C-%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81%D1%8B

Method consequences:

- Yandex itself exposes popular sites/pages, defines clustering by semantic/intent proximity, describes competitiveness in the context of Top-10, and makes region/device selectable.
- Dominant result type/format is useful intent evidence.
- SERP-based clustering should compare identical ranking URLs in Top-10; domain overlap alone is insufficient.

## 3. Mandatory execution sequence

### Phase A — representative-query authority

Freeze a bounded representative set with stable query IDs, exact texts, upstream lineage and stated discovery purpose.

### Phase B — bounded SERP acquisition

Acquire the authorized depth while preserving raw/normalized evidence and provenance. Before every async action reconcile the latest durable state.

Terminal guard:

```text
all_successful=true + unresolved=0 + final_export_received=true
=> no submit / no collect / no blind retry / no duplicate final export
```

### Phase C — acquisition QA

Prove expected queries, counts, ranks, URLs, parse/normalization state, exact export identity and required readback. Acquisition QA does not complete Step06.

### Phase D — full row semantic classification

Preserve source fields and append, at minimum:

```text
rank_bucket
target_relevance
page_type
content_format
market_surface
entity_collision
classification_basis
classification_confidence
```

Allowed uncertainty stays explicit.

The `page_type` taxonomy is extensible. If a recurring surface type is not represented by the frozen schema, either add a stable type (e.g. `AUDIO`) or explicitly document that it is collapsed to `OTHER`.

### Phase E — Top-10 analytical profile

```text
TOP3 = strength amplifier
TOP10 = primary analytical layer
11-20 = secondary discovery/evidence layer
```

For each query record relevance composition, page-type composition, target purity, dominant type, accepted intent, confidence and evidence basis.

Preserve preliminary source class separately from accepted Top-10 intent.

### Phase F — collision / uncertainty control

Preserve collision rows. Separate collision-heavy visibility from target-usable interpretation. Do not make the market look cleaner by deleting evidence.

### Phase G — domain recurrence

Domain recurrence is competitor-discovery evidence only.

Every recurrence field must declare its filtering granularity:

```text
query-level subset metric != row-level target-filtered metric
```

Do not use ambiguous unqualified `clean_*` names.

Accepted-intent denominators must be recomputed after final Top-10 classification; stale preliminary denominators are prohibited unless explicitly marked as preliminary provenance.

### Phase H — pairwise SERP similarity

For a bounded representative set, calculate every unique query pair where practical. For each pair keep:

```text
exact_url_overlap_top10
domain_overlap_top10
url_union_top10
domain_union_top10
url_jaccard_top10
domain_jaccard_top10
shared_urls_top10
shared_domains_top10
```

For 22 queries: `22*21/2 = 231` pairs.

Exact URL overlap is the stronger SERP-clustering signal. Domain overlap remains a separate competitor-breadth signal. Do not invent a universal threshold that auto-creates a page inside Step06.

### Phase I — competitor registry

Build a **curated material registry** from the complete recurrence universe and qualitative result-role evidence. The registry is not necessarily the exhaustive domain list.

Every registry must state:

- inclusion basis;
- all-query / Top-3 / Top-10 breadth;
- accepted-intent denominators;
- collision-heavy / uncertain exposure;
- whether metrics are query-level or row-level;
- role classification without business-quality ranking.

### Phase J — region/device/snapshot and source limitations

Record:

```text
REGION_SCOPE
DEVICE_SCOPE
SERP_FEATURE_COVERAGE
SNAPSHOT_SCOPE
```

For the current KW-002 evidence:

```text
REGION_SCOPE = RUSSIA / provider region 225
DEVICE_SCOPE = NOT_CAPTURED_BY_CURRENT_SOURCE
SERP_FEATURE_COVERAGE = NOT_CAPTURED_BY_CURRENT_SOURCE
SNAPSHOT_SCOPE = BOUNDED_SINGLE_ACQUISITION
```

One live snapshot is evidence of observed composition, not permanent Yandex behavior.

### Phase K — content angle boundary

Content type and format are Step06 intent evidence. Full content-angle/content-brief analysis is deferred to the later content/page-specification step unless the roadmap explicitly expands Step06.

Do not claim a full content-strategy audit merely because titles/snippets were reviewed.

## 4. PASS gates

```text
REPRESENTATIVE_QUERY_SET_FROZEN = true
LATEST_STATE_GUARD = PASS
PROVIDER_ACQUISITION_ACCOUNTING = PASS
FINAL_EXPORT_RECEIVED = true
DURABLE_EVIDENCE_READBACK = PASS where required
FULL_ROW_CLASSIFICATION = PASS
EXPLICIT_UNCERTAINTY_PRESERVED = true
TOP10_QUERY_PROFILE = COMPLETE
COLLISION_CONTROL = PASS
DOMAIN_RECURRENCE = COMPLETE
RECURRENCE_GRANULARITY_EXPLICIT = true
ACCEPTED_DENOMINATORS_CURRENT = true
PAIRWISE_SERP_SIMILARITY = COMPLETE
SEARCH_COMPETITOR_REGISTRY = HARDENED
REGION_DEVICE_SCOPE = DISCLOSED
SERP_SOURCE_LIMITATIONS = DISCLOSED
SNAPSHOT_LIMITATION = DISCLOSED
PAGE_TYPE_TAXONOMY_LIMITATION = DISCLOSED where applicable
FINAL_PAGE_DECISIONS = NONE
STEP07_STARTED = false
KNOWN_FAILURE_REGRESSION_MATRIX = PASS
OPEN_CRITICAL_DEFECTS = 0
```

For current KW-002:

```text
CLASSIFIED_ROWS = 440
QUERY_PROFILES = 22
PAIRWISE_QUERY_COMPARISONS = 231
DOMAIN_RECURRENCE_UNIVERSE = 165
CURATED_COMPETITOR_REGISTRY = 32
```

## 5. Prohibited shortcuts

Do not:

- equate full acquisition with full analysis;
- overweight ranks 11-20 as first-page strength;
- infer final clusters from domain overlap;
- hide collision evidence;
- freeze preliminary class as truth;
- use stale denominators after reclassification;
- call query-level exclusion a row-level target filter;
- infer uncaptured SERP features;
- claim device coverage that was not captured;
- treat one snapshot as permanent behavior;
- force recurring uncategorized page types into a misleading homogeneous `OTHER` narrative;
- convert pairwise similarity into final page ownership inside Step06;
- start Step07 before Step06 durable acceptance.
