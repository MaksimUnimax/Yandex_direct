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

`YES` is about the paid final deliverable, not merely existence of one API call.

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
| F-008 | Technical + SEO audit of one website | 2,000 ₽ — cross-card evidence from same seller listing | 1 site; PDF + Excel appendices; optional Keys.so organic export | 10 days | not supplied | 5.0; 798 completed; 1 positive / 0 negative for this kwork |
| **F-009** | **Technical SEO audit + 2-page desktop usability bonus** | **3,000 ₽ — cross-card evidence from prior Kwork recommendation for this exact listing** | **all pages of 1 site + 2 usability pages** | **3 days** | not supplied | **5.0; 1,104 completed; 25 positive / 0 negative for this kwork** |

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

`n=2` confirms paid demand but is still too small for a market median. The two packages also differ materially in provider/tooling and manual usability work.

---

# 7. LIVE SELLABLE SERVICE COVERAGE

## READY NOW

| Case | Sellable service | Supported boundary | Execution |
|---|---|---|---|
| F-002 | SEO semantic core / keyword collection | Yandex Wordstat-based; no Google-volume promise | seeds → Wordstat → merge/dedupe → intent work → XLSX/CSV |
| F-004 variant | Yandex-based niche demand/seasonality + limited competitor analysis | Wordstat + Yandex SERP + public review; no Ahrefs/GKP metrics | demand/dynamics → competitors → review/scoring → report/XLSX/chart |
| F-006 | Semantic core for Yandex Direct: 100 keywords + base frequency + minus-words | URL + geotargeting; Direct mutation not required | offer → Wordstat → filtering → groups → frequency → minus-words → XLSX |
| F-007 | Grouped semantic core for Yandex Direct, up to 500 final keywords | product/service + seed queries + URL + target region | offer → Wordstat → dedupe/clean → ВЧ/СЧ/НЧ → groups → XLSX |

## PARTIALLY COVERED

| Case | Exact advertised service | What works now | Main blocker |
|---|---|---|---|
| F-001 | Yandex + Google rank tracking, up to 500 keywords | Yandex rank extraction + XLSX | no Google organic SERP provider; no bulk rank job |
| F-003 | Ahrefs-based semantic core + clustering | Wordstat, Yandex SERP, clustering, artifacts | no Ahrefs data source |
| F-004 | Full seller-equivalent niche analysis | demand, seasonality, Yandex competitors, reports | no Ahrefs/SEO-metrics provider; no durable competitor crawler |
| F-005 | Up to 10,000 supplied keywords with exact `!` Wordstat frequency for 2025 | current operator query per key + XLSX/zero filtering | no 10k durable batch; quota economics unverified; historical Dynamics cannot reproduce full `!` semantics |
| F-008 | Seller-equivalent technical + SEO site audit with full crawl + Excel appendices + optional Keys.so organic export | Yandex Webmaster/Metrika/Search analysis, public/manual page review, recommendations and PDF/XLSX generation | no full-site technical crawler/inventory; no Keys.so provider; no durable crawl-error dataset/report workflow |
| **F-009** | **70-point technical SEO audit of all pages + prioritized fixes + 2-page usability review** | **Yandex Webmaster/Metrika/Search context, analysis/recommendations and artifact generation; bounded manual page review** | **no autonomous all-page crawler/checklist engine; no dedicated performance/HTML/structured-data inspection layer; usability review not productized** |

## NOT COVERED

None recorded yet.

---

# 8. DEMAND-DERIVED CAPABILITY BACKLOG

| Capability | Cases | Current state | Market signal |
|---|---|---|---|
| **Wordstat-based keyword processing** | F-002..F-007 except F-001 | core provider path exists | **VERY HIGH — repeated across 6 unique cases** |
| **Wordstat batch orchestration / durable queue** | F-002, F-003, F-004, F-005; reinforced by larger F-006/F-007 scopes | no dedicated batch job | **VERY HIGH — repeated** |
| **Advertising Semantic Core Builder** | F-006, F-007 | end-to-end feasible now; not productized as one workflow | **VERY HIGH — repeated across independent sellers** |
| **Commercial relevance cleaning + logical ad grouping** | F-006, F-007 | ChatGPT can do it; not productized | **VERY HIGH — repeated paid deliverable** |
| **Semantic clustering / intent grouping** | F-002, F-003, F-004, F-006, F-007 | feasible; no durable large-dataset workflow | **VERY HIGH — repeated 5x** |
| **Reusable XLSX/CSV/PDF/report builder** | F-001..F-009 | artifact tooling available; not Bridge workflow | **VERY HIGH reuse** |
| **Keyword normalization / dedupe / checkpoint-resume** | F-002..F-007 large scopes | operationally possible in parts | **VERY HIGH reuse** |
| **Full-site crawler / technical SEO inventory** | **F-008, F-009; overlaps competitor-crawl need in F-004** | **missing** | **VERY HIGH — repeated across 2 independent paid audit listings** |
| **Crawler-export importer (Netpeak/Screaming Frog-class datasets)** | **F-008, useful for F-009** | **missing dedicated workflow** | **HIGH — quickest path to external-tool compatibility** |
| **Technical SEO rules + prioritization/report workflow** | **F-008, F-009** | manual/ChatGPT analysis possible if crawl data supplied | **VERY HIGH — repeated paid deliverable** |
| **Performance / HTML / structured-data audit layer** | **F-008, F-009** | partial/manual only | **HIGH — repeated technical-audit need** |
| **Usability / commercial-factor page review** | **F-009** | manual reasoning possible; no governed reusable workflow | **HIGH candidate — explicit paid bonus and adjacent market family** |
| **Keys.so / external organic-visibility provider or importer** | **F-008** | **missing** | **HIGH candidate — explicit paid deliverable** |
| Bulk Wordstat Frequency Checker | F-005 | missing | HIGH — direct paid workflow |
| ВЧ/СЧ/НЧ classification | F-007 | feasible from frequencies | HIGH candidate |
| Minus-word builder | F-006 | feasible with ChatGPT | HIGH — direct paid deliverable |
| Bulk SERP / Rank Tracker orchestration | F-001, F-004 | missing | HIGH — repeated |
| Google organic SERP provider | F-001 | missing | HIGH |
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
Current: Yandex single-key rank/domain match + XLSX = YES.
Missing: Google SERP provider + durable bulk rank queue/checkpoint/resume.
```

Repeated submission of the same card was recognized as a duplicate and was not assigned a second F-id.

## F-002 — Detailed SEO semantic core, up to 10,000 keywords

**Verdict:** `YES — WITH YANDEX WORDSTAT AS DATA SOURCE`

```text
Market: 45,000 ₽; up to 10,000; 30 days; usually 5 days.
Input: topic + region + commercial/informational intent.
Workflow: seed map → Wordstat getTop → persist → merge/dedupe → expand branches → intent filter/tag → XLSX/CSV.
Boundary: no Google-volume promise; do not pad narrow niches with irrelevant keys.
```

## F-003 — Ahrefs-based semantic core + clustering

**Verdict:** `PARTIAL`

```text
Market: from 2,500 ₽; 25 ₽/100 displayed; up to 10,000; 7 days.
Promise: Ahrefs Search Volume, KD, Traffic Potential, Clicks, competitor data, clustering.
Current: Wordstat + Yandex SERP + semantic/intent clustering + artifacts = YES.
Missing: Ahrefs provider.
If client supplies Ahrefs export, analysis/clustering can be completed now.
```

## F-004 — Niche analysis for a website

**Exact seller-equivalent verdict:** `PARTIAL`  
**Bounded Yandex-only variant:** `YES`

```text
Market: price UNKNOWN; 1 niche / 1 region; 10 days.
Input: niche/product, region, optional site, audience/offer notes.
Promise: semantic cluster, frequency/dynamics, 12-month seasonality, competitors,
site comparison, niche averages, difficulty 1..10, recommendations,
DOCX/PDF + XLSX + chart.
```

Current bounded workflow: Wordstat current/dynamics → seasonality → Yandex SERP competitors → public review → transparent difficulty rubric → recommendations/artifacts. Seller-equivalent Ahrefs metrics are unavailable.

## F-005 — Wordstat exact-frequency check, up to 10,000 supplied keywords

**Verdict:** `PARTIAL`

```text
Market: from 4,500 ₽; 45 ₽/100; up to 10,000; one region; 7 days.
Input: ready keyword list + region.
Promise: exact `!` frequency, wording claims 2025, zero-frequency rows removed.
Demo: 5,267 keyword rows; main columns = keyword + `!` YW; no zero rows observed.
Current: one current operator-frequency check + region + XLSX + zero filtering = YES.
Missing: durable 10k batch, proven quota/economics, historical exact-`!` semantics.
```

Future products must separate:

```text
A. current exact-operator frequency;
B. historical Dynamics with only operators actually supported there.
```

## F-006 — Semantic core for Yandex Direct advertising, 100-key base

**Verdict:** `YES — READY NOW`

```text
Market: from 1,500 ₽; 100 keys; 1,500 ₽/100; 2 days.
Input: advertised product/service URL + geotargeting.
Output: Wordstat-based grouped keyword workbook + base frequency + minus-words.
Demo: 17 sheets; 15 thematic sheets + contents + minus-words;
1,206 phrase-frequency records, 1,204 unique phrases, 290 unique minus-words.
```

Pricing boundary: demo size is much larger than the advertised base package and must not be treated as included in 1,500 ₽.

Workflow: inspect offer → seeds → Wordstat → merge/dedupe → commercial/relevance cleaning → thematic groups → frequency → minus-words → contracted final volume → XLSX QA.

## F-007 — Grouped semantic core for Yandex Direct, up to 500 keys

**Verdict:** `YES — READY NOW`

```text
Market: from 4,000 ₽; up to 500; 800 ₽/100; 10 days.
Seller uses Wordstat + Key Collector, but Key Collector is not part of the promised client data contract.
Input: 2–3 seed requests per product/service + description + site URL; our workflow must confirm region.
Output: manually/semantically cleaned, logically grouped ВЧ/СЧ/НЧ keyword set in XLSX.
```

Workflow: offer research → regional Wordstat → dedupe → reject noise/wrong intent/geo → frequency-based ВЧ/СЧ/НЧ → logical ad groups → up to 500 final keys → XLSX QA.

## F-008 — Technical and SEO audit of one website

**Marketplace:** Kwork  
**Title:** `Технический и СЕО аудит сайта`  
**Verdict:** `PARTIAL`

### Market data

```text
listed price = 2,000 ₽ (cross-card evidence from the same seller's Kwork listing)
volume = audit of 1 website
advertised deadline = 10 days
seller = 5.0 / 798 completed orders
order-specific reviews = 1 positive / 0 negative
```

### Client gives

```text
1. website URL
```

The advertised service does not require the client to provide Yandex Webmaster/Metrika access, crawler exports or Keys.so exports.

### Advertised deliverable

```text
- PDF report describing current technical/SEO state;
- sequential list of discovered errors;
- Excel appendices with detail;
- Keys.so organic-search export when data exists.
```

### Owner-supplied demo PDF evidence

The supplied 25-page demo is a technical crawler report for `maevka27.com`, dated 2025-07-06. It is not merely a Webmaster summary.

Observed crawl/report scope includes:

```text
scanned URLs = 576
important-error URLs = 555 (96%) in summary
non-2xx = 156 (27%)
non-indexable HTML = 156 (27%)
large response-time flag = 550 URLs (95%)
duplicate content = 6
image problems = 399 URLs (69%)
```

It covers, among other things:

```text
URL structure and depth;
HTTP response codes and redirects;
indexability;
Meta Robots / X-Robots-Tag;
canonical usage;
server response time;
HTTP/HTTPS and mixed-content checks;
Title / Description / H1 uniqueness, presence and length;
content size and word counts;
image sizes / alt-related errors;
internal-link and PageRank-style graph issues;
broken links and malformed URLs;
criticality-ranked error lists.
```

The report identifies Netpeak Spider as the crawl engine and records `576/576` URLs scanned, `49/77` selected parameters and JavaScript rendering disabled for that run.

The final page adds human recommendations: investigate indexation/sitemap/Webmaster, optimize meta tags, fix duplicate meta tags and broken links, add image alt attributes, improve server response time, further promote popular pages, and perform additional Yandex Metrika/site analytics.

### What current Bridge can contribute now

```text
Yandex Webmaster account/site data = YES where client grants access
Yandex index/search diagnostic context = YES within current Webmaster scope
Yandex Metrika traffic/behavior context = YES where client grants access
Yandex Search/SERP checks = YES
manual/public review of representative pages = YES
analysis/prioritization/recommendations = YES
PDF/XLSX artifact construction = YES
```

These capabilities make a strong Yandex-connected SEO-analysis layer, but they do not produce the same underlying full-site crawl dataset from only a public URL.

### Why exact advertised coverage is not ready

1. **No full-site crawler.** The Bridge does not currently enumerate every discoverable URL and calculate HTTP status, redirect chains, canonical/meta-robots state, internal-link graph/depth, content/meta duplication, image attributes/sizes and response timing across hundreds/thousands of URLs.
2. **No crawler error dataset lifecycle.** There is no durable `site audit job` with per-URL checkpoints, normalized issue types, severity, affected-URL inventory and deterministic Excel appendices.
3. **No Keys.so source.** The advertised optional organic export is provider-specific and cannot be inferred from Webmaster/Search data.
4. **One-URL input matters.** Requiring the client to provide Netpeak/Screaming Frog or Keys.so exports would be a different service contract from the advertised card.

### What can be sold now as a bounded variant

If the client grants Yandex access, a separate honest product can already be offered:

```text
"SEO-анализ сайта по данным Яндекс Вебмастера, Метрики и поисковой выдачи
с выводами и рекомендациями."
```

That must not be described as a complete Netpeak/Screaming-Frog-class technical crawl.

If a client supplies an existing Netpeak/Screaming Frog crawl export, ChatGPT can already analyze, prioritize and convert the dataset into a report; the missing piece then becomes a reusable import/normalization workflow rather than crawl acquisition.

### Required capabilities to turn F-008 into READY

```text
SITE CRAWLER / TECHNICAL SEO AUDIT ENGINE

input:
  start URL/domain
  crawl limits/policies

acquisition:
  crawl URLs
  → HTTP/redirect state
  → canonical/robots/indexability
  → internal link graph/depth
  → title/description/H1
  → content/duplicate signals
  → image/alt/size signals
  → response timing

processing:
  normalize per-URL dataset
  → classify issues
  → severity/prioritization
  → checkpoint/resume
  → affected-URL lists
  → aggregate summary
  → deterministic XLSX appendices
  → PDF/DOCX conclusions/recommendations
```

Parallel external-data option:

```text
KEYS.SO PROVIDER OR IMPORTER
→ organic keywords / visibility data where commercially justified.
```

A lower-cost first implementation path is likely:

```text
CRAWLER EXPORT IMPORTER
(Netpeak / Screaming Frog-class CSV/XLSX)
→ normalized audit dataset
→ ChatGPT analysis/prioritization
→ client report
```

before building our own crawler from scratch. This still would not make the one-URL seller-equivalent service fully autonomous, but it would open audit work when a crawl export is available.

## F-009 — Technical SEO optimization audit + usability bonus

**Marketplace:** Kwork  
**Title:** `Аудит технической SEO оптимизации + бонус`  
**Verdict:** `PARTIAL`

### Market data

```text
listed price = 3,000 ₽ (cross-card evidence from the exact listing shown in the prior Kwork recommendation block)
volume = technical SEO check of all pages of 1 site + usability review of 2 desktop pages
advertised deadline = 3 days
seller = 5.0 / 1,104 completed orders
order-specific reviews = 25 positive / 0 negative
```

### Client gives

```text
required:
- website URL

optional:
- target audience
- special recommendations/context
- 2 specific URLs for the usability bonus
```

If robot protection blocks scanning, the seller explicitly changes/cancels the scope; this confirms that machine-readable all-site access is fundamental to the service.

### Advertised deliverable

```text
- technical SEO audit against an up-to-date checklist;
- commercial-factor checks;
- prioritized discovered errors;
- recommendations for fixing them;
- bonus usability audit of 2 desktop pages;
- PDF report with screenshots/copyright marks.
```

### Owner-supplied demo PDF evidence

The 4-page demo says the complete checklist has **70 items** and that the example PDF contains only the errors found, not all checks.

Observed technical findings include:

```text
analytics counters;
Yandex directory/business presence;
mobile/desktop speed scores and optimization suggestions;
404 page handling;
robots.txt and indexation exclusions;
missing/duplicate H1 and Title;
broken/HTML-contaminated or missing Description;
Description-length checks;
canonical links pointing to 500 pages;
500-error pages;
missing image alt;
parameterized URL indexation;
structured data;
SERP/snippet recommendations;
internal product-card linking;
out-of-stock product handling;
price/currency presentation.
```

The demo also contains a separate desktop usability section checking:

```text
breadcrumbs;
scroll-to-top control;
hover/cursor feedback on add-to-cart;
footer-link behavior and clickable email;
required-field marking and form-error presentation.
```

The seller states that error priority follows the numbering in the report.

### What current Bridge can contribute now

```text
Yandex Webmaster diagnostics/context = YES where client grants access
Yandex Metrika analytics context = YES where client grants access
Yandex Search/SERP checks = YES
reasoning about technical findings once data exists = YES
priority/recommendation generation = YES
PDF/XLSX/report generation = YES
bounded manual inspection of supplied/public pages = possible
```

### Why exact advertised coverage is not ready

1. **All-page crawl is still missing.** The seller promises checking all pages and explicitly warns that robot protection may block the service. Our Bridge cannot yet enumerate and inspect the complete public site from one URL.
2. **No unified 70-point technical rules engine.** We do not have a deterministic per-URL/site-level checklist engine for status codes, robots, canonical, meta duplication/presence/length, alt, parameterized URLs, internal linking and commercial checks.
3. **No governed speed/performance acquisition.** The demo reports mobile/desktop speed scores and concrete optimization findings, but the Bridge has no dedicated PageSpeed/Lighthouse-class provider/runtime.
4. **No structured-data/HTML validation layer.** These are explicitly promised checks and are not provided by Webmaster/Metrika/Search alone.
5. **Usability bonus is not productized.** ChatGPT can reason about page UX when a page/screenshots/browser evidence are available, but there is no reusable extension workflow that loads two pages, checks interaction states/forms and records screenshot evidence deterministically.

### What can be sold now as a bounded variant

The same bounded Yandex-data audit variant identified for F-008 remains feasible when the client grants Yandex account access. A second bounded service is possible when the client supplies a crawler/export dataset and screenshots/URLs for the usability pages:

```text
crawler export + Yandex Webmaster/Metrika context
→ issue normalization
→ prioritization
→ technical recommendations
→ 2-page manual usability analysis
→ PDF/XLSX report
```

It must not be advertised as an autonomous all-pages 70-point crawl until acquisition is implemented.

### Product consequence

F-009 independently confirms the F-008 signal:

```text
TECHNICAL SEO AUDIT ENGINE
= repeated paid service across independent sellers
= crawler acquisition + normalized rules + prioritization + report artifacts
```

The likely build sequence remains:

```text
1. crawler-export importer
2. normalized technical SEO issue schema/rules/reporting
3. autonomous site crawler
4. performance/HTML/structured-data inspection adapters
5. optional screenshot-aware usability/commercial-factor workflow
```
