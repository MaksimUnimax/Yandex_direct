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

## 2. Mandatory fields for every card

For every new card preserve:

```text
case id
marketplace / category / service type
listed price
whether price is exact or "from"
listed unit price when present
service volume
advertised deadline
seller's stated usual completion time when present
seller rating / completed orders when supplied
order-specific review count when supplied
client inputs
promised deliverables
end-to-end verdict = YES / PARTIAL / NO
current Bridge/ChatGPT coverage
exact execution workflow
missing Bridge capability
missing external provider/access/data
manual work remaining
commercial/operational constraints
reusable capability signals
```

Never invent a missing price or duration. If it is absent from the supplied card and cannot be verified, record `UNKNOWN` and update it when evidence appears.

## 3. Verdict rules

```text
YES
= we can accept the order now and return the promised final deliverable end-to-end.

PARTIAL
= substantial parts are possible, but at least one required provider/data/workflow is missing for the exact advertised service.

NO
= the core required data/action is unavailable with the current system.
```

Do not mark a card `YES` merely because an API call exists. `YES` means we can go from the client's inputs to the final artifact they paid for.

## 4. Market-pricing methodology

Do not average unrelated services together.

Pricing analysis must group comparable cards by:

```text
service family
scope/volume
included data providers
included analysis depth
included artifact/report complexity
manual-work share
```

For comparable groups, once there is enough evidence, calculate:

```text
sample count
minimum / maximum
median listed price
25th–75th percentile when useful
median advertised deadline
median stated actual completion when available
normalized price per unit (per 100 keywords / per niche / per site / per report)
```

Our eventual price should then be based on:

```text
market median/range
+ provider/API cost
+ expected operator/ChatGPT time
+ artifact/report complexity
+ revision/risk buffer
+ desired margin
```

A very cheap card with weak scope and an expensive expert analysis are not treated as the same product simply because both mention "semantic core".

---

# 5. MARKET SNAPSHOT

| Case | Service | Listed price | Unit / volume | Deadline | Usual completion | Seller signal |
|---|---|---:|---|---:|---|---|
| F-001 | Yandex + Google rank tracking | 500 ₽ | up to 500 keywords; displayed add-on 100 ₽/quantity block | 1 day | usually 2 hours | 5.0; 412 completed; 7 positive order reviews shown |
| F-002 | Detailed SEO semantic core | 45,000 ₽ | up to 10,000 keywords; derived 450 ₽/100 keywords | 30 days | usually 5 days | 4.9; 235 completed; 2 positive order reviews shown |
| F-003 | Ahrefs-based semantic core + clustering | from 2,500 ₽ | 10,000 keywords; listing also shows 25 ₽/100 keywords | 7 days | not supplied | 5.0; 220 completed; 11 positive / 0 negative for this kwork |
| F-004 | Niche analysis for a website | **UNKNOWN — price absent from supplied capture** | 1 niche / 1 region | 10 days | not supplied | 5.0; 220 completed; no reviews for this kwork |

Notes:
- `derived` unit prices are calculations from listed price/volume, not necessarily the seller's advertised unit tariff.
- F-001, F-002, F-003 and F-004 are not directly interchangeable products; do not take a single median across all four.

---

# 6. LIVE SELLABLE SERVICE COVERAGE

## READY NOW

| Case | Sellable service | Supported boundary | Execution |
|---|---|---|---|
| F-002 | SEO semantic core / keyword collection, up to 10,000 phrases | **Yandex Wordstat-based** collection. Google keyword-volume data is not promised. Base service does not include full automatic clustering. | Wordstat seed expansion → merge/deduplicate → intent filtering/tagging → XLSX/CSV |
| F-004 variant | Yandex-based niche demand/seasonality + limited competitor analysis | Sell as our own explicitly bounded methodology: Yandex Wordstat + Yandex SERP + public/manual review of up to 3 competitors. Do **not** promise Ahrefs/Google Keyword Planner/backlink metrics. | Wordstat cluster/dynamics → Yandex SERP competitor discovery → public competitor review → averages/scoring → report + XLSX + chart |

## PARTIALLY COVERED

| Case | Exact advertised service | What we already cover | Main blocker |
|---|---|---|---|
| F-001 | Rank tracking in Yandex + Google, up to 500 keywords | Yandex SERP/rank extraction + final XLSX | No Google organic SERP provider; no durable bulk rank-check job |
| F-003 | Ahrefs-based semantic core + clustering, up to 10,000 phrases / competitor research | Wordstat collection, Yandex SERP research, deduplication, semantic/intent clustering, spreadsheet/report production | No Ahrefs data source/provider for KD, Traffic Potential, Clicks and Ahrefs competitor datasets |
| F-004 | Full niche analysis matching supplied seller example | Demand, 12-month dynamics, seasonality, competitor discovery, public-content analysis, averages, score/recommendations, report artifacts | No Ahrefs/SEO-metrics provider; no robust competitor crawler/landing-page inventory; no productized search-visibility batch workflow |

## NOT COVERED

```text
None recorded yet.
```

---

# 7. DEMAND-DERIVED CAPABILITY BACKLOG

This is not automatically an implementation roadmap. Repeated appearance across independent paid cards raises priority.

| Capability | Cases | Current state | Market signal |
|---|---|---|---|
| Bulk SERP / Rank Tracker orchestration | F-001, F-004 | Missing | **HIGH — repeated** |
| Google organic SERP provider | F-001 | Missing | HIGH |
| Yandex high-volume/deferred Search workflow | F-001, F-004 | Deferred from Phase 2 | **HIGH — repeated** |
| Semantic Core Builder / Wordstat batch orchestration | F-002, F-003, F-004 | Can be orchestrated now; no dedicated batch job | **VERY HIGH — repeated 3x** |
| Seed expansion + deduplication + checkpoint/resume | F-002, F-003, F-004 | Operationally possible; not productized | **VERY HIGH — repeated 3x** |
| Semantic clustering / intent grouping | F-002, F-003, F-004 | ChatGPT can perform it; no durable large-dataset clustering workflow | **VERY HIGH — repeated 3x** |
| Reusable XLSX/CSV/report builder | F-001, F-002, F-003, F-004 | Available through artifact tooling; not a Bridge workflow | **VERY HIGH reuse** |
| Ahrefs / external SEO-metrics access or import layer | F-003, F-004 | Missing | **HIGH — repeated** |
| Competitor keyword/domain research workflow | F-003, F-004 | Partial via Yandex SERP; no external competitor corpus | **HIGH — repeated** |
| Public competitor site crawl / structure inventory | F-004 | Missing as durable governed workflow | HIGH candidate |
| Niche-analysis scoring/report workflow | F-004 | Can be assembled manually by ChatGPT; not productized | HIGH candidate |

---

# 8. CASE RECORDS

## F-001 — Rank tracking in Yandex and Google, up to 500 keywords

**Marketplace:** Kwork  
**Verdict:** `PARTIAL`

### Market data

```text
listed price = 500 ₽
volume = up to 500 keywords
advertised deadline = 1 day
seller stated usual completion = 2 hours
seller = 5.0 rating / 412 completed orders
```

### Client gives

```text
- target site URL/domain
- target region
- up to 500 keyword queries
```

### Client expects

```text
- Yandex organic position to depth 100
- Google organic position to depth 50
- Excel summary: query | Google | Yandex
```

### Current coverage

```text
Yandex one-key top-100 acquisition = YES
Yandex domain match / rank extraction = YES
XLSX generation = YES
Google rank acquisition = NO
500-key durable batch workflow = NOT PRODUCTIZED
```

### Missing

```text
Google ordinary organic SERP provider
+ durable bulk rank-check queue/checkpoint/resume
+ preferably deferred/high-volume Yandex Search
```

---

## F-002 — Detailed SEO semantic core for a website, up to 10,000 keywords

**Marketplace:** Kwork  
**Verdict:** `YES — WITH YANDEX WORDSTAT AS DATA SOURCE`

### Market data

```text
listed price = 45,000 ₽
volume = up to 10,000 keywords
derived normalization = 450 ₽ / 100 keywords
advertised deadline = 30 days
seller stated usual completion = 5 days
seller = 4.9 rating / 235 completed orders
```

### Current execution

```text
client topic + region + desired intent
→ build seed map
→ repeated explicit WORDSTAT_API_V1 getTop requests (up to 2000 phrases per seed)
→ persist results/checkpoints
→ merge + deduplicate
→ expand uncovered semantic branches
→ intent filtering/tagging
→ XLSX/CSV
```

### Boundary

Do not promise Google keyword-volume data under current product. Do not pad narrow niches to an artificial 10,000 irrelevant phrases.

---

## F-003 — Ahrefs-based semantic core + clustering, up to 10,000 keywords

**Marketplace:** Kwork  
**Verdict:** `PARTIAL`

### Market data

```text
listed price = from 2,500 ₽
listing normalized price shown = 25 ₽ / 100 keywords
volume = up to 10,000 keywords
advertised deadline = 7 days
seller = 5.0 rating / 220 completed orders
order-specific reviews = 11 positive / 0 negative
```

### Exact advertised data

```text
Ahrefs Search Volume
Keyword Difficulty (KD)
Traffic Potential
Clicks
competitor-domain datasets, potentially up to 100 domains
clustering/report output
```

### Current coverage

```text
Wordstat keyword collection = YES
Yandex SERP competitor discovery = YES
semantic/intent clustering = YES
XLSX/report production = YES
Ahrefs KD / Traffic Potential / Clicks / competitor corpus = NO
```

### Unlock path

If the client supplies an Ahrefs export, analysis and clustering can be completed now. For a fully autonomous service we need an accepted Ahrefs/API/import/provider layer.

---

## F-004 — Niche analysis for a website

**Marketplace:** Kwork  
**Category:** SEO / analytics / market analysis  
**Verdict for exact seller-equivalent service:** `PARTIAL`  
**Verdict for a clearly bounded Yandex-only variant:** `YES`

### Market data

```text
listed price = UNKNOWN (not present in supplied capture and not independently verified)
volume = 1 niche / 1 region
advertised deadline = 10 days
seller stated usual completion = not supplied
seller = 5.0 rating / 220 completed orders
order-specific reviews = none
```

### Client gives

```text
- product/service name
- promotion region
- existing site URL if any
- target audience / offer specifics if available
```

### Promised deliverables

```text
- one target semantic cluster
- cluster frequency and demand dynamics
- 12-month seasonality
- up to 3 main competitors
- competitor comparison: structure, landing pages, assortment/services, content, search visibility and other available metrics
- niche averages
- difficulty score 1..10
- launch/promotion recommendations
- PDF/DOCX report
- XLSX/Google Sheets keyword table
- seasonality chart
- competitor list with comments
- risks
```

### What the supplied real example actually contains

The supplied DOCX names these sources:

```text
Yandex Wordstat
Google Keyword Planner
pr-cy.ru
Yandex competitor analysis
Ahrefs
```

The supplied XLSX has four sheets:

```text
СЯ - Газон                 39 rows × 3 columns
Анализ - Газон             17 rows × 6 columns
Утеплитель                 1978 rows × 3 columns
Анализ - Утеплитель        16 rows × 9 columns
```

Keyword sheets contain phrase + Yandex Wordstat-like/Yandex-Direct-like numeric demand columns.

Competitor sheets calculate averages across competitors for metrics including:

```text
Yandex IKS
Ahrefs traffic
Ahrefs DR
unique referring domains
backlinks / dofollow / nofollow
organic keywords
pages in Ahrefs
site age
product-card count
social presence
blog presence
site specialization
```

In the insulation example, seven competitor sites are averaged before the written report assigns a high difficulty score.

### What current Bridge/ChatGPT can already do

```text
1 target semantic cluster = YES
regional Wordstat frequency = YES
12-month demand dynamics / seasonality = YES (Wordstat getDynamics)
seasonality chart = YES
up to 3 Yandex competitors from focus queries = YES (SEARCH_API_V1)
manual/public review of competitor structure, assortment, content, blog/social presence = YES, but not productized
basic Yandex search visibility checks for selected cluster queries = YES, but not bulk-productized
average calculations = YES for whatever metrics we actually collect
difficulty score 1..10 = YES if methodology is explicit and based only on observed metrics
recommendations = YES
PDF/DOCX + XLSX + charts = YES
```

### What prevents exact seller-equivalent coverage

```text
Ahrefs DR / backlink / traffic / organic-keyword / indexed-page metrics = NO PROVIDER
Google Keyword Planner data = NO GOVERNED PROVIDER IN BRIDGE
robust landing-page/site-structure inventory = NO DURABLE CRAWLER
large repeatable search-visibility measurement = NO BULK SERP JOB
```

The seller example derives its conclusion from Ahrefs-style averages. We must not invent equivalent DR/backlink/traffic numbers from Wordstat or Yandex Search.

### Sellable bounded variant we can perform now

We can offer a different but honest service:

```text
"Анализ ниши для SEO на основе Яндекс Wordstat и поисковой выдачи Яндекса"
```

Workflow:

```text
1. Receive niche, region, optional site and target-audience notes.
2. Build one target semantic cluster through Wordstat.
3. Collect current frequency.
4. Collect 12-month dynamics and calculate seasonality.
5. Select 3–5 focus queries from the cluster.
6. Use Yandex Search SERP to identify recurring organic competitors.
7. Select up to 3 main competitors.
8. Review public competitor sites for:
   - offer/category structure;
   - main landing-page types visible from navigation/search;
   - assortment/services;
   - content/blog;
   - commercial elements;
   - social links where visible.
9. Measure bounded Yandex search presence across the selected focus queries.
10. Calculate transparent averages for only the measured signals.
11. Score difficulty 1..10 using a documented rubric, not Ahrefs imitation.
12. Produce recommendations, risks, seasonality chart, XLSX keyword table and DOCX/PDF report.
```

### Capability signal

F-004 strongly reinforces two missing capabilities already seen in F-003:

```text
external SEO-metrics provider/import = HIGH — repeated
competitor research workflow = HIGH — repeated
```

It also creates a new strong candidate product workflow:

```text
NICHE ANALYSIS BUILDER
Wordstat demand + dynamics
→ semantic cluster
→ SERP competitor discovery
→ competitor-site evidence
→ scoring
→ report artifacts
```

---

# 9. HOW THIS WILL BE USED LATER

After a broader sample of cards, derive:

```text
A. SELLABLE SERVICE CATALOG
   only services/verifiable bounded variants we can complete end-to-end

B. MARKET PRICE BOOK
   comparable-card groups with price/volume/deadline statistics

C. NEAR-TERM PRODUCT ROADMAP
   repeated missing capabilities that convert PARTIAL/NO into YES

D. STANDARD OPERATING PROCEDURES
   exact step-by-step execution for each sellable service
```

Target operating map:

```text
freelance service
→ market price range
→ expected deadline
→ required client inputs
→ exact Bridge/API actions
→ analysis steps
→ final artifact
→ provider/API cost
→ operator time
→ risks/revisions
→ our recommended listing price
```
