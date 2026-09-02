# Exact Codex prompt — OKNO_MSK Step 14A

Use this prompt without semantic shortening. Codex may make implementation choices needed to execute it, but must not weaken acceptance criteria or advance to Step 15.

---

You are working in the GitHub repository:

`MaksimUnimax/Yandex_direct`

Use the existing working branch:

`roadmap/kwork-productization-2026-08-28`

Your task is to execute **ONLY the mandatory Step 14A correction for OKNO_MSK: deterministic current-site discovery + literal as-is internal-link topology verification**.

Do NOT execute Step 15 or any later roadmap step.
Do NOT use Yandex GenSearch/Alice/AI evidence.
Do NOT make paid provider/API calls.
Do NOT mutate the public website.
Do NOT invent SEO ownership decisions that require analytical judgment.

## 1. Mandatory context to read first

Before writing or running code, read these repository authorities in this order:

1. `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/RULES_ARCHITECTURE.md`
2. `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/RULES_ARCHITECTURE_CODEX_SITE_DISCOVERY_GATE_ADDENDUM_2026-09-02.md`
3. `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/STEP_14_SEARCH_ONLY_ARCHITECTURE_FREEZE_METHOD.md`
4. `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`
5. `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/STEP_RULES_INDEX.md`
6. `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14A_CODEX_DISCOVERY_TOPOLOGY_CORRECTION_AND_GATE_2026-09-02.md`
7. `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14_CURRENT_STATE.json`
8. `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14_SEARCH_ONLY_ARCHITECTURE_FREEZE.tsv`
9. `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14_INTERNAL_LINK_ARCHITECTURE.tsv`
10. `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14_CURRENT_URL_RECHECK.tsv`
11. `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14_UNRESOLVED_AND_BOUNDARY_LEDGER.tsv`
12. Step-11 Codex discovery precedent for this same job, especially files matching:
    - `STEP_11_CODEX_DISCOVERED_URLS.tsv`
    - `STEP_11_CODEX_PAGE_PROFILE_LEDGER.tsv`
    - `STEP_11_CODEX_CURRENT_PAGE_REFRESH_REPORT_2026-08-30.md`

Also inspect any existing scripts/runners/workflows used for Step 11 or Step 14 before creating a new one. Reuse or extend the strongest existing deterministic pattern when practical. Do not create a duplicate weaker mechanism merely for convenience.

## 2. Why this correction exists

The first Step 14 run correctly rechecked 59 known implementation-relevant URLs, but that was a **known-URL recheck**, not proof that the complete current relevant public-site universe had been discovered.

The earlier logic incorrectly allowed this implication:

```text
all known upstream URLs rechecked and live
-> current architecture coverage is sufficient
```

That is invalid because:

```text
KNOWN_URL_RECHECK != CURRENT_SITE_DISCOVERY
UPSTREAM_INPUT_UNIVERSE != CURRENT_SITE_UNIVERSE
```

A closed list cannot prove its own completeness.

The first Step 14 run also preserved 15 recommended internal-link actions after source URL, target URL and semantic compatibility checks, but endpoint existence is not proof of a literal current link:

```text
SOURCE_LIVE + TARGET_LIVE + SEMANTIC_FIT != EDGE_IMPLEMENTED
SEMANTIC_LINK_RECOMMENDATION != CURRENT_AS_IS_LINK
```

This correction must therefore independently discover the current site and build the actual literal HTML link graph.

## 3. Site and scope

Primary public site:

`https://okno-msk.ru/`

The crawl is for public same-site HTML discovery/topology evidence only.

Do not crawl arbitrary external sites.
Do not follow tracking/login/account/action URLs.
Do not submit forms.
Do not trigger business actions.
Do not mutate anything.

Use normal respectful bounded HTTP fetching. Implement a sensible timeout, bounded retries and a modest concurrency/rate so the site is not hammered.

If the site has public sitemap index/sitemaps, use them as **additional discovery evidence**, not as the sole crawl source.

## 4. Discovery requirements

Build an independent deterministic current URL universe using at minimum:

### A. Crawl discovery
- start at the homepage;
- follow normal same-site HTML `<a href>` links;
- perform BFS-style or equivalently auditable traversal;
- record minimum crawl depth from the start page where observable;
- preserve discovery parent/source where practical.

### B. Sitemap discovery
- discover public sitemap(s) from conventional locations and/or site evidence;
- parse sitemap index/sitemap XML when available;
- add same-site public page URLs as a separate discovery source;
- preserve whether a URL is crawl-discovered, sitemap-discovered, known-upstream, or multiple.

### C. Known-upstream reconciliation seeds
Load known URLs from accepted Step 12/13/14 artifacts so that important known pages remain visible even if the crawl cannot fetch one temporarily.

Do NOT treat the known-upstream set as the crawl universe.

## 5. URL normalization and exclusions

Implement deterministic normalization sufficient to avoid duplicate graph nodes from superficial URL variants while preserving material redirect/final-URL evidence.

At minimum consider:
- absolute vs relative links;
- fragments;
- scheme/host canonicalization for the same public site;
- default ports if relevant;
- obvious tracking query parameters;
- trailing-slash normalization consistent with observed site behavior;
- redirects/final URLs.

Do NOT collapse materially distinct URLs merely because they look similar.

Persist exclusions/reasons for non-page/action/tracking/external links when useful for QA.

## 6. Fetch/profile ledger

For each discovered/known public page URL, persist machine-readable evidence including as applicable:

- normalized URL;
- originally discovered URL if different;
- discovery origin(s);
- HTTP/fetch state;
- status code;
- final URL after redirects;
- redirect state/chain summary when observable;
- content type;
- title;
- H1 or first relevant H1;
- minimum crawl depth where observable;
- incoming internal-link count;
- outgoing internal-link count;
- sitemap membership;
- crawl reachability;
- fetch/parser error state if any.

Do not use OCR. This is HTML/network evidence.

## 7. Literal internal-link graph

For fetched HTML pages, extract literal same-site internal links from actual `<a href>` elements.

Persist at minimum:

- `source_url`
- `target_url`
- normalized target URL
- anchor text when available
- source fetch state
- whether target is known/fetched/live/redirected/broken/unknown
- discovery/provenance fields needed to reproduce the edge

The graph must represent **current as-is HTML evidence**, not SEO recommendations.

## 8. Topology classifications

Using deterministic evidence only, classify observable conditions such as:

- crawl + sitemap discovered;
- crawl-only;
- sitemap-only;
- known-upstream-only;
- orphan candidate / no crawl inlinks from discovered HTML graph;
- fetch failed / indeterminate;
- redirected page;
- broken internal target;
- unreachable from homepage crawl but present in sitemap/upstream.

Be conservative with the word `orphan`: if the crawl is incomplete or blocked, use `ORPHAN_CANDIDATE` / bounded wording rather than an absolute claim.

## 9. Reconcile with upstream Step 14

Create a machine-readable reconciliation between the newly discovered current URL universe and the known Step 12/13/14 universe.

Every URL not represented upstream must be surfaced for ChatGPT analytical review.

Do NOT decide semantic ownership yourself unless the repository already contains a deterministic exact rule that clearly applies.

For new URLs, output evidence fields that let ChatGPT later classify:

```text
ARCHITECTURE_MATERIAL
NON_MATERIAL_WITH_REASON
OUT_OF_SCOPE_WITH_REASON
```

But leave the analytical classification pending when semantic judgment is required.

The reconciliation must make these sets/counts explicit:

```text
TOTAL_NORMALIZED_CURRENT_URLS
CRAWL_DISCOVERED_URLS
SITEMAP_DISCOVERED_URLS
KNOWN_UPSTREAM_URLS
CURRENT_URLS_NOT_IN_UPSTREAM
UPSTREAM_URLS_NOT_FOUND_BY_CRAWL
UPSTREAM_URLS_NOT_FOUND_BY_SITEMAP
FETCH_FAILED_OR_INDETERMINATE
REDIRECTED_URLS
BROKEN_INTERNAL_TARGETS
ORPHAN_CANDIDATES
```

## 10. Verify all planned Step-14 IMPLEMENT edges

Load the exact planned/recommended internal-link rows from:

`STEP_14_INTERNAL_LINK_ARCHITECTURE.tsv`

Identify the 15 edges that Step 14 currently treats as IMPLEMENT/frozen recommendations.

For EACH of those 15, independently verify the current source HTML and classify the actual topology state from literal normalized `<a href>` evidence:

```text
AS_IS_PRESENT
AS_IS_ABSENT_PLANNED
BLOCKED_OR_UNVERIFIED
NOT_APPLICABLE
```

Rules:

`AS_IS_PRESENT`
= the fetched current source HTML contains a literal normalized `<a href>` resolving to the target/final target under the accepted normalization rules.

`AS_IS_ABSENT_PLANNED`
= source and target are available/current enough to test, recommendation remains merely a recommendation, but literal current edge is absent.

`BLOCKED_OR_UNVERIFIED`
= fetch/parser/redirect/other evidence prevents a reliable current claim.

Do NOT infer `AS_IS_PRESENT` from breadcrumbs, shared navigation taxonomy, semantic relatedness, endpoint liveness or previous Step-12 recommendation alone.

Persist recommendation state separately from as-is state.

The output must account for all 15 rows exactly once.

## 11. Required outputs

Write these artifacts under:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/`

Required filenames:

1. `STEP_14A_CODEX_SITE_DISCOVERY_URLS.tsv`
2. `STEP_14A_CODEX_INTERNAL_LINK_GRAPH.tsv`
3. `STEP_14A_CODEX_PAGE_PROFILE_LEDGER.tsv`
4. `STEP_14A_CODEX_UPSTREAM_RECONCILIATION.tsv`
5. `STEP_14A_CODEX_REQUIRED_EDGE_VERIFICATION.tsv`
6. `STEP_14A_CODEX_QA.json`
7. `STEP_14A_CODEX_REPORT.md`

Also commit the deterministic runner/script used for the crawl/topology analysis under an appropriate existing tooling/test location. Prefer extending an existing Step-11/Step-14 runner if that is cleaner and preserves compatibility.

If additional machine-readable helper artifacts materially improve reproducibility, add them, but do not replace the required outputs.

## 12. QA requirements

`STEP_14A_CODEX_QA.json` must contain explicit boolean/count checks, not only prose.

At minimum test/report:

```text
CODEX_RUN_EXECUTED = true
DISCOVERY_FROM_CRAWL_ATTEMPTED = true
SITEMAP_DISCOVERY_ATTEMPTED = true
NORMALIZED_CURRENT_URL_UNIVERSE_MATERIALIZED = true
DISCOVERY_ORIGINS_PRESERVED = true
LITERAL_INTERNAL_HTML_GRAPH_MATERIALIZED = true
PAGE_PROFILE_LEDGER_MATERIALIZED = true
UPSTREAM_RECONCILIATION_MATERIALIZED = true
CURRENT_URLS_NOT_IN_UPSTREAM_COUNT = <integer>
UNRECONCILED_MECHANICAL_URL_ROWS = 0
PLANNED_IMPLEMENT_EDGE_BASELINE = 15
PLANNED_IMPLEMENT_EDGES_CLASSIFIED = 15
PLANNED_IMPLEMENT_EDGES_AS_IS_PRESENT = <integer>
PLANNED_IMPLEMENT_EDGES_AS_IS_ABSENT_PLANNED = <integer>
PLANNED_IMPLEMENT_EDGES_BLOCKED_OR_UNVERIFIED = <integer>
PLANNED_IMPLEMENT_EDGES_NOT_APPLICABLE = <integer>
PLANNED_IMPLEMENT_EDGE_ACCOUNTING = 15/15
RECOMMENDATION_STATE_SEPARATE_FROM_AS_IS_STATE = true
SILENT_URL_DROP = 0
SILENT_EDGE_DROP = 0
PUBLIC_SITE_MUTATIONS = 0
PAID_PROVIDER_CALLS = 0
GENSEARCH_ALICE_CALLS = 0
STEP15_EXECUTED = false
```

If crawl completeness is materially blocked by fetch failures, loops, anti-bot behavior, parser errors or another limitation, do not fabricate PASS. Record the exact limitation and fail closed where required.

## 13. Important analytical boundary

Your job is to generate deterministic current-site evidence.

Do NOT automatically:

- create new target pages;
- assign phrases to newly discovered pages;
- change page ownership;
- merge/delete pages;
- recommend 301/308 redirects;
- set canonicals;
- decide that a newly discovered page is architecture-material merely because it exists;
- change Step-13 cannibalization conclusions without explicit evidence and analytical review.

Instead surface the evidence so ChatGPT can perform the semantic reconciliation after readback.

## 14. Preserve the existing semantic baseline unless contradicted

Do not destroy the accepted Step-14 semantic baseline merely because Step 14A is reopened.

The following remain provisional-preserved inputs unless new deterministic evidence creates a concrete affected-unit issue:

```text
ACTIVE_PHRASES = 2332
ASSIGNED = 2313
PRESERVED_UNRESOLVED = 19
STRUCTURAL_UNITS = 168
STEP13_EFFECTIVE_PAIRS = 199
STEP13_QUERY_FAMILY_CASES = 21
STEP12_FINAL_LINK_ROWS = 58
SUPPORTED_NEW_PAGE_ACTIONS = 0
SUPPORTED_DESTRUCTIVE_ACTIONS = 0
```

Do not silently change those counts.

## 15. Git and report discipline

Work only on the specified existing branch.

Commit all code and required artifacts.

At the end, provide a concise completion report containing:

1. final commit SHA;
2. files created/changed;
3. crawler/script path;
4. total normalized current URLs;
5. crawl-discovered count;
6. sitemap-discovered count;
7. current URLs not represented upstream;
8. fetch failures/indeterminate count;
9. broken internal target count;
10. orphan-candidate count;
11. 15-edge classification counts (`AS_IS_PRESENT`, `AS_IS_ABSENT_PLANNED`, `BLOCKED_OR_UNVERIFIED`, `NOT_APPLICABLE`);
12. QA status;
13. any blocker/limitation requiring ChatGPT analytical review.

Do not claim Step 14 is finally closed. Codex produces the evidence; ChatGPT performs the semantic reconciliation and final acceptance/readback afterward.

---

END OF PROMPT
