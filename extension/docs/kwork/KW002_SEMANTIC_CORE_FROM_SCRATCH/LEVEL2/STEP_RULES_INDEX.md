# KW-002 — LEVEL 2 STEP RULES INDEX

Status: **DRAFT FOR OWNER REVIEW / DO NOT EXECUTE YET**  
Product: from-scratch semantic core + clustering + planned site architecture for modern Yandex.

Level 2 contains universal rules for each execution step. Concrete Blood & Sand data belongs only in `work/BLOOD_SAND_GREENFIELD_2026-09-08/`.

## Global execution order

```text
00 scope freeze
01 business/assortment model
02 seed map
03 primary Wordstat acquisition
04 first family triage
05 targeted expansion / coverage control
06 current Yandex competitor discovery
07 competitor semantic expansion
08 competitor-derived Wordstat expansion
09 candidate semantic master freeze
10 row-level cleanup + intent + user job
11 Search-stage semantic freeze
12 ordinary Yandex Search batch acquisition
13 SERP + task-first clustering
14 query→page ownership + Search-only IA freeze
15 AI-search diagnostic selection
16 AI-search evidence acquisition
17 Search-vs-AI reconciliation
18 final semantic core + site IA + Page Jobs + internal-link model
19 client deliverables
20 final QA / recipient acceptance
21 revision rehearsal + Kwork productization measurement
22 job close
```

No step may be silently skipped because a later step appears to contain similar data.

---

# STEP 00 — order / scope / source freeze

### Purpose

Make the order reproducible before research can influence the brief.

### Inherited KW-001 rule

`scope freeze before evidence acquisition`.

### Required actions

Freeze:

```text
business description
region
actual assortment/services
commercial goal
business exclusions
site state
allowed input sources
sealed/prohibited sources
order-specific deliverable scope
```

### Output

`JOB_MANIFEST.md` + frozen brief/source whitelist.

### PASS

No unresolved ambiguity that would change what business or geography is being researched.

---

# STEP 01 — business and assortment model

### Purpose

Understand what can genuinely be sold/represented before inventing search vocabulary.

### Method

Build a neutral model:

```text
products/services
families/categories
attributes
uses/problems solved
selection dimensions
commercial actions
known exclusions
```

Do not use prior SEO research as a shortcut in a greenfield rehearsal.

### Output

`BUSINESS_AND_ASSORTMENT_MODEL`.

### PASS

Every seed family in Step 02 can trace to an actual offer/use/business boundary.

---

# STEP 02 — seed / acquisition probe map

### Purpose

Create probes for discovering demand, not a fake final keyword list.

### Inherited KW-001 rule

```text
SEED != FINAL KEYWORD
SEED != FINAL PAGE TARGET
```

A seed may be broad or diagnostic if it is useful for discovering a real demand family.

### Required seed dimensions

Where relevant:

```text
head product/service terms
synonyms / common naming variants
category/family terms
use-case terms
selection/comparison terms
commercial modifiers
problem/question terms
attribute/material/form-factor terms
brand terms only as a separate class
```

### Output

`SEED_MAP` with purpose and business lineage for each seed.

### PASS

Coverage is broad enough to probe the business without claiming completeness.

---

# STEP 03 — primary Wordstat acquisition

### Purpose

Acquire current Yandex human-demand evidence from the seed map.

### Inherited KW-001 rules

```text
provider success != collection completion
preserve complete result required by the step
preserve seed/region/provenance for every occurrence
one returned phrase may occur under multiple seeds; do not destroy provenance early
```

### Official source

`https://yandex.ru/support2/wordstat/ru/`

Operators, when deliberately needed:

`https://yandex.ru/support2/wordstat/ru/content/operators`

### Bridge

Use durable Wordstat batch/provider jobs. Technical batch size is not a product limit.

### Output

Complete raw primary Wordstat occurrence table(s).

### PASS

Every authorized seed has known terminal/acquisition status and complete preserved required payload.

---

# STEP 04 — first family triage

### Purpose

Understand what demand families exist and where collection is obviously noisy or incomplete before row-level cleanup.

### Inherited KW-001 rules

```text
FAMILY TRIAGE != FINAL ROW CLEANUP
LOW FREQUENCY ALONE != IRRELEVANCE
```

### Actions

Classify observed families approximately as:

```text
strong in-scope
plausible in-scope
mixed/ambiguous
obvious out-of-scope
coverage gap / requires expansion
```

### Output

`FAMILY_TRIAGE` + targeted-expansion queue.

### PASS

No family is permanently rejected solely on a superficial token/frequency rule.

---

# STEP 05 — targeted expansion / coverage control

### Purpose

Close obvious vocabulary holes created by initial seed choice.

### Inherited KW-001 boundary

A second acquisition must use the same union-compatible evidence/provenance model as primary acquisition.

### Possible evidence routes

```text
new synonyms/naming variants discovered in Wordstat
promising related-query branches
missing business families
regional/dynamics checks when they affect scope/priority
owner/client clarification when a business boundary is unclear
```

### Stopping rule

Stop when another acquisition branch has low expected information gain, not because an arbitrary fixed number of seeds was reached.

### Output

Targeted Wordstat additions merged without losing provenance.

---

# STEP 06 — current Yandex competitor discovery

### Purpose

Find actual search competitors for observed demand, not merely businesses the client calls competitors.

### Method

Use representative in-scope query families in current ordinary Yandex Search and record:

```text
query
region/time
ranked domains/URLs
page/result type
recurrence of domains across families
```

### Rule

```text
BUSINESS RIVAL != SEARCH COMPETITOR
```

### Output

`SEARCH_COMPETITOR_REGISTRY` with reasons each domain was selected for semantic inspection.

---

# STEP 07 — competitor semantic expansion

### Purpose

Discover vocabulary/topics missed by our own starting language.

### Transferred KW-001 Step 5A rules

```text
COMPETITOR PAGE TOPIC != EXACT QUERY RANKING
COMPETITOR RANKING != AUTOMATIC KEYWORD ACCEPTANCE
COMPETITOR-DERIVED SEED != FINAL KEYWORD
TESTED QUERY VISIBILITY != FULL COMPETITOR KEYWORD UNIVERSE
```

### Method

```text
real recurring Yandex competitor
→ inspect evidence-bearing relevant public pages
→ extract candidate missed topics/seeds
→ compare against already acquired semantic universe
→ only genuinely new candidates continue
```

This is semantic coverage research, not a full competitor SEO audit and not a substitute for a reverse-domain database.

### Output

`COMPETITOR_DERIVED_SEED_CANDIDATES` with source URL and topic evidence.

---

# STEP 08 — competitor-derived Wordstat expansion

### Purpose

Test whether competitor-derived topics correspond to real Yandex demand.

### Rule

```text
PUBLIC PAGE TOPIC
MUST RETURN TO DEMAND EVIDENCE
BEFORE IT CAN ENTER THE FINAL CORE AS SEARCH DEMAND
```

### Method

Run new candidate seeds through Wordstat under the same persistence/provenance rules as Step 03.

### Output

Competitor-derived Wordstat occurrences + candidate decisions:

```text
NEW_DEMAND
ALREADY_COVERED
NO_USEFUL_DEMAND
OUT_OF_SCOPE
HOLD
```

---

# STEP 09 — candidate semantic master freeze

### Purpose

Create one auditable pre-cleanup universe before subjective row-level decisions.

### Inherited KW-001 rule

Do not silently lose demand/provenance fields at semantic freeze boundaries.

### Master must preserve

```text
phrase
all acquisition sources/seeds
region
provider demand fields
occurrence lineage
competitor-derived lineage if applicable
status/errors
```

### Output

`CANDIDATE_SEMANTIC_MASTER`.

---

# STEP 10 — row-level cleanup + intent + user job

### Purpose

Decide which phrases genuinely belong to the client business and what users are trying to do.

### Transferred KW-001 rules

```text
NO DEFAULT KEEP
POSITIVE IN-SCOPE EVIDENCE REQUIRED
ACCOUNTING QA != SEMANTIC QA
UNCERTAINTY STAYS EXPLICIT
```

### Every row receives

```text
KEEP / REJECT / HOLD
relevance reason
user task/job
intent class or mixed intent
commercial/informational role
business-fit state
frequency/demand evidence
primary/secondary candidate state where useful
```

### Important

Intent is not determined mechanically only by words such as `купить`, `цена`, `что такое`. Current SERP evidence in later steps can refine the judgment.

### Output

`CLEANED_SEMANTIC_MASTER`.

---

# STEP 11 — Search-stage semantic freeze

### Purpose

Freeze the exact retained semantic set that will receive structural/Search evidence.

### Inherited KW-001 rule

Every retained phrase must have deterministic lineage back to demand/provenance evidence. Silent field loss = FAIL.

### Output

`SEARCH_STAGE_SEMANTIC_SET`.

This is not yet final clustering or IA.

---

# STEP 12 — ordinary Yandex Search batch acquisition

### Purpose

Acquire current SERP evidence needed for clustering and page-boundary decisions.

### Bridge capability

Use the accepted ordinary Search batch hand and split large final sets across multiple jobs when a single technical job limit is reached.

### No product cap

```text
SEARCH_BATCH_JOB_LIMIT != KW002 FINAL-CORE LIMIT
```

### Preserve for each query

```text
query
region/time
ranked URLs/domains/titles
result/page types where analytically derived
provider/job provenance
```

### Output

Complete persisted Search batch evidence for the authorized set.

---

# STEP 13 — SERP + task-first clustering

### Purpose

Determine which retained phrases should be served by the same page and which require separate page jobs.

### Transferred KW-001 clustering rules

```text
TASK-FIRST CORE
SERP OVERLAP = EVIDENCE, NOT AUTOMATIC VERDICT
NO UNIVERSAL MAGIC OVERLAP THRESHOLD
MIXED INTENT MUST REMAIN VISIBLE
```

### External corroboration

- Ahrefs: `https://ahrefs.com/blog/keyword-clustering/`
- Semrush: `https://www.semrush.com/blog/keyword-clustering/`

### Inputs

```text
semantic meaning
user job
intent
current ranked URLs/domains/page types
SERP overlap/jaccard/containment projections
business/assortment boundaries
```

### Work rule

Large pairwise/cluster analysis is a mandatory Work candidate. Do not reduce the dataset to a representative sample merely because pair count is large.

### Output

`CLUSTER_MASTER` with member coherence and split/merge reasoning.

---

# STEP 14 — query→page ownership + Search-only IA freeze

### Purpose

Turn clusters into a planned site architecture before AI-search evidence can influence it.

### Transferred KW-001 rules

```text
one cluster must have an explicit primary page owner
cluster ownership != merely mentioning the phrase on many pages
target page != observed competitor/current relevant URL
SEARCH-ONLY ARCHITECTURE MUST BE FROZEN BEFORE AI COMPARISON
```

### For a greenfield site assign

```text
planned page/unit ID
page type
working URL/slug candidate
parent section
primary cluster
secondary clusters/queries
user job
commercial/informational/hybrid role
supporting-page relationships
```

### Output

`SEARCH_ONLY_QUERY_PAGE_MAP` + `SEARCH_ONLY_IA`.

---

# STEP 15 — AI-search diagnostic selection

### Purpose

Select the smallest sufficient set of cases that can reveal whether generative Yandex changes or de-risks Search-only page decisions.

### Transferred KW-001 rules

```text
DIAGNOSTIC SET != REPRESENTATIVE OF EVERY QUERY BY DEFAULT
SELECT FOR DECISION VALUE, NOT DECORATION
STABILITY/CONTROL CASES SEPARATE FROM CHANGE-CANDIDATE CASES
```

Select cases across material boundaries such as:

```text
commercial vs informational
broad root vs explanatory query
mixed-intent family
cluster split/merge boundary
source-quality-sensitive topic
selection/comparison task
```

### Output

`AI_SEARCH_CASE_REGISTER` with explicit reason for each case.

---

# STEP 16 — AI-search evidence acquisition

### Purpose

Observe the generative Yandex search surface relevant to the selected cases.

### Claim boundary

```text
GENSEARCH/STRUCTURED AI-SEARCH EVIDENCE != GUARANTEED CONSUMER ALICE STATE FOREVER
ONE AI ANSWER != STABLE UNIVERSAL TRUTH
SOURCE ORDER != RANKING
```

Preserve:

```text
query/case
observation surface/provider mode
answer/user-job orientation
source domains/types
used-source truth where exposed
search-query expansion themes where exposed
commercial vs explanatory orientation
raw/durable evidence reference
```

### Output

`AI_SEARCH_EVIDENCE_REGISTER`.

---

# STEP 17 — Search-vs-AI reconciliation

### Purpose

Measure whether AI-search evidence changes the Search-only semantic/page architecture.

### Transferred KW-001 rule

Every case preserves:

```text
selection reason
frozen Search-only baseline
evidence comparison
verdict
downstream effect
```

Allowed verdicts:

```text
NO_CHANGE
DE_RISK
ENRICH_PAGE_JOB
SPLIT_SUPPORTED
MERGE_SUPPORTED
PRIORITY_CHANGE
HOLD / INSUFFICIENT
```

### Rule

Do not force an AI delta. Supported `NO_CHANGE` is a valid client-visible result.

### Output

`SEARCH_AI_RECONCILIATION` and explicit mutation list against Search-only IA.

---

# STEP 18 — final semantic core + IA + Page Jobs + internal-link model

### Purpose

Materialize the final site-ready semantic architecture after reconciliation.

### Final page/unit record should include

```text
page/unit ID
working URL/slug candidate
parent/section
page type
Page Job in plain language
primary cluster/query
secondary queries
intent mix
supporting pages
internal-link relationships
required product/category content scope
important evidence/uncertainty notes
semantic priority (analytical, not implementation schedule)
```

### Final phrase record should include

```text
phrase
frequency/demand evidence
cluster
primary page owner
intent/user job
source/provenance
Search evidence status
AI-search relevance/delta state where applicable
KEEP/HOLD state
notes
```

### Rule

Do not create thin pages merely because a micro-query exists. Do not merge materially different user jobs merely to reduce page count.

### Output

Canonical final truth feeding all client artifacts.

---

# STEP 19 — client deliverables

### Purpose

Turn canonical truth into artifacts the commissioner can use without reading internal evidence logs.

### Transferred KW-001 packaging rules

```text
ONE CURRENT TRUTH FEEDS ALL VIEWS
CORRECT DATABASE != CLIENT-USABLE WORKBOOK
INTERNAL TRACEABILITY != CLIENT NARRATIVE
```

Expected artifact classes for the first rehearsal:

```text
1. standalone semantic core workbook
2. clusters + query→page map
3. planned site structure / IA
4. Page Jobs + internal-link map
5. competitor semantic-gap evidence summary
6. Search-vs-AI decision summary
7. plain-Russian client report / handoff
```

Exact final package is frozen after the rehearsal proves what is useful and commercially viable.

---

# STEP 20 — final QA / recipient acceptance

### Purpose

Verify both data correctness and usefulness of each promised artifact.

### Transferred KW-001 rules

```text
PACKAGE PASS != EVERY ARTIFACT PASS
DATA QA != WORKBOOK QA != RECIPIENT-USABILITY QA
RENDER/OPEN PASS != CONTENT COMPLETENESS
```

Check at minimum:

```text
no silent missing retained rows
no unexplained duplicate rows
region/provenance correct
all important clusters have page owners
no unexplained competing page owners
all planned pages have Page Jobs
Search/AI claim scopes correct
competitor-derived phrases have demand lineage
HOLD/uncertainty visible
workbooks open and are understandable
client-facing language explains completed work and result
```

### Output

`FINAL_QA` with per-artifact verdicts.

---

# STEP 21 — revision rehearsal + Kwork productization measurement

### Purpose

Prove the service can handle a realistic client correction without restarting unrelated paid work and measure whether the product is sellable.

### Revision test examples

```text
client removes one product family
client corrects geography
client says an assumed service/product is not offered
client changes a real commercial priority
```

Recompute only affected downstream truth while preserving history.

Measure separately from client SEO result:

```text
analyst/Work execution burden
provider request counts/cost
owner/operator actions
large-data handoffs
elapsed constraints
revision-sensitive stages
artifact-generation burden
```

This is Kwork productization economics, not the economics of the client website.

---

# STEP 22 — job close

Close only when:

```text
final deliverables complete
final QA passed or accepted exceptions recorded
revision test/real revision closed
no pending provider/Work/operator action
productization measurements recorded for a rehearsal
owner handoff complete
```

A job close does not automatically modify Level 1 or Level 2 methodology.

---

# Blood & Sand test-only gate — NOT A UNIVERSAL CLIENT STEP

After Step 20 final result is frozen, the Blood & Sand rehearsal may open its sealed previous research for a separate regression comparison.

This comparison belongs in that `work/<JOB_ID>/` only and must not alter the already frozen from-scratch result before the comparison is recorded.

It asks:

```text
what KW-002 independently reproduced
what it newly discovered
what it missed
where it disagreed and why
whether the product methodology requires owner-approved correction before sale
```
