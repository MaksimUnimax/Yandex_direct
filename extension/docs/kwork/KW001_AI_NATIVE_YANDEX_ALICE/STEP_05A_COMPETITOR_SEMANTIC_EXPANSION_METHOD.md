# KW-001 — STEP 5A COMPETITOR SEMANTIC EXPANSION METHOD

Updated: 2026-09-08  
Status: **APPROVED / ACTIVE / PROJECT-TEST-VALIDATED / OWNER-CANONIZED PERMANENT METHOD**

## 1. Purpose

Step 5A exists to reduce semantic blind spots left by the client's/site's own starting vocabulary without turning KW-001 into a deep competitor SEO audit.

Canonical client-facing meaning:

```text
ПРОВЕРКА СЕМАНТИКИ ПО РЕАЛЬНЫМ КОНКУРЕНТАМ В ЯНДЕКСЕ
=
найти реальные поисковые конкуренты
→ использовать их реально ранжирующиеся страницы как дополнительный источник тем/seeds
→ раскрыть эти новые темы через Wordstat
→ проверить найденные запросы в текущей выдаче Яндекса
→ добавить только подтверждённые релевантные запросы в общее ядро
```

This is an acquisition/coverage-expansion stage. It happens after the initial Wordstat acquisition/targeted expansion and before the semantic set is finally cleaned/frozen for downstream clustering and page ownership.

## 2. Core claim boundary

The method must never confuse three different facts:

```text
COMPETITOR PAGE CONTAINS / TARGETS A TOPIC
!=
COMPETITOR RANKS FOR AN EXACT QUERY
!=
WE HAVE ENUMERATED THE COMPETITOR'S FULL ORGANIC KEYWORD UNIVERSE
```

Public competitor pages can produce candidate topics/seeds.

Yandex Wordstat can show whether real search demand exists around those seeds and return popular containing/similar queries.

Current Yandex Search evidence can show whether a competitor is actually present for a tested exact query and which URL/page type is returned.

Without an external reverse-domain visibility database or an independently maintained equivalent index, KW-001 must not claim that it has recovered every query for which a competitor ranks.

## 3. Method origin and direct sources

### OFFICIAL — Yandex Wordstat

Direct source:

https://yandex.ru/support2/wordstat/en/content/api-structure

Supported claim:

`/v1/topRequests` returns popular queries containing the specified phrase and queries similar to it, with regional/device controls. Therefore a competitor-derived candidate phrase can legitimately be used as a new acquisition probe rather than treated as a final keyword by itself.

### OFFICIAL — Yandex Search API

Direct source:

https://yandex.cloud/ru/services/search-api

Supported claim:

Yandex Search API provides responses from Yandex's search base and explicitly supports SEO/semantic-core use cases. Therefore current query → returned domain/URL/page-type observations are an executable Yandex-native evidence route.

### INDUSTRY_PRACTICE — identify organic competitors from search results

Direct source:

https://www.semrush.com/blog/how-to-do-seo-competitive-analysis/

Supported claim:

SEO competitors can be identified from the sites that repeatedly appear for relevant search queries; direct business rivals and organic-search competitors are not necessarily identical. The same source recommends examining competitor keyword footprints and winning pages.

### INDUSTRY_PRACTICE — competitor keyword/content gaps

Direct sources:

https://www.semrush.com/blog/competitor-keywords/
https://help.ahrefs.com/en/articles/9025740-how-to-use-content-gap-to-find-keyword-ideas-from-competitor-websites

Supported claim:

Keywords/topics competitors rank for but the target does not are a standard source of new SEO/content opportunities. These sources describe reverse-domain databases as one way to obtain the gap; KW-001 does not make such a database mandatory.

### PROJECT-SPECIFIC ADDITION — VALIDATED PERMANENT ORCHESTRATION

The exact low-cost KW-001 loop:

```text
ranked competitor page
→ candidate topic/seed extraction
→ Wordstat expansion
→ Yandex Search recheck
→ merge into shared semantic acquisition layer
```

is a project-specific execution design. External sources support the individual evidence mechanics and the value of competitor gaps, but they do not define this exact Yandex-only orchestration.

The orchestration has now passed an owner-accepted varied project execution and is therefore approved as the permanent Step 5A workflow for KW-001. Future jobs still require current job evidence, bounded acquisition, preserved provenance and all claim boundaries in this method. Project-test validation of the workflow does **not** establish a universal numeric saturation threshold for every market or site.

## 4. Inputs

Required:

```text
frozen client/business scope
region
initial acquired semantic set from Step3/Step5
current site/business model or new-site business model
current Yandex Search access route
Wordstat access route
```

Optional:

```text
client-supplied competitor names
external reverse-domain visibility export/provider
owned Webmaster data for the client's own domain
```

Client-supplied competitors are hints, not automatic SEO-competitor truth.

External reverse-domain data is optional enrichment, not a base-package dependency.

## 5. Execution sequence

### 5A.1 — Discover real search competitors

Use representative in-scope query families from the acquired semantic set and current regional Yandex Search evidence.

Record returned domains/URLs and identify domains that recur across materially different relevant query families.

Classify each candidate at minimum as:

```text
DIRECT_BUSINESS_COMPETITOR
ORGANIC_COMPETITOR_OTHER_MODEL
AGGREGATOR_DIRECTORY
MARKETPLACE
MANUFACTURER_OR_BRAND_SOURCE
INFORMATIONAL_PUBLISHER
OTHER_REVIEW
```

The classification is used only to decide whether the domain is an appropriate seed source for the client's business scope. It must not be presented as an official Yandex taxonomy.

Do not freeze a universal numeric competitor-count threshold. Start bounded and expand only while new material semantic information is still being added.

### 5A.2 — Inspect evidence-bearing competitor pages

Prefer competitor URLs that actually appeared in the current Yandex results used for discovery.

For those pages, record only the public elements needed to discover additional demand directions:

```text
competitor domain
competitor URL
query that exposed the URL
observed result position/order
page type
Title/H1 when available
topic/product/service/use-case axes
material subtopics / headings / navigation directions
observation date
```

This is not a technical SEO audit. Do not add backlink analysis, Core Web Vitals, schema, ad creatives, review audit or other deep-competitor-audit scope unless separately sold/authorized.

### 5A.3 — Derive candidate competitor seeds

Compare competitor-page topics with the already acquired semantic directions.

A new seed must have explicit lineage:

```text
candidate seed
← competitor domain
← competitor URL
← Yandex query/result observation that exposed the page
← exact page/topic element that motivated the seed
```

Canonical rule:

```text
COMPETITOR-DERIVED SEED != ACCEPTED KEYWORD
```

Do not infer that the competitor ranks for the seed merely because the seed wording appears on the page.

### 5A.4 — Expand missing candidate seeds through Wordstat

Run only genuinely new/information-gaining competitor-derived seeds through the same bounded Wordstat acquisition discipline as Step3/Step5.

Persist every returned occurrence using the same union-compatible acquisition schema required by Step3/Step5, including demand/provenance/region/device/operator/request/timestamp/raw-evidence/completeness fields.

Canonical rule:

```text
COMPETITOR ACQUISITION IS ANOTHER LINEAGE INTO THE SAME CORE
!=
A SEPARATE DECORATIVE COMPETITOR SPREADSHEET
```

### 5A.5 — Filter business/scope noise

Competitor-derived demand is not automatically relevant to the client.

Reject or hold phrases/topics that are clearly outside the frozen business scope, geography or supported offer.

Do not use competitor presence as a substitute for business truth.

### 5A.6 — Recheck material new candidates in Yandex Search

For materially new candidate queries/families, obtain current regional Yandex Search evidence sufficient to determine:

```text
whether selected competitors actually appear for the tested query
which competitor URLs rank/appear
what page types dominate
whether the observed intent is compatible with the client's business/search job
```

This recheck is what supports the statement `competitor is visible for tested query X`.

If current Search evidence does not support the claim, do not retain a ranking claim merely because the competitor page discussed the topic.

### 5A.7 — Decision and merge

Every material competitor-derived candidate reaches one executable outcome:

```text
ADD_TO_PIPELINE
= relevant demand + sufficient evidence; merge into the common semantic pipeline

ALREADY_COVERED
= competitor evidence confirms an existing semantic direction; no duplicate addition

REJECT_OFF_SCOPE
= conflicts with frozen business/scope/region

HOLD_EVIDENCE
= potentially relevant but current evidence is insufficient for a stronger decision
```

These are project routing states, not provider facts.

Confirmed additions proceed into the same downstream cleanup, freeze, clustering, page-ownership, Search-only architecture and Alice comparison stages as all other acquired phrases.

### 5A.8 — Stop on diminishing information gain

Do not crawl competitors or generate recursive Wordstat seeds indefinitely.

Stop when additional competitor pages/domains mostly repeat already known semantic directions or add noise rather than material new in-scope demand.

No universal numeric saturation threshold is authorized. Each job must use an explicit bounded information-gain stop assessment. Future varied executions may refine a reusable stopping heuristic, but the absence of a universal number does not block the approved Step 5A method.

## 6. Modes

### EXISTING_SITE_REBUILD

Compare competitor-derived candidates against:

```text
current acquired semantic set
existing public page/business model
owned query evidence when legitimately available
```

A missing keyword/topic does not automatically justify a new page; downstream page-ownership evidence still decides that.

### NEW_SITE

Use the frozen business model + initial Wordstat semantic set as the target baseline.

Competitor-derived candidates can expose missed demand directions before the planned architecture is frozen.

No own-domain ranking history is required.

## 7. Required outputs

A Step5A execution must produce equivalent durable records for:

```text
COMPETITOR_DISCOVERY_REGISTER
COMPETITOR_PAGE_EVIDENCE_REGISTER
COMPETITOR_DERIVED_SEED_REGISTER
COMPETITOR_WORDSTAT_OCCURRENCE_LAYER
COMPETITOR_QUERY_VISIBILITY_MATRIX
COMPETITOR_GAP_DECISION_REGISTER
MERGE_RECONCILIATION
```

Names are not required to be literal filenames, but the information must exist durably and be traceable.

Client-facing materialization should expose the useful result in plain Russian, for example:

```text
Конкуренты и найденные пропуски
```

The client view should explain:

```text
which real search competitors were examined
which additional demand directions they exposed
which new Wordstat queries were found
which competitor/query relationships were actually confirmed in current Yandex results
which candidates were added / already covered / rejected / held
which later clusters/pages changed because of this evidence
```

The recipient-ready view must expose material accepted phrases and concrete tested query → competitor → observed position evidence when those facts exist; summary counts alone are not sufficient for the usefulness gate.

## 8. Explicit non-goals

Step5A does not promise:

```text
full reverse-domain keyword enumeration
full competitor SEO audit
backlink audit
technical SEO audit
traffic estimation
revenue estimation
proof that a competitor receives clicks/leads from an observed ranking
proof that every competitor page is successful
automatic page creation for every competitor topic
```

## 9. Source-to-method trace

| Method element | Source/evidence | What it supports | Project-specific part | Executable output |
|---|---|---|---|---|
| Find organic competitors from relevant SERPs | Semrush SEO competitor analysis | Search competitors are domains repeatedly competing on relevant search results | Use current regional Yandex Search rather than a mandatory Semrush provider | competitor discovery register |
| Use competitor winners to discover missed directions | Semrush competitor analysis / competitor keyword guidance | Competitor keyword footprints and winning pages reveal gaps/opportunities | Extract candidate seeds from public evidence-bearing pages | competitor-derived seed register |
| Expand a seed into real Yandex demand | Official Yandex Wordstat API | containing + similar query discovery with regional/device controls | preserve competitor lineage into existing acquisition schema | Wordstat occurrence layer |
| Confirm exact query ↔ competitor visibility | Official Yandex Search API | executable current Yandex search-result evidence | interpret returned order/domain/URL for the tested query | query visibility matrix |
| Merge accepted candidates into main semantic pipeline | Step3/Step5 durability rules | collect once / preserve completely / union-compatible acquisition | competitor source becomes another lineage, not a separate truth silo | merge reconciliation |
| External reverse-domain database remains optional | Product boundary + industry gap sources | such databases are one route to competitor keyword gaps | base KW-001 remains executable without them | no mandatory external-provider dependency |
| Stop on diminishing information gain | Project-specific heuristic | no authoritative universal threshold found | bounded job-level information-gain stop assessment; future varied executions may refine reusable heuristics | explicit stop rationale |

## 10. Failure classes and non-repeat controls

### Failure A — competitor-site text treated as ranking evidence

Control:

```text
PAGE TOPIC != EXACT QUERY RANKING
```

Exact tested ranking/visibility claims require current Search evidence.

### Failure B — competitor ranking treated as automatic keyword acceptance

Control:

```text
COMPETITOR SIGNAL
+ BUSINESS/SCOPE FIT
+ WORDSTAT DEMAND
+ SEARCH INTENT EVIDENCE WHEN MATERIAL
→ ADD / HOLD / REJECT
```

### Failure C — competitor expansion becomes endless recursive collection

Control: every seed must state explicit information gain; stop on diminishing material novelty.

### Failure D — competitor acquisition loses provenance during merge

Control: union-compatible Step3/Step5 occurrence persistence with competitor lineage retained.

### Failure E — deep competitor audit silently enters base package

Control: inspect only evidence required for semantic expansion; deep technical/link/traffic analysis is outside Step5A.

### Failure F — third-party provider becomes a hidden required dependency

Control: base method is executable with public competitor pages + Wordstat + Yandex Search; reverse-domain sources remain optional enrichment.

### Failure G — accepted competitor-derived additions are left outside the main pipeline

Control: every `ADD_TO_PIPELINE` occurrence must be merged into the same downstream cleanup/freeze/clustering/ownership chain as ordinary acquisition before the next real release. A competitor worksheet is evidence/materialization, not an alternate semantic truth silo.

### Failure H — client receives only aggregate counts instead of inspectable result

Control: recipient-facing materialization must expose the material new directions/phrases and concrete tested competitor visibility facts at the depth needed to understand what was actually found and why it matters.

## 11. Permanent project-test validation gate

Step 5A has earned `PROJECT_TEST_VALIDATED / APPROVED ACTIVE` status through an owner-accepted varied execution. The following ten conditions remain permanent regression gates for future material changes to the method:

```text
real-search-competitor discovery works in the target region
competitor page → seed lineage is durable
Wordstat expansion adds measurable candidate coverage or explicitly proves no material gap
returned Wordstat rows are fully preserved under Step3/Step5 schema
material new candidates receive correct Search confirmation/HOLD routing
website-text-as-ranking overclaim = 0
full-competitor-keyword-universe overclaim = 0
merge counts reconcile
external reverse-domain provider required for base execution = false
client-facing competitor-gap result is understandable and materially useful
```

Permanent state:

```text
ROADMAP_STAGE_EXISTS = true
OWNER_AUTHORIZATION_TO_ADD_STAGE = true
EXTERNAL_METHOD_RESEARCH = complete
PROJECT_TEST_VALIDATED = true
OWNER_CLIENT_USEFULNESS_GATE = accepted
FULL_PERMANENT_METHOD_PROMOTION = APPROVED_ACTIVE
PERMANENT_DIMINISHING_GAIN_THRESHOLD_VALIDATED = false
```

The proof that earned promotion belongs in Level2 rehearsal evidence and Git history; concrete case domains, counts, costs and phrases must not become permanent Level1 inputs.

A future material change to the Step 5A mechanics must re-run the affected regression gates and preserve the same claim boundaries. The approved method does not authorize recursive competitor crawling, mandatory third-party reverse-domain providers, automatic page creation, or bypassing downstream semantic processing.