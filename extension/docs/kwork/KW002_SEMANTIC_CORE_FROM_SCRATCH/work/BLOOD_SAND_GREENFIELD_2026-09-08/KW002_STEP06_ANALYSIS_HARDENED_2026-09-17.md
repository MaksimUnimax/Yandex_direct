# KW-002 Step06 — hardened SERP / search-competitor analysis

Date: 2026-09-17  
Status: **FINAL LOCAL HARDENING PASS — READY FOR TASK-SPECIFIC OWNER UPLOAD**

## 1. Evidence base

```text
representative queries = 22
organic rows/query = 20
total SERP rows = 440
unique query pairs = 231
domain recurrence universe = 165
curated competitor registry = 32
new provider calls during hardening = 0
```

The three delegated Work artifacts already published by the owner remain immutable inputs and are **not** included in this final delta package.

## 2. Accepted Top-10 intent after semantic hardening

```text
INFORMATIONAL_LED = 11
COMMERCIAL_LED = 6
COLLISION_OR_MISMATCH = 3
HYBRID = 1
UNCERTAIN = 1
```

This supersedes the preliminary broad 8-commercial / 9-informational narrative for accepted analysis. Preliminary `source_serp_class` is preserved only as provenance in the Work dataset.

## 3. Top-10 is the primary competitive layer

Ranks 1-10 are the primary analytical layer; Top-3 amplifies strength; 11-20 remains useful for discovery but is not narrated as equal first-page strength.

Leading Top-10 recurrence in the 22-query bounded snapshot:

| site | Top-10 query coverage | Top-3 query coverage | all SERP rows |
|---|---:|---:|---:|
| ru.wikipedia.org | 15 | 14 | 21 |
| ozon.ru | 10 | 7 | 28 |
| ru.ruwiki.ru | 8 | 7 | 10 |
| wildberries.ru | 7 | 4 | 23 |
| livemaster.ru | 5 | 1 | 11 |
| avito.ru | 4 | 2 | 10 |
| happywitch.ru | 4 | 2 | 4 |
| славяне.сайт | 4 | 1 | 4 |
| slavyanskieoberegi.ru | 4 | 1 | 7 |
| elarus.ru | 3 | 2 | 3 |
| ru.pinterest.com | 3 | 1 | 5 |
| market.yandex.ru | 3 | 1 | 25 |


These figures describe search-surface recurrence, not business quality.

## 4. Exact URL overlap remains separate from domain overlap

The 231-pair matrix is complete.

Two diagnostic examples:

```text
аум ↔ ом
exact URL overlap in Top-10 = 5
domain overlap in Top-10 = 6

руна альгиз ↔ руна отал
exact URL overlap in Top-10 = 0
domain overlap in Top-10 = 6
```

The second pair is the key anti-regression example: the same sites can rank different pages for different intents. Therefore domain recurrence is competitor evidence, not page-cluster proof.

## 5. Collision / uncertainty control

Collision-heavy audit queries remain explicitly visible rather than deleted:

- `талисман` — Top-10 mostly informational target meaning, but material named-entity collisions appear deeper in Top-20;
- `ваджра` — person/media collision dominates;
- `лотос` — unrelated medical/business and other meanings materially contaminate the broad query;
- `улитка` — biological/reference meaning dominates rather than target symbolic/product demand.

`подкова` remains `UNCERTAIN` at Top-10 because real/equestrian and symbolic/souvenir meanings mix.

## 6. Corrected recurrence semantics

The final domain and registry CSVs no longer use ambiguous unqualified `clean_*` labels. They use:

```text
safe_query_subset_top10_coverage_17
```

and state explicitly that this is **query-level filtering**, not row-level target-relevance filtering.

Accepted-intent denominators are now current and explicit:

```text
commercial = 6
informational = 11
hybrid = 1
uncertain = 1
collision/mismatch = 3
collision-heavy audit flags = 4
safe query subset = 17
```

Stale preliminary `commercial_*_8` / `informational_*_9` fields were removed from the final registry.

## 7. Competitor registry interpretation

The 32-row registry is a **curated material registry** selected from the complete 165-domain recurrence universe. It is intentionally not presented as an exhaustive list of every observed domain.

Roles distinguish broad commercial platforms, specialty commerce, broad information authorities, thematic information competitors and cluster-specific commerce. Collision exposure is kept separate.

## 8. Source and scope limitations

```text
REGION_SCOPE = RUSSIA / provider region 225
DEVICE_SCOPE = NOT_CAPTURED_BY_CURRENT_SOURCE
SERP_FEATURE_COVERAGE = NOT_CAPTURED_BY_CURRENT_SOURCE
SNAPSHOT_SCOPE = BOUNDED_SINGLE_ACQUISITION
AUDIO_SURFACES_MAY_BE_COLLAPSED_TO_OTHER_IN_WORK_SCHEMA = TRUE
CONTENT_ANGLE_FULL_AUDIT = DEFERRED_TO_LATER_CONTENT/PAGE-SPEC STEP
```

The frozen Work page-type enum omitted `AUDIO`, so recurring listening/music surfaces can appear under `OTHER`. This is disclosed rather than silently reinterpreted. It is not a blocker for Step06 search-competitor discovery, but future executions must use an extensible taxonomy.

A single snapshot proves observed composition at acquisition time, not permanent Yandex behavior.

## 9. Boundary

```text
FINAL_PAGE_DECISIONS = NONE
FINAL_CLUSTER_DECISIONS = NONE
STEP07_STARTED = FALSE
```

Step06 provides evidence for later governed clustering; it does not assign final pages.
