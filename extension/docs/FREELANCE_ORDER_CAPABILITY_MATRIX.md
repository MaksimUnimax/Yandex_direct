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
| F-013 | Website semantic core with TOP/SERP-overlap clustering + competition score | 500 ₽ | 100 keywords; 500 ₽/100 | 4 days | usually 3 days | 5.0; 4,026 completed; 1,573 positive / 8 negative on kwork |
| F-014 | Wordstat semantic core from scratch + manual cleaning + section/subsection/TOP grouping | 1,000 ₽ | 150 keywords; derived ~667 ₽/100 | 4 days | usually 2 days | 5.0; 677 completed; 64 positive / 0 negative on kwork |
| F-015 | Standalone TOP/SERP-overlap clustering of a supplied semantic core | 1,000 ₽ | base scope up to 500 supplied keywords; derived 200 ₽/100; title says 1,000 but body/base volume says 500 | 2 days | usually 2 days | 5.0; 4,986 completed; 9 positive / 0 negative on this kwork |
| **F-016** | **Competitor-derived keyword selection for one website** | **3,000 ₽** | **up to 300 keywords; derived 1,000 ₽/100** | **4 days** | **usually 11 hours** | **4.9; 1,625 completed; 47 positive / 2 negative on this kwork** |

Do not calculate one median across unrelated products.

### Comparable slice — advertising semantic core for Yandex Direct

| Case | Base scope | Listed price | Normalized | Deadline | Included depth |
|---|---:|---:|---:|---:|---|
| F-006 | 100 keys | from 1,500 ₽ | 1,500 ₽/100 | 2 days | Wordstat base frequency + thematic groups + minus-words |
| F-007 | up to 500 keys | from 4,000 ₽ | 800 ₽/100 | 10 days | Wordstat/Key Collector collection + cleaning + logical groups + ВЧ/СЧ/НЧ |
| F-014 base | 150 keys | 1,000 ₽ | ~667 ₽/100 | 4 days; usually 2 | Yandex Wordstat only + general frequency + manual cleaning + structural/TOP grouping; minus-words extra |

`n=3` is still too small for a final market price. The observed normalized range is now approximately **667–1,500 ₽ per 100 keywords**, but the packages differ materially in keyword volume, grouping depth and minus-word inclusion.

A duplicate revisit of the exact F-006 listing confirmed the seller-displayed **usual completion = 21 hours**. This enriches F-006 only; it is not a new market observation and does not change the demand/pricing sample size.

### Comparable family — technical SEO audits

| Case | Listed price | Scope | Deadline | Distinguishing depth |
|---|---:|---|---:|---|
| F-008 | 2,000 ₽ cross-card evidence | 1 site | 10 days | Netpeak-style full crawl report + Excel appendices + optional Keys.so |
| F-009 | 3,000 ₽ cross-card evidence | all pages of 1 site + 2 usability pages | 3 days | 70-point technical checklist + prioritized recommendations + usability bonus |

`n=2` confirms paid demand but is still too small for a market median.

### Comparable family — website semantic cores

| Case | Listed price | Scope | Deadline | Distinguishing depth |
|---|---:|---|---:|---:|
| F-002 | 45,000 ₽ | up to 10,000 keys | 30 days; usually 5 | high-volume Wordstat-based SEO core |
| F-010 | from 5,000 ₽ cross-card evidence | 100 keys | 5 days | simple from-scratch core or review of existing core |
| F-012 | 1,000 ₽ | 160 keys | 4 days; usually 4 | base + exact frequency, competition/difficulty, recommendations; demos expose Yandex + Google metrics |
| F-013 | 500 ₽ | 100 keys | 4 days; usually 3 | Wordstat frequency + manual cleaning + competition score + TOP-overlap clustering in base package |
| F-014 | 1,000 ₽ | 150 keys | 4 days; usually 2 | Yandex-only commercial semantic core + general frequency + manual cleaning + section/subsection/TOP grouping |
| **F-016** | **3,000 ₽** | **up to 300 keys** | **4 days; usually 11 hours** | **competitor-derived seed/topic analysis + final keyword selection; no ranking-keyword export provider promised** |

These are not homogeneous enough for a single family median yet: volume, metric depth, competitor-analysis depth and manual work differ materially.

### Standalone semantic-core cleanup

| Case | Listed price | Scope | Deadline | Normalized |
|---|---:|---|---:|---:|
| F-011 | from 8,000 ₽ | up to 5,000 supplied keys | 30 days | 160 ₽/100 shown |

`n=1` is not enough for a market price conclusion, but it proves that cleanup/deduplication itself is sold as a standalone service rather than only as part of collection.

### Standalone TOP/SERP-overlap clustering

| Case | Listed price | Scope | Deadline | Normalized |
|---|---:|---|---:|---:|
| F-015 | 1,000 ₽ | up to 500 supplied keywords in the actual base description | 2 days; usually 2 | 200 ₽/100 |

`n=1` is not enough to establish a market median for standalone TOP clustering. It is nevertheless a strong observation because F-013/F-014 bundle TOP grouping into broader semantic-core packages, while F-015 sells **clustering itself** as the base product and moves keyword collection into an optional add-on.

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
| F-013 bounded equivalent | 100-key Yandex semantic core with frequency + TOP-overlap clustering + our transparent competition score | do not promise exact seller demo columns `Бюджет [YD]`, global Yandex page count or global Title count; Russian/Yandex scope | seeds/site → Wordstat → clean → final 100 → one bounded Yandex SERP set per key → overlap graph → manual refinement → competitor-domain summary → competition score → XLSX |
| F-014 base | 150-key Yandex Wordstat semantic core from scratch with manual cleaning, general frequency and section/subsection/TOP grouping | commercial standard topics; Russian language; Yandex only; informational keys, exact frequency, minus-words and detailed manual clustering are separate options | topic/site/sections + region → seed map → Wordstat → merge/dedupe → manual relevance cleaning → structural grouping → bounded TOP validation where needed → general frequency → XLSX/Google-compatible table |
| F-015 bounded variant | Standalone Yandex TOP/SERP-overlap clustering of a supplied semantic core, up to ~100 keys | client supplies keyword list; our intake must also confirm target region; no keyword collection included unless sold separately | keyword list + region → one bounded SERP acquisition per key → persist → domain sets → overlap graph → cluster QA/manual correction → XLSX |
| **F-016** | **Competitor-derived keyword selection, up to 300 keys for one website** | **public/client-supplied competitor analysis + Yandex SERP + Wordstat; no promise of Ahrefs/Keys.so organic-ranking export or exhaustive competitor crawl; confirm target region** | **client site → competitor set → public page/topic extraction → regional Wordstat expansion → merge/dedupe → relevance/coverage scoring → final up-to-300 keyword list/artifact** |

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
| F-013 exact seller-demo workbook | 100-key core matching seller's example columns and scoring inputs exactly | Wordstat, retrieved Yandex SERP domains/titles, TOP clustering, competitor aggregation and XLSX are feasible | current Search normalizer does not expose global Yandex result count; current Direct slice has no budget-forecast method; exact seller `Бюджет [YD]` / global-pages / global-title metrics therefore cannot be guaranteed |
| F-014 exact-frequency add-on at repeated scale | seller-style `YW / "YW" / "!YW"` frequency expansion across the whole supplied set | bounded operator-form collection and XLSX are feasible | no durable per-key exact-frequency queue/checkpoint/resume; must be separately budgeted and should not be silently included in the 1,000 ₽ base package |
| F-015 exact advertised 500-key base | TOP-based clustering of up to 500 supplied keywords within the 2-day base offer | all provider primitives exist: regional Yandex Search, domain/rank/title evidence, overlap computation, manual refinement and artifact output | no durable 500-request Search queue with per-key checkpoint/resume/progress/budget controls; manual one-command-per-key execution is not a reliable commercial workflow at this scale |

## NOT COVERED

None recorded yet.

---

# 8. DEMAND-DERIVED CAPABILITY BACKLOG

| Capability | Cases | Current state | Market signal |
|---|---|---|---|
| **Wordstat-based keyword processing** | F-002, F-003, F-004, F-005, F-006, F-007, F-010, F-012, F-013, F-014, **F-016 current workflow** | core provider path exists | **VERY HIGH — repeated across 11 applicable cases** |
| **Wordstat batch orchestration / durable queue** | F-002, F-003, F-004, F-005, F-012, F-013, F-014; reinforced by larger F-006/F-007 scopes | no dedicated batch job | **VERY HIGH — repeated** |
| **Website Semantic Core Builder** | F-002, F-010, F-012, F-013, F-014, **F-016** | end-to-end Yandex variants feasible; richer provider metrics vary | **VERY HIGH — 6 independent seller observations** |
| **Advertising Semantic Core Builder** | F-006, F-007, F-014 | end-to-end feasible now within each card's stated scope; not productized as one workflow | **VERY HIGH — repeated across 3 independent sellers** |
| **Semantic-core cleanup / noise filtering / semantic dedupe** | F-002, F-006, F-007, F-010, F-011, F-012, F-013, F-014, **F-016** | feasible now; F-011 proves standalone sale | **VERY HIGH — repeated and directly monetized** |
| **Large semantic-dataset processor / checkpoint-resume** | F-002, F-003, F-005, F-011, F-015 | possible with artifacts/manual orchestration; no dedicated durable job | **VERY HIGH — repeated large-volume need** |
| **Semantic clustering / intent grouping** | F-002, F-003, F-004, F-006, F-007, optional F-012, base F-013, base F-014, F-015 | feasible; no durable large-dataset workflow | **VERY HIGH — repeated; F-015 proves TOP clustering is independently monetized as its own base service** |
| **SERP-overlap / TOP clustering engine** | F-013, F-014, F-015; useful to F-003/F-004/F-012 | raw Yandex domain/rank sets are available; no durable pairwise-overlap graph, thresholding, checkpoint/resume or manual-review workflow | **VERY HIGH — confirmed by 3 independent sellers, including one standalone clustering offer** |
| **Standalone TOP clustering service workflow** | F-015; related bundled evidence F-013/F-014 | bounded ~100-key execution feasible now; advertised 500-key job lacks durable queue/checkpoint/resume | **VERY HIGH candidate — direct paid service at 1,000 ₽ / 500 keys** |
| **Reusable XLSX/CSV/PDF/report builder** | F-001..F-016 | artifact tooling available; not Bridge workflow | **VERY HIGH reuse** |
| **Full-site crawler / technical SEO inventory** | F-008, F-009; overlaps F-004 competitor crawl | missing | **VERY HIGH — repeated across independent paid audits** |
| **Crawler-export importer** | F-008, useful for F-009 and F-016 exhaustive variant | missing dedicated workflow | **HIGH — quickest audit/competitor compatibility path** |
| **Technical SEO rules + prioritization/report workflow** | F-008, F-009 | manual analysis possible if crawl data supplied | **VERY HIGH — repeated paid deliverable** |
| **Performance / HTML / structured-data audit layer** | F-008, F-009 | partial/manual only | **HIGH — repeated** |
| **Usability / commercial-factor page review** | F-009 | manual reasoning possible; no reusable workflow | **HIGH candidate** |
| **Keys.so / external organic-visibility provider or importer** | F-008; optional richer F-016 variant | missing | **HIGH candidate — would deepen competitor-derived keyword services but is not required by F-016 base contract** |
| **Per-keyword competition/difficulty scorer** | F-004, F-012, F-013 | Yandex-side scoring is feasible; no deterministic reusable production scorer/batch | **VERY HIGH candidate — repeatedly monetized** |
| **Keyword → relevant landing-page mapper** | F-012; useful for F-010/F-014/F-016 | manual mapping possible on bounded sites; no crawler-backed workflow | **HIGH candidate** |
| **Bulk Wordstat Frequency Checker** | F-005; smaller analogues F-012/F-013; F-014 exact-frequency add-on | missing durable batch | **VERY HIGH candidate — direct paid workflow/add-on repeated across cards** |
| ВЧ/СЧ/НЧ classification | F-007, F-013; useful to F-014/F-016 | feasible from frequencies | HIGH candidate |
| Minus-word builder | F-006; F-014 paid add-on | feasible with ChatGPT | HIGH — direct paid deliverable |
| **Bulk SERP orchestration / safe checkpoint-resume** | F-001, F-004, F-013, F-014, F-015 | individual Search calls work; no durable multi-key job | **VERY HIGH — F-015 turns the missing queue into the main blocker of a directly sellable 500-key service** |
| **Google organic SERP / competition provider** | F-001, optional F-011, F-012 seller-equivalent | missing | **VERY HIGH candidate — blocks multiple service families and an otherwise sellable semantic-core package** |
| **Yandex high-volume/deferred Search** | F-001, F-004, F-013, F-014, F-015 | deferred from Phase 2 | **VERY HIGH — F-015 makes cost/throughput critical because one 500-key pass is hundreds of paid Search calls** |
| Ahrefs/external SEO metrics | F-003, F-004; optional richer F-016 variant | missing | HIGH — repeated |
| **Competitor keyword/domain research** | F-003, F-004, F-013, **F-016** | bounded Yandex/public-site competitor analysis is feasible; no external organic-keyword export provider | **VERY HIGH — repeated across 4 independent cards and now directly drives a 300-key paid deliverable** |
| **Competitor-derived semantic-core workflow** | **F-016**; related evidence F-003/F-004/F-013 | bounded end-to-end flow is feasible now using client site + public competitors + Yandex SERP + Wordstat; not productized | **HIGH/VERY HIGH candidate — direct 3,000 ₽ / 300-key service with 11-hour usual completion** |
| **Public competitor/site crawl + structure inventory** | F-004, F-008, F-009, **F-016** | bounded public/manual inspection feasible; no durable crawler | **VERY HIGH — repeated and now directly tied to competitor-derived keyword selection** |
| Niche-analysis scoring/report workflow | F-004 | manually feasible | HIGH candidate |
| Yandex Direct keyword budget/forecast acquisition | F-013 seller-demo exactness | not present in accepted Direct first slice | MEDIUM/HIGH — not required for our sellable equivalent, but blocks byte/column-equivalent seller report |
| **Information-keyword expansion workflow** | F-014 paid add-on; overlaps F-002 | feasible with Wordstat + intent classification; not a dedicated product flow | **HIGH — explicitly monetized add-on** |

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
Market: from 4,000 ₽; up to 500 keys; 800 ₽/100; 10 days.
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

F-011 proves that semantic cleanup is itself a paid standalone product and should also be reused inside F-002/F-006/F-007/F-010/F-012/F-013/F-014/F-016.

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

## F-014 — Wordstat semantic core from scratch + grouping by sections/subsections/TOP

**Marketplace:** Kwork  
**Listing id:** `18555096`  
**Seller:** `Anastasy-Mar`  
**Title:** `Сбор ключевых фраз + группировка для семантического ядра из Вордстат`  
**Base verdict:** `YES — READY NOW`

### Market data

```text
listed base price = 1,000 ₽
volume = 150 keywords
derived normalized price ≈ 667 ₽ / 100 keywords
advertised deadline = 4 days
seller-displayed usual completion = 2 days
seller = 5.0 / 677 completed orders
kwork reviews shown = 64 positive / 0 negative
language = Russian only
provider boundary = Yandex Wordstat only; seller explicitly does not work with Google
```

### Client gives

```text
1. topic / niche to collect from;
2. active website URL if it exists, or planned site sections;
3. target region — explicitly required by the seller;
4. nuances / exclusions;
5. optional competitor-site links as context.
```

The seller explicitly says that **competitor analysis itself is not included**, even though competitor links may be supplied as background. Therefore F-014 does not require Ahrefs, Keys.so, a competitor crawler or Google data.

### Advertised base deliverable

The base package is narrower than several prior semantic-core cards:

```text
- relevant keyword collection from Yandex Wordstat from scratch;
- manual removal of garbage and off-topic phrases;
- commercial keywords for standard topics;
- general Wordstat frequency;
- grouping / clustering by sections, subsections and TOP;
- Excel or Google-compatible table/report;
- final 150-key scope.
```

The seller separately monetizes:

```text
- informational keywords;
- complex/specific topics;
- exact frequency;
- minus-words;
- detailed manual clustering;
- urgent work;
- rework caused by an incorrect brief.
```

Those add-ons must not be treated as blockers for the 1,000 ₽ base verdict.

### Supplied screenshot evidence — inspected locally

**Commercial household-goods example**

The first screenshot shows a hierarchical commercial semantic core with large sections such as:

```text
Средства для стирки
Порошки
Гели/капсулы
Кондиционеры
```

and nested subgroups including membrane fabrics, white/black/colored laundry, jackets/down coats, delicate fabrics, dark/black laundry and similar product-intent splits. Each query has one displayed frequency value. This is consistent with a base general-frequency + hierarchical-grouping deliverable rather than a complex competition-metric workbook.

**Informational-keyword example**

The second screenshot is intentionally different and supports the seller's add-on boundary. It contains broader informational clusters such as:

```text
расстройство пищевого поведения
рпп
нарушение пищевого поведения
переедание
булимия
отказ от еды
диета
правильное питание
```

with query-frequency values. This demonstrates that informational expansion is a separate layer that can be sold independently of the commercial base.

**Exact-frequency example**

The third screenshot groups immigration/legal queries under blocks such as:

```text
Общее
Патент
РВП
ВНЖ
```

and shows three frequency-style columns labeled approximately `YW`, `"YW"`, `"!YW"`. This is evidence that the exact-frequency add-on returns multiple Wordstat operator forms rather than only the single general-frequency number used in the base examples.

### Current Bridge coverage

```text
topic/site reasoning = YES
seed-map creation = YES
Yandex Wordstat getTop collection = YES
region-specific Wordstat = YES
up to 2,000 returned phrases per getTop seed = YES
manual/LLM relevance cleaning = YES
semantic dedupe = YES
commercial-vs-informational classification = YES
section/subsection grouping = YES
bounded Yandex TOP validation = YES
XLSX generation = YES
Google dependency = NONE by contract
competitor-analysis dependency = NONE by contract
Direct account access = NOT REQUIRED
```

The current Wordstat protocol exposes `getTop`, `getDynamics`, `getRegionsDistribution` and `getRegionsTree`. `getTop` accepts one seed phrase, a region list and `numPhrases` from 1 to 2,000, which is sufficient to acquire a 150-key final set from one or more explicit seed requests.

### Why F-014 base is a clean YES

Unlike F-012 and F-013, the seller's base package does **not** require unavailable Google metrics, Yandex-wide document counts, Direct budget forecasts or external SEO providers.

The required primitives are already present:

```text
Wordstat → candidate phrases + general frequency + region
ChatGPT → manual-quality relevance cleaning + commercial-intent filtering + section/subsection structure
Yandex Search → optional/bounded TOP evidence where grouping requires SERP confirmation
artifact tooling → Excel output
```

The phrase `по разделам/подразделам и ТОПу` means that a robust implementation should preserve the possibility of TOP/SERP validation for ambiguous grouping. We should not reduce every order to semantic similarity only. However, unlike F-013, the card does not expose a seller-specific competition formula or require a separate competitor-analysis sheet.

### Exact operating workflow we can sell now

```text
1. Receive topic, site/planned sections, region, nuances and optional competitor links.
2. Inspect the offer/site structure and create a seed map by product/service category.
3. Issue bounded regional Wordstat getTop requests for the strongest seeds.
4. Persist each paid/provider result before issuing the next request.
5. Merge candidates and normalize phrase text while preserving original Wordstat wording/frequency.
6. Remove exact duplicates, semantic duplicates, garbage, wrong intent and wrong geography.
7. Keep the base package commercial for standard topics unless the buyer orders informational expansion.
8. Build section/subsection groups from site structure and query intent.
9. For ambiguous groups, use bounded Yandex TOP/SERP evidence to confirm whether phrases belong together.
10. Manually review obvious bad merges/splits.
11. Select the final ~150 useful phrases; do not pad an exhausted niche.
12. Attach general Wordstat frequency.
13. Deliver XLSX / Google-compatible table with section, subsection, phrase and frequency.
14. Run QA for duplicates, region consistency, relevance, row count and artifact readability.
```

### Add-on coverage

```text
Informational keywords = YES now; Wordstat + intent classification + separate information clusters.
Minus-words = YES now; reusable negative-term extraction/review workflow.
Detailed manual clustering = YES operationally; stronger if backed by the F-013 TOP-overlap workflow.
Exact-frequency add-on = feasible on bounded sets, but PARTIAL as a durable repeated workflow because no per-key checkpoint/resume batch exists yet.
Complex/specific niches = case-by-case commercial scope, not a provider blocker.
```

### Commercial / product consequence

F-014 reinforces three conclusions:

```text
1. The most repeated immediately sellable product family is now clearly a Yandex Wordstat Semantic Core Builder.
2. Sellers monetize a low-cost base and move expensive operator work into add-ons; our own catalog should preserve the same separation instead of bundling exact frequency / minus-words / deep clustering into every cheap order.
3. TOP grouping is now independently observed in F-013 and F-014, so the durable TOP-clustering / paid-Search queue is no longer a one-card optimization.
```

At the displayed 1,000 ₽ / 150-key base price, unnecessary per-key provider calls would destroy margin. Productization should therefore distinguish:

```text
cheap base = Wordstat collection + cleaning + structural grouping + general frequency
paid depth = exact-frequency batch and/or deep TOP/SERP clustering
```

This is a strong architecture/pricing signal, not a reason to delay accepting the base service now.

## F-015 — Standalone TOP/SERP-overlap clustering of a supplied semantic core

**Marketplace:** Kwork  
**Listing id:** `5331960`  
**Seller:** `reboox`  
**Title:** `Кластеризация 1000 запросов, семантического ядра`  
**Exact advertised base verdict:** `PARTIAL`  
**Bounded current variant:** `YES — UP TO ~100 SUPPLIED KEYS`

### Market data and title/body mismatch

```text
listed base price = 1,000 ₽
headline says = 1,000 queries
actual base description says = supplied semantic core not more than 500 queries
explicit `Объем услуги в кворке` = 500 keys
therefore the defensible base volume for market statistics = 500 keys
derived normalized price = 200 ₽ / 100 keys
advertised deadline = 2 days
seller-displayed usual completion = 2 days
seller = 5.0 / 4,986 completed orders
kwork reviews shown = 9 positive / 0 negative
```

Do not count the headline's `1000` as the actual included base volume. The body and explicit volume field both say 500; larger volume is handled through paid options.

### Client gives

Base service:

```text
- a ready semantic core / keyword list;
- not more than 500 queries in the base package.
```

If the buyer has no keyword list, the card offers a separate paid `сбор запросов` option. Keyword acquisition is therefore **not a blocker for the clustering base** and should not be bundled into our cost model unless that add-on is sold.

The seller card does not explicitly request a search region. Our own implementation must nevertheless **confirm target region before any Yandex TOP acquisition**, because SERP-overlap clustering is region-sensitive and should be reproducible.

### Advertised deliverable

```text
- grouping / clustering of the supplied semantic core by TOP;
- suitable for SEO/site promotion and advertising preparation;
- report in PDF, Excel or Word at seller discretion;
- rapid completion.
```

No demo artifact is supplied in this card, so no exact workbook columns, threshold formula, TOP depth or cluster-linkage rule can be claimed from the source.

One visible review complains that queries should be grouped by semantic meaning; the seller replies that corrected clusters were sent separately. This does not redefine the contract, but it is useful qualitative evidence that **automatic TOP clustering still needs human QA/refinement** — consistent with the explicit warning already observed in F-013.

### Current Bridge coverage

Current accepted Search protocol provides:

```text
Yandex Search API = YES
regional RU search = YES
1..100 groups per query = YES
rank / URL / domain / title evidence = YES after normalization
one explicit request per keyword = YES
local domain-set overlap computation = YES
pairwise graph/threshold clustering in analysis layer = YES
manual merge/split review = YES
XLSX/PDF/DOCX artifact generation = YES
```

The current protocol uses `/v2/web/search`, defaults RU searches to region `225` when none is supplied, supports explicit region for RU/TR, allows `groupsOnPage` from 1 to 100 and carries a conservative synchronous cost snapshot of `0.488 RUB/request`.

### Why the exact 500-key base is PARTIAL

The blocker is **not missing search data**. It is production-scale orchestration.

A direct one-pass TOP acquisition for all 500 supplied keywords means approximately:

```text
500 provider Search requests
× 0.488 RUB conservative sync snapshot
≈ 244 RUB provider-search cost before retries/errors/operator time
```

After acquisition, a full 500-key pairwise comparison is `124,750` keyword pairs, which is computationally trivial locally. The risky/expensive part is the provider-request lifecycle, not the overlap math.

Today the accepted Bridge can execute each Search command correctly, but it does not yet provide a durable 500-key job with:

```text
- persistent input queue;
- one completed-key checkpoint before the next paid request;
- safe resume without re-running successful paid SERPs;
- progress reporting;
- request/cost budget;
- deterministic retry/unknown-outcome handling;
- cluster-review queue;
- final aggregate artifact build from persisted evidence.
```

Manually driving hundreds of paid one-key commands is technically possible, but it is not a reliable commercial workflow for a 1,000 ₽ / 2-day service. Under the matrix verdict rule, the exact advertised 500-key base is therefore `PARTIAL`, not `YES`.

### Bounded service we can sell now

A smaller supplied-core TOP clustering job around the F-013 scale is already practical:

```text
1. Receive ready keyword list and confirm target region.
2. Normalize/dedupe the supplied list without changing intent.
3. For each final keyword, request a bounded regional Yandex SERP.
4. Persist every completed result before issuing the next paid request.
5. Build keyword → set(domains) evidence.
6. Compute pairwise domain overlap.
7. Form clusters using a declared threshold/graph rule.
8. Manually review semantic-intent mismatches and obvious false merges/splits.
9. Preserve ungrouped/uncertain phrases for review rather than forcing them into bad clusters.
10. Deliver XLSX (or PDF/DOCX when commercially useful) with phrase → cluster mapping and methodology note.
```

At approximately 100 supplied keys, this is already the same bounded acquisition scale qualified operationally in F-013 and can be accepted now. Direct, Metrika, Webmaster and Wordstat are not required for the **base clustering-only** order.

### Optional collection add-on

If the buyer also purchases keyword collection, our existing Wordstat path can supply the candidate core first, after which the clustering pipeline begins. That becomes a combined semantic-core service similar to F-013/F-014 and should be priced separately because provider acquisition and cleaning are additional work.

### Product consequence

F-015 materially upgrades the priority of the already identified `TOP CLUSTERING JOB`:

```text
supplied keyword list + region
→ durable paid Search queue
→ per-key checkpoint/resume
→ domain/rank evidence store
→ overlap matrix / graph
→ deterministic clustering
→ human review queue
→ final report
```

This is no longer inferred from a bundled feature. A seller with nearly 5,000 completed orders is directly selling the clustering step itself at **1,000 ₽ for an actual base scope of 500 keys**.

The commercial lesson is equally important: at the current conservative Search snapshot, a naïve 500-request synchronous implementation spends about **244 ₽** on Search alone — roughly one quarter of the displayed 1,000 ₽ retail price before operator time. Therefore high-volume/deferred Search economics, checkpoint/resume and avoiding unnecessary repeated SERP calls are core margin requirements, not optional engineering polish.

F-015 also confirms that our future catalog should separate:

```text
A. semantic-core collection/cleaning;
B. TOP clustering of an already supplied core;
C. combined collection + clustering package.
```

That separation maps directly to how the market already sells the work.

## F-016 — Competitor-derived keyword selection for one website

**Marketplace:** Kwork  
**Listing id:** `17864370`  
**Seller:** `Arseniy84`  
**Title:** `Подберу для Вашего сайта Ключевые слова`  
**Verdict:** `YES — READY NOW WITH PUBLIC/YANDEX COMPETITOR-ANALYSIS BOUNDARY`

### Market data

```text
listed base price = 3,000 ₽
volume = up to 300 keywords for one website
derived normalized price = 1,000 ₽ / 100 keywords
advertised deadline = 4 days
seller-displayed usual completion = 11 hours
seller profile = 4.9 / 1,625 completed orders
kwork reviews shown = 47 positive / 2 negative
```

### Client gives

The card explicitly requires:

```text
- client website URL;
- nearest competitor URLs are desirable but optional.
```

Our own intake must additionally confirm:

```text
- target region;
- priority products/services/categories;
- any exclusions or business boundaries.
```

The region is not stated in the card, but it is necessary for reproducible Yandex SERP discovery and regional Wordstat expansion.

### Advertised deliverable and evidence boundary

The seller promises **up to 300 keywords selected after analyzing the semantics of the nearest competitors**. The card does **not** promise:

```text
- Ahrefs / Keys.so / Semrush export;
- a complete list of every organic keyword a competitor ranks for;
- search volume or exact frequency columns;
- clustering;
- position data;
- a full-site crawl of every competitor;
- a specific XLSX/PDF schema.
```

No demo artifact or named competitor-data provider is supplied in the card. Therefore we must not silently reinterpret the service as an exhaustive external organic-keyword export. The paid outcome is the useful final keyword list, with competitor analysis as the acquisition method.

### Current Bridge + ChatGPT coverage

```text
client-site offer/topic analysis = YES
competitor domains supplied by client = YES
nearest Yandex competitor discovery when not supplied = YES through regional Search
bounded public competitor-page/category inspection = YES through ordinary ChatGPT/web work
competitor topic / product / modifier seed extraction = YES
Yandex Wordstat expansion from competitor-derived seeds = YES
regional Wordstat = YES
merge / normalize / dedupe = YES
relevance / intent filtering = YES
cross-competitor recurrence/coverage scoring = YES in analysis layer
final up-to-300 selection = YES
XLSX/CSV/list artifact = YES
external organic-ranking keyword database = NO, but not required by the card
full autonomous competitor crawler = NO, but not required by the bounded base contract
Direct / Metrika / Webmaster = NOT REQUIRED
```

The current Wordstat protocol provides `getTop` with one seed phrase, region IDs and up to 2,000 returned phrases. The current Search protocol can identify domains/pages in a target Yandex region and returns rank, URL, domain and title evidence after normalization. Together these are sufficient for a bounded competitor-derived 300-key job without an Ahrefs/Keys.so dependency.

### Exact operating workflow we can sell now

```text
1. Receive client site URL, target region, priority directions and optional competitor URLs.
2. Inspect the client's public offer/category structure and build a seed/topic map.
3. If competitor URLs were not supplied, run a small bounded set of representative regional Yandex searches and identify the nearest recurring commercial competitors.
4. Select a manageable competitor set, for example 3–10 genuinely relevant domains rather than arbitrary directories/aggregators.
5. Inspect public competitor home/category/service/landing pages relevant to the client's offer.
6. Extract recurring product/service nouns, synonyms, modifiers, use cases, category terms and commercial intents.
7. Build a competitor-derived seed map and record which competitor/topic supplied each seed.
8. Expand the strongest seeds through regional Wordstat `getTop` requests.
9. Persist each provider result before moving to the next paid request.
10. Merge all candidates, normalize phrase text and remove exact/semantic duplicates.
11. Remove phrases that are irrelevant to the client's actual offer, geography or business model even if competitors use them.
12. Score remaining candidates by client relevance plus competitor recurrence/topic coverage; Wordstat frequency may be used internally or included as a value-add, but is not required by the advertised card.
13. Select up to 300 useful keywords; do not pad a narrow niche to hit 300 artificially.
14. Deliver an XLSX/CSV/list with at minimum keyword and optional source/topic/frequency columns.
15. QA duplicates, relevance, competitor-source coverage, regional consistency and artifact readability.
```

### Why this is YES rather than PARTIAL

The phrase `проанализировав семантику ближайших конкурентов` does not by itself require a third-party ranking-keyword database. The seller does not name Keys.so, Ahrefs, Semrush or any equivalent data source and does not promise exhaustive ranking-keyword coverage.

We can honestly perform competitor semantic analysis from:

```text
client site + public competitor pages + regional Yandex SERP + Wordstat
```

and return the promised final list of up to 300 keywords end-to-end. That satisfies the source contract.

The service becomes `PARTIAL` only if a buyer adds a requirement such as:

```text
- export every competitor's organic ranking keywords;
- provide Keys.so/Ahrefs visibility/search-volume metrics;
- crawl a very large competitor estate exhaustively;
- reproduce a named third-party tool's dataset.
```

Those are richer requirements not present in this card.

### Commercial / product consequence

F-016 is an important signal because it monetizes **competitor-derived seed discovery** separately from plain Wordstat collection. A seller with more than 1,600 completed orders sells up to 300 selected keywords for **3,000 ₽** and usually completes the work in **11 hours**.

This suggests a reusable workflow:

```text
COMPETITOR-DERIVED SEMANTIC CORE
client site + region
→ competitor discovery / supplied competitors
→ public offer/category extraction
→ competitor seed map
→ Wordstat expansion
→ dedupe / client-fit filtering
→ recurrence/coverage scoring
→ final keyword set
```

Unlike TOP clustering, this workflow does not require hundreds of paid Search calls: competitor discovery can use a small bounded set of representative SERPs, while the bulk candidate expansion comes from Wordstat. That makes the displayed 3,000 ₽ / 300-key price much more compatible with our current provider economics than F-015's 1,000 ₽ / 500-key full TOP clustering.

Direct approval does not block this service.