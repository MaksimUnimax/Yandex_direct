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

Never invent missing price/duration. Record `UNKNOWN` until evidence appears.

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
| F-001 | Yandex + Google rank tracking | 500 ₽ | up to 500 keywords; displayed add-on 100 ₽/quantity block | 1 day | usually 2 hours | 5.0; 412 completed; 7 positive reviews shown |
| F-002 | Detailed SEO semantic core | 45,000 ₽ | up to 10,000 keywords; derived 450 ₽/100 | 30 days | usually 5 days | 4.9; 235 completed; 2 positive reviews shown |
| F-003 | Ahrefs semantic core + clustering | from 2,500 ₽ | 10,000 keywords; listing also shows 25 ₽/100 | 7 days | not supplied | 5.0; 220 completed; 11 positive / 0 negative |
| F-004 | Niche analysis for a website | UNKNOWN | 1 niche / 1 region | 10 days | not supplied | 5.0; 220 completed; no reviews for this kwork |
| F-005 | Wordstat frequency check for supplied keywords | **from 4,500 ₽** (cross-card evidence from same seller listing) | up to 10,000 keywords / 1 region; **45 ₽/100 keywords** shown | 7 days | not supplied | 4.9; 235 completed; 1 positive / 0 negative |

Do not calculate one median across these unrelated products.

---

# 6. LIVE SELLABLE SERVICE COVERAGE

## READY NOW

| Case | Sellable service | Supported boundary | Execution |
|---|---|---|---|
| F-002 | SEO semantic core / keyword collection | Yandex Wordstat-based collection; no Google keyword-volume promise | Wordstat seed expansion → merge/dedupe → intent work → XLSX/CSV |
| F-004 variant | Yandex-based niche demand/seasonality + limited competitor analysis | Wordstat + Yandex SERP + public/manual review; no Ahrefs/Google Keyword Planner metrics | demand/dynamics → competitors → review/scoring → report/XLSX/chart |

## PARTIALLY COVERED

| Case | Exact advertised service | What works now | Main blocker |
|---|---|---|---|
| F-001 | Yandex + Google rank tracking, up to 500 keywords | Yandex rank acquisition/extraction + XLSX | no Google organic SERP provider; no bulk rank job |
| F-003 | Ahrefs-based semantic core + clustering | Wordstat, Yandex SERP, clustering, artifacts | no Ahrefs KD/Traffic Potential/Clicks/competitor corpus |
| F-004 | Full seller-equivalent niche analysis | demand, seasonality, Yandex competitors, public analysis, reports | no Ahrefs/SEO-metrics provider; no durable competitor crawler/bulk visibility workflow |
| F-005 | Up to 10,000 supplied keywords with exact `!` Wordstat frequency **for 2025**, zero rows removed | exact current operator query is technically possible per keyword; XLSX + zero filtering are easy | no 10k durable frequency-check batch; quota economics unverified; historical Dynamics does not reproduce full `!` operator semantics |

## NOT COVERED

None recorded yet.

---

# 7. DEMAND-DERIVED CAPABILITY BACKLOG

| Capability | Cases | Current state | Market signal |
|---|---|---|---|
| **Wordstat batch orchestration / durable queue** | F-002, F-003, F-004, F-005 | no dedicated batch job | **VERY HIGH — repeated 4x** |
| **Bulk Wordstat Frequency Checker** | F-005 | missing | **HIGH — direct paid workflow** |
| Seed expansion / dedupe / checkpoint-resume | F-002, F-003, F-004, F-005 | operationally possible in parts; not productized | **VERY HIGH — repeated 4x** |
| Semantic clustering / intent grouping | F-002, F-003, F-004 | ChatGPT can perform; no durable large-dataset workflow | VERY HIGH — repeated 3x |
| Reusable XLSX/CSV/report builder | F-001..F-005 | artifact tooling available; not Bridge workflow | **VERY HIGH reuse** |
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
Workflow: seed map → explicit Wordstat getTop calls (up to 2000 returned phrases/seed)
→ persist → merge/dedupe → expand uncovered branches → intent filter/tag → XLSX/CSV.
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

Owner-supplied example proves the seller uses Yandex Wordstat, Google Keyword Planner, PR-CY/Yandex competitor analysis and Ahrefs. The competitor layer includes DR/backlink/traffic/page metrics. Current Bridge can reproduce the Yandex-demand/seasonality/SERP/public-review/report side, but not Ahrefs-equivalent numbers.

Sellable current variant:

```text
"Анализ ниши для SEO на основе Яндекс Wordstat и поисковой выдачи Яндекса"
```

Workflow: cluster → Wordstat current/dynamics → seasonality chart → focus queries → Yandex SERP competitors → public competitor review → transparent measured averages → explicit difficulty rubric → recommendations + artifacts.

## F-005 — Wordstat exact-frequency check for supplied keyword list, up to 10,000

**Marketplace:** Kwork  
**Title:** `Статистика запросов Яндекс wordstat 2025 Частотность запросов вордстат`  
**Verdict:** `PARTIAL`

### Market data

```text
listed price = from 4,500 ₽ (cross-card evidence from this seller's earlier Kwork listing)
listed normalization = 45 ₽ / 100 keywords
volume = up to 10,000 supplied keyword phrases
region count = 1 per listed price
advertised deadline = 7 days
seller = 4.9 / 235 completed orders
order-specific reviews = 1 positive / 0 negative
```

### Client gives

```text
1. ready keyword list
2. target region
```

### Advertised deliverable

```text
- Wordstat frequency for every supplied phrase
- frequency in exact `!` correspondence
- wording claims frequency "for 2025"
- zero-frequency phrases removed
- one-region result table
```

### Supplied XLSX example

Owner supplied `Пример, спрос товаров и услуг Яндекс регион Россия.xlsx`.
Observed:

```text
sheet = Лист1
used range = A1:D5268
non-header keyword rows = 5,267
main columns = Ключевое слово | "!" YW
region note = Яндекс wordstat регион Россия
zero-frequency rows = none observed
minimum tail frequencies = 1
```

This confirms that the client-facing artifact is simple. The hard part is high-volume frequency acquisition with the promised semantics.

### What current Bridge can already do

Current `WORDSTAT_API_V1/getTop` accepts one `phrase` per command. Wordstat Top queries supports search operators such as `!` and quotes, so a current exact-form/operator query can be issued for one phrase/region. The resulting table can then be normalized, zero rows removed and written to XLSX.

```text
one current operator-frequency check = YES
region selection = YES
XLSX generation = YES
zero filtering = YES
10,000-key durable commercial batch = NO
historical 2025 exact-`!` semantics = NO through current governed path
```

### Why exact advertised coverage is not ready

1. **Volume:** the current protocol accepts one phrase per explicit `getTop` command. A supplied list of 10,000 phrases therefore implies up to roughly 10,000 provider operations, not one bulk request.
2. **Quota/economics:** Wordstat API has personal request-per-second/day quotas. We have not proven that a 10,000-key commercial run fits the actual account quota, cost and seven-day SLA.
3. **Historical semantics:** Top queries supports the normal operator set but represents recent/top-request data (last-30-day semantics in the official API). Historical `Dynamics` can cover 2025 date ranges, but Dynamics does not support the full operator set needed to claim the same exact `!` result historically. Therefore `"exact ! frequency for 2025"` must not be inferred or advertised from the current API.
4. **Durability:** no dedicated keyword-list queue exists yet for checkpoint/resume, per-row terminal state, rate limiting and non-replay after interruption.

### What we could honestly sell before full productization

A bounded current variant could be:

```text
"Проверю текущую частотность Яндекс Wordstat для согласованного списка запросов
в одном регионе и подготовлю XLSX."
```

But the acceptable list size must be determined from verified live quota/economics before advertising a large fixed volume.

### Required capability to turn F-005 into READY

```text
BULK WORDSTAT FREQUENCY CHECKER

input:
  keywords[]
  region
  operator policy / measurement mode

workflow:
  normalize input
  → persistent queue
  → one governed provider operation per required phrase
  → rate/quota/cost guard
  → checkpoint result
  → resume without blind replay
  → filter zero rows
  → deterministic XLSX
  → completeness report
```

Separately define two honest measurement products instead of mixing them:

```text
A. CURRENT EXACT-OPERATOR FREQUENCY
   → `!` / quote semantics where supported by current Top queries.

B. HISTORICAL DYNAMICS
   → monthly/weekly/daily historical demand with only the operator semantics actually supported by Dynamics.
```

### Product signal from F-005

F-005 is strong evidence that Wordstat bulk orchestration is not merely internal convenience. It directly unlocks a simple paid service whose deliverable is highly standardized. Together with F-002/F-003/F-004, high-volume Wordstat processing is now a repeated **4x** market requirement.

---

# 9. Later outputs from this matrix

After enough cards exist, derive:

```text
A. SELLABLE SERVICE CATALOG — only proven YES/bounded variants.
B. NEAR-TERM PRODUCT ROADMAP — repeated blockers that convert PARTIAL/NO into YES.
C. STANDARD OPERATING PROCEDURES — exact execution logic for each service.
D. PRICING GRID — comparable-market median/range + provider cost + time/risk/margin.
```
