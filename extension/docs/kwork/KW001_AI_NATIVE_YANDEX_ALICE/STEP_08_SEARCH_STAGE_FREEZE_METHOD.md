# KW-001 — STEP 08 SEARCH-STAGE SEMANTIC FREEZE METHOD

Date: 2026-08-29
Status: **APPROVED / ACTIVE AFTER CORRECTION / OWNER-LOCKED**

## Step purpose

Freeze a stable, auditable handoff from accepted row-level semantic cleanup into ordinary Search validation without silently dropping uncertainty or prematurely deciding clustering, page ownership or architecture.

Step 8 is a **project-specific workflow boundary**, not an official Yandex SEO stage.

## External method support

### Official Yandex — user need and site/query fit
https://yandex.ru/support/webmaster/ru/recommendations/targeting

Supports:
- Search exists to answer user needs expressed in queries;
- site content should match those needs/wording;
- suitable phrases should relate to the product/service the site can answer.

Does NOT support:
- a separate `business evidence route` taxonomy.

### Official Yandex — target query selection and potential
https://yandex.ru/support/webmaster/ru/service/queries-selection

Supports:
- selecting suitable target queries;
- analyzing query potential;
- studying pages/competition for those queries.

### Official Yandex — query/page Search evidence
https://www.yandex.ru/support/webmaster/ru/service/search-queries

Supports:
- observing which pages appear for which queries;
- keeping query/page evidence as a Search-layer concern.

### Ahrefs — Keyword Intent
https://ahrefs.com/blog/keyword-intent/

Updated 2026-03-13.

Supports:
- keyword/search intent is the reason behind a query;
- intent can act as a filter for whether a keyword belongs in a strategy;
- business potential is a separate evaluation dimension.

### Ahrefs — Keyword Strategy
https://ahrefs.com/blog/keyword-strategy/

Updated 2026-03-13.

Supports:
- scoring business potential separately;
- mapping keywords to search intent/content type;
- using these dimensions in strategy/prioritization rather than inventing them as independent evidence providers.

### Semrush — Keyword Clustering
https://www.semrush.com/blog/keyword-clustering/

Supports:
- clustering around shared search intent;
- one-page compatibility depends on intent, not lexical similarity alone.

### Semrush — Keyword Mapping
https://www.semrush.com/blog/keyword-mapping/

Updated 2026-07-27.

Supports:
- mapping target keywords/topics to existing or planned pages downstream;
- search-result changes can alter mapping decisions.

## Approved method

### 1. Preserve accepted upstream truth

Step 8 must not rewrite accepted Step-7 semantic status without new evidence.

```text
KEEP stays KEEP upstream
REVIEW stays REVIEW upstream
EXCLUDE_* stays EXCLUDE_* upstream
```

Step-8 disposition is a routing/handoff layer only.

### 2. Use only executable routing states

Approved Step-8 dispositions:

```text
CORE_CANDIDATE
REVIEW_SEARCH
REVIEW_DEFERRED
EXCLUDED_PRESERVED
```

Meanings:

```text
CORE_CANDIDATE
= accepted KEEP; remains eligible working semantic evidence.

REVIEW_SEARCH
= ordinary Search/SERP is the real next evidence action required to resolve intent, relevance, result type, boundary or compatibility.

REVIEW_DEFERRED
= unresolved evidence preserved, but no immediate bounded Search action is justified yet.

EXCLUDED_PRESERVED
= accepted exclusion preserved for audit with no active Search route.
```

The exact names are PROJECT-SPECIFIC.

### 3. Do not create non-executable evidence routes

Forbidden as Step-8 routes unless a real independent source/action actually exists:

```text
REVIEW_BUSINESS
REVIEW_SEARCH_AND_BUSINESS
```

Reason:

```text
business relevance/potential is an evaluation dimension;
internal business priority is a separate client/internal-data constraint;
neither automatically creates an evidence provider/action.
```

### 4. Distinguish public business relevance from internal business priority

```text
PUBLIC BUSINESS RELEVANCE / FIT
= can the known public offer/site satisfy the query once intent is understood?

INTERNAL BUSINESS PRIORITY
= margin, capacity, growth preference, operational priority, strategic focus.
```

Public relevance can be evaluated from known business/site scope together with Search intent.

If internal priority is unavailable, record it as a later limitation/client-confirmation point. Do not create a semantic-routing category for missing private data.

### 5. Preserve REVIEW rather than simplifying it away

Every accepted REVIEW row must either:

```text
receive REVIEW_SEARCH
or
receive REVIEW_DEFERRED
```

No REVIEW row may disappear simply to reduce Search workload.

### 6. Preserve non-exact duplicates without automatic merge

Non-exact duplicate candidates remain unresolved until Search/intent/page-boundary evidence justifies a merge.

Possible Step-8 duplicate routes:

```text
ORDINARY_SEARCH_BEFORE_ANY_NONEXACT_MERGE
DEFER_UNLESS_GROUP_SELECTED_FOR_SEARCH
```

No automatic merge in Step 8.

### 7. Freeze immutable artifacts and hashes

The step must produce a stable snapshot that downstream Search can reference. Exact filenames are project mechanics; the essential requirement is:

```text
complete row-preserving handoff
explicit REVIEW routing
preserved exclusions
preserved non-exact candidates
reconciliation
hashes/version identity
```

## Known error — unsupported business routing taxonomy

### What failed

A Step-8 implementation created:

```text
REVIEW_BUSINESS
REVIEW_SEARCH_AND_BUSINESS
```

and defended an empty `REVIEW_BUSINESS = 0` category.

### Root cause

External research had been collected, but individual invented method elements were not traced to the exact source claims.

```text
RESEARCH_COLLECTED
was incorrectly treated as
METHOD_VALIDATED
```

The model created a tidy symmetric taxonomy after the research even though the sources did not require it and the workflow had no real `business evidence` action.

### Corrected method

Only use states that have:

```text
1. a direct source/project justification;
2. a concrete purpose;
3. a real executable next action/output.
```

Apply universal:
`SOURCE_TO_METHOD_TRACEABILITY_GATE.md`.

## Non-repeat controls

Before Step 8 execution:

```text
SOURCE_TO_METHOD_TRACEABILITY = PASS
UNSUPPORTED_METHOD_ELEMENTS = 0
NON_EXECUTABLE_EVIDENCE_ROUTES = 0
UPSTREAM_STATUS_REWRITES_PLANNED = 0
REVIEW_SILENT_DROP_ALLOWED = false
NONEXACT_AUTO_MERGE_ALLOWED = false
FINAL_CLUSTERING_ALLOWED = false
PAGE_OWNERSHIP_ALLOWED = false
```

After execution:

```text
ALL_INPUT_PHRASE_KEYS_RECONCILE = true
ALL_REVIEW_ROWS_ROUTED = true
FORBIDDEN_BUSINESS_ROUTE_STATES = 0
SILENT_DROPS = 0
UPSTREAM_STATUS_REWRITES = 0
NONEXACT_AUTO_MERGES = 0
SEARCH_PROVIDER_CALLS_DURING_FREEZE = 0
```

## Pass gate

Step 8 passes only when:

```text
1. every accepted upstream phrase key is preserved;
2. every accepted REVIEW row has a real route;
3. every accepted exclusion remains auditable;
4. no invented/non-executable evidence route remains;
5. no upstream semantic decision is silently changed;
6. non-exact duplicates remain unresolved unless stronger evidence already exists;
7. no final clustering/page ownership is performed;
8. immutable snapshot identity/reconciliation exists;
9. source-to-method traceability passes.
```

## What Step 8 does NOT decide

```text
final Search intent
bounded Search query sample/manifest
final clustering
page ownership
structural actions
cannibalization
Search-only architecture
AI evidence
internal margin/capacity priorities
final recommendation priority
```

## Method origin

```text
OFFICIAL:
Yandex user need/query selection/query-page evidence

INDUSTRY_PRACTICE:
intent/business-potential separation; intent-based clustering/mapping

PROJECT-SPECIFIC:
explicit freeze layer, exact state names, artifact/hash mechanics

PROJECT_TEST_VALIDATED:
unsupported business-route failure and corrected minimal routing
```

Canonical markers:

```text
KW001_STEP8_METHOD_APPROVED_AFTER_CORRECTION = true
KW001_STEP8_ONLY_EXECUTABLE_ROUTES_ALLOWED = true
KW001_STEP8_REVIEW_BUSINESS_FORBIDDEN_WITHOUT_REAL_SOURCE = true
KW001_STEP8_REVIEW_SEARCH_AND_BUSINESS_FORBIDDEN_WITHOUT_REAL_SOURCE = true
KW001_STEP8_INTERNAL_PRIORITY_NOT_SEMANTIC_ROUTE = true
KW001_STEP8_SOURCE_TO_METHOD_TRACEABILITY_REQUIRED = true
```