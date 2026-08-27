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
| F-006 | Semantic core for Yandex Direct advertising | **from 1,500 ₽** | **100 keywords** base volume; 1,500 ₽/100 keywords | **2 days** | not supplied | 5.0; 742 completed; 41 positive / 0 negative for this kwork; 344 total ratings shown |

Do not calculate one median across unrelated products. F-002/F-003/F-006 belong to a broad semantic-core family but differ materially in promised depth, provider data and volume.

---

# 6. LIVE SELLABLE SERVICE COVERAGE

## READY NOW

| Case | Sellable service | Supported boundary | Execution |
|---|---|---|---|
| F-002 | SEO semantic core / keyword collection | Yandex Wordstat-based collection; no Google keyword-volume promise | Wordstat seed expansion → merge/dedupe → intent work → XLSX/CSV |
| F-004 variant | Yandex-based niche demand/seasonality + limited competitor analysis | Wordstat + Yandex SERP + public/manual review; no Ahrefs/Google Keyword Planner metrics | demand/dynamics → competitors → review/scoring → report/XLSX/chart |
| **F-006** | **Semantic core for Yandex Direct: 100 keywords + base Wordstat frequency + minus-words in Excel** | client supplies landing/product/service URL + geotargeting; no campaign mutation required | inspect offer → seed map → regional Wordstat collection → relevance/commercial filtering → thematic grouping → base frequency → minus-words → XLSX |

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
| **Wordstat-based keyword processing** | F-002, F-003, F-004, F-005, F-006 | core provider path exists | **VERY HIGH — repeated across 5 cases** |
| **Wordstat batch orchestration / durable queue** | F-002, F-003, F-004, F-005; reinforced by large F-006 example | no dedicated batch job | **VERY HIGH — repeated; F-006 base 100 does not require it but sample exceeds 1,200 rows** |
| **Bulk Wordstat Frequency Checker** | F-005 | missing | **HIGH — direct paid workflow** |
| **Advertising Semantic Core Builder** | F-006; overlaps F-002/F-003 | end-to-end feasible now, not productized as one durable workflow | **HIGH — proven paid workflow** |
| **Minus-word / negative-keyword builder** | F-006 | ChatGPT can do it; not productized | **HIGH — direct paid deliverable** |
| Keyword-set normalization / dedupe / checkpoint-resume | F-002, F-003, F-004, F-005, F-006 large scopes | operationally possible in parts; not productized | **VERY HIGH reuse** |
| Semantic clustering / intent grouping | F-002, F-003, F-004, F-006 | ChatGPT can perform; no durable large-dataset workflow | **VERY HIGH — repeated 4x** |
| Reusable XLSX/CSV/report builder | F-001..F-006 | artifact tooling available; not Bridge workflow | **VERY HIGH reuse** |
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

## F-006 — Semantic core for Yandex Direct advertising, 100-key base package

**Marketplace:** Kwork  
**Title:** `Семантическое ядро для рекламы. Семантика Яндекс Директ. Сбор СЯ`  
**Verdict:** `YES — READY NOW`

### Market data

```text
listed base price = from 1,500 ₽
base volume = 100 keywords
listed normalization = 1,500 ₽ / 100 keywords
advertised deadline = 2 days
seller = 5.0 / 742 completed orders
order-specific ratings = speed 5 / quality 5 / communication 5
order-specific reviews = 41 positive / 0 negative
seller total ratings shown = 344
```

The order configurator also displayed additional 3,000 ₽ and 1,000 ₽ options, but their labels were not present in the supplied capture. Do not assign semantics to those add-ons without evidence.

### Client gives

```text
1. link to advertised product/service
2. geotargeting / target region
3. topic should preferably be agreed before order
```

### Advertised deliverable

```text
- semantic core for contextual advertising
- Excel workbook
- base Wordstat frequency
- minus-words
- base package volume: 100 keywords
```

The card says the seller parses keywords using Wordstat services. The service is intended to prepare semantics for Yandex Direct / Google Ads, but the advertised artifact itself is a keyword workbook; it does not require campaign creation or mutation.

### Supplied XLSX example

Owner supplied `Семантика грузчики Тольятти.xlsx`.

Observed workbook structure:

```text
worksheets total = 17
content/theme worksheets = 15
+ Оглавление
+ Минус-слова
```

The 15 theme sheets are:

```text
Грузчики для переезда
Перевозка мебели
Переезд в другой город
Дачный переезд
Квартирный переезд
Офисный переезд
Перевозка сейфов
Утилизация мебели
Разнорабочие
Земельные работы
Демонтажные работы
Вывоз строительного мусора
Сборка и разборка мебели
Вырубка кустарников
Муж на час
```

Across those theme sheets the workbook contains:

```text
phrase-frequency records = 1,206
unique phrases = 1,204
cross-sheet duplicate phrase names = 2
frequency minimum = 1
frequency maximum = 1,043
median frequency = 2
minus-word rows with text = 290
unique minus-words = 290
```

The keyword sheets are arranged as repeated phrase/frequency pairs, typically separated by blank columns. The example therefore demonstrates substantially more than the base 100-key package: thematic segmentation, Wordstat-like frequency values and a large negative-keyword list.

**Pricing boundary:** do not infer that 1,206 keyword-frequency rows are included in the base 1,500 ₽ package. The advertised base volume is explicitly 100 keywords. The sample proves deliverable structure/quality, not base-package quantity.

### Why current Bridge/ChatGPT can complete the base package now

```text
public landing/offer inspection = YES
regional Wordstat keyword expansion = YES
base frequency = YES
commercial/relevance filtering = YES
selecting a bounded 100-key final set = YES
thematic grouping = YES
minus-word extraction = YES via ChatGPT analysis
XLSX generation = YES
Yandex Direct API mutation = NOT REQUIRED
```

A 100-key order does not need the missing 10,000-key durable frequency-check queue from F-005. Wordstat `getTop` can return a much larger candidate set from a seed, after which ChatGPT can select and structure the best 100 phrases for the agreed offer/region.

### Exact execution workflow

```text
1. Receive product/service URL and geotargeting.
2. Inspect the public offer and extract:
   - core service/product categories;
   - commercial modifiers;
   - geographic modifiers;
   - obvious exclusions.
3. Agree/derive seed map.
4. Run regional WORDSTAT_API_V1 getTop for the required seeds.
5. Merge and deduplicate candidates.
6. Remove irrelevant/informational/foreign-geo phrases inconsistent with the agreed ad scope.
7. Build thematic groups suitable for ad-campaign preparation.
8. Preserve base Wordstat frequency for selected phrases.
9. Derive minus-words from rejected queries and cross-theme noise; review manually/semantically before finalizing.
10. Select the contracted final volume (base = 100 keys).
11. Produce XLSX with:
    - grouped keywords;
    - base frequency;
    - separate minus-word sheet;
    - optional contents sheet when multiple groups exist.
12. Quality check: duplicates, wrong geography, obvious intent contamination, empty groups and accidental negative-keyword conflicts.
```

### Commercial boundary

The card refuses a long list of prohibited/sensitive/undesired topics. Our own eventual listing should define its own accepted-topic policy rather than copy that list blindly. The technical service itself is read-only keyword research and does not need Direct production access.

### Product signal from F-006

F-006 is especially useful because it is a **fully sellable service under the current stack**, not merely a future roadmap case. It proves demand for a standardized product:

```text
ADVERTISING SEMANTIC CORE BUILDER
URL + region
→ Wordstat collection
→ commercial/relevance filtering
→ thematic grouping
→ frequency
→ minus-words
→ XLSX
```

It also proves that minus-word generation and thematic grouping should become first-class reusable workflow stages even though they can already be completed manually/orchestrated with ChatGPT.

---

# 9. Later outputs from this matrix

After enough cards exist, derive:

```text
A. SELLABLE SERVICE CATALOG — only proven YES/bounded variants.
B. NEAR-TERM PRODUCT ROADMAP — repeated blockers that convert PARTIAL/NO into YES.
C. STANDARD OPERATING PROCEDURES — exact execution logic for each service.
D. PRICING GRID — comparable-market median/range + provider cost + time/risk/margin.
```