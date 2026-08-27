# FREELANCE ORDER CAPABILITY MATRIX — Yandex Marketing Bridge

Status: **ACTIVE / PERMANENT PRODUCT-DISCOVERY AND SERVICE-COVERAGE AUTHORITY**  
Started: 2026-08-27

## 1. Purpose

This document converts real freelance-marketplace cards into a practical operating map:

```text
real freelance order
→ required client inputs
→ required final deliverable
→ can we complete it now?
→ exact Bridge/ChatGPT workflow
→ missing capability/provider if not
→ repeated market demand
→ future product priority
```

The target is to derive the sellable service catalog and the next product roadmap from real paid work rather than inventing features in isolation.

This is planning/evidence only. It does not authorize `extension/src` changes. While Phase 5 Direct owner-live is pending, this file remains on the QA branch and the frozen Direct product stays immutable.

## 2. Verdict rules

```text
YES
= we can accept the order now and return the promised final deliverable end-to-end.

PARTIAL
= substantial parts are possible, but at least one required provider/data/workflow is missing for the exact advertised service.

NO
= the core required data/action is unavailable with the current system.
```

Do not mark a card `YES` merely because an API call exists. `YES` means we can go from the client's inputs to the final artifact they paid for.

---

# 3. LIVE SELLABLE SERVICE COVERAGE

## READY NOW

| Case | Sellable service | Supported boundary | Execution |
|---|---|---|---|
| F-002 | SEO semantic core / keyword collection, up to 10,000 phrases | **Yandex Wordstat-based** collection. Google keyword-volume data is not promised. Base service does not include full automatic clustering. | Wordstat seed expansion → merge/deduplicate → intent filtering/tagging → XLSX/CSV |

## PARTIALLY COVERED

| Case | Service | What we already cover | Main blocker |
|---|---|---|---|
| F-001 | Rank tracking in Yandex + Google, up to 500 keywords | Yandex SERP/rank extraction + final XLSX | No Google organic SERP provider; no durable bulk rank-check job |
| F-003 | Ahrefs-based semantic core + clustering, up to 10,000 phrases / competitor research | Wordstat collection, Yandex SERP research, deduplication, semantic/intent clustering, spreadsheet/report production | No Ahrefs data source/provider for KD, Traffic Potential, Clicks and Ahrefs competitor datasets |

## NOT COVERED

```text
None recorded yet.
```

---

# 4. DEMAND-DERIVED CAPABILITY BACKLOG

This is not automatically an implementation roadmap. Repeated appearance across independent paid cards raises priority.

| Capability | Cases | Current state | Market signal |
|---|---|---|---|
| Bulk SERP / Rank Tracker orchestration | F-001 | Missing | HIGH |
| Google organic SERP provider | F-001 | Missing | HIGH |
| Yandex high-volume/deferred Search workflow | F-001 | Deferred from Phase 2 | HIGH candidate |
| Reusable rank-report XLSX builder | F-001 | Can be produced with artifact tooling; not productized | MEDIUM |
| Semantic Core Builder / Wordstat batch orchestration | F-002, F-003 | Can be orchestrated now; no dedicated batch job | **HIGH — repeated** |
| Seed expansion + deduplication + checkpoint/resume | F-002, F-003 | Operationally possible; not productized | **HIGH — repeated** |
| Semantic clustering / intent grouping | F-002 (optional scope), F-003 (core scope) | ChatGPT can perform it; no durable large-dataset clustering workflow | **HIGH — repeated** |
| Semantic-core XLSX/CSV/report builder | F-002, F-003 | Available through artifact tooling | HIGH reuse |
| Ahrefs data access / import/provider layer | F-003 | Missing | HIGH for Ahrefs/competitor SEO orders; confirm repetition |
| Competitor keyword/domain research workflow | F-003 | Partial via Yandex SERP; no Ahrefs corpus | HIGH candidate |

---

# 5. CASE RECORDS

## F-001 — Rank tracking in Yandex and Google, up to 500 keywords

**Marketplace:** Kwork  
**Category:** SEO / semantic core / rank tracking  
**Verdict:** `PARTIAL`

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
- numeric rank or "-" when not found
```

Two owner-supplied sample XLSX files confirmed that the artifact itself is simple. The hard part is reliable bulk SERP acquisition.

### What works now

Current `SEARCH_API_V1` can perform official Yandex web search with region control and request up to 100 result groups. Normalized results contain rank, URL and domain.

Therefore:

```text
Yandex one-key top-100 acquisition = YES
Yandex domain match / rank extraction = YES
XLSX generation = YES
Google rank acquisition = NO
500-key durable batch workflow = NOT PRODUCTIZED
```

### Missing

```text
1. Google organic SERP provider with verified ordinary-SERP fidelity, region targeting and depth >= 50.
2. Durable bulk rank-check job:
   keyword queue
   → provider request
   → target-domain match
   → checkpoint
   → resume without blind replay
   → final table.
3. Preferably a high-volume/deferred Yandex Search path for commercial bulk work.
```

### Target workflow after completion

```text
client domain + region + keyword list
→ normalize domain
→ create rank job
→ Yandex top-100 per keyword
→ Google top-50 per keyword
→ find first target-domain rank
→ checkpoint each completed unit
→ completeness QA
→ XLSX
→ deliver
```

### Direct dependency

```text
NONE
```

---

## F-002 — Detailed SEO semantic core for a website, up to 10,000 keywords

**Marketplace:** Kwork  
**Category:** SEO / semantic core from scratch  
**Verdict:** `YES — WITH YANDEX WORDSTAT AS DATA SOURCE`

### Client gives

```text
- topic / business direction
- desired query type: informational / commercial / both
- region
- optional site/category context
```

### Client expects

```text
- current relevant keyword phrases
- frequency data
- up to 10,000 phrases
- file suitable for SEO/site-structure work
```

The analyzed base card explicitly leaves final filtering to the client; grouping is a separate option. Therefore complete automatic clustering is not required for the base-service verdict.

### What works now

Current `WORDSTAT_API_V1` supports:

```text
method = getTop
one seed phrase per command
numPhrases = 1..2000
region filtering
current Wordstat result data
```

Several strong seed branches can therefore be expanded iteratively, merged and deduplicated until the requested relevant unique-key coverage is reached or the real niche is exhausted.

### Exact workflow available now

```text
1. Receive topic, intent and region.
2. Resolve Wordstat region ID.
3. Build initial seed map:
   categories / synonyms / products / services / commercial modifiers / informational modifiers.
4. Run explicit bounded Wordstat getTop commands for strong seeds.
5. Persist results/checkpoints.
6. Merge all phrases.
7. Normalize and deduplicate while preserving provider values.
8. Inspect uncovered semantic branches.
9. Use useful returned phrases as new seeds and repeat.
10. Stop when purchased relevant coverage is reached or the niche is genuinely exhausted.
11. Tag/filter informational vs commercial intent if required.
12. Produce XLSX/CSV.
13. Validate unique count, duplicates, region and artifact integrity.
14. Deliver.
```

Example command pattern:

```text
WORDSTAT_API_V1
{
  "method": "getTop",
  "phrase": "<seed>",
  "numPhrases": 2000,
  "regions": ["<REGION_ID>"],
  "devices": ["DEVICE_ALL"]
}
```

### Commercial boundary

Do not promise exactly 10,000 *relevant unique* phrases in a genuinely narrow niche. Do not pad the file with garbage solely to hit a numeric quota.

If the client explicitly requires Google keyword-volume data, this variant is no longer `YES` because we do not currently have that provider.

### Missing only for productization, not for accepting the work

```text
Semantic Core Builder / Wordstat Batch Orchestrator:
seed queue
→ Wordstat
→ unique set
→ expansion queue
→ checkpoint/resume
→ optional intent tagging
→ artifact builder
```

### Direct dependency

```text
NONE
```

---

## F-003 — Ahrefs-based semantic core analysis and clustering

**Marketplace:** Kwork  
**Category:** SEO / semantic core / competitor research  
**Advertised volume:** up to 10,000 keyword phrases and research of up to 100 competitor domains  
**Verdict:** `PARTIAL`

### Client gives

```text
- main business/topic direction
- up to 3 categories/sections
- ideally 1–3 competitors in the target region
- optional client site URL
```

### Client expects

The service is explicitly based on Ahrefs Keyword Explorer / competitor data and promises metrics such as:

```text
- Search Volume
- Keyword Difficulty (KD, 0–100)
- Traffic Potential
- Clicks
- semantic keyword set / cluster analysis
- research of competitors/domains
- Google Sheets or Ahrefs-format/report deliverable
```

### Why this is not READY NOW

The exact advertised value depends on **Ahrefs-owned data**.

Our current providers do not supply equivalent metrics:

```text
Yandex Wordstat frequency ≠ Ahrefs Search Volume
Yandex Search SERP ≠ Ahrefs Keyword Difficulty
Yandex Search SERP ≠ Ahrefs Traffic Potential
Yandex Search SERP ≠ Ahrefs Clicks
current Bridge ≠ Ahrefs competitor keyword database
```

We must not fabricate or approximate Ahrefs fields and label them as Ahrefs data.

### What we can already do

Even without Ahrefs, much of the processing layer already exists conceptually:

```text
Yandex Wordstat keyword expansion = YES
Yandex regional SERP research = YES
competitor discovery from Yandex SERP = YES, bounded by collected SERPs
merge / normalization / deduplication = YES
semantic intent classification = YES
semantic clustering by phrase meaning = YES
spreadsheet/report production = YES
```

If the owner/client supplies a genuine **Ahrefs export** containing the required metrics, ChatGPT can process that supplied dataset:

```text
import Ahrefs export
→ validate columns/rows
→ normalize/deduplicate
→ classify intent
→ cluster phrases
→ compare competitors/categories
→ preserve KD/Volume/TP/Clicks as source data
→ summarize clusters
→ produce Google-Sheets-compatible XLSX/CSV/report
```

That would allow the **analysis/clustering portion** without a direct Ahrefs Bridge integration, because acquisition has been supplied externally.

### What is missing for the exact turnkey service

#### A. Ahrefs data acquisition

Need one governed source of real Ahrefs data:

```text
option 1: owner-operated Ahrefs subscription + exports
option 2: official Ahrefs API/provider integration if commercially/technically available for the required datasets
```

Before any integration we would need to verify current Ahrefs plan/API terms, limits, available endpoints, cost and permitted automation. No Ahrefs credential/provider exists in the Bridge today.

#### B. Large semantic clustering workflow

ChatGPT can cluster data, but 10,000 rows should not rely on one giant prompt. A reusable workflow should provide:

```text
input dataset
→ normalization
→ duplicate/near-duplicate control
→ deterministic chunking
→ intent classification
→ lexical/semantic pre-groups
→ optional SERP evidence per group
→ cluster merge/reconciliation
→ cluster IDs/names
→ quality checks for split/merged intent
→ checkpoint/resume
→ final spreadsheet
```

This is now a repeated market signal because semantic clustering also appeared as an optional extension to F-002.

#### C. Competitor dataset workflow

The advertised scale says up to 100 competing domains. For an Ahrefs-equivalent service we need a structured pipeline for:

```text
competitor domains
→ their ranking keywords/pages from Ahrefs source
→ overlap/gap analysis
→ unique keyword opportunities
→ cluster assignment
→ metrics aggregation
```

Yandex SERP can help identify real competitors but does not replace the Ahrefs historical/ranking-keyword corpus.

### Exact workflow after Ahrefs data access is available

```text
1. Receive main direction, up to 3 sections, competitors and optional client URL.
2. Define target country/region and search intent boundary.
3. Collect Ahrefs Keyword Explorer data for seed topics.
4. Collect Ahrefs competitor keyword/page data for selected relevant competitors.
5. Union datasets with source provenance.
6. Normalize phrases and remove duplicates while preserving Ahrefs metrics.
7. Filter obvious irrelevant/mismatched intent phrases.
8. Classify informational/commercial/navigational intent as required.
9. Cluster up to the purchased volume using deterministic chunk/checkpoint workflow.
10. Reconcile clusters and optionally map them to sections/landing-page candidates.
11. Aggregate useful cluster metrics without inventing missing provider values.
12. QA rows, metrics, cluster membership, duplicates and source coverage.
13. Produce Google-Sheets-compatible XLSX/CSV or agreed Ahrefs-style report.
14. Deliver with a short explanation of columns and cluster logic.
```

### Alternative service we could sell today

We **can** offer a different product now:

```text
"Семантическое ядро и кластеризация на основе Яндекс Wordstat + анализа Яндекс SERP"
```

But that is **not** the same as advertising an Ahrefs-based report with KD / Traffic Potential / Clicks.

### Direct dependency

```text
NONE
```

### Product signal generated by F-003

```text
Ahrefs/importable external SEO-data layer = HIGH candidate
semantic clustering workflow = HIGH and now repeated
competitor keyword-gap workflow = HIGH candidate
```

---

# 6. HOW THIS MATRIX WILL BE USED

After a sufficiently broad card sample, derive three concrete project outputs:

```text
A. SELLABLE SERVICE CATALOG
   only services with verdict YES and their exact commercial boundaries.

B. STANDARD OPERATING PROCEDURES
   client inputs
   → Bridge/API commands
   → analysis
   → artifact
   → QA
   → delivery.

C. NEXT PRODUCT ROADMAP
   missing capabilities ranked by how many real paid order types they unlock.
```

The desired final logic is:

```text
freelance order type
→ can we accept it?
→ what do we ask from client?
→ exact execution steps
→ provider/API cost and limits
→ manual work remaining
→ final deliverable
→ missing capability if blocked
```
