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

`YES` is about the paid final deliverable, not merely existence of one API call. A card may be `YES` for a clearly bounded configuration (for example Yandex-only) while a richer provider-specific variant remains `PARTIAL`; that boundary must be explicit.

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
| F-006 | Semantic core for Yandex Direct advertising | from 1,500 ₽ | 100 keywords; 1,500 ₽/100 | 2 days | usually 21 hours | 5.0; 742 completed; 41 positive / 0 negative |
| F-007 | Grouped semantic core for Yandex Direct advertising | from 4,000 ₽ | up to 500; 800 ₽/100 shown | 10 days | not supplied | 5.0; 798 completed; 5 positive / 0 negative |
| F-008 | Technical + SEO audit of one website | 2,000 ₽ — cross-card evidence | 1 site; PDF + Excel appendices; optional Keys.so organic export | 10 days | not supplied | 5.0; 798 completed; 1 positive / 0 negative |
| F-009 | Technical SEO audit + 2-page desktop usability bonus | 3,000 ₽ — cross-card evidence | all pages of 1 site + 2 usability pages | 3 days | not supplied | 5.0; 1,104 completed; 25 positive / 0 negative |
| F-010 | Semantic core for a website from scratch / review of existing core | from 5,000 ₽ — cross-card evidence | 100 keywords; 5,000 ₽/100 shown | 5 days | not supplied | 5.0; 59 completed; 1 positive / 0 negative |
| F-011 | Filtering existing semantic core from noise and duplicates | from 8,000 ₽ | up to 5,000; 160 ₽/100 shown; 1 search engine / 1 Yandex region | 30 days | not supplied | 4.9; 235 completed; 1 positive / 0 negative |
| F-012 | Turnkey website semantic core + frequency + competition/difficulty + recommendations | 1,000 ₽ | 160 keywords; derived 625 ₽/100 | 4 days | usually 4 days | 5.0; 5,177 completed; 186 positive / 2 negative on kwork |
| **F-013** | **Website semantic core with TOP/SERP-overlap clustering + competition score** | **500 ₽** | **100 keywords; 500 ₽/100** | **4 days** | **usually 3 days** | **5.0; 4,026 completed; 1,573 positive / 8 negative on kwork** |

Do not calculate one median across unrelated products.

### Comparable slice — advertising semantic core for Yandex Direct

| Case | Base scope | Listed price | Normalized | Deadline | Included depth |
|---|---:|---:|---:|---:|---|
| F-006 | 100 keys | from 1,500 ₽ | 1,500 ₽/100 | 2 days | Wordstat base frequency + thematic groups + minus-words |
| F-007 | up to 500 keys | from 4,000 ₽ | 800 ₽/100 | 10 days | Wordstat/Key Collector collection + cleaning + logical groups + ВЧ/СЧ/НЧ |

`n=2` is not enough to set our final price. Current observed normalized range is **800–1,500 ₽ per 100 keywords** and deliverable depth differs.

A duplicate revisit of the exact F-006 listing confirmed the seller-displayed **usual completion = 21 hours**. This enriches F-006 only; it is not a new market observation and does not change the demand/pricing sample size.

### Comparable family — technical SEO audits

| Case | Listed price | Scope | Deadline | Distinguishing depth |
|---|---:|---|---:|---|
| F-008 | 2,000 ₽ cross-card evidence | 1 site | 10 days | Netpeak-style full crawl report + Excel appendices + optional Keys.so |
| F-009 | 3,000 ₽ cross-card evidence | all pages of 1 site + 2 usability pages | 3 days | 70-point technical checklist + prioritized recommendations + usability bonus |

`n=2` confirms paid demand but is still too small for a market median.

### Comparable family — website semantic cores

| Case | Listed price | Scope | Deadline | Distinguishing depth |
|---|---:|---|---:|---|
| F-002 | 45,000 ₽ | up to 10,000 keys | 30 days; usually 5 | high-volume Wordstat-based SEO core |
| F-010 | from 5,000 ₽ cross-card evidence | 100 keys | 5 days | simple from-scratch core or review of existing core |
| F-012 | 1,000 ₽ | 160 keys | 4 days; usually 4 | base + exact frequency, competition/difficulty, recommendations; demos expose Yandex + Google metrics |
| **F-013** | **500 ₽** | **100 keys** | **4 days; usually 3** | **Wordstat frequency + manual cleaning + competition score + TOP-overlap clustering in base package** |

These are not homogeneous enough for a single family median yet: volume, metric depth and manual work differ materially. F-013 is nevertheless a major low-price reference because **TOP/SERP-overlap clustering is included in the 500 ₽ base package**, not sold only as an add-on.

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
| F-011 Yandex scope | Cleanup/filtering of supplied semantic core, up to 5,000 keys | client supplies core + niche rules/examples | import → normalize → semantic dedupe → classify → selective Yandex validation → artifact |
| F-012 bounded Yandex-only variant | Turnkey semantic core with Yandex frequency, transparent Yandex-based difficulty and recommendations | do not promise seller-demo Google KEI/title metrics; confirm region; exact-frequency collection must be explicitly budgeted | site/topic → seeds → Wordstat → clean → current exact checks → Yandex SERP difficulty → recommendations → XLSX |
| **F-013 bounded equivalent** | **100-key Yandex semantic core with frequency + TOP-overlap clustering + our transparent competition score** | **do not promise exact seller demo columns `Бюджет [YD]`, global Yandex page count or global Title count; Russian/Yandex scope** | **seeds/site → Wordstat → clean → final 100 → one bounded Yandex SERP set per key → overlap graph → manual refinement → competitor-domain summary → competition score → XLSX** |

## PARTIALLY COVERED

| Case | Exact advertised service | What works now | Main blocker |
|---|---|---|---|
| F-001 | Yandex + Google rank tracking, up to 500 keywords | Yandex rank extraction + XLSX | no Google organic SERP provider; no bulk rank job |
| F-003 | Ahrefs-based semantic core + clustering | Wordstat, Yandex SERP, clustering, artifacts | no Ahrefs data source |
| F-004 | Full seller-equivalent niche analysis | demand, seasonality, Yandex competitors, reports | no Ahrefs/SEO-metrics provider; no durable competitor crawler |
| F-005 | Up to 10,000 supplied keywords with exact `!` Wordstat frequency for 2025 | current operator query per key + XLSX/zero filtering | no 10k durable batch; quota economics unverified; historical Dynamics cannot reproduce full `!` semantics |
| F-008 | Seller-equivalent technical + SEO site audit with full crawl + optional Keys.so | Yandex diagnostics, analysis, recommendations, artifacts | no full-site crawler/inventory; no Keys.so provider |
| F-009 | 70-point all-page technical audit + 2-page usability review | Yandex context, analysis, bounded manual page review | no autonomous crawler/rules/performance/HTML/structured-data layer |
| F-011 Google-specific validation variant | Google-specific semantic filtering for Russia if buyer expects SERP validation | semantic cleanup itself is feasible | no dedicated Google organic SERP/data provider |
| F-012 exact seller-equivalent package | 160-key turnkey core matching supplied examples, including Yandex + Google competition/difficulty fields | collection, cleaning, Yandex frequency, Yandex SERP review, recommendations, XLSX and optional clustering are feasible | no Google organic SERP/competition provider; no durable per-key difficulty/exact-frequency batch workflow |
| **F-013 exact seller-demo workbook** | **100-key core matching seller's example columns and scoring inputs exactly** | **Wordstat, retrieved Yandex SERP domains/titles, TOP clustering, competitor aggregation and XLSX are feasible** | **current Search normalizer does not expose global Yandex result count; current Direct slice has no budget-forecast method; exact seller `Бюджет [YD]` / global-pages / global-title metrics therefore cannot be guaranteed** |

## NOT COVERED

None recorded yet.

---

# 8. DEMAND-DERIVED CAPABILITY BACKLOG

| Capability | Cases | Current state | Market signal |
|---|---|---|---|
| **Wordstat-based keyword processing** | F-002, F-003, F-004, F-005, F-006, F-007, F-010, F-012, F-013 | core provider path exists | **VERY HIGH — repeated across 9 unique cases** |
| **Wordstat batch orchestration / durable queue** | F-002, F-003, F-004, F-005, F-012, F-013; reinforced by larger F-006/F-007 scopes | no dedicated batch job | **VERY HIGH — repeated** |
| **Website Semantic Core Builder** | F-002, F-010, F-012, F-013 | end-to-end Yandex variants feasible; richer provider metrics vary | **VERY HIGH — 4 independent seller observations** |
| **Advertising Semantic Core Builder** | F-006, F-007 | end-to-end feasible now; not productized as one workflow | **VERY HIGH — repeated across independent sellers** |
| **Semantic-core cleanup / noise filtering / semantic dedupe** | F-002, F-006, F-007, F-010, F-011, F-012, F-013 | feasible now; F-011 proves standalone sale | **VERY HIGH — repeated and directly monetized** |
| **Large semantic-dataset processor / checkpoint-resume** | F-002, F-003, F-005, F-011 | possible with artifacts/manual orchestration; no dedicated durable job | **VERY HIGH — repeated large-volume need** |
| **Semantic clustering / intent grouping** | F-002, F-003, F-004, F-006, F-007, optional F-012, **base F-013** | feasible; no durable large-dataset workflow | **VERY HIGH — repeated; F-013 proves TOP clustering is monetized in a low-price base package** |
| **SERP-overlap / TOP clustering engine** | **F-013; useful to F-003/F-004/F-012** | **raw Yandex domain/rank sets are available; no durable pairwise-overlap graph, thresholding, checkpoint/resume or manual-review workflow** | **VERY HIGH candidate — direct base deliverable from a 4,026-order seller** |
| **Reusable XLSX/CSV/PDF/report builder** | F-001..F-013 | artifact tooling available; not Bridge workflow | **VERY HIGH reuse** |
| **Full-site crawler / technical SEO inventory** | F-008, F-009; overlaps F-004 competitor crawl | missing | **VERY HIGH — repeated across independent paid audits** |
| **Crawler-export importer** | F-008, useful for F-009 | missing dedicated workflow | **HIGH — quickest audit compatibility path** |
| **Technical SEO rules + prioritization/report workflow** | F-008, F-009 | manual analysis possible if crawl data supplied | **VERY HIGH — repeated paid deliverable** |
| **Performance / HTML / structured-data audit layer** | F-008, F-009 | partial/manual only | **HIGH — repeated** |
| **Usability / commercial-factor page review** | F-009 | manual reasoning possible; no reusable workflow | **HIGH candidate** |
| **Keys.so / external organic-visibility provider or importer** | F-008 | missing | **HIGH candidate** |
| **Per-keyword competition/difficulty scorer** | F-004, F-012, **F-013** | Yandex-side scoring is feasible; no deterministic reusable production scorer/batch | **VERY HIGH candidate — repeatedly monetized** |
| **Keyword → relevant landing-page mapper** | F-012; useful for F-010 | manual mapping possible on bounded sites; no crawler-backed workflow | **HIGH candidate** |
| Bulk Wordstat Frequency Checker | F-005; smaller analogues F-012/F-013 | missing durable batch | HIGH — direct paid workflow |
| ВЧ/СЧ/НЧ classification | F-007, F-013 | feasible from frequencies | HIGH candidate |
| Minus-word builder | F-006 | feasible with ChatGPT | HIGH — direct paid deliverable |
| **Bulk SERP orchestration / safe checkpoint-resume** | F-001, F-004, **F-013** | individual Search calls work; no durable multi-key job | **VERY HIGH — F-013 alone requires roughly one SERP acquisition per final keyword for TOP clustering** |
| **Google organic SERP / competition provider** | F-001, optional F-011, F-012 seller-equivalent | missing | **VERY HIGH candidate — blocks multiple service families and an otherwise sellable semantic-core package** |
| Yandex high-volume/deferred Search | F-001, F-004, F-013 | deferred from Phase 2 | **VERY HIGH candidate — repeated and now tied to low-margin TOP clustering economics** |
| Ahrefs/external SEO metrics | F-003, F-004 | missing | HIGH — repeated |
| Competitor keyword/domain research | F-003, F-004, F-013 | partial; F-013 domain-frequency summary is feasible from Yandex SERPs | HIGH — repeated |
| Public competitor/site crawl + structure inventory | F-004, F-008, F-009 | no durable crawler | **VERY HIGH — repeated** |
| Niche-analysis scoring/report workflow | F-004 | manually feasible | HIGH candidate |
| **Yandex Direct keyword budget/forecast acquisition** | **F-013 seller-demo exactness** | **not present in accepted Direct first slice** | **MEDIUM/HIGH — not required for our sellable equivalent, but blocks byte/column-equivalent seller report** |

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
Market: from 1,500 ₽; 100 keys; 1,500 ₽/100; 2 days; usually 21 hours.
Input: advertised product/service URL + geotargeting.
Output: Wordstat-based grouped workbook + base frequency + minus-words.
Demo: 17 sheets; 15 thematic + contents + minus-words; 1,206 phrase-frequency records; 1,204 unique; 290 unique minus-words.
Workflow: offer → seeds → Wordstat → dedupe/clean → groups → frequency → minus-words → XLSX QA.
```

Direct API is not required because the deliverable prepares semantics for advertising but does not mutate an advertising account.

The exact same listing was later seen again and correctly treated as a duplicate. That revisit added only one new market fact — seller-displayed usual completion of **21 hours** — and did not create another F-id or market observation.

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
**Verdict:** `YES — READY NOW FOR YANDEX SCOPE`; optional Google-specific validation remains bounded.

```text
Market: from 8,000 ₽; up to 5,000 supplied keywords; 160 ₽/100; 30 days.
Input: existing core + niche + examples keep/remove + region/search-engine configuration.
Output: cleaned ready-to-use core.
Workflow: preserve original → normalize → exact/semantic dedupe → relevance/intent classes → selective Yandex validation → cleaned + removed/review sheets → QA.
Boundary: Google-specific SERP validation is not promised until a Google organic provider exists.
```

F-011 proves that semantic cleanup is itself a paid standalone product and should also be reused inside F-002/F-006/F-007/F-010/F-012/F-013.

## F-012 — Turnkey website semantic core with frequency, difficulty and recommendations

**Marketplace:** Kwork  
**Listing id:** `226452`  
**Seller:** `allsab`  
**Title:** `Разработка Семантического Ядра сайта Под Ключ`  
**Exact seller-equivalent verdict:** `PARTIAL`  
**Bounded Yandex-only variant:** `YES — SELLABLE NOW WITH EXPLICIT SCOPE`

### Market data

```text
listed base price = 1,000 ₽
volume = 160 keywords (seller says it can be slightly less depending on niche)
derived unit price = 625 ₽ / 100 keywords
advertised deadline = 4 days
seller-displayed usual completion = 4 days
seller = 5.0 / 5,177 completed orders
kwork reviews shown = 186 positive / 2 negative
base clustering = NOT included; manual clustering is an add-on
```

### Client gives

```text
- website URL, or topic of a future website;
- up to 3 priority seed queries when available;
- other wishes/constraints;
- our workflow must additionally confirm target region.
```

### Advertised base deliverable

The seller promises:

```text
1. manual topic/site/content analysis;
2. related queries, synonyms, same-root phrases and search suggestions;
3. base and real/exact frequency analysis;
4. removal of zero-value, non-target and ambiguous queries;
5. competition / ranking-difficulty analysis;
6. relevant-page assignment when possible;
7. informative report;
8. recommendations for the most effective promotion queries;
9. clustering only when the paid add-on is ordered.
```

### Supplied demo evidence — inspected locally

Four attached XLSX examples were inspected rather than inferred from the card text.

**`russkydubai.tilda.ws_семантическое ядро.xlsx`**

```text
150 keyword rows
150 unique phrases / 0 exact duplicate phrases
6 rows with exact frequency = 0
7 main fields:
- keyword
- base frequency
- exact frequency
- Yandex competition [KEI]
- Google competition [KEI]
- Yandex title-based difficulty
- Google title-based difficulty
no workbook formulas; metrics are delivered as static values
```

**`zaimy.space_семантическое ядро.xlsx`**

```text
170 keyword rows
170 unique phrases / 0 exact duplicates
20 rows with exact frequency = 0
same 7 metric columns including Yandex + Google competition/difficulty
no formulas
```

**`moresvinok.ru_семантическое ядро.xlsx`**

```text
314 keyword rows
314 unique phrases / 0 exact duplicates
121 rows with exact frequency = 0
same 7 metric columns
separate explanatory sheet showing how the seller interprets difficulty values
```

**`moresvinok.ru_группировка.xlsx`** — this corresponds to the optional clustering/grouping layer:

```text
9 thematic groups/sheets:
антикафе = 50
контактный зоопарк = 85
кафе с животными = 35
антикафе с животными = 18
развлечения в центре = 10
где посмотреть животных = 26
зоопарк = 47
кафе тайм = 8
кафе аренда = 36
315 grouped phrase records total
```

The companion core contains 314 phrase rows; the grouping workbook contains one additional phrase (`антикафе москва свинки`). This is demo evidence only and is not treated as a defect in the advertised base service.

### Current Bridge coverage

```text
site/topic reasoning = YES
seed generation / synonyms / semantic expansion = YES
Yandex Wordstat related-query acquisition = YES
regional acquisition = YES
base-frequency work = YES
current exact/operator-frequency work = possible on bounded sets, but not durable batch-productized
noise / ambiguity / duplicate filtering = YES
Yandex SERP review = YES
recommendations = YES
XLSX report = YES
optional semantic grouping = YES
relevant-page mapping = manual/bounded YES when site structure is inspectable
Google KEI / Google title-difficulty data = NO
```

The current Wordstat protocol exposes `getTop`, `getDynamics`, `getRegionsDistribution`, `getRegionsTree`; `getTop` accepts one phrase, region IDs and up to 2,000 returned phrases. The current Search protocol is Yandex Search (`/v2/web/search`), region-capable for the RU path, with conservative sync cost snapshot `0.488 RUB/request`. There is no Google organic SERP provider in the accepted Bridge.

### Why the exact seller-equivalent package is PARTIAL

The card text itself says competition/difficulty analysis, while the supplied examples show what that means in practice: the customer sees **both Yandex and Google competition/difficulty columns**. We can create a transparent Yandex-side score, but we cannot honestly reproduce the Google columns from current accepted providers.

Therefore:

```text
seller-demo-equivalent Yandex + Google report = PARTIAL
a clearly marketed Yandex-only report = YES
```

Do not silently substitute Yandex metrics into columns labeled Google.

### Sellable bounded workflow now

```text
1. Receive site/topic, target region, priority phrases and wishes.
2. Inspect offer/content and build seed map.
3. Collect related Yandex Wordstat phrases in bounded explicit requests.
4. Merge, normalize and remove exact/semantic duplicates.
5. Remove empty/non-target/ambiguous phrases.
6. Select target set around requested ~160 useful phrases; do not pad if niche is exhausted.
7. Collect base frequency.
8. For the final bounded list, collect current exact/operator frequency where required.
9. Run Yandex SERP checks for a transparent Yandex competition/difficulty model.
10. If site structure is small/inspectable, assign a relevant URL or mark `new page required` / `manual review`.
11. Produce promotion recommendations.
12. Deliver XLSX with clearly labeled Yandex-only metrics and methodology notes.
13. If clustering add-on is sold, produce thematic group sheets / mapping.
```

### Missing product capabilities

```text
1. Google organic SERP / competition provider.
2. Durable per-key exact-frequency queue/checkpoint/resume for repeated 100–500 keyword jobs.
3. Reusable deterministic Yandex keyword-difficulty scoring model rather than ad-hoc reasoning.
4. Durable per-key SERP batch orchestration.
5. Optional crawler-backed keyword → landing-page mapper for larger sites.
```

### Commercial consequence

F-012 is a strong demand/price signal because the seller has more than 5,000 completed orders and the base package is only **1,000 ₽ for 160 keywords**. We should not copy that price mechanically: the seller may have mature automation and cheap acquisition paths that we do not yet have. Our future price must be based on verified API cost plus operator time.

It also changes roadmap weighting: Google organic/competition access is no longer relevant only to rank tracking. It now blocks an otherwise highly sellable turnkey semantic-core service whose Yandex-side workflow is mostly already available.

## F-013 — Semantic core up to 100 queries with TOP/SERP-overlap clustering

**Marketplace:** Kwork  
**Listing id:** `9812`  
**Seller:** `Leomon`  
**Title:** `Семантическое ядро для сайта до 100 запросов с группировкой по ТОПу`  
**Sellable equivalent verdict:** `YES — READY NOW WITH EXPLICIT YANDEX METHODOLOGY`  
**Exact seller-demo workbook verdict:** `PARTIAL`

### Market data

```text
listed base price = 500 ₽
volume = 100 keywords
normalized price = 500 ₽ / 100 keywords
advertised deadline = 4 days
seller-displayed usual completion = 3 days
seller = 5.0 / 4,026 completed orders
kwork reviews shown = 1,573 positive / 8 negative
seller states >3,000 semantic cores collected on Kwork
language boundary = no English-language cores
```

### Client gives

```text
- initial seed-query list, especially for a specific niche;
- site or site categories as a starting structure;
- target region;
- competitor domains;
- query/content wishes and exclusions.
```

### Advertised base deliverable

Without paid options the card includes:

```text
1. ВЧ / СЧ / НЧ query collection;
2. manual noise cleaning;
3. frequency analysis;
4. competition calculation by formula;
5. TOP-based clustering (`key-assort`), with manual correction when needed;
6. final Excel report.
```

The seller explicitly says clustering is based on TOP/search-result overlap and warns that automatic grouping often needs manual refinement. This is important: semantic similarity alone is not an equivalent implementation of the base promise.

### Supplied workbook evidence — inspected locally

**`Стандартный кворк.xlsx`**

```text
sheets = 4
main `Ключевые фразы` = 159 grouped keyword rows, 159 unique phrases, 7 group starts
`Без группы` = 43 additional phrases, none duplicated in the main grouped sheet
combined grouped + ungrouped example = 202 unique phrases
`ТОП тематики` = 100 competitor domains ranked by how often they occurred in analyzed SERPs
`Пояснения` = definitions of delivered metrics
workbook formulas = none; delivered values are static
```

Main metric columns are:

```text
Группа
Фраза
Базовая частота [YW]
Частота ! [YW]
Бюджет [YD]
Страниц в Яндексе
Морды в Яндексе
Title в Яндексе
Конкуренция
```

A useful reverse-engineering observation: in all **159/159** grouped rows of the supplied standard workbook, `Конкуренция = (Title в Яндексе)^3`. Examples include `5 → 125`, `6 → 216`, `7 → 343`, `10 → 1000`. The workbook contains no formulas, so this relationship is inferred from the delivered static values, not from an embedded spreadsheet formula.

**`Разбивка на смысловые группы.xlsx`**

The supplied expanded example has a navigation map and nine topical data sheets:

```text
Общее
Форель
Семга
Горбуша
Дорадо
Скумбрия
Тунец
Кета
Лосось
```

Across those nine topical sheets there are **635 phrase records and 635 unique phrase texts**. The large category sheets retain the same Yandex frequency / budget / SERP-derived competition columns. This supports the interpretation that grouping and metric collection are reusable across larger site/category structures.

### Supplied instruction / TЗ evidence

The supplied explanatory screenshot states that automatic clustering is performed by a clusterer using intersections of queries from search results and that clusters should be manually reviewed/corrected. It also explains base frequency, exact frequency and competition concepts.

The attached `Пример ТЗ.docx` is **not part of the base semantic-core promise**. The card says the buyer can prepare a copywriter brief from the semantics or order one separately. The demo TЗ contains a 5,500-character target, 3 subheadings, 2 recommended images, ≥90% uniqueness, H1/main-key placement guidance, exact/morphological occurrence counts, supporting terms and stop-word constraints. Treat this as a separate optional content-brief service rather than a blocker for F-013 base scope.

### Current Bridge coverage

```text
seed / related-query acquisition through Yandex Wordstat = YES
region-specific Wordstat = YES
base frequency = YES
bounded current exact/operator frequency = YES, but not durable batch-productized
manual noise / intent cleaning = YES
ВЧ/СЧ/НЧ classification = YES
one Yandex SERP acquisition per final keyword = YES
retrieved SERP rank + URL + domain + title = YES
TOP-domain set overlap for clustering = YES in reasoning/artifact layer
manual cluster review/refinement = YES
aggregate competitor-domain frequency / `ТОП тематики` analogue = YES
XLSX artifact = YES
seller-exact `Бюджет [YD]` forecast = NO
seller-exact global `Страниц в Яндексе` count = NO through current normalized Search result
seller-exact global `Title в Яндексе` count = NOT GUARANTEED
```

The accepted Search protocol can request 1..100 groups per query and supports region on the RU path. Its conservative sync cost snapshot is `0.488 RUB/request`. The Search XML normalizer preserves returned result rank, URL, domain, title, snippet and modtime, but the normalized result exposes only the number of returned documents — not the search engine's global total-found count.

The accepted Direct first slice exposes only `listCampaigns`, `listAdGroups`, `listAds`, `listKeywords` and `getCampaignPerformance`; it has no keyword budget-forecast operation. Therefore Yandex Direct owner-live approval does **not** solve the seller-exact `Бюджет [YD]` column by itself.

### Why our sellable equivalent is YES

The paid client outcome is a useful cleaned core clustered by actual Yandex TOP overlap. We already possess the two required provider primitives:

```text
Wordstat → phrase acquisition + frequency
Yandex Search → per-query SERP domain sets
```

For 100 final keywords the current workflow can deliberately perform one bounded Search request per keyword, persist each result, compute pairwise domain overlap, form connected/thresholded clusters, then manually correct false merges/splits using intent and the site structure.

A one-pass 100-key clustering run is approximately:

```text
100 Search requests × 0.488 RUB conservative snapshot ≈ 48.8 RUB
```

This excludes Wordstat cost, repeated/error handling and operator time. It is feasible at current scale, but the seller's 500 ₽ market price makes automation/checkpointing commercially important.

Our competition score must be sold under **our own transparent methodology** — for example a documented combination of frequency, SERP overlap/fragmentation and observable TOP composition. That satisfies a competition-analysis deliverable without pretending we reproduced unavailable seller inputs.

### Why exact seller-demo equivalence is PARTIAL

To reproduce the attached workbook columns byte/semantics-equivalently we would need data not exposed by the accepted first slice:

```text
- `Бюджет [YD]` forecast: missing Direct forecast operation;
- global `Страниц в Яндексе`: current normalized Search output does not expose global total-found;
- global `Title в Яндексе`: current result-set parser exposes returned titles, not a guaranteed index-wide title-match count;
- exact seller competition methodology therefore cannot be guaranteed even though the sample values reveal a Title^3 relationship.
```

We must not label a sampled TOP metric as an index-wide count.

### Exact operating workflow we can sell now

```text
1. Receive seeds, site/categories, region, competitor domains and exclusions.
2. Inspect site/topic and build/normalize the initial seed map.
3. Run bounded Wordstat collection and merge candidate phrases.
4. Remove duplicates, noise, wrong intent and wrong geography.
5. Select the final up-to-100 useful phrases; do not pad a narrow niche.
6. Attach base frequency and, where included, current exact/operator frequency.
7. Classify ВЧ/СЧ/НЧ using a declared rule for the niche/region.
8. For each final phrase, retrieve a bounded Yandex SERP result set in the target region.
9. Persist every completed SERP result before moving to the next paid request.
10. Build keyword → set(domains) evidence.
11. Compute pairwise overlap and cluster by a declared threshold/graph rule.
12. Manually review clusters for obvious intent/site-structure errors; split/merge where justified.
13. Aggregate domain appearances across the collected SERPs into a competitor/TOP sheet.
14. Calculate our clearly labeled Yandex competition score from available evidence.
15. Deliver XLSX with grouped keywords, frequency, competition score, optional ungrouped/review sheet, TOP competitor sheet and methodology notes.
```

### Product consequence

F-013 is one of the strongest product-shaping cards so far because a seller with more than 4,000 completed orders includes **TOP-based clustering in a 500 ₽ / 100-key base package**.

The missing capability is no longer primarily a provider. The high-value product component is:

```text
TOP CLUSTERING JOB
keyword list + region
→ paid Search queue
→ per-key checkpoint
→ domain sets
→ overlap matrix / graph
→ deterministic thresholding
→ cluster QA / manual-review queue
→ competitor-domain aggregation
→ final workbook
```

This should reuse the existing exactly-once/cost discipline and avoid blind re-running paid SERPs. It would directly strengthen F-003/F-004/F-012 and future SEO-structure services as well.