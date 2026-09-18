# KW-002 — LEVEL 2 / STEP 07 COMPETITOR SEMANTIC EXPANSION

Status: **ACTIVE / UNIVERSAL / MANDATORY FOR STEP07**  
Created: 2026-09-17  
Post-acceptance methodology amendment: **2026-09-18 — dual-lane competitor discovery + access-state evidence validation are mandatory.**  
Source-availability fallback amendment: **2026-09-18 — unavailable external ranking-query enrichment is a declared recall limitation, not an unconditional roadmap deadlock.**  
Applies to: every KW-002 job that reaches competitor semantic expansion.

Companion authorities:

- `STEP_RULES_INDEX.md`;
- `../LEVEL1/COMMON_RULES.md`;
- `../LEVEL1/INHERITED_KW001_UNIVERSAL_RULES.md`;
- `../LEVEL1/DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md`;
- `../LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`;
- `../LEVEL1/METHOD_SOURCE_AND_EVIDENCE_RULES.md`;
- `../LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`;
- `../LEVEL1/WORK_HANDOFF_RULE.md`;
- `../LEVEL1/WORK_BASE_FRESHNESS_AND_AUTHORITY_DRIFT_RULE.md`;
- current accepted Step03B, Step04, Step05 and Step06 job authorities.

This is a universal rule. Client names, live domains, current row counts, hashes,
snapshot dates and job-specific paths belong in `work/<JOB_ID>/`.

---

## 0. Purpose and hard boundary

Step07 is **competitor semantic expansion**. It uses only search competitors
authorized by accepted Step06 evidence to discover candidate terminology,
categories, subcategories, use-cases, attributes, naming variants, problem or
service formulations and informational branches that may be missing from the
accepted semantic universe.

```text
COMPETITOR PAGE TOPIC != PROVEN SEARCH DEMAND
COMPETITOR-DERIVED SEED != PRODUCTION KEYWORD
BUSINESS RIVAL != SEARCH COMPETITOR
FAMILY != FINAL INTENT != SERP CLUSTER != PAGE
STEP07 DISCOVERS CANDIDATES
STEP08 VALIDATES DEMAND
```

Step07 MUST NOT perform Wordstat validation, Search/SERP acquisition, final
intent classification, final clustering, site architecture, URL ownership,
H1/Title decisions or final keyword-to-page mapping.

---

## 1. Entry gate and authority order

Step07 may start only when all conditions are true:

```text
CURRENT_REMOTE_BASE_FETCHED = true
APPLICABLE_LEVEL1_AND_LEVEL2_RULES_READ = true
STEP03B_ACCEPTED_AUTHORITY_IDENTIFIED = true
STEP04_ACCEPTED_AUTHORITY_IDENTIFIED = true
STEP05_ACCEPTED_AUTHORITY_IDENTIFIED = true
STEP06_DURABLE_PASS = true
STEP06_AUTHORIZED_COMPETITOR_UNIVERSE_FROZEN = true
STEP07_JOB_SCHEMA_CONTRACT_PRESENT = true
STEP07_JOB_WORK_PROMPT_PRESENT = true
PRE_STEP_EXTERNAL_RESEARCH_COMPLETE = true
```

Authority order:

1. current live Level1 rules;
2. this Level2 rule and current `STEP_RULES_INDEX.md`;
3. current accepted upstream manifests/acceptances;
4. job-specific Step07 pre-handoff manifest and schema contract;
5. current live data files named by those authorities;
6. historical/supporting artifacts only where explicitly named as such.

If the remote base or any authoritative input differs from the preparation
manifest, execution pauses for authority-drift reconciliation. It MUST NOT
silently continue from a stale prepared whitelist or schema.

---

## 2. Authorized competitor universe

The accepted Step06 curated competitor registry is the only authority allowed
to admit a competitor into Step07.

Every job MUST materialize a stable Step07 authority ID mapped one-to-one to a
current Step06 registry row. The mapping retains at least:

```text
competitor_authority_id
source_registry_row_number
site
canonical_site
registry_class
registry_priority
registry_inclusion_basis
collision_dependency
evidence_queries
source_registry_sha256
authority_status
```

Rules:

- a domain in raw SERP evidence but absent from the curated registry is not
  authorized;
- a business rival not proved by Step06 is not authorized;
- sibling domains and subdomains are not inherited automatically;
- `www` is only a presentation alias when the registry/evidence resolves it to
  the same canonical host;
- an international, regional, language or mobile host is a separate authority
  unless the job manifest explicitly proves and permits the equivalence;
- collision-dependent competitors remain authorized only under their explicit
  collision controls; their language is not accepted at face value;
- a secondary-discovery competitor may yield candidates but does not acquire
  demand authority or primary status.

```text
RAW STEP06 DOMAIN != AUTHORIZED STEP07 COMPETITOR
AUTHORIZED HOST != ALL SIBLING HOSTS
```

---

## 3. Allowed source surfaces

Step07 may inspect public, legitimately accessible surfaces on an authorized
host when they fall inside the job-specific theme/path scope:

- category and subcategory pages;
- product or service pages;
- public navigation and taxonomy labels;
- collection or use-case landing pages;
- public articles, guides, FAQ/help and glossaries;
- page titles, headings, breadcrumbs, labels and concise contextual text;
- public sitemaps used for URL discovery;
- public structured metadata that is visibly attributable to the page.

Step07 MUST NOT:

- authenticate, log in or enter private areas;
- bypass CAPTCHA, robots restrictions, paywalls or anti-bot controls;
- probe private APIs or hidden endpoints;
- use a search-demand provider to compensate for inaccessible pages;
- expand from an authorized host to arbitrary external links;
- copy reviews, user-generated text or unsupported claims as business truth;
- treat footer boilerplate, legal text, tracking labels or UI controls as
  semantic candidates without independent topical context.

An inaccessible surface becomes coverage evidence. Its content is never
fabricated or inferred.

---

## 3A. Mandatory dual-lane semantic discovery

Competitor semantic expansion is not complete if it mines only visible page text.
Every Step07 execution MUST treat competitor discovery as two complementary lanes:

### Lane A — `PAGE_SURFACE_DISCOVERY`

Mine the permitted public surfaces defined above for terminology, taxonomy,
product/service names, use-cases, attributes, problem formulations and
informational branches.

### Lane B — `ORGANIC_RANKING_QUERY_DISCOVERY`

For every materially relevant authorized search competitor, acquire current
organic ranking-query evidence from a method-approved source that can show
queries for which the competitor domain or relevant competitor URL is visible
in Yandex organic search, or the closest explicitly approved Yandex-oriented
ranking dataset available to the product.

The ranking-query lane exists because a page may rank for a query whose wording
does not literally occur in its title, headings, taxonomy labels or body text.
Page mining alone therefore cannot claim complete competitor-semantic recall.

Minimum ranking-query provenance, where supplied by the source:

```text
competitor_authority_id
source_system
source_snapshot_or_timestamp
query_raw
query_normalized_comparison_key
ranking_url
ranking_position_or_visibility_metric_if_available
source_export_or_evidence_identity
candidate_relation
notes
```

Hard boundaries:

- ranking-query evidence is a discovery signal, not proven demand volume;
- a competitor ranking query does not become a production keyword in Step07;
- Wordstat validation remains Step08;
- ranking position/visibility does not override business scope or sanitation;
- ranking-query candidates must pass the same reconciliation/provenance rules
  as page-derived candidates;
- source-specific estimates such as traffic/volume are not inherited as Yandex
  demand authority unless a later rule explicitly authorizes them;
- if a material authorized competitor cannot be covered by the ranking-query
  source, record the limitation explicitly.

A Step07 release MUST declare one of:

```text
RANKING_QUERY_LANE = COMPLETE
RANKING_QUERY_LANE = SOURCE_UNAVAILABLE_DECLARED_LIMITATION
RANKING_QUERY_LANE = NOT_APPLICABLE_BY_PRE_FROZEN_PRODUCT_MODE_EXCEPTION
```

`SOURCE_UNAVAILABLE_DECLARED_LIMITATION` is permitted only when all of the
following are true:

```text
PAGE_SURFACE_DISCOVERY_LANE_COMPLETE = true
ACCESS_STATE_CONTENT_VALIDATION = PASS
RANKING_QUERY_SOURCE_RECOVERY_DOCUMENTED = true
LEGITIMATELY_ACCESSIBLE_APPROVED_SOURCE_FOUND = false
ACCESS_CONTROL_BYPASS = false
GOOGLE_OR_PAID_SEARCH_DATA_MISREPRESENTED_AS_YANDEX_ORGANIC = false
KNOWN_RECALL_LIMITATION_EXPLICIT = true
RANKING_QUERY_LANE_REOPEN_CONDITION_EXPLICIT = true
```

Source recovery must be a bounded, evidence-bearing attempt to locate a source
that can expose real competitor domain/URL -> raw query -> Yandex organic
ranking evidence. A failed source-recovery attempt is not a zero-query result.

When this declared limitation is valid, Step07 may PASS for the evidence that
is actually available and may hand off its acquired candidate universe to
Step08. It MUST NOT claim full competitor ranking-query recall or full
competitor-semantic completeness. If legitimate access becomes available
later, the ranking-query lane may be reopened as enrichment without rewriting
immutable page evidence or invalidating already preserved provenance.

A pre-frozen product-mode exception still must be justified by Main Chat before
execution. Silence is never an exception or a limitation state.

```text
PAGE_TEXT_MINING_ONLY != COMPLETE_COMPETITOR_SEMANTIC_RECALL
SOURCE_UNAVAILABLE != ZERO RANKING QUERIES
SOURCE_UNAVAILABLE != PERMISSION TO FABRICATE EVIDENCE
EXTERNAL ENRICHMENT SOURCE UNAVAILABLE != PERMANENT ROADMAP DEADLOCK
COMPETITOR_RANKING_QUERY != PROVEN_DEMAND
STEP07_DISCOVERY_RECALL_REQUIRES_DECLARED_CHANNELS
```

---
## 4. Host-scope policy

The job must assign every authorized competitor exactly one deterministic
scope policy:

### `EVIDENCE_ANCHORED_RELEVANT_SUBTREE`

Use for broad platforms, encyclopedias, dictionaries and other domains whose
whole-site universe is unrelated or practically unbounded. Eligible discovery
starts from every Step06-observed URL for that authorized host, then follows
public taxonomy/navigation only within the same demonstrably relevant topical
branch. The rest of the host is out of scope.

### `THEME_SCOPED_PUBLIC_TAXONOMY`

Use for specialized commercial or thematic sites. Inspect the public,
authorized-host taxonomy that is relevant to the job theme, including all
eligible category/product/informational URLs discovered inside that scope.
Unrelated site branches remain excluded with a reason.

No policy authorizes crawling the entire Internet or an entire general-purpose
marketplace. Scope is defined by Step06 evidence plus public site taxonomy,
not by an arbitrary page quota.

---

## 5. URL discovery and canonicalization

For every authorized competitor, build a deterministic URL frontier from:

1. all Step06-observed URLs for the canonical host;
2. public navigation/breadcrumb links reachable inside the allowed scope;
3. public sitemap URLs or sitemap indexes that can be scoped to the allowed
   host/path/theme;
4. sequential pagination URLs required to enumerate an eligible collection;
5. redirects reached from an already eligible URL.

URL handling:

- retain `source_url_raw` exactly as discovered;
- resolve relative URLs against their discovery page;
- lowercase scheme and host only;
- convert host identity consistently between Unicode and IDNA/Punycode while
  retaining both display and canonical forms;
- remove fragments for retrieval identity;
- retain path case unless the server proves case-insensitive equivalence;
- normalize dot segments and standard/default ports;
- remove known tracking/session parameters only under an enumerated rule;
- do not remove a parameter that changes page content or product/variant
  identity;
- follow redirects without crossing the authorized host boundary unless the
  final host is separately authorized;
- record declared canonical URL, redirect target and computed canonical URL as
  separate fields;
- do not treat `rel=canonical` as infallible proof; conflicting signals remain
  an explicit ambiguity;
- preserve separately useful paginated pages while excluding alternative-sort
  and duplicate filter variants under an explicit rule;
- prevent faceted/infinite URL expansion by deterministic parameter rules, not
  by taking an arbitrary top-N sample.

---

## 6. Access and terminal URL states

Every discovered URL receives exactly one terminal processing state:

```text
INSPECTED_CANDIDATE_YIELD
INSPECTED_NO_CANDIDATE
EXCLUDED_OUT_OF_SCOPE
EXCLUDED_DUPLICATE_CANONICAL
EXCLUDED_FACET_OR_SORT_VARIANT
EXCLUDED_NON_HTML_OR_UNSUPPORTED
INACCESSIBLE_ROBOTS
INACCESSIBLE_AUTH_OR_LOGIN
INACCESSIBLE_CAPTCHA_OR_ANTI_BOT
INACCESSIBLE_HTTP
INACCESSIBLE_TIMEOUT_OR_NETWORK
DELETED_OR_NOT_FOUND
REDIRECTED_IN_SCOPE
REDIRECTED_OUT_OF_SCOPE
UNRESOLVED_DYNAMIC_CONTENT
ERROR
```

`ERROR`, `UNRESOLVED_DYNAMIC_CONTENT` and inaccessible states are not silently
converted into `INSPECTED_NO_CANDIDATE`.

For JavaScript, infinite-scroll or load-more interfaces, inspect legitimately
rendered public content only. Use public sequential URLs/sitemaps where they
exist. If exhaustive enumeration cannot be established, record unresolved
coverage and do not claim completion for that competitor.

---

## 6A. Evidence-content validation for access states

A terminal label is valid only when it matches the captured evidence content.

An URL may be classified as `INSPECTED_CANDIDATE_YIELD` or
`INSPECTED_NO_CANDIDATE` only when the stored evidence demonstrates that the
target page's substantive public content was actually obtained and inspected.

The following are not substantive target-page content and MUST NOT be converted
to `INSPECTED_NO_CANDIDATE`:

- browser/connector error shells;
- connection or network failure pages;
- VPN/proxy restriction notices;
- CAPTCHA or anti-bot interstitials;
- access-denied/login barriers;
- placeholder/loading shells with no resolved target content;
- HTTP error pages or target-side service failure pages.

They must map to the applicable inaccessible/error/unresolved state.

Required full-volume QA:

```text
EVERY_INSPECTED_STATE_HAS_TARGET_CONTENT_EVIDENCE = true
BLOCK_OR_ERROR_EVIDENCE_MISCLASSIFIED_AS_INSPECTED = 0
ACCESS_STATE_CONTENT_VALIDATION_SCOPE = FULL_DISCOVERED_URL_LEDGER
```

Mechanical reconciliation of counts is insufficient. The QA must validate the
semantic meaning of the terminal state against the actual stored evidence.
Producer-assigned states cannot self-certify this gate.

```text
COUNTS_RECONCILE != ACCESS_CLASSIFICATION_PROVEN
INSPECTED_STATUS != TARGET_CONTENT_OBTAINED_UNLESS_EVIDENCE_CONFIRMS_IT
```

---
## 7. Full-volume coverage contract

Step07 is not a representative-page review. It processes the complete bounded
eligible URL universe for every authorized competitor.

Required per-competitor accounting:

```text
authorized_competitor = 1
discovered_urls
eligible_urls
inspected_urls
excluded_urls
inaccessible_urls
redirected_urls
candidate_yield_urls
no_candidate_urls
unresolved_urls
terminal_coverage_status
```

Mechanical reconciliation:

```text
DISCOVERED_URLS
= INSPECTED_URLS
 + EXCLUDED_URLS
 + INACCESSIBLE_URLS
 + REDIRECTED_TERMINAL_URLS
 + UNRESOLVED_URLS
```

The discovery frontier closes only when every eligible link/sitemap/pagination
path already discovered in the authorized scope has been processed to a
terminal state and no unprocessed eligible URL remains.

If an eligible universe is too large for one run, divide it into deterministic
complete chunks (for example by sitemap file, stable path prefix or canonical
URL sort range). Do not sample. Step07 remains `INCOMPLETE` until all chunks
reconcile.

Terminal competitor states:

```text
COMPLETE
COMPLETE_WITH_INACCESSIBLE_EVIDENCE
INCOMPLETE_UNRESOLVED_COVERAGE
BLOCKED
ERROR
```

Step07 as a whole cannot PASS while any authorized competitor is absent from
the coverage ledger. Material unresolved coverage must be surfaced, not hidden
by a high aggregate inspection rate.

---

## 8. Candidate extraction and provenance

Every candidate occurrence retains enough evidence to reconstruct its origin.
At minimum:

```text
provenance_id
candidate_id
competitor_authority_id
competitor_domain
source_url_id
source_url_raw
source_url_canonical
source_page_type
source_section
source_location
raw_wording
source_context
normalized_candidate
transformation_rule
extraction_timestamp_utc
ambiguity_flag
out_of_scope_reason
notes
```

Raw wording is immutable. A normalized candidate never replaces its source
text. One candidate may have many provenance rows; one source URL may yield
many candidates.

Candidate material may be extracted from a title, heading, breadcrumb,
category label, product/service name, use-case label, FAQ question, glossary
term or a concise contextual formulation. The location and evidence class must
be recorded.

---

## 9. Text normalization

Normalization is a comparison aid, not authority to rewrite meaning.

Required ordered rules:

1. retain `raw_wording` and `source_context` unchanged;
2. decode valid HTML character references and remove markup while retaining
   visible text;
3. apply Unicode NFC, never blind compatibility folding;
4. trim outer whitespace and collapse internal whitespace;
5. use Unicode-aware casefold only for the comparison key;
6. remove demonstrable UI/formatting noise only under an enumerated rule;
7. preserve punctuation, digits, hyphens and mixed-language tokens when they
   may affect meaning;
8. preserve brand/product/category names as observed;
9. do not lemmatize or merge morphology as an exact-duplicate operation;
10. record every semantic rewrite/removal in `transformation_rule`.

Competitor brand removal is permitted only as a separate derived candidate
when the remaining wording is independently meaningful and the transformation
is explicit. The branded raw occurrence remains preserved.

Long wording may yield a shorter candidate only when the source span and
transformation are reproducible. The shorter wording must not inherit demand
evidence from the longer wording or vice versa.

```text
HISTORICAL DEMAND FOR PHRASE A
!= DEMAND FOR TRANSFORMED PHRASE B
```

---

## 10. Reconciliation taxonomy

Each candidate summary receives exactly one status:

### `ALREADY_PRESENT`

Exact normalized wording matches an accepted upstream identity. Record the
upstream layer and ID. Audit-only; no new Step08 probe is created.

### `NEW_CANDIDATE`

No exact accepted upstream identity exists; the wording is in scope and not a
mere duplicate. It may proceed to Step08 as an unvalidated candidate.

### `NORMALIZED_DUPLICATE`

Two or more raw occurrences become the same comparison key under permitted
non-semantic normalization. Link to the canonical candidate and retain all
provenance. No separate Step08 row.

### `POSSIBLE_VARIANT`

Morphological, lexical, transliteration, spelling or likely-synonym relation is
plausible but not exact. Preserve as a distinct candidate pending later
evidence. It may proceed separately to Step08 and cannot inherit another
phrase's demand.

### `OUT_OF_SCOPE`

Evidence clearly falls outside the business/theme/source boundary. Preserve
for audit with an enumerated reason; exclude from Step08.

### `AMBIGUOUS`

Meaning, referent, extraction or transformation cannot be resolved reliably.
Hold; do not send to Step08 until separately resolved.

Required fields:

```text
existing_universe_relation
reconciliation_status
upstream_match_id
upstream_match_layer
step08_route
ambiguity_flag
ambiguity_reason
out_of_scope_reason
```

Semantic decisions must be represented by enumerated fields, not only notes.

---

## 11. Reconciliation authority

The job-specific manifest identifies exact canonical files and join keys.
Minimum reconciliation order:

1. full accepted normalized identity universe;
2. current Step03B KEEP/HOLD/EXCLUDE partition;
3. current Step04 preliminary family/ambiguity signals;
4. current Step05 additive or zero-row closure evidence;
5. any other explicitly accepted layer named by the job manifest.

Exact phrase matching uses the upstream-compatible comparison key. Family or
topic similarity alone is not `ALREADY_PRESENT`. A Step04 family is context,
not a final intent or duplicate key.

---

## 12. Deduplication without premature clustering

Definitions:

- **exact duplicate**: identical raw wording after no transformation;
- **normalized duplicate**: identical allowed comparison key after NFC,
  whitespace and casefold controls;
- **same candidate / several URLs**: one candidate summary, several provenance
  rows;
- **same candidate / several competitors**: one candidate summary, all
  competitor provenance retained and source counts recomputed;
- **morphological or lexical variant**: separate `POSSIBLE_VARIANT` unless an
  exact accepted key exists;
- **likely synonym**: separate candidate with relationship metadata;
- **distinct intent-like wording**: remains separate pending later demand/SERP
  work.

```text
LOOKS SIMILAR != DUPLICATE
MULTI-SOURCE EVIDENCE != LICENSE TO DROP OCCURRENCES
STEP07 DEDUPLICATION != FINAL CLUSTERING
```

---

## 13. Required outputs

Every job publishes schemas before execution. The minimum output set is:

```text
COMPETITOR_GAP_CANDIDATES.csv
STEP07_COMPETITOR_COVERAGE_LEDGER.csv
STEP07_SOURCE_URL_LEDGER.csv
STEP07_CANDIDATE_PROVENANCE_LEDGER.csv
STEP07_EXECUTION_QA.md
```

The candidate table is one row per canonical candidate identity. The
provenance ledger carries all candidate/source occurrences. The URL ledger is
one row per authorized-competitor/canonical-URL pair. The coverage ledger is
one row per authorized competitor.

Exact fields, enums, sort order, keys and job paths are frozen in a
job-specific machine-readable schema contract.

---

## 14. QA gate

Step07 PASS requires all of the following:

```text
ONLY_STEP06_AUTHORIZED_COMPETITORS_USED = true
ALL_AUTHORIZED_COMPETITORS_ACCOUNTED_FOR = true
ALL_DISCOVERED_ELIGIBLE_SURFACES_ACCOUNTED_FOR = true
INACCESSIBLE_AND_BLOCKED_SURFACES_RECORDED = true
ARBITRARY_SAMPLE_OR_TOP_N_SUBSTITUTION = 0
PAGE_SURFACE_DISCOVERY_LANE_COMPLETE = true
RANKING_QUERY_DISCOVERY_LANE_COMPLETE = true OR RANKING_QUERY_SOURCE_UNAVAILABLE_DECLARED_LIMITATION = true OR PRE_FROZEN_PRODUCT_MODE_EXCEPTION = true
RANKING_QUERY_SOURCE_RECOVERY_DOCUMENTED = true where RANKING_QUERY_SOURCE_UNAVAILABLE_DECLARED_LIMITATION = true
KNOWN_RECALL_LIMITATION_EXPLICIT = true where RANKING_QUERY_SOURCE_UNAVAILABLE_DECLARED_LIMITATION = true
FULL_COMPETITOR_RANKING_QUERY_RECALL_CLAIM = false where RANKING_QUERY_SOURCE_UNAVAILABLE_DECLARED_LIMITATION = true
SEMANTIC_RECALL_CHANNELS_DECLARED = true
EVERY_INSPECTED_STATE_HAS_TARGET_CONTENT_EVIDENCE = true
BLOCK_OR_ERROR_EVIDENCE_MISCLASSIFIED_AS_INSPECTED = 0
EVERY_CANDIDATE_HAS_PROVENANCE = true
RAW_WORDING_PRESERVED = true
EVERY_TRANSFORMATION_RULE_RECORDED = true
UPSTREAM_RECONCILIATION_COMPLETE = true
SILENTLY_DISCARDED_DUPLICATES = 0
MULTI_SOURCE_PROVENANCE_PRESERVED = true
COMPETITOR_TOPIC_TREATED_AS_PROVEN_DEMAND = 0
WORDSTAT_CALLS_IN_STEP07 = 0
SEARCH_PROVIDER_CALLS_IN_STEP07 = 0
FINAL_INTENT_DECISIONS = 0
FINAL_CLUSTER_DECISIONS = 0
PAGE_URL_H1_TITLE_DECISIONS = 0
HOLD_AMBIGUOUS_ERROR_COUNTS_EXPLICIT = true
OUTPUT_COUNTS_RECONCILE = true
SCHEMA_COMPLIANCE = PASS
EXECUTION_COMPLETENESS_DEMONSTRABLE = true
```

Additional mechanical checks:

- unique authority IDs, candidate IDs, URL IDs and provenance IDs;
- every foreign key resolves;
- every authorized competitor has exactly one coverage row;
- every candidate has at least one provenance row;
- summary source counts equal distinct provenance counts;
- every discovered URL has one terminal state;
- every `INSPECTED_*` URL is validated against stored target-content evidence;
- block/error/connection/VPN/CAPTCHA evidence is never counted as `INSPECTED_NO_CANDIDATE`;
- page-surface and ranking-query discovery lanes have explicit coverage/accounting, a valid `SOURCE_UNAVAILABLE_DECLARED_LIMITATION`, or a pre-frozen allowed exception;
- source concentration and single-source candidate concentration are reported as recall/confidence diagnostics, not hidden by aggregate counts;
- all enums are valid and all required fields are nonblank;
- sort order is deterministic;
- input hashes/base HEAD are recorded;
- no accepted upstream file is mutated in place.

If blocked or unresolved evidence prevents complete accounting, report
`INCOMPLETE` or `COMPLETE_WITH_INACCESSIBLE_EVIDENCE` precisely. A narrative
claim or quality score cannot override a failed hard gate.

---

## 15. Step08 handoff boundary

Only `NEW_CANDIDATE` and eligible `POSSIBLE_VARIANT` rows route toward Step08.
They enter Step08 explicitly as **unvalidated competitor-derived candidates**.

Step08 independently decides whether demand validation is authorized and how
to perform it. Step07 does not pre-authorize a provider call.

```text
STEP07 PASS
-> CANDIDATE DISCOVERY COMPLETE FOR DECLARED AVAILABLE SOURCES
-> KNOWN RECALL LIMITATION REMAINS EXPLICIT IF RANKING SOURCE WAS UNAVAILABLE
-> DEMAND STILL UNPROVEN
-> STEP08 REQUIRES SEPARATE RELEASE
```

---

## 16. Plain-language rule

Use only competitors that Step06 actually proved. Exhaust the bounded public
page surface and attempt the declared organic ranking-query lane under the
released product mode. If a legitimate Yandex organic reverse-index source is
available, acquire it full-volume; if it is not available after documented
source recovery, record `SOURCE_UNAVAILABLE_DECLARED_LIMITATION` and keep the
resulting recall limitation explicit instead of fabricating evidence or
permanently deadlocking the roadmap. Preserve every acquired URL, query and raw
wording, validate every `INSPECTED_*` state against actual target content,
normalize without changing meaning, reconcile every acquired candidate against
the accepted universe, retain multi-source provenance, and stop before demand
validation, intent, clustering or page design.
