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

Preserve for every card: case id, marketplace/category/service type, listed price and whether it is exact/from, unit price when present, volume, advertised deadline, usual completion when supplied, seller signal, client inputs, promised deliverables, verdict, current coverage, exact workflow, missing Bridge capability, missing external provider/access/data, remaining manual work, commercial constraints and reusable capability signals.

Never invent missing price/duration. Record `UNKNOWN` until evidence appears. Duplicate cards are not counted twice in market-demand or pricing statistics.

## 3. Verdict rules

```text
YES = can accept now and return the promised final deliverable end-to-end.
PARTIAL = substantial parts work, but exact advertised service still lacks provider/data/workflow.
NO = core required data/action is unavailable.
```

`YES` is about the paid final deliverable, not merely existence of one API call.

## 4. Market-pricing methodology

Compare only genuinely comparable services by family, volume, provider set, depth, artifact complexity and manual-work share. When the sample becomes large enough, calculate min/max/median, quartiles where useful, median deadlines, stated actual completion and normalized unit prices. Our eventual price must include provider/API cost, expected operator/ChatGPT time, artifact complexity, revision/risk buffer and desired margin.

---

# 5. MARKET SNAPSHOT

| Case | Service | Listed price | Unit / volume | Deadline | Usual completion | Seller signal |
|---|---|---:|---|---:|---|---|
| F-001 | Yandex + Google rank tracking | 500 ₽ | up to 500 keywords | 1 day | usually 2 hours | 5.0; 412 completed; 7 positive reviews shown |
| F-002 | Detailed SEO semantic core | 45,000 ₽ | up to 10,000 keywords; derived 450 ₽/100 | 30 days | usually 5 days | 4.9; 235 completed; 2 positive reviews shown |
| F-003 | Ahrefs semantic core + clustering | from 2,500 ₽ | 10,000 keywords; listing also shows 25 ₽/100 | 7 days | not supplied | 5.0; 220 completed; 11 positive / 0 negative |
| F-004 | Niche analysis for a website | UNKNOWN | 1 niche / 1 region | 10 days | not supplied | 5.0; 220 completed; no reviews for this kwork |
| F-005 | Wordstat frequency check for supplied keywords | from 4,500 ₽ | up to 10,000 keywords / 1 region; 45 ₽/100 shown | 7 days | not supplied | 4.9; 235 completed; 1 positive / 0 negative |
| F-006 | Semantic core for Yandex Direct advertising | from 1,500 ₽ | 100 keywords; 1,500 ₽/100 | 2 days | not supplied | 5.0; 742 completed; 41 positive / 0 negative |
| **F-007** | **Grouped semantic core for Yandex Direct advertising** | **from 4,000 ₽** (same-card cross-listing evidence) | **up to 500 keywords; 800 ₽/100 shown** | **10 days** | not supplied | **5.0; 798 completed; 5 positive / 0 negative** |

Do not calculate one median across unrelated products.

### Preliminary comparable slice — advertising semantic core for Yandex Direct

Current independent-seller sample:

| Case | Base scope | Listed price | Normalized | Deadline | Included depth |
|---|---:|---:|---:|---:|---|
| F-006 | 100 keys | from 1,500 ₽ | 1,500 ₽/100 | 2 days | Wordstat base frequency + thematic groups + minus-words |
| F-007 | up to 500 keys | from 4,000 ₽ | 800 ₽/100 | 10 days | Wordstat/Key Collector collection + manual cleaning + logical grouping + ВЧ/СЧ/НЧ |

`n=2` is not enough to set our final market price. The current observed normalized range is **800–1,500 ₽ per 100 keywords**, but the deliverable depth differs, so this is only an early market signal.

---

# 6. LIVE SELLABLE SERVICE COVERAGE

## READY NOW

| Case | Sellable service | Supported boundary | Execution |
|---|---|---|---|
| F-002 | SEO semantic core / keyword collection | Yandex Wordstat-based collection; no Google keyword-volume promise | Wordstat seed expansion → merge/dedupe → intent work → XLSX/CSV |
| F-004 variant | Yandex-based niche demand/seasonality + limited competitor analysis | Wordstat + Yandex SERP + public/manual review; no Ahrefs/Google Keyword Planner metrics | demand/dynamics → competitors → review/scoring → report/XLSX/chart |
| F-006 | Semantic core for Yandex Direct: 100 keywords + base Wordstat frequency + minus-words | URL + geotargeting; no Direct mutation required | offer → Wordstat → filtering → thematic groups → frequency → minus-words → XLSX |
| **F-007** | **Grouped semantic core for Yandex Direct, up to 500 final keywords** | product/service + seed queries + site URL; our workflow must also confirm target region before collection | offer research → regional Wordstat expansion → dedupe → relevance/intent cleaning → ВЧ/СЧ/НЧ labeling → logical grouping → XLSX |

## PARTIALLY COVERED

| Case | Exact advertised service | What works now | Main blocker |
|---|---|---|---|
| F-001 | Yandex + Google rank tracking, up to 500 keywords | Yandex rank acquisition/extraction + XLSX | no Google organic SERP provider; no bulk rank job |
| F-003 | Ahrefs-based semantic core + clustering | Wordstat, Yandex SERP, clustering, artifacts | no Ahrefs KD/Traffic Potential/Clicks/competitor corpus |
| F-004 | Full seller-equivalent niche analysis | demand, seasonality, Yandex competitors, public analysis, reports | no Ahrefs/SEO-metrics provider; no durable competitor crawler/bulk visibility workflow |
| F-005 | Up to 10,000 supplied keywords with exact `!` Wordstat frequency for 2025 | current operator query per keyword + XLSX/zero filtering | no 10k durable frequency-check batch; quota economics unverified; historical Dynamics does not reproduce full `!` semantics |

## NOT COVERED

None recorded yet.

---

# 7. DEMAND-DERIVED CAPABILITY BACKLOG

| Capability | Cases | Current state | Market signal |
|---|---|---|---|
| **Wordstat-based keyword processing** | F-002, F-003, F-004, F-005, F-006, F-007 | core provider path exists | **VERY HIGH — repeated across 6 cases** |
| **Wordstat batch orchestration / durable queue** | F-002, F-003, F-004, F-005; reinforced by F-006/F-007 larger examples/scopes | no dedicated batch job | **VERY HIGH — repeated** |
| **Advertising Semantic Core Builder** | **F-006, F-007**; overlaps F-002/F-003 | end-to-end feasible now, not productized as one durable workflow | **VERY HIGH — repeated paid workflow across independent sellers** |
| **Commercial relevance cleaning + logical ad grouping** | F-006, F-007 | ChatGPT can do it; not productized | **VERY HIGH — repeated paid deliverable** |
| **ВЧ/СЧ/НЧ classification** | F-007 | feasible from collected frequency data; no dedicated workflow | HIGH candidate |
| **Minus-word / negative-keyword builder** | F-006 | ChatGPT can do it; not productized | HIGH — direct paid deliverable |
| **Bulk Wordstat Frequency Checker** | F-005 | missing | HIGH — direct paid workflow |
| Keyword-set normalization / dedupe / checkpoint-resume | F-002..F-007 large scopes | operationally possible in parts; not productized | **VERY HIGH reuse** |
| Semantic clustering / intent grouping | F-002, F-003, F-004, F-006, F-007 | ChatGPT can perform; no durable large-dataset workflow | **VERY HIGH — repeated 5x** |
| Reusable XLSX/CSV/report builder | F-001..F-007 | artifact tooling available; not Bridge workflow | **VERY HIGH reuse** |
| Bulk SERP / Rank Tracker orchestration | F-001, F-004 | missing | HIGH — repeated |
| Google organic SERP provider | F-001 | missing | HIGH |
| Yandex high-volume/deferred Search | F-001, F-004 | deferred from Phase 2 | HIGH — repeated |
| Ahrefs/external SEO-metrics import/provider | F-003, F-004 | missing | HIGH — repeated |
| Competitor keyword/domain research | F-003, F-004 | partial | HIGH — repeated |
| Public competitor site crawl / structure inventory | F-004 | missing durable workflow | HIGH candidate |
| Niche-analysis scoring/report workflow | F-004 | manually feasible | HIGH candidate |

---

# 8. CASE RECORDS

## F-001 — Rank tracking in Yandex and Google, up to 500 keywords

**Verdict:** `PARTIAL`

```text
Market: 500 ₽; up to 500 keywords; 1 day; usually 2 hours.
Input: domain + region + keyword list.
Output: Yandex top-100 + Google top-50 positions in XLSX.
Current: Yandex single-key rank + domain match + XLSX = YES.
Missing: Google SERP provider + durable bulk rank queue/checkpoint/resume.
```

## F-002 — Detailed SEO semantic core, up to 10,000 keywords

**Verdict:** `YES — WITH YANDEX WORDSTAT AS DATA SOURCE`

```text
Market: 45,000 ₽; up to 10,000; 30 days; usually 5 days.
Input: topic + region + commercial/informational intent.
Workflow: seed map → explicit Wordstat getTop calls → persist → merge/dedupe
→ expand uncovered branches → intent filter/tag → XLSX/CSV.
Boundary: no Google keyword-volume promise; do not pad narrow niches with irrelevant keys.
```

## F-003 — Ahrefs-based semantic core + clustering

**Verdict:** `PARTIAL`

```text
Market: from 2,500 ₽; 25 ₽/100 displayed; up to 10,000; 7 days.
Promise: Ahrefs Search Volume, KD, Traffic Potential, Clicks, competitor datasets, clustering.
Current: Wordstat + Yandex SERP + semantic/intent clustering + report/XLSX = YES.
Missing: Ahrefs data source/provider.
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

Owner-supplied example uses Yandex Wordstat, Google Keyword Planner, PR-CY/Yandex competitor analysis and Ahrefs. Current Bridge can reproduce the Yandex-demand/seasonality/SERP/public-review/report side, but not Ahrefs-equivalent DR/backlink/traffic/page metrics.

Sellable current variant: `Анализ ниши для SEO на основе Яндекс Wordstat и поисковой выдачи Яндекса`.

## F-005 — Wordstat exact-frequency check for supplied keyword list, up to 10,000

**Verdict:** `PARTIAL`

```text
Market: from 4,500 ₽; 45 ₽/100; up to 10,000; 1 region; 7 days.
Input: ready keyword list + region.
Promise: exact `!` frequency, wording claims 2025, zero rows removed, table.
Sample: 5,267 keyword rows, no zero-frequency rows observed.
Current: one current operator-frequency check + region + XLSX + zero filtering = YES.
Missing: durable 10k batch, verified quota economics, historical exact-`!` semantics.
```

Required future workflow: `BULK WORDSTAT FREQUENCY CHECKER` with persistent queue, rate/quota/cost guard, checkpoint/resume, zero filtering, deterministic XLSX and completeness report.

## F-006 — Semantic core for Yandex Direct advertising, 100-key base package

**Verdict:** `YES — READY NOW`

```text
Market: from 1,500 ₽; 100 keys; 1,500 ₽/100; 2 days.
Seller: 5.0 / 742 completed; 41 positive / 0 negative for this kwork.
Input: advertised product/service URL + geotargeting.
Promise: Excel semantic core + base Wordstat frequency + minus-words.
```

Owner-supplied `Семантика грузчики Тольятти.xlsx` proves a richer example structure:

```text
17 worksheets total
15 thematic worksheets
1,206 phrase-frequency records
1,204 unique phrases
290 unique minus-words
```

Do not infer that this 1,200+ row example is included in the 1,500 ₽ / 100-key base package.

Current workflow:

```text
offer inspection
→ seed map
→ regional Wordstat
→ merge/dedupe
→ commercial/relevance filtering
→ thematic grouping
→ preserve base frequency
→ derive/review minus-words
→ contracted final volume
→ XLSX + QA
```

Direct API is not required because the paid artifact is keyword research for advertising, not campaign mutation.

## F-007 — 500 grouped search queries for Yandex Direct advertising

**Marketplace:** Kwork  
**Title:** `Соберу 500 поисковых запросов - семантика для рекламы в Яндекс Директ`  
**Verdict:** `YES — READY NOW`

### Market data

```text
listed price = from 4,000 ₽
evidence = the exact same card appears in supplied Kwork cross-listing with 4,000 ₽ and 800 ₽/100
volume = up to 500 grouped keywords
listed normalization = 800 ₽ / 100 keywords
advertised deadline = 10 days
seller = 5.0 / 798 completed orders
seller total ratings shown = 355
order-specific reviews = 5 positive / 0 negative
orders currently in work = 1
```

The order configurator also shows 2,500 ₽, 1,500 ₽ and 1,000 ₽ options without visible labels in the supplied capture. Do not assign meanings to those add-ons.

### Client gives

```text
1. initial seed list: 2–3 queries
2. description of advertised product/service
3. if several products/services: short description + 2–3 seed queries for each
4. advertised site/product/service URL
```

The seller card does not explicitly list target region in the required-input block. For our own execution, **region/geotargeting must be confirmed before Wordstat collection**, because the service is intended for Yandex Direct and Wordstat frequency/relevance are region-sensitive.

### Advertised deliverable

```text
- semantic core for contextual advertising in Yandex Direct
- up to 500 final keywords
- ВЧ / СЧ / НЧ coverage
- manual cleaning of junk and implicit duplicates
- logical grouping
- grouped/filtered Excel report
```

The seller says they use Yandex Wordstat and Key Collector. `Key Collector` is the seller's implementation tool, not a promised client-side data source or metric. We do not need to reproduce that software itself; we need to reproduce the advertised result quality.

### Why current Bridge/ChatGPT can complete this order now

```text
public offer/topic research = YES
regional Wordstat expansion = YES
seed-based expansion = YES
merge/deduplication = YES
implicit-duplicate/relevance review = YES via ChatGPT
commercial-intent cleaning = YES
logical grouping = YES
frequency-based ВЧ/СЧ/НЧ labeling = YES
selecting up to 500 final phrases = YES
XLSX generation = YES
Yandex Direct API mutation = NOT REQUIRED
```

This is not the same problem as F-005. F-005 requires a frequency measurement for **every one of up to 10,000 pre-supplied phrases**. F-007 instead uses a small seed set to collect a candidate universe and then returns a selected, cleaned final set of up to 500 phrases. Existing Wordstat seed expansion can already support that workflow without 500 separate exact-frequency provider operations.

### Exact execution workflow

```text
1. Receive product/service description, URL and 2–3 seed phrases per offer branch.
2. Confirm target region/geotargeting.
3. Inspect offer and build a semantic seed map.
4. Run regional Wordstat collection for required seeds.
5. Merge candidate sets and normalize spelling/case/duplicates.
6. Remove:
   - irrelevant intent;
   - informational noise when campaign scope is commercial;
   - wrong geography;
   - unrelated products/services;
   - obvious junk;
   - semantic duplicates that would add no useful targeting coverage.
7. Preserve/compare Wordstat frequencies for surviving candidates.
8. Label or segment frequency bands (ВЧ / СЧ / НЧ) using an explicit project-relative rule rather than pretending universal thresholds exist for every niche.
9. Group phrases by logical advertising intent/product/service branch.
10. Select up to the contracted 500 final phrases with useful coverage across groups and demand levels.
11. Produce XLSX with clear group structure and frequencies.
12. QA:
    - duplicate scan;
    - wrong-intent scan;
    - wrong-geo scan;
    - empty/overbroad groups;
    - obvious missing high-value semantic branches.
```

### Commercial conclusion

F-007 is the second independent market proof that **advertising semantic-core preparation for Yandex Direct is already a sellable service for our current stack**.

It also shows that our eventual service should probably offer graduated volumes rather than one fixed package, for example 100 / 300 / 500 keys, while pricing must be derived only after more comparable cards are collected.

---

# 9. Later outputs from this matrix

After enough cards exist, derive:

```text
A. SELLABLE SERVICE CATALOG — only proven YES/bounded variants.
B. NEAR-TERM PRODUCT ROADMAP — repeated blockers that convert PARTIAL/NO into YES.
C. STANDARD OPERATING PROCEDURES — exact execution logic for each service.
D. PRICING GRID — comparable-market median/range + provider cost + time/risk/margin.
```
