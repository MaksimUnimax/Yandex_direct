# FREELANCE ORDER CAPABILITY MATRIX — Yandex Marketing Bridge

Status: **ACTIVE / PERMANENT PRODUCT-DISCOVERY, SERVICE-COVERAGE AND MARKET-PRICING AUTHORITY**  
Started: 2026-08-27

## 1. Purpose

This document converts real freelance-marketplace cards into a practical operating map:

```text
real freelance order
→ market price / deadline / volume
→ required client inputs
→ required final deliverable
→ can we complete it now?
→ exact Bridge/ChatGPT workflow
→ missing capability/provider if not
→ repeated market demand
→ future product priority
→ later: defensible pricing for our own services
```

The target is to derive the sellable service catalog, operating procedures, next product roadmap and pricing from real paid work rather than inventing features or prices in isolation.

This is planning/evidence only. It does not authorize `extension/src` changes. While Phase 5 Direct owner-live is pending, this file remains on the QA branch and the frozen Direct product stays immutable.

## 2. Duplicate-card rule

Duplicate cards are expected and MUST NOT be counted twice in demand or pricing statistics.

Before assigning a new `F-xxx` id, compare, in order:

```text
1. marketplace card URL / numeric listing id when visible;
2. seller + exact service title;
3. seller + same scope/price/description when URL is missing;
4. supplied demo files / same deliverable when useful for confirmation.
```

If the same listing is seen again:

```text
→ keep the original F-id;
→ optionally enrich the existing record with genuinely new evidence;
→ do not create a new market observation;
→ do not increment repeated-demand counters;
→ do not count its price again.
```

Different sellers offering the same service are independent observations and SHOULD be counted separately.

## 3. Mandatory fields for every unique card

Preserve: case id, marketplace/category/service type, listed price and whether exact/from, unit price when present, volume, advertised deadline, usual completion when supplied, seller signal, client inputs, promised deliverables, demo-output evidence, verdict, current coverage, exact workflow, missing Bridge capability, missing external provider/access/data, remaining manual work, commercial constraints and reusable capability signals.

Never invent missing price/duration. Record `UNKNOWN` until evidence appears. Cross-card evidence from the same seller may be recorded only when the title/listing identity is clear and must be labeled as cross-card evidence.

## 4. Verdict rules

```text
YES = can accept now and return the promised final deliverable end-to-end.
PARTIAL = substantial parts work, but exact advertised service still lacks provider/data/workflow.
NO = core required data/action is unavailable.
```

`YES` is about the paid final deliverable, not merely existence of one API call. A card may be `YES` for a clearly bounded configuration (for example Yandex-only) while an optional provider-specific variant remains `PARTIAL`; that boundary must be explicit.

## 5. Market-pricing methodology

Compare only genuinely comparable services by family, volume, provider set, depth, artifact complexity and manual-work share. When the sample becomes large enough, calculate min/max/median, quartiles where useful, median deadlines, stated actual completion and normalized unit prices.

Our eventual price must include:

```text
provider/API cost
+ expected operator/ChatGPT time
+ artifact complexity
+ revision/risk buffer
+ desired margin.
```

---

# 6. MARKET SNAPSHOT — UNIQUE CARDS ONLY

| Case | Service | Listed price | Unit / volume | Deadline | Usual completion | Seller signal |
|---|---|---:|---|---:|---|---|
| F-001 | Yandex + Google rank tracking | 500 ₽ | up to 500 keywords | 1 day | usually 2 hours | 5.0; 412 completed; 7 positive shown |
| F-002 | Detailed SEO semantic core | 45,000 ₽ | up to 10,000; derived 450 ₽/100 | 30 days | usually 5 days | 4.9; 235 completed; 2 positive shown |
| F-003 | Ahrefs semantic core + clustering | from 2,500 ₽ | 10,000; listing also shows 25 ₽/100 | 7 days | not supplied | 5.0; 220 completed; 11 positive / 0 negative |
| F-004 | Niche analysis for a website | UNKNOWN | 1 niche / 1 region | 10 days | not supplied | 5.0; 220 completed; no reviews for this kwork |
| F-005 | Wordstat frequency check for supplied keywords | from 4,500 ₽ | up to 10,000 / 1 region; 45 ₽/100 shown | 7 days | not supplied | 4.9; 235 completed; 1 positive / 0 negative |
| F-006 | Semantic core for Yandex Direct advertising | from 1,500 ₽ | 100 keywords; 1,500 ₽/100 | 2 days | not supplied | 5.0; 742 completed; 41 positive / 0 negative |
| F-007 | Grouped semantic core for Yandex Direct advertising | from 4,000 ₽ | up to 500; 800 ₽/100 shown | 10 days | not supplied | 5.0; 798 completed; 5 positive / 0 negative |
| F-008 | Technical + SEO audit of one website | 2,000 ₽ — cross-card evidence | 1 site; PDF + Excel appendices; optional Keys.so organic export | 10 days | not supplied | 5.0; 798 completed; 1 positive / 0 negative |
| F-009 | Technical SEO audit + 2-page desktop usability bonus | 3,000 ₽ — cross-card evidence | all pages of 1 site + 2 usability pages | 3 days | not supplied | 5.0; 1,104 completed; 25 positive / 0 negative |
| F-010 | Semantic core for a website from scratch / review of existing core | from 5,000 ₽ — cross-card evidence | 100 keywords; 5,000 ₽/100 shown | 5 days | not supplied | 5.0; 59 completed; 1 positive / 0 negative |
| **F-011** | **Filtering an existing semantic core from noise and duplicates** | **from 8,000 ₽; same-page exact-listing evidence** | **up to 5,000 keywords; 160 ₽/100 shown; one search engine / one Yandex region** | **30 days** | not supplied | **4.9; 235 completed; 1 positive / 0 negative** |

Do not calculate one median across unrelated products.

### Comparable slice — advertising semantic core for Yandex Direct

| Case | Base scope | Listed price | Normalized | Deadline | Included depth |
|---|---:|---:|---:|---:|---|
| F-006 | 100 keys | from 1,500 ₽ | 1,500 ₽/100 | 2 days | Wordstat base frequency + thematic groups + minus-words |
| F-007 | up to 500 keys | from 4,000 ₽ | 800 ₽/100 | 10 days | Wordstat/Key Collector collection + cleaning + logical groups + ВЧ/СЧ/НЧ |

`n=2` is not enough to set our final price. Current observed normalized range is **800–1,500 ₽ per 100 keywords** and deliverable depth differs.

### Comparable family — technical SEO audits

| Case | Listed price | Scope | Deadline | Distinguishing depth |
|---|---:|---|---:|---|
| F-008 | 2,000 ₽ cross-card evidence | 1 site | 10 days | Netpeak-style full crawl report + Excel appendices + optional Keys.so |
| F-009 | 3,000 ₽ cross-card evidence | all pages of 1 site + 2 usability pages | 3 days | 70-point technical checklist + prioritized recommendations + usability bonus |

`n=2` confirms paid demand but is still too small for a market median.

### Comparable family — website semantic cores

| Case | Listed price | Scope | Deadline | Distinguishing depth |
|---|---:|---|---:|---|
| F-002 | 45,000 ₽ | up to 10,000 keys | 30 days; usually 5 | detailed Wordstat-based SEO core at high volume |
| F-010 | from 5,000 ₽ cross-card evidence | 100 keys | 5 days | from-scratch core or review of an existing core |

### Standalone semantic-core cleanup

| Case | Listed price | Scope | Deadline | Normalized |
|---|---:|---|---:|---:|
| F-011 | from 8,000 ₽ | up to 5,000 supplied keys | 30 days | 160 ₽/100 shown |

`n=1` is not enough for a market price conclusion, but it proves that cleanup/deduplication itself is sold as a standalone service rather than only as part of collection.

---

# 7. LIVE SELLABLE SERVICE COVERAGE

## READY NOW

| Case | Sellable service | Supported boundary | Execution |
|---|---|---|---|
| F-002 | SEO semantic core / keyword collection | Yandex Wordstat-based; no Google-volume promise | seeds → Wordstat → merge/dedupe → intent work → XLSX/CSV |
| F-004 variant | Yandex-based niche demand/seasonality + limited competitor analysis | Wordstat + Yandex SERP + public review; no Ahrefs/GKP metrics | demand/dynamics → competitors → review/scoring → report/XLSX/chart |
| F-006 | Semantic core for Yandex Direct: 100 keywords + base frequency + minus-words | URL + geotargeting; Direct mutation not required | offer → Wordstat → filtering → groups → frequency → minus-words → XLSX |
| F-007 | Grouped semantic core for Yandex Direct, up to 500 final keywords | product/service + seed queries + URL + target region | offer → Wordstat → dedupe/clean → ВЧ/СЧ/НЧ → groups → XLSX |
| F-010 | Website semantic core, 100 keywords, or review of an existing core | site + target directions; confirm region | site/directions → seeds → Wordstat → clean/dedupe → relevance/intent review → final core |
| **F-011 Yandex scope** | **Cleanup/filtering of supplied semantic core, up to 5,000 keys** | **client supplies core + niche rules/examples; Yandex region can be used for borderline validation** | **import → normalize → exact/semantic dedupe → classify relevance/noise → keep/remove reason → QA → cleaned artifact** |

## PARTIALLY COVERED

| Case | Exact advertised service | What works now | Main blocker |
|---|---|---|---|
| F-001 | Yandex + Google rank tracking, up to 500 keywords | Yandex rank extraction + XLSX | no Google organic SERP provider; no bulk rank job |
| F-003 | Ahrefs-based semantic core + clustering | Wordstat, Yandex SERP, clustering, artifacts | no Ahrefs data source |
| F-004 | Full seller-equivalent niche analysis | demand, seasonality, Yandex competitors, reports | no Ahrefs/SEO-metrics provider; no durable competitor crawler |
| F-005 | Up to 10,000 supplied keywords with exact `!` Wordstat frequency for 2025 | current operator query per key + XLSX/zero filtering | no 10k durable batch; quota economics unverified; historical Dynamics cannot reproduce full `!` semantics |
| F-008 | Seller-equivalent technical + SEO site audit with full crawl + optional Keys.so | Yandex diagnostics, analysis, recommendations, artifacts | no full-site crawler/inventory; no Keys.so provider |
| F-009 | 70-point all-page technical audit + 2-page usability review | Yandex context, analysis, bounded manual page review | no autonomous crawler/rules/performance/HTML/structured-data layer |
| **F-011 Google-specific validation variant** | **Google-specific semantic filtering for Russia if the buyer expects search-engine/SERP validation** | **semantic cleanup itself is feasible** | **no dedicated Google organic SERP/data provider; do not imply Google-specific validation without it** |

## NOT COVERED

None recorded yet.

---

# 8. DEMAND-DERIVED CAPABILITY BACKLOG

| Capability | Cases | Current state | Market signal |
|---|---|---|---|
| **Wordstat-based keyword processing** | F-002, F-003, F-004, F-005, F-006, F-007, F-010 | core provider path exists | **VERY HIGH — repeated across 7 unique cases** |
| **Wordstat batch orchestration / durable queue** | F-002, F-003, F-004, F-005; reinforced by larger F-006/F-007 scopes | no dedicated batch job | **VERY HIGH — repeated** |
| **Website Semantic Core Builder** | F-002, F-010 | end-to-end feasible now; not productized as one workflow | **VERY HIGH — repeated across independent sellers** |
| **Advertising Semantic Core Builder** | F-006, F-007 | end-to-end feasible now; not productized as one workflow | **VERY HIGH — repeated across independent sellers** |
| **Semantic-core cleanup / noise filtering / semantic dedupe** | **F-002, F-006, F-007, F-010, F-011** | **feasible now; F-011 proves it is sellable standalone** | **VERY HIGH — repeated and directly monetized** |
| **Large semantic-dataset processor / checkpoint-resume** | **F-002, F-003, F-005, F-011** | **possible with artifacts/manual orchestration; no dedicated durable job** | **VERY HIGH — repeated large-volume need** |
| **Semantic clustering / intent grouping** | F-002, F-003, F-004, F-006, F-007 | feasible; no durable large-dataset workflow | **VERY HIGH — repeated 5x** |
| **Reusable XLSX/CSV/PDF/report builder** | F-001..F-011 | artifact tooling available; not Bridge workflow | **VERY HIGH reuse** |
| **Full-site crawler / technical SEO inventory** | F-008, F-009; overlaps F-004 competitor crawl | missing | **VERY HIGH — repeated across independent paid audits** |
| **Crawler-export importer** | F-008, useful for F-009 | missing dedicated workflow | **HIGH — quickest audit compatibility path** |
| **Technical SEO rules + prioritization/report workflow** | F-008, F-009 | manual analysis possible if crawl data supplied | **VERY HIGH — repeated paid deliverable** |
| **Performance / HTML / structured-data audit layer** | F-008, F-009 | partial/manual only | **HIGH — repeated** |
| **Usability / commercial-factor page review** | F-009 | manual reasoning possible; no reusable workflow | **HIGH candidate** |
| **Keys.so / external organic-visibility provider or importer** | F-008 | missing | **HIGH candidate** |
| Bulk Wordstat Frequency Checker | F-005 | missing | HIGH — direct paid workflow |
| ВЧ/СЧ/НЧ classification | F-007 | feasible from frequencies | HIGH candidate |
| Minus-word builder | F-006 | feasible with ChatGPT | HIGH — direct paid deliverable |
| Bulk SERP / Rank Tracker orchestration | F-001, F-004 | missing | HIGH — repeated |
| Google organic SERP provider | F-001; optional F-011 Google-specific validation | missing | **HIGH — now useful across multiple service families** |
| Yandex high-volume/deferred Search | F-001, F-004 | deferred from Phase 2 | HIGH — repeated |
| Ahrefs/external SEO metrics | F-003, F-004 | missing | HIGH — repeated |
| Competitor keyword/domain research | F-003, F-004 | partial | HIGH — repeated |
| Public competitor/site crawl + structure inventory | F-004, F-008, F-009 | no durable crawler | **VERY HIGH — repeated** |
| Niche-analysis scoring/report workflow | F-004 | manually feasible | HIGH candidate |

---

# 9. CASE RECORDS

## F-001 — Rank tracking in Yandex and Google, up to 500 keywords

**Verdict:** `PARTIAL`

```text
Market: 500 ₽; up to 500 keywords; 1 day; usually 2 hours.
Input: domain + region + keyword list.
Output: Yandex top-100 + Google top-50 positions in XLSX.
Current: Yandex rank/domain work + XLSX = partial.
Missing: Google SERP provider + durable bulk rank queue/checkpoint/resume.
```

Repeated submission of the same card was recognized as a duplicate and was not assigned a second F-id.

## F-002 — Detailed SEO semantic core, up to 10,000 keywords

**Verdict:** `YES — WITH YANDEX WORDSTAT AS DATA SOURCE`

```text
Market: 45,000 ₽; up to 10,000; 30 days; usually 5 days.
Input: topic + region + commercial/informational intent.
Workflow: seed map → Wordstat → persist → merge/dedupe → expand → intent filter/tag → XLSX/CSV.
Boundary: no Google-volume promise; do not pad narrow niches with irrelevant keys.
```

## F-003 — Ahrefs-based semantic core + clustering

**Verdict:** `PARTIAL`

```text
Market: from 2,500 ₽; 25 ₽/100 shown; up to 10,000; 7 days.
Promise: Ahrefs Search Volume, KD, Traffic Potential, Clicks, competitor data, clustering.
Current: Wordstat + Yandex SERP + clustering + artifacts.
Missing: Ahrefs provider. If client supplies Ahrefs export, analysis/clustering can be completed now.
```

## F-004 — Niche analysis for a website

**Exact seller-equivalent verdict:** `PARTIAL`  
**Bounded Yandex-only variant:** `YES`

```text
Market: price UNKNOWN; 1 niche / 1 region; 10 days.
Input: niche/product, region, optional site, audience/offer notes.
Promise: semantic cluster, frequency/dynamics, 12-month seasonality, competitors,
site comparison, niche averages, difficulty 1..10, recommendations, DOCX/PDF + XLSX + chart.
Current bounded workflow: Wordstat current/dynamics → seasonality → Yandex SERP competitors → public review → transparent scoring → report.
Missing for seller-equivalent depth: Ahrefs/external SEO metrics + durable competitor crawler.
```

## F-005 — Wordstat exact-frequency check, up to 10,000 supplied keywords

**Verdict:** `PARTIAL`

```text
Market: from 4,500 ₽; 45 ₽/100; up to 10,000; one region; 7 days.
Input: ready keyword list + region.
Promise: exact `!` frequency, wording claims 2025, zero-frequency rows removed.
Demo: 5,267 keyword rows; keyword + `!` YW; no zero rows observed.
Current: one current operator-frequency check + region + XLSX + zero filtering.
Missing: durable 10k batch, proven quota/economics, historical exact-`!` semantics.
```

## F-006 — Semantic core for Yandex Direct advertising, 100-key base

**Verdict:** `YES — READY NOW`

```text
Market: from 1,500 ₽; 100 keys; 1,500 ₽/100; 2 days.
Input: advertised product/service URL + geotargeting.
Output: Wordstat-based grouped workbook + base frequency + minus-words.
Demo: 17 sheets; 15 thematic + contents + minus-words; 1,206 phrase-frequency records; 1,204 unique; 290 unique minus-words.
Workflow: offer → seeds → Wordstat → dedupe/clean → groups → frequency → minus-words → XLSX QA.
```

Direct API is not required because the deliverable prepares semantics for advertising but does not mutate an advertising account.

## F-007 — Grouped semantic core for Yandex Direct, up to 500 keys

**Verdict:** `YES — READY NOW`

```text
Market: from 4,000 ₽; up to 500; 800 ₽/100; 10 days.
Seller uses Wordstat + Key Collector; Key Collector is not part of the promised client data contract.
Input: 2–3 seed queries per product/service + description + site URL; our workflow confirms region.
Output: cleaned, logically grouped ВЧ/СЧ/НЧ keyword set in XLSX.
Workflow: offer research → regional Wordstat → dedupe → reject noise/wrong intent/geo → frequency bands → logical groups → XLSX.
```

## F-008 — Technical and SEO audit of one website

**Verdict:** `PARTIAL`

```text
Market: 2,000 ₽ cross-card evidence; 1 site; 10 days.
Promise: PDF state/error report + Excel appendices + optional Keys.so organic export.
Demo: Netpeak-style crawl; 576 URLs; 555 important-error URLs; 156 non-2xx; 156 non-indexable;
550 response-time flags; 6 duplicate-content findings; 399 image-problem URLs; 49/77 selected Netpeak parameters.
```

Current Bridge adds Webmaster/Metrika/Search context, manual/public page review, prioritization and artifact generation. Missing: autonomous full-site crawler, durable per-URL issue dataset and Keys.so provider/importer. Lowest-cost bridge is a Netpeak/Screaming-Frog export importer before autonomous crawl acquisition.

## F-009 — Technical SEO optimization audit + usability bonus

**Verdict:** `PARTIAL`

```text
Market: 3,000 ₽ cross-card evidence; all pages of 1 site + 2 usability pages; 3 days.
Seller demo: 70-item complete checklist; example shows only discovered errors.
Checks include speed, 404/500, robots, H1/Title/Description, canonical, alt, parameter URLs,
structured data, internal linking and commercial factors; usability bonus covers breadcrumbs, controls, footer and forms.
```

Current Yandex data + reasoning/reporting can support analysis, but autonomous all-page crawler/checklist, performance, HTML/structured-data and governed usability acquisition are missing.

## F-010 — Semantic core for a website, 100-key base

**Listing id:** `40987776`  
**Verdict:** `YES — READY NOW`

```text
Market: from 5,000 ₽ cross-card evidence; 100 keywords; 5 days.
Input: website URL + promotion directions; optional existing semantic core.
Our execution additionally confirms target region.
Workflow: inspect offer → seeds → Wordstat → normalize/dedupe → relevance/intent cleaning → optional old-core diff → final 100 keys → artifact.
```

No Ahrefs/Google/Direct/crawler dependency is required by the advertised contract.

## F-011 — Filtering an existing semantic core from noise and duplicates

**Marketplace:** Kwork  
**Listing id:** `10494024`  
**Seller:** `nychkos`  
**Title:** `Фильтрация Вашего семантического ядра от мусорных запросов`  
**Verdict:** `YES — READY NOW FOR YANDEX SCOPE`; optional Google-specific validation is bounded as described below.

### Market data

```text
listed price = from 8,000 ₽
price evidence = exact same listing is shown on the supplied Kwork page with 8,000 ₽ and 160 ₽/100
volume = up to 5,000 supplied keywords
advertised deadline = 30 days
scope wording = price for one search engine and one Yandex region; Google filtering only for Russia
seller = 4.9 / 235 completed orders
order-specific reviews = 1 positive / 0 negative
```

### Client gives

```text
- existing semantic core / keyword dataset;
- clear topic and niche specifics;
- examples of what should remain;
- examples of what should be filtered out;
- target region/search-engine configuration.
```

### Advertised deliverable

A cleaned ready-to-use semantic core with irrelevant/noise queries and duplicates removed, suitable for planning categories, articles, product cards or service pages. The card does not promise Ahrefs metrics, Wordstat frequency acquisition, SERP clustering or another named external dataset.

### Why Yandex scope is ready now

The core job is classification and dataset transformation, not acquisition of a proprietary metric:

```text
supplied keyword file = YES
parse/normalize up to thousands of rows = YES
exact duplicate removal = YES
near/semantic duplicate detection = YES
niche relevance classification = YES
intent classification = YES
keep/remove rules from client examples = YES
Yandex-region spot validation through available Yandex paths when needed = YES
XLSX/CSV output = YES
```

Wordstat is optional here rather than mandatory. The client already supplies the keyword universe. Yandex Search/Wordstat can be used selectively for ambiguous phrases instead of spending provider calls on every row.

### Execution workflow

```text
1. Import the supplied semantic core without destroying original columns.
2. Capture niche description, region and client keep/remove examples.
3. Normalize text for comparison while preserving original phrase text.
4. Remove exact duplicates deterministically.
5. Detect near duplicates / morphological variants / redundant wording.
6. Classify every remaining phrase:
   KEEP
   REMOVE_NOISE
   REMOVE_WRONG_INTENT
   REMOVE_WRONG_PRODUCT
   REMOVE_WRONG_GEO
   REVIEW_AMBIGUOUS
7. Use niche/site/client examples to resolve the first pass.
8. For ambiguous Yandex cases, selectively validate with Yandex data/search rather than blanket-querying 5,000 rows.
9. Produce final cleaned core plus, preferably, a removed/review sheet with reasons for QA and revisions.
10. Run final duplicate/relevance sanity checks and deliver XLSX/CSV.
```

### Google boundary

The card also mentions filtering for Google in Russia. Pure semantic cleanup of a client-supplied list remains possible because it does not inherently require Google data. However, if the buyer expects **Google-specific SERP/search-engine validation** as part of deciding which phrases remain, our current stack has no dedicated Google organic SERP provider. Therefore do not market that stronger Google-specific interpretation until such a provider exists.

### Product consequence

F-011 proves that this reusable component is itself a paid product:

```text
SEMANTIC CORE CLEANER
input file + niche + region + keep/remove examples
→ normalize
→ exact/semantic dedupe
→ relevance + intent classification
→ optional selective Yandex validation
→ cleaned core + removed/review reasons
→ XLSX/CSV
```

This should be reusable inside F-002/F-006/F-007/F-010 and also sellable standalone. The main future improvement is a durable large-dataset job/checkpoint workflow, not a new mandatory provider for the Yandex version.
