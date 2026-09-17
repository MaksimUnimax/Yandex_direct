# KW-002 — STEP07 PREPARATION EXTERNAL METHODOLOGY AUDIT

Date: 2026-09-17  
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`  
Step: `STEP07_PREPARATION`  
Remote base inspected: `0630d3f6dbd1962290dc8ab77a454e86c604a795`

Status: **COMPLETE / PREPARATION ONLY / STEP07 NOT EXECUTED**

---

## 1. Research question and boundary

The research tested how a later Step07 execution should:

- discover competitor taxonomy and candidate language without inventing demand;
- inventory public category/product/informational surfaces at full bounded volume;
- preserve URL and text provenance;
- canonicalize URLs without losing materially distinct pages;
- control pagination, facets, parameters and dynamic content;
- respect robots, authentication and anti-bot boundaries;
- normalize candidate wording without changing semantics;
- deduplicate while retaining multi-source evidence;
- prevent competitor-copy bias and overclaiming;
- demonstrate a deterministic stopping condition.

No Wordstat, Yandex Search, AI Search, GenSearch or other project provider
acquisition was performed.

```text
NEW_WORDSTAT_CALLS = 0
NEW_YANDEX_SEARCH_CALLS = 0
NEW_AI_SEARCH_OR_GENSEARCH_CALLS = 0
STEP07_PRODUCTION_EXTRACTION = 0
```

External research was used to challenge and refine the existing KW-002 method.
It did not replace project authority.

---

## 2. Sources used and decisions

| SOURCE | URL | PUBLISHER | DATE / LAST UPDATED | SUPPORTED METHODOLOGICAL POINT | RELATION TO EXISTING KW-002 METHOD | DECISION | RATIONALE |
|---|---|---|---|---|---|---|---|
| Help Google understand your ecommerce site structure | https://developers.google.com/search/docs/specialty/ecommerce/help-google-understand-your-ecommerce-site-structure | Google Search Central | 2025-12-10 | Menus, category→subcategory→product links and sitemaps expose the usable site taxonomy; search boxes alone do not prove discoverable coverage. | Supports taxonomy/navigation as source surfaces and a frontier based on real links. | ADOPT / MODIFY | Adopt link/sitemap discovery. Modify by limiting traversal to Step06-authorized hosts and job-relevant branches; Google indexing guidance is not a demand model. |
| Managing crawling of faceted navigation URLs | https://developers.google.com/crawling/docs/faceted-navigation | Google Crawling Infrastructure | 2025-12-18 | Parameterized facets can create an effectively infinite URL space and duplicate/crawl waste. | Supports deterministic filter/sort exclusion and explicit facet accounting. | ADOPT | Prevents convenience caps from masquerading as coverage while avoiding unbounded generated combinations. |
| What is URL canonicalization | https://developers.google.com/search/docs/crawling-indexing/canonicalization | Google Search Central | 2026-08-20 | Duplicate pages may have one representative canonical; redirects, sitemap presence and `rel=canonical` are signals rather than infallible commands. | Supports raw URL + declared canonical + computed canonical separation. | ADOPT / MODIFY | Preserve signals and conflicts; never erase a URL solely because a page declares a canonical. |
| Pagination, incremental page loading, and Search | https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading | Google Search Central | 2025-12-10 | Sequential links and unique page URLs allow enumeration; crawlers do not generally click buttons or trigger user-action JavaScript. | Supports processing all eligible pagination and recording unresolved infinite-scroll coverage. | ADOPT | Converts dynamic-interface limitations into auditable coverage evidence. |
| Designing a URL structure for ecommerce sites | https://developers.google.com/search/docs/specialty/ecommerce/designing-a-url-structure-for-ecommerce-sites | Google Search Central | 2025-12-10 | Alternative URLs, session/tracking parameters, fragments and continually changing values can create duplicate or infinite URL spaces. | Supports parameter taxonomy and stable URL identity rules. | ADOPT / MODIFY | Adopt for duplicate control; retain parameters that materially change product/variant/page identity. |
| Sitemaps XML format | https://www.sitemaps.org/protocol.html | Sitemaps.org | 2016-11-21 | Sitemaps and sitemap indexes enumerate host-scoped URL sets; one file may contain up to 50,000 URLs and large sites can use multiple files. | Supports deterministic inventory and chunking by sitemap rather than top-N sampling. | ADOPT / MODIFY | A sitemap is a discovery source, not proof that every URL is relevant, live, canonical or complete. Each URL still receives a ledger state. |
| RFC 9309 — Robots Exclusion Protocol | https://www.rfc-editor.org/rfc/rfc9309.html | IETF / RFC Editor | 2022-09 | Crawlers must apply matching robots rules; a network/server-unreachable robots file has a conservative handling path. Robots is not access authorization. | Supports no-bypass policy and separate `robots_status`/access states. | ADOPT / TIGHTEN | Step07 applies a stricter ethical boundary: no bypass, and unclear/unreachable robot control becomes inaccessible/unresolved evidence rather than aggressive access. |
| RFC 3986 — URI Generic Syntax, section 6 | https://www.rfc-editor.org/rfc/rfc3986.html#section-6 | IETF / RFC Editor | 2005-01 | URI normalization can reduce duplicate retrieval; equivalence is purpose-specific, false positives must be avoided, and fragments are excluded for retrieval comparison. | Supports conservative canonical URL construction. | ADOPT | Use syntax-safe normalization while retaining raw URL and avoiding semantic parameter collapse. |
| PROV-O: The PROV Ontology | https://www.w3.org/TR/prov-o/ | W3C | 2013-04-30 | Provenance can represent entities, activities, derivations, primary sources, locations and responsibility chains. | Supports separate candidate summaries and occurrence-level source derivation. | ADOPT / SIMPLIFY | The CSV ledgers implement a practical subset: candidate, source URL, raw wording, transformation and upstream reconciliation links. Full RDF/OWL is unnecessary. |
| Unicode Standard Annex #15 — Unicode Normalization Forms | https://www.unicode.org/reports/tr15/ | Unicode Consortium | 2026-08-12 / Unicode 18.0.0 | NFC preserves canonical equivalence; compatibility forms can erase distinctions and must not be applied blindly. | Supports NFC and rejects silent NFKC semantic folding. | ADOPT | Matches existing Step03A-style conservative text handling and protects mixed-language/product-name distinctions. |
| Keyword Gap | https://www.semrush.com/analytics/keywordgap/ | Semrush | Date not stated; accessed 2026-09-17 | Competitor comparison can surface common and unique terms across domains/subdomains/folders/URLs. | Supports the general idea that competitor evidence can reveal missing directions. | MODIFY / REJECT AS AUTHORITY | Step07 does not import an arbitrary tool-generated competitor universe and does not treat competitor terms as proven demand. Step06 registry controls competitors; Step08 is the demand gate. |

---

## 3. Explicit methodological comparison

| External proposition | Existing KW-002 principle | Prepared Step07 treatment |
|---|---|---|
| Traverse linked taxonomy and sitemaps to discover pages. | Large data must be processed without representative sampling. | Adopt a complete bounded frontier from Step06 URLs, relevant public navigation and scoped sitemaps. |
| Canonicalize duplicates and parameter variants. | Raw evidence and uncertainty must remain durable. | Retain raw, declared and computed canonical URLs; deduplicate only under an enumerated rule; preserve conflicts. |
| Facets can generate infinite URL spaces. | Completeness must be bounded and demonstrable, not asserted. | Exclude known filter/sort generators deterministically; process all remaining eligible pages; unresolved generators block full completion. |
| Dynamic UI may hide pages from link crawlers. | Missing evidence is UNKNOWN, not an invented result. | Use public sequential URLs/sitemaps; otherwise record `UNRESOLVED_DYNAMIC_CONTENT`. No scripted bypass. |
| Competitor gaps surface possible opportunities. | Competitor page topic is not proven demand. | Accept only as unvalidated candidate discovery; route eligible new rows to Step08. |
| URI or text normalization aids deduplication. | Normalization must not silently alter demand semantics. | NFC + whitespace + comparison casefold; no blind compatibility folding, lemmatization, synonym collapse or inherited demand. |
| Provenance should represent derivation. | Raw→normalized lineage must be auditable. | Use candidate summary plus occurrence-level provenance with exact source location, raw wording and transformation. |

---

## 4. Adopted controls

### 4.1 Search competitor authority, not business rivalry

Only the accepted Step06 curated registry may authorize a domain. External
competitor tools and analyst intuition may not add domains in Step07.

### 4.2 Two host-scope classes

- Broad marketplaces, encyclopedias and dictionaries use
  `EVIDENCE_ANCHORED_RELEVANT_SUBTREE`.
- Specialized commercial/thematic sites use
  `THEME_SCOPED_PUBLIC_TAXONOMY`.

This avoids both extremes: arbitrary page samples and impossible whole-domain
crawls of general-purpose platforms.

### 4.3 Full-volume means frontier exhaustion, not “all URLs on the Internet”

Coverage is complete only after every discovered in-scope URL is terminally
classified. If the bounded universe exceeds one execution window, it is split
into deterministic complete chunks. Sampling remains forbidden.

### 4.4 Provenance is many-to-many

One normalized candidate can occur on many URLs and domains. Deduplication
creates one candidate summary but never deletes occurrence provenance.
Independent competitor occurrences remain measurable as source diversity, not
as search demand.

### 4.5 Bias controls

To reduce competitor-copy bias:

1. preserve every source and competitor class;
2. keep branded wording distinct from generic derived wording;
3. reconcile against all accepted upstream identities before calling a row
   new;
4. do not promote a candidate because one competitor repeats it heavily;
5. retain `POSSIBLE_VARIANT` instead of forcing synonym merges;
6. keep collision-dependent registrants under explicit ambiguity review;
7. require Step08 validation before any demand claim;
8. forbid final intent/page decisions in Step07.

---

## 5. Rejected or constrained practices

| Practice | Decision | Reason |
|---|---|---|
| Add competitors from an external SEO tool | REJECT | Violates Step06 authority and can confuse business competitors with search competitors. |
| Inspect “top pages” or a fixed representative sample | REJECT | Cannot prove bounded full-volume coverage. |
| Crawl an entire general marketplace or encyclopedia | REJECT | Scope is effectively unbounded and mostly irrelevant; use evidence-anchored relevant subtrees. |
| Treat sitemap membership as canonical or relevant truth | REJECT | Sitemap is discovery evidence only. |
| Trust `rel=canonical` without retaining conflicts | REJECT | Canonical is a signal, not infallible proof. |
| Generate every faceted parameter combination | REJECT | Creates artificial/infinite URL space and unnecessary site load. |
| Bypass robots, login, CAPTCHA or anti-bot protection | REJECT | Outside legitimate public-access scope. |
| NFKC/lemmatize/synonym-collapse all candidate text | REJECT | Can erase semantically material distinctions. |
| Assign historical demand from phrase A to transformed phrase B | REJECT | Breaks evidence identity; Step08 must validate the actual candidate wording. |
| Infer production page architecture from competitor taxonomy | REJECT | Step07 discovers candidates only; final intent/clustering/page design are later stages. |

---

## 6. Resulting Step07 preparation decisions

The research changed or confirmed the prepared contract as follows:

- explicit two-class host-scope policy;
- sitemap/navigation/Step06 URL frontier instead of arbitrary top-N;
- one terminal state for every discovered URL;
- conservative canonicalization with raw/declared/computed URL separation;
- deterministic facet, pagination, redirect, region and language handling;
- robots/auth/CAPTCHA/dynamic limitations as coverage evidence;
- Unicode NFC and explicit transformations;
- candidate-summary plus occurrence-provenance model;
- strict Step08 demand boundary;
- `INCOMPLETE` when unresolved coverage prevents an honest completion claim.

No external source was used to overwrite current KW-002 authority, competitor
membership, accepted counts or project state.

---

## 7. Snapshot statement

This audit records methodology sources as accessed on 2026-09-17. External
documentation can change. Actual Step07 must re-fetch the repository base and
refresh any materially unstable access/crawl rule before execution.

```text
STEP07_PREPARATION_EXTERNAL_RESEARCH = COMPLETE
EXTERNAL_METHOD_REPLACED_PROJECT_AUTHORITY = false
PROVIDER_ACQUISITION_PERFORMED = false
STEP07_EXECUTED = false
```
